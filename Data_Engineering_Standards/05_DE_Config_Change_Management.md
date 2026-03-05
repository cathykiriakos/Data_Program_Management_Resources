# Configuration-Based Practices & Change Management
## Working with IT Change Managers in the Modern Data Stack

**Document Owner:** Chief Data Office  
**Domain:** Data Engineering  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Config-First Architecture](#1-config-first-architecture)
2. [Configuration File Standards](#2-configuration-file-standards)
3. [Environment Parameterization](#3-environment-parameterization)
4. [Change Management Integration](#4-change-management-integration)
5. [Terraform State & Drift Management](#5-terraform-state--drift-management)
6. [CI/CD Pipeline Configuration](#6-cicd-pipeline-configuration)
7. [Config-Driven Pipeline Reference Implementation](#7-config-driven-pipeline-reference-implementation)
8. [Change Classification Reference](#8-change-classification-reference)

---

## 1. Config-First Architecture

### 1.1 Core Philosophy

> **Every value that could differ by environment, business rule, or operational need must live in a config file — never in code.**

This principle exists for three reasons:
1. **IT Change Management:** Configuration changes are reviewable, auditable, and reversible without code deployments.
2. **Environment promotion:** The same code runs in dev, staging, and prod — only config changes.
3. **Repeatability:** Any engineer can re-run any pipeline from any point in time by checking out the config at that point in Git history.

### 1.2 What Belongs in Config vs. Code

| Belongs in **Config** | Belongs in **Code** |
|---|---|
| Connection strings, database names, schema names | Extract/transform/load logic |
| Warehouse or cluster size | Data quality rule engine |
| Schedule (cron expression) | Retry handler |
| Source table names, watermark columns | Logging framework |
| Row count thresholds, quality rule parameters | Surrogate key generation |
| Notification targets (Slack channel, email) | Merge / upsert implementation |
| Data retention days | Authentication helper |
| Merge keys, write mode | SCD2 snapshot logic |
| Feature flags (enable_pii_masking, etc.) | Pipeline base class |

### 1.3 Config Hierarchy

```
base_config.yaml           ← Shared defaults (all environments)
    │
    ├── dev_config.yaml    ← Dev overrides (smaller warehouses, dev schemas)
    ├── staging_config.yaml ← Staging overrides (prod-like but isolated)
    └── prod_config.yaml   ← Production values
```

At runtime, configs are merged: base → environment-specific. Environment-specific values always win.

---

## 2. Configuration File Standards

### 2.1 Base Config Structure

Every pipeline must have a `base_config.yaml` with the following structure:

```yaml
# base_config.yaml
# ------------------------------------------------------------------
# Pipeline: finance_erp_bronze
# Owner: Finance Data Engineering
# Last Updated: 2024-01-15
# Change Ticket: CHG-2024-042 (if last change was IT-tracked)
# ------------------------------------------------------------------

pipeline:
  name: finance_erp_bronze_daily
  version: "3.2.1"            # Matches git tag
  description: "Daily incremental load of ERP GL transactions to Bronze layer"
  owner_team: finance-data-engineering
  owner_email: finance-data@company.com
  domain: DOMAIN_FINANCE
  
schedule:
  cron: "0 2 * * *"           # 2 AM UTC daily
  timezone: UTC
  enabled: true
  sla_minutes: 120            # Must complete within 120 minutes of schedule time

source:
  type: jdbc                  # jdbc | rest_api | s3_file | kafka | snowflake | databricks
  driver: com.microsoft.sqlserver.jdbc.SQLServerDriver
  watermark_column: UPDATED_AT
  watermark_type: timestamp   # timestamp | integer | date
  batch_size: 50000           # rows per batch

destination:
  layer: bronze               # bronze | silver | gold
  write_mode: append          # append | overwrite | merge | upsert
  
quality:
  enabled: true
  fail_pipeline_on_error: true
  
notifications:
  on_failure:
    channels: ["slack", "pagerduty"]
  on_sla_breach:
    channels: ["slack", "email"]
  on_success:
    channels: []              # No noise on success by default

retry:
  max_attempts: 3
  backoff_seconds: [30, 120, 300]   # Wait before each retry
  retry_on: ["ConnectionError", "TimeoutError", "SnowflakeError"]
```

### 2.2 Environment-Specific Config

```yaml
# prod_config.yaml
# Only specify values that DIFFER from base_config.yaml
# ------------------------------------------------------------------

pipeline:
  environment: production

source:
  connection_secret: "prod/jdbc/erp_finance"    # Secrets manager path
  database: FINANCE_PROD_DB
  schema: GL
  table: TRANSACTIONS
  watermark_state_store: "s3://prod-config-store/watermarks/finance_erp_gl.json"

destination:
  platform: snowflake
  account_secret: "prod/snowflake/svc_finance_loader"
  database: PROD_FINANCE_BRONZE
  schema: ERP
  table: GL_TRANSACTIONS

compute:
  platform: databricks
  workspace_secret: "prod/databricks/svc_finance"
  cluster_policy_id: "A1B2C3D4"              # From cluster policy IaC
  node_type: "m5d.2xlarge"
  min_workers: 2
  max_workers: 8
  spark_version: "15.4.x-scala2.12"

quality:
  checks:
    not_null:
      columns: ["TRANSACTION_ID", "TRANSACTION_DATE", "AMOUNT", "ACCOUNT_CODE"]
    unique:
      columns: ["TRANSACTION_ID"]
    accepted_range:
      AMOUNT:
        min: -99999999.99
        max: 99999999.99
    row_count:
      min_rows: 500
      max_variance_pct: 40

notifications:
  on_failure:
    slack_channel: "#data-alerts-prod"
    pagerduty_service: "finance-data-prod"
  on_sla_breach:
    slack_channel: "#data-alerts-prod"
    email_recipients: ["finance-data@company.com", "data-engineering@company.com"]
```

```yaml
# dev_config.yaml
pipeline:
  environment: development

source:
  connection_secret: "dev/jdbc/erp_finance"
  database: FINANCE_DEV_DB
  schema: GL
  table: TRANSACTIONS
  watermark_state_store: "s3://dev-config-store/watermarks/finance_erp_gl.json"

destination:
  platform: snowflake
  account_secret: "dev/snowflake/svc_finance_loader"
  database: DEV_FINANCE_BRONZE
  schema: ERP
  table: GL_TRANSACTIONS

compute:
  platform: databricks
  workspace_secret: "dev/databricks/svc_finance"
  cluster_policy_id: "DEV_POLICY_001"
  node_type: "m5d.xlarge"
  min_workers: 1
  max_workers: 2
  spark_version: "15.4.x-scala2.12"

quality:
  checks:
    not_null:
      columns: ["TRANSACTION_ID"]    # Looser in dev
    row_count:
      min_rows: 1
      max_variance_pct: 100          # No variance alert in dev

notifications:
  on_failure:
    slack_channel: "#data-dev-alerts"
  on_sla_breach:
    slack_channel: "#data-dev-alerts"
```

### 2.3 Config Loader Pattern (Python)

```python
# config_loader.py
"""
Config loader that merges base + environment config.
All pipelines use this; never load config ad hoc.
"""

import os
import yaml
from pathlib import Path
from typing import Any
from copy import deepcopy


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Override wins on conflicts."""
    merged = deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_pipeline_config(
    config_dir: str,
    env: str | None = None
) -> dict[str, Any]:
    """
    Load merged pipeline config.
    
    Args:
        config_dir: Path to directory containing base and env configs
        env: Environment name (dev/staging/prod). Reads ENV var if not provided.
    
    Returns:
        Merged configuration dictionary
    """
    env = env or os.environ.get("PIPELINE_ENV", "dev")
    config_path = Path(config_dir)

    # Load base config
    base_path = config_path / "base_config.yaml"
    if not base_path.exists():
        raise FileNotFoundError(f"Base config not found: {base_path}")

    with open(base_path) as f:
        base_config = yaml.safe_load(f)

    # Load environment override
    env_path = config_path / f"{env}_config.yaml"
    if not env_path.exists():
        raise FileNotFoundError(f"Environment config not found: {env_path}")

    with open(env_path) as f:
        env_config = yaml.safe_load(f)

    # Merge
    final_config = deep_merge(base_config, env_config)
    
    # Validate required fields
    _validate_config(final_config)
    
    return final_config


def _validate_config(config: dict) -> None:
    """Validate required config fields are present."""
    required_paths = [
        ("pipeline", "name"),
        ("pipeline", "version"),
        ("pipeline", "environment"),
        ("pipeline", "owner_team"),
        ("source", "type"),
        ("destination", "layer"),
        ("destination", "write_mode"),
    ]
    for path in required_paths:
        node = config
        for key in path:
            if key not in node:
                raise ValueError(
                    f"Missing required config field: {' -> '.join(path)}"
                )
            node = node[key]
```

---

## 3. Environment Parameterization

### 3.1 Snowflake — Terraform Parameterization

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "domain" {
  type        = string
  description = "Data domain"
}

variable "warehouse_sizes" {
  type = map(string)
  default = {
    dev     = "X-SMALL"
    staging = "SMALL"
    prod    = "LARGE"
  }
}

# main.tf
resource "snowflake_warehouse" "transform_wh" {
  name           = "${upper(var.environment)}_${upper(var.domain)}_TRANSFORM_WH"
  warehouse_size = var.warehouse_sizes[var.environment]
  auto_suspend   = var.environment == "prod" ? 120 : 60
  auto_resume    = true
  max_cluster_count = var.environment == "prod" ? 3 : 1
  
  tag {
    name  = "environment"
    value = var.environment
  }
  tag {
    name  = "managed_by"
    value = "terraform"
  }
}
```

### 3.2 Databricks — Terraform Parameterization

```hcl
# databricks_jobs.tf
resource "databricks_job" "finance_erp_bronze" {
  name = "finance_erp_bronze_daily_${var.environment}"

  job_cluster {
    job_cluster_key = "main_cluster"
    new_cluster {
      spark_version = "15.4.x-scala2.12"
      node_type_id  = var.environment == "prod" ? "m5d.2xlarge" : "m5d.xlarge"
      
      autoscale {
        min_workers = var.environment == "prod" ? 2 : 1
        max_workers = var.environment == "prod" ? 8 : 2
      }
      
      aws_attributes {
        instance_profile_arn = var.instance_profile_arn
      }
      
      spark_env_vars = {
        PIPELINE_ENV     = var.environment
        CONFIG_STORE_PATH = "s3://${var.environment}-config-store"
      }
    }
  }

  task {
    task_key = "main"
    job_cluster_key = "main_cluster"
    
    python_wheel_task {
      package_name = "finance_pipelines"
      entry_point  = "finance_erp_bronze"
      parameters   = ["--env", var.environment]
    }
  }

  schedule {
    quartz_cron_expression = "0 0 2 * * ?"   # 2 AM UTC
    timezone_id            = "UTC"
    pause_status           = var.environment == "prod" ? "UNPAUSED" : "PAUSED"
  }

  tags = {
    environment  = var.environment
    domain       = "finance"
    managed_by   = "terraform"
    cost_center  = var.cost_center
  }
}
```

---

## 4. Change Management Integration

### 4.1 Change Tier Decision Tree

```
Is this a data engineering change?
          │
          ▼
Does it affect PRODUCTION infrastructure 
(warehouses, clusters, network, RBAC, databases)?
     YES │                    NO │
         ▼                       ▼
 Does it affect          Does it affect 
 network, RBAC,         schemas, warehouse
 or new accounts?       sizing, new tables?
  YES │   NO │            YES │    NO │
      ▼       ▼               ▼        ▼
   MAJOR   MINOR           MINOR    STANDARD
  (CAB)   (DE Lead        (DE Lead  (PR Review
          + Change         Approval)  Only)
           Ticket)
```

### 4.2 Standard Change — No Ticket Required

Applies to: dbt model logic updates, new dbt tests, Python pipeline logic changes (not config), documentation updates.

**Process:**
1. Developer creates feature branch
2. Opens PR with description of change
3. Peer review by Senior DE or Analytics Engineer (required)
4. CI/CD gates pass (tests, linting, secret scan)
5. Merge to `main` → auto-deploys to prod

**Evidence required:** PR with approval, CI/CD pass log.

---

### 4.3 Minor Change — Change Ticket Required

Applies to: New source onboarding, schema additions, warehouse size changes, new pipelines, new database objects, schedule changes.

**Process:**
1. Developer creates feature branch + config changes
2. Opens PR → peer review + CI/CD pass
3. **Raises Minor Change Ticket** (template below)
4. DE Lead approves change ticket
5. Deploy to staging → attach staging test evidence to ticket
6. DE Lead signs off → deploy to prod
7. Post-deployment validation documented; ticket closed

**Change Ticket Template — Minor:**

```markdown
## Minor Change Request

**Ticket ID:** CHG-YYYY-NNN
**Requestor:** [Name]
**Date Submitted:** YYYY-MM-DD
**Target Deployment Date:** YYYY-MM-DD

### Change Description
[Plain-language description of what is changing and why]

### Affected Systems
- [ ] Snowflake: [database/schema/table/warehouse name]
- [ ] Databricks: [catalog/schema/table/job name]
- [ ] Cloud storage: [bucket/container]
- [ ] CI/CD: [pipeline name]
- [ ] Config files: [list changed files]

### Testing Evidence
- Staging deployment date: YYYY-MM-DD
- Row count comparison (staging vs expected): 
- Quality gate results: PASS / FAIL
- Screenshot/log attachment: [link]

### Rollback Plan
[Step-by-step rollback instructions — must be executable in < 30 minutes]

### Downstream Impact
- [ ] No downstream consumers affected
- [ ] Consumers notified (list and notification date):

### Approvals
- DE Lead: _____________ Date: _______
```

---

### 4.4 Major Change — CAB Review Required

Applies to: New platform accounts, network changes, RBAC restructure, new Snowflake/Databricks environments, external sharing, pricing tier changes, new cloud storage accounts.

**Additional requirements beyond Minor:**
- Full **technical design document** attached
- **Security review** from InfoSec (written sign-off)
- **Privacy review** if PII data scoping is changing
- **CAB presentation** (15-minute slot in change advisory board)
- **Rollback drill** documented (not just theoretical)
- **Communication plan** for affected consumers

**Lead time:** Minimum 10 business days.

---

### 4.5 Emergency / Hotfix Changes

For production incidents requiring an immediate fix:

1. Verbal approval from DE Lead (documented in incident channel)
2. Deploy fix
3. Raise retrospective change ticket within 24 hours
4. Post-incident review within 5 business days
5. Root cause and preventive action documented

---

## 5. Terraform State & Drift Management

### 5.1 Remote State Configuration

```hcl
# backend.tf — always use remote state; never local
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "data-platform/${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"    # Prevents concurrent applies
  }
}
```

### 5.2 Drift Detection Workflow

```yaml
# .github/workflows/drift_detection.yml
name: Terraform Drift Detection

on:
  schedule:
    - cron: '0 6 * * *'    # Run at 6 AM UTC daily

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
        
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ secrets[format('AWS_ROLE_{0}', matrix.environment)] }}
          
      - name: Terraform Init
        run: terraform init -backend-config="environments/${{ matrix.environment }}/backend.hcl"
        
      - name: Terraform Plan (Drift Check)
        id: plan
        run: |
          terraform plan -detailed-exitcode \
            -var-file="environments/${{ matrix.environment }}/terraform.tfvars" \
            -out=drift_plan.tfplan 2>&1 | tee plan_output.txt
          echo "exit_code=$?" >> $GITHUB_OUTPUT
          
      - name: Alert on Drift
        if: steps.plan.outputs.exit_code == '2'
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: '#data-platform-alerts'
          slack-message: |
            🚨 *Terraform Drift Detected* — ${{ matrix.environment }}
            Resources have changed outside of IaC.
            Plan output: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

---

## 6. CI/CD Pipeline Configuration

### 6.1 Full CI/CD Pipeline for dbt + Python Pipelines

```yaml
# .github/workflows/data_engineering_cicd.yml
name: Data Engineering CI/CD

on:
  pull_request:
    branches: [main, staging]
  push:
    branches: [main, staging]

env:
  PYTHON_VERSION: "3.11"

jobs:
  # ── 1. Code Quality ─────────────────────────────────────────────
  lint-and-format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff black isort
      - run: ruff check .
      - run: black --check .
      - run: isort --check-only .

  # ── 2. Secret Scanning ──────────────────────────────────────────
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # ── 3. Unit Tests ───────────────────────────────────────────────
  unit-tests:
    runs-on: ubuntu-latest
    needs: [lint-and-format, secret-scan]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit/ -v --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3

  # ── 4. dbt Compile & Test (Staging) ─────────────────────────────
  dbt-staging:
    runs-on: ubuntu-latest
    needs: [unit-tests]
    if: github.event_name == 'pull_request'
    environment: staging
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install dbt-snowflake
      - run: dbt deps
        working-directory: ./dbt
      - run: dbt compile --profiles-dir . --target staging
        working-directory: ./dbt
      - run: dbt test --profiles-dir . --target staging
        working-directory: ./dbt

  # ── 5. Deploy to Production ──────────────────────────────────────
  deploy-prod:
    runs-on: ubuntu-latest
    needs: [dbt-staging]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install dbt-snowflake
      - run: dbt run --profiles-dir . --target prod
        working-directory: ./dbt
      - run: dbt test --profiles-dir . --target prod
        working-directory: ./dbt
```

---

## 7. Config-Driven Pipeline Reference Implementation

Complete, runnable reference pipeline using all config patterns:

```python
# pipelines/finance_erp_bronze/src/pipeline.py

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

from config_loader import load_pipeline_config
from secrets_helper import get_secret
from quality_runner import run_quality_checks
from watermark_store import get_watermark, save_watermark
from notifications import send_alert


class FinanceErpBronzePipeline:
    """
    Config-driven, idempotent pipeline for ERP GL → Bronze.
    Extend BasePipeline for shared logging, run(), error handling.
    """

    def __init__(self, config_dir: str, env: str):
        self.config = load_pipeline_config(config_dir, env)
        self.pipeline_cfg = self.config["pipeline"]
        self.source_cfg = self.config["source"]
        self.dest_cfg = self.config["destination"]
        self.quality_cfg = self.config["quality"]
        self.notify_cfg = self.config["notifications"]
        
        self.batch_id = str(uuid.uuid4())
        self.run_start = datetime.now(timezone.utc)
        
        self.logger = logging.getLogger(self.pipeline_cfg["name"])
        self.spark = SparkSession.builder \
            .appName(self.pipeline_cfg["name"]) \
            .getOrCreate()

    def extract(self) -> DataFrame:
        """Incremental extract using watermark from state store."""
        creds = get_secret(self.source_cfg["connection_secret"])
        last_watermark = get_watermark(self.source_cfg["watermark_state_store"])
        
        self.logger.info(f"Extracting from watermark: {last_watermark}")
        
        df = self.spark.read.format("jdbc") \
            .option("url", creds["jdbc_url"]) \
            .option("dbtable", f"""
                (SELECT * FROM {self.source_cfg['schema']}.{self.source_cfg['table']}
                 WHERE {self.source_cfg['watermark_column']} > '{last_watermark}'
                ) AS src
            """) \
            .option("user", creds["username"]) \
            .option("password", creds["password"]) \
            .option("numPartitions", 8) \
            .option("fetchsize", self.source_cfg["batch_size"]) \
            .load()
        
        self.logger.info(f"Extracted {df.count()} rows.")
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        """Add standard Bronze audit columns."""
        return df \
            .withColumn("_batch_id", F.lit(self.batch_id)) \
            .withColumn("_source_system", F.lit(self.source_cfg.get("source_system", "ERP"))) \
            .withColumn("_ingested_at", F.current_timestamp()) \
            .withColumn("_pipeline_version", F.lit(self.pipeline_cfg["version"]))

    def load(self, df: DataFrame) -> None:
        """Write to destination using config-specified write mode."""
        dest_creds = get_secret(self.dest_cfg["account_secret"])
        table_name = (
            f"{self.dest_cfg['database']}.{self.dest_cfg['schema']}.{self.dest_cfg['table']}"
        )
        
        writer = df.write \
            .format("snowflake") \
            .options(**{
                "sfURL": dest_creds["account"],
                "sfUser": dest_creds["username"],
                "pem_private_key": dest_creds["private_key"],
                "sfDatabase": self.dest_cfg["database"],
                "sfSchema": self.dest_cfg["schema"],
                "sfWarehouse": dest_creds["warehouse"],
                "dbtable": self.dest_cfg["table"],
            })
        
        write_mode = self.dest_cfg["write_mode"]
        if write_mode == "append":
            writer.mode("append").save()
        elif write_mode == "overwrite":
            writer.mode("overwrite").save()
        else:
            raise ValueError(f"Unsupported write_mode: {write_mode}")
        
        self.logger.info(f"Loaded to {table_name} via {write_mode} mode.")

    def run(self) -> None:
        try:
            raw = self.extract()
            
            # Quality pre-check on source data
            if self.quality_cfg.get("enabled"):
                passed = run_quality_checks(raw, self.quality_cfg["checks"])
                if not passed and self.quality_cfg.get("fail_pipeline_on_error"):
                    raise ValueError("Quality checks failed on extracted data.")
            
            transformed = self.transform(raw)
            self.load(transformed)
            
            # Save watermark only after successful load
            new_watermark = raw.agg(
                F.max(self.source_cfg["watermark_column"])
            ).collect()[0][0]
            save_watermark(self.source_cfg["watermark_state_store"], str(new_watermark))
            
            self.logger.info(
                f"Pipeline completed successfully. "
                f"Duration: {(datetime.now(timezone.utc) - self.run_start).seconds}s"
            )
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}", exc_info=True)
            send_alert(
                config=self.notify_cfg["on_failure"],
                pipeline_name=self.pipeline_cfg["name"],
                error=str(e),
                batch_id=self.batch_id
            )
            raise


# Entrypoint
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, choices=["dev", "staging", "prod"])
    parser.add_argument("--config-dir", default="config")
    args = parser.parse_args()
    
    pipeline = FinanceErpBronzePipeline(
        config_dir=args.config_dir,
        env=args.env
    )
    pipeline.run()
```

---

## 8. Change Classification Reference

Quick-reference table for the Data Engineering team and IT Change Managers:

| Change Type | Tier | Lead Time | Approvers | CAB Required |
|---|---|---|---|---|
| dbt model logic update | Standard | Same day | PR Reviewer | No |
| New dbt model | Standard | Same day | PR Reviewer | No |
| Python transform logic change | Standard | Same day | PR Reviewer | No |
| Pipeline config change (schedule, thresholds) | Minor | 3–5 days | DE Lead | No |
| New Bronze pipeline (new source) | Minor | 3–5 days | DE Lead | No |
| New schema or table | Minor | 3–5 days | DE Lead | No |
| Warehouse size change | Minor | 3–5 days | DE Lead + Finance | No |
| New database or catalog | Minor | 5 days | DE Lead | No |
| RBAC role addition (non-admin) | Minor | 5 days | DE Lead + InfoSec | No |
| New RBAC hierarchy or role restructure | Major | 10–15 days | CDO + InfoSec + CAB | Yes |
| New Snowflake/Databricks account or workspace | Major | 10–15 days | CDO + InfoSec + CAB | Yes |
| Network configuration change (PrivateLink, VPC) | Major | 10–15 days | CDO + InfoSec + CAB | Yes |
| External data sharing (Snowflake Secure Share) | Major | 10–15 days | CDO + Legal + CAB | Yes |
| Cloud storage account creation | Major | 10–15 days | CDO + InfoSec + CAB | Yes |
| Platform pricing tier or contract change | Major | 15+ days | CDO + Finance + Procurement | Yes |
| Production data incident / hotfix | Emergency | Immediate | DE Lead (verbal) | Retrospective |

---

*This document is maintained by the Data Engineering Lead and reviewed with IT Change Management quarterly. Changes to the change tier classification require joint approval from the DE Lead and IT Change Management.*
