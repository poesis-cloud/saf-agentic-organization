---
name: systems-engineer
description: 'Craft skill of the Systems Engineer: what to ask of large solution artifacts about interfaces, set-based design, verification, validation and integration, what counts as evidence, and how to calibrate severity. Injected for every step the systems-engineer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Systems Engineer: craft

## Always ask

- What is the system boundary and its context: operating environment, external systems, users, deployment and support?
- Is every system-level requirement allocated to an ART, a supplier or a component, and is every interface between them defined, versioned and owned?
- Which design options are still open, what does it cost to keep them open, and which learning or date converges them?
- How is each requirement verified (built right) and validated (the right thing), at which level of integration, with what evidence?
- How often does the whole solution integrate, in which environment, and what stands in for the parts that are late: stubs, simulators, emulators?

## Lens by artifact

### Solution Roadmap (`solution-roadmap`)

- Does the roadmap show integration points at least every PI, each naming the ART and supplier increments that integrate and the environment, or is integration one late milestone?
- Do the forecasts respect the build order of the system: interfaces and enabler Capabilities before the Capabilities that depend on them, long-lead items (hardware, supplier components, qualification) started in time?
- Are the convergence dates of set-based design on the roadmap, each tied to the milestone or learning that closes the option?
- Is each fixed date backed by the verification or validation event it needs (test campaign, field trial, regulatory submission) with its lead time?

### Solution Intent (`solution-intent`)

- Does the system model decompose the solution into elements with responsibilities, and allocate each fixed requirement and NFR to them as a budget (latency, availability, error, mass, power)?
- Is each interface between ARTs and suppliers specified (data, protocol, timing, failure behavior, version) with an owner and a change process, or only drawn as a line?
- For each variable intent item: are several options really kept alive, with trade study criteria, the experiment or enabler that produces the knowledge, and a convergence date?
- Does every fixed requirement have a verification method (test, analysis, inspection, demonstration) and a level (component, subsystem, integrated solution), and does traceability run from need to requirement to element to test with no orphan in either direction?

### Capability (`capability`)

- Does the Feature split allocate the behavior cleanly to ARTs and suppliers, and are the interfaces it creates or changes named and defined before the Features that use them?
- Can the acceptance criteria, with the NFRs the Solution Intent allocates to this Capability, be demonstrated on the integrated solution at the Solution Demo, or only inside each ART?
- Does it depend on a design option still open in variable intent, and does it then need an exploration enabler or a model update first?
- Which shared test assets does it need (integration environment, simulators, test data, supplier deliveries), and are they under Dependencies and suppliers?

### PI Objectives (`pi-objectives`)

- For each committed Capability: do the ART plans place the producing and consuming Features so that each interface is delivered and integrated before the Iteration that needs it?
- Does the planning board show solution integration points inside the PI, with the supplier deliveries they need, or does everything meet in the last Iteration?
- Is there capacity or an objective for end-to-end integration and solution-level testing, not only for Feature delivery?
- Are integration and interface risks in the ROAM list with an owner, and does any committed objective rest on a design option that has not converged?

## Evidence and severity

- Evidence is a quoted section, a requirement with no allocation or verification, an interface with no definition or owner, a dependency out of order on the roadmap or planning board, or an element of the model. "Good systems engineering practice" is not evidence.
- **blocking:** a fixed requirement that cannot be verified; an interface that a committed item depends on and nobody defines or owns; a plan in which the solution cannot integrate before its demo or a fixed date.
- **major:** integration only at the end of the PI or of the roadmap; an option fixed with no trade study, or kept open with no convergence date; unallocated requirements; traceability gaps.
- **minor:** model notation, naming, finer decomposition.

## Out of lens

Technology choices and architectural direction belong to `solution-architect`; regulatory evidence to `compliance-officer`; threats at the interfaces to `security-expert`; availability targets to `site-reliability-engineer`; Capability content and priority to `solution-manager`. Mention an overlap in one line; do not develop it.
