"""The CD marketplace bump points the organization plugin entry at a released plugin commit."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from tests.loaders import load_plugin, organization_root

_PATH = organization_root() / ".github" / "scripts" / "bump_marketplace.py"
_SPEC = importlib.util.spec_from_file_location("bump_marketplace", _PATH)
assert _SPEC is not None and _SPEC.loader is not None
bump_marketplace = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(bump_marketplace)

SHA = "a" * 40


def test_bump_creates_then_updates_the_entry(tmp_path: Path) -> None:
    plugin = load_plugin()
    path = tmp_path / ".github" / "plugin" / "marketplace.json"
    assert bump_marketplace.main([str(path), "poesis-saf-preview", "0.1.0-alpha.1", "plugin-v0.1.0-alpha.1", SHA]) == 0
    catalogue = json.loads(path.read_text(encoding="utf-8"))
    assert catalogue["name"] == "poesis-saf-preview"
    assert catalogue["plugins"] == [
        {
            "name": plugin["name"],
            "version": "0.1.0-alpha.1",
            "description": plugin["description"],
            "source": {"source": "github", "repo": "poesis-cloud/saf-agentic-organization", "ref": "plugin-v0.1.0-alpha.1", "sha": SHA},
            "license": "Apache-2.0",
            "keywords": plugin["keywords"],
        }
    ]
    harness = {"name": "poesis-saf-agentic-harness", "version": "1.0.0"}
    catalogue["plugins"].insert(0, harness)
    path.write_text(json.dumps(catalogue), encoding="utf-8")
    bump_marketplace.bump(path, "ignored", "0.1.0", "plugin-v0.1.0", "b" * 40)
    catalogue = json.loads(path.read_text(encoding="utf-8"))
    assert catalogue["name"] == "poesis-saf-preview"
    assert catalogue["plugins"][0] == harness
    assert catalogue["plugins"][1]["version"] == "0.1.0"
    assert catalogue["plugins"][1]["source"]["sha"] == "b" * 40


def test_bump_usage() -> None:
    assert bump_marketplace.main(["m.json", "poesis-saf", "0.1.0", "plugin-v0.1.0", "short"]) == 2
