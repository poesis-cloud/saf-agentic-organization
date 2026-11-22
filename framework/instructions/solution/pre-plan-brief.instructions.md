---
description: 'Workflow brief of pre-plan: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Pre-Plan (`pre-plan`)

Align and prepare the ARTs and suppliers of the Solution Train for PI Planning.

- **Record:** `event-record` at `portfolio/solution-trains/<solution-train-slug>/events/<event-slug>.pre-plan.md` (template `templates/events/pre-plan.artifact-template.md`), with `event: pre-plan`.

## Agenda

- Solution Vision and roadmap highlights for the PI.
- The ready Capabilities and enabler Capabilities, in WSJF order, and their split into Features per ART.
- Cross-ART and supplier dependencies, and the integration points of the PI.
- Planning context each ART takes into its own PI Planning.

## After the run

Each ART runs `pi-planning` with its Release Train Engineer; then `solution-train-pi-planning`.
