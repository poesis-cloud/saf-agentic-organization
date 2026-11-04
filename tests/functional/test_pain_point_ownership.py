"""Pain points are written only by the role the access-control list authorizes, in a governed step.

The harness denies a `pain-point` write by any other actor, and every artifact write must happen
in a registered step session. So actors record friction in their step's `stepOutcomes` entry and
only the `release-train-engineer`, as the actor of the `improvement-backlog` workflow, writes
pain points, one per run.
"""

from __future__ import annotations

import pytest
import yaml

from tests.conftest import ORG_ROOT

ORCHESTRATORS = ("value-management-officer", "release-train-engineer", "scrum-master")
OWNER_RULE = "**Only `@release-train-engineer` writes pain points**"
OWNER_HANDOFF = "only `@release-train-engineer` writes the ART `improvement-backlog`"
FRICTION_NOTE = "`friction` note of your step's `stepOutcomes` entry"
SELF_WRITE = (
    "friction captured in the ART `improvement-backlog`",
    "capture workflow friction in the ART `improvement-backlog`",
    "append a pain point",
    "→ ART `improvement-backlog`",
)


def _acl() -> dict:
    return yaml.safe_load((ORG_ROOT / "conf" / "access-control-list.conf.yaml").read_text(encoding="utf-8"))


def _pain_point_writers() -> set[str]:
    acl = _acl()
    roles = {
        role["slug"]
        for role in acl["roles"]
        if any(p["artifact"] == "pain-point" and p["action"] == "create" for p in role["privileges"])
    }
    return {actor["slug"] for actor in acl["actors"] if roles & set(actor["roles"])}


def test_only_the_release_train_engineer_may_create_pain_points() -> None:
    assert _pain_point_writers() == {"release-train-engineer"}


@pytest.mark.parametrize("slug", [slug for slug in ORCHESTRATORS if slug != "release-train-engineer"])
def test_other_orchestrators_route_pain_points_to_the_owner(slug: str) -> None:
    text = (ORG_ROOT / "skills" / f"{slug}.skill.md").read_text(encoding="utf-8")
    assert OWNER_RULE in text


@pytest.mark.parametrize("slug", sorted({actor["slug"] for actor in _acl()["actors"]} - {"release-train-engineer"}))
def test_no_other_actor_writes_pain_points_itself(slug: str) -> None:
    for path in (ORG_ROOT / "skills" / f"{slug}.skill.md", ORG_ROOT / "agents" / f"{slug}.agent.md"):
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if "improvement-backlog" not in text:
            continue
        assert [phrase for phrase in SELF_WRITE if phrase in text] == [], path
        if "pain-point.md" in text:
            assert OWNER_HANDOFF in text, path


def _steps() -> list[tuple[str, dict]]:
    steps = []
    for path in sorted((ORG_ROOT / "workflows").glob("**/*.workflow.conf.yaml")):
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        steps += [(workflow["slug"], step) for step in workflow["steps"]]
    return steps


def test_pain_points_are_written_only_by_the_improvement_backlog_workflow() -> None:
    writers = {(workflow, step["slug"]) for workflow, step in _steps() if step["artifact"] == "pain-point"}
    assert writers == {("improvement-backlog", "record-pain-point")}
    workflow = yaml.safe_load(
        (ORG_ROOT / "workflows" / "program" / "improvement-backlog.workflow.conf.yaml").read_text(encoding="utf-8")
    )
    assert workflow["orchestrator"] == "release-train-engineer"
    assert {step["actor"] for step in workflow["steps"]} == {"release-train-engineer"}


def test_friction_is_recorded_in_the_step_outcome() -> None:
    schema = (ORG_ROOT / "artifacts" / "framework-definitions.schema.json").read_text(encoding="utf-8")
    assert '"friction"' in schema
    specialists = {actor["slug"] for actor in _acl()["actors"]} - set(ORCHESTRATORS)
    skills = [ORG_ROOT / "skills" / f"{slug}.skill.md" for slug in sorted(specialists)]
    handoffs = [path for path in skills if path.exists() and OWNER_HANDOFF in path.read_text(encoding="utf-8")]
    assert handoffs
    for path in handoffs:
        assert FRICTION_NOTE in path.read_text(encoding="utf-8"), path
