# Data Engineering KPIs, Benchmarking & Scorecard
## Snowflake | Databricks | dbt | Airflow

**Document Owner:** Chief Data Office
**Domain:** Data Engineering
**Version:** 1.0
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [KPI Framework Overview](#1-kpi-framework-overview)
2. [Full KPI Registry](#2-full-kpi-registry)
3. [DE Scorecard — Monthly Template](#3-de-scorecard--monthly-template)
4. [KPI Data Collection — Python Pattern](#4-kpi-data-collection--python-pattern)
5. [YAML Configuration — KPI Definitions](#5-yaml-configuration--kpi-definitions)
6. [Benchmarking Reference](#6-benchmarking-reference)
7. [Maturity-Gated KPI Targets](#7-maturity-gated-kpi-targets)

---

## 1. KPI Framework Overview

Data Engineering KPIs are organized into four perspectives aligned to a **DE Balanced Scorecard**:

```
┌──────────────────────┐    ┌──────────────────────┐
│  PLATFORM HEALTH     │    │  DATA QUALITY         │
│  Is the platform     │    │  Is the data fit for  │
│  stable and managed? │    │  use at every layer?  │
└──────────────────────┘    └──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  OPERATIONAL         │    │  COST &               │
│  EXCELLENCE          │    │  EFFICIENCY           │
│  Are pipelines       │    │  Is compute spend     │
│  reliable & governed?│    │  justified & managed? │
└──────────────────────┘    └──────────────────────┘
```

### 1.1 KPI Ownership Model

| Perspective | Primary Owner | Reporting Cadence | Audience |
|---|---|---|---|
| Platform Health | Data Platform Engineer | Monthly | DE Lead, CDO |
| Data Quality | Analytics Engineer + DE Team | Daily/Weekly | DE Lead, Stewards |
| Operational Excellence | DE Lead | Monthly | CDO, Governance |
| Cost & Efficiency | Data Platform Engineer | Monthly | CDO, Finance |

---

## 2. Full KPI Registry

### 2.1 Platform Health KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| PH-DE-01 | IaC Coverage Rate | Objects managed by Terraform / Total objects | 100% | Monthly | Terraform state |
| PH-DE-02 | IaC Drift Incidents | Count of detected drift events per month | 0 | Monthly | Terraform plan output |
| PH-DE-03 | Secrets in Code Incidents | Confirmed secrets found in version control | 0 | Per commit | gitleaks / CI/CD |
| PH-DE-04 | Service Account Recertification Rate | Accounts reviewed on time / Total accounts | 100% | Quarterly | IAM / Snowflake |
| PH-DE-05 | Snowflake Warehouse Auto-Suspend Coverage | Warehouses with auto-suspend / Total warehouses | 100% | Monthly | Snowflake |
| PH-DE-06 | Databricks Cluster Auto-Termination Coverage | Clusters with auto-terminate / Total clusters | 100% | Monthly | Databricks API |
| PH-DE-07 | Environment Parity Score | Config attributes matching between staging and prod | ≥ 95% | Monthly | Config diff check |

### 2.2 Data Quality KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| DQ-DE-01 | Critical DQ Gate Pass Rate | Pipelines passing CRITICAL gates / Total pipeline runs | ≥ 99.5% | Daily | DQ results table |
| DQ-DE-02 | High DQ Gate Pass Rate | Pipelines passing HIGH gates / Total pipeline runs | ≥ 98% | Daily | DQ results table |
| DQ-DE-03 | Schema Drift Incidents | Unreviewed schema changes detected | 0 | Weekly | Information schema diff |
| DQ-DE-04 | Bronze Layer Quality Score | Bronze tables with defined DQ rules / Total bronze tables | ≥ 80% | Monthly | DQ config registry |
| DQ-DE-05 | Silver Layer Quality Score | Silver tables with defined DQ rules / Total silver tables | 100% | Monthly | DQ config registry |
| DQ-DE-06 | Gold Layer Quality Score | Gold tables with defined DQ rules / Total gold tables | 100% | Monthly | DQ config registry |
| DQ-DE-07 | Repeat Pipeline Failure Rate | Same pipeline failing 2+ consecutive runs / Total runs | < 2% | Weekly | Pipeline run log |
| DQ-DE-08 | Data Contract Coverage | Gold objects with active data contracts / Total gold objects | 100% | Monthly | Contract registry |
| DQ-DE-09 | SLA Breach Rate | Pipeline runs missing SLA / Total runs | < 1% | Daily | Pipeline run log |

### 2.3 Operational Excellence KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| OE-DE-01 | Metadata Completeness — Silver | Silver tables with descriptions + column tags / Total | 100% | Monthly | Snowflake / Unity Catalog |
| OE-DE-02 | Metadata Completeness — Gold | Gold tables with descriptions + column tags + owner / Total | 100% | Monthly | Snowflake / Unity Catalog |
| OE-DE-03 | Config Coverage Rate | Production pipelines with a YAML config file / Total | 100% | Monthly | Git repository scan |
| OE-DE-04 | CI/CD Gate Pass Rate | Pipeline deployments passing all gates / Total deployments | ≥ 98% | Monthly | CI/CD run log |
| OE-DE-05 | Deployment Rollback Rate | Deployments requiring rollback / Total deployments | < 2% | Monthly | CI/CD run log |
| OE-DE-06 | Change Management Compliance | Production changes with approved change ticket / Total major changes | 100% | Monthly | ITSM system |
| OE-DE-07 | Mean Time to Detect (MTTD) — Pipeline Failure | Avg minutes from failure to alert | < 15 min | Per incident | Monitoring system |
| OE-DE-08 | Mean Time to Resolve (MTTR) — Pipeline Failure | Avg hours from alert to resolution | < 4 hrs (P1), < 8 hrs (P2) | Per incident | Incident log |
| OE-DE-09 | Lineage Documentation Coverage | Gold assets with end-to-end lineage / Total gold assets | ≥ 95% | Monthly | Collibra / dbt lineage |
| OE-DE-10 | Dead Letter Queue Aging | Records in DLQ older than 48 hours | 0 | Daily | DLQ monitor |

### 2.4 Cost & Efficiency KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| CE-DE-01 | Snowflake Compute Budget Variance | Actual credits / Budgeted credits | ≤ 105% | Monthly | Snowflake cost report |
| CE-DE-02 | Databricks DBU Budget Variance | Actual DBUs / Budgeted DBUs | ≤ 105% | Monthly | Databricks cost report |
| CE-DE-03 | Untagged Compute Spend | Compute spend without required cost tags / Total spend | 0% | Monthly | Cloud billing |
| CE-DE-04 | Idle Warehouse Spend | Credits consumed by warehouses with 0 queries in billing period | Trending ↓ | Monthly | Snowflake |
| CE-DE-05 | Cost per Pipeline Run | Total compute cost / Total successful pipeline runs | Trending ↓ | Monthly | Cloud billing + run log |
| CE-DE-06 | Storage Growth Rate | Month-over-month storage increase vs. data volume growth | ≤ 1:1 ratio | Monthly | Snowflake / Databricks |
| CE-DE-07 | Clone / Time Travel Overhead | Storage cost attributable to clones and time travel / Total storage | < 15% | Monthly | Snowflake |

---

## 3. DE Scorecard — Monthly Template

```markdown
# Data Engineering Scorecard — [Month YYYY]

## Overall Program Health: [X.X / 5.0] (↑/→/↓ from prior month)

| Perspective | Score | Trend | Status |
|---|---|---|---|
| Platform Health | X% | ↑ | 🟢 On Track |
| Data Quality | X% | → | 🟡 At Risk |
| Operational Excellence | X% | ↑ | 🟢 On Track |
| Cost & Efficiency | X% | ↓ | 🔴 Off Track |

---

## Platform Health

| KPI | Target | Actual | Status |
|---|---|---|---|
| PH-DE-01 IaC Coverage | 100% | X% | 🟢/🔴 |
| PH-DE-02 IaC Drift Events | 0 | X | 🟢/🔴 |
| PH-DE-03 Secrets Incidents | 0 | X | 🟢/🔴 |
| PH-DE-05 Warehouse Auto-Suspend | 100% | X% | 🟢/🔴 |
| PH-DE-07 Env Parity Score | ≥95% | X% | 🟢/🔴 |

## Data Quality

| KPI | Target | Actual | Status |
|---|---|---|---|
| DQ-DE-01 Critical Gate Pass Rate | ≥99.5% | X% | 🟢/🔴 |
| DQ-DE-02 High Gate Pass Rate | ≥98% | X% | 🟢/🔴 |
| DQ-DE-03 Schema Drift Events | 0 | X | 🟢/🔴 |
| DQ-DE-08 Data Contract Coverage | 100% | X% | 🟢/🔴 |
| DQ-DE-09 SLA Breach Rate | <1% | X% | 🟢/🔴 |

## Operational Excellence

| KPI | Target | Actual | Status |
|---|---|---|---|
| OE-DE-01 Metadata — Silver | 100% | X% | 🟢/🔴 |
| OE-DE-02 Metadata — Gold | 100% | X% | 🟢/🔴 |
| OE-DE-07 MTTD | <15 min | X min | 🟢/🔴 |
| OE-DE-08 MTTR (P1) | <4 hrs | X hrs | 🟢/🔴 |
| OE-DE-09 Lineage Coverage | ≥95% | X% | 🟢/🔴 |

## Cost & Efficiency

| KPI | Target | Actual | Status |
|---|---|---|---|
| CE-DE-01 Snowflake Budget Variance | ≤105% | X% | 🟢/🔴 |
| CE-DE-02 Databricks Budget Variance | ≤105% | X% | 🟢/🔴 |
| CE-DE-03 Untagged Spend | 0% | X% | 🟢/🔴 |
| CE-DE-04 Idle Warehouse Spend | Trending ↓ | $X | 🟢/🔴 |

---

## Incidents This Month
| Incident ID | Severity | Pipeline | Duration | Root Cause | Status |
|---|---|---|---|---|---|
| INC-XXX | P1/P2 | [name] | Xh | [description] | Resolved/Open |

## Top 3 Risks
1. [Risk] — Owner: [name] — Due: [date]
2. [Risk] — Owner: [name] — Due: [date]
3. [Risk] — Owner: [name] — Due: [date]

## Remediation Actions
| Finding | Owner | Due | Status |
|---|---|---|---|
| [finding] | [name] | [date] | Open/In Progress/Closed |
```

---

## 4. KPI Data Collection — Python Pattern

KPI data is sourced from three systems:
- **Snowflake** — DQ results, metadata completeness, pipeline run logs, cost data
- **Databricks API** — cluster configuration, DBU cost, job run status
- **Git / CI/CD** — config coverage, deployment gate pass rates, IaC drift results

```python
# de_kpi_collector.py
"""
Config-driven KPI collection for the Data Engineering program.
Collects from Snowflake, Databricks API, and Git/CI sources.
Follows the class-based, YAML-injected pattern.
"""

import yaml
import os
import pandas as pd
import snowflake.connector
import requests
from datetime import datetime, date
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any


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
    status: str  # GREEN | AMBER | RED | NO_DATA
    frequency: str
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "run_date": self.run_date,
            "kpi_id": self.kpi_id,
            "kpi_name": self.kpi_name,
            "perspective": self.perspective,
            "source": self.source,
            "actual": self.actual,
            "target": self.target,
            "target_operator": self.target_operator,
            "unit": self.unit,
            "status": self.status,
            "frequency": self.frequency,
            "notes": self.notes,
        }


class DEKPICollector:
    """
    Collects Data Engineering KPIs from Snowflake, Databricks, and Git.
    Designed to be scheduled monthly via Airflow or Databricks Workflows.
    All queries and targets are externalized to YAML — no hardcoded values.
    """

    def __init__(
        self,
        config_path: str,
        snowflake_conn_params: dict,
        databricks_host: str | None = None,
        databricks_token: str | None = None,
    ):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.sf_conn = snowflake.connector.connect(**snowflake_conn_params)
        self.databricks_host = databricks_host
        self.databricks_token = databricks_token
        self.run_date = datetime.utcnow().date()

    # ── Public API ────────────────────────────────────────────────

    def collect_all(self, perspectives: list[str] | None = None) -> pd.DataFrame:
        """Collect all KPIs. Optionally filter by perspective."""
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

    def save_results(self, df: pd.DataFrame, target_table: str = "data_engineering.kpis.results") -> None:
        """Persist KPI results to Snowflake for trending and dashboards."""
        cursor = self.sf_conn.cursor()
        for _, row in df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO {target_table}
                    (run_date, kpi_id, kpi_name, perspective, source,
                     actual, target, target_operator, unit, status, frequency, notes)
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
        elif source == "databricks":
            return self._collect_databricks(kpi)
        elif source == "git":
            return self._collect_git(kpi)
        else:
            raise ValueError(f"Unknown source type: {source}")

    # ── Collectors ────────────────────────────────────────────────

    def _collect_snowflake(self, kpi: dict) -> KPIResult:
        cursor = self.sf_conn.cursor()
        cursor.execute(kpi["query"])
        row = cursor.fetchone()
        actual = float(row[0]) if row and row[0] is not None else None
        return self._build_result(kpi, actual)

    def _collect_databricks(self, kpi: dict) -> KPIResult:
        """Call Databricks REST API for cluster/job/cost metrics."""
        if not self.databricks_host or not self.databricks_token:
            return self._build_result(kpi, actual=None, notes="Databricks credentials not configured")

        headers = {"Authorization": f"Bearer {self.databricks_token}"}
        endpoint = kpi["endpoint"]
        resp = requests.get(
            f"https://{self.databricks_host}{endpoint}",
            headers=headers,
            params=kpi.get("params", {}),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        actual = self._extract_nested(data, kpi["response_path"])
        return self._build_result(kpi, actual)

    def _collect_git(self, kpi: dict) -> KPIResult:
        """
        For Git-sourced KPIs (e.g. config coverage), query the pre-computed
        results table that the CI/CD pipeline writes to after each run.
        """
        cursor = self.sf_conn.cursor()
        cursor.execute(kpi["query"])
        row = cursor.fetchone()
        actual = float(row[0]) if row and row[0] is not None else None
        return self._build_result(kpi, actual)

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
            amber = amber_threshold and actual >= amber_threshold
        elif op == "lte":
            ok = actual <= target
            amber = amber_threshold and actual <= amber_threshold
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

    @staticmethod
    def _extract_nested(data: dict, path: str) -> Any:
        """Navigate a dot-separated path in a JSON response."""
        keys = path.split(".")
        val = data
        for key in keys:
            val = val.get(key) if isinstance(val, dict) else None
        return val


# ── DDL: Results Table ────────────────────────────────────────────────────────

CREATE_KPI_RESULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS data_engineering.kpis.results (
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
# config/kpis/de_kpis_config.yaml
# All KPI definitions for the Data Engineering program.
# Add/edit KPIs here — no code changes required.

kpis:

  # ── Platform Health ───────────────────────────────────────────────────────

  - kpi_id: "PH-DE-01"
    name: "IaC Coverage Rate"
    perspective: "platform_health"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    amber_threshold: 0.95
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN managed_by_iac THEN 1 END)::FLOAT / COUNT(*)
      FROM data_engineering.audit.object_inventory
      WHERE environment = 'prod'
        AND scan_date = (SELECT MAX(scan_date) FROM data_engineering.audit.object_inventory)

  - kpi_id: "PH-DE-02"
    name: "IaC Drift Incidents"
    perspective: "platform_health"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(*)
      FROM data_engineering.audit.iac_drift_log
      WHERE detected_at >= DATE_TRUNC('month', CURRENT_DATE())
        AND resolved = FALSE

  - kpi_id: "PH-DE-05"
    name: "Snowflake Warehouse Auto-Suspend Coverage"
    perspective: "platform_health"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN AUTO_SUSPEND IS NOT NULL AND AUTO_SUSPEND > 0 THEN 1 END)::FLOAT
        / NULLIF(COUNT(*), 0)
      FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSES
      WHERE DELETED IS NULL

  - kpi_id: "PH-DE-06"
    name: "Databricks Cluster Auto-Termination Coverage"
    perspective: "platform_health"
    source: "databricks"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    endpoint: "/api/2.0/clusters/list"
    response_path: "auto_terminate_rate"  # Pre-computed field in response handler

  # ── Data Quality ──────────────────────────────────────────────────────────

  - kpi_id: "DQ-DE-01"
    name: "Critical DQ Gate Pass Rate"
    perspective: "data_quality"
    source: "snowflake"
    frequency: "daily"
    unit: "percentage"
    target: 0.995
    amber_threshold: 0.98
    target_operator: "gte"
    query: |
      SELECT
        SUM(CASE WHEN passed THEN 1 ELSE 0 END)::FLOAT / NULLIF(COUNT(*), 0)
      FROM data_quality.pipeline_test_results
      WHERE severity = 'CRITICAL'
        AND run_date = CURRENT_DATE() - 1
        AND environment = 'prod'

  - kpi_id: "DQ-DE-08"
    name: "Data Contract Coverage — Gold"
    perspective: "data_quality"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    amber_threshold: 0.90
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN has_active_contract THEN 1 END)::FLOAT / NULLIF(COUNT(*), 0)
      FROM data_engineering.catalog.gold_objects
      WHERE environment = 'prod'
        AND is_consumer_facing = TRUE

  - kpi_id: "DQ-DE-09"
    name: "SLA Breach Rate"
    perspective: "data_quality"
    source: "snowflake"
    frequency: "daily"
    unit: "percentage"
    target: 0.01
    target_operator: "lte"
    query: |
      SELECT
        COUNT(CASE WHEN sla_breached THEN 1 ELSE 0 END)::FLOAT / NULLIF(COUNT(*), 0)
      FROM data_engineering.pipelines.run_log
      WHERE run_date >= CURRENT_DATE() - 30
        AND environment = 'prod'

  # ── Operational Excellence ────────────────────────────────────────────────

  - kpi_id: "OE-DE-03"
    name: "Config Coverage Rate"
    perspective: "operational_excellence"
    source: "git"
    frequency: "monthly"
    unit: "percentage"
    target: 1.0
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN has_config_yaml THEN 1 END)::FLOAT / NULLIF(COUNT(*), 0)
      FROM data_engineering.audit.pipeline_registry
      WHERE is_production = TRUE
        AND scan_date = (SELECT MAX(scan_date) FROM data_engineering.audit.pipeline_registry)

  - kpi_id: "OE-DE-07"
    name: "Mean Time to Detect — Pipeline Failure (minutes)"
    perspective: "operational_excellence"
    source: "snowflake"
    frequency: "monthly"
    unit: "minutes"
    target: 15
    target_operator: "lte"
    query: |
      SELECT AVG(DATEDIFF('minute', failure_time, first_alert_time))
      FROM data_engineering.incidents.incident_log
      WHERE incident_date >= CURRENT_DATE() - 30
        AND environment = 'prod'
        AND FIRST_ALERT_TIME IS NOT NULL

  # ── Cost & Efficiency ─────────────────────────────────────────────────────

  - kpi_id: "CE-DE-01"
    name: "Snowflake Compute Budget Variance"
    perspective: "cost_efficiency"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.05
    target_operator: "lte"
    query: |
      SELECT
        SUM(actual_credits) / NULLIF(SUM(budgeted_credits), 0)
      FROM data_engineering.finance.monthly_compute_budget
      WHERE budget_month = DATE_TRUNC('month', CURRENT_DATE() - 1)

  - kpi_id: "CE-DE-03"
    name: "Untagged Compute Spend Percentage"
    perspective: "cost_efficiency"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 0.0
    target_operator: "lte"
    query: |
      SELECT
        SUM(CASE WHEN cost_center_tag IS NULL THEN credits_used_cloud_services ELSE 0 END)
        / NULLIF(SUM(credits_used_cloud_services), 0)
      FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
      WHERE START_TIME >= DATE_TRUNC('month', CURRENT_DATE() - 1)
        AND START_TIME < DATE_TRUNC('month', CURRENT_DATE())
```

---

## 6. Benchmarking Reference

The following industry benchmarks provide context for target-setting. Adjust to your organization's maturity level.

| KPI | Early Stage (Yr 1) | Developing (Yr 2) | Mature (Yr 3+) | Best-in-Class |
|---|---|---|---|---|
| IaC Coverage | ≥ 60% | ≥ 85% | 100% | 100% |
| Critical DQ Gate Pass Rate | ≥ 95% | ≥ 98% | ≥ 99.5% | > 99.9% |
| SLA Breach Rate | < 10% | < 5% | < 1% | < 0.1% |
| MTTD — Pipeline Failure | < 60 min | < 30 min | < 15 min | < 5 min |
| MTTR — P1 Failure | < 24 hrs | < 8 hrs | < 4 hrs | < 1 hr |
| Metadata Completeness (Gold) | ≥ 50% | ≥ 80% | 100% | 100% |
| Data Contract Coverage (Gold) | ≥ 20% | ≥ 60% | 100% | 100% |
| Budget Variance | ≤ 130% | ≤ 115% | ≤ 105% | ≤ 100% |

---

## 7. Maturity-Gated KPI Targets

KPI targets should be set relative to program maturity. Use the following progression:

| Maturity Level | IaC Coverage | Gold Metadata | Contract Coverage | Critical DQ Pass | MTTD |
|---|---|---|---|---|---|
| **Level 1 — Ad Hoc** | No target | No target | No target | Baseline only | No target |
| **Level 2 — Managed** | ≥ 70% | ≥ 50% | ≥ 20% | ≥ 95% | < 60 min |
| **Level 3 — Defined** | ≥ 95% | ≥ 90% | ≥ 75% | ≥ 98% | < 30 min |
| **Level 4 — Optimized** | 100% | 100% | 100% | ≥ 99.5% | < 15 min |
| **Level 5 — Leading** | 100% + drift=0 | 100% + lineage | 100% + versioned | ≥ 99.9% | < 5 min |

> **CDO Mandate:** All production data engineering programs must achieve and maintain Level 3 targets within 12 months of program establishment. Level 4 targets are required for regulated data domains.

---

*Document Owner: Chief Data Officer | Domain Lead: Data Engineering Lead | Review Cycle: Semi-Annual*
