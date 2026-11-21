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
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
PLACEHOLDER = re.compile(r"<[a-z0-9-]+>")
LAYERS = ("portfolio", "solution", "art", "team")
ORCHESTRATOR_DUTIES = (
    "workflow-selection-handling",
    "step-resolution-handling",
    "no-next-step-handling",
    "reports-handling",
)


def organization_root() -> Path:
    return ORG_ROOT


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_named(directory: Path, suffix: str) -> Iterator[Path]:
    yield from sorted(path for path in directory.rglob(f"*{suffix}") if path.is_file())


def stems(folder: str, suffix: str) -> tuple[str, ...]:
    return tuple(path.name[: -len(suffix)] for path in iter_named(ORG_ROOT / folder, suffix))


def skill_slugs() -> tuple[str, ...]:
    return stems("skills", SKILL_SUFFIX)


def instruction_slugs() -> tuple[str, ...]:
    return stems("instructions", INSTRUCTION_SUFFIX)


def agent_slugs() -> tuple[str, ...]:
    return stems("agents", AGENT_SUFFIX)


def schema_slugs() -> tuple[str, ...]:
    return stems("artifacts", SCHEMA_SUFFIX)


def load_workflows() -> dict[str, Mapping[str, Any]]:
    """Every workflow configuration, keyed by slug, with its layer folder under `layer`."""
    catalog: dict[str, Mapping[str, Any]] = {}
    for path in iter_named(ORG_ROOT / "workflows", WORKFLOW_SUFFIX):
        data = dict(load_yaml(path))
        assert path.name == f"{data['slug']}{WORKFLOW_SUFFIX}", path
        data["layer"] = path.parent.name
        catalog[str(data["slug"])] = data
    return catalog


def load_schemas() -> dict[str, Mapping[str, Any]]:
    return {path.name[: -len(SCHEMA_SUFFIX)]: load_json(path) for path in iter_named(ORG_ROOT / "artifacts", SCHEMA_SUFFIX)}


def template_slugs() -> set[str]:
    templates = ORG_ROOT / "templates"
    return {path.relative_to(templates).as_posix()[: -len(TEMPLATE_SUFFIX)] for path in iter_named(templates, TEMPLATE_SUFFIX)}


def layout_nodes() -> list[tuple[str, str, str]]:
    """Every artifact node of the workspace layout as (path, kind, template slug)."""
    nodes: list[tuple[str, str, str]] = []

    def walk(children: list[Mapping[str, Any]], prefix: str) -> None:
        for node in children:
            path = prefix + str(node["slug"])
            if "children" in node:
                walk(node["children"], path + "/")
            else:
                nodes.append((path, str(node["artifact"]), str(node["template"])))

    walk(load_yaml(ORG_ROOT / "conf" / "workspace.conf.yaml")["nodes"], "")
    return nodes


def load_plugin() -> Mapping[str, Any]:
    return load_json(ORG_ROOT / "builds" / "plugin" / "plugin.json")


def load_tools_map() -> Mapping[str, Any]:
    return load_yaml(ORG_ROOT / "builds" / "plugin" / "tools.yaml")


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


def body_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    return text[match.end():] if match else text


def word_count(text: str) -> int:
    return len(text.split())


def is_loop(workflow: Mapping[str, Any]) -> bool:
    return workflow["steps"][0]["slug"] == "draft"


def fill_template(template_slug: str, slug: str, overrides: Mapping[str, Any] | None = None) -> tuple[dict[str, Any], str]:
    """Fill a template the way an actor does: (frontmatter data, file text)."""
    path = ORG_ROOT / "templates" / f"{template_slug}{TEMPLATE_SUFFIX}"
    data = {**dict(parse_frontmatter(path)), "slug": slug, **dict(overrides or {})}
    text = "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body_of(path)
    return data, text
