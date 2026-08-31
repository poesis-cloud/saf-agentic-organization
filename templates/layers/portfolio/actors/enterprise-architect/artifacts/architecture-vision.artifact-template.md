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

# Architectural Vision Template — `portfolio/architecture-vision.md` (singleton)

The cross-product **Architectural Vision** (SAFe) — the future-state architecture, the NFR
backbone, and the architectural-runway direction. Authored by `@enterprise-architect` in the
**Architectural Vision** practice (`architecture-vision`); the portfolio's
intentional-architecture anchor. Feeds Epic runway (`reviewing→analyzing`) and every product's
NFR register + runway register. Portfolio-scoped singleton.

```markdown
---
id: architecture-vision
owner: central-supervisor   # EA hat
revised: YYYY-MM-DD
---

# Architectural Vision

## Future-state architecture
Target architecture across the portfolio's products; key components and boundaries.

## Architectural principles (intentional architecture)
The standing decisions + constraints (security, data, integration, observability, set-based options).

## NFR backbone
Cross-product nonfunctional requirements (→ each product's `products/<product-slug>/nfr-list.md`).

## Runway direction & enabler Epics
The runway the portfolio must build ahead of demand; seeds **enabler Epics** (`type: enabler`,
`enablerType: architectural | infrastructure | compliance`).

## Target ARTs / products
Which products realise which parts of the Vision.
```
