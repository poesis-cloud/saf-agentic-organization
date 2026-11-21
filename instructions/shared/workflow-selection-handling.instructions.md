---
description: 'Orchestrator duty: map the human's concern to one workflow and start it on assent.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Selecting a workflow

1. **Listen.** The human states a concern in their own words. They never have to name a workflow or a ceremony.
2. **Map** it to exactly one workflow of your catalog, by purpose. If two fit, ask one question. If the concern is another layer's grain, say which orchestrator to talk to and stop.
3. **Propose.** Name the workflow, the artifact that will reach the gate and the subject (the scope folder and item slug). Start nothing before the human agrees.
4. **Start.** Ask the harness `resolve-step` for that workflow. It continues the latest unfinished run of the workflow, or opens a new one.
5. **One session, one run.** When the run ends, name the workflow that comes next and ask the human to start a new session for it. Asked to "drive to done", answer with the plan of runs and start only the first.
