"""Artifact schemas, templates and the workspace layout agree with each other and with the harness."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import HARNESS_SRC, ORG_ROOT
from tests.loaders import (
    PLACEHOLDER,
    SCHEMA_SUFFIX,
    TEMPLATE_SUFFIX,
    body_of,
    fill_template,
    iter_named,
    layout_nodes,
    load_json,
    load_schemas,
    parse_frontmatter,
)

from utils.schema_validator import SchemaValidator

CONTRACTS = HARNESS_SRC.parent / "contracts"
SCHEMAS = load_schemas()
NODES = layout_nodes()
DEFINITIONS = load_json(ORG_ROOT / "artifacts" / "framework-definitions.schema.json")["definitions"]


@pytest.fixture(scope="module")
def registry() -> SchemaValidator:
    return SchemaValidator.compile_contracts(
        [*sorted(CONTRACTS.rglob("*.schema.json")), *iter_named(ORG_ROOT / "artifacts", SCHEMA_SUFFIX)]
    )


@pytest.mark.parametrize(("path", "kind", "template"), NODES, ids=[node[0] for node in NODES])
def test_a_filled_template_is_a_valid_artifact_of_its_kind(registry: SchemaValidator, path: str, kind: str, template: str) -> None:
    """The harness validates the frontmatter an actor writes; a template must hold every required field."""
    data, _ = fill_template(template, "sample")
    errors = registry.validate_instance(SCHEMAS[kind]["$id"], data)
    assert errors == (), f"{template}: {[f'{e.path}: {e.message}' for e in errors]}"
    assert data["stepOutcomes"] == [], template


@pytest.mark.parametrize("kind", sorted(SCHEMAS))
def test_schema_extends_the_harness_base_and_copies_the_shared_definitions(kind: str) -> None:
    schema = SCHEMAS[kind]
    assert schema["$id"] == f"gsmarc://saf/artifacts/{kind}.artifact/v1"
    assert schema["$ref"] == "gsmarc://saf/contracts/artifact/v1"
    assert {"title", "stepOutcomes"} <= set(schema["required"]) <= set(schema["properties"])
    for name, definition in schema["$defs"].items():
        assert definition == DEFINITIONS[name], f"{kind}: {name} drifted from framework-definitions"
    refs = {prop["$ref"].rsplit("/", 1)[1] for prop in schema["properties"].values() if "$ref" in prop}
    assert refs == set(schema["$defs"]), kind


@pytest.mark.parametrize("kind", sorted(SCHEMAS))
def test_schema_metadata_matches_the_layout(kind: str) -> None:
    meta = SCHEMAS[kind]["x-artifact"]
    assert meta["kind"] == kind and meta["class"] in ("main", "challenge", "record")
    assert sorted(meta["pathPatterns"]) == sorted({PLACEHOLDER.sub("*", path) for path, node_kind, _ in NODES if node_kind == kind})
    assert sorted(meta["templates"]) == sorted({f"templates/{template}{TEMPLATE_SUFFIX}" for _, node_kind, template in NODES if node_kind == kind})
    assert (meta["class"] == "main") is bool(meta["owners"]), kind


@pytest.mark.parametrize(("path", "kind", "template"), NODES, ids=[node[0] for node in NODES])
def test_template_sections_are_the_schema_sections(path: str, kind: str, template: str) -> None:
    body = body_of(ORG_ROOT / "templates" / f"{template}{TEMPLATE_SUFFIX}")
    headings = [line[3:] for line in body.splitlines() if line.startswith("## ")]
    sections = SCHEMAS[kind]["x-artifact"]["sections"]
    assert [h for h in headings if h in sections["required"]] == sections["required"], template
    if kind != "event-record":  # each SAFe event has its own agenda sections
        assert headings == [*sections["required"], *sections["optional"]] or set(headings) == set(sections["required"]) | set(sections["optional"]), template


def test_dates_in_templates_are_quoted_strings() -> None:
    for path in iter_named(ORG_ROOT / "templates", TEMPLATE_SUFFIX):
        for key, value in parse_frontmatter(path).items():
            if "date" in key.lower() or key in ("updated", "lastReviewed"):
                assert value is None or isinstance(value, str), f"{path.name}: {key}"


def test_event_templates_cover_every_event_of_the_schema() -> None:
    events = set(SCHEMAS["event-record"]["properties"]["event"]["enum"])
    templates = {Path(template).name: parse_frontmatter(ORG_ROOT / "templates" / f"{template}{TEMPLATE_SUFFIX}")["event"] for _, kind, template in NODES if kind == "event-record"}
    assert set(templates) == events == set(templates.values())
    assert all(name == event for name, event in templates.items())


def test_kanban_templates_carry_the_states_of_their_backlog_item() -> None:
    boards = {"portfolio-kanban": ("epic", "epic-enabler"), "solution-train-kanban": ("capability", "capability-enabler"),
              "art-kanban": ("feature", "feature-enabler"), "team-kanban": ("story",)}
    for board, items in boards.items():
        columns = parse_frontmatter(ORG_ROOT / "templates" / "kanbans" / f"{board}{TEMPLATE_SUFFIX}")["columns"]
        for item in items:  # an enabler flows through the same board as its business sibling
            assert [column["state"] for column in columns] == SCHEMAS[item]["properties"]["status"]["enum"], (board, item)
