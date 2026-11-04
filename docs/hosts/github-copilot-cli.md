# Host build — GitHub Copilot app / Copilot CLI

`builds/github-copilot-cli/` renders this host-agnostic source into a Copilot CLI plugin, the
runtime the GitHub Copilot desktop app embeds. The VS Code build (`builds/github-copilot/`) is
untouched; both read the same `agents/`, `skills/`, `workflows/`, and `conf/`.

## Inputs

| File | Role |
| --- | --- |
| `plugin.json` | Legacy-layout manifest: `name`, `version`, `description` (tracked against the VS Code manifest by a test), `agents: agents/`, `skills: skills/`. No `hooks` key. |
| `tools.yaml` | Per-agent `tools:` as CLI aliases. Orchestrators: `read, edit, search, execute, agent, skill, ask_user`. Bench: `read, edit, search, execute, skill`. Must list exactly the source agents. |
| `host-binding.md` | Section appended to every rendered agent: dispatch with `task`, the two agent-invoked harness commands, skill loading, `FRAMEWORK_DIR` path anchoring, and the trust note. |
| `render_bundle.py` | `render_bundle.py <source-root> <bundle-root>`. Wipes and rewrites the bundle and refuses any target that is the source, an ancestor of it, or an existing path that is not an earlier bundle. |

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

Written later by the harness installer, never by the renderer:

- `hooks.json`, the plugin-level hook file the CLI picks up from the plugin root;
- the agent-scoped `hooks:` block between `# >>> safe-harness copilot-cli >>>` /
  `# <<< safe-harness copilot-cli <<<` in each orchestrator's frontmatter;
- optionally `<portfolio>/.github/hooks/safe-harness-copilot-cli.json`.

The renderer refuses a source agent that declares `hooks:` and a manifest with `hooks`, so the
installer's slots are always free. A test injects a marker block into a rendered orchestrator and
checks that the frontmatter still parses.

## Host-specific decisions

- **Dispatch.** Orchestrators dispatch with `task`, `agent_type` = the step's `actor` slug,
  synchronously, passing the model `resolve-step-model` returned as `model`. The orchestrator
  skills name the host's dispatch tool generically; the binding pins it for this host.
- **Model routing.** `conf/model-profiles.conf.yaml` holds canonical slugs only. The harness
  adapter's `models.yaml` maps them to host model ids; the bundle never hardcodes one.
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
