---
name: team-story-transition-transition-enabler
description: 'Story Transition — System Architect records one requested status change, or no-change, on the sibling Enabler Story.'
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

# Story Transition — transition Enabler Story

The System Architect records **one** Story status transition, requested by the orchestrator, on the Enabler Story it authors. This is the only way a Story `status:` changes outside the workflow step that authors the Story: orchestrators never write it.

Inputs: the transition request named in the dispatch — the Story slug, the expected current `status:`, the target `status:`, and its trigger (a human gate decision quoted verbatim, a roll-up event, a block or unblock with its impediment, or the close).
Output: the Enabler Story artifact, with exactly one new `stepOutcomes` entry (`step: story-transition/transition-enabler`).

- If the request concerns this Enabler Story: check that its current `status:` is the expected source and that the trigger is evidenced (a gate decision quoted from the Central Supervisor, the child states for a roll-up). If so, write the target `status:` and record `outcome: revised` with the trigger in `note`. If not, leave `status:` unchanged and record `outcome: no-change` with the reason in `note`.
- **Consistency before advancing.** Before you record a forward move (`backlog→ready→in-progress→in-review→in-qa→awaiting-pr→done`, or an unblock), check this Enabler Story against its governing artifacts: its parent Feature (`committed` or later before work starts), its latest refinement packet (Definition of Ready for `→ready`), and for `→awaiting-pr` its QA sign-off. If they disagree, do not advance: leave `status:` unchanged and record `outcome: no-change` with the reason in `note`, naming the governing artifact, the field that disagrees and the workflow that resolves it (`team-backlog-refinement`, `verification`), so the orchestrator reports it to the user instead of the transition. Moving a unit back (a gate rejection, `→blocked`) is always recorded.
- If the request concerns only the business Story, leave the content unchanged and record `outcome: no-change` ("transition applies to the business Story").
- A sibling Enabler Story with `status: not-needed` keeps it: record `outcome: no-change` ("no enabler required").
- Change nothing else: content changes belong to the authoring workflows, and a gate rejection reiterates that workflow.
- Record workflow friction in the `friction` note of your step entry, never as a pain point.
