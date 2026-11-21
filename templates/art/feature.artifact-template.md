---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Feature title>"
owner: "product-manager"   # Agent slug of the author
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
parent: null   # The Epic or Capability this Feature splits from; null for a Feature from the ART's local context
targetPi: null   # PI slug the Feature is planned for, or null
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Description

<!-- Required. What the Feature is, in one paragraph. -->

## Benefit hypothesis

<!-- Required. The measurable benefit expected for the customer or the business, and how it will be observed. -->

## Acceptance criteria

<!-- Required. One bullet per criterion (AC1, AC2, …), independently testable, covering the functionality and the relevant NFRs. Given/When/Then where it helps. -->

## Nonfunctional requirements

<!-- Optional: omit the section when empty. The NFR ids from the ART's register that apply, and any tightening. A missing NFR is an `nfr-refinement` concern, not an acceptance criterion. -->

## Stories

<!-- Optional: omit the section when empty. Candidate split into Stories, each a vertical slice. -->

## Dependencies

<!-- Optional: omit the section when empty. Other Features, teams, ARTs, suppliers, architecture decisions. -->

## Open questions

<!-- Optional: omit the section when empty. What is still unknown, who can answer, and the assumption taken meanwhile. -->
