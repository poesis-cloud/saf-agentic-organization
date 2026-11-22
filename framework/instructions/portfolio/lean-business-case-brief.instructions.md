---
description: 'Workflow brief of lean-business-case: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Lean Business Case (`lean-business-case`)

Analyze one Epic in the analyzing state: define its MVP, estimate its cost and projected value, and recommend go or no-go.

- **Main artifact:** `lean-business-case` at `portfolio/epics/<epic-slug>/<epic-slug>.lean-business-case.md` (template `templates/portfolio/lean-business-case.artifact-template.md`), owned by `epic-owner`.
- **Challenge packets:** `portfolio/epics/<epic-slug>/challenges/lean-business-case-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `enterprise-architect`, `financial-controller`, `security-expert`, `data-protection-officer`, `legal-counsel`.

## Draft

- Read the Epic and, when they exist, the Architecture Vision and Lean Budgets. One Lean Business Case per run, for the Epic the human names.
- Define the MVP as the smallest solution that can prove or disprove the hypothesis. Estimate the MVP cost and the forecast implementation cost separately.
- End with a recommendation: `go`, `no-go`, or `pending` with the missing fact. Do not change the Epic: its status moves in `epic-transition`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Would the MVP, as defined, actually settle the hypothesis?
- Are the cost estimates explained, and is the full cost left uncommitted until the MVP proves the hypothesis?

## Revise

Done when: The recommendation is `go` or `no-go`, or `pending` names the fact missing; cost and return are stated with their assumptions. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides go or no-go. Next: `epic-transition` to record it (analyzing → ready on go; → done with resolution no-go otherwise).
