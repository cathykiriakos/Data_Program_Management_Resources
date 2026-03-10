# Business Intelligence Standards
## Domain README — Document Index and Navigation Guide

**Domain Owner:** BI Center of Excellence Lead
**Platform:** Tableau · Power BI · Alteryx · Snowflake (semantic layer via dbt)
**Version:** 1.0 | **Last Updated:** 2026-03
**Classification:** Internal — Program Reference

> **Purpose:** This domain defines how BI content is built, governed, certified, and consumed. It covers the governed self-service model, certified dataset program, report tier framework (T1–T3), access and RLS standards, branding, content lifecycle, change management, and the audit framework for the BI layer.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 01 | `01_BI_Best_Practices.md` | 1.0 | ✅ Active | All BI practitioners |
| 02 | `02_BI_Program_Establishment.md` | 1.0 | ✅ Active | BI COE Lead, CDO |
| 03 | `03_BI_Standards.md` | 1.0 | ✅ Active | BI Developers, Analytics Engineers |
| 04 | `04_BI_Auditing_Guide.md` | 1.0 | ✅ Active | Governance, IT Audit |
| 05 | `05_BI_Config_Change_Management.md` | 1.0 | ✅ Active | BI Engineers, IT, Change Mgmt |
| 06 | `06_BI_KPIs_and_Benchmarking.md` | 1.0 | ✅ Active | BI COE Lead, CDO |

### Document Descriptions

| # | Document | Description |
|---|---|---|
| 01 | `01_BI_Best_Practices.md` | Governed self-service model, authentication standards, RLS patterns, visualization principles, branding, regulated environment controls, incident considerations |
| 02 | `02_BI_Program_Establishment.md` | BI COE structure and roles, phased rollout, certified dataset program, self-service enablement, maturity model, governance council |
| 03 | `03_BI_Standards.md` | Binding standards: report tiers (T1–T3), naming conventions, certification requirements, approved source compliance, content lifecycle, zero-tolerance rules |
| 04 | `04_BI_Auditing_Guide.md` | 1LOD self-assessment + 2LOD audit procedures, access entitlement sampling, PII exposure testing, cost audit, regulatory readiness |
| 05 | `05_BI_Config_Change_Management.md` | Config-first BI operations, Report Registry as code, environment promotion, refresh SLA monitoring, change classification tiers, CAB templates |
| 06 | `06_BI_KPIs_and_Benchmarking.md` | Full KPI registry (governance & trust, content quality, adoption & consumption, cost & performance), scorecard, Python collector |

---

## Quick Navigation

| You need to... | Start here |
|---|---|
| Understand the BI content governance model | `01_BI_Best_Practices.md` → Section 3 (Governed Self-Service) |
| Build or certify a new report or dataset | `03_BI_Standards.md` → Section 4 (Certification) + `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` |
| Set up RLS for a new dataset | `01_BI_Best_Practices.md` → Section 7 (RLS) + `03_BI_Standards.md` → Section 6 |
| Prepare a self-assessment or audit | `04_BI_Auditing_Guide.md` → Section 2 (1LOD controls) |
| Submit a change to IT / CAB | `05_BI_Config_Change_Management.md` → Section 8 (change classification table) |
| Report on KPIs to the CDO | `06_BI_KPIs_and_Benchmarking.md` → Section 5 (scorecard template) |
| Handle a certified report data error | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` → INC-BI + `CROSS_DOMAIN_RACI.md` → Section 9.2 |

---

## Report Tier Framework

| Tier | Label | Owner | DGO Involvement | Certification Required |
|---|---|---|---|---|
| **T1** | Executive / Certified | BI COE | Yes — DGO validates source + access | Yes — formal certification process |
| **T2** | Domain Governed | Domain BI Lead | Informed | Light review by BI COE |
| **T3** | Self-Service | Individual analyst | None (workspace guardrails apply) | No |

**Zero-Tolerance Rules (no exception pathway):**
- Direct connection to production source systems → immediate revocation
- Personal credentials in published data sources → immediate credential rotation
- PII visible to users without Restricted data role → immediate takedown + Privacy Officer
- External sharing of Restricted/Top Secret content → immediate revocation + Legal

---

## Key Design Conventions

- **Approved sources only** — BI tools may only connect to Gold layer or certified semantic layer objects; no direct Bronze/Silver access
- **Report Registry as code** — all T1/T2 content is registered in YAML config under version control
- **RLS by persona** — row-level security is tested against named personas before certification; PowerBIRLSValidator class automates this
- **Data minimization** — certified datasets include only columns and rows needed by the intended audience; import mode requires pre-filtering
- **Content lifecycle enforced** — T3 reports with no views in 90 days are auto-archived
- **CI/CD for BI** — T1 content deployed via pipeline; manual publishes to T1 workspaces trigger an incident

---

## Audit Cadence

| Activity | Frequency | Owner | Output |
|---|---|---|---|
| 1LOD Self-Assessment | Monthly | BI COE Lead | Self-attestation submitted to DGO |
| Data Source Compliance Scan | Monthly | BI COE | Unapproved connection report |
| PII Exposure Audit | Quarterly | BI COE + Privacy | PII risk report |
| Report Registry Review | Quarterly | BI COE | Registry completeness report |
| Access Certification | Quarterly | BI COE + Domain Stewards | Entitlement report |
| 2LOD Independent Audit | Semi-Annual | DGO | Audit findings + remediation plan |

---

## Cross-Domain Dependencies

| This domain... | Depends on... |
|---|---|
| Consumes certified data from | Data Engineering → Gold layer + `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` |
| Resolves metric conflicts via | Data Governance → Collibra glossary + `CROSS_DOMAIN_RACI.md` → Section 9.4 |
| Responds to report incidents via | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` (INC-BI) |
| Submits changes through | `05_BI_Config_Change_Management.md` → change tiers aligned to IT CAB |

---

*Maintained by: BI Center of Excellence Lead | DGO Oversight: Data Governance Office | Last reviewed: 2026-03*
