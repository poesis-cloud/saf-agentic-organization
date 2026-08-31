---
name: strategic-portfolio-review
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Strategic Portfolio Review playbook loaded by `@value-management-officer` per unit (on an Epic enter/exit). USE FOR: re-ranking the portfolio backlog by WSJF; revising Strategic Themes; pivot/persevere/stop recommendations on in-flight Epics; triaging portfolio-scope pain points from the workflow-improvement ledger. DO NOT USE FOR: deciding the ★ Epic Gate or accepting outcomes (Central Supervisor); shaping an individual Epic (use `business-owner`); program ceremonies (use `inspect-and-adapt`). Loaded by `@value-management-officer` before facilitating.'
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

# SAFe Ceremony — Strategic Portfolio Review

The **normative spec** is the machine-readable **[workflows/portfolio/strategic-portfolio-review.workflow.conf.yaml](../workflows/portfolio/strategic-portfolio-review.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@value-management-officer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[VMO orchestration core](value-management-officer.skill.md)**. The WSJF re-rank + Strategic-Theme revisions are authored via `business-owner`; **the Central Supervisor decides** pivot/persevere/stop and **only `@value-management-officer` writes `status:`**. A workflow-improvement is a meta-artifact change, never a product Epic.
