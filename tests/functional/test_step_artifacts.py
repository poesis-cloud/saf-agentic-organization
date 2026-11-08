"""No valid step without artifact: every step commits its declared artifact, whatever the outcome.

The harness enforces it with a built-in postcondition (the step's declared artifact must have an
instance committed by that step's session). This organization makes it satisfiable: every step
declares an artifact, every artifact carries a `stepOutcomes` record for the step's decision,
enablers can be committed as `not-needed`, and no prose tells an actor to answer only in its reply.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tests.conftest import ORG_ROOT
from tests.loaders import load_workflows

SCHEMAS = sorted((ORG_ROOT / "artifacts").glob("*/*.artifact.schema.json"))
TEMPLATES = sorted((ORG_ROOT / "templates").rglob("*.artifact-template.md"))
DEFINITION = json.loads((ORG_ROOT / "artifacts" / "framework-definitions.schema.json").read_text(encoding="utf-8"))[
    "definitions"
]["stepOutcomes"]
ENABLERS = ("epic-enabler", "feature-enabler", "story-enabler")
PROSE = sorted(
    [
        *(ORG_ROOT / "instructions").rglob("*.md"),
        *(ORG_ROOT / "skills").glob("*.md"),
        *(ORG_ROOT / "agents").glob("*.md"),
        *(ORG_ROOT / "workflows").rglob("*.yaml"),
        *(ORG_ROOT / "builds").rglob("*.md"),
        ORG_ROOT / "README.md",
    ]
)
REPLY_ONLY = (
    "explicit-none",
    "explicit no-change",
    "no-change note",
    "user-facing output only",
    "user-facing text only",
    "do not write or update any artifact",
)
ORCHESTRATORS = ("value-management-officer", "release-train-engineer", "scrum-master")
SPECIALISTS = (
    "business-owner",
    "enterprise-architect",
    "product-manager",
    "system-architect",
    "product-owner",
    "developer",
    "operator",
    "security-expert",
    "ux-designer",
    "quality-engineer",
    "tech-writer",
)
EVIDENCE_RULE = "**No valid step without artifact"
INDICATIVE = "indicative"


def _schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_every_workflow_step_declares_an_artifact() -> None:
    missing = [
        f"{slug}/{step['slug']}"
        for slug, workflow in load_workflows().items()
        for step in workflow["steps"]
        if not step.get("artifact")
    ]
    assert missing == []


@pytest.mark.parametrize("path", SCHEMAS, ids=lambda path: path.name)
def test_every_schema_records_step_outcomes(path: Path) -> None:
    schema = _schema(path)
    assert schema["properties"]["stepOutcomes"]["$ref"] == "#/$defs/stepOutcomes"
    assert schema["$defs"]["stepOutcomes"] == DEFINITION
    assert "stepOutcomes" not in schema.get("required", [])


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda path: path.name)
def test_every_template_frontmatter_starts_an_empty_step_outcome_record(path: Path) -> None:
    fences = re.findall(r"^```(markdown|json)\n(.*?)^```", path.read_text(encoding="utf-8"), re.S | re.M)
    assert fences, "template body must be fenced"
    assert re.search(r'^\s*"?stepOutcomes"?: \[\]', fences[0][1], re.M)


def test_step_outcome_definition_accepts_each_outcome_and_rejects_reply_only_shapes() -> None:
    validator = Draft202012Validator(DEFINITION)
    entry = {"step": "feature-backlog-refinement/draft-enabler", "date": "2026-11-05", "note": "No enabler needed."}
    for outcome in ("written", "revised", "confirmed", "no-change", "none"):
        assert list(validator.iter_errors([{**entry, "outcome": outcome}])) == []
    assert list(validator.iter_errors([{**entry, "outcome": "skipped"}]))
    assert list(validator.iter_errors([{**entry, "outcome": "none", "note": ""}]))
    assert list(validator.iter_errors([{**entry, "outcome": "none", "step": "draft-enabler"}]))


@pytest.mark.parametrize("kind", ENABLERS)
def test_enablers_can_be_committed_as_not_needed(kind: str) -> None:
    (schema_path,) = [path for path in SCHEMAS if path.name == f"{kind}.artifact.schema.json"]
    assert "not-needed" in _schema(schema_path)["properties"]["status"]["enum"]
    (template,) = [path for path in TEMPLATES if path.name == f"{kind}.artifact-template.md"]
    assert re.search(r"^status: .*# .*\| not-needed$", template.read_text(encoding="utf-8"), re.M)


@pytest.mark.parametrize("path", PROSE, ids=lambda path: str(path.relative_to(ORG_ROOT)))
def test_no_prose_settles_a_step_in_the_reply_only(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    assert [phrase for phrase in REPLY_ONLY if phrase in text] == []


@pytest.mark.parametrize("name", ORCHESTRATORS + SPECIALISTS)
def test_skills_state_that_artifacts_are_the_only_evidence(name: str) -> None:
    text = (ORG_ROOT / "skills" / f"{name}.skill.md").read_text(encoding="utf-8")
    assert EVIDENCE_RULE in text
    assert INDICATIVE in text
    assert "`stepOutcomes`" in text


def test_readme_and_plugin_binding_state_the_rule() -> None:
    readme = (ORG_ROOT / "README.md").read_text(encoding="utf-8")
    assert "No valid step" in readme and INDICATIVE in readme
    binding = (ORG_ROOT / "builds" / "plugin" / "host-binding.md").read_text(encoding="utf-8")
    assert "**Step evidence.**" in binding and INDICATIVE in binding
