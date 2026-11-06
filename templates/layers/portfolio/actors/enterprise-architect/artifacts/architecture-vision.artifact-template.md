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

# Architectural Vision Template — `portfolio/products/<product-slug>/architecture-vision.md`

The cross-product **Architectural Vision** (SAFe) — the future-state architecture, the NFR
backbone, and the architectural-runway direction. Authored by `@enterprise-architect` in the
**Architectural Vision** practice (`architecture-vision`); the portfolio's
intentional-architecture anchor. Feeds Epic runway (`reviewing→analyzing`) and every product's
NFR register + runway register. Portfolio-scoped singleton.

```markdown
---
slug: <product-slug>-architecture-vision
id: architecture-vision
owner: central-supervisor   # EA hat
revised: "YYYY-MM-DD"
closedItems: []          # open items on Epics this Vision closes: { artifact: epic | epic-enabler, unit: <Epic id, e.g. E-2>, item: <openItems id>, resolution: <one line> }; epic-vision-alignment flips each to resolved on that Epic
stepOutcomes: []          # every step that commits this file appends one entry: { step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <what was decided and why>, friction: <optional workflow friction observed> }
---

# Architectural Vision

## Future-state architecture
Target architecture across the portfolio's products; key components and boundaries.

## Architectural principles (intentional architecture)
The standing decisions + constraints (security, data, integration, observability, set-based options).

## NFR backbone
Cross-product nonfunctional requirements (→ each product's `portfolio/products/<product-slug>/nfr-list.md`).

## Runway direction & enabler Epics
The runway the portfolio must build ahead of demand; seeds **enabler Epics** (`type: enabler`,
`enablerType: architectural | infrastructure | compliance`).

## Target ARTs / products
Which products realise which parts of the Vision.

## Decisions on Epics
Per Epic or Enabler Epic (by id): the Feature seeds this Vision places on it (MVP or not, each
with its target ART), the WSJF inputs the runway changes (job size), and the open items it
closes (also listed in `closedItems`). The Vision never writes an Epic: `epic-vision-alignment`,
run once per Epic named here, has the owners write them into the Enabler Epic, the Epic and
the Lean Business Case. A Vision that decides about no Epic leaves this section empty.
```
