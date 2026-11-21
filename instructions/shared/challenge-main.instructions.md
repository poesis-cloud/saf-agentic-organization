---
description: 'Pattern of a challenge step: one expert writes one packet of findings on the drafted main artifact.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Challenge the main artifact

You sit on the expert panel. Find what would make the human regret accepting this artifact, through **your lens only**.

- **Target.** The artifact the `draft` step of this run delivered; the subject gives its path. Read it fully, then only the sources your lens needs.
- **Packet.** Write one packet at the brief's challenge path, from `templates/shared/challenge.artifact-template.md`. Set `target` to the exact workspace path of the target, `targetKind` to its kind and `challenger` to your agent slug.
- **Lens.** Use the section of your skill for this artifact, plus the questions under `## Challenge` in the brief.
- **Findings.** Each one is a claim, the evidence (where in the artifact or source it shows) and the smallest ask that would resolve it. Severity: `blocking` (accepting as is would cause harm, break a law or a commitment, or rest on something infeasible or untestable), `major` (materially weakens the artifact), `minor` (worth improving). Seven findings at most, most severe first; no style remarks.
- **Verdict.** `pass` (no finding), `concerns`, `blocking` (at least one blocking finding), or `not-applicable`: your lens does not apply, said in one sentence. Before answering not-applicable, check that the artifact is right to assume so.
- **Never write owner content.** Do not edit the target, do not draft its replacement text: ask for the change.
- **Rerun.** If your packet exists, update it in place: drop the findings the owner resolved, keep those that stand.
- **Outcome:** `written` or `revised`; the note gives the verdict and the number of findings.
