---
description: 'Inspect & Adapt Step 1 — calculate PI metrics by reading existing artifact content and present them to the facilitator. No dedicated metric fields are required on source artifacts.'
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
| Features committed → done | Count `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md` files whose `id` is listed in `art/<art-slug>/pi-<pi-slug>/objectives.md` committed Features and whose `status` is `done`. Divide by total committed Features. | `art/<art-slug>/pi-<pi-slug>/objectives.md` + `art/<art-slug>/program-backlog/*/<feature-slug>.feature.md` |
| Stories committed → done | Count `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md` files whose `id` appears in the `products/<product-slug>/<plan-slug>.plan.md` Prioritized Story List and whose `status` is `done`. Divide by total listed Stories. | `products/<product-slug>/<plan-slug>.plan.md` + `art/<art-slug>/teams/*/team-backlog/*/<story-slug>.story.md` |
| Predictability (actual/planned BV %) | For each committed Feature in `art/<art-slug>/pi-<pi-slug>/objectives.md`, read `plannedBv` and `actualBv` (filled at I&A). Sum `actualBv` / sum `plannedBv` × 100. | `art/<art-slug>/pi-<pi-slug>/objectives.md` |
| ★ PR Gate cycle time (avg days) | For each Story that reached `awaiting-pr` or `done`, compute `(merge/PR-open date) - (first in-review date)` from `products/<product-slug>/<plan-slug>.plan.md` and `products/<product-slug>/<progress-slug>.progress.md` notes/tables. Average over the PI. | `products/<product-slug>/<plan-slug>.plan.md` + `products/<product-slug>/<progress-slug>.progress.md` |
| ★ Architecture Gate cycle time (avg days) | For each Feature with an `art/<art-slug>/program-backlog/<feature-slug>/<architecture-review-slug>.architecture-review.md`, compute `(review accepted date) - (review requested date)` from the review artifact. Average over the PI. | `art/<art-slug>/program-backlog/*/<architecture-review-slug>.architecture-review.md` |
| Defect escape rate | Count bugs listed in `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<qa-signoff-slug>.qa-signoff.md` Bugs filed tables. Divide by the number of Stories done in the PI. | `art/<art-slug>/teams/*/team-backlog/*/<qa-signoff-slug>.qa-signoff.md` + `art/<art-slug>/teams/*/team-backlog/*/<story-slug>.story.md` |
| Open blockers at PI end | Count rows in the latest `products/<product-slug>/<progress-slug>.progress.md` Open blockers table. | `products/<product-slug>/<progress-slug>.progress.md` |
| Risk ROAM distribution | Count Resolved / Owned / Accepted / Mitigated rows in `art/<art-slug>/pi-<pi-slug>/risks.md` Risk register. | `art/<art-slug>/pi-<pi-slug>/risks.md` |

## Output

Present the calculated metrics to the facilitator. Call out the top 2–3 deviations and hypothesize systemic causes. This step is user-facing output only; do not write or update any artifact.
