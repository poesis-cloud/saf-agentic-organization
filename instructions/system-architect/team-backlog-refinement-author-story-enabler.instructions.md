---
name: team-backlog-refinement-author-story-enabler
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

# Team Backlog Refinement — author Enabler Story

The System Architect authors the Enabler Story that unblocks the business Story.

Inputs: the Story (just drafted or already existing), the parent Feature / Enabler Feature, ADRs, and `products/<product-slug>/nfr-list.md`.
Output: the story-enabler artifact, including `## NFR applicability / trace` inherited from the parent Feature. Do not rewrite the business Story. Do not author the product NFR register.

Surgical Demand: write or thicken the Enabler Story only when it is in-scope. If the Demand does not require an Enabler, emit explicit-none rather than inventing one.
