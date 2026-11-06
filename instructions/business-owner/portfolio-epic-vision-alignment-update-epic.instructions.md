---
name: portfolio-epic-vision-alignment-update-epic
description: 'Owner update: the Business Owner writes the Architectural Vision''s decisions on the business Epic into it.'
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

# Epic–Vision Alignment — update Epic

The Business Owner writes into the business Epic what the committed Architectural Vision decided about it, after the Enterprise Architect updated the Enabler Epic. The Vision decides; the Epic must carry the decision, or the ★ Epic Gate sees a unit that contradicts its governing Vision. This workflow runs once per Epic, after `architectural-vision`; the dispatch names the Epic.

Inputs: the Architectural Vision `portfolio/products/<product-slug>/architecture-vision.md` (its `closedItems` and `## Decisions on Epics`), the business Epic `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md`, the Enabler Epic just updated, and the Lean Business Case.
Output: the epic artifact only. Do not edit the Vision, the Enabler Epic or the Lean Business Case: the next step reconciles the case with this Epic.

Write, at least:

- **Closed open items.** For every `closedItems` entry with `artifact: epic` and `unit:` this Epic's `id`, set that `openItems` entry to `status: resolved` and record the Vision's `resolution` on it. Never delete the entry. If the Vision closes an item this Epic does not carry, record that contradiction as a new open item; never invent an entry just to close it. `epic-transition` refuses to dispatch while an item the Vision closes is still `open` here.
- **Dependencies and scope.** `dependsOn` and `## Dependencies / constraints` on the Enabler Epic's runway as now written, and `## Enterprise-Architect runway (EA hat)` and `## Affected products & Feature seeds` against the Vision's decisions on this Epic. If the Enabler Epic now carries a blocking item for an `epic-lean-business-case` replay, record the same dependency here.
- **MVP and WSJF.** `mvpFeatures` and `## MVP & pivot/persevere` when the Vision changes the first-release scope; `wsjf.jobSize` and `wsjf.score` when it changes the size of the work. Change the value inputs only when the Vision states a reason.

If the change invalidates the Epic hypothesis itself (not just its runway, scope or size), do not rewrite the hypothesis here: record a blocking open item so the ★ Epic Gate sees it and `epic-lean-business-case` runs again.

If the Vision decides nothing about this Epic, or it already matches, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
