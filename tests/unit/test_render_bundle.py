"""Renderer contract: inject tools, refuse stale agent maps."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import render_bundle


def _write_source(root: Path, *, extra_agent: bool = False, drop_tools: bool = False) -> None:
    agents = root / "agents"
    agents.mkdir()
    (agents / "value-management-officer.agent.md").write_text(
        "---\nname: value-management-officer\n---\n# vmo\n",
        encoding="utf-8",
    )
    build = root / "builds" / "github-copilot"
    build.mkdir(parents=True)
    agents_list = ["agents/value-management-officer.agent.md"]
    if extra_agent:
        agents_list.append("agents/ghost.agent.md")
        (agents / "ghost.agent.md").write_text("---\nname: ghost\n---\n", encoding="utf-8")
    (build / "plugin.json").write_text(
        json.dumps({"agents": agents_list, "version": "0.1.0"}),
        encoding="utf-8",
    )
    tools = {} if drop_tools else {"agents": {"agents/value-management-officer.agent.md": ["read/readFile"]}}
    (build / "tools.yaml").write_text(yaml.safe_dump(tools), encoding="utf-8")


def test_render_injects_tools(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write_source(source)
    bundle = tmp_path / "bundle"
    monkeypatch.setattr("sys.argv", ["render_bundle.py", str(source), str(bundle)])
    assert render_bundle.main() == 0
    rendered = (bundle / "agents" / "value-management-officer.agent.md").read_text(encoding="utf-8")
    assert "tools: [read/readFile]" in rendered
    assert (bundle / "plugin.json").is_file()


def test_render_refuses_missing_tools_map(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write_source(source, extra_agent=True)
    bundle = tmp_path / "bundle"
    monkeypatch.setattr("sys.argv", ["render_bundle.py", str(source), str(bundle)])
    assert render_bundle.main() == 1


def test_render_refuses_extra_tools_map(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write_source(source)
    tools_path = source / "builds" / "github-copilot" / "tools.yaml"
    tools_path.write_text(
        yaml.safe_dump(
            {
                "agents": {
                    "agents/value-management-officer.agent.md": ["read/readFile"],
                    "agents/ghost.agent.md": ["read/readFile"],
                }
            }
        ),
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle"
    monkeypatch.setattr("sys.argv", ["render_bundle.py", str(source), str(bundle)])
    assert render_bundle.main() == 1


def test_render_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["render_bundle.py"])
    assert render_bundle.main() == 2


def test_inject_tools_replaces_existing(tmp_path: Path) -> None:
    path = tmp_path / "agent.md"
    path.write_text("---\nname: x\ntools: [old]\n---\nbody\n", encoding="utf-8")
    render_bundle._inject_tools(path, ["read/readFile"])
    assert "tools: [read/readFile]" in path.read_text(encoding="utf-8")
    assert "old" not in path.read_text(encoding="utf-8")


def test_inject_tools_rejects_unclosed_frontmatter(tmp_path: Path) -> None:
    path = tmp_path / "agent.md"
    path.write_text("---\nname: x\n", encoding="utf-8")
    with pytest.raises(ValueError):
        render_bundle._inject_tools(path, ["read/readFile"])


def test_inject_tools_rejects_missing_frontmatter(tmp_path: Path) -> None:
    path = tmp_path / "agent.md"
    path.write_text("no frontmatter\n", encoding="utf-8")
    with pytest.raises(ValueError):
        render_bundle._inject_tools(path, ["read/readFile"])


def test_ignore_skips_generated_dirs() -> None:
    ignored = render_bundle._ignore("/tmp", [".git", "agents", "__pycache__"])
    assert ignored == {".git", "__pycache__"}
