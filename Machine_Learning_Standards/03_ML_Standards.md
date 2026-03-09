# Machine Learning Standards
## Binding Standards for ML Development, Governance & Deployment

**Document Owner:** Chief Data Office  
**Domain:** Machine Learning  
**Version:** 1.0  
**Classification:** Internal — Binding Standard  
**Review Cycle:** Annual (or upon major platform or regulatory change)

---

> **Note:** These are binding standards. Exceptions require written approval from the ML Engineering Lead and Data Governance Lead. All exceptions are logged and reviewed quarterly.

---

## Table of Contents

1. [Experiment Tracking Standards](#1-experiment-tracking-standards)
2. [Data & Feature Standards](#2-data--feature-standards)
3. [Model Development Standards](#3-model-development-standards)
4. [Model Registry & Lifecycle Standards](#4-model-registry--lifecycle-standards)
5. [Deployment Standards](#5-deployment-standards)
6. [Monitoring Standards](#6-monitoring-standards)
7. [Governance & Documentation Standards](#7-governance--documentation-standards)
8. [Code & Reproducibility Standards](#8-code--reproducibility-standards)
9. [Cost Management Standards](#9-cost-management-standards)
10. [Zero-Tolerance Rules](#10-zero-tolerance-rules)

---

## 1. Experiment Tracking Standards

### STD-EXP-001: Every Run Must Be Tracked

**Standard:** Every model training run — including exploratory and failed runs — must be logged to the experiment tracking server (MLflow, SageMaker Experiments, or equivalent). Untracked training is prohibited in all environments above the developer sandbox.

**Rationale:** Untracked runs cannot be reproduced, audited, or compared. Regulators may require evidence of which model version was deployed and what data it was trained on.

---

### STD-EXP-002: Required Metadata on Every Run

**Standard:** Every training run must log the following tags (at minimum):

```
model.name, model.version, model.tier, model.domain
model.owner_team, model.use_case
data.feature_table, data.train_start, data.train_end
data.row_count, data.feature_hash
governance.pii_used, governance.bias_audit_done
env.python_version, git.commit, git.branch
```

Runs missing required metadata are flagged as non-compliant in the monthly governance scan.

---

### STD-EXP-003: Experiment Naming Convention

**Standard:** Experiments must follow the naming convention: `/{domain}/{model_name}/{env}`

```
/finance/revenue_forecast/prod
/sales/churn_predictor/prod
/risk/fraud_detector/prod
```

Experiments not following this convention will be moved or deleted during quarterly cleanup.

---

### STD-EXP-004: Artifact Logging

**Standard:** Every training run must log:
- Trained model artifact (with MLflow model signature)
- Data profile JSON (row count, column list, null counts, snapshot timestamp)
- `requirements.txt` or `conda.yaml` (environment reproducibility)
- Evaluation metrics (all metrics in the performance standards section)
- Feature importance (for tree-based and linear models)
- SHAP values artifact (T1 and T2 models)

---

## 2. Data & Feature Standards

### STD-DATA-001: Training Data Must Come from the Feature Store or Gold Layer

**Standard:** All training datasets must be sourced from:
1. A registered feature table in the feature store, OR
2. The Gold layer of the data platform (approved certified tables)

Direct queries to Bronze or Silver layers for training data require written approval from the DE Lead. Raw source system connections for training are prohibited.

---

### STD-DATA-002: Point-in-Time Correctness Mandatory

**Standard:** All training datasets must use point-in-time correct feature retrieval. No future data leakage is permitted. Every training pipeline must use a time-based split where the test period is strictly after the training period.

**Verification:** This is checked during the staging promotion review. Models with detectable future leakage cannot be promoted.

---

### STD-DATA-003: Training Data Must Be Versioned

**Standard:** Every production model training run must reference a versioned, immutable snapshot of training data. Versioning must be traceable — model registry must contain enough information to reconstruct the exact training dataset.

**Accepted approaches:**
- DVC (Data Version Control) hash logged to MLflow
- Delta Lake table snapshot (version number logged)
- SageMaker Feature Store query with `AsOfTime` parameter logged
- Snowflake time travel query timestamp logged

---

### STD-DATA-004: PII in Training Data — Documented Approval Required

**Standard:** Any model trained on PII-containing features requires:
- Written justification from the business owner
- Privacy Officer review and sign-off
- `governance.pii_used: true` tag in the training run
- PII features listed explicitly in the model card

**Additional requirement for T1 models using PII:** Legal review and sign-off.

---

### STD-DATA-005: No Training Data Older Than Policy Limit

**Standard:** Models may not be trained exclusively on data older than 3 years without documented business justification. For models used in regulated decisions (T1), training data currency must be reviewed at least annually.

---

## 3. Model Development Standards

### STD-DEV-001: Baseline Required Before Evaluation

**Standard:** Every model evaluation must include comparison to at least one documented baseline:
- Classification: prior probability classifier + a simple logistic regression
- Regression/Forecast: naive (last period) + seasonal naive
- Recommendation: most popular items
- Clustering: always report n_clusters and silhouette score relative to k-1 and k+1

Models that do not beat documented baselines cannot be promoted to Staging.

---

### STD-DEV-002: Hyperparameter Tuning Must Be Logged

**Standard:** All hyperparameter tuning runs must be logged in MLflow (not just the final run). This enables review of whether tuning was thorough and prevents p-hacking on validation data.

**Accepted methods:** MLflow + Optuna, MLflow + Hyperopt, SageMaker Automatic Model Tuning.

---

### STD-DEV-003: Hold-Out Test Set Integrity

**Standard:** The test set must not be used for any tuning decisions. One test set evaluation per model version is permitted. Multiple evaluations on the same test set contaminate results and constitute data leakage.

**Enforcement:** Senior ML Engineer or ML Engineering Lead must sign off on the test set evaluation as the final evaluation step.

---

### STD-DEV-004: Cross-Validation for Small Datasets

**Standard:** For datasets with fewer than 10,000 training rows, k-fold cross-validation (k ≥ 5) is required instead of a single train/test split. Results must be reported as mean ± standard deviation across folds.

---

### STD-DEV-005: Explainability Requirement by Tier

| Tier | Requirement | Method |
|---|---|---|
| T1 — Critical | Mandatory. Feature importance + SHAP values per prediction | SHAP (TreeExplainer for tree models; DeepExplainer for neural nets) |
| T2 — Significant | Global SHAP feature importance; local SHAP on request | SHAP or LIME |
| T3 — Standard | Global feature importance | Permutation importance or model-native |
| T4 — Exploratory | None | N/A |

---

### STD-DEV-006: Bias Audit for T1 Models

**Standard:** Every T1 model must pass a documented bias audit before production promotion. The audit must test:
- Demographic parity (4/5 rule) across all protected attributes available
- Equalized odds (TPR + FPR) across protected attribute groups
- AUC score comparison across protected attribute groups (max gap ≤ 5pp)

**Attestation:** ML Governance Analyst signs off on bias audit completion.

---

## 4. Model Registry & Lifecycle Standards

### STD-REG-001: All Production Models Must Be Registered

**Standard:** No model may serve predictions in production unless it is registered in the approved model registry (MLflow Model Registry with Unity Catalog, SageMaker Model Registry, or equivalent). Models deployed via ad hoc scripts or direct file copies are not permitted in production.

---

### STD-REG-002: Stage Promotion Gates

**Standard:** Promotion between registry stages requires documented gate passage:

| Transition | Required Evidence |
|---|---|
| None → Staging | Performance gates passed; data profile logged; required metadata complete |
| Staging → Production | Change ticket; domain owner approval; champion/challenger results (T1/T2); model card published |
| Production → Archived | Business owner notified; replacement model (if any) in production; scoring traffic drained |

---

### STD-REG-003: Model Governance Registry Entry

**Standard:** Every model in Production stage must have a corresponding entry in the Model Governance Registry (YAML in Git). The registry entry must include all fields defined in the Model Inventory standard.

Registry entries are audited monthly; gaps are HIGH findings.

---

### STD-REG-004: Model Retirement SLA

**Standard:** Models that fall below their performance gate threshold must be reviewed within 10 business days. Models confirmed as degraded must be retrained or retired within 30 business days.

Models below gate that are neither retrained nor retired after 30 business days are automatically archived and their serving endpoints suspended.

---

### STD-REG-005: Model Version Retention

**Standard:** Model artifacts (weights, parameters, signatures) must be retained for:
- T1 models: 7 years (or applicable regulatory retention period)
- T2 models: 3 years
- T3 models: 1 year after archival
- T4 models: No retention requirement; deleted upon sandbox cleanup

---

## 5. Deployment Standards

### STD-DEPLOY-001: CI/CD Required for Production Deployment

**Standard:** No model may be manually deployed to a production serving endpoint or batch scoring job. All production deployments must go through the approved CI/CD pipeline, which includes:
- Automated performance gate check
- Change ticket validation
- Deployment approval (signed off in the CI/CD system)
- Automated rollback capability

---

### STD-DEPLOY-002: Prediction Output Must Include Lineage Metadata

**Standard:** Every table or API response containing model predictions must include:
```
_model_name, _model_version, _model_run_id,
_feature_table, _scored_at, _prediction_id,
_confidence_score, _model_tier, _pipeline_version
```

Predictions without lineage metadata cannot be used for business decisions.

---

### STD-DEPLOY-003: Canary / Blue-Green Deployment for T1/T2

**Standard:** T1 and T2 model promotions must use a phased rollout:
1. Route 10% of traffic to new model; compare performance for 48 hours
2. If no degradation, increase to 50% for 24 hours
3. If no degradation, complete rollout to 100%
4. Prior model remains available for immediate rollback for 7 days after full rollout

---

### STD-DEPLOY-004: Latency SLA by Deployment Type

| Deployment Type | Target Latency | Maximum Latency | Alert Threshold |
|---|---|---|---|
| Real-time REST endpoint (T1) | < 100ms p50 | < 500ms p99 | p99 > 300ms |
| Real-time REST endpoint (T2/T3) | < 200ms p50 | < 1000ms p99 | p99 > 500ms |
| Snowflake UDF (batch inline) | < 500ms per row | — | Query > 10 minutes |
| Batch scoring job | Completes within SLA | Varies | Alert if >2x baseline |

---

### STD-DEPLOY-005: Rollback Capability

**Standard:** Every production model deployment must have a documented and tested rollback procedure that can restore the prior model version within 30 minutes.

The rollback procedure is tested at least once during the staging promotion phase.

---

## 6. Monitoring Standards

### STD-MON-001: Monitoring Mandatory for T1/T2

**Standard:** All T1 and T2 production models must have active monitoring configured and alerting enabled before the production promotion is approved. Monitoring includes:
- Data drift (daily)
- Prediction drift (daily)
- Model performance (monthly or when labels available)
- Data quality on incoming features (daily)

---

### STD-MON-002: Drift Alert Thresholds

**Standard:** Default thresholds (overridable in model config):

| Metric | Warning | Critical (retrain trigger) |
|---|---|---|
| PSI (Population Stability Index) | > 0.1 | > 0.25 |
| Share of drifted features | > 10% | > 25% |
| KS Statistic (feature) | > 0.05 | > 0.10 |
| Relative AUC drop vs. baseline | > 3% | > 8% |
| Absolute AUC floor | < 0.78 | < 0.72 |

---

### STD-MON-003: Monitoring Review Cadence

| Tier | Data Drift Review | Performance Review | Business KPI Review |
|---|---|---|---|
| T1 — Critical | Daily automated + weekly human | Monthly | Monthly |
| T2 — Significant | Daily automated + bi-weekly human | Monthly | Monthly |
| T3 — Standard | Weekly automated | Quarterly | Quarterly |

---

### STD-MON-004: Baseline Dataset Storage

**Standard:** A baseline dataset (representative sample of the training feature distribution) must be stored and versioned alongside every T1/T2 model. The baseline must be updated whenever the model is retrained. Baselines are used by the drift monitoring framework as the reference distribution.

---

## 7. Governance & Documentation Standards

### STD-GOV-001: Model Card Mandatory for T1/T2

**Standard:** Every T1 and T2 model must have a published and maintained model card covering:
- Model identity, version, owner, intended use, out-of-scope uses
- Training data description and date range
- Performance metrics on holdout set (vs. baseline and prior version)
- Limitations and known failure modes
- Bias audit results
- Explainability method and findings
- Monitoring summary and retraining schedule

Model cards are published in the data catalog and linked from the model registry entry.

---

### STD-GOV-002: Risk Assessment Mandatory for T1/T2

**Standard:** Every T1 and T2 model must have a completed, signed risk assessment before staging promotion. The risk assessment must use the standard ML Risk Assessment scorecard and be signed by the ML Governance Analyst.

---

### STD-GOV-003: Business KPI Defined Before Development Begins

**Standard:** Before any T1 or T2 model development begins, a business KPI must be documented and agreed upon with the business owner. Model development cannot be justified without a measurable business outcome.

This is enforced via the Model Development Brief template (submitted to ML Engineering Lead and business owner before development).

---

### STD-GOV-004: Change Ticket for Production Changes

**Standard:** All production model deployments, retraining runs that result in version promotion, and serving endpoint changes require a change ticket per the ML change management classification in this document.

---

## 8. Code & Reproducibility Standards

### STD-CODE-001: Python Version and Dependency Management

| Standard | Rule |
|---|---|
| Python version | 3.11+ |
| Dependency management | `requirements.txt` (pinned versions) or `pyproject.toml` + `uv` |
| Environment snapshot | `requirements.txt` logged as artifact on every training run |
| No unpinned dependencies | `scikit-learn>=1.3` is not allowed in training code; exact version required |
| Virtual environments | Always; never install into system Python |

---

### STD-CODE-002: No Hardcoded Values

**Standard:** The following must never be hardcoded in ML training or scoring code:
- File paths or table names
- Model hyperparameters (must be in config)
- Performance thresholds / gate values
- Environment names
- Credentials or API keys
- Column names (where configurable)

All of the above must be externalized to config files (`YAML` / `TOML`) per the config-first pattern.

---

### STD-CODE-003: Notebook Standards for ML

- Notebooks are for **experimentation and exploration** only. Production training pipelines are Python scripts or Databricks Jobs with `.py` entry points.
- No production scoring pipeline runs in a notebook.
- Notebooks must not contain hardcoded credentials.
- Before a notebook experiment is promoted, the logic must be refactored into a Python module with unit tests.

---

### STD-CODE-004: Random Seed Reproducibility

**Standard:** Every training run must use a fixed, logged random seed. The seed must be logged as a parameter in the experiment tracker. Runs without a logged seed cannot be reproduced and are flagged as non-compliant.

---

### STD-CODE-005: Unit Tests Required

**Standard:** Every ML module (transform, feature engineering, evaluation function) must have unit tests covering:
- Standard input → expected output
- Edge cases (empty dataframe, all-null column, single row)
- Invalid input → graceful error (not silent failure)

Minimum unit test coverage: 70% for T1/T2 pipeline code; 50% for T3.

---

## 9. Cost Management Standards

### STD-COST-001: Training Compute Must Be Tagged

**Standard:** Every training job (Databricks cluster, SageMaker training job, self-hosted compute) must carry these tags:
```
model_name, domain, environment, cost_center, managed_by, tier
```

Untagged resources are terminated in non-production environments within 24 hours.

---

### STD-COST-002: Auto-Termination on All Training Clusters

**Standard:** All training clusters must have auto-termination enabled:
- Development / exploratory: 30 minutes idle
- Training jobs: job-scoped clusters (terminated after job completion)
- GPU clusters: 15 minutes idle maximum

---

### STD-COST-003: Spot/Preemptible Instances for Training

**Standard:** T3 and T2 training jobs must use spot/preemptible instances where the workload allows. T1 model retraining may use on-demand instances if SLA requires guaranteed completion.

---

### STD-COST-004: Per-Model Cost Attribution

**Standard:** ML platform costs must be attributable per model within 30 days of program launch. The monthly ML cost dashboard must show:
- Compute cost by model
- Compute cost by domain
- Cost per prediction (batch scoring)
- Cost trend vs. prior month

---

## 10. Zero-Tolerance Rules

The following standards have **no exception pathway**. Violations are immediately escalated to the ML Engineering Lead and Data Governance Lead:

| Rule | Violation Action |
|---|---|
| Untracked model in production (no registry entry) | Immediate decommission; incident report |
| Training on PII without Privacy Officer approval | Immediate model suspension; incident report |
| T1 model in production without bias audit | Immediate suspension; bias audit required before reinstatement |
| Model artifact deleted before retention period | Security incident report; storage audit |
| Credentials or API keys in training code or notebooks committed to Git | Immediate credential rotation; access review |
| Production model deployed via manual script (no CI/CD) | Rollback required; incident report |
| T1/T2 model without active monitoring in production | Immediate escalation; 5-day remediation SLA |
| Test set reused for multiple evaluation iterations (p-hacking) | Model invalidated; full retrain required |

---

*These standards are binding. Non-compliance is escalated as defined above. Standards reviewed annually and upon major platform or regulatory changes.*
