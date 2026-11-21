---
description: 'Workflow brief of epic-hypothesis: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Epic hypothesis (`epic-hypothesis`)

Capture or thicken one Epic as an Epic hypothesis statement, ready for Portfolio Leadership to review.

- **Main artifact:** `epic` at `portfolio/epics/<epic-slug>/<epic-slug>.epic.md` (template `templates/portfolio/epic.artifact-template.md`), owned by `epic-owner`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/epic-hypothesis-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `enterprise-architect`, `business-owner`, `data-analyst`.

## Draft

- One Epic per run. Create it with `status: funnel`, or thicken the existing one without changing its status.
- Write the hypothesis statement, the business outcomes hypothesis and leading indicators; set `type` (an enabler Epic extends the runway or improves the value stream).
- Estimate WSJF relatively against the other Epics. Outline the MVP in one paragraph; the Lean Business Case details it later.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the hypothesis falsifiable: could the leading indicators prove it wrong early?
- Is this an Epic, or a Capability or Feature that fits in a PI and belongs to another layer?

## Revise

Done when: Hypothesis, outcomes, leading indicators, scope and WSJF are filled; unknowns sit under Open questions with an assumption. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides whether the Epic is worth reviewing, then analyzing. Next: `epic-transition` to record the move (funnel → reviewing → analyzing); once analyzing, `lean-business-case`.
