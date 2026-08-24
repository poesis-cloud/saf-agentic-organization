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

# Operability Review Template — `products/<product-slug>/.../reviews/<subject>-operability-review.md`

Authored by `@operator`. The operability verdict on a subject (a Feature, runway item, deployment topology, or release) — CI/CD, Helm, environment config, observability, and runtime concerns. One review per subject per attempt; a `fail` records blocking `openItems`.

```markdown
---
id: <subject>-operability-review
subject: <artifact-id-or-path under review>
reviewer: '@operator'
verdict: pass            # pass | concerns | fail
created: YYYY-MM-DD
findings: []
openItems: []
---

# Operability Review — <subject>

## Subject under review
Link / id. Restate the deployment, pipeline, or runtime surface under review.

## Findings
| id | severity | finding | recommendation |
|---|---|---|---|
| F-01 | high | ... | ... |

## Verdict
**PASS** — operationally ready.
*(or)* **CONCERNS** — non-blocking issues recorded as `openItems`.
*(or)* **FAIL** — blocking operability defect; subject returns to its owner.

## Recommendations
Remediation guidance, owner, and target.
```

## Lifecycle
One review per subject per attempt. A `fail` lists blocking `openItems`; the next attempt produces `<subject>-operability-review-2.md`.
