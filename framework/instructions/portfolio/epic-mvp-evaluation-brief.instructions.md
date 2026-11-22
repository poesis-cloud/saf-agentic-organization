---
description: 'Workflow brief of epic-mvp-evaluation: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Epic MVP evaluation (`epic-mvp-evaluation`)

Evaluate the MVP of one implementing Epic against its hypothesis and recommend to persevere, pivot or stop.

- **Main artifact:** `epic` at `portfolio/epics/<epic-slug>/<epic-slug>.epic.md` (template `templates/portfolio/epic.artifact-template.md`), owned by `epic-owner`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/epic-mvp-evaluation-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `data-analyst`, `business-owner`, `financial-controller`.

## Draft

- Read the Epic, its Lean Business Case, and the evidence the human or the trains provide (demos, measures, Feature outcomes).
- Under `## MVP`, record the evidence against each leading indicator, then the recommendation: persevere, pivot (to which new hypothesis) or stop.
- Do not change `status`, `implementationStage` or `resolution`: they move in `epic-transition` after the human decided.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Does the evidence measure the hypothesis, or only that work was delivered?
- Is the recommendation free of sunk-cost reasoning?

## Revise

Done when: Each leading indicator has a result or an explicit gap; the recommendation follows from the evidence. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides to persevere, pivot or stop. Next: `epic-transition` to record it; a pivot starts a new `epic-hypothesis`.
