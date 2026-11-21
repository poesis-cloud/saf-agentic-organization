---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Enabler Epic title>"
owner: "enterprise-architect"   # Agent slug of the author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
enablerType: "exploration"   # exploration | architecture | infrastructure | compliance
status: "funnel"   # funnel | reviewing | analyzing | ready | implementing | done
blocked: false   # True while an impediment stops the item; say why under `## Open questions`
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReductionOpportunityEnablement: 0
  jobSize: 0
  score: 0
transitions: []   # Kanban history
implementationStage: null   # mvp | persevere | null
resolution: null   # delivered | no-go | pivoted | stopped | null
strategicThemes: []   # Ids of the Strategic Themes the enabler Epic serves
valueStreams: []   # Paths of the value streams impacted
enables: []   # Paths of the business Epics this enabler makes possible or faster
leadingIndicators: []   # Early measures that predict the outcome
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Epic hypothesis statement

<!-- Required. For <the value streams or trains> who <need something>, the <enabler> is a <runway, platform, exploration or compliance change> that <makes this possible or faster>. Unlike <the alternative>, it <does something better: the why>. -->

## Outcomes hypothesis

<!-- Required. The measurable benefits expected if the hypothesis holds: what the enabled Epics gain in speed, cost, risk or compliance. -->

## Enabled work

<!-- Optional: omit the section when empty. The business Epics, Capabilities or Features that need this enabler, and by when. -->

## Leading indicators

<!-- Optional: omit the section when empty. The early measures and how they will be collected. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. Qualities and constraints the enabler Epic imposes or must respect. -->

## Scope

<!-- Optional: omit the section when empty. In scope, out of scope. -->

## MVP

<!-- Optional: omit the section when empty. The minimal version sufficient to prove or disprove the hypothesis; once run, the evidence and the pivot-or-persevere recommendation. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
