# Data Quality Standards
## Domain README: Document Index and Navigation Guide

**Domain Owner:** Chief Data Office, Data Engineering
**Platform:** dbt · Great Expectations · Snowflake · Databricks · GitHub Actions
**Version:** 1.0 | **Last Updated:** 2026-11
**Classification:** Internal: Program Reference

> **Purpose:** This series holds the implementation guides for data quality rules referenced in the Data Governance and Data Engineering standards. It shows how to build a test suite, how to use dbt tests well, and how to run data quality checks in CI/CD with result storage and observability. The series is numbered 06 to 08 and has no documents 01 to 05. The policies and thresholds live in the Governance and Engineering standards.

---

## Document Index

| # | Document | Version | Status | Primary Audience |
|---|---|---|---|---|
| 06 | `06_DQ_Complete_Suite_Builder.md` | 1.0 | ✅ Active | Engineers new to data test automation |
| 07 | `07_DQ_dbt_Testing_Deep_Dive.md` | 1.0 | ✅ Active | Analytics engineers, dbt developers |
| 08 | `08_DQ_CICD_and_Observability.md` | 1.0 | ✅ Active | Data engineers, platform engineers |

## Quick Navigation

| You need to... | Start here |
|---|---|
| Build a first data test suite from nothing | `06_DQ_Complete_Suite_Builder.md` |
| Choose dbt tests, packages, and severity levels | `07_DQ_dbt_Testing_Deep_Dive.md` |
| Run checks in CI/CD, store results, and alert on SLA breaches | `08_DQ_CICD_and_Observability.md` |
| Find the rule definitions and thresholds | `03_data_governance_standards.md` and `03_DE_Standards.md` |

## Cross-Domain Dependencies

| Related document | Relationship |
|---|---|
| `03_data_governance_standards.md` | Defines data quality rules and criticality classes |
| `01_DE_Best_Practices.md` | Defines the medallion layers where checks run |
| `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | Uses data quality results as a certification gate |
| `AI_FIRST_STRATEGY_ADDENDUM.md` | Treats data quality gates as readiness criteria before agents consume data |

---

*Maintained by: Chief Data Office | Last reviewed: 2026-11*
