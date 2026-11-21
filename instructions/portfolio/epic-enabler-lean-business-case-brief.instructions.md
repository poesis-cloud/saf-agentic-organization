---
description: 'Workflow brief of epic-enabler-lean-business-case: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Enabler Epic Lean Business Case (`epic-enabler-lean-business-case`)

Analyze one enabler Epic under analysis: its MVP, its cost and the value it unlocks for the Epics it enables, ending in go or no-go.

- **Main artifact:** `lean-business-case` at `portfolio/epics/<epic-slug>/<epic-slug>.lean-business-case.md` (template `templates/portfolio/lean-business-case.artifact-template.md`), owned by `enterprise-architect`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/epic-enabler-lean-business-case-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-architect`, `financial-controller`, `finops-engineer`, `security-expert`, `legal-counsel`.

## Draft

- Read the enabler Epic, the Architecture Vision, the business Epics it enables and the Lean Budgets. One case per run; set `owner: enterprise-architect`.
- Define the MVP as the smallest runway that proves or disproves the hypothesis on one enabled Epic. Estimate MVP, implementation and run costs separately.
- End with a recommendation: `go`, `no-go`, or `pending` with the missing fact. Do not change the enabler Epic: its status moves in `epic-enabler-transition`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the return stated as what the enabled Epics gain, and by when they need it?
- Are build, run and exit costs explained, and the full cost uncommitted until the MVP proves the hypothesis?

## Revise

Done when: The recommendation is `go` or `no-go`, or `pending` names the fact missing; cost and return are stated with their assumptions. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides go or no-go. Next: `epic-enabler-transition` to record it (analyzing → ready on go; → done with resolution no-go otherwise).
