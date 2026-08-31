---
name: system-demo
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The System Demo playbook loaded by `@release-train-engineer` at PI increment review. USE FOR: staging the ART increment for the ★ Demo Gate; measuring Feature cost once; capturing stakeholder feedback at program scope. DO NOT USE FOR: iteration increment review (use `iteration-review`); Inspect & Adapt (use `inspect-and-adapt`); authoring Features. Loaded by `@release-train-engineer` before facilitating.'
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

# SAFe Ceremony — System Demo

A **program / ART increment review**. The **normative spec** is the machine-readable **[workflows/program/system-demo.workflow.conf.yaml](../workflows/program/system-demo.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@release-train-engineer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[RTE orchestration core](release-train-engineer.skill.md)**. The facilitator stages the Demo Gate packet only — it authors no Feature content and flips no ★ gate; **only the Central Supervisor decides**.
ART increment demoed + Demo Gate packet staged + Feature cost written once.
