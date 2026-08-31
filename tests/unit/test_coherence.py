"""Live-tree coherence: slugs, ceremonies, ACL, required-reading, plugin."""

from __future__ import annotations

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
    assert nfr_schema["x-artifact"]["pathPatterns"] == ["products/*/nfr-list.md"]


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
    plugin = load_plugin()
    skills = plugin["skills"]
    assert set(skills) == {f"skills/{slug}.skill.md" for slug in skill_slugs()}
    assert set(plugin["agents"]) == {f"agents/{slug}.agent.md" for slug in agent_slugs()}
    assert plugin["version"] == "0.1.0"
    for path in skills:
        assert path.startswith("skills/")
        assert path.count("/") == 1
        assert path.endswith(".skill.md")
    tools = load_tools_map()["agents"]
    assert set(tools) == set(plugin["agents"])


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
