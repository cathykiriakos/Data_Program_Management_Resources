# Cross-Domain RACI
## Accountability Framework for Inter-Domain Data Program Operations

**Document Owner:** Chief Data Officer + Data Governance Office
**Classification:** Internal — Binding Standard
**Version:** 1.0 | **Last Updated:** 2026-03
**Review Cycle:** Semi-Annual or upon org change

> **Purpose:** This document defines accountability at the boundaries between data domains — the places where gaps are most likely to form and where conflicting assumptions about ownership cause the most damage. It covers all five program domains (Data Engineering, Data Governance, Business Intelligence, Machine Learning, Data Quality), all cross-cutting functions (IT, Legal/Privacy, Model Risk, Finance), and every major activity class from asset creation to incident response to regulatory compliance.

---

## Table of Contents

1. [How to Read This Document](#1-how-to-read-this-document)
2. [Roles Reference](#2-roles-reference)
3. [RACI: Data Product Lifecycle](#3-raci-data-product-lifecycle)
4. [RACI: Data Quality and Incident Management](#4-raci-data-quality-and-incident-management)
5. [RACI: Access Control and Security](#5-raci-access-control-and-security)
6. [RACI: Platform and Infrastructure Change](#6-raci-platform-and-infrastructure-change)
7. [RACI: Audit and Compliance](#7-raci-audit-and-compliance)
8. [RACI: Machine Learning Governance](#8-raci-machine-learning-governance)
9. [RACI: Business Intelligence Governance](#9-raci-business-intelligence-governance)
10. [RACI: Metadata and Catalog Management](#10-raci-metadata-and-catalog-management)
11. [Scenario-Based Decision Trees](#11-scenario-based-decision-trees)
12. [Escalation Paths](#12-escalation-paths)
13. [Conflict Resolution](#13-conflict-resolution)
14. [RACI Review and Maintenance](#14-raci-review-and-maintenance)

---

## 1. How to Read This Document

### 1.1 RACI Definitions

| Letter | Role | Obligation |
|---|---|---|
| **R** | **Responsible** | Does the work. At least one R must exist for every activity. Multiple R allowed. |
| **A** | **Accountable** | Ultimately answerable for the outcome. Signs off. Exactly one A per activity. |
| **C** | **Consulted** | Must be consulted before the work proceeds. Two-way dialogue. |
| **I** | **Informed** | Receives notification after the fact. One-way communication. |
| **—** | **Not involved** | No role in this activity. |

### 1.2 Anti-Patterns This Document Is Designed to Prevent

| Anti-Pattern | Risk | How This Document Addresses It |
|---|---|---|
| Two teams both assume they own something | Duplicate, conflicting work | Exactly one A per row — no shared accountability |
| No team owns something | Work falls through the gap | Every row has at least one A |
| "The data team" is used as a catch-all | No individual accountability | Roles are function-specific, not team-level |
| Accountability assigned to a committee | No one actually accountable | Committees may be C or I; A is always an individual role |
| IT owns governance, not the business | Compliance theater | Business domain ownership is explicit throughout |

### 1.3 Governing Principles

1. **Accountability is singular.** Only one role carries A. If two parties want A, the CDO arbitrates.
2. **Responsibility can be shared.** Multiple R is normal for collaborative work.
3. **Consultation is binding.** A C obligation means the work cannot proceed without that party's input.
4. **Informed is not optional.** Teams marked I must receive notifications even if they have no action.
5. **RACI follows the tier.** T1 assets have more C and A requirements than T3. Where tier affects who is consulted or accountable, it is noted in the cell.

---

## 2. Roles Reference

### 2.1 Primary Program Roles

| Role ID | Role Name | Description | Typical Individual |
|---|---|---|---|
| **CDO** | Chief Data Officer | Executive program sponsor; final escalation owner; regulatory accountability | Chief Data Officer |
| **DGO** | Data Governance Office | Policy ownership; Collibra platform; 2LOD oversight; stewardship program management | DGO Program Manager / Data Governance Lead |
| **DE-L** | Data Engineering Lead | Platform engineering; pipeline standards; IaC ownership; DE team leadership | Data Engineering Lead |
| **DE** | Data Engineering Team | Pipeline development; source onboarding; platform operations | Data Engineers, Analytics Engineers, Platform Engineers |
| **BI-COE** | BI Center of Excellence Lead | BI platform governance; certified content; self-service program | BI COE Lead |
| **BI** | BI Domain Teams | Domain-specific report development; embedded domain analytics | Domain BI Leads, BI Developers |
| **ML-L** | ML Engineering Lead | MLOps platform; model registry; ML governance; T1 model oversight | ML Engineering Lead / ML COE Lead |
| **ML** | ML Engineering Team | Model development; feature engineering; deployment; monitoring | ML Engineers, Data Scientists |
| **DO** | Data Owner | Business-accountable individual for a specific data domain or product | Finance Controller, Sales VP, etc. |
| **DS** | Data Steward | Operational quality, access certification, metadata management for a domain | Analytics Lead, Senior Analyst |

### 2.2 Cross-Cutting Function Roles

| Role ID | Role Name | Description |
|---|---|---|
| **IT** | IT / Infrastructure | Cloud infra; network security; ITSM; change management; audit logging |
| **CISO** | CISO / InfoSec | Security policy; breach response; access control oversight; pen testing |
| **PRIV** | Privacy Officer | PII governance; GDPR/CCPA/HIPAA compliance; data subject rights |
| **LEGAL** | Legal | Regulatory notification decisions; contract review; regulatory submissions |
| **MR** | Model Risk | Independent T1 model validation; regulatory model risk oversight |
| **AUDIT** | Internal Audit | Third line of defense; annual program audits; control testing |
| **CAB** | Change Advisory Board | Change approval body for Major and above changes |
| **GC** | Governance Council | Monthly executive forum; policy arbitration; cross-domain escalation |

### 2.3 Role Hierarchy for Escalation

```
Tier 1 — Operational (same business day)
  Data Steward → Data Owner → Domain Lead

Tier 2 — Program (next business day)
  Domain Lead → DGO Lead → CDO

Tier 3 — Executive (same day for P1/P2 incidents)
  CDO → GC → Board / Regulatory Authority (if applicable)

Special escalation paths:
  PII incident         → Privacy Officer (parallel, not sequential)
  Security breach      → CISO (parallel, not sequential)
  T1 model incident   → Model Risk (parallel, not sequential)
  Regulatory matter    → Legal (parallel, not sequential)
```

---

## 3. RACI: Data Product Lifecycle

### 3.1 Asset Creation and Registration

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Identify need for new data asset | I | C | C | C | C | C | C | C | **A** | R | — |
| Initiate formal data product request | — | **A** | C | C | C | C | C | C | R | R | — |
| Assess source system availability | — | I | **A** | R | — | — | — | — | C | C | C |
| Data Impact Assessment (new source) | — | **A** | R | R | C | C | C | C | C | C | C |
| Assign data owner and steward | **A** | R | — | — | — | — | — | — | — | — | — |
| Register asset in Collibra catalog | — | **A** | C | R | — | — | — | — | I | I | — |
| Apply initial data classification | — | **A** | R | R | — | — | — | — | C | C | — |
| Define business glossary terms | — | **A** | — | — | — | — | — | — | C | R | — |

### 3.2 Bronze Layer (Ingestion)

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ingestion pipeline design | — | C | **A** | R | — | — | — | — | I | I | C |
| Source schema documentation | — | I | **A** | R | — | — | — | — | C | C | — |
| PII identification at source | — | **A** | C | R | — | — | — | — | C | R | — |
| Bronze DQ rules definition | — | **A** | C | R | — | — | — | — | C | C | — |
| Audit column standards enforcement | — | C | **A** | R | — | — | — | — | — | — | — |
| Ingestion SLA agreement with source | — | C | **A** | R | — | — | — | — | R | C | C |
| Bronze-to-Silver promotion gate | — | C | **A** | R | — | — | — | — | — | I | — |

### 3.3 Silver Layer (Cleansing and Conforming)

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Silver transformation design | — | C | **A** | R | — | — | C | C | I | I | — |
| PII masking policy implementation | — | **A** | C | R | — | — | — | — | — | C | — |
| DGO PII review sign-off | — | **A** | I | I | — | — | — | — | C | C | — |
| SCD2 / deduplication logic | — | C | **A** | R | — | — | — | — | I | I | — |
| Referential integrity test definition | — | C | **A** | R | — | — | — | — | C | C | — |
| Silver DQ 7-day pass streak validation | — | **A** | R | R | — | — | — | — | I | I | — |
| Data custodian sign-off | — | C | — | **A** | — | — | — | — | I | I | — |

### 3.4 Gold Layer (Business-Ready / Certification)

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Gold model / fact-dim design | — | C | **A** | R | C | C | C | C | C | C | — |
| Business rule implementation | — | C | C | R | C | C | C | C | **A** | R | — |
| Semantic metric definition | — | C | C | R | C | C | C | C | **A** | R | — |
| Duplicate metric detection scan | — | **A** | C | R | C | — | C | — | C | C | — |
| Gold DQ rules registration | — | **A** | C | R | — | — | — | — | C | R | — |
| Data contract authoring | — | C | — | **A** | C | C | C | C | C | C | — |
| Data contract consumer sign-off (BI) | — | C | — | I | **A** | R | — | — | C | C | — |
| Data contract consumer sign-off (ML) | — | C | — | I | — | — | **A** | R | C | C | — |
| T1 certification — DGO validation | — | **A** | C | C | C | — | C | — | C | C | — |
| T1 certification — domain owner sign-off | — | C | — | — | — | — | — | — | **A** | R | — |
| T1 certification — CDO sign-off | **A** | R | — | — | — | — | — | — | C | C | — |
| T2 certification — steward sign-off | — | C | — | — | — | — | — | — | C | **A** | — |
| Certification register update | — | **A** | — | R | — | — | — | — | — | — | — |
| Certified date and review date set | — | **A** | — | R | — | — | — | — | I | I | — |

### 3.5 Semantic Layer

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dbt metric definition | — | C | C | **A** | C | — | C | — | C | R | — |
| Metric linked to Collibra glossary term | — | **A** | — | R | — | — | — | — | C | R | — |
| Metric approved by domain owner | — | C | — | — | — | — | — | — | **A** | R | — |
| Semantic model published to BI tools | — | I | C | **A** | R | — | — | — | I | I | — |
| Semantic model published to ML feature store | — | I | C | **A** | — | — | R | — | I | I | — |
| Breaking change to metric (T1) | C | **A** | C | R | R | R | R | R | R | R | — |
| Metric deprecation | — | **A** | C | R | R | — | R | — | C | R | — |

### 3.6 Decertification and Deprecation

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Identify zero-usage / deprecation candidate | — | **A** | R | R | R | R | R | R | — | — | — |
| Notify owner and steward | — | **A** | — | — | — | — | — | — | R | R | — |
| Owner confirms deprecation decision | — | C | — | — | — | — | — | — | **A** | R | — |
| Consumer deprecation notice (30 days) | — | **A** | R | R | R | R | R | R | C | C | — |
| Access revocation on decommission date | — | **A** | — | R | — | — | — | — | I | I | R |
| Physical data retention and archival | — | C | **A** | R | — | — | — | — | C | I | C |
| Collibra status → DEPRECATED / ARCHIVED | — | **A** | — | R | — | — | — | — | I | I | — |

---

## 4. RACI: Data Quality and Incident Management

### 4.1 DQ Rule Lifecycle

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DQ rule identification and definition | — | **A** | C | R | C | C | C | C | C | R | — |
| DQ rule YAML authoring | — | C | C | **A** | — | — | — | — | — | R | — |
| DQ rule registration in Collibra DQ | — | **A** | — | R | — | — | — | — | I | I | — |
| DQ gate implementation in CI/CD | — | C | **A** | R | — | — | — | — | — | — | — |
| DQ threshold change (tighten) | — | **A** | C | R | C | C | C | C | C | C | — |
| DQ threshold change (loosen) | C | **A** | C | R | C | C | C | C | R | R | — |
| DQ rule retirement | — | **A** | C | R | — | — | — | — | C | R | — |
| DQ score published to Collibra | — | **A** | — | R | — | — | — | — | I | I | — |

### 4.2 DQ Failure Response

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CRITICAL DQ failure — first alert | — | I | **A** | R | I | I | I | I | I | I | — |
| Pipeline suspension decision | — | C | **A** | R | — | — | — | — | I | I | — |
| Downstream consumer notification | — | **A** | R | R | R | R | R | R | C | C | — |
| Root cause investigation | — | C | **A** | R | C | — | C | — | — | C | — |
| Fix implementation and testing | — | C | **A** | R | — | — | — | — | — | — | — |
| DGO incident log entry | — | **A** | I | I | I | I | I | I | I | I | — |
| Domain owner final sign-off to re-promote | — | C | C | — | — | — | — | — | **A** | R | — |
| Post-incident DQ rule strengthening | — | **A** | C | R | — | — | — | — | C | C | — |

### 4.3 Incident Classification and Response (All Types)

*See `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` for full response procedures. This table defines the RACI for who activates and owns each incident type.*

| Incident Type | Incident Commander | First Responder | DGO Role | Domain Owner Role | Escalation Threshold |
|---|---|---|---|---|---|
| **INC-DQ** — Pipeline DQ failure | DE-L | DE on-call | Notified; logs incident | Notified; signs off on re-promote | > 4hr blocking Gold → CDO |
| **INC-PII** — PII exposure | CDO | DE on-call | **Opens formal incident; owns 2LOD** | Notified immediately | Immediate — all PII incidents |
| **INC-ACC** — Unauthorized access | CISO | IT | Owns access review | Notified | Immediate — all access incidents |
| **INC-OUT** — Platform/SLA outage | DE-L | DE on-call | Notified | Notified (T1 SLA breach) | T1 outage > 2hr → CDO |
| **INC-ML** — Model failure | ML-L | ML on-call | Tracks; escalates to Model Risk | Notified | T1 model → Model Risk same day |
| **INC-BI** — Report / data error | BI-COE | Domain BI Lead | Reviews if certified content | Signs off on re-certification | T1 report wrong → CDO within 4hr |
| **INC-SCH** — Schema breaking change | DE-L | DE on-call | Mediates contract process | Notified | Consumers not notified → DGO arbitrates |
| **INC-SEC** — Security breach | CISO | IT / InfoSec | Opens formal incident | Notified | Immediate — parallel CDO + Legal |

### 4.4 Cross-System Reconciliation Failures

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Reconciliation discrepancy detected | — | I | **A** | R | I | I | I | I | I | I | — |
| Source system investigation | — | C | **A** | R | — | — | — | — | C | C | C |
| Business impact assessment | — | C | C | C | C | C | C | C | **A** | R | — |
| Decision: hold / publish with caveat / suppress | — | C | C | — | C | — | C | — | **A** | R | — |
| Consumer communication of known discrepancy | — | **A** | R | R | R | R | R | R | C | C | — |
| Reconciliation query registration in DQ registry | — | **A** | C | R | — | — | — | — | C | C | — |

---

## 5. RACI: Access Control and Security

### 5.1 Access Provisioning

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| New user access request (standard role) | — | I | — | — | — | — | — | — | — | **A** | R |
| New user access request (Restricted data) | — | **A** | — | — | — | — | — | — | R | R | R |
| New user access request (T1 ML feature data) | — | C | — | — | — | — | **A** | R | C | C | R |
| Data Usage Agreement (DUA) execution | — | **A** | — | — | — | — | — | — | R | R | C |
| RBAC role creation or modification | — | **A** | C | R | C | — | C | — | C | C | **R** |
| Column masking policy creation | — | **A** | C | R | — | — | — | — | — | C | — |
| Row-level security policy creation | — | **A** | C | R | R | R | C | — | C | C | — |
| Service account creation | — | C | **A** | R | — | — | — | — | — | — | R |
| Emergency (break-glass) access | — | **A** | C | R | — | — | — | — | C | C | R |
| Temporary access grant (> 30 days) | — | **A** | C | R | — | — | — | — | C | C | R |
| External / guest access provisioning | C | **A** | C | R | — | — | — | — | R | R | R |

### 5.2 Access Certification

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Access certification report generation | — | **A** | — | R | — | — | — | — | — | — | R |
| Certification review — finance domain assets | — | C | — | — | — | — | — | — | C | **A** | — |
| Certification review — BI certified datasets | — | C | — | — | **A** | R | — | — | C | C | — |
| Certification review — ML feature tables | — | C | — | — | — | — | **A** | R | C | C | — |
| Certification review — platform / infra roles | — | C | **A** | R | — | — | — | — | — | — | C |
| Revoke access on certification failure | — | **A** | C | R | C | C | C | C | C | C | R |
| Escalate uncertified access (> 10 business days) | — | **A** | I | I | I | I | I | I | I | I | I |
| Report certification completion rate to CDO | — | **A** | — | — | — | — | — | — | — | — | — |

### 5.3 Classification Changes

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Request to reclassify an asset (up) | — | **A** | C | R | C | C | C | C | R | R | — |
| Request to reclassify an asset (down) | C | **A** | C | R | C | C | C | C | R | R | — |
| Classification schema change | **A** | R | C | C | C | C | C | C | C | C | C |
| Privacy review on classification change | — | **A** | — | — | — | — | — | — | C | C | — |
| Platform tag update after classification change | — | C | **A** | R | — | — | — | — | — | — | — |
| Collibra catalog update | — | **A** | — | R | — | — | — | — | I | I | — |
| Consumer notification of classification change | — | **A** | R | R | R | R | R | R | C | C | — |

### 5.4 Security Events and Breach Response

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Security anomaly detected | I | I | I | — | — | — | — | — | — | — | **A** |
| Incident declared | C | R | C | — | — | — | — | — | — | — | **A** |
| Evidence preservation | — | C | C | R | — | — | — | — | — | — | **A** |
| Scope assessment — data affected | — | **A** | R | R | R | R | R | R | C | C | R |
| Containment decision | C | R | C | — | — | — | — | — | — | — | **A** |
| Regulatory notification assessment | **A** | C | — | — | — | — | — | — | — | — | — |
| Legal notification | — | C | — | — | — | — | — | — | — | — | — |
| Regulatory authority notification (if required) | **A** | R | — | — | — | — | — | — | — | — | C |
| Post-breach access review | — | **A** | C | R | C | C | C | C | C | C | R |
| Preventive control implementation | — | C | C | R | C | C | C | C | — | — | **A** |

---

## 6. RACI: Platform and Infrastructure Change

### 6.1 Change Initiation and Classification

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT | CAB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Change request submission | — | — | — | R | R | R | R | R | — | — | — | — |
| Change tier classification | — | C | **A** | R | C | C | C | C | — | — | C | — |
| Data Impact Assessment authoring | — | C | **A** | R | C | C | C | C | C | C | C | — |
| Change ticket approval — Standard | — | — | **A** | R | — | — | — | — | — | — | — | — |
| Change ticket approval — Minor | — | C | **A** | R | C | C | C | C | — | — | C | — |
| Change ticket approval — Major | C | R | R | R | R | R | R | R | R | R | R | **A** |
| Emergency / Hotfix authorization | — | I | **A** | R | — | — | — | — | — | — | C | — |
| Retrospective ticket (post-hotfix) | — | I | **A** | R | — | — | — | — | — | — | C | — |

### 6.2 Source System Onboarding

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Source system onboarding request | — | C | C | — | — | — | — | — | **A** | R | — |
| Technical feasibility assessment | — | C | **A** | R | — | — | — | — | I | I | C |
| PII and classification pre-scan | — | **A** | C | R | — | — | — | — | C | C | — |
| Data Impact Assessment | — | **A** | R | R | C | C | C | C | C | C | C |
| Ingestion pipeline build | — | I | **A** | R | — | — | — | — | — | — | — |
| Source schema documentation | — | C | **A** | R | — | — | — | — | C | C | — |
| Bronze certification gate | — | **A** | C | R | — | — | — | — | I | I | — |
| Source owner SLA agreement | — | C | **A** | R | — | — | — | — | R | C | C |

### 6.3 Snowflake Platform Changes

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| New Snowflake account / environment | I | C | **A** | R | C | — | C | — | — | — | R |
| New database or schema | — | C | **A** | R | C | — | C | — | — | — | C |
| Warehouse creation or resize | — | — | **A** | R | C | — | C | — | — | — | C |
| RBAC role restructure | — | **A** | C | R | C | — | C | — | C | C | R |
| Dynamic masking policy change | — | **A** | C | R | — | — | — | — | C | C | — |
| Row access policy change | — | **A** | C | R | C | — | C | — | C | C | — |
| Data share creation (external) | C | **A** | C | R | — | — | — | — | R | R | C |
| Time Travel / Fail-safe configuration | — | C | **A** | R | — | — | — | — | I | I | — |
| Network policy change | — | C | C | R | — | — | — | — | — | — | **A** |
| Resource monitor configuration | — | — | **A** | R | C | — | C | — | — | — | C |

### 6.4 Databricks / Unity Catalog Changes

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| New Unity Catalog catalog | — | C | **A** | R | C | — | C | — | — | — | C |
| New schema within catalog | — | C | **A** | R | C | — | C | — | — | — | — |
| Cluster policy change | — | — | **A** | R | — | — | C | — | — | — | C |
| Unity Catalog RBAC change | — | **A** | C | R | C | — | C | — | C | C | R |
| Column mask creation (Unity Catalog) | — | **A** | C | R | — | — | — | — | C | C | — |
| Row filter policy change | — | **A** | C | R | C | — | C | — | C | C | — |
| Delta Sharing endpoint creation | C | **A** | C | R | — | — | — | — | R | R | C |
| ML cluster / pool change | — | — | C | C | — | — | **A** | R | — | — | C |
| Workspace access model change | — | C | C | R | C | — | C | — | — | — | **A** |
| Databricks version / runtime upgrade | — | I | **A** | R | C | — | C | C | — | — | C |

### 6.5 IaC and CI/CD Changes

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Terraform module change (non-breaking) | — | — | **A** | R | — | — | — | — | — | — | C |
| Terraform state migration | — | — | **A** | R | — | — | — | — | — | — | R |
| New GitHub Actions workflow | — | — | **A** | R | C | — | C | — | — | — | C |
| Secret / credential rotation | — | — | C | R | R | R | R | R | — | — | **A** |
| Pre-commit hook update | — | — | **A** | R | — | — | — | — | — | — | — |
| CI/CD environment variable change | — | — | **A** | R | C | — | C | — | — | — | C |
| Infrastructure drift detected | — | I | **A** | R | — | — | — | — | — | — | C |

---

## 7. RACI: Audit and Compliance

### 7.1 First Line of Defense (1LOD) — Self-Attestation

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DE monthly self-assessment execution | — | C | **A** | R | — | — | — | — | — | — | — |
| BI monthly self-assessment execution | — | C | — | — | **A** | R | — | — | — | — | — |
| ML monthly self-assessment execution | — | C | — | — | — | — | **A** | R | — | — | — |
| Domain DQ score attestation | — | C | — | — | — | — | — | — | **A** | R | — |
| Self-assessment results submitted to DGO | — | **A** | R | — | R | — | R | — | R | — | — |
| Gap remediation planning (1LOD finding) | — | C | **A** | R | **A** | R | **A** | R | C | C | — |
| Gap remediation evidence submission | — | **A** | R | R | R | R | R | R | — | — | — |

### 7.2 Second Line of Defense (2LOD) — Independent Review

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT | AUDIT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2LOD audit schedule publication | C | **A** | I | I | I | I | I | I | I | I | I | C |
| Evidence package preparation (auditee) | — | I | R | R | R | R | R | R | R | R | R | — |
| Audit fieldwork execution | — | **A** | C | C | C | C | C | C | C | C | C | C |
| Preliminary findings review | — | **A** | C | — | C | — | C | — | C | — | C | C |
| Audit report issuance | C | **A** | I | I | I | I | I | I | I | I | I | I |
| Remediation planning (2LOD finding) | — | C | R | R | R | R | R | R | **A** | R | R | — |
| Remediation evidence submission | — | **A** | R | R | R | R | R | R | R | R | R | — |
| Remediation sign-off | — | **A** | I | I | I | I | I | I | I | I | I | C |
| CDO presentation of audit results | **A** | R | — | — | — | — | — | — | — | — | — | — |

### 7.3 Third Line of Defense (3LOD) — Internal and External Audit

| Activity | CDO | DGO | DE-L | BI-COE | ML-L | DO | IT | LEGAL | AUDIT |
|---|---|---|---|---|---|---|---|---|---|
| Annual audit scope setting | C | C | C | C | C | C | C | C | **A** |
| Audit access provisioning | — | C | C | C | C | — | **A** | — | R |
| PBC (Provided by Client) list response | — | **A** | R | R | R | R | R | — | R |
| Control walkthrough facilitation | — | **A** | C | C | C | C | C | — | R |
| Regulatory examination response | **A** | R | C | C | C | C | C | R | C |
| Audit finding — management response authoring | **A** | R | C | C | C | C | C | C | — |
| Finding remediation implementation | — | C | **A** | **A** | **A** | C | R | — | — |
| Remediation evidence submission to auditors | — | **A** | R | R | R | R | R | — | — |

### 7.4 Regulatory Compliance Activities

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | PRIV | LEGAL | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GDPR data mapping update | — | **A** | C | R | C | C | C | C | R | C | — |
| HIPAA BAA execution (new vendor) | C | C | — | — | — | — | — | — | C | **A** | — |
| PCI DSS scope change assessment | C | C | C | R | C | C | — | — | C | C | **A** |
| Data subject access request (DSAR) response | — | **A** | C | R | C | — | — | C | R | C | — |
| Right to erasure implementation | — | **A** | C | R | C | — | — | C | R | C | — |
| Annual privacy impact assessment | — | R | C | C | C | C | C | C | **A** | C | — |
| SOX data control attestation | C | C | C | R | C | C | — | **A** | — | C | C |
| Regulatory breach notification decision | **A** | C | — | — | — | — | — | — | C | R | — |
| Regulatory notification submission | — | R | — | — | — | — | — | — | R | **A** | — |

---

## 8. RACI: Machine Learning Governance

### 8.1 Feature Engineering and Feature Store

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|
| Feature definition and specification | — | C | C | C | — | **A** | R | C | C | — |
| Feature lineage documentation | — | **A** | C | R | — | C | R | I | I | — |
| PII in training data review | — | **A** | C | R | — | C | C | C | R | — |
| Feature data contract sign-off (DE as producer) | — | C | — | **A** | — | R | R | C | C | — |
| Feature data contract sign-off (ML as consumer) | — | C | — | I | — | **A** | R | C | C | — |
| Feature store registration | — | I | C | C | — | **A** | R | I | I | — |
| Feature freshness SLA agreement | — | C | **A** | R | — | C | C | I | I | — |

### 8.2 Model Development

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | DS | MR | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Experiment tracking setup | — | — | — | — | — | **A** | R | — | — | — | — |
| Model card authoring | — | C | — | — | — | **A** | R | C | C | C | — |
| Bias and fairness audit | — | C | — | — | — | C | R | — | — | **A** | — |
| Validation data set certification | — | **A** | C | R | — | C | C | C | C | — | — |
| Model performance gate definition | — | C | — | — | — | **A** | R | C | C | C | — |
| T1 model — independent validation | — | C | — | — | — | C | C | C | — | **A** | — |
| T1 model — model card final sign-off | C | C | — | — | — | **A** | R | R | C | R | — |

### 8.3 Model Promotion and Production Deployment

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | MR | IT | CAB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T3 model → production | — | — | — | — | — | **A** | R | — | — | — | — |
| T2 model → production | — | C | — | — | — | **A** | R | R | — | — | — |
| T1 model → production — ML Lead sign-off | — | C | — | — | — | **A** | R | R | C | — | — |
| T1 model → production — Model Risk sign-off | — | C | — | — | — | C | C | C | **A** | — | — |
| T1 model → production — CDO sign-off | **A** | R | — | — | — | R | — | R | R | — | — |
| T1 model → production — CAB approval | — | R | C | — | — | R | — | R | R | C | **A** |
| Model registry update | — | I | — | — | — | **A** | R | I | I | — | — |
| Rollback execution | — | I | C | C | — | **A** | R | I | I | — | — |
| Post-deployment monitoring activation | — | I | — | — | — | **A** | R | I | — | — | — |

### 8.4 Model Monitoring and Incident Response

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | MR | IT |
|---|---|---|---|---|---|---|---|---|---|---|
| Performance degradation alert — first response | — | I | — | — | — | **A** | R | I | I | — |
| Drift detection — investigation | — | C | C | C | — | **A** | R | C | C | — |
| T1 model incident — Model Risk notification | I | R | — | — | — | R | — | — | **A** | — |
| T1 model suspension decision | C | C | — | — | — | **A** | R | R | R | — |
| T1 model — emergency rollback decision | C | C | — | — | — | **A** | R | R | R | — |
| Root cause analysis | — | C | C | C | — | **A** | R | C | C | — |
| Retraining decision | — | C | — | — | — | **A** | R | R | R | — |
| T1 post-incident review | C | R | — | — | — | **A** | R | R | **A** | — |
| Model Risk Committee notification (T1 recurring) | **A** | R | — | — | — | R | — | R | R | — |

### 8.5 Model Retirement

| Activity | CDO | DGO | DE-L | DE | BI-COE | ML-L | ML | DO | MR | IT |
|---|---|---|---|---|---|---|---|---|---|---|
| Retirement recommendation | — | C | — | — | — | **A** | R | R | R | — |
| T1 model retirement — Model Risk sign-off | — | C | — | — | — | C | — | C | **A** | — |
| T1 model retirement — CDO sign-off | **A** | R | — | — | — | R | — | R | R | — |
| Consumer notification of model retirement | — | **A** | — | — | — | R | R | R | — | — |
| Feature store clean-up | — | C | C | R | — | **A** | R | — | — | — |
| Model registry status → RETIRED | — | I | — | — | — | **A** | R | I | I | — |

---

## 9. RACI: Business Intelligence Governance

### 9.1 Certified Dataset Program

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Certified dataset proposal | — | C | C | C | **A** | R | — | — | C | C | — |
| Data source approval (Gold / semantic only) | — | **A** | C | R | C | — | — | — | C | C | — |
| RLS design review | — | **A** | C | R | R | — | — | — | C | C | — |
| Column inclusion / data minimization review | — | **A** | C | R | R | — | — | — | C | C | — |
| RLS persona testing | — | C | — | — | **A** | R | — | — | C | C | — |
| Domain owner data accuracy sign-off | — | C | — | — | — | — | — | — | **A** | R | — |
| BI COE certification badge application | — | C | — | — | **A** | R | — | — | I | I | — |
| Certified dataset registered in Report Registry | — | C | — | — | **A** | R | — | — | I | I | — |
| Review cadence set (6-month / 12-month) | — | **A** | — | — | R | — | — | — | C | C | — |

### 9.2 Report Governance

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 report development | — | C | — | — | **A** | R | — | — | C | C | — |
| T2 report development | — | C | — | — | C | **A** | — | — | C | C | — |
| T3 report (self-service) | — | — | — | — | — | **A** | — | — | — | — | — |
| Report promotion T3 → T2 | — | C | — | — | C | **A** | — | — | C | C | — |
| Report promotion T2 → T1 | — | C | — | — | **A** | R | — | — | R | R | — |
| Report Registry entry creation | — | — | — | — | **A** | R | — | — | I | I | — |
| T3 stale report archival (90-day) | — | — | — | — | **A** | I | — | — | I | I | — |
| T1 report content error — takedown decision | — | **A** | — | — | R | R | — | — | R | R | — |
| T1 report re-publish after error fix | — | C | — | — | **A** | R | — | — | R | R | — |

### 9.3 BI Platform and Tool Governance

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BI tool version upgrade | C | C | — | — | **A** | R | — | — | I | I | R |
| New BI tool evaluation and approval | **A** | C | C | — | R | R | C | — | C | — | C |
| Workspace structure change | — | C | — | — | **A** | R | — | — | I | I | R |
| Sensitivity label policy (Power BI / Tableau) | — | **A** | — | — | R | — | — | — | C | C | R |
| External sharing policy | C | **A** | — | — | R | — | — | — | C | C | R |
| BI admin role provisioning | — | C | — | — | **A** | — | — | — | — | — | R |
| BI cost and license review | — | — | — | — | **A** | R | — | — | — | — | C |
| CI/CD for BI deployments | — | — | C | — | **A** | R | — | — | — | — | C |

### 9.4 Metric Conflict Resolution

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS |
|---|---|---|---|---|---|---|---|---|---|---|
| Conflicting metric detected | — | R | C | C | **A** | R | C | C | C | C |
| Competing definitions documented | — | **A** | — | — | R | R | — | — | C | C |
| Domain stakeholder consultation | — | **A** | — | — | R | R | — | — | R | R |
| Governance Council arbitration required? | C | **A** | — | — | R | — | — | — | R | — |
| Governing definition established | — | **A** | — | R | R | — | — | — | R | R |
| Collibra glossary term updated | — | **A** | — | R | — | — | — | — | C | R |
| Non-governing metric deprecated | — | **A** | — | R | R | R | — | — | C | C |
| Consumer communications issued | — | **A** | — | — | R | R | R | R | C | C |

---

## 10. RACI: Metadata and Catalog Management

### 10.1 Collibra Catalog Operations

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Collibra platform administration | — | **A** | — | — | — | — | — | — | — | — | R |
| Collibra connector configuration (Snowflake / Databricks) | — | **A** | C | R | — | — | — | — | — | — | C |
| New domain onboarding to catalog | — | **A** | R | R | R | R | R | R | C | C | — |
| Asset auto-discovery scan | — | **A** | C | R | — | — | — | — | — | — | — |
| Catalog asset review and cleanup | — | **A** | C | C | C | C | C | C | C | R | — |
| Collibra workflow modification | — | **A** | C | — | C | — | C | — | C | C | — |
| Collibra user and role management | — | **A** | — | — | — | — | — | — | — | — | R |
| Collibra version upgrade | — | **A** | C | — | C | — | C | — | — | — | R |

### 10.2 Business Glossary

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS |
|---|---|---|---|---|---|---|---|---|---|---|
| New glossary term proposal | — | C | C | C | C | C | C | C | **A** | R |
| Term definition review and approval | — | **A** | — | — | C | — | — | — | C | R |
| Cross-domain term conflict resolution | C | **A** | — | — | C | — | — | — | R | R |
| Term deprecation | — | **A** | — | — | C | — | — | — | C | R |
| Glossary linked to platform column | — | **A** | C | R | C | — | C | — | C | R |
| Annual glossary review | — | **A** | C | — | C | — | C | — | R | R |

### 10.3 Lineage Management

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dbt lineage sync to Collibra | — | **A** | C | R | — | — | — | — | — | — | — |
| Snowflake access-history lineage extraction | — | **A** | C | R | — | — | — | — | — | — | — |
| Databricks OpenLineage emission | — | C | C | R | — | — | **A** | R | — | — | — |
| BI report lineage documentation | — | C | — | — | **A** | R | — | — | C | C | — |
| ML feature-to-model lineage documentation | — | C | — | — | — | — | **A** | R | I | I | — |
| Lineage gap investigation | — | **A** | R | R | R | R | R | R | C | C | — |
| Lineage completeness report (weekly) | — | **A** | I | I | I | I | I | I | I | I | — |
| Annual lineage attestation (T1 assets) | — | **A** | R | R | R | R | R | R | C | R | — |

### 10.4 Retention and Lifecycle

| Activity | CDO | DGO | DE-L | DE | BI-COE | BI | ML-L | ML | DO | DS | IT | LEGAL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Retention policy definition by classification | C | **A** | C | — | — | — | — | — | — | — | — | C |
| Retention policy implementation (platform) | — | C | **A** | R | — | — | R | — | — | — | C | — |
| Legal hold invocation | — | C | C | R | — | — | — | — | — | — | C | **A** |
| Legal hold release | — | C | C | R | — | — | — | — | — | — | C | **A** |
| Secure deletion execution | — | **A** | C | R | — | — | R | — | — | — | C | C |
| Deletion evidence and certificate | — | **A** | C | R | — | — | R | — | — | — | C | I |
| Annual retention schedule review | — | **A** | C | — | — | — | — | — | — | — | — | C |

---

## 11. Scenario-Based Decision Trees

These decision trees address the most common cross-domain situations where teams are unsure who owns an activity or decision. Use these before escalating.

---

### 11.1 "Who owns this DQ failure?"

```
A DQ failure has been detected.
          │
          ▼
Where was the failure detected?

  BRONZE LAYER ──────────────────────────────────────────────────────────────
  │  Owner: DE (Data Custodian — R/A)
  │  DGO: Notified (I)
  │  Action: DE investigates source, fixes ingestion or raises source incident
  └──────────────────────────────────────────────────────────────────────────

  SILVER LAYER ──────────────────────────────────────────────────────────────
  │  Owner: DE (Data Custodian — R/A)
  │  DGO: Consulted if PII-related
  │  Action: DE investigates transformation logic; DGO if PII masking failure
  └──────────────────────────────────────────────────────────────────────────

  GOLD LAYER / CERTIFIED ASSET
          │
          ▼
    Is the DQ rule a CRITICAL severity rule?
         YES                        NO
          │                          │
          ▼                          ▼
    Pipeline suspended?         DE Lead owns fix.
         YES                    DGO notified.
          │                     Domain Owner informed.
          ▼
    Notify downstream consumers immediately.
    Owner: DE Lead (R/A) — must fix within 2 hours (T1) / 4 hours (T2)
    DGO: Opens incident log. Tracks resolution.
    Domain Owner: Must sign off before re-promotion to T1.
          │
          ▼
    Is this a RECURRING failure (3rd time in 90 days)?
         YES
          │
          ▼
    DGO escalates to CDO.
    Governance Council agenda item required within 30 days.
    Domain Owner: Accountable for structural fix.

  SEMANTIC LAYER
          │
          ▼
    Which team produced the broken metric?
      DE (dbt model)         → DE Lead owns fix; BI-COE and ML-L notified
      BI (dataset metric)    → BI-COE owns fix; DE notified; DGO if T1
      ML (feature definition) → ML-L owns fix; DE notified

  BI REPORT / DASHBOARD
          │
          ▼
    Is the report T1 certified?
         YES                        NO
          │                          │
          ▼                          ▼
    Take report offline.        Domain BI Lead owns fix.
    BI-COE Lead: A              No DGO involvement unless
    Domain Owner: must          data is Restricted class.
    sign off before
    re-publish.
    DGO: Tracks if certified.
```

---

### 11.2 "Who approves this access request?"

```
An access request has been received.
          │
          ▼
What data classification is the requested asset?

  PUBLIC or INTERNAL
          │
          ▼
    Standard role exists for this domain?
         YES → Data Steward approves (A). IT provisions (R).
         NO  → DE Lead creates role first (minor change ticket). Then Steward approves.

  CONFIDENTIAL
          │
          ▼
    Is the requestor from the owning domain?
         YES → Data Steward approves (A). IT provisions (R).
         NO  → Domain Owner reviews and approves (A). DGO is Consulted. IT provisions (R).

  RESTRICTED
          │
          ▼
    Is there a signed Data Usage Agreement on file?
         NO  → DGO issues DUA. Requestor must sign before access is provisioned.
         YES (and current) →
              │
              ▼
          Is the requestor's manager approved for Restricted access?
               NO  → Escalate to Domain Owner. Domain Owner decides (A).
               YES → Domain Owner approves (A). DGO is Consulted. IT provisions (R).

  T1 ML FEATURE DATA (regardless of classification)
          │
          ▼
    ML Lead reviews access need (A).
    DGO consulted if adding non-ML team member.
    IT provisions (R).
    Logged in Collibra.

  EXTERNAL / GUEST USER
          │
          ▼
    CDO approval required (A) regardless of classification.
    DGO consulted (C). Legal consulted if contractual data.
    Privacy Officer consulted if Restricted data involved.
    IT provisions (R). Logged with expiry date.
```

---

### 11.3 "Who owns a schema breaking change?"

```
A schema change is proposed that will break downstream consumers.
          │
          ▼
Who is proposing the change?

  DATA ENGINEERING (upstream table change)
          │
          ▼
    DE Lead: Responsible for notifying all downstream consumers.
    Notification must go to: BI-COE, ML-L, and all registered data contract signatories.
    Minimum notice periods:
      T1 asset: 14 days before change is deployed
      T2 asset:  7 days before change is deployed
      T3 asset:  3 days before change is deployed
          │
          ▼
    Do all downstream contract signatories acknowledge?
         YES → Proceed with change. Minor or Major change ticket depending on scope.
         NO  →
              │
              ▼
          DGO mediates (A). 
          Governance Council arbitration if unresolved in 5 business days.
          CDO makes final call if Governance Council cannot resolve.

  BUSINESS INTELLIGENCE (semantic layer / certified dataset change)
          │
          ▼
    BI-COE Lead: Responsible for notifying ML and all report consumers.
    Same notice periods apply.
    DGO consulted for T1 metric changes.

  MACHINE LEARNING (feature schema change)
          │
          ▼
    ML Lead: Responsible for notifying DE (if feature derived from Gold tables).
    DE Lead: Responsible for notifying ML if the Gold table is being changed.
    If feature breaking change affects a T1 model: Model Risk notified same day.
```

---

### 11.4 "Who decides whether to publish data with a known quality issue?"

```
A Gold asset has a known quality issue. 
Business is requesting publication anyway.
          │
          ▼
What is the severity of the quality issue?

  CRITICAL DQ rule failing
          │
          ▼
    Publication is BLOCKED. No exception process exists for CRITICAL DQ on T1/T2 assets.
    DE Lead (A): must fix before publication.
    Domain Owner: accountable for the delay. 
    If business impact is severe: CDO may authorize a time-limited exception.
      → CDO authorization must be documented in Collibra incident log.
      → Exception cannot exceed 48 hours.
      → DGO must monitor and close the exception.

  HIGH DQ rule failing
          │
          ▼
    Domain Owner (A): decides whether to publish with known caveat.
    DGO (C): must be consulted; documents decision in incident log.
    Consumer notification required: all downstream consumers must be notified of the
    known issue before they consume the data.
    Issue must be resolved within 4 hours (T1) / 8 hours (T2) regardless of publication.

  MEDIUM / LOW DQ rule failing
          │
          ▼
    Domain Steward (A): decides whether to publish.
    DGO (I): notified.
    Issue logged and tracked.
    Resolution within 2 business days (MEDIUM) / 5 business days (LOW).
```

---

### 11.5 "Who owns a cross-domain metric conflict?"

```
Two business units or teams are using different definitions for the same metric.
          │
          ▼
Are both definitions used in T1 certified assets?
         YES → Governance Council arbitration required immediately.
               CDO sets resolution timeline (A). DGO facilitates (R).
               Neither definition may be changed unilaterally during arbitration.
         NO  →
              │
              ▼
          Is one definition T1 and the other T2 or below?
               YES → T1 definition is governing by default.
                     T2/T3 consumer must align to T1 definition.
                     DGO updates Collibra glossary (A).
                     Non-governing metric deprecated with 30-day notice.
               NO  →
                    │
                    ▼
               Is there an agreed Collibra glossary term for this metric?
                    YES → Collibra definition governs.
                          Non-aligned team must align within 60 days.
                          DGO (A): tracks alignment.
                    NO  →
                         │
                         ▼
                    DGO convenes a cross-domain definition workshop (A).
                    Domain Owners from both domains are required attendees.
                    Governing definition must be agreed and published within 30 days.
                    Escalates to Governance Council if unresolved at day 30.
```

---

### 11.6 "Who decides to shut down a T1 ML model?"

```
A T1 model is exhibiting a problem. 
Should it be shut down / suspended?
          │
          ▼
What type of problem?

  PERFORMANCE DEGRADATION (drift, accuracy drop)
          │
          ▼
    Is the model currently serving regulated decisions (credit, hiring, clinical)?
         YES → Model Risk immediately escalated (parallel to below).
               Suspension decision: ML Lead (A) + Domain Owner (A) + Model Risk (C).
               CDO informed. GC on agenda within 5 days.
         NO  →
              │
              ▼
          Has performance breached the T1 performance gate (2 consecutive months)?
               YES → Model Risk Committee notification required (see ML KPI doc).
                     Suspension decision: ML Lead (A) + Domain Owner (A).
                     CDO informed same day.
               NO  →
                    │
                    ▼
               ML Lead owns investigation (A). Retraining decision within 30 days.

  DATA QUALITY FAILURE IN FEATURES
          │
          ▼
    Feature freshness SLA breached?
      YES → DE Lead (A): fix feature pipeline immediately.
            ML Lead (A): suspend model if feature staleness exceeds model SLA.
            Domain Owner (A): business impact decision.
    Feature correctness failure?
      → Same as CRITICAL DQ rule failing — see Section 11.4.

  SECURITY / PII EXPOSURE IN TRAINING DATA
          │
          ▼
    Immediate suspension: ML Lead (A). No exceptions.
    DGO opens formal incident (A).
    CDO notified immediately.
    Privacy Officer notified immediately.
    Do NOT redeploy until DGO and Privacy Officer sign off.
```

---

### 11.7 "Who owns onboarding a new source system?"

```
A new source system needs to be connected.
          │
          ▼
Who made the request?
  Business domain (DO / DS) → Formal request via Collibra intake workflow.
  Engineering (DE)          → DE Lead assesses and submits for DGO review.
  ML team                   → ML Lead requests via DE.
          │
          ▼
DGO conducts PII and classification pre-scan (A).
DE Lead conducts technical feasibility (A).
          │
          ▼
Does the source contain Restricted data (PII, PHI, PCI)?
         YES → Privacy Officer review required (C).
               Legal review required if regulated (C).
               CISO review required for network/connection (C).
               Data Impact Assessment mandatory (DGO — A).
         NO  →
              Data Impact Assessment required (DGO — A).
              CISO review if new network connection required.
          │
          ▼
Minor change ticket raised. DE Lead approves (A).
IT approves if new network connection (A).
          │
          ▼
DE builds ingestion pipeline (R). Bronze certification gate runs.
DGO confirms Bronze minimum standards met (A) before Silver build begins.
Domain Owner (A): confirms business accuracy before Gold certification.
```

---

## 12. Escalation Paths

### 12.1 Standard Escalation Chain

| Situation | Level 1 (same day) | Level 2 (next business day) | Level 3 (CDO) | Level 4 (GC / Board) |
|---|---|---|---|---|
| DQ failure — pipeline blocked | DE on-call → DE Lead | DE Lead → DGO | T1 asset not resolved > 4hr | T1 recurring (3rd in 90 days) |
| PII exposure | DE on-call → Privacy Officer | CDO + Legal | Immediate escalation | Regulatory notification decision |
| Unauthorized data access | IT/CISO | CISO → CDO | Immediate for Restricted | Legal if external breach |
| T1 SLA breach | DE on-call | DE Lead → DGO | > 2hr unresolved | — |
| T1 ML model failure | ML on-call → ML Lead | ML Lead → Model Risk | > 4hr unresolved | MRC notification (regulatory) |
| T1 BI report wrong data | Domain BI Lead → BI COE | BI COE → Data Owner | T1 report taken offline | — |
| Cross-domain metric conflict | BI COE | DGO mediates | GC arbitration at 5 days | CDO decision if GC cannot resolve |
| Schema breaking change dispute | Contract parties | DGO mediates | — | GC at 5 days |
| Owner departed — no replacement | Steward as temporary | DGO + HR | Escalate at day 14 | — |
| Audit finding not remediated | Domain team | DGO tracks | CDO escalation at deadline | External audit if critical |

### 12.2 Regulatory Escalation Triggers

| Event | Escalation Path | Timeline | Regulation |
|---|---|---|---|
| PII breach — EU data subjects affected | DGO → Privacy Officer → Legal → CDO → Supervisory Authority | 72 hours from discovery | GDPR Article 33 |
| PII breach — CA data subjects affected | DGO → Privacy Officer → Legal → CDO → AG (if > 500 CA residents) | 45 days | CCPA/CPRA |
| PHI breach | DGO → Privacy Officer → Legal → CDO → HHS | 60 days (< 500 affected); annual report (< 500) | HIPAA Breach Notification Rule |
| PCI DSS cardholder data compromise | CISO → Legal → CDO → Card Brand / Acquirer | Immediately | PCI DSS Req 12.10 |
| SOX material weakness identified | Internal Audit → CFO → CDO → External Auditor / Audit Committee | Per SOX reporting timeline | SOX Section 302/404 |

### 12.3 Escalation SLAs

| Tier | Acknowledge | Contain | Resolve | Post-Incident Review |
|---|---|---|---|---|
| P1 — Critical | 15 minutes | 1 hour | 4 hours | Mandatory; within 5 business days |
| P2 — High | 30 minutes | 2 hours | 8 hours | Mandatory for regulatory; within 10 days |
| P3 — Medium | 2 hours | 8 hours | 2 business days | Recommended; within 30 days |
| P4 — Low | 1 business day | 5 business days | 5 business days | Optional |

---

## 13. Conflict Resolution

### 13.1 When Conflicts Arise

Cross-domain conflicts most commonly arise in these scenarios:

| Conflict Type | Most Likely Between | Resolution Owner | Forum |
|---|---|---|---|
| Metric definition disagreement | BI vs. Finance DO | DGO mediates; GC arbitrates | Governance Council |
| Schema change blocking downstream | DE vs. BI or ML | DGO mediates via data contract | Contract + DGO |
| Access denied vs. business urgency | CISO/DGO vs. Domain team | CDO makes final call | CDO review |
| DQ threshold too strict / too loose | DE vs. Domain Owner | Domain Owner decides; DGO records | DGO log |
| Two teams claim ownership of same asset | Any two domains | CDO arbitrates | CDO + DGO |
| BI self-service vs. governed access | BI vs. DGO | BI COE Lead + DGO alignment | Working session |
| Model feature uses data without contract | ML vs. DE | Data contract process; DGO mediates | Contract + DGO |
| Certification tier assignment dispute | Domain vs. DGO | CDO decides | CDO review |

### 13.2 Resolution Process

```
Step 1 — Direct Resolution (1–2 business days)
  Parties attempt direct resolution.
  If resolved: document outcome in Collibra task. Done.
  If not resolved: proceed to Step 2.

Step 2 — DGO Mediation (3–5 business days)
  DGO Program Manager facilitates a structured mediation session.
  Both parties present their position.
  DGO recommends a resolution in writing.
  If both parties accept: implement; document in Collibra. Done.
  If not resolved: proceed to Step 3.

Step 3 — Governance Council Arbitration (next scheduled GC meeting, max 30 days)
  DGO presents the conflict and recommendation to the Governance Council.
  Domain Owners from both sides attend and present (5 minutes each).
  Governance Council votes.
  Decision is binding and documented in GC minutes.
  If conflict involves a T1 asset or regulatory implication: CDO may override.
  If not resolved: proceed to Step 4.

Step 4 — CDO Decision (final)
  CDO reviews GC recommendation and conflict history.
  CDO decision is final.
  Decision documented in CDO decision log.
  RACI updated if conflict arose from an ambiguity in this document.
```

### 13.3 RACI Amendment Process

If an activity is not covered by this document, or if a conflict has revealed an ambiguity, the RACI must be updated.

| Trigger | Who Initiates | Approval | Update Cadence |
|---|---|---|---|
| New activity identified (gap) | Any team lead | DGO reviews; CDO approves for A-level changes | Within 30 days of identification |
| Conflict revealed ambiguity | DGO | CDO approves | Post-resolution; within 30 days |
| Org change (new team, restructure) | CDO | CDO | Within 30 days of org change effective date |
| Platform change (new tool, new domain) | Domain lead | DGO reviews; CDO approves | Before go-live of new capability |
| Scheduled review | DGO | CDO | Semi-annual |

---

## 14. RACI Review and Maintenance

### 14.1 Review Schedule

| Review | Frequency | Owner | Participants | Output |
|---|---|---|---|---|
| Scheduled review | Semi-annual | DGO | All domain leads + CDO | Updated RACI; version increment if changed |
| Triggered review | As needed (org change, conflict, new platform) | DGO | Affected parties | Targeted update; change log entry |
| Annual full audit | Annual | DGO + Internal Audit | All parties | Audit attestation that RACI is current and operating as designed |

### 14.2 Change Log

| Version | Date | Changed By | Summary of Changes |
|---|---|---|---|
| 1.0 | 2026-03 | DGO | Initial release — covers all five domains, cross-cutting functions, scenario trees |

### 14.3 How to Raise a RACI Question or Amendment

If you believe:
- An activity in this document assigns accountability incorrectly
- An important cross-domain activity is missing
- A scenario tree does not address your situation

**Raise a Collibra workflow task** of type `RACI Amendment Request` and assign it to the DGO Program Manager. Include:
1. The specific activity or scenario at issue
2. The current RACI assignment (if applicable)
3. Your proposed change and business justification
4. The other domain leads who should be consulted

DGO will acknowledge within 2 business days and schedule a resolution.

---

## Appendix A — Role Abbreviation Reference

| Abbreviation | Full Role Name |
|---|---|
| CDO | Chief Data Officer |
| DGO | Data Governance Office |
| DE-L | Data Engineering Lead |
| DE | Data Engineering Team |
| BI-COE | BI Center of Excellence Lead |
| BI | BI Domain Teams |
| ML-L | ML Engineering Lead |
| ML | ML Engineering Team |
| DO | Data Owner (domain-specific) |
| DS | Data Steward (domain-specific) |
| IT | IT / Infrastructure |
| CISO | CISO / InfoSec |
| PRIV | Privacy Officer |
| LEGAL | Legal |
| MR | Model Risk |
| AUDIT | Internal Audit |
| CAB | Change Advisory Board |
| GC | Governance Council |

## Appendix B — Related Documents

| Document | Location | Relationship |
|---|---|---|
| Data Governance Best Practices | `Data_Governance_Standards/01_data_governance_best_practices.md` | Governance principles underpinning ownership rules |
| Establishing Governance Program | `Data_Governance_Standards/02_establishing_governance_program.md` | Operating model this RACI operationalizes |
| Data Product Certification Framework | `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | Certification RACI details in Section 3.4 |
| Data Incident Response Playbook | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | Incident commander and response roles |
| DE Config and Change Management | `Data_Engineering_Standards/05_DE_Config_Change_Management.md` | Change tier and CAB requirements |
| BI Config and Change Management | `Business_Intelligence_Standards/05_BI_Config_Change_Management.md` | BI change tier details |
| ML Config and Change Management | `Machine_Learning_Standards/05_ML_Config_Change_Management.md` | ML change tier and Model Risk requirements |
| 2nd Line of Defense Strategy | `Data_Governance_Standards/04_2nd_line_of_defense_strategy.md` | 2LOD audit ownership and evidence requirements |
| Master Library README | `README.md` | Summary RACI in Section 5 |

---

*Document Owner: Chief Data Officer + Data Governance Office*
*Review Cycle: Semi-Annual or upon material org change*
*Disputes or amendments: raise a Collibra RACI Amendment Request task to the DGO Program Manager*
