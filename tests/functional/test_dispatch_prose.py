"""Orchestrator dispatch prose states the harness boundaries actors and sessions must respect.

Only the workflow's facilitator may ask `resolve-step` / `resolve-step-model` (the harness refuses
an actor with `not-facilitator`), actors work from the framework, never from the harness source,
and one orchestrator session drives one workflow instance (harness function 3, invariant 9), so
a finished instance answers `no-next-step` and the next run needs a new session.
"""

from __future__ import annotations

import pytest
import yaml

from tests.conftest import ORG_ROOT

ORCHESTRATORS = ("value-management-officer", "release-train-engineer", "scrum-master")
SKILL_RULES = (
    "**Every step dispatch also tells the actor (mandatory).** The actor **never calls the harness**",
    "no `resolve-step`, no `resolve-step-model`",
    "`not-facilitator`",
    "**never reads the harness source code or tests**",
    "**One orchestrator session drives one workflow instance** (harness function 3, invariant 9)",
    "`no-next-step`",
    "needs a **new orchestrator session**: when you return the mains, tell the user so",
    "`portfolio-sync` writes **one** product manifest per run",
    "**name the next workflow toward the gate**",
    "**and say that it runs in a new orchestrator session**",
    "only its first run is started, on assent: never improvise across instances",
)
AGENT_RULES = (
    "never calls the harness (`resolve-step` / `resolve-step-model`",
    "never reads the harness source or tests",
    "needs a new orchestrator session",
    "which workflow comes next toward the gate",
    "answer a \"drive to the gate\" request with that plan",
)


@pytest.mark.parametrize("slug", ORCHESTRATORS)
def test_orchestrator_skill_states_the_dispatch_boundaries(slug: str) -> None:
    text = (ORG_ROOT / "skills" / f"{slug}.skill.md").read_text(encoding="utf-8")
    assert [rule for rule in SKILL_RULES if rule not in text] == []


@pytest.mark.parametrize("slug", ORCHESTRATORS)
def test_orchestrator_agent_states_the_dispatch_boundaries(slug: str) -> None:
    text = (ORG_ROOT / "agents" / f"{slug}.agent.md").read_text(encoding="utf-8")
    assert [rule for rule in AGENT_RULES if rule not in text] == []


def test_plugin_host_binding_states_the_dispatch_boundaries() -> None:
    text = (ORG_ROOT / "builds" / "plugin" / "host-binding.md").read_text(encoding="utf-8")
    assert "**Actors never ask the harness.**" in text
    assert "`not-facilitator`" in text
    assert "never reads the harness source code or tests" in text
    assert "After `no-next-step` this session" in text
    assert "which workflow comes next toward the gate" in text


@pytest.mark.parametrize("slug", ORCHESTRATORS)
def test_orchestrator_names_the_next_run_and_answers_drive_to_gate_with_a_plan(slug: str) -> None:
    """Function 1 handling: a gate is several instances away, one orchestrator session each."""
    text = (ORG_ROOT / "instructions" / slug / f"{slug}-interpret-speech-acts.instructions.md").read_text(encoding="utf-8")
    for rule in (
        "**Return, and the next run.** At `no-next-step` this session is done",
        "say it runs in a **new** orchestrator session",
        "**Drive to a gate**",
        "answer it with the plan",
        "Never improvise across instances.",
        "One session per run." if slug != "value-management-officer" else "Seven runs, seven sessions.",
    ):
        assert rule in text


def test_no_orchestrator_prose_drives_autonomously_to_a_gate_across_instances() -> None:
    texts = [
        (ORG_ROOT / folder / f"{slug}.{kind}.md").read_text(encoding="utf-8")
        for slug in ORCHESTRATORS
        for folder, kind in (("skills", "skill"), ("agents", "agent"))
    ]
    assert not [text for text in texts if "until the next gate packet is ready" in text or "until the ★ Epic Gate packet is ready" in text]


def test_portfolio_sync_writes_one_product_manifest_per_run() -> None:
    workflow = yaml.safe_load(
        (ORG_ROOT / "workflows" / "portfolio" / "portfolio-sync.workflow.conf.yaml").read_text(encoding="utf-8")
    )
    assert [step["slug"] for step in workflow["steps"] if step["artifact"] == "product-manifest"] == [
        "update-product-manifest"
    ]

