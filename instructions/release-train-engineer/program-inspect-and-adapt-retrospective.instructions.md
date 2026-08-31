---
description: 'Inspect & Adapt Step 2 — run the problem-solving workshop using the ART improvement-backlog pain points as primary input, then update those pain points and dispatch owning actors to create derived backlog items.'
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

Run the PI problem-solving workshop. This step updates pain-point artifacts but does **not** author derived Features, Stories, or enablers — those are created by their owning actors in subsequent workflow steps. 

## Inputs

- All `art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md` artifacts with `status: open`.
- The metrics presented in Step 1.

## Procedure

1. **Metrics interpretation** — call out the top 2–3 indicators that deviated most from plan and hypothesize systemic causes.
2. **Pain-point root-cause analysis** — for each open pain point:
   - Cluster related pain points.
   - Apply five-whys / fishbone analysis.
   - Decide resolution: `workflow-improvement`, `product-improvement`, `accepted`, or `duplicate`.
3. **Update pain points** — set `rootCause`, `resolution`, `targetArtifact`, and `status` on each reviewed pain point.
4. **Triage** — for each pain point, record:
   - `workflow-improvement` → target meta-artifact (`layers/...`, `instructions/...`, `conf/...`) and owning actor.
   - `product-improvement` → derived backlog item type, owning actor, and location.
5. **Prepare derived backlog items** — for each `product-improvement` pain point, set:
   - `derivedFeatures` or `derivedStories` placeholders
   - Type: `feature`, `story`, `feature-enabler`, or `story-enabler`
   - Owning actor: `@product-manager` (Features), `@product-owner` (Stories), or `@system-architect` (enablers)
   - Proposed title and rationale in the pain point body
   Do **not** create the artifact yourself. The owning actor creates it in the next workflow step.
6. **Dispatch workflow improvements** — for each `workflow-improvement` pain point, record the target meta-artifact and owning actor. The owning actor implements the change in its own workflow.
7. **PI+1 priming** — list carry-over Features (committed but not done) and top candidates for the next PI funnel. Output this as user-facing text only.

## Output

Update each reviewed pain point's frontmatter and body with root cause, resolution, target artifact, derived item placeholders, and final `status` (`converted`, `resolved`, `accepted`, or `duplicate`).

**Only `@release-train-engineer` updates pain-point artifacts in this workflow.**
