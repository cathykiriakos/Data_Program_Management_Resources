# Enterprise Data Program Library
## Chief Data Officer — Program Reference & Navigation Guide

> **Platform Stack:** Snowflake · Databricks · Collibra · dbt · MLflow  
> **Frameworks:** DAMA DMBOK · DCAM · Three Lines of Defense  
> **Version:** 1.0 | **Last Updated:** 2026-03  
> **Classification:** Internal — Program Reference

---

## What This Library Is

This is the authoritative documentation library for the enterprise data program. It covers four operational domains — Data Governance, Data Engineering, Business Intelligence, and Machine Learning — each with a consistent set of artifacts covering best practices, program establishment, binding standards, audit frameworks, configuration and change management, KPIs, and ground-up strategy.

Every document in this library is:

- **Production-ready** — not conceptual. Templates, code, YAML, and SQL are included and deployable.
- **Config-driven** — all repeatable patterns use externalized YAML config so rules can be changed without code modifications.
- **Governance-as-code** — policy enforcement, DQ rules, and classification are version-controlled and CI/CD compatible.
- **Audit-ready** — each domain has explicit 1st and 2nd Line of Defense control frameworks tied to evidence requirements.

---

## How to Use This Library

| You are... | Start here |
|---|---|
| New CDO or program lead orienting to the program | Section 2 (Architecture) → Section 5 (Cross-Domain RACI) → each domain's `01_Best_Practices` |
| Engineer onboarding to a domain | Your domain's `01_Best_Practices` → `03_Standards` → `05_Config_Change_Management` |
| Preparing for an audit | Your domain's `04_Auditing_Guide` → Governance `04_2nd_Line_of_Defense_Strategy` |
| Building a KPI dashboard | Your domain's `05/06_KPIs_and_Benchmarking` → `03_Standards` for metric definitions |
| Standing up a new program from scratch | Your domain's `02_Program_Establishment` → `07_Ground_Up_Strategy` (Governance) |
| Reviewing a change with IT/CAB | Your domain's `05_Config_Change_Management` → change tier classification table |

---

## 1. Technology Stack

```
┌────────────────────────────────────────────────────────────────────┐
│  GOVERNANCE CONTROL PLANE                                          │
│  Collibra — Catalog · Glossary · Lineage · DQ · Access · Policy   │
└──────────────────────────┬─────────────────────────────────────────┘
                           │ governs & certifies assets in
          ┌────────────────┴────────────────┐
          │                                 │
  ┌───────▼────────┐               ┌────────▼───────┐
  │   SNOWFLAKE    │               │  DATABRICKS    │
  │  Data Warehouse│               │  Data Lakehouse│
  │  Bronze/Silver │               │  Bronze/Silver │
  │  Gold · RBAC   │               │  Gold · Unity  │
  │  Masking · Tags│               │  Catalog · ML  │
  └───────┬────────┘               └────────┬───────┘
          │                                 │
          └──────────────┬──────────────────┘
                         │
              ┌──────────▼──────────┐
              │   SEMANTIC LAYER    │
              │   dbt + Metrics     │
              └──────────┬──────────┘
                         │
         ┌───────────────┼──────────────────┐
         │               │                  │
  ┌──────▼──────┐  ┌─────▼──────┐  ┌───────▼──────┐
  │     BI      │  │     ML     │  │  APIs / Apps │
  │  Tableau    │  │  MLflow    │  │              │
  │  Power BI   │  │  Feature   │  │              │
  │  Alteryx    │  │  Store     │  │              │
  └─────────────┘  └────────────┘  └──────────────┘
```

| Layer | Platform | Primary Role |
|---|---|---|
| Governance Control Plane | Collibra Data Intelligence Cloud | Catalog, glossary, DQ, lineage, access governance, policy |
| Data Warehouse | Snowflake | Structured workloads, RBAC, column masking, row policies, tagging |
| Data Lakehouse | Databricks (Unity Catalog) | ML/unstructured, streaming, feature store, Unity Catalog governance |
| Semantic Layer | dbt Core / dbt Cloud | SQL-first transformations, metrics layer, data contracts |
| Experiment Tracking | MLflow (Databricks-hosted) | Model registry, run tracking, artifact store, lineage |
| Governance Config | Git (YAML) | Version-controlled source of truth for all governance rules |
| Orchestration | Apache Airflow / Databricks Workflows | DAG-based scheduling, pipeline dependency management |
| CI/CD | GitHub Actions | Automated testing, IaC deployment, config validation |
| Secrets | AWS Secrets Manager / Azure Key Vault | Zero-secret-in-code enforcement |
| ITSM | ServiceNow / Jira | Change management, incident tracking, audit evidence |

---

## 2. Program Architecture

### 2.1 Data Flow Architecture

```
SOURCE SYSTEMS
  ERP · CRM · SaaS APIs · Files · Streaming · Legacy DB
        │
        ▼
  INGESTION LAYER
  Fivetran / Airbyte / Custom Python (config-driven)
        │
        ▼
  BRONZE (Raw)  ←── Schema validation · Dead letter queue
        │
        ▼
  SILVER (Cleaned) ←── DQ gates · PII masking · Lineage
        │
        ▼
  GOLD (Curated) ←── Data contracts · Certified products · RBAC
        │
        ▼
  SEMANTIC LAYER  ←── dbt metrics · Certified datasets for BI
     │        │
     ▼        ▼
    BI       ML
  Tools   Feature Store → Model Training → Serving
```

### 2.2 Governance Flow Architecture

```
COLLIBRA (System of Record for Governance)
  │
  ├── Business Glossary      → Drives shared definitions across all domains
  ├── Data Catalog           → All governed assets registered here
  ├── DQ Engine (Owl)        → Rule results feed from Snowflake / Databricks
  ├── Lineage Graph          → End-to-end lineage source → BI / ML
  ├── Access Governance      → Access certifications, entitlement reviews
  ├── Policy Manager         → Policy exceptions, regulatory controls
  └── Workflow Engine        → Stewardship tasks, approvals, onboarding
         │
         ▼ (push down via API / native connectors)
  ENFORCEMENT LAYER
  Snowflake: RBAC · Column masking · Row access policies · Object tags
  Databricks: Unity Catalog row/column filters · Table ACLs · Audit logs
```

### 2.3 Key Design Principles

| Principle | Practice |
|---|---|
| **Config over code** | All rules, thresholds, and environment values live in YAML — not hardcoded |
| **Governance left-shift** | Quality and classification enforced at ingest, not remediated downstream |
| **Collibra as control plane** | Business users and stewards interact with governance through Collibra; platforms enforce |
| **Everything as code** | IaC, pipelines, DQ rules, access policies, ML configs — all version-controlled |
| **Audit by design** | Every layer produces traceable records without manual intervention |
| **Separation of concerns** | DE builds, Governance certifies, BI/ML consume — with explicit handoffs |

---

## 3. Domain Library Index

### 3.1 Data Governance (`Data_Governance_Standards/`)

> **Purpose:** Defines the policies, standards, oversight model, and operating framework that govern all data across all domains. Collibra is the governance control plane.

| # | Document | Version | Description |
|---|---|---|---|
| 01 | `01_data_governance_best_practices.md` | 2.0 | Core principles, pillars, Collibra platform role, anti-patterns, maturity model |
| 02 | `02_establishing_governance_program.md` | 2.0 | Operating model, RACI, phased rollout with Collibra onboarding, meeting cadence |
| 03 | `03_data_governance_standards.md` | 2.0 | Naming, classification schema, DQ rules, access, lifecycle standards |
| 04 | `04_2nd_line_of_defense_strategy.md` | 2.0 | Oversight model, Collibra-sourced audit framework, escalation matrix, maturity scoring |
| 05 | `05_kpis_and_benchmarking.md` | 2.0 | Full KPI registry, balanced scorecard, Python collector (Collibra API + Snowflake) |
| 06 | `06_configuration_and_change_management.md` | 2.0 | Part A (executive guide) + Part B (governance-as-code, Collibra integration, CI/CD, CAB) |
| 07 | `07_ground_up_strategy.md` | 2.0 | CDO vision, 2-year roadmap, Collibra architecture, federated governance model |
| — | `DATAGOV_README.md` | 2.0 | Domain-level README and document index |

### 3.2 Data Engineering (`Data_Engineering_Standards/`)

> **Purpose:** Defines how the data platform is built, operated, and governed. Covers infrastructure, pipelines, quality gates, standards, and config management across Snowflake and Databricks.

| # | Document | Version | Description |
|---|---|---|---|
| 01 | `01_DE_Best_Practices.md` | 1.0 | Cloud infra, medallion architecture, auth, tagging, semantic layer, observability |
| 02 | `02_DE_Program_Establishment.md` | 1.0 | Ground-up build strategy, team RACI, phased rollout, maturity model, roadmap |
| 03 | `03_DE_Standards.md` | 1.0 | Binding naming conventions, object creation, code, pipeline, access, cost standards |
| 04 | `04_DE_Auditing_Guide.md` | 1.0 | 1LOD self-assessment controls + 2LOD independent audit procedures, evidence requirements |
| 05 | `05_DE_Config_Change_Management.md` | 1.0 | Config-first architecture, Terraform, CI/CD, change classification tiers, CAB templates |
| 06 | `06_DE_KPIs_and_Benchmarking.md` | 1.0 | Full KPI registry, scorecard, Python collector (Snowflake + Databricks API + Git) |
| — | `DE_README.md` | 1.0 | Domain-level README and document index |

### 3.3 Business Intelligence (`Business_Intelligence_Standards/`)

> **Purpose:** Defines how BI content is built, governed, certified, and consumed. Covers Tableau, Power BI, and Alteryx with standards for self-service, access, branding, and performance.

| # | Document | Version | Description |
|---|---|---|---|
| 01 | `01_BI_Best_Practices.md` | 1.0 | Governed self-service model, auth standards, RLS, visualization, branding, regulated controls |
| 02 | `02_BI_Program_Establishment.md` | 1.0 | BI COE structure, phased rollout, certified dataset program, maturity model, governance council |
| 03 | `03_BI_Standards.md` | 1.0 | Binding standards: report tiers, naming, certification, source compliance, content lifecycle |
| 04 | `04_BI_Auditing_Guide.md` | 1.0 | 1LOD self-assessment + 2LOD audit procedures, access sampling, PII testing, regulatory readiness |
| 05 | `05_BI_Config_Change_Management.md` | 1.0 | Config-first BI ops, Report Registry as code, environment promotion, change tiers, CAB templates |
| 06 | `06_BI_KPIs_and_Benchmarking.md` | 1.0 | Full KPI registry, scorecard, Python collector (Snowflake + Tableau/Power BI APIs) |
| — | `BI_README.md` | 1.0 | Domain-level README and document index |

### 3.4 Machine Learning (`Machine_Learning_Standards/`)

> **Purpose:** Defines how ML models are developed, governed, deployed, monitored, and retired. Covers MLflow, Snowflake ML, Databricks, and SageMaker with a risk-tiered model governance framework.

| # | Document | Version | Description |
|---|---|---|---|
| 01 | `01_ML_Best_Practices.md` | 1.0 | ML operating model, experiment tracking, Snowflake/Databricks ML, lineage, feature store, monitoring |
| 02 | `02_ML_Program_Establishment.md` | 1.0 | MLOps build strategy, team RACI, model inventory, MLOps maturity progression, build vs. buy |
| 03 | `03_ML_Standards.md` | 1.0 | Binding standards: experiment tracking, feature management, registry, deployment, monitoring, code |
| 04 | `04_ML_Auditing_Guide.md` | 1.0 | 1LOD controls + 2LOD audit procedures, bias auditing, lineage verification, regulatory readiness |
| 05 | `05_ML_Config_Change_Management.md` | 1.0 | Config-first MLOps, model YAML config, CI/CD for ML, serving config, monitoring as code |
| 06 | `06_ML_KPIs_and_Benchmarking.md` | 1.0 | Full KPI registry by model tier, scorecard, Python collector (MLflow + Snowflake) |
| — | `ML_README.md` | 1.0 | Domain-level README and document index |

### 3.5 Cross-Domain Standards (root `/`)

> **Purpose:** Governing frameworks and operational standards that span all domains and cannot be owned by a single domain. These documents carry CDO and DGO joint ownership.

| Document | Version | Description |
|---|---|---|
| `CROSS_DOMAIN_RACI.md` | 1.0 | Full accountability matrix — 35 RACI tables, 7 scenario-based decision trees, escalation paths, conflict resolution |
| `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | 1.0 | P1–P4 incident classification, 8 incident type playbooks, evidence preservation, regulatory notification |
| `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | 1.0 | T1–T4 certification tiers, five-pillar gate, Snowflake/Databricks/BI platform coverage, CI/CD pipeline |
| `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` | 1.0 | V1–V4 vendor tiers, onboarding process, risk scoring, contractual requirements, monitoring, offboarding |

### 3.6 Data Quality (`Data_Quality_Standards/`)

> **Purpose:** Provides the engineering framework for building, running, storing, and observing automated data quality test suites. These are the implementation guides for DQ rules referenced in DE and Governance standards.

| # | Document | Version | Description |
|---|---|---|---|
| 06 | `06_DQ_Complete_Suite_Builder.md` | 1.0 | Step-by-step framework for building production-grade DQ test suites from scratch |
| 08 | `08_DQ_CICD_and_Observability.md` | 1.0 | CI/CD integration, DQ result storage, alerting design, SLA monitoring, observability dashboard |

---

## 4. Document Template Structure

Every domain follows a consistent six-to-seven document structure. This is intentional — a new team member or auditor can navigate any domain using the same mental model.

| Position | Document Type | Purpose | Primary Audience |
|---|---|---|---|
| `01` | Best Practices | Principles, patterns, platform alignment, anti-patterns | All practitioners |
| `02` | Program Establishment | Operating model, RACI, phased build strategy, maturity model | Program leads, CDO |
| `03` | Standards | Binding rules: naming, access, code, deployment | Engineers, stewards |
| `04` | Auditing Guide | 1LOD controls + 2LOD independent audit procedures | Governance, Audit, Risk |
| `05` | Config & Change Management | Config-first patterns, IT change integration, CAB templates | Engineers, IT, Change Mgmt |
| `06` | KPIs & Benchmarking | KPI registry, scorecard template, Python collector, benchmarks | CDO, Program leads |
| `07` | Ground-Up Strategy | CDO vision, roadmap, federated model (Governance only) | CDO, Executives |

---

## 5. Cross-Domain RACI

This table resolves ownership at the boundaries between domains — the areas most likely to produce accountability gaps.

### 5.1 Data Product Lifecycle

| Activity | Data Engineering | Data Governance | BI | ML | IT |
|---|---|---|---|---|---|
| Pipeline design and build | **R/A** | C | I | I | I |
| Data classification (new asset) | C | **R/A** | I | I | I |
| DQ rule definition | C | **R/A** | C | C | I |
| DQ gate implementation in pipeline | **R/A** | C | I | I | I |
| Gold object certification | C | **R/A** | C | C | I |
| Data contract authoring | **R/A** | C | C | C | I |
| Data contract sign-off (consumer) | I | C | **R/A** (BI), C | **R/A** (ML), C | I |
| Schema change notification | **R/A** | I | **R** (inform) | **R** (inform) | I |
| Lineage documentation | **R** | **A** | C | C | I |
| Access provisioning | C | **A** | R (request) | R (request) | **R** |
| Access certification | I | **A** | R (attest) | R (attest) | R |
| Retention policy enforcement | **R** (platform) | **A** (policy) | I | I | I |

### 5.2 Incident & Issue Resolution

| Scenario | First Responder | Escalation Path | Governance Role |
|---|---|---|---|
| Pipeline DQ failure blocking Gold | DE on-call | DE Lead → CDO if > 4hr | DGO notified; tracks in incident log |
| BI report showing wrong numbers | Domain BI Lead | BI COE Lead → Data Owner | DGO reviews if certified content |
| ML model performance degradation | Domain ML Lead | ML COE Lead → Model Risk (T1) | DGO tracks; Model Risk owns T1 |
| PII found in non-restricted layer | DE on-call | CDO + Privacy Officer immediately | DGO opens formal incident; 2LOD review |
| Unauthorized data access detected | IT/CISO | CDO + Legal | DGO opens access review |
| Schema change breaks downstream | DE Lead | Contract owner + affected consumers | DGO mediates via data contract process |
| Conflicting metric definitions | BI COE Lead | Governance Council arbitration | DGO owns glossary resolution |

### 5.3 Platform Change Authority

| Change Type | Approver | Required Evidence | Process |
|---|---|---|---|
| New source system onboarding | DE Lead + DGO | Data Impact Assessment | Minor change ticket |
| New Snowflake database / schema | DE Lead + IT | IaC PR + Terraform plan | Minor change ticket |
| RBAC role restructure | DE Lead + IT + DGO | Access review + rollback plan | Major change ticket + CAB |
| New BI certified dataset | BI COE + DGO | RLS test evidence + data contract | Minor change ticket |
| New T1 ML model to production | ML Lead + Model Risk + DGO | Full model card + change ticket + validation | Major change ticket + CAB |
| Classification schema change | CDO + DGO | Impact assessment + migration plan | Major change ticket + CAB |
| Collibra workflow / policy change | DGO | Staging environment test + steward sign-off | Minor change ticket |

---

## 6. Program KPI Summary

Each domain publishes a monthly KPI scorecard. The CDO-level view consolidates key indicators across domains.

### 6.1 CDO Dashboard — Headline KPIs

| Domain | Headline KPI | Target | Frequency |
|---|---|---|---|
| **Governance** | Asset Ownership Coverage | ≥ 95% | Monthly |
| **Governance** | Critical DQ Pass Rate | ≥ 99.5% | Daily |
| **Governance** | Policy Exception Aging (> 30 days) | 0 | Weekly |
| **Data Engineering** | IaC Drift Incidents | 0 | Monthly |
| **Data Engineering** | Gold Metadata Completeness | 100% | Monthly |
| **Data Engineering** | SLA Breach Rate | < 1% | Daily |
| **Business Intelligence** | Unapproved Source Incidents | 0 | Monthly |
| **Business Intelligence** | T1 Report Freshness SLA | 100% | Daily |
| **Business Intelligence** | Consumer Satisfaction Score | ≥ 4.0 | Quarterly |
| **Machine Learning** | T1 Model Registry Coverage | 100% | Monthly |
| **Machine Learning** | T1 Model Performance Gate Compliance | 100% | Monthly |
| **Machine Learning** | PII in Training Data Violations | 0 | Monthly |

### 6.2 KPI Document Index

| Domain | KPI Document |
|---|---|
| Data Governance | `Data_Governance_Standards/05_kpis_and_benchmarking.md` |
| Data Engineering | `Data_Engineering_Standards/05_DE_KPIs_and_Benchmarking.md` |
| Business Intelligence | `Business_Intelligence_Standards/06_BI_KPIs_and_Benchmarking.md` |
| Machine Learning | `Machine_Learning_Standards/06_ML_KPIs_and_Benchmarking.md` |

---

## 7. Audit & Oversight Reference

### 7.1 Three Lines of Defense — Domain Map

| Line | Who | Role | Cadence |
|---|---|---|---|
| **1st Line** | DE Team, BI COE, ML Engineering, Domain Stewards | Own and operate controls; self-attest | Monthly |
| **2nd Line** | Data Governance Office (DGO), Model Risk, Privacy Officer | Independent verification; challenge; escalate | Quarterly audit; continuous monitoring |
| **3rd Line** | Internal Audit, External Audit, Regulators | Independent deep-dive testing; regulatory examination | Annual / as triggered |

### 7.2 Audit Document Index

| Domain | 1LOD Controls | 2LOD Audit Guide |
|---|---|---|
| Data Governance | `04_2nd_line_of_defense_strategy.md` (section 3) | `04_2nd_line_of_defense_strategy.md` (section 5) |
| Data Engineering | `04_DE_Auditing_Guide.md` (section 2) | `04_DE_Auditing_Guide.md` (section 3) |
| Business Intelligence | `04_BI_Auditing_Guide.md` (section 2) | `04_BI_Auditing_Guide.md` (section 3) |
| Machine Learning | `04_ML_Auditing_Guide.md` (section 2) | `04_ML_Auditing_Guide.md` (section 3) |

### 7.3 Audit Cadence

| Audit | Frequency | Led By | Output |
|---|---|---|---|
| DE 1LOD Self-Assessment | Monthly | DE Lead | Self-attestation report |
| BI 1LOD Self-Assessment | Monthly | BI COE Lead | Self-attestation report |
| ML 1LOD Self-Assessment | Monthly | ML Lead | Self-attestation report |
| Governance 2LOD Review | Quarterly | DGO | Compliance scorecard |
| DE 2LOD Independent Audit | Semi-Annual | DGO / IT Audit | Formal audit findings |
| BI 2LOD Independent Audit | Semi-Annual | DGO / IT Audit | Formal audit findings |
| ML 2LOD Model Audit (T1/T2) | Semi-Annual | DGO / Model Risk | Model audit report |
| Cross-Domain Program Review | Annual | CDO | Program maturity assessment |

---

## 8. Configuration & Change Management Reference

All four domains follow a tiered change classification model aligned to the IT Change Advisory Board (CAB) process.

### 8.1 Change Tier Summary

| Tier | Description | Lead Time | CAB Required | Examples |
|---|---|---|---|---|
| **Self-Service** | User-controlled, no platform impact | Immediate | No | T3 BI report creation, sandbox ML experiment |
| **Standard** | Logic changes, no infrastructure impact | Same day | No | Pipeline logic update, dbt model change, T2 report update |
| **Minor** | New objects, additive schema changes | 3–5 days | No | New source onboarding, new certified dataset, new T2 model |
| **Major** | Infrastructure, RBAC, security, new platforms | 10–15 days | Yes | RBAC restructure, new Snowflake account, T1 model to prod, classification change |
| **Hotfix** | Production incident emergency fix | Immediate (retrospective ticket within 24hr) | No (post-hoc) | P1 pipeline fix, serving endpoint emergency patch |

### 8.2 Change Management Document Index

| Domain | Config & Change Document |
|---|---|
| Data Governance | `Data_Governance_Standards/06_configuration_and_change_management.md` |
| Data Engineering | `Data_Engineering_Standards/05_DE_Config_Change_Management.md` |
| Business Intelligence | `Business_Intelligence_Standards/05_BI_Config_Change_Management.md` |
| Machine Learning | `Machine_Learning_Standards/05_ML_Config_Change_Management.md` |

---

## 9. Document Version Control

All documents in this library are versioned and reviewed on the following schedule:

| Review Trigger | Action |
|---|---|
| Major platform change (Snowflake version, Databricks upgrade, Collibra release) | Impacted documents reviewed within 30 days |
| Regulatory change affecting data handling | Impacted standards updated within 60 days |
| Scheduled annual review | All documents reviewed; versions incremented if updated |
| Audit finding requires standard update | Standard updated; version incremented; change logged |

### 9.1 Document Status Definitions

| Status | Meaning |
|---|---|
| `Active` | Current, enforced, applies to all in-scope programs |
| `Draft` | In review; not yet enforced |
| `Superseded` | Replaced by a newer version; retained for audit history |
| `Archived` | No longer applicable; retained for historical reference only |

### 9.2 Current Document Status

| Domain | Documents | Status | Latest Version |
|---|---|---|---|
| Data Governance | 7 documents + domain README | ✅ Active | 2.0 |
| Data Engineering | 6 documents + domain README | ✅ Active | 1.0 |
| Business Intelligence | 6 documents + domain README | ✅ Active | 1.0 |
| Machine Learning | 6 documents + domain README | ✅ Active | 1.0 |
| Data Quality | 2 documents | ✅ Active | 1.0 |
| Cross-Domain | 4 documents | ✅ Active | 1.0 |

---

## 10. Gaps & Planned Additions

### 10.1 Completed Items

| Document | Domain | Completed |
|---|---|---|
| `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | Cross-domain | ✅ 2026-03 |
| `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | Cross-domain | ✅ 2026-03 |
| `CROSS_DOMAIN_RACI.md` | Cross-domain | ✅ 2026-03 |
| `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` | Cross-domain | ✅ 2026-03 |
| Domain READMEs — DE, BI, ML | All | ✅ 2026-03 |

### 10.2 Remaining Gaps

| Priority | Document | Domain | Rationale |
|---|---|---|---|
| P2 | `Data_Quality_Standards/01_DQ_Best_Practices.md` through `05_DQ_Config_Change_Management.md` | Data Quality | DQ domain has implementation guides (docs 06 + 08) but lacks the full six-document standards structure (best practices, program establishment, standards, auditing guide, config & change management) |

---

## 11. Contacts & Ownership

| Role | Responsibilities |
|---|---|
| **Chief Data Officer** | Program sponsor; escalation owner; executive reporting |
| **Data Governance Lead (DGO)** | Policy ownership; 2LOD oversight; Collibra platform; stewardship program |
| **Data Engineering Lead** | Platform engineering; pipeline standards; IaC ownership |
| **BI COE Lead** | BI platform; certified content program; self-service governance |
| **ML COE Lead** | MLOps platform; model registry; ML governance; T1 model oversight |
| **Model Risk** | Independent T1 model validation; regulatory model submissions |
| **Privacy Officer** | PII governance; data subject rights; privacy reviews on new data products |
| **IT / InfoSec** | Cloud infrastructure; network security; ITSM change management; audit logging |

---

*Maintained by: Chief Data Office | Last reviewed: 2026-03 (updated: cross-domain docs complete, domain READMEs added) | Next scheduled review: 2026-09*
