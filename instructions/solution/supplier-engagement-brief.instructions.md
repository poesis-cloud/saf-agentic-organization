---
description: 'Workflow brief of supplier-engagement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Supplier engagement (`supplier-engagement`)

Write or revise the agreement that brings one supplier into the Solution Train's cadence, quality expectations and compliance obligations.

- **Main artifact:** `supplier-agreement` at `portfolio/solution-trains/<solution-train-slug>/suppliers/<supplier-slug>/<supplier-slug>.supplier-agreement.md` (template `templates/solution/supplier-agreement.artifact-template.md`), owned by `procurement-manager`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/suppliers/<supplier-slug>/challenges/supplier-engagement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `legal-counsel`, `security-expert`, `compliance-officer`, `financial-controller`, `solution-architect`.

## Draft

- Read the Solution Intent, the capabilities the supplier contributes to, and the terms the human provides.
- Prefer terms that tolerate variable scope and base acceptance on objective evaluation of working deliverables.
- State how the supplier joins Pre-Plan, PI Planning, the syncs and the Solution Demo. Keep `status: draft`: it moves in `supplier-agreement-transition`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the terms let scope evolve without renegotiation at every PI?
- Which obligations (security, privacy, compliance) pass to the supplier, and how are they evidenced?

## Revise

Done when: Scope, collaboration model and acceptance are filled; obligations passed to the supplier are explicit. Every packet of this run has its `challengeLedger` entry.

## Human gate

The human owner of the supplier relationship decides whether to proceed on these terms. Next: `supplier-agreement-transition` to record it (draft → negotiating), then `active` once the humans signed. This artifact is a working agreement, not the signed contract.
