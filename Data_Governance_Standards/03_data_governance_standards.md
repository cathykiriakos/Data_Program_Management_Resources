# Data Governance Standards
> **Role:** Chief Data Officer | **Platform:** Snowflake / Databricks  
> **Version:** 1.0 | **Last Updated:** 2026-03

---

## 1. Purpose & Scope

These standards define the **mandatory rules and specifications** all data assets, pipelines, and consumers must conform to. Standards are enforced through automated controls where possible and audited on a defined cadence.

> **Authority:** These standards are approved by the Data Governance Council and are mandatory for all business units.

---

## 2. Naming Standards

### 2.1 Snowflake Object Naming

```
Pattern:  <ENV>_<DOMAIN>_<LAYER>_<OBJECT>
Example:  PROD_FINANCE_CURATED_REVENUE_SUMMARY

Environment:   DEV | QA | PROD
Domain:        FINANCE | MARKETING | OPS | HR | CUSTOMER | PRODUCT
Layer:         RAW | STAGED | CURATED | PUBLISHED
```

| Object Type | Convention | Example |
|---|---|---|
| Database | `{ENV}_{DOMAIN}` | `PROD_FINANCE` |
| Schema | `{LAYER}` | `CURATED` |
| Table | `{NOUN}_{NOUN}` (snake_case) | `REVENUE_SUMMARY` |
| View | `V_{TABLE_NAME}` | `V_REVENUE_SUMMARY` |
| Stage | `STG_{SOURCE}_{OBJECT}` | `STG_SALESFORCE_ACCOUNTS` |
| Tag | `{DOMAIN}_{TAG_NAME}` | `FINANCE_PII_FLAG` |
| Role | `{DOMAIN}_{ACCESS_LEVEL}` | `FINANCE_READ`, `FINANCE_WRITE` |

### 2.2 Databricks / Delta Lake Naming

```
Pattern:  <catalog>.<schema>.<table>
Example:  prod_finance.curated.revenue_summary
```

| Object | Convention | Example |
|---|---|---|
| Catalog | `{env}_{domain}` | `prod_finance` |
| Schema | `{layer}` | `curated` |
| Table | `snake_case noun` | `revenue_summary` |
| Volume | `{domain}_{source}_raw` | `finance_erp_raw` |

### 2.3 Column Naming

| Rule | Standard |
|---|---|
| Case | `snake_case` always |
| Primary Key | `{table_name}_id` (e.g., `customer_id`) |
| Foreign Key | `{referenced_table}_id` |
| Timestamps | `created_at`, `updated_at`, `deleted_at` |
| Boolean | `is_{condition}` or `has_{condition}` |
| Date | `{noun}_date` (e.g., `order_date`) |
| Amounts | `{noun}_amount` (e.g., `revenue_amount`) |

---

## 3. Data Classification Standards

### 3.1 Classification Tiers

| Tier | Tag Value | Definition | Examples |
|---|---|---|---|
| 1 | `PUBLIC` | Freely shareable | Published KPIs, public docs |
| 2 | `INTERNAL` | Internal use, no external sharing | Operational metrics, headcount |
| 3 | `CONFIDENTIAL` | Business-sensitive, need-to-know | Revenue, margins, strategy |
| 4 | `RESTRICTED` | Regulated data — highest controls | PII, PHI, PCI, financial account data |

### 3.2 Classification Rules

- Classification is applied at the **column level**
- Tables inherit the **highest classification** of any column they contain
- Classification must be **reviewed annually** or on material data change
- **Restricted** data requires a signed **Data Usage Agreement** for access

### 3.3 Snowflake Tag Implementation

```sql
-- Create classification tag
CREATE OR REPLACE TAG governance.classification_tier
  ALLOWED_VALUES 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED';

-- Apply to column
ALTER TABLE prod_finance.curated.customer
  MODIFY COLUMN ssn
  SET TAG governance.classification_tier = 'RESTRICTED';

-- Query tagged objects
SELECT * FROM TABLE(
  INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
    'PROD_FINANCE.CURATED.CUSTOMER', 'table'
  )
);
```

---

## 4. Data Quality Standards

### 4.1 DQ Rules Registry Format

All DQ rules must be defined in the central YAML registry:

```yaml
# dq_rules_registry.yaml
rules:
  - rule_id: "DQ-FINANCE-001"
    asset: "prod_finance.curated.revenue_summary"
    column: "revenue_amount"
    dimension: "completeness"
    check: "not_null"
    severity: "CRITICAL"
    owner: "finance_steward@company.com"
    sla_hours: 2

  - rule_id: "DQ-FINANCE-002"
    asset: "prod_finance.curated.revenue_summary"
    column: "revenue_amount"
    dimension: "validity"
    check: "greater_than_or_equal_to"
    threshold: 0
    severity: "HIGH"
    owner: "finance_steward@company.com"
    sla_hours: 4

  - rule_id: "DQ-CUSTOMER-001"
    asset: "prod_customer.curated.customers"
    column: "customer_id"
    dimension: "uniqueness"
    check: "unique"
    severity: "CRITICAL"
    owner: "customer_steward@company.com"
    sla_hours: 2
```

### 4.2 DQ Severity SLAs

| Severity | Definition | Notification | Resolution SLA |
|---|---|---|---|
| **CRITICAL** | Data unusable or compliance risk | Immediate PagerDuty + Steward | 2 hours |
| **HIGH** | Significant business impact | Email + Slack within 30 min | 4 hours |
| **MEDIUM** | Moderate impact, workaround exists | Email within 2 hours | 2 business days |
| **LOW** | Cosmetic or minor issue | Weekly digest | 5 business days |

### 4.3 DQ Gate Requirements

| Pipeline Layer | Required DQ Gates |
|---|---|
| Raw Ingestion | Schema validation, null check on primary keys |
| Staging | Format validation, referential integrity |
| Curated | All registered DQ rules must pass at CRITICAL/HIGH severity |
| Published (Consumer) | 100% DQ pass rate + steward sign-off |

---

## 5. Metadata Standards

### 5.1 Required Metadata Fields

Every governed data asset **must** have the following metadata populated in the catalog:

| Field | Required | Description |
|---|---|---|
| `asset_name` | ✅ | Display name |
| `business_description` | ✅ | Plain-language description |
| `domain` | ✅ | Owning business domain |
| `owner` | ✅ | Named individual owner |
| `steward` | ✅ | Named data steward |
| `classification` | ✅ | Classification tier |
| `dq_score` | ✅ | Current DQ pass rate |
| `lineage_documented` | ✅ | Boolean — lineage mapped |
| `sla` | ✅ for Tier 1 | Availability SLA in hours |
| `glossary_terms` | ✅ for key columns | Linked glossary terms |
| `last_reviewed` | ✅ | Date of last governance review |
| `retention_policy` | ✅ | Retention period and basis |

### 5.2 Business Glossary Standards

- Terms must be **approved by the owning domain steward** before publication
- Each term must have: definition, example, synonyms, domain, owner, status
- Terms in conflict between domains require **Data Governance Council arbitration**
- Deprecated terms must remain in catalog with `DEPRECATED` status for 12 months

---

## 6. Access Control Standards

### 6.1 Role Structure (Snowflake)

```
SYSADMIN (platform)
 └── {DOMAIN}_ADMIN        — full access within domain
      └── {DOMAIN}_WRITE   — write access to curated/published
           └── {DOMAIN}_READ — read access to published
                └── {DOMAIN}_RESTRICTED_READ — access to restricted data
```

### 6.2 Access Provisioning Standards

| Rule | Requirement |
|---|---|
| Access requests | Must go through ITSM (ServiceNow/Jira) with business justification |
| Restricted data access | Requires steward approval + signed DUA |
| Service account access | Must be non-personal, documented, with quarterly review |
| Temporary access | Max 90 days; must have expiry date set |
| Shared credentials | Prohibited — all access must be individual |
| Privileged access | MFA required; break-glass process for emergency |

### 6.3 Access Review Cycle

```
Quarterly Access Certification Process:
  1. DGO generates access report per domain (automated)
  2. Domain steward reviews access list
  3. Steward certifies or revokes within 10 business days
  4. Uncertified access is automatically suspended
  5. DGO reports certification completion rate to CDO
```

---

## 7. Lifecycle & Retention Standards

| Classification | Retention (Default) | Archival | Deletion Method |
|---|---|---|---|
| Public | 7 years | Year 3+ | Soft delete + purge |
| Internal | 5 years | Year 3+ | Soft delete + purge |
| Confidential | 7 years | Year 5+ | Secure delete |
| Restricted | Per regulation | As required | Crypto-shred or secure wipe |

### Snowflake Time Travel Configuration

```sql
-- Set time travel per classification
ALTER TABLE prod_finance.curated.revenue_summary
  SET DATA_RETENTION_TIME_IN_DAYS = 90;  -- Confidential: 90 days

-- Fail-safe window is fixed at 7 days (not configurable)
```

---

## 8. Pipeline & Engineering Standards

| Standard | Requirement |
|---|---|
| All transformations | Must be implemented in dbt or approved orchestration tool |
| Schema changes | Must go through change management (see Configuration Practices doc) |
| Breaking changes | Must have 30-day deprecation notice + downstream owner notification |
| New sensitive fields | Must trigger classification review before merge |
| Test coverage | Minimum: not_null + unique on PKs, accepted_values on categorical fields |
| Documentation | dbt model descriptions required on all `curated` and `published` models |

---

*Document Owner: Chief Data Officer | Approved by: Data Governance Council | Review Cycle: Semi-Annual*
