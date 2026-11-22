---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Capability title>"
owner: "solution-manager"   # Agent slug of the author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
status: "funnel"   # funnel | analyzing | ready | implementing | validating-on-staging | deploying-to-production | releasing | done
blocked: false   # True while an impediment stops the item; say why under `## Open questions`
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReductionOpportunityEnablement: 0
  jobSize: 0
  score: 0
transitions: []   # Kanban history
parent: null   # The portfolio Epic this capability splits from
targetPi: null   # PI slug the capability is planned for, or null
arts: []   # Paths of the ART folders expected to contribute
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model. Template: drop this line and the guidance comments in the artifact. -->

## Description

<!-- Required. What the capability is, in one paragraph. -->

## Benefit hypothesis

<!-- Required. The measurable benefit expected for the customer or the business. -->

## Acceptance criteria

<!-- Required. Independently testable criteria that cover the functionality and the relevant NFRs. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. Solution Intent constraints that apply, and any tightening. -->

## Feature split

<!-- Optional: omit the section when empty. The Features each ART would take, as candidates. -->

## Dependencies and suppliers

<!-- Optional: omit the section when empty. Cross-ART and supplier dependencies. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
