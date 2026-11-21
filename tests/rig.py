"""A fixture workspace driven through the real harness, the way a host drives it.

Each step instance runs in its own worker session: preconditions (function 5), registration
(function 0), authorization (function 8), the write, the commit gate (function 9) and the
postconditions with promotion (function 10). Nothing is mocked: the session logs and Git refs the
organization's conditions read are the ones the harness writes.
"""

from __future__ import annotations

import json
import re
import subprocess
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Mapping

from tests.loaders import INSTRUCTION_SUFFIX, PLACEHOLDER, fill_template, load_workflows, organization_root

from application import Application

ORG = organization_root()
FLAGS = {
    "sessionId": "--session-id",
    "parentSessionId": "--parent-session-id",
    "agent": "--agent",
    "workflowSlug": "--workflow-slug",
    "artifactPath": "--artifact-path",
    "artifactPaths": "--artifact-path",
    "action": "--action",
}
LAYOUT_ENV = {
    "FRAMEWORK_AGENTS_DIR": "agents",
    "FRAMEWORK_ARTIFACTS_DIR": "artifacts",
    "FRAMEWORK_INSTRUCTIONS_DIR": "instructions",
    "FRAMEWORK_SKILLS_DIR": "skills",
    "FRAMEWORK_TEMPLATES_DIR": "templates",
    "FRAMEWORK_WORKFLOWS_DIR": "workflows",
}
DATE = "2026-11-21"


def concrete(path: str, **slugs: str) -> str:
    """A layout path with its `<name-slug>` variables bound (default: the variable's own noun)."""
    return PLACEHOLDER.sub(lambda match: slugs.get(match.group(0)[1:-1].replace("-", "_"), match.group(0)[1:-6]), path)


def brief_paths(workflow_slug: str) -> dict[str, str]:
    """The paths and templates a workflow brief gives its actors: main, packets, record, board."""
    layer = load_workflows()[workflow_slug]["layer"]
    text = (ORG / "instructions" / layer / f"{workflow_slug}-brief{INSTRUCTION_SUFFIX}").read_text(encoding="utf-8")
    found: dict[str, str] = {}
    for label, key in (("Main artifact", "main"), ("Item", "main"), ("Record", "main"), ("Challenge packets", "packets"), ("Board", "board")):
        match = re.search(rf"\*\*{label}:\*\* (?:`[a-z-]+` at )?`([^`]+)`(?:[^\n]*?\(template `templates/([^`]+)\.artifact-template\.md`\))?", text)
        if match:
            found[key] = match.group(1)
            if match.group(2):
                found[f"{key}Template"] = match.group(2)
    return found


def outcome(step: str, value: str) -> dict[str, str]:
    return {"step": step, "outcome": value, "date": DATE, "note": f"{value} in {step}"}


def git(workspace: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True, text=True).stdout.strip()


def init_workspace(workspace: Path) -> None:
    workspace.mkdir()
    git(workspace, "init", "-q")
    git(workspace, "config", "user.email", "tests@poesis.cloud")
    git(workspace, "config", "user.name", "organization-tests")
    git(workspace, "commit", "-q", "--allow-empty", "-m", "init")


class Rig:
    """The organization's harness over one fixture workspace."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self._application: Application | None = None
        self._sessions = 0

    def invoke(self, function: str, **flags: Any) -> dict[str, Any]:
        if self._application is None:
            self._application = Application(ORG)
        argv = [function]
        for key, value in flags.items():
            for item in value if isinstance(value, (list, tuple)) else (value,):
                argv.extend((FLAGS[key], str(item)))
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self._application.dispatch_command(argv)
        assert code == 0, err.getvalue() or out.getvalue()
        return json.loads(out.getvalue())

    def seed(self, path: str, template: str, overrides: Mapping[str, Any] | None = None) -> str:
        """Commit one artifact straight onto the workspace branch: state that existed before the run."""
        self.write(path, template, overrides)
        git(self.workspace, "add", "-A")
        git(self.workspace, "commit", "-q", "-m", f"seed {path}")
        return path

    def write(self, path: str, template: str, overrides: Mapping[str, Any] | None = None) -> None:
        target = self.workspace / path
        _, text = fill_template(template, Path(path).name.split(".")[0], overrides)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def read(self, path: str) -> dict[str, Any]:
        import yaml

        text = (self.workspace / path).read_text(encoding="utf-8")
        return yaml.safe_load(text.split("---\n", 2)[1])

    def open(self, workflow_slug: str) -> str:
        self._sessions += 1
        session = f"orchestrator-{self._sessions}"
        started = self.invoke("start-session", sessionId=session, agent=load_workflows()[workflow_slug]["orchestrator"])
        assert started["outcome"]["status"] == "started", started
        return session

    def resolve(self, session: str, workflow_slug: str) -> dict[str, Any]:
        return self.invoke("resolve-step", sessionId=session, workflowSlug=workflow_slug)

    def next_step(self, session: str, workflow_slug: str, expected: str) -> dict[str, Any]:
        resolved = self.resolve(session, workflow_slug)
        assert resolved["outcome"]["status"] == "step-resolution", resolved
        assert resolved["step"]["slug"] == expected, resolved["step"]["slug"]
        return resolved["step"]

    def preconditions(self, session: str) -> dict[str, Any]:
        return self.invoke("check-step-preconditions", sessionId=session)

    def deliver(self, session: str, step: Mapping[str, Any], path: str, template: str, overrides: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Run one step instance in its own worker session, through function 10."""
        gate = self.preconditions(session)
        assert gate["outcome"]["status"] == "pass", gate
        self._sessions += 1
        worker = f"{step['actor']}-{self._sessions}"
        started = self.invoke("start-session", sessionId=worker, parentSessionId=session, agent=step["actor"])
        assert started["outcome"]["status"] == "started", started
        action = "update" if (self.workspace / path).exists() else "create"
        authorized = self.invoke("check-step-authorization", sessionId=worker, artifactPath=path, action=action)
        assert authorized["outcome"]["status"] == "allowed", authorized
        self.write(path, template, overrides)
        checked = self.invoke("check-step-artifact", sessionId=worker, artifactPaths=[path])
        assert checked["outcome"]["status"] == "valid", checked
        return self.invoke("check-step-postconditions", sessionId=session)


def failed_conditions(report: Mapping[str, Any]) -> list[str]:
    return [check["condition"]["slug"] for check in report["conditionChecks"] if check["outcome"] != "pass"]
