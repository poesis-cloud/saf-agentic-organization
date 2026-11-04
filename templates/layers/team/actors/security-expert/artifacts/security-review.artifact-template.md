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

# Security Review Template

The review sits beside its subject, at one of the paths `conf/workspace.conf.yaml` binds for this kind:

- `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.security-review.md`
- `portfolio/products/<product-slug>/architecture-vision.security-review.md`

Authored by `@security-expert`. The security verdict on a subject (a Story, Feature, ADR, runway item, or PR). One review file per subject; a `fail` records blocking `openItems` the owning step must clear.

```markdown
---
slug: <subject-slug>-security-review
id: <subject>-security-review
subject: <artifact-id-or-path under review>
reviewer: '@security-expert'
verdict: pass            # pass | concerns | fail
created: "YYYY-MM-DD"
findings: []
openItems: []
stepOutcomes: []          # every step that commits this file appends one entry: { step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <what was decided and why>, friction: <optional workflow friction observed> }
---

# Security Review — <subject>

## Subject under review
Link / id. Restate the trust boundary, surface, or change under review.

## Findings
| id | severity | finding | recommendation |
|---|---|---|---|
| F-01 | high | ... | ... |

## Verdict
**PASS** — no blocking security concerns.
*(or)* **CONCERNS** — non-blocking issues recorded as `openItems`.
*(or)* **FAIL** — blocking security defect; subject returns to its owner.

## Recommendations
Remediation guidance, owner, and target.
```

## Lifecycle
One review file per subject. A `fail` lists blocking `openItems`; a later review pass updates the same file and appends its own `stepOutcomes` entry.
