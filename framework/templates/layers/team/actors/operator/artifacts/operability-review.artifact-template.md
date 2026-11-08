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

# Operability Review Template

The review sits beside its subject, at one of the paths `conf/workspace.conf.yaml` binds for this kind:

- `portfolio/art/<art-slug>/releases/<release-slug>/<release-slug>.operability-review.md`
- `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.operability-review.md`
- `portfolio/products/<product-slug>/architecture-vision.operability-review.md`
- `portfolio/products/<product-slug>/architecture-runway.operability-review.md`

Authored by `@operator`. The operability verdict on a subject (a Feature, runway item, deployment topology, or release) — CI/CD, Helm, environment config, observability, and runtime concerns. One review file per subject; a `fail` records blocking `openItems`.

```markdown
---
slug: <subject-slug>-operability-review
id: <subject>-operability-review
subject: <artifact-id-or-path under review>
reviewer: '@operator'
verdict: pass            # pass | concerns | fail
created: "YYYY-MM-DD"
findings: []
openItems: []
stepOutcomes: []          # every step that commits this file appends one entry: { step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <what was decided and why>, friction: <optional workflow friction observed> }
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
One review file per subject. A `fail` lists blocking `openItems`; a later review pass updates the same file and appends its own `stepOutcomes` entry.
