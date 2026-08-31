---
name: architectural-vision
user-invocable: false
description: '**SAFe PRACTICE SKILL.** The Architectural Vision practice (Continuous Exploration) loaded by `@value-management-officer` per Epic (when a `reviewing` Epic needs its runway + NFR backbone toward `analyzing`). USE FOR: `@enterprise-architect` authoring the Architectural Vision, the NFR backbone, and the architectural-runway register; seeding **enabler Epics** for runway gaps; setting Feature seeds + target ARTs; business-owner challenges scope/value. DO NOT USE FOR: the ★ Epic Gate (Central Supervisor); ART-level ADRs (use `architectural-runway-extension`); the Epic hypothesis (use `epic-lean-business-case`). Loaded by `@value-management-officer` before facilitating; returns the runway-augmented Epic or a replay-required result when late enabler seeding invalidates prior business shaping; the VMO commits.'
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

# SAFe Practice — Architectural Vision (Continuous Exploration)

A **practice** (Continuous Exploration) that establishes the cross-product **architectural runway** + **NFR** backbone. The **normative spec** is the machine-readable **[workflows/portfolio/architectural-vision.workflow.conf.yaml](../workflows/portfolio/architectural-vision.workflow.conf.yaml)** — every step + its `conditions`, consumed by `@value-management-officer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[VMO orchestration core](value-management-officer.skill.md)**. The Vision is authored via `enterprise-architect`, and **only `@value-management-officer` writes `status:`**. On a runway gap the pass may seed enabler Epics; if that invalidates the parent Epic's shaping it returns a **replay-required** outcome that routes the Epic back through **Epic Lean Business Case**. ART ADRs belong to `architectural-runway-extension`.
