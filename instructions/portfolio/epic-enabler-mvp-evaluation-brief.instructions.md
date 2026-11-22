---
description: 'Workflow brief of epic-enabler-mvp-evaluation: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Enabler Epic MVP evaluation (`epic-enabler-mvp-evaluation`)

Evaluate the MVP of one implementing enabler Epic against its hypothesis and recommend to persevere, pivot or stop.

- **Main artifact:** `epic-enabler` at `portfolio/epics/<epic-slug>/<epic-slug>.epic-enabler.md` (template `templates/portfolio/epic-enabler.artifact-template.md`), owned by `enterprise-architect`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/epic-enabler-mvp-evaluation-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `data-analyst`, `business-owner`, `financial-controller`.

## Draft

- Read the enabler Epic, its Lean Business Case, and the evidence the human or the trains provide (enabled Features delivered, platform or pipeline measures).
- Under `## MVP`, record the evidence against each leading indicator, then the recommendation: persevere, pivot (to which new hypothesis) or stop.
- Do not change `status`, `implementationStage` or `resolution`: they move in `epic-enabler-transition` after the human decided.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Does the evidence show the enabled Epics using the runway, or only that it was built?
- Is the recommendation free of sunk-cost reasoning?

## Revise

Done when: Each leading indicator has a result or an explicit gap; the recommendation follows from the evidence. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides to persevere, pivot or stop. Next: `epic-enabler-transition` to record it; a pivot starts a new `epic-enabler-hypothesis`.
