---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Story title>"
owner: "product-owner"   # Agent slug of the owning author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
type: "user"   # user | enabler
enablerType: null   # exploration | architecture | infrastructure | compliance | null
status: "backlog"   # backlog | ready | in-progress | in-review | accepted
blocked: false   # True while an impediment stops the item; say why under `## Open questions`
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReductionOpportunityEnablement: 0
  jobSize: 0
  score: 0
transitions: []   # Kanban history
parent: null   # The Feature this Story splits from; null for a Story from the team's local context
estimate: null   # Story points (modified Fibonacci), set by the team
iteration: null   # Iteration slug the Story is planned in, or null
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Story

<!-- Required. As a <user role>, I want to <activity>, so that <business value>. For an enabler: what must be learned or built, and why now. -->

## Acceptance criteria

<!-- Required. One bullet per criterion (AC1, AC2, …): Given <context>, when <action>, then <observable outcome>. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. The NFR ids that apply to this Story and how they are checked. -->

## Notes

<!-- Optional: omit the section when empty. Design notes, examples, links. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
