---
name: participatory-budgeting
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Participatory Budgeting playbook loaded by `@value-management-officer` per Epic (when an approved `portfolio-backlog` Epic competes for the portfolio delivery capacity, or an Epic `→done` frees capacity). USE FOR: collaboratively allocating the portfolio Lean Budgets (delivery-capacity guardrails per ART / value stream) and committing which `portfolio-backlog` Epics get active capacity; setting the business-vs-enabler split. The standard third LPM event alongside Strategic Portfolio Review + Portfolio Sync. DO NOT USE FOR: re-ranking the backlog or pivots (use `strategic-portfolio-review`); the ★ Epic Gate (Central Supervisor); operational risk reconcile (use `portfolio-sync`). Loaded by `@value-management-officer` before facilitating.'
---

<!-- Copyright 2026 Poesis Cloud and contributors

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. -->

# SAFe Ceremony — Participatory Budgeting

The standard SAFe LPM event that allocates **Lean Budgets** (delivery-capacity guardrails) across ARTs / value streams and commits Epic funding. The **normative spec** is the machine-readable **[workflows/portfolio/strategic-investment-planning.workflow.conf.yaml](../workflows/portfolio/strategic-investment-planning.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@value-management-officer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[VMO orchestration core](value-management-officer.skill.md)**. Arguments come from the bench; **the Central Supervisor commits** the allocation (Business-Owner authority); the funded set honours the business/enabler guardrail split without over-committing capacity; and **only `@value-management-officer` writes `status:`**.
