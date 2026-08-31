---
name: program-feature-backlog-refinement-author-enabler-feature
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

# Feature Backlog Refinement — author Enabler Feature

The System Architect authors or thickens the Enabler Feature that unblocks the business Feature.

Inputs: the business Feature (just drafted or already existing), Architectural Vision, Architectural Runway, the product NFR register `products/<product-slug>/nfr-list.md`, and the parent Enabler Epic (if any).
Output: the feature-enabler artifact. Name the consuming Feature, the unblocked capability, the validation evidence, and **NFR applicability / trace**.

Fill `## NFR applicability / trace` from the product register. Do not add or rewrite canonical NFRs. A missing NFR is a runway concern, not Enabler AC.

Do not rewrite the business Feature. Do not author ADR, NFR list, or runway — those belong to `architectural-runway-extension`.

Surgical Demand: write or thicken the Enabler only when it is in-scope. If the Demand does not require an Enabler, emit explicit-none (no Enabler needed) rather than inventing one.
