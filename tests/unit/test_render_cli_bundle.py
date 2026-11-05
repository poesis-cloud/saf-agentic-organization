"""Copilot app / CLI renderer contract: plugin layout, CLI tools, SKILL.md folders, harness slots."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

from tests.loaders import load_workflows, organization_root, parse_frontmatter

ORG = organization_root()
BUILD = ORG / "builds" / "github-copilot-cli"
_SPEC = importlib.util.spec_from_file_location("render_cli_bundle", BUILD / "render_bundle.py")
assert _SPEC is not None and _SPEC.loader is not None
render_cli_bundle = importlib.util.module_from_spec(_SPEC)
sys.modules["render_cli_bundle"] = render_cli_bundle
_SPEC.loader.exec_module(render_cli_bundle)

PLUGIN = "poesis-saf-agentic-organization"
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
HARNESS_BLOCK = (
    "# >>> safe-harness copilot-cli >>>\n"
    "hooks:\n"
    "  preToolUse:\n"
    "    - type: command\n"
    "      bash: python /abs/harness/adapters/github-copilot-cli/hook.py preToolUse\n"
    "# <<< safe-harness copilot-cli <<<\n"
)


def _write_source(root: Path) -> None:
    (root / ".env").write_text(
        "FRAMEWORK_SKILLS_DIR=skills\nFRAMEWORK_WORKFLOWS_DIR=workflows\nFRAMEWORK_WORKSPACE_DIR=workspace\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text("# org\n", encoding="utf-8")
    (root / "agents").mkdir()
    (root / "agents" / "value-management-officer.agent.md").write_text(
        "---\nname: value-management-officer\ndescription: 'Portfolio orchestrator'\ntools: [old/tool]\n---\n"
        "Load [lpm.skill.md](lpm.skill.md) and [flow](../workflows/flow.workflow.conf.yaml#steps).\n"
        "Keep [external](https://example.com) and [anchor](#here).\n",
        encoding="utf-8",
    )
    (root / "agents" / "developer.agent.md").write_text(
        "---\nname: developer\ndescription: Developer\n---\nBody\n",
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
    (root / "workflows" / "__pycache__").mkdir()
    (root / "conf").mkdir()
    (root / "conf" / "model-profiles.conf.yaml").write_text("profiles: {}\n", encoding="utf-8")
    build = root / "builds" / "github-copilot-cli"
    build.mkdir(parents=True)
    (build / "plugin.json").write_text(
        json.dumps(
            {
                "$license": "Apache-2.0 header",
                "name": PLUGIN,
                "version": "0.1.0",
                "description": "d",
                "author": {"name": "Poesis Cloud"},
                "agents": "agents/",
                "skills": "skills/",
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
    (build / "host-binding.md").write_text("<!-- license -->\n## Host binding\n\nAgents: {{AGENT_IDS}}\n", encoding="utf-8")


def _run(monkeypatch: pytest.MonkeyPatch, source: Path, bundle: Path) -> int:
    monkeypatch.setattr("sys.argv", ["render_bundle.py", str(source), str(bundle)])
    return render_cli_bundle.main()


@pytest.fixture()
def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    _write_source(root)
    return root


def test_render_writes_cli_plugin(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bundle = tmp_path / "bundle"
    (bundle / "stale").mkdir(parents=True)
    (bundle / "plugin.json").write_text("{}", encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 0
    assert not (bundle / "stale").exists()
    manifest = json.loads((bundle / "plugin.json").read_text(encoding="utf-8"))
    assert "$license" not in manifest
    assert manifest["agents"] == "agents/" and manifest["skills"] == "skills/"
    assert "hooks" not in manifest
    assert not (bundle / "hooks.json").exists()
    market = json.loads((bundle / ".github" / "plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert market["name"] == f"{PLUGIN}-local"
    assert market["plugins"] == [{**{k: manifest[k] for k in ("name", "description", "version", "author")}, "source": "."}]

    vmo = (bundle / "agents" / "value-management-officer.agent.md").read_text(encoding="utf-8")
    meta = parse_frontmatter(bundle / "agents" / "value-management-officer.agent.md")
    assert meta["tools"] == ["read", "execute", "agent"]
    assert "old/tool" not in vmo
    assert "[lpm.skill.md](../skills/lpm/SKILL.md)" in vmo
    assert "(../workflows/flow.workflow.conf.yaml#steps)" in vmo
    assert "(https://example.com)" in vmo and "(#here)" in vmo
    assert "## Host binding" in vmo and "<!-- license -->" not in vmo
    assert f"`{PLUGIN}:developer`, `{PLUGIN}:value-management-officer`" in vmo
    assert parse_frontmatter(bundle / "agents" / "developer.agent.md")["tools"] == ["read", "edit", "search", "execute"]

    skill = bundle / "skills" / "lpm" / "SKILL.md"
    assert parse_frontmatter(skill)["name"] == "lpm"
    assert parse_frontmatter(skill)["user-invocable"] is False
    text = skill.read_text(encoding="utf-8")
    assert "(../../workflows/flow.workflow.conf.yaml)" in text
    assert "(../developer.skill.md)" in text
    assert (bundle / "skills" / "lpm.skill.md").read_text(encoding="utf-8") == (source / "skills" / "lpm.skill.md").read_text(
        encoding="utf-8"
    )
    assert (bundle / "workflows" / "flow.workflow.conf.yaml").is_file()
    assert not (bundle / "workflows" / "__pycache__").exists()
    assert (bundle / "conf" / "model-profiles.conf.yaml").is_file()
    assert (bundle / ".env").is_file() and (bundle / "README.md").is_file()
    assert not (bundle / "builds").exists()


def test_harness_block_keeps_agent_frontmatter_valid(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    path = bundle / "agents" / "value-management-officer.agent.md"
    text = path.read_text(encoding="utf-8")
    head, rest = text.split("\n---\n", 1)
    path.write_text(head + "\n" + HARNESS_BLOCK + "---\n" + rest, encoding="utf-8")
    meta = parse_frontmatter(path)
    assert meta["name"] == "value-management-officer"
    assert meta["hooks"]["preToolUse"][0]["type"] == "command"


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda s: (s / "agents" / "ghost.agent.md").write_text("---\nname: ghost\ndescription: g\n---\n"), "missing tools map"),
        (
            lambda s: (s / "builds" / "github-copilot-cli" / "tools.yaml").write_text(
                yaml.safe_dump({"agents": {"agents/value-management-officer.agent.md": ["read"], "agents/developer.agent.md": [], "agents/x.agent.md": []}})
            ),
            "names no source agent",
        ),
        (lambda s: (s / "agents" / "developer.agent.md").write_text("---\nname: developer\n---\n"), "description"),
        (lambda s: (s / "agents" / "developer.agent.md").write_text("---\nname: dev\ndescription: d\n---\n"), "name: developer"),
        (
            lambda s: (s / "agents" / "developer.agent.md").write_text("---\nname: developer\ndescription: d\nhooks: {}\n---\n"),
            "declares hooks",
        ),
        (lambda s: (s / "agents" / "developer.agent.md").write_text("no frontmatter\n"), "missing YAML frontmatter"),
        (lambda s: (s / "agents" / "developer.agent.md").write_text("---\nname: developer\n"), "not closed"),
        (lambda s: (s / "skills" / "lpm.skill.md").write_text("---\nname: lpm\ndescription: ''\n---\n"), "1..1024"),
        (lambda s: (s / "skills" / "lpm.skill.md").write_text(f"---\nname: lpm\ndescription: '{'x' * 1025}'\n---\n"), "1..1024"),
        (lambda s: (s / ".env").unlink(), "layout file"),
    ],
)
def test_render_refuses_bad_source(
    source: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    mutate,
    message: str,
) -> None:
    mutate(source)
    assert _run(monkeypatch, source, tmp_path / "bundle") == 1
    assert message in capsys.readouterr().err


@pytest.mark.parametrize(
    ("patch", "message"),
    [
        ({"name": "Not Kebab"}, "kebab-case"),
        ({"name": "a" * 65}, "kebab-case"),
        ({"agents": ["agents/x.agent.md"]}, "agents: agents/"),
        ({"skills": "skills"}, "skills: skills/"),
        ({"hooks": "hooks.json"}, "must not declare hooks"),
    ],
)
def test_render_refuses_bad_manifest(
    source: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    patch: dict,
    message: str,
) -> None:
    path = source / "builds" / "github-copilot-cli" / "plugin.json"
    path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")), **patch}), encoding="utf-8")
    assert _run(monkeypatch, source, tmp_path / "bundle") == 1
    assert message in capsys.readouterr().err


def test_render_without_author_uses_plugin_name_as_owner(source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = source / "builds" / "github-copilot-cli" / "plugin.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    del manifest["author"]
    path.write_text(json.dumps(manifest), encoding="utf-8")
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    market = json.loads((bundle / ".github" / "plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert market["owner"] == {"name": PLUGIN}


@pytest.mark.parametrize("target", [".", "..", "skills", "workflows", "builds", "README.md"])
def test_render_refuses_to_overwrite_source(source: Path, monkeypatch: pytest.MonkeyPatch, target: str) -> None:
    assert _run(monkeypatch, source, source / target) == 2
    assert (source / "skills" / "lpm.skill.md").is_file()


def test_render_refuses_foreign_directory(tmp_path: Path, source: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    foreign = tmp_path / "home"
    foreign.mkdir()
    (foreign / "notes.txt").write_text("keep", encoding="utf-8")
    assert _run(monkeypatch, source, foreign) == 2
    assert (foreign / "notes.txt").is_file()
    assert _run(monkeypatch, source, source / "dist") == 0
    assert _run(monkeypatch, source, source / "dist") == 0


@pytest.mark.parametrize("target", ["builds/github-copilot-cli", "builds/github-copilot", "builds/github-copilot/out"])
def test_render_refuses_build_inputs(source: Path, monkeypatch: pytest.MonkeyPatch, target: str) -> None:
    (source / "builds" / "github-copilot").mkdir(exist_ok=True)
    (source / "builds" / "github-copilot" / "plugin.json").write_text("{}", encoding="utf-8")
    build_inputs = sorted(p.relative_to(source) for p in (source / "builds").rglob("*"))
    assert _run(monkeypatch, source, source / target) == 2
    assert sorted(p.relative_to(source) for p in (source / "builds").rglob("*")) == build_inputs


def test_failed_render_keeps_earlier_bundle(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    (bundle / "hooks.json").write_text("{}", encoding="utf-8")
    earlier = {p.relative_to(bundle): p.read_bytes() for p in bundle.rglob("*") if p.is_file()}
    skill = source / "skills" / "lpm.skill.md"
    good = skill.read_text(encoding="utf-8")
    skill.write_text("---\nname: lpm\ndescription: ''\n---\n", encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 1
    assert "1..1024" in capsys.readouterr().err
    assert {p.relative_to(bundle): p.read_bytes() for p in bundle.rglob("*") if p.is_file()} == earlier
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]
    skill.write_text(good, encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 0
    assert not (bundle / "hooks.json").exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]


def _tree(root: Path) -> dict[Path, bytes]:
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


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
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    earlier = _tree(bundle)
    path = source / "builds" / "github-copilot-cli" / "tools.yaml"
    agents = yaml.safe_load(path.read_text(encoding="utf-8"))["agents"]
    tools = ["agents/value-management-officer.agent.md"] if entry is None else {**agents, **entry}
    path.write_text(yaml.safe_dump({"agents": tools}), encoding="utf-8")
    assert _run(monkeypatch, source, bundle) == 1
    assert message in capsys.readouterr().err
    assert _tree(bundle) == earlier


def test_unexpected_error_cleans_staging(source: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(render_cli_bundle, "_rewrite_links", boom)
    with pytest.raises(RuntimeError):
        _run(monkeypatch, source, source / "dist")
    assert not [p.name for p in source.iterdir() if p.name.startswith(".") and p.name != ".env"]
    assert not (source / "dist").exists()


def test_failed_promotion_restores_earlier_bundle(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    bundle = tmp_path / "bundle"
    assert _run(monkeypatch, source, bundle) == 0
    (bundle / "hooks.json").write_text("{}", encoding="utf-8")
    earlier = _tree(bundle)
    rename = Path.rename

    def failing_rename(self: Path, target: Path) -> Path:
        if self.name.startswith(".bundle.render-"):
            raise OSError("promotion failed")
        return rename(self, target)

    monkeypatch.setattr(Path, "rename", failing_rename)
    assert _run(monkeypatch, source, bundle) == 1
    assert "promotion failed" in capsys.readouterr().err
    assert _tree(bundle) == earlier
    assert sorted(p.name for p in tmp_path.iterdir()) == ["bundle", "source"]


def test_render_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["render_bundle.py"])
    assert render_cli_bundle.main() == 2


def _orchestrators() -> set[str]:
    return {workflow["orchestrator"] for workflow in load_workflows().values() if workflow.get("orchestrator")}


@pytest.fixture(scope="module")
def live_bundle(tmp_path_factory: pytest.TempPathFactory) -> Path:
    bundle = tmp_path_factory.mktemp("cli") / "bundle"
    render_cli_bundle.render(ORG, bundle)
    yield bundle
    shutil.rmtree(bundle, ignore_errors=True)


def test_live_bundle_matches_harness_contract(live_bundle: Path) -> None:
    orchestrators = _orchestrators()
    assert orchestrators == {"value-management-officer", "release-train-engineer", "scrum-master"}
    agents = {path.name[: -len(".agent.md")]: parse_frontmatter(path) for path in (live_bundle / "agents").glob("*.agent.md")}
    assert set(agents) == {path.name[: -len(".agent.md")] for path in (ORG / "agents").glob("*.agent.md")}
    for slug, meta in agents.items():
        assert meta["name"] == slug and meta["description"]
        assert "hooks" not in meta
        assert {"read", "edit", "search", "execute"} <= set(meta["tools"])
        assert ("agent" in meta["tools"]) is (slug in orchestrators)
        assert not any("/" in tool for tool in meta["tools"]), slug
    for slug in orchestrators:
        text = (live_bundle / "agents" / f"{slug}.agent.md").read_text(encoding="utf-8")
        assert "agent_type" in text
        commands = [line for line in text.splitlines() if re.search(r"harness\.py>? ", line)]
        assert commands, slug
        assert not [line for line in commands if re.search(r"harness\.py>? \S+[^`]*--(parent-)?session-id", line)], slug


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


def test_live_bundle_states_only_the_adapter_admitted_harness_command(live_bundle: Path) -> None:
    files = [*(live_bundle / "agents").glob("*.agent.md"), *(live_bundle / "skills").glob("*/SKILL.md")]
    commands = [span for path in files for span in re.findall(r"`([^`]*harness\.py>? [^`]*)`", path.read_text(encoding="utf-8"))]
    assert commands
    assert [span for span in commands if not ALLOWED_HARNESS_COMMAND.fullmatch(span)] == []
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert not [word for word in RETIRED_HARNESS_SETUP if word in text], path
    for slug in _orchestrators():
        for path in (live_bundle / "agents" / f"{slug}.agent.md", live_bundle / "skills" / slug / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            assert re.search(rf"`& {CLI_HARNESS_COMMAND}`", text), path
            assert "resolve-step-model" in text, path
            assert [phrase for phrase in HOOK_ANSWER_PROSE if phrase not in text] == [], path
            assert [phrase for phrase in WRITE_TOOL_PROSE if phrase not in text] == [], path
        skill = (live_bundle / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        assert re.search(rf"`{VSCODE_HARNESS_COMMAND}`", skill), slug
        assert "In both hosts your shell or terminal does NOT run this command" in skill, slug
        assert "`Tool execution denied: SAFe agentic harness RESULT (<function>): …`" in skill, slug
        assert "`<PreToolUse-context>`" in skill, slug


def test_live_bundle_dispatches_namespaced_agents_once_per_step(live_bundle: Path) -> None:
    plugin = json.loads((live_bundle / "plugin.json").read_text(encoding="utf-8"))["name"]
    namespaced = f'agent_type: "{plugin}:<'
    for slug in _orchestrators():
        for path in (live_bundle / "agents" / f"{slug}.agent.md", live_bundle / "skills" / slug / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            assert namespaced in text, path
            assert re.findall(r'agent_type: "([^"]+)"', text) == [f"{plugin}:<agent-id>"] * len(re.findall(r'agent_type: "', text)), path
            assert "--bound-model" not in text and "boundModels" not in text, path
        skill = (live_bundle / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        assert "step-session-bound" in skill, slug
        assert "Unknown agent_type" in skill, slug
    binding = (live_bundle / "agents" / "developer.agent.md").read_text(encoding="utf-8")
    assert f"`agent_type` set to `{plugin}:<actor>`" in binding
    assert f"`{plugin}:release-train-engineer`" in binding
    assert "exactly once" in binding and "step-session-bound" in binding


def test_live_bundle_skills_are_cli_skill_folders(live_bundle: Path) -> None:
    sources = {path.name[: -len(".skill.md")] for path in (ORG / "skills").glob("*.skill.md")}
    folders = {path.parent.name for path in (live_bundle / "skills").glob("*/SKILL.md")}
    assert folders == sources
    for stem in folders:
        meta = parse_frontmatter(live_bundle / "skills" / stem / "SKILL.md")
        assert meta["name"] == stem
        assert 0 < len(meta["description"]) <= 1024
        assert (live_bundle / "skills" / f"{stem}.skill.md").is_file()


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


def test_live_bundle_never_adds_broken_links(live_bundle: Path) -> None:
    source = _broken_links([*(ORG / "agents").glob("*.agent.md"), *(ORG / "skills").glob("*.skill.md")])
    bundle = _broken_links([*(live_bundle / "agents").glob("*.agent.md"), *(live_bundle / "skills").glob("*/SKILL.md")])
    assert len(bundle) <= len(source)
    assert not [link for link in bundle if "SKILL.md" in link.split(" -> ", 1)[1]]


def test_cli_manifest_tracks_vscode_manifest() -> None:
    cli = json.loads((BUILD / "plugin.json").read_text(encoding="utf-8"))
    vscode = json.loads((ORG / "builds" / "github-copilot" / "plugin.json").read_text(encoding="utf-8"))
    assert (cli["name"], cli["version"], cli["description"]) == (vscode["name"], vscode["version"], vscode["description"])
