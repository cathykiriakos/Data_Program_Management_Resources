# Machine Learning KPIs, Benchmarking & Scorecard
## MLflow | Snowflake ML | Databricks | SageMaker

**Document Owner:** Chief Data Office
**Domain:** Machine Learning
**Version:** 1.0
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [KPI Framework Overview](#1-kpi-framework-overview)
2. [Full KPI Registry](#2-full-kpi-registry)
3. [ML Scorecard — Monthly Template](#3-ml-scorecard--monthly-template)
4. [KPI Data Collection — Python Pattern](#4-kpi-data-collection--python-pattern)
5. [YAML Configuration — KPI Definitions](#5-yaml-configuration--kpi-definitions)
6. [Benchmarking Reference](#6-benchmarking-reference)
7. [Maturity-Gated KPI Targets](#7-maturity-gated-kpi-targets)

---

## 1. KPI Framework Overview

Machine Learning KPIs are organized into four perspectives aligned to a **ML Balanced Scorecard**:

```
┌──────────────────────┐    ┌──────────────────────┐
│  MODEL GOVERNANCE    │    │  MODEL PERFORMANCE    │
│  Are models tracked, │    │  Are models accurate, │
│  registered & owned? │    │  current & healthy?   │
└──────────────────────┘    └──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  OPERATIONS &        │    │  RISK &               │
│  RELIABILITY         │    │  COMPLIANCE           │
│  Are ML systems      │    │  Are models safe,     │
│  stable & governed?  │    │  fair & auditable?    │
└──────────────────────┘    └──────────────────────┘
```

### 1.1 KPI Ownership Model

| Perspective | Primary Owner | Reporting Cadence | Audience |
|---|---|---|---|
| Model Governance | ML Governance Analyst | Monthly | CDO, Model Risk |
| Model Performance | Domain ML Leads | Monthly | CDO, Business Owners |
| Operations & Reliability | ML Platform Engineer | Monthly | ML COE Lead, CDO |
| Risk & Compliance | ML Governance Analyst + Model Risk | Monthly | CDO, Risk Committee |

### 1.2 Model Tier Reference

All ML KPIs are applied with reference to model risk tiers:

| Tier | Description | Examples | Regulatory Scrutiny |
|---|---|---|---|
| **T1** | High-risk / regulated decisions | Credit scoring, fraud, AML, medical | Highest — model validation required |
| **T2** | Business-critical, non-regulated | Revenue forecasting, churn, demand planning | High — governance required |
| **T3** | Operational / automation | Content recommendation, search ranking | Standard |
| **T4** | Experimental / sandbox | Prototypes, R&D models | Minimal |

---

## 2. Full KPI Registry

### 2.1 Model Governance KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| MG-ML-01 | Model Registry Coverage | Production models in registry / Total production models detected | 100% | Monthly | MLflow API |
| MG-ML-02 | Model Card Completeness — T1 | T1 models with complete model cards / Total T1 production models | 100% | Monthly | MLflow artifacts |
| MG-ML-03 | Model Card Completeness — T2 | T2 models with complete model cards / Total T2 production models | 100% | Monthly | MLflow artifacts |
| MG-ML-04 | Model Ownership Coverage | Production models with named owner / Total production models | 100% | Monthly | Model Registry YAML |
| MG-ML-05 | Experiment Tracking Coverage | Experiments with MLflow tracking / Total experiments run | ≥ 95% | Monthly | MLflow API |
| MG-ML-06 | Feature Lineage Coverage | Production models with feature store lineage / Total | ≥ 90% | Monthly | Feature store + registry |
| MG-ML-07 | Retraining Schedule Coverage | Production models with defined retraining trigger / Total | 100% | Monthly | Model Registry YAML |
| MG-ML-08 | Model Retirement Compliance | Deprecated models removed from serving within SLA / Total | 100% | Monthly | Registry + serving layer |
| MG-ML-09 | Stale Model Rate | Production models without a refresh or review in 90+ days | 0% (T1/T2), < 10% (T3) | Monthly | MLflow API |

### 2.2 Model Performance KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| MP-ML-01 | T1 Performance Gate Compliance | T1 models meeting all defined performance gates / Total T1 | 100% | Monthly | MLflow metrics |
| MP-ML-02 | T2 Performance Gate Compliance | T2 models meeting all defined performance gates / Total T2 | ≥ 95% | Monthly | MLflow metrics |
| MP-ML-03 | Feature Drift Incidents — T1 | T1 models with detected feature drift not remediated within SLA | 0 | Weekly | Monitoring store |
| MP-ML-04 | Feature Drift Incidents — T2 | T2 models with detected feature drift not remediated within SLA | < 2 | Monthly | Monitoring store |
| MP-ML-05 | Prediction Volume Anomaly Rate | Models with prediction volume > 2σ from baseline / Total | < 5% | Daily | Serving logs |
| MP-ML-06 | Model Accuracy Degradation (T1) | T1 models with > 3pp accuracy drop from baseline | 0 | Monthly | Evaluation pipeline |
| MP-ML-07 | Monitoring Coverage — T1 | T1 models with active drift monitoring / Total T1 | 100% | Monthly | Monitoring config |
| MP-ML-08 | Monitoring Coverage — T2 | T2 models with active drift monitoring / Total T2 | 100% | Monthly | Monitoring config |
| MP-ML-09 | Labeled Outcome Feedback Rate | Production models with actuals feedback loop / Total (where applicable) | ≥ 70% | Monthly | Data pipeline |

### 2.3 Operations & Reliability KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| OR-ML-01 | Model Serving Availability (T1) | Uptime / Total time for T1 serving endpoints | ≥ 99.9% | Monthly | Serving infrastructure |
| OR-ML-02 | Model Serving Availability (T2) | Uptime / Total time for T2 serving endpoints | ≥ 99.5% | Monthly | Serving infrastructure |
| OR-ML-03 | Inference Latency P95 (T1) | 95th percentile latency for T1 real-time serving | Per model SLA | Monthly | Serving telemetry |
| OR-ML-04 | Model Deployment Lead Time (T1) | Days from code-complete to production promotion | < 10 days | Per deployment | MLflow + CI/CD |
| OR-ML-05 | Model Deployment Lead Time (T2/T3) | Days from code-complete to production promotion | < 5 days | Per deployment | MLflow + CI/CD |
| OR-ML-06 | Retraining Pipeline Failure Rate | Failed retraining runs / Total scheduled retraining runs | < 3% | Monthly | Pipeline run log |
| OR-ML-07 | Change Management Compliance | T1 promotions with approved change ticket / Total T1 promotions | 100% | Monthly | ITSM + MLflow tags |
| OR-ML-08 | MTTD — Model Degradation | Avg days from degradation start to detection | < 7 days (T1), < 14 days (T2) | Per incident | Incident log |
| OR-ML-09 | MTTR — Model Incident | Avg days from degradation detection to resolution | < 2 days (T1), < 5 days (T2) | Per incident | Incident log |
| OR-ML-10 | Feature Store SLA Compliance | Feature pipelines meeting freshness SLA / Total | ≥ 98% | Daily | Feature store |

### 2.4 Risk & Compliance KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| RC-ML-01 | T1 Model Validation Completion | T1 models with completed independent validation / Total T1 | 100% | Semi-annual | Model Risk |
| RC-ML-02 | Bias Audit Completion — T1 | T1 models with completed bias audit / Total T1 | 100% | Semi-annual | Model Risk |
| RC-ML-03 | Bias Audit Completion — T2 | T2 models with completed bias audit / Total T2 | ≥ 80% | Annual | ML Governance |
| RC-ML-04 | PII in Training Data Violations | Models using unauthorized PII in training data | 0 | Per review | Privacy Officer |
| RC-ML-05 | ML Compute Budget Variance | Actual ML compute cost / Budgeted ML compute cost | ≤ 110% | Monthly | Cloud billing |
| RC-ML-06 | Untagged ML Compute Spend | ML compute without cost center tags / Total ML compute | 0% | Monthly | Cloud billing |
| RC-ML-07 | Open High/Critical Risk Findings | Unresolved High or Critical model risk findings | 0 (Critical), < 3 (High) | Monthly | Risk register |
| RC-ML-08 | Model Explainability Coverage — T1 | T1 models with documented explainability approach / Total T1 | 100% | Monthly | Model cards |
| RC-ML-09 | Regulatory Model Submission SLA | Regulatory model submissions on time / Total required | 100% | Per event | Model Risk |

---

## 3. ML Scorecard — Monthly Template

```markdown
# Machine Learning Scorecard — [Month YYYY]

## Overall Program Health: [X.X / 5.0] (↑/→/↓ from prior month)

| Perspective | Score | Trend | Status |
|---|---|---|---|
| Model Governance | X% | ↑ | 🟢 On Track |
| Model Performance | X% | → | 🟡 At Risk |
| Operations & Reliability | X% | ↑ | 🟢 On Track |
| Risk & Compliance | X% | ↓ | 🔴 Off Track |

---

## Model Governance

| KPI | Target | Actual | Status |
|---|---|---|---|
| MG-ML-01 Registry Coverage | 100% | X% | 🟢/🔴 |
| MG-ML-02 Model Card — T1 | 100% | X% | 🟢/🔴 |
| MG-ML-04 Ownership Coverage | 100% | X% | 🟢/🔴 |
| MG-ML-07 Retraining Schedule | 100% | X% | 🟢/🔴 |
| MG-ML-09 Stale Model Rate (T1/T2) | 0% | X% | 🟢/🔴 |

## Model Performance

| KPI | Target | Actual | Status |
|---|---|---|---|
| MP-ML-01 T1 Gate Compliance | 100% | X% | 🟢/🔴 |
| MP-ML-02 T2 Gate Compliance | ≥95% | X% | 🟢/🔴 |
| MP-ML-03 T1 Drift Incidents | 0 | X | 🟢/🔴 |
| MP-ML-06 T1 Accuracy Degradation | 0 | X | 🟢/🔴 |
| MP-ML-07 T1 Monitoring Coverage | 100% | X% | 🟢/🔴 |

## Operations & Reliability

| KPI | Target | Actual | Status |
|---|---|---|---|
| OR-ML-01 T1 Serving Availability | ≥99.9% | X% | 🟢/🔴 |
| OR-ML-07 Change Mgmt Compliance | 100% | X% | 🟢/🔴 |
| OR-ML-08 MTTD — T1 Degradation | <7 days | X days | 🟢/🔴 |
| OR-ML-09 MTTR — T1 Incident | <2 days | X days | 🟢/🔴 |
| OR-ML-10 Feature Store SLA | ≥98% | X% | 🟢/🔴 |

## Risk & Compliance

| KPI | Target | Actual | Status |
|---|---|---|---|
| RC-ML-01 T1 Validation Complete | 100% | X% | 🟢/🔴 |
| RC-ML-02 T1 Bias Audit | 100% | X% | 🟢/🔴 |
| RC-ML-04 PII Violations | 0 | X | 🟢/🔴 |
| RC-ML-07 Open Critical Findings | 0 | X | 🟢/🔴 |
| RC-ML-08 T1 Explainability | 100% | X% | 🟢/🔴 |

---

## Model Inventory Summary
| Tier | Total in Production | Healthy | Drifting | Under Review |
|---|---|---|---|---|
| T1 | X | X | X | X |
| T2 | X | X | X | X |
| T3 | X | X | X | X |

## Incidents This Month
| Incident ID | Model | Tier | Type | Duration | Status |
|---|---|---|---|---|---|
| INC-XXX | [model name] | T1/T2 | Drift/Failure/PII | X days | Resolved/Open |

## Top 3 Risks
1. [Risk] — Owner: [name] — Due: [date]
2. [Risk] — Owner: [name] — Due: [date]
3. [Risk] — Owner: [name] — Due: [date]

## Remediation Actions
| Finding | Model | Owner | Due | Status |
|---|---|---|---|---|
| [finding] | [model] | [name] | [date] | Open/In Progress/Closed |
```

---

## 4. KPI Data Collection — Python Pattern

ML KPI data is sourced from three systems:
- **MLflow API** — model registry, experiment tracking, performance metrics, governance YAML tags
- **Snowflake** — feature store SLA, serving logs, cost data, outcome feedback
- **Monitoring Store** — drift detection results, prediction volume anomalies

```python
# ml_kpi_collector.py
"""
Config-driven KPI collection for the Machine Learning program.
Collects from MLflow API, Snowflake, and the ML monitoring store.
Follows the class-based, YAML-injected pattern.
"""

import yaml
import os
import pandas as pd
import snowflake.connector
import requests
from datetime import datetime, date
from dataclasses import dataclass
from typing import Any
from mlflow.tracking import MlflowClient


@dataclass
class KPIResult:
    run_date: date
    kpi_id: str
    kpi_name: str
    perspective: str
    source: str
    actual: Any
    target: Any
    target_operator: str
    unit: str
    status: str
    frequency: str
    notes: str = ""

    def to_dict(self) -> dict:
        return self.__dict__


class MLKPICollector:
    """
    Collects Machine Learning KPIs from MLflow, Snowflake, and the monitoring store.
    Scheduled monthly via Airflow or Databricks Workflows.
    All queries and targets externalized to YAML.
    """

    def __init__(
        self,
        config_path: str,
        snowflake_conn_params: dict,
        mlflow_tracking_uri: str,
    ):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.sf_conn = snowflake.connector.connect(**snowflake_conn_params)
        self.mlflow_client = MlflowClient(tracking_uri=mlflow_tracking_uri)
        self.run_date = datetime.utcnow().date()

    # ── Public API ────────────────────────────────────────────────

    def collect_all(self, perspectives: list[str] | None = None) -> pd.DataFrame:
        results = []
        for kpi in self.config["kpis"]:
            if perspectives and kpi["perspective"] not in perspectives:
                continue
            try:
                result = self._dispatch(kpi)
            except Exception as e:
                result = self._build_result(kpi, actual=None, notes=f"Collection error: {e}")
            results.append(result.to_dict())
        return pd.DataFrame(results)

    def save_results(self, df: pd.DataFrame, target_table: str = "machine_learning.kpis.results") -> None:
        cursor = self.sf_conn.cursor()
        for _, row in df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO {target_table}
                    (run_date, kpi_id, kpi_name, perspective, source, actual, target,
                     target_operator, unit, status, frequency, notes)
                VALUES
                    (%(run_date)s, %(kpi_id)s, %(kpi_name)s, %(perspective)s, %(source)s,
                     %(actual)s, %(target)s, %(target_operator)s, %(unit)s, %(status)s,
                     %(frequency)s, %(notes)s)
                """,
                row.to_dict(),
            )

    # ── Dispatch ──────────────────────────────────────────────────

    def _dispatch(self, kpi: dict) -> KPIResult:
        source = kpi.get("source", "snowflake")
        if source == "snowflake":
            return self._collect_snowflake(kpi)
        elif source == "mlflow":
            return self._collect_mlflow(kpi)
        else:
            raise ValueError(f"Unknown source type: {source}")

    # ── Collectors ────────────────────────────────────────────────

    def _collect_snowflake(self, kpi: dict) -> KPIResult:
        cursor = self.sf_conn.cursor()
        cursor.execute(kpi["query"])
        row = cursor.fetchone()
        actual = float(row[0]) if row and row[0] is not None else None
        return self._build_result(kpi, actual)

    def _collect_mlflow(self, kpi: dict) -> KPIResult:
        """
        Evaluate a KPI using the MLflow Python client.
        The YAML 'mlflow_method' field maps to a method on this collector.
        """
        method_name = kpi.get("mlflow_method")
        if not method_name:
            return self._build_result(kpi, actual=None, notes="No mlflow_method defined")

        method = getattr(self, f"_mlflow_{method_name}", None)
        if not method:
            return self._build_result(kpi, actual=None, notes=f"Unknown mlflow_method: {method_name}")

        actual = method(kpi)
        return self._build_result(kpi, actual)

    # ── MLflow Method Implementations ─────────────────────────────

    def _mlflow_registry_coverage(self, kpi: dict) -> float:
        """
        Compare models in Production stage against the governance YAML registry.
        Coverage = registered in both / total detected in Production stage.
        """
        production_models = {
            mv.name
            for mv in self.mlflow_client.search_model_versions("tags.stage = 'production'")
        }
        registered_models = {
            mv.name
            for mv in self.mlflow_client.search_model_versions("tags.governance_registered = 'true'")
            if mv.current_stage == "Production"
        }
        if not production_models:
            return 1.0  # No models = 100% (vacuously true)
        return len(registered_models & production_models) / len(production_models)

    def _mlflow_model_card_completeness(self, kpi: dict) -> float:
        """
        Check what fraction of T1 (or T2) production models have a complete model card.
        A model card is considered complete if the required_tags are all present.
        """
        tier = kpi.get("model_tier", "T1")
        required_tags = kpi.get("required_tags", [
            "governance.model_card_version",
            "governance.owner",
            "governance.risk_tier",
            "governance.last_bias_audit_date",
            "governance.explainability_approach",
        ])

        production_models = self.mlflow_client.search_model_versions(
            f"tags.stage = 'production' and tags.governance.risk_tier = '{tier}'"
        )
        if not production_models:
            return 1.0

        complete = sum(
            1 for mv in production_models
            if all(tag in mv.tags for tag in required_tags)
        )
        return complete / len(production_models)

    def _mlflow_stale_model_rate(self, kpi: dict) -> float:
        """
        Fraction of T1/T2 production models not refreshed or reviewed in 90+ days.
        """
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=90)
        tiers = kpi.get("model_tiers", ["T1", "T2"])

        models = []
        for tier in tiers:
            models.extend(self.mlflow_client.search_model_versions(
                f"tags.stage = 'production' and tags.governance.risk_tier = '{tier}'"
            ))

        if not models:
            return 0.0

        stale = sum(
            1 for mv in models
            if self._last_activity(mv) < cutoff
        )
        return stale / len(models)

    def _last_activity(self, model_version) -> datetime:
        """Return the most recent activity date for a model version."""
        last_updated = datetime.utcfromtimestamp(model_version.last_updated_timestamp / 1000)
        return last_updated

    # ── Helpers ───────────────────────────────────────────────────

    def _build_result(self, kpi: dict, actual: Any, notes: str = "") -> KPIResult:
        status = self._evaluate_status(actual, kpi)
        return KPIResult(
            run_date=self.run_date,
            kpi_id=kpi["kpi_id"],
            kpi_name=kpi["name"],
            perspective=kpi["perspective"],
            source=kpi.get("source", "snowflake"),
            actual=actual,
            target=kpi["target"],
            target_operator=kpi["target_operator"],
            unit=kpi.get("unit", "count"),
            status=status,
            frequency=kpi["frequency"],
            notes=notes,
        )

    def _evaluate_status(self, actual: Any, kpi: dict) -> str:
        if actual is None:
            return "NO_DATA"
        target = kpi["target"]
        op = kpi["target_operator"]
        amber_threshold = kpi.get("amber_threshold")
        if op == "gte":
            ok = actual >= target
            amber = amber_threshold and actual >= amber_threshold and not ok
        elif op == "lte":
            ok = actual <= target
            amber = amber_threshold and actual <= amber_threshold and not ok
        elif op == "eq":
            ok = actual == target
            amber = False
        else:
            ok = False
            amber = False
        if ok:
            return "GREEN"
        elif amber:
            return "AMBER"
        return "RED"


# ── DDL: Results Table ────────────────────────────────────────────────────────

CREATE_KPI_RESULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS machine_learning.kpis.results (
    run_date          DATE          NOT NULL,
    kpi_id            VARCHAR(30)   NOT NULL,
    kpi_name          VARCHAR(200)  NOT NULL,
    perspective       VARCHAR(50)   NOT NULL,
    source            VARCHAR(50),
    actual            FLOAT,
    target            FLOAT,
    target_operator   VARCHAR(10),
    unit              VARCHAR(30),
    status            VARCHAR(10),
    frequency         VARCHAR(20),
    notes             VARCHAR(500),
    inserted_at       TIMESTAMP_TZ  DEFAULT CURRENT_TIMESTAMP()
);
"""
```

---

## 5. YAML Configuration — KPI Definitions

```yaml
# config/kpis/ml_kpis_config.yaml

kpis:

  # ── Model Governance ──────────────────────────────────────────────────────

  - kpi_id: "MG-ML-01"
    name: "Model Registry Coverage"
    perspective: "model_governance"
    source: "mlflow"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    mlflow_method: "registry_coverage"

  - kpi_id: "MG-ML-02"
    name: "Model Card Completeness — T1"
    perspective: "model_governance"
    source: "mlflow"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    mlflow_method: "model_card_completeness"
    model_tier: "T1"
    required_tags:
      - "governance.model_card_version"
      - "governance.owner"
      - "governance.risk_tier"
      - "governance.last_bias_audit_date"
      - "governance.explainability_approach"
      - "governance.last_validation_date"

  - kpi_id: "MG-ML-09"
    name: "Stale Model Rate — T1/T2"
    perspective: "model_governance"
    source: "mlflow"
    frequency: "monthly"
    unit: "percentage"
    target: 0.0
    target_operator: "lte"
    mlflow_method: "stale_model_rate"
    model_tiers: ["T1", "T2"]

  # ── Model Performance ─────────────────────────────────────────────────────

  - kpi_id: "MP-ML-01"
    name: "T1 Performance Gate Compliance"
    perspective: "model_performance"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    amber_threshold: 0.95
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN meets_all_gates THEN 1 END)::FLOAT
        / NULLIF(COUNT(*), 0)
      FROM machine_learning.governance.model_gate_evaluation
      WHERE risk_tier = 'T1'
        AND eval_date = (SELECT MAX(eval_date) FROM machine_learning.governance.model_gate_evaluation)
        AND is_production = TRUE

  - kpi_id: "MP-ML-03"
    name: "Feature Drift Incidents — T1 (unresolved)"
    perspective: "model_performance"
    source: "snowflake"
    frequency: "weekly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(DISTINCT model_name)
      FROM machine_learning.monitoring.drift_incidents
      WHERE risk_tier = 'T1'
        AND resolved = FALSE
        AND detected_at < DATEADD('day', -3, CURRENT_TIMESTAMP())

  # ── Operations & Reliability ──────────────────────────────────────────────

  - kpi_id: "OR-ML-01"
    name: "T1 Model Serving Availability"
    perspective: "operations_reliability"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 0.999
    amber_threshold: 0.998
    target_operator: "gte"
    query: |
      SELECT
        SUM(available_minutes)::FLOAT / SUM(total_minutes)
      FROM machine_learning.monitoring.serving_availability
      WHERE risk_tier = 'T1'
        AND measurement_month = DATE_TRUNC('month', CURRENT_DATE() - 1)

  - kpi_id: "OR-ML-07"
    name: "T1 Change Management Compliance"
    perspective: "operations_reliability"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN change_ticket_id IS NOT NULL AND ticket_approved THEN 1 END)::FLOAT
        / NULLIF(COUNT(*), 0)
      FROM machine_learning.governance.production_promotions
      WHERE risk_tier = 'T1'
        AND promoted_at >= DATE_TRUNC('month', CURRENT_DATE() - 1)

  # ── Risk & Compliance ─────────────────────────────────────────────────────

  - kpi_id: "RC-ML-04"
    name: "PII in Training Data Violations"
    perspective: "risk_compliance"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(*)
      FROM machine_learning.governance.data_usage_review
      WHERE pii_violation_confirmed = TRUE
        AND review_date >= DATE_TRUNC('month', CURRENT_DATE() - 1)

  - kpi_id: "RC-ML-05"
    name: "ML Compute Budget Variance"
    perspective: "risk_compliance"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.10
    amber_threshold: 1.05
    target_operator: "lte"
    query: |
      SELECT actual_cost / NULLIF(budgeted_cost, 0)
      FROM machine_learning.finance.monthly_compute_budget
      WHERE budget_month = DATE_TRUNC('month', CURRENT_DATE() - 1)

  - kpi_id: "RC-ML-07"
    name: "Open Critical Risk Findings"
    perspective: "risk_compliance"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(*)
      FROM machine_learning.governance.risk_findings
      WHERE severity = 'CRITICAL'
        AND status NOT IN ('CLOSED', 'ACCEPTED')
```

---

## 6. Benchmarking Reference

| KPI | Early Stage (Yr 1) | Developing (Yr 2) | Mature (Yr 3+) | Best-in-Class |
|---|---|---|---|---|
| Model Registry Coverage | ≥ 50% | ≥ 80% | 100% | 100% |
| T1 Model Card Completeness | ≥ 60% | ≥ 85% | 100% | 100% |
| T1 Performance Gate Compliance | ≥ 70% | ≥ 90% | 100% | 100% |
| T1 Serving Availability | ≥ 99% | ≥ 99.5% | ≥ 99.9% | 99.99% |
| T1 Monitoring Coverage | ≥ 50% | ≥ 80% | 100% | 100% |
| MTTD — T1 Model Degradation | < 30 days | < 14 days | < 7 days | < 2 days |
| MTTR — T1 Incident | < 10 days | < 5 days | < 2 days | < 1 day |
| T1 Bias Audit Completion | ≥ 50% | ≥ 80% | 100% | 100% |
| PII Violations | < 3/yr | < 1/yr | 0 | 0 |
| Change Mgmt Compliance (T1) | ≥ 70% | ≥ 90% | 100% | 100% |

---

## 7. Maturity-Gated KPI Targets

| Maturity Level | Registry Coverage | T1 Card Complete | T1 Monitoring | T1 Serving SLA | PII Violations |
|---|---|---|---|---|---|
| **Level 1 — Ad Hoc** | No target | No target | No target | Baseline | No target |
| **Level 2 — Managed** | ≥ 60% | ≥ 60% | ≥ 50% | ≥ 99% | < 3/yr |
| **Level 3 — Defined** | ≥ 90% | ≥ 90% | ≥ 90% | ≥ 99.5% | 0 |
| **Level 4 — Optimized** | 100% | 100% | 100% | ≥ 99.9% | 0 |
| **Level 5 — Leading** | 100% + lineage | 100% + explainability | 100% + predictive | 99.99% | 0 |

> **CDO Mandate:** All T1 (regulated/high-risk) models must operate at Level 3 KPI targets or above at all times. Failure to meet T1 targets for two consecutive months triggers a mandatory risk escalation to the Model Risk Committee.

---

*Document Owner: Chief Data Officer | Domain Lead: ML COE Lead | Review Cycle: Semi-Annual*
