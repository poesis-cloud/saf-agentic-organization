"""Drive the sibling harness against this live organization tree."""

from __future__ import annotations

import json
import os
import subprocess
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from tests.conftest import HARNESS_SRC, ORG_ROOT
from tests.loaders import load_workflows

from application import Application
from config.config_loader import ConfigLoader
from errors import ConfigurationError
from utils.env_loader import EnvLoader
from utils.schema_validator import SchemaValidator
from utils.yaml_loader import YamlLoader

CONTRACTS = HARNESS_SRC.parent / "contracts"

LAYOUT_KEYS = (
    "FRAMEWORK_DIR",
    "FRAMEWORK_AGENTS_DIR",
    "FRAMEWORK_ARTIFACTS_DIR",
    "FRAMEWORK_INSTRUCTIONS_DIR",
    "FRAMEWORK_SKILLS_DIR",
    "FRAMEWORK_TEMPLATES_DIR",
    "FRAMEWORK_WORKFLOWS_DIR",
    "FRAMEWORK_WORKSPACE_DIR",
)

LAYER_CASES = (
    (
        "portfolio-sync",
        "value-management-officer",
        "portfolio/sync/q1.portfolio-sync.md",
        "portfolio-sync",
    ),
    (
        "art-sync",
        "release-train-engineer",
        "portfolio/art/core/pi-1/art-sync.md",
        "art-sync",
    ),
    (
        "team-sync",
        "scrum-master",
        "portfolio/art/core/teams/alpha/daily/stand.team-sync.md",
        "team-sync",
    ),
)


def _init_git(workspace: Path) -> None:
    subprocess.run(["git", "init"], cwd=workspace, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "tests@poesis.cloud"], cwd=workspace, check=True)
    subprocess.run(["git", "config", "user.name", "organization-tests"], cwd=workspace, check=True)
    (workspace / ".gitkeep").write_text("", encoding="utf-8")
    subprocess.run(["git", "add", ".gitkeep"], cwd=workspace, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=workspace, check=True, capture_output=True)


@pytest.fixture()
def live_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _init_git(workspace)
    for key in LAYOUT_KEYS:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("FRAMEWORK_AGENTS_DIR", "agents")
    monkeypatch.setenv("FRAMEWORK_ARTIFACTS_DIR", "artifacts")
    monkeypatch.setenv("FRAMEWORK_INSTRUCTIONS_DIR", "instructions")
    monkeypatch.setenv("FRAMEWORK_SKILLS_DIR", "skills")
    monkeypatch.setenv("FRAMEWORK_TEMPLATES_DIR", "templates")
    monkeypatch.setenv("FRAMEWORK_WORKFLOWS_DIR", "workflows")
    monkeypatch.setenv("FRAMEWORK_WORKSPACE_DIR", str(workspace))
    return workspace


def _loader() -> ConfigLoader:
    validator = SchemaValidator.compile_contracts(sorted(CONTRACTS.rglob("*.schema.json")))
    return ConfigLoader(EnvLoader(), YamlLoader(), validator)


def _invoke(application: Application, function: str, **flags: str) -> dict[str, object]:
    argv = [function]
    mapping = {
        "sessionId": "--session-id",
        "parentSessionId": "--parent-session-id",
        "agent": "--agent",
        "workflowSlug": "--workflow-slug",
        "artifactPath": "--artifact-path",
        "action": "--action",
    }
    for key, value in flags.items():
        argv.extend((mapping[key], value))
    out, err = StringIO(), StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = application.dispatch_command(argv)
    assert code == 0, err.getvalue()
    return json.loads(out.getvalue())


def test_config_loader_accepts_this_checkout(live_env: Path) -> None:
    loader = _loader()
    layout = loader.load_framework_layout(ORG_ROOT)
    assert layout.framework_dir == ORG_ROOT
    assert layout.workspace_dir == live_env
    loader.load_access_control_list(ORG_ROOT)
    loader.load_model_profiles(ORG_ROOT)
    loader.load_workspace_layout(ORG_ROOT)
    catalog = loader.load_workflow_catalog(ORG_ROOT)
    assert set(load_workflows()) == set(catalog.workflows)


def test_application_constructs(live_env: Path) -> None:
    Application(ORG_ROOT)


def test_missing_layout_is_configuration_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for key in LAYOUT_KEYS:
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(ConfigurationError) as failure:
        _loader().load_framework_layout(tmp_path)
    assert failure.value.code == "missing-layout-variable"


@pytest.mark.parametrize("workflow_slug,agent,path,resource", LAYER_CASES)
def test_start_resolve_and_authorize_per_layer(
    live_env: Path, workflow_slug: str, agent: str, path: str, resource: str
) -> None:
    application = Application(ORG_ROOT)
    session_id = f"{workflow_slug}-session"
    started = _invoke(application, "start-session", sessionId=session_id, agent=agent)
    assert started["outcome"]["status"] == "started"
    resolved = _invoke(
        application, "resolve-step", sessionId=session_id, workflowSlug=workflow_slug
    )
    assert resolved["outcome"]["status"] == "step-resolution"
    assert resolved["step"]["actor"] == agent
    authorized = _invoke(
        application,
        "check-step-authorization",
        sessionId=session_id,
        artifactPath=path,
        action="create",
    )
    assert authorized["outcome"]["status"] == "allowed"
    assert authorized["authorization"]["resource"] == resource


def _commit_epic(workspace: Path, status: str) -> None:
    """Commit one schema-valid business Epic, filled from the organization template."""
    from tests.functional.test_state_conditions import _artifact

    registry = SchemaValidator.compile_contracts(
        [*sorted(CONTRACTS.rglob("*.schema.json")), *sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json"))]
    )
    path, text = _artifact(registry, "epic", "e-1", {"id": "E-1", "status": status, "openItems": []})
    target = workspace / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=workspace, check=True)
    subprocess.run(["git", "commit", "-m", "epic"], cwd=workspace, check=True, capture_output=True)


@pytest.mark.parametrize(("epic_status", "outcome"), [(None, "fail"), ("analyzing", "fail"), ("portfolio-backlog", "pass")])
def test_feature_derivation_is_refused_until_an_epic_is_approved(
    live_env: Path, epic_status: str | None, outcome: str
) -> None:
    """The CEL precondition runs at the real dispatch boundary: no Feature before the ★ Epic Gate."""
    if epic_status:
        _commit_epic(live_env, epic_status)
    application = Application(ORG_ROOT)
    _invoke(application, "start-session", sessionId="rte-session", agent="release-train-engineer")
    resolved = _invoke(application, "resolve-step", sessionId="rte-session", workflowSlug="feature-derivation")
    assert resolved["step"]["slug"] == "derive-business"
    checked = _invoke(application, "check-step-preconditions", sessionId="rte-session")
    assert checked["outcome"]["status"] == outcome
    assert [(check["condition"]["slug"], check["outcome"]) for check in checked["conditionChecks"]] == [
        ("an-approved-epic-exists", outcome)
    ]


def test_a_step_session_is_injected_its_actor_authoring_skill(live_env: Path) -> None:
    """Function 7 resolves the step's declared `skills:`: the actor's author skill, not dispatch prose."""
    application = Application(ORG_ROOT)
    _invoke(application, "start-session", sessionId="vmo-session", agent="value-management-officer")
    resolved = _invoke(application, "resolve-step", sessionId="vmo-session", workflowSlug="epic-lean-business-case")
    assert (resolved["step"]["actor"], resolved["step"]["skills"]) == ("business-owner", ["business-owner"])
    _invoke(application, "start-session", sessionId="bo-session", parentSessionId="vmo-session", agent="business-owner")
    skills = _invoke(application, "resolve-step-skills", sessionId="bo-session", parentSessionId="vmo-session")
    assert skills["skills"] == ["business-owner"]
