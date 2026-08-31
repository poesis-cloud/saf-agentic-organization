---
name: program-architectural-runway-extension-author-nfrs
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

# Architectural Runway Extension — author NFR list

The System Architect records or thickens the **product** Nonfunctional Requirements register
(`products/<product-slug>/nfr-list.md`) **before** any ADR is written. NFRs are enduring product
constraints and a precondition for ADR production. This step does not write a Feature-folder list.

Inputs: Architectural Vision NFR backbone, existing product `nfr-list` (if any), current Architecture
Runway, the Feature / Enabler Feature that exposed the gap (already shaped in Feature Backlog
Refinement).
Output: the product `nfr-list` artifact. Security, operability, and feasibility challengers read
this list; they do not rewrite it.

If the concern is a new or changed product NFR, write or thicken this register; do not mint a new
Feature and do not skip ahead to an ADR. If no NFR change is required, emit explicit-none (no NFR
change) rather than inventing a list. Feature and Story files only trace which NFRs apply.
