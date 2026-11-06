# Agentic AI Standards
## Domain README: Document Index and Navigation Guide

**Domain Owner:** Data Program Management Lead
**Platform:** Agent runtimes, identity providers, and model providers (vendor neutral)
**Version:** 1.0 | **Last Updated:** 2026-11
**Classification:** Internal, Program Reference
**Review Cycle:** Annual, plus a dated landscape check before each workshop

> **Purpose:** This domain defines how an organization stands up a governed agent: one identity per agent, a written charter that states its bounds and names the control that enforces each one, a registry row, and a review step that is independent of the builder. It reuses the risk tiers and boundary contracts from the AI-First Strategy Addendum (`AI_FIRST_STRATEGY_ADDENDUM.md`) and adds what that document does not cover: agent identity, charters, assessor agents, open-weight models, and agent runtimes. A lean track keeps it usable by teams of one to ten.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 01 | `01_Agentic_Best_Practices.md` | 1.0 | Active | Everyone building or approving agents |
| 02 | `02_Agentic_Program_Establishment.md` | 1.0 | Active | Program leads, executive directors, CAIO |
| 03 | `03_Agentic_Standards.md` | 1.0 | Active | Agent owners, engineers, reviewers |
| 04 | `04_Agentic_Auditing_Guide.md` | 1.0 | Active | Reviewers, risk and audit, assessor authors |
| 05 | `05_Agentic_Config_Change_Management.md` | 1.0 | Active | Agent owners, IT, change management |
| 06 | `06_Agentic_KPIs_and_Benchmarking.md` | 1.0 | Active | Program leads, CAIO |
| | `AGENT_INCIDENT_RESPONSE_ADDENDUM.md` | 1.0 | Active | Incident commanders, agent owners |
| | `LANDSCAPE_SNAPSHOT.md` | 1.0 | Active, dated | Facilitators, program leads |
| | `SOURCES.md` | 1.0 | Active, dated | Anyone checking a claim |

### Templates and examples

| File | Purpose |
|---|---|
| `templates/SOUL.template.md` | Charter template: frontmatter fields and the eleven required sections |
| `templates/registry.schema.yaml` | Schema and commented example for one registry row |
| `templates/assessors/charter_conformance_assessor.md` | Assessor charter that checks sampled work against the target's own charter |
| `templates/assessors/boundary_assessor.md` | Assessor charter that checks sampled work against the three boundary contracts |
| `examples/donor_acknowledgment_agent/SOUL.md` | Worked T3 charter, with its registry row `registry_row.yaml` |
| `examples/donor_acknowledgment_agent/assessor_run.md` | Worked assessor run on five sample outputs, with the escalation record |

### Workshop kit

| File | Purpose |
|---|---|
| `workshop/CHECKLIST_ONE_PAGE.md` | Ten questions to answer before an agent touches client data, and ten things teams usually miss |
| `workshop/EXERCISE_BUILD_AN_AGENT_CHARTER.md` | Timed hands-on exercise, with a no-tooling lean path |
| `workshop/FACILITATOR_NOTES.md` | Timing for two formats, failure modes, and the morning-of fact check |

The agent linter, `tools/agent_lint.py`, checks a charter against its registry row. The library linter, `tools/library_lint.py`, checks the index, references, prose rules, and header fields for this folder.

---

## Quick Navigation

| You need to... | Start here |
|---|---|
| Understand why a charter is not a control | `01_Agentic_Best_Practices.md` |
| Stand up the first agent on a small team | `02_Agentic_Program_Establishment.md` (lean track), then `templates/SOUL.template.md` |
| Check what is required of an agent | `03_Agentic_Standards.md` (each standard names its enforcement layer) |
| Set up independent review of agent work | `04_Agentic_Auditing_Guide.md`, then `templates/assessors/boundary_assessor.md` |
| Change a model, a tool, or a charter safely | `05_Agentic_Config_Change_Management.md` |
| Respond to an agent that misbehaved | `AGENT_INCIDENT_RESPONSE_ADDENDUM.md` |
| Check a date, version, or licence claim | `LANDSCAPE_SNAPSHOT.md`, then `SOURCES.md` |
| Run the workshop exercise | `workshop/EXERCISE_BUILD_AN_AGENT_CHARTER.md` |

## Key Design Conventions

| Convention | Rule |
|---|---|
| Charter is a prompt | A charter states the bounds. Each bound names the control outside the model that enforces it. |
| Mirror check | Write tools, data classes, and approval gates in the charter must match the registry row. The agent linter tests this. |
| Tiers | T1 to T4 from the addendum. The lean track covers T3 and T4. |
| Independent review | T1 to T3 are reviewed by someone other than the builder. An assessor agent triages and samples. It is never the sole gate for T1, T2, or any external write. |
| Volatile facts | Dates, versions, and licences live only in the Landscape Snapshot, each with a Sources row. |

## Audit Cadence

| Activity | Frequency | Led By |
|---|---|---|
| Charter and registry review | Monthly for lean track, quarterly for full track | Agent Owner |
| Assessor sampling | Per the sampling rule in the agent's charter | Assessor, with a named human reviewer |
| Kill switch drill | Per the Standards (03), by tier | Agent Owner |
| Landscape Snapshot check | Quarterly and before each workshop | Program lead |

## Cross-Domain Dependencies

| Related document | Relationship |
|---|---|
| `AI_FIRST_STRATEGY_ADDENDUM.md` | Source of tiers, boundary contracts, and stage gates this domain extends |
| `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | Notification and evidence procedures the agent incident addendum points to |
| `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` | Model provider and tool vendor due diligence |
| `03_data_governance_standards.md` | Data classification that agent data classes map to |
| `CROSS_DOMAIN_RACI.md` | Agent incident and agent owner rows |

---

*Maintained by: Data Program Management | Last reviewed: 2026-11*
