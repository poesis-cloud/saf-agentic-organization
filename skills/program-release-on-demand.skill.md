---
name: release-on-demand
user-invocable: false
description: '**SAFe PRACTICE SKILL.** The Release on Demand playbook loaded by `@release-train-engineer` when an increment is releasable. USE FOR: Continuous Deployment readiness (`@operator` operability review) and the Product Manager release decision, decoupled from PI and iteration cadences. DO NOT USE FOR: System Demo / Demo Gate (use `system-demo`); Inspect & Adapt (use `inspect-and-adapt`); authoring Features. Loaded by `@release-train-engineer` before facilitating.'
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

# SAFe Practice — Release on Demand

The ART **Continuous Delivery Pipeline** close: deployability first, then the business release decision. The **normative spec** is the machine-readable **[workflows/release-on-demand.workflow.conf.yaml](../workflows/release-on-demand.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@release-train-engineer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[RTE orchestration core](release-train-engineer.skill.md)**. `@operator` records Continuous Deployment readiness. `@product-manager` authors whether value is held, dark-launched, canaried, or released. The facilitator authors neither verdict.
