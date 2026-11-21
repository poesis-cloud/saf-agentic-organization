---
description: 'Workflow brief of epic-enabler-hypothesis: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Enabler Epic hypothesis (`epic-enabler-hypothesis`)

Capture or thicken one enabler Epic (runway, platform, exploration or compliance) as an Epic hypothesis ready for Portfolio Leadership to review.

- **Main artifact:** `epic-enabler` at `portfolio/epics/<epic-slug>/<epic-slug>.epic-enabler.md` (template `templates/portfolio/epic-enabler.artifact-template.md`), owned by `enterprise-architect`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/epic-enabler-hypothesis-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-architect`, `platform-engineer`, `business-owner`, `finops-engineer`, `data-analyst`.

## Draft

- One enabler Epic per run, with its `enablerType`. Create it with `status: funnel`, or thicken the existing one without changing its status.
- Write the hypothesis and outcomes as what the business Epics listed in `enables` gain; name leading indicators that show the runway is used.
- Estimate WSJF against all Epics, business ones included: they compete for the same budget. Outline the MVP in one paragraph; the Lean Business Case details it later.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Does a named business Epic need this runway soon, or is it built ahead of need?
- Is this an Epic, or enabler work that fits in a PI and belongs to a train?

## Revise

Done when: Hypothesis, outcomes, enabled work, leading indicators, `enablerType` and WSJF are filled; unknowns sit under Open questions with an assumption. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides whether the enabler Epic is worth reviewing, then analyzing. Next: `epic-enabler-transition` to record the move (funnel → reviewing → analyzing); once analyzing, `epic-enabler-lean-business-case`.
