# Data Governance: 2nd Line of Defense Strategy
> **Role:** Chief Data Officer | **Platform:** Snowflake / Databricks / Collibra  
> **Version:** 2.0 | **Last Updated:** 2026-03

---

## 1. Overview: Three Lines of Defense Model

The Three Lines of Defense (3LOD) model defines **who** is responsible for governance controls and **how** oversight is structured:

```
┌──────────────────────────────────────────────────────────────┐
│  1st LINE OF DEFENSE — Operational Ownership                 │
│  Data Stewards, Domain Owners, Engineering Teams            │
│  → Own controls, execute governance day-to-day              │
└──────────────────────────────────────────────────────────────┘
                           ▼ reports to / overseen by
┌──────────────────────────────────────────────────────────────┐
│  2nd LINE OF DEFENSE — Oversight & Challenge   ← THIS DOC   │
│  Data Governance Office (DGO), Risk, Compliance             │
│  → Defines policy, monitors, challenges, escalates          │
└──────────────────────────────────────────────────────────────┘
                           ▼ independent review of
┌──────────────────────────────────────────────────────────────┐
│  3rd LINE OF DEFENSE — Independent Assurance                 │
│  Internal Audit, External Audit, Regulators                  │
│  → Independent testing and attestation                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 2nd Line of Defense Mandate

The **Data Governance Office (DGO)** operates as the 2nd line of defense. Its mandate is to:

1. **Define** governance policies and standards
2. **Monitor** 1st line adherence through automated KPIs and periodic reviews
3. **Challenge** findings, exceptions, and remediation quality
4. **Escalate** material risks and non-compliance to the CDO and Governance Council
5. **Report** on governance posture to executive and risk audiences

> The 2nd line does **not** own or operate the data — it sets the rules and holds the 1st line accountable.

---

## 3. 2nd Line Governance Review Framework

### 3.1 Continuous Monitoring (Automated)

The DGO maintains an automated monitoring layer that provides real-time visibility into governance posture. **Collibra is the primary source of truth for program health metrics** — asset ownership, classification coverage, workflow completion, and policy status are all tracked there. Snowflake and Databricks provide technical audit logs and DQ pipeline results that feed back into Collibra dashboards.

| Monitor | Primary Source | Frequency | Alert Threshold |
|---|---|---|---|
| DQ pass rate by domain | Collibra DQ dashboard + pipeline results | Daily | < 99% on CRITICAL rules |
| Unowned assets | Collibra catalog API | Daily | Any asset > 7 days unowned |
| Unclassified assets | Collibra attribute completeness report | Daily | Any new asset > 3 days unclassified |
| Access certification overdue | Collibra Workflow task status | Daily | Certification > 10 business days overdue |
| Policy exceptions open | Collibra Policy Manager | Daily | Any exception > 30 days |
| Orphaned service accounts | IAM / Snowflake access history | Weekly | Service account with no owner in Collibra |
| Schema drift (ungoverned) | Pipeline alerts → Collibra incident | Real-time | Any unreviewed schema change in PROD |
| Sensitive data in wrong layer | Snowflake tag scan + Collibra classification | Daily | RESTRICTED data in RAW schema |

### 3.2 Python Monitoring Script Pattern

```python
# governance_monitor.py
# Repeatable, config-driven monitoring runner

import yaml
import pandas as pd
from datetime import datetime, timedelta
from snowflake.connector import connect

class GovernanceMonitor:
    """
    Config-driven 2nd line governance monitoring.
    All thresholds and checks defined in governance_monitor_config.yaml
    """

    def __init__(self, config_path: str, conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = connect(**conn_params)
        self.findings = []

    def run_all_checks(self) -> pd.DataFrame:
        for check in self.config["checks"]:
            result = self._run_check(check)
            self.findings.extend(result)
        return pd.DataFrame(self.findings)

    def _run_check(self, check: dict) -> list:
        cursor = self.conn.cursor()
        cursor.execute(check["query"])
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        findings = []
        for row in rows:
            record = dict(zip(cols, row))
            if self._breaches_threshold(record, check):
                findings.append({
                    "check_id": check["check_id"],
                    "check_name": check["name"],
                    "severity": check["severity"],
                    "finding": record,
                    "run_at": datetime.utcnow().isoformat()
                })
        return findings

    def _breaches_threshold(self, record: dict, check: dict) -> bool:
        if "threshold_field" not in check:
            return True  # Presence of any row is a finding
        field = check["threshold_field"]
        op = check["threshold_operator"]
        val = check["threshold_value"]
        actual = record.get(field)
        if op == "lt": return actual < val
        if op == "gt": return actual > val
        if op == "eq": return actual == val
        if op == "ne": return actual != val
        return False

    def export_report(self, output_path: str):
        df = self.run_all_checks()
        df.to_csv(output_path, index=False)
        return df
```

```yaml
# governance_monitor_config.yaml
checks:
  - check_id: "2LOD-001"
    name: "Unowned Data Assets"
    severity: "HIGH"
    query: |
      SELECT asset_name, domain, created_date
      FROM governance.catalog.assets
      WHERE owner IS NULL
        AND created_date < DATEADD(day, -7, CURRENT_DATE())
    threshold_field: null  # any row = finding

  - check_id: "2LOD-002"
    name: "DQ Pass Rate Below Threshold"
    severity: "CRITICAL"
    query: |
      SELECT asset_name, domain, pass_rate
      FROM governance.dq.daily_summary
      WHERE severity = 'CRITICAL'
        AND run_date = CURRENT_DATE() - 1
    threshold_field: "pass_rate"
    threshold_operator: "lt"
    threshold_value: 0.99

  - check_id: "2LOD-003"
    name: "Overdue Access Certifications"
    severity: "HIGH"
    query: |
      SELECT domain, steward, due_date, days_overdue
      FROM governance.access.certification_status
      WHERE status = 'PENDING'
        AND due_date < CURRENT_DATE()
```

---

## 4. Periodic Review Calendar

| Review | Frequency | Led By | Audience | Output |
|---|---|---|---|---|
| DQ Incident Review | Weekly | DGO | Stewards + Engineering | Incident register update |
| Access Certification Review | Quarterly | DGO | Domain Owners + IT | Certification report |
| Policy Compliance Review | Quarterly | DGO | Governance Council | Compliance scorecard |
| Data Governance Audit | Semi-Annual | DGO | CDO + Risk | Audit report |
| Executive KPI Briefing | Monthly | CDO | Executive team | Governance dashboard |
| Standards Review | Annual | DGO | Council | Updated standards |
| Regulatory Review | As triggered | DGO + Legal | CDO + Risk | Impact assessment |

---

## 5. Audit Execution Guide (2nd Line)

### 5.1 Audit Scope Definition

For each audit cycle, define scope using the **Audit Scope Template**:

```yaml
# audit_scope_YYYY_HX.yaml
audit_id: "DG-AUDIT-2026-H1"
period: "2026-01-01 to 2026-06-30"
domains_in_scope:
  - Finance
  - Customer
  - Product
control_areas:
  - data_ownership           # Verified in Collibra catalog
  - data_classification      # Verified in Collibra + Snowflake/Databricks tag sync
  - access_control           # Collibra access certifications + platform RBAC
  - data_quality             # Collibra DQ results + pipeline pass rates
  - lineage_documentation    # Collibra lineage coverage report
  - policy_exceptions        # Collibra Policy Manager exception log
  - glossary_completeness    # Collibra Business Glossary coverage
risk_rating_basis: "criticality + regulatory exposure"
lead_auditor: "DGO Program Manager"
review_date: "2026-07-15"
```

### 5.2 Control Testing Matrix

| Control Area | Test Method | Evidence Required | Pass Criteria |
|---|---|---|---|
| Data Ownership | Collibra catalog ownership report | Owner field populated in Collibra | 100% of Tier 1 assets owned |
| Classification | Collibra attribute audit + Snowflake/Databricks tag verify | Classification in Collibra and synced to platform | 100% critical columns classified |
| Access Control | Collibra access certification report + role audit | Signed Collibra certifications + RBAC role export | 0 uncertified access entitlements |
| DQ Enforcement | Collibra DQ dashboard + pipeline logs | DQ run logs and Collibra pass/fail summary | 0 CRITICAL violations unresolved >2hrs |
| Lineage | Collibra lineage coverage report | Lineage graph present in Collibra for each asset | >90% of Tier 1 assets have documented lineage |
| Policy Exceptions | Collibra Policy Manager exception log | Approved exception records with expiry dates | 0 exceptions >30 days without review |
| Retention Enforcement | Snowflake/Databricks retention config + Collibra policy attribute | Retention config set + documented in Collibra | 100% of Restricted assets configured |

### 5.3 Audit Finding Severity Ratings

| Rating | Definition | Resolution Timeline |
|---|---|---|
| **Critical** | Material compliance or regulatory risk | 5 business days |
| **High** | Significant control gap | 15 business days |
| **Medium** | Control weakness, compensating control exists | 30 business days |
| **Low** | Process improvement opportunity | 60 business days |
| **Observation** | Best practice recommendation | Next planning cycle |

### 5.4 Audit Report Structure

```markdown
# Data Governance Audit Report — [Period]

## Executive Summary
- Overall Governance Maturity Score: X/5
- Total Findings: N (Critical: X, High: X, Medium: X, Low: X)
- Domains Reviewed: [list]
- Key Risks Identified: [summary]

## Control Area Results
| Control | Result | Finding Count | Maturity |
...

## Detailed Findings
### Finding DG-F-001: [Title]
- Severity: HIGH
- Control Area: Access Control
- Domain: Finance
- Observation: [What was found]
- Risk: [Business impact]
- Root Cause: [Why it happened]
- Recommendation: [What to do]
- Management Response: [1st line response]
- Due Date: [date]
- Owner: [name]

## Remediation Tracker
...

## Trend vs. Prior Period
...
```

---

## 6. Escalation Matrix

| Scenario | Escalation Path | Timeline |
|---|---|---|
| CRITICAL DQ failure unresolved | DGO → Steward → Domain Owner → CDO | 2 hours |
| Unowned asset > 14 days | DGO → Domain Owner | Immediate |
| Access certification not complete | DGO → Steward → Domain Owner → CISO | Day 11 |
| Regulatory data breach / exposure | DGO → CDO → Legal + Compliance | Immediate |
| Repeated policy violations (3+) | DGO → Domain Owner → CDO | Next governance meeting |
| Audit finding — Critical | DGO → CDO → Risk Committee | 5 business days |

---

## 7. KPIs: 2nd Line Performance Metrics

| KPI | Target | Frequency |
|---|---|---|
| % Monitoring checks executed on schedule | 100% | Monthly |
| % Audit findings with remediation plan within SLA | 100% | Per audit |
| % Critical findings resolved within 5 days | 100% | Per audit |
| Policy exception aging > 30 days | 0 | Weekly |
| Governance maturity score trend | Increasing QoQ | Quarterly |
| % Escalations resolved within SLA | > 95% | Monthly |
| Audit report delivery within 10 days of fieldwork | 100% | Per audit |

---

## 8. Benchmarking Framework

### 8.1 Internal Benchmarks (Domain-to-Domain)

Compare governance performance across domains monthly:

| Metric | Finance | Marketing | Operations | Customer | Target |
|---|---|---|---|---|---|
| Asset ownership % | 98% | 82% | 91% | 95% | >95% |
| Classification coverage % | 100% | 75% | 88% | 97% | >98% |
| DQ pass rate (CRITICAL) | 99.8% | 97.2% | 98.5% | 99.1% | >99% |
| Access cert completion % | 100% | 90% | 95% | 100% | 100% |

### 8.2 External Benchmarks

| Framework | Relevance | Benchmark Source |
|---|---|---|
| DAMA DMBOK | Overall governance maturity | DAMA International |
| DCAM (EDM Council) | Data management capability | EDM Council |
| CMMI Data Management | Process maturity | CMMI Institute |
| ISO 8000 | Data quality standards | ISO |
| NIST Privacy Framework | Privacy/PII governance | NIST |

### 8.3 Maturity Scoring Rubric

Score each control area 1–5 quarterly:

```python
# maturity_scorer.py
MATURITY_RUBRIC = {
    "data_ownership": {
        1: "No formal ownership assignments",
        2: "Ownership defined for some critical assets",
        3: "Ownership defined for all Tier 1 assets; formal process",
        4: "All assets owned; quarterly review cycle active",
        5: "Automated ownership assignment; continuous review"
    },
    "data_quality": {
        1: "No formal DQ checks",
        2: "Ad hoc DQ checks on some assets",
        3: "DQ rules registered and automated for Tier 1",
        4: "DQ gates enforced at all pipeline layers; SLA tracked",
        5: "ML-assisted anomaly detection; self-healing pipelines"
    },
    "access_control": {
        1: "No RBAC; ad hoc access",
        2: "RBAC defined but not consistently enforced",
        3: "RBAC enforced; quarterly certifications running",
        4: "ABAC for sensitive data; automated provisioning",
        5: "Zero-trust model; continuous access monitoring"
    }
}

def calculate_maturity_score(domain_scores: dict) -> dict:
    """
    Args:
        domain_scores: {control_area: score_1_to_5}
    Returns:
        dict with overall score and level label
    """
    avg = sum(domain_scores.values()) / len(domain_scores)
    level = (
        "Initial" if avg < 2 else
        "Developing" if avg < 3 else
        "Defined" if avg < 4 else
        "Managed" if avg < 5 else
        "Optimizing"
    )
    return {"score": round(avg, 2), "level": level, "detail": domain_scores}
```

---

*Document Owner: Data Governance Office | Report To: Chief Data Officer | Review Cycle: Semi-Annual*
