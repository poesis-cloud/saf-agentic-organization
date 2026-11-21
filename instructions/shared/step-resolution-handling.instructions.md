---
description: 'Orchestrator duty: dispatch each step the harness resolves, exactly once, with the subject and nothing else.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Dispatching a resolved step

For each `step-resolution` the harness returns:

1. Ask `resolve-step-model`.
2. Dispatch **one** worker: the agent is the step's `actor` (yourself included, when the step is yours), the model is the resolved profile.
3. The prompt holds two things and nothing else:
   - the step, verbatim: workflow slug, step slug, artifact kind, description;
   - **Subject:** the human's concern in their words; the workspace paths of this run (the scope folder, the main artifact once `draft` delivered it, the packet paths for `revise`); the human's decision or concerns from a previous gate.
4. Add no advice on content and pre-digest nothing: the harness injects the actor's instructions and skill.
5. When the worker returns, ask `resolve-step` again. Never dispatch a step twice on your own, never skip or reorder one.
6. During the run, tell the human one line per step at most.
