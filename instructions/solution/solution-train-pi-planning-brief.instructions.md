---
description: 'Workflow brief of solution-train-pi-planning: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Solution Train PI Planning (`solution-train-pi-planning`)

Aggregate the ARTs' PI plans into the Solution Train's PI Objectives, planning board and risks for one PI.

- **Main artifact:** `pi-objectives` at `portfolio/solution-trains/<solution-train-slug>/pis/<pi-slug>/pi-objectives.md` (template `templates/solution/pi-objectives.artifact-template.md`), owned by `solution-train-engineer`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/pis/<pi-slug>/challenges/solution-train-pi-planning-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-manager`, `solution-architect`, `systems-engineer`, `business-owner`.

## Draft

- Read the Pre-Plan record and each ART's `pi-objectives.md` for this PI. Set `scope: solution-train`.
- Summarize the ARTs' objectives into Solution Train objectives; show capability delivery, cross-ART dependencies and integration points on the planning board.
- ROAM the solution-level risks. Leave business value and the confidence vote for the human gate.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the ART plans, taken together, deliver each committed capability, with dependencies in a feasible order?
- Which solution-level risk has no owner?

## Revise

Done when: Objectives are split committed and uncommitted; every committed capability is on the board. Every packet of this run has its `challengeLedger` entry.

## Human gate

The solution's Business Owners assign business value and the train commits. Next: `solution-gate-decision` (record the commitment); then `coordinate-and-deliver` during the PI.
