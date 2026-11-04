---
name: program-improvement-backlog-record-pain-point
description: 'Improvement Backlog — create or update exactly one ART pain point from one friction note. One pain point per run, never a batch.'
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

# Improvement Backlog — record one pain point

The Release Train Engineer records **exactly one** pain point per run in
`art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`.

## Input

One friction note, named in the dispatch:

- the `friction` note of a step's `stepOutcomes` entry (any artifact, any actor);
- one row of the PI's Inspect & Adapt record (`art/<art-slug>/pi-<pi-slug>/inspect-and-adapt.md`):
  a **Pain-point candidate** or a **Triage** decision;
- a program-scope escalation in a team's Iteration Retrospective;
- friction the Central Supervisor reports.

## Procedure

1. Look for an open pain point with the same systemic cause.
2. **Same cause found** — update that pain point only: add the new evidence, or apply the
   Triage row (`rootCause`, `resolution`, `targetArtifact`, derived-item placeholders,
   `status`). Append a `stepOutcomes` entry (`outcome: revised`).
3. **No match** — create one pain point (`status: open`, `origin` from the source: `workflow`
   for a step's friction note, `metrics-review` for a metrics candidate, `iteration` for a
   team escalation, `pi` or `cross-product` otherwise). Append a `stepOutcomes` entry
   (`outcome: written`).
4. **Nothing to record** (the note is already fully captured) — still commit the matching
   pain point with a `stepOutcomes` entry (`outcome: no-change`, the note says why).

Never touch a second pain point in the same run: a second note is a second
`improvement-backlog` run. Never author a derived Feature, Story or meta-artifact change:
those are later Demands for their owners.
