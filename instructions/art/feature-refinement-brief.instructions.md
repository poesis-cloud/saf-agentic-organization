---
description: 'Workflow brief of feature-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Feature refinement (`feature-refinement`)

Write or thicken one business Feature so it is ready for PI Planning: benefit hypothesis, acceptance criteria and WSJF.

- **Main artifact:** `feature` at `portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature.md` (template `templates/art/feature.artifact-template.md`), owned by `product-manager`.
- **Challenge packets:** `portfolio/arts/<art-slug>/features/<feature-slug>/challenges/feature-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `system-architect`, `software-engineer`, `quality-engineer`, `security-expert`, `ux-designer`, `data-protection-officer`.

## Draft

- One Feature per run, sized to fit a PI (generally under two months of total effort). Create it with `status: funnel`, or thicken it without changing its status.
- Write the benefit hypothesis and independently testable acceptance criteria; list the NFR ids that apply; estimate WSJF against the other Features.
- Set `parent` when it splits from an Epic or Capability. Architecture decisions, new NFRs and enabler Features are not written here: name them under Dependencies.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Could a team demonstrate each acceptance criterion at a System Demo?
- Does it fit one PI, or should it be split?

## Revise

Done when: Benefit hypothesis, acceptance criteria, NFR applicability and WSJF are filled; unknowns sit under Open questions. Every packet of this run has its `challengeLedger` entry.

## Human gate

Product Management's human lead decides whether the Feature is ready for PI Planning. Next: `feature-transition` to record the move; then `pi-planning`.
