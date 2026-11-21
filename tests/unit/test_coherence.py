"""Live-tree coherence: the catalog, the roster, the access control list and the context budgets.

These tests state the organization's design rules:

- four SAFe layers, one orchestrator each;
- every workflow is one of four patterns (loop, transition, event, gate) with fixed step shapes;
- every main artifact kind is challenged by an expert panel before the human gate;
- every agent holds exactly the privileges its steps need;
- what the harness injects into a session stays small.
"""

from __future__ import annotations

import re
from collections import defaultdict

import pytest

from tests.loaders import (
    AGENT_SUFFIX,
    INSTRUCTION_SUFFIX,
    LAYERS,
    ORCHESTRATOR_DUTIES,
    SKILL_SUFFIX,
    agent_slugs,
    body_of,
    instruction_slugs,
    is_loop,
    iter_named,
    layout_nodes,
    load_acl,
    load_plugin,
    load_schemas,
    load_tools_map,
    load_workflows,
    organization_root,
    parse_frontmatter,
    schema_slugs,
    skill_slugs,
    slug_refs,
    template_slugs,
    word_count,
)

ORG = organization_root()
CATALOG = load_workflows()
SCHEMAS = load_schemas()
ORCHESTRATORS = {
    "portfolio": "value-management-officer",
    "solution": "solution-train-engineer",
    "art": "release-train-engineer",
    "team": "scrum-master",
}
PATTERNS = {
    "draft": "draft-main",
    "revise": "revise-main",
    "record-transition": "record-transition",
    "update-kanban": "update-kanban",
    "record": "record-event",
    "record-decision": "record-gate-decision",
}
COPYRIGHT = "Copyright 2026 Poesis Cloud"
AGENT_SECTIONS = ("Mission", "You own", "You never", "SAFe anchor")
MAX_STEPS = 8
MAX_PANEL = 6
MAX_INSTRUCTION_WORDS = 420
MAX_WORKER_CONTEXT_WORDS = 800
MAX_ORCHESTRATOR_CONTEXT_WORDS = 1600
MAX_AGENT_WORDS = 450
MAX_SKILL_WORDS = 1000


def _steps() -> list[tuple[str, dict, dict]]:
    return [(slug, workflow, step) for slug, workflow in CATALOG.items() for step in workflow["steps"]]


def _challenged_kinds() -> dict[str, set[str]]:
    """agent slug -> the artifact kinds it challenges."""
    seats: dict[str, set[str]] = defaultdict(set)
    for workflow in CATALOG.values():
        if is_loop(workflow):
            for step in workflow["steps"][1:-1]:
                seats[step["actor"]].add(workflow["steps"][0]["artifact"])
    return seats


def _authored_kinds() -> dict[str, set[str]]:
    """agent slug -> the main artifact kinds it drafts."""
    authored: dict[str, set[str]] = defaultdict(set)
    for workflow in CATALOG.values():
        if is_loop(workflow):
            authored[workflow["steps"][0]["actor"]].add(workflow["steps"][0]["artifact"])
    return authored


# --- layers and orchestrators -----------------------------------------------------------------


def test_the_four_safe_layers_each_have_one_orchestrator() -> None:
    by_layer: dict[str, set[str]] = defaultdict(set)
    for workflow in CATALOG.values():
        by_layer[workflow["layer"]].add(workflow["orchestrator"])
    assert {layer: next(iter(names)) for layer, names in by_layer.items() if len(names) == 1} == ORCHESTRATORS
    assert tuple(sorted(by_layer)) == tuple(sorted(LAYERS))


def test_every_workflow_and_step_has_a_description() -> None:
    for slug, workflow in CATALOG.items():
        assert str(workflow.get("description", "")).strip(), slug
        for step in workflow["steps"]:
            assert str(step.get("description", "")).strip(), f"{slug}/{step['slug']}"


def test_every_workflow_injects_the_orchestrator_duties_and_its_catalog() -> None:
    for slug, workflow in CATALOG.items():
        assert slug_refs(workflow["instructions"]) == (*ORCHESTRATOR_DUTIES, f"{workflow['orchestrator']}-catalog"), slug
        assert "skills" not in workflow, f"{slug}: the orchestrator's context is its duties and catalog, no skill"


def test_every_catalog_lists_exactly_the_workflows_of_its_orchestrator() -> None:
    for layer, orchestrator in ORCHESTRATORS.items():
        text = (ORG / "instructions" / layer / f"{orchestrator}-catalog{INSTRUCTION_SUFFIX}").read_text(encoding="utf-8")
        listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", text, re.MULTILINE))
        assert listed == {slug for slug, workflow in CATALOG.items() if workflow["orchestrator"] == orchestrator}, layer
        for other in set(ORCHESTRATORS.values()) - {orchestrator}:
            assert f"`{other}`" in text, f"{orchestrator} must hand off to {other}"


# --- workflow patterns ------------------------------------------------------------------------


def test_every_step_carries_the_contract_its_pattern_and_the_workflow_brief() -> None:
    for slug, workflow, step in _steps():
        contract, pattern, brief = slug_refs(step["instructions"])
        assert contract == "step-contract" and brief == f"{slug}-brief", f"{slug}/{step['slug']}"
        expected = "challenge-main" if step["slug"].startswith("challenge-") else PATTERNS[step["slug"]]
        assert pattern == expected, f"{slug}/{step['slug']}"
        assert slug_refs(step["skills"]) == (step["actor"],), f"{slug}/{step['slug']}: the step injects its actor's craft skill"


def test_workflows_are_concise() -> None:
    for slug, workflow in CATALOG.items():
        assert 1 <= len(workflow["steps"]) <= MAX_STEPS, slug


def test_a_loop_is_draft_then_expert_challenges_then_owner_revision() -> None:
    loops = {slug: workflow for slug, workflow in CATALOG.items() if is_loop(workflow)}
    assert loops
    for slug, workflow in loops.items():
        draft, *panel, revise = workflow["steps"]
        assert (draft["slug"], revise["slug"]) == ("draft", "revise"), slug
        assert draft["actor"] == revise["actor"] and draft["artifact"] == revise["artifact"], slug
        assert 2 <= len(panel) <= MAX_PANEL, slug
        experts = [step["actor"] for step in panel]
        assert len(set(experts)) == len(experts) and draft["actor"] not in experts, slug
        for step in panel:
            assert step["slug"] == f"challenge-{step['actor']}" and step["artifact"] == "challenge", slug
            assert {"kind": "precondition", "slug": "after-draft", "step": "draft"} in step["conditions"], slug
            assert "packet-targets-the-drafted-artifact" in [c["slug"] for c in step["conditions"]], slug
        gates = {c["step"] for c in revise["conditions"] if c["kind"] == "precondition" and "step" in c}
        assert gates == {step["slug"] for step in panel}, f"{slug}: the owner revises after every challenge"
        revise_conditions = {c["slug"] for c in revise["conditions"]}
        assert {"revises-the-drafted-artifact", "every-packet-is-answered"} <= revise_conditions, slug


def test_every_main_artifact_kind_is_challenged_before_the_human_gate() -> None:
    mains = {slug for slug, schema in SCHEMAS.items() if schema["x-artifact"]["class"] == "main"}
    challenged = {workflow["steps"][0]["artifact"] for workflow in CATALOG.values() if is_loop(workflow)}
    assert mains <= challenged, f"never challenged: {sorted(mains - challenged)}"
    assert challenged - mains == {"event-record"}, "only Inspect and Adapt puts a record through the loop"
    for slug in mains:
        assert "challengeLedger" in SCHEMAS[slug]["required"], slug


def test_every_backlog_item_moves_through_its_owner_transition_and_a_board() -> None:
    transitions = {slug: workflow for slug, workflow in CATALOG.items() if workflow["steps"][0]["slug"] == "record-transition"}
    assert {workflow["steps"][0]["artifact"] for workflow in transitions.values()} == {"epic", "capability", "feature", "story"}
    for slug, workflow in transitions.items():
        record, board = workflow["steps"]
        assert board["slug"] == "update-kanban" and board["artifact"] == "kanban" and board["actor"] == workflow["orchestrator"], slug
        assert record["actor"] in SCHEMAS[record["artifact"]]["x-artifact"]["owners"], slug
        assert any("challenged" in c["slug"] for c in record["conditions"]), f"{slug}: no ready item without a challenge"


def test_every_layer_records_human_decisions_and_its_events() -> None:
    for layer, orchestrator in ORCHESTRATORS.items():
        mine = [workflow for workflow in CATALOG.values() if workflow["layer"] == layer]
        gates = [w for w in mine if w["steps"][0]["slug"] == "record-decision"]
        assert len(gates) == 1 and gates[0]["steps"][0]["actor"] == orchestrator, layer
        assert [c["slug"] for c in gates[0]["steps"][0]["conditions"]] == ["accepted-only-if-challenged"], layer
        events = [w for w in mine if w["steps"][0]["slug"] == "record"]
        assert events and all(w["steps"][0]["actor"] == orchestrator for w in events), layer


def test_advisory_predecessors_stay_inside_the_layer() -> None:
    for slug, workflow in CATALOG.items():
        for predecessor in workflow.get("predecessors", []):
            assert CATALOG[predecessor]["layer"] == workflow["layer"], f"{slug} <- {predecessor}"


# --- references resolve -----------------------------------------------------------------------


def test_every_reference_resolves() -> None:
    skills, instructions, agents, schemas = set(skill_slugs()), set(instruction_slugs()), set(agent_slugs()), set(schema_slugs())
    for slug, workflow in CATALOG.items():
        assert workflow["orchestrator"] in agents, slug
        assert set(slug_refs(workflow["instructions"])) <= instructions, slug
        for step in workflow["steps"]:
            where = f"{slug}/{step['slug']}"
            assert step["actor"] in agents and step["artifact"] in schemas, where
            assert set(slug_refs(step["skills"])) <= skills, where
            assert set(slug_refs(step["instructions"])) <= instructions, where
    assert len(instruction_slugs()) == len(set(instruction_slugs())), "instruction slugs are unique across folders"


def test_every_schema_is_delivered_by_a_step_and_bound_in_the_layout() -> None:
    delivered = {step["artifact"] for _, _, step in _steps()}
    assert set(schema_slugs()) == delivered
    assert {kind for _, kind, _ in layout_nodes()} == delivered
    assert {template for _, _, template in layout_nodes()} == template_slugs()


def test_every_brief_names_real_paths_templates_and_workflows() -> None:
    paths = {path for path, _, _ in layout_nodes()}
    for slug, workflow in CATALOG.items():
        text = (ORG / "instructions" / workflow["layer"] / f"{slug}-brief{INSTRUCTION_SUFFIX}").read_text(encoding="utf-8")
        for template in re.findall(r"`templates/([a-z0-9/-]+)\.artifact-template\.md`", text):
            assert template in template_slugs(), f"{slug}: {template}"
        for path in re.findall(r" at `(portfolio/[^`]+)`", text):
            assert path in paths, f"{slug}: {path}"
        for name in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text):
            if name.endswith(("-refinement", "-transition", "-planning", "-decision", "-launch")) and name not in SCHEMAS:
                assert name in CATALOG, f"{slug} names unknown workflow {name}"


# --- access control ---------------------------------------------------------------------------


def test_the_access_control_list_grants_exactly_what_the_steps_deliver() -> None:
    acl = load_acl()
    roles = {role["slug"]: {(p["artifact"], p["action"]) for p in role["privileges"]} for role in acl["roles"]}
    actors = {actor["slug"]: actor["roles"] for actor in acl["actors"]}
    assert set(actors) == set(agent_slugs()) and all(roles_ == [slug] for slug, roles_ in actors.items())
    needed: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for _, _, step in _steps():
        needed[step["actor"]] |= {(step["artifact"], "create"), (step["artifact"], "update")}
    assert roles == {slug: needed[slug] for slug in agent_slugs()}, "least privilege: no unused grant, no missing grant"


def test_orchestrators_hold_no_backlog_item_and_experts_only_what_they_author() -> None:
    acl = {role["slug"]: {p["artifact"] for p in role["privileges"]} for role in load_acl()["roles"]}
    for orchestrator in ORCHESTRATORS.values():
        assert acl[orchestrator].isdisjoint({"epic", "capability", "feature", "story", "code-change"}), orchestrator
        assert {"event-record", "kanban", "gate-decision"} <= acl[orchestrator], orchestrator
    for slug, kinds in acl.items():
        owned = {kind for kind, schema in SCHEMAS.items() if slug in schema["x-artifact"]["owners"]}
        if slug not in ORCHESTRATORS.values():
            assert kinds - {"challenge"} == owned & kinds, f"{slug} writes only its own mains and its challenge packets"


# --- the roster -------------------------------------------------------------------------------


def test_every_agent_acts_a_step_and_has_a_craft_skill() -> None:
    actors = {step["actor"] for _, _, step in _steps()}
    assert set(agent_slugs()) == actors == set(skill_slugs())


@pytest.mark.parametrize("slug", agent_slugs())
def test_agent_file_is_a_compact_identity(slug: str) -> None:
    path = ORG / "agents" / f"{slug}{AGENT_SUFFIX}"
    meta = parse_frontmatter(path)
    assert meta.get("name") == slug and 0 < len(meta.get("description", "")) <= 300, slug
    body = body_of(path)
    assert COPYRIGHT in body.splitlines()[0], slug
    headings = re.findall(r"^## (.+)$", body, re.MULTILINE)
    judge = "How you work" if slug in ORCHESTRATORS.values() else "How you judge"
    assert headings == ["Mission", "You own", "You never", judge, "SAFe anchor"], slug
    assert word_count(body) <= MAX_AGENT_WORDS, slug
    assert "STUB" not in body, slug


@pytest.mark.parametrize("slug", skill_slugs())
def test_skill_covers_every_artifact_its_agent_authors_and_challenges(slug: str) -> None:
    path = ORG / "skills" / f"{slug}{SKILL_SUFFIX}"
    meta = parse_frontmatter(path)
    assert meta.get("name") == slug and 0 < len(meta.get("description", "")) <= 300, slug
    body = body_of(path)
    assert COPYRIGHT in body.splitlines()[0] and "STUB" not in body, slug
    assert word_count(body) <= MAX_SKILL_WORDS, slug
    sections = re.split(r"^## ", body, flags=re.MULTILINE)
    by_title = {section.split("\n", 1)[0].strip(): section for section in sections[1:]}
    assert "Always ask" in by_title, slug
    challenged, authored = _challenged_kinds()[slug], _authored_kinds()[slug]
    if challenged:
        lens = set(re.findall(r"\(`([a-z0-9-]+)`\)", "\n".join(re.findall(r"^### .+$", by_title.get("Lens by artifact", ""), re.MULTILINE))))
        assert challenged <= lens, f"{slug}: no lens for {sorted(challenged - lens)}"
    else:
        assert "Lens by artifact" not in by_title, slug
    if authored:
        guide = set(re.findall(r"`([a-z0-9-]+)`", "\n".join(re.findall(r"^### .+$", by_title.get("Authoring guide", ""), re.MULTILINE))))
        assert authored <= guide, f"{slug}: no authoring guide for {sorted(authored - guide)}"


def test_prose_names_only_existing_agents_and_workflows() -> None:
    agents, workflows = set(agent_slugs()), set(CATALOG)
    suffixes = ("-engineer", "-officer", "-manager", "-architect", "-owner", "-designer", "-specialist", "-analyst", "-counsel", "-controller", "-writer", "-expert", "-coach", "-administrator", "-master")
    for folder in ("agents", "skills", "instructions"):
        for path in iter_named(ORG / folder, ".md"):
            for name in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", path.read_text(encoding="utf-8")):
                if name.endswith(suffixes):
                    assert name in agents, f"{path.name} names unknown agent {name}"
                if name.endswith(("-refinement", "-transition", "-gate-decision")) and name != "record-transition":
                    assert name in workflows, f"{path.name} names unknown workflow {name}"


def test_no_prose_tells_an_agent_which_skill_to_load_or_to_decide_for_the_human() -> None:
    for folder in ("agents", "skills", "instructions"):
        for path in iter_named(ORG / folder, ".md"):
            assert "load skills/" not in path.read_text(encoding="utf-8"), path.name


# --- context budgets --------------------------------------------------------------------------


def _instruction_words() -> dict[str, int]:
    return {path.name[: -len(INSTRUCTION_SUFFIX)]: word_count(body_of(path)) for path in iter_named(ORG / "instructions", INSTRUCTION_SUFFIX)}


def test_injected_instructions_fit_their_context_budget() -> None:
    words = _instruction_words()
    for slug, count in words.items():
        assert count <= (900 if slug.endswith("-catalog") else MAX_INSTRUCTION_WORDS), f"{slug}: {count} words"
    for slug, workflow, step in _steps():
        injected = sum(words[ref] for ref in slug_refs(step["instructions"]))
        assert injected <= MAX_WORKER_CONTEXT_WORDS, f"{slug}/{step['slug']}: {injected} words injected"
    for workflow in CATALOG.values():
        injected = sum(words[ref] for ref in slug_refs(workflow["instructions"]))
        assert injected <= MAX_ORCHESTRATOR_CONTEXT_WORDS, f"{workflow['orchestrator']}: {injected} words injected"


def test_every_shipped_file_carries_the_copyright_line() -> None:
    for folder in ("agents", "skills", "instructions", "conf", "workflows", "templates"):
        for path in sorted((ORG / folder).rglob("*")):
            if path.suffix in (".md", ".yaml"):
                assert COPYRIGHT in path.read_text(encoding="utf-8"), path


# --- the plugin -------------------------------------------------------------------------------


def test_plugin_binds_exactly_the_source_agents() -> None:
    plugin = load_plugin()
    assert "skills" not in plugin and "agents" not in plugin
    assert plugin["name"] == "poesis-saf-agentic-organization"
    assert re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?", plugin["version"])
    assert not [path for path in (ORG / "skills").rglob(f"*{SKILL_SUFFIX}") if path.parent != ORG / "skills"]
    tools = load_tools_map()["agents"]
    assert set(tools) == {f"agents/{slug}{AGENT_SUFFIX}" for slug in agent_slugs()}
    for slug in agent_slugs():
        dispatches = "agent" in tools[f"agents/{slug}{AGENT_SUFFIX}"]
        assert dispatches is (slug in ORCHESTRATORS.values()), f"{slug}: only orchestrators dispatch"


def test_the_catalog_document_lists_every_agent_workflow_and_kind() -> None:
    text = (ORG / "docs" / "catalog.md").read_text(encoding="utf-8")
    for name in (*agent_slugs(), *CATALOG, *schema_slugs()):
        assert f"`{name}`" in text, name
