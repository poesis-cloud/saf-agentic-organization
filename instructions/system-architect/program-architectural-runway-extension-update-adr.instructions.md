---
name: program-architectural-runway-extension-update-adr
description: 'Owner update: the System Architect absorbs the challenge findings into the ADR this run authored.'
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

# Architectural Runway Extension — update ADR

Only `@system-architect` updates the ADR that this run's `author-adr` step committed (`portfolio/art/<art-slug>/program-backlog/<feature-slug>/<adr-slug>.adr.md`) after the security, operability and feasibility challenge packets, and against the NFR list as updated. One decision stays one ADR: do not split it or author another one here. Do not edit the NFR list, the runway register or the reviews.

Absorb the findings into the options evaluation, the decision, its consequences and its NFR trace. If the document already matches, or is out of scope on this run, commit it with only a new `stepOutcomes` entry (`outcome: no-change`, note naming what you checked). Otherwise commit it with `outcome: revised` and a note listing what changed. The file is this step's evidence; your reply is indicative.
