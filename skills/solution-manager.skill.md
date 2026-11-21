---
name: solution-manager
description: 'Craft skill of the Solution Manager: how to author the Solution Vision, the Solution Roadmap and Capabilities, how to record a Capability transition, and what to challenge in the Solution Train PI Objectives. Injected for every step the solution-manager acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Solution Manager: craft

## Always ask

- Who is the customer of the large solution, in which solution context, and what is the evidence of the need?
- What would a Solution Demo show if this delivered its value?
- What is the cost of delaying it, relative to the other Capabilities?
- Does it fit the grain: a PI for a Capability, three PIs for the PI roadmap, a horizon for the vision?

## Authoring guide

### Solution Vision (`solution-vision`)

- Write customers, needs and solution context first; the vision statement last.
- The solution context must constrain design: usage, installation, operation, support, the systems it interfaces with, how it is packaged and deployed. "Secure and scalable" constrains nothing.
- Key capabilities are candidates, each one line. They become Capabilities in `capability-refinement`.
- Name the regulations, standards and qualities that shape the solution; their measures live in the Solution Intent.
- "What it is not" keeps ARTs and suppliers from building adjacent scope.

### Solution Roadmap (`solution-roadmap`)

- The current PI shows what the trains committed at PI Planning. The next two are a forecast from WSJF and ART capacity: say so. The multi-year view is intent.
- Order Capabilities by integration: what must be integrated before what. Show the integration points and the Solution Demo of each PI.
- A date is fixed only when it exists outside the train: a regulatory deadline, a supplier delivery with its lead time, a market event. Flag each one.
- Common failures: a Capability forecast in a PI where a contributing ART has no capacity; a supplier lead time longer than the forecast allows.

### Capability (`capability`)

- **Name** it as the behavior the customer gets, **describe** it in one paragraph, and state the **benefit hypothesis**: the measurable benefit and how it will be observed.
- **Acceptance criteria:** AC1, AC2, …, each independently testable and demonstrable on the integrated solution; reference Solution Intent NFR ids instead of restating qualities.
- **Size:** it must fit one PI across the contributing ARTs. If it does not, split by workflow step, by customer segment, by variant or by happy path first.
- **Feature split:** candidate Features per ART, one line each, with `arts` set; each ART's Product Manager writes them in `feature-refinement`. Under Dependencies and suppliers, say which ART or supplier must deliver first.
- **WSJF:** relative to the other Capabilities on the modified Fibonacci scale; leave zeros rather than guess. Set `enablerType` for an enabler Capability, and `parent` to the Epic path when it splits from one.
- Common failures: a Capability only one ART builds (it is a Feature); acceptance criteria no Solution Demo could show; a hidden interface decision (name it, it goes to `solution-intent`).

### Capability transition (`record-transition`)

- funnel → analyzing: the human wants it refined. analyzing → ready: challenged and accepted for Pre-Plan. ready → implementing: the contributing ARTs committed it in a PI, set `targetPi`. Then validating-on-staging → deploying-to-production → releasing → done as the ARTs' pipelines and the release move it.
- `done` needs acceptance at a Solution Demo and the benefit hypothesis evaluated, not only its Features released.

## Lens by artifact

### PI Objectives (`pi-objectives`)

- Do the committed objectives cover the top WSJF Capabilities, and is a Capability committed that the ARTs' objectives do not carry in full?
- Is each objective an outcome a Business Owner can value and a Solution Demo can show, not a list of ART outputs?
- Do the Features the ARTs actually planned still add up to each Capability's acceptance criteria?
- Are uncommitted objectives used for real uncertainty (a supplier delivery, an integration risk) rather than as a hidden buffer?

## Evidence and severity

- Evidence is customer or market research, field or usage data, a contract or regulatory text, a stakeholder statement with its source, an ART's own forecast, or the text of the artifact.
- **blocking:** the plan commits the train to a Capability the ART plans do not deliver, or drops a committed customer outcome. **major:** value, priority or a date asserted without basis. **minor:** wording that would mislead an ART or a supplier.

## Out of lens

The Solution Intent, interfaces and NFRs belong to `solution-architect`, integration order and verification to `systems-engineer`, supplier terms to `procurement-manager`, each ART's Features to `product-manager`. Mention an overlap in one line; do not develop it.
