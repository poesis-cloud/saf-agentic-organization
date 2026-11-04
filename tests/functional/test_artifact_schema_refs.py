"""Every artifact schema `$ref` resolves against what the harness actually compiles.

The harness's `check-step-artifact` validates against a registry of its own `contracts/`
plus this organization's `*.artifact.schema.json` files — nothing else. A `$ref` to any
other `$id` raises `Unresolvable` at validation time, so it is caught here instead.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

import pytest
from referencing.exceptions import Unresolvable

from tests.conftest import HARNESS_SRC, ORG_ROOT

from utils.schema_validator import SchemaValidator

CONTRACTS = HARNESS_SRC.parent / "contracts"
ARTIFACTS = ORG_ROOT / "artifacts"
SCHEMAS = sorted(ARTIFACTS.rglob("*.artifact.schema.json"))
DEFINITIONS = json.loads((ARTIFACTS / "framework-definitions.schema.json").read_text(encoding="utf-8"))["definitions"]


def _refs(node: Any) -> Iterator[str]:
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            yield node["$ref"]
        for value in node.values():
            yield from _refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from _refs(value)


@pytest.fixture(scope="module")
def validator() -> SchemaValidator:
    return SchemaValidator.compile_contracts([*sorted(CONTRACTS.rglob("*.schema.json")), *SCHEMAS])


def test_harness_contracts_declare_the_referenced_ids() -> None:
    ids = {json.loads(path.read_text(encoding="utf-8")).get("$id") for path in CONTRACTS.rglob("*.schema.json")}
    assert {"gsmarc://saf/contracts/artifact/v1", "gsmarc://saf/contracts/slugs/v1"} <= ids


@pytest.mark.parametrize("path", SCHEMAS, ids=lambda path: path.name)
def test_every_ref_resolves_against_harness_registry(validator: SchemaValidator, path: Path) -> None:
    schema = json.loads(path.read_text(encoding="utf-8"))
    resolver = validator._registry.resolver(base_uri=schema["$id"])
    unresolved: list[str] = []
    for ref in _refs(schema):
        try:
            resolver.lookup(ref)
        except Unresolvable:
            unresolved.append(ref)
    assert unresolved == []
    assert schema.get("$ref") == "gsmarc://saf/contracts/artifact/v1"


@pytest.mark.parametrize("path", SCHEMAS, ids=lambda path: path.name)
def test_inlined_framework_definitions_match_the_canonical_file(path: Path) -> None:
    schema = json.loads(path.read_text(encoding="utf-8"))
    used = {ref[len("#/$defs/") :] for ref in _refs(schema) if ref.startswith("#/$defs/")}
    inlined = schema.get("$defs", {})
    assert set(inlined) == used
    for name, definition in inlined.items():
        assert definition == DEFINITIONS[name], name


def test_schema_validation_traverses_without_unresolvable(validator: SchemaValidator) -> None:
    for path in SCHEMAS:
        schema_id = json.loads(path.read_text(encoding="utf-8"))["$id"]
        validator.validate_instance(schema_id, {})


def test_step_outcomes_validate_through_the_harness_registry(validator: SchemaValidator) -> None:
    entry = {"step": "epic-lean-business-case/draft-epic", "outcome": "no-change", "date": "2026-11-05", "note": "Out of scope."}
    for path in SCHEMAS:
        schema_id = json.loads(path.read_text(encoding="utf-8"))["$id"]
        assert not [e for e in validator.validate_instance(schema_id, {"stepOutcomes": [entry]}) if e.path.startswith("/stepOutcomes")]
        bad = validator.validate_instance(schema_id, {"stepOutcomes": [{**entry, "outcome": "skipped"}]})
        assert [e for e in bad if e.path.startswith("/stepOutcomes")], path.name
