# Data Governance KPIs, Benchmarking & Scorecard
> **Role:** Chief Data Officer | **Platform:** Snowflake / Databricks / Collibra  
> **Version:** 2.0 | **Last Updated:** 2026-03

---

## 1. KPI Framework Overview

KPIs are organized into four perspectives aligned to a **Governance Balanced Scorecard**:

```
┌──────────────────────┐    ┌──────────────────────┐
│  PROGRAM HEALTH      │    │  DATA QUALITY         │
│  Is the governance   │    │  Is the data reliable │
│  program operating?  │    │  and fit for use?     │
└──────────────────────┘    └──────────────────────┘

┌──────────────────────┐    ┌──────────────────────┐
│  COMPLIANCE &        │    │  BUSINESS VALUE       │
│  RISK                │    │  Is governance        │
│  Are we compliant    │    │  enabling the         │
│  and controlled?     │    │  business?            │
└──────────────────────┘    └──────────────────────┘
```

---

## 2. Full KPI Registry

### 2.1 Program Health KPIs

| KPI ID | Metric | Formula | Target | Frequency | Owner |
|---|---|---|---|---|---|
| PH-01 | Asset Ownership Coverage | Owned assets / Total assets | ≥ 95% | Monthly | DGO |
| PH-02 | Asset Classification Coverage | Classified assets / Total assets | ≥ 98% | Monthly | DGO |
| PH-03 | Glossary Term Coverage | Assets linked to glossary / Total | ≥ 80% | Monthly | DGO |
| PH-04 | Lineage Documentation Coverage | Assets with lineage / Tier 1 assets | ≥ 90% | Monthly | DGO |
| PH-05 | Metadata Completeness Score | Required fields populated / Total required | ≥ 90% | Monthly | DGO |
| PH-06 | Steward Engagement Rate | Stewards active in catalog / Total stewards | ≥ 90% | Monthly | DGO |
| PH-07 | New Asset Onboarding SLA | % assets fully onboarded within 5 days | ≥ 95% | Monthly | DGO |

### 2.2 Data Quality KPIs

| KPI ID | Metric | Formula | Target | Frequency | Owner |
|---|---|---|---|---|---|
| DQ-01 | Critical DQ Pass Rate | Passing CRITICAL rules / Total CRITICAL rules | ≥ 99.5% | Daily | Engineering |
| DQ-02 | High DQ Pass Rate | Passing HIGH rules / Total HIGH rules | ≥ 98% | Daily | Engineering |
| DQ-03 | DQ Incident Volume | Count of DQ incidents opened | Trending ↓ | Weekly | DGO |
| DQ-04 | Mean Time to Detect (MTTD) | Avg time from incident to alert | < 30 min | Per incident | Engineering |
| DQ-05 | Mean Time to Resolve (MTTR) | Avg time from alert to resolution | CRITICAL < 2hr | Per incident | Steward |
| DQ-06 | DQ Rule Coverage | Assets with DQ rules / Tier 1 assets | 100% | Monthly | DGO |
| DQ-07 | Repeat DQ Incident Rate | Incidents recurring within 30 days / Total | < 5% | Monthly | DGO |
| DQ-08 | Schema Drift Rate | Unreviewed schema changes / Total changes | 0% | Weekly | Engineering |

### 2.3 Compliance & Risk KPIs

| KPI ID | Metric | Formula | Target | Frequency | Owner |
|---|---|---|---|---|---|
| CR-01 | Access Certification Completion Rate | Certified entitlements / Total entitlements | 100% | Quarterly | DGO |
| CR-02 | Overdue Certifications | Count open certifications past due date | 0 | Weekly | DGO |
| CR-03 | Policy Exception Aging | Exceptions open > 30 days | 0 | Weekly | DGO |
| CR-04 | Privileged Access Violations | Unauthorized privileged access events | 0 | Weekly | CISO |
| CR-05 | Audit Finding Resolution Rate | Findings resolved within SLA / Total | 100% | Per audit | DGO |
| CR-06 | Open Critical Audit Findings | Count critical findings > 5 days | 0 | Daily | DGO |
| CR-07 | Regulatory Data Exposure Incidents | Incidents involving Restricted data | 0 | Real-time | DGO + CISO |
| CR-08 | Retention Policy Compliance | Assets with retention configured / Total | 100% Restricted | Monthly | Engineering |

### 2.4 Business Value KPIs

| KPI ID | Metric | Formula | Target | Frequency | Owner |
|---|---|---|---|---|---|
| BV-01 | Data Consumer Satisfaction Score | Survey: 1–5 scale | ≥ 4.0 | Quarterly | DGO |
| BV-02 | Self-Service Data Usage Rate | Consumers using catalog / Total consumers | Trending ↑ | Monthly | DGO |
| BV-03 | Time to Trust (new data product) | Days from request to certified product | < 10 days | Per product | DGO |
| BV-04 | Governance-Blocked Incidents Prevented | Incidents caught by governance controls | Trending ↑ | Monthly | DGO |
| BV-05 | Duplicate Data Elimination | Deduplicated assets removed / Prior count | Trending ↑ | Quarterly | Engineering |

---

## 3. Governance Scorecard — Monthly Template

```markdown
# Data Governance Scorecard — [Month YYYY]

## Overall Maturity Score: X.X / 5.0 (↑ from X.X)

| Perspective | Score | Trend | Status |
|---|---|---|---|
| Program Health | X% | ↑ | 🟢 On Track |
| Data Quality | X% | → | 🟡 At Risk |
| Compliance & Risk | X% | ↑ | 🟢 On Track |
| Business Value | X% | ↑ | 🟢 On Track |

## KPI Dashboard

### Program Health
| KPI | Target | Actual | Status |
| PH-01 Asset Ownership | ≥95% | 97% | 🟢 |
| PH-02 Classification | ≥98% | 94% | 🔴 |
...

## Top Risks This Month
1. [Risk description] — Owner: [name] — Due: [date]
...

## Highlight Achievements
- ...

## Remediation Actions
| Finding | Owner | Due | Status |
...
```

---

## 4. KPI Data Collection — Python Pattern

KPI data is sourced from two systems:
- **Collibra REST API** — program health metrics (ownership, classification, glossary, certification)
- **Snowflake** — DQ pipeline results, access logs, retention configurations

```python
# governance_kpi_collector.py
# Config-driven KPI collection from Collibra API and Snowflake

import yaml
import pandas as pd
import requests
import snowflake.connector
from datetime import datetime


class GovernanceKPICollector:
    """
    Collects governance KPIs from Collibra and Snowflake based on YAML config.
    Designed to be scheduled (daily/weekly/monthly) via Airflow or similar.
    """

    def __init__(self, config_path: str, collibra_base_url: str,
                 collibra_auth: tuple, snowflake_conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.collibra = requests.Session()
        self.collibra.auth = collibra_auth
        self.collibra.headers.update({"Content-Type": "application/json"})
        self.collibra_base = collibra_base_url
        self.sf_conn = snowflake.connector.connect(**snowflake_conn_params)
        self.run_date = datetime.utcnow().date()

    def collect_all(self) -> pd.DataFrame:
        results = []
        for kpi in self.config["kpis"]:
            source = kpi.get("source", "snowflake")
            if source == "collibra":
                result = self._collect_collibra_kpi(kpi)
            else:
                result = self._collect_snowflake_kpi(kpi)
            results.append(result)
        return pd.DataFrame(results)

    def _collect_snowflake_kpi(self, kpi: dict) -> dict:
        cursor = self.sf_conn.cursor()
        cursor.execute(kpi["query"])
        row = cursor.fetchone()
        actual = row[0] if row else None
        return self._build_result(kpi, actual)

    def _collect_collibra_kpi(self, kpi: dict) -> dict:
        """Call Collibra REST API and evaluate the KPI result."""
        resp = self.collibra.get(
            f"{self.collibra_base}{kpi['endpoint']}",
            params=kpi.get("params", {})
        )
        resp.raise_for_status()
        data = resp.json()
        actual = self._extract_collibra_value(data, kpi["response_path"])
        return self._build_result(kpi, actual)

    def _extract_collibra_value(self, data: dict, path: str):
        """Navigate dot-separated path in Collibra response JSON."""
        keys = path.split(".")
        val = data
        for key in keys:
            val = val.get(key) if isinstance(val, dict) else None
        return val

    def _build_result(self, kpi: dict, actual) -> dict:
        status = self._evaluate_status(actual, kpi)
        return {
            "run_date": self.run_date,
            "kpi_id": kpi["kpi_id"],
            "kpi_name": kpi["name"],
            "perspective": kpi["perspective"],
            "source": kpi.get("source", "snowflake"),
            "actual": actual,
            "target": kpi["target"],
            "target_operator": kpi["target_operator"],
            "unit": kpi.get("unit", "count"),
            "status": status,
            "frequency": kpi["frequency"]
        }

    def _evaluate_status(self, actual, kpi: dict) -> str:
        if actual is None:
            return "NO_DATA"
        target = kpi["target"]
        op = kpi["target_operator"]
        if op == "gte": ok = actual >= target
        elif op == "lte": ok = actual <= target
        elif op == "eq": ok = actual == target
        else: ok = False
        return "GREEN" if ok else "RED"
```

```yaml
# governance_kpis_config.yaml
kpis:
  # ── Collibra-sourced KPIs ──────────────────────────────────────
  - kpi_id: "PH-01"
    name: "Asset Ownership Coverage"
    perspective: "program_health"
    source: "collibra"
    frequency: "monthly"
    unit: "percentage"
    target: 0.95
    target_operator: "gte"
    endpoint: "/rest/2.0/assets/search"
    params:
      typePublicId: "Data Set"
      limit: 0
    response_path: "ownership_rate"  # Pre-calculated in Collibra reporting view

  - kpi_id: "PH-03"
    name: "Glossary Term Coverage"
    perspective: "program_health"
    source: "collibra"
    frequency: "monthly"
    unit: "percentage"
    target: 0.80
    target_operator: "gte"
    endpoint: "/rest/2.0/reporting/glossary/coverage"
    params: {}
    response_path: "coverage_rate"

  # ── Snowflake-sourced KPIs ─────────────────────────────────────
  - kpi_id: "DQ-01"
    name: "Critical DQ Pass Rate"
    perspective: "data_quality"
    source: "snowflake"
    frequency: "daily"
    unit: "percentage"
    target: 0.995
    target_operator: "gte"
    query: |
      SELECT SUM(pass_count) / SUM(total_count) AS pass_rate
      FROM governance.dq.daily_results
      WHERE severity = 'CRITICAL'
        AND run_date = CURRENT_DATE() - 1

  - kpi_id: "CR-02"
    name: "Overdue Access Certifications"
    perspective: "compliance_risk"
    source: "collibra"
    frequency: "weekly"
    unit: "count"
    target: 0
    target_operator: "lte"
    endpoint: "/rest/2.0/workflowTasks/search"
    params:
      taskType: "ACCESS_CERTIFICATION"
      status: "OVERDUE"
    response_path: "total"
```

---

## 5. Benchmarking Against Industry Standards

### 5.1 DCAM (Data Management Capability Assessment Model)

| Capability Area | DCAM Level 1 | DCAM Level 2 | DCAM Level 3 | Our Target |
|---|---|---|---|---|
| Data Governance | Policy exists | Council operating | Enforced, measured | Level 3 by Q4 |
| Data Quality | Defined | Monitored | Optimized | Level 2 by Q2 |
| Data Architecture | Documented | Standardized | Governed | Level 2 by Q3 |
| Data Catalog | Exists | Populated | Trusted, self-service | Level 2 by Q2 |

### 5.2 Peer Benchmarks (Financial Services / Enterprise)

| Metric | Industry Average | Top Quartile | Our Current | Gap |
|---|---|---|---|---|
| Asset Ownership Coverage | 72% | 96% | TBD | TBD |
| DQ Monitoring Automation | 45% | 85% | TBD | TBD |
| Glossary Term Coverage | 55% | 90% | TBD | TBD |
| Access Cert Completion | 78% | 100% | TBD | TBD |
| Time to Resolve DQ Incident | 3 days | 4 hours | TBD | TBD |

*Source: DCAM benchmarks, EDM Council annual survey*

### 5.3 Maturity Benchmark Scoring

Run quarterly using the maturity scorer pattern (see 2LOD document):

| Control Domain | Q1 Score | Q2 Target | Q3 Target | Q4 Target |
|---|---|---|---|---|
| Data Ownership | — | 2.5 | 3.5 | 4.0 |
| Data Classification | — | 2.0 | 3.0 | 3.5 |
| Data Quality | — | 2.5 | 3.5 | 4.0 |
| Access Control | — | 3.0 | 3.5 | 4.0 |
| Metadata & Catalog | — | 2.0 | 3.0 | 3.5 |
| Lineage | — | 1.5 | 2.5 | 3.0 |
| **Overall** | **—** | **2.3** | **3.2** | **3.7** |

---

## 6. Executive Reporting Package

### Monthly CDO Dashboard (1-pager)

```
┌─────────────────────────────────────────────────────────┐
│           DATA GOVERNANCE — MONTHLY DASHBOARD           │
│                      March 2026                         │
├────────────────┬────────────────┬────────────────────── │
│ MATURITY SCORE │ OPEN RISKS     │ DQ PASS RATE          │
│    3.2 / 5.0   │    2 HIGH      │   99.3% (↑ 0.2%)     │
│    (↑ from 2.9)│    5 MEDIUM    │   Target: 99.5%       │
├────────────────┴────────────────┴────────────────────── │
│  KPI STATUS: 14 🟢  3 🟡  1 🔴                         │
├─────────────────────────────────────────────────────────│
│  TOP RISK: Finance domain classification at 87%         │
│  ACTION: Steward sprint targeted for April              │
├─────────────────────────────────────────────────────────│
│  HIGHLIGHT: Q1 access certification 100% complete       │
└─────────────────────────────────────────────────────────┘
```

---

*Document Owner: Data Governance Office | Review Cycle: Quarterly*
