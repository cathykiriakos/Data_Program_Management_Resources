# Machine Learning Standards
## Domain README — Document Index and Navigation Guide

**Domain Owner:** ML Engineering Lead (ML COE Lead)
**Platform:** MLflow (Databricks-hosted) · Databricks (Unity Catalog) · Snowflake ML · Feature Store
**Version:** 1.0 | **Last Updated:** 2026-03
**Classification:** Internal — Program Reference

> **Purpose:** This domain defines how ML models are developed, governed, deployed, monitored, and retired. It covers the risk-tiered model framework (T1–T4), experiment tracking standards, feature store governance, model registry, MLOps change management, bias and fairness auditing, and the audit framework for the ML layer. T1 model governance is jointly owned with Model Risk.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 01 | `01_ML_Best_Practices.md` | 1.0 | ✅ Active | All ML practitioners |
| 02 | `02_ML_Program_Establishment.md` | 1.0 | ✅ Active | ML Lead, CDO |
| 03 | `03_ML_Standards.md` | 1.0 | ✅ Active | ML Engineers, Data Scientists |
| 04 | `04_ML_Auditing_Guide.md` | 1.0 | ✅ Active | Governance, Model Risk, Audit |
| 05 | `05_ML_Config_Change_Management.md` | 1.0 | ✅ Active | ML Engineers, IT, Change Mgmt |
| 06 | `06_ML_KPIs_and_Benchmarking.md` | 1.0 | ✅ Active | ML Lead, CDO, Model Risk |

### Document Descriptions

| # | Document | Description |
|---|---|---|
| 01 | `01_ML_Best_Practices.md` | ML operating model, experiment tracking, Snowflake/Databricks ML patterns, lineage, feature store governance, model monitoring |
| 02 | `02_ML_Program_Establishment.md` | MLOps build strategy, team RACI, model inventory, MLOps maturity progression, build-vs-buy framework |
| 03 | `03_ML_Standards.md` | Binding standards: experiment tracking requirements, feature management, model registry, deployment gates, monitoring thresholds, ML code standards |
| 04 | `04_ML_Auditing_Guide.md` | 1LOD controls + 2LOD audit procedures, bias audit sampling, lineage verification, PII-in-training review, T1 model deep-dive, regulatory readiness |
| 05 | `05_ML_Config_Change_Management.md` | Config-first MLOps, model YAML config, CI/CD for ML promotion, serving config, monitoring as code, change classification tiers, CAB templates |
| 06 | `06_ML_KPIs_and_Benchmarking.md` | Full KPI registry by tier (model governance, model performance, operations & reliability, risk & compliance), scorecard, Python collector (MLflow + Snowflake) |

---

## Quick Navigation

| You need to... | Start here |
|---|---|
| Understand the ML governance model and tiers | `01_ML_Best_Practices.md` → Section 2 (ML Operating Model) |
| Promote a model to production | `05_ML_Config_Change_Management.md` → Section 4 (change classification by tier) |
| Register a new model in the registry | `03_ML_Standards.md` → Section 4 (Model Registry Standards) |
| Run a bias or fairness audit | `04_ML_Auditing_Guide.md` → Section 2 (1LOD bias controls) |
| Prepare a T1 model for regulatory review | `04_ML_Auditing_Guide.md` → Section 5 (Model Risk Audit) |
| Handle a T1 model performance incident | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` → INC-ML + `CROSS_DOMAIN_RACI.md` → Section 8.4 |
| Report on model KPIs to the CDO | `06_ML_KPIs_and_Benchmarking.md` → Section 5 (CDO scorecard) |

---

## Model Tier Framework

| Tier | Label | Production Gate | DGO Role | Model Risk Role | CDO Sign-off |
|---|---|---|---|---|---|
| **T1** | Critical | ML Lead + Model Risk + CDO + CAB | Required — governance tracking | Independent validation required | Required |
| **T2** | Governed | ML Lead + Domain Owner | Informed | Not required | Not required |
| **T3** | Managed | ML Engineering Lead | Not required | Not required | Not required |
| **T4** | Sandbox / Experimental | None | Not required | Not required | Not required |

**T1 mandatory requirements:**
- Model card authored and signed off by ML Lead, Domain Owner, and Model Risk
- Independent validation completed by Model Risk before any production promotion
- Bias and fairness audit completed and no material concerns unresolved
- Monitoring activated on deployment day — no grace period
- Two consecutive months of performance gate failure → Model Risk Committee notification (mandatory)

---

## Key Design Conventions

- **Every model is registered** — no unregistered models in any environment beyond T4 sandbox
- **Every experiment is tracked** — MLflow tracking is mandatory; unapproved frameworks require ML Lead approval
- **Model config is YAML** — hyperparameters, thresholds, serving config externalized; not hardcoded
- **Feature data contracts** — ML team must sign as consumer on any Gold table used as a feature source
- **PII in training data is governed** — Privacy Officer review required; DGO signs off; documented in model card
- **Monitoring is code** — drift thresholds, alert webhooks, and monitoring cadence defined in config and version-controlled
- **T1 rollback is always possible** — previous version remains registered and deployable; rollback procedure documented before go-live

---

## Audit Cadence

| Activity | Frequency | Owner | Output |
|---|---|---|---|
| 1LOD Self-Assessment | Monthly | ML Lead | Self-attestation submitted to DGO |
| Bias Audit (T1/T2 models) | Per promotion + semi-annual refresh | ML Governance Analyst | Bias audit report |
| Model Performance Review (T1) | Monthly | Domain ML Lead + Model Risk | Performance scorecard |
| PII-in-Training Review | Per model + annual | DGO + Privacy Officer | PII review sign-off |
| 2LOD Independent Audit (T1/T2) | Semi-Annual | DGO + Model Risk | ML audit findings |
| Model Risk Committee Report | As triggered (T1 performance breach) | CDO + Model Risk | MRC report |

---

## Cross-Domain Dependencies

| This domain... | Depends on... |
|---|---|
| Consumes feature data from | Data Engineering → Gold layer + feature store; data contract required |
| Certifies models through | DGO + Model Risk → `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` (T1/T2) |
| Responds to model incidents via | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` (INC-ML) |
| Resolves cross-domain conflicts via | `CROSS_DOMAIN_RACI.md` → Section 8 (ML Governance RACI) |
| Uses vendor data through | `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` → V1 + ML Data Provenance Assessment |

---

*Maintained by: ML Engineering Lead | Model Risk: Independent oversight of T1/T2 models | DGO Oversight: Data Governance Office | Last reviewed: 2026-03*
