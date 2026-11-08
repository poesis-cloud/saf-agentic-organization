---
name: portfolio-epic-vision-alignment-reconcile-lean-business-case
description: 'Owner update: the Business Owner reconciles the Lean Business Case with the Epic the Vision just changed.'
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

# Epic–Vision Alignment — reconcile Lean Business Case

The Business Owner reconciles the Lean Business Case with the business Epic that `update-epic` just committed. The Vision can change the Epic's first-release scope, size and runway dependency; the case must then say the same, or the Epic and its case contradict each other, `epic-transition` refuses the next forward move, and a later `epic-lean-business-case` run would restore the stale values.

Inputs: the Lean Business Case `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.lean-business-case.md`, the business Epic just updated, the Enabler Epic, and the Architectural Vision.
Output: the lean-business-case artifact only. Do not edit the Epic, the Enabler Epic or the Vision.

Align the case with the Epic, field by field: `wsjf` (and `## WSJF`) with the Epic's WSJF; `## Solution hypothesis (MVP)` with the Epic's `mvpFeatures` and `## MVP & pivot/persevere`; `## Enabler / runway dependency` and `## Cost / effort estimate` with the Enabler Epic's runway and size; `workItemRelations` with the Epic's. The Epic, as the Vision left it, takes precedence for these fields. Record what changed and why under `## Challenge findings` (source: the Architectural Vision). Never rewrite `## Problem & opportunity` or the hypothesis: if the Epic now carries a blocking item for an `epic-lean-business-case` replay, carry it as an `openItems` entry here too and leave the hypothesis to that replay.

If the case already matches the Epic, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
