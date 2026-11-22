---
description: 'Orchestrator duty: react to a denied dispatch, a failed step or a refused request.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# When the harness says no

- **Dispatch denied (precondition failed).** Tell the human which state is missing and which workflow produces it. Do not work around it.
- **Step failed (delivery or postcondition).** Ask `resolve-step` again: the same step comes back. Dispatch it once more, with the failure messages added verbatim to the subject. After three failures of the same step, stop and give the human the messages.
- **`step-in-flight`, `session-instance-bound`, `workflow-instance-busy`.** Do not retry. A new session is needed; for a busy run, give the human the recovery command the message prints.
- **`REJECTED` request.** Correct the command as the message says and ask again.
- **Never** override a check, edit an artifact to make a check pass, or surface step detail to the human unless the run is stuck.
