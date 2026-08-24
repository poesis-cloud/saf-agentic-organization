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

# Objectives Template — `art/<art-slug>/pi-<pi-slug>/objectives.md`

Authored by RTE at PI Planning. One file per product per PI.

```markdown
---
pi: M
product: <product-slug>
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
capacity_points: 0
committedFeatures:
  - id: F-12
    title: ...
    plannedBv: 8
    actualBv: null           # filled at Inspect & Adapt
    status: committed          # committed | in-progress | done | blocked | cancelled
stretchFeatures:
  - id: F-15
    title: ...
    plannedBv: 5
    status: refined            # refined | in-progress | done | blocked | cancelled
---

# PI-M Objectives — <product>

## PI theme
One sentence framing what this PI delivers.

## Committed Features (with business value 1–10, set by Central Supervisor)

| Feature | Title | Planned BV | Actual BV (filled at I&A) | Status |
|---|---|---|---|---|
| F-12 | ... | 8 | — | committed |

## Stretch Features
| Feature | Title | Planned BV | Status |
|---|---|---|---|
| F-15 | ... | 5 | refined |

## Cross-product dependencies
List Features in other products that this PI depends on (`<other-slug>/F-N`).

## Milestones
- M+0 weeks: ...
- M+N weeks (IP): Inspect & Adapt
```

## Lifecycle

Created at PI Planning; updated at each Iteration boundary; closed at Inspect & Adapt with actual BV filled in.
