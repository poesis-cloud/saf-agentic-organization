---
name: portfolio-epic-transition-transition-epic
description: 'Epic Transition — Business Owner records one requested Epic status change, or no-change, on the business Epic.'
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

# Epic Transition — transition business Epic

The Business Owner records **one** Epic status transition, requested by the orchestrator, on the business Epic it authors. This is the only way a Epic `status:` changes outside the workflow step that authors the Epic: orchestrators never write it.

Inputs: the transition request named in the dispatch — the Epic slug, the expected current `status:`, the target `status:`, and its trigger (a human gate decision quoted verbatim, a roll-up event, a block or unblock with its impediment, or the close).
Output: the business Epic artifact, with exactly one new `stepOutcomes` entry (`step: epic-transition/transition-epic`).

- If the request concerns this business Epic: check that its current `status:` is the expected source and that the trigger is evidenced (a gate decision quoted from the Central Supervisor, the child states for a roll-up). If so, write the target `status:`, and, when the target is `done`, the `cost:` block once from the ecosystem logs (Epic overhead plus the sum of child Feature `tokensRolled`, `source: measured`, or `estimated` only if the logs are gone) and record `outcome: revised` with the trigger in `note`. If not, leave `status:` unchanged and record `outcome: no-change` with the reason in `note`.
- **Consistency before advancing.** Before you record a forward move (`funnel→reviewing→analyzing→portfolio-backlog→implementing→done`, or an unblock), check this Epic against its governing artifacts: the Lean Business Case, the Architectural Vision (every item its `closedItems` lists for this Epic is `resolved` here; its `## Decisions on Epics` seeds, MVP and size are written here) and the sibling Enabler Epic; for `→portfolio-backlog`, no blocking `open` item. If they disagree, do not advance: leave `status:` unchanged and record `outcome: no-change` with the reason in `note`, naming the governing artifact, the field that disagrees and the workflow that resolves it (`epic-vision-alignment` for the Vision's decisions, `epic-lean-business-case` for the case), so the orchestrator reports it to the user instead of the transition. Moving a unit back (a gate rejection, `→blocked`) is always recorded. The harness refuses to start `epic-transition` at all (move back included) while an item the Architectural Vision closes is still `open` on any Epic or Enabler Epic: that write-back, `epic-vision-alignment` for that Epic, comes first.
- If the request concerns only the sibling Enabler Epic, leave the content unchanged and record `outcome: no-change` ("transition applies to the sibling Enabler Epic").
- Change nothing else: content changes belong to the authoring workflows, and a gate rejection reiterates that workflow.
- Record workflow friction in the `friction` note of your step entry, never as a pain point.
