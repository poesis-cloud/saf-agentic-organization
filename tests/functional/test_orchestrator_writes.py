"""Orchestrators commit only the artifact kinds the access-control list grants them.

The harness authorizes every write by the actor's ACL privileges (function 8) and accepts it only
inside a resolved step session (functions 9 and 10). So an orchestrator never flips an Epic,
Feature or Story `status:` itself: each change after creation is one `*-transition` workflow run
whose owner step commits it. These tests keep the org prose and catalogue in line with that.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tests.conftest import ORG_ROOT

ORCHESTRATORS = ("value-management-officer", "release-train-engineer", "scrum-master")
TIER_SKILLS = {"value-management-officer": "lpm", "release-train-engineer": "art", "scrum-master": "scrum"}
ALIASES = {
    "value-management-officer": ("value-management-officer", "vmo"),
    "release-train-engineer": ("release-train-engineer", "rte"),
    "scrum-master": ("scrum-master", "sm"),
}
TRANSITIONS = {
    "epic-transition": ("value-management-officer", {"epic": "business-owner", "epic-enabler": "enterprise-architect"}),
    "feature-transition": (
        "release-train-engineer",
        {"feature": "product-manager", "feature-enabler": "system-architect"},
    ),
    "story-transition": ("scrum-master", {"story": "product-owner", "story-enabler": "system-architect"}),
}

WRITE_VERB = r"(?:writes?|commits?|flips?|creates?|seeds?|sets?|updates?|maintains?|renders?|appends?|rolls? up)"
NEGATION = re.compile(r"\b(?:never|not|no|don't|cannot|only by|holds no|without)\b", re.IGNORECASE)
# Kind nouns as they appear in prose; `None` marks files outside the workspace layout, never grantable.
KIND_NOUNS: tuple[tuple[str, str | None], ...] = (
    (r"enabler epic", "epic-enabler"),
    (r"enabler feature", "feature-enabler"),
    (r"enabler story", "story-enabler"),
    (r"`?status:`?", "status"),
    (r"`?cost[:.]", "status"),
    (r"lean business case", "lean-business-case"),
    (r"portfolio kanban", "portfolio-kanban"),
    (r"program kanban", "program-kanban"),
    (r"team kanban", "team-sync"),
    (r"pain points?", "pain-point"),
    (r"risks\.md", "risks"),
    (r"progress\.md", None),
    (r"\.gitkeep", None),
    (r"decision-inventory", None),
    (r"\bepics?\b", "epic"),
    (r"\bfeatures?\b", "feature"),
    (r"\bstor(?:y|ies)\b", "story"),
    (r"\badrs?\b", "adr"),
)
CLAUSE_SPLIT = re.compile(r"(?<=[.;!?])\s+|\n| — | \| |, then | and then ")


def _acl() -> dict:
    return yaml.safe_load((ORG_ROOT / "conf" / "access-control-list.conf.yaml").read_text(encoding="utf-8"))


def _grants() -> dict[str, set[tuple[str, str]]]:
    acl = _acl()
    roles = {role["slug"]: {(p["artifact"], p["action"]) for p in role["privileges"]} for role in acl["roles"]}
    return {actor["slug"]: set().union(*(roles[r] for r in actor["roles"])) for actor in acl["actors"]}


def _writable(actor: str) -> set[str]:
    return {kind for kind, action in _grants()[actor] if action in {"create", "update"}}


def _workflows() -> dict[str, dict]:
    workflows = {}
    for path in sorted((ORG_ROOT / "workflows").glob("**/*.workflow.conf.yaml")):
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        workflows[workflow["slug"]] = workflow
    return workflows


def _body(path: Path) -> str:
    return re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def _sources(orchestrator: str) -> list[tuple[Path, bool]]:
    """Return (file, whether second person / facilitator means this orchestrator)."""
    own = [ORG_ROOT / "skills" / f"{orchestrator}.skill.md", ORG_ROOT / "skills" / f"{TIER_SKILLS[orchestrator]}.skill.md"]
    own += [ORG_ROOT / "agents" / f"{orchestrator}.agent.md"]
    own += sorted((ORG_ROOT / "instructions" / orchestrator).glob("*.instructions.md"))
    tier = {"value-management-officer": "portfolio", "release-train-engineer": "program", "scrum-master": "team"}
    own += sorted((ORG_ROOT / "skills").glob(f"{tier[orchestrator]}-*.skill.md"))
    others = [
        path
        for path in sorted((ORG_ROOT / "skills").glob("*.skill.md")) + sorted((ORG_ROOT / "agents").glob("*.agent.md"))
        if path not in own
    ]
    return [(path, True) for path in own] + [(path, False) for path in others]


def _subject(orchestrator: str, implicit: bool) -> re.Pattern[str]:
    names = "|".join(re.escape(alias) for alias in ALIASES[orchestrator])
    implicit_names = r"|\byou\b|the facilitator|the orchestrator" if implicit else ""
    return re.compile(rf"(?:@?\b(?:{names})\b{implicit_names})", re.IGNORECASE)


def _claimed_writes(orchestrator: str) -> list[tuple[str, str, str]]:
    claims = []
    writable = _writable(orchestrator)
    for path, implicit in _sources(orchestrator):
        subject = _subject(orchestrator, implicit)
        for clause in CLAUSE_SPLIT.split(_body(path)):
            for match in subject.finditer(clause):
                rest = clause[match.end() :]
                verb = re.match(rf"[`*]*\s*(?:(?:then|also|only|itself|alone)\s+)?{WRITE_VERB}\b", rest, re.IGNORECASE)
                if not verb or NEGATION.search(clause[: match.end() + verb.end()]):
                    continue
                obj = rest[verb.end() :]
                hits = [(found.start(), noun, kind) for noun, kind in KIND_NOUNS if (found := re.search(noun, obj, re.IGNORECASE))]
                if not hits:
                    continue
                start, noun, kind = min(hits, key=lambda hit: hit[0])
                if not NEGATION.search(obj[:start]) and (kind is None or kind not in writable):
                    claims.append((str(path.relative_to(ORG_ROOT)), kind or noun, clause.strip()))
    return claims


@pytest.mark.parametrize("orchestrator", ORCHESTRATORS)
def test_no_prose_has_an_orchestrator_commit_a_kind_it_is_not_granted(orchestrator: str) -> None:
    assert _claimed_writes(orchestrator) == []


@pytest.mark.parametrize("orchestrator", ORCHESTRATORS)
def test_orchestrators_hold_no_backlog_unit_privilege(orchestrator: str) -> None:
    units = {"epic", "epic-enabler", "feature", "feature-enabler", "story", "story-enabler"}
    assert _writable(orchestrator) & units == set()


def test_every_step_actor_may_write_its_artifact() -> None:
    for slug, workflow in _workflows().items():
        for step in workflow["steps"]:
            assert {(step["artifact"], "create"), (step["artifact"], "update")} <= _grants()[step["actor"]], (
                slug,
                step["slug"],
            )


@pytest.mark.parametrize("slug", sorted(TRANSITIONS))
def test_transition_workflows_route_each_status_change_to_its_author(slug: str) -> None:
    orchestrator, authors = TRANSITIONS[slug]
    workflow = _workflows()[slug]
    assert workflow["orchestrator"] == orchestrator
    by_kind = {step["artifact"]: step["actor"] for step in workflow["steps"]}
    assert {kind: by_kind[kind] for kind in authors} == authors
    for step in workflow["steps"]:
        if step["actor"] == orchestrator:
            assert step["artifact"] in _writable(orchestrator), step["slug"]


def _committed_by_tables() -> list[tuple[Path, str]]:
    cells = []
    for path in sorted((ORG_ROOT / "skills").glob("*.skill.md")) + sorted((ORG_ROOT / "agents").glob("*.agent.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if "Committed by (governed step)" not in line:
                continue
            column = [cell.strip() for cell in line.strip().strip("|").split("|")].index("Committed by (governed step)")
            for row in lines[index + 2 :]:
                if not row.startswith("|"):
                    break
                cells.append((path, [cell.strip() for cell in row.strip().strip("|").split("|")][column]))
    return cells


def test_lifecycle_tables_name_existing_governed_steps() -> None:
    cells = _committed_by_tables()
    assert cells, "no lifecycle table found"
    workflows = _workflows()
    for path, cell in cells:
        if cell.startswith("—"):
            continue
        refs = re.findall(r"`([a-z0-9-]+)(?:/([a-z0-9-]+))?`", cell)
        named = [(wf, step) for wf, step in refs if wf in workflows]
        assert named, (path.name, cell)
        for wf, step in named:
            if step:
                assert step in {s["slug"] for s in workflows[wf]["steps"]}, (path.name, cell)
    assert not any(
        re.search(r"→\s*(?:vmo|rte|sm)\s+commits", path.read_text(encoding="utf-8"), re.IGNORECASE)
        for path in (ORG_ROOT / "skills").glob("*.skill.md")
    )
