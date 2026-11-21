---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Enabler Capability title>"
owner: "solution-architect"   # Agent slug of the author
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
parent: null   # The Epic or enabler Epic this enabler Capability splits from
enables: []   # Paths of the Capabilities this enabler makes possible or faster
targetPi: null   # PI slug the enabler Capability is planned for, or null
arts: []   # Paths of the ART folders expected to contribute
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Description

<!-- Required. What the enabler builds or must learn, in one paragraph. -->

## Benefit hypothesis

<!-- Required. What it makes possible or faster for the named Capabilities, and how that will be observed. -->

## Acceptance criteria

<!-- Required. Criteria demonstrable on the integrated solution at a Solution Demo, covering the relevant NFRs. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. Solution Intent constraints that apply, and any tightening. -->

## Feature split

<!-- Optional: omit the section when empty. The enabler Features each ART would take, as candidates. -->

## Dependencies and suppliers

<!-- Optional: omit the section when empty. Cross-ART and supplier dependencies, and the variable intent it closes. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
