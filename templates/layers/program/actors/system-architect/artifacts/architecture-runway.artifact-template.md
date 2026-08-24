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

# Architectural Runway Register Template — `products/<product-slug>/architecture-runway.md`

The product's **Architectural Runway** register (SAFe) — the runway capabilities, references, and
enabler work that build technical foundation ahead of business Features. Seeded by the
**Architectural Vision** and extended by the **Architectural Runway Extension** practice
(`architectural-runway-extension`). Each runway item may have:

- an **architecture reference** from the standard artifact set (ADR, architecture decision
  inventory, NFR register, or other owned template-backed artifact) that defines or constrains the
  runway item, and
- one or more **enabler Features** (`type: enabler`) that realize that runway item through the
  normal Feature FSM + gates.

This register tracks both the reference artifact and the backlog realization so PI Planning can
budget enabler capacity without confusing architecture documentation with enabler backlog units. It
is architecture-scoped and belongs under the product's `art/<art-slug>/program-backlog/` folder, not beside the
backlog folders.

```markdown
---
product: <slug>
revised: YYYY-MM-DD
---

# <Product> — Architectural Runway

| Runway item | Architecture reference | Realized by enabler Features | enablerType | Consumed by (Features) | Readiness |
|---|---|---|---|---|---|
| <capability> | ADR-N; `<adr-slug>.adr.md`; `<feature-slug>.nfr-list.md` | F-N (`type: enabler`) | architectural | F-AA, F-BB | building |

enablerType: exploration · architectural · infrastructure · compliance.
Readiness: building · ready · depleting.

## Runway health
- Ready ahead of demand: ...
- Gaps (seed enabler Features → `architectural-runway-extension`): ...
- Depleting (needs extension): ...
```
