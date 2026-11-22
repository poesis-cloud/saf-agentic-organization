---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Challenge packet title>"
target: "<path of the challenged artifact>"   # The main artifact challenged
targetKind: "<artifact-kind>"   # Artifact kind of the target
challenger: "<agent-slug>"   # Agent slug of the expert
verdict: "pass"   # pass | concerns | blocking | not-applicable
findings: []   # Findings, most severe first
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Summary

<!-- Required. Two or three sentences: what you checked through your lens and your verdict. If not applicable, say why in one sentence. -->

## Findings

<!-- Optional: omit the section when empty. One short paragraph per finding id when the frontmatter line is not enough. Omit when there is no finding. -->

## Questions for the human gate

<!-- Optional: omit the section when empty. Only what a human must decide (a trade-off, a risk appetite). Omit when there is none. -->
