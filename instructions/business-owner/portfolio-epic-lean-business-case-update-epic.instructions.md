---
name: portfolio-epic-lean-business-case-update-epic
description: 'Owner update: the Business Owner aligns the Epic with the Lean Business Case after the feasibility challenge.'
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

# Epic Lean Business Case — update Epic

The Business Owner aligns the business Epic with the Lean Business Case that `owner-rewrite` just committed. The challenge and the rewrite can change the bet; the Epic must not contradict it.

Inputs: the Epic `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md`, the rewritten Lean Business Case `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.lean-business-case.md`, the Enabler Epic, and the feasibility review `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.feasibility-review.md`.
Output: the epic artifact only. Do not edit the Lean Business Case, the Enabler Epic or the review.

Check and align, at least: `## In scope / out of scope` against the LBC's solution hypothesis; `dependsOn` and `## Dependencies / constraints` against the LBC's enabler / runway dependency (including a dependency on the Enabler Epic); `mvpFeatures` and `## MVP & pivot/persevere` (the first-release scope) against the LBC's MVP and pivot / persevere / stop criteria; WSJF and leading indicators against the LBC's figures.

If the document already matches, or is out of scope on this run, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
