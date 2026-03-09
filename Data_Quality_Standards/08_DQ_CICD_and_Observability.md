# Data Engineering Quality Engineering
## Document 8: CI/CD Integration, Observability & Production Operations
### Running Tests Automatically, Storing Results, Alerting, and Operating at Scale

**Document Owner:** Chief Data Office — Data Engineering  
**Domain:** Quality Engineering  
**Version:** 1.0  
**Who This Is For:** Data engineers ready to move from "tests that run locally" to "tests that run automatically, alert on failure, and produce governance-ready reports."

---

## Table of Contents

1. [The Production Testing Lifecycle](#1-the-production-testing-lifecycle)
2. [Pipeline Integration Patterns](#2-pipeline-integration-patterns)
3. [Airflow Integration — Complete Example](#3-airflow-integration--complete-example)
4. [Databricks Workflows Integration](#4-databricks-workflows-integration)
5. [Alert Design — Who Gets Notified, When, and How](#5-alert-design--who-gets-notified-when-and-how)
6. [The DQ Results Table — Design and Queries](#6-the-dq-results-table--design-and-queries)
7. [Observability — The DQ Dashboard](#7-observability--the-dq-dashboard)
8. [Test Result Trending and Anomaly Detection](#8-test-result-trending-and-anomaly-detection)
9. [SLA Monitoring at Scale](#9-sla-monitoring-at-scale)
10. [Managing Test Debt — What to Do When You Have Too Many Failures](#10-managing-test-debt--what-to-do-when-you-have-too-many-failures)
11. [The Complete Operations Runbook](#11-the-complete-operations-runbook)

---

## 1. The Production Testing Lifecycle

### 1.1 What Happens in Production

When a data pipeline runs in production, tests must integrate into the pipeline — not run separately. The sequence is:

```
┌──────────────────────────────────────────────────────────────────────┐
│  PRODUCTION PIPELINE RUN                                             │
│                                                                      │
│  1. EXTRACT                                                          │
│     Source → Bronze table                                            │
│     ↓                                                                │
│  2. BRONZE GATE (Tests run here)                                     │
│     ✅ Bronze schema tests pass → continue                           │
│     🚨 CRITICAL failure → STOP. Alert. Do not run Silver.           │
│     ⚠️  HIGH failure → Alert. Continue to Silver (but log).         │
│     ↓                                                                │
│  3. TRANSFORM                                                        │
│     Bronze → Silver (dbt run)                                       │
│     ↓                                                                │
│  4. SILVER GATE (Tests run here)                                     │
│     ✅ Silver tests pass → continue                                  │
│     🚨 CRITICAL failure → STOP. Alert. Do not update Gold.          │
│     ↓                                                                │
│  5. TRANSFORM                                                        │
│     Silver → Gold (dbt run)                                         │
│     ↓                                                                │
│  6. GOLD GATE (Tests run here)                                       │
│     ✅ Gold tests pass → mark pipeline successful                    │
│     🚨 CRITICAL failure → STOP. Alert. Mark pipeline failed.        │
│     Roll back Gold table to prior version.                           │
│     ↓                                                                │
│  7. STORE RESULTS                                                    │
│     All test results → DQ results table                             │
│     ↓                                                                │
│  8. NOTIFY                                                           │
│     Slack/email/PagerDuty based on severity and result              │
└──────────────────────────────────────────────────────────────────────┘
```

### 1.2 The Gate Pattern Explained

A **quality gate** is a checkpoint that decides whether the pipeline should proceed. Think of it like a quality inspector on an assembly line — if the part doesn't pass inspection, it doesn't proceed to the next station.

Without gates: Bad Bronze data becomes bad Silver data becomes bad Gold data that reaches dashboards.  
With gates: Bad Bronze data is caught at the first checkpoint. The dashboard never sees it.

The key design decision: **which tests are gates and which are monitors?**

| Type | When | Action on Failure |
|---|---|---|
| **Gate test** | Runs in-pipeline; blocks if it fails | Stop pipeline; alert team |
| **Monitor test** | Runs after pipeline completes; never blocks | Log result; alert if bad |

**Gate tests:** Completeness of primary keys, uniqueness of primary keys, existence of required columns, referential integrity for T1 consumers  
**Monitor tests:** Statistical distribution tests, volume day-over-day, freshness SLA, mean stability

---

## 2. Pipeline Integration Patterns

### 2.1 The Quality Gate Function

```python
# quality/gate.py
"""
A quality gate is a function you call at any point in your pipeline.
It runs a set of tests, evaluates the results, and either continues
or raises an exception to stop the pipeline.

HOW TO USE:
    gate = QualityGate("bronze_orders_gate", block_on=["CRITICAL"])
    gate.check(test_schema_all_columns_present, df, required_cols, "bronze.raw_orders")
    gate.check(test_completeness_not_null, df, "order_id", "bronze.raw_orders")
    gate.evaluate()   # Raises if any CRITICAL tests failed
"""

from __future__ import annotations
import logging
from typing import Callable

from .result import TestResult
from .runner import DataQualitySuiteRunner, DataQualityError
from .reporter import ResultReporter


class QualityGate:
    """
    A named quality checkpoint in a pipeline.
    Collects test results and decides whether to proceed.
    """

    def __init__(
        self,
        gate_name: str,
        environment: str = "prod",
        pipeline_run_id: str = "",
        block_on: list[str] = None,
        reporter: ResultReporter | None = None,
        notifier=None
    ):
        self.runner = DataQualitySuiteRunner(
            suite_name=gate_name,
            environment=environment,
            pipeline_run_id=pipeline_run_id,
            block_on_severity=block_on or ["CRITICAL"],
            reporter=reporter
        )
        self.notifier = notifier
        self.gate_name = gate_name
        self.logger = logging.getLogger(f"QualityGate.{gate_name}")

    def check(self, test_fn: Callable, *args, **kwargs) -> TestResult:
        """Run one test and add it to this gate's results."""
        return self.runner.run(test_fn, *args, **kwargs)

    def evaluate(self) -> bool:
        """
        Finalize the gate.
        Returns True if the pipeline should proceed.
        Raises DataQualityError if blocking tests failed.
        """
        try:
            suite_result = self.runner.finalize()
            if self.notifier:
                self.notifier.notify_on_warnings(suite_result)
            return True
        except DataQualityError as e:
            if self.notifier:
                self.notifier.notify_critical_failure(self.gate_name, str(e))
            raise  # Re-raise to stop the pipeline
```

### 2.2 Integrating into a Standard Pipeline

```python
# pipelines/orders_pipeline.py
"""
The complete orders ingestion and transformation pipeline
with quality gates at each layer.
"""

import os
import uuid
from datetime import datetime, timezone

import pandas as pd

from quality.gate import QualityGate
from quality.validators import (
    test_schema_all_columns_present,
    test_schema_column_type,
    test_completeness_not_null,
    test_uniqueness_no_duplicates,
    test_validity_in_set,
    test_validity_range,
    test_freshness_max_age,
    test_volume_day_over_day,
    test_statistical_mean_stability,
    test_aggregate_row_count,
)
from quality.reporter import ResultReporter
from quality.notifier import SlackNotifier
from quality.loader import load_tests_from_config
from data.connectors import SnowflakeConnector


def run_orders_pipeline(env: str = "prod") -> dict:
    """
    End-to-end orders pipeline with quality gates.
    Returns a summary dict with pipeline status and test results.
    """
    pipeline_run_id = str(uuid.uuid4())
    run_start = datetime.now(timezone.utc)

    # Setup shared infrastructure
    conn = SnowflakeConnector(env=env)
    reporter = ResultReporter(
        connection=conn.engine,
        table="data_quality.pipeline_test_results"
    )
    notifier = SlackNotifier(
        webhook_url=os.environ["SLACK_WEBHOOK_DQ_ALERTS"],
        channel="#data-quality-alerts",
        environment=env
    )

    print(f"[{pipeline_run_id}] Starting orders pipeline — {env}")

    # ── STEP 1: Extract ────────────────────────────────────────────
    print("Extracting from source system...")
    raw_df = conn.query("SELECT * FROM source_system.orders WHERE updated_at >= SYSDATE() - INTERVAL '2 HOURS'")

    # ── GATE 1: Bronze / Ingestion Gate ───────────────────────────
    print("Running Bronze quality gate...")
    bronze_gate = QualityGate(
        gate_name="bronze_orders_gate",
        environment=env,
        pipeline_run_id=pipeline_run_id,
        block_on=["CRITICAL"],         # Only CRITICAL failures stop the pipeline
        reporter=reporter,
        notifier=notifier
    )

    # Load tests from config (YAML-driven)
    bronze_tests = load_tests_from_config(
        "config/bronze/raw_orders.yaml",
        raw_df
    )
    for test_fn in bronze_tests:
        bronze_gate.check(test_fn)

    bronze_gate.evaluate()   # 🚨 Raises here if CRITICAL tests failed
    print("✅ Bronze gate passed.")

    # ── STEP 2: Transform Bronze → Silver ─────────────────────────
    print("Transforming Bronze → Silver...")
    silver_df = transform_to_silver(raw_df)

    # ── GATE 2: Silver Gate ────────────────────────────────────────
    print("Running Silver quality gate...")
    silver_gate = QualityGate(
        gate_name="silver_orders_gate",
        environment=env,
        pipeline_run_id=pipeline_run_id,
        block_on=["CRITICAL"],
        reporter=reporter,
        notifier=notifier
    )

    silver_tests = load_tests_from_config("config/silver/stg_orders.yaml", silver_df)
    for test_fn in silver_tests:
        silver_gate.check(test_fn)

    silver_gate.evaluate()
    print("✅ Silver gate passed.")

    # ── STEP 3: Transform Silver → Gold ───────────────────────────
    print("Transforming Silver → Gold...")
    gold_df = transform_to_gold(silver_df)

    # ── GATE 3: Gold Gate ──────────────────────────────────────────
    print("Running Gold quality gate...")
    gold_gate = QualityGate(
        gate_name="gold_orders_gate",
        environment=env,
        pipeline_run_id=pipeline_run_id,
        block_on=["CRITICAL", "HIGH"],  # Gold is stricter — HIGH also blocks
        reporter=reporter,
        notifier=notifier
    )

    gold_tests = load_tests_from_config("config/gold/fact_orders.yaml", gold_df)
    for test_fn in gold_tests:
        gold_gate.check(test_fn)

    # Volume comparison vs. yesterday
    yesterday_count = conn.scalar(
        "SELECT COUNT(*) FROM gold.fact_orders WHERE DATE(order_date) = CURRENT_DATE() - 1"
    )
    gold_gate.check(
        test_volume_day_over_day,
        today_count=len(gold_df),
        yesterday_count=yesterday_count,
        table="gold.fact_orders",
        max_drop_pct=30.0,
        severity="HIGH"
    )

    gold_gate.evaluate()
    print("✅ Gold gate passed.")

    # ── STEP 4: Load Gold ──────────────────────────────────────────
    conn.write(gold_df, "gold.fact_orders", mode="merge", merge_key="order_id")

    run_end = datetime.now(timezone.utc)
    duration_sec = (run_end - run_start).total_seconds()

    summary = {
        "pipeline_run_id": pipeline_run_id,
        "status": "SUCCESS",
        "duration_sec": duration_sec,
        "rows_loaded": len(gold_df),
        "run_at": run_start.isoformat()
    }
    print(f"✅ Pipeline complete. {len(gold_df):,} rows loaded in {duration_sec:.1f}s")
    return summary


def transform_to_silver(df: pd.DataFrame) -> pd.DataFrame:
    """Cleanse and deduplicate Bronze → Silver."""
    return (
        df
        .drop_duplicates(subset=["order_id"], keep="last")
        .assign(
            amount_usd=lambda x: x.apply(lambda r: r["amount"] * get_fx_rate(r["currency"]), axis=1),
            status=lambda x: x["status"].str.lower().str.strip(),
            created_at=lambda x: pd.to_datetime(x["created_at"], utc=True)
        )
        .dropna(subset=["order_id", "customer_id"])
    )


def transform_to_gold(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich Silver → Gold."""
    from pandas.tseries.offsets import QuarterBegin
    return df.assign(
        order_date=lambda x: x["created_at"].dt.date,
        status_normalized=lambda x: x["status"].map(STATUS_NORMALIZATION_MAP).fillna(x["status"]),
        fiscal_quarter=lambda x: x["created_at"].dt.to_period("Q").astype(str),
        _created_at=datetime.now(timezone.utc)
    )


STATUS_NORMALIZATION_MAP = {
    "completed": "completed", "complete": "completed", "COMPLETED": "completed",
    "cancelled": "cancelled", "canceled": "cancelled", "CANCELLED": "cancelled",
    "pending": "pending", "PENDING": "pending",
    "processing": "processing", "in_process": "processing",
    "shipped": "shipped", "SHIPPED": "shipped", "in_transit": "shipped",
}


def get_fx_rate(currency: str) -> float:
    """Get USD conversion rate for a currency. In production: call FX API."""
    rates = {"USD": 1.0, "EUR": 1.08, "GBP": 1.27, "CAD": 0.74, "AUD": 0.65}
    return rates.get(currency.upper(), 1.0)  # Default 1.0 for unknown currencies
```

---

## 3. Airflow Integration — Complete Example

```python
# airflow/dags/orders_pipeline_dag.py
"""
Airflow DAG for the orders pipeline with integrated quality gates.

HOW TESTS INTEGRATE INTO AIRFLOW:
    - Each quality gate is its own Airflow task.
    - If a gate task fails, downstream tasks are automatically blocked by Airflow.
    - No custom blocking logic needed — Airflow's task dependency graph does the work.

DAG STRUCTURE:
    extract_orders
        ↓
    gate_bronze_orders          ← If this fails, nothing downstream runs
        ↓
    transform_to_silver
        ↓
    gate_silver_orders          ← If this fails, gold transform doesn't run
        ↓
    transform_to_gold
        ↓
    gate_gold_orders            ← If this fails, load doesn't happen
        ↓
    load_gold_orders
        ↓
    notify_success
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

import sys
sys.path.insert(0, "/opt/airflow/dags/pipelines")


DEFAULT_ARGS = {
    "owner":            "data-engineering",
    "depends_on_past":  False,
    "email_on_failure": True,
    "email":            ["data-alerts@company.com"],
    "retries":          1,
    "retry_delay":      timedelta(minutes=5),
}

with DAG(
    dag_id="orders_pipeline_with_quality_gates",
    default_args=DEFAULT_ARGS,
    description="Orders ingestion and transformation with DQ gates",
    schedule_interval="0 * * * *",     # Hourly
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["orders", "data-quality", "critical"],
) as dag:

    # ── Extract ────────────────────────────────────────────────────
    def extract_orders(**context):
        """Extract orders from source system and store to Bronze."""
        from pipelines.extract import extract_to_bronze
        run_id = context["run_id"]
        row_count = extract_to_bronze(run_id=run_id)
        # Push row_count to XCom for downstream tasks
        context["task_instance"].xcom_push(key="bronze_row_count", value=row_count)

    extract_task = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_orders,
    )

    # ── Bronze Quality Gate ────────────────────────────────────────
    def run_bronze_gate(**context):
        """
        Run quality gate on freshly extracted Bronze data.
        Reads from the Bronze table just written (not from XCom).

        WHY READ FROM TABLE (not XCom DataFrame):
            XCom can't hold large DataFrames efficiently.
            Reading from the table also ensures we test the
            WRITTEN data, not the in-memory pre-write data.
        """
        from quality.gate import QualityGate
        from quality.loader import load_tests_from_config
        from data.connectors import SnowflakeConnector
        from quality.reporter import ResultReporter
        from quality.notifier import SlackNotifier

        run_id = context["run_id"]
        conn = SnowflakeConnector(env="prod")

        # Load only today's Bronze rows for testing
        df = conn.query(
            "SELECT * FROM bronze.raw_orders "
            "WHERE DATE(_ingested_at) = CURRENT_DATE() "
            "LIMIT 100000"
        )

        gate = QualityGate(
            gate_name="bronze_orders_gate",
            environment="prod",
            pipeline_run_id=run_id,
            block_on=["CRITICAL"],
            reporter=ResultReporter(conn.engine, "data_quality.pipeline_test_results"),
            notifier=SlackNotifier(
                Variable.get("SLACK_DQ_WEBHOOK"),
                channel="#data-quality-prod"
            )
        )

        tests = load_tests_from_config("config/bronze/raw_orders.yaml", df)
        for test_fn in tests:
            gate.check(test_fn)

        gate.evaluate()  # Raises AirflowException if CRITICAL failures → blocks DAG

    bronze_gate_task = PythonOperator(
        task_id="gate_bronze_orders",
        python_callable=run_bronze_gate,
        # On failure: mark task red, alert team, block downstream
    )

    # ── dbt Silver Transform ───────────────────────────────────────
    dbt_silver_task = BashOperator(
        task_id="transform_to_silver",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt run --select stg_orders --target prod --store-failures"
        )
    )

    # ── Silver Quality Gate (via dbt test) ─────────────────────────
    dbt_silver_test_task = BashOperator(
        task_id="gate_silver_orders",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt test --select stg_orders --target prod --store-failures"
        )
    )

    # ── dbt Gold Transform ─────────────────────────────────────────
    dbt_gold_task = BashOperator(
        task_id="transform_to_gold",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt run --select fact_orders agg_daily_revenue --target prod --store-failures"
        )
    )

    # ── Gold Quality Gate ──────────────────────────────────────────
    dbt_gold_test_task = BashOperator(
        task_id="gate_gold_orders",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt test --select fact_orders agg_daily_revenue --target prod --store-failures"
        )
    )

    # ── Success Notification ───────────────────────────────────────
    def notify_success(**context):
        from quality.notifier import SlackNotifier
        notifier = SlackNotifier(Variable.get("SLACK_DQ_WEBHOOK"), "#data-pipelines-prod")
        notifier.notify_success("orders_pipeline", context["run_id"])

    notify_task = PythonOperator(
        task_id="notify_success",
        python_callable=notify_success,
        trigger_rule="all_success",
    )

    # ── Task Dependencies ──────────────────────────────────────────
    (
        extract_task
        >> bronze_gate_task
        >> dbt_silver_task
        >> dbt_silver_test_task
        >> dbt_gold_task
        >> dbt_gold_test_task
        >> notify_task
    )
```

---

## 4. Databricks Workflows Integration

```python
# databricks/workflows/orders_workflow.py
"""
Databricks Workflow definition using the Databricks SDK.
Each quality gate is a separate task with declared dependencies.

EQUIVALENT CONCEPT TO AIRFLOW DAGS:
    Databricks Workflows are Databricks' native orchestration.
    The quality gate pattern is identical — each gate is a task
    that blocks downstream tasks if it fails.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import (
    Task, NotebookTask, PythonWheelTask, JobCluster,
    TaskDependency, JobSettings
)


def create_orders_workflow(
    workspace_url: str,
    token: str,
    cluster_policy_id: str
) -> int:
    """
    Create the orders pipeline workflow in Databricks.
    Returns the job_id of the created workflow.
    """
    w = WorkspaceClient(host=workspace_url, token=token)

    job_settings = JobSettings(
        name="Orders Pipeline with Quality Gates",
        tasks=[
            Task(
                task_key="extract_orders",
                python_wheel_task=PythonWheelTask(
                    package_name="pipelines",
                    entry_point="extract_orders",
                    parameters=["--env", "prod"]
                ),
                job_cluster_key="standard_cluster"
            ),
            Task(
                task_key="gate_bronze_orders",
                depends_on=[TaskDependency(task_key="extract_orders")],
                python_wheel_task=PythonWheelTask(
                    package_name="quality",
                    entry_point="run_gate",
                    parameters=[
                        "--gate-name", "bronze_orders_gate",
                        "--config", "config/bronze/raw_orders.yaml",
                        "--table", "bronze.raw_orders",
                        "--env", "prod"
                    ]
                ),
                job_cluster_key="standard_cluster"
            ),
            Task(
                task_key="dbt_silver",
                depends_on=[TaskDependency(task_key="gate_bronze_orders")],
                notebook_task=NotebookTask(
                    notebook_path="/Shared/pipelines/dbt_silver_orders",
                    base_parameters={"dbt_command": "dbt run --select stg_orders"}
                ),
                job_cluster_key="standard_cluster"
            ),
            Task(
                task_key="gate_silver_orders",
                depends_on=[TaskDependency(task_key="dbt_silver")],
                notebook_task=NotebookTask(
                    notebook_path="/Shared/pipelines/dbt_silver_orders",
                    base_parameters={"dbt_command": "dbt test --select stg_orders --store-failures"}
                ),
                job_cluster_key="standard_cluster"
            ),
            Task(
                task_key="dbt_gold",
                depends_on=[TaskDependency(task_key="gate_silver_orders")],
                notebook_task=NotebookTask(
                    notebook_path="/Shared/pipelines/dbt_gold_orders",
                    base_parameters={"dbt_command": "dbt run --select fact_orders+"}
                ),
                job_cluster_key="standard_cluster"
            ),
            Task(
                task_key="gate_gold_orders",
                depends_on=[TaskDependency(task_key="dbt_gold")],
                notebook_task=NotebookTask(
                    notebook_path="/Shared/pipelines/dbt_gold_orders",
                    base_parameters={"dbt_command": "dbt test --select fact_orders+ --store-failures"}
                ),
                job_cluster_key="standard_cluster"
            ),
        ],
        job_clusters=[
            JobCluster(
                job_cluster_key="standard_cluster",
                new_cluster={
                    "cluster_policy_id": cluster_policy_id,
                    "spark_version": "15.4.x-scala2.12",
                    "node_type_id": "m5d.xlarge",
                    "autoscale": {"min_workers": 2, "max_workers": 8}
                }
            )
        ],
        email_notifications={
            "on_failure": ["data-engineering@company.com"],
            "no_alert_for_skipped_runs": True
        }
    )

    job = w.jobs.create(**job_settings.__dict__)
    print(f"Created workflow job_id: {job.job_id}")
    return job.job_id
```

---

## 5. Alert Design — Who Gets Notified, When, and How

### 5.1 Alert Fatigue Is a Real Risk

The biggest failure mode of a DQ alerting system is **alert fatigue** — so many alerts that the team starts ignoring them. Design alerts so that:
- Every alert requires human action
- The alert contains enough context to act without debugging
- Alerts are routed to the right people (not everyone gets everything)

### 5.2 The Notifier Class

```python
# quality/notifier.py
"""
Notification system for DQ alerts.

DESIGN PRINCIPLES:
    1. CRITICAL alerts → PagerDuty (page on-call, even at 3 AM)
    2. HIGH alerts → Slack #data-quality-alerts (urgent but not page-worthy)
    3. MEDIUM alerts → Slack #data-quality-daily (daily digest)
    4. LOW alerts → Stored in DB only (reviewed in weekly report)
    5. SUCCESS → Slack #data-pipelines-prod (visible but not urgent)
"""

import json
import os
import requests
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class AlertMessage:
    title: str
    body: str
    severity: str
    pipeline: str
    environment: str
    run_id: str
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


class SlackNotifier:
    """Send DQ alerts to Slack channels."""

    def __init__(self, webhook_url: str, channel: str, environment: str = "prod"):
        self.webhook_url = webhook_url
        self.channel = channel
        self.environment = environment

    def notify_critical_failure(self, gate_name: str, error_message: str, run_id: str = "") -> None:
        """
        Send a CRITICAL failure alert.
        Format: clear, actionable, includes direct link to failing test details.
        """
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🚨 CRITICAL: Pipeline Blocked"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Gate:*\n{gate_name}"},
                    {"type": "mrkdwn", "text": f"*Environment:*\n{self.environment.upper()}"},
                    {"type": "mrkdwn", "text": f"*Run ID:*\n`{run_id[:12]}...`" if run_id else "*Run ID:*\nN/A"},
                    {"type": "mrkdwn", "text": f"*Time:*\n{datetime.now(timezone.utc).strftime('%H:%M UTC')}"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Error:*\n```{error_message[:500]}```"}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "*Action Required:*\n"
                        "1. Check the failing tests in the DQ dashboard\n"
                        "2. Determine root cause (source system change? pipeline bug?)\n"
                        "3. Either fix the data issue or acknowledge and override if intentional\n"
                        f"4. Rerun pipeline after fix"
                    )
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "📊 View DQ Dashboard"},
                        "url": f"https://company.retool.com/apps/dq-dashboard?run_id={run_id}",
                        "style": "danger"
                    }
                ]
            }
        ]
        self._send({"channel": self.channel, "blocks": blocks})

    def notify_on_warnings(self, suite_result) -> None:
        """Send a summary of non-critical warnings."""
        failed_tests = [r for r in suite_result.all_results if not r.passed]
        if not failed_tests:
            return

        warning_tests = [r for r in failed_tests if r.severity in ("HIGH", "MEDIUM")]
        if not warning_tests:
            return

        summary_lines = [
            f"• `{r.test_name}` ({r.severity}): {r.failing_count:,} rows failed"
            for r in warning_tests[:10]
        ]
        if len(warning_tests) > 10:
            summary_lines.append(f"  _(and {len(warning_tests) - 10} more...)_")

        self._send({
            "channel": self.channel,
            "text": (
                f"⚠️ *DQ Warnings — {suite_result.suite_name}*\n"
                f"Environment: {suite_result.environment.upper()} | "
                f"Run: `{suite_result.run_at[:10]}`\n\n"
                + "\n".join(summary_lines)
            )
        })

    def notify_success(self, pipeline_name: str, run_id: str) -> None:
        """Send a success notification (lower urgency)."""
        self._send({
            "channel": self.channel,
            "text": (
                f"✅ *{pipeline_name}* completed successfully "
                f"[{datetime.now(timezone.utc).strftime('%H:%M UTC')}]"
            )
        })

    def _send(self, payload: dict) -> None:
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            # Never let notification failure break the pipeline
            import logging
            logging.getLogger(__name__).warning(f"Slack notification failed: {e}")
```

### 5.3 Alert Routing by Severity

```yaml
# config/alerting.yaml
# Defines who gets notified for each severity level and pipeline

routing:
  CRITICAL:
    channels:
      - type: pagerduty
        service_key: "${PAGERDUTY_DQ_SERVICE_KEY}"
        urgency: high
      - type: slack
        webhook: "${SLACK_DQ_CRITICAL_WEBHOOK}"
        channel: "#data-quality-critical"
    conditions:
      environments: [prod]    # Only page in production
      hours: all              # Page anytime — critical is critical

  HIGH:
    channels:
      - type: slack
        webhook: "${SLACK_DQ_ALERTS_WEBHOOK}"
        channel: "#data-quality-alerts"
    conditions:
      environments: [prod, staging]
      hours: business          # 7 AM – 10 PM local

  MEDIUM:
    channels:
      - type: slack
        webhook: "${SLACK_DQ_DAILY_WEBHOOK}"
        channel: "#data-quality-daily"
        digest: true           # Batch medium alerts into daily digest (not immediate)
    conditions:
      environments: [prod]

  LOW:
    channels: []               # Log to DB only; reviewed in weekly governance report
```

---

## 6. The DQ Results Table — Design and Queries

### 6.1 DDL for the Results Table

```sql
-- Create this table before any pipelines run
-- This is the foundation of your DQ observability

CREATE TABLE IF NOT EXISTS data_quality.pipeline_test_results (
    -- Test identity
    test_id             VARCHAR(500)    NOT NULL,          -- Unique test identifier
    test_name           VARCHAR(500)    NOT NULL,
    test_type           VARCHAR(100),                       -- not_null | unique | range | etc.
    suite_name          VARCHAR(200),

    -- What was tested
    table_name          VARCHAR(500),
    column_name         VARCHAR(200),
    layer               VARCHAR(20),                        -- bronze | silver | gold

    -- Results
    passed              BOOLEAN         NOT NULL,
    severity            VARCHAR(20),                        -- CRITICAL | HIGH | MEDIUM | LOW
    failing_count       INTEGER         DEFAULT 0,
    total_count         INTEGER         DEFAULT 0,
    failing_pct         FLOAT           DEFAULT 0.0,
    message             TEXT,

    -- Context
    pipeline_run_id     VARCHAR(200),
    environment         VARCHAR(50),
    run_at              TIMESTAMP_TZ    NOT NULL,

    -- Partitioning (for Snowflake/Databricks performance)
    run_date            DATE            GENERATED ALWAYS AS (run_at::DATE),

    -- Metadata
    _inserted_at        TIMESTAMP_TZ    DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY (run_date, table_name);      -- Optimize for date-range and table queries
```

### 6.2 Essential Operational Queries

```sql
-- ── Query 1: Today's test results summary ────────────────────────────────────
SELECT
    layer,
    severity,
    COUNT(*)                                                        AS total_tests,
    SUM(CASE WHEN passed THEN 1 ELSE 0 END)                         AS passed,
    SUM(CASE WHEN NOT passed THEN 1 ELSE 0 END)                     AS failed,
    ROUND(AVG(CASE WHEN passed THEN 100.0 ELSE 0 END), 1)           AS pass_rate_pct
FROM data_quality.pipeline_test_results
WHERE run_date = CURRENT_DATE()
  AND environment = 'prod'
GROUP BY 1, 2
ORDER BY
    CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2
                  WHEN 'MEDIUM'   THEN 3 WHEN 'LOW'  THEN 4 END,
    CASE layer WHEN 'gold' THEN 1 WHEN 'silver' THEN 2 WHEN 'bronze' THEN 3 END;


-- ── Query 2: Open failures (failed today, not resolved) ──────────────────────
SELECT
    test_name,
    table_name,
    column_name,
    severity,
    failing_count,
    total_count,
    ROUND(failing_pct, 2)                                           AS failing_pct,
    message
FROM data_quality.pipeline_test_results
WHERE run_date = CURRENT_DATE()
  AND environment = 'prod'
  AND NOT passed
ORDER BY
    CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2
                  WHEN 'MEDIUM' THEN 3 ELSE 4 END,
    failing_count DESC;


-- ── Query 3: 30-day pass rate trend ─────────────────────────────────────────
SELECT
    run_date,
    COUNT(*)                                                        AS total_tests,
    SUM(CASE WHEN NOT passed AND severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_failures,
    SUM(CASE WHEN NOT passed AND severity = 'HIGH' THEN 1 ELSE 0 END)     AS high_failures,
    ROUND(AVG(CASE WHEN passed THEN 100.0 ELSE 0 END), 2)           AS overall_pass_rate_pct,
    ROUND(AVG(CASE WHEN passed AND severity = 'CRITICAL' THEN 100.0
                   WHEN severity = 'CRITICAL' THEN 0.0
                   ELSE NULL END), 2)                               AS critical_pass_rate_pct
FROM data_quality.pipeline_test_results
WHERE run_date >= CURRENT_DATE() - 30
  AND environment = 'prod'
GROUP BY 1
ORDER BY 1 DESC;


-- ── Query 4: Recurring failures (flapping tests) ────────────────────────────
-- Tests that fail more than 20% of the time are either:
-- a) Testing a real, persistent data problem (fix the data)
-- b) Testing with wrong thresholds (fix the threshold)
-- c) Not stable tests (fix or remove them)
SELECT
    test_name,
    table_name,
    column_name,
    severity,
    COUNT(*)                                                        AS run_count,
    SUM(CASE WHEN NOT passed THEN 1 ELSE 0 END)                     AS failure_count,
    ROUND(SUM(CASE WHEN NOT passed THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS failure_rate_pct,
    MAX(CASE WHEN NOT passed THEN run_date END)                     AS last_failure_date
FROM data_quality.pipeline_test_results
WHERE run_date >= CURRENT_DATE() - 30
  AND environment = 'prod'
GROUP BY 1, 2, 3, 4
HAVING failure_rate_pct > 20
ORDER BY failure_rate_pct DESC, failure_count DESC;


-- ── Query 5: DQ health score by table ───────────────────────────────────────
-- A single score per table for the governance dashboard
SELECT
    table_name,
    layer,
    COUNT(*)                                                        AS tests_run_today,
    SUM(CASE WHEN NOT passed AND severity = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_failures,
    SUM(CASE WHEN NOT passed AND severity = 'HIGH' THEN 1 ELSE 0 END)     AS high_failures,
    -- Health score: 100 - (CRITICAL_FAILURES * 30) - (HIGH_FAILURES * 10) - (MEDIUM * 3)
    GREATEST(0, 100
        - SUM(CASE WHEN NOT passed AND severity = 'CRITICAL' THEN 30 ELSE 0 END)
        - SUM(CASE WHEN NOT passed AND severity = 'HIGH'     THEN 10 ELSE 0 END)
        - SUM(CASE WHEN NOT passed AND severity = 'MEDIUM'   THEN 3  ELSE 0 END)
    )                                                               AS health_score,
    CASE
        WHEN SUM(CASE WHEN NOT passed AND severity = 'CRITICAL' THEN 1 ELSE 0 END) > 0 THEN 'RED'
        WHEN SUM(CASE WHEN NOT passed AND severity = 'HIGH'     THEN 1 ELSE 0 END) > 0 THEN 'AMBER'
        ELSE 'GREEN'
    END                                                             AS health_status
FROM data_quality.pipeline_test_results
WHERE run_date = CURRENT_DATE()
  AND environment = 'prod'
GROUP BY 1, 2
ORDER BY health_score ASC;
```

---

## 7. Observability — The DQ Dashboard

### 7.1 Required BI Dashboard Panels

Every data engineering team should have a DQ observability dashboard. Minimum panels:

```
┌─────────────────────────────────────────────────────────────────────┐
│  DATA QUALITY HEALTH DASHBOARD                           [PROD]     │
│  Last refreshed: 2024-01-15 14:32 UTC                              │
├────────────────┬────────────────┬───────────────┬──────────────────┤
│ TODAY'S TESTS  │  PASS RATE     │ CRITICAL OPEN │  HIGH OPEN       │
│    1,247       │   97.8%        │     0         │     3            │
│ ▲ 12 vs yest.  │ ▼ 0.4pp       │ ✅ Zero       │ ⚠️ 3 open       │
├─────────────────────────────────────────────────────────────────────┤
│  TABLE HEALTH STATUS                                                │
│                                                                     │
│  🟢 fact_orders           health: 100  tests: 48   failures: 0     │
│  🟢 stg_orders            health: 100  tests: 31   failures: 0     │
│  🟡 agg_daily_revenue     health: 87   tests: 12   failures: 1 HIGH│
│  🟢 dim_customers         health: 100  tests: 22   failures: 0     │
│  🔴 raw_orders            health: 60   tests: 18   failures: 2 HIGH│
├─────────────────────────────────────────────────────────────────────┤
│  OPEN FAILURES                                                      │
│                                                                     │
│  ⚠️ HIGH  raw_orders.currency.in_set                               │
│          47 rows have currency='XXX' (first seen: 14:15 UTC today) │
│                                                                     │
│  ⚠️ HIGH  raw_orders.amount.not_null                               │
│          3 rows have null amount (recurring: also failed yesterday) │
│                                                                     │
│  ⚠️ HIGH  agg_daily_revenue.volume_dod                            │
│          Volume dropped 34% vs yesterday (today: 28K, yest: 42K)  │
├─────────────────────────────────────────────────────────────────────┤
│  30-DAY PASS RATE TREND               FAILURE DISTRIBUTION BY TYPE │
│  [Line chart: daily pass rate %]      [Pie: completeness 45%,      │
│                                             validity 30%,           │
│                                             volume 15%,             │
│                                             freshness 10%]         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. Test Result Trending and Anomaly Detection

### 8.1 Detecting Gradually Degrading Quality

```python
# quality/trend_monitor.py
"""
Detect gradual quality degradation before it becomes a crisis.

The problem this solves:
    Pass rate was 99.8% two months ago. Today it's 97.2%.
    No single day had a big drop, so no alert fired.
    But the trend is clearly downward — something is slowly getting worse.

This monitor detects trends that individual-day alerts miss.
"""

import pandas as pd
import numpy as np
from scipy import stats


def detect_quality_trend(
    daily_pass_rates: pd.Series,  # Index: dates, Values: pass rate %
    lookback_days: int = 14,
    min_slope_alert_pct_per_day: float = -0.1  # Alert if declining >0.1% per day
) -> dict:
    """
    Detect if pass rates are trending downward.
    Uses linear regression on the last N days to estimate the trend slope.
    """
    if len(daily_pass_rates) < lookback_days:
        return {"has_trend": False, "reason": "Insufficient history"}

    recent = daily_pass_rates.tail(lookback_days)
    x = np.arange(len(recent))
    y = recent.values

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # slope is in units of "% per day"
    is_declining = slope < min_slope_alert_pct_per_day
    is_statistically_significant = p_value < 0.05

    trend_result = {
        "slope_pct_per_day":     round(float(slope), 4),
        "r_squared":             round(float(r_value ** 2), 4),
        "p_value":               round(float(p_value), 4),
        "is_significant":        is_statistically_significant,
        "alert":                 is_declining and is_statistically_significant,
        "projected_rate_7d":     round(float(recent.iloc[-1] + slope * 7), 2),
        "start_rate":            round(float(recent.iloc[0]), 2),
        "current_rate":          round(float(recent.iloc[-1]), 2),
    }

    if trend_result["alert"]:
        trend_result["message"] = (
            f"Quality degradation trend detected: "
            f"Pass rate declining {abs(slope):.3f}%/day over last {lookback_days} days "
            f"({trend_result['start_rate']}% → {trend_result['current_rate']}%). "
            f"Projected in 7 days: {trend_result['projected_rate_7d']}%"
        )

    return trend_result
```

---

## 9. SLA Monitoring at Scale

```python
# quality/sla_monitor.py
"""
Monitor freshness SLAs for all production tables.
Run this on a schedule (e.g., every 30 minutes) to detect stale tables
before downstream consumers notice.
"""

import yaml
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd


def check_all_freshness_slas(
    sla_config_path: str,
    warehouse_connection,
    notifier=None
) -> pd.DataFrame:
    """
    Check freshness SLAs for all configured tables.
    Returns a DataFrame of SLA status for the monitoring dashboard.
    """
    with open(sla_config_path) as f:
        config = yaml.safe_load(f)

    now = datetime.now(timezone.utc)
    results = []

    for table_cfg in config["tables"]:
        table = table_cfg["table"]
        ts_col = table_cfg["timestamp_column"]
        max_age_hours = table_cfg["max_age_hours"]
        severity = table_cfg.get("severity", "HIGH")
        owner_team = table_cfg.get("owner_team", "data-engineering")

        # Query the table for its most recent timestamp
        try:
            result = warehouse_connection.scalar(
                f"SELECT MAX({ts_col}) FROM {table}"
            )
            latest = pd.to_datetime(result, utc=True) if result else None
        except Exception as e:
            latest = None

        if latest is None:
            age_hours = float("inf")
            status = "UNKNOWN"
        else:
            age_hours = (now - latest).total_seconds() / 3600
            if age_hours <= max_age_hours * 0.75:
                status = "FRESH"
            elif age_hours <= max_age_hours:
                status = "WARNING"
            else:
                status = "STALE"

        results.append({
            "table":           table,
            "latest_record":   str(latest) if latest else "NONE",
            "age_hours":       round(age_hours, 2) if age_hours != float("inf") else None,
            "max_age_hours":   max_age_hours,
            "status":          status,
            "severity":        severity,
            "owner_team":      owner_team,
            "checked_at":      now.isoformat()
        })

        # Alert immediately on STALE critical tables
        if status == "STALE" and severity == "CRITICAL" and notifier:
            notifier.notify_critical_failure(
                gate_name=f"freshness_sla.{table}",
                error_message=(
                    f"Table {table} is STALE: most recent record is "
                    f"{age_hours:.1f} hours old (SLA: {max_age_hours} hours). "
                    f"Latest record: {latest}"
                )
            )

    return pd.DataFrame(results)
```

---

## 10. Managing Test Debt — What to Do When You Have Too Many Failures

### 10.1 The Failure Triage Process

When you first enable tests on an existing system, you will likely see many failures. This is normal and expected — the tests are working correctly by revealing existing issues. The challenge is: you cannot fix everything at once, and you should not disable tests to make the dashboard green.

```
TRIAGE PROCESS FOR NEW FAILURES:

Step 1: Classify each failure (takes 5 minutes per test)
    a) Is this a real data problem? → Fix the data or upstream process
    b) Is this a wrong threshold? → Update the threshold in YAML config
    c) Is this a test for a rule that no longer applies? → Delete the test
    d) Is this a known acceptable condition? → Document it; lower severity

Step 2: Prioritize by severity × business impact
    CRITICAL + high business impact → fix within 24 hours
    HIGH + high business impact → fix within 5 days
    HIGH + low business impact → schedule in next sprint
    MEDIUM → schedule in monthly cleanup

Step 3: Never disable tests without documenting why
    If you must skip a test temporarily:
    - Add a YAML comment: "# TEMPORARILY DISABLED: JIRA-123 - fixing upstream"
    - Set severity to 'warn' (not 'error') so it logs but doesn't block
    - Add it to the team's test-debt backlog
    - Restore to 'error' once the underlying issue is resolved

Step 4: Do not add 'warn' everywhere to make the dashboard green
    warn = "we acknowledge this is a problem but are not fixing it"
    error = "this is unacceptable and must be fixed"
    If you change error → warn because it's inconvenient, you've hidden a bug.
```

### 10.2 The Test Quality Backlog Query

```sql
-- Identify your highest-priority test debt
SELECT
    test_name,
    table_name,
    severity,
    COUNT(DISTINCT run_date)                AS days_with_failures,
    AVG(failing_count)                      AS avg_failing_rows,
    MAX(failing_count)                      AS max_failing_rows,
    MIN(run_date)                           AS first_failure_date,
    DATEDIFF('day', MIN(run_date), CURRENT_DATE()) AS days_open,
    -- Priority score: severity weight × days open
    CASE severity
        WHEN 'CRITICAL' THEN 4
        WHEN 'HIGH'     THEN 3
        WHEN 'MEDIUM'   THEN 2
        ELSE 1
    END * DATEDIFF('day', MIN(run_date), CURRENT_DATE()) AS priority_score
FROM data_quality.pipeline_test_results
WHERE NOT passed
  AND environment = 'prod'
  AND run_date >= CURRENT_DATE() - 30
GROUP BY 1, 2, 3
ORDER BY priority_score DESC;
```

---

## 11. The Complete Operations Runbook

### 11.1 On-Call Runbook for DQ Incidents

```markdown
## DATA QUALITY INCIDENT RUNBOOK

### When you receive a CRITICAL DQ alert:

#### Step 1: Assess (2 minutes)
- Open the DQ dashboard: https://company.retool.com/apps/dq-dashboard
- Identify: which table, which test, which pipeline
- Check: when did it start? (Is this recurring or new?)

#### Step 2: Contain (5 minutes)
- Is a downstream job consuming this table right now?
  → YES: Kill the downstream job. Stale data is better than wrong data.
  → NO: Continue to diagnose.
- Is this a Bronze failure that hasn't propagated to Gold yet?
  → YES: Stop the Silver and Gold transforms. Investigate Bronze first.

#### Step 3: Diagnose (15 minutes)
- Query the failing rows directly:
  SELECT * FROM data_quality.not_null_stg_orders_order_id LIMIT 20;
  (dbt --store-failures creates this table automatically)
- Check if the source system had any changes or incidents
- Check the pipeline logs for error messages

#### Step 4: Resolve or Escalate (30 minutes)
- If the fix is clear (wrong FX rate, source schema change, etc.) → fix it, rerun
- If the root cause is unclear → escalate to senior DE or domain team
- If data is irrecoverably bad for a partition → use time-travel to restore prior version:
  -- Snowflake time travel
  INSERT INTO gold.fact_orders
  SELECT * FROM gold.fact_orders AT (OFFSET => -3600)  -- 1 hour ago
  WHERE order_date = CURRENT_DATE();

#### Step 5: Document (After Resolution)
- Write a one-paragraph incident report in #data-incidents Slack channel
- Create a Jira ticket for the root cause fix
- Update the test if the threshold needs adjusting
- Post-mortem if CRITICAL + duration > 2 hours
```

---

*This document is part of the Data Engineering Quality Engineering library. For questions: data-engineering@company.com*
