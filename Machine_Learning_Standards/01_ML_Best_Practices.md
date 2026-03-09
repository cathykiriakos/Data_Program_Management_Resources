# Machine Learning Best Practices
## Model Governance | MLflow | Snowflake ML | SageMaker | Open Source Frameworks

**Document Owner:** Chief Data Office  
**Domain:** Machine Learning  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Guiding Philosophy & ML Operating Model](#1-guiding-philosophy--ml-operating-model)
2. [ML Experiment Management — Databricks MLflow](#2-ml-experiment-management--databricks-mlflow)
3. [ML Governance — Snowflake Cortex & Snowpark ML](#3-ml-governance--snowflake-cortex--snowpark-ml)
4. [ML Governance — Open Source & Hybrid Stacks](#4-ml-governance--open-source--hybrid-stacks)
5. [ML Governance — AWS SageMaker](#5-ml-governance--aws-sagemaker)
6. [Model Lineage & Provenance](#6-model-lineage--provenance)
7. [Model Types — Best Practices by Domain](#7-model-types--best-practices-by-domain)
8. [Model Selection Matrix](#8-model-selection-matrix)
9. [Performance Metrics & KPIs](#9-performance-metrics--kpis)
10. [Benchmarking Standards](#10-benchmarking-standards)
11. [Risk Framework for ML](#11-risk-framework-for-ml)
12. [Feature Engineering & Feature Store Standards](#12-feature-engineering--feature-store-standards)
13. [Model Deployment & Serving Standards](#13-model-deployment--serving-standards)
14. [Monitoring & Drift Detection](#14-monitoring--drift-detection)

---

## 1. Guiding Philosophy & ML Operating Model

### 1.1 Mission

> The ML program delivers repeatable, auditable, and risk-aware machine learning capabilities — from experiment to production — with transparent lineage from raw data through model output, governed by clear ownership, performance accountability, and change control.

### 1.2 The ML Governance Gap

Most ML failures in production are governance failures, not technical ones:

| Governance Gap | Real-World Consequence |
|---|---|
| No experiment tracking | "Which version of the model are we running?" — no answer |
| No lineage from data to model | Regulatory audit: cannot demonstrate what data trained the model |
| No performance benchmarks | No signal that model has degraded until business outcome has already been harmed |
| No model ownership | No one is accountable when predictions are wrong |
| No risk classification | High-stakes credit/clinical model governed same as low-stakes recommendation |
| No reproducibility | Model cannot be retrained from scratch after data scientist leaves |
| No drift monitoring | Model trained on 2022 data still running in 2025 on completely different population |

### 1.3 ML Maturity Levels

| Level | Characteristics | Target |
|---|---|---|
| **0 — Manual** | Notebooks, no versioning, no tracking, ad hoc deployment | Never acceptable for production |
| **1 — Tracked** | Experiments logged in MLflow, models versioned, basic metrics captured | Minimum for production |
| **2 — Governed** | Full lineage, model registry, staging gates, champion/challenger framework | Standard requirement |
| **3 — Automated** | CI/CD for models (MLOps), automated retraining triggers, drift alerting | Target for T1 models |
| **4 — Optimized** | Continuous learning, A/B testing infrastructure, automated risk assessment | Aspirational for high-value models |

### 1.4 ML Model Tier Classification

Every model must be assigned a tier at registration. Tier drives the governance requirements.

| Tier | Description | Examples | Governance Requirement |
|---|---|---|---|
| **T1 — Critical** | High business impact; regulatory exposure; consequential for individuals | Credit scoring, clinical risk, fraud detection, pricing | Full MLOps; mandatory explainability; bias audit; legal review |
| **T2 — Significant** | Meaningful business impact; moderate risk | Revenue forecasting, churn prediction, demand planning | Full experiment tracking; champion/challenger; monitoring |
| **T3 — Standard** | Operational use; limited risk | Product recommendations, search ranking, segmentation | Experiment tracking; basic monitoring |
| **T4 — Exploratory** | Prototyping; never in production without promotion | Research, sandbox | No production deployment without tier promotion |

### 1.5 ML Governance Roles

| Role | Responsibilities |
|---|---|
| **ML Engineering Lead** | Platform, MLOps infrastructure, deployment standards, model registry governance |
| **Senior ML Engineer / Data Scientist** | Model development, experiment tracking, champion/challenger design |
| **ML Platform Engineer** | Feature store, serving infrastructure, monitoring, compute management |
| **ML Governance Analyst** | Model inventory, risk classification, audit preparation, lineage validation |
| **Model Risk Officer** *(or Data Governance Lead)* | Independent model validation for T1/T2 models; regulatory compliance |

---

## 2. ML Experiment Management — Databricks MLflow

### 2.1 MLflow Architecture in Databricks

```
┌──────────────────────────────────────────────────────────────────┐
│  DATABRICKS WORKSPACE                                            │
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────┐                    │
│  │  MLflow Tracking │    │  MLflow Model    │                    │
│  │  Server          │    │  Registry        │                    │
│  │                  │    │                  │                    │
│  │  Experiments     │    │  Staging →       │                    │
│  │  Runs            │    │  Production →    │                    │
│  │  Metrics         │    │  Archived        │                    │
│  │  Artifacts       │    │                  │                    │
│  └────────┬─────────┘    └────────┬─────────┘                   │
│           │                       │                              │
│           └──────────┬────────────┘                              │
│                      │                                           │
│           ┌──────────▼────────────┐                              │
│           │  Unity Catalog        │                              │
│           │  (ML namespace)       │                              │
│           │  Models, Volumes,     │                              │
│           │  Feature Tables       │                              │
│           └───────────────────────┘                              │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Experiment Tracking Standards

**Rule:** Every model training run — including exploratory runs — must be tracked in MLflow. No untracked training.

```python
# ml/base/mlflow_trainer.py
"""
Standard base class for all ML training pipelines.
Enforces consistent experiment tracking, artifact logging, and metadata.
"""

from __future__ import annotations

import os
import json
import hashlib
import platform
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.base import BaseEstimator

from config_loader import load_ml_config
from data_loader import load_feature_dataset


class BaseMLTrainer(ABC):
    """
    All ML models extend this class.
    Enforces: experiment tracking, artifact standards, metadata, lineage.
    """

    def __init__(self, config_path: str, env: str = "dev"):
        self.config = load_ml_config(config_path, env)
        self.model_cfg = self.config["model"]
        self.data_cfg = self.config["data"]
        self.training_cfg = self.config["training"]
        self.env = env

        # Set MLflow tracking URI and experiment
        mlflow.set_tracking_uri(self.config["mlflow"]["tracking_uri"])
        mlflow.set_experiment(self._experiment_name())

    def _experiment_name(self) -> str:
        """Standard experiment naming: /{domain}/{model_name}/{env}"""
        return (
            f"/{self.model_cfg['domain']}/"
            f"{self.model_cfg['name']}/"
            f"{self.env}"
        )

    def _log_standard_metadata(self, run: mlflow.ActiveRun) -> None:
        """Log required metadata on every run — non-negotiable."""
        mlflow.set_tags({
            # Identity
            "model.name":           self.model_cfg["name"],
            "model.version":        self.model_cfg["version"],
            "model.tier":           self.model_cfg["tier"],          # T1/T2/T3/T4
            "model.domain":         self.model_cfg["domain"],
            "model.use_case":       self.model_cfg["use_case"],
            "model.owner":          self.model_cfg["owner_team"],
            "model.owner_email":    self.model_cfg["owner_email"],

            # Data lineage
            "data.feature_table":   self.data_cfg["feature_table"],
            "data.snapshot_date":   self.data_cfg.get("snapshot_date", ""),
            "data.train_start":     str(self.data_cfg.get("train_start_date", "")),
            "data.train_end":       str(self.data_cfg.get("train_end_date", "")),
            "data.row_count":       str(self.data_cfg.get("row_count", "")),
            "data.feature_hash":    self._hash_feature_list(),

            # Governance
            "governance.pii_used":          str(self.data_cfg.get("pii_used", False)),
            "governance.bias_audit_done":   str(self.model_cfg.get("bias_audit_done", False)),
            "governance.explainability":    self.model_cfg.get("explainability_method", "none"),
            "governance.risk_classification": self.model_cfg.get("risk_classification", ""),

            # Environment
            "env.name":             self.env,
            "env.python_version":   platform.python_version(),
            "env.platform":         platform.platform(),
            "git.commit":           os.environ.get("GIT_COMMIT_SHA", "unknown"),
            "git.branch":           os.environ.get("GIT_BRANCH", "unknown"),
        })

    def _hash_feature_list(self) -> str:
        """Deterministic hash of feature list for lineage tracking."""
        features = sorted(self.data_cfg.get("features", []))
        return hashlib.sha256("|".join(features).encode()).hexdigest()[:16]

    def _log_data_profile(self, df: pd.DataFrame) -> None:
        """Log data profile as artifact for reproducibility."""
        profile = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "dtypes": {c: str(t) for c, t in df.dtypes.items()},
            "null_counts": df.isnull().sum().to_dict(),
            "snapshot_timestamp": datetime.now(timezone.utc).isoformat(),
        }
        mlflow.log_dict(profile, "data_profile/training_data_profile.json")

    @abstractmethod
    def load_data(self) -> tuple[pd.DataFrame, pd.Series]:
        """Load features and target from feature store."""
        pass

    @abstractmethod
    def train(self, X_train, y_train) -> BaseEstimator:
        """Train and return the model."""
        pass

    @abstractmethod
    def evaluate(self, model, X_test, y_test) -> dict[str, float]:
        """Evaluate model; return dict of metric_name → value."""
        pass

    def run(self) -> str:
        """Full training run with standard tracking. Returns run_id."""
        with mlflow.start_run() as run:
            self._log_standard_metadata(run)

            # Load data
            X, y = self.load_data()
            self._log_data_profile(pd.concat([X, y], axis=1))

            # Split
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=self.training_cfg.get("test_size", 0.2),
                random_state=self.training_cfg.get("random_state", 42),
                stratify=y if self.training_cfg.get("stratify", False) else None
            )

            mlflow.log_params({
                "test_size":     self.training_cfg.get("test_size", 0.2),
                "random_state":  self.training_cfg.get("random_state", 42),
                "train_rows":    len(X_train),
                "test_rows":     len(X_test),
                **self.training_cfg.get("hyperparameters", {})
            })

            # Train
            model = self.train(X_train, y_train)

            # Evaluate
            metrics = self.evaluate(model, X_test, y_test)
            mlflow.log_metrics(metrics)

            # Log model with signature
            from mlflow.models import infer_signature
            signature = infer_signature(X_train, model.predict(X_train))
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                signature=signature,
                registered_model_name=f"{self.model_cfg['domain']}.{self.model_cfg['name']}"
            )

            # Log requirements
            mlflow.log_artifact("requirements.txt", "environment")

            print(f"Run complete. Run ID: {run.info.run_id}")
            print(f"Metrics: {metrics}")
            return run.info.run_id
```

### 2.3 MLflow Model Config Standard

```yaml
# configs/churn/prod_config.yaml
model:
  name: customer_churn_predictor
  version: "4.2.0"
  tier: T2                         # T1 | T2 | T3 | T4
  domain: sales
  use_case: churn_prediction
  algorithm: gradient_boosting
  owner_team: sales-ml-team
  owner_email: sales-ml@company.com
  bias_audit_done: true
  explainability_method: shap      # shap | lime | permutation | none
  risk_classification: MEDIUM      # LOW | MEDIUM | HIGH | CRITICAL
  target_variable: is_churned_90d
  prediction_type: binary_classification

data:
  feature_table: "prod_sales_gold.ml.customer_features_v3"
  train_start_date: "2022-01-01"
  train_end_date: "2023-12-31"
  snapshot_date: "2024-01-15"
  features:
    - tenure_days
    - avg_monthly_spend
    - support_tickets_90d
    - last_login_days_ago
    - plan_tier
    - contract_type
    - nps_score_last
  target: is_churned_90d
  pii_used: false

training:
  test_size: 0.2
  random_state: 42
  stratify: true
  hyperparameters:
    n_estimators: 500
    max_depth: 6
    learning_rate: 0.05
    subsample: 0.8
    colsample_bytree: 0.8

mlflow:
  tracking_uri: "databricks"
  model_registry_uri: "databricks-uc"

performance_gates:
  min_auc_roc: 0.80
  min_precision_at_k: 0.65         # Precision at top-K ranked customers
  max_feature_drift_threshold: 0.10
  retraining_trigger: "monthly_or_drift"

serving:
  endpoint_name: "customer_churn_prod"
  compute_type: databricks_model_serving
  scaling: auto
  latency_sla_ms: 200
```

### 2.4 MLflow Model Registry Workflow

```python
# ml/registry/model_lifecycle.py
"""
Manages model promotion through MLflow registry stages.
All stage transitions are logged and require documented justification.
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime, timezone


class ModelLifecycleManager:
    """
    Controls model stage transitions in MLflow Model Registry.
    Enforces governance gates at each transition.
    """

    STAGES = ["None", "Staging", "Production", "Archived"]

    def __init__(self, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()

    def promote_to_staging(
        self,
        model_name: str,
        version: str,
        run_id: str,
        validation_report_path: str,
        promoter: str
    ) -> None:
        """
        Promote model version to Staging.
        Requires: validation report and promoter identity.
        """
        # Verify performance gates passed
        run = self.client.get_run(run_id)
        self._check_performance_gates(model_name, run)

        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Staging",
            archive_existing_versions=False
        )

        # Log promotion metadata
        self.client.update_model_version(
            name=model_name,
            version=version,
            description=(
                f"Promoted to Staging by {promoter} on "
                f"{datetime.now(timezone.utc).isoformat()}. "
                f"Validation report: {validation_report_path}"
            )
        )
        self.client.set_model_version_tag(
            name=model_name, version=version,
            key="staging.promoter", value=promoter
        )
        self.client.set_model_version_tag(
            name=model_name, version=version,
            key="staging.timestamp", value=datetime.now(timezone.utc).isoformat()
        )
        self.client.set_model_version_tag(
            name=model_name, version=version,
            key="staging.validation_report", value=validation_report_path
        )
        print(f"Model {model_name} v{version} promoted to Staging.")

    def promote_to_production(
        self,
        model_name: str,
        version: str,
        approval_ticket: str,
        approver: str,
        champion_challenger_results: dict | None = None
    ) -> None:
        """
        Promote model version to Production.
        Requires: change ticket, approver, and champion/challenger results (T1/T2).
        """
        model_tier = self._get_model_tier(model_name, version)

        # T1/T2 models require champion/challenger results
        if model_tier in ("T1", "T2") and not champion_challenger_results:
            raise ValueError(
                f"T1/T2 model {model_name} requires champion/challenger results "
                "before production promotion."
            )

        # Archive current production version
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production",
            archive_existing_versions=True   # Auto-archives old production
        )

        # Log promotion metadata
        tags = {
            "production.approver":      approver,
            "production.timestamp":     datetime.now(timezone.utc).isoformat(),
            "production.change_ticket": approval_ticket,
        }
        if champion_challenger_results:
            tags["production.cc_lift"] = str(
                champion_challenger_results.get("challenger_lift_pct", "N/A")
            )
            tags["production.cc_test_duration_days"] = str(
                champion_challenger_results.get("test_duration_days", "N/A")
            )

        for key, value in tags.items():
            self.client.set_model_version_tag(
                name=model_name, version=version,
                key=key, value=value
            )
        print(f"Model {model_name} v{version} promoted to Production. Ticket: {approval_ticket}")

    def _check_performance_gates(self, model_name: str, run: mlflow.entities.Run) -> None:
        """Verify minimum performance metrics are met before staging promotion."""
        # Retrieve gates from model config (or MLflow model tag)
        gates = {
            "auc_roc": float(run.data.tags.get("gate.min_auc_roc", 0)),
            "precision": float(run.data.tags.get("gate.min_precision", 0)),
        }
        metrics = run.data.metrics
        for gate_name, min_val in gates.items():
            if metrics.get(gate_name, 0) < min_val:
                raise ValueError(
                    f"Performance gate failed: {gate_name} = "
                    f"{metrics.get(gate_name, 'N/A')} < required {min_val}. "
                    "Cannot promote to Staging."
                )

    def _get_model_tier(self, model_name: str, version: str) -> str:
        mv = self.client.get_model_version(model_name, version)
        return mv.tags.get("model.tier", "T3")
```

### 2.5 Champion/Challenger Framework

```python
# ml/evaluation/champion_challenger.py
"""
Champion/Challenger evaluation framework.
Required for all T1 and T2 model promotions.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    mean_absolute_error, mean_squared_error
)
from dataclasses import dataclass
from typing import Callable


@dataclass
class CCResult:
    champion_metric: float
    challenger_metric: float
    lift_pct: float
    winner: str               # "champion" | "challenger" | "no_significant_difference"
    significance_p_value: float
    recommendation: str
    test_duration_days: int
    sample_size: int


def run_champion_challenger(
    champion_predict_fn: Callable,
    challenger_predict_fn: Callable,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    metric_fn: Callable,
    metric_name: str,
    min_lift_threshold_pct: float = 2.0,   # Challenger must beat champion by ≥2%
    test_duration_days: int = 14
) -> CCResult:
    """
    Compare champion model against challenger.
    Challenger wins only if it exceeds champion by min_lift_threshold_pct.
    """
    from scipy import stats

    champion_preds = champion_predict_fn(X_test)
    challenger_preds = challenger_predict_fn(X_test)

    champ_score = metric_fn(y_test, champion_preds)
    chal_score = metric_fn(y_test, challenger_preds)

    lift_pct = ((chal_score - champ_score) / abs(champ_score)) * 100

    # Statistical significance test
    t_stat, p_val = stats.ttest_rel(
        np.abs(y_test - champion_preds),
        np.abs(y_test - challenger_preds)
    )

    if lift_pct >= min_lift_threshold_pct and p_val < 0.05:
        winner = "challenger"
        recommendation = (
            f"Challenger wins with {lift_pct:.1f}% lift on {metric_name} "
            f"(p={p_val:.3f}). Recommend promoting challenger to production."
        )
    elif abs(lift_pct) < min_lift_threshold_pct:
        winner = "no_significant_difference"
        recommendation = (
            f"No significant difference ({lift_pct:.1f}% lift). "
            "Retain champion. Consider rerunning with larger sample."
        )
    else:
        winner = "champion"
        recommendation = (
            f"Champion retains superiority. Challenger shows {lift_pct:.1f}% "
            f"change on {metric_name}. Do not promote challenger."
        )

    return CCResult(
        champion_metric=champ_score,
        challenger_metric=chal_score,
        lift_pct=lift_pct,
        winner=winner,
        significance_p_value=p_val,
        recommendation=recommendation,
        test_duration_days=test_duration_days,
        sample_size=len(X_test)
    )
```

---

## 3. ML Governance — Snowflake Cortex & Snowpark ML

### 3.1 Snowflake ML Capabilities Overview

| Capability | Tool | Governance Surface |
|---|---|---|
| In-database ML training | Snowpark ML `snowflake.ml.modeling` | Snowflake access history + Unity-style tagging |
| LLM / foundation model inference | Cortex AI (`CORTEX.COMPLETE`, `CORTEX.SENTIMENT`) | Query audit log; function-level governance |
| Feature engineering | Snowpark Python / dbt | Same lineage as data tables |
| Model registry | Snowflake Model Registry (GA) | Tracked versions in SNOWFLAKE.ML schema |
| Forecast / anomaly | Cortex ML Functions (`FORECAST`, `ANOMALY_DETECTION`) | SQL-native; logged in query history |

### 3.2 Snowflake Model Registry

```python
# snowflake_ml/registry/snowflake_model_registry.py
"""
Snowflake Model Registry integration.
Tracks models trained with Snowpark ML or externally imported.
"""

from snowflake.ml.registry import Registry
from snowflake.ml.model import custom_model
import snowflake.snowpark as snowpark
import pandas as pd
from sklearn.base import BaseEstimator


def register_model_in_snowflake(
    session: snowpark.Session,
    model: BaseEstimator,
    model_name: str,
    model_version: str,
    sample_input: pd.DataFrame,
    metadata: dict
) -> None:
    """
    Register a trained model (sklearn, xgboost, pytorch, etc.)
    into the Snowflake Model Registry with full governance metadata.
    """
    reg = Registry(
        session=session,
        database_name=metadata["registry_database"],
        schema_name="ML_REGISTRY"
    )

    mv = reg.log_model(
        model=model,
        model_name=model_name,
        version_name=model_version,
        sample_input_data=sample_input,
        comment=(
            f"Owner: {metadata['owner_team']} | "
            f"Use case: {metadata['use_case']} | "
            f"Tier: {metadata['tier']} | "
            f"Training data: {metadata['feature_table']}"
        ),
        tags={
            "domain":           metadata["domain"],
            "use_case":         metadata["use_case"],
            "tier":             metadata["tier"],
            "owner_team":       metadata["owner_team"],
            "feature_table":    metadata["feature_table"],
            "train_end_date":   metadata["train_end_date"],
            "git_commit":       metadata.get("git_commit", "unknown"),
            "risk_class":       metadata.get("risk_classification", "LOW"),
        }
    )
    print(f"Model {model_name} v{model_version} registered in Snowflake Registry.")
    return mv


def deploy_model_as_udf(
    session: snowpark.Session,
    model_name: str,
    model_version: str,
    registry_database: str,
    target_schema: str,
    udf_name: str
) -> None:
    """
    Deploy a registered model as a Snowflake UDF for inline scoring.
    Predictions run directly against data in Snowflake — no data egress.
    """
    reg = Registry(session=session, database_name=registry_database, schema_name="ML_REGISTRY")
    mv = reg.get_model(model_name).version(model_version)

    mv.deploy(
        deployment_name=udf_name,
        target_method="predict",
        permanent=True,
        options={"target_platforms": ["WAREHOUSE"]}
    )
    print(f"Model deployed as UDF: {target_schema}.{udf_name}")
```

### 3.3 Cortex ML Functions — Governed Usage

```sql
-- Standard governed usage of Snowflake Cortex ML Functions
-- All Cortex calls logged in query history with user + timestamp

-- FORECAST: Time-series forecasting (no model training code required)
-- Create a forecast model (versioned, auditable via Snowflake object history)
CREATE OR REPLACE SNOWFLAKE.ML.FORECAST finance_revenue_forecast (
    INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'PROD_FINANCE_GOLD.ML.VW_REVENUE_TRAINING_DATA'),
    SERIES_COLNAME => 'region_code',
    TIMESTAMP_COLNAME => 'month_start_date',
    TARGET_COLNAME => 'net_revenue_usd'
);

-- Generate forecast — logged in query history
CALL finance_revenue_forecast!FORECAST(
    FORECASTING_PERIODS => 12,
    CONFIG_OBJECT => {'prediction_interval': 0.95}
);

-- Governance: Tag the forecast object
ALTER SNOWFLAKE.ML.FORECAST finance_revenue_forecast
    SET TAG governance.tags.domain = 'DOMAIN_FINANCE',
            governance.tags.data_classification = 'CONFIDENTIAL',
            governance.tags.owner = 'finance-ml-team';
```

### 3.4 Snowpark ML Training Pipeline

```python
# snowflake_ml/training/snowpark_trainer.py
"""
Training pipeline using Snowpark ML — data never leaves Snowflake.
"""

import snowflake.snowpark as snowpark
from snowflake.ml.modeling.pipeline import Pipeline
from snowflake.ml.modeling.preprocessing import StandardScaler, OrdinalEncoder
from snowflake.ml.modeling.xgboost import XGBClassifier
from snowflake.ml.modeling.model_selection import train_test_split
from snowflake.ml.modeling.metrics import accuracy_score, roc_auc_score
import mlflow  # MLflow also supported with Snowflake backend


def train_churn_model_snowpark(
    session: snowpark.Session,
    feature_table: str,
    target_col: str,
    config: dict
) -> Pipeline:
    """
    Train a churn model entirely within Snowflake using Snowpark ML.
    Data never leaves the Snowflake security boundary.
    """

    # Load features from governed Gold feature table
    df = session.table(feature_table)

    # Split within Snowflake
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        label_cols=[target_col]
    )

    feature_cols = config["features"]
    cat_cols = config.get("categorical_features", [])
    num_cols = [c for c in feature_cols if c not in cat_cols]

    # Build pipeline — executes as Snowflake SQL / UDFs
    pipeline = Pipeline(steps=[
        ("encoder", OrdinalEncoder(
            input_cols=cat_cols,
            output_cols=[f"{c}_encoded" for c in cat_cols]
        )),
        ("scaler", StandardScaler(
            input_cols=num_cols,
            output_cols=[f"{c}_scaled" for c in num_cols]
        )),
        ("classifier", XGBClassifier(
            input_cols=[f"{c}_scaled" for c in num_cols] +
                       [f"{c}_encoded" for c in cat_cols],
            label_cols=[target_col],
            output_cols=["prediction", "prediction_proba"],
            **config["hyperparameters"]
        ))
    ])

    pipeline.fit(train_df)

    # Evaluate
    predictions = pipeline.predict(test_df)
    auc = roc_auc_score(
        df=predictions,
        y_true_col_names=target_col,
        y_score_col_names="prediction_proba"
    )
    print(f"Snowpark ML Model AUC-ROC: {auc:.4f}")

    return pipeline
```

---

## 4. ML Governance — Open Source & Hybrid Stacks

### 4.1 OSS MLOps Stack Reference

For teams not using a managed platform (Databricks or SageMaker), the following open source stack provides production-grade ML governance:

| Layer | Tool | Purpose |
|---|---|---|
| Experiment Tracking | MLflow (self-hosted) | Metrics, params, artifacts, model versions |
| Feature Store | Feast (open source) | Feature definitions, serving, point-in-time correctness |
| Pipeline Orchestration | Apache Airflow or Prefect | DAG-based training and retraining pipelines |
| Model Serving | BentoML or FastAPI + Docker | Standardized model serving |
| Model Monitoring | Evidently AI | Data drift, target drift, model performance |
| Data Versioning | DVC (Data Version Control) | Reproducible datasets tied to model versions |
| Container Registry | Docker + ECR/ACR/GCR | Model container versioning |
| CI/CD | GitHub Actions | MLOps deployment automation |

### 4.2 Self-Hosted MLflow Setup

```python
# infrastructure/mlflow_server/docker-compose.yml pattern equivalent in Python

"""
MLflow server setup with PostgreSQL backend and S3 artifact store.
Deploy via Docker or on a dedicated EC2/VM instance.
"""

# mlflow_server_config.py
MLFLOW_CONFIG = {
    "backend_store_uri": "postgresql://mlflow_user:{password}@{host}:5432/mlflow",
    "default_artifact_root": "s3://{bucket}/mlflow-artifacts",
    "host": "0.0.0.0",
    "port": 5000,
    "serve_artifacts": True,
    "artifacts_destination": "s3://{bucket}/mlflow-artifacts"
}

# Startup command:
# mlflow server \
#   --backend-store-uri postgresql://... \
#   --default-artifact-root s3://... \
#   --host 0.0.0.0 --port 5000 \
#   --serve-artifacts
```

### 4.3 DVC for Data Versioning

```python
# data_versioning/dvc_manager.py
"""
Data Version Control (DVC) integration.
Every model training run references a versioned dataset snapshot.
This creates the data ↔ model lineage required for governance.
"""

import subprocess
import hashlib
import json
from pathlib import Path


def snapshot_training_data(
    source_path: str,
    snapshot_name: str,
    metadata: dict
) -> str:
    """
    Create a DVC-tracked snapshot of training data.
    Returns the DVC file hash (used as lineage reference in MLflow).
    """
    # Add to DVC tracking
    subprocess.run(["dvc", "add", source_path], check=True)

    # Read the generated .dvc file for the hash
    dvc_file = f"{source_path}.dvc"
    with open(dvc_file) as f:
        dvc_content = f.read()
    data_hash = _extract_md5_from_dvc(dvc_file)

    # Log metadata alongside DVC file
    metadata_path = Path(source_path).parent / f"{snapshot_name}_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump({**metadata, "dvc_hash": data_hash, "snapshot_name": snapshot_name}, f, indent=2)

    # Commit DVC files to Git
    subprocess.run(["git", "add", dvc_file, str(metadata_path)], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"data: snapshot {snapshot_name} (hash: {data_hash[:8]})"],
        check=True
    )
    return data_hash


def _extract_md5_from_dvc(dvc_file: str) -> str:
    import yaml
    with open(dvc_file) as f:
        content = yaml.safe_load(f)
    return content["outs"][0]["md5"]
```

### 4.4 Evidently AI — Model Monitoring (OSS)

```python
# monitoring/evidently_monitor.py
"""
Open source model and data drift monitoring using Evidently AI.
Runs on schedule; outputs to monitoring dashboard.
"""

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import (
    DataDriftPreset,
    TargetDriftPreset,
    ClassificationPreset,
    RegressionPreset
)
from evidently.metrics import (
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
    ColumnDriftMetric
)
from evidently.test_suite import TestSuite
from evidently.tests import (
    TestNumberOfDriftedColumns,
    TestShareOfDriftedColumns,
    TestColumnValueMean
)


def generate_drift_report(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    target_col: str,
    prediction_col: str,
    model_type: str,          # "classification" | "regression"
    output_path: str
) -> dict:
    """
    Generate data drift, target drift, and model performance report.
    Returns summary dict for logging to MLflow or monitoring store.
    """

    # Build report based on model type
    presets = [DataDriftPreset(), TargetDriftPreset()]
    if model_type == "classification":
        presets.append(ClassificationPreset())
    elif model_type == "regression":
        presets.append(RegressionPreset())

    report = Report(metrics=presets)
    report.run(
        reference_data=reference_df,
        current_data=current_df,
        column_mapping={
            "target": target_col,
            "prediction": prediction_col
        }
    )
    report.save_html(output_path)

    # Extract summary metrics
    result = report.as_dict()
    drift_share = result["metrics"][0]["result"]["share_of_drifted_columns"]

    return {
        "drift_share_of_columns": drift_share,
        "drift_detected": drift_share > 0.2,    # Alert if >20% columns drifted
        "report_path": output_path,
        "reference_rows": len(reference_df),
        "current_rows": len(current_df),
    }


def run_drift_tests(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    max_drift_share: float = 0.2
) -> bool:
    """
    Run automated drift tests. Returns True if all tests pass.
    Used as a gate in retraining pipelines.
    """
    suite = TestSuite(tests=[
        TestShareOfDriftedColumns(lt=max_drift_share),
        TestNumberOfDriftedColumns(lt=5),
        TestDatasetDriftMetric()
    ])
    suite.run(reference_data=reference_df, current_data=current_df)
    return suite.as_dict()["summary"]["all_passed"]
```

---

## 5. ML Governance — AWS SageMaker

### 5.1 SageMaker MLOps Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  AWS SAGEMAKER ECOSYSTEM                                      │
│                                                              │
│  SageMaker Studio (IDE + experiments)                        │
│      └── SageMaker Experiments → Track runs, metrics        │
│      └── SageMaker Model Registry → Version + approval      │
│                                                              │
│  SageMaker Pipelines (MLOps orchestration)                   │
│      └── Processing → Training → Evaluation → Register      │
│                                                              │
│  SageMaker Feature Store                                     │
│      └── Online store (low-latency serving)                  │
│      └── Offline store (S3 — training)                       │
│                                                              │
│  SageMaker Model Monitor                                     │
│      └── Data quality, model quality, bias, explainability  │
│                                                              │
│  SageMaker Clarify                                           │
│      └── Bias detection, SHAP explainability                 │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 SageMaker Pipeline — Config-Driven

```python
# sagemaker/pipelines/churn_pipeline.py
"""
Config-driven SageMaker Pipeline for model training and registration.
All parameters externalized to config — no hardcoding.
"""

import boto3
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.parameters import ParameterFloat, ParameterString
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.model_metrics import MetricsSource, ModelMetrics


def build_churn_pipeline(config: dict, role: str, session: sagemaker.Session) -> Pipeline:
    """
    Build a SageMaker Pipeline from config.
    Returns a pipeline object ready to upsert and execute.
    """
    env = config["pipeline"]["environment"]

    # Pipeline parameters (overridable at execution time)
    min_auc_roc = ParameterFloat(name="MinAUCROC", default_value=config["gates"]["min_auc_roc"])
    feature_table = ParameterString(name="FeatureTable", default_value=config["data"]["feature_table"])

    # Step 1: Data processing
    processor = SKLearnProcessor(
        framework_version="1.2-1",
        role=role,
        instance_type=config["compute"]["processing_instance"],
        instance_count=1,
        base_job_name=f"{config['pipeline']['name']}-process-{env}",
        tags=[
            {"Key": "environment", "Value": env},
            {"Key": "pipeline",    "Value": config["pipeline"]["name"]},
            {"Key": "managed_by",  "Value": "sagemaker-pipeline"},
            {"Key": "cost_center", "Value": config["pipeline"]["cost_center"]},
        ]
    )

    processing_step = ProcessingStep(
        name="ProcessData",
        processor=processor,
        inputs=[...],
        outputs=[...],
        code="scripts/process.py",
        job_arguments=["--feature-table", feature_table]
    )

    # Step 2: Training
    estimator = SKLearn(
        entry_point="scripts/train.py",
        framework_version="1.2-1",
        role=role,
        instance_type=config["compute"]["training_instance"],
        instance_count=1,
        hyperparameters=config["training"]["hyperparameters"],
        metric_definitions=[
            {"Name": "auc_roc",   "Regex": "auc_roc: ([0-9\\.]+)"},
            {"Name": "precision", "Regex": "precision: ([0-9\\.]+)"},
            {"Name": "recall",    "Regex": "recall: ([0-9\\.]+)"},
        ],
        tags=[
            {"Key": "environment", "Value": env},
            {"Key": "managed_by",  "Value": "sagemaker-pipeline"},
        ]
    )

    training_step = TrainingStep(
        name="TrainModel",
        estimator=estimator,
        inputs={"train": processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri}
    )

    # Step 3: Conditional registration (only if AUC >= gate)
    auc_condition = ConditionGreaterThanOrEqualTo(
        left=JsonGet(
            step_name=training_step.name,
            property_file=None,
            json_path="metrics.auc_roc.value"
        ),
        right=min_auc_roc
    )

    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri=f"{training_step.properties.ModelArtifacts.S3ModelArtifacts}/metrics.json",
            content_type="application/json"
        )
    )

    # Registration step
    register_step = ModelStep(
        name="RegisterModel",
        step_args=estimator.register(
            content_types=["text/csv"],
            response_types=["text/csv"],
            inference_instances=[config["compute"]["inference_instance"]],
            model_package_group_name=f"{config['pipeline']['name']}-{env}",
            model_metrics=model_metrics,
            approval_status="PendingManualApproval",  # Require human approval for T1/T2
            description=(
                f"Churn predictor | Tier: {config['model']['tier']} | "
                f"Owner: {config['model']['owner_team']}"
            )
        )
    )

    condition_step = ConditionStep(
        name="CheckAUCGate",
        conditions=[auc_condition],
        if_steps=[register_step],
        else_steps=[]    # Fail silently if gate not met; log in experiment
    )

    return Pipeline(
        name=f"{config['pipeline']['name']}-{env}",
        parameters=[min_auc_roc, feature_table],
        steps=[processing_step, training_step, condition_step],
        sagemaker_session=session
    )
```

### 5.3 SageMaker Model Monitor Configuration

```python
# sagemaker/monitoring/model_monitor_setup.py
"""
Configure SageMaker Model Monitor for data quality and model drift.
"""

from sagemaker.model_monitor import (
    DataCaptureConfig,
    DefaultModelMonitor,
    ModelQualityMonitor,
    CronExpressionGenerator
)


def setup_data_capture(endpoint_name: str, s3_capture_path: str) -> DataCaptureConfig:
    """Enable data capture on endpoint for monitoring baseline."""
    return DataCaptureConfig(
        enable_capture=True,
        sampling_percentage=20,            # Capture 20% of inference traffic
        destination_s3_uri=s3_capture_path,
        capture_options=["REQUEST", "RESPONSE"],
        csv_content_types=["text/csv"],
        json_content_types=["application/json"]
    )


def setup_data_quality_monitor(
    role: str,
    endpoint_name: str,
    baseline_dataset_uri: str,
    schedule_name: str,
    output_s3_uri: str,
    sns_topic_arn: str
) -> DefaultModelMonitor:
    """Configure scheduled data quality monitoring."""
    monitor = DefaultModelMonitor(
        role=role,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        volume_size_in_gb=20,
        max_runtime_in_seconds=3600
    )

    monitor.suggest_baseline(
        baseline_dataset=baseline_dataset_uri,
        dataset_format={"csv": {"header": True}},
        output_s3_uri=f"{output_s3_uri}/baseline"
    )

    monitor.create_monitoring_schedule(
        monitor_schedule_name=schedule_name,
        endpoint_input=endpoint_name,
        output_s3_uri=f"{output_s3_uri}/reports",
        statistics=monitor.baseline_statistics(),
        constraints=monitor.suggested_constraints(),
        schedule_cron_expression=CronExpressionGenerator.daily(),
        enable_cloudwatch_metrics=True
    )

    return monitor
```

---

## 6. Model Lineage & Provenance

### 6.1 Full Lineage Chain

Every production model must have a documented, unbroken lineage chain:

```
Source System Data
      │
      ▼ (Data Engineering Pipeline — documented in DE standards)
Bronze Layer Table (raw)
      │
      ▼ (dbt Silver transformation — logged in dbt lineage graph)
Silver Layer Table (cleansed)
      │
      ▼ (Feature engineering pipeline — logged in Feature Store)
Feature Table / Feature Store
      │
      ▼ (Training run — logged in MLflow / SageMaker Experiments)
Model Artifact (versioned, with run_id → feature_table → source table chain)
      │
      ▼ (Model registration — MLflow Registry / SageMaker Model Registry)
Registered Model Version (Staging → Production promotion logged)
      │
      ▼ (Deployment — endpoint, UDF, batch job)
Predictions / Scores
      │
      ▼ (Scored records written back to Gold layer or feature store)
Prediction Table (with model_name, model_version, run_id, scored_at)
```

### 6.2 Lineage Metadata Standard

Every prediction output table must include:

```sql
-- Required columns on all ML output / prediction tables
_model_name         VARCHAR    -- Registered model name
_model_version      VARCHAR    -- Model version used for scoring
_model_run_id       VARCHAR    -- MLflow / SageMaker run ID
_feature_table      VARCHAR    -- Feature table used (name + version)
_scored_at          TIMESTAMP  -- When this prediction was generated
_prediction_id      VARCHAR    -- Unique ID per prediction (UUID)
_confidence_score   FLOAT      -- Model confidence / probability
_model_tier         VARCHAR    -- T1/T2/T3
_pipeline_version   VARCHAR    -- Scoring pipeline code version (git tag)
```

### 6.3 Lineage Registry (Python)

```python
# ml/lineage/lineage_registry.py
"""
Central lineage registry.
Records the full chain from source data to prediction for every model version.
Queryable for audit and regulatory purposes.
"""

import json
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ModelLineageRecord:
    # Model identity
    model_name: str
    model_version: str
    model_tier: str
    run_id: str

    # Data lineage
    feature_table: str
    feature_table_version: str
    training_data_hash: str        # DVC hash or dataset fingerprint
    train_start_date: str
    train_end_date: str
    source_tables: list[str]       # List of upstream source tables

    # Code lineage
    git_commit_sha: str
    git_repo: str
    training_script: str
    requirements_hash: str         # Hash of requirements.txt

    # Governance
    owner_team: str
    risk_classification: str
    bias_audit_completed: bool
    explainability_method: str
    approval_ticket: Optional[str]
    promoted_by: Optional[str]

    # Timestamps
    trained_at: str
    registered_at: str
    promoted_to_production_at: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def persist_lineage_record(
    record: ModelLineageRecord,
    snowflake_session=None,
    output_path: str | None = None
) -> None:
    """
    Persist lineage record to Snowflake governance table and/or file.
    """
    record_dict = record.to_dict()

    # Write to Snowflake governance table if session provided
    if snowflake_session:
        import pandas as pd
        df = pd.DataFrame([record_dict])
        snowflake_session.write_pandas(
            df,
            table_name="ML_LINEAGE_REGISTRY",
            schema="GOVERNANCE",
            database="PROD_GOVERNANCE",
            overwrite=False
        )

    # Write to file (for OSS stacks)
    if output_path:
        with open(output_path, "a") as f:
            f.write(record.to_json() + "\n")
```

---

## 7. Model Types — Best Practices by Domain

### 7.1 Forecasting Models

**Use cases:** Revenue forecasting, demand planning, inventory optimization, capacity planning

**Algorithm selection:**

| Data Characteristics | Recommended Approach |
|---|---|
| Univariate, < 2 years history, business users need interpretability | Facebook Prophet / NeuralProphet |
| Multivariate, many series, strong seasonality | LightGBM or XGBoost with time features |
| Long history, complex seasonality, many correlated series | TFT (Temporal Fusion Transformer) or N-BEATS |
| Simple trend + seasonality, regulatory need for transparency | ARIMA / SARIMA (with documented coefficients) |
| Real-time streaming | Online learning (River) or Spark Structured Streaming + model serving |

**Best practices:**
- Always establish a **naive baseline** (last period, same period last year) before comparing model metrics
- Report metrics at multiple horizons (1-week, 1-month, 3-month)
- Track and report **forecast bias** (systematic over/under-forecasting), not just MAE
- Prediction intervals (confidence bands) are mandatory for all production forecasts
- Backtesting using expanding window (not sliding window) to simulate production conditions

```python
# forecasting/evaluation.py
"""Standard evaluation suite for all forecasting models."""

import numpy as np
import pandas as pd
from typing import Callable


def evaluate_forecast(
    actuals: pd.Series,
    forecast: pd.Series,
    lower_bound: pd.Series | None = None,
    upper_bound: pd.Series | None = None,
    baseline_forecast: pd.Series | None = None
) -> dict:
    """
    Compute standard forecast evaluation metrics.
    Always compare against a naive baseline.
    """
    errors = actuals - forecast
    abs_errors = np.abs(errors)
    pct_errors = np.abs(errors / actuals.replace(0, np.nan))

    metrics = {
        "mae":              float(abs_errors.mean()),
        "rmse":             float(np.sqrt((errors ** 2).mean())),
        "mape":             float(pct_errors.mean() * 100),
        "smape":            float((2 * abs_errors / (np.abs(actuals) + np.abs(forecast))).mean() * 100),
        "forecast_bias":    float(errors.mean()),       # Positive = under-forecast
        "bias_pct":         float(errors.mean() / actuals.mean() * 100),
        "n_periods":        len(actuals),
    }

    # Coverage of prediction intervals
    if lower_bound is not None and upper_bound is not None:
        in_interval = ((actuals >= lower_bound) & (actuals <= upper_bound)).mean()
        metrics["interval_coverage_pct"] = float(in_interval * 100)

    # Skill score vs. naive baseline
    if baseline_forecast is not None:
        baseline_mae = float(np.abs(actuals - baseline_forecast).mean())
        metrics["skill_score_vs_naive"] = float(
            1 - (metrics["mae"] / baseline_mae)
        )  # Positive = better than naive

    return metrics
```

### 7.2 Segmentation / Clustering Models

**Use cases:** Customer segmentation, market segmentation, anomaly grouping, cohort analysis

**Best practices:**
- Segmentation is a **business decision**, not purely a statistical one — always validate segments with domain experts
- Document the **business interpretation** of each cluster in the model registry
- Use **stability metrics** (ARI between runs) to confirm segments are stable over time
- Never expose raw cluster IDs to business users — map to named segments with business descriptions
- Perform **demographic analysis** on segments for regulated use cases (fair lending, HR) — disparate impact testing

```python
# segmentation/cluster_evaluator.py
"""Standard cluster quality evaluation."""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)
from sklearn.metrics.cluster import adjusted_rand_score


def evaluate_clustering(
    X: np.ndarray,
    labels: np.ndarray,
    prev_labels: np.ndarray | None = None
) -> dict:
    """
    Comprehensive cluster quality metrics.
    Includes stability check if previous run labels are provided.
    """
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    metrics = {
        "n_clusters":           n_clusters,
        "silhouette_score":     float(silhouette_score(X, labels, sample_size=10000)),
        "calinski_harabasz":    float(calinski_harabasz_score(X, labels)),
        "davies_bouldin":       float(davies_bouldin_score(X, labels)),  # Lower is better
        "cluster_sizes":        {str(k): int(v) for k, v in pd.Series(labels).value_counts().items()},
        "smallest_cluster_pct": float(pd.Series(labels).value_counts(normalize=True).min() * 100),
    }

    # Stability vs. prior run
    if prev_labels is not None:
        metrics["stability_ari"] = float(adjusted_rand_score(prev_labels, labels))
        metrics["is_stable"] = metrics["stability_ari"] >= 0.7   # 0.7 threshold standard

    return metrics
```

### 7.3 Recommendation Systems

**Use cases:** Product recommendations, content personalization, next best action, cross-sell/upsell

**Best practices:**
- Always implement **offline and online evaluation** — offline metrics (Precision@K, NDCG) are necessary but not sufficient
- Document the **cold start strategy** (new users/items with no history)
- Implement **diversity and serendipity** metrics alongside accuracy — a good recommender doesn't just recommend the same popular items
- For regulated industries: document and test for **filter bubble** effects and disparate recommendation quality across demographic groups
- Implement **exposure logging** — what was shown, not just what was clicked, to avoid popularity bias in training

```python
# recommendations/offline_evaluator.py
"""Offline evaluation metrics for recommendation systems."""

import numpy as np
from typing import List


def precision_at_k(
    recommended: List[int],
    relevant: List[int],
    k: int
) -> float:
    """What fraction of top-K recommendations are relevant?"""
    top_k = set(recommended[:k])
    relevant_set = set(relevant)
    return len(top_k & relevant_set) / k


def ndcg_at_k(
    recommended: List[int],
    relevant: List[int],
    k: int
) -> float:
    """Normalized Discounted Cumulative Gain @ K."""
    def dcg(items, relevant_set, k):
        return sum(
            1 / np.log2(i + 2)
            for i, item in enumerate(items[:k])
            if item in relevant_set
        )
    relevant_set = set(relevant)
    idcg = dcg(sorted(relevant_set)[:k], relevant_set, k)
    return dcg(recommended, relevant_set, k) / idcg if idcg > 0 else 0.0


def coverage(
    all_recommendations: List[List[int]],
    total_items: int
) -> float:
    """What fraction of the item catalog is being recommended?"""
    recommended_items = set(item for recs in all_recommendations for item in recs)
    return len(recommended_items) / total_items


def evaluate_recommender(
    recommendations: List[List[int]],
    ground_truth: List[List[int]],
    total_items: int,
    k_values: List[int] = [5, 10, 20]
) -> dict:
    """Standard recommender evaluation suite."""
    metrics = {}
    for k in k_values:
        p_at_k = np.mean([
            precision_at_k(rec, gt, k)
            for rec, gt in zip(recommendations, ground_truth)
        ])
        ndcg_k = np.mean([
            ndcg_at_k(rec, gt, k)
            for rec, gt in zip(recommendations, ground_truth)
        ])
        metrics[f"precision_at_{k}"] = float(p_at_k)
        metrics[f"ndcg_at_{k}"] = float(ndcg_k)

    metrics["catalog_coverage"] = float(coverage(recommendations, total_items))
    return metrics
```

---

## 8. Model Selection Matrix

### 8.1 Primary Selection Matrix

| Problem Type | First Choice | When to Consider | Avoid If |
|---|---|---|---|
| **Binary Classification** | Gradient Boosting (XGBoost/LightGBM) | Logistic Regression (interpretability required); Neural Net (very large dataset + feature interactions) | Dataset < 1,000 rows (use simple LR) |
| **Multi-class Classification** | Gradient Boosting | Random Forest (robustness); Neural Net (text/image input) | Unbalanced classes without resampling |
| **Regression** | Gradient Boosting | Linear Regression (interpretability); Neural Net (large dataset) | Always compare to linear baseline first |
| **Time-Series Forecast (few series)** | Prophet | ARIMA/SARIMA (strict interpretability); LSTM (long-range dependency) | Fewer than 12 periods of history |
| **Time-Series Forecast (many series)** | LightGBM with time features | TFT / N-BEATS (deep learning budget available) | N-BEATS without GPU compute |
| **Clustering / Segmentation** | K-Means (known K) or HDBSCAN (unknown K) | Gaussian Mixture Models (soft assignment needed) | DBSCAN on high-dimensional data without UMAP |
| **Anomaly Detection** | Isolation Forest | Autoencoder (complex interactions); Statistical methods (interpretability) | Deep methods without explainability plan |
| **Recommendation (collaborative)** | Matrix Factorization (ALS) | Two-tower neural network (large scale) | Pure content-based without cold start solution |
| **NLP / Text Classification** | Fine-tuned transformer (BERT/RoBERTa) | TF-IDF + LR (low data; interpretability) | Raw LLM API without RAG guardrails in production |
| **Causal Inference** | Double ML / DML | Propensity Score Matching; Instrumental Variables | Standard supervised learning (confounding present) |

### 8.2 Model Complexity vs. Interpretability Trade-Off

```
High Interpretability ←────────────────────────────────→ High Performance
                                                        
  Linear/Logistic │ Decision   │ Random   │ Gradient  │ Deep
  Regression      │ Tree       │ Forest   │ Boosting  │ Neural Net
                  │            │          │           │
  T1 Regulated ───┼────────────┼──────────┼───────────┼── Requires SHAP/LIME
  (Credit/Clinical)│ Preferred  │ Requires │ Requires  │   + Model Card
                  │            │  explainability       │
  T2 Significant ─┼────────────┼──────────┼───────────┼── Recommended
  (Forecasting)   │            │          │ Default   │
                  │            │          │           │
  T3 Standard ────┼────────────┼──────────┼───────────┼── Acceptable
  (Recommendations│            │          │           │
```

### 8.3 Explainability Requirement by Tier

| Tier | Explainability Required | Method | Documented In |
|---|---|---|---|
| T1 — Critical | ✅ Mandatory | SHAP values per prediction + global feature importance | Model card + MLflow artifact |
| T2 — Significant | ✅ Required | Global SHAP feature importance; local on request | MLflow artifact |
| T3 — Standard | Recommended | Global feature importance | MLflow artifact |
| T4 — Exploratory | Optional | None required | N/A |

---

## 9. Performance Metrics & KPIs

### 9.1 Classification Metrics

| Metric | Use When | Formula / Note |
|---|---|---|
| **AUC-ROC** | Ranking quality; imbalanced classes | Area under ROC curve; threshold-independent |
| **AUC-PR** | Highly imbalanced (fraud, anomaly) | Better than ROC when positives are rare |
| **F1 Score** | Balance of precision and recall needed | Harmonic mean; choose weighted avg for multi-class |
| **Precision@K** | Top-K scoring (credit, risk triage) | Precision among top K predictions by score |
| **Lift** | Marketing, direct response campaigns | Lift over random baseline in top decile |
| **KS Statistic** | Credit scoring standard | Max separation between positive/negative CDFs |
| **Brier Score** | Probability calibration quality | Lower is better; 0 = perfect calibration |
| **Log Loss** | Probabilistic classifier quality | Lower is better; penalizes confident wrong predictions |

### 9.2 Regression/Forecast Metrics

| Metric | Use When | Note |
|---|---|---|
| **MAE** | Robust to outliers; interpretable | "Average absolute error in original units" |
| **RMSE** | Penalize large errors more | Sensitive to outliers; report alongside MAE |
| **MAPE** | Percentage errors; scalability | Fails at zero actuals; use sMAPE instead |
| **sMAPE** | Symmetric; handles zero actuals | Standard for demand forecasting competitions |
| **Forecast Bias** | Systematic over/under-forecasting | `mean(actual - forecast)` — should be near zero |
| **Coverage (PI)** | Prediction interval calibration | % of actuals falling within stated interval |
| **Skill Score** | Relative improvement vs. naive | `1 - (model_MAE / naive_MAE)` |

### 9.3 Business KPIs Linked to ML Models

Every production model must have **at least one business KPI** it is accountable for — not just technical metrics.

| Model Type | Example Business KPI | Measurement Frequency |
|---|---|---|
| Churn prediction | % of predicted churners retained via intervention | Monthly |
| Revenue forecast | Forecast accuracy vs. actual (% variance) | Monthly |
| Fraud detection | False positive rate on approved transactions | Weekly |
| Recommendation | CTR, conversion rate on recommendations | Daily |
| Demand planning | Inventory turns, out-of-stock rate | Weekly |
| Credit scoring | Gini coefficient; default rate in approved band | Quarterly |
| Anomaly detection | Alert precision rate (true alerts vs. total alerts) | Weekly |

### 9.4 Model Performance Dashboard — Required KPIs

Every T1/T2 model must have a published performance dashboard (in the BI tool) showing:

```
□ Current model version in production
□ Technical metric (AUC, MAE, etc.) vs. launch baseline and prior version
□ Prediction volume (# predictions made) — trend
□ Data drift score — last 30 days vs. training distribution
□ Business KPI linked to model — trend
□ Last retrained date
□ Next scheduled review date
□ Champion/challenger status (if running)
□ Model tier and risk classification
```

---

## 10. Benchmarking Standards

### 10.1 Baseline Model Requirement

**Rule:** Every model must beat a documented baseline before it can be promoted to production.

| Model Type | Minimum Baseline |
|---|---|
| Classification | Random classifier (50% AUC) + Prior probability classifier |
| Forecasting | Naive forecast (last period) + Seasonal naive (same period last year) |
| Regression | Mean prediction + Linear regression |
| Recommendation | Most popular items + Random recommendation |
| Clustering | Single cluster (all one group) |
| Anomaly detection | Statistical threshold (mean ± 3σ) |

### 10.2 Benchmark Reporting Template

```yaml
# benchmark_report.yaml — required for every T1/T2 model registration
benchmark_report:
  model_name: customer_churn_predictor
  model_version: "4.2.0"
  evaluation_date: "2024-01-15"
  evaluator: "ML Engineering Lead"
  
  dataset:
    name: "Churn holdout set Q4 2023"
    size: 45230
    positive_rate: 0.082
    date_range: "2023-10-01 to 2023-12-31"

  baselines:
    - name: "Random classifier"
      auc_roc: 0.500
      f1: 0.152
    - name: "Prior probability classifier"
      auc_roc: 0.500
      f1: 0.152
    - name: "Logistic regression (simple)"
      auc_roc: 0.731
      f1: 0.401
    - name: "Prior production model (v3.8.1)"
      auc_roc: 0.821
      f1: 0.498

  current_model:
    auc_roc: 0.863
    f1: 0.541
    precision_at_10pct: 0.71
    ks_statistic: 0.49
    brier_score: 0.062

  improvements_vs_prior_production:
    auc_roc_delta: +0.042          # +5.1%
    f1_delta: +0.043               # +8.6%
    business_kpi_projected_lift: "+12% retention rate in top decile"

  gate_results:
    min_auc_roc_gate: 0.80         # Required
    current_auc_roc: 0.863         # PASS
    beats_prior_production: true   # PASS
    explainability_complete: true  # PASS
    bias_audit_complete: true      # PASS

  recommendation: APPROVE FOR STAGING
```

---

## 11. Risk Framework for ML

### 11.1 ML Risk Classification Matrix

| Risk Dimension | Low | Medium | High | Critical |
|---|---|---|---|---|
| **Consequence of error** | Inconvenience | Revenue impact < $100K | Revenue/reputation impact >$100K | Legal liability; harm to individuals |
| **Population affected** | Single user | Small team | Large business unit | All customers or employees |
| **Regulatory exposure** | None | Internal policy | Industry regulation | Legal statute (FCRA, ECOA, HIPAA) |
| **Reversibility** | Easily reversed | Reversible within 24h | Difficult to reverse | Irreversible (credit denial, clinical) |
| **Human oversight** | No override needed | Soft recommendation | Human reviews edge cases | Human required for all consequential decisions |

### 11.2 Model Risk Assessment — Required for T1/T2

```python
# ml/governance/risk_assessment.py
"""
Model Risk Assessment scorecard.
Required for all T1 and T2 models before production promotion.
"""

from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


@dataclass
class ModelRiskAssessment:
    model_name: str
    model_version: str
    assessor: str
    assessment_date: str

    # Risk dimensions (1=Low, 4=Critical)
    consequence_of_error: int        # 1–4
    population_affected: int         # 1–4
    regulatory_exposure: int         # 1–4
    reversibility: int               # 1–4
    human_oversight_level: int       # 1–4 (4 = no oversight = high risk)

    # Controls in place
    explainability_implemented: bool
    bias_audit_completed: bool
    performance_monitoring_active: bool
    human_review_process_documented: bool
    rollback_plan_documented: bool

    def overall_risk_score(self) -> int:
        """Raw risk score (5–20 range)."""
        return (
            self.consequence_of_error +
            self.population_affected +
            self.regulatory_exposure +
            self.reversibility +
            self.human_oversight_level
        )

    def risk_classification(self) -> RiskLevel:
        score = self.overall_risk_score()
        if score <= 8:   return "LOW"
        if score <= 13:  return "MEDIUM"
        if score <= 17:  return "HIGH"
        return "CRITICAL"

    def required_controls_met(self) -> bool:
        risk = self.risk_classification()
        if risk == "CRITICAL":
            return all([
                self.explainability_implemented,
                self.bias_audit_completed,
                self.performance_monitoring_active,
                self.human_review_process_documented,
                self.rollback_plan_documented
            ])
        if risk == "HIGH":
            return all([
                self.explainability_implemented,
                self.bias_audit_completed,
                self.performance_monitoring_active,
                self.rollback_plan_documented
            ])
        if risk == "MEDIUM":
            return all([
                self.performance_monitoring_active,
                self.rollback_plan_documented
            ])
        return True  # LOW risk — no mandatory controls beyond tracking
```

### 11.3 Bias & Fairness Assessment

For T1 models making consequential decisions (credit, employment, healthcare, pricing):

```python
# ml/governance/bias_audit.py
"""
Bias and fairness audit for T1 models.
Required before any T1 model can be promoted to production.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score


def demographic_parity_check(
    predictions: pd.Series,
    sensitive_attribute: pd.Series,
    threshold: float = 0.5
) -> dict:
    """
    Check demographic parity: each group should have similar positive prediction rates.
    Disparity ratio < 0.8 or > 1.25 triggers a finding (80% rule / 4/5 rule).
    """
    groups = sensitive_attribute.unique()
    group_positive_rates = {}

    for group in groups:
        mask = sensitive_attribute == group
        group_positive_rates[str(group)] = float(
            (predictions[mask] >= threshold).mean()
        )

    max_rate = max(group_positive_rates.values())
    min_rate = min(group_positive_rates.values())
    disparity_ratio = min_rate / max_rate if max_rate > 0 else 1.0

    return {
        "group_positive_rates":     group_positive_rates,
        "disparity_ratio":          round(disparity_ratio, 4),
        "four_fifths_rule_pass":    disparity_ratio >= 0.8,
        "finding":                  "PASS" if disparity_ratio >= 0.8 else "FAIL — Disparate Impact"
    }


def equalized_odds_check(
    y_true: pd.Series,
    y_pred: pd.Series,
    sensitive_attribute: pd.Series
) -> dict:
    """
    Check equalized odds: TPR and FPR should be similar across groups.
    """
    results = {}
    for group in sensitive_attribute.unique():
        mask = sensitive_attribute == group
        tp = ((y_pred[mask] >= 0.5) & (y_true[mask] == 1)).sum()
        fn = ((y_pred[mask] < 0.5) & (y_true[mask] == 1)).sum()
        fp = ((y_pred[mask] >= 0.5) & (y_true[mask] == 0)).sum()
        tn = ((y_pred[mask] < 0.5) & (y_true[mask] == 0)).sum()

        results[str(group)] = {
            "tpr": tp / (tp + fn) if (tp + fn) > 0 else None,
            "fpr": fp / (fp + tn) if (fp + tn) > 0 else None,
            "auc": float(roc_auc_score(y_true[mask], y_pred[mask]))
        }

    return results
```

---

## 12. Feature Engineering & Feature Store Standards

### 12.1 Feature Store Standards

| Rule | Standard |
|---|---|
| Single source of truth | Features used in training and serving must come from the same feature store entity |
| Point-in-time correctness | All training datasets must use point-in-time joins to prevent future data leakage |
| Feature versioning | Features are versioned; models log the feature version they were trained on |
| Ownership | Every feature group has a named owner and domain classification |
| Freshness SLA | Feature freshness must match or exceed the model's serving requirement |

### 12.2 Feature Definition Standard

```python
# features/customer/customer_features.py
"""
Feature definitions for the customer domain.
All features documented with business meaning, owner, and freshness.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FeatureDefinition:
    name: str
    description: str
    dtype: str
    owner_team: str
    domain: str
    freshness_sla_hours: int
    pii: bool
    derivation_logic: str             # SQL or description of how feature is computed
    source_table: str
    nullable: bool = False
    approved_for_tiers: list = None   # Which model tiers may use this feature

    def __post_init__(self):
        if self.approved_for_tiers is None:
            self.approved_for_tiers = ["T1", "T2", "T3"]


# Documented feature catalog for customer domain
CUSTOMER_FEATURES = [
    FeatureDefinition(
        name="tenure_days",
        description="Number of days since the customer's account was first activated.",
        dtype="INTEGER",
        owner_team="sales-ml-team",
        domain="DOMAIN_SALES",
        freshness_sla_hours=24,
        pii=False,
        derivation_logic="DATEDIFF('day', account_created_at, CURRENT_DATE())",
        source_table="PROD_SALES_GOLD.sales.dim_customer"
    ),
    FeatureDefinition(
        name="avg_monthly_spend_usd",
        description="Average monthly spend in USD over the trailing 6 months. NULL if <2 months history.",
        dtype="FLOAT",
        owner_team="sales-ml-team",
        domain="DOMAIN_SALES",
        freshness_sla_hours=24,
        pii=False,
        derivation_logic="AVG(monthly_revenue_usd) OVER last 6 complete months",
        source_table="PROD_SALES_GOLD.sales.fact_revenue",
        nullable=True
    ),
]
```

---

## 13. Model Deployment & Serving Standards

### 13.1 Deployment Pattern Selection

| Pattern | Use Case | Platform | Latency | Cost |
|---|---|---|---|---|
| **REST API endpoint** | Real-time scoring, <500ms SLA | Databricks Model Serving, SageMaker Endpoint, FastAPI | Low | Medium-High |
| **Snowflake UDF** | In-database scoring, SQL callable | Snowflake Model Registry | Low | Low (compute in Snowflake) |
| **Batch scoring job** | Daily/weekly scores, no latency req. | Databricks Jobs, SageMaker Batch | N/A (offline) | Low |
| **Streaming scoring** | Near real-time (fraud, anomaly) | Databricks Structured Streaming | Near real-time | Medium |
| **Embedded in pipeline** | Score as part of ETL | dbt + UDF, Spark job | N/A | Low |

### 13.2 Model Card — Required for T1/T2

Every T1 and T2 model must have a published Model Card:

```markdown
# Model Card: Customer Churn Predictor

## Model Details
- **Name:** customer_churn_predictor
- **Version:** 4.2.0
- **Tier:** T2
- **Owner:** Sales ML Team | sales-ml@company.com
- **Algorithm:** Gradient Boosting (XGBoost)
- **Registry:** MLflow | Run ID: abc123def456

## Intended Use
- **Primary use:** Score all active customers monthly for 90-day churn risk
- **Intended users:** Sales operations team (for intervention campaigns)
- **Out-of-scope:** Not for credit decisions; not for legal determination of account status

## Training Data
- **Feature table:** prod_sales_gold.ml.customer_features_v3
- **Train period:** 2022-01-01 to 2023-12-31
- **Train size:** 284,000 customers
- **Target:** is_churned_90d (binary; 8.2% positive rate)

## Performance (Holdout Set — Q4 2023)
| Metric | Value | Gate | Pass? |
|--------|-------|------|-------|
| AUC-ROC | 0.863 | ≥0.80 | ✅ |
| F1 | 0.541 | ≥0.45 | ✅ |
| Precision@10% | 0.71 | ≥0.65 | ✅ |

## Limitations & Risks
- Model was not trained on customers acquired via the 2024 product line — accuracy may be lower for this cohort
- Predictions degrade materially if customer has <90 days tenure (flag in output)
- Not validated for geographic markets outside North America

## Bias Audit
- Bias audit completed: 2024-01-10
- 4/5 rule: PASS across all tested demographic dimensions
- Equalized odds: PASS

## Explainability
- SHAP values computed for all predictions
- Top 3 driving features logged per prediction
- Global feature importance: available in MLflow artifact

## Monitoring
- Drift monitoring: daily (Evidently AI)
- Performance review: monthly
- Retraining trigger: monthly or >10% drift on any top-5 feature
```

---

## 14. Monitoring & Drift Detection

### 14.1 Monitoring Framework

| Monitor Type | What It Detects | Frequency | Action on Alert |
|---|---|---|---|
| **Data drift** | Input feature distributions shifted from training | Daily | Investigate; trigger retraining if severe |
| **Target drift** | Distribution of outcomes shifting | Weekly | Investigate; flag for model review |
| **Prediction drift** | Distribution of model predictions shifting | Daily | Investigate; may indicate data or model issue |
| **Model performance** | AUC/MAE vs. labeled actuals (when available) | Monthly (or as labels arrive) | Retrain if below gate |
| **Data quality** | Missing values, type errors, out-of-range values | Daily | Block scoring if critical features missing |
| **Concept drift** | Relationship between features and target has changed | Monthly (performance gate) | Full model rebuild required |

### 14.2 Drift Alert Thresholds

```yaml
# monitoring/drift_thresholds.yaml
# Applied per model; defaults below — override in model config

defaults:
  data_drift:
    psi_threshold: 0.2              # PSI > 0.2 = significant drift
    js_divergence_threshold: 0.1   # Jensen-Shannon divergence
    share_of_drifted_cols_pct: 20  # Alert if >20% of features drifted
  prediction_drift:
    ks_statistic_threshold: 0.1
  performance_degradation:
    relative_auc_drop_pct: 5       # Alert if AUC drops >5% vs. launch baseline
    absolute_auc_floor: 0.75       # Alert regardless if AUC drops below this
  retraining_trigger:
    psi_threshold: 0.25            # Auto-trigger retraining job
    performance_drop_pct: 10       # Auto-trigger if performance drops >10%
```

---

*Document controlled by the Chief Data Office. Changes require approval from the ML Engineering Lead and Data Governance Lead.*
