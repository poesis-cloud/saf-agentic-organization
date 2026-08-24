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

# NFR Register Template — `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.nfr-list.md`

The product **Nonfunctional Requirements** register (SAFe NFRs / quality attributes). Seeded from
the **Architectural Vision** NFR backbone (`architecture-vision`), maintained by
`@system-architect` + `@security-expert`. NFRs are **enduring constraints** on Features / Stories,
**verified** at Verification & Sign-off and the Demo Gate. Compliance or architecture gaps may
spawn **enabler** work. The canonical register is architecture-scoped and belongs under the
product's `art/<art-slug>/program-backlog/` folder; Features should only trace which NFRs apply to them.

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
