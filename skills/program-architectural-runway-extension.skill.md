---
name: architectural-runway-extension
user-invocable: false
description: '**SAFe PRACTICE SKILL.** Architectural Runway Extension loaded by `@release-train-engineer`. Normative spec is workflows/program/architectural-runway-extension.workflow.conf.yaml. USE FOR: NFR list then ADR then Architecture Runway, with security/operability/feasibility challenges. DO NOT USE FOR: Feature AC/WSJF (use feature-backlog-refinement); portfolio NFR backbone (use architectural-vision); the ★ Architecture Gate decision (Central Supervisor).'
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

# SAFe Practice — Architectural Runway Extension (intentional architecture)

A **practice** (Continuous Exploration / intentional architecture) that extends the **architectural runway** for a structurant Feature. The **normative spec** is the machine-readable **[workflows/program/architectural-runway-extension.workflow.conf.yaml](../workflows/program/architectural-runway-extension.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@release-train-engineer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

**NFR list is a precondition for ADR production.** Shared model lives in **[RTE orchestration core](release-train-engineer.skill.md)**. ADRs are authored via `system-architect` (one ADR per decision unit); **only `@release-train-engineer` writes `status:`** and **stages the ★ Architecture Gate** only when the packet is complete (it never decides). A late-seeded enabler Feature forces the parent Feature to replay **Feature Backlog Refinement** before the gate is restaged.
