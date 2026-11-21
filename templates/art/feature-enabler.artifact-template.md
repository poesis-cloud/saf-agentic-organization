---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Enabler Feature title>"
owner: "system-architect"   # Agent slug of the author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
enablerType: "exploration"   # exploration | architecture | infrastructure | compliance
status: "funnel"   # funnel | analyzing | ready | implementing | validating-on-staging | deploying-to-production | releasing | done
blocked: false   # True while an impediment stops the item; say why under `## Open questions`
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReductionOpportunityEnablement: 0
  jobSize: 0
  score: 0
transitions: []   # Kanban history
parent: null
enables: []   # Paths of the Features this enabler makes possible or faster
adrs: []   # Paths of the architecture decisions it implements
targetPi: null   # PI slug the enabler Feature is planned for, or null
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Description

<!-- Required. What the enabler builds or must learn, in one paragraph. -->

## Benefit hypothesis

<!-- Required. What it makes possible or faster for the named Features, and how that will be observed. -->

## Acceptance criteria

<!-- Required. One bullet per criterion (AC1, AC2, …), demonstrable on a working system, covering the relevant NFRs. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. The NFR ids from the ART's register that apply, and any tightening. -->

## Stories

<!-- Optional: omit the section when empty. Candidate split into enabler Stories (a spike is an exploration enabler). -->

## Dependencies

<!-- Optional: omit the section when empty. Other Features, teams, ARTs, suppliers, architecture decisions. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
