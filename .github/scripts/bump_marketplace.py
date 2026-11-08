#!/usr/bin/env python3
"""Point a marketplace catalogue's organization plugin entry at a released plugin commit.

    python .github/scripts/bump_marketplace.py <marketplace.json> <marketplace name> \
        <version> <ref> <sha>

Creates the catalogue, or the plugin entry, when absent; otherwise bumps the entry's
`version` and its GitHub `source` (`ref`, `sha`) and refreshes its description, license and
keywords from the plugin manifest, leaving everything else as it was.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPOSITORY = "poesis-cloud/saf-agentic-organization"
MANIFEST = Path(__file__).resolve().parents[2] / "builds" / "plugin" / "plugin.json"


def bump(path: Path, marketplace: str, version: str, ref: str, sha: str, manifest: Path = MANIFEST) -> dict:
    plugin = json.loads(manifest.read_text(encoding="utf-8"))
    if path.is_file():
        catalogue = json.loads(path.read_text(encoding="utf-8"))
    else:
        catalogue = {"name": marketplace, "owner": {"name": "Poesis SAS"}, "plugins": []}
    plugins = catalogue.setdefault("plugins", [])
    entry = next((item for item in plugins if item.get("name") == plugin["name"]), None)
    if entry is None:
        entry = {"name": plugin["name"]}
        plugins.append(entry)
    entry["version"] = version
    entry["description"] = plugin["description"]
    entry["source"] = {"source": "github", "repo": REPOSITORY, "ref": ref, "sha": sha}
    entry["license"] = plugin["license"]
    entry["keywords"] = list(plugin.get("keywords", []))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalogue, indent=2) + "\n", encoding="utf-8")
    return catalogue


def main(arguments: list[str]) -> int:
    if len(arguments) != 5 or len(arguments[4]) != 40:
        print(__doc__, file=sys.stderr)
        return 2
    bump(Path(arguments[0]), *arguments[1:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
