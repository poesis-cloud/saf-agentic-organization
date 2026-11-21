"""Every workflow of the catalog, run to its human gate through the real harness.

The happy path proves each workflow can actually be completed from its brief and templates: the
paths the brief gives are authorized, the filled templates are schema-valid, every condition
passes and the run ends on `no-next-step`. The refusals prove the organization's rules are
enforced by the harness, not by prose: no acceptance without challenge, no unanswered packet,
no item ready before it was challenged, no Epic approved without a go business case, no draft that
names another owner, no Story accepted while its code change is unmerged.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator, Mapping

import pytest

from tests.loaders import is_loop, layout_nodes, load_workflows
from tests.rig import LAYOUT_ENV, Rig, brief_paths, concrete, failed_conditions, init_workspace, outcome

CATALOG = load_workflows()
LOOPS = sorted(slug for slug, workflow in CATALOG.items() if is_loop(workflow))
TRANSITIONS = sorted(slug for slug, workflow in CATALOG.items() if workflow["steps"][0]["slug"] == "record-transition")
EVENTS = sorted(slug for slug, workflow in CATALOG.items() if workflow["steps"][0]["slug"] == "record")
GATES = sorted(slug for slug, workflow in CATALOG.items() if workflow["steps"][0]["slug"] == "record-decision")
TEMPLATES = {path: template for path, _, template in layout_nodes()}

EPIC = "portfolio/epics/<epic-slug>/<epic-slug>.epic.md"
EPIC_ENABLER = "portfolio/epics/<epic-slug>/<epic-slug>.epic-enabler.md"
CAPABILITY = "portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/<capability-slug>.capability.md"
CAPABILITY_ENABLER = CAPABILITY.replace(".capability.md", ".capability-enabler.md")
SUPPLIER = "portfolio/solution-trains/<solution-train-slug>/suppliers/<supplier-slug>/<supplier-slug>.supplier-agreement.md"
FEATURE = "portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature.md"
FEATURE_ENABLER = FEATURE.replace(".feature.md", ".feature-enabler.md")
ADR = "portfolio/arts/<art-slug>/adrs/<adr-slug>/<adr-slug>.adr.md"
RELEASE = "portfolio/arts/<art-slug>/releases/<release-slug>/<release-slug>.release.md"
STORY = "portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.story.md"
CODE_CHANGE = STORY.replace(".story.md", ".code-change.md")
LEDGER = [{"packet": "portfolio/challenges/x.challenge.md", "challenger": "agile-coach", "verdict": "pass", "responses": []}]


@pytest.fixture()
def rig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Rig]:
    workspace = tmp_path / "workspace"
    init_workspace(workspace)
    for key, value in LAYOUT_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("FRAMEWORK_DIR", raising=False)
    monkeypatch.setenv("FRAMEWORK_WORKSPACE_DIR", str(workspace))
    yield Rig(workspace)


def seed(rig: Rig, pattern: str, status: str, **extra: Any) -> str:
    """Commit one backlog item in the given state, under a slug named after that state."""
    key = pattern.rsplit("<", 1)[1].split(">")[0].replace("-", "_")
    return rig.seed(concrete(pattern, **{key: f"seeded-{status}"}), TEMPLATES[pattern], {"status": status, **extra})


def prerequisites(rig: Rig, workflow: str) -> dict[str, Any]:
    """Seed the state a workflow's first step requires; return the overrides its main needs."""
    if workflow == "lean-business-case":
        return {"epic": seed(rig, EPIC, "analyzing")}
    if workflow == "epic-enabler-lean-business-case":
        return {"epic": seed(rig, EPIC_ENABLER, "analyzing"), "owner": "enterprise-architect"}
    if workflow == "solution-train-pi-planning":
        seed(rig, CAPABILITY, "ready")
    if workflow == "pi-planning":
        seed(rig, FEATURE, "ready")
    if workflow == "release-on-demand":
        seed(rig, FEATURE, "implementing")
    if workflow == "iteration-planning":
        seed(rig, STORY, "ready")
    if workflow == "story-implementation":
        return {"story": seed(rig, STORY, "ready")}
    return {}


def main_of(rig: Rig, workflow: str) -> tuple[str, str]:
    """The concrete main path of a run and its template."""
    paths = brief_paths(workflow)
    if workflow == "epic-mvp-evaluation":
        return seed(rig, EPIC, "implementing"), TEMPLATES[EPIC]
    if workflow == "epic-enabler-mvp-evaluation":
        return seed(rig, EPIC_ENABLER, "implementing"), TEMPLATES[EPIC_ENABLER]
    return concrete(paths["main"]), TEMPLATES[paths["main"]]


def run_loop(rig: Rig, workflow: str, *, ledger: bool = True, target: str | None = None) -> tuple[str, Mapping[str, Any]]:
    """Draft, challenge and revise; return the main path and the revise step's report."""
    overrides = prerequisites(rig, workflow)
    main, template = main_of(rig, workflow)
    packets_pattern = brief_paths(workflow)["packets"]
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "draft")
    existing = rig.read(main) if (rig.workspace / main).exists() else {}
    drafted = {**existing, **overrides, "stepOutcomes": [*existing.get("stepOutcomes", []), outcome(f"{workflow}/draft", "written")]}
    report = rig.deliver(session, step, main, template, drafted)
    assert report["outcome"]["status"] == "pass", report
    packets = []
    for expert in [s["actor"] for s in CATALOG[workflow]["steps"][1:-1]]:
        step = rig.next_step(session, workflow, f"challenge-{expert}")
        packet = concrete(packets_pattern.replace("<your-agent-slug>", expert))
        report = rig.deliver(
            session, step, packet, "shared/challenge",
            {"target": target or main, "targetKind": CATALOG[workflow]["steps"][0]["artifact"], "challenger": expert,
             "verdict": "pass", "findings": [], "stepOutcomes": [outcome(f"{workflow}/{step['slug']}", "written")]},
        )
        if target is not None:
            return main, report
        assert report["outcome"]["status"] == "pass", report
        packets.append((packet, expert))
    step = rig.next_step(session, workflow, "revise")
    entries = [{"packet": packet, "challenger": expert, "verdict": "pass", "responses": []} for packet, expert in packets]
    revised = {**drafted, "challengeLedger": entries if ledger else entries[:-1],
               "stepOutcomes": [*drafted["stepOutcomes"], outcome(f"{workflow}/revise", "confirmed")]}
    report = rig.deliver(session, step, main, template, revised)
    if report["outcome"]["status"] == "pass":
        assert rig.resolve(session, workflow)["outcome"]["status"] == "no-next-step"
    return main, report


# --- the happy path of every workflow ---------------------------------------------------------


@pytest.mark.parametrize("workflow", LOOPS)
def test_a_loop_runs_from_draft_through_the_panel_to_the_human_gate(rig: Rig, workflow: str) -> None:
    main, report = run_loop(rig, workflow)
    assert report["outcome"]["status"] == "pass", report
    assert report["promotion"]["outcome"] == "promoted"
    committed = rig.read(main)
    assert len(committed["challengeLedger"]) == len(CATALOG[workflow]["steps"]) - 2
    assert [entry["step"] for entry in committed["stepOutcomes"]][-2:] == [f"{workflow}/draft", f"{workflow}/revise"]


@pytest.mark.parametrize("workflow", EVENTS)
def test_an_event_is_recorded_and_its_board_rendered(rig: Rig, workflow: str) -> None:
    paths = brief_paths(workflow)
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "record")
    record = concrete(paths["main"])
    report = rig.deliver(session, step, record, paths["mainTemplate"], {"stepOutcomes": [outcome(f"{workflow}/record", "written")]})
    assert report["outcome"]["status"] == "pass", report
    assert rig.read(record)["event"] == paths["mainTemplate"].split("/")[1]
    if "board" in paths:
        step = rig.next_step(session, workflow, "update-kanban")
        report = rig.deliver(session, step, concrete(paths["board"]), paths["boardTemplate"], {"stepOutcomes": [outcome(f"{workflow}/update-kanban", "written")]})
        assert report["outcome"]["status"] == "pass", report
    assert rig.resolve(session, workflow)["outcome"]["status"] == "no-next-step"


def _transition(rig: Rig, workflow: str, item: str, status: str, **fields: Any) -> Mapping[str, Any]:
    paths = brief_paths(workflow)
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "record-transition")
    before = rig.read(item)
    after = {**before, "status": status, **fields,
             "transitions": [*before["transitions"], {"from": before["status"], "to": status, "date": "2026-11-21", "decidedBy": "the human lead", "reason": "decided at the gate"}],
             "stepOutcomes": [*before["stepOutcomes"], outcome(f"{workflow}/record-transition", "revised")]}
    report = rig.deliver(session, step, item, TEMPLATES[paths["main"]], after)
    if report["outcome"]["status"] == "pass":
        if "board" in paths:
            step = rig.next_step(session, workflow, "update-kanban")
            board = rig.deliver(session, step, concrete(paths["board"]), paths["boardTemplate"], {"stepOutcomes": [outcome(f"{workflow}/update-kanban", "written")]})
            assert board["outcome"]["status"] == "pass", board
        assert rig.resolve(session, workflow)["outcome"]["status"] == "no-next-step"
    return report


FIRST_MOVES = {
    "epic-transition": (EPIC, "funnel", "reviewing"),
    "epic-enabler-transition": (EPIC_ENABLER, "funnel", "reviewing"),
    "capability-transition": (CAPABILITY, "analyzing", "ready"),
    "capability-enabler-transition": (CAPABILITY_ENABLER, "analyzing", "ready"),
    "supplier-agreement-transition": (SUPPLIER, "draft", "negotiating"),
    "feature-transition": (FEATURE, "analyzing", "ready"),
    "feature-enabler-transition": (FEATURE_ENABLER, "analyzing", "ready"),
    "adr-transition": (ADR, "proposed", "accepted"),
    "release-transition": (RELEASE, "ready", "released"),
    "story-transition": (STORY, "backlog", "ready"),
    "code-change-transition": (CODE_CHANGE, "ready-for-review", "approved"),
}


def test_every_transition_has_a_first_move() -> None:
    assert set(FIRST_MOVES) == set(TRANSITIONS)


@pytest.mark.parametrize("workflow", TRANSITIONS)
def test_a_challenged_item_moves_and_the_board_is_rendered(rig: Rig, workflow: str) -> None:
    pattern, start, target = FIRST_MOVES[workflow]
    item = seed(rig, pattern, start, challengeLedger=LEDGER)
    report = _transition(rig, workflow, item, target)
    assert report["outcome"]["status"] == "pass", report
    assert rig.read(item)["status"] == target


@pytest.mark.parametrize("workflow", TRANSITIONS)
def test_an_unchallenged_item_cannot_leave_refinement(rig: Rig, workflow: str) -> None:
    pattern, start, target = FIRST_MOVES[workflow]
    item = seed(rig, pattern, start)
    report = _transition(rig, workflow, item, target)
    assert report["outcome"]["status"] == "fail"
    assert failed_conditions(report) == [next(c["slug"] for c in CATALOG[workflow]["steps"][0]["conditions"] if "challenged" in c["slug"])]
    assert report["promotion"]["outcome"] == "withheld"


@pytest.mark.parametrize("workflow", TRANSITIONS)
def test_a_recorded_refusal_is_a_valid_transition_step(rig: Rig, workflow: str) -> None:
    pattern, start, _ = FIRST_MOVES[workflow]
    item = seed(rig, pattern, start)
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "record-transition")
    refused = {**rig.read(item), "stepOutcomes": [outcome(f"{workflow}/record-transition", "no-change")]}
    assert rig.deliver(session, step, item, TEMPLATES[pattern], refused)["outcome"]["status"] == "pass"


EPIC_TRANSITIONS = [("epic-transition", EPIC), ("epic-enabler-transition", EPIC_ENABLER)]


def _business_case(epic: str) -> str:
    return epic.rsplit(".", 2)[0] + ".lean-business-case.md"


@pytest.mark.parametrize(("workflow", "pattern"), EPIC_TRANSITIONS)
def test_an_epic_is_approved_only_with_a_go_business_case(rig: Rig, workflow: str, pattern: str) -> None:
    epic = seed(rig, pattern, "analyzing", challengeLedger=LEDGER)
    rig.seed(_business_case(epic), "portfolio/lean-business-case", {"epic": epic, "recommendation": "pending"})
    report = _transition(rig, workflow, epic, "ready")
    assert failed_conditions(report) == ["approved-epic-has-a-go-business-case"]


@pytest.mark.parametrize(("workflow", "pattern"), EPIC_TRANSITIONS)
def test_an_epic_with_a_go_business_case_becomes_ready(rig: Rig, workflow: str, pattern: str) -> None:
    epic = seed(rig, pattern, "analyzing", challengeLedger=LEDGER)
    rig.seed(_business_case(epic), "portfolio/lean-business-case", {"epic": epic, "recommendation": "go"})
    assert _transition(rig, workflow, epic, "ready")["outcome"]["status"] == "pass"


@pytest.mark.parametrize("change", ["approved", None])
def test_a_story_is_accepted_only_once_its_code_change_is_merged(rig: Rig, change: str | None) -> None:
    story = seed(rig, STORY, "in-review", challengeLedger=LEDGER)
    if change:
        rig.seed(story.replace(".story.md", ".code-change.md"), "team/code-change", {"story": story, "status": change})
    report = _transition(rig, "story-transition", story, "accepted")
    assert failed_conditions(report) == (["accepted-story-has-no-unmerged-change"] if change else [])  # a spike has no change


def test_a_story_with_a_merged_code_change_is_accepted(rig: Rig) -> None:
    story = seed(rig, STORY, "in-review", challengeLedger=LEDGER)
    rig.seed(story.replace(".story.md", ".code-change.md"), "team/code-change", {"story": story, "status": "merged"})
    assert _transition(rig, "story-transition", story, "accepted")["outcome"]["status"] == "pass"


# --- the human gate record --------------------------------------------------------------------


def _decide(rig: Rig, workflow: str, target: str, decision: str) -> Mapping[str, Any]:
    paths = brief_paths(workflow)
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "record-decision")
    return rig.deliver(session, step, concrete(paths["main"]), paths["mainTemplate"],
                       {"target": target, "decision": decision, "stepOutcomes": [outcome(f"{workflow}/record-decision", "written")]})


@pytest.mark.parametrize("workflow", GATES)
@pytest.mark.parametrize("decision", ["accepted", "accepted-with-concerns"])
def test_no_acceptance_without_challenge(rig: Rig, workflow: str, decision: str) -> None:
    target = rig.seed("portfolio/strategic-themes.md", "portfolio/strategic-themes")
    report = _decide(rig, workflow, target, decision)
    assert report["outcome"]["status"] == "fail" and failed_conditions(report) == ["accepted-only-if-challenged"]


@pytest.mark.parametrize("workflow", GATES)
def test_a_challenged_artifact_can_be_accepted_and_any_artifact_rejected(rig: Rig, workflow: str) -> None:
    target = rig.seed("portfolio/strategic-themes.md", "portfolio/strategic-themes")
    assert _decide(rig, workflow, target, "rejected")["outcome"]["status"] == "pass"
    rig.seed("portfolio/challenges/strategic-themes-data-analyst.challenge.md", "shared/challenge", {"target": target})
    assert _decide(rig, workflow, target, "accepted")["outcome"]["status"] == "pass"


# --- the challenge loop is enforced -----------------------------------------------------------


def test_a_packet_must_target_the_drafted_artifact(rig: Rig) -> None:
    _, report = run_loop(rig, "team-formation", target="portfolio/strategic-themes.md")
    assert report["outcome"]["status"] == "fail" and failed_conditions(report) == ["packet-targets-the-drafted-artifact"]


def test_the_owner_must_answer_every_packet(rig: Rig) -> None:
    _, report = run_loop(rig, "team-formation", ledger=False)
    assert report["outcome"]["status"] == "fail" and failed_conditions(report) == ["every-packet-is-answered"]
    assert report["promotion"]["outcome"] == "withheld"


def test_the_owner_must_revise_the_artifact_it_drafted(rig: Rig) -> None:
    workflow = "team-formation"
    session = rig.open(workflow)
    charter = concrete(brief_paths(workflow)["main"])
    step = rig.next_step(session, workflow, "draft")
    assert rig.deliver(session, step, charter, "team/team-charter", {"stepOutcomes": [outcome(f"{workflow}/draft", "written")]})["outcome"]["status"] == "pass"
    for expert in ("agile-coach", "product-owner", "quality-engineer"):
        step = rig.next_step(session, workflow, f"challenge-{expert}")
        packet = concrete(brief_paths(workflow)["packets"].replace("<your-agent-slug>", expert))
        assert rig.deliver(session, step, packet, "shared/challenge", {"target": charter})["outcome"]["status"] == "pass"
    step = rig.next_step(session, workflow, "revise")
    other = concrete(brief_paths(workflow)["main"], team_slug="another-team")
    report = rig.deliver(session, step, other, "team/team-charter", {})
    assert "revises-the-drafted-artifact" in failed_conditions(report)
    assert rig.next_step(session, workflow, "revise")["slug"] == "revise"  # the failed step comes back


# --- SAFe guards on the first step ------------------------------------------------------------

REFUSED_STARTS = {
    "lean-business-case": "an-epic-is-under-analysis",
    "epic-enabler-lean-business-case": "an-epic-enabler-is-under-analysis",
    "epic-mvp-evaluation": "an-epic-is-implementing",
    "epic-enabler-mvp-evaluation": "an-epic-enabler-is-implementing",
    "solution-train-pi-planning": "a-capability-is-ready",
    "pi-planning": "a-feature-is-ready",
    "release-on-demand": "a-feature-is-built",
    "iteration-planning": "a-story-is-ready",
    "story-implementation": "a-story-is-ready",
}


@pytest.mark.parametrize("workflow", sorted(REFUSED_STARTS))
def test_a_workflow_is_refused_while_its_input_state_is_missing(rig: Rig, workflow: str) -> None:
    session = rig.open(workflow)
    rig.next_step(session, workflow, "draft")
    gate = rig.preconditions(session)
    assert gate["outcome"]["status"] == "fail" and failed_conditions(gate) == [REFUSED_STARTS[workflow]]


@pytest.mark.parametrize(("workflow", "enabler"), [("pi-planning", FEATURE_ENABLER), ("solution-train-pi-planning", CAPABILITY_ENABLER)])
def test_planning_starts_when_only_an_enabler_is_ready(rig: Rig, workflow: str, enabler: str) -> None:
    seed(rig, enabler, "ready")
    session = rig.open(workflow)
    rig.next_step(session, workflow, "draft")
    assert rig.preconditions(session)["outcome"]["status"] == "pass"


def _draft(rig: Rig, workflow: str, overrides: Mapping[str, Any]) -> Mapping[str, Any]:
    main, template = main_of(rig, workflow)
    session = rig.open(workflow)
    step = rig.next_step(session, workflow, "draft")
    return rig.deliver(session, step, main, template, overrides)


PARENT_CASES = [
    ("capability-refinement", EPIC, "funnel", "parent-epic-is-approved"),
    ("capability-refinement", EPIC, "implementing", None),
    ("capability-refinement", EPIC_ENABLER, "ready", "parent-epic-is-approved"),  # business work never splits from an enabler
    ("capability-enabler-refinement", EPIC_ENABLER, "analyzing", "parent-is-approved"),
    ("capability-enabler-refinement", EPIC_ENABLER, "ready", None),
    ("capability-enabler-refinement", EPIC, "implementing", None),
    ("feature-refinement", EPIC, "analyzing", "parent-is-approved"),
    ("feature-refinement", EPIC, "ready", None),
    ("feature-refinement", CAPABILITY, "funnel", "parent-is-approved"),
    ("feature-refinement", CAPABILITY, "ready", None),
    ("feature-refinement", CAPABILITY_ENABLER, "ready", "parent-is-approved"),
    ("feature-enabler-refinement", CAPABILITY, "done", "parent-is-approved"),
    ("feature-enabler-refinement", EPIC, "implementing", None),
    ("feature-enabler-refinement", EPIC_ENABLER, "ready", None),
    ("feature-enabler-refinement", CAPABILITY_ENABLER, "analyzing", None),
    ("story-refinement", FEATURE, "analyzing", "parent-feature-is-approved"),
    ("story-refinement", FEATURE, "implementing", None),
    ("story-refinement", FEATURE_ENABLER, "ready", None),
]


@pytest.mark.parametrize(("workflow", "parent", "status", "refusal"), PARENT_CASES)
def test_an_item_splits_only_from_an_approved_parent(rig: Rig, workflow: str, parent: str, status: str, refusal: str | None) -> None:
    report = _draft(rig, workflow, {"parent": seed(rig, parent, status)})
    assert failed_conditions(report) == ([refusal] if refusal else []), report


@pytest.mark.parametrize("workflow", ["capability-refinement", "capability-enabler-refinement", "feature-refinement", "feature-enabler-refinement", "story-refinement"])
def test_an_item_from_the_local_context_needs_no_parent(rig: Rig, workflow: str) -> None:
    assert _draft(rig, workflow, {"parent": None})["outcome"]["status"] == "pass"


CASES = [
    ("lean-business-case", EPIC, EPIC, "epic-owner", "case-names-an-epic-under-analysis"),
    ("lean-business-case", EPIC, EPIC_ENABLER, "epic-owner", "case-names-an-epic-under-analysis"),
    ("epic-enabler-lean-business-case", EPIC_ENABLER, EPIC_ENABLER, "enterprise-architect", "case-names-an-epic-enabler-under-analysis"),
    ("epic-enabler-lean-business-case", EPIC_ENABLER, EPIC, "enterprise-architect", "case-names-an-epic-enabler-under-analysis"),
]


@pytest.mark.parametrize(("workflow", "analyzed", "named", "owner", "refusal"), CASES)
def test_a_business_case_must_name_an_epic_of_its_kind_under_analysis(rig: Rig, workflow: str, analyzed: str, named: str, owner: str, refusal: str) -> None:
    seed(rig, analyzed, "analyzing")
    status = "funnel" if named == analyzed else "analyzing"
    report = _draft(rig, workflow, {"epic": seed(rig, named, status), "owner": owner})
    assert failed_conditions(report) == [refusal]


@pytest.mark.parametrize(("workflow", "owner"), [("team-formation", "agile-coach"), ("epic-enabler-lean-business-case", "epic-owner")])
def test_the_draft_must_name_its_author_as_owner(rig: Rig, workflow: str, owner: str) -> None:
    overrides = {**prerequisites(rig, workflow), "owner": owner}
    assert failed_conditions(_draft(rig, workflow, overrides)) == ["owner-is-the-author"]


def test_a_code_change_must_implement_a_planned_story(rig: Rig) -> None:
    seed(rig, STORY, "ready")
    report = _draft(rig, "story-implementation", {"story": seed(rig, STORY, "backlog")})
    assert failed_conditions(report) == ["change-implements-a-planned-story"]


def test_every_declared_state_condition_has_a_refusal_test() -> None:
    declared = {c["slug"] for workflow in CATALOG.values() for step in workflow["steps"] for c in step["conditions"] if "setPredicate" in c}
    refused = {
        "packet-targets-the-drafted-artifact", "every-packet-is-answered", "revises-the-drafted-artifact",
        "accepted-only-if-challenged", "approved-epic-has-a-go-business-case", *(case[4] for case in CASES),
        "change-implements-a-planned-story", "owner-is-the-author", "accepted-story-has-no-unmerged-change",
        *REFUSED_STARTS.values(), *(case[3] for case in PARENT_CASES if case[3]),
        *(c["slug"] for slug in TRANSITIONS for c in CATALOG[slug]["steps"][0]["conditions"] if "challenged" in c["slug"]),
    }
    assert declared == refused
