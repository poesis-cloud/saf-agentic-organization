---
name: iteration-review
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Iteration Review playbook loaded by `@scrum-master` per Story (on `awaiting-pr`/`done`). USE FOR: demoing the iteration increment to the Central Supervisor + stakeholders; capturing feedback into new/changed backlog items. DO NOT USE FOR: the ★ PR / Feature gates (Central Supervisor / `demo-gate`); the retro (use `retrospective`); authoring Stories (use `product-owner`). Loaded by `@scrum-master` before facilitating.'
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

# SAFe Ceremony — Iteration Review

A stage-and-capture review (**not a gate** — the ★ Demo Gate is the **Demo Gate**). The **normative spec** is the machine-readable **[workflows/team/iteration-review.workflow.conf.yaml](../workflows/team/iteration-review.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@scrum-master` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[scrum-master orchestration core](scrum-master.skill.md)**. The facilitator stages + captures only: stakeholders + the Central Supervisor give feedback, which routes to new/changed backlog items (Stories via the PO; scope up to `@release-train-engineer`); it flips no ★ gate.
Increment demoed + feedback captured + routed to the right backlog.
