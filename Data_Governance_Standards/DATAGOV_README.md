# Data Governance Program Library
> **Platform:** Snowflake / Databricks / Collibra | **Role:** Chief Data Officer  
> **Version:** 2.0 | **Last Updated:** 2026-03

---

## Document Index

| # | Document | Description |
|---|---|---|
| 01 | [Best Practices](./01_data_governance_best_practices.md) | Core principles, pillars, Collibra platform role, anti-patterns, maturity model |
| 02 | [Establishing a Program](./02_establishing_governance_program.md) | Operating model, RACI, phased rollout with Collibra onboarding, meeting cadence |
| 03 | [Standards](./03_data_governance_standards.md) | Naming, classification, DQ rules, access, lifecycle standards |
| 04 | [2nd Line of Defense Strategy](./04_2nd_line_of_defense_strategy.md) | Oversight model, Collibra-sourced audit framework, escalation matrix, maturity scoring |
| 05 | [KPIs & Benchmarking](./05_kpis_and_benchmarking.md) | Full KPI registry, scorecard, Python collector (Collibra API + Snowflake), benchmarks |
| 06 | [Configuration & Change Management](./06_configuration_and_change_management.md) | **Executive guide** + governance-as-code, Collibra integration, CI/CD, CAB templates |
| 07 | [Ground-Up Strategy](./07_ground_up_strategy.md) | CDO vision, 2-year roadmap, Collibra architecture, federated model, quick wins |

---

## Technology Stack

| Layer | Platform | Role |
|---|---|---|
| **Governance Control Plane** | Collibra Data Intelligence Cloud | Central catalog, glossary, workflows, DQ, lineage, access governance |
| **Data Warehouse** | Snowflake | Data storage + technical enforcement (RBAC, masking, row policies, tagging) |
| **Data Lakehouse** | Databricks (Unity Catalog) | Analytics + ML data with Unity Catalog governance enforcement |
| **Governance Config** | Git (YAML) | Version-controlled source of truth for all governance rules |
| **DQ Supplementary** | Great Expectations / dbt tests | Pipeline-layer quality gates feeding results to Collibra |
| **Orchestration** | Airflow / CI/CD (GitHub Actions) | Automated deployment and KPI collection |

---

## Key Design Conventions

- **Collibra is the human-facing governance layer** — stewards, owners, and executives work here
- **Snowflake and Databricks are the enforcement layer** — Collibra decisions are pushed down via API and native connectors
- **All rules are YAML-driven** — edit config, not code; version-controlled in Git
- **Python scripts use a class-based, config-injected pattern** — reusable across environments
- **Document 06 is written in two parts** — an executive-friendly business guide (Part A) and a technical implementation guide (Part B)
- **KPIs are collected from both Collibra API and Snowflake** — no manual spreadsheets

---

## Domain Coverage (Planned)

| Domain | Status |
|---|---|
| ✅ Data Governance | Complete (v2.0 — includes Collibra) |
| 🔜 Data Engineering | Planned |
| 🔜 Business Intelligence | Planned |
| 🔜 Machine Learning | Planned |

---

*Maintained by: Data Governance Office | CDO Sponsor: Chief Data Officer*
