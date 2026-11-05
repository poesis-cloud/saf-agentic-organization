"""Every artifact template, filled in, is a valid artifact for the harness.

The harness validates the bytes an actor writes against the artifact's schema (function 9): the
YAML frontmatter of a Markdown artifact, or the whole document of any other file, parsed as JSON.
It injects nothing, so a template must carry every required field itself, including the base
`slug`. Each template is filled the way an actor fills it (dates written over `YYYY-MM-DD`,
`<placeholders>` replaced by schema-valid sample values), written to a concrete path of the
workspace layout and validated by the harness `ArtifactStore`.
"""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from tests.conftest import HARNESS_SRC, ORG_ROOT

from application import _resolve_artifact_schemas
from config.config_loader import ConfigLoader
from stores.artifact_store.artifact_store import ArtifactStore
from utils.env_loader import EnvLoader
from utils.schema_validator import SchemaValidator
from utils.yaml_loader import YamlLoader

CONTRACTS = HARNESS_SRC.parent / "contracts"
SAMPLE_DATE = "2026-11-04"
PLACEHOLDER = re.compile(r"<[^<>\n]+>")
FENCE = {".md": "markdown", ".yaml": "json"}
PATTERN_SAMPLES = ("sample", "E-1", "F-1", "S-1", "ADR-1", "PP-1", "NFR-1", "pi-1", SAMPLE_DATE, "@developer", "1")
LAYOUT_KEYS = {
    "FRAMEWORK_AGENTS_DIR": "agents",
    "FRAMEWORK_ARTIFACTS_DIR": "artifacts",
    "FRAMEWORK_INSTRUCTIONS_DIR": "instructions",
    "FRAMEWORK_SKILLS_DIR": "skills",
    "FRAMEWORK_TEMPLATES_DIR": "templates",
    "FRAMEWORK_WORKFLOWS_DIR": "workflows",
}


def _layout_nodes() -> list[tuple[str, str, str]]:
    nodes: list[tuple[str, str, str]] = []

    def walk(children: list[dict], prefix: str) -> None:
        for node in children:
            path = prefix + node["slug"]
            if "children" in node:
                walk(node["children"], path + "/")
            else:
                nodes.append((path, node["artifact"], node["template"]))

    walk(yaml.safe_load((ORG_ROOT / "conf" / "workspace.conf.yaml").read_text(encoding="utf-8"))["nodes"], "")
    return nodes


NODES = _layout_nodes()


def _template_text(template: str) -> str:
    return (ORG_ROOT / "templates" / f"{template}.artifact-template.md").read_text(encoding="utf-8")


def artifact_block(template: str, suffix: str) -> str:
    """Return the artifact the template documents: its first fenced block of the file's format."""
    found = re.search(rf"^```{FENCE[suffix]}\n(.*?)^```\s*$", _template_text(template), re.S | re.M)
    assert found, f"{template}: no ```{FENCE[suffix]} artifact block"
    return found.group(1)


@pytest.fixture(scope="module")
def store(tmp_path_factory: pytest.TempPathFactory) -> ArtifactStore:
    workspace = tmp_path_factory.mktemp("workspace")
    with pytest.MonkeyPatch.context() as patch:
        for key, value in LAYOUT_KEYS.items():
            patch.setenv(key, value)
        patch.setenv("FRAMEWORK_WORKSPACE_DIR", str(workspace))
        loader = ConfigLoader(
            EnvLoader(), YamlLoader(), SchemaValidator.compile_contracts(sorted(CONTRACTS.rglob("*.schema.json")))
        )
        layout = loader.load_framework_layout(ORG_ROOT)
        workspace_layout = loader.load_workspace_layout(ORG_ROOT)
        schemas = _resolve_artifact_schemas(layout, workspace_layout, loader.load_workflow_catalog(ORG_ROOT))
    return ArtifactStore(workspace, schemas, workspace_layout)


@pytest.fixture(scope="module")
def registry() -> SchemaValidator:
    schemas = sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json"))
    return SchemaValidator.compile_contracts([*sorted(CONTRACTS.rglob("*.schema.json")), *schemas])


def _schema(kind: str) -> dict:
    path = next((ORG_ROOT / "artifacts").rglob(f"{kind}.artifact.schema.json"))
    return json.loads(path.read_text(encoding="utf-8"))


class _Filler:
    """Replace placeholders with sample values that satisfy the schema at their location."""

    def __init__(self, registry: SchemaValidator, schema: dict) -> None:
        self._resolver = registry._registry.resolver(base_uri=schema["$id"])
        self._root = schema

    def _resolve(self, sub: Any) -> dict:
        while isinstance(sub, dict) and "$ref" in sub:
            merged = {key: value for key, value in sub.items() if key != "$ref"}
            target = self._resolver.lookup(sub["$ref"]).contents
            sub = {**target, **merged, "properties": {**target.get("properties", {}), **merged.get("properties", {})}}
        return sub if isinstance(sub, dict) else {}

    def _sample(self, sub: Any) -> Any:
        sub = self._resolve(sub)
        if "const" in sub:
            return sub["const"]
        if "enum" in sub:
            return next(value for value in sub["enum"] if value is not None)
        for key in ("oneOf", "anyOf"):
            if key in sub:
                return self._sample(next(option for option in sub[key] if self._resolve(option).get("type") != "null"))
        kind = sub.get("type")
        if isinstance(kind, list):
            kind = next(item for item in kind if item != "null")
        if kind in {"integer", "number"}:
            return max(1, sub.get("minimum", 1))
        if kind == "boolean":
            return True
        if kind == "array":
            return [self._sample(sub.get("items", {}))]
        if kind == "object":
            return {}
        if "pattern" in sub:
            matches = [value for value in PATTERN_SAMPLES if re.search(sub["pattern"], value)]
            assert matches, f"no sample value matches pattern {sub['pattern']!r}"
            return matches[0]
        return SAMPLE_DATE if sub.get("format") == "date" else "sample"

    def fill(self, value: Any, sub: Any) -> Any:
        sub = self._resolve(sub)
        if isinstance(value, dict):
            properties = sub.get("properties", {})
            return {key: self.fill(item, properties.get(key, {})) for key, item in value.items()}
        if isinstance(value, list):
            return [self.fill(item, sub.get("items", {})) for item in value]
        if isinstance(value, str) and PLACEHOLDER.search(value):
            return self._sample(sub)
        return value

    def fill_root(self, value: Any) -> Any:
        return self.fill(value, self._root)


def _concrete(path: str) -> str:
    return PLACEHOLDER.sub("sample", path)


def _dates(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return [found for item in value.values() for found in _dates(item)]
    if isinstance(value, list):
        return [found for item in value for found in _dates(item)]
    return [value] if isinstance(value, (datetime.date, datetime.datetime)) else []


def _filled(block: str, suffix: str) -> tuple[Any, str]:
    text = block.replace("YYYY-MM-DD", SAMPLE_DATE)
    if suffix == ".md":
        assert text.startswith("---\n"), "Markdown artifact must open with YAML frontmatter"
        raw, body = text[4:].split("\n---\n", 1)
        return yaml.safe_load(raw), body
    return json.loads(text), ""


TEMPLATES = sorted({(Path(path).suffix, template, kind) for path, kind, template in NODES})


@pytest.mark.parametrize("suffix,template,kind", TEMPLATES, ids=[template for _, template, _ in TEMPLATES])
def test_filled_template_is_a_valid_artifact(
    store: ArtifactStore, registry: SchemaValidator, suffix: str, template: str, kind: str
) -> None:
    data, body = _filled(artifact_block(template, suffix), suffix)
    assert _dates(data) == [], "date values must be quoted strings"
    assert "slug" in data, "the harness identity field `slug` must be authored"
    assert not [key for key in data if key.startswith("__")], "the harness injects no `__*` field"
    data = _Filler(registry, _schema(kind)).fill_root(data)
    path = _concrete(next(path for path, node_kind, node_template in NODES if node_template == template))
    target = store._workspace_dir / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if suffix == ".md":
        target.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body, encoding="utf-8")
    else:
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    assert [finding.message for finding in store.validate_artifact(Path(path))] == []


@pytest.mark.parametrize("suffix,template,kind", TEMPLATES, ids=[template for _, template, _ in TEMPLATES])
def test_template_headings_match_the_schema_sections(suffix: str, template: str, kind: str) -> None:
    sections = _schema(kind)["x-artifact"].get("sections")
    if suffix != ".md" or not sections:
        return
    headings = re.findall(r"^## (.+?)\s*$", artifact_block(template, suffix), re.M)
    assert set(sections["required"]) <= set(headings)
    if not sections.get("allowUnknown", True):
        assert set(headings) <= set(sections["required"]) | set(sections.get("optional", []))


def test_no_schema_declares_harness_injected_fields() -> None:
    for path in sorted((ORG_ROOT / "artifacts").rglob("*.artifact.schema.json")):
        text = path.read_text(encoding="utf-8")
        assert '"__' not in text and "injected by the" not in text, path.name


def test_dates_in_templates_and_examples_are_quoted() -> None:
    unquoted = re.compile(r"[A-Za-z_]+:\s+(?:\d{4}-\d{2}-\d{2}|YYYY-MM-DD)\b")
    prose = [ORG_ROOT / "README.md", *(path for folder in ("templates", "skills", "instructions", "agents", "docs")
             for path in (ORG_ROOT / folder).rglob("*.md"))]
    offenders = [path.relative_to(ORG_ROOT).as_posix() for path in sorted(prose) if unquoted.search(path.read_text(encoding="utf-8"))]
    assert offenders == []
