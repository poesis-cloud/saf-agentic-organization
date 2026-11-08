# Poesis SAFe Agentic Organization

[![CI](https://github.com/poesis-cloud/saf-agentic-organization/actions/workflows/ci.yml/badge.svg)](https://github.com/poesis-cloud/saf-agentic-organization/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/poesis-cloud/saf-agentic-organization)](https://github.com/poesis-cloud/saf-agentic-organization/releases/latest)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

> **SAFe-shaped agentic organization for GitHub Copilot / VS Code and portable agent hosts** —
> multi-agent orchestration (portfolio/program/iteration orchestrators), a framework-owned
> specialist bench, skills, instructions, workflows, artifact schemas, and deterministic model routing.
> Open-source developer tooling from [Poesis Cloud](https://poesis.cloud).

---

> **Note — v0.1:** This repository root is the **host-agnostic source** of the framework. The
> installable artifact is the Copilot plugin `poesis-saf-agentic-organization` rendered from
> [`builds/plugin/`](builds/plugin/) — see [Installing](#installing).

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

The Poesis SAFe Agentic Organization brings SAFe-shaped multi-agent orchestration into
agent execution environments that support custom agents and skills. It includes:

- **Orchestrators**: `@value-management-officer`, `@release-train-engineer`, `@scrum-master`
- **Specialist bench**: framework-owned author, architecture, development, QA, security, operator, docs, and UX agents
- **Skills**: SAFe ceremony, practice, authoring, and orchestration playbooks loaded on demand
- **Agent-adapted ceremonies**: ART Sync, System Demo, Team Sync, Iteration Retrospective, Inspect & Adapt, PI Planning, Iteration Planning/Review (plus portfolio sync/review, Strategic Investment Planning, and Feature/Story refinement)
- **Model routing**: deterministic LLM tier + capability-score routing — no random model selection
- **Portable harness**: deterministic artifact, gate-packet, and runtime-trace checks independent of VS Code hooks —
  methodology- and host-agnostic, so the same familiar agentic work method follows you from host to host as you
  move between environments (shipped separately as [`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness))

How a human talks to the organization (principles, per-workflow purpose, NFR model, splitting
versus refinement) is in [docs/usage-model.md](docs/usage-model.md).

## Installing

The organization ships as the Copilot plugin `poesis-saf-agentic-organization`. It needs the
harness plugin `poesis-saf-agentic-harness`; both come from the marketplace
[`poesis-cloud/saf-marketplace`](https://github.com/poesis-cloud/saf-marketplace), as `poesis-saf`
(stable, branch `main`) or `poesis-saf-preview` (pre-releases, branch `preview`).
Requirements: the [Copilot CLI](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli),
Git ≥ 2.38 with a Git identity, and Python ≥ 3.10.

**One command** (Copilot CLI, also used by the GitHub Copilot app). It adds the marketplace if it
is missing and installs both plugins; add `--preview` / `-Preview` for the pre-release channel:

```bash
curl -fsSL https://raw.githubusercontent.com/poesis-cloud/saf-agentic-organization/main/install.sh | sh
```

```powershell
irm https://raw.githubusercontent.com/poesis-cloud/saf-agentic-organization/main/install.ps1 | iex
```

**Manually** with the Copilot CLI (for preview, add `poesis-cloud/saf-marketplace#preview` and
install `@poesis-saf-preview`):

```bash
copilot plugin marketplace add poesis-cloud/saf-marketplace
copilot plugin install poesis-saf-agentic-harness@poesis-saf
copilot plugin install poesis-saf-agentic-organization@poesis-saf
```

**GitHub Copilot app:** Customize → marketplaces → add `poesis-cloud/saf-marketplace`, then
install both plugins. **VS Code:** enable `chat.plugins.enabled`, add the marketplace to
`chat.plugins.marketplaces`, install both plugins, and use Session Target: Copilot.

**From a checkout** (contributors): `make plugin PLUGIN_DIR=<dir>` renders the plugin, then
`copilot plugin install <dir>` installs it.

## Initialising a workspace

The harness governs only a **SAF workspace**: a Git repository whose `HEAD` holds
`.saf/workspace.yaml`. Open the repository in a trusted folder (in an untrusted folder the
harness hooks do not run), start a Copilot session, and ask to initialise it as a SAF workspace.
The `poesis-saf-agentic-organization:init` skill checks Git, writes and commits
`.saf/workspace.yaml` and `.github/copilot/settings.json` (which recommends the marketplace and
enables both plugins for everyone who opens the repository). Then start a new Copilot session and
pick an orchestrator: `value-management-officer`, `release-train-engineer` or `scrum-master`
(`copilot --agent poesis-saf-agentic-organization:<orchestrator>`). One orchestrator session
drives one workflow run; the orchestrator names the next workflow at each return. Host details
are in [docs/hosts/copilot-plugin.md](docs/hosts/copilot-plugin.md).

## Deterministic harness

The [`saf-agentic-harness`](https://github.com/poesis-cloud/saf-agentic-harness) plugin's hooks
resolve each workflow step, its model, instructions and skills, and authorize and check every
artifact write. Orchestrators ask it with one plain `resolve-step` / `resolve-step-model`
command, which the harness hook answers itself. Agents write artifacts with the host's file-edit
tools, never through the shell. **No valid step without artifact:** each step's Copilot session
commits a change to exactly one artifact of its declared kind, with a `stepOutcomes` entry
recording its decision ([docs/step-artifacts.md](docs/step-artifacts.md)). Reports are
indicative; artifacts are the only evidence.

## Layout

- [`agents/`](agents/) — the orchestrators and the specialist bench (`<name>.agent.md`)
- [`skills/`](skills/) — ceremony, practice, authoring, and orchestration playbooks (`<name>.skill.md`)
- [`instructions/`](instructions/) — step instructions per actor; shared refs in `instructions/shared/`
- [`workflows/`](workflows/) — ceremony and practice catalogs by layer (`portfolio/`, `program/`, `team/`)
- [`conf/`](conf/) — harness configuration: `harness`, `model-profiles`, `access-control-list`, `workspace`
- [`templates/`](templates/) and [`artifacts/`](artifacts/) — artifact templates and JSON Schemas
- [`builds/plugin/`](builds/plugin/) — the plugin renderer and its inputs

## Verifying

```bash
python3 -m pip install -r requirements-dev.txt
make verify            # harness checkout at ../saf-agentic-harness (override SAF_HARNESS_SRC)
```

`make verify` runs the coherence, plugin-contract, and live-load tests against the harness, with
≥95% coverage on the organization's Python.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions are accepted under Apache-2.0 with the
[Developer Certificate of Origin](https://developercertificate.org/).

## License

Apache License, Version 2.0. See [LICENSE](LICENSE).

Copyright 2026 Poesis Cloud and contributors.

<!-- roadmap:start -->
## Roadmap

![Roadmap](docs/roadmap.svg)

<!-- roadmap:end -->
