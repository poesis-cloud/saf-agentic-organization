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
)
AGENT_RULES = (
    "never calls the harness (`resolve-step` / `resolve-step-model`",
    "never reads the harness source or tests",
    "needs a new orchestrator session",
)


@pytest.mark.parametrize("slug", ORCHESTRATORS)
def test_orchestrator_skill_states_the_dispatch_boundaries(slug: str) -> None:
    text = (ORG_ROOT / "skills" / f"{slug}.skill.md").read_text(encoding="utf-8")
    assert [rule for rule in SKILL_RULES if rule not in text] == []


@pytest.mark.parametrize("slug", ORCHESTRATORS)
def test_orchestrator_agent_states_the_dispatch_boundaries(slug: str) -> None:
    text = (ORG_ROOT / "agents" / f"{slug}.agent.md").read_text(encoding="utf-8")
    assert [rule for rule in AGENT_RULES if rule not in text] == []


def test_cli_host_binding_states_the_dispatch_boundaries() -> None:
    text = (ORG_ROOT / "builds" / "github-copilot-cli" / "host-binding.md").read_text(encoding="utf-8")
    assert "**Actors never ask the harness.**" in text
    assert "`not-facilitator`" in text
    assert "never reads the harness source code or tests" in text
    assert "After `no-next-step` this session" in text


def test_portfolio_sync_writes_one_product_manifest_per_run() -> None:
    workflow = yaml.safe_load(
        (ORG_ROOT / "workflows" / "portfolio" / "portfolio-sync.workflow.conf.yaml").read_text(encoding="utf-8")
    )
    assert [step["slug"] for step in workflow["steps"] if step["artifact"] == "product-manifest"] == [
        "update-product-manifest"
    ]

