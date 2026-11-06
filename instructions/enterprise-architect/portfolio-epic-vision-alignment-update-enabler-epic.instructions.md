---
name: portfolio-epic-vision-alignment-update-enabler-epic
description: 'Owner update: the Enterprise Architect writes the Architectural Vision''s decisions on the Enabler Epic into it.'
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

# Epic–Vision Alignment — update Enabler Epic

The Enterprise Architect writes into the Enabler Epic what the committed Architectural Vision decided about it. The Vision decides; the Enabler Epic must carry the decision, or the ★ Epic Gate sees a unit that contradicts its governing Vision. This workflow runs once per Epic, after `architectural-vision`; the dispatch names the Epic.

Inputs: the Architectural Vision `portfolio/products/<product-slug>/architecture-vision.md` (its `closedItems` and `## Decisions on Epics`), the Enabler Epic `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic-enabler.md`, and the business Epic.
Output: the epic-enabler artifact only. Do not edit the Vision, the business Epic or the Lean Business Case.

Write, at least:

- **Closed open items.** For every `closedItems` entry with `artifact: epic-enabler` and `unit:` this Enabler Epic's `id`, set that `openItems` entry to `status: resolved` and record the Vision's `resolution` on it. Never delete the entry. If the Vision closes an item this Enabler Epic does not carry, record that contradiction as a new open item; never invent an entry just to close it. `epic-transition` accepts only a `no-change` refusal on this Enabler Epic, and on its business Epic, while an item the Vision closes is still `open` here.
- **A no-enabler decision the Vision overturns.** If this Enabler Epic is `status: not-needed` and the Vision now requires runway from it (Feature seeds, an enabler, a runway dependency), the no-enabler decision is invalid. Record a blocking open item naming the runway the Vision requires and that `epic-lean-business-case` must run again (its `draft-enabler-epic` step decides the enabler) before the ★ Epic Gate is staged, and commit with `outcome: revised`. Do not write `status:` (that is `epic-transition`), and do not add the seeds or WSJF to a `not-needed` Enabler Epic. If it stays not needed, `no-change`.
- **MVP Feature seeds.** The Feature seeds the Vision places on this Enabler Epic go into `## Affected products & Feature seeds` (each with its target ART), and the MVP ones into `mvpFeatures` and `## MVP & pivot/persevere`.
- **WSJF.** When the Vision's runway changes the size of the work (the seeded Features), update `wsjf.jobSize` and recompute `wsjf.score` = (userBusinessValue + timeCriticality + riskReduction) / jobSize. Change the other WSJF inputs only when the Vision states a reason.
- **Runway and dependencies.** `## Enterprise-Architect runway (EA hat)`, `## Dependencies / constraints` and `workItemRelations` against the Vision's runway direction; add the Vision to `sources`.

If the Vision decides nothing about this Enabler Epic, or it already matches, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed (the items closed, the seeds added, the WSJF change). The file is this step's evidence; your reply is indicative.
