# Data Engineering Standards
## Binding Standards for the Modern Data Lakehouse Program

**Document Owner:** Chief Data Office  
**Domain:** Data Engineering  
**Version:** 1.0  
**Classification:** Internal — Binding Standard  
**Review Cycle:** Annual (or upon major platform change)

---

> **Note:** These are **binding standards**, not guidelines. Exceptions require written approval from the Data Engineering Lead and Data Governance Lead. All exceptions are logged and reviewed quarterly.

---

## Table of Contents

1. [Naming Conventions](#1-naming-conventions)
2. [Object Creation Standards](#2-object-creation-standards)
3. [Code Standards](#3-code-standards)
4. [Pipeline Standards](#4-pipeline-standards)
5. [Security & Access Standards](#5-security--access-standards)
6. [Data Quality Standards](#6-data-quality-standards)
7. [Documentation Standards](#7-documentation-standards)
8. [Version Control Standards](#8-version-control-standards)
9. [Cost Management Standards](#9-cost-management-standards)
10. [Exception Process](#10-exception-process)

---

## 1. Naming Conventions

### 1.1 Database / Catalog Naming

**Standard:** `{ENV}_{DOMAIN}_{LAYER}`

| Component | Allowed Values | Example |
|---|---|---|
| `ENV` | `DEV`, `STG`, `PROD` | `PROD` |
| `DOMAIN` | From approved domain taxonomy | `FINANCE`, `SALES`, `HR`, `CUSTOMER`, `OPERATIONS`, `RISK`, `PRODUCT` |
| `LAYER` | `BRONZE`, `SILVER`, `GOLD` | `GOLD` |

**Full example:** `PROD_FINANCE_GOLD`  
**Databricks catalog equivalent:** `prod_finance_gold` *(lowercase)*

### 1.2 Schema Naming

**Standard:** `{SOURCE_SYSTEM}` (Bronze) or `{BUSINESS_DOMAIN}` (Silver/Gold)

| Layer | Schema Naming | Example |
|---|---|---|
| Bronze | Source system name | `erp`, `crm`, `salesforce` |
| Silver | Source system or domain | `erp_cleansed`, `crm_cleansed` |
| Gold | Business domain | `finance`, `sales`, `customer` |

### 1.3 Table Naming

| Object Type | Prefix | Example |
|---|---|---|
| Fact table | `fact_` | `fact_revenue` |
| Dimension table | `dim_` | `dim_customer` |
| Bridge/junction | `bridge_` | `bridge_customer_product` |
| Staging/intermediate | `stg_` | `stg_erp_gl_transactions` |
| Intermediate (dbt) | `int_` | `int_orders_aggregated` |
| Snapshot (SCD2) | `snap_` | `snap_dim_customer` |
| Aggregate/summary | `agg_` | `agg_monthly_revenue` |
| Lookup/reference | `lkp_` | `lkp_currency_codes` |

**Rules:**
- All lowercase; words separated by underscores
- No abbreviations unless in the approved abbreviation registry
- No special characters except underscore
- Maximum 128 characters

### 1.4 Column Naming

| Pattern | Example |
|---|---|
| Primary key | `{table_name_singular}_key` → `customer_key` |
| Natural/business key | `{entity}_id` → `customer_id` |
| Foreign key | Same as referenced PK → `customer_key` |
| Date | `{context}_date` → `transaction_date` |
| Timestamp | `{context}_at` → `created_at`, `updated_at` |
| Flag/boolean | `is_{condition}` or `has_{condition}` → `is_active`, `has_orders` |
| Audit columns | Prefixed with underscore → `_batch_id`, `_ingested_at` |
| Amount/measure | `{measure}_{unit}` → `revenue_usd`, `quantity_units` |

### 1.5 Pipeline / Job Naming

**Standard:** `{domain}_{source}_{destination}_{frequency}`

| Component | Example |
|---|---|
| Domain | `finance` |
| Source | `erp` |
| Destination layer | `bronze` |
| Frequency | `daily`, `hourly`, `streaming` |

**Full example:** `finance_erp_bronze_daily`

### 1.6 Warehouse / Cluster Naming

**Snowflake Warehouses:** `{WORKLOAD}_{ENV}_WH`  
Examples: `TRANSFORM_PROD_WH`, `BI_PROD_WH`, `ML_PROD_WH`

**Databricks Job Clusters:** Created dynamically per job; named `{job_name}_cluster`  
**Databricks All-Purpose:** `{team}_{user_initials}_dev_cluster` (dev only)

---

## 2. Object Creation Standards

### 2.1 All Objects Must Be IaC-Managed

**Standard:** No Snowflake database, schema, warehouse, role, or grant may be created outside of Terraform in staging or production environments.

**Standard:** No Databricks catalog, schema, cluster policy, or workspace object may be created outside of Terraform in staging or production environments.

**Verification:** Terraform state drift detection runs nightly. Any drift triggers a P2 alert.

### 2.2 Required Object Properties

#### Snowflake Tables

```sql
-- Every table must be created with these properties
CREATE TABLE {database}.{schema}.{table_name} (
    -- columns here --
)
COMMENT = '{business description}'
DATA_RETENTION_TIME_IN_DAYS = {per_policy}  -- 1 (dev), 7 (staging), 90 (prod)
ENABLE_SCHEMA_EVOLUTION = FALSE;             -- Explicit evolution only
```

#### Databricks / Delta Tables

```python
# Every Delta table created via code must include:
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {catalog}.{schema}.{table_name} (
    -- columns here --
)
USING DELTA
COMMENT '{business_description}'
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'owner' = '{owner_team}',
    'domain' = '{domain}',
    'layer' = '{layer}',
    'data_classification' = '{classification}'
)
""")
```

### 2.3 Required Audit Columns

All Silver and Gold tables must include these columns:

```sql
_batch_id          VARCHAR(36)   NOT NULL,  -- UUID for the pipeline run
_source_system     VARCHAR(100)  NOT NULL,  -- Source system name
_ingested_at       TIMESTAMP_NTZ NOT NULL,  -- Timestamp landed in Bronze
_processed_at      TIMESTAMP_NTZ NOT NULL,  -- Timestamp written to this layer
_pipeline_version  VARCHAR(50)   NOT NULL,  -- Git tag of the pipeline code
_is_deleted        BOOLEAN       NOT NULL DEFAULT FALSE  -- Soft delete flag
```

### 2.4 Surrogate Keys

- Surrogate keys must be **deterministic hashes** (SHA-256) of the natural key components — not sequences or UUIDs.
- This ensures idempotency across pipeline runs.

```python
import hashlib

def generate_surrogate_key(*natural_key_parts: str) -> str:
    """Generate deterministic surrogate key from natural key components."""
    combined = "|".join(str(p).strip().upper() for p in natural_key_parts)
    return hashlib.sha256(combined.encode()).hexdigest()
```

---

## 3. Code Standards

### 3.1 Python Standards

| Standard | Rule |
|---|---|
| Python version | 3.11+ |
| Style guide | PEP 8; enforced via `ruff` or `black` |
| Type hints | Required on all function signatures |
| Docstrings | Required on all public functions and classes (Google style) |
| Max line length | 120 characters |
| Import order | Standard lib → third-party → internal (enforced via `isort`) |
| Exception handling | Catch specific exceptions; never bare `except:` |
| Logging | Use Python `logging` module; never `print()` in production code |
| Secrets | Never in code; always retrieved from secrets manager at runtime |
| Hardcoded values | Never. All business values go in config files |

### 3.2 SQL Standards (dbt and direct SQL)

| Standard | Rule |
|---|---|
| Keyword case | Uppercase (`SELECT`, `FROM`, `WHERE`, `JOIN`) |
| Identifier case | Lowercase with underscores |
| Indentation | 4 spaces |
| CTEs | Preferred over subqueries for readability |
| SELECT * | Never in production models |
| Explicit column aliases | Always on aggregations and expressions |
| Table aliases | Always meaningful (not single letters in complex queries) |
| Comments | Required on non-obvious logic |

```sql
-- GOOD: CTE-based, explicit columns, meaningful aliases
WITH orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        o.total_amount_usd
    FROM {{ ref('stg_erp_orders') }} AS o
    WHERE o.is_voided = FALSE
),

customer_orders AS (
    SELECT
        customer_id,
        COUNT(order_id)         AS total_orders,
        SUM(total_amount_usd)   AS lifetime_value_usd,
        MIN(order_date)         AS first_order_date,
        MAX(order_date)         AS last_order_date
    FROM orders
    GROUP BY customer_id
)

SELECT * FROM customer_orders
```

### 3.3 Notebook Standards (Databricks)

- Notebooks are for **development and exploration only**. Production pipelines must be Python files or dbt models.
- Notebooks must not contain hardcoded credentials.
- Notebooks used in production workflows must be converted to `.py` files with proper unit tests before promotion.
- All notebooks must have a header cell with: author, date, purpose, and cluster requirements.

---

## 4. Pipeline Standards

### 4.1 Mandatory Pipeline Properties

Every production pipeline must have:

| Property | Standard |
|---|---|
| Config file | YAML config file, version-controlled, environment-parameterized |
| Idempotency | Re-runnable; same input = same output |
| Incremental load | Watermark-based; no full-reload unless explicitly configured |
| Error handling | All exceptions caught, logged, and written to dead letter table |
| Retry logic | 3 retries with exponential backoff (default) |
| Alerting | Failure and SLA breach alerts to Slack + PagerDuty |
| Observability | Row counts, duration, and status logged per run |
| Lineage | Registered in data catalog upon first successful run |
| Data contract | Signed contract for all Gold-layer outputs |

### 4.2 Retry Standard

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=30, max=300),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True
)
def execute_with_retry(fn, *args, **kwargs):
    return fn(*args, **kwargs)
```

### 4.3 Dead Letter Table Standard

```sql
-- Create in Bronze layer per domain
CREATE TABLE {env}_{domain}_bronze.{schema}.dead_letter_queue (
    dl_id              VARCHAR(36)    NOT NULL DEFAULT UUID_STRING(),
    pipeline_name      VARCHAR(200)   NOT NULL,
    batch_id           VARCHAR(36)    NOT NULL,
    source_system      VARCHAR(100)   NOT NULL,
    error_type         VARCHAR(200)   NOT NULL,
    error_message      VARCHAR(4000)  NOT NULL,
    failed_record      VARIANT,                -- Raw failed record
    stack_trace        VARCHAR(8000),
    retry_count        INTEGER        NOT NULL DEFAULT 0,
    resolved           BOOLEAN        NOT NULL DEFAULT FALSE,
    created_at         TIMESTAMP_NTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP()
)
COMMENT = 'Dead letter queue for failed pipeline records. Review and resolve within 48 hours.'
DATA_RETENTION_TIME_IN_DAYS = 30;
```

---

## 5. Security & Access Standards

### 5.1 Credential Standards

| Rule | Standard |
|---|---|
| No hardcoded secrets | Zero tolerance; enforced via pre-commit hook and CI scan |
| Secret rotation | Service account keys rotated every 90 days |
| MFA | Required for all human users on all platforms |
| SSO | Required; username/password login disabled in staging and prod |
| Least privilege | Service accounts have only the permissions needed for their task |
| No shared credentials | Every service has its own service account |
| Audit trail | All credential access events logged |

### 5.2 Data Access Standards

| Data Classification | Who Can Access | Access Method |
|---|---|---|
| `PUBLIC` | Any authenticated user | Direct or BI tool |
| `INTERNAL` | All employees | BI tool preferred; direct access with role |
| `CONFIDENTIAL` | Data roles + approved business users | Role-based; BI tool masked display |
| `RESTRICTED` | Named individuals only | Dynamic data masking + audit trail |
| `TOP_SECRET` | Named executives + legal | Separate secured environment |

### 5.3 Dynamic Data Masking (Snowflake)

```sql
-- Masking policy for PII — applied at column level
CREATE MASKING POLICY governance.policies.mask_email
AS (val STRING) RETURNS STRING ->
    CASE
        WHEN IS_ROLE_IN_SESSION('ANALYST_RESTRICTED_ROLE') THEN val
        ELSE REGEXP_REPLACE(val, '.+@', '***@')
    END;

ALTER TABLE prod_finance_gold.finance.dim_customer
    MODIFY COLUMN email
    SET MASKING POLICY governance.policies.mask_email;
```

---

## 6. Data Quality Standards

### 6.1 Required Tests Per Layer

| Test | Bronze | Silver | Gold |
|---|---|---|---|
| Row count > 0 | ✅ Required | ✅ Required | ✅ Required |
| Freshness SLA | ✅ Required | ✅ Required | ✅ Required |
| Schema validation | ✅ Required | ✅ Required | ✅ Required |
| PK uniqueness | — | ✅ Required | ✅ Required |
| Not null (key cols) | ✅ Required | ✅ Required | ✅ Required |
| Accepted values | — | ✅ If applicable | ✅ Required |
| Referential integrity | — | ✅ Required | ✅ Required |
| Value range checks | — | ✅ If applicable | ✅ Required |
| Business rules | — | — | ✅ Required |
| Anomaly detection | — | Optional | ✅ Required |

### 6.2 SLA Standards

| Layer | Default Freshness SLA | Breach Action |
|---|---|---|
| Bronze | Source SLA + 2 hours | PagerDuty alert |
| Silver | Source SLA + 4 hours | PagerDuty alert |
| Gold | Source SLA + 6 hours | PagerDuty alert + email to domain owner |

---

## 7. Documentation Standards

### 7.1 What Must Be Documented

| Artifact | Required | Location |
|---|---|---|
| Pipeline README | Yes — every pipeline | Git repo `/pipelines/{name}/README.md` |
| Data contract | Yes — every Gold object | Data catalog + Git `/contracts/` |
| ERD | Yes — every Gold domain | Data catalog + Git `/docs/erd/` |
| Column descriptions | Yes — every column | dbt YAML or catalog metadata |
| Config file | Yes — every pipeline | Git `/configs/{name}/{env}_config.yaml` |
| Runbook | Yes — every production pipeline | Confluence/Notion |
| Architecture decision record | Yes — major decisions | Git `/docs/adr/` |

### 7.2 Data Contract Template

```yaml
# data_contract.yaml
contract:
  id: "DC-2024-001"
  name: "finance.fact_revenue"
  version: "1.0.0"
  status: "active"           # draft | active | deprecated | retired
  effective_date: "2024-01-01"
  
producer:
  team: "Finance Data Engineering"
  contact: "finance-data@company.com"
  
consumer:
  teams:
    - "BI / Analytics"
    - "Finance Leadership"
  
sla:
  freshness: "daily by 06:00 UTC"
  availability: "99.5%"
  
schema:
  - name: revenue_key
    type: VARCHAR(64)
    nullable: false
    pii: false
    description: "Surrogate key; SHA-256 of transaction_id + source_system"
  - name: gross_revenue
    type: DECIMAL(18,2)
    nullable: false
    pii: false
    description: "Pre-discount, pre-tax revenue in USD"
    
quality_expectations:
  - "No null revenue_key values"
  - "gross_revenue >= 0 for all non-void transactions"
  - "Row count variance < 25% vs prior day"
  
change_notification:
  breaking_changes: "14 days notice to all consumers"
  additive_changes: "3 days notice to all consumers"
```

---

## 8. Version Control Standards

### 8.1 Repository Structure

```
data-engineering/
├── infrastructure/        # Terraform IaC
│   ├── modules/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── README.md
├── pipelines/             # Python pipeline code
│   ├── {pipeline_name}/
│   │   ├── config/
│   │   │   ├── dev_config.yaml
│   │   │   ├── staging_config.yaml
│   │   │   └── prod_config.yaml
│   │   ├── src/
│   │   ├── tests/
│   │   └── README.md
├── dbt/                   # dbt project
│   ├── models/
│   ├── tests/
│   ├── macros/
│   └── dbt_project.yml
├── docs/
│   ├── erd/               # ERD files (Mermaid/dbdiagram)
│   ├── adr/               # Architecture decision records
│   └── contracts/         # Data contracts
└── .github/workflows/     # CI/CD
```

### 8.2 Branching Strategy

| Branch | Purpose | Protection |
|---|---|---|
| `main` | Production-deployed code | Protected; requires PR + 1 approval + CI pass |
| `staging` | Staging-deployed code | Protected; requires PR + CI pass |
| `feature/{ticket-id}-{description}` | Feature development | No protection |
| `hotfix/{ticket-id}-{description}` | Production hotfixes | Requires expedited approval |

### 8.3 Commit Standards

Follow **Conventional Commits** format:
```
{type}({scope}): {short description}

Types: feat | fix | docs | refactor | test | chore | ci
Scope: pipeline name, dbt model, infra component

Examples:
feat(finance-gl-pipeline): add incremental watermark-based loading
fix(dim-customer): resolve null customer_id for legacy source records
docs(erd): update finance domain ERD with new revenue tables
```

---

## 9. Cost Management Standards

### 9.1 Tagging Requirements

All cloud resources (Snowflake warehouses, Databricks clusters, S3/ADLS buckets, compute instances) must carry:

```
owner:          {team name}
environment:    dev | staging | prod
cost_center:    {finance cost center code}
project:        {project name}
managed_by:     terraform
domain:         {data domain}
```

**Untagged resources are terminated within 48 hours in non-production environments.**

### 9.2 Cost Guardrails

| Resource | Control | Limit |
|---|---|---|
| Snowflake warehouse | Resource monitor | Alert at 75%, suspend at 100% of monthly budget |
| Databricks cluster | Auto-terminate | All-purpose: ≤60 min idle. Never disabled. |
| Databricks jobs | Job cluster | Always. All-purpose clusters forbidden in prod. |
| Cloud storage | Lifecycle policies | Move to cold tier after 90 days; delete after retention period |
| Dev environments | Weekend auto-shutdown | All non-essential dev resources suspended Fri 11 PM – Mon 6 AM |

---

## 10. Exception Process

### 10.1 How to Request an Exception

1. Submit a written exception request to the Data Engineering Lead.
2. Include: standard being waived, business justification, risk assessment, compensating controls, duration of exception.
3. DE Lead + Data Governance Lead must both approve.
4. Exception logged in the Exception Register with expiry date.
5. Exception reviewed at next quarterly governance review.

### 10.2 Zero-Tolerance Standards (No Exceptions)

These standards have **no exception pathway**:

- Secrets in code or version control
- Manual object creation in production outside IaC
- PII data in non-production environments without masking
- Production pipelines running on all-purpose clusters
- Tables without data classification tags in Gold layer

---

*These standards are binding. Non-compliance is escalated to the Data Engineering Lead and, for repeated violations, to the Chief Data Officer. Standards reviewed annually or upon major platform changes.*
