---
slug: "<artifact-slug>"   # lowercase letters, digits and hyphens: the slug used in the file path
title: "<Team Kanban title>"
level: "team"   # portfolio | solution-train | art | team
scope: "<path of the scope folder>"   # The folder whose backlog is rendered
updated: "YYYY-MM-DD"   # YYYY-MM-DD of the last rendering
columns:
  - { state: backlog, wipLimit: null, items: [] }
  - { state: ready, wipLimit: null, items: [] }
  - { state: in-progress, wipLimit: null, items: [] }
  - { state: in-review, wipLimit: null, items: [] }
  - { state: accepted, wipLimit: null, items: [] }   # One entry per state, in flow order
stepOutcomes: []   # each step that commits this file appends { step: <workflow>/<step>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line> }
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Template: drop this line and the guidance comments in the artifact. -->

## Board

<!-- Required. One line per state: the state, its WIP limit, the item titles. Flag a state over its limit. -->

## Flow notes

<!-- Optional: omit the section when empty. Bottlenecks, blocked items and aged items, one line each. -->
