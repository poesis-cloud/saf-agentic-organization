---
name: portfolio-manager
description: 'Craft skill of the Portfolio Manager: how to author Strategic Themes, the Portfolio Vision and canvas, a development value stream, the Portfolio Roadmap and Lean Budgets with their guardrails. Injected for every step the portfolio-manager acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Portfolio Manager: craft

## Always ask

- Which statement of the enterprise strategy does this serve, and what does the portfolio stop doing because of it?
- What is the current state in facts: value streams, solutions, customers, spend, KPIs?
- Is this committed, forecast or intent, and who committed?
- Does the money fund a value stream that persists, or a project in disguise?

## Authoring guide

### Strategic Themes (`strategic-themes`)

- A theme is a portfolio-level business objective that gives competitive differentiation and strategic advantage. Keep them few, each with a stable id (ST1, ST2) that Epics cite in `strategicThemes`.
- OKR format: one objective (the business outcome) and two to five key results, each a measurable success criterion with baseline, target and date. "Launch the portal" is an activity, not a key result.
- Common failures: business as usual stated as a theme; a key result with no data source; nothing under "What we will not pursue", which means no choice was made.

### Portfolio Vision (`portfolio-vision`)

- Current-state canvas: facts only, each number with its source. A block nobody can fill is an open question, not a guess.
- Derive the future state from the Strategic Themes and a SWOT/TOWS reading; say which blocks change and which stay.
- Write the vision statement last, short and motivational.

### Development Value Stream (`value-stream`)

- Map the operational value stream first (customer, trigger, steps, value delivered): the development value stream builds the solutions those steps use.
- Size the trains from the people needed: above 125, several ARTs; several ARTs and suppliers building one large solution form a Solution Train.
- Four to seven KPIs, from the Strategic Themes and local concerns, each an outcome with unit, baseline and data source.
- Common failure: a value stream drawn along a department or a technology layer instead of the flow of value.

### Portfolio Roadmap (`portfolio-roadmap`)

- Grain by horizon: near term by PI, each Epic with its path; mid term by quarter or half-year; long term as undated themes and bets.
- Check the near term against the funded capacity in the Lean Budgets; say where it does not fit.
- Milestones: separate dates fixed outside the portfolio (regulation, contract, market event) from internal targets.
- Common failures: precision that grows with distance; an Epic drawn at full scope before its MVP proved the hypothesis.

### Lean Budgets (`lean-budgets`)

- Per value stream, Baseline Solution Investments (BSIs) first: the cost to develop, support and operate the solutions that deliver current business capabilities. Fund, adjust or decommission each.
- Then Proposed Solution Initiatives (PSIs): portfolio Epics, and solution Epics above `epicThreshold`; those below it count as BSIs. Give each value stream its proportional share of an Epic's cost.
- Budget only the Epic cost expected in the period: the full cost is not committed until the MVP hypothesis is proven. An Epic in progress re-enters as a PSI when its remaining cost exceeds the threshold; prior spend is sunk cost. The value stream totals must sum to `totalBudget`: show the arithmetic.
- The four Lean budget guardrails, each as applied: guiding investments by horizon (target and actual mix); applying capacity allocation to optimize value and solution integrity (the split per value stream); approving significant initiatives (the threshold and who approves); continuous Business Owner engagement (when and how). The first two are quantitative: give numbers.
- Forum insights: record the funding patterns of the Strategic Investment Planning forums and the reasons given. Partially funded items are candidates for termination or cutbacks.

## Evidence and severity

- Evidence is the human's strategy input quoted with its source, a committed artifact cited by path, a financial figure with unit, period and source, or a train's own forecast. A number without a source is an assumption: label it.
- Weigh the findings you answer on this scale. **blocking:** the draft breaks a guardrail, does not sum to the total budget, funds an Epic beyond its MVP before the hypothesis is proven, or shows a commitment no train made. **major:** a theme, canvas block, KPI or allocation without a measurable basis or a link to a Strategic Theme. **minor:** wording that would mislead a value stream.

## Out of lens

Epics and Lean Business Cases belong to `epic-owner`, the Architecture Vision to `enterprise-architect`, cost realism and CapEx and OpEx treatment to `financial-controller`. Name such a point in one line; do not develop it.
