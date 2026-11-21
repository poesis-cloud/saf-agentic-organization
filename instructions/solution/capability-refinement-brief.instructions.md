---
description: 'Workflow brief of capability-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Capability refinement (`capability-refinement`)

Write or thicken one Capability so it is ready for Pre-Plan: benefit hypothesis, acceptance criteria, WSJF and the Features each ART would take.

- **Main artifact:** `capability` at `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/<capability-slug>.capability.md` (template `templates/solution/capability.artifact-template.md`), owned by `solution-manager`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/challenges/capability-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-architect`, `systems-engineer`, `security-expert`, `compliance-officer`.

## Draft

- One Capability per run, sized to fit a PI. Create it with `status: funnel`, or thicken it without changing its status.
- Write the benefit hypothesis and testable acceptance criteria; estimate WSJF against the other capabilities.
- Outline the Feature split per ART and the cross-ART and supplier dependencies. Set `parent` when it splits from an Epic.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Does it fit one PI, and can its acceptance be demonstrated at a Solution Demo?
- Which Solution Intent constraints apply?

## Revise

Done when: Benefit hypothesis, acceptance criteria, WSJF and the candidate Feature split are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

Solution Management's human lead decides whether the Capability is ready. Next: `capability-transition` to record the move; then `pre-plan`.
