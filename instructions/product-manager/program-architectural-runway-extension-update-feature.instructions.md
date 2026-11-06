---
name: program-architectural-runway-extension-update-feature
description: 'Owner update: the Product Manager writes the committed architecture packet''s decisions on the business Feature into it.'
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

# Architectural Runway Extension — update business Feature

The Product Manager writes into the business Feature what the architecture packet this run committed (the NFR list, the ADR and the runway register that `owner-rewrite` just committed) decided about it. The ★ Architecture Gate reads the Feature: it must link the packet and carry its open gate entries, or the gate sees a Feature that contradicts its architecture.

Inputs: the business Feature `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md`, the runway register `portfolio/products/<product-slug>/architecture-runway.md`, this run's ADR in the Feature folder, the product NFR list `portfolio/products/<product-slug>/nfr-list.md`, and the security, operability and feasibility reviews of this run.
Output: the feature artifact only. Do not edit the ADR, the NFR list, the runway register, the Enabler Feature or the reviews.

Write, at least:

- `adrs`: the ids of the ADRs that now cover this Feature, this run's included; `architectureInventory` and `## Architecture decision inventory`: the decision inventory the runway register commits for this Feature: each row names the ADR or the explicit waiver that covers it, or stays explicitly uncovered when the packet leaves that decision for a later pass (an incremental pass decides only the units that are ready). Full coverage is what the ★ Architecture Gate requires, not this step: an uncovered row keeps the Feature `arch-pending` and gets a blocking `openItems` entry (below).
- `## NFR applicability / trace`: the product NFRs the packet makes applicable to this Feature.
- `openItems`: an entry for every Architecture Gate decision the packet leaves open, and an Enabler Feature seed it records (blocking, so the gate sees it). Set an entry the packet resolves to `status: resolved`; never delete one.

Do not reshape the Description, the acceptance criteria or WSJF here: that is `feature-backlog-refinement`. Do not write `status:`: that is `feature-transition`.

If the packet decides nothing about this business Feature (for example it serves the Enabler Feature only), or the Feature already matches, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
