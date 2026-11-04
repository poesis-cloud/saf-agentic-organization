"""Every workspace path the framework mentions is a path of the workspace layout.

The harness resolves an artifact's kind, and the actor's authorization, from its path in the
layout `conf/workspace.conf.yaml` binds. A schema, template, skill, instruction, agent or doc that
names a path the layout doesn't have sends an actor to a file the harness refuses (or to a stale
`path:` value). Workspace paths are written in full, from the layout root (`portfolio/…`); a bare
artifact file name is ambiguous and is written as its full path too.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from tests.conftest import ORG_ROOT

PLACEHOLDER = r"(?:<[^<>/\s]+>|\*|[A-Za-z0-9][A-Za-z0-9._-]*)"
WORKSPACE_ROOTS = {
    "portfolio", "art", "products", "epics", "features", "portfolio-backlog", "program-backlog", "teams",
    "team-backlog", "improvement-backlog", "iterations", "daily", "releases", "reviews", "sync", "_sync", "qa",
    "kanban",
}  # fmt: skip
NOT_ARTIFACTS = re.compile(
    r"(^|/)(README|PROJECT_BRIEF|CONTRIBUTING|SKILL|AGENTS|copilot-instructions|host-binding)\.md$|^(tools|models)\.yaml$"
    r"|\.(skill|instructions|agent|prompt|artifact-template)\.md$|\.conf\.yaml$|\.schema\.json$"
)
PROSE_DIRS = ("skills", "instructions", "agents", "templates", "docs")
WORKFLOWS = {path.name.split(".", 1)[0] for path in (ORG_ROOT / "workflows").rglob("*.workflow.conf.yaml")}


def _layout() -> list[str]:
    paths: list[str] = []

    def walk(children: list[dict], prefix: str) -> None:
        for node in children:
            path = prefix + node["slug"]
            if "children" in node:
                walk(node["children"], path + "/")
            else:
                paths.append(path)

    walk(yaml.safe_load((ORG_ROOT / "conf" / "workspace.conf.yaml").read_text(encoding="utf-8"))["nodes"], "")
    return paths


def _pattern(path: str) -> str:
    return "".join(PLACEHOLDER if part.startswith("<") else re.escape(part) for part in re.split(r"(<[^<>]+>)", path))


LAYOUT = _layout()
FILES = re.compile("|".join(_pattern(path) for path in LAYOUT))
FOLDERS = re.compile(
    "|".join(sorted({_pattern(path.rsplit("/", depth)[0]) for path in LAYOUT for depth in range(1, path.count("/") + 1)}))
)
LEAVES = re.compile("|".join(sorted({_pattern(path.rsplit("/", 1)[-1]) for path in LAYOUT})))


def offending(token: str) -> bool:
    token = re.sub(r"^<FRAMEWORK_WORKSPACE_DIR>/", "", token.lstrip("\"'([").rstrip("\"'.,;:)]"))
    if not token or "://" in token or token.startswith(("../", "./", "#", "$", "logs/")):
        return False
    if "/" not in token:
        return token.endswith((".md", ".yaml", ".yml")) and not NOT_ARTIFACTS.search(token)
    first = token.split("/", 1)[0]
    if first in WORKFLOWS or first not in WORKSPACE_ROOTS and not first.startswith("pi-"):
        return False
    folder = re.sub(r"/(\*\*?)?$", "", token)
    return not (FILES.fullmatch(token) or FOLDERS.fullmatch(folder))


def _tokens(text: str) -> list[str]:
    return [word for span in re.findall(r"`([^`\n]+)`", text) for word in re.split(r"[\s,]+", span) if word]


def _prose() -> list[Path]:
    return sorted([ORG_ROOT / "README.md", *(path for folder in PROSE_DIRS for path in (ORG_ROOT / folder).rglob("*.md"))])


def _schema_strings(value: object) -> list[str]:
    if isinstance(value, dict):
        return [found for item in value.values() for found in _schema_strings(item)]
    if isinstance(value, list):
        return [found for item in value for found in _schema_strings(item)]
    return [value] if isinstance(value, str) else []


@pytest.mark.parametrize("path", _prose(), ids=lambda path: path.relative_to(ORG_ROOT).as_posix())
def test_prose_names_only_layout_paths(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md" and "templates" in path.parts:
        text += "\n".join(f"`{line}`" for line in re.findall(r"^\s*([\w<>*./-]+/[\w<>*./-]*)\s*(?:#.*)?$", text, re.M))
    assert sorted({token for token in _tokens(text) if offending(token)}) == []


@pytest.mark.parametrize(
    "path", sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json")), ids=lambda path: path.name
)
def test_schemas_name_only_layout_paths(path: Path) -> None:
    schema = json.loads(path.read_text(encoding="utf-8"))
    words = [word for text in _schema_strings(schema) for word in _tokens(text) + re.findall(r"^[\w<>*./-]+/[\w<>*./-]+$", text)]
    assert sorted({word for word in words if offending(word)}) == []


def test_the_rule_rejects_stale_paths() -> None:
    assert not offending("portfolio/portfolio-manifest.yaml")
    assert not offending("portfolio/products/<product-slug>/nfr-list.md")
    assert not offending("portfolio/art/<art-slug>/pi-<pi-slug>/objectives.md")
    assert not offending("portfolio/portfolio-backlog/*/*.epic.md")
    assert not offending("portfolio/art/<art-slug>/improvement-backlog/")
    for stale in ("portfolio-manifest.yaml", "products/<product-slug>/nfr-list.md", "art/<art-slug>/art-manifest.yaml",
                  "portfolio/products/<p>/risks.md", "portfolio/epics/"):  # fmt: skip
        assert offending(stale), stale
