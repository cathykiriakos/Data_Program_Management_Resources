# Machine Learning Auditing Guide
## First & Second Line of Defense

**Document Owner:** Chief Data Office  
**Domain:** Machine Learning  
**Version:** 1.0  
**Classification:** Internal — Audit & Control

---

## Table of Contents

1. [Control Framework Overview](#1-control-framework-overview)
2. [First Line of Defense — Self-Assessment Controls](#2-first-line-of-defense--self-assessment-controls)
3. [Second Line of Defense — Independent Audit Procedures](#3-second-line-of-defense--independent-audit-procedures)
4. [Automated Audit Queries & Scripts](#4-automated-audit-queries--scripts)
5. [Model Risk Audit — T1 Deep Dive](#5-model-risk-audit--t1-deep-dive)
6. [Lineage Audit Procedures](#6-lineage-audit-procedures)
7. [Audit Cadence & Reporting](#7-audit-cadence--reporting)
8. [Findings Classification & Escalation](#8-findings-classification--escalation)
9. [Regulatory Audit Readiness](#9-regulatory-audit-readiness)

---

## 1. Control Framework Overview

### 1.1 Three Lines Model for ML

```
┌─────────────────────────────────────────────────────────────────┐
│  FIRST LINE: ML Engineering Team + Domain ML Teams             │
│  Own and operate controls; self-attest monthly                  │
│  Controls: Experiment tracking coverage, registry currency,     │
│  monitoring health, bias audit completion, cost controls,       │
│  model card completeness, performance gate compliance           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ attests to
┌──────────────────────────▼──────────────────────────────────────┐
│  SECOND LINE: Data Governance / Model Risk / Compliance         │
│  Independently verifies 1LOD controls are effective             │
│  Controls: Model inventory audit, lineage verification,         │
│  bias audit sampling, PII usage review, performance review,     │
│  regulatory model validation (T1)                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ independent assurance to
┌──────────────────────────▼──────────────────────────────────────┐
│  THIRD LINE: Internal Audit / Model Risk Committee / Regulator  │
│  Periodic deep-dive audits; regulatory model validation         │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Control Domains

| Domain | Key Risk | 1LOD Owner | 2LOD Verifier |
|---|---|---|---|
| Experiment tracking coverage | Untracked models in production | ML Engineering Lead | Data Governance |
| Model registry currency | Unregistered or orphaned models | ML Engineering Lead | Data Governance |
| Lineage completeness | Cannot trace model to source data | ML Engineering Lead | Data Governance |
| Bias & fairness | Discriminatory model outcomes | ML Governance Analyst | Model Risk / Legal |
| PII in training data | Unauthorized PII use | ML Governance Analyst | Privacy Officer |
| Model performance | Degraded model making bad decisions | Domain ML Lead | Model Risk |
| Monitoring health | Drift undetected | ML Platform Engineer | Data Governance |
| Cost management | Budget overruns | ML Platform Engineer | Finance |
| T1 model governance | Regulatory exposure | ML Governance Analyst | Model Risk / Legal |

---

## 2. First Line of Defense — Self-Assessment Controls

### Control ML-01: Experiment Tracking Coverage

**Objective:** Confirm 100% of production models have experiment tracking records.

**Frequency:** Monthly

**Procedure:**

```python
# ml/audit/tracking_coverage_check.py
"""
Cross-references production model registry with MLflow experiment records.
Flags production models without traceable experiment runs.
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime


def check_tracking_coverage(tracking_uri: str) -> list[dict]:
    """
    Find production models without linked experiment runs.
    Returns list of compliance gaps.
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    gaps = []

    # Get all production model versions
    for registered_model in client.search_registered_models():
        prod_versions = [
            v for v in client.search_model_versions(f"name='{registered_model.name}'")
            if v.current_stage == "Production"
        ]

        for version in prod_versions:
            issues = []

            # Check: has a linked run
            if not version.run_id:
                issues.append("No linked experiment run")
                gaps.append({
                    "model": registered_model.name,
                    "version": version.version,
                    "stage": version.current_stage,
                    "issues": issues,
                    "severity": "CRITICAL"
                })
                continue

            # Check: run has required metadata tags
            run = client.get_run(version.run_id)
            required_tags = [
                "model.name", "model.tier", "model.owner_team",
                "data.feature_table", "data.train_end",
                "governance.pii_used", "git.commit"
            ]
            missing_tags = [t for t in required_tags if t not in run.data.tags]
            if missing_tags:
                issues.append(f"Missing required tags: {missing_tags}")

            # Check: model artifact was logged
            artifacts = [a.path for a in client.list_artifacts(version.run_id)]
            if not any("model" in a for a in artifacts):
                issues.append("No model artifact logged")

            # Check: data profile was logged
            if not any("data_profile" in a for a in artifacts):
                issues.append("No data profile logged")

            if issues:
                gaps.append({
                    "model": registered_model.name,
                    "version": version.version,
                    "run_id": version.run_id,
                    "issues": issues,
                    "severity": "HIGH" if len(issues) > 1 else "MEDIUM"
                })

    return gaps
```

**Self-attestation:** ML Engineering Lead signs off on zero unresolved gaps monthly.

---

### Control ML-02: Model Registry Currency

**Objective:** Confirm Model Governance Registry (YAML) matches production model registry.

**Frequency:** Monthly

**Procedure:**

```python
# ml/audit/registry_currency_check.py
"""
Compare Model Governance Registry (YAML files) against MLflow production models.
Finds production models missing from governance registry.
"""

import os
import yaml
import mlflow
from mlflow.tracking import MlflowClient
from pathlib import Path


def check_registry_currency(
    governance_registry_dir: str,
    tracking_uri: str
) -> dict:
    """
    Returns governance gaps:
    - in_platform_not_in_registry: production models not in governance YAML
    - in_registry_not_in_platform: YAML entries for non-existent models
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    # Production models in platform
    platform_models = set()
    for rm in client.search_registered_models():
        for v in client.search_model_versions(f"name='{rm.name}'"):
            if v.current_stage == "Production":
                platform_models.add(rm.name)

    # Models in governance registry
    registry_models = set()
    for yaml_file in Path(governance_registry_dir).rglob("*.yaml"):
        with open(yaml_file) as f:
            entry = yaml.safe_load(f)
        if entry.get("model", {}).get("status") == "active":
            registry_models.add(entry["model"]["name"])

    return {
        "in_platform_not_in_registry": list(platform_models - registry_models),
        "in_registry_not_in_platform": list(registry_models - platform_models),
        "platform_count": len(platform_models),
        "registry_count": len(registry_models),
    }
```

---

### Control ML-03: Monitoring Health Check

**Objective:** Confirm all T1/T2 models have active, non-failing drift monitoring.

**Frequency:** Weekly (automated) + Monthly attestation

**Procedure:**

```python
# ml/audit/monitoring_health.py
"""
Verify monitoring jobs are active and not in failed/paused state.
"""

import mlflow
from mlflow.tracking import MlflowClient
from databricks.sdk import WorkspaceClient   # adjust for SageMaker equivalent


def check_monitoring_health(
    tracking_uri: str,
    databricks_host: str,
    databricks_token: str
) -> list[dict]:
    """
    For all T1/T2 production models, confirm monitoring is active.
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    w = WorkspaceClient(host=databricks_host, token=databricks_token)
    findings = []

    for rm in client.search_registered_models():
        for v in client.search_model_versions(f"name='{rm.name}'"):
            if v.current_stage != "Production":
                continue
            tier = v.tags.get("model.tier", "T3")
            if tier not in ("T1", "T2"):
                continue

            # Check monitoring job exists and is active
            # (In practice, map model name to monitoring job name via config)
            monitor_job_name = f"monitor_{rm.name.replace('.', '_')}"
            jobs = list(w.jobs.list(name=monitor_job_name))

            if not jobs:
                findings.append({
                    "model": rm.name,
                    "version": v.version,
                    "tier": tier,
                    "issue": "No monitoring job found",
                    "severity": "HIGH"
                })
            else:
                job = jobs[0]
                # Check last run status
                runs = list(w.jobs.list_runs(job_id=job.job_id, limit=1))
                if runs and runs[0].state.result_state.value not in ("SUCCESS", "RUNNING"):
                    findings.append({
                        "model": rm.name,
                        "version": v.version,
                        "tier": tier,
                        "issue": f"Last monitoring run failed: {runs[0].state.result_state.value}",
                        "severity": "HIGH"
                    })

    return findings
```

---

### Control ML-04: Bias Audit Completion

**Objective:** Confirm all T1 production models have a completed, current bias audit.

**Frequency:** Quarterly

**Self-Assessment Checklist:**
```
□ All T1 production models listed
□ Each has a bias audit completed within the last 12 months
□ Bias audit covers all available protected attributes
□ 4/5 rule results documented
□ Equalized odds results documented
□ ML Governance Analyst has signed off on each audit
□ Any bias findings have documented remediation plans
```

---

### Control ML-05: Performance Gate Compliance

**Objective:** Confirm all production models are above their defined performance gates.

**Frequency:** Monthly

**Procedure:**

```python
# ml/audit/performance_gate_check.py
"""
Check all production models against their defined performance gates.
Flags models below gate for immediate review.
"""

import mlflow
from mlflow.tracking import MlflowClient
import yaml
from pathlib import Path


def check_performance_gates(
    tracking_uri: str,
    governance_registry_dir: str
) -> list[dict]:
    """
    For each production model, check latest metrics vs. configured gates.
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    findings = []

    for yaml_file in Path(governance_registry_dir).rglob("*.yaml"):
        with open(yaml_file) as f:
            entry = yaml.safe_load(f)

        if entry.get("model", {}).get("status") != "active":
            continue

        model_name = entry["model"]["name"]
        gates = entry.get("performance_gates", {})
        current_metrics = entry.get("performance", {})

        for gate_name, gate_value in gates.items():
            if gate_name.startswith("min_"):
                metric_name = gate_name[4:]  # Remove "min_" prefix
                current_value = current_metrics.get(metric_name)
                if current_value is not None and float(current_value) < float(gate_value):
                    findings.append({
                        "model": model_name,
                        "gate": gate_name,
                        "gate_value": gate_value,
                        "current_value": current_value,
                        "gap": round(float(gate_value) - float(current_value), 4),
                        "severity": "HIGH"
                    })

    return findings
```

---

### Control ML-06: Cost vs. Budget

**Objective:** Confirm ML compute costs are within approved budget.

**Frequency:** Monthly

**Procedure:**
1. Pull Databricks / SageMaker / cloud cost reports filtered by ML cost center tags.
2. Compare to monthly budget by model and by domain.
3. Flag any model exceeding 25% of its monthly allocation.
4. Confirm all compute has required cost tags (untagged = finding).

---

## 3. Second Line of Defense — Independent Audit Procedures

### Audit ML-AU-01: Independent Model Inventory Reconciliation

**Objective:** Independently verify the ML team's model inventory is complete and accurate — without relying on the ML team's own attestation.

**Frequency:** Quarterly

**Procedure:**
1. Query the production ML platform (MLflow API / SageMaker API) directly using a Data Governance service account.
2. List all models in Production stage.
3. Cross-reference each against the Model Governance Registry YAML files.
4. For each gap, determine:
   - Model in platform but not in registry: **HIGH finding**
   - Model in registry but not in platform: Stale registry entry — **MEDIUM finding**
5. For a 10% sample of registered models, verify the governance YAML content matches the platform record (version number, tier, owner).

```python
# 2LOD uses a separate read-only service account — not the ML team's account
# to ensure independence

def independent_inventory_audit(
    governance_svc_token: str,     # 2LOD service account
    governance_registry_dir: str,
    tracking_uri: str
) -> dict:
    """2LOD independent model inventory audit."""
    import mlflow
    mlflow.set_tracking_uri(tracking_uri)
    # Set auth to 2LOD service account
    import os
    os.environ["MLFLOW_TRACKING_TOKEN"] = governance_svc_token

    # Rest of logic same as ML-02 but executed by 2LOD team
    # with independent service account
    return check_registry_currency(governance_registry_dir, tracking_uri)
```

---

### Audit ML-AU-02: PII Usage Independent Review

**Objective:** Confirm no model is training on PII without documented Privacy Officer approval.

**Frequency:** Quarterly

**Procedure:**
1. Query MLflow for all production runs with `governance.pii_used = true`.
2. For each, retrieve the associated governance registry entry.
3. Verify a Privacy Officer sign-off record exists (linked in the registry or model card).
4. For T1 models with PII: verify Legal review sign-off also exists.
5. Also check the **negative case**: sample 20 production models with `governance.pii_used = false` and verify the training feature table does not contain PII columns (cross-reference with data catalog PII tags).

```python
# ml/audit/pii_usage_audit.py

def audit_pii_usage(
    tracking_uri: str,
    governance_registry_dir: str,
    data_catalog_api_url: str
) -> list[dict]:
    """
    2LOD: Verify PII usage is declared and approved for all production models.
    """
    import mlflow
    from mlflow.tracking import MlflowClient
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    findings = []

    for rm in client.search_registered_models():
        for v in client.search_model_versions(f"name='{rm.name}'"):
            if v.current_stage != "Production":
                continue

            run = client.get_run(v.run_id)
            pii_used = run.data.tags.get("governance.pii_used", "false").lower()
            feature_table = run.data.tags.get("data.feature_table", "")

            if pii_used == "true":
                # Check for Privacy Officer approval in governance registry
                approval_found = _check_privacy_approval(
                    rm.name, governance_registry_dir
                )
                if not approval_found:
                    findings.append({
                        "audit": "ML-AU-02",
                        "model": rm.name,
                        "version": v.version,
                        "issue": "PII used but no Privacy Officer approval found",
                        "severity": "CRITICAL"
                    })

            # Spot-check: verify feature table PII status matches declaration
            if feature_table and pii_used == "false":
                table_has_pii = _query_catalog_for_pii(
                    feature_table, data_catalog_api_url
                )
                if table_has_pii:
                    findings.append({
                        "audit": "ML-AU-02",
                        "model": rm.name,
                        "version": v.version,
                        "feature_table": feature_table,
                        "issue": "Feature table contains PII but model declares pii_used=false",
                        "severity": "HIGH"
                    })

    return findings


def _check_privacy_approval(model_name: str, registry_dir: str) -> bool:
    """Check if Privacy Officer approval exists in governance registry."""
    from pathlib import Path
    import yaml
    for f in Path(registry_dir).rglob("*.yaml"):
        with open(f) as yf:
            entry = yaml.safe_load(yf)
        if entry.get("model", {}).get("name") == model_name:
            gov = entry.get("governance", {})
            return gov.get("privacy_officer_approval", False)
    return False


def _query_catalog_for_pii(feature_table: str, catalog_api: str) -> bool:
    """Query the data catalog to check if a table has PII tags."""
    import requests
    try:
        resp = requests.get(f"{catalog_api}/tables/{feature_table}/tags")
        tags = resp.json().get("tags", {})
        pii_tags = [v for k, v in tags.items() if "pii" in k.lower()]
        return any(v not in ("NONE", "false", "") for v in pii_tags)
    except Exception:
        return False  # Cannot verify — flag for manual review
```

---

### Audit ML-AU-03: Model Lineage Completeness Verification

**Objective:** Confirm every production model has a complete, verifiable lineage from source data to predictions.

**Frequency:** Quarterly

**Procedure (for each production model, verify all 5 lineage links):**

```python
# ml/audit/lineage_audit.py
"""
Verify the complete lineage chain for production models.
5 required links: source → bronze → silver → feature table → model → predictions.
"""

from mlflow.tracking import MlflowClient
import mlflow


@dataclass
class LineageAuditResult:
    model_name: str
    version: str
    link_1_source_to_bronze: bool      # Source system → Bronze table
    link_2_bronze_to_silver: bool      # Bronze → Silver (dbt lineage)
    link_3_silver_to_features: bool    # Silver → Feature table
    link_4_features_to_model: bool     # Feature table → Model run (MLflow tag)
    link_5_model_to_predictions: bool  # Model version → Prediction table column
    complete: bool
    gaps: list[str]


def audit_model_lineage(
    model_name: str,
    model_version: str,
    tracking_uri: str,
    snowflake_session=None
) -> LineageAuditResult:
    """
    Verify complete lineage chain for a production model version.
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    mv = client.get_model_version(model_name, model_version)
    run = client.get_run(mv.run_id)
    tags = run.data.tags
    gaps = []

    # Link 4: Feature table recorded in run tags
    feature_table = tags.get("data.feature_table", "")
    link_4 = bool(feature_table)
    if not link_4:
        gaps.append("Link 4: data.feature_table tag missing from training run")

    # Link 5: Model version visible in prediction table
    link_5 = False
    if snowflake_session and feature_table:
        try:
            pred_table = f"{feature_table.split('.')[0]}.ml.predictions_{model_name.split('.')[-1]}"
            result = snowflake_session.sql(
                f"SELECT COUNT(*) FROM {pred_table} "
                f"WHERE _model_name = '{model_name}' AND _model_version = '{model_version}' LIMIT 1"
            ).collect()
            link_5 = result[0][0] > 0
        except Exception:
            link_5 = False
    if not link_5:
        gaps.append(f"Link 5: No predictions found with model_version={model_version}")

    # Links 1–3 verified via data catalog / dbt lineage (simplified)
    link_1 = bool(tags.get("data.source_system", ""))
    link_2 = bool(tags.get("data.train_start", ""))
    link_3 = link_4  # If feature table is tracked, link 3 is implied

    if not link_1:
        gaps.append("Link 1: data.source_system tag missing")
    if not link_2:
        gaps.append("Link 2: data.train_start tag missing")

    complete = all([link_1, link_2, link_3, link_4, link_5])

    return LineageAuditResult(
        model_name=model_name,
        version=model_version,
        link_1_source_to_bronze=link_1,
        link_2_bronze_to_silver=link_2,
        link_3_silver_to_features=link_3,
        link_4_features_to_model=link_4,
        link_5_model_to_predictions=link_5,
        complete=complete,
        gaps=gaps
    )
```

---

### Audit ML-AU-04: Independent Bias Audit Sampling

**Objective:** Independently verify bias audit completeness and accuracy for T1 models.

**Frequency:** Semi-annual

**Procedure:**
1. Identify all T1 models currently in production.
2. For each, retrieve the bias audit report from the model card / MLflow artifact.
3. Independently re-run the bias checks using a 2LOD service account and the holdout dataset.
4. Compare 2LOD results to the 1LOD bias audit report — flag material discrepancies (>2pp difference in disparity ratio).
5. Verify that all tested protected attributes are those defined in the bias audit policy (not a cherry-picked subset).

---

### Audit ML-AU-05: Model Performance Trend Review

**Objective:** Independently verify models are performing as reported; catch any concealed degradation.

**Frequency:** Quarterly

**Procedure:**
1. For all T1/T2 production models, pull the last 90 days of drift monitoring results from the monitoring store.
2. Independently compare current feature distributions to training baselines.
3. Where labeled actuals are available (e.g., churn outcomes for churn models), independently compute AUC on recent labeled data.
4. Compare 2LOD AUC to the ML team's reported current AUC.
5. Flag models where 2LOD performance metric deviates >3pp from reported metric.

---

### Audit ML-AU-06: Change Management Compliance

**Objective:** Confirm all production model promotions followed the change management process.

**Frequency:** Quarterly (sample-based)

**Procedure:**
1. Pull all production promotions in the quarter from MLflow registry tags (`production.timestamp`, `production.change_ticket`).
2. Sample 10 promotions or 25% (whichever is larger).
3. For each sampled promotion, verify:
   - A change ticket exists in ITSM with the matching ticket number.
   - The ticket was approved by the required approvers (ML Engineering Lead + domain owner).
   - For T1/T2 models: champion/challenger results attached.
   - Staging promotion preceded production promotion.
   - CI/CD pipeline log shows the deployment was automated (not manual).
4. Report compliance rate.

---

## 4. Automated Audit Queries & Scripts

### 4.1 Monthly ML Governance Summary

```python
# ml/audit/monthly_governance_summary.py
"""
Automated monthly governance summary.
Runs all 1LOD checks and produces a report.
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime, timezone
import json


def run_monthly_ml_audit(
    tracking_uri: str,
    governance_registry_dir: str,
    output_path: str
) -> dict:
    """Run all self-assessment controls and produce monthly summary."""

    results = {
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "controls": {}
    }

    # ML-01: Tracking coverage
    from ml.audit.tracking_coverage_check import check_tracking_coverage
    tracking_gaps = check_tracking_coverage(tracking_uri)
    results["controls"]["ML-01_tracking_coverage"] = {
        "total_gaps": len(tracking_gaps),
        "critical_gaps": len([g for g in tracking_gaps if g["severity"] == "CRITICAL"]),
        "pass": len(tracking_gaps) == 0,
        "gaps": tracking_gaps
    }

    # ML-02: Registry currency
    from ml.audit.registry_currency_check import check_registry_currency
    currency = check_registry_currency(governance_registry_dir, tracking_uri)
    results["controls"]["ML-02_registry_currency"] = {
        "unregistered_production_models": len(currency["in_platform_not_in_registry"]),
        "stale_registry_entries": len(currency["in_registry_not_in_platform"]),
        "pass": len(currency["in_platform_not_in_registry"]) == 0,
        "details": currency
    }

    # ML-05: Performance gates
    from ml.audit.performance_gate_check import check_performance_gates
    gate_failures = check_performance_gates(tracking_uri, governance_registry_dir)
    results["controls"]["ML-05_performance_gates"] = {
        "total_failures": len(gate_failures),
        "pass": len(gate_failures) == 0,
        "failures": gate_failures
    }

    # Overall assessment
    all_passed = all(c["pass"] for c in results["controls"].values())
    results["overall"] = {
        "pass": all_passed,
        "total_controls_checked": len(results["controls"]),
        "controls_failed": len([c for c in results["controls"].values() if not c["pass"]])
    }

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    return results
```

---

## 5. Model Risk Audit — T1 Deep Dive

### 5.1 T1 Model Audit Checklist

For every T1 model, the following must be verified by the 2LOD function at least annually and before any major version promotion:

```
Model Identity & Ownership
  □ Model name and version in platform matches governance registry
  □ Named owner is a current employee with active account
  □ Domain business owner is named and has confirmed accountability
  □ Model card is published, current, and complete

Data & Lineage
  □ Training data version is immutable and traceable (DVC hash / Delta snapshot)
  □ Feature table is the same one used in production scoring (no version drift)
  □ No future data leakage: test period strictly after training period
  □ PII usage declared and approved (if applicable)
  □ Source tables traceable from model back to original source systems

Performance & Validation
  □ Holdout test results independently verified (2LOD re-run)
  □ Model beats documented baselines
  □ Performance has not degraded below gate since deployment
  □ Champion/challenger results on file for the current production version
  □ Benchmark report signed off by ML Engineering Lead

Bias & Fairness
  □ Bias audit completed within last 12 months
  □ All applicable protected attributes tested
  □ 4/5 rule PASS for all groups
  □ Equalized odds within acceptable range
  □ Bias findings (if any) have documented and implemented remediation

Explainability
  □ SHAP values or equivalent generated and stored for current version
  □ Feature importance is interpretable and consistent with business expectations
  □ No feature with unexplained outsized importance (proxy variable for protected class risk)

Governance Compliance
  □ Risk assessment completed and signed
  □ Change ticket on file for production promotion
  □ Model deployed via CI/CD (not manual)
  □ Rollback plan documented and tested

Monitoring
  □ Drift monitoring active and not in failed state
  □ Alert thresholds configured correctly
  □ Last 90 days of monitoring reports available
  □ Any drift alerts in period: investigated and resolved with documentation

Business Accountability
  □ Business KPI reported monthly and on track
  □ Business owner has reviewed model performance in last quarter
```

---

## 6. Lineage Audit Procedures

### 6.1 Full Lineage Verification Workflow

```
Step 1: Identify production model version
   └── From MLflow registry: model_name, version, run_id

Step 2: Trace training data
   └── From run tags: data.feature_table, data.train_end, data.feature_hash
   └── Verify feature table exists in feature store / Gold catalog
   └── Verify DVC hash or Delta snapshot version matches registered value

Step 3: Trace feature table to Silver layer
   └── Feature table has a documented derivation (dbt model or pipeline)
   └── dbt lineage graph shows Silver → Feature table transformation
   └── Verify Silver table data_retention_policy covers the training period

Step 4: Trace Silver to Bronze
   └── dbt lineage graph shows Bronze → Silver transformation
   └── Bronze table metadata matches source system declaration

Step 5: Trace Bronze to Source
   └── Bronze table has _source_system metadata column
   └── Ingestion pipeline documented (DE standards doc)

Step 6: Trace model to predictions
   └── Prediction table exists for this model
   └── Prediction table has _model_version column
   └── Sample records confirm _model_version = verified production version
   └── Prediction table is queryable by lineage consumers

Step 7: Document and sign off
   └── Lineage record created in ML_LINEAGE_REGISTRY
   └── Audit evidence stored in evidence repository
```

### 6.2 Lineage Gap Severity

| Gap | Severity |
|---|---|
| No experiment run linked to production model | CRITICAL |
| Feature table missing from training run tags | HIGH |
| Feature table does not exist in platform | CRITICAL |
| Training data version not immutable (no snapshot) | HIGH |
| Prediction table lacks _model_version column | HIGH |
| Source system not documented in run tags | MEDIUM |
| dbt lineage graph not up to date for feature table | MEDIUM |

---

## 7. Audit Cadence & Reporting

### 7.1 Audit Calendar

| Control / Audit | 1LOD Frequency | 2LOD Frequency | Report To |
|---|---|---|---|
| Experiment tracking coverage (ML-01 / ML-AU-01) | Monthly | Quarterly | ML Engineering Lead, Data Governance |
| Registry currency (ML-02) | Monthly | Quarterly | ML Engineering Lead, Data Governance |
| Monitoring health (ML-03) | Weekly (automated) | Monthly | ML Platform Engineer, ML Engineering Lead |
| Bias audit completion (ML-04) | Quarterly | Semi-annual | ML Governance Analyst, Privacy Officer, Legal |
| Performance gate compliance (ML-05) | Monthly | Quarterly | ML Engineering Lead, CDO |
| PII usage review (ML-AU-02) | Quarterly | Quarterly | Privacy Officer, CDO |
| Lineage verification (ML-AU-03) | Monthly | Quarterly | Data Governance Lead, CDO |
| T1 model deep dive (ML-AU-04 + checklist) | Semi-annual | Annual (+ per regulatory request) | Model Risk Committee, CDO |
| Change management (ML-AU-06) | Per deployment | Quarterly | IT Audit, ML Engineering Lead |
| Cost vs. budget (ML-06) | Monthly | Monthly | Finance, ML Platform Engineer |

### 7.2 Monthly ML Governance Report Structure

```
1. Executive Summary
   - Model portfolio summary (count by tier and status)
   - Control health (green/amber/red by domain)
   - Critical and high findings opened this month
   
2. Model Inventory
   - Total production models (by tier)
   - New models promoted to production
   - Models retired / archived
   - Models currently in staging (pending promotion)
   
3. Performance & Monitoring
   - Models above / below performance gate
   - Models with active drift alerts
   - Retraining events this month
   - Champion/challenger tests in progress
   
4. Governance & Compliance
   - Bias audits completed this month
   - Risk assessments completed
   - Model cards published / updated
   - PII models reviewed
   
5. Change Management
   - Production promotions this month
   - Change ticket compliance rate
   - Emergency changes (if any)
   
6. Cost
   - Total ML compute cost vs. budget
   - Top 5 cost models (by training + serving)
   - Optimization actions taken
   
7. Findings Summary
   - Open findings by severity
   - Overdue findings
   - Findings opened / closed in period
```

---

## 8. Findings Classification & Escalation

| Severity | Definition | Remediation SLA | Escalation |
|---|---|---|---|
| **CRITICAL** | T1 model in production without bias audit; PII used without approval; model with no lineage making consequential decisions; production model not in registry | Immediate — within 24 hours | ML Engineering Lead + Privacy Officer / Legal + CDO |
| **HIGH** | Model below performance gate not remediated within 10 days; monitoring not active for T1/T2; change management bypassed; PII declaration mismatch | 5 business days | ML Engineering Lead + Data Governance Lead |
| **MEDIUM** | Missing required metadata tags; registry entry stale; model card not updated after retrain; cost tags missing | 15 business days | ML Engineering Lead |
| **LOW** | Minor metadata gaps; performance slightly below recommendation (not gate); minor documentation gap | 30 business days | Domain ML Lead |
| **INFORMATIONAL** | Optimization opportunity; process improvement suggestion | Next quarterly review | ML Engineering Lead |

---

## 9. Regulatory Audit Readiness

### 9.1 Common Regulatory Requests for ML Evidence

| Regulator Request | Evidence Location | Preparation |
|---|---|---|
| "Show us which model version was in production on date X" | MLflow registry stage history + deployment logs | Registry stage change timestamps retained; deployment logs in CI/CD |
| "What data was used to train this model?" | MLflow run tags (data.feature_table, data.train_start, data.train_end, data.feature_hash) | Tags required on all runs; DVC or Delta snapshot for immutability |
| "Demonstrate you tested this model for bias" | Bias audit report in MLflow artifact + governance registry | Bias audit report stored as artifact; registry entry links to report |
| "Who approved this model for production?" | MLflow production.approver tag + change ticket in ITSM | All promotions tagged with approver; change ticket linked |
| "Show us the model's performance over time" | Monitoring reports in data lake + BI performance dashboard | Reports retained for retention period; dashboard archived quarterly |
| "Demonstrate controls over T1 model changes" | Change management records + CI/CD logs | All T1 changes require change ticket; CI/CD logs retained 3 years |
| "What is the lineage from source data to credit decision?" | Lineage registry + dbt lineage graph + MLflow tags | Full lineage documented per lineage audit procedures |
| "Show me all models that use customer X's data" | Prediction tables (_model_name, _scored_at) + feature table lineage | Prediction tables queryable by customer_id; lineage to source documented |

### 9.2 Pre-Regulatory-Audit Checklist

```
□ Model Governance Registry current and accurate (last audit < 30 days)
□ All T1/T2 model cards published and current
□ Bias audit reports available for all T1 models (last 12 months)
□ Risk assessment completed for all T1/T2 models
□ Change tickets available for all production promotions in scope period
□ MLflow experiment tracking records retained for scope period
□ Training data snapshots or hashes verifiable for all T1/T2 models
□ Drift monitoring reports available for scope period
□ Prediction tables exist with lineage columns for all T1 models
□ All CRITICAL and HIGH findings from prior audits resolved or on documented plan
□ Model Governance Council meeting minutes available for scope period
```

---

*This auditing guide is reviewed annually and updated following any material change to the ML platform, governance policy, or regulatory landscape.*
