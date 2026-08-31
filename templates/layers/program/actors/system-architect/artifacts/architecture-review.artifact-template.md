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

# Architecture Review Template — `products/<product-slug>/.../reviews/<subject>-architecture-review.md`

Authored by `@system-architect` (or `@enterprise-architect` at the portfolio layer). A pure architecture verdict on a subject that does **not** itself produce an ADR (an ADR-producing review records its decision in the ADR attachments instead). One review per subject per attempt; a `fail` records blocking `openItems`.

```markdown
---
id: <subject>-architecture-review
subject: <artifact-id-or-path under review>
reviewer: '@system-architect'
verdict: pass            # pass | concerns | fail
created: YYYY-MM-DD
findings: []
openItems: []
---

# Architecture Review — <subject>

## Subject under review
Link / id. Restate the design, NFR, or runway item under review.

## NFR applicability
When the subject is a Feature, Feature-enabler, Story, or Story-enabler: does
`## NFR applicability / trace` match `products/<product-slug>/nfr-list.md`?
Record omitted applicable NFRs, invented NFRs, or a missing product register
(runway, not Feature/Story AC). Do not author the register in this packet.

## Findings
| id | severity | finding | recommendation |
|---|---|---|---|
| F-01 | high | ... | ... |

## Verdict
**PASS** — design clears the architecture runway.
*(or)* **CONCERNS** — non-blocking issues recorded as `openItems`.
*(or)* **FAIL** — blocking design defect; subject returns to its owner.

## Recommendations
Remediation guidance, owner, and target.
```

## Lifecycle
One review per subject per attempt. A `fail` lists blocking `openItems`; the next attempt produces `<subject>-architecture-review-2.md`.
