# Host build — the Copilot plugin

`builds/plugin/` renders this host-agnostic source into the Copilot plugin
`poesis-saf-agentic-organization` (Agent Plugins 1.0). One plugin serves every GitHub Copilot
host: the Copilot CLI, the GitHub Copilot app (which embeds it), and VS Code with Session Target:
Copilot. The harness ships separately as the plugin `poesis-saf-agentic-harness`; its `def/`
specifications are binding on this build.

## Inputs

| File | Role |
| --- | --- |
| `plugin.json` | The closed Agent Plugins 1.0 manifest (`name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`). No `agents`, `skills` or `hooks` keys: the host discovers them by convention. Its `version` is the release version. |
| `tools.yaml` | Per-agent `tools:` as Copilot aliases. Must list exactly the source agents. |
| `host-binding.md` | Section appended to every rendered agent: dispatch with `task`, the one allowed plain harness command form, artifact writes through `create`/`edit`/`apply_patch` only, skill loading, the `init` skill, and the "No harness context" refusal. |
| `bin/register.{sh,ps1}` | The `sessionStart` registration: writes `frameworks/<plugin>/root` (the plugin root) into the per-user SAF registry. |
| `skills/init/SKILL.md` | The workspace initialisation skill (`.saf/workspace.yaml`, `.github/copilot/settings.json`). |
| `render_plugin.py` | `render_plugin.py <source-root> <plugin-root>` (or `make plugin PLUGIN_DIR=<plugin-root>`). Renders into a sibling staging directory and only on success updates the plugin root in place, so a refused source leaves the earlier render intact. Refuses a target that is the source, an ancestor of it, inside `builds/`, or an existing path that is not an earlier render. |

## Plugin layout

The plugin root is the framework root the harness registry records, so it holds the framework's
`.env` and `conf/`:

```text
<plugin>/
├── plugin.json                                 Agent Plugins 1.0 manifest
├── .env                                        layout: every FRAMEWORK_*_DIR under framework/
├── conf/                                       harness.conf.yaml (harness version range) and the rest
├── framework/{agents,artifacts,instructions,skills,templates,workflows}/
├── com.github.copilot/agents/<slug>.agent.md   tools:, links re-anchored, binding appended;
│                                               orchestrators carry the scoped H0 hooks
├── com.github.copilot/hooks/hooks.json         sessionStart: the registration only
├── bin/register.{sh,ps1}
├── skills/<stem>/SKILL.md                      one Agent Skill per source skill, plus init
├── docs/{usage-model,step-artifacts}.md        the orchestrators' required reading
└── LICENSE NOTICE README.md
```

The orchestrators' scoped H0 hooks (`userPromptSubmitted`, `userPromptTransformed`) call the
harness's stable per-user launcher in the SAF registry
(`$SAF_AGENTIC_REGISTRY_DIR`, else `~/.local/state/saf-agentic/registry/harness/launcher.sh`, or
`%LOCALAPPDATA%\saf-agentic\registry\harness\launcher.ps1`). The plugin writes no machine path:
everything absolute is resolved by the harness at run time.

## Install and release

- **Users** install from the marketplace `poesis-cloud/saf-marketplace` (`poesis-saf`, or
  `poesis-saf-preview` from its `preview` branch), with `install.sh` / `install.ps1` or
  `copilot plugin install poesis-saf-agentic-organization@<marketplace>` (see the README).
- **Contributors** run `make plugin PLUGIN_DIR=<dir>` and `copilot plugin install <dir>`.
- **CI** renders the plugin, validates `plugin.json` against the Agent Plugins 1.0 schema, and
  installs it with the Copilot CLI.
- **CD** runs on a `v<version>` tag equal to the `plugin.json` version: it publishes the release
  zip, commits the rendered plugin to the orphan branch `copilot-plugin` tagged
  `plugin-v<version>`, and opens a pull request on `poesis-cloud/saf-marketplace` that pins the
  entry to that commit — on `preview` for a pre-release tag (`-alpha`, `-beta`, `-rc`), on `main`
  otherwise.

## Host-specific decisions

- **Dispatch.** Orchestrators dispatch with `task`, synchronously, passing the model
  `resolve-step-model` returned as `model`. Plugin agents are namespaced by the plugin name, so
  `agent_type` is `poesis-saf-agentic-organization:<actor>`; a bare actor id is refused as
  "Unknown agent_type". The same prefix selects an orchestrator
  (`--agent poesis-saf-agentic-organization:<orchestrator>`), and the harness adapter strips it.
  The renderer fills the binding's namespaced agent list from `plugin.json` `name`, and a test
  keeps the orchestrator skills' prefix equal to it.
- **One step = one Copilot session.** The harness binds each resolved step to the one Copilot
  session that runs it and refuses a second (`step-session-bound`). Orchestrators dispatch each resolved step
  exactly once; after a failure they ask `resolve-step` again and dispatch the new resolution,
  never re-dispatching on their own. A user KO reiterates the workflow as a new workflow instance.
- **Harness requests.** An orchestrator asks with ONE plain command, alone in its tool call:
  `& <venv python> <harness.py> resolve-step --workflow-slug <workflow-slug>` or
  `… resolve-step-model` (Linux/macOS: no leading `&`; `python`, `python3`, `py -3` also accepted;
  paths unquoted; never `--session-id`, `$env:`, `;`/`&&`/`|`, or redirection). The adapter never
  edits the command and the shell never runs it: the `preToolUse` hook runs the function for the
  host-observed session and returns the JSON report as a hook denial whose reason starts with
  `SAFe agentic harness RESULT (<function>)`. That is the successful answer, so the agent acts on
  it and does not re-issue the command. Only `SAFe agentic harness REJECTED` means refused, with
  the accepted line. No permission rule, `setx`, or `$env:` setting is needed. The orchestrator
  skills and the binding state this verbatim, and a test enforces the command form.
- **Artifact writes.** The host's file-edit tools are `create`, `edit` and `apply_patch`. Which
  ones an actor has depends on its model's tool set: the runtime picks a `task` subagent's tools
  by model, not only by the agent's `tools:`. The harness authorizes (H3) and checks (H5) all three, never a shell write. So the binding and
  the orchestrator skills name all three, forbid writing files through the shell, and every
  dispatch restates the rule to the actor.
- **Model routing.** `conf/model-profiles.conf.yaml` holds canonical slugs only. The harness
  adapter's `models.yaml` maps them to host model ids; the bundle never hardcodes one.
  `resolve-step-model` ranks the whole catalogue, so the catalogue holds only models this app
  offers and both adapters bind. Each adapter refuses, at every hook load, a catalogue slug its
  `models.yaml` does not bind (a bootstrap failure, so `preToolUse` denies); a functional test
  checks the bindings against the harness checkout. On this host a model is bindable only if its
  `task` subagents get a write tool (`create`/`edit` or `apply_patch`); the catalogue header
  records the models removed for this reason.
- **Unavailable models.** A bound slug can still name a model the app no longer offers (the
  runtime gives hooks no model list). The app does not refuse a `task` `model` it does not offer. It silently
  runs the subagent on another model but keeps the tool set of the model that was named. Trial
  evidence (2026-11-04): `model: gpt-5.5` ran as `claude-sonnet-5.5` with the GPT tool set, so the
  actor's `create` call failed with "Tool 'create' does not exist" and no Epic was written. The
  binding tells orchestrators to report such a model at the gate instead of dispatching.
- **Skills.** The CLI loads only `skills/<name>/SKILL.md` and ignores the flat
  `skills/<name>.skill.md` beside them (verified: `Installed 37 skills`). 20 source skills carry a
  display `name` that differs from the file stem; the bundle sets `name: <stem>`, so the CLI skill
  name equals the harness slug.
- **Links.** `[x.skill.md](x.skill.md)` from an agent becomes `../skills/x/SKILL.md`; skill links
  into the layout (`../workflows/...`) are re-anchored one level deeper. A test asserts that the
  rendered bundle has no more broken links than the source.

## Known source debt (not changed here)

The source agents and skills carry about 240 relative links left over from an older nested
layout (`../../../../artifacts/…`, `../scrum-master/scrum-master.skill.md`, …). They are broken
in the source and in the plugin. The plugin reproduces them and adds none.
