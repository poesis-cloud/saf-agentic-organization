#!/usr/bin/env python3
"""Render the Claude Code plugin from the host-agnostic source.

usage: render_claude_plugin.py <source-root> <plugin-root>

The plugin root is the framework root the harness registry records
(`hosts/claude-code/frameworks/<name>/root`), so it holds the framework's `.env` and `conf/`:

    <plugin>/.claude-plugin/plugin.json   the manifest (name, version, … from builds/plugin)
    <plugin>/.env                         the framework layout, every directory under framework/
    <plugin>/conf/                        the framework configuration (harness.conf.yaml included)
    <plugin>/framework/{agents,artifacts,instructions,skills,templates,workflows}/
                                          the framework layout the harness reads
    <plugin>/agents/<slug>.md             Claude Code `tools:`, this host's binding appended
    <plugin>/hooks/hooks.json             SessionStart: the shell-only registration
    <plugin>/bin/register.sh              the registration (`hosts/claude-code/frameworks/<name>/root`)
    <plugin>/skills/<stem>/SKILL.md       one Agent Skill per source skill, plus `init`

The source, the per-agent tool lists and the manifest are the Copilot build's
(`builds/plugin`): only the host vocabulary (`tools.yaml` aliases), the host binding, the
registration and the `init` skill are Claude Code's own. No hook is agent-scoped: the
harness plugin's global `UserPromptSubmit` reads the orchestrator from the conversation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_COPILOT_BUILD = Path(__file__).resolve().parents[1] / "plugin"
if str(_COPILOT_BUILD) not in sys.path:
    sys.path.insert(0, str(_COPILOT_BUILD))

import render_plugin as shared  # noqa: E402
from render_plugin import RenderError  # noqa: E402

BUILD = Path("builds") / "claude-plugin"
MANIFEST_FILE = Path(".claude-plugin") / "plugin.json"
HOOKS_FILE = Path("hooks") / "hooks.json"
AGENTS = "agents"
REGISTER = "register.sh"
REGISTER_TIMEOUT = 30
MARKETPLACE_REPOSITORY = "poesis-cloud/saf-marketplace"
CLAUDE_MANIFEST_KEYS = (
    "name", "version", "description", "author", "homepage", "repository", "license", "keywords",
)


def render_manifest(source_root: Path) -> dict:
    """The Claude Code manifest: the Copilot build's, without its Agent Plugins keys."""
    manifest = shared._load_manifest(source_root / shared.BUILD)
    return {key: manifest[key] for key in CLAUDE_MANIFEST_KEYS if key in manifest}


def load_tools(source_root: Path) -> dict[str, list[str]]:
    """Per-agent Claude Code tools: the Copilot build's alias lists, translated."""
    aliases = (yaml.safe_load((source_root / BUILD / "tools.yaml").read_text(encoding="utf-8")) or {}).get("aliases")
    if not isinstance(aliases, dict):
        raise RenderError(f"{BUILD / 'tools.yaml'} needs an `aliases` mapping")
    tools: dict[str, list[str]] = {}
    for rel, agent_aliases in shared._load_tools(source_root / shared.BUILD, source_root).items():
        unknown = sorted(set(agent_aliases) - set(aliases))
        if unknown:
            raise RenderError(f"{rel}: no Claude Code tools for alias(es) {', '.join(unknown)}")
        tools[rel] = list(dict.fromkeys(tool for alias in agent_aliases for tool in aliases[alias]))
    return tools


def marketplace(version: str) -> tuple[str, dict]:
    """The SAF marketplace channel a plugin version is published on (the CD's own rule): a
    pre-release (`-alpha`, `-beta`, `-rc`) on `preview`, a final release on `main`."""
    if "-" in version.split("+", 1)[0]:
        return "poesis-saf-preview", {"source": "github", "repo": MARKETPLACE_REPOSITORY, "ref": "preview"}
    return "poesis-saf", {"source": "github", "repo": MARKETPLACE_REPOSITORY}


def _write_marketplace(plugin_root: Path, version: str) -> None:
    """Fill the `init` skill's marketplace placeholders with this version's channel."""
    init = plugin_root / "skills" / "init" / "SKILL.md"
    if not init.is_file():
        return
    name, source = marketplace(version)
    text = init.read_text(encoding="utf-8")
    text = text.replace("{{MARKETPLACE_SOURCE}}", shared.json.dumps(source)).replace("{{MARKETPLACE}}", name)
    init.write_text(text, encoding="utf-8")


def render_hooks() -> dict:
    """The plugin's hooks: the shell-only `SessionStart` registration, nothing else."""
    return {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'sh "${{CLAUDE_PLUGIN_ROOT}}/bin/{REGISTER}"',
                            "timeout": REGISTER_TIMEOUT,
                        }
                    ]
                }
            ]
        }
    }


def render(source_root: Path, plugin_root: Path) -> tuple[int, int]:
    build_root = source_root / BUILD
    manifest = render_manifest(source_root)
    plugin = manifest["name"]
    tools = load_tools(source_root)
    layout, env = shared._layout(source_root)
    orchestrators = shared._orchestrators(source_root, layout)
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
    binding = shared._binding(build_root, plugin, agent_ids)

    staging = shared._staging_path(plugin_root)
    staging.mkdir(parents=True)
    try:
        shared._copy_framework(source_root, staging, layout, env)
        _write_agents(source_root, staging, tools, layout, skills, binding)
        shared._write_skills(
            source_root, staging, skill_paths, extra_skills, layout, skills, plugin, orchestrators
        )
        _write_marketplace(staging, str(manifest.get("version", "")))
        _write_plugin_files(build_root, staging, manifest)
        shared._promote(staging, plugin_root)
    finally:
        shared.shutil.rmtree(staging, ignore_errors=True)
    return len(tools), len(skill_paths) + len(extra_skills)


def _write_agents(
    source_root: Path,
    plugin_root: Path,
    tools: dict[str, list[str]],
    layout: list[str],
    skills: set[str],
    binding: str,
) -> None:
    (plugin_root / AGENTS).mkdir(parents=True, exist_ok=True)
    for rel, agent_tools in sorted(tools.items()):
        path = source_root / rel
        slug = path.name[: -len(".agent.md")]
        frontmatter, body = shared._split_frontmatter(path.read_text(encoding="utf-8"), path)
        meta = yaml.safe_load("".join(frontmatter)) or {}
        if meta.get("name") != slug or not meta.get("description"):
            raise RenderError(f"agent frontmatter needs `name: {slug}` and a description: {rel}")
        if "hooks" in meta:
            raise RenderError(f"source agent declares hooks (the renderer owns them): {rel}")
        frontmatter = shared._set_key(frontmatter, "tools", f"tools: {', '.join(agent_tools)}\n")
        target = f"{AGENTS}/{slug}.md"
        body = shared._rewrite_links(body, rel, target, layout, skills).rstrip("\n") + "\n\n" + binding
        (plugin_root / target).write_text(shared._join(frontmatter, body), encoding="utf-8")


def _write_plugin_files(build_root: Path, plugin_root: Path, manifest: dict) -> None:
    text = (build_root / "bin" / REGISTER).read_text(encoding="utf-8").replace("{{PLUGIN_NAME}}", manifest["name"])
    target = plugin_root / "bin" / REGISTER
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    target.chmod(0o755)
    shared._write_json(plugin_root / HOOKS_FILE, render_hooks())
    shared._write_json(plugin_root / MANIFEST_FILE, manifest)


def _unsafe_target(source_root: Path, plugin_root: Path) -> bool:
    """As the Copilot build's rule, except that an earlier render is recognized by its
    `.claude-plugin/plugin.json`."""
    if plugin_root == source_root or plugin_root in source_root.parents:
        return True
    try:
        copied, _ = shared._layout(source_root)
    except RenderError:
        copied = []
    for name in (BUILD.parts[0], "conf", "docs", *copied):
        top = source_root / name
        if plugin_root == top or top in plugin_root.parents:
            return True
    if not plugin_root.exists():
        return False
    return not (plugin_root.is_dir() and (plugin_root / MANIFEST_FILE).is_file())


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_claude_plugin.py <source-root> <plugin-root>", file=sys.stderr)
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
    print(f"rendered Claude Code plugin: {plugin_root} ({agents} agents, {skills} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
