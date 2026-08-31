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

# NFR Register Template — `products/<product-slug>/nfr-list.md`

The product **Nonfunctional Requirements** register (SAFe NFRs / quality attributes). Seeded from
the **Architectural Vision** NFR backbone (`architecture-vision`), maintained by
`@system-architect` (Security is a challenger, not a co-author). NFRs are **enduring constraints**
on Features and Stories, **verified** at Story DoD, Verification & Sign-off, and the Demo Gate.
Compliance or architecture gaps may spawn **enabler** work.

This file is a **product singleton**, same grain as `architecture-runway.md`. It is not a
Feature-folder artifact. Features and Stories **trace** which NFRs apply; they never redefine the
canonical set.

| Artifact | Relation to this register |
|---|---|
| Architectural Vision | Seeds the cross-product backbone; does not replace this measurable product set |
| This `nfr-list` | Canonical product NFRs. Architecture-owned. Authored in Architectural Runway Extension |
| Feature / Feature-enabler | Traces which NFRs apply; optional tightening; never defines the set |
| Story / Story-enabler | Inherits the parent Feature's applicable NFRs; verifies; never defines the set |
| ADR | Design decisions that realize NFRs; written only after this register exists (or explicit-none) |
| Architecture Runway | Points at this register + ADRs + enabler Features that pave them |

```markdown
---
product: <slug>
revised: YYYY-MM-DD
---

# <Product> — NFR Register

| NFR | Category | Constraint (measurable) | Applies to | Verified by | Enabler? |
|---|---|---|---|---|---|
| NFR-01 | security | all endpoints authn/z; secrets in vault | all | Verification + Security | — |
| NFR-02 | performance | p95 < 200ms | F-N | QA perf check | — |
| NFR-03 | compliance | GDPR data-retention | product | compliance enabler | E-N / F-N |

Categories: security · performance · reliability · scalability · usability · maintainability ·
observability · compliance.
```
