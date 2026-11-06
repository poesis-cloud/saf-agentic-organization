"""Every CEL state condition the organization declares, run through the real harness.

The condition language (core spec, function 5, invariant 2) reads `workspace` (artifact
instances: `kind`, `path`, `data`), `workflows` and `steps` (instances from the session logs),
the current `workflow` and `step`, and `selected` in `setPredicate`. Every `a.data` read must
sit behind a guard fixing its kind, which the harness `ConfigLoader` checks at load.

For each declared condition this suite builds a temporary Git workspace from the organization
layout, commits schema-valid fixture artifacts filled from the organization templates, and
drives the harness's real command entry points over it: the orchestrator session resolves the
workflow's steps (function 3), each earlier step instance runs in its own worker session and
delivers its artifact (functions 0, 8, 9, 10), so the session logs every condition reads are the
ones the harness writes. The evaluated step then runs function 5 (preconditions, on the
workspace branch) or function 10 (postconditions, on the step state before promotion). Each
condition has variants that must pass and variants that must fail; a condition added without
both fails the suite.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Iterator, Mapping

import pytest
import yaml

from tests.conftest import HARNESS_SRC, ORG_ROOT
from tests.functional.test_artifact_templates import LAYOUT_KEYS, NODES, PLACEHOLDER, _filled, _Filler, _schema, artifact_block

from application import Application
from config import StateCondition
from config.config_loader import ConfigLoader
from errors import ConfigurationError
from utils.env_loader import EnvLoader
from utils.schema_validator import SchemaValidator
from utils.yaml_loader import YamlLoader

CONTRACTS = HARNESS_SRC.parent / "contracts"
FLAGS = {
    "sessionId": "--session-id",
    "parentSessionId": "--parent-session-id",
    "agent": "--agent",
    "workflowSlug": "--workflow-slug",
    "artifactPath": "--artifact-path",
    "action": "--action",
}
APPROVED = ("portfolio-backlog", "implementing")

Fixture = tuple[str, str, Mapping[str, Any]]  # (kind, unit folder, frontmatter overrides)


@dataclass(frozen=True)
class Case:
    """One run: the committed workspace, then one delivery per step up to the evaluated one.

    For a precondition the deliveries are the evaluated step's predecessors; for a
    postcondition the last delivery is the evaluated step's own.
    """

    expected: str
    workspace: tuple[Fixture, ...]
    deliveries: tuple[Fixture, ...]


def _item(item_id: str, status: str) -> dict[str, Any]:
    return {"id": item_id, "kind": "clarification", "raised_by": "enterprise-architect", "owner": "business-owner", "blocking": True, "status": status}


def _closure(kind: str, unit: str, item: str) -> dict[str, str]:
    return {"artifact": kind, "unit": unit, "item": item, "resolution": "settled by the Vision's runway"}


def _epic(kind: str, unit: str, status: str = "analyzing", items: tuple[dict, ...] = ()) -> Fixture:
    return (kind, f"e-{unit[2:]}", {"id": unit, "status": status, "openItems": list(items)})


def _vision(*closed: dict[str, str]) -> Fixture:
    return ("architecture-vision", "core", {"closedItems": list(closed)})


def _feature(parent: str | None) -> Fixture:
    return ("feature", "f-1", {"parentEpic": parent})


def _epic_gate_cases() -> list[Case]:
    """Portfolio-wide by design: some business Epic is past the ★ Epic Gate."""
    return [
        Case("pass", (_epic("epic", "E-1"), _epic("epic", "E-2", "portfolio-backlog")), ()),
        Case("pass", (_epic("epic", "E-1", "implementing"),), ()),
        Case("fail", (), ()),
        # Approved Enabler Epics do not count: the guard fixes the kind to `epic`.
        Case(
            "fail",
            (_epic("epic", "E-1"), _epic("epic", "E-2", "reviewing"), _epic("epic-enabler", "E-1", "portfolio-backlog")),
            (),
        ),
    ]


def _parent_epic_cases() -> list[Case]:
    """The delivered Feature's own parent Epic is approved; a standalone Feature passes."""
    epics = (_epic("epic", "E-1"), _epic("epic", "E-2", "portfolio-backlog"), _epic("epic-enabler", "E-3", "implementing"))
    return [
        Case("pass", epics, (_feature("E-2"),)),
        Case("pass", epics, (_feature(None),)),
        # E-2 is approved, but this Feature derives from E-1: a portfolio-wide check would pass.
        Case("fail", epics, (_feature("E-1"),)),
        Case("fail", epics, (_feature("E-9"),)),
        # E-3 names only an approved Enabler Epic, not a business Epic.
        Case("fail", epics, (_feature("E-3"),)),
    ]


def _vision_closure_cases(kind: str) -> list[Case]:
    """The Vision closes FR4 on E-1 and E-2 of `kind` (and of the other kind on E-2).

    Only the Epic the evaluated step delivers decides: E-1, the bystander, keeps FR4 `open`
    in the passing variant, which the former portfolio-wide precondition refused.
    """
    other = "epic-enabler" if kind == "epic" else "epic"
    vision = _vision(_closure(kind, "E-1", "FR4"), _closure(kind, "E-2", "FR4"), _closure(kind, "E-2", "FR3"), _closure(other, "E-2", "FR5"))
    workspace = (
        vision,
        _epic("epic", "E-1", items=(_item("FR4", "open"),)),
        _epic("epic", "E-2", items=(_item("FR4", "open"),)),
        _epic("epic-enabler", "E-1", items=(_item("FR4", "open"),)),
        _epic("epic-enabler", "E-2", items=(_item("FR4", "open"),)),
    )
    sibling = _epic(other, "E-2", "portfolio-backlog", (_item("FR4", "open"),))

    def delivered(*items: dict) -> Fixture:
        return _epic(kind, "E-2", "portfolio-backlog", items)

    def run(subject: Fixture) -> tuple[Fixture, ...]:
        return (subject,) if kind == "epic" else (sibling, subject)

    return [
        Case("pass", workspace, run(delivered(_item("FR3", "withdrawn"), _item("FR4", "resolved"), _item("FR5", "open")))),
        Case("pass", workspace, run(delivered(_item("FR6", "open")))),
        Case("fail", workspace, run(delivered(_item("FR3", "resolved"), _item("FR4", "open")))),
        Case("fail", workspace, run(delivered(_item("FR3", "open"), _item("FR4", "resolved")))),
    ]


CASES: dict[tuple[str, str, str], list[Case]] = {
    ("feature-derivation", "derive-business", "an-approved-epic-exists"): _epic_gate_cases(),
    ("feature-derivation", "derive-business", "parent-epic-approved"): _parent_epic_cases(),
    ("epic-transition", "transition-epic", "no-epic-item-open-that-the-vision-closes"): _vision_closure_cases("epic"),
    ("epic-transition", "transition-enabler", "no-enabler-epic-item-open-that-the-vision-closes"): _vision_closure_cases("epic-enabler"),
}
PARAMETERS = [(key, index, case) for key, cases in sorted(CASES.items()) for index, case in enumerate(cases)]


def _loader() -> ConfigLoader:
    return ConfigLoader(EnvLoader(), YamlLoader(), SchemaValidator.compile_contracts(sorted(CONTRACTS.rglob("*.schema.json"))))


@pytest.fixture(scope="module")
def catalog(tmp_path_factory: pytest.TempPathFactory):
    with pytest.MonkeyPatch.context() as patch:
        for key, value in LAYOUT_KEYS.items():
            patch.setenv(key, value)
        patch.setenv("FRAMEWORK_WORKSPACE_DIR", str(tmp_path_factory.mktemp("unused-workspace")))
        return _loader().load_workflow_catalog(ORG_ROOT)


@pytest.fixture(scope="module")
def registry() -> SchemaValidator:
    return SchemaValidator.compile_contracts(
        [*sorted(CONTRACTS.rglob("*.schema.json")), *sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json"))]
    )


def _declared(catalog) -> dict[tuple[str, str, str], StateCondition]:
    return {
        (workflow.slug, step.slug, condition.slug): condition
        for workflow in catalog.workflows.values()
        for step in workflow.steps
        for condition in step.conditions
        if isinstance(condition, StateCondition)
    }


def _git(workspace: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True, text=True).stdout.strip()


def _artifact(registry: SchemaValidator, kind: str, unit: str, overrides: Mapping[str, Any]) -> tuple[str, str]:
    """Fill the kind's template the way an actor does, apply the overrides, place it in its folder."""
    path, _, template = next(node for node in NODES if node[1] == kind)
    data, body = _filled(artifact_block(template, Path(path).suffix), Path(path).suffix)
    data = _Filler(registry, _schema(kind)).fill_root(data)
    data = {**copy.deepcopy(data), "slug": f"{unit}-{kind}", **overrides}
    return PLACEHOLDER.sub(unit, path), "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body


class Rig:
    """The organization's harness over one fixture workspace, driven as a host drives it."""

    def __init__(self, workspace: Path, registry: SchemaValidator) -> None:
        self.workspace = workspace
        self._registry = registry
        self._application: Application | None = None
        self._sessions = 0

    def commit(self, fixtures: tuple[Fixture, ...]) -> None:
        for kind, unit, overrides in fixtures:
            self._write(kind, unit, overrides)
        _git(self.workspace, "add", "-A")
        _git(self.workspace, "commit", "-q", "--allow-empty", "-m", "fixtures")

    def invoke(self, function: str, *, ok: bool = True, **flags: Any) -> dict[str, Any]:
        if self._application is None:
            self._application = Application(ORG_ROOT)
        argv = [function]
        for key, value in flags.items():
            for item in value if isinstance(value, (list, tuple)) else (value,):
                argv.extend((FLAGS.get(key, "--artifact-path"), str(item)))
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self._application.dispatch_command(argv)
        if ok:
            assert code == 0, err.getvalue() or out.getvalue()
        return json.loads(out.getvalue())

    def open(self, workflow) -> str:
        self._sessions += 1
        orchestrator = f"orchestrator-{self._sessions}"
        started = self.invoke("start-session", sessionId=orchestrator, agent=workflow.facilitator)
        assert started["outcome"]["status"] == "started", started
        return orchestrator

    def resolve(self, orchestrator: str, workflow, step_slug: str) -> dict[str, Any]:
        resolved = self.invoke("resolve-step", sessionId=orchestrator, workflowSlug=workflow.slug)
        assert resolved["outcome"]["status"] == "step-resolution", resolved
        assert resolved["step"]["slug"] == step_slug, resolved
        return resolved["step"]

    def deliver(self, orchestrator: str, step: Mapping[str, Any], fixture: Fixture) -> dict[str, Any]:
        """Run one step instance in its own worker session through function 10."""
        gate = self.invoke("check-step-preconditions", sessionId=orchestrator)
        assert gate["outcome"]["status"] == "pass", gate
        self._sessions += 1
        worker = f"{step['actor']}-{self._sessions}"
        started = self.invoke("start-session", sessionId=worker, parentSessionId=orchestrator, agent=step["actor"])
        assert started["outcome"]["status"] == "started", started
        kind, unit, overrides = fixture
        assert kind == step["artifact"], (kind, step)
        path = self._path(kind, unit)
        action = "update" if (self.workspace / path).exists() else "create"
        authorized = self.invoke("check-step-authorization", sessionId=worker, artifactPath=path, action=action)
        assert authorized["outcome"]["status"] == "allowed", authorized
        self._write(kind, unit, overrides)
        checked = self.invoke("check-step-artifact", sessionId=worker, artifactPaths=[path])
        assert checked["outcome"]["status"] == "valid", checked
        return self.invoke("check-step-postconditions", sessionId=orchestrator)

    def head(self) -> str:
        return _git(self.workspace, "rev-parse", "HEAD")

    def _path(self, kind: str, unit: str) -> str:
        return _artifact(self._registry, kind, unit, {})[0]

    def _write(self, kind: str, unit: str, overrides: Mapping[str, Any]) -> None:
        path, text = _artifact(self._registry, kind, unit, overrides)
        target = self.workspace / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


@pytest.fixture()
def rig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, registry: SchemaValidator) -> Iterator[Rig]:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _git(workspace, "init", "-q")
    _git(workspace, "config", "user.email", "tests@poesis.cloud")
    _git(workspace, "config", "user.name", "organization-tests")
    _git(workspace, "commit", "-q", "--allow-empty", "-m", "init")
    for key, value in LAYOUT_KEYS.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("FRAMEWORK_DIR", raising=False)
    monkeypatch.setenv("FRAMEWORK_WORKSPACE_DIR", str(workspace))
    yield Rig(workspace, registry)


def _check(report: Mapping[str, Any], slug: str) -> str:
    (outcome,) = [check["outcome"] for check in report["conditionChecks"] if check["condition"]["slug"] == slug]
    return outcome


def test_every_state_condition_has_a_passing_and_a_failing_case(catalog) -> None:
    assert sorted(_declared(catalog)) == sorted(CASES)
    for key, cases in CASES.items():
        assert {case.expected for case in cases} == {"pass", "fail"}, key


@pytest.mark.parametrize(
    ("key", "index", "case"), PARAMETERS, ids=[f"{key[0]}/{key[1]}/{key[2]}-{index}-{case.expected}" for key, index, case in PARAMETERS]
)
def test_state_condition_outcome(catalog, rig: Rig, key: tuple[str, str, str], index: int, case: Case) -> None:
    workflow_slug, step_slug, condition_slug = key
    workflow = catalog.find_workflow(workflow_slug)
    condition = _declared(catalog)[key]
    steps = [step.slug for step in workflow.steps]
    evaluated = steps.index(step_slug)
    is_postcondition = condition.kind == "postcondition"
    assert len(case.deliveries) == evaluated + (1 if is_postcondition else 0), "one delivery per step up to the evaluated one"

    rig.commit(case.workspace)
    orchestrator = rig.open(workflow)
    for slug, fixture in zip(steps[:evaluated], case.deliveries):
        concluded = rig.deliver(orchestrator, rig.resolve(orchestrator, workflow, slug), fixture)
        assert concluded["outcome"]["status"] == "pass", concluded
    step = rig.resolve(orchestrator, workflow, step_slug)

    if not is_postcondition:
        report = rig.invoke("check-step-preconditions", sessionId=orchestrator)
        assert _check(report, condition_slug) == case.expected
        assert report["outcome"]["status"] == case.expected
        return

    before = rig.head()
    report = rig.deliver(orchestrator, step, case.deliveries[-1])
    assert report["artifactDelivery"]["outcome"] == "pass", report
    assert _check(report, condition_slug) == case.expected
    assert report["outcome"]["status"] == case.expected
    # Postconditions run on the step state before promotion: a failing one accepts nothing.
    assert report["promotion"]["outcome"] == ("promoted" if case.expected == "pass" else "withheld")
    assert (rig.head() == before) is (case.expected == "fail")


def _organization_copy(tmp_path: Path) -> Path:
    root = tmp_path / "organization"
    for name in ("agents", "artifacts", "conf", "instructions", "skills", "templates", "workflows"):
        shutil.copytree(ORG_ROOT / name, root / name)
    return root


@pytest.mark.parametrize(
    ("set_query", "code"),
    [
        ("artifacts['epic'].filter(e, e.status == 'implementing')", "unknown-condition-variable"),
        ("workspace.filter(e, e.data.status == 'implementing')", "unguarded-artifact-data"),
        ("workspace.filter(e, e.kind == 'epic' && e.data.parentEpic == 'E-1')", "undeclared-artifact-property"),
        ("workspace.filter(f, f.path == step.artifact.path)", "precondition-step-path-join"),
    ],
)
def test_config_loader_types_every_condition(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, set_query: str, code: str) -> None:
    """The harness under test checks the condition language's typing at load, so the suite runs
    against a harness that has it (saf-agentic-harness `main`, de1b5f0 or later)."""
    root = _organization_copy(tmp_path)
    path = root / "workflows" / "program" / "feature-derivation.workflow.conf.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    (gate,) = [condition for condition in data["steps"][0]["conditions"] if condition["slug"] == "an-approved-epic-exists"]
    gate["setSelector"]["setQuery"] = set_query
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    for key, value in LAYOUT_KEYS.items():
        monkeypatch.setenv(key, value)
    (tmp_path / "workspace").mkdir()
    monkeypatch.setenv("FRAMEWORK_WORKSPACE_DIR", str(tmp_path / "workspace"))
    with pytest.raises(ConfigurationError) as failure:
        _loader().load_workflow_catalog(root)
    assert failure.value.code == code
