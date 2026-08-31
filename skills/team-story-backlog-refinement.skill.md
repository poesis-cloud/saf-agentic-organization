---
name: story-backlog-refinement
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Story Backlog Refinement playbook loaded by `@scrum-master` per Story (when a `backlog` Story is not DoR-ready, including replay after a late enabler invalidates prior grooming). USE FOR: grooming upcoming Stories toward the Definition of Ready ahead of next Iteration Planning; clarifying AC; splitting oversized Stories; clearing upstream blockers. DO NOT USE FOR: running the ★ Story Gate (use `iteration-planning`); authoring Stories yourself (use `product-owner`); Feature Backlog Refinement (program layer). Loaded by `@scrum-master` before facilitating.'
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

# SAFe Ceremony — Story Backlog Refinement

The **normative spec** is the machine-readable **[workflows/team/team-backlog-refinement.workflow.conf.yaml](../workflows/team/team-backlog-refinement.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@scrum-master` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Mains are `story` and `story-enabler`. System Architect **challenges** those mains with `architecture-review`; ADR/NFR belong to program `architectural-runway-extension`.

Shared model lives in **[scrum-master orchestration core](scrum-master.skill.md)**. Business Stories are authored via `product-owner`, enabler Stories via `system-architect`; the Story stays `backlog` and **only `@scrum-master` writes `status:`** (the ★ Story Gate / DoR runs at Iteration Planning).
