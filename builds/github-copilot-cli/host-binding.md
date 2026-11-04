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
- **Harness commands (orchestrators only).** Run exactly one plain command through the shell tool
  (`bash` on Linux/macOS, `powershell` on Windows), synchronously:
  `[&] <python | py -3 | interpreter full path> <installed harness.py> resolve-step --workflow-slug <slug>`
  or the same with `resolve-step-model`. Take the interpreter and `harness.py` path from the
  harness context injected when the session opened. Nothing else is allowed: no chaining (`;`,
  `&&`, `||`, `|`), no redirection, no `cd` or environment prefix, no other harness function, and
  never `--session-id` / `--parent-session-id`. The hooks stamp the session and deny any other
  form.
- **Writing artifacts.** Write every file with `create` / `edit`, never through the shell
  (`echo >`, `Set-Content`, `Out-File`, heredocs, scripts). The harness authorizes and
  schema-checks only file-tool writes, and reverts an invalid one.
- **Skills.** Load a skill by name with the `skill` tool. The name is the source file stem
  (`team-verification`, `program-pi-planning`, …). When the harness injects a load directive
  naming a framework file (`<framework root>/skills/<name>.skill.md`), read that file.
- **Framework paths.** Relative framework paths in this agent and its skills (`workflows/`,
  `conf/`, `templates/`, `artifacts/`, `instructions/`, `skills/`) resolve against the framework
  root that the injected harness context names, never against the current folder. Artifacts
  are written in the workspace that the same context names.
- **Hooks.** The harness hooks run only in a trusted folder. If no harness context was injected
  when this session opened, say so before the first dispatch and mark the gate packet
  `harness=unchecked`.
