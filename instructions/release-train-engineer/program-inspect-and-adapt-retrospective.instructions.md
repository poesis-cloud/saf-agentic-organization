---
description: 'Inspect & Adapt Step 2 — run the problem-solving workshop using the ART improvement-backlog pain points as primary input, and record the triage of each one in the PI Inspect & Adapt record.'
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

# Inspect & Adapt — Step 2: Retrospective

Run the PI problem-solving workshop. This step updates **exactly one** artifact, the PI's
Inspect & Adapt record (`art/<art-slug>/pi-<pi-slug>/inspect-and-adapt.md`). It writes no
pain point and authors no derived Feature, Story or enabler.

## Inputs

- All `art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`
  artifacts with `status: open` (read only).
- The record's **Metrics** and **Pain-point candidates** from Step 1.

## Procedure

1. **Metrics interpretation** — call out the top 2–3 indicators that deviated most from plan
   and hypothesize systemic causes.
2. **Pain-point root-cause analysis** — for each open pain point and each candidate:
   - Cluster related pain points.
   - Apply five-whys / fishbone analysis.
   - Decide resolution: `workflow-improvement`, `product-improvement`, `accepted`, or
     `duplicate`.
3. **Triage** — one **Triage** row per pain point: root cause, resolution, target artifact,
   and the status to set (`converted`, `resolved`, `accepted`, or `duplicate`).
   - `workflow-improvement` → target meta-artifact (`layers/...`, `instructions/...`,
     `conf/...`) and owning actor.
   - `product-improvement` → derived item type (`feature`, `story`, `feature-enabler`,
     `story-enabler`), owning actor (`@product-manager` for Features, `@product-owner` for
     Stories, `@system-architect` for enablers), proposed title and rationale.
4. **PI+1 priming** — list carry-over Features (committed but not done) and top candidates
   for the next PI funnel. This list is indicative input to the next PI Planning and decides
   nothing: carry-over is already evidenced by the Features' `status` and the PI objectives,
   and a new candidate enters only as a derived item or a later Demand.

## Output

Update the record: the **Triage** table, **PI+1 priming**, `status: triaged`, and a
`stepOutcomes` entry (`outcome: revised`). Each Triage row is applied to its pain point by one
later `improvement-backlog` run; each derived item is a later Demand for its owner.

**Only `@release-train-engineer` writes pain points, one per `improvement-backlog` run.**
