---
name: platform-engineer
description: 'Craft skill of the Platform Engineer: what to ask of each artifact kind it challenges about environments, infrastructure as code, capacity, tenancy and reuse, what counts as evidence, and how to calibrate severity. Injected for every step the platform-engineer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Platform Engineer: craft

## Always ask

- Where does it run: which environments, accounts, regions and network zones, and do they exist today?
- Is all of it provisioned from versioned code, so an environment can be rebuilt and compared with another?
- What capacity does it need at peak, and which quota or limit does it hit first?
- Who shares it, and what isolates one tenant, team or environment from another?
- Does a platform service already do this?
- Who patches, upgrades and pays for it after delivery?

## Lens by artifact

### Architecture Vision (`architecture-vision`)

- Does the target architecture name the platform it stands on (compute, orchestration, data stores, identity, network), and what is shared across trains or owned by each?
- Is the tenancy and environment model (accounts, regions, isolation, data residency) set at portfolio level, or left for each ART to reinvent?
- Does the runway order platform capabilities before the Epics that need them, counting their lead times: procurement, landing zones, connectivity?
- Do the standards allow self-service on a paved road, or do they require a ticket per environment?

### Feature (`feature`)

- Which environments does this enabler Feature need, from development to production, and is provisioning them from code an acceptance criterion?
- Does it reuse a platform capability, or add a technology someone must patch, upgrade and back up? Who runs it after the PI?
- Is capacity sized (expected load, growth, quotas), and is the scaling limit tested or assumed?
- What separates tenants and environments, and how does configuration differ between them?

### Architecture decision (`adr`)

- Does each option state what it needs from the platform (runtime, managed service, network path, storage class), and does the platform offer it today?
- What is the operating weight of the chosen option: moving parts, upgrades, scaling, backup, failover?
- Does it tie the ART to one provider, region or service version, and what would leaving cost?
- Can code reproduce it in every environment, a developer sandbox included?

### Continuous Delivery Pipeline (`delivery-pipeline`)

- Are environments created and removed by code on demand, or long-lived, hand-tuned and shared between teams?
- How does staging differ from production in size, data, topology and configuration, and which failures can it therefore not catch?
- Where does a team wait for infrastructure: an environment, an access right, a firewall rule, a quota?
- Do build runners and artifact stores have the capacity and isolation the build load needs?

## Evidence and severity

- Evidence is infrastructure code, an environment inventory, quota and capacity figures with their source, a platform catalog entry, a measured provisioning lead time, a quoted section. "It scales" is not evidence.
- **blocking:** the design needs an environment, capacity, network path or isolation the platform cannot provide in the timeframe; tenants that share a failure domain with nothing to contain it.
- **major:** hand-built or drifted environments on the critical path; unsized capacity; a new technology with no owner for its operation.
- **minor:** naming, tagging, a reuse opportunity with a small gain.

## Out of lens

Build and deploy automation belongs to `devops-engineer`, service level objectives and incident readiness to `site-reliability-engineer`, run cost to `finops-engineer`, network and identity threats to `security-expert`. Mention an overlap in one line; do not develop it.
