# Data Engineering Standards
## Domain README — Document Index and Navigation Guide

**Domain Owner:** Data Engineering Lead
**Platform:** Snowflake · Databricks (Unity Catalog) · dbt · Terraform · GitHub Actions
**Version:** 1.0 | **Last Updated:** 2026-03
**Classification:** Internal — Program Reference

> **Purpose:** This domain defines how the data platform is built, operated, and governed. It covers infrastructure-as-code, medallion pipeline architecture, quality gates, binding naming and access standards, change management, KPIs, and the audit framework for the engineering layer.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 01 | `01_DE_Best_Practices.md` | 1.0 | ✅ Active | All DE practitioners |
| 02 | `02_DE_Program_Establishment.md` | 1.0 | ✅ Active | DE Lead, CDO |
| 03 | `03_DE_Standards.md` | 1.0 | ✅ Active | Data Engineers, Analytics Engineers |
| 04 | `04_DE_Auditing_Guide.md` | 1.0 | ✅ Active | Governance, IT Audit |
| 05 | `05_DE_Config_Change_Management.md` | 1.0 | ✅ Active | Engineers, IT, Change Mgmt |
| 06 | `06_DE_KPIs_and_Benchmarking.md` | 1.0 | ✅ Active | DE Lead, CDO |

### Document Descriptions

| # | Document | Description |
|---|---|---|
| 01 | `01_DE_Best_Practices.md` | Cloud infrastructure patterns, medallion architecture, auth standards, object tagging, semantic layer integration, observability |
| 02 | `02_DE_Program_Establishment.md` | Ground-up build strategy, team RACI, phased rollout, maturity model, platform roadmap |
| 03 | `03_DE_Standards.md` | Binding naming conventions, object creation rules, pipeline code standards, access control, cost management standards |
| 04 | `04_DE_Auditing_Guide.md` | 1LOD self-assessment controls + 2LOD independent audit procedures, Snowflake audit queries, evidence requirements |
| 05 | `05_DE_Config_Change_Management.md` | Config-first architecture, Terraform IaC patterns, CI/CD for pipelines, change classification tiers, CAB templates |
| 06 | `06_DE_KPIs_and_Benchmarking.md` | Full KPI registry (platform health, data quality, operational excellence, cost efficiency), scorecard, Python collector |

---

## Quick Navigation

| You need to... | Start here |
|---|---|
| Understand how the platform is structured | `01_DE_Best_Practices.md` → Section 2 (Medallion Architecture) |
| Build a new pipeline from scratch | `01_DE_Best_Practices.md` → `03_DE_Standards.md` → `05_DE_Config_Change_Management.md` |
| Prepare a self-assessment or audit | `04_DE_Auditing_Guide.md` → Section 2 (1LOD controls) |
| Submit a change to IT / CAB | `05_DE_Config_Change_Management.md` → Section 4 (change classification) |
| Report on KPIs to the CDO | `06_DE_KPIs_and_Benchmarking.md` → Section 5 (scorecard template) |
| Onboard a new data source | `05_DE_Config_Change_Management.md` → Minor change process + `CROSS_DOMAIN_RACI.md` → Section 11.7 |

---

## Key Design Conventions

- **Infrastructure-as-code first** — all Snowflake and Databricks objects are Terraform-managed; manual creation triggers a drift alert
- **Config over code** — pipeline behavior driven by YAML config files, not hardcoded logic
- **Medallion architecture** — Bronze (raw) → Silver (cleaned, masked, conformed) → Gold (certified, business-ready)
- **DQ gates at every layer** — no pipeline promotes data without passing registered DQ rules
- **Audit columns on every table** — `_loaded_at`, `_source`, `_batch_id` stamped by the pipeline, not optional
- **Secrets manager only** — zero tolerance for credentials in code; enforced via pre-commit hook and CI scan
- **Class-based Python** — all pipeline classes accept a config dict; reusable across sources and environments

---

## Platform Standards at a Glance

| Standard | Rule |
|---|---|
| Naming | `{env}_{domain}_{layer}_{object_type}` — all lowercase, underscores |
| Environment promotion | Dev → Staging → Prod via CI/CD; no direct prod deployments |
| Warehouse sizing | Defined in Terraform; resize requires Minor change ticket |
| RBAC | Roles granted to groups, never individuals; defined in IaC |
| PII masking | Applied at Silver layer; column-level masking policies in Snowflake |
| DQ threshold changes (tighten) | DGO approval required; loosen = CDO awareness required |
| T1 asset SLA breach | Alert + escalation within 2 hours |

---

## Audit Cadence

| Activity | Frequency | Owner | Output |
|---|---|---|---|
| 1LOD Self-Assessment | Monthly | DE Lead | Self-attestation submitted to DGO |
| IaC Drift Detection | Daily (automated) | DE Team | Slack alert if drift detected |
| Access Review | Quarterly | DE Lead + IT | Access certification report |
| 2LOD Independent Audit | Semi-Annual | DGO | Audit findings + remediation plan |

---

## Cross-Domain Dependencies

| This domain... | Depends on... |
|---|---|
| Sources data from | External vendor feeds → `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` |
| Certifies assets through | Data Governance → `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` |
| Responds to incidents via | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` (INC-DQ, INC-OUT, INC-SCH) |
| Resolves cross-domain conflicts via | `CROSS_DOMAIN_RACI.md` → Sections 3, 6, 11 |

---

*Maintained by: Data Engineering Lead | DGO Oversight: Data Governance Office | Last reviewed: 2026-03*
