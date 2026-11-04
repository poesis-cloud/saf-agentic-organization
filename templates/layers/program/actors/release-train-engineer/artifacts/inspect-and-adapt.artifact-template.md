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

# Inspect & Adapt Template — `art/<art-slug>/pi-<pi-slug>/inspect-and-adapt.md`

Authored by `@release-train-engineer`. One record per ART and PI: `metrics-review` creates it,
`pi-retrospective` updates it. It never writes pain points: each candidate and each triage
decision below is applied to one pain point by one `improvement-backlog` workflow run.

```markdown
---
art: <art-slug>
pi: <pi-slug>
status: metrics-reviewed  # metrics-reviewed | triaged
stepOutcomes: []          # every step that commits this file appends one entry: { step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: YYYY-MM-DD, note: <what was decided and why>, friction: <optional workflow friction observed> }
---

# Inspect & Adapt — <art-slug> PI <pi-slug>

## Metrics
| Indicator | Value | Plan | Deviation |
|---|---|---|---|

## Pain-point candidates
One row per deviation or friction to record; "none — PI within plan" when nothing deviates.

| Candidate | Origin | Symptom | Impact | Hypothesized cause | Existing pain point |
|---|---|---|---|---|---|

## Triage
One row per open pain point reviewed in the problem-solving workshop.

| Pain point | Root cause | Resolution | Target artifact | Derived item (type, owner) | Status to set |
|---|---|---|---|---|---|

## PI+1 priming
Indicative input to the next PI Planning; decides nothing.
```
