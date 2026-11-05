#!/usr/bin/env python3
"""Render the GitHub Copilot app / Copilot CLI plugin bundle from the host-agnostic source.

usage: render_bundle.py <source-root> <bundle-root>

The bundle is a Copilot CLI plugin directory (legacy manifest layout):

    <bundle>/plugin.json             manifest; `agents: agents/`, `skills: skills/`
    <bundle>/agents/<slug>.agent.md  CLI `tools:` aliases + this host's binding section
    <bundle>/skills/<stem>/SKILL.md  one folder per source skill, `name` = file stem
    <bundle>/skills/<stem>.skill.md  the flat source skills, kept so the bundle stays a valid
                                     FRAMEWORK_DIR (the harness resolves skills by file stem)
    <bundle>/{workflows,conf,...}    the framework layout named by `.env`
    <bundle>/.github/plugin/marketplace.json
                                     a one-plugin local marketplace, so the app loads the bundle
                                     live from this directory (no copy, no reinstall after the
                                     harness writes its hooks)

The harness installer runs second and writes `<bundle>/hooks.json` plus an agent-scoped
`hooks:` block in each orchestrator's frontmatter; this renderer therefore never emits either.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import shutil
import sys
import uuid
from pathlib import Path

import yaml

BUILD = Path("builds") / "github-copilot-cli"
LAYOUT_FILES = (".env", "LICENSE", "NOTICE", "README.md")
MANIFEST_KEYS = ("name", "version", "description", "author", "license", "repository", "keywords", "agents", "skills")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
LEADING_COMMENT_RE = re.compile(r"\A\s*<!--.*?-->\s*", re.DOTALL)
MARKETPLACE = Path(".github") / "plugin" / "marketplace.json"


def marketplace_name(plugin_name: str) -> str:
    return f"{plugin_name}-local"


class RenderError(Exception):
    """A source or build input the renderer refuses to guess around."""


def _split_frontmatter(text: str, path: Path) -> tuple[list[str], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise RenderError(f"missing YAML frontmatter: {path}")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "".join(lines[index + 1 :])
    raise RenderError(f"frontmatter is not closed: {path}")


def _set_key(frontmatter: list[str], key: str, rendered: str) -> list[str]:
    """Replace a top-level `key:` line (or append it) with `rendered`."""
    out = list(frontmatter)
    for index, line in enumerate(out):
        if line.startswith(f"{key}:"):
            out[index] = rendered
            return out
    out.append(rendered)
    return out


def _join(frontmatter: list[str], body: str) -> str:
    return "---\n" + "".join(frontmatter) + "---\n" + body


def _layout_dirs(source_root: Path) -> list[str]:
    """Framework directories named by `.env` (minus the workspace) plus `conf`."""
    env_path = source_root / ".env"
    if not env_path.is_file():
        raise RenderError(f"missing framework layout file: {env_path}")
    dirs = {"conf"}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key.startswith("FRAMEWORK_") and key.endswith("_DIR") and key != "FRAMEWORK_WORKSPACE_DIR":
            dirs.add(value.strip("'\""))
    return sorted(dirs)


def _load_manifest(build_root: Path) -> dict:
    manifest = json.loads((build_root / "plugin.json").read_text(encoding="utf-8"))
    name = manifest.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        raise RenderError(f"plugin name must be kebab-case, at most 64 characters: {name!r}")
    if manifest.get("agents") != "agents/" or manifest.get("skills") != "skills/":
        raise RenderError("plugin.json must declare `agents: agents/` and `skills: skills/`")
    if "hooks" in manifest:
        raise RenderError("plugin.json must not declare hooks: the harness installer writes <bundle>/hooks.json")
    return {key: manifest[key] for key in MANIFEST_KEYS if key in manifest}


def _load_tools(build_root: Path, source_root: Path) -> dict[str, list[str]]:
    tools_map = (yaml.safe_load((build_root / "tools.yaml").read_text(encoding="utf-8")) or {}).get("agents") or {}
    if not isinstance(tools_map, dict):
        raise RenderError("tools.yaml `agents` must be a mapping of agent path to tool list")
    sources = {f"agents/{path.name}" for path in (source_root / "agents").glob("*.agent.md")}
    missing = sorted(sources - set(tools_map))
    extra = sorted(set(tools_map) - sources)
    if missing or extra:
        details = [f"  - missing tools map entry: {rel}" for rel in missing]
        details += [f"  - tools map names no source agent: {rel}" for rel in extra]
        raise RenderError("tools.yaml does not match agents/:\n" + "\n".join(details))
    invalid = _invalid_tools(tools_map)
    if invalid:
        raise RenderError("tools.yaml entries must be lists of tool names:\n" + "\n".join(f"  - {rel}" for rel in invalid))
    return {rel: list(tools) for rel, tools in tools_map.items()}


def _invalid_tools(agent_tools: dict) -> list[str]:
    """Tools-map entries that are not a list of tool names (a blank entry parses as None)."""
    return sorted(
        rel for rel, tools in agent_tools.items() if not isinstance(tools, list) or not all(isinstance(t, str) and t for t in tools)
    )


def _binding(build_root: Path, plugin: str, agent_ids: list[str]) -> str:
    """The host binding, with plugin agents namespaced as the CLI dispatches them (`<plugin>:<agent>`)."""
    text = (build_root / "host-binding.md").read_text(encoding="utf-8")
    text = LEADING_COMMENT_RE.sub("", text, count=1)
    text = text.replace("{{AGENT_IDS}}", ", ".join(f"`{plugin}:{slug}`" for slug in agent_ids))
    return text.replace("{{PLUGIN_NAME}}", plugin)


def _rewrite_links(body: str, source_rel: str, bundle_rel: str, layout: list[str], skills: set[str]) -> str:
    """Re-anchor relative links from a file's source location to its bundle location."""
    source_dir = posixpath.dirname(source_rel)
    bundle_dir = posixpath.dirname(bundle_rel)

    def target_of(raw: str) -> str | None:
        path = raw.split("#", 1)[0]
        if not path or "://" in raw or raw.startswith(("#", "/", "mailto:")):
            return None
        name = posixpath.basename(path)
        if name.endswith(".skill.md") and name[: -len(".skill.md")] in skills:
            return f"skills/{name[: -len('.skill.md')]}/SKILL.md"
        resolved = posixpath.normpath(posixpath.join(source_dir, path))
        if resolved.split("/", 1)[0] in layout:
            return resolved
        return None

    def replace(match: re.Match[str]) -> str:
        raw = match.group(2)
        target = target_of(raw)
        if target is None:
            return match.group(0)
        anchor = "#" + raw.split("#", 1)[1] if "#" in raw else ""
        return f"{match.group(1)}{posixpath.relpath(target, bundle_dir or '.')}{anchor}{match.group(3)}"

    return LINK_RE.sub(replace, body)


def render(source_root: Path, bundle_root: Path) -> tuple[int, int]:
    build_root = source_root / BUILD
    manifest = _load_manifest(build_root)
    tools = _load_tools(build_root, source_root)
    layout = _layout_dirs(source_root)
    skill_paths = sorted((source_root / "skills").glob("*.skill.md"))
    skills = {path.name[: -len(".skill.md")] for path in skill_paths}
    agent_ids = sorted(Path(rel).name[: -len(".agent.md")] for rel in tools)
    binding = _binding(build_root, manifest["name"], agent_ids)

    staging = _staging_path(bundle_root)
    staging.mkdir(parents=True)
    try:
        _write_bundle(source_root, staging, manifest, tools, layout, skill_paths, skills, binding)
        _replace(staging, bundle_root)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return len(tools), len(skill_paths)


def _write_bundle(
    source_root: Path,
    bundle_root: Path,
    manifest: dict,
    tools: dict[str, list[str]],
    layout: list[str],
    skill_paths: list[Path],
    skills: set[str],
    binding: str,
) -> None:
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")
    for name in layout:
        if (source_root / name).is_dir():
            shutil.copytree(source_root / name, bundle_root / name, ignore=ignore)
    for name in LAYOUT_FILES:
        if (source_root / name).is_file():
            shutil.copy2(source_root / name, bundle_root / name)
    (bundle_root / "agents").mkdir(exist_ok=True)

    for rel, agent_tools in sorted(tools.items()):
        path = source_root / rel
        slug = path.name[: -len(".agent.md")]
        frontmatter, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        meta = yaml.safe_load("".join(frontmatter)) or {}
        if meta.get("name") != slug or not meta.get("description"):
            raise RenderError(f"agent frontmatter needs `name: {slug}` and a description: {rel}")
        if "hooks" in meta:
            raise RenderError(f"source agent declares hooks (the harness installer owns them): {rel}")
        frontmatter = _set_key(frontmatter, "tools", f"tools: [{', '.join(agent_tools)}]\n")
        body = _rewrite_links(body, rel, rel, layout, skills).rstrip("\n") + "\n\n" + binding
        (bundle_root / rel).write_text(_join(frontmatter, body), encoding="utf-8")

    for path in skill_paths:
        stem = path.name[: -len(".skill.md")]
        rel = f"skills/{path.name}"
        frontmatter, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        meta = yaml.safe_load("".join(frontmatter)) or {}
        description = meta.get("description") or ""
        if not description or len(description) > 1024:
            raise RenderError(f"skill description must be 1..1024 characters: {rel}")
        frontmatter = _set_key(frontmatter, "name", f"name: {stem}\n")
        target = bundle_root / "skills" / stem / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        body = _rewrite_links(body, rel, f"skills/{stem}/SKILL.md", layout, skills)
        target.write_text(_join(frontmatter, body), encoding="utf-8")

    _write_json(bundle_root / "plugin.json", manifest)
    _write_json(bundle_root / MARKETPLACE, _marketplace(manifest))


def _staging_path(bundle_root: Path) -> Path:
    """A sibling of the bundle root, so the finished render replaces it with a rename."""
    return bundle_root.parent / f".{bundle_root.name}.render-{uuid.uuid4().hex}"


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


def _marketplace(manifest: dict) -> dict:
    entry = {key: manifest[key] for key in ("name", "description", "version", "author") if key in manifest}
    entry["source"] = "."
    return {
        "name": marketplace_name(manifest["name"]),
        "owner": manifest.get("author", {"name": manifest["name"]}),
        "metadata": {"description": "Local marketplace for a rendered bundle", "version": manifest.get("version", "0.0.0")},
        "plugins": [entry],
    }


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_bundle.py <source-root> <bundle-root>", file=sys.stderr)
        return 2
    source_root = Path(sys.argv[1]).resolve()
    bundle_root = Path(sys.argv[2]).resolve()
    if _unsafe_target(source_root, bundle_root):
        print(f"refusing to replace {bundle_root}: not an earlier rendered bundle", file=sys.stderr)
        return 2
    try:
        agents, skills = render(source_root, bundle_root)
        plugin = json.loads((bundle_root / "plugin.json").read_text(encoding="utf-8"))["name"]
    except (RenderError, OSError, ValueError) as error:
        print(f"render failed: {error}", file=sys.stderr)
        return 1
    print(f"rendered GitHub Copilot CLI bundle: {bundle_root} ({agents} agents, {skills} skills)")
    print("next: 1) harness hook install, with the harness venv python:"
          " <venv python> <harness>/adapters/github-copilot-cli/install.py"
          f" --framework-dir <org checkout> --bundle-dir {os.fspath(bundle_root)} [--workspace-dir <portfolio>]")
    print(f"      2) copilot plugin marketplace add {os.fspath(bundle_root)}")
    print(f"      3) copilot plugin install {plugin}@{marketplace_name(plugin)}")
    return 0


def _unsafe_target(source_root: Path, bundle_root: Path) -> bool:
    """The bundle root is replaced: refuse the source, its ancestors, its `builds` subtree (the
    checked-in build inputs carry a `plugin.json` too), and any existing path that is not an
    earlier rendered bundle (a directory with `plugin.json` at its root)."""
    if bundle_root == source_root or bundle_root in source_root.parents:
        return True
    builds = source_root / BUILD.parts[0]
    if bundle_root == builds or builds in bundle_root.parents:
        return True
    if not bundle_root.exists():
        return False
    return not (bundle_root.is_dir() and (bundle_root / "plugin.json").is_file())


if __name__ == "__main__":
    raise SystemExit(main())
