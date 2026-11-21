---
description: 'Workflow brief of pi-planning: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# PI Planning (`pi-planning`)

Plan one PI for the ART: team and ART PI Objectives, the planning board and the PI risks.

- **Main artifact:** `pi-objectives` at `portfolio/arts/<art-slug>/pis/<pi-slug>/pi-objectives.md` (template `templates/art/pi-objectives.artifact-template.md`), owned by `release-train-engineer`.
- **Challenge packets:** `portfolio/arts/<art-slug>/pis/<pi-slug>/challenges/pi-planning-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `product-manager`, `system-architect`, `software-engineer`, `business-owner`.

## Draft

- Read the Product Vision, PI Roadmap, the ready Features in WSJF order, the ART canvas and team charters. Set `scope: art`.
- Per team: objectives stated as outcomes, committed or uncommitted, within capacity; plan no work in the IP iteration.
- Place Features and dependencies on the planning board and list the PI risks. Propose business value; the Business Owners assign it at the gate.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is each team's load within its capacity, with uncommitted objectives absorbing the uncertainty?
- Is every cross-team dependency placed before the iteration that needs it?

## Revise

Done when: Objectives are split committed and uncommitted per team; risks are listed with a ROAM state. Every packet of this run has its `challengeLedger` entry.

## Human gate

The Business Owners assign business value and the ART commits with a confidence vote. Next: `art-gate-decision` (record the commitment and the vote); `feature-transition` for each committed Feature; then `iteration-planning` with each team.
