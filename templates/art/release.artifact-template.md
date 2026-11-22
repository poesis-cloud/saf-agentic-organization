---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Release title>"
owner: "release-manager"   # Agent slug of the author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
status: "planned"   # planned | ready | released | rolled-back | cancelled
features: []   # Paths of the Features released
targetDate: null   # YYYY-MM-DD targeted, or null for on demand
strategy: "<release strategy>"   # How the release is exposed (e.g
transitions: []   # State history
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model. Template: drop this line and the guidance comments in the artifact. -->

## Scope

<!-- Required. The Features released and the customers who get them. -->

## Release strategy

<!-- Required. How release is decoupled from deployment, the audience, and the order of exposure. -->

## Readiness evidence

<!-- Required. Acceptance, NFR verification, security and compliance evidence, with links. -->

## Rollout and rollback

<!-- Required. Steps, checkpoints, the rollback trigger and its tested procedure. -->

## Operations readiness

<!-- Optional: omit the section when empty. Monitoring, alerts, service level objectives, runbooks, support. -->

## Communication and enablement

<!-- Optional: omit the section when empty. Release notes, documentation, training, customer messaging. -->

## Measure

<!-- Optional: omit the section when empty. The outcomes to observe after release to evaluate each Feature's benefit hypothesis. -->

## Risks

<!-- Optional: omit the section when empty. What could go wrong and who decides to stop. -->
