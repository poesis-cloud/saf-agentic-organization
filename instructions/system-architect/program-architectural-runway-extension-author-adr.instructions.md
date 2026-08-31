---
name: program-architectural-runway-extension-author-adr
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

# Architectural Runway Extension — author ADR

The System Architect records one architectural decision unit. The NFR list from the previous step is a precondition; do not author an ADR against an empty or unstated NFR set.

Inputs: the product nfr-list just written or confirmed (`products/<product-slug>/nfr-list.md`), the existing Feature / Enabler Feature, Architectural Vision, current Architecture Runway, existing ADRs on the Feature folder.
Output: one ADR (one decision).

If the Demand is an ADR on an existing Feature, write that ADR; do not redraft the Feature. If no new decision is required, write an explicit "no new decision" ADR note rather than inventing a review packet or a sibling Feature.
