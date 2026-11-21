---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Code change title>"
owner: "software-engineer"   # Agent slug of the author
challengeLedger: []   # The owner's answers to the expert challenge (see the definition)
story: "<path of the story>"   # The Story implemented
repository: "<repository>"   # The code repository changed
branch: "<branch>"   # The branch that holds the change
pullRequest: null   # Pull request link, or null
status: "in-progress"   # in-progress | ready-for-review | changes-requested | approved | merged
testsPassing: false   # True when the automated tests of the change pass
transitions: []   # State history
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Summary

<!-- Required. What changed and why, in a few lines a reviewer can check against the diff. -->

## Design notes

<!-- Optional: omit the section when empty. The approach, the alternatives dropped, and any deviation from an architecture decision. -->

## Tests

<!-- Required. The tests written first and the behaviors they pin down; how to run them; the result. -->

## Definition of Done

<!-- Required. Each item of the team's Definition of Done, checked or explained. -->

## How to verify

<!-- Optional: omit the section when empty. The steps for a human to see the acceptance criteria met. -->

## Risks and rollback

<!-- Optional: omit the section when empty. What could break and how to undo the change. -->
