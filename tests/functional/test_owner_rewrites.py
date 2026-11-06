"""Every main drafted before a challenge is revisited by its owner after the challenge.

A draft → challenge → owner-rewrite workflow can change one main in the rewrite; a sibling main
drafted before the challenge must then not be left contradicting it. So each drafted main has a
later owner step, committing the same artifact kind, that runs after every challenge step of the
workflow (one artifact per step; `no-change` when the main already holds).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tests.conftest import ORG_ROOT

WORKFLOWS = sorted((ORG_ROOT / "workflows").rglob("*.workflow.conf.yaml"))


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _ancestors(steps: dict[str, dict], slug: str) -> set[str]:
    seen: set[str] = set()
    stack = [c["step"] for c in steps[slug].get("conditions") or [] if c.get("kind") == "precondition"]
    while stack:
        current = stack.pop()
        if current not in seen:
            seen.add(current)
            stack.extend(c["step"] for c in steps[current].get("conditions") or [] if c.get("kind") == "precondition")
    return seen


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda path: path.name.split(".")[0])
def test_drafted_mains_are_revisited_after_the_challenge(path: Path) -> None:
    workflow = _load(path)
    steps = {step["slug"]: step for step in workflow["steps"]}
    challenges = {slug for slug, step in steps.items() if step["description"].startswith("Challenge packet")}
    if not challenges:
        return
    missing = []
    for slug, step in steps.items():
        if not step["description"].startswith("Main artifact draft"):
            continue
        revisited = [
            other
            for other, later in steps.items()
            if later["artifact"] == step["artifact"]
            and later["actor"] == step["actor"]
            and challenges <= _ancestors(steps, other)
        ]
        if not revisited:
            missing.append(f"{slug} ({step['artifact']})")
    assert missing == []


def test_epic_lean_business_case_aligns_epic_and_enabler_with_the_rewritten_case() -> None:
    steps = {
        step["slug"]: step
        for step in _load(ORG_ROOT / "workflows" / "portfolio" / "epic-lean-business-case.workflow.conf.yaml")["steps"]
    }
    for slug, actor, artifact in (
        ("update-epic", "business-owner", "epic"),
        ("update-enabler-epic", "enterprise-architect", "epic-enabler"),
    ):
        assert (steps[slug]["actor"], steps[slug]["artifact"]) == (actor, artifact)
        assert "owner-rewrite" in _ancestors(steps, slug)


def test_decisions_on_another_owners_artifact_are_written_back_by_that_owner() -> None:
    """The architecture packet decides about the Feature (ADR links, inventory, gate entries): the
    Feature owners write it back after the runway rewrite, one artifact per step."""
    steps = {
        step["slug"]: step
        for step in _load(ORG_ROOT / "workflows" / "program" / "architectural-runway-extension.workflow.conf.yaml")["steps"]
    }
    updates = (("update-feature", "product-manager", "feature"), ("update-feature-enabler", "system-architect", "feature-enabler"))
    for slug, actor, artifact in updates:
        assert (steps[slug]["actor"], steps[slug]["artifact"]) == (actor, artifact)
        assert "owner-rewrite" in _ancestors(steps, slug)
    assert list(steps)[-2:] == [slug for slug, _, _ in updates]


def test_a_vision_only_run_needs_no_epic() -> None:
    """Every step delivers exactly one instance of its artifact: architectural-vision writes the
    Vision and its reviews only, so a standalone Demand vision completes without any Epic."""
    workflow = _load(ORG_ROOT / "workflows" / "portfolio" / "architectural-vision.workflow.conf.yaml")
    assert {step["artifact"] for step in workflow["steps"]} == {"architecture-vision", "security-review", "operability-review"}


def test_epic_vision_alignment_writes_the_visions_decisions_into_one_epic_through_its_owners() -> None:
    workflow = _load(ORG_ROOT / "workflows" / "portfolio" / "epic-vision-alignment.workflow.conf.yaml")
    assert workflow["predecessors"] == ["architectural-vision"]
    steps = {step["slug"]: step for step in workflow["steps"]}
    assert [(slug, step["actor"], step["artifact"]) for slug, step in steps.items()] == [
        ("update-enabler-epic", "enterprise-architect", "epic-enabler"),
        ("update-epic", "business-owner", "epic"),
        ("reconcile-lean-business-case", "business-owner", "lean-business-case"),
    ]
    assert _ancestors(steps, "reconcile-lean-business-case") == {"update-epic", "update-enabler-epic"}


def test_alignment_flags_a_not_needed_enabler_that_the_vision_needs() -> None:
    text = (
        ORG_ROOT / "instructions" / "enterprise-architect" / "portfolio-epic-vision-alignment-update-enabler-epic.instructions.md"
    ).read_text(encoding="utf-8")
    assert "`status: not-needed`" in text and "blocking open item" in text
    assert "`epic-lean-business-case` must run again" in text


@pytest.mark.parametrize("instruction", ["product-manager/program-feature-transition-transition-business", "system-architect/program-feature-transition-transition-enabler"])
def test_feature_transitions_check_the_parent_epic_only_when_set(instruction: str) -> None:
    text = (ORG_ROOT / "instructions" / f"{instruction}.instructions.md").read_text(encoding="utf-8")
    assert "its parent Epic when `parentEpic` is set" in text
    assert "`parentEpic: null`" in text and "never refused for it" in text
