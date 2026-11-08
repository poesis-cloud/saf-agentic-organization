"""GitHub Copilot plugin renderer contract (Agent Plugins 1.0): closed manifest, framework layout
under `framework/`, Copilot agents with scoped H0 hooks, Agent Skills folders, registration."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

from tests.loaders import load_workflows, organization_root, parse_frontmatter

ORG = organization_root()
BUILD = ORG / "builds" / "plugin"
_SPEC = importlib.util.spec_from_file_location("render_plugin", BUILD / "render_plugin.py")
assert _SPEC is not None and _SPEC.loader is not None
render_plugin = importlib.util.module_from_spec(_SPEC)
sys.modules["render_plugin"] = render_plugin
_SPEC.loader.exec_module(render_plugin)

PLUGIN = "poesis-saf-agentic-organization"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENTS = "com.github.copilot/agents"
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def _write_source(root: Path) -> None:
    (root / ".env").write_text(
        "# layout\nFRAMEWORK_SKILLS_DIR=skills\nFRAMEWORK_WORKFLOWS_DIR='workflows'\n"
        "FRAMEWORK_WORKSPACE_DIR=workspace\nOTHER=value\nnot-an-assignment\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text("# org\n", encoding="utf-8")
    (root / "agents").mkdir()
    (root / "agents" / "value-management-officer.agent.md").write_text(
        "---\nname: value-management-officer\ndescription: 'Portfolio orchestrator'\ntools: [old/tool]\n---\n"
        "Load [lpm.skill.md](../skills/lpm.skill.md) and [flow](../workflows/flow.workflow.conf.yaml#steps).\n"
        "Keep [external](https://example.com), [anchor](#here) and [readme](../README.md).\n",
        encoding="utf-8",
    )
    (root / "agents" / "developer.agent.md").write_text(
        "---\nname: developer\ndescription: Developer\n---\nRead [profiles](../conf/model-profiles.conf.yaml).\n",
        encoding="utf-8",
    )
    (root / "skills").mkdir()
    (root / "skills" / "lpm.skill.md").write_text(
        "---\nname: Lean Portfolio Management\ndescription: 'LPM procedure'\nuser-invocable: false\n---\n"
        "See [flow](../workflows/flow.workflow.conf.yaml) and [dev](developer.skill.md).\n",
        encoding="utf-8",
    )
    (root / "workflows").mkdir()
    (root / "workflows" / "flow.workflow.conf.yaml").write_text("orchestrator: value-management-officer\n", encoding="utf-8")
    (root / "workflows" / "plain.workflow.conf.yaml").write_text("- not a mapping\n", encoding="utf-8")
    (root / "workflows" / "__pycache__").mkdir()
    (root / "conf").mkdir()
    (root / "conf" / "model-profiles.conf.yaml").write_text("profiles: {}\n", encoding="utf-8")
    build = root / "builds" / "plugin"
    (build / "bin").mkdir(parents=True)
    (build / "plugin.json").write_text(
        json.dumps(
            {
                "$schema": SCHEMA,
                "name": PLUGIN,
                "version": "1.0.0",
                "description": "d",
                "author": {"name": "Poesis SAS"},
                "license": "Apache-2.0",
            }
        ),
        encoding="utf-8",
    )
    (build / "tools.yaml").write_text(
        yaml.safe_dump(
            {
                "agents": {
                    "agents/value-management-officer.agent.md": ["read", "execute", "agent"],
                    "agents/developer.agent.md": ["read", "edit", "search", "execute"],
                }
            }
        ),
        encoding="utf-8",
    )
    (build / "host-binding.md").write_text(
        "<!-- license -->\n## Host binding\n\nAgents: {{AGENT_IDS}}; init: `{{PLUGIN_NAME}}:init`\n", encoding="utf-8"
    )
    (build / "bin" / "register.sh").write_text("#!/bin/sh\necho {{PLUGIN_NAME}}\n", encoding="utf-8")
    (build / "bin" / "register.ps1").write_text("Write-Output '{{PLUGIN_NAME}}'\n", encoding="utf-8")
    (build / "skills" / "init").mkdir(parents=True)
    (build / "skills" / "init" / "SKILL.md").write_text(
        "---\nname: init\ndescription: 'Initialise a workspace'\n---\n"
        "Framework `{{PLUGIN_NAME}}`, root `{{WORKSPACE_ROOT}}`, orchestrators {{ORCHESTRATORS}}.\n",
        encoding="utf-8",
    )


def _run(monkeypatch: pytest.MonkeyPatch, source: Path, plugin: Path) -> int:
    monkeypatch.setattr("sys.argv", ["render_plugin.py", str(source), str(plugin)])
    return render_plugin.main()


def _tree(root: Path) -> dict[Path, bytes]:
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@pytest.fixture()
def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    _write_source(root)
    return root


def test_render_writes_the_plugin(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    plugin = tmp_path / "plugin"
    (plugin / "stale").mkdir(parents=True)
    (plugin / "plugin.json").write_text("{}", encoding="utf-8")
    assert _run(monkeypatch, source, plugin) == 0
    assert not (plugin / "stale").exists()
    manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
    assert manifest == json.loads((source / "builds" / "plugin" / "plugin.json").read_text(encoding="utf-8"))

    env = (plugin / ".env").read_text(encoding="utf-8")
    assert "FRAMEWORK_SKILLS_DIR=framework/skills\n" in env
    assert "FRAMEWORK_WORKFLOWS_DIR=framework/workflows\n" in env
    assert "FRAMEWORK_WORKSPACE_DIR=workspace\n" in env and "OTHER=value\n" in env
    assert (plugin / "framework" / "workflows" / "flow.workflow.conf.yaml").is_file()
    assert (plugin / "framework" / "skills" / "lpm.skill.md").is_file()
    assert not (plugin / "framework" / "workflows" / "__pycache__").exists()
    assert not (plugin / "framework" / "agents").exists()
    assert (plugin / "conf" / "model-profiles.conf.yaml").is_file()
    assert (plugin / "README.md").is_file() and not (plugin / "LICENSE").exists()
    assert not (plugin / "builds").exists() and not (plugin / "agents").exists()

    vmo_path = plugin / AGENTS / "value-management-officer.agent.md"
    vmo = vmo_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(vmo_path)
    assert meta["tools"] == ["read", "execute", "agent"] and "old/tool" not in vmo
    assert set(meta["hooks"]) == {"userPromptSubmitted", "userPromptTransformed"}
    entry = meta["hooks"]["userPromptSubmitted"][0]
    assert entry["type"] == "command" and entry["timeoutSec"] == 120
    assert entry["command"].endswith(f"harness/launcher.sh\" userPromptSubmitted --framework {PLUGIN} --agent value-management-officer")
    assert "launcher.ps1" in entry["windows"]
    assert "[lpm.skill.md](../../skills/lpm/SKILL.md)" in vmo
    assert "(../../framework/workflows/flow.workflow.conf.yaml#steps)" in vmo
    assert "(https://example.com)" in vmo and "(#here)" in vmo and "(../README.md)" in vmo
    assert "## Host binding" in vmo and "<!-- license -->" not in vmo
    assert f"`{PLUGIN}:developer`, `{PLUGIN}:value-management-officer`" in vmo and f"`{PLUGIN}:init`" in vmo
    developer = plugin / AGENTS / "developer.agent.md"
    assert parse_frontmatter(developer)["tools"] == ["read", "edit", "search", "execute"]
    assert "hooks" not in parse_frontmatter(developer)
    assert "(../../conf/model-profiles.conf.yaml)" in developer.read_text(encoding="utf-8")

    skill = plugin / "skills" / "lpm" / "SKILL.md"
    assert parse_frontmatter(skill)["name"] == "lpm"
    assert parse_frontmatter(skill)["user-invocable"] is False
    text = skill.read_text(encoding="utf-8")
    assert "(../../framework/workflows/flow.workflow.conf.yaml)" in text
    assert "(../../framework/skills/developer.skill.md)" in text
    assert not list((plugin / "skills").glob("*.skill.md"))
    init = (plugin / "skills" / "init" / "SKILL.md").read_text(encoding="utf-8")
    assert f"Framework `{PLUGIN}`, root `portfolio`, orchestrators {PLUGIN}:value-management-officer." in init

    assert json.loads((plugin / "com.github.copilot" / "hooks" / "hooks.json").read_text(encoding="utf-8")) == render_plugin.render_hooks()
    assert (plugin / "bin" / "register.sh").read_text(encoding="utf-8") == f"#!/bin/sh\necho {PLUGIN}\n"
    assert (plugin / "bin" / "register.ps1").read_text(encoding="utf-8").startswith(f"Write-Output '{PLUGIN}'")
    if os.name == "posix":
        assert os.access(plugin / "bin" / "register.sh", os.X_OK)


def test_render_hooks_are_the_shell_only_registration() -> None:
    hooks = render_plugin.render_hooks()
    assert hooks["version"] == 1 and set(hooks["hooks"]) == {"sessionStart"}
    (entry,) = hooks["hooks"]["sessionStart"]
    assert "bin/register.sh" in entry["bash"] and "register.ps1" in entry["powershell"]
    assert "python" not in json.dumps(entry).lower()


def _write(path: str, text: str):
    return lambda s: (s / path).write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_write("agents/ghost.agent.md", "---\nname: ghost\ndescription: g\n---\n"), "missing tools map"),
        (
            _write(
                "builds/plugin/tools.yaml",
                yaml.safe_dump(
                    {"agents": {"agents/value-management-officer.agent.md": ["read"], "agents/developer.agent.md": ["read"], "agents/x.agent.md": ["read"]}}
                ),
            ),
            "names no source agent",
        ),
        (_write("agents/developer.agent.md", "---\nname: developer\n---\n"), "description"),
        (_write("agents/developer.agent.md", "---\nname: dev\ndescription: d\n---\n"), "name: developer"),
        (_write("agents/developer.agent.md", "---\nname: developer\ndescription: d\nhooks: {}\n---\n"), "declares hooks"),
        (_write("agents/developer.agent.md", "no frontmatter\n"), "missing YAML frontmatter"),
        (_write("agents/developer.agent.md", "---\nname: developer\n"), "not closed"),
        (_write("skills/lpm.skill.md", "---\nname: lpm\ndescription: ''\n---\n"), "1..1024"),
        (_write("skills/lpm.skill.md", f"---\nname: lpm\ndescription: '{'x' * 1025}'\n---\n"), "1..1024"),
        (_write("skills/Bad_Name.skill.md", "---\ndescription: d\n---\n"), "kebab-case"),
        (_write("builds/plugin/skills/init/SKILL.md", "---\nname: init\n---\n"), "1..1024"),
        (lambda s: shutil.copytree(s / "builds/plugin/skills/init", s / "builds/plugin/skills/lpm"), "shadow source skills"),
        (_write("workflows/flow.workflow.conf.yaml", "orchestrator: ghost\n"), "orchestrators with no agent"),
        (lambda s: (s / ".env").unlink(), "layout file"),
        (_write(".env", "FRAMEWORK_SKILLS_DIR=/abs\n"), "relative child"),
        (_write(".env", "FRAMEWORK_SKILLS_DIR=conf\n"), "relative child"),
        (_write(".env", "FRAMEWORK_SKILLS_DIR=nested/../../outside\n"), "relative child"),
        (_write(".env", "FRAMEWORK_SKILLS_DIR=C:/abs\n"), "relative child"),
        (_write(".env", "FRAMEWORK_SKILLS_DIR=..\\outside\n"), "relative child"),
        (lambda s: shutil.rmtree(s / "conf"), "framework configuration"),
    ],
)
def test_render_refuses_bad_source(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], mutate, message: str
) -> None:
    mutate(source)
    assert _run(monkeypatch, source, tmp_path / "plugin") == 1
    assert message in capsys.readouterr().err
    assert not (tmp_path / "plugin").exists()


@pytest.mark.parametrize(
    ("patch", "message"),
    [
        ({"agents": "agents/"}, "unknown keys: agents"),
        ({"hooks": "hooks.json", "skills": "skills/"}, "unknown keys: hooks, skills"),
        ({"$schema": "https://example.com/plugin.json"}, "must declare `$schema"),
        ({"name": "Not Kebab"}, "name rule"),
        ({"name": "a--b"}, "name rule"),
        ({"name": "a" * 65}, "name rule"),
        ({"author": {"name": "x", "org": "y"}}, "author"),
        ({"author": "Poesis"}, "author"),
    ],
)
def test_render_refuses_bad_manifest(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], patch: dict, message: str
) -> None:
    path = source / "builds" / "plugin" / "plugin.json"
    path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")), **patch}), encoding="utf-8")
    assert _run(monkeypatch, source, tmp_path / "plugin") == 1
    assert message in capsys.readouterr().err


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        ({"agents/value-management-officer.agent.md": None}, "must be lists of tool names"),
        ({"agents/value-management-officer.agent.md": ["read", 3]}, "must be lists of tool names"),
        (None, "must be a mapping"),
    ],
)
def test_render_refuses_malformed_tools_entries(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], entry, message: str
) -> None:
    plugin = tmp_path / "plugin"
    assert _run(monkeypatch, source, plugin) == 0
    earlier = _tree(plugin)
    path = source / "builds" / "plugin" / "tools.yaml"
    agents = yaml.safe_load(path.read_text(encoding="utf-8"))["agents"]
    tools = ["agents/value-management-officer.agent.md"] if entry is None else {**agents, **entry}
    path.write_text(yaml.safe_dump({"agents": tools}), encoding="utf-8")
    assert _run(monkeypatch, source, plugin) == 1
    assert message in capsys.readouterr().err
    assert _tree(plugin) == earlier


@pytest.mark.parametrize(
    "target",
    [".", "..", "skills", "skills/out", "workflows", "workflows/new/out", "conf/out", "docs/out", "builds", "builds/plugin",
     "builds/plugin/out", "README.md"],
)
def test_render_refuses_to_overwrite_source(source: Path, monkeypatch: pytest.MonkeyPatch, target: str) -> None:
    build_inputs = sorted(p.relative_to(source) for p in (source / "builds").rglob("*"))
    assert _run(monkeypatch, source, source / target) == 2
    assert (source / "skills" / "lpm.skill.md").is_file()
    assert sorted(p.relative_to(source) for p in (source / "builds").rglob("*")) == build_inputs


def test_render_refuses_foreign_directory(tmp_path: Path, source: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    foreign = tmp_path / "home"
    foreign.mkdir()
    (foreign / "notes.txt").write_text("keep", encoding="utf-8")
    assert _run(monkeypatch, source, foreign) == 2
    assert (foreign / "notes.txt").is_file()
    assert _run(monkeypatch, source, source / "dist") == 0
    assert _run(monkeypatch, source, source / "dist") == 0


def test_failed_render_keeps_earlier_plugin(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    plugin = tmp_path / "plugin"
    assert _run(monkeypatch, source, plugin) == 0
    (plugin / "extra.json").write_text("{}", encoding="utf-8")
    earlier = _tree(plugin)
    skill = source / "skills" / "lpm.skill.md"
    good = skill.read_text(encoding="utf-8")
    skill.write_text("---\nname: lpm\ndescription: ''\n---\n", encoding="utf-8")
    assert _run(monkeypatch, source, plugin) == 1
    assert "1..1024" in capsys.readouterr().err
    assert _tree(plugin) == earlier
    assert sorted(p.name for p in tmp_path.iterdir()) == ["plugin", "source"]
    skill.write_text(good, encoding="utf-8")
    assert _run(monkeypatch, source, plugin) == 0
    assert not (plugin / "extra.json").exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["plugin", "source"]


def test_unexpected_error_cleans_staging(source: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(render_plugin, "_rewrite_links", boom)
    with pytest.raises(RuntimeError):
        _run(monkeypatch, source, source / "dist")
    assert not [p.name for p in source.iterdir() if p.name.startswith(".") and p.name != ".env"]
    assert not (source / "dist").exists()


def _lock_directory(monkeypatch: pytest.MonkeyPatch, locked: Path) -> None:
    """Simulate Windows with the plugin loaded live: the open directory cannot be renamed."""
    for name in ("rename", "replace"):
        original = getattr(os, name)

        def refuse(src, dst, *args, _original=original, **kwargs):
            if Path(src) == locked:
                raise PermissionError(5, "Access is denied", str(src))
            return _original(src, dst, *args, **kwargs)

        monkeypatch.setattr(os, name, refuse)


@pytest.mark.skipif(os.name != "posix", reason="symlinks need privileges on Windows")
def test_rerender_updates_live_plugin_in_place(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fresh = tmp_path / "fresh"
    assert _run(monkeypatch, source, fresh) == 0
    plugin = tmp_path / "plugin"
    assert _run(monkeypatch, source, plugin) == 0
    inode = plugin.stat().st_ino
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep", encoding="utf-8")
    (plugin / "stale" / "deep").mkdir(parents=True)
    (plugin / "stale" / "deep" / "old.md").write_text("old", encoding="utf-8")
    (plugin / "link").symlink_to(outside, target_is_directory=True)
    (plugin / "file-link").symlink_to(outside / "keep.txt")
    agent = plugin / AGENTS / "value-management-officer.agent.md"
    agent.unlink()
    (agent / "nested").mkdir(parents=True)
    shutil.rmtree(plugin / "conf")
    (plugin / "conf").write_text("not a directory", encoding="utf-8")
    _lock_directory(monkeypatch, plugin)
    assert _run(monkeypatch, source, plugin) == 0
    assert plugin.stat().st_ino == inode
    assert _tree(plugin) == _tree(fresh)
    assert not (plugin / "link").exists() and not (plugin / "link").is_symlink()
    assert not (plugin / "file-link").is_symlink()
    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["fresh", "outside", "plugin", "source"]


def test_failed_in_place_update_can_be_retried(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    plugin = tmp_path / "plugin"
    assert _run(monkeypatch, source, plugin) == 0
    vmo = source / "agents" / "value-management-officer.agent.md"
    vmo.write_text(vmo.read_text(encoding="utf-8") + "\nv2\n", encoding="utf-8")
    with monkeypatch.context() as patch:
        _lock_directory(patch, plugin)
        replace = os.replace

        def failing_replace(src, dst, *args, **kwargs):
            if Path(dst).name.endswith(".agent.md"):
                raise PermissionError(5, "Access is denied", str(dst))
            return replace(src, dst, *args, **kwargs)

        patch.setattr(os, "replace", failing_replace)
        assert _run(monkeypatch, source, plugin) == 1
    assert "Access is denied" in capsys.readouterr().err
    assert (plugin / "plugin.json").is_file()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["plugin", "source"]
    assert _run(monkeypatch, source, plugin) == 0
    assert "v2" in (plugin / AGENTS / "value-management-officer.agent.md").read_text(encoding="utf-8")


def test_render_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["render_plugin.py"])
    assert render_plugin.main() == 2


# --- The live tree --------------------------------------------------------------------------


def _orchestrators() -> set[str]:
    return {workflow["orchestrator"] for workflow in load_workflows().values() if workflow.get("orchestrator")}


@pytest.fixture(scope="module")
def live_plugin(tmp_path_factory: pytest.TempPathFactory) -> Path:
    plugin = tmp_path_factory.mktemp("live") / "plugin"
    render_plugin.render(ORG, plugin)
    yield plugin
    shutil.rmtree(plugin, ignore_errors=True)


def test_live_manifest_is_a_closed_agent_plugins_manifest() -> None:
    manifest = json.loads((BUILD / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["$schema"] == SCHEMA and manifest["name"] == PLUGIN
    assert set(manifest) <= set(render_plugin.MANIFEST_KEYS)


def test_live_plugin_ships_the_usage_model(live_plugin: Path) -> None:
    assert (live_plugin / "docs" / "usage-model.md").is_file() and (live_plugin / "docs" / "step-artifacts.md").is_file()
    for slug in _orchestrators():
        text = (ORG / "instructions" / slug / f"{slug}-interpret-speech-acts.instructions.md").read_text(encoding="utf-8")
        assert "`docs/usage-model.md` at the framework root" in text and "README usage model" not in text


def test_live_plugin_matches_harness_contract(live_plugin: Path) -> None:
    orchestrators = _orchestrators()
    assert orchestrators == {"value-management-officer", "release-train-engineer", "scrum-master"}
    agents = {path.name[: -len(".agent.md")]: parse_frontmatter(path) for path in (live_plugin / AGENTS).glob("*.agent.md")}
    assert set(agents) == {path.name[: -len(".agent.md")] for path in (ORG / "agents").glob("*.agent.md")}
    for slug, meta in agents.items():
        assert meta["name"] == slug and meta["description"]
        assert ("hooks" in meta) is (slug in orchestrators), slug
        assert {"read", "edit", "search", "execute"} <= set(meta["tools"])
        assert ("agent" in meta["tools"]) is (slug in orchestrators)
        assert not any("/" in tool for tool in meta["tools"]), slug
    for slug in orchestrators:
        assert agents[slug]["hooks"] == render_plugin.scoped_hooks(PLUGIN, slug)
        text = (live_plugin / AGENTS / f"{slug}.agent.md").read_text(encoding="utf-8")
        assert "agent_type" in text
        commands = [line for line in text.splitlines() if re.search(r"harness\.py>? ", line)]
        assert commands, slug
        assert not [line for line in commands if re.search(r"harness\.py>? \S+[^`]*--(parent-)?session-id", line)], slug
    env = (live_plugin / ".env").read_text(encoding="utf-8")
    dirs = [line.split("=", 1)[1] for line in env.splitlines() if line.startswith("FRAMEWORK_") and "WORKSPACE" not in line]
    assert dirs and all(value.startswith("framework/") and (live_plugin / value).is_dir() for value in dirs)
    assert (live_plugin / "conf" / "harness.conf.yaml").is_file()


CLI_HARNESS_COMMAND = r"<venv python> <harness\.py> (resolve-step --workflow-slug <[a-z-]+>|resolve-step-model)"
VSCODE_HARNESS_COMMAND = r"python <harness\.py> (resolve-step|resolve-step-model) --workflow-slug <[a-z-]+>"
ALLOWED_HARNESS_COMMAND = re.compile(rf"(& )?{CLI_HARNESS_COMMAND}|{VSCODE_HARNESS_COMMAND}")
HOOK_ANSWER_PROSE = (
    "does NOT run this command",
    "`SAFe agentic harness RESULT (<function>)`",
    "do not re-issue the command",
    "`SAFe agentic harness REJECTED`",
)
WRITE_TOOL_PROSE = ("`create`", "`edit`", "`apply_patch`", "never through the shell")
RETIRED_HARNESS_SETUP = ("setx", "$env:FRAMEWORK", "permissions-config")


def test_live_plugin_states_only_the_adapter_admitted_harness_command(live_plugin: Path) -> None:
    files = [*(live_plugin / AGENTS).glob("*.agent.md"), *(live_plugin / "skills").glob("*/SKILL.md")]
    commands = [span for path in files for span in re.findall(r"`([^`]*harness\.py>? [^`]*)`", path.read_text(encoding="utf-8"))]
    assert commands
    assert [span for span in commands if not ALLOWED_HARNESS_COMMAND.fullmatch(span)] == []
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert not [word for word in RETIRED_HARNESS_SETUP if word in text], path
    for slug in _orchestrators():
        for path in (live_plugin / AGENTS / f"{slug}.agent.md", live_plugin / "skills" / slug / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            assert re.search(rf"`& {CLI_HARNESS_COMMAND}`", text), path
            assert "resolve-step-model" in text, path
            assert [phrase for phrase in HOOK_ANSWER_PROSE if phrase not in text] == [], path
            assert [phrase for phrase in WRITE_TOOL_PROSE if phrase not in text] == [], path


def test_live_plugin_dispatches_namespaced_agents_once_per_step(live_plugin: Path) -> None:
    namespaced = f'agent_type: "{PLUGIN}:<'
    for slug in _orchestrators():
        for path in (live_plugin / AGENTS / f"{slug}.agent.md", live_plugin / "skills" / slug / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            assert namespaced in text, path
            assert re.findall(r'agent_type: "([^"]+)"', text) == [f"{PLUGIN}:<agent-id>"] * len(re.findall(r'agent_type: "', text)), path
            assert "--bound-model" not in text and "boundModels" not in text, path
        skill = (live_plugin / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        assert "step-session-bound" in skill, slug
        assert "Unknown agent_type" in skill, slug
    binding = (live_plugin / AGENTS / "developer.agent.md").read_text(encoding="utf-8")
    assert f"`agent_type` set to `{PLUGIN}:<actor>`" in binding
    assert f"`{PLUGIN}:release-train-engineer`" in binding and f"`{PLUGIN}:init`" in binding
    assert "exactly once" in binding and "step-session-bound" in binding
    assert "{{" not in binding


def test_live_plugin_skills_are_agent_skill_folders(live_plugin: Path) -> None:
    sources = {path.name[: -len(".skill.md")] for path in (ORG / "skills").glob("*.skill.md")}
    folders = {path.parent.name for path in (live_plugin / "skills").glob("*/SKILL.md")}
    assert folders == sources | {"init"}
    for stem in folders:
        meta = parse_frontmatter(live_plugin / "skills" / stem / "SKILL.md")
        assert meta["name"] == stem
        assert 0 < len(meta["description"]) <= 1024
    init = (live_plugin / "skills" / "init" / "SKILL.md").read_text(encoding="utf-8")
    assert "{{" not in init and PLUGIN in init


def _broken_links(paths: list[Path]) -> list[str]:
    broken: list[str] = []
    for path in paths:
        for raw in LINK_RE.findall(path.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0]
            if not target or "://" in raw or raw.startswith(("#", "/", "mailto:", "<")) or "{" in target:
                continue
            if target.endswith((".md", ".yaml", ".json")) and not (path.parent / target).exists():
                broken.append(f"{path.name} -> {raw}")
    return broken


def test_live_plugin_never_adds_broken_links(live_plugin: Path) -> None:
    source = _broken_links([*(ORG / "agents").glob("*.agent.md"), *(ORG / "skills").glob("*.skill.md")])
    rendered = _broken_links([*(live_plugin / AGENTS).glob("*.agent.md"), *(live_plugin / "skills").glob("*/SKILL.md")])
    assert len(rendered) <= len(source)
    assert not [link for link in rendered if "SKILL.md" in link.split(" -> ", 1)[1]]
