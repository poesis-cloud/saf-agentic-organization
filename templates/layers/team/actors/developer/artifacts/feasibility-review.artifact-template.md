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

# Feasibility Review Template — `products/<product-slug>/.../reviews/<subject>-feasibility-review.md`

Authored by `@developer`. The implementation-feasibility verdict on a subject (a Feature, Story, or enabler) — technical risk, effort realism, dependency exposure, and build viability. One review per subject per attempt; a `fail` records blocking `openItems`.

```markdown
---
id: <subject>-feasibility-review
subject: <artifact-id-or-path under review>
reviewer: '@developer'
verdict: pass            # pass | concerns | fail
created: YYYY-MM-DD
findings: []
openItems: []
---

# Feasibility Review — <subject>

## Subject under review
Link / id. Restate the scope, the proposed approach, and the dependencies under review.

## Findings
| id | severity | finding | recommendation |
|---|---|---|---|
| F-01 | high | ... | ... |

## Verdict
**PASS** — implementation feasible as scoped.
*(or)* **CONCERNS** — non-blocking risks recorded as `openItems`.
*(or)* **FAIL** — blocking feasibility defect; subject returns to its owner.

## Recommendations
Remediation guidance, owner, and target.
```

## Lifecycle
One review per subject per attempt. A `fail` lists blocking `openItems`; the next attempt produces `<subject>-feasibility-review-2.md`.
