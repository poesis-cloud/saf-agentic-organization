---
name: feature-backlog-refinement
user-invocable: false
description: 'SAFe ART ceremony — Feature Backlog Refinement (suborchestration of @release-train-engineer). Normative spec is workflows/program/feature-backlog-refinement.workflow.conf.yaml. USE FOR: PI-ready Feature + Enabler Feature. DO NOT USE FOR: ADR/NFR/runway (use architectural-runway-extension); Epic split (use feature-derivation).'
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

# SAFe Ceremony — Feature Backlog Refinement

The **normative spec** is the machine-readable **[workflows/program/feature-backlog-refinement.workflow.conf.yaml](../workflows/program/feature-backlog-refinement.workflow.conf.yaml)** — the step sequence and every step's `conditions`, consumed by both `@release-train-engineer` and the deterministic harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Mains are `feature` and `feature-enabler`. System Architect **challenges** those mains with `architecture-review`; ADR, NFR list, and Architecture Runway belong to `architectural-runway-extension`.

Shared model (the open-item ledger, ★ gates, the bench, invariants, artifact templates) lives in **[RTE orchestration core](release-train-engineer.skill.md)**. Authoring bodies load *inside* the steps: business Features via `product-manager`, enabler Features via `system-architect`.
