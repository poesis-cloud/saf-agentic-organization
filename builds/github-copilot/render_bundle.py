#!/usr/bin/env python3
"""Render the GitHub Copilot bundle from host-agnostic source agents."""

from __future__ import annotations

import json
import shutil
import sys
import uuid
from pathlib import Path

import yaml

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "dist", "target"}


def _ignore(_root: str, names: list[str]) -> set[str]:
    return {name for name in names if name in SKIP_DIRS}


def _inject_tools(agent_path: Path, tools: list[str]) -> None:
    lines = agent_path.read_text().splitlines(keepends=True)
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError(f"agent file lacks YAML frontmatter: {agent_path}")

    frontmatter_end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            frontmatter_end = index
            break
    if frontmatter_end is None:
        raise ValueError(f"agent frontmatter is not closed: {agent_path}")

    rendered = f"tools: [{', '.join(tools)}]\n"
    for index in range(1, frontmatter_end):
        if lines[index].startswith("tools:"):
            lines[index] = rendered
            break
    else:
        lines.insert(frontmatter_end, rendered)

    agent_path.write_text("".join(lines))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_bundle.py <source-root> <bundle-root>", file=sys.stderr)
        return 2

    source_root = Path(sys.argv[1]).resolve()
    bundle_root = Path(sys.argv[2]).resolve()
    build_root = source_root / "builds" / "github-copilot"
    manifest_path = build_root / "plugin.json"
    tools_map_path = build_root / "tools.yaml"

    if _unsafe_target(source_root, bundle_root):
        print(f"refusing to replace {bundle_root}: not an earlier rendered bundle", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text())
    tools_map = yaml.safe_load(tools_map_path.read_text()) or {}
    agent_tools = tools_map.get("agents") or {}
    if not isinstance(agent_tools, dict):
        print("tools map `agents` must be a mapping of agent path to tool list", file=sys.stderr)
        return 1

    missing = [rel for rel in manifest.get("agents", []) if rel not in agent_tools]
    extra = sorted(set(agent_tools) - set(manifest.get("agents", [])))
    invalid = _invalid_tools(agent_tools)
    if missing or extra or invalid:
        if missing:
            print("missing tools map entries:", file=sys.stderr)
            for rel in missing:
                print(f"  - {rel}", file=sys.stderr)
        if extra:
            print("tools map contains non-manifest agents:", file=sys.stderr)
            for rel in extra:
                print(f"  - {rel}", file=sys.stderr)
        if invalid:
            print("tools map entries must be lists of tool names:", file=sys.stderr)
            for rel in invalid:
                print(f"  - {rel}", file=sys.stderr)
        return 1

    staging = bundle_root.parent / f".{bundle_root.name}.render-{uuid.uuid4().hex}"
    try:
        staging.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_root, staging, ignore=_ignore_except(staging))
        for rel in manifest.get("agents", []):
            _inject_tools(staging / rel, list(agent_tools[rel]))
        (staging / "plugin.json").write_text(manifest_path.read_text())
        _replace(staging, bundle_root)
    except (OSError, ValueError) as error:
        print(f"render failed: {error}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    print(f"rendered GitHub Copilot bundle: {bundle_root}")
    return 0


def _invalid_tools(agent_tools: dict) -> list[str]:
    """Tools-map entries that are not a list of tool names (a blank entry parses as None)."""
    return sorted(
        rel for rel, tools in agent_tools.items() if not isinstance(tools, list) or not all(isinstance(t, str) and t for t in tools)
    )


def _ignore_except(staging: Path):
    """`_ignore`, plus the staging directory itself when it sits inside the source."""

    def ignore(root: str, names: list[str]) -> set[str]:
        return _ignore(root, names) | {name for name in names if Path(root, name) == staging}

    return ignore


def _replace(staging: Path, bundle_root: Path) -> None:
    """Swap a complete render in for the bundle root; the earlier bundle is removed only after."""
    if not bundle_root.exists():
        staging.rename(bundle_root)
        return
    retired = bundle_root.parent / f".{bundle_root.name}.retired-{uuid.uuid4().hex}"
    bundle_root.rename(retired)
    try:
        staging.rename(bundle_root)
    except BaseException:
        retired.rename(bundle_root)
        raise
    shutil.rmtree(retired)


def _unsafe_target(source_root: Path, bundle_root: Path) -> bool:
    """The bundle root is replaced: refuse the source, its ancestors, any path inside the source
    that the copy would include (its `builds` subtree among them; generated directories such as
    `dist` are skipped and stay allowed), and any existing path that is not an earlier rendered
    bundle (a directory with `plugin.json` at its root)."""
    if bundle_root == source_root or bundle_root in source_root.parents:
        return True
    if source_root in bundle_root.parents and bundle_root.relative_to(source_root).parts[0] not in SKIP_DIRS:
        return True
    if not bundle_root.exists():
        return False
    return not (bundle_root.is_dir() and (bundle_root / "plugin.json").is_file())


if __name__ == "__main__":
    raise SystemExit(main())