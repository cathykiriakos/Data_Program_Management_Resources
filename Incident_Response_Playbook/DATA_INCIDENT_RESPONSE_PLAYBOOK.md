# Data Incident Response Playbook
## Cross-Domain | Snowflake · Databricks · Collibra · BI Tools · ML Platform

**Document Owner:** Chief Data Officer + Data Governance Office
**Classification:** Internal — Restricted Distribution
**Version:** 1.0 | **Last Updated:** 2026-03
**Review Cycle:** Semi-Annual or after any P1 incident

> **How to use this playbook:** Jump to Section 3 for the incident type that matches your situation. Sections 1–2 provide mandatory orientation before you begin response actions. Sections 4–7 cover escalation, evidence, post-incident procedures, and YAML-driven automation.

---

## Table of Contents

1. [Incident Classification Framework](#1-incident-classification-framework)
2. [Universal First Response — All Incidents](#2-universal-first-response--all-incidents)
3. [Incident Type Playbooks](#3-incident-type-playbooks)
   - [3.1 Data Quality Failure — Pipeline Blocked](#31-data-quality-failure--pipeline-blocked)
   - [3.2 PII / Sensitive Data Exposure](#32-pii--sensitive-data-exposure)
   - [3.3 Unauthorized Data Access](#33-unauthorized-data-access)
   - [3.4 Data Pipeline Outage / SLA Breach](#34-data-pipeline-outage--sla-breach)
   - [3.5 ML Model Failure / Degradation](#35-ml-model-failure--degradation)
   - [3.6 BI Report Producing Incorrect Data](#36-bi-report-producing-incorrect-data)
   - [3.7 Schema Change Breaking Downstream Consumers](#37-schema-change-breaking-downstream-consumers)
   - [3.8 Credentials / Secret Exposure](#38-credentials--secret-exposure)
4. [Escalation Matrix](#4-escalation-matrix)
5. [Evidence Preservation Guide](#5-evidence-preservation-guide)
6. [Post-Incident Process](#6-post-incident-process)
7. [Incident Automation — Python Pattern](#7-incident-automation--python-pattern)
8. [YAML Configuration — Incident Routing](#8-yaml-configuration--incident-routing)
9. [Regulatory Notification Reference](#9-regulatory-notification-reference)
10. [Incident Register Template](#10-incident-register-template)

---

## 1. Incident Classification Framework

### 1.1 Severity Levels

| Severity | Definition | Response SLA | Examples |
|---|---|---|---|
| **P1 — Critical** | Active exposure of regulated/restricted data; total platform outage; T1 ML model down; regulatory notification obligation triggered | Acknowledge: 15 min · Contain: 1 hr · Resolve: 4 hr | PII visible to unauthorized users, credentials in Git and active, T1 model serving degraded predictions, Snowflake account-wide outage |
| **P2 — High** | Significant control failure with material downstream impact; no confirmed external exposure | Acknowledge: 30 min · Contain: 4 hr · Resolve: 8 hr | DQ gate failure blocking Gold for >1 hr, masking policy not applied to confidential column, unauthorized active access to restricted schema |
| **P3 — Medium** | Localized failure or control gap with limited impact; no regulatory exposure | Acknowledge: 2 hr · Contain: 8 hr · Resolve: 2 business days | Single pipeline SLA breach (<4 hr), T2 BI report refreshing stale data, T2 ML model drift not yet causing decision errors |
| **P4 — Low** | Minor issue, no data exposure, no downstream consumer impact | Acknowledge: 1 business day · Resolve: 5 business days | Metadata missing on new Bronze table, orphaned BI report without owner, unused service account not yet removed |

### 1.2 Incident Type Taxonomy

| Code | Incident Type | Primary Domain | Regulatory Risk |
|---|---|---|---|
| `INC-DQ` | Data Quality Failure | Data Engineering / Governance | Medium — depends on asset classification |
| `INC-PII` | PII / Sensitive Data Exposure | Cross-domain | **High** — regulatory clock may start |
| `INC-ACC` | Unauthorized Data Access | Cross-domain | **High** — regulatory notification may apply |
| `INC-OUT` | Pipeline / Platform Outage / SLA Breach | Data Engineering | Low–Medium |
| `INC-ML` | ML Model Failure or Degradation | Machine Learning | Medium–High for T1 models |
| `INC-BI` | BI Report Incorrect Data | Business Intelligence | Medium–High for regulatory reports |
| `INC-SCH` | Schema Change Breaking Downstream | Data Engineering | Low–Medium |
| `INC-SEC` | Credentials / Secret Exposure | Cross-domain | **High** — treat as active breach until proven otherwise |

### 1.3 Classification Decision Tree

```
Is data actively visible to unauthorized parties?
  YES  →  P1 · INC-PII or INC-ACC · Go to Section 3.2 / 3.3
  NO   ↓

Are credentials/secrets confirmed or suspected exposed?
  YES  →  P1 · INC-SEC · Go to Section 3.8
  NO   ↓

Is a critical pipeline blocked / Gold data not refreshing?
  YES  →  Is it blocking regulated reporting or T1 BI dashboards?
    YES  →  P2 · INC-DQ or INC-OUT · Go to Section 3.1 / 3.4
    NO   →  P3 · INC-DQ or INC-OUT
  NO   ↓

Is a T1 ML model producing incorrect or degraded predictions?
  YES  →  P1/P2 · INC-ML · Go to Section 3.5
  NO   ↓

Is a T1 BI report showing incorrect data?
  YES  →  Is it a regulatory report?
    YES  →  P2 · INC-BI · Go to Section 3.6
    NO   →  P3 · INC-BI
  NO   →  Classify as P3 or P4 using judgment
```

---

## 2. Universal First Response — All Incidents

**These five steps apply to every incident regardless of type or severity. Do them in order before consulting the type-specific playbook.**

### Step 1 — Open an Incident Record (< 5 minutes)

Open a ticket in ITSM (ServiceNow / Jira) immediately. Do not wait until you understand the full scope.

```yaml
# Minimum fields to populate at incident open
incident_id:         "INC-[YYYY]-[TYPE]-[####]"
opened_at:           "[timestamp UTC]"
opened_by:           "[your name]"
severity:            "P1 / P2 / P3 / P4"
incident_type:       "INC-DQ / INC-PII / INC-ACC / INC-OUT / INC-ML / INC-BI / INC-SCH / INC-SEC"
initial_description: "[What you know right now — incomplete is fine]"
affected_asset:      "[Table / Pipeline / Report / Model name if known]"
data_classification: "Restricted / Confidential / Internal / Public / Unknown"
detection_source:    "Alert / User report / Audit / Monitoring"
```

### Step 2 — Notify the Incident Commander (< 10 minutes)

| Severity | Incident Commander | Notification Method |
|---|---|---|
| P1 | CDO | Phone + Slack + email |
| P2 | Data Governance Lead | Slack + email |
| P3 | Domain Lead (DE / BI COE / ML Lead) | Slack |
| P4 | Domain Lead | Slack |

The Incident Commander owns all decisions from this point forward.

### Step 3 — Preserve Evidence Before Any Remediation Action

> **Critical:** Do not delete logs, modify tables, rotate credentials, revoke access, or take any remediation action before confirming that all relevant evidence has been captured and stored in the incident evidence folder.

```
Evidence to capture immediately:
  □ Screenshot or export of alert / error that triggered detection
  □ Query history export (Snowflake: QUERY_HISTORY; Databricks: audit logs)
  □ Access log extract for affected asset (time range: T-24hr to now)
  □ Platform-level audit logs (Snowflake ACCOUNT_USAGE, Databricks audit logs)
  □ Pipeline run log for affected job
  □ Collibra DQ dashboard snapshot (if DQ-related)
  □ BI report export / screenshot (if BI-related)
  □ MLflow run and model version details (if ML-related)
```

See Section 5 for detailed evidence collection queries.

### Step 4 — Contain First, Investigate Second

Containment stops the bleeding. Investigation explains why it happened.

| Containment Action | When to Use |
|---|---|
| Suspend pipeline / job | DQ failure, schema issue, pipeline producing bad data |
| Revoke access / disable account | Unauthorized access, exposed credentials |
| Take BI report offline | PII exposure via BI, incorrect regulatory data |
| Redirect serving to fallback model | T1 ML model failure |
| Rotate credentials / API keys | Any confirmed or suspected credential exposure |

### Step 5 — Communicate Status

**P1:** CDO sends initial communication to stakeholders within 30 minutes of incident open. Update every hour until contained.

**P2:** Domain Lead sends initial communication within 2 hours. Update every 4 hours.

**P3/P4:** Internal Slack update only; no formal stakeholder communication unless business impact is confirmed.

```
# Incident Status Communication Template

[P1] 🚨 / [P2] ⚠️  DATA INCIDENT — INC-YYYY-TYPE-####

Status:              OPEN | INVESTIGATING | CONTAINED | RESOLVED
Opened:              [timestamp UTC]
Type:                [INC-DQ / INC-PII / etc.]
Affected:            [asset or system name]
Impact:              [what is broken or at risk — plain language]
Classification:      [Restricted / Confidential / etc.]
Containment Status:  [Not yet contained / Contained at HH:MM UTC]
Next Update:         [time]
Incident Commander:  [name]
```

---

## 3. Incident Type Playbooks

---

### 3.1 Data Quality Failure — Pipeline Blocked

**Incident Type:** `INC-DQ` | **Typical Severity:** P2–P3

**Description:** A DQ gate in a data pipeline has failed, blocking promotion to Silver or Gold. Data consumers may be receiving stale data or no refresh.

#### Detection Sources
- Airflow / Databricks Workflows task failure alert
- DQ results table: CRITICAL failures exceeding 2-hour SLA
- Collibra DQ dashboard alert
- SLA monitoring: Gold object freshness exceeded

#### Containment Steps

```
□ Confirm which layer is blocked (Bronze / Silver / Gold)
□ Identify downstream consumers of the blocked object:
    - BI reports: Query Report Registry for affected certified datasets
    - ML features: Query feature store dependency map
    - Other pipelines: Review dbt lineage or Airflow DAG dependencies
□ Notify downstream consumer leads of the data freeze
□ If the blocked table has a last-known-good snapshot, assess whether to serve it
    → Only serve snapshot with explicit CDO or Domain Lead approval
    → Annotate snapshot data: "INCIDENT FREEZE DATA — [INC-ID]"
□ If blocking a regulatory report: escalate immediately to P1/P2
```

#### Investigation Query

```python
# Run in Snowflake to identify failing DQ rules and trend
def investigate_dq_incident(conn, pipeline_name: str, run_date: str) -> dict:
    cursor = conn.cursor()

    # Current failures
    cursor.execute("""
        SELECT
            test_name, table_name, column_name, severity,
            failing_count, total_count,
            ROUND(failing_count * 100.0 / NULLIF(total_count, 0), 2) AS fail_pct,
            message, run_at
        FROM data_quality.pipeline_test_results
        WHERE suite_name = %(pipeline)s
          AND run_date   = %(run_date)s
          AND passed     = FALSE
        ORDER BY
            CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2
                          WHEN 'MEDIUM' THEN 3 ELSE 4 END,
            failing_count DESC
    """, {"pipeline": pipeline_name, "run_date": run_date})
    failures = cursor.fetchall()

    # 14-day recurrence trend
    cursor.execute("""
        SELECT run_date,
               SUM(CASE WHEN NOT passed AND severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_fails
        FROM data_quality.pipeline_test_results
        WHERE suite_name = %(pipeline)s
          AND run_date  >= %(run_date)s::DATE - 14
        GROUP BY 1 ORDER BY 1 DESC
    """, {"pipeline": pipeline_name, "run_date": run_date})
    trend = cursor.fetchall()

    return {
        "current_failures": failures,
        "14_day_trend": trend,
        "is_recurring": any(row[1] > 0 for row in trend[1:])
    }
```

#### Resolution Checklist

```
□ Root cause identified (source system / transform logic / threshold misconfiguration)
□ Fix applied and validated in non-production environment
□ Pipeline re-run from failed step; DQ gates passing
□ Downstream consumers confirmed refreshed and accurate
□ If threshold misconfiguration: YAML config updated via PR, reviewed and merged
□ If source system issue: source team notified; SLA ticket raised
□ Post-incident review scheduled if P1 or recurring P2
```

---

### 3.2 PII / Sensitive Data Exposure

**Incident Type:** `INC-PII` | **Typical Severity:** P1

**Description:** Personally Identifiable Information (PII) or other Restricted/Confidential data has been accessed by, transmitted to, or made visible to unauthorized parties.

> ⚠️ **Regulatory Clock Warning:** Depending on jurisdiction and data type, a regulatory notification obligation (e.g., GDPR 72-hour, HIPAA 60-day, CCPA 45-day) may begin the moment exposure is confirmed or reasonably suspected. Do not delay notification assessment. See Section 9.

#### Detection Sources
- Snowflake: PII-tagged column with no masking policy applied
- Collibra DQ / classification gap report
- User report: "I can see SSNs in this table"
- SIEM alert: unusual query pattern on Restricted tables
- BI audit log: export of Restricted content
- DE audit procedure AU-02 (monthly PII exposure scan)

#### Immediate Containment (< 1 hour, P1)

```
□ DO NOT remediate before preserving evidence (see Section 5)
□ Identify the exposure vector:
    - Snowflake: missing masking policy on PII column?
    - Databricks: Unity Catalog column filter not applied?
    - BI tool: RLS not configured or bypassed?
    - Pipeline: PII copied to a non-restricted schema?
□ Revoke or restrict access to the affected asset immediately:
    SNOWFLAKE:  REVOKE SELECT ON TABLE <t> FROM ROLE <affected_role>;
    DATABRICKS: DENY SELECT ON TABLE <catalog>.<schema>.<table> TO <principal>;
    BI TOOL:    Take report / dataset offline immediately
□ Identify all users who accessed the data during the exposure window:
    SELECT query_id, user_name, query_text, start_time
    FROM snowflake.account_usage.query_history
    WHERE start_time >= '<exposure_start>'
      AND query_text ILIKE '%<affected_table>%'
    ORDER BY start_time;
□ Notify Privacy Officer within 1 hour of confirmed or suspected exposure
□ Notify CDO within 1 hour
□ Notify Legal / Compliance within 2 hours if Restricted data confirmed
□ Do not communicate externally until Legal has been consulted
```

#### Investigation Checklist

```
□ Determine classification tier of exposed data (Restricted / Confidential / Internal)
□ Identify the root cause:
    - Masking policy never applied?       → Onboarding process gap
    - Masking policy removed without approval? → Change management failure
    - Role granted above privilege level?  → RBAC failure
    - Data copied to less-restricted schema? → Pipeline design failure
□ Determine exposure window: when did the gap first exist?
□ Enumerate all queries / exports against the affected asset during the window
□ Determine whether data was exported, downloaded, or transmitted externally
□ Quantify affected data subjects (count of distinct individuals exposed)
□ Assess regulatory notification obligation (see Section 9)
```

#### Resolution Checklist

```
□ Masking policy re-applied and verified in Snowflake / Unity Catalog
□ RBAC roles reviewed and corrected
□ All unauthorized user access revoked and confirmed
□ Affected data subject count documented
□ Regulatory notification decision made (notify / no notify) with Legal sign-off
□ Root cause fix implemented, tested, and deployed
□ Full classification and DQ scan triggered for affected domain in Collibra
□ Post-incident review mandatory (all P1 PII incidents)
□ If regulatory notification required: see Section 9
```

---

### 3.3 Unauthorized Data Access

**Incident Type:** `INC-ACC` | **Typical Severity:** P1–P2

**Description:** A user, service account, or external party has accessed data they are not authorized to access — including departed employees with active accounts, privilege escalation, and external intrusion.

#### Detection Sources
- Quarterly access certification identifies over-provisioned or orphaned account
- SIEM alert: access to Restricted table from non-standard IP or time
- Snowflake ACCOUNT_USAGE: role grant not in approved role hierarchy
- HR notification: employee departure — account not deprovisioned
- User self-report: "I can see data I shouldn't be able to see"
- Databricks audit log: unauthorized access to restricted catalog

#### Containment Steps

```
□ Preserve evidence FIRST (see Section 5)
□ Identify the access vector:
    - Direct platform access (Snowflake / Databricks)
    - BI tool access
    - API / application layer
    - Service account
□ Disable or restrict the account immediately — preserve for forensics, do not delete:
    SNOWFLAKE:  ALTER USER <user> SET DISABLED = TRUE;
                REVOKE ROLE <role> FROM USER <user>;
    DATABRICKS: Revoke via admin console or Unity Catalog DENY
    BI TOOL:    Suspend user via admin API
□ If a service account: rotate credentials immediately (see Section 3.8)
□ Notify CDO and Privacy Officer (if Restricted data accessed): within 1 hour
□ Notify InfoSec / CISO: within 1 hour for any confirmed unauthorized access
```

#### Investigation Queries

```sql
-- Full query history for unauthorized user during investigation window
SELECT
    q.query_id, q.user_name, q.role_name, q.query_type,
    q.query_text, q.database_name, q.schema_name,
    q.start_time, q.rows_produced, q.bytes_scanned
FROM snowflake.account_usage.query_history q
WHERE q.user_name   = '<unauthorized_user>'
  AND q.start_time >= '<investigation_start_utc>'
ORDER BY q.start_time;

-- All distinct objects accessed (for scope assessment)
SELECT DISTINCT direct_objects_accessed
FROM snowflake.account_usage.access_history
WHERE user_name       = '<unauthorized_user>'
  AND query_start_time >= '<investigation_start_utc>';

-- Role grant history for the user
SELECT created_on, deleted_on, grantee_name, role AS role_name, granted_by
FROM snowflake.account_usage.grants_to_users
WHERE grantee_name = '<unauthorized_user>'
ORDER BY created_on DESC;
```

#### Resolution Checklist

```
□ Unauthorized access confirmed revoked across all pathways (not just the one detected)
□ Root cause corrected: RBAC / provisioning / HR deprovision process fix
□ RBAC audit run for the affected role to confirm no other over-provisioned users
□ Access certification cycle triggered for affected domain
□ Regulatory notification decision made with Legal sign-off
□ Forensic evidence package prepared and archived (see Section 5)
□ Post-incident review mandatory (P1 / P2)
```

---

### 3.4 Data Pipeline Outage / SLA Breach

**Incident Type:** `INC-OUT` | **Typical Severity:** P2–P3

**Description:** A data pipeline has failed to complete within its defined SLA, causing downstream consumers to receive stale or absent data.

#### Detection Sources
- Airflow / Databricks Workflows: task in FAILED state
- SLA monitoring alert: pipeline not completed by scheduled delivery time
- Consumer report: "Dashboard is showing yesterday's data"
- Dead Letter Queue aging alert: records stuck > 48 hours
- Snowflake resource monitor: warehouse suspended due to credit exhaustion

#### Containment Steps

```
□ Identify the scope: which pipeline(s) and which downstream consumers are affected
□ Confirm last successful run timestamp
□ Assess downstream impact severity:
    - T1 BI reports affected?          → Notify BI COE Lead
    - ML feature pipelines affected?   → Notify ML Lead
    - Regulatory reports using this?   → Escalate to P1/P2
□ Determine data freeze posture:
    - Can consumers safely use last-known-good data?
    - Is stale data misleading enough to cause bad decisions?
    → If misleading: take downstream reports offline until resolved
□ Attempt restart from last successful checkpoint
□ If Snowflake warehouse suspended: increase resource monitor or use fallback warehouse
□ Notify consumer leads with an ETA within 1 hour of incident open
```

#### Investigation Query

```sql
SELECT
    run_id, task_name, state, error_code, error_message,
    scheduled_time, completed_time,
    DATEDIFF('minute', scheduled_time, CURRENT_TIMESTAMP()) AS minutes_overdue
FROM data_engineering.pipelines.run_log
WHERE pipeline_name = '<pipeline_name>'
  AND run_date >= CURRENT_DATE() - 3
ORDER BY scheduled_time DESC
LIMIT 20;
```

#### Resolution Checklist

```
□ Root cause identified (infrastructure / logic / source system / resource limits)
□ Fix applied; pipeline restarted from correct checkpoint
□ Data validated as current and accurate end-to-end
□ Downstream consumers confirmed refreshed and using current data
□ SLA breach duration logged in incident register
□ If recurring (same pipeline ≥ 2 failures in 30 days): root cause analysis required
□ Resource monitor limits reviewed if credit exhaustion was a factor
□ Dead Letter Queue cleared; records reviewed for data integrity
```

---

### 3.5 ML Model Failure / Degradation

**Incident Type:** `INC-ML` | **Typical Severity:** P1 (T1) · P2 (T2)

**Description:** A production ML model is producing incorrect, degraded, or unavailable predictions. Any confirmed T1 performance degradation is P1.

#### Detection Sources
- MLflow / monitoring store: feature drift alarm above threshold
- Serving endpoint health check: error rate > 1% or latency > SLA
- Prediction volume anomaly: volume > 2σ from baseline
- Outcome feedback pipeline: accuracy vs. actuals below performance gate
- Business stakeholder report: "The fraud model is missing obvious cases"

#### Containment Steps by Tier

**T1 Model (Regulated / High-Risk):**
```
□ Notify CDO, ML Lead, and Model Risk within 15 minutes of confirmed P1
□ Assess immediately whether serving should be suspended:
    - Is the model making materially wrong predictions right now?
    - Is a prior stable version available in the MLflow registry?
    - Is a rules-based fallback available?
    → If model must be suspended: activate fallback; document who authorized and when
□ DO NOT retrain or promote a new version without the standard change process
    (P1 does not exempt T1 models from change management requirements)
□ Preserve current MLflow run and model version details before any action
```

**T2 Model:**
```
□ Notify ML Lead within 30 minutes
□ Assess whether degradation materially affects business decisions
□ If yes: roll back to previous version from MLflow registry
□ If no: continue serving with intensified monitoring (hourly drift checks)
```

#### Investigation

```python
def investigate_ml_incident(
    model_name: str,
    mlflow_client,
    snowflake_conn,
    window_days: int = 7
) -> dict:
    """Pull production model metadata, drift status, and prediction volume."""

    # Production version(s)
    prod_versions = mlflow_client.search_model_versions(
        f"name='{model_name}' and tags.stage='production'"
    )

    cursor = snowflake_conn.cursor()

    # Active drift incidents
    cursor.execute("""
        SELECT feature_name, drift_score, drift_threshold,
               drift_score > drift_threshold AS is_drifted,
               detected_at, is_resolved
        FROM machine_learning.monitoring.drift_incidents
        WHERE model_name = %(model)s
          AND detected_at >= DATEADD('day', -%(window)s, CURRENT_TIMESTAMP())
        ORDER BY detected_at DESC
    """, {"model": model_name, "window": window_days})
    drift_records = cursor.fetchall()

    # Prediction volume anomalies (z-score > 2)
    cursor.execute("""
        SELECT prediction_date, prediction_count, baseline_mean,
               ABS(prediction_count - baseline_mean)
                 / NULLIF(baseline_stddev, 0) AS z_score
        FROM machine_learning.monitoring.prediction_volume
        WHERE model_name = %(model)s
          AND prediction_date >= CURRENT_DATE() - %(window)s
          AND ABS(prediction_count - baseline_mean)
                / NULLIF(baseline_stddev, 0) > 2
        ORDER BY prediction_date DESC
    """, {"model": model_name, "window": window_days})
    anomalies = cursor.fetchall()

    return {
        "production_versions": [v.version for v in prod_versions],
        "active_drift": [r for r in drift_records if r[3] and not r[5]],
        "volume_anomalies": anomalies,
    }
```

#### Resolution Checklist

```
□ Root cause identified:
    - Feature drift (upstream data changed)   → Resolve feature pipeline first
    - Concept drift (world changed)           → Emergency retrain
    - Serving infrastructure failure          → Platform fix; model may not need retrain
    - Training data contamination             → Invalidate run; full retrain
□ Fallback status documented: what is currently serving predictions
□ New model version validated against holdout set before promotion
□ T1 model: Model Risk notified; validation assessment before reinstating new version
□ Serving restored; confirmed healthy for 24 hours before incident closed
□ Monitoring thresholds reviewed and tightened where appropriate
□ Post-incident review mandatory for all T1 incidents
```

---

### 3.6 BI Report Producing Incorrect Data

**Incident Type:** `INC-BI` | **Typical Severity:** P2 (regulatory) · P3 (operational)

**Description:** A published BI report is displaying data that is materially incorrect or stale in a way that could lead to wrong business or regulatory decisions.

#### Detection Sources
- Business user report: "These numbers don't match last week"
- Automated reconciliation job: Gold layer value vs. BI report diverges
- External audit / regulator identifying a reporting discrepancy
- Data contract check failure on a certified dataset

#### Containment Steps

```
□ Is this a T1 Certified (regulatory) report?
    YES → P2; notify CDO, BI COE Lead, and Compliance immediately
    NO  → P3; notify BI COE Lead and domain data owner
□ Take the report offline if it is actively driving wrong decisions or is regulatory:
    TABLEAU:  Unpublish workbook or move to "Under Review" project
    POWER BI: Disable workspace access; take dataset offline
□ Post an incident notice in the BI tool description field:
    "UNAVAILABLE — Data quality investigation in progress (INC-YYYY-####).
     Contact [BI COE Lead] for status. ETA: [time]."
□ Communicate the last-known-correct refresh timestamp to stakeholders
```

#### Investigation Checklist

```
□ Trace the error using the data lineage chain:
    Source system → Bronze → Silver → Gold → Semantic layer → BI dataset → Report
    Work backwards from the incorrect value
□ Identify the break point:
    - BI report calculation / measure?  → Report logic error (BI COE)
    - Semantic layer / dbt metric?      → Transformation error (Analytics Eng.)
    - Gold table?                       → Pipeline error (DE → Section 3.1)
    - Source system?                    → Upstream issue (Source team + DE)
□ Review recent changes in the lineage chain:
    - BI tool deployment history
    - dbt run history
    - Pipeline run log
    - Source system change log
□ Quantify the error: how many rows / time periods are affected?
□ Assess regulatory impact: has an incorrect number been filed or submitted?
```

#### Resolution Checklist

```
□ Root cause identified and documented in incident record
□ Fix applied and validated end-to-end (source → report)
□ Report republished after BI COE Lead and data owner sign-off
□ Affected stakeholders notified of resolution and corrected figures
□ If incorrect data was in a regulatory submission:
    → Legal + Compliance assess whether a correction filing is required
    → CDO sign-off on correction approach
□ Historical data corrected in underlying tables if applicable (with change ticket)
□ All other reports consuming the same broken dataset reviewed
□ Post-incident review for all P2 BI incidents
```

---

### 3.7 Schema Change Breaking Downstream Consumers

**Incident Type:** `INC-SCH` | **Typical Severity:** P2–P3

**Description:** A schema change (column renamed/dropped, type changed, table moved) has broken downstream consumers that depend on the affected object, without a data contract change notification having been issued.

#### Detection Sources
- Pipeline failure: "column not found" or "type mismatch" error
- BI report failure: dataset refresh error after a Gold table change
- ML feature pipeline error: feature column missing from serving payload
- dbt test failure: not_null test on a column that has been dropped

#### Containment Steps

```
□ Identify all consumers of the affected schema object:
    - Collibra lineage: downstream dependencies
    - dbt: ref() and source() usage
    - Report Registry: certified datasets using this table
    - Feature store dependency map: ML features derived from this table
□ Notify all affected consumer leads immediately
□ Assess rollback feasibility:
    - Can the schema change be reverted without losing data?
    - Is the change already receiving active writes to the new schema?
□ If rollback feasible and consumers are broken: rollback first, fix process second
□ If rollback not feasible: create a compatibility view (old column names mapped to new):
    CREATE OR REPLACE VIEW <schema>.<table>_compat AS
    SELECT <new_column> AS <old_column>, ...
    FROM <schema>.<table>;
```

#### Resolution Checklist

```
□ All broken consumers identified and notified
□ Schema reverted or compatibility view deployed
□ All consumers restored and validated
□ Data contract updated to reflect the schema change (if change is staying)
□ Consumer teams scheduled to migrate to new schema (planned cut-over)
□ Root cause: was the data contract change notification process followed?
    NO → Post-incident: process retrain for responsible team; update change management doc
□ Collibra lineage updated to reflect current schema state
```

---

### 3.8 Credentials / Secret Exposure

**Incident Type:** `INC-SEC` | **Typical Severity:** P1

**Description:** A credential, API key, service account password, or connection string has been confirmed or suspected to be exposed — most commonly via Git commit, log file, or shared storage.

> ⚠️ **Assume breach until proven otherwise.** Treat any exposed credential as if it has already been used maliciously, even with no evidence of misuse yet.

#### Immediate Containment (< 30 minutes, P1)

```
□ Rotate the exposed credential IMMEDIATELY — do not wait for investigation:
    SNOWFLAKE:  ALTER USER <svc_account> RESET PASSWORD;
                Generate new RSA key pair and register public key
    DATABRICKS: Revoke PAT; issue new service principal secret
    AWS:        Deactivate key in IAM Console; issue replacement key
    API KEY:    Revoke via provider API / console; issue new key
□ Remove the secret from the exposure location:
    GIT:        git filter-repo or BFG Repo Cleaner to purge from all history branches
    LOG FILE:   Truncate or secure the log; notify log aggregation team
    CONFIG:     Remove hardcoded value; replace with Secrets Manager reference
□ Notify InfoSec / CISO within 30 minutes
□ Notify CDO within 1 hour
□ Preserve all evidence before any further action (see Section 5)
```

#### Investigation Steps

```
□ Determine exposure window:
    GIT:       git log --all -- <filename>  → find first commit containing the secret
    LOG FILE:  Check log file creation / modification timestamps
□ Determine the blast radius: what systems and data can this credential access?
□ Review audit logs for the credential during the full exposure window:
    SNOWFLAKE:  SELECT * FROM snowflake.account_usage.login_history
                WHERE user_name = '<svc_account>'
                  AND event_timestamp >= '<exposure_start>';
    DATABRICKS: Audit log review for token usage activity
□ Confirm whether the credential was used by unauthorized parties
□ Identify all actions taken by the credential during the exposure window
□ Identify the root cause: how did the secret enter the exposure location?
```

#### Resolution Checklist

```
□ New credential active and tested (services using it confirmed operational)
□ Secret purged from all exposure locations and version control history
□ Secrets Manager / Key Vault reference in place (no hardcoded secrets remain)
□ Pre-commit hook (gitleaks / trufflehog) confirmed active for affected repo
□ All repos scanned for similar patterns using the same secret-scanning tool
□ Investigation completed: confirmed whether unauthorized access occurred
□ If unauthorized access confirmed: open INC-ACC in parallel (Section 3.3)
□ Post-incident review mandatory; process retrain for responsible team
□ Credential rotation schedule updated to quarterly minimum if not already in place
```

---

## 4. Escalation Matrix

### 4.1 Notification by Incident Type and Severity

| Incident Type | P1 (< 1 hour) | P2 (< 4 hours) | P3 (< 1 business day) |
|---|---|---|---|
| `INC-DQ` | CDO, DE Lead, DGO, consumer leads | DE Lead, DGO, consumer leads | DE Lead |
| `INC-PII` | CDO, Privacy Officer, Legal, InfoSec, DGO | CDO, Privacy Officer, DGO | DGO, Domain Owner |
| `INC-ACC` | CDO, InfoSec/CISO, Privacy Officer, Legal | CDO, InfoSec, DGO | DGO, Domain Owner, IT |
| `INC-OUT` | CDO, DE Lead, consumer leads | DE Lead, consumer leads | DE Lead |
| `INC-ML` (T1) | CDO, ML Lead, Model Risk, DGO | CDO, ML Lead, Model Risk | ML Lead |
| `INC-ML` (T2/T3) | ML Lead, DGO | ML Lead | ML Lead |
| `INC-BI` (regulatory) | CDO, BI COE Lead, Compliance, Legal | CDO, BI COE Lead, Compliance | BI COE Lead |
| `INC-BI` (operational) | BI COE Lead, Domain Owner | BI COE Lead | BI COE Lead |
| `INC-SCH` | DE Lead, all consumer leads | DE Lead, consumer leads | DE Lead |
| `INC-SEC` | CDO, InfoSec/CISO, Legal, DGO, DE Lead | CDO, InfoSec | DE Lead, InfoSec |

### 4.2 Escalation Triggers

| Condition | Action |
|---|---|
| P1 not contained within 1 hour | CDO escalates to executive team; Board notification assessed |
| P1 regulatory notification threshold met | Legal + CDO initiate regulatory filing (see Section 9) |
| P2 not resolved within 8 hours | Escalate to P1 |
| Any P1 involving a T1 ML model | Model Risk Committee notified within 24 hours |
| Confirmed unauthorized access to Restricted data | Privacy Officer + Legal notified; GDPR / CCPA / HIPAA clock assessed |
| Incident involves a vendor or third-party system | Legal reviews vendor SLA and breach notification obligations |
| Post-incident reveals systemic control failure | CDO commissions 2LOD review; DGO opens formal audit finding |

---

## 5. Evidence Preservation Guide

Evidence must be captured **before** any remediation action. Store all evidence in the incident evidence folder:

```
incident-evidence/
  {YYYY}/
    {INC-YYYY-TYPE-####}/
      00_incident_record.yaml        ← Incident metadata and timeline
      01_detection_evidence/         ← Original alert / screenshot / log
      02_query_history/              ← Platform query history exports
      03_access_logs/                ← User access logs, SIEM exports
      04_platform_snapshots/         ← Config state at time of incident
      05_communications/             ← Notification records with timestamps
      06_remediation_log/            ← Timestamped log of every action taken
      07_root_cause_analysis/        ← RCA document (post-incident)
```

### 5.1 Evidence Collection SQL — Snowflake

```sql
-- ── Query history for affected table ──────────────────────────────────────────
SELECT
    query_id, user_name, role_name, query_type, query_text,
    database_name, schema_name, start_time, end_time,
    rows_produced, bytes_scanned
FROM snowflake.account_usage.query_history
WHERE (query_text ILIKE '%<affected_table>%'
       OR query_text ILIKE '%<affected_schema>%')
  AND start_time >= '<incident_window_start>'
ORDER BY start_time DESC;

-- ── Object-level access history ───────────────────────────────────────────────
SELECT
    user_name, query_id, query_start_time,
    direct_objects_accessed, base_objects_accessed, objects_modified
FROM snowflake.account_usage.access_history
WHERE query_start_time >= '<incident_window_start>'
  AND ARRAY_CONTAINS('<affected_table>'::VARIANT, direct_objects_accessed)
ORDER BY query_start_time DESC;

-- ── Login history for a specific user ─────────────────────────────────────────
SELECT
    event_timestamp, user_name, client_ip,
    reported_client_type, is_success, error_code, error_message
FROM snowflake.account_usage.login_history
WHERE user_name = '<user>'
  AND event_timestamp >= '<incident_window_start>'
ORDER BY event_timestamp DESC;

-- ── Role grant history ────────────────────────────────────────────────────────
SELECT
    created_on, deleted_on, grantee_name,
    role AS role_name, granted_by, granted_to
FROM snowflake.account_usage.grants_to_users
WHERE grantee_name = '<user>'
ORDER BY created_on DESC;
```

### 5.2 Evidence Retention Requirements

| Evidence Type | Minimum Retention | Notes |
|---|---|---|
| P1 incident records | 7 years | SOX, GDPR, HIPAA may apply |
| P2 incident records | 5 years | Per data retention policy |
| P3/P4 incident records | 2 years | Per data retention policy |
| Regulatory notification records | 7 years or per regulation | GDPR, CCPA, HIPAA specific |
| Platform audit logs (Snowflake / Databricks) | Minimum 1 year; 3 years for regulated data | Configure in ACCOUNT_USAGE retention settings |

---

## 6. Post-Incident Process

### 6.1 When Is a Post-Incident Review Required?

| Condition | Requirement |
|---|---|
| Any P1 incident | Mandatory within 5 business days |
| Any P2 involving regulated data | Mandatory within 10 business days |
| Recurring P2 (same root cause within 30 days) | Mandatory |
| Any P2+ involving a vendor or third party | Mandatory |
| P3 with a novel or unusual root cause | Recommended |

### 6.2 Post-Incident Review Template

```markdown
# Post-Incident Review — INC-[YYYY]-[TYPE]-[####]

## Incident Summary
- **ID / Type / Severity:** INC-YYYY-TYPE-#### · [P1/P2/P3]
- **Opened:** [timestamp UTC]
- **Contained:** [timestamp] (elapsed: X hr Y min)
- **Resolved:** [timestamp] (elapsed: X hr Y min)
- **Incident Commander:** [name]

## Timeline
| Time (UTC) | Action | Actor |
|---|---|---|
| HH:MM | Detection event | System / Person |
| HH:MM | First notification sent | Name |
| HH:MM | Containment action taken | Name |
| HH:MM | Resolution confirmed | Name |

## Root Cause Analysis (5 Whys)
1. Why did [symptom] occur? → [answer]
2. Why did [answer-1] occur? → [answer]
3. Why did [answer-2] occur? → [answer]
4. Why did [answer-3] occur? → [answer]
5. Why did [answer-4] occur? → **[root cause]**

## Impact Assessment
- **Data affected:** [table / report / model]
- **Classification:** [Restricted / Confidential / etc.]
- **Duration of impact:** [X hr Y min]
- **Consumers affected:** [list]
- **Data subjects affected (if PII):** [count or N/A]
- **Regulatory notification required:** Yes / No — [basis]

## What Went Well
- [Item]

## What Could Have Gone Better
- [Item]

## Action Items
| Action | Owner | Due Date | Priority |
|---|---|---|---|
| [Corrective control] | [Name] | [Date] | P1/P2/P3 |
| [Process improvement] | [Name] | [Date] | P1/P2/P3 |
| [Standard update] | [Name] | [Date] | P1/P2/P3 |

## Approval
- Incident Commander: _________________ Date: _______
- CDO (P1 required): _________________ Date: _______
- DGO Lead: _________________ Date: _______
```

---

## 7. Incident Automation — Python Pattern

```python
# incident_manager.py
"""
Automated incident triage, Slack notification, evidence collection,
and Snowflake register persistence.
Config-driven: all routing, channels, and SLAs defined in YAML.
"""

import yaml
import json
import csv
import requests
import snowflake.connector
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from enum import Enum


class Severity(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentType(str, Enum):
    DQ  = "INC-DQ"
    PII = "INC-PII"
    ACC = "INC-ACC"
    OUT = "INC-OUT"
    ML  = "INC-ML"
    BI  = "INC-BI"
    SCH = "INC-SCH"
    SEC = "INC-SEC"


@dataclass
class Incident:
    incident_type: IncidentType
    severity: Severity
    description: str
    affected_asset: str
    data_classification: str
    detection_source: str
    detected_by: str
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    incident_id: str = ""
    status: str = "OPEN"

    def __post_init__(self):
        if not self.incident_id:
            ts = self.opened_at.strftime("%Y%m%d%H%M")
            tag = self.incident_type.value.replace("INC-", "")
            self.incident_id = f"INC-{self.opened_at.year}-{tag}-{ts}"

    def to_dict(self) -> dict:
        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "affected_asset": self.affected_asset,
            "data_classification": self.data_classification,
            "detection_source": self.detection_source,
            "detected_by": self.detected_by,
            "opened_at": self.opened_at.isoformat(),
            "status": self.status,
        }


class IncidentManager:
    """
    Opens, tracks, and closes data incidents.
    On P1/P2 open: automatically triggers Snowflake evidence collection.
    All escalation routing is externalized to incident_config.yaml.
    """

    def __init__(
        self,
        config_path: str,
        snowflake_conn_params: dict,
        slack_webhook: str,
        evidence_base_path: str = "/mnt/incident-evidence",
    ):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.sf_conn = snowflake.connector.connect(**snowflake_conn_params)
        self.slack_webhook = slack_webhook
        self.evidence_base_path = Path(evidence_base_path)

    # ── Public API ────────────────────────────────────────────────

    def open_incident(self, incident: Incident) -> str:
        self._persist_incident(incident)
        self._notify_slack(incident)
        if incident.severity in (Severity.P1, Severity.P2):
            self._collect_evidence(incident)
        return incident.incident_id

    def update_status(self, incident_id: str, status: str, note: str = "") -> None:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            UPDATE data_governance.incidents.incident_register
            SET status = %(status)s,
                notes  = ARRAY_APPEND(COALESCE(notes, ARRAY_CONSTRUCT()), %(note)s),
                updated_at = CURRENT_TIMESTAMP()
            WHERE incident_id = %(id)s
        """, {"status": status, "note": note, "id": incident_id})
        self._notify_slack_update(incident_id, status, note)

    def close_incident(self, incident_id: str, resolution_summary: str) -> None:
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            UPDATE data_governance.incidents.incident_register
            SET status             = 'RESOLVED',
                resolved_at        = CURRENT_TIMESTAMP(),
                resolution_summary = %(summary)s,
                updated_at         = CURRENT_TIMESTAMP()
            WHERE incident_id = %(id)s
        """, {"summary": resolution_summary, "id": incident_id})
        self._notify_slack_update(incident_id, "RESOLVED", resolution_summary)

    # ── Evidence Collection ───────────────────────────────────────

    def _collect_evidence(self, incident: Incident) -> None:
        evidence_dir = self.evidence_base_path / incident.incident_id
        evidence_dir.mkdir(parents=True, exist_ok=True)

        # Persist incident record
        with open(evidence_dir / "00_incident_record.json", "w") as f:
            json.dump(incident.to_dict(), f, indent=2, default=str)

        # Snowflake query history for affected asset (T-24hr to now)
        window_start = incident.opened_at - timedelta(hours=24)
        cursor = self.sf_conn.cursor()
        cursor.execute("""
            SELECT query_id, user_name, role_name, query_type,
                   query_text, database_name, schema_name,
                   start_time, rows_produced, bytes_scanned
            FROM snowflake.account_usage.query_history
            WHERE UPPER(query_text) LIKE UPPER(%(pattern)s)
              AND start_time >= %(window_start)s
            ORDER BY start_time DESC
            LIMIT 1000
        """, {
            "pattern": f"%{incident.affected_asset}%",
            "window_start": window_start
        })
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        with open(evidence_dir / "02_query_history.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

    # ── Notifications ─────────────────────────────────────────────

    def _notify_slack(self, incident: Incident) -> None:
        emoji = {"P1": "🚨", "P2": "⚠️", "P3": "🔶", "P4": "🔷"}
        routing = self.config["escalation"].get(
            incident.incident_type.value, {}
        ).get(incident.severity.value, {})
        channels = routing.get("slack_channels", ["#data-incidents"])
        notify   = ", ".join(routing.get("notify", []))

        text = (
            f"{emoji.get(incident.severity.value, '⚠️')} "
            f"*[{incident.severity.value}] DATA INCIDENT — {incident.incident_id}*\n"
            f"*Type:* {incident.incident_type.value} | "
            f"*Asset:* `{incident.affected_asset}` | "
            f"*Classification:* {incident.data_classification}\n"
            f"*Description:* {incident.description}\n"
            f"*Detected by:* {incident.detected_by} | "
            f"*Opened:* {incident.opened_at.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"*Notify:* {notify}"
        )
        for channel in channels:
            requests.post(
                self.slack_webhook,
                json={"text": text, "channel": channel},
                timeout=10,
            )

    def _notify_slack_update(self, incident_id: str, status: str, note: str) -> None:
        requests.post(
            self.slack_webhook,
            json={"text": f"📋 *{incident_id}* → *{status}*\n_{note}_"},
            timeout=10,
        )

    # ── Persistence ───────────────────────────────────────────────

    def _persist_incident(self, incident: Incident) -> None:
        cursor = self.sf_conn.cursor()
        d = incident.to_dict()
        cursor.execute("""
            INSERT INTO data_governance.incidents.incident_register
                (incident_id, incident_type, severity, description,
                 affected_asset, data_classification, detection_source,
                 detected_by, opened_at, status)
            VALUES
                (%(incident_id)s, %(incident_type)s, %(severity)s, %(description)s,
                 %(affected_asset)s, %(data_classification)s, %(detection_source)s,
                 %(detected_by)s, %(opened_at)s, %(status)s)
        """, d)


# ── DDL ───────────────────────────────────────────────────────────────────────

CREATE_INCIDENT_REGISTER_SQL = """
CREATE TABLE IF NOT EXISTS data_governance.incidents.incident_register (
    incident_id              VARCHAR(60)   NOT NULL PRIMARY KEY,
    incident_type            VARCHAR(20)   NOT NULL,
    severity                 VARCHAR(5)    NOT NULL,
    description              TEXT,
    affected_asset           VARCHAR(300),
    data_classification      VARCHAR(30),
    detection_source         VARCHAR(100),
    detected_by              VARCHAR(100),
    opened_at                TIMESTAMP_TZ  NOT NULL,
    status                   VARCHAR(20)   DEFAULT 'OPEN',
    contained_at             TIMESTAMP_TZ,
    resolved_at              TIMESTAMP_TZ,
    resolution_summary       TEXT,
    root_cause               TEXT,
    regulatory_notified      BOOLEAN       DEFAULT FALSE,
    regulatory_notified_at   TIMESTAMP_TZ,
    notes                    ARRAY,
    updated_at               TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP(),
    inserted_at              TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);
"""
```

---

## 8. YAML Configuration — Incident Routing

```yaml
# config/incidents/incident_config.yaml
# All escalation routing, SLA definitions, and notification targets.
# Edit here — no code changes required.

sla_minutes:
  P1: { acknowledge: 15,  contain: 60,   resolve: 240  }
  P2: { acknowledge: 30,  contain: 240,  resolve: 480  }
  P3: { acknowledge: 120, contain: 480,  resolve: 2880 }   # 2 business days
  P4: { acknowledge: 480,               resolve: 7200 }   # 5 business days

escalation:

  INC-DQ:
    P1:
      notify: ["CDO", "DE Lead", "DGO Lead", "Consumer Leads"]
      slack_channels: ["#data-incidents-p1", "#data-engineering"]
    P2:
      notify: ["DE Lead", "DGO Lead", "Consumer Leads"]
      slack_channels: ["#data-incidents", "#data-engineering"]
    P3:
      notify: ["DE Lead"]
      slack_channels: ["#data-engineering"]

  INC-PII:
    P1:
      notify: ["CDO", "Privacy Officer", "Legal", "InfoSec", "DGO Lead"]
      slack_channels: ["#data-incidents-p1", "#security-incidents"]
      regulatory_assessment_required: true
    P2:
      notify: ["CDO", "Privacy Officer", "DGO Lead"]
      slack_channels: ["#data-incidents"]
      regulatory_assessment_required: true

  INC-ACC:
    P1:
      notify: ["CDO", "InfoSec", "Privacy Officer", "Legal", "DGO Lead"]
      slack_channels: ["#data-incidents-p1", "#security-incidents"]
      regulatory_assessment_required: true
    P2:
      notify: ["CDO", "InfoSec", "DGO Lead"]
      slack_channels: ["#data-incidents", "#security-incidents"]

  INC-OUT:
    P1:
      notify: ["CDO", "DE Lead", "Consumer Leads"]
      slack_channels: ["#data-incidents-p1", "#data-engineering"]
    P2:
      notify: ["DE Lead", "Consumer Leads"]
      slack_channels: ["#data-incidents", "#data-engineering"]

  INC-ML:
    P1:
      notify: ["CDO", "ML Lead", "Model Risk", "DGO Lead"]
      slack_channels: ["#data-incidents-p1", "#ml-ops"]
    P2:
      notify: ["ML Lead", "DGO Lead"]
      slack_channels: ["#data-incidents", "#ml-ops"]

  INC-BI:
    P1:
      notify: ["CDO", "BI COE Lead", "Compliance", "Legal"]
      slack_channels: ["#data-incidents-p1", "#bi-governance"]
    P2:
      notify: ["CDO", "BI COE Lead", "Compliance"]
      slack_channels: ["#data-incidents", "#bi-governance"]

  INC-SCH:
    P1:
      notify: ["DE Lead", "All Consumer Leads"]
      slack_channels: ["#data-incidents-p1", "#data-engineering"]
    P2:
      notify: ["DE Lead", "Consumer Leads"]
      slack_channels: ["#data-incidents", "#data-engineering"]

  INC-SEC:
    P1:
      notify: ["CDO", "InfoSec", "Legal", "DGO Lead", "DE Lead"]
      slack_channels: ["#data-incidents-p1", "#security-incidents"]
      regulatory_assessment_required: true

# Regulatory assessment thresholds by data classification
regulatory:
  Restricted:
    assessment_required: true
    gdpr_72hr_clock: true
    hipaa_60_day_rule: true
    ccpa_45_day_rule: true
    notify_legal_within_hours: 2
  Confidential:
    assessment_required: true
    notify_legal_within_hours: 24
  Internal:
    assessment_required: false
```

---

## 9. Regulatory Notification Reference

> **This section does not constitute legal advice. Legal and Compliance must be consulted before any external notification is made.**

### 9.1 When to Assess

A regulatory notification assessment is mandatory when:
- Restricted data is confirmed or reasonably suspected to have been exposed to unauthorized parties
- PII, PHI, or financial account data has been accessed without authorization
- A security breach has occurred and the scope of data accessed is not yet fully known

### 9.2 Regulatory Clock Reference

| Regulation | Scope | Notification Window | To Whom |
|---|---|---|---|
| **GDPR** (EU/UK) | EU/UK data subject PII | 72 hours from knowledge of breach | Supervisory Authority (e.g., ICO) |
| **HIPAA** (US) | Protected Health Information (PHI) | 60 days from discovery | HHS OCR + affected individuals |
| **CCPA / CPRA** (California) | California resident PII | Expedient; 45 days if AG requests | Affected individuals; CA AG if >500 residents |
| **PCI DSS** | Cardholder data | Immediately upon suspicion | Card brands + acquiring bank |
| **SOX** | Financial reporting data integrity | Material breach disclosed promptly | SEC / Board Audit Committee |
| **State breach laws** | Varies; SSN, financial, health data typical | 30–90 days (varies by state) | Affected individuals; State AG |

### 9.3 Decision Flow

```
Restricted data exposure confirmed?
  YES  →  Identify data subject jurisdiction(s)
    EU/UK residents         →  GDPR 72-hr clock starts
    PHI involved            →  HIPAA clock starts
    California residents    →  CCPA/CPRA clock starts
    Cardholder data         →  PCI/SOX assessment required
  NO   →  Confidential data only → Legal assesses case-by-case

Legal must answer:
  □ Is this a "breach" under the applicable regulation?
  □ How many data subjects are affected?
  □ What categories of data were exposed?
  □ Is there a meaningful risk of harm to data subjects?
  □ Does a risk-of-harm assessment waive notification? (HIPAA / GDPR allow this)

CDO approves final notification decision.
All external notifications are sent by Legal on behalf of the organization.
CDO and DGO are copied on all regulatory correspondence.
```

---

## 10. Incident Register Template

```yaml
# 00_incident_record.yaml
# One file per incident, stored in: incident-evidence/{YYYY}/{INC-ID}/

incident_id:   "INC-2026-DQ-0001"
incident_type: "INC-DQ"       # INC-DQ | INC-PII | INC-ACC | INC-OUT | INC-ML | INC-BI | INC-SCH | INC-SEC
severity:      "P2"            # P1 | P2 | P3 | P4
status:        "RESOLVED"      # OPEN | INVESTIGATING | CONTAINED | RESOLVED

# Detection
opened_at:                 "2026-03-09T14:23:00Z"
detected_by:               "Airflow alert"
detection_source:          "Automated monitoring"
first_human_notified_at:   "2026-03-09T14:25:00Z"
first_human_notified:      "Jane Smith (DE Lead)"

# Scope
affected_asset:      "PROD_FINANCE_GOLD.finance.fact_revenue"
affected_domain:     "Finance"
data_classification: "Confidential"
affected_consumers:
  - "Finance KPI Dashboard (T1 BI)"
  - "Revenue Forecast ML Model (T2)"

description: |
  CRITICAL DQ gate failure in the finance_erp_gold_daily pipeline.
  fact_revenue has not been updated since 2026-03-08 22:00 UTC.
  Root cause: null revenue_key values introduced by source ERP extract bug.

# Timeline
timeline:
  - timestamp: "2026-03-09T14:23:00Z"
    event:     "Airflow task finance_erp_gold_daily failed with DQ gate error"
    actor:     "Airflow"
  - timestamp: "2026-03-09T14:25:00Z"
    event:     "Alert sent to #data-incidents and DE Lead"
    actor:     "IncidentManager"
  - timestamp: "2026-03-09T14:35:00Z"
    event:     "Incident opened in ITSM; investigation begun"
    actor:     "Jane Smith"
  - timestamp: "2026-03-09T15:10:00Z"
    event:     "Root cause identified: null revenue_key in ERP extract"
    actor:     "Jane Smith"
  - timestamp: "2026-03-09T16:45:00Z"
    event:     "Fix deployed; pipeline re-run; DQ gates passing"
    actor:     "Jane Smith"
  - timestamp: "2026-03-09T17:00:00Z"
    event:     "BI and ML consumers confirmed refreshed and accurate"
    actor:     "Jane Smith"

# Resolution
contained_at:         "2026-03-09T15:10:00Z"
resolved_at:          "2026-03-09T17:00:00Z"
total_duration_hours: 2.62
resolution_summary: |
  Source ERP export bug introduced null revenue_key values.
  Fix applied at source; pipeline re-run from Bronze layer.
  DQ gate updated: null revenue_key now CRITICAL severity.
root_cause:                   "Source system ERP export bug — null primary key values"
repeat_incident:              false
regulatory_notification_required: false

# Post-incident
post_incident_review_required: false
action_items:
  - action:    "Add null-check alert to ERP connector monitoring"
    owner:     "Jane Smith"
    due_date:  "2026-03-23"
    priority:  "P2"
  - action:    "Audit all fact table DQ configs for CRITICAL null PK check"
    owner:     "John Doe"
    due_date:  "2026-03-23"
    priority:  "P2"

# Evidence
evidence_collected:
  - "01_detection_evidence/airflow_task_log.txt"
  - "02_query_history/snowflake_query_history_20260309.csv"
  - "03_access_logs/pipeline_run_log.csv"

incident_commander: "Jane Smith"
cdo_notified:       false    # P2 non-regulatory; DE Lead is sufficient
```

---

*Document Owner: Chief Data Officer + Data Governance Office*
*Review Cycle: Semi-Annual | Mandatory review after any P1 incident*
*Related: `04_2nd_line_of_defense_strategy.md` · `04_DE_Auditing_Guide.md` · `04_ML_Auditing_Guide.md` · `04_BI_Auditing_Guide.md` · `README.md`*
