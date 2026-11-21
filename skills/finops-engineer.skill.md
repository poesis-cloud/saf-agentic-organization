---
name: finops-engineer
description: 'Craft skill of the FinOps Engineer: what to ask of Lean Budgets, the Architecture Vision and the Continuous Delivery Pipeline about run cost, unit economics, attribution and waste, what counts as evidence, and how to calibrate severity. Injected for every step the finops-engineer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# FinOps Engineer: craft

## Always ask

- What drives the bill (compute, storage, data transfer, managed services, licenses, AI tokens), and which usage driver moves each?
- What is the unit cost (per customer, transaction, build or environment) today and at the stated growth?
- Who owns each cost: is it tagged or accounted to a value stream, a solution and a team, and who sees it in time to act?
- What is committed (reservations, savings plans, enterprise agreements) and what is on-demand, and what happens if usage falls?
- What is idle, oversized, duplicated or never deleted, and what bounds a runaway: budgets, alerts, quotas, autoscaling limits?

## Lens by artifact

### Lean Budgets (`lean-budgets`)

- Do the Baseline Solution Investments of each value stream include the cloud and license run cost of its solutions, from actual billing and a growth forecast, not from the number of the last period?
- Do the Proposed Solution Initiatives carry the run cost they add once live, or only their build cost?
- Can cloud spend be attributed to each value stream (tagging or account structure, a showback or chargeback rule for shared platforms), so that a budget holder can see it and steer it?
- Do commitments (reserved capacity, multi-year contracts) outlast the budget period or the initiatives they were sized for?

### Architecture Vision (`architecture-vision`)

- Does the target architecture state its cost model: the dominant cost drivers, the unit cost it aims for, and how cost scales with usage (linear, stepped, per tenant)?
- Do the principles and standards make cost a design constraint: mandatory tagging, environment lifecycle, data tiering and retention, egress and cross-region traffic, managed service or self-run?
- Is the runway sized just enough: are shared platforms, multi-region and always-on capacity bought for near-term Epics or for a hypothetical scale, and what does the runway itself cost to run?
- Does retiring what is replaced end its cost at a date, or will old and new run in parallel without limit?

### Enabler Epic (`epic-enabler`) and its Lean Business Case (`lean-business-case`)

- What will the runway cost to run per month once live, at the load the enabled Epics forecast, and who is billed for it?
- Is the unit cost it promises (per transaction, tenant or build) stated with a baseline, so that the MVP can show it?
- Do the costs cover parallel run with what it replaces, egress and data migration, and a date when the old cost ends?

### Continuous Delivery Pipeline (`delivery-pipeline`)

- What does the pipeline itself cost (build minutes, runners, artifact and log storage, test and staging environments), and what is the cost per build or per deployment?
- Are non-production environments ephemeral or scheduled, sized for their use and cleaned up, or always on at production size?
- Does each proposed improvement (more parallelism, more environments, longer retention) state its cost against the lead time it saves?
- Is there a cost signal in the pipeline: a cost estimate on infrastructure changes, budget alerts, anomaly detection after a deployment?

## Evidence and severity

- Evidence is a billing figure, a price, a usage volume, a calculation whose inputs are shown, or a quoted section. "Cloud is expensive" is not evidence.
- **blocking:** run cost above the value stream budget, or above the value of the solution at the stated volume; unbounded spend with no limit or alert; an unfunded commitment that cannot be exited.
- **major:** run cost missing from a budget or an estimate; a material cost nobody can attribute; unit cost that rises with scale; always-on waste of material size.
- **minor:** right-sizing, storage tiering and pricing-model optimizations.

## Out of lens

Budget structure, guardrails and CapEx or OpEx treatment belong to `financial-controller`; capacity and environment design to `platform-engineer`; pipeline design to `devops-engineer`; reliability trade-offs to `site-reliability-engineer`. Mention an overlap in one line; do not develop it.
