"""Every CEL state condition the organization declares, run through the real harness.

The harness evaluates a `stateCondition` (`setSelector.setQuery` over `artifacts['<kind>']`, then
`setPredicate` over `selected`) against committed workspace state (function 5, invariant 2;
function 10, invariant 1). For each declared condition this suite builds a Git workspace from the
organization layout, commits schema-valid artifacts filled from the organization templates in a
variant that must pass and one that must fail, and evaluates the condition with the harness's own
`ArtifactStore` and `ConditionEvaluator`. A condition added without cases here fails the suite.
"""

from __future__ import annotations

import copy
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from tests.conftest import HARNESS_SRC, ORG_ROOT
from tests.functional.test_artifact_templates import LAYOUT_KEYS, NODES, PLACEHOLDER, _filled, _Filler, _schema, artifact_block

from application import _resolve_artifact_schemas
from config import StateCondition
from config.config_loader import ConfigLoader
from services.checking.condition_evaluator import ConditionEvaluator
from stores.artifact_store.artifact_store import ArtifactStore
from utils.env_loader import EnvLoader
from utils.schema_validator import SchemaValidator
from utils.yaml_loader import YamlLoader

CONTRACTS = HARNESS_SRC.parent / "contracts"


def _item(item_id: str, status: str) -> dict[str, Any]:
    return {"id": item_id, "kind": "clarification", "raised_by": "enterprise-architect", "owner": "business-owner", "blocking": True, "status": status}


def _closure(kind: str, unit: str, item: str) -> dict[str, str]:
    return {"artifact": kind, "unit": unit, "item": item, "resolution": "settled by the Vision's runway"}


# (kind, unit folder, frontmatter overrides) per artifact; one Vision per product.
def _epics(kind: str, statuses: dict[str, str], items: dict[str, list[dict]]) -> list[tuple[str, str, dict]]:
    return [(kind, f"e-{unit[2:]}", {"id": unit, "status": statuses.get(unit, "analyzing"), "openItems": items.get(unit, [])}) for unit in ("E-1", "E-2")]


def _vision(closed: list[dict]) -> tuple[str, str, dict]:
    return ("architecture-vision", "core", {"closedItems": closed})


def _closure_cases(kind: str, other: str) -> dict[str, list[tuple[str, str, dict]]]:
    """The Vision closes FR4 on `kind` E-2. E-1 (same item id) and `other` E-2 (same unit id) carry an
    open FR4 that the Vision does not close, so only `kind` E-2's own item decides the outcome."""
    vision = _vision([_closure(kind, "E-2", "FR4"), _closure(kind, "E-2", "FR3")])
    bystanders = {"E-1": [_item("FR4", "open")]}
    return {
        "pass": [
            vision,
            *_epics(kind, {}, {**bystanders, "E-2": [_item("FR3", "withdrawn"), _item("FR4", "resolved"), _item("FR5", "open")]}),
            *_epics(other, {}, {"E-2": [_item("FR4", "open")]}),
        ],
        "fail": [
            vision,
            *_epics(kind, {}, {**bystanders, "E-2": [_item("FR3", "resolved"), _item("FR4", "open"), _item("FR5", "open")]}),
            *_epics(other, {}, {"E-2": [_item("FR4", "resolved")]}),
        ],
    }


CASES: dict[tuple[str, str, str], dict[str, list[tuple[str, str, dict]]]] = {
    ("epic-transition", "transition-epic", "no-epic-item-open-that-the-vision-closes"): _closure_cases("epic", "epic-enabler"),
    ("epic-transition", "transition-epic", "no-enabler-epic-item-open-that-the-vision-closes"): _closure_cases("epic-enabler", "epic"),
    ("feature-derivation", "derive-business", "an-approved-epic-exists"): {
        "pass": _epics("epic", {"E-1": "analyzing", "E-2": "portfolio-backlog"}, {}),
        "fail": [
            *_epics("epic", {"E-1": "analyzing", "E-2": "reviewing"}, {}),
            *_epics("epic-enabler", {"E-1": "portfolio-backlog", "E-2": "implementing"}, {}),
        ],
    },
}


@pytest.fixture(scope="module")
def harness(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    with pytest.MonkeyPatch.context() as patch:
        for key, value in LAYOUT_KEYS.items():
            patch.setenv(key, value)
        patch.setenv("FRAMEWORK_WORKSPACE_DIR", str(tmp_path_factory.mktemp("unused-workspace")))
        validator = SchemaValidator.compile_contracts(sorted(CONTRACTS.rglob("*.schema.json")))
        loader = ConfigLoader(EnvLoader(), YamlLoader(), validator)
        layout = loader.load_framework_layout(ORG_ROOT)
        workspace_layout = loader.load_workspace_layout(ORG_ROOT)
        catalog = loader.load_workflow_catalog(ORG_ROOT)
        schemas = _resolve_artifact_schemas(layout, workspace_layout, catalog)
    registry = SchemaValidator.compile_contracts(
        [*sorted(CONTRACTS.rglob("*.schema.json")), *sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json"))]
    )
    return {"catalog": catalog, "schemas": schemas, "workspace_layout": workspace_layout, "registry": registry}


def _declared(catalog) -> dict[tuple[str, str, str], tuple[StateCondition, str]]:
    return {
        (workflow.slug, step.slug, condition.slug): (condition, step.artifact)
        for workflow in catalog.workflows.values()
        for step in workflow.steps
        for condition in step.conditions
        if isinstance(condition, StateCondition)
    }


def _git(workspace: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True)


def _artifact(registry: SchemaValidator, kind: str, unit: str, overrides: dict) -> tuple[str, str]:
    """Fill the kind's template the way an actor does, apply the overrides, place it in its folder."""
    path, _, template = next(node for node in NODES if node[1] == kind)
    data, body = _filled(artifact_block(template, Path(path).suffix), Path(path).suffix)
    data = _Filler(registry, _schema(kind)).fill_root(data)
    data = {**copy.deepcopy(data), "slug": f"{unit}-{kind}", **overrides}
    return PLACEHOLDER.sub(unit, path), "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body


def _evaluate(harness: dict[str, Any], tmp_path: Path, key: tuple[str, str, str], artifacts: list[tuple[str, str, dict]]) -> str:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _git(workspace, "init")
    _git(workspace, "config", "user.email", "tests@poesis.cloud")
    _git(workspace, "config", "user.name", "organization-tests")
    for kind, unit, overrides in artifacts:
        path, text = _artifact(harness["registry"], kind, unit, overrides)
        target = workspace / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    _git(workspace, "add", "-A")
    _git(workspace, "commit", "-m", "fixtures")
    store = ArtifactStore(workspace, harness["schemas"], harness["workspace_layout"])
    condition, step_artifact = _declared(harness["catalog"])[key]
    (check,) = ConditionEvaluator(store).evaluate_conditions((condition,), None, step_artifact)
    return check.outcome


def test_every_state_condition_has_a_passing_and_a_failing_case(harness: dict[str, Any]) -> None:
    assert sorted(_declared(harness["catalog"])) == sorted(CASES)


@pytest.mark.parametrize("variant", ["pass", "fail"])
@pytest.mark.parametrize("key", sorted(CASES), ids=lambda key: f"{key[0]}/{key[1]}/{key[2]}")
def test_state_condition_outcome(harness: dict[str, Any], tmp_path: Path, key: tuple[str, str, str], variant: str) -> None:
    assert _evaluate(harness, tmp_path, key, CASES[key][variant]) == variant
