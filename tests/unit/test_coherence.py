"""Live-tree coherence: slugs, ceremonies, ACL, required-reading, plugin."""

from __future__ import annotations

import re
from pathlib import Path

from tests.loaders import (
    CEREMONY_PAIRS,
    ORCHESTRATOR_READING,
    agent_slugs,
    instruction_slugs,
    load_acl,
    load_plugin,
    load_tools_map,
    load_workflows,
    markdown_skill_targets,
    organization_root,
    parse_frontmatter,
    required_reading_skill_hrefs,
    schema_slugs,
    skill_slugs,
    slug_refs,
    template_slugs,
)

ORG = organization_root()


def test_every_workflow_and_step_has_a_description() -> None:
    for slug, workflow in load_workflows().items():
        description = workflow.get("description")
        assert isinstance(description, str) and description.strip(), slug
        for step in workflow["steps"]:
            step_description = step.get("description")
            assert isinstance(step_description, str) and step_description.strip(), (
                f"{slug}/{step['slug']}"
            )


SPEECH_ACT_INSTRUCTION = {
    "value-management-officer": "value-management-officer-interpret-speech-acts",
    "release-train-engineer": "release-train-engineer-interpret-speech-acts",
    "scrum-master": "scrum-master-interpret-speech-acts",
}


def test_every_workflow_loads_orchestrator_speech_act_instruction() -> None:
    for slug, workflow in load_workflows().items():
        expected = SPEECH_ACT_INSTRUCTION[workflow["orchestrator"]]
        assert expected in slug_refs(workflow.get("instructions")), slug


def test_catalog_split_keeps_architecture_out_of_feature_refinement() -> None:
    catalog = load_workflows()
    feature_artifacts = {step["artifact"] for step in catalog["feature-backlog-refinement"]["steps"]}
    assert feature_artifacts == {
        "feature",
        "feature-enabler",
        "feasibility-review",
        "architecture-review",
        "security-review",
        "ux-review",
    }
    assert {"adr", "nfr-list", "architecture-runway", "operability-review"}.isdisjoint(feature_artifacts)

    runway_steps = catalog["architectural-runway-extension"]["steps"]
    runway_slugs = [step["slug"] for step in runway_steps]
    assert runway_slugs[:2] == ["author-nfrs", "author-adr"]
    adr = next(step for step in runway_steps if step["slug"] == "author-adr")
    assert any(condition.get("step") == "author-nfrs" for condition in adr["conditions"])
    assert {step["artifact"] for step in runway_steps} >= {"nfr-list", "adr", "architecture-runway"}

    vision_artifacts = {step["artifact"] for step in catalog["architectural-vision"]["steps"]}
    assert "architecture-vision" in vision_artifacts
    assert "adr" not in vision_artifacts

    derivation_artifacts = {step["artifact"] for step in catalog["feature-derivation"]["steps"]}
    assert derivation_artifacts == {"feature", "feature-enabler"}
    assert "story-derivation" not in catalog

    story_artifacts = {step["artifact"] for step in catalog["team-backlog-refinement"]["steps"]}
    assert {"story", "story-enabler", "architecture-review", "ux-review"} <= story_artifacts
    assert {"adr", "nfr-list", "architecture-runway"}.isdisjoint(story_artifacts)

    from tests.loaders import load_json

    nfr_schema = load_json(ORG / "artifacts" / "system-architect" / "nfr-list.artifact.schema.json")
    assert nfr_schema["x-artifact"]["pathPatterns"] == ["portfolio/products/*/nfr-list.md"]


def test_every_schema_is_a_workflow_step_artifact() -> None:
    schemas = set(schema_slugs())
    used = {
        step["artifact"]
        for workflow in load_workflows().values()
        for step in workflow["steps"]
    }
    assert schemas == used, f"unused={sorted(schemas - used)} missing_schema={sorted(used - schemas)}"


def test_every_workflow_skill_and_instruction_slug_resolves() -> None:
    skills = set(skill_slugs())
    instructions = set(instruction_slugs())
    schemas = set(schema_slugs())
    agents = set(agent_slugs())
    for slug, workflow in load_workflows().items():
        assert slug in {
            path.stem.replace(".workflow.conf", "")
            for path in (ORG / "workflows").rglob("*.yaml")
        }
        assert workflow["orchestrator"] in agents
        for ref in slug_refs(workflow.get("skills")):
            assert ref in skills, f"{slug} skill {ref}"
        for ref in slug_refs(workflow.get("instructions")):
            assert ref in instructions, f"{slug} instruction {ref}"
        for step in workflow["steps"]:
            assert step["actor"] in agents
            assert step["artifact"] in schemas
            for ref in slug_refs(step.get("skills")):
                assert ref in skills, f"{slug}/{step['slug']} skill {ref}"
            for ref in slug_refs(step["instructions"]):
                assert ref in instructions, f"{slug}/{step['slug']} instruction {ref}"


def test_workspace_templates_resolve() -> None:
    known = template_slugs()
    missing: list[str] = []

    def walk(nodes: list[object]) -> None:
        for node in nodes:
            if not isinstance(node, dict):
                continue
            if "template" in node:
                if node["template"] not in known:
                    missing.append(str(node["template"]))
            walk(list(node.get("children") or []))

    from tests.loaders import load_yaml

    walk(list(load_yaml(ORG / "conf" / "workspace.conf.yaml")["nodes"]))
    assert missing == []


def test_ceremony_skill_workflow_pairs() -> None:
    catalog = load_workflows()
    for workflow_slug, skill_slug, orchestrator in CEREMONY_PAIRS:
        workflow = catalog[workflow_slug]
        assert workflow["orchestrator"] == orchestrator
        assert skill_slug in slug_refs(workflow.get("skills"))
        assert (ORG / "skills" / f"{skill_slug}.skill.md").is_file()
        assert len(workflow["steps"]) >= 1


def test_acl_covers_every_actor_and_orchestrator() -> None:
    acl_actors = {actor["slug"] for actor in load_acl()["actors"]}
    for slug in agent_slugs():
        assert slug in acl_actors
    for workflow in load_workflows().values():
        assert workflow["orchestrator"] in acl_actors
        for step in workflow["steps"]:
            assert step["actor"] in acl_actors


def test_orchestrator_required_reading_is_distinct() -> None:
    for agent_slug, expected in ORCHESTRATOR_READING.items():
        hrefs = required_reading_skill_hrefs(agent_slug)
        for name in expected:
            assert name in hrefs
            assert (ORG / "skills" / name).is_file()
        assert expected[0] != expected[1]


def test_no_broken_markdown_skill_links() -> None:
    skills_dir = ORG / "skills"
    broken: list[str] = []
    for path in (*((ORG / "agents").glob("*.md")), *((ORG / "skills").glob("*.md"))):
        for target, resolved in markdown_skill_targets(path):
            stem = Path(target).name
            if resolved.is_file() or (skills_dir / stem).is_file():
                continue
            broken.append(f"{path.name} -> {target}")
    assert broken == []


def test_plugin_skills_are_flat_skill_files() -> None:
    """Source skills are flat `skills/<stem>.skill.md` files; the Agent Plugins 1.0 manifest is
    closed (components are discovered by convention, never enumerated) and the tools map binds
    exactly the source agents."""
    plugin = load_plugin()
    assert "skills" not in plugin and "agents" not in plugin
    assert plugin["name"] == "poesis-saf-agentic-organization"
    assert re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?", plugin["version"])
    assert skill_slugs()
    assert not [path for path in (ORG / "skills").rglob("*.skill.md") if path.parent != ORG / "skills"]
    tools = load_tools_map()["agents"]
    assert set(tools) == {f"agents/{slug}.agent.md" for slug in agent_slugs()}


def test_agent_frontmatter_name_matches_filename() -> None:
    for slug in agent_slugs():
        path = ORG / "agents" / f"{slug}.agent.md"
        frontmatter = parse_frontmatter(path)
        assert frontmatter.get("name") == slug


def test_pm_skill_is_safe_feature_authoring() -> None:
    text = (ORG / "skills" / "product-manager.skill.md").read_text(encoding="utf-8")
    assert "Feature ∅→funnel" in text
    assert "funnel→refined" in text
    assert "DO NOT USE FOR" in text
    assert "Poesis GitHub Project sync" in text
    body = text.split("---", 2)[-1]
    assert "github-sync" not in body.lower()


def _actor_skills() -> set[str]:
    """Actors with an author or bench skill: the skill the harness injects into their step (function 7)."""
    return {
        slug
        for slug in skill_slugs()
        if str(parse_frontmatter(ORG / "skills" / f"{slug}.skill.md").get("description", "")).startswith(
            ("**SAFe AUTHOR SKILL", "**SAFe BENCH SKILL")
        )
    }


def test_actor_skills_are_the_author_and_bench_hats() -> None:
    assert _actor_skills() == {
        "business-owner",
        "developer",
        "enterprise-architect",
        "operator",
        "product-manager",
        "product-owner",
        "quality-engineer",
        "security-expert",
        "system-architect",
        "tech-writer",
        "ux-designer",
    }


def test_every_step_declares_its_actor_authoring_skill() -> None:
    actor_skills = _actor_skills()
    missing = [
        f"{slug}/{step['slug']} ({step['actor']})"
        for slug, workflow in load_workflows().items()
        for step in workflow["steps"]
        if step["actor"] in actor_skills and step["actor"] not in slug_refs(step.get("skills"))
    ]
    assert missing == []


def test_dispatch_prose_does_not_name_the_skill_to_load() -> None:
    offenders = [
        path.name
        for folder in ("skills", "agents", "instructions")
        for path in sorted((ORG / folder).rglob("*.md"))
        if "load skills/" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []
