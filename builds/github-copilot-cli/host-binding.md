<!-- Copyright 2026 Poesis Cloud and contributors

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. -->

## Host binding — GitHub Copilot app / Copilot CLI

Rendered by `builds/github-copilot-cli`; it binds the host-agnostic prose above to this host.

- **Dispatch (orchestrators only).** The subagent-dispatch tool is `task`. Dispatch a step with
  `agent_type` set to the step's `actor` exactly — one of {{AGENT_IDS}} (no `@`). Dispatch
  synchronously: background mode is denied for governed steps. Pass the model the harness resolved
  (`resolve-step-model`) as the `task` `model` argument, verbatim; never pick, omit, or hardcode one.
- **Harness commands.** Run `python <harness>/harness.py resolve-step --workflow-slug <slug>` and
  `python <harness>/harness.py resolve-step-model` through the shell tool (`bash` on Linux/macOS,
  `powershell` on Windows), synchronously, and never with `--session-id` / `--parent-session-id`:
  the harness hooks stamp the session; a command that carries them is denied. No other harness
  function is agent-invoked. `<harness>` is the harness checkout the injected harness context
  names; its Python is the one the harness was installed with (a venv on Windows and Linux/macOS).
- **Skills.** Load a skill by name with the `skill` tool — the name is the source file stem
  (`team-verification`, `program-pi-planning`, …). When the harness injects a load directive
  naming a framework file (`<FRAMEWORK_DIR>/skills/<name>.skill.md`), read that file.
- **Framework paths.** Relative framework paths in this agent and its skills (`workflows/`,
  `conf/`, `templates/`, `artifacts/`, `instructions/`, `skills/`) resolve against the framework
  root — the `FRAMEWORK_DIR` environment variable (`$FRAMEWORK_DIR` in bash,
  `$env:FRAMEWORK_DIR` in PowerShell) — never against the current folder. Artifacts are written
  in the workspace (`FRAMEWORK_WORKSPACE_DIR`, the trusted folder open in the app).
- **Hooks.** The harness hooks run only in a trusted folder. If no harness context was injected
  when this session opened, say so before the first dispatch and mark the gate packet
  `harness=unchecked`.
