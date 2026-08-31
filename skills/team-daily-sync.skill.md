---
name: daily-sync
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Daily Sync playbook loaded by `@scrum-master` per Story (after each Story transition). USE FOR: walking the Team Kanban; surfacing + removing blockers (Story `blocked`/unblock); coaching the Driver/Navigator pair; enforcing WIP limits; writing `daily-DD.md` + updating `progress.md`. DO NOT USE FOR: status changes across a ★ gate; authoring artifacts; the retro (use `retrospective`). Loaded by `@scrum-master` before facilitating.'
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

# SAFe Ceremony — Daily Sync

A **reconcile** ceremony (no authoring, no gate). The **normative spec** is the machine-readable **[workflows/team/team-sync.workflow.conf.yaml](../workflows/team/team-sync.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@scrum-master` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[scrum-master orchestration core](scrum-master.skill.md)**. The facilitator walks WIP + blockers, enforces the WIP limits (`in-progress` = 1/pair, `in-qa` ≤ 2), and flips `→blocked`/unblock only — no flow edge, no authoring, no gate; **only `@scrum-master` writes `status:`**.
Every pair synced + blockers actioned + WIP within limits + sprint artifacts written.
