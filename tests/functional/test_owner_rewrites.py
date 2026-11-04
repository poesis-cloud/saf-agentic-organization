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
