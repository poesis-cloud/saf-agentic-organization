---
name: inspect-and-adapt
user-invocable: false
description: '**SAFe CEREMONY SKILL.** The Inspect & Adapt playbook loaded by `@release-train-engineer` at PI end. USE FOR: the PI quantitative metrics review + the problem-solving workshop; root-causing program-scope pain points from the ART improvement-backlog; dispatching owning actors to create derived Features/Stories/enablers. DO NOT USE FOR: the ★ Demo Gate (use `demo-gate` in the ART workflow); portfolio re-ranking (use `strategic-portfolio-review`); iteration retrospectives. Loaded by `@release-train-engineer` before facilitating.'
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

# SAFe Ceremony — Inspect & Adapt

The **program-scope** closed-loop event at the end of a PI. It has **no demo gate** (that is handled by the ART workflow). The **normative spec** is the machine-readable **[workflows/program/inspect-and-adapt.workflow.conf.yaml](../workflows/program/inspect-and-adapt.workflow.conf.yaml)** — every step + its `conditions` (metrics review → retrospective), consumed by `@release-train-engineer` and the harness (`check-step` / `check-artifact`). Load and follow it; do not restate it here.

Shared model lives in **[RTE orchestration core](release-train-engineer.skill.md)**.

## Step instructions

- **Step 1 — Metrics review**: [instructions/metrics-review.instructions.md](instructions/metrics-review.instructions.md)
- **Step 2 — Retrospective**: [instructions/retrospective.instructions.md](instructions/retrospective.instructions.md)

**Only `@release-train-engineer` facilitates I&A and updates pain-point `status`. Derived Features, Stories, and enablers are authored by their owning actors.**
