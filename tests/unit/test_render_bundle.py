"""Renderer contract: inject tools, refuse stale agent maps and unsafe targets."""

from __future__ import annotations

import json
import os
import shutil
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


def _tree(root: Path) -> dict[Path, bytes]:
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize(
    ("tools", "message"),
    [
        ("agents:\n  agents/value-management-officer.agent.md:\n", "must be lists of tool names"),
        ("agents:\n  agents/value-management-officer.agent.md: [read/readFile, '']\n", "must be lists of tool names"),
        ("agents: [agents/value-management-officer.agent.md]\n", "must be a mapping"),
    ],
)
def test_render_refuses_malformed_tools_entries(
    source: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tools: str, message: str
) -> None:
    assert _run(monkeypatch, source, source / "dist") == 0
    earlier = _tree(source / "dist")
    (source / "builds" / "github-copilot" / "tools.yaml").write_text(tools, encoding="utf-8")
    assert _run(monkeypatch, source, source / "dist") == 1
    assert message in capsys.readouterr().err
    assert _tree(source / "dist") == earlier
    assert sorted(p.name for p in source.iterdir()) == ["agents", "builds", "dist"]


def test_unexpected_error_cleans_staging(source: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_path: Path, _tools: list[str]) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(render_bundle, "_inject_tools", boom)
    with pytest.raises(RuntimeError):
        _run(monkeypatch, source, source / "dist")
    assert sorted(p.name for p in source.iterdir()) == ["agents", "builds"]


def _lock_directory(monkeypatch: pytest.MonkeyPatch, locked: Path) -> None:
    """Simulate Windows with the bundle loaded live: the open directory cannot be renamed."""
    for name in ("rename", "replace"):
        original = getattr(os, name)

        def refuse(src, dst, *args, _original=original, **kwargs):
            if Path(src) == locked:
                raise PermissionError(5, "Access is denied", str(src))
            return _original(src, dst, *args, **kwargs)

        monkeypatch.setattr(os, name, refuse)


def test_rerender_updates_live_bundle_in_place(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fresh = tmp_path / "fresh"
    assert _run(monkeypatch, source, fresh) == 0
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    inode = bundle.stat().st_ino
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep", encoding="utf-8")
    (bundle / "hooks.json").write_text("{}", encoding="utf-8")
    (bundle / "stale" / "deep").mkdir(parents=True)
    (bundle / "stale" / "deep" / "old.md").write_text("old", encoding="utf-8")
    (bundle / "link").symlink_to(outside, target_is_directory=True)
    (bundle / "file-link").symlink_to(outside / "keep.txt")
    agent = bundle / "agents/value-management-officer.agent.md"
    agent.unlink()
    (agent / "nested").mkdir(parents=True)
    shutil.rmtree(bundle / "builds")
    (bundle / "builds").write_text("not a directory", encoding="utf-8")
    _lock_directory(monkeypatch, bundle)
    assert _run(monkeypatch, source, bundle) == 0
    assert bundle.stat().st_ino == inode
    assert _tree(bundle) == _tree(fresh)
    assert not (bundle / "link").exists() and not (bundle / "link").is_symlink()
    assert not (bundle / "file-link").is_symlink()
    assert (outside / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(["bundle", "fresh", "outside", "source"])


def test_failed_in_place_update_can_be_retried(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    (source / "agents/value-management-officer.agent.md").write_text(
        (source / "agents/value-management-officer.agent.md").read_text(encoding="utf-8") + "\nv2\n", encoding="utf-8"
    )
    with monkeypatch.context() as patch:
        _lock_directory(patch, bundle)
        replace = os.replace

        def failing_replace(src, dst, *args, **kwargs):
            if Path(dst).name.endswith(".agent.md"):
                raise PermissionError(5, "Access is denied", str(dst))
            return replace(src, dst, *args, **kwargs)

        patch.setattr(os, "replace", failing_replace)
        assert _run(monkeypatch, source, bundle) == 1
    assert "Access is denied" in capsys.readouterr().err
    assert (bundle / "plugin.json").is_file()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]
    assert _run(monkeypatch, source, bundle) == 0
    assert "v2" in (bundle / "agents/value-management-officer.agent.md").read_text(encoding="utf-8")
