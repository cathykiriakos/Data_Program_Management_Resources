# Data Governance Standards
## Domain README — Document Index and Navigation Guide

**Domain Owner:** Chief Data Officer + Data Governance Office
**Platform:** Collibra (control plane) · Snowflake · Databricks
**Version:** 2.0 | **Last Updated:** 2026-03
**Classification:** Internal — Program Reference

> **Purpose:** This domain defines the policies, standards, oversight model, and operating framework that govern all data across all domains. Collibra is the governance control plane. Snowflake and Databricks are the enforcement layer.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 01 | `01_data_governance_best_practices.md` | 2.0 | ✅ Active | All practitioners |
| 02 | `02_establishing_governance_program.md` | 2.0 | ✅ Active | Program leads, CDO |
| 03 | `03_data_governance_standards.md` | 2.0 | ✅ Active | Engineers, stewards |
| 04 | `04_2nd_line_of_defense_strategy.md` | 2.0 | ✅ Active | Governance, Audit, Risk |
| 05 | `05_kpis_and_benchmarking.md` | 2.0 | ✅ Active | CDO, Program leads |
| 06 | `06_configuration_and_change_management.md` | 2.0 | ✅ Active | Engineers, IT, Change Mgmt |
| 07 | `07_ground_up_strategy.md` | 2.0 | ✅ Active | CDO, Executives |

### Document Descriptions

| # | Document | Description |
|---|---|---|
| 01 | `01_data_governance_best_practices.md` | Core principles, pillars, Collibra platform role, anti-patterns, maturity model |
| 02 | `02_establishing_governance_program.md` | Operating model, RACI, phased rollout with Collibra onboarding, meeting cadence |
| 03 | `03_data_governance_standards.md` | Naming, classification schema, DQ rules, access, lifecycle standards |
| 04 | `04_2nd_line_of_defense_strategy.md` | Oversight model, Collibra-sourced audit framework, escalation matrix, maturity scoring |
| 05 | `05_kpis_and_benchmarking.md` | Full KPI registry, balanced scorecard, Python collector (Collibra API + Snowflake) |
| 06 | `06_configuration_and_change_management.md` | Part A (executive guide) + Part B (governance-as-code, Collibra integration, CI/CD, CAB) |
| 07 | `07_ground_up_strategy.md` | CDO vision, 2-year roadmap, Collibra architecture, federated governance model |

---

## Key Design Conventions

- **Collibra is the human-facing governance layer** — stewards, owners, and executives work here
- **Snowflake and Databricks are the enforcement layer** — Collibra decisions are pushed down via API and native connectors
- **All rules are YAML-driven** — edit config, not code; version-controlled in Git
- **Python scripts use a class-based, config-injected pattern** — reusable across environments
- **Document 06 is written in two parts** — an executive-friendly business guide (Part A) and a technical implementation guide (Part B)
- **KPIs are collected from both Collibra API and Snowflake** — no manual spreadsheets

---

## Domain Coverage

| Domain | Standards Status | README |
|---|---|---|
| ✅ Data Governance | Complete (v2.0 — includes Collibra) | This file |
| ✅ Data Engineering | Complete (v1.0) | `Data_Engineering_Standards/DE_README.md` |
| ✅ Business Intelligence | Complete (v1.0) | `Business_Intelligence_Standards/BI_README.md` |
| ✅ Machine Learning | Complete (v1.0) | `Machine_Learning_Standards/ML_README.md` |
| ✅ Cross-Domain | Complete (v1.0) | `README.md` (root) |
| 🔧 Data Quality | Partial — docs 06 + 08 active; docs 01–05 pending | `Data_Quality_Standards/` |

---

## Related Cross-Domain Documents

| Document | Description |
|---|---|
| `CROSS_DOMAIN_RACI.md` | Accountability matrix for all inter-domain activities |
| `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | P1–P4 incident response procedures |
| `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | T1–T4 data product certification |
| `VENDOR_THIRD_PARTY_DATA_RISK_STANDARD.md` | External data vendor risk and onboarding |

---

*Maintained by: Data Governance Office | CDO Sponsor: Chief Data Officer | Last reviewed: 2026-03*
