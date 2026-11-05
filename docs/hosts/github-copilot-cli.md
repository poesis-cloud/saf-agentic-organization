# Host build — GitHub Copilot app / Copilot CLI

`builds/github-copilot-cli/` renders this host-agnostic source into a Copilot CLI plugin, the
runtime the GitHub Copilot desktop app embeds. The VS Code build (`builds/github-copilot/`) is
untouched; both read the same `agents/`, `skills/`, `workflows/`, and `conf/`.

## Inputs

| File | Role |
| --- | --- |
| `plugin.json` | Legacy-layout manifest: `name`, `version`, `description` (tracked against the VS Code manifest by a test), `agents: agents/`, `skills: skills/`. No `hooks` key. |
| `tools.yaml` | Per-agent `tools:` as CLI aliases. Orchestrators: `read, edit, search, execute, agent, skill, ask_user`. Bench: `read, edit, search, execute, skill`. Must list exactly the source agents. |
| `host-binding.md` | Section appended to every rendered agent: dispatch with `task`, actors never asking the harness (`not-facilitator`) or reading its source, one workflow instance per orchestrator session, the one allowed plain harness command form, artifact writes through `create`/`edit`/`apply_patch` only, skill loading, framework-path anchoring on the injected harness context, and the trust note. |
| `render_bundle.py` | `render_bundle.py <source-root> <bundle-root>`. Renders into a sibling staging directory and, only when the render succeeds, updates an existing bundle in place (changed files replaced, new ones added, stale ones removed; the bundle directory itself is never renamed, so a live-loaded bundle re-renders on Windows), so a refused source leaves the earlier bundle intact. Refuses any target that is the source, an ancestor of it, inside its `builds/` subtree, or an existing path that is not an earlier bundle. |

## Bundle layout

```text
<bundle>/
├── plugin.json                       manifest ($license stripped)
├── .github/plugin/marketplace.json   one-plugin local marketplace (source ".")
├── agents/<slug>.agent.md            tools: rewritten, links re-anchored, binding appended
├── skills/<stem>/SKILL.md            one folder per source skill, name: <stem>
├── skills/<stem>.skill.md            flat source skills (the harness load directives name these)
├── workflows/ conf/ instructions/ templates/ artifacts/   framework layout from .env
└── .env LICENSE NOTICE README.md
```

Written later by the harness installer (`adapters/github-copilot-cli/install.py --framework-dir
<org checkout> --bundle-dir <bundle> [--workspace-dir <portfolio>] [--hooks-target
plugin|repo|user] [--hook-style exec|shell]`, or `make install-hooks-copilot-cli FRAMEWORK_DIR=…
BUNDLE_DIR=… [WORKSPACE_DIR=…] [HARNESS_PYTHON=…]`), never by the renderer:

- `hooks.json`, the plugin-level hook file the CLI picks up from the plugin root. Each hook's
  `env` carries `FRAMEWORK_DIR` and every `FRAMEWORK_*_DIR`, so no user-level variables are set;
- the agent-scoped `hooks:` block between `# >>> safe-harness copilot-cli >>>` /
  `# <<< safe-harness copilot-cli <<<` in each orchestrator's frontmatter;
- with `--hooks-target repo`, `<portfolio>/.github/hooks/safe-harness-copilot-cli.json` instead
  of `hooks.json`.

The renderer refuses a source agent that declares `hooks:` and a manifest with `hooks`, so the
installer's slots are always free. A test injects a marker block into a rendered orchestrator and
checks that the frontmatter still parses.

## Host-specific decisions

- **Dispatch.** Orchestrators dispatch with `task`, synchronously, passing the model
  `resolve-step-model` returned as `model`. Plugin agents are namespaced by the plugin name, so
  `agent_type` is `poesis-saf-agentic-organization:<actor>`; a bare actor id is refused as
  "Unknown agent_type". The same prefix selects an orchestrator
  (`--agent poesis-saf-agentic-organization:<orchestrator>`), and the harness adapter strips it.
  The renderer fills the binding's namespaced agent list from `plugin.json` `name`, and a test
  keeps the orchestrator skills' prefix equal to it.
- **One step = one session.** The harness binds each resolved step to the one session that runs
  it and refuses a second (`step-session-bound`). Orchestrators dispatch each resolved step
  exactly once; after a failure they ask `resolve-step` again and dispatch the new resolution,
  never re-dispatching on their own. A user KO reiterates the workflow as a new instance.
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
  ones an actor has depends on its model's tool set: GPT-family models write with `apply_patch`.
  The harness authorizes (H3) and checks (H5) all three, never a shell write. So the binding and
  the orchestrator skills name all three, forbid writing files through the shell, and every
  dispatch restates the rule to the actor.
- **Model routing.** `conf/model-profiles.conf.yaml` holds canonical slugs only. The harness
  adapter's `models.yaml` maps them to host model ids; the bundle never hardcodes one.
  `resolve-step-model` ranks the whole catalogue, so the catalogue holds only models this app
  offers and both adapters bind. Each adapter refuses, at every hook load, a catalogue slug its
  `models.yaml` does not bind (a bootstrap failure, so `preToolUse` denies); a functional test
  checks the bindings against the harness checkout.
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
- **Install.** `copilot plugin install <path>` copies the plugin and is deprecated for direct
  paths. A local marketplace (`copilot plugin marketplace add <bundle>`, then
  `install <plugin>@<plugin>-local`) loads the bundle live from its directory. A harness re-install
  or re-render then takes effect in the next session with no reinstall.

## Verification evidence (Copilot CLI 1.0.105, Linux)

- `copilot plugin marketplace add` / `plugin install`: accepted, `Installed 37 skills`, `source: live`.
- Session debug log: `Plugin activation [agents]: … loaded=14`.
- Not verifiable offline: model-backed dispatch and hook execution. These need an authenticated
  session in a trusted folder, which is the live trial in the GitHub Copilot app.

## Known source debt (not changed here)

The source agents and skills carry about 240 relative links left over from an older nested
layout (`../../../../artifacts/…`, `../scrum-master/scrum-master.skill.md`, …). They are broken
in the source and in both bundles. The CLI bundle reproduces them and adds none.
