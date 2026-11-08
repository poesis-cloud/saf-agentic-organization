---
description: 'Inspect & Adapt Step 1 — calculate PI metrics by reading existing artifact content and create the PI Inspect & Adapt record with them. No dedicated metric fields are required on source artifacts.'
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

# Inspect & Adapt — Step 1: Metrics Review

Calculate the following PI indicators by reading the existing artifact content. Do not require or add dedicated metric fields to source artifacts.

## Indicators and calculation rules

| Indicator | How to calculate | Source artifacts |
|---|---|---|
| Features committed → done | Count `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md` files whose `id` is listed in `portfolio/art/<art-slug>/pi-<pi-slug>/objectives.md` committed Features and whose `status` is `done`. Divide by total committed Features. | `portfolio/art/<art-slug>/pi-<pi-slug>/objectives.md` + `portfolio/art/<art-slug>/program-backlog/*/<feature-slug>.feature.md` |
| Stories committed → done | Count `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md` files whose `id` appears in the `portfolio/art/<art-slug>/pi-<pi-slug>/iterations/<iteration-slug>/plan.md` Prioritized Story List and whose `status` is `done`. Divide by total listed Stories. | `portfolio/art/<art-slug>/pi-<pi-slug>/iterations/<iteration-slug>/plan.md` + `portfolio/art/<art-slug>/teams/*/team-backlog/*/<story-slug>.story.md` |
| Predictability (actual/planned BV %) | For each committed Feature in `portfolio/art/<art-slug>/pi-<pi-slug>/objectives.md`, read `plannedBv` and `actualBv` (filled at I&A). Sum `actualBv` / sum `plannedBv` × 100. | `portfolio/art/<art-slug>/pi-<pi-slug>/objectives.md` |
| ★ PR Gate cycle time (avg days) | For each Story that reached `awaiting-pr` or `done`, compute `(merge/PR-open date) - (first in-review date)` from `portfolio/art/<art-slug>/pi-<pi-slug>/iterations/<iteration-slug>/plan.md` and `portfolio/art/<art-slug>/teams/<team-slug>/daily/<daily-slug>.team-sync.md` notes/tables. Average over the PI. | `portfolio/art/<art-slug>/pi-<pi-slug>/iterations/<iteration-slug>/plan.md` + `portfolio/art/<art-slug>/teams/<team-slug>/daily/<daily-slug>.team-sync.md` |
| ★ Architecture Gate cycle time (avg days) | For each Feature with an `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.architecture-review.md`, compute `(review accepted date) - (review requested date)` from the review artifact. Average over the PI. | `portfolio/art/<art-slug>/program-backlog/*/<feature-slug>.architecture-review.md` |
| Defect escape rate | Count bugs listed in `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.qa-signoff.md` Bugs filed tables. Divide by the number of Stories done in the PI. | `portfolio/art/<art-slug>/teams/*/team-backlog/*/<story-slug>.qa-signoff.md` + `portfolio/art/<art-slug>/teams/*/team-backlog/*/<story-slug>.story.md` |
| Open blockers at PI end | Count rows in the latest `portfolio/art/<art-slug>/teams/<team-slug>/daily/<daily-slug>.team-sync.md` Open blockers table. | `portfolio/art/<art-slug>/teams/<team-slug>/daily/<daily-slug>.team-sync.md` |
| Risk ROAM distribution | Count Resolved / Owned / Accepted / Mitigated rows in `portfolio/art/<art-slug>/pi-<pi-slug>/risks.md` Risk register. | `portfolio/art/<art-slug>/pi-<pi-slug>/risks.md` |

## Output

Create the PI's Inspect & Adapt record, `portfolio/art/<art-slug>/pi-<pi-slug>/inspect-and-adapt.md`
(`status: metrics-reviewed`), from its template. This step writes **exactly one** artifact,
that record, and never a pain point.

- **Metrics** — every indicator above with its value, plan and deviation.
- **Pain-point candidates** — the top 2–3 deviations from plan: `symptom` names the indicator,
  `impact` gives its value against plan, plus the hypothesized systemic cause and, when one
  exists, the open pain point with the same cause. When no indicator deviates, write one row
  "none — PI within plan".
- A `stepOutcomes` entry (`outcome: written`).

Each candidate becomes one pain point in a later `improvement-backlog` run (one run per
candidate). The metrics you present are indicative; the record is the evidence.
