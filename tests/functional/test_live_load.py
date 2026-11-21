"""Drive the sibling harness against this live organization tree."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import HARNESS_SRC, ORG_ROOT
from tests.loaders import ORCHESTRATOR_DUTIES, load_workflows
from tests.rig import LAYOUT_ENV, Rig, brief_paths, concrete, init_workspace

from application import Application
from config.config_loader import ConfigLoader
from errors import ConfigurationError
from utils.env_loader import EnvLoader
from utils.schema_validator import SchemaValidator
from utils.yaml_loader import YamlLoader

CONTRACTS = HARNESS_SRC.parent / "contracts"
LAYER_EVENTS = (
    ("portfolio-sync", "value-management-officer"),
    ("coordinate-and-deliver", "solution-train-engineer"),
    ("art-sync", "release-train-engineer"),
    ("team-sync", "scrum-master"),
)


@pytest.fixture()
def live_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    workspace = tmp_path / "workspace"
    init_workspace(workspace)
    monkeypatch.delenv("FRAMEWORK_DIR", raising=False)
    for key, value in LAYOUT_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("FRAMEWORK_WORKSPACE_DIR", str(workspace))
    return workspace


def _loader() -> ConfigLoader:
    return ConfigLoader(EnvLoader(), YamlLoader(), SchemaValidator.compile_contracts(sorted(CONTRACTS.rglob("*.schema.json"))))


def test_config_loader_accepts_this_checkout(live_env: Path) -> None:
    loader = _loader()
    layout = loader.load_framework_layout(ORG_ROOT)
    assert layout.framework_dir == ORG_ROOT and layout.workspace_dir == live_env
    loader.load_access_control_list(ORG_ROOT)
    loader.load_model_profiles(ORG_ROOT)
    loader.load_workspace_layout(ORG_ROOT)
    assert set(load_workflows()) == set(loader.load_workflow_catalog(ORG_ROOT).workflows)


def test_application_constructs(live_env: Path) -> None:
    """Fail-fast configuration validity: every CEL condition is typed against the artifact schemas here."""
    Application(ORG_ROOT)


def test_missing_layout_is_configuration_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("FRAMEWORK_DIR", "FRAMEWORK_WORKSPACE_DIR", *LAYOUT_ENV):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ConfigurationError) as failure:
        _loader().load_framework_layout(tmp_path)
    assert failure.value.code == "missing-layout-variable"


@pytest.mark.parametrize(("workflow", "orchestrator"), LAYER_EVENTS)
def test_each_layer_orchestrator_is_injected_its_duties_and_catalog(live_env: Path, workflow: str, orchestrator: str) -> None:
    rig = Rig(live_env)
    session = rig.open(workflow)
    instructions = rig.invoke("resolve-workflow-instructions", sessionId=session)["instructions"]
    assert instructions == [*ORCHESTRATOR_DUTIES, f"{orchestrator}-catalog"]
    assert not rig.invoke("resolve-workflow-skills", sessionId=session).get("skills")
    step = rig.next_step(session, workflow, "record")
    assert step["actor"] == orchestrator
    worker = f"{orchestrator}-worker"
    rig.invoke("start-session", sessionId=worker, parentSessionId=session, agent=orchestrator)
    record = concrete(brief_paths(workflow)["main"])
    authorized = rig.invoke("check-step-authorization", sessionId=worker, artifactPath=record, action="create")
    assert authorized["outcome"]["status"] == "allowed" and authorized["authorization"]["resource"] == "event-record"


def test_a_worker_is_injected_the_contract_its_pattern_the_brief_and_its_craft_skill(live_env: Path) -> None:
    rig = Rig(live_env)
    session = rig.open("feature-refinement")
    step = rig.next_step(session, "feature-refinement", "draft")
    assert (step["actor"], step["skills"], step["artifact"]) == ("product-manager", ["product-manager"], "feature")
    rig.invoke("start-session", sessionId="pm", parentSessionId=session, agent="product-manager")
    assert rig.invoke("resolve-step-instructions", sessionId="pm", parentSessionId=session)["instructions"] == ["step-contract", "draft-main", "feature-refinement-brief"]
    assert rig.invoke("resolve-step-skills", sessionId="pm", parentSessionId=session)["skills"] == ["product-manager"]


def test_an_expert_may_write_its_packet_but_never_the_artifact_it_challenges(live_env: Path) -> None:
    rig = Rig(live_env)
    session = rig.open("feature-refinement")
    step = rig.next_step(session, "feature-refinement", "draft")
    feature = concrete(brief_paths("feature-refinement")["main"])
    assert rig.deliver(session, step, feature, "art/feature")["outcome"]["status"] == "pass"
    rig.next_step(session, "feature-refinement", "challenge-system-architect")
    assert rig.preconditions(session)["outcome"]["status"] == "pass"
    for index, expert in enumerate(("system-architect",)):
        rig.invoke("start-session", sessionId=f"expert-{index}", parentSessionId=session, agent=expert)
        packet = concrete(brief_paths("feature-refinement")["packets"].replace("<your-agent-slug>", expert))
        assert rig.invoke("check-step-authorization", sessionId=f"expert-{index}", artifactPath=packet, action="create")["outcome"]["status"] == "allowed"


def test_an_orchestrator_cannot_write_a_backlog_item(live_env: Path) -> None:
    rig = Rig(live_env)
    session = rig.open("art-sync")
    rig.next_step(session, "art-sync", "record")
    rig.invoke("start-session", sessionId="rte", parentSessionId=session, agent="release-train-engineer")
    feature = concrete(brief_paths("feature-refinement")["main"])
    denied = rig.invoke("check-step-authorization", sessionId="rte", artifactPath=feature, action="create")
    assert denied["outcome"]["status"] == "denied"
