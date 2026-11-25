# Host build — the Claude Code plugin

`builds/claude-plugin/` renders this host-agnostic source into the Claude Code plugin
`poesis-saf-agentic-organization`. The harness ships separately as the Claude Code plugin
`poesis-saf-agentic-harness` (rendered by the harness's `make plugin-claude`); its
`def/adapter/claude-code/spec.md` specification is binding on this build.

## Inputs

| File | Role |
| --- | --- |
| `builds/plugin/plugin.json` | The manifest is the Copilot build's, without its Agent Plugins keys (`$schema`, `extensions`): one name and one version for both hosts. |
| `builds/plugin/tools.yaml` | The per-agent tool lists, as host-agnostic aliases (generated from the model). |
| `tools.yaml` | The Claude Code vocabulary: each alias → the Claude Code tools it grants (`edit` → `Write`, `Edit`; `agent` → `Agent`; …). |
| `host-binding.md` | Section appended to every rendered agent: dispatch with `Agent` and `run_in_background: false`, the one allowed plain harness command form, artifact writes through `Write`/`Edit` only, skill loading, the `init` skill, and the "No harness context" refusal. |
| `bin/register.sh` | The `SessionStart` registration: writes `hosts/claude-code/frameworks/<plugin>/root` (the plugin root) into the per-user SAF registry. |
| `skills/init/SKILL.md` | The workspace initialisation skill (`.saf/workspace.yaml`, written and committed in one `Bash` command). |
| `render_claude_plugin.py` | `render_claude_plugin.py <source-root> <plugin-root>` (or `make plugin-claude CLAUDE_PLUGIN_DIR=<plugin-root>`). It reuses the Copilot build's renderer for everything host-agnostic (layout, links, skills, staging and in-place promotion), and refuses the same unsafe targets. |

## Plugin layout

The plugin root is the framework root the harness registry records, so it holds the framework's
`.env` and `conf/`:

```text
<plugin>/
├── .claude-plugin/plugin.json      the manifest
├── .env                            layout: every FRAMEWORK_*_DIR under framework/
├── conf/                           harness.conf.yaml (harness version range) and the rest
├── framework/{agents,artifacts,instructions,skills,templates,workflows}/
├── agents/<slug>.md                tools:, links re-anchored, binding appended (no hooks)
├── hooks/hooks.json                SessionStart: the registration only
├── bin/register.sh
├── skills/<stem>/SKILL.md          one Agent Skill per source skill, plus init
├── docs/{usage-model,step-artifacts}.md
└── LICENSE NOTICE README.md
```

## Host-specific decisions

- **No agent-scoped hooks.** Claude Code names the conversation's selected agent in every
  hook payload (`agent_type`), so the harness plugin's global `UserPromptSubmit` opens the
  orchestrator's session (H0). The framework plugin carries only its registration.
- **Dispatch.** Orchestrators dispatch with the `Agent` tool, `subagent_type`
  `poesis-saf-agentic-organization:<actor>` (plugin agents are namespaced), and
  `run_in_background: false`: Claude Code may run a dispatch that omits it in the background,
  and the harness denies such a dispatch because the step's return could not be evaluated.
- **Model routing.** The harness adapter's `models.yaml` maps each catalogue slug to a Claude
  Code model alias (`opus`, `sonnet`, `haiku`, `fable`), the only values the `Agent` tool's
  `model` accepts. Each alias runs the account's current model of that family.
- **Artifact writes.** `Write` and `Edit` are the file tools; the harness authorizes (H3) and
  checks (H5) both. A write the harness rejects is reverted and reported to the agent next to
  the tool result.
- **Human gate.** Orchestrators ask the user in the conversation (`AskUserQuestion` in an
  interactive session). Non-interactive runs (`claude -p`) cannot hold a human gate.
- **Workspace initialisation.** The `init` skill writes and commits `.saf/workspace.yaml` in one
  `Bash` command. It writes no Claude Code settings: the plugins are not published in a
  marketplace yet.

## Install

Until both plugins are published, render them and load them per session:

```bash
make plugin-claude CLAUDE_PLUGIN_DIR=../saf-agentic-organization-claude-plugin
# in saf-agentic-harness:
make plugin-claude CLAUDE_PLUGIN_DIR=../saf-agentic-harness-claude-plugin
cd <your SAF workspace>
claude --plugin-dir <harness plugin> --plugin-dir <organization plugin> \
       --agent poesis-saf-agentic-organization:release-train-engineer
```
