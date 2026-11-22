---
description: 'Workflow brief of solution-roadmap: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Solution Roadmap (`solution-roadmap`)

Forecast the solution's deliverables: a PI roadmap (one committed PI, two forecast) and a multi-year view.

- **Main artifact:** `solution-roadmap` at `portfolio/solution-trains/<solution-train-slug>/solution-roadmap.md` (template `templates/solution/solution-roadmap.artifact-template.md`), owned by `solution-manager`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/challenges/solution-roadmap-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-architect`, `systems-engineer`, `release-manager`.

## Draft

- Read the Solution Vision, the capabilities and their status, and the ARTs' PI roadmaps.
- The current PI is committed; the next two are a forecast; beyond is intent.
- Show integration points, Solution Demos and supplier dates.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the forecasts respect integration order and supplier lead times?
- Is anything shown as committed that no train committed to?

## Revise

Done when: Committed, forecast and intent are distinct; fixed dates are flagged. Every packet of this run has its `challengeLedger` entry.

## Human gate

Solution Management's human lead decides whether to communicate this roadmap. Next: `solution-gate-decision`.
