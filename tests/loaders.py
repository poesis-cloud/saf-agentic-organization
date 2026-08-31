"""Content loaders asserted by the organization coherence suite."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator, Mapping

import yaml

ORG_ROOT = Path(__file__).resolve().parents[1]
SKILL_SUFFIX = ".skill.md"
INSTRUCTION_SUFFIX = ".instructions.md"
AGENT_SUFFIX = ".agent.md"
WORKFLOW_SUFFIX = ".workflow.conf.yaml"
SCHEMA_SUFFIX = ".artifact.schema.json"
TEMPLATE_SUFFIX = ".artifact-template.md"
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

CEREMONY_PAIRS = (
    ("art-sync", "program-art-sync", "release-train-engineer"),
    ("system-demo", "program-system-demo", "release-train-engineer"),
    ("team-sync", "team-daily-sync", "scrum-master"),
    ("iteration-retrospective", "team-retrospective", "scrum-master"),
)

ORCHESTRATOR_READING = {
    "value-management-officer": ("value-management-officer.skill.md", "lpm.skill.md"),
    "release-train-engineer": ("release-train-engineer.skill.md", "art.skill.md"),
    "scrum-master": ("scrum-master.skill.md", "scrum.skill.md"),
}


def organization_root() -> Path:
    return ORG_ROOT


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_named(directory: Path, suffix: str) -> Iterator[Path]:
    yield from sorted(path for path in directory.rglob(f"*{suffix}") if path.is_file())


def skill_slugs() -> tuple[str, ...]:
    return tuple(path.name[: -len(SKILL_SUFFIX)] for path in iter_named(ORG_ROOT / "skills", SKILL_SUFFIX))


def instruction_slugs() -> tuple[str, ...]:
    return tuple(
        path.name[: -len(INSTRUCTION_SUFFIX)]
        for path in iter_named(ORG_ROOT / "instructions", INSTRUCTION_SUFFIX)
    )


def agent_slugs() -> tuple[str, ...]:
    return tuple(path.name[: -len(AGENT_SUFFIX)] for path in iter_named(ORG_ROOT / "agents", AGENT_SUFFIX))


def workflow_paths() -> tuple[Path, ...]:
    return tuple(iter_named(ORG_ROOT / "workflows", WORKFLOW_SUFFIX))


def load_workflows() -> dict[str, Mapping[str, Any]]:
    catalog: dict[str, Mapping[str, Any]] = {}
    for path in workflow_paths():
        data = load_yaml(path)
        catalog[str(data["slug"])] = data
    return catalog


def schema_slugs() -> tuple[str, ...]:
    return tuple(
        path.name[: -len(SCHEMA_SUFFIX)]
        for path in iter_named(ORG_ROOT / "artifacts", SCHEMA_SUFFIX)
    )


def template_slugs() -> set[str]:
    templates = ORG_ROOT / "templates"
    slugs: set[str] = set()
    for path in templates.rglob(f"*{TEMPLATE_SUFFIX}"):
        relative = path.relative_to(templates).with_suffix("").as_posix()
        if relative.endswith(".artifact-template"):
            relative = relative[: -len(".artifact-template")]
        slugs.add(relative)
    return slugs


def load_plugin() -> Mapping[str, Any]:
    return load_json(ORG_ROOT / "builds" / "github-copilot" / "plugin.json")


def load_tools_map() -> Mapping[str, Any]:
    return load_yaml(ORG_ROOT / "builds" / "github-copilot" / "tools.yaml")


def load_acl() -> Mapping[str, Any]:
    return load_yaml(ORG_ROOT / "conf" / "access-control-list.conf.yaml")


def slug_refs(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def parse_frontmatter(path: Path) -> Mapping[str, Any]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if match is None:
        return {}
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, Mapping) else {}


def markdown_skill_targets(path: Path) -> tuple[tuple[str, Path], ...]:
    text = path.read_text(encoding="utf-8")
    found: list[tuple[str, Path]] = []
    for _label, target in MARKDOWN_LINK.findall(text):
        if not target.endswith(SKILL_SUFFIX):
            continue
        resolved = (path.parent / target).resolve()
        found.append((target, resolved))
    return tuple(found)


def required_reading_skill_hrefs(agent_slug: str) -> tuple[str, ...]:
    text = (ORG_ROOT / "agents" / f"{agent_slug}{AGENT_SUFFIX}").read_text(encoding="utf-8")
    hrefs: list[str] = []
    for _label, target in MARKDOWN_LINK.findall(text):
        if target.endswith(SKILL_SUFFIX):
            hrefs.append(Path(target).name)
    return tuple(hrefs)
