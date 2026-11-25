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

## Host binding — Claude Code (plugin)

Rendered by `builds/claude-plugin`; it binds the host-agnostic prose above to the Claude Code
runtime.

- **Dispatch (orchestrators only).** The subagent-dispatch tool is `Agent`. Plugin agents are
  namespaced: dispatch a step with `subagent_type` set to `{{PLUGIN_NAME}}:<actor>`, the step's
  `actor` behind the plugin name — one of {{AGENT_IDS}} (no `@`). Always pass
  `run_in_background: false`: the harness denies a dispatch that omits it or runs in the
  background, because the step's return must be evaluated. Pass the model the harness names
  for this host in its `resolve-step-model` answer (a Claude Code alias such as `opus`) as the
  `Agent` `model` argument, verbatim; never pick, omit, or hardcode one.
- **One step = one session (orchestrators only).** Dispatch each step the harness resolved
  exactly once. The harness binds the step to that one session and refuses a second
  (`step-session-bound`). After a failed step, ask `resolve-step` again: it resolves the failed
  step again, and you dispatch that new resolution once, relaying the failure messages. Never
  re-dispatch, retry or re-run a step on your own.
- **Actors never ask the harness.** Only the orchestrator runs `resolve-step` /
  `resolve-step-model`; the harness refuses an actor with `not-facilitator`. Every step dispatch
  says so, and that the actor never reads the harness source code or tests.
- **One session, one workflow instance (orchestrators only).** After `no-next-step` this session
  can run no other instance. Tell the user which workflow comes next (for example the
  `*-transition` or gate-decision workflow that records their decision) and that it needs a new
  session: `claude --agent {{PLUGIN_NAME}}:<orchestrator>`. Answer a "drive to the gate" request
  with that plan, one session per run, and start only the first run.
- **Asking the harness (orchestrators only).** Run ONE plain command with the `Bash` tool, alone
  in its tool call: `<python> <harness.py> resolve-step --workflow-slug <workflow-slug>` or
  `<python> <harness.py> resolve-step-model`. `python`, `python3` or `py -3` are also accepted
  as the interpreter; take the paths from the harness context injected at session open. Never
  add `--session-id` / `--parent-session-id`, variable assignments, `;` / `&&` / `|`, or
  redirection.
- **Reading the harness answer.** Your shell does NOT run this command. The harness hook runs it
  for your session and returns its JSON report as the tool response, shown as a hook denial whose
  reason starts with `SAFe agentic harness RESULT (<function>)`. That is the successful answer,
  not an error: act on the report and do not re-issue the command. Only a reason starting with
  `SAFe agentic harness REJECTED` means the request was refused: fix the named problem, using the
  accepted line it gives.
- **Writing artifacts.** Write every file with this host's file tools — `Write` or `Edit` —
  never through the shell (`echo >`, `cat <<EOF`, `tee`, scripts). The harness authorizes and
  schema-checks both, and flags an invalid write as rejected after reverting it; it cannot see a
  shell write.
- **Step evidence.** A step is valid only when its session commits a change to **exactly one**
  instance of its declared artifact kind. Commit it whatever the outcome, with one new
  `stepOutcomes` entry recording the decision (`written`, `revised`, `confirmed`, `no-change` or
  `none`): a write identical to the committed file does not count. Record workflow friction in
  that entry's `friction` note, never as a pain point. Your reply is indicative; the artifact is
  the only evidence.
- **Skills.** Load a skill by name with the `Skill` tool. The name is the source file stem
  (`security-expert`, `product-manager`, …). When the harness injects a load directive naming a
  framework file (`<framework root>/framework/skills/<name>.skill.md`), read that file.
- **Framework paths.** Relative framework paths in this agent and its skills (`workflows/`,
  `templates/`, `artifacts/`, `instructions/`, `skills/`) resolve under `framework/` in the
  framework root that the injected harness context names (`conf/` sits at that root itself),
  never against the current folder. Artifacts are written in the workspace that the same
  context names.
- **Not a SAF workspace (orchestrators only).** When the harness context says this folder is
  not a SAF workspace, offer to initialise it with the `init` skill, run it only on the user's
  yes, and dispatch nothing until a new session opens in the initialised workspace.
- **No harness context (orchestrators only).** The harness context is injected when you receive
  a prompt, by the `poesis-saf-agentic-harness` plugin. If none was injected, refuse to
  dispatch: say the SAF harness is not active, and that the user must install and enable both
  SAF plugins and start a new session.
