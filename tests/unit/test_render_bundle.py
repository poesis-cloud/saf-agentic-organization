"""Renderer contract: inject tools, refuse stale agent maps and unsafe targets."""

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


def _run(monkeypatch: pytest.MonkeyPatch, source: Path, bundle: Path) -> int:
    monkeypatch.setattr("sys.argv", ["render_bundle.py", str(source), str(bundle)])
    return render_bundle.main()


@pytest.fixture()
def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    _write_source(root)
    return root


@pytest.mark.parametrize(
    "target",
    [".", "..", "agents", "builds", "builds/github-copilot", "builds/github-copilot-cli", "builds/github-copilot/out"],
)
def test_render_refuses_source_and_build_inputs(source: Path, monkeypatch: pytest.MonkeyPatch, target: str) -> None:
    (source / "builds" / "github-copilot-cli").mkdir()
    (source / "builds" / "github-copilot-cli" / "plugin.json").write_text("{}", encoding="utf-8")
    tree = sorted(p.relative_to(source) for p in source.rglob("*"))
    assert _run(monkeypatch, source, source / target) == 2
    assert sorted(p.relative_to(source) for p in source.rglob("*")) == tree


def test_render_refuses_foreign_directory_but_rerenders_into_dist(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    foreign = tmp_path / "home"
    foreign.mkdir()
    (foreign / "notes.txt").write_text("keep", encoding="utf-8")
    assert _run(monkeypatch, source, foreign) == 2
    assert (foreign / "notes.txt").is_file()
    for _ in range(2):
        assert _run(monkeypatch, source, source / "dist") == 0
        assert (source / "dist" / "agents" / "value-management-officer.agent.md").is_file()
        assert not (source / "dist" / "dist").exists()
        assert sorted(p.name for p in source.iterdir()) == ["agents", "builds", "dist"]


def test_failed_render_keeps_earlier_bundle(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    earlier = {p.relative_to(bundle): p.read_bytes() for p in bundle.rglob("*") if p.is_file()}
    agent = source / "agents" / "value-management-officer.agent.md"
    good = agent.read_text(encoding="utf-8")
    agent.write_text("no frontmatter\n", encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 1
    assert "lacks YAML frontmatter" in capsys.readouterr().err
    assert {p.relative_to(bundle): p.read_bytes() for p in bundle.rglob("*") if p.is_file()} == earlier
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]
    agent.write_text(good.replace("# vmo", "# vmo v2"), encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 0
    assert "# vmo v2" in (bundle / "agents" / "value-management-officer.agent.md").read_text(encoding="utf-8")
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]


def test_invalid_tools_map_leaves_earlier_bundle(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    (source / "builds" / "github-copilot" / "tools.yaml").write_text("{}", encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 1
    assert "tools: [read/readFile]" in (bundle / "agents" / "value-management-officer.agent.md").read_text(encoding="utf-8")


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
