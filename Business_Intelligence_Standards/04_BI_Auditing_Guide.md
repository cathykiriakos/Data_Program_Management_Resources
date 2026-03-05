# Business Intelligence Auditing Guide
## First & Second Line of Defense

**Document Owner:** Chief Data Office  
**Domain:** Business Intelligence  
**Version:** 1.0  
**Classification:** Internal — Audit & Control

---

## Table of Contents

1. [Control Framework Overview](#1-control-framework-overview)
2. [First Line of Defense — Self-Assessment Controls](#2-first-line-of-defense--self-assessment-controls)
3. [Second Line of Defense — Independent Audit Procedures](#3-second-line-of-defense--independent-audit-procedures)
4. [Automated Audit Queries & Scripts](#4-automated-audit-queries--scripts)
5. [Audit Cadence & Reporting](#5-audit-cadence--reporting)
6. [Findings Classification & Escalation](#6-findings-classification--escalation)
7. [Evidence Requirements](#7-evidence-requirements)
8. [Regulatory Audit Readiness](#8-regulatory-audit-readiness)

---

## 1. Control Framework Overview

### 1.1 Three Lines Model for BI

```
┌─────────────────────────────────────────────────────────────────┐
│  FIRST LINE: BI COE + Domain BI Leads                          │
│  Own and operate controls; self-attest monthly                  │
│  Controls: Report certification, data source registry,          │
│  access review, brand compliance, content lifecycle,            │
│  performance monitoring, compute cost monitoring                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ attests to
┌──────────────────────────▼──────────────────────────────────────┐
│  SECOND LINE: Data Governance / Risk / Compliance               │
│  Independently verifies 1LOD controls are effective             │
│  Controls: Access sampling, data source validation,             │
│  PII exposure testing, report registry audit, cost audit,       │
│  regulatory compliance spot-checks                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ independent assurance to
┌──────────────────────────▼──────────────────────────────────────┐
│  THIRD LINE: Internal Audit / External Audit                    │
│  Periodic deep-dive audits (annual or regulatory-driven)        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Control Domains

| Domain | Key Risk | 1LOD Owner | 2LOD Verifier |
|---|---|---|---|
| Authentication & Access | Unauthorized data access via BI tools | BI Platform Eng. | Data Governance / IT Audit |
| Data Source Compliance | Unapproved connections bypassing governance | BI COE Lead | Data Governance |
| PII & Data Privacy | PII visible in BI tools to unauthorized users | Governance Analyst | Privacy Officer |
| Content Certification | Uncertified content treated as authoritative | BI COE Lead | Data Governance |
| Compute & Cost | Budget overruns from unmanaged BI workloads | BI Platform Eng. | Finance / IT |
| Content Lifecycle | Stale reports consuming resources; orphaned owners | Governance Analyst | Data Governance |
| Brand & Standards | Inconsistent, non-compliant report presentation | BI COE Lead | Data Governance |
| Regulatory Reporting | Inaccurate regulatory outputs from BI tools | Domain BI Lead | Compliance / Legal |

---

## 2. First Line of Defense — Self-Assessment Controls

### Control BI-01: Data Source Compliance Check

**Objective:** Confirm all production BI content connects only to approved data sources.

**Frequency:** Monthly

**Procedure:**

```python
# Power BI: Audit all dataset connections via REST API
import requests

def audit_powerbi_datasources(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    approved_registry: list[dict]
) -> list[dict]:
    """
    Retrieve all dataset connections and flag non-approved sources.
    """
    # Get access token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_resp = requests.post(token_url, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    })
    token = token_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    approved_sources = {r["name"] for r in approved_registry if r["status"] == "active"}
    findings = []

    # Get all workspaces
    workspaces = requests.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups?$top=200",
        headers=headers
    ).json().get("value", [])

    for ws in workspaces:
        datasets = requests.get(
            f"https://api.powerbi.com/v1.0/myorg/admin/groups/{ws['id']}/datasets",
            headers=headers
        ).json().get("value", [])
        
        for ds in datasets:
            # Check datasources for each dataset
            datasources = requests.get(
                f"https://api.powerbi.com/v1.0/myorg/admin/datasets/{ds['id']}/datasources",
                headers=headers
            ).json().get("value", [])
            
            for source in datasources:
                source_name = source.get("datasourceType", "Unknown")
                connection_details = source.get("connectionDetails", {})
                server = connection_details.get("server", "")
                database = connection_details.get("database", "")
                full_source = f"{server}/{database}"
                
                if full_source not in approved_sources and source_name not in ["AzureDataLake", "AnalysisServices"]:
                    findings.append({
                        "workspace": ws["name"],
                        "dataset": ds["name"],
                        "source_type": source_name,
                        "connection": full_source,
                        "severity": "HIGH"
                    })

    return findings
```

**Self-attestation:** BI COE Lead signs off that all flagged items have been reviewed and resolved.

---

### Control BI-02: Access Register Accuracy

**Objective:** Confirm all BI tool users are in the access register; no orphaned accounts.

**Frequency:** Monthly

**Procedure:**
1. Export active user list from all BI tools via admin API.
2. Cross-reference against HR active employee list.
3. Flag users in BI tools who are no longer in HR system (departed employees).
4. Suspend accounts within 24 hours of identification; remove within 5 business days.
5. Confirm manager has recertified all direct reports within the quarter.

**Self-Assessment Checklist:**
```
□ All BI tool users exported and cross-referenced against HR this month
□ Zero departed employees with active BI tool accounts
□ All accounts provisioned via IdP group (no direct tool provisioning)
□ Quarterly recertification completed (if quarter-end month)
□ Guest/external accounts reviewed; expired access revoked
□ Exception register updated
```

---

### Control BI-03: Report Registry Currency

**Objective:** Confirm the Report Registry reflects actual published content; no orphaned or unregistered reports.

**Frequency:** Monthly

**Procedure:**
1. Export all published reports from all BI tools via admin API.
2. Cross-reference against the Report Registry.
3. Flag reports in tools not found in the registry (non-compliant — no governance record).
4. Flag reports in the registry with no matching published content (stale registry entry).
5. Confirm every registered report has a valid, active owner.

**Evidence:** Diff report between tool export and registry; remediation actions.

---

### Control BI-04: Compute Cost vs. Budget

**Objective:** Confirm BI compute consumption is within approved budgets and monitored.

**Frequency:** Monthly

**Procedure (Snowflake — BI Warehouse):**

```sql
-- Monthly credit consumption for BI warehouse
SELECT
    warehouse_name,
    SUM(credits_used)                                   AS credits_used_mtd,
    SUM(credits_used_cloud_services)                    AS cloud_credits_mtd,
    SUM(credits_used) + SUM(credits_used_cloud_services) AS total_credits_mtd,
    ROUND((SUM(credits_used) / {monthly_budget}) * 100, 1) AS pct_of_budget
FROM snowflake.account_usage.warehouse_metering_history
WHERE warehouse_name LIKE 'BI_%'
  AND start_time >= DATE_TRUNC('month', CURRENT_DATE())
GROUP BY warehouse_name
ORDER BY total_credits_mtd DESC;
```

**Self-attestation:** BI Platform Engineer signs off on cost variance explanation if >10% over prior month or >75% of budget.

---

### Control BI-05: Stale Content Archival Execution

**Objective:** Confirm content not viewed in 90 days is being archived per policy.

**Frequency:** Monthly

**Procedure:**

```python
# Tableau: find and flag stale workbooks via REST API
import tableauserverclient as TSC
from datetime import datetime, timedelta, timezone

def get_stale_content(
    server: TSC.Server,
    days_threshold: int = 90
) -> dict:
    """Return workbooks and data sources not viewed in threshold days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
    stale = {"workbooks": [], "datasources": []}

    all_workbooks, _ = server.workbooks.get()
    for wb in all_workbooks:
        if wb.updated_at and wb.updated_at < cutoff:
            stale["workbooks"].append({
                "name": wb.name,
                "project": wb.project_name,
                "owner_id": wb.owner_id,
                "last_updated": wb.updated_at.isoformat(),
                "days_stale": (datetime.now(timezone.utc) - wb.updated_at).days
            })

    all_ds, _ = server.datasources.get()
    for ds in all_ds:
        if ds.updated_at and ds.updated_at < cutoff:
            stale["datasources"].append({
                "name": ds.name,
                "project": ds.project_name,
                "owner_id": ds.owner_id,
                "last_updated": ds.updated_at.isoformat(),
                "days_stale": (datetime.now(timezone.utc) - ds.updated_at).days
            })

    return stale
```

---

### Control BI-06: Brand Compliance Spot-Check

**Objective:** Confirm T1 and T2 reports comply with branding standards.

**Frequency:** Monthly (sample of 10% of T1/T2 reports)

**Procedure:**
1. Randomly select 10% of T1/T2 reports from the Report Registry.
2. For each, confirm:
   - Brand template applied (fonts, colors from approved palette)
   - Classification label present on every page
   - "Last Refreshed" timestamp visible
   - Owner contact in footer
3. Document violations; require remediation within 5 business days.

---

## 3. Second Line of Defense — Independent Audit Procedures

### Audit BI-AU-01: Unauthorized Data Source Detection

**Objective:** Independently confirm no BI content connects to unapproved data sources — without relying on the BI COE's own audit.

**Frequency:** Quarterly

**Procedure (Power BI — Admin API):**

```python
# Independent 2LOD audit — run by Data Governance team, not BI COE
# Uses a separate service principal with read-only admin API access

def independent_datasource_audit(
    token: str,
    approved_sources_file: str
) -> list[dict]:
    """
    Independently enumerate all Power BI dataset connections.
    Compare against the approved registry from a controlled copy.
    """
    import json
    import requests

    with open(approved_sources_file) as f:
        approved = {s["connection_string"] for s in json.load(f) if s["status"] == "active"}

    headers = {"Authorization": f"Bearer {token}"}
    findings = []

    # Use admin-level API (separate from BI COE service principal)
    datasets_resp = requests.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets?$top=1000",
        headers=headers
    )
    
    for ds in datasets_resp.json().get("value", []):
        sources_resp = requests.get(
            f"https://api.powerbi.com/v1.0/myorg/admin/datasets/{ds['id']}/datasources",
            headers=headers
        )
        for src in sources_resp.json().get("value", []):
            conn = src.get("connectionDetails", {})
            conn_str = f"{conn.get('server','')}/{conn.get('database','')}"
            if conn_str and conn_str not in approved:
                findings.append({
                    "audit": "BI-AU-01",
                    "dataset_id": ds["id"],
                    "dataset_name": ds.get("name"),
                    "workspace_id": ds.get("workspaceId"),
                    "source_type": src.get("datasourceType"),
                    "connection": conn_str,
                    "severity": "HIGH",
                    "finding": "Connection not in approved registry"
                })

    return findings
```

**Expected result:** Zero findings (all connections in approved registry).

---

### Audit BI-AU-02: PII Exposure Sampling

**Objective:** Independently verify PII is not visible in reports accessible to general audiences.

**Frequency:** Quarterly

**Procedure:**
1. Identify all certified datasets tagged with `pii_contains: true` in the Approved Data Source Registry.
2. For each, identify the connected T1/T2 reports.
3. Access each report using a test account with standard (non-restricted) access.
4. Systematically check every column visible in the report against the list of known PII columns from the data catalog.
5. Document any PII visible to the standard test account.

**Also check:**
- Tooltip text (sometimes exposes underlying column values)
- Filter dropdowns (may expose PII values in filter selection)
- Export outputs (PDF, Excel) — verify masking applies to exports

**Expected result:** Zero PII visible to non-RESTRICTED test account.

**Finding if PII visible:** CRITICAL severity — immediate escalation to Privacy Officer.

---

### Audit BI-AU-03: Access Entitlement Independent Review

**Objective:** Independently verify no unauthorized access to BI tools or content.

**Frequency:** Quarterly

**Procedure:**
1. Independently export all BI tool user lists via admin API (separate service account from 1LOD).
2. Cross-reference against HR termination list for the quarter.
3. Cross-reference against access register for the quarter (confirming all accesses have an approval record).
4. Sample 20 random user-to-role assignments and verify each has an approval record in the ITSM system.
5. Identify any direct tool provisioning (not via IdP group) — policy violation.

**Verification queries:**

```python
# Compare BI tool users vs HR active employees
# Uses HR data from HRIS API and Power BI admin API
# Executed by Data Governance team independently

def compare_bi_users_to_hr(
    bi_users: list[dict],           # from BI admin API
    hr_active_employees: list[dict] # from HRIS
) -> dict:
    bi_emails = {u["email"].lower() for u in bi_users if u.get("email")}
    hr_emails = {e["work_email"].lower() for e in hr_active_employees}

    departed_with_access = bi_emails - hr_emails
    
    return {
        "total_bi_users": len(bi_emails),
        "total_hr_active": len(hr_emails),
        "departed_with_bi_access": list(departed_with_access),
        "count_departed_with_access": len(departed_with_access),
        "severity": "CRITICAL" if departed_with_access else "PASS"
    }
```

---

### Audit BI-AU-04: Regulatory Report Accuracy Spot-Check

**Objective:** For regulated industries — independently verify that T1 certified reports used for regulatory reporting produce accurate outputs.

**Frequency:** Quarterly (or before each regulatory submission)

**Procedure:**
1. Identify all T1 reports used as input to regulatory submissions (tagged `regulatory_use: true` in the Report Registry).
2. For each, independently query the underlying Gold layer data using the same logic as the report.
3. Compare the report output to the independent query output.
4. Document any discrepancy — even rounding differences must be explained.

**Evidence:** Independent SQL query results, report screenshot, reconciliation documentation.

**Finding if discrepancy:** HIGH or CRITICAL (depending on materiality) — immediately involve Compliance and the domain owner.

---

### Audit BI-AU-05: Compute Cost Governance Verification

**Objective:** Independently confirm resource monitors are active on all BI warehouses and that no BI workloads are running on shared ELT compute.

**Frequency:** Monthly

**Procedure (Snowflake):**

```sql
-- Find BI-tagged warehouses without resource monitors
SELECT
    name AS warehouse_name,
    size,
    created_on,
    resource_monitor,
    auto_suspend,
    comment
FROM snowflake.account_usage.warehouses
WHERE deleted_on IS NULL
  AND (
      LOWER(name) LIKE '%bi%'
      OR LOWER(comment) LIKE '%business intelligence%'
      OR LOWER(name) LIKE '%tableau%'
      OR LOWER(name) LIKE '%powerbi%'
  )
  AND (resource_monitor IS NULL OR resource_monitor = '')    -- FINDING
ORDER BY name;

-- Find ELT warehouses being used by BI service accounts (co-mingled compute)
SELECT
    query_type,
    warehouse_name,
    user_name,
    COUNT(*) AS query_count,
    SUM(credits_used_cloud_services) AS credits_used
FROM snowflake.account_usage.query_history
WHERE warehouse_name LIKE 'TRANSFORM_%'   -- ELT warehouse
  AND user_name IN (                        -- BI service accounts
      'SVC_TABLEAU_PROD',
      'SVC_POWERBI_PROD',
      'SVC_ALTERYX_PROD'
  )
  AND start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY credits_used DESC;
```

---

### Audit BI-AU-06: Content Lifecycle Compliance

**Objective:** Confirm stale content is being archived per policy; no orphaned owners.

**Frequency:** Quarterly

**Procedure:**
1. Pull complete Report Registry.
2. For each registered report, verify:
   - The owner is still an active employee (HR cross-check)
   - The report is still published in the tool (not a ghost registry entry)
   - The report was viewed at least once in the past 90 days (from usage logs)
3. Identify reports that should have been archived but were not — policy failure.
4. Identify reports in the tool but not in the registry — compliance gap.

---

### Audit BI-AU-07: External Sharing Inspection

**Objective:** Confirm no content has been shared externally without approval.

**Frequency:** Monthly

**Procedure (Power BI):**

```python
# Identify any external guest users in Power BI via admin API
def find_external_users(token: str, approved_guests: list[str]) -> list[dict]:
    import requests
    
    headers = {"Authorization": f"Bearer {token}"}
    users = requests.get(
        "https://api.powerbi.com/v1.0/myorg/admin/users",
        headers=headers
    ).json().get("value", [])
    
    findings = []
    for user in users:
        email = user.get("emailAddress", "")
        is_external = "#EXT#" in user.get("identifier", "") or \
                      not email.endswith("@yourcompany.com")   # adjust domain
        if is_external and email.lower() not in [g.lower() for g in approved_guests]:
            findings.append({
                "audit": "BI-AU-07",
                "user": email,
                "display_name": user.get("displayName"),
                "user_type": user.get("userType"),
                "finding": "External user not in approved guest register",
                "severity": "HIGH"
            })
    return findings
```

---

## 4. Automated Audit Queries & Scripts

### 4.1 Monthly BI Audit Dashboard Query (Snowflake — BI Usage)

```sql
-- BI audit summary: query volume, top consumers, cost by service account
WITH bi_usage AS (
    SELECT
        user_name,
        warehouse_name,
        COUNT(*)                            AS query_count,
        SUM(execution_time) / 1000          AS total_exec_seconds,
        SUM(credits_used_cloud_services)    AS credits_consumed,
        AVG(rows_produced)                  AS avg_rows_returned,
        MAX(bytes_scanned) / 1e9            AS max_gb_scanned
    FROM snowflake.account_usage.query_history
    WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
      AND warehouse_name LIKE 'BI_%'
    GROUP BY user_name, warehouse_name
),

high_scan_queries AS (
    SELECT
        query_id,
        user_name,
        warehouse_name,
        query_text,
        bytes_scanned / 1e9 AS gb_scanned,
        execution_time / 1000 AS exec_seconds,
        start_time
    FROM snowflake.account_usage.query_history
    WHERE start_time >= DATEADD('month', -1, CURRENT_TIMESTAMP())
      AND warehouse_name LIKE 'BI_%'
      AND bytes_scanned > 10e9    -- > 10 GB scanned — flag for optimization
    ORDER BY bytes_scanned DESC
    LIMIT 20
)

SELECT 'BI Usage Summary' AS section, * FROM bi_usage
UNION ALL
SELECT 'High-Scan Queries', query_id, user_name, warehouse_name, NULL, NULL,
       gb_scanned, exec_seconds FROM high_scan_queries;
```

### 4.2 Tableau Server Admin Insights Queries

```python
# tableau_audit_runner.py
# Runs standard audit queries against Tableau Admin Insights

import tableauserverclient as TSC
from datetime import datetime, timedelta, timezone
import csv

def run_monthly_audit(server: TSC.Server, output_dir: str) -> None:
    """Execute and export monthly audit checks to CSV files."""

    # 1. All published workbooks with owner and last view date
    all_wbs, _ = server.workbooks.get()
    with open(f"{output_dir}/workbooks_audit.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "name", "project", "owner_id", "created_at", "updated_at",
            "size_bytes", "certified", "tags"
        ])
        writer.writeheader()
        for wb in all_wbs:
            writer.writerow({
                "name": wb.name,
                "project": wb.project_name,
                "owner_id": wb.owner_id,
                "created_at": wb.created_at,
                "updated_at": wb.updated_at,
                "size_bytes": wb.size,
                "certified": getattr(wb, "certified", False),
                "tags": "|".join(wb.tags) if wb.tags else ""
            })

    # 2. All data sources with certification status
    all_ds, _ = server.datasources.get()
    uncertified = [
        {"name": ds.name, "project": ds.project_name, "owner": ds.owner_id}
        for ds in all_ds
        if not getattr(ds, "certified", False)
        and ds.project_name not in ["T4-Sandbox", "T3-Self-Service"]
    ]
    
    with open(f"{output_dir}/uncertified_datasources.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "project", "owner"])
        writer.writeheader()
        writer.writerows(uncertified)

    print(f"Audit complete. {len(all_wbs)} workbooks, {len(uncertified)} uncertified data sources found.")
```

---

## 5. Audit Cadence & Reporting

### 5.1 Audit Calendar

| Control / Audit | 1LOD Frequency | 2LOD Frequency | Report To |
|---|---|---|---|
| Data source compliance (BI-01 / BI-AU-01) | Monthly | Quarterly | BI COE Lead, Data Governance |
| Access register accuracy (BI-02 / BI-AU-03) | Monthly | Quarterly | BI COE Lead, IT/InfoSec |
| Report Registry currency (BI-03) | Monthly | Quarterly | BI COE Lead, Data Governance |
| Compute cost vs. budget (BI-04 / BI-AU-05) | Monthly | Monthly | BI Platform Eng., Finance |
| Stale content archival (BI-05 / BI-AU-06) | Monthly | Quarterly | BI COE Lead |
| Brand compliance (BI-06) | Monthly | Quarterly | BI COE Lead |
| PII exposure sampling (BI-AU-02) | N/A (2LOD only) | Quarterly | Privacy Officer, CDO |
| Regulatory report accuracy (BI-AU-04) | N/A (2LOD only) | Quarterly | Compliance, CDO |
| External sharing (BI-AU-07) | Monthly | Monthly | BI COE Lead, Data Governance |

### 5.2 Monthly BI Governance Report Template

```
1. Executive Summary
   - Overall control health (green / amber / red per domain)
   - Critical and high findings opened this month
   - Findings resolved vs. prior month

2. Access & Identity
   - Total active users by tool
   - Provisioning actions (additions, removals)
   - Departed employees removed: count and time-to-remove
   - Guest/external users: count and expiry dates

3. Content Governance
   - Total published reports by tier (T1/T2/T3)
   - New certifications this month
   - Deprecations this month
   - Reports without valid owners (count and list)
   - Stale content archived (count)

4. Data Source Compliance
   - Total approved data sources in registry
   - Data source audit findings (count by severity)
   - Exception requests received and decisions

5. Compute & Cost
   - BI warehouse credit consumption vs. budget
   - Top 5 consumers (anonymized if sensitive)
   - Cost trend (12-month chart)
   - Optimization actions taken

6. Security & Compliance
   - PII audit results (if quarterly)
   - External sharing incidents: count
   - Classification labeling compliance rate
   - Data breach / incident count (BI-related): 0 expected

7. Findings Summary
   - Open findings by severity
   - Findings overdue for remediation
   - Findings opened / closed in period
```

---

## 6. Findings Classification & Escalation

| Severity | Definition | Remediation SLA | Escalation |
|---|---|---|---|
| **CRITICAL** | Active exposure: PII visible to unauthorized users; departed employee accessing data; external sharing of RESTRICTED content | Immediate — within 4 hours | BI COE Lead + Privacy Officer + CDO |
| **HIGH** | Unapproved data source connection; orphaned account; regulatory report discrepancy; no resource monitor | 5 business days | BI COE Lead + Data Governance Lead |
| **MEDIUM** | Report without owner; uncertified data source in T2 workspace; brand violation in T1; subscription to departed user | 15 business days | BI COE Lead |
| **LOW** | Report not in registry; minor performance violation; stale content not yet archived | 30 business days | Domain BI Lead |
| **INFORMATIONAL** | Optimization opportunity; process improvement suggestion | Next quarterly review | BI COE Lead |

---

## 7. Evidence Requirements

### 7.1 Evidence Standards

All 2LOD audit evidence must:
- Be collected by the Data Governance / Risk / Compliance team (not the BI COE)
- Come from system-generated logs or API outputs — not manually prepared reports
- Be timestamped with collection date and auditor identity
- Be retained for 3 years minimum (or per regulatory requirement)
- Be stored in a read-only, tamper-evident audit evidence repository

### 7.2 Evidence Repository

```
bi-audit-evidence/
├── {YYYY}/
│   ├── {MM}/
│   │   ├── 1LOD_Attestations/
│   │   │   ├── BI-01_DataSource_Audit.csv
│   │   │   ├── BI-02_Access_Register.csv
│   │   │   ├── BI-04_Cost_Report.pdf
│   │   │   └── Monthly_Self_Attestation_SignOff.pdf
│   │   ├── 2LOD_Audit_Results/
│   │   │   ├── BI-AU-01_Datasource_Findings.csv
│   │   │   ├── BI-AU-02_PII_Sampling_Results.pdf
│   │   │   ├── BI-AU-03_Access_Entitlement_Review.csv
│   │   │   └── Monthly_BI_Audit_Report.pdf
│   │   └── Findings/
│   │       ├── FINDING-BI-2024-001_[desc].md
│   │       └── FINDING-BI-2024-001_Remediation_Evidence.pdf
```

---

## 8. Regulatory Audit Readiness

### 8.1 Common Regulator Requests for BI Evidence

Regulators (SEC, OCC, FCA, HIPAA auditors, SOX auditors) frequently request:

| Request | Evidence Location | Preparation |
|---|---|---|
| "Show us who had access to [system] on [date]" | BI tool audit logs + SIEM | Ensure logs retained per requirement; SIEM search capability tested quarterly |
| "Demonstrate your controls over financial reporting data" | Report Registry + certification records + data lineage | T1 reports tagged `regulatory_use: true`; lineage from source to report documented |
| "Show us how you prevent unauthorized PII access" | RLS configurations + PII sampling audit results | Quarterly PII audit evidence retained; RLS test results documented |
| "Who approved changes to this report?" | Change management records + deployment pipeline logs | All T1 changes go through documented change process; evidence in ITSM |
| "Show me the data lineage for this regulatory figure" | dbt lineage + Snowflake access history + Report Registry | Lineage documentation linked from Report Registry |
| "Demonstrate data retention and disposal" | Data catalog retention metadata + lifecycle audit | Retention periods documented per table; disposal logs for archived content |

### 8.2 Pre-Audit Readiness Checklist

```
□ Report Registry is current and complete
□ All T1/T2 reports have a named, active owner
□ All T1/T2 reports tagged with correct classification and regulatory_use flag
□ Data lineage documented from source to all regulatory T1 reports
□ Last 4 quarters of access recertification records available
□ Last 4 quarters of monthly audit reports available
□ PII sampling audit results available for last 4 quarters
□ Change management records available for all T1 report changes in scope period
□ Audit logs available in SIEM for the full scope period
□ RLS configurations documented and last test results available
□ Resource monitor configurations documented
□ All findings from prior audits closed or on documented remediation plan
```

---

*This auditing guide is reviewed annually and updated following any material change to the BI platform, governance policy, or regulatory landscape. Questions should be directed to the Data Governance function.*
