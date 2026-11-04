---
name: program-architectural-runway-extension-rewrite-architecture-runway
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

# Architectural Runway Extension — rewrite Architecture Runway

Only `@system-architect` re-synthesizes Architecture Runway after the security, operability, and feasibility challenge packets.

Absorb challenge findings into the runway register (`portfolio/products/<product-slug>/architecture-runway.md`). Record the NFR and ADR updates the `update-nfrs` and `update-adr` steps committed, or an explicit waiver. Do not rewrite the business Feature. If a late-seeded Enabler Feature is required, record it in the runway register (and the `stepOutcomes` note) and return replay-required so Feature Backlog Refinement runs before the Architecture Gate is restaged. Always commit the register; when no finding changes it, append a `stepOutcomes` entry (`outcome: no-change`).
