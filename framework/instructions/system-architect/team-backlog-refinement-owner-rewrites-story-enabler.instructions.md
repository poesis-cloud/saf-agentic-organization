---
name: team-backlog-refinement-owner-rewrites-story-enabler
description: 'owner-rewrite precedence: only @system-architect re-synthesizes an Enabler Story from the routed challenge findings.'
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

# Team Backlog Refinement — owner rewrites Enabler Story

Only `@system-architect` re-synthesizes the Enabler Story `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story-enabler.md` after the feasibility, UX and architecture challenge packets, so it does not contradict them or the business Story. Do not edit the business Story or the reviews.

Surgical Demand: rewrite only if the Enabler Story was in-scope and challenged. If the Enabler is `status: not-needed` on this run, or was out of scope, do not invent or rewrite one: commit the Enabler file with only a new `stepOutcomes` entry (`outcome: no-change`, note why). Otherwise commit it with `outcome: revised` and a note listing the findings absorbed. The file is this step's evidence; your reply is indicative.
