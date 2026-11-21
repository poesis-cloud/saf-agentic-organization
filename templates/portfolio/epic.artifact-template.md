---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Epic title>"
owner: "epic-owner"   # Agent slug of the owning author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
type: "business"   # business | enabler
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
strategicThemes: []   # Ids of the Strategic Themes the Epic serves
valueStreams: []   # Paths of the value streams impacted
leadingIndicators: []   # Early measures that predict the business outcome
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Epic hypothesis statement

<!-- Required. For <customers> who <do something>, the <solution> is a <something: the how> that <provides this value>. Unlike <the alternative>, our solution <does something better: the why>. -->

## Business outcomes hypothesis

<!-- Required. The measurable benefits the business expects if the hypothesis holds. -->

## Leading indicators

<!-- Optional: omit the section when empty. The early measures and how they will be collected. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. Qualities and constraints the Epic imposes or must respect. -->

## Scope

<!-- Optional: omit the section when empty. In scope, out of scope. -->

## MVP

<!-- Optional: omit the section when empty. The minimal version sufficient to prove or disprove the hypothesis; once run, the evidence and the pivot-or-persevere recommendation. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
