"""Claude Code plugin renderer contract: manifest derived from the Copilot build, framework layout
under `framework/`, Claude Code agents (translated tools, no hooks), Agent Skills folders, the
shell-only registration."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest
import yaml

from tests.loaders import organization_root, parse_frontmatter
from tests.unit.test_render_plugin import PLUGIN, _write_source

ORG = organization_root()
BUILD = ORG / "builds" / "claude-plugin"
_SPEC = importlib.util.spec_from_file_location("render_claude_plugin", BUILD / "render_claude_plugin.py")
assert _SPEC is not None and _SPEC.loader is not None
render_claude_plugin = importlib.util.module_from_spec(_SPEC)
sys.modules["render_claude_plugin"] = render_claude_plugin
_SPEC.loader.exec_module(render_claude_plugin)

MANIFEST = Path(".claude-plugin") / "plugin.json"


def _write_claude_build(root: Path) -> None:
    build = root / "builds" / "claude-plugin"
    (build / "bin").mkdir(parents=True)
    (build / "tools.yaml").write_text(
        yaml.safe_dump(
            {
                "aliases": {
                    "read": ["Read"],
                    "edit": ["Write", "Edit"],
                    "search": ["Grep", "Glob"],
                    "execute": ["Bash"],
                    "agent": ["Agent"],
                }
            }
        ),
        encoding="utf-8",
    )
    (build / "host-binding.md").write_text(
        "<!-- license -->\n## Claude binding\n\nAgents: {{AGENT_IDS}}; plugin `{{PLUGIN_NAME}}`\n",
        encoding="utf-8",
    )
    (build / "bin" / "register.sh").write_text("#!/bin/sh\necho {{PLUGIN_NAME}}\n", encoding="utf-8")
    (build / "skills" / "init").mkdir(parents=True)
    (build / "skills" / "init" / "SKILL.md").write_text(
        "---\nname: init\ndescription: 'Initialise a workspace'\n---\n"
        "Framework `{{PLUGIN_NAME}}`, root `{{WORKSPACE_ROOT}}`, orchestrators {{ORCHESTRATORS}}.\n",
        encoding="utf-8",
    )


@pytest.fixture()
def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    _write_source(root)
    _write_claude_build(root)
    return root


def _run(monkeypatch: pytest.MonkeyPatch, *argv: str) -> int:
    monkeypatch.setattr("sys.argv", ["render_claude_plugin.py", *argv])
    return render_claude_plugin.main()


def test_render_writes_the_claude_code_plugin(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin = tmp_path / "plugin"
    (plugin / ".claude-plugin").mkdir(parents=True)
    (plugin / MANIFEST).write_text("{}", encoding="utf-8")
    (plugin / "stale").mkdir()
    assert _run(monkeypatch, str(source), str(plugin)) == 0
    assert not (plugin / "stale").exists()

    manifest = json.loads((plugin / MANIFEST).read_text(encoding="utf-8"))
    assert manifest == {
        "name": PLUGIN,
        "version": "1.0.0",
        "description": "d",
        "author": {"name": "Poesis SAS"},
        "license": "Apache-2.0",
    }
    assert not (plugin / "plugin.json").exists() and not (plugin / "com.github.copilot").exists()
    assert "FRAMEWORK_SKILLS_DIR=framework/skills\n" in (plugin / ".env").read_text(encoding="utf-8")
    assert (plugin / "framework" / "workflows" / "flow.workflow.conf.yaml").is_file()
    assert (plugin / "conf" / "model-profiles.conf.yaml").is_file()

    vmo_path = plugin / "agents" / "value-management-officer.md"
    vmo = vmo_path.read_text(encoding="utf-8")
    meta = parse_frontmatter(vmo_path)
    assert meta["tools"] == "Read, Bash, Agent" and "hooks" not in meta
    assert "[lpm.skill.md](../skills/lpm/SKILL.md)" in vmo
    assert "(../framework/workflows/flow.workflow.conf.yaml#steps)" in vmo
    assert "## Claude binding" in vmo and "<!-- license -->" not in vmo
    assert f"`{PLUGIN}:developer`, `{PLUGIN}:value-management-officer`" in vmo
    developer = plugin / "agents" / "developer.md"
    assert parse_frontmatter(developer)["tools"] == "Read, Write, Edit, Grep, Glob, Bash"
    assert "(../conf/model-profiles.conf.yaml)" in developer.read_text(encoding="utf-8")

    assert parse_frontmatter(plugin / "skills" / "lpm" / "SKILL.md")["name"] == "lpm"
    init = (plugin / "skills" / "init" / "SKILL.md").read_text(encoding="utf-8")
    assert f"Framework `{PLUGIN}`, root `portfolio`, orchestrators {PLUGIN}:value-management-officer." in init

    hooks = json.loads((plugin / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert hooks == render_claude_plugin.render_hooks()
    assert (plugin / "bin" / "register.sh").read_text(encoding="utf-8") == f"#!/bin/sh\necho {PLUGIN}\n"
    if os.name == "posix":
        assert os.access(plugin / "bin" / "register.sh", os.X_OK)


def test_render_hooks_are_the_shell_only_registration() -> None:
    hooks = render_claude_plugin.render_hooks()["hooks"]
    assert set(hooks) == {"SessionStart"}
    ((entry,),) = [group["hooks"] for group in hooks["SessionStart"]]
    assert entry["command"] == 'sh "${CLAUDE_PLUGIN_ROOT}/bin/register.sh"'
    assert "python" not in json.dumps(entry).lower()


@pytest.mark.parametrize(
    ("path", "text", "message"),
    [
        ("builds/claude-plugin/tools.yaml", "aliases: [read]\n", "needs an `aliases` mapping"),
        ("builds/claude-plugin/tools.yaml", "aliases:\n  read: [Read]\n", "no Claude Code tools for alias"),
        ("agents/ghost.agent.md", "---\nname: ghost\ndescription: g\n---\n", "missing tools map"),
        ("workflows/other.workflow.conf.yaml", "orchestrator: nobody\n", "orchestrators with no agent"),
        ("skills/init.skill.md", "---\nname: init\ndescription: i\n---\n", "shadow source skills"),
    ],
)
def test_render_refuses_inconsistent_inputs(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
    path: str, text: str, message: str,
) -> None:
    (source / path).write_text(text, encoding="utf-8")
    assert _run(monkeypatch, str(source), str(tmp_path / "plugin")) == 1
    assert message in capsys.readouterr().err
    assert not (tmp_path / "plugin").exists()


@pytest.mark.parametrize(
    ("agent", "message"),
    [
        ("---\nname: other\ndescription: d\n---\n", "needs `name: developer`"),
        ("---\nname: developer\ndescription: d\nhooks: {}\n---\n", "declares hooks"),
    ],
)
def test_render_refuses_malformed_agents(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
    agent: str, message: str,
) -> None:
    (source / "agents" / "developer.agent.md").write_text(agent, encoding="utf-8")
    assert _run(monkeypatch, str(source), str(tmp_path / "plugin")) == 1
    assert message in capsys.readouterr().err


def test_main_refuses_unsafe_targets_and_bad_usage(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert _run(monkeypatch, str(source)) == 2
    for target in (source, source.parent, source / "builds" / "x", source / "workflows" / "x", source / "conf"):
        assert _run(monkeypatch, str(source), str(target)) == 2
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    (foreign / "plugin.json").write_text("{}", encoding="utf-8")
    assert _run(monkeypatch, str(source), str(foreign)) == 2
    assert render_claude_plugin._unsafe_target(tmp_path / "nolayout", tmp_path / "out") is False


def test_the_real_organization_renders(tmp_path: Path) -> None:
    """The checked-in Claude Code build renders this organization: every agent, every alias."""
    agents, skills = render_claude_plugin.render(ORG, tmp_path / "plugin")
    assert agents == len(list((ORG / "agents").glob("*.agent.md")))
    assert skills == len(list((ORG / "skills").glob("*.skill.md"))) + 1
    rendered = (tmp_path / "plugin" / "agents" / "release-train-engineer.md").read_text(encoding="utf-8")
    assert "{{" not in rendered and "## Host binding — Claude Code (plugin)" in rendered
    assert "run_in_background: false" in rendered
