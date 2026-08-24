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

# Pain Point Template — `art/<art-slug>/improvement-backlog/<pp-slug>/<pain-point-slug>.pain-point.md`

Authored by `@release-train-engineer` (or any agent observing systemic friction). A pain point is a raw, append-only input to the Inspect & Adapt problem-solving workshop. It is triaged there and either resolved as a workflow improvement or converted into a product improvement (Feature / Story).

```markdown
---
id: PP-YYYYMMDD-NN
title: <short symptom statement>
status: open                 # open | triaged | resolved | converted | accepted | duplicate
origin: iteration            # iteration | pi | workflow | cross-product | metrics-review
layer: program               # portfolio | program | team
symptom: <one-sentence observable friction>
impact: <who is affected and how much>
rootCause: null             # filled during I&A problem-solving
resolution: null             # workflow-improvement | product-improvement | accepted | duplicate
targetArtifact: null        # file/artifact for workflow improvements
derivedFeatures: []         # filled when resolution = product-improvement
derivedStories: []          # filled when resolution = product-improvement
relatedPainPoints: []
owner: @release-train-engineer
created: YYYY-MM-DD
---

# PP-YYYYMMDD-NN — <title>

## Symptom
What exactly was observed? Be specific and avoid solution language.

## Impact
- Affected roles:
- Frequency:
- Cost (time, quality, morale):

## Root cause
Filled during the Inspect & Adapt problem-solving workshop (five-whys / fishbone).

## Resolution
- `workflow-improvement` — change a skill / instruction / prompt / orchestrator / template.
- `product-improvement` — create a Feature or Story in the appropriate backlog.
- `accepted` — acknowledged as inherent constraint, no action.
- `duplicate` — superseded by another pain point.

## Target artifact
For workflow improvements: the concrete file or artifact id to change.

## Derived backlog items
For product improvements: links to the created Feature / Story artifacts.

## Related pain points
- PP-...
```

## Lifecycle

1. **Capture** — anyone may append a pain point the moment friction is observed.
2. **Triage** — `@release-train-engineer` triages at Inspect & Adapt, setting `resolution` and `rootCause`.
3. **Resolve or convert** — workflow improvements are implemented and marked `resolved`; product improvements spawn Features/Stories and are marked `converted`.
