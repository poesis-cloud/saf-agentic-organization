---
name: program-feature-transition-transition-enabler
description: 'Feature Transition — System Architect records one requested status change, or no-change, on the sibling Enabler Feature.'
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

# Feature Transition — transition Enabler Feature

The System Architect records **one** Feature status transition, requested by the orchestrator, on the Enabler Feature it authors. This is the only way a Feature `status:` changes outside the workflow step that authors the Feature: orchestrators never write it.

Inputs: the transition request named in the dispatch — the Feature slug, the expected current `status:`, the target `status:`, and its trigger (a human gate decision quoted verbatim, a roll-up event, a block or unblock with its impediment, or the close).
Output: the Enabler Feature artifact, with exactly one new `stepOutcomes` entry (`step: feature-transition/transition-enabler`).

- If the request concerns this Enabler Feature: check that its current `status:` is the expected source and that the trigger is evidenced (a gate decision quoted from the Central Supervisor, the child states for a roll-up). If so, write the target `status:` and record `outcome: revised` with the trigger in `note`. If not, leave `status:` unchanged and record `outcome: no-change` with the reason in `note`.
- If the request concerns only the business Feature, leave the content unchanged and record `outcome: no-change` ("transition applies to the business Feature").
- A sibling Enabler Feature with `status: not-needed` keeps it: record `outcome: no-change` ("no enabler required").
- Change nothing else: content changes belong to the authoring workflows, and a gate rejection reiterates that workflow.
- Record workflow friction in the `friction` note of your step entry, never as a pain point.
