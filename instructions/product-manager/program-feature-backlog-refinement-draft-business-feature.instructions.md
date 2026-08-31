---
name: program-feature-backlog-refinement-draft-business-feature
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

# Feature Backlog Refinement — draft business Feature

The Product Manager drafts or thickens the business Feature so the ART can construct it together.

Inputs: the parent Epic / Lean Business Case / Enabler Epic (if any), Strategic Themes, Product Vision / Roadmap, and the product NFR register `products/<product-slug>/nfr-list.md`.
Output: the Feature artifact (benefit hypothesis, AC, WSJF, sizing, **NFR applicability / trace**).

Fill `## NFR applicability / trace` from the product register: which NFRs apply, plus any Feature-specific tightening. Do not add, rewrite, or omit the canonical NFR set. If a needed NFR is missing from the register, record that as an open item and refuse-to-runway (`architectural-runway-extension`); do not invent an NFR here.

Surgical Demand: if this run's in-scope mains include the Feature, write or thicken it. If the Demand is only an Enabler Feature sibling on an **existing** Feature, do not invent a new Feature and do not redraft the existing one — emit an explicit no-change note naming the existing Feature. Do not write the Enabler Feature. Do not author ADR, NFR list, or runway — those belong to `architectural-runway-extension`.
