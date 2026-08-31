---
name: art-sync
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The ART Sync playbook (Coach Sync + PO Sync) loaded by `@release-train-engineer` per Feature (after a Feature transition or a `blocked`). USE FOR: cross-team dependency + Feature-progress reconcile during a PI; architecture-runway check while ADRs are in flight; updating program risk; removing program impediments (Feature `blocked`/unblock). DO NOT USE FOR: committing the PI (use `pi-planning`); the ★ Architecture/Demo gates (Central Supervisor); portfolio risk (use `portfolio-sync`). Loaded by `@release-train-engineer` before facilitating.'
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

# SAFe Ceremony — ART Sync (Coach + PO Sync)

A **reconcile** ceremony in the program / ART layer. The **normative spec** is the machine-readable **[workflows/program/art-sync.workflow.conf.yaml](../workflows/program/art-sync.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@release-train-engineer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[RTE orchestration core](release-train-engineer.skill.md)**. The facilitator reconciles cross-team Feature progress + dependencies, delegates runway questions to `@system-architect`, updates ROAM risk, and flips `→blocked`/unblock only — it authors no Feature/ADR and flips no ★ gate; **only `@release-train-engineer` writes `status:`**.
Features reconciled to objectives + runway ahead of need + risks current + board refreshed.
