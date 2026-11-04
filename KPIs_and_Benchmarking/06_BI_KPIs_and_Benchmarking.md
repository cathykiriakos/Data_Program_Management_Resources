# Business Intelligence KPIs, Benchmarking & Scorecard
## Tableau | Power BI | Alteryx | Self-Service Analytics

**Document Owner:** Chief Data Office
**Domain:** Business Intelligence
**Version:** 1.0
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [KPI Framework Overview](#1-kpi-framework-overview)
2. [Full KPI Registry](#2-full-kpi-registry)
3. [BI Scorecard — Monthly Template](#3-bi-scorecard--monthly-template)
4. [KPI Data Collection — Python Pattern](#4-kpi-data-collection--python-pattern)
5. [YAML Configuration — KPI Definitions](#5-yaml-configuration--kpi-definitions)
6. [Benchmarking Reference](#6-benchmarking-reference)
7. [Maturity-Gated KPI Targets](#7-maturity-gated-kpi-targets)

---

## 1. KPI Framework Overview

Business Intelligence KPIs are organized into four perspectives aligned to a **BI Balanced Scorecard**:

```
┌──────────────────────┐    ┌──────────────────────┐
│  GOVERNANCE &        │    │  CONTENT QUALITY      │
│  TRUST               │    │  Is BI content        │
│  Is content governed │    │  accurate and         │
│  and trustworthy?    │    │  fit for purpose?     │
└──────────────────────┘    └──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  ADOPTION &          │    │  COST &               │
│  CONSUMPTION         │    │  PERFORMANCE          │
│  Are users getting   │    │  Is BI infrastructure │
│  value from BI?      │    │  efficient?           │
└──────────────────────┘    └──────────────────────┘
```

### 1.1 KPI Ownership Model

| Perspective | Primary Owner | Reporting Cadence | Audience |
|---|---|---|---|
| Governance & Trust | BI COE Lead + Data Governance | Monthly | CDO, Governance Council |
| Content Quality | Domain BI Leads | Monthly | BI COE, Domain Owners |
| Adoption & Consumption | BI COE Lead | Monthly | CDO, Business Stakeholders |
| Cost & Performance | BI Platform Engineer | Monthly | CDO, Finance |

---

## 2. Full KPI Registry

### 2.1 Governance & Trust KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| GT-BI-01 | Certified Report Coverage | T1 + T2 certified reports / Total published reports | ≥ 80% | Monthly | Report Registry |
| GT-BI-02 | Report Registry Completeness | Reports with all required registry fields / Total reports | 100% | Monthly | Report Registry |
| GT-BI-03 | Approved Data Source Compliance | BI connections to approved sources / Total connections | 100% | Monthly | Platform audit |
| GT-BI-04 | Unapproved Data Source Incidents | Direct connections to unapproved/raw sources detected | 0 | Monthly | Platform audit |
| GT-BI-05 | Access Certification Completion Rate | Entitlements certified on time / Total entitlements | 100% | Quarterly | IAM / BI platform |
| GT-BI-06 | Orphaned Report Rate | Reports with no owner or expired owner / Total reports | 0% | Monthly | Report Registry |
| GT-BI-07 | PII Exposure Incidents | Confirmed PII visible to unauthorized BI users | 0 | Per incident | Privacy / audit |
| GT-BI-08 | RLS Validation Coverage | Certified datasets with tested RLS / Total certified datasets | 100% | Monthly | BI COE checklist |
| GT-BI-09 | Sensitivity Label Coverage | Published reports with sensitivity labels / Total | 100% | Monthly | Platform audit |

### 2.2 Content Quality KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| CQ-BI-01 | T1 Report Data Freshness SLA | T1 reports meeting freshness SLA / Total T1 reports | 100% | Daily | Platform monitoring |
| CQ-BI-02 | T2 Report Data Freshness SLA | T2 reports meeting freshness SLA / Total T2 reports | ≥ 98% | Daily | Platform monitoring |
| CQ-BI-03 | Broken Report Rate | Reports with failed data refresh / Total reports | < 1% | Daily | Platform monitoring |
| CQ-BI-04 | Stale Content Rate | Published reports not accessed in 90 days / Total | Trending ↓ | Monthly | Usage logs |
| CQ-BI-05 | Brand Compliance Rate | Reports passing brand validation / Total certified | 100% | Monthly | Brand audit |
| CQ-BI-06 | Semantic Layer Usage Rate | Certified reports using semantic layer / Total certified | ≥ 90% | Monthly | Connection audit |
| CQ-BI-07 | Metric Definition Conflicts | Conflicting metric definitions across reports (same name, different logic) | 0 | Monthly | Governance review |
| CQ-BI-08 | Report Deprecation SLA | Legacy reports deprecated within 30 days of replacement | 100% | Per event | BI COE log |

### 2.3 Adoption & Consumption KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| AC-BI-01 | Active BI User Rate | Users accessing BI tools in the period / Total licensed users | ≥ 70% | Monthly | Usage logs |
| AC-BI-02 | Certified Content Usage Rate | Sessions using certified (T1/T2) content / Total sessions | ≥ 60% | Monthly | Usage logs |
| AC-BI-03 | Self-Service Adoption Rate | T3 self-service users / Total BI-enabled users | Trending ↑ | Monthly | Usage logs |
| AC-BI-04 | IT Report Request Volume | Formal IT report requests per month | Trending ↓ | Monthly | ITSM system |
| AC-BI-05 | Consumer Satisfaction Score | Survey: data consumers (1–5 scale) | ≥ 4.0 | Quarterly | Survey |
| AC-BI-06 | New Report Time-to-Publish (T1) | Days from business request to T1 published | < 15 days | Monthly | BI COE log |
| AC-BI-07 | New Report Time-to-Publish (T2) | Days from business request to T2 published | < 7 days | Monthly | BI COE log |
| AC-BI-08 | Self-Service Request Fulfillment Rate | Self-service requests completed without IT intervention / Total | Trending ↑ | Monthly | ITSM system |

### 2.4 Cost & Performance KPIs

| KPI ID | Metric | Formula | Target | Frequency | Source |
|---|---|---|---|---|---|
| CP-BI-01 | BI Compute Budget Variance | Actual BI compute cost / Budgeted BI compute cost | ≤ 105% | Monthly | Cloud / platform billing |
| CP-BI-02 | Untagged BI Compute Spend | Untagged BI queries / Total BI query cost | 0% | Monthly | Snowflake billing |
| CP-BI-03 | Average Dashboard Load Time (T1) | Avg seconds for T1 dashboard initial load | < 5 sec | Monthly | Platform telemetry |
| CP-BI-04 | Slow Query Rate | Queries exceeding 30-second threshold / Total queries | < 5% | Monthly | Platform telemetry |
| CP-BI-05 | Extract Cache Hit Rate | Extracts served from cache / Total extract requests | ≥ 60% | Monthly | Tableau / Power BI admin |
| CP-BI-06 | License Utilization Rate | Active users / Licensed users | ≥ 75% | Monthly | Platform admin |
| CP-BI-07 | Alteryx Workflow Failure Rate | Failed Alteryx workflow runs / Total runs | < 3% | Monthly | Alteryx Server |
| CP-BI-08 | Storage Consumed by Stale Extracts | GB of data extracts untouched > 30 days | Trending ↓ | Monthly | Platform admin |

---

## 3. BI Scorecard — Monthly Template

```markdown
# Business Intelligence Scorecard — [Month YYYY]

## Overall Program Health: [X.X / 5.0] (↑/→/↓ from prior month)

| Perspective | Score | Trend | Status |
|---|---|---|---|
| Governance & Trust | X% | ↑ | 🟢 On Track |
| Content Quality | X% | → | 🟡 At Risk |
| Adoption & Consumption | X% | ↑ | 🟢 On Track |
| Cost & Performance | X% | ↓ | 🔴 Off Track |

---

## Governance & Trust

| KPI | Target | Actual | Status |
|---|---|---|---|
| GT-BI-01 Certified Report Coverage | ≥80% | X% | 🟢/🔴 |
| GT-BI-03 Approved Source Compliance | 100% | X% | 🟢/🔴 |
| GT-BI-04 Unapproved Source Incidents | 0 | X | 🟢/🔴 |
| GT-BI-05 Access Certification | 100% | X% | 🟢/🔴 |
| GT-BI-07 PII Exposure Incidents | 0 | X | 🟢/🔴 |

## Content Quality

| KPI | Target | Actual | Status |
|---|---|---|---|
| CQ-BI-01 T1 Freshness SLA | 100% | X% | 🟢/🔴 |
| CQ-BI-03 Broken Report Rate | <1% | X% | 🟢/🔴 |
| CQ-BI-06 Semantic Layer Usage | ≥90% | X% | 🟢/🔴 |
| CQ-BI-07 Metric Conflicts | 0 | X | 🟢/🔴 |

## Adoption & Consumption

| KPI | Target | Actual | Status |
|---|---|---|---|
| AC-BI-01 Active User Rate | ≥70% | X% | 🟢/🔴 |
| AC-BI-02 Certified Content Usage | ≥60% | X% | 🟢/🔴 |
| AC-BI-04 IT Report Request Volume | Trending ↓ | X | 🟢/🔴 |
| AC-BI-05 Consumer Satisfaction | ≥4.0 | X.X | 🟢/🔴 |
| AC-BI-06 T1 Time-to-Publish | <15 days | X days | 🟢/🔴 |

## Cost & Performance

| KPI | Target | Actual | Status |
|---|---|---|---|
| CP-BI-01 Compute Budget Variance | ≤105% | X% | 🟢/🔴 |
| CP-BI-03 T1 Dashboard Load Time | <5 sec | X sec | 🟢/🔴 |
| CP-BI-04 Slow Query Rate | <5% | X% | 🟢/🔴 |
| CP-BI-06 License Utilization | ≥75% | X% | 🟢/🔴 |

---

## Incidents & Findings
| ID | Type | Severity | Description | Status |
|---|---|---|---|---|
| INC-XXX | PII / DQ / Access | High/Med | [description] | Open/Closed |

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

BI KPI data is sourced from three systems:
- **Snowflake** — query cost, user usage logs, semantic layer usage, freshness SLA
- **BI Platform APIs** — Tableau REST API or Power BI Admin API for usage, content inventory, extract size
- **Report Registry** (Git/Snowflake) — certification status, ownership, registry completeness

```python
# bi_kpi_collector.py
"""
Config-driven KPI collection for the Business Intelligence program.
Collects from Snowflake, Tableau REST API, and Power BI Admin API.
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


class BIKPICollector:
    """
    Collects BI KPIs from Snowflake, Tableau REST API, and Power BI Admin API.
    Scheduled monthly via Airflow or Databricks Workflows.
    All queries and targets externalized to YAML.
    """

    def __init__(
        self,
        config_path: str,
        snowflake_conn_params: dict,
        tableau_server_url: str | None = None,
        tableau_token: str | None = None,
        powerbi_tenant_id: str | None = None,
        powerbi_token: str | None = None,
    ):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.sf_conn = snowflake.connector.connect(**snowflake_conn_params)
        self.tableau_server_url = tableau_server_url
        self.tableau_token = tableau_token
        self.powerbi_tenant_id = powerbi_tenant_id
        self.powerbi_token = powerbi_token
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

    def save_results(self, df: pd.DataFrame, target_table: str = "business_intelligence.kpis.results") -> None:
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
        elif source == "tableau":
            return self._collect_tableau(kpi)
        elif source == "powerbi":
            return self._collect_powerbi(kpi)
        else:
            raise ValueError(f"Unknown source type: {source}")

    # ── Collectors ────────────────────────────────────────────────

    def _collect_snowflake(self, kpi: dict) -> KPIResult:
        cursor = self.sf_conn.cursor()
        cursor.execute(kpi["query"])
        row = cursor.fetchone()
        actual = float(row[0]) if row and row[0] is not None else None
        return self._build_result(kpi, actual)

    def _collect_tableau(self, kpi: dict) -> KPIResult:
        """Query Tableau REST API for content and usage metrics."""
        if not self.tableau_server_url or not self.tableau_token:
            return self._build_result(kpi, actual=None, notes="Tableau credentials not configured")

        headers = {
            "x-tableau-auth": self.tableau_token,
            "Content-Type": "application/json",
        }
        endpoint = kpi["endpoint"]
        resp = requests.get(
            f"{self.tableau_server_url}/api/3.21{endpoint}",
            headers=headers,
            params=kpi.get("params", {}),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        actual = self._extract_nested(data, kpi["response_path"])
        return self._build_result(kpi, actual)

    def _collect_powerbi(self, kpi: dict) -> KPIResult:
        """Query Power BI Admin API for workspace and activity metrics."""
        if not self.powerbi_token:
            return self._build_result(kpi, actual=None, notes="Power BI credentials not configured")

        headers = {"Authorization": f"Bearer {self.powerbi_token}"}
        endpoint = kpi["endpoint"]
        resp = requests.get(
            f"https://api.powerbi.com/v1.0/myorg{endpoint}",
            headers=headers,
            params=kpi.get("params", {}),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        actual = self._extract_nested(data, kpi["response_path"])
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

    @staticmethod
    def _extract_nested(data: dict, path: str) -> Any:
        keys = path.split(".")
        val = data
        for key in keys:
            val = val.get(key) if isinstance(val, dict) else None
        return val


# ── DDL: Results Table ────────────────────────────────────────────────────────

CREATE_KPI_RESULTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS business_intelligence.kpis.results (
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
# config/kpis/bi_kpis_config.yaml

kpis:

  # ── Governance & Trust ────────────────────────────────────────────────────

  - kpi_id: "GT-BI-01"
    name: "Certified Report Coverage"
    perspective: "governance_trust"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 0.80
    amber_threshold: 0.65
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN certification_tier IN ('T1','T2') THEN 1 END)::FLOAT
        / NULLIF(COUNT(*), 0)
      FROM business_intelligence.registry.report_registry
      WHERE is_published = TRUE
        AND is_deprecated = FALSE

  - kpi_id: "GT-BI-04"
    name: "Unapproved Data Source Incidents"
    perspective: "governance_trust"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(*)
      FROM business_intelligence.audit.source_compliance_log
      WHERE scan_date >= DATE_TRUNC('month', CURRENT_DATE() - 1)
        AND is_approved_source = FALSE

  - kpi_id: "GT-BI-07"
    name: "PII Exposure Incidents"
    perspective: "governance_trust"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(*)
      FROM business_intelligence.incidents.incident_log
      WHERE incident_type = 'PII_EXPOSURE'
        AND incident_date >= DATE_TRUNC('month', CURRENT_DATE() - 1)

  # ── Content Quality ───────────────────────────────────────────────────────

  - kpi_id: "CQ-BI-01"
    name: "T1 Report Data Freshness SLA"
    perspective: "content_quality"
    source: "snowflake"
    frequency: "daily"
    unit: "percentage"
    target: 1.0
    amber_threshold: 0.98
    target_operator: "gte"
    query: |
      SELECT
        COUNT(CASE WHEN last_refresh_at >= DATEADD('hour', -freshness_sla_hours, CURRENT_TIMESTAMP()) THEN 1 END)::FLOAT
        / NULLIF(COUNT(*), 0)
      FROM business_intelligence.registry.report_registry
      WHERE certification_tier = 'T1'
        AND is_published = TRUE
        AND is_deprecated = FALSE

  - kpi_id: "CQ-BI-07"
    name: "Metric Definition Conflicts"
    perspective: "content_quality"
    source: "snowflake"
    frequency: "monthly"
    unit: "count"
    target: 0
    target_operator: "lte"
    query: |
      SELECT COUNT(DISTINCT metric_name)
      FROM business_intelligence.audit.metric_conflict_log
      WHERE detected_date >= DATE_TRUNC('month', CURRENT_DATE() - 1)
        AND is_resolved = FALSE

  # ── Adoption & Consumption ────────────────────────────────────────────────

  - kpi_id: "AC-BI-01"
    name: "Active BI User Rate"
    perspective: "adoption_consumption"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 0.70
    amber_threshold: 0.55
    target_operator: "gte"
    query: |
      SELECT
        COUNT(DISTINCT active.user_id)::FLOAT
        / NULLIF(COUNT(DISTINCT licensed.user_id), 0)
      FROM business_intelligence.usage.licensed_users licensed
      LEFT JOIN (
        SELECT DISTINCT user_id
        FROM business_intelligence.usage.session_log
        WHERE session_date >= DATE_TRUNC('month', CURRENT_DATE() - 1)
      ) active ON licensed.user_id = active.user_id

  - kpi_id: "AC-BI-05"
    name: "Consumer Satisfaction Score"
    perspective: "adoption_consumption"
    source: "snowflake"
    frequency: "quarterly"
    unit: "score_1_5"
    target: 4.0
    amber_threshold: 3.5
    target_operator: "gte"
    query: |
      SELECT AVG(satisfaction_score)
      FROM business_intelligence.surveys.consumer_satisfaction
      WHERE survey_date >= DATE_TRUNC('quarter', CURRENT_DATE() - 1)

  # ── Cost & Performance ────────────────────────────────────────────────────

  - kpi_id: "CP-BI-01"
    name: "BI Compute Budget Variance"
    perspective: "cost_performance"
    source: "snowflake"
    frequency: "monthly"
    unit: "percentage"
    target: 1.05
    target_operator: "lte"
    query: |
      SELECT actual_cost / NULLIF(budgeted_cost, 0)
      FROM business_intelligence.finance.monthly_cost_budget
      WHERE budget_month = DATE_TRUNC('month', CURRENT_DATE() - 1)

  - kpi_id: "CP-BI-03"
    name: "Average T1 Dashboard Load Time (seconds)"
    perspective: "cost_performance"
    source: "snowflake"
    frequency: "monthly"
    unit: "seconds"
    target: 5.0
    amber_threshold: 8.0
    target_operator: "lte"
    query: |
      SELECT AVG(load_time_seconds)
      FROM business_intelligence.telemetry.dashboard_load_times
      WHERE certification_tier = 'T1'
        AND measured_date >= CURRENT_DATE() - 30
        AND environment = 'prod'

  - kpi_id: "CP-BI-06"
    name: "License Utilization Rate"
    perspective: "cost_performance"
    source: "tableau"
    frequency: "monthly"
    unit: "percentage"
    target: 0.75
    amber_threshold: 0.60
    target_operator: "gte"
    endpoint: "/sites/{site_id}/users"
    response_path: "utilization_rate"  # Pre-computed in response handler
```

---

## 6. Benchmarking Reference

| KPI | Early Stage (Yr 1) | Developing (Yr 2) | Mature (Yr 3+) | Best-in-Class |
|---|---|---|---|---|
| Certified Report Coverage | ≥ 30% | ≥ 55% | ≥ 80% | ≥ 95% |
| T1 Freshness SLA Compliance | ≥ 90% | ≥ 97% | 100% | 100% |
| Active BI User Rate | ≥ 40% | ≥ 55% | ≥ 70% | ≥ 85% |
| Certified Content Usage Rate | ≥ 20% | ≥ 40% | ≥ 60% | ≥ 80% |
| Consumer Satisfaction Score | ≥ 3.0 | ≥ 3.5 | ≥ 4.0 | ≥ 4.5 |
| Unapproved Source Incidents | < 5/mo | < 2/mo | 0 | 0 |
| License Utilization | ≥ 50% | ≥ 65% | ≥ 75% | ≥ 85% |
| T1 Dashboard Load Time | < 15 sec | < 10 sec | < 5 sec | < 3 sec |
| Metric Conflicts (open) | Baseline | < 5 | 0 | 0 |

---

## 7. Maturity-Gated KPI Targets

| Maturity Level | Certified Coverage | T1 SLA | Active Users | Satisfaction | PII Incidents |
|---|---|---|---|---|---|
| **Level 1 — Ad Hoc** | No target | No target | Baseline | No target | No target |
| **Level 2 — Managed** | ≥ 30% | ≥ 90% | ≥ 40% | ≥ 3.0 | < 3/qtr |
| **Level 3 — Defined** | ≥ 65% | ≥ 98% | ≥ 60% | ≥ 3.5 | 0 |
| **Level 4 — Optimized** | ≥ 80% | 100% | ≥ 70% | ≥ 4.0 | 0 |
| **Level 5 — Leading** | ≥ 95% | 100% | ≥ 85% | ≥ 4.5 | 0 |

> **CDO Mandate:** All BI programs serving regulated data must operate at Level 3 or above. The combination of PII Exposure Incidents = 0 and 100% Approved Source Compliance are non-negotiable floor conditions at any maturity level once a regulated domain is onboarded.

---

*Document Owner: Chief Data Officer | Domain Lead: BI COE Lead | Review Cycle: Semi-Annual*
