---
description: 'Workflow brief of capability-enabler-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Enabler Capability refinement (`capability-enabler-refinement`)

Write or thicken one enabler Capability that extends the runway of the large solution, so it is ready for Pre-Plan.

- **Main artifact:** `capability-enabler` at `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/<capability-slug>.capability-enabler.md` (template `templates/solution/capability-enabler.artifact-template.md`), owned by `solution-architect`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/challenges/capability-enabler-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-manager`, `systems-engineer`, `security-expert`, `compliance-officer`, `platform-engineer`.

## Draft

- One enabler Capability per run, sized to fit a PI, with its `enablerType`. Create it with `status: funnel`, or thicken it without changing its status.
- State the benefit as what it makes possible or faster for the Capabilities listed in `enables`; write acceptance criteria demonstrable at a Solution Demo.
- Estimate WSJF against all Capabilities, business ones included. Outline the enabler Feature split per ART; set `parent` when it splits from an Epic or enabler Epic.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the runway built just in time for the Capabilities that need it, and which variable intent does it close?
- Can completion be demonstrated on the integrated solution?

## Revise

Done when: `enablerType`, the Capabilities enabled, acceptance criteria, WSJF and the candidate split are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

Solution Management's human lead and the solution's architects decide whether the enabler Capability is ready. Next: `capability-enabler-transition` to record the move; then `pre-plan`.
