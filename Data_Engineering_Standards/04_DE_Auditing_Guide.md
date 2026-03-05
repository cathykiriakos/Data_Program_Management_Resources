# Data Engineering Auditing Guide
## First & Second Line of Defense

**Document Owner:** Chief Data Office  
**Domain:** Data Engineering  
**Version:** 1.0  
**Classification:** Internal — Audit & Control

---

## Purpose

This guide defines how the organization audits its data engineering program. It establishes:

- **First Line of Defense (1LOD):** Controls owned and executed by the Data Engineering team itself.
- **Second Line of Defense (2LOD):** Independent oversight by Data Governance, Risk, or Compliance functions who verify that 1LOD controls are operating effectively.

The goal is not duplicative work — it is a **structured assurance model** where engineering teams self-attest and second-line functions provide independent verification.

---

## Table of Contents

1. [Control Framework Overview](#1-control-framework-overview)
2. [First Line of Defense — Self-Assessment Controls](#2-first-line-of-defense--self-assessment-controls)
3. [Second Line of Defense — Independent Audit Procedures](#3-second-line-of-defense--independent-audit-procedures)
4. [Automated Audit Queries](#4-automated-audit-queries)
5. [Audit Cadence & Reporting](#5-audit-cadence--reporting)
6. [Findings Classification & Escalation](#6-findings-classification--escalation)
7. [Evidence Requirements](#7-evidence-requirements)

---

## 1. Control Framework Overview

### 1.1 Three Lines Model

```
┌─────────────────────────────────────────────────────────────────┐
│  FIRST LINE: Data Engineering Team                              │
│  Owns and operates controls; self-attests monthly               │
│  Controls: Pipeline quality gates, IaC reviews, tagging,        │
│  metadata completeness, cost monitors, access reviews           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ attests to
┌──────────────────────────▼──────────────────────────────────────┐
│  SECOND LINE: Data Governance / Risk / Compliance               │
│  Independently verifies 1LOD controls are effective             │
│  Controls: Audit queries, access reviews, tag validation,       │
│  pipeline control testing, lineage verification                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ independent assurance to
┌──────────────────────────▼──────────────────────────────────────┐
│  THIRD LINE: Internal Audit / External Audit                    │
│  Periodic deep-dive audits (annual or regulatory-driven)        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Control Domains

| Control Domain | Key Risk | 1LOD Owner | 2LOD Verifier |
|---|---|---|---|
| Access & Authentication | Unauthorized data access | DE Lead | Data Governance |
| IaC Compliance | Manual object creation drift | Senior DE | Data Governance / IT Audit |
| Pipeline Quality | Data quality failures reaching consumers | DE Team | Data Governance |
| Metadata & Tagging | Ungoverned, undiscoverable data | Analytics Engineer | Data Governance |
| PII & Data Privacy | PII exposure in wrong environments | DE Team | Privacy / Compliance |
| Cost Controls | Budget overruns | Platform Engineer | Finance / IT |
| Lineage & Provenance | Inability to trace data origin | DE Team | Data Governance |
| Change Management | Unapproved changes in production | DE Lead | IT Audit |

---

## 2. First Line of Defense — Self-Assessment Controls

The DE team executes these controls and maintains evidence. Self-attestation is submitted monthly to the Data Governance function.

### Control DE-01: IaC Drift Detection

**Control Objective:** Ensure all production objects are managed by Terraform. No manual changes.

**Frequency:** Nightly (automated) + Monthly attestation

**Procedure:**
1. Run `terraform plan` against production state nightly.
2. Any drift (resources created/modified outside IaC) triggers a P2 alert.
3. Monthly: DE Lead reviews drift log; attests zero unresolved drift items.

**Evidence:** Terraform drift report; alert log with resolution timestamps.

---

### Control DE-02: Pipeline Quality Gate Pass Rate

**Control Objective:** All production pipelines pass defined quality gates before promotion.

**Frequency:** Per deployment + Monthly summary

**Procedure:**
1. CI/CD pipeline enforces quality gates (code review, tests, metadata).
2. Any gate failure blocks deployment.
3. Monthly: Report on gate pass/fail rates; investigate and resolve failures.

**Self-Assessment Checklist (Monthly):**
```
□ All deployments this month passed Gate 1 (Code Review)
□ All deployments this month passed Gate 2 (Test Coverage)
□ All deployments this month passed Gate 3 (Metadata Completeness)
□ All deployments this month passed Gate 4 (Change Management)
□ Zero exceptions granted without documentation
□ Exception register up to date
```

**Evidence:** CI/CD pipeline run logs; PR merge history; exception register.

---

### Control DE-03: Metadata Completeness

**Control Objective:** Every table and column in Silver and Gold has required metadata.

**Frequency:** Weekly scan + Monthly attestation

**Procedure:**
Run the following scan weekly; remediate gaps within 5 business days:

```python
# metadata_completeness_scan.py
import snowflake.connector
from config import get_secret

def scan_metadata_completeness(env: str, layers: list[str] = ["SILVER", "GOLD"]) -> list[dict]:
    """
    Scan for tables/columns missing required metadata.
    Returns list of findings.
    """
    conn = snowflake.connector.connect(**get_secret(f"{env}/snowflake/audit_account"))
    findings = []
    
    for layer in layers:
        # Check for tables missing descriptions or tags
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT
                table_catalog,
                table_schema,
                table_name,
                CASE WHEN comment IS NULL OR comment = '' THEN 'MISSING_DESCRIPTION' END AS issue
            FROM {env}_information_schema.tables
            WHERE table_schema NOT IN ('INFORMATION_SCHEMA')
              AND (comment IS NULL OR comment = '')
            ORDER BY table_catalog, table_schema, table_name
        """)
        for row in cursor.fetchall():
            findings.append({
                "control": "DE-03",
                "layer": layer,
                "object": f"{row[0]}.{row[1]}.{row[2]}",
                "issue": row[3],
                "severity": "MEDIUM"
            })
    
    conn.close()
    return findings
```

**Evidence:** Weekly scan output; gap closure tickets; monthly summary report.

---

### Control DE-04: Secrets Scan

**Control Objective:** No credentials, connection strings, or tokens in version control.

**Frequency:** Every commit (automated) + Monthly audit of scan logs

**Procedure:**
1. `gitleaks` or `trufflehog` pre-commit hook scans every commit.
2. CI/CD pipeline re-scans on every PR.
3. Monthly: Review scan logs; confirm zero confirmed secrets found.

**Evidence:** CI/CD secret scan logs; pre-commit hook configuration.

---

### Control DE-05: Service Account Access Review

**Control Objective:** All service accounts have current, least-privilege access.

**Frequency:** Quarterly

**Procedure:**
1. Export all service accounts and their roles.
2. Confirm each account is actively used (check last authentication date).
3. Remove or disable accounts inactive for >90 days.
4. Confirm roles match the documented minimum privilege for each account.

**Evidence:** Access review report; deprovisioned account log; role-to-account mapping.

---

### Control DE-06: Data Quality Gate Pass Rate

**Control Objective:** Data quality checks pass for ≥98% of pipeline runs.

**Frequency:** Daily (automated dashboard) + Monthly attestation

**Procedure:**
1. Quality check results logged to observability table after every run.
2. Daily dashboard shows pass/fail rate by pipeline.
3. Any quality failure triggers investigation within 4 business hours.
4. Monthly: Attest quality pass rate ≥98%; document root causes for failures.

**Evidence:** Quality check run log; incident tickets for failures; monthly pass rate report.

---

### Control DE-07: Cost Monitor Adherence

**Control Objective:** No warehouse or cluster exceeds budget without alert.

**Frequency:** Daily (automated alerts) + Monthly review

**Procedure:**
1. Resource monitors configured in Snowflake; auto-suspend at 100% monthly budget.
2. Databricks budget alerts configured at 75% and 100%.
3. Monthly: Review actual vs. budget; identify optimization opportunities.

**Evidence:** Resource monitor configuration; cost report; alert log.

---

## 3. Second Line of Defense — Independent Audit Procedures

The 2LOD function (Data Governance / Risk / Compliance) independently verifies that 1LOD controls are operating effectively. These procedures are executed **without relying solely on DE team attestations**.

### Audit AU-01: Unauthorized Object Detection (IaC Compliance)

**Objective:** Independently confirm no objects were created outside IaC.

**Frequency:** Monthly

**Procedure:**

```sql
-- Snowflake: Find objects created outside of the Terraform service account
-- (adjust service account name to match your environment)

SELECT
    table_catalog,
    table_schema,
    table_name,
    table_type,
    created,
    last_altered,
    table_owner
FROM snowflake.account_usage.tables
WHERE created >= DATEADD('month', -1, CURRENT_TIMESTAMP())
  AND table_owner != 'TERRAFORM_ROLE'      -- expected IaC service account role
  AND table_schema != 'INFORMATION_SCHEMA'
  AND deleted IS NULL
ORDER BY created DESC;
```

```sql
-- Also check warehouses created outside IaC
SELECT
    name,
    created_on,
    owner,
    type,
    size,
    auto_suspend,
    comment
FROM snowflake.account_usage.warehouses
WHERE created_on >= DATEADD('month', -1, CURRENT_TIMESTAMP())
  AND owner != 'TERRAFORM_ROLE'
ORDER BY created_on DESC;
```

**Expected Result:** Zero rows (all objects created by Terraform service account).

**Finding if Rows Returned:** Escalate as HIGH finding; require DE Lead to document and remediate within 5 business days.

---

### Audit AU-02: PII Exposure Risk Assessment

**Objective:** Confirm PII fields are tagged and masked in all non-production environments.

**Frequency:** Monthly

**Procedure:**

```sql
-- Step 1: Find all columns tagged as PII
SELECT
    t.table_catalog,
    t.table_schema,
    t.table_name,
    c.column_name,
    tv.tag_value AS pii_type
FROM snowflake.account_usage.tag_references tv
JOIN snowflake.account_usage.tables t
    ON tv.object_name = t.table_name
    AND tv.object_database = t.table_catalog
JOIN snowflake.account_usage.columns c
    ON c.table_name = t.table_name
    AND c.column_name = tv.column_name
WHERE tv.tag_name = 'PII_TYPE'
  AND tv.tag_value != 'NONE'
  AND tv.domain = 'COLUMN';

-- Step 2: Confirm masking policies are applied to all PII columns
SELECT
    c.table_catalog,
    c.table_schema,
    c.table_name,
    c.column_name,
    pm.masking_policy_name
FROM snowflake.account_usage.columns c
LEFT JOIN snowflake.account_usage.policy_references pr
    ON pr.ref_entity_name = c.table_name
    AND pr.ref_entity_domain = 'TABLE'
LEFT JOIN snowflake.account_usage.masking_policies pm
    ON pm.policy_name = pr.policy_name
WHERE c.table_catalog LIKE 'PROD_%'  -- production only
  AND c.column_name IN (
      -- PII column names from Step 1
      SELECT column_name FROM (-- above query --)
  )
  AND pm.masking_policy_name IS NULL;  -- Missing masking policy = FINDING
```

**Expected Result:** Zero PII columns without masking policies in production.

---

### Audit AU-03: Access Entitlement Review

**Objective:** Confirm all users have appropriate access; no privilege creep; no orphaned accounts.

**Frequency:** Quarterly

**Procedure:**

```sql
-- Snowflake: Review all role grants to users
SELECT
    grantee_name AS username,
    role AS role_name,
    granted_on,
    granted_by,
    grant_option
FROM snowflake.account_usage.grants_to_users
WHERE deleted_on IS NULL
ORDER BY granted_on DESC;

-- Flag accounts not logged in for > 90 days
SELECT
    u.name AS username,
    u.login_name,
    u.email,
    u.last_success_login,
    u.disabled,
    DATEDIFF('day', u.last_success_login, CURRENT_DATE()) AS days_since_login
FROM snowflake.account_usage.users u
WHERE u.deleted_on IS NULL
  AND u.disabled = FALSE
  AND (
      u.last_success_login IS NULL
      OR DATEDIFF('day', u.last_success_login, CURRENT_DATE()) > 90
  )
ORDER BY days_since_login DESC NULLS FIRST;
```

**Expected Result:** No users inactive >90 days; all roles traceable to approved role hierarchy.

---

### Audit AU-04: Data Lineage Completeness

**Objective:** Confirm all Gold layer objects have registered lineage traceable to source systems.

**Frequency:** Quarterly

**Procedure:**

```sql
-- Snowflake: Find Gold tables without lineage records in access history
-- (lineage can also be verified via dbt docs or Unity Catalog lineage API)

SELECT
    t.table_catalog,
    t.table_schema,
    t.table_name
FROM snowflake.account_usage.tables t
LEFT JOIN (
    SELECT DISTINCT
        objects_modified:objectName::STRING AS table_name
    FROM snowflake.account_usage.access_history,
    LATERAL FLATTEN(input => objects_modified)
    WHERE query_start_time >= DATEADD('month', -3, CURRENT_TIMESTAMP())
) lineage_objects
    ON lineage_objects.table_name = t.table_name
WHERE t.table_catalog LIKE 'PROD_%GOLD%'
  AND lineage_objects.table_name IS NULL
  AND t.deleted IS NULL;
```

**Also verify in dbt:**
```bash
# Check dbt lineage graph completeness
dbt ls --select +tag:gold --output json | \
python3 -c "
import sys, json
models = [json.loads(l) for l in sys.stdin]
no_source = [m for m in models if not m.get('depends_on', {}).get('sources')]
print(f'Gold models without source lineage: {len(no_source)}')
for m in no_source:
    print(f'  - {m[\"unique_id\"]}')
"
```

---

### Audit AU-05: Pipeline Quality Control Effectiveness

**Objective:** Confirm data quality gates are actually catching defects; not just passing by default.

**Frequency:** Quarterly — walkthrough test

**Procedure (Walkthrough Test):**
1. Select 3 production pipelines at random.
2. Review the quality check definitions — are they meaningful? (e.g., not just `row_count > 0`)
3. Review the last 30 days of quality check run history.
4. Confirm at least one quality check has **failed and been remediated** (proving the control is active, not just green by chance).
5. If no failures in 30 days, inject a synthetic defect in staging and confirm the gate catches it.

**Evidence Required from 1LOD:**
- Quality check definitions for selected pipelines
- 30-day run history
- At least one documented remediation of a quality failure

---

### Audit AU-06: Change Management Compliance

**Objective:** Confirm all production changes went through the defined change management process.

**Frequency:** Quarterly — sample-based

**Procedure:**
1. Pull list of all production deployments from CI/CD system in the quarter.
2. Sample 10 deployments (or 25% for smaller volumes).
3. For each sampled deployment, verify:
   - PR was reviewed and approved by a non-author
   - CI/CD gates passed (test logs available)
   - For Minor/Major changes: change ticket exists and was approved before deployment
   - For Major changes: CAB approval documented
4. Report compliance rate.

**Expected Result:** 100% of sampled changes have complete evidence chain.

---

### Audit AU-07: Cost Control Verification

**Objective:** Confirm resource monitors are configured and no resources running unmonitored.

**Frequency:** Monthly

**Procedure:**

```sql
-- Snowflake: Find warehouses without resource monitors
SELECT
    w.name AS warehouse_name,
    w.size,
    w.created_on,
    w.owner,
    rm.name AS resource_monitor
FROM snowflake.account_usage.warehouses w
LEFT JOIN snowflake.account_usage.resource_monitors rm
    ON rm.name = w.resource_monitor
WHERE w.deleted_on IS NULL
  AND rm.name IS NULL     -- No resource monitor = FINDING
ORDER BY w.name;

-- Also confirm auto-suspend is set on all warehouses
SELECT
    name,
    size,
    auto_suspend,
    auto_resume
FROM snowflake.account_usage.warehouses
WHERE deleted_on IS NULL
  AND (auto_suspend IS NULL OR auto_suspend = 0)  -- FINDING: no auto-suspend
ORDER BY name;
```

---

## 4. Automated Audit Queries

### 4.1 Master Audit Dashboard Query (Snowflake)

```sql
-- Executive audit summary — run monthly
WITH table_metadata_check AS (
    SELECT
        'Metadata Completeness' AS control,
        COUNT_IF(comment IS NULL OR comment = '') AS failing_objects,
        COUNT(*) AS total_objects,
        ROUND(100.0 * COUNT_IF(comment IS NOT NULL AND comment != '') / COUNT(*), 1) AS pass_rate_pct
    FROM snowflake.account_usage.tables
    WHERE table_catalog LIKE 'PROD_%'
      AND deleted IS NULL
      AND table_schema != 'INFORMATION_SCHEMA'
),

warehouse_monitor_check AS (
    SELECT
        'Warehouse Monitor Coverage' AS control,
        COUNT_IF(resource_monitor IS NULL) AS failing_objects,
        COUNT(*) AS total_objects,
        ROUND(100.0 * COUNT_IF(resource_monitor IS NOT NULL) / COUNT(*), 1) AS pass_rate_pct
    FROM snowflake.account_usage.warehouses
    WHERE deleted_on IS NULL
),

inactive_user_check AS (
    SELECT
        'Active User Hygiene' AS control,
        COUNT_IF(DATEDIFF('day', last_success_login, CURRENT_DATE()) > 90
                 OR last_success_login IS NULL) AS failing_objects,
        COUNT(*) AS total_objects,
        ROUND(100.0 * COUNT_IF(
            DATEDIFF('day', last_success_login, CURRENT_DATE()) <= 90
            AND last_success_login IS NOT NULL
        ) / COUNT(*), 1) AS pass_rate_pct
    FROM snowflake.account_usage.users
    WHERE deleted_on IS NULL AND disabled = FALSE
)

SELECT * FROM table_metadata_check
UNION ALL
SELECT * FROM warehouse_monitor_check
UNION ALL
SELECT * FROM inactive_user_check
ORDER BY pass_rate_pct ASC;
```

---

## 5. Audit Cadence & Reporting

### 5.1 Audit Calendar

| Control / Audit | 1LOD Frequency | 2LOD Frequency | Report To |
|---|---|---|---|
| IaC Drift (DE-01 / AU-01) | Nightly automated | Monthly | DE Lead, Data Governance |
| Metadata Completeness (DE-03) | Weekly scan | Monthly | DE Lead, Data Governance |
| Secrets Scan (DE-04) | Every commit | Monthly log review | DE Lead, InfoSec |
| PII Exposure (AU-02) | Monthly | Monthly | Privacy Officer, CDO |
| Access Review (DE-05 / AU-03) | Quarterly | Quarterly | DE Lead, CDO, HR (for leavers) |
| Lineage Completeness (AU-04) | Monthly | Quarterly | Data Governance |
| Quality Effectiveness (AU-05) | Monthly | Quarterly | Data Governance |
| Change Management (AU-06) | Per deployment | Quarterly | IT Audit, DE Lead |
| Cost Controls (DE-07 / AU-07) | Daily alerts, monthly review | Monthly | Finance, CDO |

### 5.2 Monthly Audit Report Structure

```
1. Executive Summary (1 page)
   - Overall compliance score
   - Critical findings
   - Findings opened/closed vs. prior month

2. Control Attestations (1LOD)
   - Self-attestation sign-off table
   - Exceptions logged this month

3. Independent Verification (2LOD)
   - Audit procedures completed
   - Findings by severity
   - Prior period finding closure rate

4. Trending Metrics
   - Quality pass rate trend (12-month)
   - Metadata completeness trend
   - Inactive user trend
   - Cost vs. budget trend
```

---

## 6. Findings Classification & Escalation

### 6.1 Severity Ratings

| Severity | Definition | Remediation SLA |
|---|---|---|
| **CRITICAL** | Active data breach, PII exposed to unauthorized parties, credentials compromised | Immediate — within 4 hours |
| **HIGH** | Control failure creating material risk (e.g., unapproved production change, masking not applied, inactive privileged account) | 5 business days |
| **MEDIUM** | Control weakness that could lead to risk if unaddressed (e.g., missing metadata, no resource monitor) | 15 business days |
| **LOW** | Best practice gap with minimal immediate risk | 30 business days |
| **INFORMATIONAL** | Observation or improvement opportunity, no active risk | Next quarterly review |

### 6.2 Escalation Matrix

| Severity | Immediate Notification | Resolution Owner | Escalation if Overdue |
|---|---|---|---|
| CRITICAL | CDO + InfoSec + Privacy Officer | DE Lead + InfoSec | Board notification per incident policy |
| HIGH | CDO + DE Lead + Data Governance | DE Lead | CDO + Legal |
| MEDIUM | Data Governance + DE Lead | DE Team | CDO |
| LOW | DE Lead | DE Team | Data Governance |

---

## 7. Evidence Requirements

### 7.1 Evidence Standards

All audit evidence must:
- Be collected by an independent party (2LOD) or from system-generated logs (not manually prepared by 1LOD)
- Be timestamped and attributable to a specific run/query
- Be retained for **3 years** (or per regulatory requirement if longer)
- Be stored in a read-only audit evidence repository (not editable by the DE team)

### 7.2 Evidence Repository Structure

```
audit-evidence/
├── {YYYY}/
│   ├── {MM}/
│   │   ├── 1LOD_Attestations/
│   │   │   ├── DE-01_IaC_Drift_Report.csv
│   │   │   ├── DE-03_Metadata_Scan.csv
│   │   │   └── Self_Attestation_Sign_Off.pdf
│   │   ├── 2LOD_Audit_Results/
│   │   │   ├── AU-01_Unauthorized_Objects.csv
│   │   │   ├── AU-02_PII_Exposure.csv
│   │   │   └── Monthly_Audit_Report.pdf
│   │   └── Findings/
│   │       ├── FINDING-2024-001_[description].md
│   │       └── FINDING-2024-001_Remediation_Evidence.pdf
```

---

*This auditing guide is reviewed annually and updated following any material changes to the data engineering platform or control environment. Questions should be directed to the Data Governance function.*
