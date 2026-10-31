---
name: product-manager
description: '**WORKFLOW SKILL** — Poesis product management: systematic feature capture, backlog governance, opportunity identification, and GitHub Project synchronization across all Poesis products. USE FOR: reasoning about product strategy, feature decomposition, backlog coherence, market positioning, business opportunity identification, cross-product dependency analysis, SAFe taxonomy alignment, feature prioritization, roadmap planning, and GitHub Project sync operations. DO NOT USE FOR: GSM ontology semantics (use gsm-knowledge skill); ontology sourcing into OIP (use oip-ontology-sourcing skill); runtime deployment or CI/CD. REFERENCES: def/features/ artifacts, def/features/github_project_sync/, strategy/poesis-strategy.md.'
---

# Product Manager Skill

Systematic product management for the **Poesis** product portfolio. Load this skill when reasoning about features, backlog, prioritization, market opportunities, roadmap planning, or GitHub Project synchronization.

## Poesis Product Portfolio

Poesis is a **systemic governance platform** with two business lines (open theory + commercial product) and multiple products at different maturity stages.

### Product Map

| Product | Type | Phase | Owner Repo | Feature Models |
|---------|------|-------|------------|----------------|
| **GSM** | Theory / Publication | Publication planning (Q2 2026) | `gsm/` | None (theory) |
| **SIE** | AI Context Platform (engine) | Design + early MVP | `sie/` | ✅ Extensive (def/features/) |
| **OIP** | Domain App (Organizational Intelligence) | Design-time | `oip/` | ❌ None yet |
| **GSM Sourcer** | Sourcing Pipeline | Design documentation | `gsm-sourcer/` | ❌ None yet |

### SIE Sub-Components (infrastructure)

| Component | Type | Phase | Feature Models |
|-----------|------|-------|----------------|
| SIE Definition Manager | Java microservice | Active MVP dev | Partial (GSM schema) |
| SIE Definition Database | PostgreSQL (Helm) | Scaffolding | None |
| SIE Definition Graph Database | Neo4j projection | Design-time | None |
| SIE Event Bus | Kafka (Helm) | Scaffolding | None |
| SIE Schema Registry | Schema Registry (Helm) | Scaffolding | None |

### Business Lines (from strategy/poesis-strategy.md)

**Line 1 — GSM Model (Open)**
- Academic paper → web content → book
- Business model: citation authority → consulting market (Beer/VSM pattern)
- Timeline: Q2 2026 (paper) → Q4 2026 (book)

**Line 2 — GSM Framework (Commercial)**
- SIE platform + OIP domain app + framework mappings + certification
- Business model: SaaS product + consulting + certification (SAFe pattern)
- Timeline: ongoing (product) → 2027 (certification)

## Product Architecture (Systemic)

```
┌─────────────────────────────────────────────────┐
│                   POESIS                        │
│                                                 │
│  ┌──────────┐   ┌──────────┐   ┌────────────┐  │
│  │   GSM    │   │   SIE    │   │   OIP      │  │
│  │ (theory) │──▶│ (engine) │◀──│ (IT app)   │  │
│  └──────────┘   └────┬─────┘   └────────────┘  │
│                      │                          │
│               ┌──────┴──────┐                   │
│               │ GSM Sourcer │                   │
│               │ (pipeline)  │                   │
│               └─────────────┘                   │
│                                                 │
│  Future domain apps follow OIP pattern:         │
│  Finance Intelligence, Healthcare Intelligence  │
└─────────────────────────────────────────────────┘
```

**SIE** is the engine (hosts GSM, enforces governance, provides analytics).
**OIP** is the first domain application (translates GSM into IT vocabulary).
**GSM Sourcer** ingests external artifacts into GSM definitions.
**GSM** is the theoretical foundation (open, published).
**Future domain apps** follow the OIP pattern for other verticals.

## SAFe Taxonomy (Poesis-aligned)

The backlog uses a SAFe-aligned taxonomy mapped to systemics:

| SAFe Level | Poesis Mapping | Scope |
|------------|---------------|-------|
| **Portfolio Epic** | Control/governance objective | Cross-product, outcome-oriented |
| **Capability** | Controller sub-mechanism / sensor mechanism | Solution-level, multi-feature |
| **Feature** | Definable deliverable / bounded engine behavior | Program-level, shippable |
| **Story** | (Design-time: out of scope; runtime: concrete task) | Sprint-level |
| **Enabler** | Runway work (architecture, infra, compliance) | Can enable Epic/Capability |

### Systemics Coherence Rule for Backlog Items

A backlog item is only *operationally valuable* if it:
1. Results in a **Definition-plane deliverable**
2. Can be **realized through Remediation** into State
3. Can then be **re-observed** (closing the governance loop)

### Current Epic Structure

**Business Epics (analytics maturity → Gartner model)**:
- **E-1**: Descriptive Analytics — "What is / was?" (observation, measurement, reporting)
- **E-2**: Diagnostic Analytics — "Why?" (root cause, anomaly, pattern)
- **E-3**: Predictive Analytics — "What will happen?" (forecasting, risk, simulation)
- **E-4**: Prescriptive Analytics — "What should we do?" (synthesis, remediation, AI)
- **E-5**: Cross-Cutting Intelligence & Assurance (views, provenance, safety)

**Enabler Epics (runway)**:
- **EN-1**: Evidence, Trace, Provenance runway
- **EN-2**: Constraint runtime + formal validation runway
- **EN-3**: Safe automation runway
- **EN-4**: Environmental Context & System Presets runway

### IMPORTANT: Current Coverage Gap

The existing feature models are **SIE-analytics-dominated**. They capture *what the engine observes/analyzes/decides* but do NOT cover:

- **OIP application features** (what the IT domain app delivers to users)
- **GSM Sourcer pipeline features** (ingestion, extraction, verification)
- **GSM publication features** (paper, web, book production pipeline)
- **Platform/infrastructure features** (SIE Definition Manager API, event contracts, schema lifecycle)
- **Cross-product integration features** (SIE↔OIP, SIE↔Sourcer, Sourcer↔OIP)
- **Commercial features** (multi-tenancy, billing, onboarding, marketplace)

## Feature Capture Methodology

### When to create feature models

1. **New product identified** → Create product Epic(s) in backlog
2. **New capability identified** → Decompose into Features, map to parent Epic
3. **New user need / business opportunity** → Trace to Feature → Capability → Epic
4. **Cross-product dependency found** → Model as Enabler or `requires` link

### Feature Model Artifacts (under def/features/)

| Artifact | Purpose | Convention |
|----------|---------|------------|
| `*-safe-backlog.puml` | Epic → Capability → Feature hierarchy (SAFe view) | One per product or cross-product |
| `*-capabilities.puml` | Feature → Capability mapping | PD frame diagram |
| `*-features.puml` | Detailed feature packages with descriptions | PD frame diagram |
| `*-market-value.puml` | Priority buckets (P0–P3) | PD frame diagram |
| `*-feature-evaluation.puml` | Complexity + Feasibility tiers | PD frame diagram |
| `analytics-usecases/*.puml` | UC diagrams with SAFe mapping + feasibility notes | One per use case |
| `backlog/github-project-sync-config.json` | GitHub Project sync configuration | JSON |
| `backlog/backlog-export.json` | Exported backlog (auto-generated) | JSON |
| `backlog/github-project-sync-state.json` | Sync state (auto-generated) | JSON |
| `backlog/coherence-audit.md` | Coherence audit report (auto-generated) | Markdown |

### Feature Naming Conventions

- Epic IDs: `E-{n}` (business), `EN-{n}` (enabler)
- Capability IDs: `{epic-id}/{slug}` (e.g., `E-1/state-monitoring-audit`)
- Feature IDs: `{capability-id}/{slug}`
- UseCase IDs: `UC:{filename-stem}`

### PlantUML Conventions for Features

- Frame prefix: `PD - Poesis - {title} - v1`
- Stereotypes: `<<Epic>>`, `<<Capability>>`, `<<Feature>>`, `<<Story>>`, `<<Enabler>>`
- Combined stereotypes: `<<Capability, Enabler>>` for enabler capabilities
- Notes with `**Validation Rules:**` for constraints
- Notes with `**SAFe mapping:**` for UC → Epic/Capability/Feature tracing

## GitHub Project Synchronization

### Toolchain

Located at `def/features/github_project_sync/`:

| Tool | Purpose | Command |
|------|---------|---------|
| `export_backlog.py` | Parse PlantUML → JSON export | `python3 def/features/github_project_sync/export_backlog.py def/features/backlog/github-project-sync-config.json > def/features/backlog/backlog-export.json` |
| `sync_project.py` | Push/update GitHub Project v2 items | `python3 def/features/github_project_sync/sync_project.py def/features/backlog/backlog-export.json def/features/backlog/github-project-sync-config.json` |
| `audit_backlog.py` | Coherence audit of exported backlog | `python3 def/features/github_project_sync/audit_backlog.py --export def/features/backlog/backlog-export.json --out def/features/backlog/coherence-audit.md` |

**All commands run from the workspace root** (`poesis/`).

### GitHub Project Configuration

- **Org**: `<github-org>`
- **Project**: #2 — "Poesis Product Features"
- **Fields**: Status, Priority (P0–P3), Estimate, Item SAFe Type, Complexity
- **Auth**: `gh auth status` must show logged-in; scopes needed: `read:project`, `project`

### Sync Workflow (standard)

1. Edit PlantUML feature models
2. Export: `python3 def/features/github_project_sync/export_backlog.py ...`
3. Sync: `python3 def/features/github_project_sync/sync_project.py ...`
4. Audit: `python3 def/features/github_project_sync/audit_backlog.py ...`
5. Review coherence audit for gaps
6. Iterate

### Sync Semantics

- Items are matched by `localId` (from state file) or by title (fallback search)
- New items are created as Draft Issues with default status "Backlog"
- Existing items get updated: SAFe Type, Priority, Complexity, Effort, description
- **Status is never overwritten** for existing items (preserves workflow changes in GitHub)
- Status is **pulled back** from GitHub into state file after sync

## Product Opportunity Analysis Framework

When analyzing business opportunities for Poesis, evaluate along these dimensions:

### 1. Market Timing

- **Regulatory pressure** (GDPR, NIS2, DORA, AI Act → compliance automation demand)
- **Technical debt awareness** (industry shift toward systematic architecture governance)
- **AI/LLM adoption** (organizations seeking structured AI governance, not just chatbots)
- **Framework fatigue** (TOGAF, SAFe, ITIL → fragmented, no unifying theory)

### 2. Competitive Positioning

- **No direct competitor** combines: systemics theory + governance engine + domain apps + sourcing pipeline
- **Indirect competitors**: ServiceNow (CMDB), Backstage (developer portal), ArchiMate tools (architecture), GRC platforms (compliance)
- **Differentiation**: Poesis is *generative* (defines, then derives) vs competitors who are *descriptive* (observe, then report)

### 3. Value Chain Analysis

Map every feature to the value chain position:
- **Define** (GSM theory → SIE engine → domain vocabularies)
- **Source** (external artifacts → GSM definitions via Sourcer)
- **Govern** (DNA grammar → constraint enforcement → drift detection)
- **Observe** (evidence → analytics → dashboards)
- **Act** (remediation → homeostasis → closed-loop)

### 4. Customer Journey Stages

| Stage | Product | Key Feature |
|-------|---------|-------------|
| **Discover** | GSM (paper, web) | Conceptual authority, framework comparisons |
| **Evaluate** | SIE + OIP (free tier / demo) | Instant architecture discovery, conformance analysis |
| **Adopt** | SIE + OIP (paid) | Continuous dashboards, data lineage, LLM governance |
| **Expand** | Multi-domain apps, Sourcer | Regulatory sourcing, cross-domain governance |
| **Champion** | GSM Certification | Training, certification, consulting market |

### 5. Product-Led Growth Signals

Features that drive adoption virally:
- **Architecture Discovery** (instant value, shareable maps → social proof)
- **Conformance Dashboards** (replaces quarterly audits → visible ROI)
- **Regulatory Presets** (GDPR/NIS2/DORA → compliance in a box)
- **LLM Definition Authoring** (natural language → governance definitions → low barrier)

## Backlog Coherence Checks

When adding or modifying features, verify:

1. **Epic completeness**: Every Capability has a parent Epic
2. **Capability coverage**: Every Capability has at least one UseCase (functional grounding)
3. **Priority coverage**: Every Capability has a priorityBucket (P0–P3)
4. **Feasibility coverage**: Every Capability has complexity + feasibility tier
5. **Enabler tracing**: Business Epics `requires` Enabler Epics where runway is needed
6. **Cross-product tracing**: Features touching multiple products have explicit dependency links
7. **Plane placement**: Every feature maps to at least one governance plane (Definition/Description/Remediation)
8. **Systemics coherence**: Feature closes the governance loop (define → realize → observe)

## Proactive Opportunity Identification

When working with the business owner, proactively surface:

1. **Uncovered products**: Which products have no feature models? (currently: OIP, GSM Sourcer, platform infra)
2. **Missing customer journeys**: Which user personas lack end-to-end feature coverage?
3. **Enabler bottlenecks**: Which enablers block the most business features?
4. **Quick wins**: Features with HIGH value + LOW complexity + NOW feasibility
5. **Competitive moats**: Features that create switching costs or network effects
6. **Publication-product alignment**: How does GSM publication timeline align with product readiness?
7. **Framework sourcing opportunities**: Which regulatory/governance frameworks are in demand but not yet sourced?
8. **Cross-product synergies**: Where does integrating SIE+OIP+Sourcer create value > sum of parts?
