# Semantic Layer Guidebook
## Cross-Domain | Snowflake · Databricks · dbt · Collibra · BI Tools

**Document Owner:** Chief Data Officer + Analytics Engineering Lead
**Classification:** Internal — Program Standard
**Version:** 1.0 | **Last Updated:** 2026-03
**Review Cycle:** Semi-Annual or upon material platform change

> **Purpose:** This guidebook defines how the semantic layer is designed, built, governed, certified, and consumed across all data domains. The semantic layer is the single source of truth for business metric definitions — every BI report, ML feature, and ad-hoc query that touches a governed metric must derive it from here.

---

## Table of Contents

1. [What Is the Semantic Layer and Why It Matters](#1-what-is-the-semantic-layer-and-why-it-matters)
2. [Architecture: Where the Semantic Layer Sits](#2-architecture-where-the-semantic-layer-sits)
3. [Platform Options and Selection Matrix](#3-platform-options-and-selection-matrix)
4. [dbt Semantic Layer — Standards and Patterns](#4-dbt-semantic-layer--standards-and-patterns)
5. [Snowflake Semantic Layer and Cortex Analyst](#5-snowflake-semantic-layer-and-cortex-analyst)
6. [Databricks AI/BI Genie and Unity Catalog Metrics](#6-databricks-aibi-genie-and-unity-catalog-metrics)
7. [BI Tool Semantic Layer (Tableau / Power BI)](#7-bi-tool-semantic-layer-tableau--power-bi)
8. [Metric Definition Standards](#8-metric-definition-standards)
9. [Certification and Governance](#9-certification-and-governance)
10. [Auditing the Semantic Layer](#10-auditing-the-semantic-layer)
11. [Config-Based Management and Change Control](#11-config-based-management-and-change-control)
12. [Ground-Up Build Strategy](#12-ground-up-build-strategy)
13. [KPIs and Health Metrics](#13-kpis-and-health-metrics)
14. [Appendix: Templates and Reference SQL](#14-appendix-templates-and-reference-sql)

---

## 1. What Is the Semantic Layer and Why It Matters

### 1.1 Definition

The **semantic layer** is the governed translation layer between physical data model objects (tables, columns, raw SQL) and business-consumable concepts (metrics, dimensions, business terms). It answers the question: *"When the CFO says 'revenue', what exactly does that mean in data terms?"*

Without a semantic layer:
- Finance calculates revenue one way; Sales calculates it differently; the Board gets a third number.
- A schema change silently breaks twelve downstream reports.
- A junior analyst redefines "active customer" in their workbook and no one finds out until an earnings call.

With a governed semantic layer:
- Every consumer — BI report, ML feature, API, ad-hoc query — derives metrics from one certified definition.
- A breaking change is caught at the gate before it reaches production.
- Metric definitions are versioned, auditable, and searchable in the data catalog.

### 1.2 The Cost of Not Having One

| Failure Mode | Business Impact |
|---|---|
| Metric definition inconsistency | Conflicting KPI numbers in executive reports; loss of trust in data |
| No single source of truth | Analysts spend 30–40% of their time reconciling metrics rather than generating insight |
| Silent schema breakage | Downstream reports show wrong values with no alert |
| Ungoverned BI logic | Metric definitions live in individual workbooks; knowledge walks out the door with staff turnover |
| Regulatory reporting errors | Incorrect figures filed due to conflicting calculation logic |
| ML training on wrong features | Models trained on different "revenue" definitions than what is reported to the business |

### 1.3 Guiding Principles

| Principle | Definition |
|---|---|
| **Single definition** | Every business metric has exactly one certified definition. Duplicates are prohibited. |
| **Code-first** | Metric definitions live in version-controlled YAML and SQL, not in spreadsheets or BI workbook expressions. |
| **Governed by domain** | Each metric is owned by a domain data owner who approves changes. |
| **Consumer-agnostic** | The same metric definition serves BI, ML, APIs, and ad-hoc SQL equally. |
| **Auditable** | Every metric definition, change, and usage event is traceable. |
| **Discoverable** | All certified metrics are registered in the data catalog (Collibra) and searchable. |

### 1.4 Scope

This guidebook covers:
- **Metrics** — aggregations with a business meaning (Revenue, Active Customers, Churn Rate)
- **Dimensions** — attributes used to slice metrics (Region, Product Category, Customer Segment)
- **Business terms** — glossary definitions that link physical columns to human language
- **Entities** — core business objects (Customer, Order, Product) with canonical keys

This guidebook does **not** cover:
- Raw data ingestion or Bronze/Silver pipeline patterns (see `01_DE_Best_Practices.md`)
- BI report development standards (see `01_BI_Best_Practices.md`)
- ML feature store design (see `01_ML_Best_Practices.md`)

---

## 2. Architecture: Where the Semantic Layer Sits

### 2.1 Position in the Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CONSUMPTION LAYER                            │
│   BI Reports (Tableau / Power BI)  │  ML Features  │  APIs  │  SQL │
└──────────────────────┬──────────────────────────────────────────────┘
                       │  All metric consumption flows through here
┌──────────────────────▼──────────────────────────────────────────────┐
│                      SEMANTIC LAYER  ◄── THIS GUIDEBOOK             │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │  dbt Metrics    │  │ Snowflake Cortex  │  │  Databricks Genie │  │
│  │  (primary)      │  │ Analyst / Semantic│  │  Unity Catalog    │  │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬──────────┘  │
│           └───────────────────►│◄───────────────────┘             │
│                    Collibra (governance control plane)              │
└──────────────────────┬──────────────────────────────────────────────┘
                       │  Reads from certified Gold objects only
┌──────────────────────▼──────────────────────────────────────────────┐
│                         GOLD LAYER                                  │
│           Fact tables · Dimension tables · Aggregates               │
│                (Snowflake / Databricks Unity Catalog)               │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Non-Negotiable Architecture Rules

| Rule | Rationale |
|---|---|
| The semantic layer reads **only** from certified Gold objects | Silver and Bronze data is not clean or conformed enough to produce reliable metrics |
| No metric definition lives **only** in a BI tool | BI-only definitions cannot be versioned, tested, or reused by ML or APIs |
| Every metric must have a **single owner** | Metrics without owners drift; no one is accountable for correctness |
| Metric definitions are stored in **Git** | Enables review, approval workflows, diff-based change management, and rollback |
| Every certified metric is registered in **Collibra** | Enables discoverability, lineage, and governance audit trails |
| **No raw SQL metrics** in production reports | Production reports must use dbt-defined or platform-certified metrics, never inline SQL aggregations |

### 2.3 Three-Layer Semantic Model

```
Layer 1 — Physical:   Gold tables, columns, keys (engineered by DE team)
                           │
Layer 2 — Semantic:   Metric definitions, dimension maps, business term links (this layer)
                           │
Layer 3 — Presentation: BI dashboards, self-service queries, ML feature views
```

Layer 2 is owned jointly by the Analytics Engineering team (technical implementation) and Domain Data Owners (business definition approval).

---

## 3. Platform Options and Selection Matrix

### 3.1 Platform Decision Matrix

| Capability | dbt Semantic Layer | Snowflake Cortex Analyst | Databricks AI/BI Genie | BI Tool (Tableau / Power BI) |
|---|---|---|---|---|
| **Primary use case** | Cross-platform metric governance | Snowflake-native NLQ + metrics | Databricks-native exploration | Business user self-service |
| **Version control** | ✅ Native (Git) | ⚠️ Via Terraform/API | ⚠️ Via API | ❌ Manual |
| **Cross-BI-tool reuse** | ✅ Full | ⚠️ Snowflake consumers only | ⚠️ Databricks consumers only | ❌ Tool-specific |
| **ML feature access** | ✅ Via dbt models | ⚠️ Limited | ✅ Strong | ❌ None |
| **Governance integration** | ✅ Collibra via API | ✅ Native catalog | ✅ Unity Catalog | ⚠️ Partial |
| **Natural language query** | ❌ Requires BI tool | ✅ Native Cortex | ✅ Native Genie | ✅ Copilot/Ask Data |
| **Cost** | OSS + dbt Cloud | Included in Snowflake | Included in DBU | Tool license |
| **Best for** | ✅ **Primary governance layer** | Snowflake-centric teams | Databricks-centric teams | Consumer-facing supplement |

### 3.2 Recommended Architecture by Stack

**Snowflake-primary stack:**
```
dbt Semantic Layer (governance) → Snowflake Semantic Views / Cortex Analyst (serving) → Tableau / Power BI
```

**Databricks-primary stack:**
```
dbt Semantic Layer (governance) → Unity Catalog Metrics (serving) → Databricks AI/BI Genie / Tableau / Power BI
```

**Hybrid stack (Snowflake + Databricks):**
```
dbt Semantic Layer (single source of truth) → Platform-native serving layer on each platform
Collibra (catalog and governance across both)
```

> **Standard:** For organizations running both Snowflake and Databricks, dbt is the mandatory single source of truth for metric definitions. Platform-native layers are permitted as serving layers only — they must mirror dbt metric definitions, not diverge from them.

---

## 4. dbt Semantic Layer — Standards and Patterns

### 4.1 Project Structure

```
dbt_project/
├── dbt_project.yml                    # Project-level config
├── profiles.yml                       # Connection profiles (secrets via env vars)
│
├── models/
│   ├── bronze/                        # Raw staging models
│   ├── silver/                        # Cleansed, conformed models
│   └── gold/                          # Business-ready, certified models
│       ├── finance/
│       │   ├── _finance_models.yml    # Model metadata + tests
│       │   ├── fact_revenue.sql
│       │   └── dim_customer.sql
│       └── sales/
│           ├── _sales_models.yml
│           └── fact_orders.sql
│
├── semantic_models/                   # ← Semantic layer lives here
│   ├── finance/
│   │   ├── sem_revenue.yml            # Semantic model: entities, measures, dimensions
│   │   └── metrics_finance.yml        # Metric definitions
│   ├── sales/
│   │   ├── sem_orders.yml
│   │   └── metrics_sales.yml
│   └── _shared_dimensions.yml        # Cross-domain dimensions (Date, Geography)
│
├── tests/
│   ├── semantic/
│   │   ├── test_metric_consistency.sql    # Validate metrics match source
│   │   └── test_duplicate_metrics.sql     # Catch duplicate definitions
│
├── macros/
│   └── semantic/
│       └── assert_metric_approved.sql     # Governance gate macro
│
└── docs/
    └── semantic_catalog.md                # Auto-generated metric catalog
```

### 4.2 Semantic Model YAML Standard

Every semantic model must follow this structure. No exceptions.

```yaml
# semantic_models/finance/sem_revenue.yml
version: 2

semantic_models:
  - name: sem_revenue
    label: "Revenue"
    description: >
      Semantic model for all revenue metrics. Source of truth for gross revenue,
      net revenue, and discount metrics across the Finance domain.
      DO NOT derive revenue metrics from any other source.

    model: ref('fact_revenue')

    # ── Governance metadata (required) ──────────────────────────────
    meta:
      domain:            "Finance"
      owner:             "finance-data@company.com"
      steward:           "jane.smith@company.com"
      collibra_asset_id: "clb-sem-revenue-001"
      tier:              "T1"               # T1 / T2 / T3
      certified:         true
      certified_date:    "2026-03-01"
      certified_by:      "Finance Controller + DGO"
      review_date:       "2026-09-01"
      data_classification: "CONFIDENTIAL"

    # ── Entities (business keys) ─────────────────────────────────────
    entities:
      - name: transaction
        type: primary
        expr: revenue_key

      - name: customer
        type: foreign
        expr: customer_key

      - name: product
        type: foreign
        expr: product_key

    # ── Measures (raw aggregatable columns) ──────────────────────────
    measures:
      - name: gross_revenue_usd
        label: "Gross Revenue (USD)"
        description: "Pre-discount, pre-tax revenue amount in USD."
        agg: sum
        expr: gross_revenue_usd
        agg_time_dimension: transaction_date

      - name: net_revenue_usd
        label: "Net Revenue (USD)"
        description: "Revenue after discounts, before taxes."
        agg: sum
        expr: net_revenue_usd
        agg_time_dimension: transaction_date

      - name: discount_amount_usd
        label: "Discount Amount (USD)"
        description: "Total discount value applied to transactions."
        agg: sum
        expr: discount_amount_usd
        agg_time_dimension: transaction_date

      - name: transaction_count
        label: "Transaction Count"
        description: "Count of non-voided revenue transactions."
        agg: count
        expr: revenue_key

    # ── Dimensions (slice/filter attributes) ─────────────────────────
    dimensions:
      - name: transaction_date
        type: time
        label: "Transaction Date"
        expr: transaction_date
        type_params:
          time_granularity: day

      - name: customer_segment
        type: categorical
        label: "Customer Segment"
        expr: customer_segment

      - name: product_category
        type: categorical
        label: "Product Category"
        expr: product_category

      - name: sales_region
        type: categorical
        label: "Sales Region"
        expr: sales_region

      - name: is_voided
        type: categorical
        label: "Is Voided"
        expr: is_voided
```

### 4.3 Metric Definition YAML Standard

```yaml
# semantic_models/finance/metrics_finance.yml
version: 2

metrics:

  # ── Simple sum metric ─────────────────────────────────────────────
  - name: gross_revenue
    label: "Gross Revenue"
    description: >
      Total pre-discount, pre-tax revenue in USD.
      Excludes voided transactions (is_voided = false).
      CERTIFIED T1 — Finance Domain Owner and DGO approval required before modification.
      Collibra glossary term: "Gross Revenue" (ID: clb-term-gross-revenue)
    type: simple
    type_params:
      measure: gross_revenue_usd
    filter: |
      {{ Dimension('transaction__is_voided') }} = false
    meta:
      tier:              "T1"
      domain:            "Finance"
      owner:             "finance-data@company.com"
      steward:           "jane.smith@company.com"
      collibra_asset_id: "clb-metric-gross-revenue-001"
      glossary_term:     "Gross Revenue"
      breaking_change_notice_days: 14
      certified_date:    "2026-03-01"
      regulatory_metric: false

  # ── Ratio metric ──────────────────────────────────────────────────
  - name: discount_rate
    label: "Discount Rate"
    description: >
      Discount amount as a percentage of gross revenue.
      Formula: discount_amount / gross_revenue_usd.
    type: ratio
    type_params:
      numerator: discount_amount_usd
      denominator: gross_revenue_usd
    filter: |
      {{ Dimension('transaction__is_voided') }} = false
    meta:
      tier:     "T2"
      domain:   "Finance"
      owner:    "finance-data@company.com"
      steward:  "jane.smith@company.com"

  # ── Derived metric (formula combining other metrics) ─────────────
  - name: net_revenue
    label: "Net Revenue"
    description: >
      Gross Revenue minus Discount Amount.
      Net of discounts; excludes taxes and COGS.
    type: derived
    type_params:
      expr: gross_revenue - discount_amount_usd
      metrics:
        - name: gross_revenue
        - name: discount_amount_usd
    meta:
      tier:              "T1"
      domain:            "Finance"
      owner:             "finance-data@company.com"
      collibra_asset_id: "clb-metric-net-revenue-001"
      glossary_term:     "Net Revenue"
      breaking_change_notice_days: 14
      certified_date:    "2026-03-01"

  # ── Cumulative metric ─────────────────────────────────────────────
  - name: ytd_gross_revenue
    label: "YTD Gross Revenue"
    description: "Year-to-date cumulative gross revenue. Resets at the start of each fiscal year."
    type: cumulative
    type_params:
      measure: gross_revenue_usd
      cumulation_window:
        count: 1
        granularity: year
    meta:
      tier:   "T1"
      domain: "Finance"
      owner:  "finance-data@company.com"
```

### 4.4 Required Metadata Fields by Tier

| Field | T1 (Critical) | T2 (Standard) | T3 (Exploratory) |
|---|---|---|---|
| `name` | Required | Required | Required |
| `label` | Required | Required | Required |
| `description` | Required (full) | Required | Brief OK |
| `type` + `type_params` | Required | Required | Required |
| `meta.tier` | Required | Required | Required |
| `meta.domain` | Required | Required | Required |
| `meta.owner` | Required | Required | Recommended |
| `meta.steward` | Required | Required | Optional |
| `meta.collibra_asset_id` | Required | Required | Optional |
| `meta.glossary_term` | Required | Required | Optional |
| `meta.certified_date` | Required | Required | N/A |
| `meta.certified_by` | Required | Required | N/A |
| `meta.breaking_change_notice_days` | 14 days minimum | 7 days minimum | N/A |
| `meta.regulatory_metric` | Required | Required | Optional |
| `filter` (exclusions) | Required if applicable | Required if applicable | Optional |

### 4.5 dbt Model Standards for Gold Layer (Semantic Sources)

Gold tables that feed the semantic layer carry additional requirements beyond standard dbt model standards.

```yaml
# models/gold/finance/_finance_models.yml
version: 2

models:
  - name: fact_revenue
    description: >
      Grain: one row per revenue transaction.
      Canonical source for all revenue metrics.
      Feeds sem_revenue semantic model.
      Data classification: CONFIDENTIAL.
    meta:
      owner:               "finance-data@company.com"
      steward:             "jane.smith@company.com"
      domain:              "DOMAIN_FINANCE"
      layer:               "gold"
      data_classification: "CONFIDENTIAL"
      refresh_frequency:   "daily"
      sla_hours:           4
      semantic_source_for: ["sem_revenue"]      # Links back to semantic model
      collibra_asset_id:   "clb-table-fact-revenue-001"
      certified:           true

    columns:
      - name: revenue_key
        description: "Surrogate key — SHA256(transaction_id, source_system)."
        tests:
          - unique
          - not_null

      - name: gross_revenue_usd
        description: "Pre-discount, pre-tax revenue in USD. NULL if transaction voided."
        tests:
          - not_null:
              where: "is_voided = false"
          - dbt_utils.accepted_range:
              min_value: 0

      - name: transaction_date
        description: "Date of transaction in source system. UTC."
        tests:
          - not_null
          - dbt_utils.recency:
              field: transaction_date
              datepart: day
              interval: 2

      - name: is_voided
        description: "True if the transaction was voided and should be excluded from revenue metrics."
        tests:
          - not_null
          - accepted_values:
              values: [true, false]
```

### 4.6 Testing Semantic Metrics

Semantic metrics require their own test layer beyond standard dbt column tests.

```python
# tests/semantic/test_metric_consistency.py
"""
Validates that dbt-computed metric values match direct SQL aggregations
from the underlying Gold table. Catches semantic model expression errors.
Run daily as part of the semantic layer CI/CD gate.
"""

import snowflake.connector
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class MetricConsistencyResult:
    metric_name: str
    dbt_value: float
    direct_sql_value: float
    delta_pct: float
    passed: bool
    threshold_pct: float = 0.001  # 0.1% tolerance


class SemanticMetricValidator:
    """
    Compares dbt metric outputs against direct Gold table SQL.
    All validation logic is config-driven from YAML.
    """

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**conn_params)

    def validate_metric(
        self,
        metric_name: str,
        validation_date: str,
        tolerance_pct: float = 0.001,
    ) -> MetricConsistencyResult:
        metric_cfg = self.config["metrics"][metric_name]

        # Value from dbt-materialized metric result table
        dbt_val = self._query_scalar(
            metric_cfg["dbt_result_query"],
            {"date": validation_date}
        )

        # Value directly from Gold table
        direct_val = self._query_scalar(
            metric_cfg["direct_sql_query"],
            {"date": validation_date}
        )

        delta_pct = abs(dbt_val - direct_val) / max(abs(direct_val), 1e-9)

        return MetricConsistencyResult(
            metric_name=metric_name,
            dbt_value=dbt_val,
            direct_sql_value=direct_val,
            delta_pct=delta_pct,
            passed=delta_pct <= tolerance_pct,
            threshold_pct=tolerance_pct,
        )

    def run_all_validations(self, validation_date: str) -> list[MetricConsistencyResult]:
        results = []
        for metric_name in self.config["metrics"]:
            result = self.validate_metric(metric_name, validation_date)
            results.append(result)
        return results

    def _query_scalar(self, query: str, params: dict) -> float:
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0
```

```yaml
# config/semantic/metric_validation_config.yaml
metrics:
  gross_revenue:
    tolerance_pct: 0.001
    dbt_result_query: |
      SELECT metric_value
      FROM dbt_metrics.finance.gross_revenue__daily
      WHERE metric_time = %(date)s
    direct_sql_query: |
      SELECT SUM(gross_revenue_usd)
      FROM prod_finance_gold.finance.fact_revenue
      WHERE transaction_date = %(date)s
        AND is_voided = false

  transaction_count:
    tolerance_pct: 0.0
    dbt_result_query: |
      SELECT metric_value
      FROM dbt_metrics.finance.transaction_count__daily
      WHERE metric_time = %(date)s
    direct_sql_query: |
      SELECT COUNT(revenue_key)
      FROM prod_finance_gold.finance.fact_revenue
      WHERE transaction_date = %(date)s
        AND is_voided = false
```

---

## 5. Snowflake Semantic Layer and Cortex Analyst

### 5.1 When to Use

Use the Snowflake semantic layer (Semantic Views + Cortex Analyst) when:
- Your primary consumer population is Snowflake-native (Streamlit apps, Snowflake Notebooks, SQL users)
- You want natural language query (NLQ) capability over governed metrics without BI tool intermediary
- Your team has strong Snowflake SQL skills and limited dbt adoption

> **Constraint:** Snowflake semantic objects must mirror dbt metric definitions. They are a serving layer, not an independent definition source.

### 5.2 Semantic View Pattern

```sql
-- Create a semantic view in Snowflake that exposes dbt-governed metrics
-- This is the serving layer — definitions MUST match dbt metrics_finance.yml

CREATE OR REPLACE SEMANTIC VIEW prod_finance_gold.semantic.revenue_semantic_view
  TABLES (
    fact_revenue AS f
      PRIMARY KEY (revenue_key)
      WITH SYNONYMS ('revenue transactions', 'sales transactions')
  )

  FACTS (
    -- Maps to dbt measure: gross_revenue_usd
    f.gross_revenue_usd
      WITH SYNONYMS ('gross revenue', 'total revenue', 'pre-discount revenue')
      COMMENT = 'Pre-discount, pre-tax revenue in USD. Excludes voided transactions.',

    -- Maps to dbt measure: net_revenue_usd
    f.net_revenue_usd
      WITH SYNONYMS ('net revenue', 'revenue after discounts')
      COMMENT = 'Revenue after discounts, before taxes.',

    f.discount_amount_usd
      WITH SYNONYMS ('discount', 'discount value')
  )

  DIMENSIONS (
    f.transaction_date
      WITH SYNONYMS ('date', 'transaction day', 'when')
      COMMENT = 'Date of revenue transaction.',

    f.customer_segment
      WITH SYNONYMS ('segment', 'customer type')
      COMMENT = 'Customer classification segment.',

    f.product_category
      WITH SYNONYMS ('category', 'product type')
      COMMENT = 'Product line category.',

    f.sales_region
      WITH SYNONYMS ('region', 'geography', 'territory')
  )

  FILTERS (
    is_active AS f.is_voided = false
      WITH SYNONYMS ('active transactions', 'non-voided')
      COMMENT = 'Excludes voided transactions from all revenue aggregations.'
  )

  METRICS (
    gross_revenue AS SUM(f.gross_revenue_usd)
      WITH SYNONYMS ('total gross revenue', 'gross sales')
      DEFAULT FILTER is_active
      COMMENT = 'SUM of gross_revenue_usd. Excludes voided transactions.',

    net_revenue AS SUM(f.net_revenue_usd)
      WITH SYNONYMS ('total net revenue', 'revenue net of discounts')
      DEFAULT FILTER is_active
      COMMENT = 'SUM of net_revenue_usd. Excludes voided transactions.'
  );
```

### 5.3 Cortex Analyst Integration

```python
# cortex_analyst_client.py
"""
Config-driven Cortex Analyst query wrapper.
Enforces that all NLQ queries route through the governed semantic view.
"""

import snowflake.connector
import yaml
from dataclasses import dataclass


@dataclass
class CortexQueryResult:
    question: str
    generated_sql: str
    result_rows: list
    semantic_view_used: str
    confidence_score: float


class CortexAnalystClient:
    """
    Wraps Snowflake Cortex Analyst to enforce semantic view governance.
    All queries must be directed at a registered semantic view.
    """

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**conn_params)
        self._registered_views = {
            v["name"]: v for v in self.config["semantic_views"]
        }

    def query(self, question: str, domain: str) -> CortexQueryResult:
        """Submit a natural language question against a domain's semantic view."""
        if domain not in [v["domain"] for v in self.config["semantic_views"]]:
            raise ValueError(
                f"Domain '{domain}' has no registered semantic view. "
                f"Available: {list(self._registered_views.keys())}"
            )

        view_cfg = next(
            v for v in self.config["semantic_views"] if v["domain"] == domain
        )

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT SNOWFLAKE.CORTEX.ANALYST(?, ?)",
            [question, view_cfg["view_fqn"]]
        )
        result = cursor.fetchone()
        return CortexQueryResult(
            question=question,
            generated_sql=result[0].get("sql", ""),
            result_rows=result[0].get("results", []),
            semantic_view_used=view_cfg["view_fqn"],
            confidence_score=result[0].get("confidence", 0.0),
        )
```

```yaml
# config/semantic/cortex_config.yaml
semantic_views:
  - name:       "revenue_semantic_view"
    domain:     "Finance"
    view_fqn:   "prod_finance_gold.semantic.revenue_semantic_view"
    dbt_source: "sem_revenue"           # Must always match a dbt semantic model
    tier:       "T1"
    owner:      "finance-data@company.com"

  - name:       "orders_semantic_view"
    domain:     "Sales"
    view_fqn:   "prod_sales_gold.semantic.orders_semantic_view"
    dbt_source: "sem_orders"
    tier:       "T1"
    owner:      "sales-data@company.com"
```

---

## 6. Databricks AI/BI Genie and Unity Catalog Metrics

### 6.1 Unity Catalog Metric Registration

Unity Catalog metrics are the Databricks-native equivalent of Snowflake semantic views. As with Snowflake, they must mirror dbt metric definitions.

```python
# databricks_metric_registry.py
"""
Registers dbt-governed metrics in Databricks Unity Catalog.
Config-driven: metric definitions sourced from dbt YAML, not hardcoded.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    MetricInfo,
    MetricDependency,
)
import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class UnityMetricConfig:
    name: str
    catalog: str
    schema: str
    source_table: str
    expression: str
    filter_expression: str | None
    comment: str
    owner: str


class UnityMetricRegistrar:
    """
    Registers and updates Databricks Unity Catalog metrics from config.
    Idempotent: safe to run on every CI/CD deployment.
    """

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.client = WorkspaceClient()

    def register_all(self) -> list[str]:
        registered = []
        for metric_cfg in self.config["metrics"]:
            self._upsert_metric(UnityMetricConfig(**metric_cfg))
            registered.append(metric_cfg["name"])
        return registered

    def _upsert_metric(self, cfg: UnityMetricConfig) -> None:
        full_name = f"{cfg.catalog}.{cfg.schema}.{cfg.name}"
        try:
            # Update if exists
            self.client.metrics.update(
                full_name=full_name,
                comment=cfg.comment,
                owner=cfg.owner,
            )
        except Exception:
            # Create if not exists
            self.client.metrics.create(
                catalog_name=cfg.catalog,
                schema_name=cfg.schema,
                name=cfg.name,
                metrictype="AGGREGATE",
                expression=cfg.expression,
                comment=cfg.comment,
                owner=cfg.owner,
            )
```

```yaml
# config/semantic/unity_catalog_metrics.yaml
metrics:
  - name:              "gross_revenue"
    catalog:           "prod_finance_gold"
    schema:            "semantic"
    source_table:      "prod_finance_gold.finance.fact_revenue"
    expression:        "SUM(gross_revenue_usd)"
    filter_expression: "is_voided = false"
    comment: >
      Total pre-discount, pre-tax revenue in USD.
      Excludes voided transactions.
      Mirrors dbt metric: gross_revenue (semantic_models/finance/metrics_finance.yml).
      CERTIFIED T1 — Finance Domain Owner approval required before modification.
    owner: "finance-data@company.com"

  - name:              "net_revenue"
    catalog:           "prod_finance_gold"
    schema:            "semantic"
    source_table:      "prod_finance_gold.finance.fact_revenue"
    expression:        "SUM(net_revenue_usd)"
    filter_expression: "is_voided = false"
    comment: >
      Revenue after discounts, before taxes.
      Mirrors dbt metric: net_revenue (semantic_models/finance/metrics_finance.yml).
    owner: "finance-data@company.com"
```

### 6.2 AI/BI Genie Space Configuration

```python
# genie_space_manager.py
"""
Creates and manages Databricks AI/BI Genie spaces.
Config-driven: each domain has a registered Genie space with
curated metric context and governance guardrails.
"""

from databricks.sdk import WorkspaceClient
import yaml


class GenieSpaceManager:
    """Manages Genie spaces for governed NLQ over certified metrics."""

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.client = WorkspaceClient()

    def create_domain_space(self, domain: str) -> str:
        """Create or update a Genie space for a domain."""
        domain_cfg = next(
            d for d in self.config["genie_spaces"] if d["domain"] == domain
        )

        # Genie space creation via Databricks SDK
        space = self.client.genie.create_space(
            title=domain_cfg["title"],
            description=domain_cfg["description"],
            warehouse_id=domain_cfg["warehouse_id"],
        )
        return space.space_id
```

```yaml
# config/semantic/genie_spaces.yaml
genie_spaces:
  - domain:        "Finance"
    title:         "Finance Metrics — AI/BI Genie"
    description: >
      Governed natural language interface to Finance domain metrics.
      All responses are derived from certified Gold tables via Unity Catalog metrics.
      Metric definitions: prod_finance_gold.semantic.*
      Data classification: CONFIDENTIAL — Finance team and authorized users only.
    warehouse_id:  "abc123"
    certified_tables:
      - "prod_finance_gold.finance.fact_revenue"
      - "prod_finance_gold.finance.dim_customer"
    context_instructions: >
      Only answer questions about revenue, net revenue, discounts, and transaction counts.
      Do not expose individual-level data. Aggregate to minimum of customer segment.
      Refer users to the Finance data steward for metric definition questions.
```

---

## 7. BI Tool Semantic Layer (Tableau / Power BI)

### 7.1 Principles for BI Tool Semantics

BI tool semantic objects (Tableau Data Sources, Power BI Datasets/Dataflows) are **consumer-facing supplements** to the dbt semantic layer, not independent definition sources.

| Rule | Enforcement |
|---|---|
| BI tool metrics must derive from dbt-certified Gold objects or semantic views | 2LOD audit checks for non-certified sources |
| No custom metric calculations in BI tool that duplicate a dbt metric | Duplicate detection scan (see Section 9.3) |
| Certified BI datasets must be registered in the Report Registry (YAML) | Automated via BI config pipeline |
| Metric names in BI tools must match dbt metric labels exactly | Monthly consistency audit |
| Certified BI datasets must not allow direct connection to Bronze or Silver | Connection audit in 2LOD procedure |

### 7.2 Tableau Published Data Source Standard

```python
# tableau_semantic_publisher.py
"""
Publishes governed Tableau data sources from config.
Enforces that all certified data sources connect only to Gold/semantic objects.
"""

import tableauserverclient as TSC
import yaml
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TableauDataSourceConfig:
    name:              str
    project:           str
    source_type:       str           # "snowflake_semantic_view" | "gold_table"
    connection_string: str
    tier:              str
    domain:            str
    owner_email:       str
    certified:         bool
    metrics:           list[str] = field(default_factory=list)
    description:       str = ""


class TableauSemanticPublisher:
    """
    Manages certified Tableau data sources.
    All sources are config-driven and connect only to approved objects.
    """

    APPROVED_SOURCE_PATTERNS = [
        "prod_%_gold.",          # Gold layer tables
        "%.semantic.%",          # Semantic views
    ]

    def __init__(self, config_path: str, server_url: str, token_name: str, token_value: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.server = TSC.Server(server_url, use_server_version=True)
        self.auth = TSC.PersonalAccessTokenAuth(token_name, token_value, "Default")

    def validate_source(self, ds_config: TableauDataSourceConfig) -> bool:
        """Reject any data source connecting to Bronze or Silver."""
        conn = ds_config.connection_string.lower()
        approved = any(
            pat.replace("%", "").lower() in conn
            for pat in self.APPROVED_SOURCE_PATTERNS
        )
        if not approved:
            raise ValueError(
                f"Data source '{ds_config.name}' connects to a non-approved layer. "
                f"Only Gold and semantic view connections are permitted for certified sources."
            )
        return True
```

```yaml
# config/semantic/tableau_data_sources.yaml
data_sources:
  - name:       "Finance — Gross Revenue (Certified)"
    project:    "Certified"
    source_type: "snowflake_semantic_view"
    connection_string: "prod_finance_gold.semantic.revenue_semantic_view"
    tier:       "T1"
    domain:     "Finance"
    owner_email: "finance-data@company.com"
    certified:  true
    metrics:
      - "gross_revenue"
      - "net_revenue"
      - "discount_rate"
    description: >
      Certified Finance revenue data source.
      Source: Snowflake semantic view (mirrors dbt sem_revenue).
      All metric definitions approved by Finance Controller and DGO.
      Do not modify metric calculations in workbooks — use this source as-is.
```

### 7.3 Power BI Dataflow Standard

```yaml
# config/semantic/powerbi_dataflows.yaml
dataflows:
  - name:       "Finance Revenue — Certified Dataflow"
    workspace:  "Finance — Certified"
    source_type: "snowflake"
    source_object: "prod_finance_gold.semantic.revenue_semantic_view"
    tier:       "T1"
    certified:  true
    owner_email: "finance-data@company.com"
    description: >
      Certified Power BI dataflow for Finance revenue metrics.
      Connects to Snowflake semantic view.
      Metric definitions governed by dbt sem_revenue model.
    refresh_schedule:
      frequency: "daily"
      time_utc:  "06:00"
    endorsement: "Certified"        # Power BI endorsement flag
```

---

## 8. Metric Definition Standards

### 8.1 Naming Conventions

| Object Type | Convention | Examples |
|---|---|---|
| Semantic model | `sem_[domain_object]` | `sem_revenue`, `sem_orders`, `sem_customers` |
| Metric | `snake_case`, business term | `gross_revenue`, `monthly_active_users`, `churn_rate` |
| Measure (raw) | `[column_name]_[unit]` | `gross_revenue_usd`, `order_count`, `session_duration_seconds` |
| Dimension | `snake_case`, descriptive | `customer_segment`, `transaction_date`, `sales_region` |
| Derived metric | describes the formula | `discount_rate`, `revenue_per_customer`, `avg_order_value` |
| Certified metric file | `metrics_[domain].yml` | `metrics_finance.yml`, `metrics_sales.yml` |
| Semantic model file | `sem_[object].yml` | `sem_revenue.yml`, `sem_orders.yml` |

### 8.2 Metric Tier Definitions

| Tier | Definition | Change Process | Notice Period |
|---|---|---|---|
| **T1 — Critical** | Regulatory metrics, board-level KPIs, contractual SLAs. Error is a P1 incident. | Domain Owner + DGO + CDO approval; CAB review | 14 calendar days minimum |
| **T2 — Standard** | Core business metrics used in certified BI reports and ML features | Domain Owner + DGO approval | 7 calendar days |
| **T3 — Exploratory** | Team-level or experimental metrics in development | Domain Steward approval | No notice required; must not feed T1/T2 reports |

### 8.3 Prohibited Patterns

The following are zero-tolerance violations:

```
❌ PROHIBITED: Inline metric calculation in a BI report workbook that duplicates a dbt metric
❌ PROHIBITED: A metric with no owner or steward
❌ PROHIBITED: A T1 metric change merged without Domain Owner and DGO sign-off in the PR
❌ PROHIBITED: A metric sourcing from Bronze or Silver tables
❌ PROHIBITED: Two metrics with the same source column, same aggregation, and same filter
❌ PROHIBITED: A metric published to production without passing the duplicate detection check
❌ PROHIBITED: Hardcoded filter values in metric expressions (use config-driven filters)
❌ PROHIBITED: A semantic model referencing an uncertified Gold table
```

### 8.4 Dimension Standards

```yaml
# semantic_models/_shared_dimensions.yml
# Shared dimensions referenced across domain semantic models.
# Changes to shared dimensions require cross-domain DGO review.

version: 2

semantic_models:
  - name: dim_date_shared
    label: "Date (Shared)"
    description: >
      Canonical date dimension. Used by all domain semantic models.
      Fiscal calendar definitions sourced from Finance domain.
    model: ref('dim_date')
    meta:
      domain:   "Cross-Domain"
      owner:    "analytics-engineering@company.com"
      tier:     "T1"
      certified: true

    dimensions:
      - name: calendar_date
        type: time
        label: "Calendar Date"
        expr: calendar_date
        type_params:
          time_granularity: day

      - name: fiscal_quarter
        type: categorical
        label: "Fiscal Quarter"
        description: "Fiscal quarter label (e.g., FY2026-Q1). Fiscal year starts February 1."
        expr: fiscal_quarter_label

      - name: fiscal_year
        type: categorical
        label: "Fiscal Year"
        expr: fiscal_year_label

      - name: is_weekend
        type: categorical
        label: "Is Weekend"
        expr: is_weekend

      - name: is_holiday
        type: categorical
        label: "Is Holiday"
        description: "US federal holidays. Non-US holidays defined per region in dim_region."
        expr: is_us_holiday
```

### 8.5 Business Glossary Integration

Every T1 and T2 metric must be linked to a Collibra Business Glossary term. The link is bidirectional: the YAML carries the Collibra asset ID, and Collibra carries the Git path to the metric definition.

```python
# collibra_metric_sync.py
"""
Syncs dbt metric metadata to Collibra Business Glossary.
Creates or updates Collibra assets for each certified metric.
Bidirectional: also writes Git path back to Collibra asset.
Config-driven: Collibra connection and field mappings in YAML.
"""

import requests
import yaml
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CollibraMetricAsset:
    collibra_asset_id:  str
    name:               str
    description:        str
    domain:             str
    owner_email:        str
    tier:               str
    dbt_metric_name:    str
    git_path:           str
    certified:          bool
    certified_date:     str


class CollibraMetricSyncer:
    """
    Keeps Collibra Business Glossary in sync with dbt metric definitions.
    Run on every merge to main to ensure catalog reflects code.
    """

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.base_url   = self.config["collibra"]["base_url"]
        self.auth       = (
            self.config["collibra"]["username"],
            self.config["collibra"]["password"],
        )
        self.domain_id  = self.config["collibra"]["glossary_domain_id"]

    def sync_metric(self, asset: CollibraMetricAsset) -> str:
        """Upsert a metric asset in Collibra. Returns Collibra asset ID."""
        payload = {
            "name":         asset.name,
            "domainId":     self.domain_id,
            "typeId":       self.config["collibra"]["metric_type_id"],
            "attributes": [
                {"typeId": self.config["collibra"]["attr_description"],    "value": asset.description},
                {"typeId": self.config["collibra"]["attr_owner"],          "value": asset.owner_email},
                {"typeId": self.config["collibra"]["attr_tier"],           "value": asset.tier},
                {"typeId": self.config["collibra"]["attr_git_path"],       "value": asset.git_path},
                {"typeId": self.config["collibra"]["attr_certified"],      "value": str(asset.certified).lower()},
                {"typeId": self.config["collibra"]["attr_certified_date"], "value": asset.certified_date},
            ]
        }

        if asset.collibra_asset_id:
            resp = requests.put(
                f"{self.base_url}/assets/{asset.collibra_asset_id}",
                json=payload, auth=self.auth
            )
        else:
            resp = requests.post(
                f"{self.base_url}/assets",
                json=payload, auth=self.auth
            )

        resp.raise_for_status()
        return resp.json()["id"]

    def sync_all_from_dbt_catalog(self, dbt_catalog_path: str) -> list[str]:
        """Read dbt catalog.json and sync all certified metrics to Collibra."""
        with open(dbt_catalog_path) as f:
            catalog = json.load(f)

        synced_ids = []
        for metric in catalog.get("metrics", []):
            meta = metric.get("meta", {})
            if not meta.get("collibra_asset_id"):
                continue
            asset = CollibraMetricAsset(
                collibra_asset_id = meta.get("collibra_asset_id", ""),
                name              = metric["label"],
                description       = metric["description"],
                domain            = meta.get("domain", "Unknown"),
                owner_email       = meta.get("owner", ""),
                tier              = meta.get("tier", "T3"),
                dbt_metric_name   = metric["name"],
                git_path          = f"semantic_models/{meta.get('domain', '').lower()}/metrics_{meta.get('domain', '').lower()}.yml",
                certified         = bool(meta.get("certified_date")),
                certified_date    = meta.get("certified_date", ""),
            )
            synced_id = self.sync_metric(asset)
            synced_ids.append(synced_id)

        return synced_ids
```

---

## 9. Certification and Governance

### 9.1 Metric Certification Workflow

```
STEP 1 — Propose
  Analytics Engineer or Domain Steward authors metric YAML in a feature branch
  Includes all required metadata fields (see Section 8.1 tier table)
  Opens a Pull Request against main

STEP 2 — Automated Gate (CI/CD)
  □ YAML schema validation (all required fields present)
  □ Duplicate metric detection SQL (Section 9.3)
  □ dbt parse + compile (no syntax errors)
  □ Unit tests pass (metric consistency vs. source)
  □ Collibra asset ID format validation

STEP 3 — Review
  □ Peer review by Analytics Engineering team member
  □ Domain Data Steward reviews business definition accuracy
  □ T1/T2: Domain Data Owner approves in PR (required sign-off)
  □ T1 regulatory: DGO Lead reviews and approves

STEP 4 — Governance Gate
  □ DGO opens a Collibra certification task
  □ Collibra asset created / updated with pending certification status
  □ T1: CAB notification (no change window required, but notification is mandatory)

STEP 5 — Merge and Publish
  □ PR merged to main
  □ CI/CD deploys dbt semantic model changes to production
  □ Platform-native sync: Snowflake semantic view / Unity Catalog metric updated
  □ Collibra asset status set to "Certified"
  □ Report Registry and BI tool certified datasets notified of new/changed metric

STEP 6 — Validation
  □ Metric consistency test runs in post-deploy pipeline
  □ If consistency test fails: P2 incident opened (INC-DQ), PR reverted
```

### 9.2 Change Management for Existing Metrics

| Change Type | Classification | Approval Required | Notice Period |
|---|---|---|---|
| New metric (T3) | Standard | Domain Steward | None |
| New metric (T2) | Standard | Domain Owner + DGO | None (notification only) |
| New metric (T1) | Significant | Domain Owner + DGO + CDO | 7 days notification |
| Filter change on existing metric | Significant | Domain Owner + DGO | T1: 14 days / T2: 7 days |
| Aggregation type change | Breaking | Domain Owner + DGO + all consumer leads | T1: 14 days / T2: 7 days |
| Source table change | Breaking | Domain Owner + DGO + all consumer leads | T1: 14 days / T2: 7 days |
| Metric rename | Breaking | Domain Owner + DGO + all consumer leads | T1: 14 days / T2: 7 days |
| Metric deprecation | Breaking | Domain Owner + DGO + CDO | T1: 30 days / T2: 14 days |
| Metric deletion | Breaking | Domain Owner + DGO + CDO + all consumer leads | T1: 60 days / T2: 30 days |

### 9.3 Duplicate Metric Detection

Run before certifying any new metric. Any result from this query is a blocking gate failure.

```sql
-- Duplicate metric detection
-- Blocks certification if a new metric is substantively equivalent to an existing certified metric
-- Run as part of CI/CD semantic gate

SELECT
    m1.metric_name          AS candidate_metric,
    m2.metric_name          AS existing_certified_metric,
    m1.source_table         AS candidate_source,
    m2.source_table         AS existing_source,
    m1.aggregation_type,
    m1.filter_expression    AS candidate_filter,
    m2.filter_expression    AS existing_filter
FROM semantic_catalog.metrics_registry m1
CROSS JOIN semantic_catalog.metrics_registry m2
WHERE m1.metric_name          != m2.metric_name
  AND m2.certified              = TRUE
  AND m1.source_table           = m2.source_table
  AND m1.source_column          = m2.source_column
  AND m1.aggregation_type       = m2.aggregation_type
  AND COALESCE(m1.filter_expression, '') = COALESCE(m2.filter_expression, '')
ORDER BY m1.metric_name;
```

### 9.4 Metric Registry Table (Snowflake DDL)

```sql
CREATE TABLE IF NOT EXISTS data_governance.semantic.metrics_registry (
    metric_id              VARCHAR(60)   NOT NULL PRIMARY KEY,
    metric_name            VARCHAR(200)  NOT NULL,
    metric_label           VARCHAR(200),
    description            TEXT,
    metric_type            VARCHAR(30),            -- simple | ratio | derived | cumulative
    aggregation_type       VARCHAR(30),            -- sum | count | average | min | max
    source_table           VARCHAR(300),
    source_column          VARCHAR(200),
    filter_expression      TEXT,
    domain                 VARCHAR(100),
    tier                   VARCHAR(5),             -- T1 | T2 | T3
    owner_email            VARCHAR(200),
    steward_email          VARCHAR(200),
    collibra_asset_id      VARCHAR(100),
    glossary_term          VARCHAR(200),
    dbt_metric_name        VARCHAR(200),
    git_path               VARCHAR(500),
    certified              BOOLEAN       DEFAULT FALSE,
    certified_date         DATE,
    certified_by           VARCHAR(200),
    review_date            DATE,
    breaking_change_notice_days  INTEGER,
    regulatory_metric      BOOLEAN       DEFAULT FALSE,
    deprecated             BOOLEAN       DEFAULT FALSE,
    deprecated_at          TIMESTAMP_TZ,
    deprecation_reason     TEXT,
    inserted_at            TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP(),
    updated_at             TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);
```

---

## 10. Auditing the Semantic Layer

### 10.1 First Line of Defense — Self-Assessment Controls

#### Control SL-01: Metric Coverage Completeness

**Frequency:** Monthly
**Owner:** Analytics Engineering Lead

```sql
-- Identify certified Gold tables with no corresponding semantic model or metric
SELECT
    t.table_catalog,
    t.table_schema,
    t.table_name,
    t.certified,
    t.tier,
    COUNT(m.metric_id) AS metric_count
FROM data_governance.catalog.gold_tables t
LEFT JOIN data_governance.semantic.metrics_registry m
    ON m.source_table = t.table_catalog || '.' || t.table_schema || '.' || t.table_name
    AND m.certified = TRUE
    AND m.deprecated = FALSE
WHERE t.certified = TRUE
  AND t.layer = 'gold'
GROUP BY 1, 2, 3, 4, 5
HAVING metric_count = 0
ORDER BY t.tier, t.table_name;
```

Pass criteria: All T1 and T2 certified Gold tables have at least one certified metric.

#### Control SL-02: Orphaned Metric Scan

**Frequency:** Monthly
**Owner:** Analytics Engineering Lead

```sql
-- Metrics registered but whose source table is no longer certified or no longer exists
SELECT
    m.metric_name,
    m.domain,
    m.tier,
    m.source_table,
    m.certified,
    g.certified AS source_table_certified,
    g.table_name AS source_table_exists
FROM data_governance.semantic.metrics_registry m
LEFT JOIN data_governance.catalog.gold_tables g
    ON m.source_table = g.table_catalog || '.' || g.table_schema || '.' || g.table_name
WHERE m.certified = TRUE
  AND m.deprecated = FALSE
  AND (g.table_name IS NULL OR g.certified = FALSE)
ORDER BY m.tier, m.metric_name;
```

Pass criteria: Zero orphaned certified metrics.

#### Control SL-03: Metric Owner Currency

**Frequency:** Quarterly
**Owner:** DGO

```sql
-- Metrics with owner or steward who is no longer active in HR system
SELECT
    m.metric_name,
    m.domain,
    m.tier,
    m.owner_email,
    m.steward_email,
    m.certified_date,
    m.review_date
FROM data_governance.semantic.metrics_registry m
LEFT JOIN hr.active_employees o ON m.owner_email = o.email
LEFT JOIN hr.active_employees s ON m.steward_email = s.email
WHERE m.certified = TRUE
  AND m.deprecated = FALSE
  AND (o.email IS NULL OR s.email IS NULL)
ORDER BY m.tier, m.metric_name;
```

Pass criteria: Every certified metric has an active employee as both owner and steward.

#### Control SL-04: BI Tool Metric Consistency Scan

**Frequency:** Monthly
**Owner:** BI COE Lead

Validates that metric names used in certified BI reports match the dbt metric labels exactly.

```python
# semantic_bi_consistency_check.py
"""
Compares metric names used in certified Tableau/Power BI reports
against the canonical dbt metric label registry.
Flags divergences for remediation.
"""

import snowflake.connector
import yaml
from dataclasses import dataclass


@dataclass
class MetricConsistencyFinding:
    report_name: str
    bi_platform: str
    bi_metric_name: str
    closest_dbt_match: str | None
    severity: str   # CRITICAL | HIGH | MEDIUM


class BIMetricConsistencyChecker:

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**conn_params)

    def run(self) -> list[MetricConsistencyFinding]:
        """Compare BI report metrics against canonical dbt metric registry."""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                r.report_name,
                r.bi_platform,
                r.metric_name     AS bi_metric,
                m.metric_label    AS dbt_label,
                m.metric_name     AS dbt_name
            FROM data_governance.bi.report_metrics r
            LEFT JOIN data_governance.semantic.metrics_registry m
                ON LOWER(r.metric_name) = LOWER(m.metric_label)
                AND m.certified = TRUE
            WHERE r.report_tier IN ('T1', 'T2')
              AND m.metric_label IS NULL   -- No exact match found
            ORDER BY r.report_name
        """)

        findings = []
        for row in cursor.fetchall():
            findings.append(MetricConsistencyFinding(
                report_name=row[0],
                bi_platform=row[1],
                bi_metric_name=row[2],
                closest_dbt_match=None,
                severity="HIGH" if row[1] == "T1" else "MEDIUM",
            ))

        return findings
```

### 10.2 Second Line of Defense — Independent Audit Procedures

#### Audit SL-AU-01: Metric Definition Completeness and Accuracy

**Frequency:** Semi-Annual
**Auditor:** DGO (independent of Analytics Engineering)
**Evidence Required:**

```
□ Export of all T1/T2 metrics from metrics_registry
□ For a sample of 20% of T1 metrics:
    - Verify SQL expression produces correct result vs. source Gold table
    - Verify filter expression excludes appropriate records
    - Verify label and description match Collibra glossary term
□ Verify all T1 metrics have Domain Owner and DGO approval on the last change PR
□ Verify review_date is not overdue (no metric > 12 months without review)
```

**Audit SQL:**

```sql
-- T1/T2 metrics overdue for review
SELECT
    metric_name, domain, tier, owner_email,
    certified_date, review_date,
    DATEDIFF('day', review_date, CURRENT_DATE()) AS days_overdue
FROM data_governance.semantic.metrics_registry
WHERE certified = TRUE
  AND deprecated = FALSE
  AND tier IN ('T1', 'T2')
  AND review_date < CURRENT_DATE()
ORDER BY tier, days_overdue DESC;
```

#### Audit SL-AU-02: Source Layer Compliance

**Frequency:** Semi-Annual
**Auditor:** DGO

Verifies no certified metric sources from Bronze or Silver.

```sql
-- Certified metrics sourcing from non-Gold objects
SELECT
    m.metric_name, m.domain, m.tier, m.source_table,
    g.layer AS source_layer
FROM data_governance.semantic.metrics_registry m
LEFT JOIN data_governance.catalog.all_tables g
    ON m.source_table = g.table_catalog || '.' || g.table_schema || '.' || g.table_name
WHERE m.certified = TRUE
  AND m.deprecated = FALSE
  AND (g.layer IS NULL OR g.layer NOT IN ('gold', 'semantic'))
ORDER BY m.tier, m.metric_name;
```

Finding of any T1 or T2 metric sourcing from Bronze/Silver is a **CRITICAL** audit finding.

#### Audit SL-AU-03: BI Tool Bypass Detection

**Frequency:** Semi-Annual
**Auditor:** DGO

Identifies BI reports that bypass the semantic layer and query Gold tables directly without using a certified data source.

```sql
-- Tableau/Power BI connections that are not registered certified data sources
SELECT
    r.report_name,
    r.bi_platform,
    r.connection_object,
    r.report_tier,
    ds.name AS certified_datasource_name
FROM data_governance.bi.report_connections r
LEFT JOIN data_governance.bi.certified_datasources ds
    ON r.connection_object = ds.source_object
    AND ds.certified = TRUE
WHERE r.report_tier IN ('T1', 'T2')
  AND ds.name IS NULL
ORDER BY r.report_tier, r.bi_platform, r.report_name;
```

#### Audit SL-AU-04: Collibra Sync Verification

**Frequency:** Quarterly
**Auditor:** DGO

Validates that Collibra Business Glossary is in sync with the dbt metric registry.

```python
# collibra_sync_audit.py
"""
Compares Collibra Business Glossary assets against the dbt metrics_registry.
Identifies: metrics in Git but not in Collibra, metrics in Collibra but not in Git,
and metadata mismatches.
"""

import requests
import snowflake.connector
import yaml
from dataclasses import dataclass


@dataclass
class SyncFinding:
    metric_name: str
    finding_type: str   # MISSING_IN_COLLIBRA | MISSING_IN_REGISTRY | METADATA_MISMATCH
    detail: str
    severity: str       # CRITICAL | HIGH | MEDIUM


class CollibraSyncAuditor:

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**conn_params)
        self.collibra_base = self.config["collibra"]["base_url"]
        self.auth = (
            self.config["collibra"]["username"],
            self.config["collibra"]["password"],
        )

    def audit(self) -> list[SyncFinding]:
        findings = []
        registry_metrics = self._get_registry_metrics()
        collibra_metrics = self._get_collibra_metrics()

        # Metrics in registry but missing in Collibra
        for m in registry_metrics:
            if m["collibra_asset_id"] not in collibra_metrics:
                findings.append(SyncFinding(
                    metric_name=m["metric_name"],
                    finding_type="MISSING_IN_COLLIBRA",
                    detail=f"Asset ID {m['collibra_asset_id']} not found in Collibra.",
                    severity="HIGH" if m["tier"] in ("T1", "T2") else "MEDIUM",
                ))

        return findings

    def _get_registry_metrics(self) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT metric_name, collibra_asset_id, tier, certified
            FROM data_governance.semantic.metrics_registry
            WHERE certified = TRUE AND deprecated = FALSE
        """)
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

    def _get_collibra_metrics(self) -> set[str]:
        resp = requests.get(
            f"{self.collibra_base}/assets",
            params={"typeId": self.config["collibra"]["metric_type_id"]},
            auth=self.auth,
        )
        resp.raise_for_status()
        return {a["id"] for a in resp.json().get("results", [])}
```

---

## 11. Config-Based Management and Change Control

### 11.1 Configuration Hierarchy

All semantic layer behavior is externalized to YAML configuration. No metric definitions, filter expressions, or business logic are hardcoded in Python or SQL files.

```
config/
  semantic/
    ├── metric_registry_config.yaml      # Master metric registry config
    ├── metric_validation_config.yaml    # Consistency test queries per metric
    ├── cortex_config.yaml               # Snowflake Cortex Analyst semantic views
    ├── unity_catalog_metrics.yaml       # Databricks Unity Catalog metrics
    ├── tableau_data_sources.yaml        # Certified Tableau data sources
    ├── powerbi_dataflows.yaml           # Certified Power BI dataflows
    ├── genie_spaces.yaml                # Databricks AI/BI Genie spaces
    └── collibra_sync_config.yaml        # Collibra API connection and field IDs
```

### 11.2 CI/CD Pipeline for Semantic Layer

```yaml
# .github/workflows/semantic_layer_cicd.yml
name: Semantic Layer CI/CD

on:
  push:
    branches: [main]
    paths:
      - 'semantic_models/**'
      - 'models/gold/**'
      - 'config/semantic/**'
  pull_request:
    branches: [main]
    paths:
      - 'semantic_models/**'
      - 'models/gold/**'
      - 'config/semantic/**'

jobs:

  validate:
    name: "Schema and YAML Validation"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pyyaml jsonschema --break-system-packages
      - name: Validate metric YAML schemas
        run: python ci/validate_metric_schemas.py --path semantic_models/

  dbt_parse:
    name: "dbt Parse and Compile"
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install dbt-snowflake --break-system-packages
      - run: dbt parse --profiles-dir profiles/ --target ci
      - run: dbt compile --profiles-dir profiles/ --target ci

  duplicate_detection:
    name: "Duplicate Metric Detection"
    needs: dbt_parse
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run duplicate metric scan
        run: python ci/detect_duplicate_metrics.py
        env:
          SNOWFLAKE_ACCOUNT:   ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER:      ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD:  ${{ secrets.SNOWFLAKE_PASSWORD }}

  metric_tests:
    name: "Metric Consistency Tests"
    needs: dbt_parse
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run metric consistency validation
        run: |
          python -c "
          from src.semantic.metric_validator import SemanticMetricValidator
          v = SemanticMetricValidator('config/semantic/metric_validation_config.yaml', conn_params)
          results = v.run_all_validations(validation_date='today')
          failures = [r for r in results if not r.passed]
          if failures:
              raise SystemExit(f'{len(failures)} metric consistency failures')
          "

  deploy_snowflake:
    name: "Deploy Snowflake Semantic Views"
    needs: [dbt_parse, duplicate_detection]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: dbt run --select "semantic_models+" --target prod
      - run: python ci/sync_snowflake_semantic_views.py

  deploy_unity_catalog:
    name: "Deploy Unity Catalog Metrics"
    needs: [dbt_parse, duplicate_detection]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python ci/sync_unity_catalog_metrics.py

  sync_collibra:
    name: "Sync Collibra Business Glossary"
    needs: [deploy_snowflake, deploy_unity_catalog]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: dbt docs generate
      - name: Sync metrics to Collibra
        run: python ci/collibra_metric_sync.py --catalog target/catalog.json
        env:
          COLLIBRA_USERNAME: ${{ secrets.COLLIBRA_USERNAME }}
          COLLIBRA_PASSWORD: ${{ secrets.COLLIBRA_PASSWORD }}

  post_deploy_validation:
    name: "Post-Deploy Metric Consistency"
    needs: [deploy_snowflake, deploy_unity_catalog]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run post-deploy consistency suite
        run: python ci/post_deploy_metric_validation.py
```

### 11.3 Change Classification Reference

| Change Type | Classification | CAB Notification | Approval |
|---|---|---|---|
| New T3 metric | Standard | None | Steward |
| New T2 metric | Standard | None | Owner + DGO |
| New T1 metric | Significant | Required (inform) | Owner + DGO + CDO |
| Metric filter change (T2) | Significant | None | Owner + DGO |
| Metric filter change (T1) | Significant | Required | Owner + DGO |
| Metric aggregation change | Breaking | Required | Owner + DGO + all consumers |
| Source column change | Breaking | Required | Owner + DGO + all consumers |
| Semantic model restructure | Breaking | Required | Owner + DGO + CAB |
| Platform semantic view update | Standard | None | Analytics Eng |
| Collibra glossary term update | Standard | None | Steward + DGO |
| Metric deprecation (T2) | Breaking | Required (14 days) | Owner + DGO |
| Metric deprecation (T1) | Breaking | Required (30 days) | Owner + DGO + CDO |

### 11.4 Rollback Procedure

If a deployed metric change causes a consistency test failure or downstream incident:

```bash
# 1. Revert the dbt metric change in Git
git revert <commit_hash> --no-commit
git commit -m "Revert: [metric_name] change — consistency failure INC-[ID]"
git push origin main

# 2. Re-deploy the previous semantic model state
dbt run --select "semantic_models+" --target prod

# 3. Re-sync platform-native layers
python ci/sync_snowflake_semantic_views.py
python ci/sync_unity_catalog_metrics.py

# 4. Update Collibra asset status to "Under Review"
# (done via Collibra UI or API by DGO)

# 5. Open incident record
# INC-DQ for consistency failures
# INC-BI if a report was already serving incorrect data
```

---

## 12. Ground-Up Build Strategy

### 12.1 Phase Overview

| Phase | Weeks | Focus | Exit Criteria |
|---|---|---|---|
| **Phase 0** — Foundation | 1–2 | Tooling, project scaffold, team alignment | dbt project scaffolded, Collibra metric type created, team trained |
| **Phase 1** — Priority Domain | 3–8 | First domain end-to-end (Finance or Sales) | 5–10 T1 metrics certified and serving BI reports |
| **Phase 2** — Expand Domains | 9–20 | Remaining priority domains onboarded | All T1 business KPIs covered by certified metrics |
| **Phase 3** — Platform Integration | 21–26 | Snowflake Cortex / Unity Catalog / NLQ | NLQ available to business users via Genie/Cortex |
| **Phase 4** — Operationalize | 27+ | Monitoring, audits, self-service governance | All audit controls passing; quarterly review cadence established |

### 12.2 Phase 0 — Foundation (Weeks 1–2)

```
□ Install dbt + dbt-snowflake / dbt-databricks
□ Initialize dbt project with semantic_models/ directory structure (Section 4.1)
□ Create metric_registry DDL in Snowflake (Section 9.4)
□ Configure Collibra: create "Data Metric" asset type, add required attributes
□ Set up GitHub Actions CI/CD skeleton (Section 11.2)
□ Define the metric tier classification policy (T1/T2/T3) and get CDO sign-off
□ Identify the Priority Domain and 5–10 candidate T1 metrics
□ Run a 1-hour "Metric definition workshop" with the Priority Domain data owner:
    - What are your top 5 KPIs?
    - What is the exact business definition of each?
    - What filters apply (e.g., exclude voided, exclude test accounts)?
    - What is the grain of the source table?
□ Publish the Semantic Layer charter to the data portal (Collibra / Confluence)
```

### 12.3 Phase 1 — First Domain (Weeks 3–8)

```
Week 3–4: Audit the Priority Domain Gold layer
  □ All T1/T2 Gold tables certified (see Data Product Certification Framework)
  □ Column-level lineage documented for all fact table measure columns
  □ PII and classification tags applied

Week 5–6: Author semantic models and metrics YAML
  □ sem_[object].yml for each fact table in scope
  □ metrics_[domain].yml with all agreed T1 metrics
  □ Shared dimensions defined in _shared_dimensions.yml
  □ All required metadata fields populated

Week 7: CI/CD gate + certification
  □ Duplicate detection passes (no existing metrics conflict)
  □ Metric consistency tests pass vs. Gold table direct SQL
  □ Domain Owner and DGO approval obtained
  □ Collibra assets created and linked

Week 8: Connect BI consumers
  □ Certified Tableau data source / Power BI dataflow published
  □ 2–3 T1 BI reports migrated to use certified source (not raw table)
  □ Post-migration validation: report values match pre-migration values within 0.1%
  □ Announce availability to Finance / Sales business team
```

### 12.4 Phase 2 — Expand Domains (Weeks 9–20)

Each additional domain follows the same 4-week pattern:
- Week 1: Domain metric workshop + Gold audit
- Week 2: Author YAML + peer review
- Week 3: CI/CD gate + certification
- Week 4: BI consumer migration + validation

Priority order recommendation: Finance → Sales → Customer/Marketing → Operations → HR → Remaining

### 12.5 Phase 3 — Platform Integration (Weeks 21–26)

```
Week 21–22: Snowflake Cortex Analyst
  □ Semantic views created for all certified domains (Section 5.2)
  □ Synonyms added for common business aliases
  □ Cortex Analyst tested with top-10 business questions per domain
  □ NLQ accuracy benchmarked: target >80% correct interpretation

Week 23–24: Databricks AI/BI Genie (if Databricks primary)
  □ Unity Catalog metrics registered for all certified domains (Section 6.1)
  □ Genie spaces created per domain (Section 6.2)
  □ Context instructions added to constrain scope and prevent PII exposure

Week 25–26: Self-service enablement
  □ Business user guide published (Section 14 template)
  □ Metric catalog page in Collibra / data portal live
  □ Metric request workflow established (how business users request new T3 metrics)
```

### 12.6 Maturity Model

| Level | Name | Characteristics |
|---|---|---|
| **L0** — Unmanaged | No semantic layer | Metrics defined ad-hoc in BI workbooks; no consistency |
| **L1** — Foundation | Basic metric definitions | dbt models with documented metrics; no formal governance |
| **L2** — Governed | Certified metrics | Formal certification process; Collibra integration; CI/CD gates |
| **L3** — Integrated | Platform-native serving | Snowflake Cortex / Unity Catalog metrics synced; NLQ available |
| **L4** — Optimized | Self-service governance | Business users can discover and request metrics; automated monitoring; quarterly audit cycle |

---

## 13. KPIs and Health Metrics

### 13.1 Semantic Layer Health KPIs

| KPI | Definition | Target | Tier |
|---|---|---|---|
| **Metric certification coverage** | % of T1/T2 business KPIs with a certified metric definition | ≥ 95% | T1 |
| **Metric consistency pass rate** | % of daily metric consistency tests passing | ≥ 99.5% | T1 |
| **Orphaned metric rate** | % of certified metrics with no active owner or source table | 0% | T1 |
| **BI source compliance rate** | % of T1/T2 BI reports connecting to certified semantic sources | ≥ 98% | T1 |
| **Collibra sync lag** | Hours since last successful Collibra sync | ≤ 24 hr | T2 |
| **Duplicate metric count** | Count of certified metrics with substantively equivalent definitions | 0 | T1 |
| **Overdue metric reviews** | Count of T1/T2 metrics with review_date > today | 0 | T2 |
| **Mean time to certify** | Average days from metric PR open to certified | ≤ 10 days | T2 |
| **Breaking change notice compliance** | % of breaking changes that met the required notice period | 100% | T1 |

### 13.2 KPI Collection Python Pattern

```python
# semantic_kpi_collector.py
"""
Collects semantic layer health KPIs and writes to Snowflake scorecard table.
Config-driven: all query definitions and thresholds in YAML.
"""

import snowflake.connector
import yaml
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class SemanticKPI:
    kpi_name:    str
    value:       float
    target:      float
    unit:        str
    passed:      bool
    collected_at: datetime


class SemanticKPICollector:

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**conn_params)

    def collect_all(self) -> list[SemanticKPI]:
        results = []
        for kpi_cfg in self.config["kpis"]:
            value = self._run_query(kpi_cfg["query"])
            target = kpi_cfg["target"]
            passed = self._evaluate(value, target, kpi_cfg["comparison"])
            results.append(SemanticKPI(
                kpi_name=kpi_cfg["name"],
                value=value,
                target=target,
                unit=kpi_cfg.get("unit", ""),
                passed=passed,
                collected_at=datetime.now(timezone.utc),
            ))
        self._persist(results)
        return results

    def _run_query(self, query: str) -> float:
        cursor = self.conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def _evaluate(self, value: float, target: float, comparison: str) -> bool:
        return {
            "gte": value >= target,
            "lte": value <= target,
            "eq":  value == target,
        }.get(comparison, False)

    def _persist(self, kpis: list[SemanticKPI]) -> None:
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO data_governance.semantic.kpi_scorecard
                (kpi_name, value, target, unit, passed, collected_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [
            (k.kpi_name, k.value, k.target, k.unit, k.passed, k.collected_at)
            for k in kpis
        ])
```

---

## 14. Appendix: Templates and Reference SQL

### A. New Metric Request Template

```markdown
## Metric Request — [Metric Name]

**Requested by:** [Name, Team]
**Date:** [YYYY-MM-DD]
**Domain:** [Finance / Sales / Customer / etc.]
**Proposed Tier:** T1 / T2 / T3

### Business Definition
[Plain-language definition. What does this metric measure? Who uses it?]

### Formula
[How is it calculated? Numerator / denominator? Filters?]

### Source
[Which Gold table / view should be the source? If unsure, which system owns the data?]

### Dimensions Required
[What dimensions should this metric be sliceable by?]

### Consumers
- BI reports: [list]
- ML models: [list]
- APIs / other: [list]

### Why a new metric?
[Does an existing metric not meet this need? Explain the gap.]

### Data Owner Approval
[ ] Domain Data Owner has reviewed and approved this request
Owner name: _____________________ Date: __________
```

### B. Metric Deprecation Notice Template

```markdown
## Metric Deprecation Notice — [Metric Name]

**Effective Deprecation Date:** [YYYY-MM-DD]
**Notice Period:** [14 / 30 / 60] days
**Replacement Metric (if applicable):** [new_metric_name]

**Reason for Deprecation:**
[Business reason, data model change, metric replaced by more precise definition, etc.]

**Impact:**
- BI reports using this metric: [list]
- ML features using this metric: [list]
- APIs using this metric: [list]

**Migration Instructions:**
[Step-by-step: how to migrate from this metric to the replacement]

**Owner:** [Domain Data Owner name]
**DGO Approval:** [DGO Lead name, date]
```

### C. Metric Registry DDL — Full Schema

```sql
-- Full DDL for the metrics registry and audit tables

CREATE SCHEMA IF NOT EXISTS data_governance.semantic;

CREATE TABLE IF NOT EXISTS data_governance.semantic.metrics_registry (
    metric_id              VARCHAR(60)   NOT NULL PRIMARY KEY,
    metric_name            VARCHAR(200)  NOT NULL UNIQUE,
    metric_label           VARCHAR(200),
    description            TEXT,
    metric_type            VARCHAR(30),
    aggregation_type       VARCHAR(30),
    source_table           VARCHAR(300),
    source_column          VARCHAR(200),
    filter_expression      TEXT,
    domain                 VARCHAR(100),
    tier                   VARCHAR(5),
    owner_email            VARCHAR(200),
    steward_email          VARCHAR(200),
    collibra_asset_id      VARCHAR(100),
    glossary_term          VARCHAR(200),
    dbt_metric_name        VARCHAR(200),
    git_path               VARCHAR(500),
    certified              BOOLEAN       DEFAULT FALSE,
    certified_date         DATE,
    certified_by           VARCHAR(200),
    review_date            DATE,
    breaking_change_notice_days INTEGER,
    regulatory_metric      BOOLEAN       DEFAULT FALSE,
    deprecated             BOOLEAN       DEFAULT FALSE,
    deprecated_at          TIMESTAMP_TZ,
    deprecation_reason     TEXT,
    inserted_at            TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP(),
    updated_at             TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS data_governance.semantic.metric_change_log (
    change_id       VARCHAR(60)   NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    metric_id       VARCHAR(60)   NOT NULL,
    metric_name     VARCHAR(200),
    change_type     VARCHAR(50),   -- CREATED | UPDATED | CERTIFIED | DEPRECATED | DELETED
    changed_by      VARCHAR(200),
    change_summary  TEXT,
    pr_url          VARCHAR(500),
    changed_at      TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS data_governance.semantic.kpi_scorecard (
    scorecard_id    VARCHAR(60)   NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::VARCHAR,
    kpi_name        VARCHAR(200),
    value           FLOAT,
    target          FLOAT,
    unit            VARCHAR(50),
    passed          BOOLEAN,
    collected_at    TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);

-- Clustered for query performance
ALTER TABLE data_governance.semantic.metrics_registry
    CLUSTER BY (domain, tier, certified);

ALTER TABLE data_governance.semantic.kpi_scorecard
    CLUSTER BY (collected_at::DATE);
```

### D. Collibra Configuration Reference

```yaml
# config/semantic/collibra_sync_config.yaml
collibra:
  base_url:          "https://your-org.collibra.com/rest/2.0"
  username:          "${COLLIBRA_USERNAME}"        # Injected from secrets manager
  password:          "${COLLIBRA_PASSWORD}"        # Injected from secrets manager
  glossary_domain_id: "clb-domain-business-glossary-001"
  metric_type_id:    "clb-type-data-metric-001"

  # Collibra attribute type IDs for metric assets
  attr_description:    "clb-attr-description-001"
  attr_owner:          "clb-attr-data-owner-001"
  attr_steward:        "clb-attr-data-steward-001"
  attr_tier:           "clb-attr-metric-tier-001"
  attr_domain:         "clb-attr-domain-001"
  attr_git_path:       "clb-attr-git-path-001"
  attr_dbt_name:       "clb-attr-dbt-metric-name-001"
  attr_certified:      "clb-attr-certified-001"
  attr_certified_date: "clb-attr-certified-date-001"
  attr_review_date:    "clb-attr-review-date-001"
  attr_regulatory:     "clb-attr-regulatory-metric-001"

  # Relationship type IDs
  rel_derived_from:    "clb-rel-derived-from-001"  # Metric → Gold Table
  rel_owned_by:        "clb-rel-owned-by-001"      # Metric → Data Owner
  rel_steward:         "clb-rel-stewarded-by-001"  # Metric → Data Steward
  rel_implements:      "clb-rel-implements-001"    # Metric → Business Term
```

---

*Document Owner: Chief Data Officer + Analytics Engineering Lead*
*Review Cycle: Semi-Annual or upon material platform change*
*Related: `01_DE_Best_Practices.md` · `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` · `03_DE_Standards.md` · `01_BI_Best_Practices.md` · `01_ML_Best_Practices.md` · `README.md`*
