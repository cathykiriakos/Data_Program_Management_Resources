# ML Configuration-Based Practices & Change Management
## MLOps | Model Lifecycle | IT Change Management Integration

**Document Owner:** Chief Data Office  
**Domain:** Machine Learning  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Config-First MLOps Architecture](#1-config-first-mlops-architecture)
2. [Model Configuration Standards](#2-model-configuration-standards)
3. [Training Pipeline Configuration](#3-training-pipeline-configuration)
4. [CI/CD for ML Models](#4-cicd-for-ml-models)
5. [Environment Promotion Workflows](#5-environment-promotion-workflows)
6. [IT Change Management Integration](#6-it-change-management-integration)
7. [Feature Store Configuration](#7-feature-store-configuration)
8. [Serving & Endpoint Configuration](#8-serving--endpoint-configuration)
9. [Monitoring Configuration as Code](#9-monitoring-configuration-as-code)
10. [Change Classification Reference](#10-change-classification-reference)

---

## 1. Config-First MLOps Architecture

### 1.1 Philosophy

Every value that differs between environments, model versions, or operational states must live in a config file — not in training code. This creates:

- **Reproducible training runs:** Any engineer can reproduce any historical run by checking out the config at that Git commit
- **IT-reviewable changes:** Change managers can review a config diff instead of Python code changes
- **Safe environment promotion:** The exact same code runs in dev/staging/prod; only config values change
- **Auditable configurations:** Every config change has a Git commit, author, and timestamp

### 1.2 Config Object Hierarchy

```
ml_config/
├── {domain}/
│   └── {model_name}/
│       ├── base_config.yaml         ← Shared defaults
│       ├── dev_config.yaml          ← Dev overrides
│       ├── staging_config.yaml      ← Staging overrides
│       ├── prod_config.yaml         ← Production values
│       └── gates_config.yaml        ← Performance gates (separate for auditability)
├── feature_store/
│   └── {domain}/
│       └── {feature_group}.yaml    ← Feature definitions
├── serving/
│   └── {endpoint_name}.yaml        ← Endpoint configuration
└── monitoring/
    └── {model_name}_monitor.yaml   ← Drift thresholds and alert config
```

---

## 2. Model Configuration Standards

### 2.1 Base Config Structure

```yaml
# ml_config/sales/customer_churn_predictor/base_config.yaml
# ------------------------------------------------------------------
# Model: customer_churn_predictor
# Owner: Sales ML Team | sales-ml@company.com
# Last Change: CHG-ML-2024-089
# ------------------------------------------------------------------

model:
  name: customer_churn_predictor
  version: "4.2.0"
  tier: T2                           # T1 | T2 | T3 | T4
  domain: sales
  use_case: "Predict 90-day customer churn probability"
  algorithm: gradient_boosting
  owner_team: sales-ml-team
  owner_email: sales-ml@company.com
  bias_audit_required: true
  explainability_method: shap
  risk_classification: MEDIUM
  prediction_type: binary_classification
  target_variable: is_churned_90d

data:
  train_start_date: "2022-01-01"
  train_end_date: "2023-12-31"
  pii_used: false
  features:
    - tenure_days
    - avg_monthly_spend_usd
    - support_tickets_90d
    - last_login_days_ago
    - plan_tier
    - contract_type
    - nps_score_last
  categorical_features:
    - plan_tier
    - contract_type
  target: is_churned_90d

training:
  test_size: 0.2
  random_state: 42
  stratify: true
  cross_val_folds: null            # null = use train/test split; set int for CV
  hyperparameters:
    n_estimators: 500
    max_depth: 6
    learning_rate: 0.05
    subsample: 0.8
    colsample_bytree: 0.8
    min_child_weight: 3
    gamma: 0.1

notifications:
  on_failure:
    - type: slack
      channel: "#ml-alerts-{{ env }}"
    - type: pagerduty
      severity: "{{ 'high' if env == 'prod' else 'low' }}"
  on_gate_failure:
    - type: slack
      channel: "#ml-alerts-{{ env }}"
  on_success:
    channels: []
```

### 2.2 Production Config (Environment Override)

```yaml
# ml_config/sales/customer_churn_predictor/prod_config.yaml
# Only values that DIFFER from base_config.yaml

model:
  environment: production

data:
  feature_table: "prod_sales_gold.ml.customer_features_v3"
  feature_table_version: "v3"
  snapshot_date: "2024-01-01"
  watermark_state: "s3://prod-ml-state/watermarks/churn_predictor.json"

mlflow:
  tracking_uri: "databricks"
  registry_uri: "databricks-uc"
  registry_model_name: "prod.sales.customer_churn_predictor"
  experiment_path: "/sales/customer_churn_predictor/prod"

compute:
  platform: databricks
  cluster_policy_id: "PROD_ML_POLICY_001"
  node_type: "m5d.2xlarge"
  min_workers: 2
  max_workers: 8
  spark_version: "15.4.x-scala2.12"
  job_cluster: true                    # Always job cluster in prod

serving:
  endpoint_name: "customer-churn-prod"
  compute_type: databricks_serverless
  scale_to_zero: false                 # T2 stays warm
  max_provisioned_throughput: 200
  latency_sla_ms: 200

scoring:
  mode: batch
  output_table: "prod_sales_gold.ml.predictions_churn"
  schedule: "0 3 * * *"               # 3 AM UTC daily
  batch_size: 10000
```

### 2.3 Performance Gates Config (Separate for Auditability)

```yaml
# ml_config/sales/customer_churn_predictor/gates_config.yaml
# Separate file so gate changes always have their own PR review
# Changes here require ML Engineering Lead + Data Governance sign-off

performance_gates:
  # Staging promotion gates
  staging:
    min_auc_roc: 0.78
    min_f1: 0.40
    min_precision_at_10pct: 0.60
    max_brier_score: 0.12

  # Production promotion gates (stricter)
  production:
    min_auc_roc: 0.80
    min_f1: 0.45
    min_precision_at_10pct: 0.65
    max_brier_score: 0.10
    must_beat_champion: true          # Challenger must beat current production model
    min_lift_over_champion_pct: 2.0   # By at least 2%

  # Degradation alert gates (post-deployment monitoring)
  monitoring:
    alert_if_auc_drops_below: 0.77
    critical_if_auc_drops_below: 0.72
    alert_if_relative_drop_pct: 5.0   # vs. launch baseline
    retrain_trigger_pct: 10.0         # Auto-trigger retraining

business_kpi_gate:
  metric: "intervention_retention_rate"
  minimum_acceptable_value: 0.25     # 25% retention rate in targeted cohort
  measurement_frequency: monthly
  review_owner: "VP Sales Operations"
```

---

## 3. Training Pipeline Configuration

### 3.1 Complete Config-Driven Trainer

```python
# ml/training/config_driven_trainer.py
"""
Production training pipeline — fully config driven.
No hardcoded values. Reads all configuration from YAML.
"""

from __future__ import annotations

import os
import yaml
import hashlib
import platform
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mlflow
import mlflow.xgboost
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score,
    brier_score_loss, average_precision_score
)
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
import shap

from ml.config.config_loader import load_ml_config
from ml.secrets.secrets_helper import get_secret
from ml.notifications.notifier import send_notification


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


class ConfigDrivenTrainer:
    """
    Fully config-driven ML training pipeline.
    Extend or compose this class for all model types.
    """

    def __init__(self, model_dir: str, env: str = "dev"):
        self.env = env
        self.config = load_ml_config(
            base_path=Path(model_dir) / "base_config.yaml",
            env_path=Path(model_dir) / f"{env}_config.yaml",
            gates_path=Path(model_dir) / "gates_config.yaml"
        )
        self.gates = self.config.get("performance_gates", {})
        self.logger = logging.getLogger(self.config["model"]["name"])

        # Set MLflow tracking
        mlflow.set_tracking_uri(self.config["mlflow"]["tracking_uri"])
        mlflow.set_experiment(self.config["mlflow"]["experiment_path"])

    # ── Data Loading ─────────────────────────────────────────────────

    def load_features(self) -> pd.DataFrame:
        """Load feature data from the configured feature table."""
        data_cfg = self.config["data"]
        self.logger.info(f"Loading features from: {data_cfg['feature_table']}")

        # Example: Snowflake connector (replace with Spark / pandas depending on platform)
        import snowflake.connector
        creds = get_secret(self.config.get("data_source_secret", f"{self.env}/snowflake/ml"))
        conn = snowflake.connector.connect(**creds)

        query = f"""
            SELECT {', '.join(data_cfg['features'] + [data_cfg['target']])}
            FROM {data_cfg['feature_table']}
            WHERE AS_OF_DATE BETWEEN '{data_cfg['train_start_date']}' AND '{data_cfg['train_end_date']}'
        """
        df = pd.read_sql(query, conn)
        conn.close()
        self.logger.info(f"Loaded {len(df):,} rows, {len(df.columns)} columns.")
        return df

    # ── Training ─────────────────────────────────────────────────────

    def build_pipeline(self) -> Pipeline:
        """Build sklearn Pipeline from config."""
        cfg = self.config
        cat_cols = cfg["data"].get("categorical_features", [])
        num_cols = [c for c in cfg["data"]["features"] if c not in cat_cols]
        hp = cfg["training"]["hyperparameters"]

        steps = []
        if cat_cols:
            steps.append(("encoder", OrdinalEncoder(
                categories="auto",
                handle_unknown="use_encoded_value",
                unknown_value=-1
            )))
        steps.append(("classifier", XGBClassifier(
            n_estimators=hp["n_estimators"],
            max_depth=hp["max_depth"],
            learning_rate=hp["learning_rate"],
            subsample=hp["subsample"],
            colsample_bytree=hp["colsample_bytree"],
            random_state=cfg["training"]["random_state"],
            eval_metric="logloss",
            tree_method="hist",
            enable_categorical=True if cat_cols else False
        )))
        return Pipeline(steps)

    # ── Evaluation ───────────────────────────────────────────────────

    def evaluate(
        self,
        pipeline: Pipeline,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> dict[str, float]:
        """Compute all standard classification metrics."""
        y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= 0.5).astype(int)
        threshold_pct = 0.1  # Top 10%

        # Precision at top-K%
        k = int(len(y_test) * threshold_pct)
        top_k_idx = np.argsort(y_pred_proba)[::-1][:k]
        precision_at_k = y_test.iloc[top_k_idx].mean()

        return {
            "auc_roc":            float(roc_auc_score(y_test, y_pred_proba)),
            "auc_pr":             float(average_precision_score(y_test, y_pred_proba)),
            "f1":                 float(f1_score(y_test, y_pred)),
            "precision":          float(precision_score(y_test, y_pred)),
            "recall":             float(recall_score(y_test, y_pred)),
            "brier_score":        float(brier_score_loss(y_test, y_pred_proba)),
            f"precision_at_{int(threshold_pct*100)}pct": float(precision_at_k),
            "positive_rate":      float(y_test.mean()),
            "n_test":             int(len(y_test)),
        }

    def check_performance_gates(self, metrics: dict, gate_level: str = "staging") -> list[str]:
        """Check metrics against configured gates. Returns list of failures."""
        gates = self.gates.get(gate_level, {})
        failures = []
        for gate_name, gate_val in gates.items():
            if gate_name.startswith("min_"):
                metric_name = gate_name[4:]
                if metric_name in metrics and metrics[metric_name] < gate_val:
                    failures.append(
                        f"{gate_name}: {metrics[metric_name]:.4f} < required {gate_val}"
                    )
            elif gate_name.startswith("max_"):
                metric_name = gate_name[4:]
                if metric_name in metrics and metrics[metric_name] > gate_val:
                    failures.append(
                        f"{gate_name}: {metrics[metric_name]:.4f} > allowed {gate_val}"
                    )
        return failures

    # ── SHAP Explainability ──────────────────────────────────────────

    def compute_shap(
        self,
        pipeline: Pipeline,
        X_sample: pd.DataFrame,
        run_id: str
    ) -> None:
        """Compute and log SHAP values as MLflow artifact."""
        if self.config["model"].get("explainability_method") != "shap":
            return

        self.logger.info("Computing SHAP values...")
        classifier = pipeline.named_steps["classifier"]
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(X_sample)

        # Global feature importance
        mean_abs_shap = pd.DataFrame({
            "feature": X_sample.columns,
            "mean_abs_shap": np.abs(shap_values).mean(axis=0)
        }).sort_values("mean_abs_shap", ascending=False)

        mlflow.log_dict(
            mean_abs_shap.to_dict(orient="records"),
            "explainability/global_feature_importance.json"
        )
        self.logger.info("SHAP values logged to MLflow.")

    # ── Main Run ─────────────────────────────────────────────────────

    def run(self) -> str:
        """Execute the full training run. Returns MLflow run_id."""
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            cfg = self.config

            # Log all parameters from config
            mlflow.log_params({
                **cfg["training"]["hyperparameters"],
                "test_size":    cfg["training"]["test_size"],
                "random_state": cfg["training"]["random_state"],
                "stratify":     cfg["training"]["stratify"],
            })

            # Required governance tags
            mlflow.set_tags({
                "model.name":               cfg["model"]["name"],
                "model.version":            cfg["model"]["version"],
                "model.tier":               cfg["model"]["tier"],
                "model.domain":             cfg["model"]["domain"],
                "model.owner_team":         cfg["model"]["owner_team"],
                "model.owner_email":        cfg["model"]["owner_email"],
                "model.risk_classification":cfg["model"]["risk_classification"],
                "model.explainability_method": cfg["model"]["explainability_method"],
                "data.feature_table":       cfg["data"]["feature_table"],
                "data.train_start":         cfg["data"]["train_start_date"],
                "data.train_end":           cfg["data"]["train_end_date"],
                "data.target":              cfg["data"]["target"],
                "governance.pii_used":      str(cfg["data"]["pii_used"]),
                "governance.bias_audit_required": str(cfg["model"]["bias_audit_required"]),
                "env.name":                 self.env,
                "env.python_version":       platform.python_version(),
                "git.commit":               os.environ.get("GIT_COMMIT_SHA", "unknown"),
                "git.branch":               os.environ.get("GIT_BRANCH", "unknown"),
            })

            # Load and profile data
            df = self.load_features()
            X = df[cfg["data"]["features"]]
            y = df[cfg["data"]["target"]]

            # Data profile
            mlflow.log_dict({
                "row_count":    int(len(df)),
                "feature_hash": hashlib.sha256(
                    "|".join(sorted(X.columns)).encode()
                ).hexdigest()[:16],
                "positive_rate": float(y.mean()),
                "snapshot_ts": datetime.now(timezone.utc).isoformat()
            }, "data_profile/profile.json")
            mlflow.log_param("data.row_count", len(df))

            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=cfg["training"]["test_size"],
                random_state=cfg["training"]["random_state"],
                stratify=y if cfg["training"]["stratify"] else None
            )
            mlflow.log_params({"train_rows": len(X_train), "test_rows": len(X_test)})

            # Train
            pipeline = self.build_pipeline()
            pipeline.fit(X_train, y_train)

            # Evaluate
            metrics = self.evaluate(pipeline, X_test, y_test)
            mlflow.log_metrics(metrics)
            self.logger.info(f"Metrics: {metrics}")

            # Gate check
            gate_failures = self.check_performance_gates(metrics, gate_level="staging")
            mlflow.log_dict(
                {"gate_failures": gate_failures, "gates_passed": len(gate_failures) == 0},
                "gates/gate_results.json"
            )

            # SHAP
            self.compute_shap(pipeline, X_test.sample(min(1000, len(X_test))), run_id)

            # Log model with signature
            from mlflow.models import infer_signature
            signature = infer_signature(X_train, pipeline.predict_proba(X_train)[:, 1])
            mlflow.sklearn.log_model(
                pipeline,
                artifact_path="model",
                signature=signature,
                registered_model_name=cfg["mlflow"]["registry_model_name"]
            )

            if gate_failures:
                self.logger.warning(f"Gate failures: {gate_failures}")
                send_notification(cfg["notifications"]["on_gate_failure"],
                                  message=f"Gate failures: {gate_failures}")
            else:
                self.logger.info("All performance gates passed.")

            return run_id
```

---

## 4. CI/CD for ML Models

### 4.1 Full ML CI/CD Pipeline

```yaml
# .github/workflows/ml_cicd.yml
name: ML Model CI/CD

on:
  pull_request:
    branches: [main]
    paths:
      - 'ml/**'
      - 'ml_config/**'
  push:
    branches: [main]
    paths:
      - 'ml/**'
      - 'ml_config/**'

env:
  PYTHON_VERSION: "3.11"

jobs:
  # ── 1. Validate Configuration ────────────────────────────────────
  validate-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install pyyaml jsonschema
      - name: Validate all model configs against schema
        run: python scripts/validate_ml_configs.py --dir ml_config/

  # ── 2. Security Scan ─────────────────────────────────────────────
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2

  # ── 3. Unit Tests ────────────────────────────────────────────────
  unit-tests:
    runs-on: ubuntu-latest
    needs: [validate-config, secret-scan]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements-dev.txt
      - run: pytest ml/tests/unit/ -v --cov=ml --cov-report=xml --cov-fail-under=70

  # ── 4. Integration Test on Staging ──────────────────────────────
  integration-test-staging:
    runs-on: ubuntu-latest
    needs: [unit-tests]
    if: github.event_name == 'pull_request'
    environment: staging
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements.txt
      - name: Run training pipeline on staging (smoke test)
        env:
          DATABRICKS_HOST:  ${{ secrets.DATABRICKS_STAGING_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_STAGING_TOKEN }}
          GIT_COMMIT_SHA:   ${{ github.sha }}
          GIT_BRANCH:       ${{ github.head_ref }}
        run: |
          python -m ml.training.config_driven_trainer \
            --model-dir ml_config/sales/customer_churn_predictor \
            --env staging
      - name: Verify performance gates on staging run
        run: python scripts/verify_staging_gates.py --model customer_churn_predictor --env staging

  # ── 5. Deploy Training Job to Production ────────────────────────
  deploy-production:
    runs-on: ubuntu-latest
    needs: [integration-test-staging]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: Deploy Databricks Job (update production training job definition)
        env:
          DATABRICKS_HOST:  ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_PROD_TOKEN }}
        run: |
          python scripts/deploy_databricks_job.py \
            --config ml_config/sales/customer_churn_predictor/prod_config.yaml \
            --env prod

  # ── 6. Post-Deployment Verification ─────────────────────────────
  verify-deployment:
    runs-on: ubuntu-latest
    needs: [deploy-production]
    steps:
      - uses: actions/checkout@v3
      - name: Verify production job is active and scheduled
        env:
          DATABRICKS_HOST:  ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_PROD_TOKEN }}
        run: python scripts/verify_prod_job.py --model customer_churn_predictor
```

---

## 5. Environment Promotion Workflows

### 5.1 Automated Staging Promotion

```python
# ml/lifecycle/auto_promote_staging.py
"""
Automatically promote a training run to Staging if all gates pass.
Called by CI/CD after staging training job completes.
"""

import mlflow
from mlflow.tracking import MlflowClient
from ml.lifecycle.model_lifecycle import ModelLifecycleManager
import json


def auto_promote_to_staging(
    run_id: str,
    model_name: str,
    gates_config_path: str,
    tracking_uri: str,
    promoter: str = "ci-cd-system"
) -> bool:
    """
    Promote a run to Staging if performance gates pass.
    Returns True if promoted, False if gates failed.
    """
    import yaml
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    run = client.get_run(run_id)
    metrics = run.data.metrics

    with open(gates_config_path) as f:
        gates = yaml.safe_load(f)["performance_gates"]["staging"]

    failures = []
    for gate_name, gate_val in gates.items():
        if gate_name.startswith("min_"):
            metric = gate_name[4:]
            if metrics.get(metric, 0) < gate_val:
                failures.append(f"{gate_name}: {metrics.get(metric, 'N/A')} < {gate_val}")
        elif gate_name.startswith("max_"):
            metric = gate_name[4:]
            if metrics.get(metric, 999) > gate_val:
                failures.append(f"{gate_name}: {metrics.get(metric, 'N/A')} > {gate_val}")

    if failures:
        print(f"❌ Staging gate failures: {failures}")
        return False

    # Get the newly registered model version
    versions = client.search_model_versions(f"name='{model_name}' and run_id='{run_id}'")
    if not versions:
        print(f"No model version found for run_id {run_id}")
        return False

    version = versions[0].version

    manager = ModelLifecycleManager(tracking_uri)
    manager.promote_to_staging(
        model_name=model_name,
        version=version,
        run_id=run_id,
        validation_report_path=f"runs:/{run_id}/gates/gate_results.json",
        promoter=promoter
    )
    print(f"✅ Model {model_name} v{version} promoted to Staging.")
    return True
```

### 5.2 Production Promotion Gate Script

```python
# scripts/promote_to_production.py
"""
Script for human-triggered production promotion.
Requires: change ticket, approver identity, and (for T1/T2) CC results.
Called manually or via ITSM automation after change ticket approval.
"""

import argparse
import yaml
import mlflow
from ml.lifecycle.model_lifecycle import ModelLifecycleManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name",         required=True)
    parser.add_argument("--version",             required=True)
    parser.add_argument("--change-ticket",       required=True)
    parser.add_argument("--approver",            required=True)
    parser.add_argument("--tracking-uri",        required=True)
    parser.add_argument("--cc-results-path",     default=None,
                        help="Path to champion/challenger results JSON (T1/T2 required)")
    args = parser.parse_args()

    cc_results = None
    if args.cc_results_path:
        import json
        with open(args.cc_results_path) as f:
            cc_results = json.load(f)

    manager = ModelLifecycleManager(args.tracking_uri)
    manager.promote_to_production(
        model_name=args.model_name,
        version=args.version,
        approval_ticket=args.change_ticket,
        approver=args.approver,
        champion_challenger_results=cc_results
    )

if __name__ == "__main__":
    main()

# Usage:
# python scripts/promote_to_production.py \
#   --model-name prod.sales.customer_churn_predictor \
#   --version 12 \
#   --change-ticket CHG-ML-2024-089 \
#   --approver "ml-engineering-lead@company.com" \
#   --tracking-uri databricks \
#   --cc-results-path /tmp/cc_results.json
```

---

## 6. IT Change Management Integration

### 6.1 ML Change Classification

| Change Type | Tier | Lead Time | Approvers | CAB |
|---|---|---|---|---|
| T4 exploratory experiment (never production) | Self-service | Immediate | None | No |
| T3 model staging promotion | Standard | Same day | ML Engineering Lead | No |
| T3 model production promotion | Standard | 3 days | ML Engineering Lead | No |
| T2 model staging promotion | Standard | 3–5 days | ML Engineering Lead + domain owner | No |
| T2 model production promotion | Minor | 5–10 days | ML Engineering Lead + domain owner + business owner | No |
| T1 model staging promotion | Minor | 5–10 days | ML Engineering Lead + ML Governance Analyst | No |
| T1 model production promotion | Major | 10–15 days | ML Engineering Lead + domain owner + ML Governance + Legal (if regulated) + CDO | Yes (T1) |
| T1 model emergency rollback | Emergency | Immediate | ML Engineering Lead (verbal) | Retrospective |
| Serving endpoint scaling change | Minor | 3–5 days | ML Platform Engineer + ML Engineering Lead | No |
| Serving endpoint new deployment | Minor | 5 days | ML Engineering Lead | No |
| Feature store schema change (additive) | Minor | 5 days | ML Engineering Lead + DE Lead | No |
| Feature store schema change (breaking) | Major | 10–15 days | ML Engineering Lead + DE Lead + CDO + CAB | Yes |
| MLflow / Model Registry configuration change | Minor | 5 days | ML Engineering Lead + IT | No |
| ML platform infrastructure change | Major | 10–15 days | ML Engineering Lead + IT + InfoSec + CAB | Yes |
| Model monitoring threshold change (T1) | Minor | 5 days | ML Engineering Lead + ML Governance + Data Governance | No |
| Bias audit methodology change | Major | 10–15 days | ML Governance + Legal + CDO + CAB | Yes |
| Retraining trigger change (T1) | Minor | 5 days | ML Engineering Lead + domain owner | No |

### 6.2 ML Change Request Template — Minor

```markdown
## ML Minor Change Request

**Ticket ID:** CHG-ML-YYYY-NNN
**Requestor:** [Name, Team]
**Date Submitted:** YYYY-MM-DD
**Target Deployment Date:** YYYY-MM-DD

### Change Summary
[Plain English: what is changing and why]

### Model / System Affected
- [ ] Model name and version:
- [ ] Model tier: T1 / T2 / T3
- [ ] Serving endpoint:
- [ ] Feature store:
- [ ] Training job:
- [ ] Monitoring configuration:

### Risk Assessment
- [ ] No change to training data or features
- [ ] No change to model algorithm
- [ ] No change to business logic / target variable
- [ ] PII impact: Yes / No
- [ ] Bias assessment needed: Yes / No (required for T1 any time features change)

### Validation Evidence (Staging)
- Staging run ID: ___________
- Staging AUC-ROC: ___ (gate: ___)
- Staging F1: ___ (gate: ___)
- Champion/Challenger results: PASS / N/A (required for T1/T2 production promotions)
- Champion/Challenger lift: ___ %

### Lineage Impact
- [ ] Feature table version unchanged
- [ ] New feature version: ___________
- [ ] Lineage registry updated: Yes / No

### Rollback Plan
[Step-by-step rollback. Must be executable in < 30 minutes]
[For model rollback: specify the prior version number to promote back to Production]

### Downstream Impact
- [ ] No downstream reports / dashboards affected
- [ ] Affected reports notified: Yes / No

### Approvals
- ML Engineering Lead: _____________ Date: _______
- Domain Business Owner: _____________ Date: _______
- ML Governance Analyst: _____________ Date: _______ (T1/T2 required)
```

---

## 7. Feature Store Configuration

### 7.1 Feature Group Definition as Code

```yaml
# ml_config/feature_store/sales/customer_features_v3.yaml
feature_group:
  name: customer_features
  version: v3
  domain: sales
  owner_team: sales-ml-team
  owner_email: sales-ml@company.com
  description: "Customer behavioral and account features for churn and propensity models"

platform:
  type: databricks_feature_store    # databricks_feature_store | feast | sagemaker | snowflake
  catalog: prod_sales_gold
  schema: ml
  table: customer_features_v3

primary_keys:
  - customer_id

timestamp_key: as_of_date

freshness:
  sla_hours: 24
  refresh_cron: "0 1 * * *"   # 1 AM UTC daily
  source_pipeline: "sales_feature_engineering_daily"

features:
  - name: tenure_days
    dtype: INTEGER
    description: "Days since customer account first activated"
    source_table: PROD_SALES_GOLD.sales.dim_customer
    derivation: "DATEDIFF('day', account_created_at, as_of_date)"
    pii: false
    nullable: false

  - name: avg_monthly_spend_usd
    dtype: FLOAT
    description: "Average monthly spend USD, trailing 6 complete months. NULL if <2 months."
    source_table: PROD_SALES_GOLD.sales.fact_revenue
    derivation: "AVG(monthly_revenue_usd) OVER (last 6 complete months)"
    pii: false
    nullable: true

  - name: support_tickets_90d
    dtype: INTEGER
    description: "Count of support tickets submitted in trailing 90 calendar days"
    source_table: PROD_OPERATIONS_GOLD.ops.fact_support_tickets
    derivation: "COUNT(*) WHERE created_at >= as_of_date - 90"
    pii: false
    nullable: false

governance:
  classification: INTERNAL
  pii_contains: false
  approved_model_tiers:
    - T1
    - T2
    - T3
  approved_since: "2024-01-01"
  next_review: "2025-01-01"
```

---

## 8. Serving & Endpoint Configuration

### 8.1 Endpoint Config as Code

```yaml
# ml_config/serving/customer-churn-prod.yaml
endpoint:
  name: customer-churn-prod
  description: "Customer churn probability score endpoint — Sales team"
  model_name: prod.sales.customer_churn_predictor
  model_stage: Production               # Always serve Production stage

platform:
  type: databricks_serverless           # databricks_serverless | sagemaker | fastapi_k8s
  
scaling:
  min_provisioned_throughput: 1         # Always warm (T2 model)
  max_provisioned_throughput: 200
  scale_to_zero_enabled: false

auth:
  type: token
  token_rotation_days: 90
  allowed_service_principals:
    - "svc-sales-scoring"
    - "svc-bi-recommendations"

performance:
  latency_sla_p50_ms: 100
  latency_sla_p99_ms: 200
  alert_if_p99_exceeds_ms: 300

logging:
  log_requests: true
  log_responses: true
  sampling_rate: 0.20                   # Log 20% of requests for monitoring
  log_destination: "prod_sales_gold.ml.endpoint_logs_churn"

governance:
  model_tier: T2
  classification: CONFIDENTIAL
  data_classification_of_inputs: INTERNAL
  approved_consumers:
    - "Sales Operations"
    - "Revenue Operations"

cost:
  cost_center: CC-1042
  monthly_budget_usd: 800
  alert_at_pct: 75
```

---

## 9. Monitoring Configuration as Code

```yaml
# ml_config/monitoring/customer_churn_predictor_monitor.yaml
monitor:
  model_name: prod.sales.customer_churn_predictor
  model_tier: T2
  monitor_type: databricks_lakehouse_monitoring  # databricks | evidently | sagemaker

reference:
  dataset: "prod_sales_gold.ml.customer_features_v3"
  snapshot_date: "2023-12-31"         # Training data end date (baseline)
  baseline_auc: 0.863                 # Production launch AUC

data_drift:
  enabled: true
  schedule: "0 8 * * *"              # 8 AM UTC daily
  features_to_monitor:
    - tenure_days
    - avg_monthly_spend_usd
    - support_tickets_90d
    - last_login_days_ago
  thresholds:
    psi_warning: 0.10
    psi_critical: 0.25
    share_drifted_warning_pct: 10
    share_drifted_critical_pct: 25
  alert_on_warning: false
  alert_on_critical: true

prediction_drift:
  enabled: true
  schedule: "0 9 * * *"
  thresholds:
    ks_statistic_warning: 0.05
    ks_statistic_critical: 0.10

model_performance:
  enabled: true                        # Requires labeled actuals
  label_table: "prod_sales_gold.sales.fact_churn_actuals"
  label_join_key: customer_id
  label_column: churned_90d
  label_delay_days: 90                 # Labels available 90 days after prediction
  schedule: "0 10 1 * *"              # 1st of month at 10 AM UTC
  thresholds:
    alert_if_auc_below: 0.77
    critical_if_auc_below: 0.72
    retrain_if_relative_drop_pct: 10

alerts:
  warning:
    - type: slack
      channel: "#ml-monitoring-prod"
  critical:
    - type: slack
      channel: "#ml-alerts-prod"
    - type: pagerduty
      severity: high
  retrain_trigger:
    - type: slack
      channel: "#ml-alerts-prod"
    - type: databricks_job_trigger
      job_name: "customer_churn_retrain_prod"

output:
  monitoring_table: "prod_sales_gold.ml.monitoring_churn_predictor"
  report_path: "s3://prod-ml-monitoring/churn-predictor/"
  retention_days: 730                 # 2 years
```

---

## 10. Change Classification Reference

Quick reference table for the ML team and IT Change Managers:

| Change | Tier | Approver(s) | Lead Time | CAB |
|---|---|---|---|---|
| T4 experiment | Self-service | None | Immediate | No |
| Config change — dev only | Self-service | Peer review | Immediate | No |
| T3 production promotion | Standard | ML Engineering Lead | 3 days | No |
| T2 production promotion | Minor | ML Engineering Lead + domain owner + business owner | 5–10 days | No |
| T1 production promotion | Major | ML Engineering Lead + domain owner + ML Governance + Legal + CDO | 10–15 days | Yes |
| T1 emergency rollback | Emergency | ML Engineering Lead (verbal) | Immediate | Retrospective |
| Feature schema change (additive) | Minor | ML Engineering Lead + DE Lead | 5 days | No |
| Feature schema change (breaking) | Major | ML Engineering Lead + DE Lead + CDO | 10–15 days | Yes |
| Monitoring threshold change (T1) | Minor | ML Engineering Lead + ML Governance | 5 days | No |
| Serving endpoint scaling | Minor | ML Platform Engineer + ML Engineering Lead | 3–5 days | No |
| MLflow server config | Minor | ML Engineering Lead + IT | 5 days | No |
| Model registry permissions | Minor | ML Engineering Lead + IT + InfoSec | 5 days | No |
| ML platform infra change | Major | ML Engineering Lead + IT + InfoSec + CAB | 10–15 days | Yes |
| Bias audit methodology change | Major | ML Governance + Legal + CDO | 10–15 days | Yes |
| New ML tool / platform adoption | Major | CDO + IT + Procurement + CAB | 30+ days | Yes |

---

*This document is maintained by the ML Engineering Lead and reviewed jointly with IT Change Management quarterly. Changes to the change tier classification require joint approval from the ML Engineering Lead and IT Change Management.*
