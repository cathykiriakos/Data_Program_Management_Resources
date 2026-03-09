# Data Product Certification Framework
## Enterprise Standards for Certified Data Across All Layers, Platforms, and Domains

**Document Owner:** Chief Data Officer + Data Governance Office
**Classification:** Internal — Binding Standard
**Version:** 1.0 | **Last Updated:** 2026-03
**Review Cycle:** Annual or upon major platform change

> **Scope:** This framework governs the certification of all data products across ETL platforms (Databricks, SQL Server, Snowflake), all medallion layers (Bronze, Silver, Gold), the semantic layer (dbt), and all consumption surfaces (Power BI, Tableau, Databricks AI/BI). It defines what a certified data product is, what it requires, how it is certified, and how it is sustained.

---

## Table of Contents

1. [What Is a Data Product?](#1-what-is-a-data-product)
2. [Certification Tiers](#2-certification-tiers)
3. [The Five Pillars of Certification](#3-the-five-pillars-of-certification)
4. [Certification Requirements by Layer](#4-certification-requirements-by-layer)
5. [Certification Requirements by Platform](#5-certification-requirements-by-platform)
6. [Certification Requirements by Consumption Surface](#6-certification-requirements-by-consumption-surface)
7. [Certification Process — End to End](#7-certification-process--end-to-end)
8. [Data Contract Standard](#8-data-contract-standard)
9. [Lineage Requirements](#9-lineage-requirements)
10. [Ownership and Stewardship Requirements](#10-ownership-and-stewardship-requirements)
11. [SLA Standards](#11-sla-standards)
12. [Decertification and Deprecation](#12-decertification-and-deprecation)
13. [Certification Automation — Python Framework](#13-certification-automation--python-framework)
14. [YAML Configuration](#14-yaml-configuration)
15. [Collibra Integration](#15-collibra-integration)
16. [Certification Register and KPIs](#16-certification-register-and-kpis)

---

## 1. What Is a Data Product?

A **data product** is any data asset — table, view, dataset, report, model, API, or feature set — that is intentionally produced to serve one or more data consumers. It has a defined producer, a defined consumer (or consumer class), a documented contract, and an owner accountable for its quality and fitness for purpose.

### 1.1 Data Product Types

| Product Type | Examples | Layers |
|---|---|---|
| **Pipeline Table** | Bronze ingested table, Silver cleansed entity, Gold fact/dimension | Bronze, Silver, Gold |
| **Semantic Metric** | dbt metric, calculated measure, KPI definition | Semantic Layer |
| **BI Dataset / Report** | Power BI certified dataset, Tableau published data source, certified workbook | BI Surface |
| **Feature Set** | Databricks Feature Store feature table for ML consumption | Gold / Feature Store |
| **API / Data Share** | Snowflake Data Share, Databricks Delta Sharing endpoint | Cross-domain |

### 1.2 What Certification Means

Certification is a formal attestation by the Data Governance Office and the owning domain that a data product meets all required standards across five pillars: **Ownership, Data Quality, Lineage, Access Control, and SLA**. Certified data products are discoverable in the data catalog, trustworthy for business decisions, and auditable by regulators.

> **Uncertified data must never be used as the basis for regulated reporting, financial decisions, or ML model training without a formal exception documented in Collibra.**

### 1.3 The Certification Hierarchy

```
TIER 1 — CRITICAL (T1)
  Regulatory reporting, executive KPIs, T1 ML model features
  Strictest controls. CDO sign-off required. Monthly 1LOD review.

TIER 2 — GOVERNED (T2)
  Department-wide reporting, operational KPIs, T2 ML features
  Standard controls. Domain owner sign-off. Quarterly review.

TIER 3 — MANAGED (T3)
  Team-level analytics, ad hoc exploration, exploratory ML
  Baseline controls. Self-certified by domain steward. Annual review.

TIER 4 — SANDBOX (T4)
  Experimental, development only, not for production decisions
  Governance-lite. No certification required. 90-day auto-expiry.
```

---

## 2. Certification Tiers

### 2.1 Tier Definitions and Entry Criteria

| Criterion | T1 Critical | T2 Governed | T3 Managed | T4 Sandbox |
|---|---|---|---|---|
| **Use case** | Regulatory, financial, executive, T1 ML | Operational, departmental, T2 ML | Team, ad hoc, exploratory | Dev/experiments only |
| **Consumer scope** | Organization-wide / Regulatory | Domain-wide | Team / individual | Creator only |
| **DQ gate threshold** | 100% CRITICAL + HIGH pass | 100% CRITICAL pass | 100% CRITICAL pass | Best effort |
| **Lineage** | Full end-to-end documented | Source-to-Gold documented | Immediate upstream documented | Not required |
| **Data contract** | Required; versioned; consumer-signed | Required; versioned | Lightweight contract | Not required |
| **Access control** | RBAC + column masking + row policies | RBAC + column masking | RBAC | Workspace isolation |
| **Owner** | Named individual; executive-backed | Named individual | Named individual | Creator |
| **Review cadence** | Monthly 1LOD + Semi-annual 2LOD | Quarterly | Annual | None |
| **CDO sign-off** | Required | Not required | Not required | Not required |
| **Collibra registration** | Mandatory | Mandatory | Mandatory | Recommended |
| **Change management** | Major change ticket + CAB | Minor change ticket | Standard change | Self-service |

### 2.2 Tier Assignment Decision Tree

```
Is this data used in regulatory reporting or financial statements?
  YES → T1

Is this data used in a T1 ML model as an input feature?
  YES → T1

Is this data used to make decisions affecting more than one department?
  YES → T1 or T2 (assess materiality with CDO)

Is this data used operationally across an entire business domain?
  YES → T2

Is this data used within a single team for regular reporting?
  YES → T3

Is this a development, prototype, or exploratory asset?
  YES → T4
```

---

## 3. The Five Pillars of Certification

Every certified data product must satisfy all five pillars at the level appropriate to its tier. No data product may be certified if any mandatory pillar requirement is unmet.

```
1. OWNERSHIP        Named owner + steward + custodian; governance chain documented
2. DATA QUALITY     DQ rules defined, automated, and passing
3. LINEAGE          Source-to-consumption trace documented in Collibra
4. ACCESS CONTROL   RBAC, column masking, row policies enforced
5. SLA              Freshness, availability, breach response documented
```

### 3.1 Pillar 1 — Ownership

A data product without a named, accountable owner cannot be certified. Ownership is not a team — it is an individual.

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Named Data Owner (business accountability) | Required | Required | Required |
| Named Data Steward (operational accountability) | Required | Required | Required |
| Named Data Custodian (technical accountability) | Required | Required | Recommended |
| Executive sponsor (CDO or Domain VP) | Required | Not required | Not required |
| Owner registered in Collibra | Required | Required | Required |
| Backup owner designated | Required | Recommended | Not required |
| Owner acknowledgment on data contract | Required | Required | Lightweight |

**Ownership definitions:**

| Role | Accountable For | Typical Person |
|---|---|---|
| **Data Owner** | Business accuracy; certification decision; escalation | Finance Controller, Sales VP, Domain Director |
| **Data Steward** | Day-to-day quality; DQ rules; access certifications; metadata | Analytics Lead, Senior Analyst, DGO Analyst |
| **Data Custodian** | Technical implementation; pipeline health; schema management | Senior Data Engineer, Analytics Engineer |

### 3.2 Pillar 2 — Data Quality

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| DQ rules registered in Collibra DQ (YAML registry) | Required | Required | Required |
| Automated DQ gate in CI/CD pipeline | Required | Required | Recommended |
| CRITICAL failures block pipeline promotion | Required | Required | Required |
| DQ pass rate threshold for certification | 100% CRITICAL+HIGH | 100% CRITICAL | 100% CRITICAL |
| DQ score published in Collibra catalog | Required | Required | Recommended |
| DQ trend (30-day) documented | Required | Recommended | Not required |
| Anomaly / statistical distribution tests | Required | Recommended | Not required |
| CRITICAL breach resolution SLA | 2 hours | 4 hours | 1 business day |

**Required DQ dimensions by layer:**

| DQ Dimension | Bronze | Silver | Gold | Semantic |
|---|---|---|---|---|
| Completeness (not null on key cols) | Required | Required | Required | Required |
| Freshness (row count > 0 after schedule) | Required | Required | Required | Required |
| Schema validity | Required | Required | Required | Required |
| Primary key uniqueness | — | Required | Required | Required |
| Referential integrity | — | Required | Required | — |
| Value range / business rules | — | Required | Required | Required |
| Volume anomaly detection | — | Recommended | T1 required | T1 required |
| Statistical distribution tests | — | — | T1 required | T1 required |
| Cross-system reconciliation | — | — | T1 required | T1 required |

### 3.3 Pillar 3 — Lineage

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Source system documented in Collibra | Required | Required | Required |
| Table-level lineage in Collibra | Required | Required | Recommended |
| Column-level lineage for key metrics | Required | Recommended | Not required |
| dbt lineage graph published | Required | Required | Recommended |
| BI report lineage linked to dataset | Required | Required | Recommended |
| ML feature lineage from feature to model | Required | Required | Not applicable |
| Lineage covers full chain (source to consumption) | Required | Source to Gold | Immediate upstream |
| Lineage reviewed and attested annually | Required | Required | Not required |

### 3.4 Pillar 4 — Access Control

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| RBAC roles defined and applied | Required | Required | Required |
| Column-level masking on PII/sensitive columns | Required | Required | Required |
| Row-level access policies (if multi-tenant) | Required | If applicable | If applicable |
| No shared credentials / service accounts | Required | Required | Required |
| Access certification cycle | Quarterly | Quarterly | Annual |
| Data Usage Agreement for Restricted data | Required | Required | Required |
| Audit logging of all access events | Required | Required | Required |
| BI RLS validated by persona testing | Required | Required | Recommended |

### 3.5 Pillar 5 — SLA

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Freshness SLA defined and documented | Required | Required | Required |
| Availability SLA defined | Required | Recommended | Not required |
| SLA monitoring automated with alerting | Required | Required | Recommended |
| SLA breach incident response documented | Required | Required | Best effort |
| Consumer SLA agreement signed | Required | Required | Lightweight |
| SLA performance tracked in KPI scorecard | Required | Monthly | Not required |

---

## 4. Certification Requirements by Layer

### 4.1 Bronze Layer

Bronze is the raw landing zone. Bronze tables are infrastructure, not consumer-facing products. They must meet **platform standards** before Silver can be certified on top of them.

**Bronze Minimum Standards:**

```yaml
# bronze_certification_checklist.yaml
bronze_standards:
  ingestion:
    - registered_in_catalog: true
    - source_system_documented: true
    - ingestion_method_documented: true   # Fivetran / Airbyte / custom Python
    - ingestion_frequency_documented: true

  schema:
    - schema_defined_in_dbt_or_yaml: true
    - evolution_policy_documented: true   # Breaking / additive change handling
    - audit_columns_present:
        - _ingested_at
        - _source_system
        - _batch_id

  data_quality:
    - not_null_on_pk_columns: CRITICAL
    - row_count_greater_than_zero: CRITICAL
    - freshness_check_against_sla: HIGH
    - schema_validation: HIGH

  access:
    - restricted_to_engineering_roles: true  # No business user direct access to Bronze
    - pii_columns_tagged: true               # Classification at landing, not downstream
    - masking_applied_if_pii_present: true

  metadata:
    - business_description_in_catalog: required
    - data_owner_assigned: required
    - classification_applied: required
    - retention_policy_documented: required
```

**Bronze-to-Silver Promotion Gate (SQL):**

```sql
-- All checks must PASS before Silver transformation is permitted

SELECT
    'bronze_freshness'          AS check_name,
    CASE WHEN MAX(_ingested_at) >= CURRENT_TIMESTAMP() - INTERVAL '25 hours'
         THEN 'PASS' ELSE 'FAIL' END AS result,
    MAX(_ingested_at)::VARCHAR   AS detail,
    'CRITICAL'                   AS severity
FROM {bronze_table}

UNION ALL

SELECT
    'bronze_row_count',
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END,
    COUNT(*)::VARCHAR || ' rows',
    'CRITICAL'
FROM {bronze_table}

UNION ALL

SELECT
    'bronze_pk_nulls',
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END,
    COUNT(*)::VARCHAR || ' null PKs found',
    'CRITICAL'
FROM {bronze_table}
WHERE {pk_column} IS NULL;
```

### 4.2 Silver Layer

Silver is the cleansed, typed, deduplicated, and PII-masked layer. Silver certification is an engineering gate that requires DGO review of PII handling before Gold is permitted to build on top.

**Silver Certification Requirements:**

| Requirement | Status |
|---|---|
| All Bronze dependencies meet minimum standards | Required |
| Column data types explicitly defined (no implicit VARCHAR catch-all) | Required |
| Nullability rules documented for every column | Required |
| PII columns tagged AND masking policy applied | Required |
| Deduplication logic documented and tested | Required |
| SCD2 pattern applied for slowly-changing entities | Required for entity tables |
| Referential integrity tests automated | Required |
| Silver DQ pass rate >= 99% on CRITICAL rules for 7 consecutive days | Required before Gold certifies |
| Data Custodian sign-off | Required |
| DGO PII review | Required |

**Silver DQ YAML Config:**

```yaml
# dq_config/silver/finance/gl_transactions_clean.yaml
silver_dq:
  table: "prod_finance_silver.erp.gl_transactions_clean"
  owner: "finance-data-engineering@company.com"
  tier: "Silver"

  rules:
    - rule_id: "SLV-FIN-001"
      column: "transaction_id"
      check: "unique_and_not_null"
      severity: "CRITICAL"

    - rule_id: "SLV-FIN-002"
      column: "amount_usd"
      check: "not_null"
      severity: "CRITICAL"

    - rule_id: "SLV-FIN-003"
      column: "transaction_date"
      check: "not_future_dated"
      threshold_days: 1
      severity: "HIGH"

    - rule_id: "SLV-FIN-004"
      check: "row_count_variance_vs_prior_day"
      max_variance_pct: 30
      severity: "HIGH"

    - rule_id: "SLV-FIN-005"
      check: "referential_integrity"
      fk_column: "customer_id"
      ref_table: "prod_customer_silver.erp.customers_clean"
      ref_column: "customer_id"
      severity: "HIGH"

  sla:
    freshness_hours: 6
    availability_pct: 99.5
```

### 4.3 Gold Layer

Gold is the primary certification layer. Gold objects represent business concepts, are optimized for consumption, and carry the full weight of all five certification pillars.

**Gold Certification Checklist (T1):**

```
OWNERSHIP PILLAR
  [ ] Data Owner identified and registered in Collibra
  [ ] Data Steward identified and registered in Collibra
  [ ] Data Custodian identified and registered in Collibra
  [ ] Executive sponsor confirmed (CDO or Domain VP)
  [ ] Backup owner designated

DATA QUALITY PILLAR
  [ ] All DQ rules in Collibra DQ YAML registry
  [ ] Automated DQ gate in CI/CD pipeline
  [ ] 30-day DQ pass rate >= 99.5% on CRITICAL rules
  [ ] 30-day DQ pass rate >= 97% on HIGH rules
  [ ] Anomaly detection configured and alerting
  [ ] Cross-system reconciliation query defined and passing

LINEAGE PILLAR
  [ ] Full source-to-Gold lineage documented in Collibra
  [ ] Column-level lineage for all key business metrics
  [ ] dbt lineage graph published and current
  [ ] All source systems identified and documented

ACCESS CONTROL PILLAR
  [ ] RBAC roles defined per classification tier
  [ ] Column masking policies applied to all PII/sensitive columns
  [ ] Row-level access policies applied (if dataset is multi-tenant)
  [ ] Access certification completed within last 90 days
  [ ] No users with access not justified by current business role

SLA PILLAR
  [ ] Freshness SLA defined and documented in Collibra
  [ ] Availability SLA defined (99.5% minimum for T1)
  [ ] Automated SLA monitoring with alert routing configured
  [ ] SLA breach runbook exists (links to Incident Response Playbook)
  [ ] Consumer SLA agreement signed by all T1/T2 consumer leads

DATA CONTRACT
  [ ] Data contract YAML file authored and committed to Git
  [ ] Contract signed by producer (Data Custodian)
  [ ] Contract signed by all T1/T2 consumer teams
  [ ] Breaking change notification policy documented (14 days minimum for T1)
  [ ] Schema version documented

COLLIBRA REGISTRATION
  [ ] Asset registered in Collibra catalog
  [ ] All required metadata fields populated (see Section 15)
  [ ] Business Glossary terms linked to key columns
  [ ] Certification status set to "Certified" in Collibra
  [ ] Review date set
```

### 4.4 Semantic Layer

The semantic layer is the contract between the data platform and BI/ML consumers. Incorrect metric definitions propagate to all downstream consumers simultaneously, making this the highest-leverage layer for quality control.

**Semantic Layer Certification Requirements:**

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Metric definition in dbt metrics or platform semantic model | Required | Required | Required |
| Business definition linked to Collibra glossary term | Required | Required | Recommended |
| Metric sourced from a single certified Gold table | Required | Required | Required |
| Duplicate metric detection scan passed | Required | Required | Required |
| Metric approved by owning domain data owner | Required | Required | Steward only |
| Expected value range test validated | Required | Required | Required |
| Consistency test vs. prior certified version | Required | Recommended | Not required |
| Documentation: time grains, dimensions, filters, nullability | Required | Required | Required |

**dbt Metric Certification Example:**

```yaml
# models/semantic/finance/_finance_metrics.yml
version: 2

metrics:
  - name: gross_revenue
    label: "Gross Revenue"
    description: >
      Total pre-discount, pre-tax revenue in USD.
      Source: prod_finance_gold.finance.fact_revenue.
      Excludes void transactions (is_voided = false).
      CERTIFIED T1 — Finance Domain Owner sign-off required before modifying.
    model: ref('fact_revenue')
    type: sum
    sql: gross_revenue_usd
    timestamp: transaction_date
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - customer_segment
      - product_category
      - sales_region
    filters:
      - field: is_voided
        operator: "="
        value: "false"
    meta:
      tier: "T1"
      owner: "finance-data@company.com"
      steward: "jane.smith@company.com"
      domain: "Finance"
      collibra_asset_id: "clb-metric-gross-revenue-001"
      certified_date: "2026-03-01"
      certified_by: "DGO + Finance Controller"
      review_date: "2026-09-01"
      breaking_change_notice_days: 14
      glossary_term: "Gross Revenue"
```

**Duplicate Metric Detection SQL:**

```sql
-- Run before certifying any new semantic metric.
-- Any result requires Governance Council resolution before certification proceeds.
SELECT
    m1.metric_name         AS candidate_metric,
    m2.metric_name         AS existing_certified_metric,
    m1.source_table        AS candidate_source,
    m2.source_table        AS existing_source
FROM semantic_catalog.metrics m1
CROSS JOIN semantic_catalog.metrics m2
WHERE m1.metric_name        != m2.metric_name
  AND m2.certified           = TRUE
  AND m1.source_table        = m2.source_table
  AND m1.source_column       = m2.source_column
  AND m1.aggregation_type    = m2.aggregation_type
  AND m1.filter_expression   IS NOT DISTINCT FROM m2.filter_expression
ORDER BY m1.metric_name;
```

---

## 5. Certification Requirements by Platform

### 5.1 Snowflake

**Required object tagging before certification is granted:**

```sql
-- Every certified Gold table must carry all required tags
ALTER TABLE {certified_table}
    SET TAG governance.data_tier               = 'T1',
            governance.classification_tier     = 'CONFIDENTIAL',
            governance.domain                  = 'FINANCE',
            governance.data_owner              = 'jane.smith@company.com',
            governance.steward                 = 'john.doe@company.com',
            governance.certified_date          = '2026-03-01',
            governance.review_date             = '2026-09-01',
            governance.sla_freshness_hours     = '6',
            governance.collibra_asset_id       = 'clb-fin-001';

-- Column masking validation — must return zero rows to proceed
SELECT
    c.table_name, c.column_name,
    tv.tag_value                        AS pii_type,
    pm.masking_policy_name,
    'MISSING MASK — BLOCKS CERTIFICATION' AS status
FROM snowflake.account_usage.columns c
JOIN snowflake.account_usage.tag_references tv
    ON  tv.object_name   = c.table_name
    AND tv.column_name   = c.column_name
    AND tv.tag_name      = 'PII_TYPE'
    AND tv.tag_value    != 'NONE'
LEFT JOIN snowflake.account_usage.policy_references pr
    ON  pr.ref_entity_name = c.table_name
    AND pr.ref_column_name = c.column_name
LEFT JOIN snowflake.account_usage.masking_policies pm
    ON  pm.policy_name = pr.policy_name
WHERE c.table_catalog      = 'PROD_FINANCE_GOLD'
  AND pm.masking_policy_name IS NULL;

-- Time Travel configuration per classification
ALTER TABLE {certified_table}
    SET DATA_RETENTION_TIME_IN_DAYS = 90;   -- CONFIDENTIAL = 90 days
```

**Snowflake Certification Validation Query:**

```sql
WITH tag_summary AS (
    SELECT
        t.table_name,
        MAX(CASE WHEN tv.tag_name = 'DATA_TIER'           THEN tv.tag_value END) AS data_tier,
        MAX(CASE WHEN tv.tag_name = 'CLASSIFICATION_TIER' THEN tv.tag_value END) AS classification,
        MAX(CASE WHEN tv.tag_name = 'DATA_OWNER'          THEN tv.tag_value END) AS data_owner,
        MAX(CASE WHEN tv.tag_name = 'STEWARD'             THEN tv.tag_value END) AS steward,
        MAX(CASE WHEN tv.tag_name = 'SLA_FRESHNESS_HOURS' THEN tv.tag_value END) AS sla_hours,
        MAX(CASE WHEN tv.tag_name = 'COLLIBRA_ASSET_ID'   THEN tv.tag_value END) AS collibra_id
    FROM snowflake.account_usage.tables t
    LEFT JOIN snowflake.account_usage.tag_references tv
        ON tv.object_name = t.table_name AND tv.object_database = t.table_catalog
    WHERE t.table_catalog = 'PROD_FINANCE_GOLD'
    GROUP BY 1
)
SELECT
    table_name,
    CASE WHEN data_tier      IS NULL THEN 'FAIL: data_tier missing'      ELSE 'OK' END AS tier_check,
    CASE WHEN classification IS NULL THEN 'FAIL: classification missing' ELSE 'OK' END AS class_check,
    CASE WHEN data_owner     IS NULL THEN 'FAIL: data_owner missing'     ELSE 'OK' END AS owner_check,
    CASE WHEN steward        IS NULL THEN 'FAIL: steward missing'        ELSE 'OK' END AS steward_check,
    CASE WHEN sla_hours      IS NULL THEN 'FAIL: sla_freshness missing'  ELSE 'OK' END AS sla_check,
    CASE WHEN collibra_id    IS NULL THEN 'FAIL: collibra_asset_id missing' ELSE 'OK' END AS collibra_check,
    CASE WHEN data_tier IS NOT NULL AND classification IS NOT NULL
          AND data_owner IS NOT NULL AND steward IS NOT NULL
          AND sla_hours IS NOT NULL AND collibra_id IS NOT NULL
         THEN 'CERTIFIED — all tags present'
         ELSE 'BLOCKED — tags incomplete' END AS overall_status
FROM tag_summary
ORDER BY overall_status DESC;
```

### 5.2 Databricks / Unity Catalog

**Python certifier for Databricks Unity Catalog:**

```python
# databricks_certifier.py
"""
Applies certification metadata to Databricks Unity Catalog tables.
Config-driven via YAML. Uses the Databricks SDK.
"""

import yaml
from dataclasses import dataclass
from databricks.sdk import WorkspaceClient


@dataclass
class DatabricksCertificationConfig:
    catalog: str
    schema: str
    table: str
    tier: str                     # T1 / T2 / T3
    classification: str           # RESTRICTED / CONFIDENTIAL / INTERNAL / PUBLIC
    domain: str
    data_owner: str
    steward: str
    custodian: str
    sla_freshness_hours: int
    collibra_asset_id: str
    certified_date: str
    review_date: str

    @classmethod
    def from_yaml(cls, path: str) -> "DatabricksCertificationConfig":
        with open(path) as f:
            return cls(**yaml.safe_load(f)["certification"])


class DatabricksCertifier:
    """Applies and validates certification properties on Unity Catalog tables."""

    def __init__(self, workspace_url: str, token: str):
        self.client = WorkspaceClient(host=workspace_url, token=token)

    def certify_table(self, config: DatabricksCertificationConfig) -> dict:
        full_name = f"{config.catalog}.{config.schema}.{config.table}"

        props = {
            "data_tier":            config.tier,
            "classification":       config.classification,
            "domain":               config.domain,
            "data_owner":           config.data_owner,
            "steward":              config.steward,
            "custodian":            config.custodian,
            "sla_freshness_hours":  str(config.sla_freshness_hours),
            "collibra_asset_id":    config.collibra_asset_id,
            "certified_date":       config.certified_date,
            "review_date":          config.review_date,
            "certification_status": "CERTIFIED",
        }

        self.client.tables.update(full_name=full_name, properties=props)
        mask_results = self._validate_column_masks(full_name)

        return {
            "table": full_name,
            "tier":  config.tier,
            "properties_applied": list(props.keys()),
            "column_mask_status": mask_results,
            "certified": all(r["mask_applied"] for r in mask_results if r.get("pii")),
        }

    def validate_certification(self, full_table_name: str) -> dict:
        table_info  = self.client.tables.get(full_table_name)
        props       = table_info.properties or {}
        required    = ["data_tier", "classification", "domain",
                       "data_owner", "steward", "sla_freshness_hours", "certification_status"]
        missing     = [p for p in required if p not in props]
        return {
            "table":              full_table_name,
            "certified":          len(missing) == 0,
            "missing_properties": missing,
        }

    def _validate_column_masks(self, full_name: str) -> list:
        table_info = self.client.tables.get(full_name)
        results    = []
        for col in (table_info.columns or []):
            tags     = getattr(col, "tags", {}) or {}
            pii_type = tags.get("pii_type", "NONE")
            if pii_type != "NONE":
                has_mask = getattr(col, "mask", None) is not None
                results.append({
                    "column":     col.name,
                    "pii_type":   pii_type,
                    "pii":        True,
                    "mask_applied": has_mask,
                    "status": "OK" if has_mask else "FAIL — mask missing, blocks certification",
                })
        return results
```

**Unity Catalog column masks and row filters:**

```sql
-- Column mask for PII (Databricks)
CREATE FUNCTION governance.mask_email(email STRING)
    RETURNS STRING
    RETURN CASE
        WHEN is_account_group_member('restricted_data_users') THEN email
        ELSE REGEXP_REPLACE(email, '.+@', '***@')
    END;

ALTER TABLE prod_finance_gold.finance.dim_customer
    ALTER COLUMN email SET MASK governance.mask_email;

-- Row filter for multi-tenant datasets
CREATE FUNCTION governance.rls_region_filter(region STRING)
    RETURNS BOOLEAN
    RETURN is_account_group_member(CONCAT('region_', LOWER(region)));

ALTER TABLE prod_sales_gold.sales.fact_opportunities
    SET ROW FILTER governance.rls_region_filter ON (sales_region);
```

### 5.3 SQL Server (Source / Legacy ETL)

SQL Server is typically a source or legacy ETL staging layer. Certification applies to the downstream Snowflake/Databricks destination, but source hygiene is required before Silver can certify.

**Source documentation query (run before ingestion setup):**

```sql
-- Run against SQL Server source to document columns, types, and PKs
-- Output populates the Bronze asset's Collibra metadata
SELECT
    s.name                                     AS schema_name,
    t.name                                     AS table_name,
    c.name                                     AS column_name,
    tp.name                                    AS data_type,
    c.is_nullable,
    ep.value                                   AS column_description,
    CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS is_primary_key
FROM sys.tables t
JOIN sys.schemas s   ON s.schema_id = t.schema_id
JOIN sys.columns c   ON c.object_id = t.object_id
JOIN sys.types tp    ON tp.user_type_id = c.user_type_id
LEFT JOIN sys.extended_properties ep
    ON ep.major_id = c.object_id AND ep.minor_id = c.column_id
    AND ep.name = 'MS_Description'
LEFT JOIN (
    SELECT ic.object_id, ic.column_id
    FROM sys.index_columns ic
    JOIN sys.indexes i ON i.object_id = ic.object_id AND i.is_primary_key = 1
) pk ON pk.object_id = c.object_id AND pk.column_id = c.column_id
WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
ORDER BY s.name, t.name, c.column_id;
```

**SQL Server pre-ingestion validation gate (Python):**

```python
# sqlserver_ingestion_gate.py

import pyodbc
import yaml
from dataclasses import dataclass
from typing import Any


@dataclass
class SourceValidationResult:
    check_name: str
    passed: bool
    severity: str
    detail: str


class SQLServerSourceGate:
    """Validates SQL Server source data before Bronze ingestion.
    All checks are config-driven from YAML — no hardcoded thresholds."""

    def __init__(self, connection_string: str, config_path: str):
        self.conn = pyodbc.connect(connection_string)
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def run_pre_ingestion_checks(self) -> list[SourceValidationResult]:
        return [self._run_check(c) for c in self.config.get("pre_ingestion_checks", [])]

    def _run_check(self, check: dict) -> SourceValidationResult:
        cursor = self.conn.cursor()
        cursor.execute(check["sql"])
        value  = cursor.fetchone()[0]
        passed = self._evaluate(value, check["condition"], check.get("threshold"))
        return SourceValidationResult(
            check_name=check["name"],
            passed=passed,
            severity=check["severity"],
            detail=f"Value: {value} | Condition: {check['condition']} {check.get('threshold', '')}",
        )

    def _evaluate(self, value: Any, condition: str, threshold: Any) -> bool:
        ops = {
            "greater_than": lambda v, t: v > t,
            "equals":       lambda v, t: v == t,
            "not_null":     lambda v, _: v is not None,
            "less_than":    lambda v, t: v < t,
        }
        return ops.get(condition, lambda *_: False)(value, threshold)
```

---

## 6. Certification Requirements by Consumption Surface

### 6.1 Power BI

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Connects only to Gold / semantic layer (no Bronze/Silver direct) | Required | Required | Required |
| Certified dataset endorsement applied in Power BI | Required | Required | Promoted endorsement only |
| Row-Level Security (RLS) configured and persona-tested | Required | Required | If sensitive data |
| Report registered in BI Report Registry | Required | Required | Recommended |
| Published via deployment pipeline (not manual publish) | Required | Required | Not required |
| Sensitivity label applied per data classification | Required | Required | Required |
| Scheduled refresh SLA configured and monitored | Required | Required | Recommended |
| Audit logging via Power BI Admin API | Required | Required | Required |
| Lineage from report to data source documented | Required | Required | Recommended |

**Power BI RLS Validation Script:**

```python
# powerbi_rls_validator.py
"""
Tests Power BI RLS configurations against expected row counts per persona.
Run as part of the T1/T2 certification gate — a failing RLS test blocks certification.
"""

import requests
from dataclasses import dataclass
import yaml


@dataclass
class RLSTestResult:
    role_name: str
    test_persona: str
    expected_range: tuple
    actual_row_count: int
    passed: bool
    detail: str


class PowerBIRLSValidator:

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, config_path: str):
        self.token   = self._get_token(tenant_id, client_id, client_secret)
        self.headers = {"Authorization": f"Bearer {self.token}"}
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def validate_dataset_rls(self, dataset_id: str) -> list[RLSTestResult]:
        return [self._test_role(dataset_id, t) for t in self.config.get("rls_tests", [])]

    def _test_role(self, dataset_id: str, role_test: dict) -> RLSTestResult:
        resp = requests.post(
            f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries",
            headers=self.headers,
            json={
                "queries": [{"query": role_test["dax_query"]}],
                "serializerSettings": {"includeNulls": True},
                "impersonatedUserName": role_test["test_user_email"],
            },
            timeout=30,
        )
        resp.raise_for_status()
        row_count   = resp.json()["results"][0]["tables"][0]["rows"][0].get("[RowCount]", 0)
        lo, hi      = role_test["expected_row_count_range"]
        passed      = lo <= row_count <= hi
        return RLSTestResult(
            role_name=role_test["role_name"],
            test_persona=role_test["test_user_email"],
            expected_range=(lo, hi),
            actual_row_count=row_count,
            passed=passed,
            detail=f"Count {row_count} {'within' if passed else 'OUTSIDE'} expected [{lo}, {hi}]",
        )

    def _get_token(self, tenant_id, client_id, client_secret) -> str:
        resp = requests.post(
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
            data={"grant_type": "client_credentials", "client_id": client_id,
                  "client_secret": client_secret,
                  "scope": "https://analysis.windows.net/powerbi/api/.default"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]
```

### 6.2 Tableau

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Published to Certified project (not default or ungoverned) | Required | Required | T3 project only |
| Certified data source badge applied via REST API | Required | Required | Not applicable |
| Connects only to Gold / semantic layer | Required | Required | Required |
| Published via CI/CD (REST API), not Desktop direct publish | Required | Required | Not required |
| Row-level security via user filters or VizQL data policy | Required | Required | If sensitive data |
| Named owner in Tableau Server | Required | Required | Required |
| Registered in BI Report Registry | Required | Required | Recommended |
| Usage metrics tracked (views, users) | Required | Required | Recommended |

**Tableau certification via REST API:**

```python
# tableau_certifier.py

import tableauserverclient as TSC
import yaml


class TableauCertifier:

    def __init__(self, server_url: str, site: str, token_name: str,
                 token_value: str, certified_project_name: str, config_path: str):
        self.server = TSC.Server(server_url, use_server_version=True)
        self.server.auth.sign_in(
            TSC.PersonalAccessTokenAuth(token_name, token_value, site)
        )
        self.certified_project_id = self._get_project_id(certified_project_name)
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def certify_datasource(self, datasource_name: str, owner_email: str) -> dict:
        ds = self._find_datasource(datasource_name)
        if not ds:
            raise ValueError(f"Datasource '{datasource_name}' not found in Tableau Server")

        ds.project_id         = self.certified_project_id
        ds.certified          = True
        ds.certification_note = (
            f"Certified {self.config.get('tier', 'T1')} — {owner_email} — "
            f"{self.config.get('certified_date', 'see Collibra')}"
        )
        self.server.datasources.update(ds)
        return {"datasource": datasource_name, "certified": True,
                "project_id": self.certified_project_id}

    def _find_datasource(self, name: str):
        req = TSC.RequestOptions()
        req.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                  TSC.RequestOptions.Operator.Equals, name))
        results, _ = self.server.datasources.get(req)
        return results[0] if results else None

    def _get_project_id(self, project_name: str) -> str:
        req = TSC.RequestOptions()
        req.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                  TSC.RequestOptions.Operator.Equals, project_name))
        projects, _ = self.server.projects.get(req)
        if not projects:
            raise ValueError(f"Certified project '{project_name}' not found")
        return projects[0].id
```

### 6.3 Databricks AI/BI (Genie / Lakehouse BI)

| Requirement | T1 | T2 | T3 |
|---|---|---|---|
| Space backed by a Unity Catalog certified Gold table | Required | Required | Required |
| Genie Space owner is a named individual | Required | Required | Required |
| Unity Catalog table-level ACLs applied | Required | Required | Required |
| Column masks applied for PII before Genie exposure | Required | Required | Required |
| AI/BI Dashboard registered in BI Report Registry | Required | Required | Recommended |
| Query history audit log enabled on workspace | Required | Required | Required |
| Certification metadata propagated from Unity Catalog | Required | Required | Required |

---

## 7. Certification Process — End to End

### 7.1 Process Overview

```
INITIATE          ASSESS           BUILD & VALIDATE      REVIEW & APPROVE       CERTIFY & PUBLISH
─────────         ──────           ────────────────       ─────────────          ─────────────────
Producer          DGO runs         Producer resolves      Domain Owner           DGO sets status
submits           pre-flight       all pillar gaps.       signs off.             to CERTIFIED in
certification     checklist        CI/CD gate must        CDO signs (T1).        Collibra.
request via       against all      pass. Evidence         DGO validates          Contract goes live.
Collibra          5 pillars.       package assembled.     completeness.          Consumers notified.
workflow.         Gaps returned                           2LOD scheduled.
                  to producer.
```

### 7.2 Stage 1 — Initiation

The producer (Data Custodian) submits a certification request by:

1. Opening a Collibra Workflow task of type `Data Product Certification Request`
2. Completing the certification request YAML (see Section 14) and committing to Git
3. Providing the initial evidence package location

**Collibra workflow trigger (API):**

```python
# collibra_certification_workflow.py
"""
Triggers a Collibra certification workflow for a data product.
Called by the CI/CD pipeline after all automated checks pass.
"""

import requests
from dataclasses import dataclass


@dataclass
class CertificationRequest:
    asset_id: str           # Collibra asset UUID
    tier: str               # T1 / T2 / T3
    domain: str
    custodian_email: str
    owner_email: str
    steward_email: str
    evidence_path: str      # Git path to evidence package


class CollibraWorkflowClient:

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.session  = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    def trigger_certification_workflow(self, req: CertificationRequest) -> dict:
        """Start the certification approval workflow for a data product asset."""
        payload = {
            "workflowDefinitionId": "data-product-certification-v1",
            "businessItemIds":      [req.asset_id],
            "formValues": {
                "tier":            req.tier,
                "domain":          req.domain,
                "custodianEmail":  req.custodian_email,
                "ownerEmail":      req.owner_email,
                "stewardEmail":    req.steward_email,
                "evidencePath":    req.evidence_path,
                "requestedBy":     req.custodian_email,
            },
        }
        resp = self.session.post(
            f"{self.base_url}/rest/2.0/workflowInstances",
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_certification_status(self, asset_id: str) -> str:
        """Return the current certification status of a Collibra asset."""
        resp = self.session.get(
            f"{self.base_url}/rest/2.0/assets/{asset_id}/attributes",
            params={"typePublicId": "certification_status"},
            timeout=30,
        )
        resp.raise_for_status()
        attrs = resp.json().get("results", [])
        return attrs[0]["value"]["value"] if attrs else "UNCERTIFIED"

    def set_certification_status(
        self, asset_id: str, status: str, reviewer_email: str
    ) -> None:
        """Set certification status and reviewer on a Collibra asset."""
        for attr_id, value in [
            ("certification_status", status),
            ("certified_by",        reviewer_email),
            ("certified_date",      __import__("datetime").date.today().isoformat()),
        ]:
            self.session.put(
                f"{self.base_url}/rest/2.0/assets/{asset_id}/attributes",
                json={"typePublicId": attr_id, "value": {"value": value}},
                timeout=30,
            )
```

### 7.3 Stage 2 — Pre-Flight Assessment

DGO runs the automated pre-flight checklist against all five pillars. Results are returned to the producer as a structured gap report.

```python
# preflight_assessor.py
"""
Automated pre-flight certification assessment across all five pillars.
Runs against Snowflake, Databricks, Collibra, and Git.
Returns a structured gap report that blocks or advances the workflow.
"""

import yaml
import snowflake.connector
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PillarResult:
    pillar: str
    checks_total: int
    checks_passed: int
    checks_failed: int
    gaps: list[dict] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.checks_failed == 0

    @property
    def pass_rate(self) -> float:
        return self.checks_passed / self.checks_total if self.checks_total else 0.0


@dataclass
class PreFlightReport:
    asset_id: str
    asset_name: str
    tier: str
    pillar_results: list[PillarResult]

    @property
    def certification_ready(self) -> bool:
        return all(p.passed for p in self.pillar_results)

    def to_dict(self) -> dict:
        return {
            "asset_id":             self.asset_id,
            "asset_name":           self.asset_name,
            "tier":                 self.tier,
            "certification_ready":  self.certification_ready,
            "pillars": [
                {
                    "pillar":         p.pillar,
                    "passed":         p.passed,
                    "pass_rate_pct":  round(p.pass_rate * 100, 1),
                    "gaps":           p.gaps,
                }
                for p in self.pillar_results
            ],
        }


class PreFlightAssessor:
    """
    Runs all five pillar checks for a data product certification request.
    Config-driven: tier-specific thresholds read from YAML.
    """

    def __init__(
        self,
        sf_conn: snowflake.connector.SnowflakeConnection,
        collibra_client,           # CollibraWorkflowClient
        config_path: str,
    ):
        self.sf_conn  = sf_conn
        self.collibra = collibra_client
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def assess(self, asset_id: str, table_fqn: str, tier: str) -> PreFlightReport:
        """Run all pillar checks and return a structured gap report."""
        asset_name = table_fqn.split(".")[-1]
        return PreFlightReport(
            asset_id=asset_id,
            asset_name=asset_name,
            tier=tier,
            pillar_results=[
                self._check_ownership(asset_id, tier),
                self._check_data_quality(table_fqn, tier),
                self._check_lineage(asset_id, tier),
                self._check_access_control(table_fqn, tier),
                self._check_sla(table_fqn, tier),
            ],
        )

    # ── Pillar 1: Ownership ───────────────────────────────────────

    def _check_ownership(self, asset_id: str, tier: str) -> PillarResult:
        gaps    = []
        checks  = 0
        passed  = 0

        # Check Collibra ownership attributes
        required_attrs = self.config["ownership_requirements"][tier]
        for attr in required_attrs:
            checks += 1
            status = self.collibra.get_certification_status(asset_id)
            # Simplified: real impl queries each attribute individually
            if status == "UNCERTIFIED":
                gaps.append({"attribute": attr, "issue": f"{attr} not set in Collibra"})
            else:
                passed += 1

        return PillarResult("Ownership", checks, passed, checks - passed, gaps)

    # ── Pillar 2: Data Quality ────────────────────────────────────

    def _check_data_quality(self, table_fqn: str, tier: str) -> PillarResult:
        gaps   = []
        checks = 0
        passed = 0

        thresholds = self.config["dq_thresholds"][tier]

        # Check 30-day CRITICAL pass rate
        cursor = self.sf_conn.cursor()
        checks += 1
        cursor.execute("""
            SELECT
                SUM(CASE WHEN passed THEN 1 ELSE 0 END) * 100.0
                    / NULLIF(COUNT(*), 0)           AS pass_rate_pct
            FROM data_quality.pipeline_test_results
            WHERE table_name  = %(table)s
              AND severity     = 'CRITICAL'
              AND run_date    >= CURRENT_DATE() - 30
        """, {"table": table_fqn})
        row      = cursor.fetchone()
        rate     = float(row[0]) if row and row[0] else 0.0
        threshold = thresholds["critical_pass_rate_pct"]
        if rate >= threshold:
            passed += 1
        else:
            gaps.append({
                "check":     "CRITICAL DQ pass rate",
                "actual":    f"{rate:.1f}%",
                "required":  f">= {threshold}%",
                "severity":  "BLOCKS_CERTIFICATION",
            })

        # Check that DQ rules exist in registry
        checks += 1
        cursor.execute("""
            SELECT COUNT(*) FROM data_quality.rules_registry
            WHERE table_name = %(table)s AND is_active = TRUE
        """, {"table": table_fqn})
        rule_count = cursor.fetchone()[0]
        if rule_count > 0:
            passed += 1
        else:
            gaps.append({
                "check":    "DQ rules in registry",
                "issue":    "No active DQ rules found — register rules before certifying",
                "severity": "BLOCKS_CERTIFICATION",
            })

        return PillarResult("Data Quality", checks, passed, checks - passed, gaps)

    # ── Pillar 3: Lineage ─────────────────────────────────────────

    def _check_lineage(self, asset_id: str, tier: str) -> PillarResult:
        gaps   = []
        checks = 0
        passed = 0

        lineage_req = self.config["lineage_requirements"][tier]

        # Check that lineage is documented in Collibra
        checks += 1
        resp = self.collibra.session.get(
            f"{self.collibra.base_url}/rest/2.0/assets/{asset_id}/relations",
            timeout=30,
        )
        relations = resp.json().get("results", []) if resp.ok else []
        has_lineage = any(
            r.get("type", {}).get("publicId") in ("sourceOf", "targetOf")
            for r in relations
        )
        if has_lineage:
            passed += 1
        else:
            gaps.append({
                "check":    "Collibra lineage relations",
                "issue":    "No lineage relations found in Collibra for this asset",
                "severity": "BLOCKS_CERTIFICATION",
            })

        return PillarResult("Lineage", checks, passed, checks - passed, gaps)

    # ── Pillar 4: Access Control ──────────────────────────────────

    def _check_access_control(self, table_fqn: str, tier: str) -> PillarResult:
        gaps   = []
        checks = 0
        passed = 0

        # Check PII columns all have masking policies
        cursor = self.sf_conn.cursor()
        checks += 1
        db, schema, table = table_fqn.split(".")
        cursor.execute("""
            SELECT COUNT(*) AS unmasked_pii_cols
            FROM snowflake.account_usage.columns c
            JOIN snowflake.account_usage.tag_references tv
                ON tv.object_name   = c.table_name
                AND tv.column_name  = c.column_name
                AND tv.tag_name     = 'PII_TYPE'
                AND tv.tag_value   != 'NONE'
            LEFT JOIN snowflake.account_usage.policy_references pr
                ON pr.ref_entity_name = c.table_name
                AND pr.ref_column_name = c.column_name
            WHERE c.table_catalog = %(db)s
              AND c.table_name    = %(table)s
              AND pr.policy_name  IS NULL
        """, {"db": db.upper(), "table": table.upper()})
        unmasked = cursor.fetchone()[0]
        if unmasked == 0:
            passed += 1
        else:
            gaps.append({
                "check":   "Column masking on PII",
                "issue":   f"{unmasked} PII column(s) missing masking policy",
                "severity": "BLOCKS_CERTIFICATION",
            })

        return PillarResult("Access Control", checks, passed, checks - passed, gaps)

    # ── Pillar 5: SLA ─────────────────────────────────────────────

    def _check_sla(self, table_fqn: str, tier: str) -> PillarResult:
        gaps   = []
        checks = 0
        passed = 0

        cursor = self.sf_conn.cursor()

        # Check that SLA tag is set
        checks += 1
        db, _, table = table_fqn.split(".")
        cursor.execute("""
            SELECT COUNT(*) FROM snowflake.account_usage.tag_references
            WHERE object_name  = %(table)s
              AND tag_name      = 'SLA_FRESHNESS_HOURS'
              AND object_database = %(db)s
        """, {"table": table.upper(), "db": db.upper()})
        has_sla_tag = cursor.fetchone()[0] > 0
        if has_sla_tag:
            passed += 1
        else:
            gaps.append({
                "check":    "SLA freshness tag",
                "issue":    "SLA_FRESHNESS_HOURS tag not set — required for certification",
                "severity": "BLOCKS_CERTIFICATION",
            })

        # Check that a data contract exists
        checks += 1
        cursor.execute("""
            SELECT COUNT(*) FROM data_governance.contracts.data_contracts
            WHERE producer_table = %(table)s AND status = 'ACTIVE'
        """, {"table": table_fqn})
        has_contract = cursor.fetchone()[0] > 0
        if has_contract:
            passed += 1
        else:
            gaps.append({
                "check":    "Active data contract",
                "issue":    "No active data contract found — author and sign contract before certifying",
                "severity": "BLOCKS_CERTIFICATION",
            })

        return PillarResult("SLA", checks, passed, checks - passed, gaps)
```

### 7.4 Stage 3 — Build and Validate

The producer resolves all gaps identified in the pre-flight report. The CI/CD pipeline enforces this gate automatically on every PR to the Gold layer.

**CI/CD Certification Gate (GitHub Actions):**

```yaml
# .github/workflows/certification_gate.yml
name: Data Product Certification Gate

on:
  pull_request:
    paths:
      - "models/gold/**"
      - "models/semantic/**"
      - "dq_config/**"
      - "contracts/**"

jobs:
  certification_preflight:
    name: Run Certification Pre-Flight
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run dbt tests
        run: |
          dbt test --select "tag:gold" --store-failures
        env:
          DBT_PROFILES_DIR: ${{ secrets.DBT_PROFILES_DIR }}

      - name: Run DQ gate
        run: |
          python scripts/dq_gate.py \
            --config dq_config/${{ env.DOMAIN }}/${{ env.TABLE }}.yaml \
            --fail-on-critical
        env:
          SNOWFLAKE_ACCOUNT:    ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER:       ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PRIVATE_KEY: ${{ secrets.SNOWFLAKE_PRIVATE_KEY }}

      - name: Validate data contract exists
        run: |
          python scripts/validate_contract.py \
            --table ${{ env.TABLE_FQN }}

      - name: Run pre-flight certification assessment
        run: |
          python scripts/preflight_assessor.py \
            --asset-id ${{ env.COLLIBRA_ASSET_ID }} \
            --table    ${{ env.TABLE_FQN }} \
            --tier     ${{ env.CERT_TIER }} \
            --output   preflight_report.json

      - name: Assert certification readiness
        run: |
          python -c "
          import json, sys
          r = json.load(open('preflight_report.json'))
          if not r['certification_ready']:
              gaps = [g for p in r['pillars'] for g in p['gaps']]
              print('CERTIFICATION BLOCKED:')
              for g in gaps:
                  print(f'  [{g[\"severity\"]}] {g[\"check\"]}: {g.get(\"issue\", g.get(\"actual\"))}')
              sys.exit(1)
          print('Pre-flight passed — certification request may proceed.')
          "

      - name: Upload pre-flight report
        uses: actions/upload-artifact@v4
        with:
          name: preflight-certification-report
          path: preflight_report.json
```

### 7.5 Stages 4–5 — Review, Approval, and Publishing

**Approval chain by tier:**

| Stage | T1 Approvers | T2 Approvers | T3 Approvers |
|---|---|---|---|
| Technical validation | Data Custodian self-attest | Data Custodian self-attest | Data Custodian self-attest |
| DGO validation | DGO Program Manager | DGO Analyst | DGO Analyst |
| Domain sign-off | Domain Owner (named individual) | Domain Steward | Domain Steward |
| Executive sign-off | CDO | Not required | Not required |
| 2LOD review scheduling | DGO schedules within 60 days | DGO schedules within 90 days | Not required |

**Post-approval actions (automated):**

```python
# post_certification_publisher.py
"""
Runs after all approvals are complete.
Sets Collibra status, applies platform tags, notifies consumers, and
activates SLA monitoring.
"""

import json
from datetime import date


class PostCertificationPublisher:

    def __init__(
        self,
        collibra_client,
        sf_conn,
        databricks_certifier,
        slack_webhook: str,
        notification_config: dict,
    ):
        self.collibra     = collibra_client
        self.sf_conn      = sf_conn
        self.db_certifier = databricks_certifier
        self.slack        = slack_webhook
        self.notify_cfg   = notification_config

    def publish(self, asset_id: str, cert_config: dict) -> None:
        """Execute all post-approval publication steps."""
        steps = [
            ("Collibra status → CERTIFIED",    self._set_collibra_certified),
            ("Platform tags applied",           self._apply_platform_tags),
            ("SLA monitoring activated",        self._activate_sla_monitoring),
            ("Consumers notified",              self._notify_consumers),
            ("Certification register updated",  self._update_register),
        ]
        results = {}
        for label, fn in steps:
            try:
                fn(asset_id, cert_config)
                results[label] = "OK"
            except Exception as e:
                results[label] = f"FAILED: {e}"

        self._post_slack_summary(cert_config, results)

    def _set_collibra_certified(self, asset_id: str, cfg: dict) -> None:
        self.collibra.set_certification_status(
            asset_id, "CERTIFIED", cfg["approved_by"]
        )

    def _apply_platform_tags(self, asset_id: str, cfg: dict) -> None:
        if cfg.get("platform") == "snowflake":
            cursor = self.sf_conn.cursor()
            cursor.execute(f"""
                ALTER TABLE {cfg['table_fqn']}
                    SET TAG governance.certified_date = '{date.today().isoformat()}',
                            governance.certification_status = 'CERTIFIED'
            """)
        elif cfg.get("platform") == "databricks":
            self.db_certifier.certify_table(cfg["databricks_config"])

    def _activate_sla_monitoring(self, asset_id: str, cfg: dict) -> None:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            INSERT INTO data_governance.sla.monitoring_registry
                (asset_id, table_fqn, sla_freshness_hours, tier, activated_at)
            VALUES (%(id)s, %(table)s, %(sla)s, %(tier)s, CURRENT_TIMESTAMP())
            ON CONFLICT (asset_id) DO UPDATE
                SET sla_freshness_hours = %(sla)s, tier = %(tier)s,
                    activated_at = CURRENT_TIMESTAMP()
        """, {
            "id":    asset_id,
            "table": cfg["table_fqn"],
            "sla":   cfg["sla_freshness_hours"],
            "tier":  cfg["tier"],
        })

    def _notify_consumers(self, asset_id: str, cfg: dict) -> None:
        import requests
        channels = self.notify_cfg.get("consumer_channels", [])
        for ch in channels:
            requests.post(self.slack, json={
                "channel": ch,
                "text": (
                    f"Data product *{cfg['asset_name']}* has been certified "
                    f"({cfg['tier']} — {cfg['domain']} domain).\n"
                    f"Owner: {cfg['owner_email']} | SLA: {cfg['sla_freshness_hours']}h\n"
                    f"Collibra: {cfg.get('collibra_url', 'see catalog')}"
                ),
            }, timeout=10)

    def _update_register(self, asset_id: str, cfg: dict) -> None:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            MERGE INTO data_governance.certification.register AS target
            USING (SELECT
                %(asset_id)s AS asset_id, %(asset_name)s AS asset_name,
                %(tier)s AS tier, %(domain)s AS domain,
                %(owner_email)s AS owner_email, %(table_fqn)s AS table_fqn,
                CURRENT_TIMESTAMP() AS certified_at,
                %(review_date)s AS review_date, 'ACTIVE' AS status
            ) AS source ON target.asset_id = source.asset_id
            WHEN MATCHED     THEN UPDATE SET target.certified_at = source.certified_at,
                                             target.status = 'ACTIVE'
            WHEN NOT MATCHED THEN INSERT VALUES (
                source.asset_id, source.asset_name, source.tier, source.domain,
                source.owner_email, source.table_fqn, source.certified_at,
                source.review_date, source.status
            )
        """, cfg)

    def _post_slack_summary(self, cfg: dict, results: dict) -> None:
        import requests
        status = "ALL STEPS OK" if all("OK" in v for v in results.values()) else "PARTIAL FAILURE"
        detail = "\n".join(f"  {k}: {v}" for k, v in results.items())
        requests.post(self.slack, json={
            "channel": "#data-governance",
            "text": (
                f"Certification published: *{cfg['asset_name']}* ({cfg['tier']})\n"
                f"Status: {status}\n{detail}"
            ),
        }, timeout=10)
```

---

## 8. Data Contract Standard

### 8.1 What a Data Contract Is

A data contract is a **versioned, signed agreement** between a data producer and all registered consumers. It defines the schema, semantics, SLAs, and change management obligations. The contract is the binding document that makes certification enforceable.

### 8.2 Data Contract YAML Schema

```yaml
# contracts/{domain}/{table}_v1.0.0.yaml
# Stored in Git. Every material change increments the version.

contract_id:   "contract-fin-fact-revenue-001"
version:       "1.0.0"
status:        "ACTIVE"          # DRAFT / ACTIVE / DEPRECATED / TERMINATED
created_date:  "2026-03-01"
review_date:   "2026-09-01"

# ── Asset Identity ────────────────────────────────────────────────────────────
asset:
  name:            "fact_revenue"
  fully_qualified: "prod_finance_gold.finance.fact_revenue"
  platform:        "snowflake"              # snowflake / databricks / both
  layer:           "gold"                   # bronze / silver / gold / semantic
  tier:            "T1"
  domain:          "Finance"
  collibra_asset_id: "clb-fin-fact-revenue-001"

# ── Ownership ─────────────────────────────────────────────────────────────────
ownership:
  producer:
    team:      "Finance Data Engineering"
    custodian: "john.doe@company.com"
    steward:   "jane.smith@company.com"
    owner:     "sarah.jones@company.com"    # Finance Controller
    signed_at: "2026-03-01T10:00:00Z"

  consumers:
    - id:          "consumer-bi-finance-001"
      name:        "Finance KPI Dashboard (Power BI)"
      team:        "BI Center of Excellence"
      contact:     "bi-coe@company.com"
      signed_at:   "2026-03-01T14:00:00Z"
      usage:       "T1 certified reporting"

    - id:          "consumer-ml-churn-001"
      name:        "Customer Churn Model — Feature Pipeline"
      team:        "ML Engineering"
      contact:     "ml-eng@company.com"
      signed_at:   "2026-03-02T09:00:00Z"
      usage:       "Feature engineering input"

# ── Schema ────────────────────────────────────────────────────────────────────
schema:
  version:             "1.0.0"
  grain:               "One row per revenue transaction"
  primary_key:         ["revenue_key"]
  partition_column:    "transaction_date"
  cluster_keys:        ["customer_segment", "product_category"]

  columns:
    - name:         "revenue_key"
      type:         "VARCHAR(64)"
      nullable:     false
      pii:          false
      classification: "INTERNAL"
      description:  "SHA-256 hash of transaction_id + source_system"
      tests:        ["unique", "not_null"]

    - name:         "transaction_date"
      type:         "DATE"
      nullable:     false
      pii:          false
      classification: "INTERNAL"
      description:  "Date of the revenue transaction (UTC)"
      tests:        ["not_null", "not_future_dated"]

    - name:         "gross_revenue_usd"
      type:         "NUMBER(18,2)"
      nullable:     false
      pii:          false
      classification: "CONFIDENTIAL"
      description:  "Pre-discount, pre-tax revenue in USD"
      tests:        ["not_null", "gte_zero"]
      glossary_term: "Gross Revenue"

    - name:         "customer_email"
      type:         "VARCHAR(255)"
      nullable:     true
      pii:          true
      pii_type:     "EMAIL"
      classification: "RESTRICTED"
      description:  "Customer email address — masked for non-restricted roles"
      masking_policy: "governance.policies.mask_email"

# ── SLA ───────────────────────────────────────────────────────────────────────
sla:
  freshness_hours:       6       # Data must refresh within 6 hours of source
  availability_pct:      99.5    # 99.5% uptime commitment
  breach_response_hours: 2       # Max time to acknowledge a breach (T1)
  incident_playbook:     "DATA_INCIDENT_RESPONSE_PLAYBOOK.md#31-data-quality-failure--pipeline-blocked"

  schedule:
    frequency:  "daily"
    window:     "02:00–04:00 UTC"
    timezone:   "UTC"

# ── Data Quality ──────────────────────────────────────────────────────────────
data_quality:
  dq_config_path: "dq_config/gold/finance/fact_revenue.yaml"
  min_critical_pass_rate_pct: 100
  min_high_pass_rate_pct:     97
  anomaly_detection_enabled:  true
  reconciliation_query:       "sql/reconciliation/finance/fact_revenue_recon.sql"

# ── Change Management ─────────────────────────────────────────────────────────
change_management:
  breaking_change_notice_days: 14    # T1 minimum: 14 days advance notice
  non_breaking_change_notice_days: 3
  deprecation_notice_days: 30

  breaking_changes_definition:
    - "Column dropped"
    - "Column renamed"
    - "Column type narrowed (e.g., NUMBER(18,4) to NUMBER(10,2))"
    - "Primary key changed"
    - "Filter added that reduces row count"
    - "Grain changed"

  non_breaking_changes:
    - "Column added (nullable)"
    - "Column description updated"
    - "SLA extended (not tightened)"
    - "New partition or cluster key"

# ── Lineage ───────────────────────────────────────────────────────────────────
lineage:
  source_systems:
    - system:   "ERP (SQL Server)"
      schema:   "dbo.GL_Transactions"
      ingestion: "Fivetran — daily full refresh"

  upstream_tables:
    - "prod_finance_bronze.erp.gl_transactions"
    - "prod_finance_silver.erp.gl_transactions_clean"
    - "prod_customer_gold.customer.dim_customer"

  downstream_consumers:
    - "Power BI: Finance KPI Dashboard (certified dataset)"
    - "ML Feature Store: customer_ltv_features"
    - "Snowflake Data Share: finance_external_partner"

  collibra_lineage_verified: true
  dbt_lineage_graph: "https://dbt-docs.internal/#!/model/fact_revenue"

# ── Access Control ────────────────────────────────────────────────────────────
access_control:
  snowflake_roles:
    read:
      - "FINANCE_READ"
      - "ANALYTICS_READ"
    restricted_read:
      - "FINANCE_RESTRICTED_READ"     # Can see unmasked PII columns
    write:
      - "FINANCE_WRITE"               # Engineering only

  row_level_security:   false        # No RLS — RBAC roles control access
  column_masking:       true         # PII columns masked by default
  data_usage_agreement: "contracts/dua/finance-restricted-dua-v1.pdf"
  last_access_review:   "2026-01-15"
  next_access_review:   "2026-04-15"
```

### 8.3 Contract Versioning Rules

```
Version format: MAJOR.MINOR.PATCH

MAJOR — breaking change (column dropped, type changed, grain changed)
  → 14 days advance notice required for T1; 7 days for T2
  → All consumers must re-acknowledge before change is applied
  → Old contract version remains accessible for 30 days

MINOR — additive change (new column, SLA extension, description update)
  → 3 days advance notice
  → Consumers notified; no re-acknowledgment required unless Restricted data added

PATCH — metadata only (description update, contact change, documentation fix)
  → No notice required
  → Auto-notified in weekly governance digest
```

---

## 9. Lineage Requirements

### 9.1 Lineage Levels

| Level | Description | Requirement |
|---|---|---|
| **L1 — System** | Source system to platform (ERP → Snowflake Bronze) | Required for all tiers |
| **L2 — Table** | Table-to-table across medallion layers | Required for all tiers |
| **L3 — Column** | Column-level transformations tracked | Required for T1; recommended T2 |
| **L4 — Semantic** | Physical column to semantic metric | Required for T1 metrics |
| **L5 — Report** | Semantic metric to BI report visual | Required for T1 BI |

### 9.2 Lineage Collection by Platform

**dbt — automated lineage via manifest:**

```python
# lineage_collector.py
"""
Extracts dbt lineage from the compiled manifest and syncs to Collibra.
Run as part of the post-deploy CI/CD step.
"""

import json
import requests
from pathlib import Path


class DBTLineageCollector:
    """Reads dbt manifest and pushes lineage relations to Collibra."""

    def __init__(self, manifest_path: str, collibra_client):
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        self.collibra = collibra_client

    def sync_gold_lineage(self) -> list[dict]:
        """Extract all Gold model dependencies and push to Collibra."""
        lineage_records = []

        for node_id, node in self.manifest["nodes"].items():
            if not (node.get("config", {}).get("meta", {}).get("layer") == "gold"):
                continue

            model_name = node["name"]
            deps       = node.get("depends_on", {}).get("nodes", [])

            for dep_id in deps:
                dep_node = self.manifest["nodes"].get(dep_id, {})
                dep_name = dep_node.get("name", dep_id)

                record = {
                    "source_model":        dep_name,
                    "target_model":        model_name,
                    "source_collibra_id":  dep_node.get("config", {}).get("meta", {}).get("collibra_asset_id"),
                    "target_collibra_id":  node.get("config",    {}).get("meta", {}).get("collibra_asset_id"),
                    "relation_type":       "sourceOf",
                }
                lineage_records.append(record)

                # Push to Collibra if both IDs are known
                if record["source_collibra_id"] and record["target_collibra_id"]:
                    self._push_relation_to_collibra(record)

        return lineage_records

    def _push_relation_to_collibra(self, record: dict) -> None:
        self.collibra.session.post(
            f"{self.collibra.base_url}/rest/2.0/relations",
            json={
                "sourceId":      record["source_collibra_id"],
                "targetId":      record["target_collibra_id"],
                "typePublicId":  record["relation_type"],
            },
            timeout=30,
        )
```

**Snowflake — platform lineage query:**

```sql
-- Extract column-level lineage for a Gold table from Snowflake Access History
-- Use to supplement dbt lineage for tables not built by dbt
SELECT
    ah.query_id,
    fl.value:objectDomain::STRING      AS source_domain,
    fl.value:objectName::STRING        AS source_object,
    cl.value:columnName::STRING        AS source_column,
    dl.value:objectName::STRING        AS target_object,
    dc.value:columnName::STRING        AS target_column,
    ah.query_start_time
FROM snowflake.account_usage.access_history ah,
    LATERAL FLATTEN(ah.base_objects_accessed)   fl,
    LATERAL FLATTEN(fl.value:columns, OUTER=>TRUE) cl,
    LATERAL FLATTEN(ah.objects_modified)        dl,
    LATERAL FLATTEN(dl.value:columns, OUTER=>TRUE) dc
WHERE ah.query_start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND dl.value:objectName::STRING LIKE 'PROD_FINANCE_GOLD%'
ORDER BY ah.query_start_time DESC
LIMIT 5000;
```

**OpenLineage integration for Databricks:**

```python
# openlineage_databricks.py
"""
Emits OpenLineage events from Databricks Spark jobs to Collibra (via Marquez or direct).
Include this in every Spark job that writes to Gold layer.
"""

from openlineage.client import OpenLineageClient, set_producer
from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client.facet import (
    SchemaDatasetFacet,
    SchemaField,
    SQLJobFacet,
)
import uuid
from datetime import datetime, timezone


def emit_gold_write_lineage(
    job_name: str,
    input_tables: list[str],
    output_table: str,
    sql: str,
    ol_endpoint: str,
) -> None:
    """Emit an OpenLineage COMPLETE event after a Gold table write."""
    client    = OpenLineageClient(url=ol_endpoint)
    run_id    = str(uuid.uuid4())
    job       = Job(namespace="databricks", name=job_name)
    run       = Run(runId=run_id)

    inputs  = [
        {"namespace": "databricks", "name": t, "facets": {}}
        for t in input_tables
    ]
    outputs = [
        {
            "namespace": "databricks",
            "name":      output_table,
            "facets":    {},
        }
    ]

    event = RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=datetime.now(timezone.utc).isoformat(),
        run=run,
        job=job,
        inputs=inputs,
        outputs=outputs,
        producer="databricks-gold-pipeline",
    )
    client.emit(event)
```

### 9.3 Lineage Completeness Check

```sql
-- Weekly lineage completeness check — run by DGO
-- Returns Gold tables missing upstream lineage (blocks T1 certification renewal)

WITH gold_tables AS (
    SELECT DISTINCT
        t.table_catalog, t.table_schema, t.table_name,
        tv.tag_value AS tier
    FROM snowflake.account_usage.tables t
    JOIN snowflake.account_usage.tag_references tv
        ON tv.object_name = t.table_name
        AND tv.tag_name   = 'DATA_TIER'
    WHERE t.table_catalog LIKE 'PROD_%_GOLD'
      AND tv.tag_value    IN ('T1', 'T2')
),
tables_with_lineage AS (
    SELECT DISTINCT target_table
    FROM data_governance.lineage.registered_lineage
    WHERE documented_in_collibra = TRUE
)
SELECT
    g.table_catalog, g.table_schema, g.table_name, g.tier,
    CASE WHEN l.target_table IS NOT NULL
         THEN 'LINEAGE DOCUMENTED'
         ELSE 'NO LINEAGE — CERTIFICATION AT RISK' END AS lineage_status
FROM gold_tables g
LEFT JOIN tables_with_lineage l
    ON l.target_table = g.table_catalog || '.' || g.table_schema || '.' || g.table_name
ORDER BY lineage_status DESC, g.tier, g.table_name;
```

---

## 10. Ownership and Stewardship Requirements

### 10.1 Ownership Assignment Rules

```yaml
# ownership_assignment_rules.yaml
# These rules are enforced by the Collibra Workflow on certification requests.

rules:
  - rule: "no_team_ownership"
    description: "Owner must be an individual, not a team distribution list"
    validation:  "owner_email must not match pattern .*-team@|.*-group@|.*-dl@"
    blocks_certification: true

  - rule: "owner_must_be_active"
    description: "Owner must be an active employee (verified via HR system)"
    validation:  "owner_email must exist in HR directory with status ACTIVE"
    blocks_certification: true

  - rule: "owner_custodian_different_people"
    description: "Business Owner and Technical Custodian must be different individuals"
    validation:  "owner_email != custodian_email"
    blocks_certification: true

  - rule: "backup_owner_required_for_t1"
    description: "T1 assets must have a backup owner designated"
    applies_to: ["T1"]
    blocks_certification: true

  - rule: "executive_sponsor_required_for_t1"
    description: "T1 assets require an executive sponsor (CDO or VP)"
    applies_to: ["T1"]
    blocks_certification: true
```

### 10.2 Ownership Change Process

Ownership changes to certified data products require a formal change process — they are not self-service updates.

```
Owner change request submitted
  ↓
DGO reviews: is this an org change or a reassignment?
  ORG CHANGE (e.g., person left, restructure)
    → Emergency process: temporary steward assigned same day
    → Permanent new owner must be confirmed within 14 days
    → No certification lapse if resolved within 14 days
  VOLUNTARY REASSIGNMENT
    → Standard minor change ticket
    → New owner must acknowledge the data contract
    → DGO updates Collibra and platform tags
    → Consumers notified
```

### 10.3 Orphaned Asset Escalation

```sql
-- Weekly scan: certified assets without an active owner
-- Escalated to DGO the same day results are found

SELECT
    cr.asset_name,
    cr.tier,
    cr.domain,
    cr.owner_email,
    cr.certified_at,
    DATEDIFF('day', cr.certified_at, CURRENT_DATE()) AS days_since_cert,
    'OWNER INACTIVE OR MISSING' AS issue
FROM data_governance.certification.register cr
WHERE cr.status = 'ACTIVE'
  AND (
      cr.owner_email IS NULL
      OR cr.owner_email NOT IN (
          SELECT email FROM hr_directory.employees WHERE status = 'ACTIVE'
      )
  )
ORDER BY cr.tier, cr.days_since_cert DESC;
```

---

## 11. SLA Standards

### 11.1 SLA Definitions

| SLA Type | Definition |
|---|---|
| **Freshness SLA** | Maximum elapsed time between source data availability and the certified Gold table reflecting that data |
| **Availability SLA** | Percentage of scheduled refresh windows in which the table is queryable with current data |
| **Breach Acknowledgment SLA** | Time from automated breach alert to first human acknowledgment of the incident |
| **Resolution SLA** | Time from breach detection to data restored to within freshness SLA |

### 11.2 SLA Targets by Tier

| SLA Component | T1 Critical | T2 Governed | T3 Managed |
|---|---|---|---|
| Freshness SLA | Defined per product; typically 4–8h | Defined per product; typically 8–24h | Defined per product |
| Availability target | 99.5% | 99.0% | 95.0% |
| Breach acknowledgment | 2 hours | 4 hours | 1 business day |
| P1 resolution | 4 hours | 8 hours | 2 business days |
| SLA measurement window | Rolling 30 days | Rolling 30 days | Monthly |

### 11.3 SLA Monitoring Implementation

```python
# sla_monitor.py
"""
Monitors freshness SLA for all certified data products.
Runs every 15 minutes. Raises incidents if SLA is breached.
Config-driven: thresholds and routing from YAML.
"""

import yaml
import snowflake.connector
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional


@dataclass
class SLAStatus:
    asset_name: str
    table_fqn: str
    tier: str
    sla_hours: int
    last_refresh: Optional[datetime]
    elapsed_hours: Optional[float]
    is_breached: bool
    breach_severity: str   # P1 / P2 / P3


class SLAMonitor:
    """
    Checks freshness SLA for all certified data products.
    On breach: opens incident, sends Slack alert, persists to breach log.
    """

    def __init__(
        self,
        sf_conn: snowflake.connector.SnowflakeConnection,
        config_path: str,
        incident_manager,
        slack_webhook: str,
    ):
        self.sf_conn          = sf_conn
        with open(config_path) as f:
            self.config       = yaml.safe_load(f)
        self.incident_manager = incident_manager
        self.slack_webhook    = slack_webhook

    def run(self) -> list[SLAStatus]:
        """Check SLA for all active certified products. Return all statuses."""
        certified_products = self._get_certified_products()
        statuses           = [self._check_freshness(p) for p in certified_products]
        breaches           = [s for s in statuses if s.is_breached]

        for breach in breaches:
            self._handle_breach(breach)

        return statuses

    def _check_freshness(self, product: dict) -> SLAStatus:
        cursor = self.sf_conn.cursor()
        cursor.execute(f"""
            SELECT MAX(_ingested_at)
            FROM {product['table_fqn']}
        """)
        last_refresh   = cursor.fetchone()[0]
        now            = datetime.now(timezone.utc)
        elapsed        = None
        is_breached    = False

        if last_refresh:
            last_refresh = last_refresh.replace(tzinfo=timezone.utc) if last_refresh.tzinfo is None else last_refresh
            elapsed      = (now - last_refresh).total_seconds() / 3600
            is_breached  = elapsed > product["sla_hours"]
        else:
            is_breached  = True

        breach_sev = self._map_severity(product["tier"], is_breached)

        return SLAStatus(
            asset_name=product["asset_name"],
            table_fqn=product["table_fqn"],
            tier=product["tier"],
            sla_hours=product["sla_hours"],
            last_refresh=last_refresh,
            elapsed_hours=elapsed,
            is_breached=is_breached,
            breach_severity=breach_sev,
        )

    def _handle_breach(self, status: SLAStatus) -> None:
        from DATA_INCIDENT_RESPONSE_PLAYBOOK_TYPES import Incident, IncidentType, Severity

        inc = Incident(
            incident_type=IncidentType.OUT,
            severity=Severity[status.breach_severity],
            description=(
                f"SLA breach: {status.asset_name} last refreshed "
                f"{status.elapsed_hours:.1f}h ago (SLA: {status.sla_hours}h)"
            ),
            affected_asset=status.table_fqn,
            data_classification="Unknown",
            detection_source="SLAMonitor automated check",
            detected_by="sla_monitor.py",
        )
        self.incident_manager.open_incident(inc)

    def _map_severity(self, tier: str, is_breached: bool) -> str:
        if not is_breached:
            return "OK"
        return {"T1": "P2", "T2": "P2", "T3": "P3"}.get(tier, "P3")

    def _get_certified_products(self) -> list[dict]:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            SELECT asset_name, table_fqn, tier,
                   sla_freshness_hours, domain
            FROM data_governance.sla.monitoring_registry
            WHERE status = 'ACTIVE'
        """)
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
```

### 11.4 SLA Reporting DDL

```sql
-- SLA performance summary — used in monthly CDO scorecard

CREATE OR REPLACE VIEW data_governance.sla.performance_summary AS
SELECT
    r.asset_name,
    r.tier,
    r.domain,
    r.sla_freshness_hours,
    COUNT(b.breach_id)                              AS breach_count_30d,
    AVG(b.breach_duration_hours)                    AS avg_breach_hours_30d,
    SUM(CASE WHEN b.resolved_within_sla THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(b.breach_id), 0)    AS pct_resolved_within_sla,
    CASE
        WHEN COUNT(b.breach_id) = 0 THEN 'GREEN'
        WHEN COUNT(b.breach_id) <= 2 THEN 'AMBER'
        ELSE 'RED'
    END                                             AS rag_status
FROM data_governance.sla.monitoring_registry r
LEFT JOIN data_governance.sla.breach_log b
    ON  b.asset_id  = r.asset_id
    AND b.breach_at >= CURRENT_DATE() - 30
WHERE r.status = 'ACTIVE'
GROUP BY 1, 2, 3, 4
ORDER BY CASE tier WHEN 'T1' THEN 1 WHEN 'T2' THEN 2 ELSE 3 END, r.asset_name;
```

---

## 12. Decertification and Deprecation

### 12.1 Decertification Triggers

A certified data product must be decertified when any of the following conditions occur:

| Trigger | Action | Timeline |
|---|---|---|
| T1 DQ pass rate < 100% CRITICAL for > 48 consecutive hours | Immediate suspension; incident opened | Same day |
| Owner departure with no replacement within 14 days | Certification suspended pending new owner | Day 14 |
| Access certification overdue by > 30 days | Certification suspended | Day 30 |
| Data contract unsigned by consumer for > 30 days after version change | Consumer access revoked | Day 30 |
| Lineage gap discovered (source changed, lineage no longer valid) | Certification suspended; lineage review required | Within 5 business days |
| Regulatory finding requiring asset rework | Certification suspended pending remediation | Per finding SLA |
| Product abandoned (zero consumer queries for > 90 days) | Deprecation process initiated | Day 90 |

### 12.2 Deprecation Process

```
Step 1 — Identify (automated weekly scan)
  Assets with zero queries for 90+ days are flagged as DEPRECATION_CANDIDATE.
  Steward and Owner are notified via Collibra workflow task.

Step 2 — Review (10 business days)
  Owner confirms: is this asset still needed?
    YES → Mark as ACTIVE; document business justification
    NO  → Proceed to deprecation

Step 3 — Notify (30 days advance)
  All registered consumers receive deprecation notice.
  Deprecation notice includes:
    - Asset name and Collibra link
    - Final decommission date
    - Recommended replacement (if exists)
    - Migration guidance

Step 4 — Sunset
  On decommission date:
    - Collibra status set to DEPRECATED
    - Snowflake/Databricks: table tagged DATA_TIER = 'DEPRECATED'
    - Read access revoked for non-engineering roles
    - Table retained in cold storage for data_retention_days per classification
    - After retention period: secure deletion with evidence record

Step 5 — Archive
  Physical table retained per retention policy.
  Collibra asset status: ARCHIVED.
  Data contract status: TERMINATED.
```

**Deprecation candidate scan:**

```sql
SELECT
    r.asset_name,
    r.tier,
    r.owner_email,
    r.certified_at,
    MAX(q.start_time)                              AS last_queried_at,
    DATEDIFF('day', MAX(q.start_time), CURRENT_DATE()) AS days_since_last_query
FROM data_governance.certification.register r
LEFT JOIN snowflake.account_usage.query_history q
    ON UPPER(q.query_text) LIKE '%' || UPPER(SPLIT_PART(r.table_fqn, '.', 3)) || '%'
WHERE r.status = 'ACTIVE'
GROUP BY 1, 2, 3, 4
HAVING MAX(q.start_time) IS NULL
    OR DATEDIFF('day', MAX(q.start_time), CURRENT_DATE()) > 90
ORDER BY days_since_last_query DESC NULLS FIRST;
```

---

## 13. Certification Automation — Python Framework

The full certification pipeline is orchestrated by a single entry-point class that wires together all components described in this document.

```python
# certification_pipeline.py
"""
End-to-end data product certification pipeline.
Orchestrates: pre-flight → contract validation → platform checks → 
              Collibra registration → workflow trigger → post-publish.

Config-driven entirely by YAML. No hardcoded asset names or thresholds.
"""

import yaml
import json
import logging
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CertificationPipelineConfig:
    asset_id:            str
    table_fqn:           str
    tier:                str
    domain:              str
    contract_path:       str
    dq_config_path:      str
    owner_email:         str
    steward_email:       str
    custodian_email:     str
    collibra_url:        str
    evidence_output_dir: str

    @classmethod
    def from_yaml(cls, path: str) -> "CertificationPipelineConfig":
        with open(path) as f:
            d = yaml.safe_load(f)
        return cls(**d["certification_pipeline"])


class CertificationPipeline:
    """
    Orchestrates the full certification lifecycle for a data product.

    Usage:
        config = CertificationPipelineConfig.from_yaml("certs/finance/fact_revenue.yaml")
        pipeline = CertificationPipeline(config, sf_conn, collibra_client, ...)
        result = pipeline.run()
    """

    def __init__(
        self,
        config:             CertificationPipelineConfig,
        sf_conn,
        collibra_client,
        db_certifier=None,
        bi_validators:      dict | None = None,   # {"powerbi": PBIValidator, "tableau": TableauCertifier}
        incident_manager=None,
        slack_webhook:      str = "",
    ):
        self.config        = config
        self.sf_conn       = sf_conn
        self.collibra      = collibra_client
        self.db_certifier  = db_certifier
        self.bi_validators = bi_validators or {}
        self.incidents     = incident_manager
        self.slack         = slack_webhook

        self.assessor      = PreFlightAssessor(sf_conn, collibra_client, config.dq_config_path)
        self.publisher     = PostCertificationPublisher(
            collibra_client, sf_conn, db_certifier, slack_webhook,
            yaml.safe_load(open(config.dq_config_path))
        )

    def run(self) -> dict:
        logger.info("Starting certification pipeline for %s (%s)",
                    self.config.table_fqn, self.config.tier)
        result = {
            "asset_id":   self.config.asset_id,
            "table_fqn":  self.config.table_fqn,
            "tier":       self.config.tier,
            "stages":     {},
        }

        # Stage 1: Pre-flight assessment
        report = self.assessor.assess(
            self.config.asset_id, self.config.table_fqn, self.config.tier
        )
        result["stages"]["preflight"] = report.to_dict()

        if not report.certification_ready:
            result["outcome"] = "BLOCKED — pre-flight gaps must be resolved"
            result["gaps"]    = [g for p in report.pillar_results for g in p.gaps]
            self._save_result(result)
            return result

        # Stage 2: Validate data contract
        contract_valid = self._validate_contract()
        result["stages"]["contract"] = {"valid": contract_valid}
        if not contract_valid:
            result["outcome"] = "BLOCKED — data contract invalid or unsigned"
            self._save_result(result)
            return result

        # Stage 3: Platform-specific checks
        platform_result = self._run_platform_checks()
        result["stages"]["platform"] = platform_result
        if not platform_result.get("all_passed"):
            result["outcome"] = "BLOCKED — platform checks failed"
            self._save_result(result)
            return result

        # Stage 4: BI surface checks (if applicable)
        if self.bi_validators:
            bi_result = self._run_bi_checks()
            result["stages"]["bi_surfaces"] = bi_result

        # Stage 5: Trigger Collibra approval workflow
        workflow = CollibraWorkflowClient(
            self.config.collibra_url, "", ""
        ).trigger_certification_workflow(
            CertificationRequest(
                asset_id=self.config.asset_id,
                tier=self.config.tier,
                domain=self.config.domain,
                custodian_email=self.config.custodian_email,
                owner_email=self.config.owner_email,
                steward_email=self.config.steward_email,
                evidence_path=self.config.evidence_output_dir,
            )
        )
        result["stages"]["workflow_triggered"] = workflow.get("id")
        result["outcome"] = "PENDING_APPROVAL — workflow triggered; awaiting sign-offs"

        self._save_result(result)
        logger.info("Certification pipeline complete: %s", result["outcome"])
        return result

    def _validate_contract(self) -> bool:
        with open(self.config.contract_path) as f:
            contract = yaml.safe_load(f)
        required_fields = ["asset", "ownership", "schema", "sla", "lineage"]
        return all(k in contract for k in required_fields)

    def _run_platform_checks(self) -> dict:
        db, schema, table = self.config.table_fqn.split(".")
        cursor = self.sf_conn.cursor()

        # Check required tags
        cursor.execute("""
            SELECT COUNT(DISTINCT tag_name) AS tag_count
            FROM snowflake.account_usage.tag_references
            WHERE object_name      = %(table)s
              AND object_database  = %(db)s
              AND tag_name IN (
                  'DATA_TIER', 'CLASSIFICATION_TIER', 'DATA_OWNER',
                  'STEWARD', 'SLA_FRESHNESS_HOURS', 'COLLIBRA_ASSET_ID'
              )
        """, {"table": table.upper(), "db": db.upper()})
        tag_count = cursor.fetchone()[0]

        return {
            "tags_complete":  tag_count == 6,
            "tags_found":     tag_count,
            "tags_required":  6,
            "all_passed":     tag_count == 6,
        }

    def _run_bi_checks(self) -> dict:
        results = {}
        for surface, validator in self.bi_validators.items():
            try:
                if surface == "powerbi" and hasattr(validator, "validate_dataset_rls"):
                    rls = validator.validate_dataset_rls(self.config.asset_id)
                    results[surface] = {
                        "rls_tests": len(rls),
                        "rls_passed": sum(1 for r in rls if r.passed),
                        "all_passed": all(r.passed for r in rls),
                    }
                elif surface == "tableau":
                    results[surface] = {"status": "manual_review_required"}
            except Exception as e:
                results[surface] = {"error": str(e)}
        return results

    def _save_result(self, result: dict) -> None:
        out = Path(self.config.evidence_output_dir) / "certification_pipeline_result.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump(result, f, indent=2, default=str)
```

---

## 14. YAML Configuration

```yaml
# config/certification/certification_tiers.yaml
# Master config for tier-specific thresholds, requirements, and routing.
# All pipeline components read from this file.

tier_config:

  T1:
    label: "Critical"
    dq_thresholds:
      critical_pass_rate_pct: 100
      high_pass_rate_pct:     97
      lookback_days:          30
    sla:
      breach_acknowledgment_hours: 2
      resolution_hours:            4
      availability_pct:            99.5
    ownership:
      required_attributes:
        - data_owner
        - steward
        - custodian
        - executive_sponsor
        - backup_owner
    lineage:
      table_level:  required
      column_level: required
      full_chain:   required
    review_cadence:
      first_line_of_defense_months:  1
      second_line_of_defense_months: 6
    change_management:
      breaking_change_notice_days:     14
      non_breaking_change_notice_days: 3
      requires_cab:                    true
    approvals_required:
      - custodian_self_attest
      - dgo_validation
      - domain_owner
      - cdo_sign_off
    slack_channels:
      certification: ["#data-governance", "#data-cert-t1"]
      breach:        ["#data-incidents-p1", "#data-governance"]

  T2:
    label: "Governed"
    dq_thresholds:
      critical_pass_rate_pct: 100
      high_pass_rate_pct:     90
      lookback_days:          30
    sla:
      breach_acknowledgment_hours: 4
      resolution_hours:            8
      availability_pct:            99.0
    ownership:
      required_attributes:
        - data_owner
        - steward
        - custodian
    lineage:
      table_level:  required
      column_level: recommended
      full_chain:   source_to_gold
    review_cadence:
      first_line_of_defense_months:  3
      second_line_of_defense_months: 12
    change_management:
      breaking_change_notice_days:     7
      non_breaking_change_notice_days: 2
      requires_cab:                    false
    approvals_required:
      - custodian_self_attest
      - dgo_validation
      - domain_steward
    slack_channels:
      certification: ["#data-governance"]
      breach:        ["#data-incidents"]

  T3:
    label: "Managed"
    dq_thresholds:
      critical_pass_rate_pct: 100
      lookback_days:          7
    sla:
      breach_acknowledgment_hours: 24
      resolution_hours:            48
    ownership:
      required_attributes:
        - data_owner
        - steward
    lineage:
      table_level:  recommended
      column_level: not_required
    review_cadence:
      first_line_of_defense_months: 12
    change_management:
      breaking_change_notice_days:  3
      requires_cab:                 false
    approvals_required:
      - custodian_self_attest
      - domain_steward

# ── RLS test config (Power BI example) ────────────────────────────────────────
rls_tests:
  - role_name:              "Finance_Manager"
    test_user_email:        "test-finance-mgr@company.com"
    dax_query:              "EVALUATE ROW(\"RowCount\", COUNTROWS(fact_revenue))"
    expected_row_count_range: [1000, 500000]

  - role_name:              "Finance_Analyst"
    test_user_email:        "test-finance-analyst@company.com"
    dax_query:              "EVALUATE ROW(\"RowCount\", COUNTROWS(fact_revenue))"
    expected_row_count_range: [100, 100000]   # Analysts see subset of regions

  - role_name:              "No_Finance_Access"
    test_user_email:        "test-no-access@company.com"
    dax_query:              "EVALUATE ROW(\"RowCount\", COUNTROWS(fact_revenue))"
    expected_row_count_range: [0, 0]          # Must see zero rows

# ── Pre-ingestion checks (SQL Server example) ─────────────────────────────────
pre_ingestion_checks:
  - name:      "source_row_count_positive"
    sql:       "SELECT COUNT(*) FROM dbo.GL_Transactions WHERE created_date = CAST(GETDATE() AS DATE)"
    condition: "greater_than"
    threshold: 0
    severity:  "CRITICAL"

  - name:      "no_null_primary_keys"
    sql:       "SELECT COUNT(*) FROM dbo.GL_Transactions WHERE transaction_id IS NULL"
    condition: "equals"
    threshold: 0
    severity:  "CRITICAL"

  - name:      "amount_column_not_all_zero"
    sql:       "SELECT SUM(ABS(amount)) FROM dbo.GL_Transactions WHERE created_date = CAST(GETDATE() AS DATE)"
    condition: "greater_than"
    threshold: 0
    severity:  "HIGH"
```

---

## 15. Collibra Integration

### 15.1 Required Collibra Asset Attributes

Every data product registered in Collibra must have all required attributes populated before certification can be granted.

| Attribute | Required | Description |
|---|---|---|
| `asset_name` | Yes | Display name matching platform object name |
| `business_description` | Yes | Plain-language description; minimum 50 characters |
| `domain` | Yes | Owning business domain |
| `data_owner` | Yes | Named individual; linked to Collibra user |
| `steward` | Yes | Named individual; linked to Collibra user |
| `custodian` | Yes | Named individual; linked to Collibra user |
| `data_tier` | Yes | T1 / T2 / T3 / T4 |
| `classification_tier` | Yes | PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED |
| `certification_status` | Yes | UNCERTIFIED / CERTIFIED / SUSPENDED / DEPRECATED |
| `certified_date` | Yes (after cert) | ISO date |
| `review_date` | Yes (after cert) | ISO date — when next review is due |
| `certified_by` | Yes (after cert) | Approver email |
| `sla_freshness_hours` | Yes | Integer — freshness SLA in hours |
| `lineage_documented` | Yes | Boolean |
| `dq_score_current` | Yes | Current DQ pass rate % |
| `data_contract_id` | Yes | Reference to signed contract |
| `last_access_review_date` | Yes | Date of last access certification |
| `retention_policy` | Yes | Retention period and basis |
| `collibra_asset_id` | Yes | UUID assigned by Collibra on registration |
| `glossary_terms` | Required for key columns | Linked Collibra Business Glossary terms |

### 15.2 Collibra Metadata Sync

```python
# collibra_metadata_sync.py
"""
Syncs certification metadata between the platform (Snowflake tags)
and Collibra. Run daily to keep Collibra as the authoritative governance hub.
"""

import snowflake.connector
from dataclasses import dataclass


class CollibraMetadataSync:
    """
    Pulls certification tags from Snowflake and updates Collibra attributes.
    Also pulls DQ scores from the DQ results table and publishes to Collibra.
    """

    REQUIRED_TAGS = [
        "DATA_TIER", "CLASSIFICATION_TIER", "DATA_OWNER", "STEWARD",
        "SLA_FRESHNESS_HOURS", "COLLIBRA_ASSET_ID", "CERTIFIED_DATE",
        "REVIEW_DATE",
    ]

    def __init__(
        self,
        sf_conn: snowflake.connector.SnowflakeConnection,
        collibra_client,
    ):
        self.sf_conn  = sf_conn
        self.collibra = collibra_client

    def sync_all_certified_tables(self, catalog_filter: str = "PROD_%_GOLD") -> list[dict]:
        """Sync all certified Gold tables from Snowflake tags to Collibra."""
        cursor = self.sf_conn.cursor()
        cursor.execute(f"""
            SELECT
                t.table_catalog, t.table_schema, t.table_name,
                {', '.join(
                    f"MAX(CASE WHEN tv.tag_name = '{tag}' THEN tv.tag_value END) AS {tag.lower()}"
                    for tag in self.REQUIRED_TAGS
                )}
            FROM snowflake.account_usage.tables t
            LEFT JOIN snowflake.account_usage.tag_references tv
                ON tv.object_name = t.table_name AND tv.object_database = t.table_catalog
            WHERE t.table_catalog LIKE '{catalog_filter}'
              AND t.deleted IS NULL
            GROUP BY 1, 2, 3
            HAVING MAX(CASE WHEN tv.tag_name = 'COLLIBRA_ASSET_ID'
                           THEN tv.tag_value END) IS NOT NULL
        """)
        rows    = cursor.fetchall()
        cols    = [d[0].lower() for d in cursor.description]
        results = []

        for row in rows:
            record       = dict(zip(cols, row))
            asset_id     = record.get("collibra_asset_id")
            dq_score     = self._get_dq_score(
                f"{record['table_catalog']}.{record['table_schema']}.{record['table_name']}"
            )

            sync_payload = {
                "data_tier":            record.get("data_tier"),
                "classification_tier":  record.get("classification_tier"),
                "data_owner":           record.get("data_owner"),
                "steward":              record.get("steward"),
                "sla_freshness_hours":  record.get("sla_freshness_hours"),
                "certified_date":       record.get("certified_date"),
                "review_date":          record.get("review_date"),
                "dq_score_current":     str(dq_score),
            }

            for attr_id, value in sync_payload.items():
                if value:
                    try:
                        self.collibra.session.put(
                            f"{self.collibra.base_url}/rest/2.0/assets/{asset_id}/attributes",
                            json={"typePublicId": attr_id, "value": {"value": value}},
                            timeout=30,
                        )
                    except Exception as e:
                        results.append({"asset_id": asset_id, "attr": attr_id, "error": str(e)})
                        continue

            results.append({"asset_id": asset_id, "table": record["table_name"], "synced": True})

        return results

    def _get_dq_score(self, table_fqn: str) -> float:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            SELECT
                SUM(CASE WHEN passed THEN 1 ELSE 0 END) * 100.0
                    / NULLIF(COUNT(*), 0) AS pass_rate
            FROM data_quality.pipeline_test_results
            WHERE table_name = %(table)s
              AND run_date  >= CURRENT_DATE() - 7
        """, {"table": table_fqn})
        row = cursor.fetchone()
        return float(row[0]) if row and row[0] else 0.0
```

---

## 16. Certification Register and KPIs

### 16.1 Certification Register DDL

```sql
-- Master certification register: one row per certified data product

CREATE TABLE IF NOT EXISTS data_governance.certification.register (
    asset_id              VARCHAR(100)   NOT NULL PRIMARY KEY,
    asset_name            VARCHAR(300)   NOT NULL,
    table_fqn             VARCHAR(500),
    tier                  VARCHAR(5)     NOT NULL,      -- T1 / T2 / T3
    domain                VARCHAR(100)   NOT NULL,
    owner_email           VARCHAR(200),
    steward_email         VARCHAR(200),
    custodian_email       VARCHAR(200),
    platform              VARCHAR(50),                  -- snowflake / databricks / both
    layer                 VARCHAR(20),                  -- bronze / silver / gold / semantic / bi
    classification        VARCHAR(20),
    certified_at          TIMESTAMP_TZ,
    certified_by          VARCHAR(200),
    review_date           DATE,
    status                VARCHAR(30)    DEFAULT 'ACTIVE',
    sla_freshness_hours   INTEGER,
    dq_score_current      FLOAT,
    collibra_url          VARCHAR(500),
    contract_path         VARCHAR(500),
    notes                 TEXT,
    inserted_at           TIMESTAMP_TZ   DEFAULT CURRENT_TIMESTAMP(),
    updated_at            TIMESTAMP_TZ   DEFAULT CURRENT_TIMESTAMP()
);

-- Certification history: every status change
CREATE TABLE IF NOT EXISTS data_governance.certification.status_history (
    event_id          VARCHAR(100)   DEFAULT UUID_STRING() PRIMARY KEY,
    asset_id          VARCHAR(100)   NOT NULL,
    asset_name        VARCHAR(300),
    from_status       VARCHAR(30),
    to_status         VARCHAR(30)    NOT NULL,
    reason            TEXT,
    changed_by        VARCHAR(200),
    changed_at        TIMESTAMP_TZ   DEFAULT CURRENT_TIMESTAMP()
);
```

### 16.2 Certification KPI Scorecard

| KPI | Target | Measurement |
|---|---|---|
| % T1 assets certified | 100% | Monthly |
| % T2 assets certified | >= 95% | Monthly |
| % Certified assets with active owner | 100% | Weekly |
| % Certifications due for review (overdue) | 0% | Weekly |
| Mean Time to Certify (submission to CERTIFIED) | T1: <= 10 days / T2: <= 7 days | Per certification |
| % T1 DQ CRITICAL pass rate (30-day rolling) | 100% | Daily |
| % Certified T1 assets meeting SLA (30-day) | >= 99.5% | Daily |
| # Active data contracts signed by all consumers | 100% of T1+T2 | Monthly |
| % Lineage completeness (T1+T2 Gold tables) | >= 98% | Monthly |
| # P1 SLA breaches (T1 assets) | 0 | Monthly |
| Certification decertification rate | Trending down | Monthly |

### 16.3 Monthly CDO Certification Dashboard Query

```sql
-- Certification health summary for CDO monthly review

SELECT
    tier,
    COUNT(*)                                           AS total_certified,
    SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN status = 'SUSPENDED' THEN 1 ELSE 0 END) AS suspended,
    SUM(CASE WHEN review_date < CURRENT_DATE() THEN 1 ELSE 0 END) AS overdue_review,
    AVG(dq_score_current)                              AS avg_dq_score_pct,
    SUM(CASE WHEN owner_email IS NULL
              OR owner_email NOT IN (
                  SELECT email FROM hr_directory.employees WHERE status = 'ACTIVE'
              ) THEN 1 ELSE 0 END)                     AS orphaned_owner_count,
    CASE
        WHEN SUM(CASE WHEN status = 'SUSPENDED' THEN 1 ELSE 0 END) > 0
          OR SUM(CASE WHEN review_date < CURRENT_DATE() THEN 1 ELSE 0 END) > 0
        THEN 'AMBER'
        WHEN AVG(dq_score_current) < 97
        THEN 'AMBER'
        ELSE 'GREEN'
    END                                                AS rag_status
FROM data_governance.certification.register
WHERE status IN ('ACTIVE', 'SUSPENDED')
GROUP BY tier
ORDER BY CASE tier WHEN 'T1' THEN 1 WHEN 'T2' THEN 2 ELSE 3 END;
```

### 16.4 Certification Register Maintenance Schedule

| Activity | Frequency | Owner | Action |
|---|---|---|---|
| New certifications processed | On demand | DGO | Run full pipeline; update register |
| DQ score sync | Daily | Automated | Pull from DQ results; update Collibra |
| Orphaned owner scan | Weekly | DGO | Notify affected teams; initiate replacement |
| SLA monitoring | Every 15 min | Automated | Alert on breach; open incident |
| Review date sweep | Weekly | DGO | Flag overdue reviews; notify owners |
| Deprecation candidate scan | Weekly | DGO | Notify owners of zero-usage assets |
| Full register audit | Semi-annual | DGO + 2LOD | Validate all certifications are still valid |
| CDO scorecard | Monthly | CDO + DGO | Publish KPI dashboard |

---

## Appendix A — Quick Reference: Certification Requirements Matrix

| Requirement | T1 Critical | T2 Governed | T3 Managed | T4 Sandbox |
|---|---|---|---|---|
| **CDO sign-off** | Yes | No | No | No |
| **Domain owner sign-off** | Yes | Yes (steward) | Yes (steward) | No |
| **DGO validation** | Yes | Yes | Self-cert | No |
| **CRITICAL DQ pass rate** | 100% | 100% | 100% | Best effort |
| **HIGH DQ pass rate** | 97% | 90% | N/A | N/A |
| **Full end-to-end lineage** | Yes | Source→Gold | Immediate upstream | No |
| **Column-level lineage** | Yes | Recommended | No | No |
| **Data contract** | Signed | Signed | Lightweight | No |
| **Access certification** | Quarterly | Quarterly | Annual | No |
| **Column masking (PII)** | Yes | Yes | Yes | Yes |
| **RLS (if multi-tenant)** | Yes | Yes | Yes | No |
| **SLA monitoring** | Yes | Yes | Recommended | No |
| **Collibra registration** | Mandatory | Mandatory | Mandatory | Recommended |
| **CI/CD gate** | Yes | Yes | Recommended | No |
| **Review cadence** | Monthly 1LOD | Quarterly | Annual | None |
| **Change management** | Major + CAB | Minor change | Standard | Self-service |
| **Decertification triggers** | Automated | Automated | Manual | Auto-expiry 90d |

---

## Appendix B — Glossary

| Term | Definition |
|---|---|
| **Certification** | Formal attestation that a data product meets all five pillar requirements for its tier |
| **Data Contract** | Versioned, signed agreement between a data producer and consumers defining schema, SLA, and change obligations |
| **Data Custodian** | Technical owner accountable for pipeline health, schema management, and DQ implementation |
| **Data Owner** | Business accountable individual; makes certification decisions; escalation owner |
| **Data Product** | Any intentionally produced data asset with a defined producer, consumer, contract, and owner |
| **Data Steward** | Operational owner of day-to-day quality, access certifications, and metadata completeness |
| **DQ Gate** | Automated quality check in a CI/CD pipeline that blocks promotion of data failing defined rules |
| **Lineage** | Documented trace of data from source system through all transformations to consumption |
| **Medallion Architecture** | Bronze (raw) / Silver (cleansed) / Gold (business-ready) layered data platform pattern |
| **Semantic Layer** | Layer translating physical tables into business-consumable, governed metric definitions |
| **SLA** | Service Level Agreement defining freshness, availability, and breach response obligations |
| **T1 / T2 / T3 / T4** | Certification tiers: Critical / Governed / Managed / Sandbox |

---

*Document Owner: Chief Data Officer + Data Governance Office*
*Review Cycle: Annual or upon major platform change*
*Related: `03_data_governance_standards.md` · `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` · `04_DE_Auditing_Guide.md` · `README.md`*
