# Poesis SAFe Agentic Organization

[![CI](https://github.com/poesis-cloud/saf-agentic-organization/actions/workflows/ci.yml/badge.svg)](https://github.com/poesis-cloud/saf-agentic-organization/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/poesis-cloud/saf-agentic-organization)](https://github.com/poesis-cloud/saf-agentic-organization/releases/latest)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

> **SAFe-shaped agentic organization for GitHub Copilot / VS Code and portable agent hosts** —
> multi-agent orchestration (portfolio/program/iteration orchestrators), a framework-owned
> specialist bench, skills, instructions, workflows, artifact schemas, and deterministic model routing.
> Open-source developer tooling from [Poesis Cloud](https://poesis.cloud).

---

> **Note — v0.1:** This repository root is the **host-agnostic source** of the framework. Agents,
> skills, workflows, and configuration are its direct children, but the installable artifact is the
> **rendered host bundle** produced from [`builds/`](builds/) — see [Installing](#installing).

---

## The SAF solution

This repository is one of the three products of the Systemic Agentic Framework (SAF):

| Product | Repository | Role |
|---|---|---|
| Agentic Harness | [`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness) | the deterministic execution engine — methodology- and host-agnostic |
| **SAFe Agentic Organization** | **this repository** | the SAFe-shaped framework application the harness executes |
| Agentic Workspace | [`saf-agentic-workspace`](https://github.com/poesis-cloud/saf-agentic-workspace) | the shared data plane the harness checks and commits into |

The harness resolves this framework through `FRAMEWORK_DIR` and the workspace through
`FRAMEWORK_WORKSPACE_DIR` — the three products stay decoupled through environment-anchored paths,
not through a shared tree.


## Overview

The Poesis SAFe Agentic Framework brings SAFe-shaped multi-agent orchestration into
agent execution environments that support custom agents and skills. It includes:

- **Orchestrators**: `@value-management-officer`, `@release-train-engineer`, `@scrum-master`
- **Specialist bench**: framework-owned author, architecture, development, QA, security, operator, docs, and UX agents
- **Skills**: SAFe ceremony, practice, authoring, and orchestration playbooks loaded on demand
- **Agent-adapted ceremonies**: ART Sync, System Demo, Daily Sync, Retrospective, Inspect & Adapt, PI Planning, iteration plan/review (plus portfolio sync/review and Feature/Story refinement)
- **Model routing**: deterministic LLM tier + capability-score routing — no random model selection
- **Portable harness**: deterministic artifact, gate-packet, and runtime-trace checks independent of VS Code hooks —
  methodology- and host-agnostic, so the same familiar agentic work method follows you from host to host as you
  move between environments (shipped separately as [`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness))

## Layout

The framework is host-agnostic source; each host's manifest lives beside its renderer under
[`builds/`](builds/) (for GitHub Copilot, `builds/github-copilot/plugin.json`):

- [`agents/`](agents/) — the orchestrators and the specialist bench (`<name>.agent.md`)
- [`skills/`](skills/) — SAFe ceremony, practice, authoring, and orchestration playbooks (`<name>.skill.md`)
- [`instructions/`](instructions/) — persistent conventions injected into agent sessions (`<name>.instructions.md`)
- [`workflows/`](workflows/) — SAFe-named ceremony and practice catalogs (`<slug>.workflow.conf.yaml`)
- [`conf/`](conf/) — remaining harness configuration: `model-profiles`, `access-control-list`, `workspace`
- [`templates/`](templates/) — artifact Markdown templates, organized per layer and actor
- [`artifacts/`](artifacts/) — the JSON Schema contract for every artifact kind the workflows produce
- [`builds/`](builds/) — host bundle renderers (currently `github-copilot/`)

## Installing

Two steps, in this order — the bundle must exist before the harness can register its hooks into it.

```bash
# 1. Render the host bundle (this repository, host-agnostic source -> installable artifact)
BUNDLE=/tmp/github-copilot-bundle
python3 builds/github-copilot/render_bundle.py . "$BUNDLE"

# 2. Register the harness hooks (from the harness repository)
make install-hooks FRAMEWORK_DIR=/abs/path/to/saf-agentic-organization BUNDLE_DIR="$BUNDLE"
```

Step 1 injects each agent's `tools:` frontmatter and writes the host manifest. Step 2 renders the
workspace hook file, the orchestrators' session-started hook, and the VS Code settings that enable
hooks at all; it refuses rather than guessing if `BUNDLE_DIR` is omitted. Then install `$BUNDLE`
as the GitHub Copilot customization plugin — or install the published release asset, which is that
same bundle.

Everything step 2 writes is generated and git-ignored: it carries machine-specific absolute paths
and must never be committed.

## Deterministic Harness

The framework's deterministic checks live in the sibling
[`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness) repository and run through its
stable entrypoint `harness.py`. They are host-neutral: a CI job, shell wrapper, VS Code hook, or
another agent runtime can call the same CLI. Point the harness at this repository with
`FRAMEWORK_DIR`.

Four commands (the global options `--portfolio-root`, `--strict`, `--json` come **before** the command):

```bash
# STATE — validate Epic/Feature/Story artifacts (FSM, linkage, schema, gates, derived fields)
python3 ../saf-agentic-harness/harness.py --portfolio-root /path/to/portfolio \
  check-artifact --unit-id sie-observability-foundation

# DRIVE — resolve the next orchestration action (dispatch | halt | done)
python3 ../saf-agentic-harness/harness.py \
  orchestrate --workflow value-management-officer --unit sie-observability-foundation

# CONDITIONS — evaluate one step's conditions and append the session ledger line
python3 ../saf-agentic-harness/harness.py \
  check-step --orchestration value-management-officer --step capture-epic \
  --unit-id sie-observability-foundation --session abc123

# HOOK — funnel a host lifecycle event (JSON on stdin) through the harness
cat event.json | python3 ../saf-agentic-harness/harness.py hook --event preToolUse
```

The harness never writes artifacts — it reports the value/edge; the orchestrator commits.

### Load contract

Point `FRAMEWORK_DIR` at this checkout. Layout keys live in [`.env`](.env) (`FRAMEWORK_*_DIR`);
process environment overrides the file. Workflows live at [workflows/](workflows/). The sibling
[`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness) `ConfigLoader` must
load layout, ACL, model-profiles, workspace, and the workflow catalog without
`ConfigurationError`. Workflow `skills` / `instructions` slugs are filename stems under
`skills/` and `instructions/`. Workflow `artifact` slugs are stems of
`artifacts/<slug>.artifact.schema.json`.

### Verify this organization

```bash
# sibling checkout: ../saf-agentic-harness  (override with SAF_HARNESS_SRC)
python3 -m pip install -r requirements-dev.txt
make verify
```

`make verify` runs unit coherence (slug resolve, ceremony pairs, ACL, required-reading,
plugin 1:1) plus functional live-load (`start-session` / `resolve-step` /
`check-step-authorization` on one portfolio, program, and team workflow). Coverage on
organization Python (`tests/loaders.py` + `render_bundle.py`) must be ≥95%.

The harness constitution itself is verified separately:
`make -C ../saf-agentic-harness verify`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions are accepted under Apache-2.0.
This project uses the [Developer Certificate of Origin (DCO)](https://developercertificate.org/).

---

## License

Apache License, Version 2.0. See [LICENSE](LICENSE).

Copyright 2026 Poesis Cloud and contributors.
