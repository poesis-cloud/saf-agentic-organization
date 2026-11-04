---
name: program-architectural-runway-extension-update-nfrs
description: 'Owner update: the System Architect absorbs the challenge findings into the product NFR list.'
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

# Architectural Runway Extension — update NFR list

Only `@system-architect` updates the product NFR list `portfolio/products/<product-slug>/nfr-list.md` after the security, operability and feasibility challenge packets, so it does not contradict them or the ADR. Do not edit the ADR, the runway register or the reviews.

Absorb every finding that adds, tightens, relaxes or waives an NFR, with its trace to the review. If the document already matches, or is out of scope on this run, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
