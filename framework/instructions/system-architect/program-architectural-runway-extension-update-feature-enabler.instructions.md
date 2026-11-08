---
name: program-architectural-runway-extension-update-feature-enabler
description: 'Owner update: the System Architect writes the committed architecture packet''s decisions on the Enabler Feature into it.'
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

# Architectural Runway Extension — update Enabler Feature

The System Architect writes into the Enabler Feature what the architecture packet this run committed (the NFR list, the ADR and the runway register) decided about it, after the Product Manager updated the business Feature. The ★ Architecture Gate reads the Feature: it must link the packet and carry its open gate entries.

Inputs: the Enabler Feature `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature-enabler.md`, the runway register, this run's ADR, the product NFR list, the business Feature just updated, and the reviews of this run.
Output: the feature-enabler artifact only. Do not edit the ADR, the NFR list, the runway register, the business Feature or the reviews.

Write, at least: `adrs`, `architectureInventory` and `## Architecture decision inventory` for the decisions that cover this Enabler Feature; `## NFR applicability / trace`; and `openItems` entries for the Architecture Gate decisions the packet leaves open (resolve the ones it closes; never delete one). An Enabler Feature with `status: not-needed` that the packet now needs records that as a blocking open item and a `revised` outcome, so Feature Backlog Refinement replays before the gate; if it stays not needed, `no-change`. Do not write `status:`: that is `feature-transition`.

If the packet decides nothing about this Enabler Feature, or it already matches, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
