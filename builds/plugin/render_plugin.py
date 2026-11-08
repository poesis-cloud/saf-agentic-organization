#!/usr/bin/env python3
"""Render the GitHub Copilot plugin (Agent Plugins 1.0) from the host-agnostic source.

usage: render_plugin.py <source-root> <plugin-root>

One plugin for every GitHub Copilot host (the Copilot CLI, the GitHub Copilot app, VS Code with
Session Target: Copilot). The plugin root is the framework root the harness registry records
(`frameworks/<name>/root`), so it holds the framework's `.env` and `conf/`:

    <plugin>/plugin.json                          the closed Agent Plugins 1.0 manifest
    <plugin>/.env                                 the framework layout, every directory under framework/
    <plugin>/conf/                                the framework configuration (harness.conf.yaml included)
    <plugin>/framework/{agents,artifacts,instructions,skills,templates,workflows}/
                                                  the framework layout the harness reads
    <plugin>/com.github.copilot/agents/<slug>.agent.md
                                                  Copilot `tools:`, this host's binding; the
                                                  orchestrators carry the scoped H0 hooks
    <plugin>/com.github.copilot/hooks/hooks.json  sessionStart: the shell-only registration
    <plugin>/bin/register.{sh,ps1}                the registration (`frameworks/<name>/root`)
    <plugin>/skills/<stem>/SKILL.md               one Agent Skill per source skill, plus `init`

The harness itself ships as its own plugin (`poesis-saf-agentic-harness`); the orchestrators'
scoped H0 entries reach it through the stable per-user launcher in the SAF registry.
"""

from __future__ import annotations

import filecmp
import json
import os
import posixpath
import re
import shutil
import sys
import uuid
from pathlib import Path

import yaml

BUILD = Path("builds") / "plugin"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MANIFEST_KEYS = (
    "$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions",
)
AUTHOR_KEYS = ("name", "email", "url")
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
LEADING_COMMENT_RE = re.compile(r"\A\s*<!--.*?-->\s*", re.DOTALL)
ROOT_FILES = ("LICENSE", "NOTICE", "README.md")
FRAMEWORK = "framework"
EXTENSION = "com.github.copilot"
AGENTS = f"{EXTENSION}/agents"
HOOKS_FILE = Path(EXTENSION) / "hooks" / "hooks.json"
REGISTER_TIMEOUT = 30
H0_EVENTS = ("userPromptSubmitted", "userPromptTransformed")
H0_TIMEOUT = 120
POSIX_LAUNCHER = '"${SAF_AGENTIC_REGISTRY_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/saf-agentic/registry}/harness/launcher.sh"'
WINDOWS_LAUNCHER = (
    "\"$(if ($env:SAF_AGENTIC_REGISTRY_DIR) { $env:SAF_AGENTIC_REGISTRY_DIR } "
    "else { Join-Path $env:LOCALAPPDATA 'saf-agentic\\registry' })\\harness\\launcher.ps1\""
)
WORKSPACE_ROOT = "portfolio"


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


def _invalid_tools(agent_tools: dict) -> list[str]:
    """Tools-map entries that are not a list of tool names (a blank entry parses as None)."""
    return sorted(
        rel for rel, tools in agent_tools.items() if not isinstance(tools, list) or not all(isinstance(t, str) and t for t in tools)
    )

def _layout(source_root: Path) -> tuple[list[str], str]:
    """The framework directories `.env` names (minus the workspace), and the plugin's `.env`:
    every layout directory re-anchored under `framework/`, the workspace kept (plugin mode
    resolves the governed workspace from the session's marker, never from the layout)."""
    env_path = source_root / ".env"
    if not env_path.is_file():
        raise RenderError(f"missing framework layout file: {env_path}")
    dirs: set[str] = set()
    lines = ["# Framework layout of this plugin (rendered by builds/plugin): the harness resolves every\n",
             "# directory against the plugin root; the workspace comes from the session's marker.\n"]
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        value = value.strip("'\"")
        if key.startswith("FRAMEWORK_") and key.endswith("_DIR") and key != "FRAMEWORK_WORKSPACE_DIR":
            if value.startswith(("/", "..")) or value in ("", ".", "conf"):
                raise RenderError(f"layout directory must be a relative child of the source: {key}={value}")
            dirs.add(value)
            value = f"{FRAMEWORK}/{value}"
        lines.append(f"{key}={value}\n")
    return sorted(dirs), "".join(lines)


def _load_manifest(build_root: Path) -> dict:
    manifest = json.loads((build_root / "plugin.json").read_text(encoding="utf-8"))
    extra = sorted(set(manifest) - set(MANIFEST_KEYS))
    if extra:
        raise RenderError(f"plugin.json is a closed Agent Plugins 1.0 manifest; unknown keys: {', '.join(extra)}")
    if manifest.get("$schema") != SCHEMA:
        raise RenderError(f"plugin.json must declare `$schema: {SCHEMA}`")
    name = manifest.get("name", "")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        raise RenderError(f"plugin name must match the Agent Plugins name rule, at most 64 characters: {name!r}")
    author = manifest.get("author", {})
    if not isinstance(author, dict) or set(author) - set(AUTHOR_KEYS):
        raise RenderError("plugin.json `author` admits only name, email and url")
    return manifest


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


def _orchestrators(source_root: Path, layout: list[str]) -> list[str]:
    """Every `orchestrator:` a workflow configuration names (the harness's own rule)."""
    found: set[str] = set()
    for folder in layout:
        for path in (source_root / folder).rglob("*.workflow.conf.yaml"):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if isinstance(data, dict) and isinstance(data.get("orchestrator"), str):
                found.add(data["orchestrator"])
    return sorted(found)


def _substitute(text: str, plugin: str, orchestrators: list[str]) -> str:
    text = text.replace("{{PLUGIN_NAME}}", plugin).replace("{{WORKSPACE_ROOT}}", WORKSPACE_ROOT)
    return text.replace("{{ORCHESTRATORS}}", ", ".join(f"{plugin}:{slug}" for slug in orchestrators))


def _binding(build_root: Path, plugin: str, agent_ids: list[str]) -> str:
    """The host binding, with plugin agents namespaced as the host dispatches them (`<plugin>:<agent>`)."""
    text = (build_root / "host-binding.md").read_text(encoding="utf-8")
    text = LEADING_COMMENT_RE.sub("", text, count=1)
    text = text.replace("{{AGENT_IDS}}", ", ".join(f"`{plugin}:{slug}`" for slug in agent_ids))
    return text.replace("{{PLUGIN_NAME}}", plugin)


def scoped_hooks(plugin: str, slug: str) -> dict[str, list[dict]]:
    """The orchestrator's scoped H0 entries: the harness's stable per-user launcher, verbatim
    from the harness adapter spec (Plugin mode: The registry, The framework's scoped H0)."""
    hooks: dict[str, list[dict]] = {}
    for event in H0_EVENTS:
        arguments = f"{event} --framework {plugin} --agent {slug}"
        hooks[event] = [
            {
                "type": "command",
                "command": f"sh {POSIX_LAUNCHER} {arguments}",
                "windows": f"& {WINDOWS_LAUNCHER} {arguments}",
                "timeoutSec": H0_TIMEOUT,
            }
        ]
    return hooks


def render_hooks() -> dict:
    """The plugin's global hooks: the shell-only `sessionStart` registration, nothing else."""
    return {
        "version": 1,
        "hooks": {
            "sessionStart": [
                {
                    "type": "command",
                    "bash": 'sh "$PLUGIN_ROOT/bin/register.sh"',
                    "powershell": (
                        "powershell -NoProfile -ExecutionPolicy Bypass -File "
                        '"$env:PLUGIN_ROOT\\bin\\register.ps1"; exit $LASTEXITCODE'
                    ),
                    "timeoutSec": REGISTER_TIMEOUT,
                }
            ]
        },
    }


def _rewrite_links(body: str, source_rel: str, bundle_rel: str, layout: list[str], skills: set[str]) -> str:
    """Re-anchor relative links from a file's source location to its plugin location."""
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
        top = resolved.split("/", 1)[0]
        if top in layout:
            return f"{FRAMEWORK}/{resolved}"
        if top == "conf":
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


def _hooks_block(hooks: dict) -> str:
    return yaml.safe_dump({"hooks": hooks}, sort_keys=False, default_flow_style=False, allow_unicode=True, width=2**31 - 1)


def render(source_root: Path, plugin_root: Path) -> tuple[int, int]:
    build_root = source_root / BUILD
    manifest = _load_manifest(build_root)
    tools = _load_tools(build_root, source_root)
    layout, env = _layout(source_root)
    orchestrators = _orchestrators(source_root, layout)
    skill_paths = sorted((source_root / "skills").glob("*.skill.md"))
    skills = {path.name[: -len(".skill.md")] for path in skill_paths}
    extra_skills = sorted(path.parent for path in (build_root / "skills").glob("*/SKILL.md"))
    clash = sorted(skills & {path.name for path in extra_skills})
    if clash:
        raise RenderError(f"build skills shadow source skills: {', '.join(clash)}")
    agent_ids = sorted(Path(rel).name[: -len(".agent.md")] for rel in tools)
    unknown = sorted(set(orchestrators) - set(agent_ids))
    if unknown:
        raise RenderError(f"workflows name orchestrators with no agent: {', '.join(unknown)}")
    binding = _binding(build_root, manifest["name"], agent_ids)

    staging = _staging_path(plugin_root)
    staging.mkdir(parents=True)
    try:
        _copy_framework(source_root, staging, layout, env)
        _write_agents(source_root, staging, manifest["name"], tools, orchestrators, layout, skills, binding)
        _write_skills(source_root, staging, skill_paths, extra_skills, layout, skills, manifest["name"], orchestrators)
        _write_plugin_files(build_root, staging, manifest)
        _promote(staging, plugin_root)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return len(tools), len(skill_paths) + len(extra_skills)


def _copy_framework(source_root: Path, plugin_root: Path, layout: list[str], env: str) -> None:
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")
    for name in layout:
        if (source_root / name).is_dir():
            shutil.copytree(source_root / name, plugin_root / FRAMEWORK / name, ignore=ignore)
    if not (source_root / "conf").is_dir():
        raise RenderError(f"missing framework configuration: {source_root / 'conf'}")
    shutil.copytree(source_root / "conf", plugin_root / "conf", ignore=ignore)
    for name in ROOT_FILES:
        if (source_root / name).is_file():
            shutil.copy2(source_root / name, plugin_root / name)
    (plugin_root / ".env").write_text(env, encoding="utf-8")


def _write_agents(
    source_root: Path,
    plugin_root: Path,
    plugin: str,
    tools: dict[str, list[str]],
    orchestrators: list[str],
    layout: list[str],
    skills: set[str],
    binding: str,
) -> None:
    (plugin_root / AGENTS).mkdir(parents=True, exist_ok=True)
    for rel, agent_tools in sorted(tools.items()):
        path = source_root / rel
        slug = path.name[: -len(".agent.md")]
        frontmatter, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        meta = yaml.safe_load("".join(frontmatter)) or {}
        if meta.get("name") != slug or not meta.get("description"):
            raise RenderError(f"agent frontmatter needs `name: {slug}` and a description: {rel}")
        if "hooks" in meta:
            raise RenderError(f"source agent declares hooks (the renderer owns them): {rel}")
        frontmatter = _set_key(frontmatter, "tools", f"tools: [{', '.join(agent_tools)}]\n")
        if slug in orchestrators:
            frontmatter.append(_hooks_block(scoped_hooks(plugin, slug)))
        target = f"{AGENTS}/{path.name}"
        body = _rewrite_links(body, rel, target, layout, skills).rstrip("\n") + "\n\n" + binding
        (plugin_root / target).write_text(_join(frontmatter, body), encoding="utf-8")


def _write_skills(
    source_root: Path,
    plugin_root: Path,
    skill_paths: list[Path],
    extra_skills: list[Path],
    layout: list[str],
    skills: set[str],
    plugin: str,
    orchestrators: list[str],
) -> None:
    for path in skill_paths:
        stem = path.name[: -len(".skill.md")]
        rel = f"skills/{path.name}"
        frontmatter, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        target = plugin_root / "skills" / stem / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        body = _rewrite_links(body, rel, f"skills/{stem}/SKILL.md", layout, skills)
        target.write_text(_join(_skill_frontmatter(frontmatter, stem, rel), body), encoding="utf-8")
    for folder in extra_skills:
        path = folder / "SKILL.md"
        frontmatter, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        _skill_frontmatter(frontmatter, folder.name, str(path))
        target = plugin_root / "skills" / folder.name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_substitute(_join(frontmatter, body), plugin, orchestrators), encoding="utf-8")


def _skill_frontmatter(frontmatter: list[str], stem: str, where: str) -> list[str]:
    """Agent Skills: `name` is the folder name; the description is 1..1024 characters."""
    if not SKILL_NAME_RE.match(stem) or len(stem) > 64:
        raise RenderError(f"skill name must be lowercase kebab-case, at most 64 characters: {where}")
    meta = yaml.safe_load("".join(frontmatter)) or {}
    description = meta.get("description") or ""
    if not description or len(description) > 1024:
        raise RenderError(f"skill description must be 1..1024 characters: {where}")
    return _set_key(frontmatter, "name", f"name: {stem}\n")


def _write_plugin_files(build_root: Path, plugin_root: Path, manifest: dict) -> None:
    plugin = manifest["name"]
    for script in ("register.sh", "register.ps1"):
        text = (build_root / "bin" / script).read_text(encoding="utf-8").replace("{{PLUGIN_NAME}}", plugin)
        target = plugin_root / "bin" / script
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n" if script.endswith(".sh") else None)
        if script.endswith(".sh"):
            target.chmod(0o755)
    _write_json(plugin_root / HOOKS_FILE, render_hooks())
    _write_json(plugin_root / "plugin.json", manifest)


def _staging_path(bundle_root: Path) -> Path:
    """A sibling of the bundle root, so the finished render replaces it with a rename."""
    return bundle_root.parent / f".{bundle_root.name}.render-{uuid.uuid4().hex}"


def _promote(staging: Path, bundle_root: Path) -> None:
    """Move a complete render into place. A new bundle root is the renamed staging directory; an
    existing one is updated in place and never renamed, because a host that loads the bundle live
    (the Copilot CLI local marketplace) keeps it open and Windows refuses to rename an open
    directory: changed files are replaced, new ones added, and stale ones removed."""
    if not bundle_root.exists():
        staging.rename(bundle_root)
        return
    rendered: set[Path] = set()
    for root, dirs, files in os.walk(staging):
        rel_root = Path(root).relative_to(staging)
        for name in dirs:
            rendered.add(rel_root / name)
            target = bundle_root / rel_root / name
            if target.is_symlink() or target.is_file():
                target.unlink()
            target.mkdir(exist_ok=True)
        for name in files:
            rendered.add(rel_root / name)
            source, target = Path(root, name), bundle_root / rel_root / name
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
            elif target.is_file() and filecmp.cmp(source, target, shallow=False):
                continue
            os.replace(source, target)
    for root, dirs, files in os.walk(bundle_root, topdown=False):
        rel_root = Path(root).relative_to(bundle_root)
        for name in files:
            if rel_root / name not in rendered:
                Path(root, name).unlink()
        for name in dirs:
            path = Path(root, name)
            if rel_root / name not in rendered:
                path.unlink() if path.is_symlink() else shutil.rmtree(path)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_plugin.py <source-root> <plugin-root>", file=sys.stderr)
        return 2
    source_root = Path(sys.argv[1]).resolve()
    plugin_root = Path(sys.argv[2]).resolve()
    if _unsafe_target(source_root, plugin_root):
        print(f"refusing to replace {plugin_root}: not an earlier rendered plugin", file=sys.stderr)
        return 2
    try:
        agents, skills = render(source_root, plugin_root)
    except (RenderError, OSError, ValueError) as error:
        print(f"render failed: {error}", file=sys.stderr)
        return 1
    print(f"rendered GitHub Copilot plugin: {plugin_root} ({agents} agents, {skills} skills)")
    return 0


def _unsafe_target(source_root: Path, plugin_root: Path) -> bool:
    """The plugin root is replaced: refuse the source, its ancestors, its `builds` subtree (the
    checked-in build inputs carry a `plugin.json` too), and any existing path that is not an
    earlier rendered plugin (a directory with `plugin.json` at its root)."""
    if plugin_root == source_root or plugin_root in source_root.parents:
        return True
    builds = source_root / BUILD.parts[0]
    if plugin_root == builds or builds in plugin_root.parents:
        return True
    if not plugin_root.exists():
        return False
    return not (plugin_root.is_dir() and (plugin_root / "plugin.json").is_file())


if __name__ == "__main__":
    raise SystemExit(main())
