# Vendor and Third-Party Data Risk Standard
## Governing External Data Across the Enterprise Data Program

**Document Owner:** Chief Data Officer + Data Governance Office
**Classification:** Internal — Binding Standard
**Version:** 1.0 | **Last Updated:** 2026-03
**Review Cycle:** Annual or upon material vendor change / regulatory update

> **Scope:** This standard applies to all external data relationships — data vendors, data providers, licensed data feeds, research subscriptions, enrichment services, API data sources, data brokers, cloud platform providers with data obligations, and any third party that delivers, processes, or has access to enterprise data. It covers onboarding, risk assessment, contractual requirements, technical integration standards, ongoing monitoring, and offboarding.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Vendor Classification Framework](#2-vendor-classification-framework)
3. [Onboarding Process](#3-onboarding-process)
4. [Risk Assessment Framework](#4-risk-assessment-framework)
5. [Contractual Requirements](#5-contractual-requirements)
6. [Technical Integration Standards](#6-technical-integration-standards)
7. [Ongoing Monitoring and Annual Review](#7-ongoing-monitoring-and-annual-review)
8. [Incident Response — Vendor-Related Events](#8-incident-response--vendor-related-events)
9. [Offboarding and Termination](#9-offboarding-and-termination)
10. [Audit and Compliance](#10-audit-and-compliance)
11. [RACI](#11-raci)
12. [Vendor Registry](#12-vendor-registry)
13. [Configuration Reference](#13-configuration-reference)
14. [Appendix](#14-appendix)

---

## 1. Executive Summary

### 1.1 Why This Standard Exists

Third-party data is one of the highest-risk surface areas in any enterprise data program. External vendors:

- Deliver data whose quality, lineage, and licensing terms we cannot directly control
- May have access to our systems, our customer data, or our regulated data
- Create regulatory exposure if their data handling practices don't meet our obligations
- Can introduce data into our pipelines that bypasses internal governance controls if not properly gated

This standard ensures every third-party data relationship is assessed, contracted, integrated, and monitored to the same rigor we apply to internally produced data — and in several cases, to a higher standard given the reduced control.

### 1.2 Governing Principles

| Principle | Application |
|---|---|
| **No data enters without a gate** | All vendor data must pass Bronze certification before reaching Silver or Gold layers |
| **Contract before connection** | No technical integration begins until data agreements are executed |
| **Classify before ingesting** | PII, classification tier, and permitted use must be determined before any pipeline is built |
| **Vendor risk is our risk** | A vendor's data breach is treated as our data breach for regulatory purposes if we hold their data |
| **Least privilege for all external parties** | No vendor receives broader access than the minimum required for the contracted service |
| **Separation of data** | Vendor data is isolated in dedicated schemas until quality, licensing, and lineage are confirmed |

### 1.3 Regulatory Basis

This standard reflects obligations under:

| Regulation | Relevant Obligation |
|---|---|
| **GDPR** | Controller-to-processor agreements (Art. 28); cross-border transfer restrictions (Art. 46); data subject rights for third-party-sourced PII |
| **CCPA / CPRA** | Service provider agreements; data broker registration obligations; opt-out signal propagation |
| **HIPAA** | Business Associate Agreements (BAA) for any vendor handling PHI |
| **SOX** | Third-party data integrity controls for financial reporting data |
| **PCI DSS** | Vendor access controls for cardholder data environments |
| **State Privacy Laws** | VCDPA, CPA, CTDPA, and others as applicable |

---

## 2. Vendor Classification Framework

### 2.1 Vendor Tiers

All third-party data relationships are classified into one of four tiers based on the data they deliver or can access.

| Tier | Label | Definition | Examples |
|---|---|---|---|
| **V1** | Critical | Delivers or accesses Restricted data (PII, PHI, PCI); directly supports regulated reporting; or has privileged platform access | Credit bureau feeds, healthcare data providers, payroll processors, identity resolution vendors, cloud platform providers (Snowflake, Databricks) |
| **V2** | High | Delivers Confidential business data; enriches internal data with external signals; or has read access to Confidential assets | Financial market data feeds, firmographic enrichment providers, geospatial data vendors, research data subscriptions |
| **V3** | Standard | Delivers Internal-class data with limited regulatory sensitivity; no access to internal systems | Industry benchmarking data, weather data, public firmographic data, open data providers |
| **V4** | Low | Delivers Public data only; no access to internal systems; freely replaceable | Public web scrapes, government open data portals, free API data sources |

### 2.2 Tier Assignment Rules

```
New vendor being evaluated.
          │
          ▼
Does the vendor deliver, process, or have access to PII / PHI / PCI?
     YES → V1 (minimum). See further escalation below.
     NO  ↓

Does the vendor deliver Confidential data or enrich our data with
external signals that are then stored in Gold or certified assets?
     YES → V2
     NO  ↓

Does the vendor deliver Internal-class data (operationally sensitive,
not publicly available) with no system access?
     YES → V3
     NO  ↓

Vendor delivers Public data only, no system access → V4
```

**V1 Escalation Rules:**

| Condition | Additional Designation |
|---|---|
| Vendor processes EU data subject PII | V1 + GDPR DPA required |
| Vendor processes PHI | V1 + HIPAA BAA required |
| Vendor has direct platform access (Snowflake, Databricks, Collibra) | V1 + Platform Access Review required |
| Vendor is a data broker (as defined by CCPA) | V1 + Data Broker Addendum required |
| Vendor delivers data used in T1 ML models | V1 + ML Data Provenance Assessment required |

### 2.3 Tier Review Triggers

Tier assignment is reviewed when:
- Contract renewal occurs
- Vendor scope expands (new data types, new platform access)
- A regulatory change affects the data category
- A vendor incident occurs
- The internal use of the data changes (e.g., data previously used for internal reporting is now used in a T1 ML model)

---

## 3. Onboarding Process

### 3.1 Process Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1        STAGE 2         STAGE 3        STAGE 4    STAGE 5  │
│  Intake &       Risk            Contract        Technical  Go-Live  │
│  Classification Assessment      Execution       Setup      & Gate  │
│                                                                     │
│  DGO            DGO + CISO      Legal + DGO     DE + IT    DE + DGO │
│  2–3 days       5–10 days       5–30 days       5–10 days  1–3 days │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Stage 1 — Intake and Classification (2–3 Business Days)

**Trigger:** Any team seeking to onboard a new data vendor submits a Vendor Data Intake Request via the Collibra governance workflow.

**Required information at intake:**

```yaml
# vendor_intake_request.yaml
vendor:
  name: "Acme Data Inc."
  website: "https://acmedata.com"
  primary_contact: "contact@acmedata.com"
  parent_company: ""           # if applicable

data_description:
  data_type: "Consumer credit attributes"
  classification_proposed: "RESTRICTED"
  contains_pii: true
  contains_phi: false
  contains_pci: false
  delivery_method: "SFTP"     # SFTP | API | Snowflake Share | S3 | Other
  delivery_frequency: "Daily"
  estimated_volume_rows: 5000000
  geographic_scope: "US"
  data_subjects: "Consumers"  # Consumers | Employees | Business entities | None

intended_use:
  business_use_case: "Credit risk model feature enrichment"
  downstream_assets: ["ml_features.credit.dim_credit_attributes"]
  used_in_t1_model: true
  used_in_regulatory_reporting: false
  used_in_external_facing_product: false

requestor:
  name: "Jane Smith"
  team: "ML Engineering"
  domain_owner_approval: true
  domain_owner_name: "John Doe"
```

**Stage 1 outputs:**
- Vendor tier assignment (DGO)
- Initial data classification assignment (DGO)
- Confirmation of required agreement types (Legal)
- Approval to proceed to Stage 2 or rejection with rationale

**Stage 1 rejection criteria:**
- Vendor cannot demonstrate a legal basis for holding the data they are offering
- Data cannot be legally received under applicable regulation
- No clear business use case tied to an approved domain objective
- Duplicate of an existing vendor relationship without justification

### 3.3 Stage 2 — Risk Assessment (5–10 Business Days)

Risk assessment depth scales with vendor tier:

| Assessment Component | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| Vendor Security Questionnaire (full) | ✅ Required | ✅ Required | — | — |
| Vendor Security Questionnaire (abbreviated) | — | — | ✅ Required | — |
| SOC 2 Type II review | ✅ Required | ✅ Required | Optional | — |
| Penetration test evidence review | ✅ Required | Optional | — | — |
| Privacy program assessment | ✅ Required | ✅ Required | — | — |
| Sub-processor disclosure review | ✅ Required | ✅ Required | — | — |
| Data lineage and provenance documentation | ✅ Required | ✅ Required | ✅ Required | Optional |
| CISO sign-off | ✅ Required | ✅ Required | — | — |
| Privacy Officer sign-off | ✅ Required (PII/PHI) | ✅ Required (PII) | — | — |
| CDO sign-off | ✅ Required | — | — | — |

**Acceptable risk assessment outcomes:**

| Outcome | Meaning | Next Step |
|---|---|---|
| **Pass** | Vendor meets all required standards for their tier | Proceed to Stage 3 |
| **Pass with Conditions** | Vendor meets minimum bar; specific remediation required within 90 days | Proceed to Stage 3; track remediation |
| **Deferred** | Additional information needed from vendor | Re-assess within 30 days |
| **Fail** | Vendor does not meet minimum bar; known security deficiencies; regulatory non-compliance | Do not proceed; document and inform requestor |

**Risk scoring model:**

```python
# vendor_risk_scorer.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import yaml
from pathlib import Path


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class VendorRiskAssessment:
    vendor_name: str
    tier: str
    soc2_type2_available: bool
    soc2_clean: bool                    # No qualified opinions
    pentest_within_12_months: bool
    pentest_no_critical_findings: bool
    gdpr_compliant: bool
    ccpa_compliant: bool
    subprocessors_disclosed: bool
    subprocessors_acceptable: bool      # No subprocessors in high-risk jurisdictions
    data_lineage_documented: bool
    breach_history_3yr: bool            # True = has had a breach
    breach_notified_timely: bool        # If breach, did they notify within required window?
    encryption_at_rest: bool
    encryption_in_transit: bool
    mfa_enforced: bool
    incident_response_plan: bool
    data_retention_policy: bool
    data_deletion_capability: bool      # Can execute deletion requests (GDPR Art. 17)

    # Computed
    risk_score: int = field(init=False)
    risk_level: RiskLevel = field(init=False)
    blocking_findings: list[str] = field(init=False)
    conditional_findings: list[str] = field(init=False)

    def __post_init__(self):
        self.blocking_findings = []
        self.conditional_findings = []
        self.risk_score = self._compute_score()
        self.risk_level = self._compute_level()

    def _compute_score(self) -> int:
        score = 0

        # Blocking findings (automatic fail regardless of score)
        if not self.encryption_at_rest:
            self.blocking_findings.append("No encryption at rest — automatic fail")
        if not self.encryption_in_transit:
            self.blocking_findings.append("No encryption in transit — automatic fail")
        if self.breach_history_3yr and not self.breach_notified_timely:
            self.blocking_findings.append(
                "Breach in last 3 years with late/no notification — automatic fail"
            )
        if not self.subprocessors_acceptable:
            self.blocking_findings.append(
                "Subprocessors in restricted jurisdictions — automatic fail"
            )

        # Scored findings
        if not self.soc2_type2_available:
            score += 30
            self.conditional_findings.append("No SOC 2 Type II — obtain within 90 days")
        elif not self.soc2_clean:
            score += 15
            self.conditional_findings.append("Qualified SOC 2 — review qualified opinions")

        if not self.pentest_within_12_months:
            score += 20
            self.conditional_findings.append("No recent pentest — require within 90 days")
        elif not self.pentest_no_critical_findings:
            score += 25
            self.conditional_findings.append("Critical pentest findings — require remediation evidence")

        if not self.mfa_enforced:
            score += 20
            self.conditional_findings.append("MFA not enforced — require before go-live")

        if not self.incident_response_plan:
            score += 10
            self.conditional_findings.append("No documented IRP — require within 60 days")

        if not self.data_lineage_documented:
            score += 15
            self.conditional_findings.append("Data lineage undocumented — require before go-live")

        if not self.data_deletion_capability:
            score += 20
            self.conditional_findings.append("Cannot execute deletion requests — required for GDPR")

        if self.breach_history_3yr:
            score += 10
            self.conditional_findings.append(
                "Breach history — enhanced monitoring required"
            )

        return score

    def _compute_level(self) -> RiskLevel:
        if self.blocking_findings:
            return RiskLevel.CRITICAL
        if self.risk_score >= 50:
            return RiskLevel.HIGH
        if self.risk_score >= 25:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def to_report(self) -> dict:
        return {
            "vendor": self.vendor_name,
            "tier": self.tier,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level.value,
            "outcome": "FAIL" if self.blocking_findings else
                       "PASS WITH CONDITIONS" if self.conditional_findings else "PASS",
            "blocking_findings": self.blocking_findings,
            "conditional_findings": self.conditional_findings,
        }


def assess_from_yaml(path: str) -> dict:
    with open(path) as f:
        data = yaml.safe_load(f)
    assessment = VendorRiskAssessment(**data["assessment"])
    return assessment.to_report()
```

### 3.4 Stage 3 — Contract Execution (5–30 Business Days)

Legal leads contract negotiation. DGO must review and sign off on data-specific clauses before execution.

**Minimum contract lead times:**
- V1 vendor: 20–30 business days (Legal review + DGO + CISO + CDO sign-off)
- V2 vendor: 10–15 business days (Legal review + DGO sign-off)
- V3 vendor: 5–10 business days (Legal review; DGO informed)
- V4 vendor: 3–5 business days (Legal standard terms review)

See Section 5 for required contractual provisions.

### 3.5 Stage 4 — Technical Setup (5–10 Business Days)

DE owns technical integration. All setup follows the standards in Section 6.

**Pre-build checklist:**

```
□ Data agreement executed and filed in contract repository
□ Vendor tier and classification confirmed in Collibra
□ Permitted use documented (what we can and cannot do with this data)
□ Schema and data dictionary received from vendor
□ PII fields identified and classification applied
□ Dedicated Bronze schema created for this vendor
□ Connection method approved by IT (SFTP, API, Snowflake Share, etc.)
□ Credentials stored in secrets manager — not hardcoded
□ Network connection approved (PrivateLink, IP allowlist, VPN as required)
□ Service account created with minimum required permissions
□ DQ rules defined based on vendor SLA and data contract
□ Audit logging enabled on all vendor data access paths
```

### 3.6 Stage 5 — Go-Live Gate (1–3 Business Days)

Before any vendor data reaches Silver or Gold layers:

| Gate Check | Owner | Pass Criterion |
|---|---|---|
| Bronze DQ validation (schema, not-null, row count) | DE | All CRITICAL rules passing |
| Classification tags applied to all PII/Restricted columns | DE | 100% coverage confirmed |
| Lineage documented from vendor source to Bronze | DE | Collibra lineage entry created |
| Permitted use documented in Collibra asset | DGO | Permitted use field populated |
| Vendor registered in Vendor Registry | DGO | Registry entry created with all required fields |
| Data contract signed between vendor (as data source) and consuming domain | DE / DGO | Signed contract on file |
| Access restricted to approved consumers only | IT / DE | No broad grants; RBAC confirmed |


---

## 4. Risk Assessment Framework

### 4.1 Risk Dimensions

Every vendor is assessed across five risk dimensions. The combination determines the overall residual risk profile and the monitoring intensity applied post-onboarding.

| Dimension | Description | Factors |
|---|---|---|
| **Data Sensitivity Risk** | Risk arising from the type of data delivered | Classification tier; PII/PHI/PCI; data subject type; regulatory scope |
| **Access Risk** | Risk from vendor access to internal systems | Platform access level; credential type; human vs. automated; scope of access |
| **Concentration Risk** | Risk from operational dependence | Unique vs. replaceable; number of downstream assets; SLA criticality |
| **Compliance Risk** | Risk from regulatory non-conformance | Jurisdiction; applicable regulations; vendor compliance posture; certification status |
| **Supply Chain Risk** | Risk from the vendor's own third parties | Sub-processor count; sub-processor jurisdictions; sub-processor audit coverage |

### 4.2 Inherent Risk Matrix

| Data Sensitivity | No System Access | Read-Only Access | Write Access | Admin / Privileged |
|---|---|---|---|---|
| **Restricted (PII/PHI/PCI)** | HIGH | CRITICAL | CRITICAL | CRITICAL |
| **Confidential** | MEDIUM | HIGH | CRITICAL | CRITICAL |
| **Internal** | LOW | MEDIUM | HIGH | CRITICAL |
| **Public** | LOW | LOW | MEDIUM | HIGH |

### 4.3 Residual Risk After Controls

Residual risk is inherent risk adjusted downward by the presence of controls:

| Control Present | Risk Reduction |
|---|---|
| SOC 2 Type II (clean, within 12 months) | -1 level |
| End-to-end encryption (at rest + in transit) | -1 level |
| MFA enforced for all vendor personnel with access | -0.5 level |
| Annual penetration test (no critical findings) | -0.5 level |
| Contractual right-to-audit | -0.5 level |
| Cyber insurance (minimum $5M coverage for V1) | -0.5 level |

**Floor rule:** Residual risk for V1 vendors cannot be reduced below MEDIUM regardless of controls. CRITICAL inherent risk with all controls present = HIGH residual.

### 4.4 Risk-Based Monitoring Intensity

| Residual Risk | Review Frequency | Monitoring Type |
|---|---|---|
| **CRITICAL** | Quarterly | Enhanced: automated anomaly detection + manual quarterly review + annual on-site/virtual assessment |
| **HIGH** | Semi-Annual | Standard: automated monitoring + semi-annual review + annual questionnaire |
| **MEDIUM** | Annual | Standard: annual questionnaire + automated DQ monitoring |
| **LOW** | Bi-Annual | Minimal: bi-annual check-in; automated DQ monitoring |

### 4.5 Automated Vendor Risk Monitor

```python
# vendor_risk_monitor.py
import snowflake.connector
import requests
import yaml
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VendorHealthSignal:
    vendor_id: str
    vendor_name: str
    tier: str
    check_date: datetime
    dq_pass_rate_7d: float
    freshness_sla_breaches_7d: int
    schema_drift_detected: bool
    row_volume_anomaly: bool          # > 2 std deviations from 30-day avg
    null_rate_anomaly: bool           # PK or critical cols exceed threshold
    contract_expiry_days: int
    cert_expiry_days: int             # SOC 2, security cert, etc.
    overall_health: str               # GREEN | AMBER | RED


class VendorRiskMonitor:
    """
    Runs nightly health checks across all active vendor data feeds.
    Results written to governance.vendor_monitoring.daily_health and
    flagged to DGO if any signal turns RED or AMBER.
    """

    def __init__(self, config_path: str, snow_conn_params: dict):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.conn = snowflake.connector.connect(**snow_conn_params)
        self.cursor = self.conn.cursor()
        self.run_date = datetime.now(timezone.utc)

    def run_all_vendors(self) -> list[VendorHealthSignal]:
        signals = []
        for vendor in self.config["vendors"]:
            if vendor["status"] != "ACTIVE":
                continue
            try:
                signal = self._check_vendor(vendor)
                signals.append(signal)
                self._write_signal(signal)
                if signal.overall_health in ("RED", "AMBER"):
                    self._raise_alert(signal)
            except Exception as e:
                logger.error(f"Health check failed for {vendor['name']}: {e}")
        return signals

    def _check_vendor(self, vendor: dict) -> VendorHealthSignal:
        vid = vendor["vendor_id"]
        bronze_table = vendor["bronze_table"]

        dq_pass_rate = self._get_dq_pass_rate(bronze_table)
        freshness_breaches = self._get_freshness_breaches(bronze_table, vendor["freshness_sla_hours"])
        schema_drift = self._detect_schema_drift(vid, bronze_table)
        volume_anomaly = self._detect_volume_anomaly(bronze_table)
        null_anomaly = self._detect_null_anomaly(bronze_table, vendor.get("critical_columns", []))
        contract_days = self._days_until(vendor["contract_expiry_date"])
        cert_days = self._days_until(vendor.get("soc2_expiry_date"))

        health = self._compute_health(
            dq_pass_rate, freshness_breaches, schema_drift,
            volume_anomaly, null_anomaly, contract_days, cert_days
        )

        return VendorHealthSignal(
            vendor_id=vid,
            vendor_name=vendor["name"],
            tier=vendor["tier"],
            check_date=self.run_date,
            dq_pass_rate_7d=dq_pass_rate,
            freshness_sla_breaches_7d=freshness_breaches,
            schema_drift_detected=schema_drift,
            row_volume_anomaly=volume_anomaly,
            null_rate_anomaly=null_anomaly,
            contract_expiry_days=contract_days,
            cert_expiry_days=cert_days,
            overall_health=health,
        )

    def _get_dq_pass_rate(self, table: str) -> float:
        sql = f"""
            SELECT
                COUNT_IF(dq_status = 'PASS') / NULLIF(COUNT(*), 0) AS pass_rate
            FROM governance.dq_results
            WHERE asset_name = '{table}'
              AND run_date >= DATEADD('day', -7, CURRENT_DATE())
        """
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return float(row[0] or 0.0)

    def _get_freshness_breaches(self, table: str, sla_hours: int) -> int:
        sql = f"""
            SELECT COUNT(*) FROM governance.dq_results
            WHERE asset_name = '{table}'
              AND rule_type = 'freshness'
              AND dq_status = 'FAIL'
              AND run_date >= DATEADD('day', -7, CURRENT_DATE())
        """
        self.cursor.execute(sql)
        return int(self.cursor.fetchone()[0])

    def _detect_schema_drift(self, vendor_id: str, table: str) -> bool:
        sql = f"""
            SELECT COUNT(*) FROM governance.vendor_schema_snapshots
            WHERE vendor_id = '{vendor_id}'
              AND snapshot_date = CURRENT_DATE()
              AND column_hash != (
                  SELECT column_hash FROM governance.vendor_schema_snapshots
                  WHERE vendor_id = '{vendor_id}'
                  AND snapshot_date = DATEADD('day', -1, CURRENT_DATE())
                  LIMIT 1
              )
        """
        self.cursor.execute(sql)
        return int(self.cursor.fetchone()[0]) > 0

    def _detect_volume_anomaly(self, table: str) -> bool:
        sql = f"""
            WITH daily_counts AS (
                SELECT DATE(load_timestamp) AS load_date,
                       COUNT(*) AS row_count
                FROM {table}
                WHERE load_timestamp >= DATEADD('day', -30, CURRENT_DATE())
                GROUP BY 1
            ),
            stats AS (
                SELECT AVG(row_count) AS avg_count,
                       STDDEV(row_count) AS std_count
                FROM daily_counts
                WHERE load_date < CURRENT_DATE()
            ),
            today AS (
                SELECT COUNT(*) AS today_count
                FROM {table}
                WHERE DATE(load_timestamp) = CURRENT_DATE()
            )
            SELECT
                CASE WHEN ABS(today.today_count - stats.avg_count) > 2 * stats.std_count
                     THEN 1 ELSE 0 END AS is_anomaly
            FROM today CROSS JOIN stats
        """
        self.cursor.execute(sql)
        return int(self.cursor.fetchone()[0]) == 1

    def _detect_null_anomaly(self, table: str, critical_cols: list[str]) -> bool:
        if not critical_cols:
            return False
        for col in critical_cols:
            sql = f"""
                SELECT COUNT_IF({col} IS NULL) / NULLIF(COUNT(*), 0)
                FROM {table}
                WHERE DATE(load_timestamp) = CURRENT_DATE()
            """
            self.cursor.execute(sql)
            null_rate = float(self.cursor.fetchone()[0] or 0.0)
            if null_rate > 0.01:   # >1% null on critical column
                return True
        return False

    def _days_until(self, date_str: Optional[str]) -> int:
        if not date_str:
            return 9999
        expiry = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (expiry - self.run_date).days

    def _compute_health(
        self, dq_rate, freshness_breaches, schema_drift,
        volume_anomaly, null_anomaly, contract_days, cert_days
    ) -> str:
        if (dq_rate < 0.90 or freshness_breaches >= 3 or
                null_anomaly or contract_days <= 30 or cert_days <= 30):
            return "RED"
        if (dq_rate < 0.95 or freshness_breaches >= 1 or schema_drift or
                volume_anomaly or contract_days <= 60 or cert_days <= 60):
            return "AMBER"
        return "GREEN"

    def _raise_alert(self, signal: VendorHealthSignal):
        logger.warning(
            f"Vendor health alert [{signal.overall_health}]: "
            f"{signal.vendor_name} (Tier {signal.tier}) — "
            f"DQ: {signal.dq_pass_rate_7d:.1%}, "
            f"Freshness breaches: {signal.freshness_sla_breaches_7d}, "
            f"Contract expires in: {signal.contract_expiry_days}d"
        )

    def _write_signal(self, s: VendorHealthSignal):
        sql = """
            INSERT INTO governance.vendor_monitoring.daily_health
            (vendor_id, vendor_name, tier, check_date, dq_pass_rate_7d,
             freshness_sla_breaches_7d, schema_drift_detected,
             row_volume_anomaly, null_rate_anomaly,
             contract_expiry_days, cert_expiry_days, overall_health)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            s.vendor_id, s.vendor_name, s.tier,
            s.check_date.date(), s.dq_pass_rate_7d,
            s.freshness_sla_breaches_7d, s.schema_drift_detected,
            s.row_volume_anomaly, s.null_rate_anomaly,
            s.contract_expiry_days, s.cert_expiry_days, s.overall_health
        ))
        self.conn.commit()
```

---

## 5. Contractual Requirements

### 5.1 Required Agreement Types by Vendor Tier

| Agreement | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| Master Data Services Agreement (MDSA) | ✅ Required | ✅ Required | ✅ Required | Optional (standard ToS review) |
| Data Processing Agreement / DPA | ✅ Required if EU data | ✅ Required if EU data | Optional | — |
| Business Associate Agreement (BAA) | ✅ Required if PHI | — | — | — |
| Data Usage Agreement (DUA) / Permitted Use Addendum | ✅ Required | ✅ Required | ✅ Required | — |
| Data Broker Addendum | ✅ Required if data broker | — | — | — |
| Information Security Addendum | ✅ Required | ✅ Required | — | — |
| Non-Disclosure Agreement (NDA) | ✅ Required | ✅ Required | ✅ Required | — |

### 5.2 Required Contractual Provisions

The following clauses are mandatory in all vendor data agreements at the indicated tier. Legal owns drafting; DGO confirms inclusion before execution.

#### 5.2.1 Data Use and Restrictions

```
REQUIRED CLAUSE — Permitted Use and Restrictions

a) Permitted Use. Recipient may use the Data solely for the purposes 
   described in Schedule A (Use Case Description) and for no other purpose.

b) Prohibited Uses. Recipient shall not:
   i.   Re-sell, license, or sub-license the Data to any third party.
   ii.  Use the Data to contact data subjects directly unless expressly
        permitted in Schedule A.
   iii. Combine the Data with other data sources in a manner that creates 
        a new commercially exploitable data product.
   iv.  Use the Data to train generative AI models unless expressly agreed 
        in writing by Provider.
   v.   Retain the Data beyond the period specified in Schedule B 
        (Retention and Deletion Schedule).

c) Derivative Works. [V1/V2] Any data product derived in whole or part 
   from the Data is subject to the same use restrictions as the underlying 
   Data unless Provider grants written permission for broader use.
```

#### 5.2.2 Data Quality Obligations

```
REQUIRED CLAUSE — Data Quality Representations (V1/V2)

Provider represents and warrants that:
   a) The Data will conform to the schema and format described in Schedule C.
   b) The Data will be complete and accurate in all material respects.
   c) The Data will be delivered within the SLA specified in Schedule D.
   d) Provider will notify Recipient within [24 hours for V1 / 48 hours for V2] 
      of any known data quality issue or delivery failure.
   e) Provider will maintain and make available a documented data lineage 
      trail showing the original source and transformation history of the Data.
```

#### 5.2.3 Security Requirements

```
REQUIRED CLAUSE — Security Standards (V1/V2)

Provider shall maintain, at minimum, the following security controls:
   a) Encryption of all Data in transit using TLS 1.2 or higher.
   b) Encryption of all Data at rest using AES-256 or equivalent.
   c) Multi-factor authentication for all personnel with access to Data 
      or systems processing Data on Recipient's behalf.
   d) Annual penetration testing by a qualified third party; results 
      available to Recipient upon request (executive summary level).
   e) SOC 2 Type II certification maintained and current; full report 
      available to Recipient under NDA.
   f) Incident detection and response capability; documented IRP 
      available to Recipient upon request.
```

#### 5.2.4 Breach Notification

```
REQUIRED CLAUSE — Breach Notification

Provider shall notify Recipient in writing within:
   - [V1, GDPR-scoped data]: 24 hours of discovery of any actual or 
     suspected Data Breach
   - [V1, all other]: 48 hours of discovery
   - [V2]: 48 hours of discovery

Notification shall include: (i) nature and scope of the breach; 
(ii) categories and estimated number of data records affected; 
(iii) likely consequences; (iv) measures taken or proposed.

Recipient's right to notify data subjects and regulators is not 
contingent on receipt of Provider's notification.
```

#### 5.2.5 Data Subject Rights (V1 — PII/PHI)

```
REQUIRED CLAUSE — Data Subject Rights

Provider shall:
   a) Within [5 business days] of Recipient's written request, provide all 
      information necessary to fulfill a data subject's rights request 
      (access, correction, erasure, portability, objection).
   b) Implement and honor suppression or opt-out signals for data subjects 
      who have exercised their rights with Recipient.
   c) Maintain a documented process for receiving and responding to 
      direct data subject rights requests.
   d) [GDPR] Cooperate with Recipient to fulfill obligations under GDPR 
      Articles 12–22 within required timeframes.
```

#### 5.2.6 Audit Rights

```
REQUIRED CLAUSE — Audit Rights (V1/V2)

Recipient reserves the right, upon [30 days'] written notice, to:
   a) Conduct an information security assessment of Provider's systems 
      and processes related to the Data, no more than once per year.
   b) Request and receive copies of Provider's most recent SOC 2 Type II 
      report, penetration test executive summary, and privacy impact 
      assessments.
   c) Review Provider's sub-processor list and request information about 
      sub-processors' security practices.
Provider shall reasonably cooperate with such assessments at no charge 
for standard requests.
```

#### 5.2.7 Termination and Data Return / Deletion

```
REQUIRED CLAUSE — Termination and Data Disposal

Upon expiration or termination of this Agreement for any reason:
   a) Provider shall immediately cease delivery of Data to Recipient.
   b) Recipient shall, within [30 days] of termination: (i) delete or 
      destroy all copies of the Data in all formats and environments, 
      including backups; or (ii) return all copies of the Data to 
      Provider if requested.
   c) [V1] Recipient shall provide Provider with written certification 
      of deletion within [45 days] of termination.
   d) Notwithstanding the above, Recipient may retain copies of Data 
      solely to the extent required by applicable law or regulation, 
      provided that retained Data is held under equivalent security 
      controls and its use is limited to regulatory compliance purposes.
```

### 5.3 Contractual Non-Negotiables

The following provisions are non-negotiable. Legal must not agree to terms that contradict these, regardless of vendor pushback. Escalate to CDO if a vendor refuses.

| Non-Negotiable | Rationale |
|---|---|
| 24–48 hour breach notification (V1) | GDPR Art. 33 requires 72-hour supervisory authority notification; we need time to act |
| Right to audit | Required for SOX internal controls; required for regulated data handling |
| Sub-processor disclosure | Required to comply with GDPR Art. 28(2); supply chain risk visibility |
| Data deletion on termination | GDPR right to erasure; CCPAobligation; data minimization |
| Prohibited re-identification clause | Prevents nominal "anonymized" data from being legally reassembled |
| Governing law (our jurisdiction) | Ensures contractual remedies are enforceable |

### 5.4 Contractual Red Flags

The following vendor contract positions require DGO escalation and CDO review before execution:

| Red Flag | Risk |
|---|---|
| Vendor claims unlimited license to use our data for their own purposes | Our internal data may be used to train competitor models or sold |
| No sub-processor disclosure or "right to use any sub-processor" | Uncontrolled data flow to unknown third parties |
| Limitation of liability cap below the value of the data contract | Insufficient recourse in case of breach |
| No SLA or SLA with no financial remedy | No incentive for vendor to maintain data quality |
| "Jurisdiction of vendor's choosing" for governing law | Contractual remedies may be unenforceable |
| Data ownership clause claiming vendor owns derived works | May prevent us from using our own analytical outputs |
| No breach notification obligation | Violates our regulatory obligations to notify regulators and data subjects |


---

## 6. Technical Integration Standards

### 6.1 Vendor Data Isolation Architecture

All vendor data is isolated in dedicated Bronze schemas until it has passed quality gates and the permitted use has been confirmed. This prevents unvalidated, unlicensed, or misclassified data from contaminating certified internal assets.

```
┌─────────────────────────────────────────────────────────────────────┐
│  VENDOR ISOLATION ZONE                                              │
│  Snowflake: vendor_bronze.{vendor_id}.raw_{feed_name}              │
│  Databricks: vendor_bronze.{vendor_id}.raw_{feed_name}             │
│                                                                     │
│  Access: DE service account only (no analyst access)               │
│  Retention: 90 days (Bronze layer standard)                        │
│  Lineage: Tracked from first load                                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │ passes Bronze gate (DQ + classification)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  SILVER INTEGRATION ZONE                                            │
│  Standard Silver schemas with vendor data merged/conformed          │
│  PII masking applied; DGO PII review completed                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │ passes Silver gate + permitted use confirmed
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GOLD / CERTIFIED CONSUMPTION                                       │
│  Vendor data available in certified assets per permitted use terms  │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Delivery Method Standards

#### SFTP

```yaml
# config/vendors/{vendor_id}/sftp.yaml
sftp:
  host: "sftp.vendor.com"
  port: 22
  username_secret: "prod/vendor/{vendor_id}/sftp_username"
  private_key_secret: "prod/vendor/{vendor_id}/sftp_private_key"
  remote_path: "/outbound/enterprise_client/"
  file_pattern: "data_export_*.csv.gpg"
  pgp_key_secret: "prod/vendor/{vendor_id}/pgp_private_key"   # if encrypted delivery
  host_key_fingerprint: "SHA256:abc123..."                     # pin for MITM prevention

delivery:
  expected_frequency: "daily"
  expected_arrival_window_utc: "02:00-06:00"
  sla_hours: 6
  alert_on_missing: true
  alert_webhook: "${SLACK_WEBHOOK_DATA_ALERTS}"
```

#### REST API

```yaml
# config/vendors/{vendor_id}/api.yaml
api:
  base_url: "https://api.vendor.com/v2"
  auth_type: "oauth2_client_credentials"   # oauth2_client_credentials | api_key | mtls
  client_id_secret: "prod/vendor/{vendor_id}/api_client_id"
  client_secret_secret: "prod/vendor/{vendor_id}/api_client_secret"
  token_endpoint: "https://auth.vendor.com/oauth/token"
  scopes: ["data:read"]

  # Rate limiting
  rate_limit_requests_per_minute: 100
  retry_max_attempts: 3
  retry_backoff_seconds: [5, 30, 120]

  # TLS
  verify_ssl: true
  tls_min_version: "TLSv1.2"

pagination:
  type: "cursor"   # cursor | offset | page
  cursor_field: "next_cursor"
  page_size: 1000
```

#### Snowflake Secure Data Share

```sql
-- For vendors delivering via Snowflake Data Share
-- Always consume via a dedicated inbound share database; never grant direct access

-- 1. Create an inbound share database (DE + IT — CAB review required for V1)
CREATE DATABASE vendor_{vendor_id}_share
  FROM SHARE {vendor_account}.{share_name};

-- 2. Grant access to DE service account only
GRANT IMPORTED PRIVILEGES ON DATABASE vendor_{vendor_id}_share
  TO ROLE de_service_account_role;

-- 3. Create Bronze table from share via COPY INTO (never direct SELECT from share in prod)
CREATE OR REPLACE TABLE vendor_bronze.{vendor_id}.raw_{feed_name}
  CLONE vendor_{vendor_id}_share.{schema}.{table};

-- 4. Log the copy event for lineage
INSERT INTO governance.lineage.vendor_load_log
  (vendor_id, load_timestamp, source_object, target_object, row_count, loaded_by)
VALUES
  ('{vendor_id}', CURRENT_TIMESTAMP(), 
   'vendor_{vendor_id}_share.{schema}.{table}',
   'vendor_bronze.{vendor_id}.raw_{feed_name}',
   (SELECT COUNT(*) FROM vendor_bronze.{vendor_id}.raw_{feed_name}),
   CURRENT_USER());
```

### 6.3 Mandatory Bronze Audit Columns

Every vendor data table loaded into the Bronze layer must include these audit columns. These are added by the ingestion pipeline — they are not expected from the vendor.

```sql
-- Audit columns added by pipeline at load time
ALTER TABLE vendor_bronze.{vendor_id}.raw_{feed_name} ADD COLUMN IF NOT EXISTS
  _vendor_id              VARCHAR NOT NULL,      -- e.g. 'acme_data'
  _feed_name              VARCHAR NOT NULL,      -- e.g. 'consumer_credit_v2'
  _vendor_contract_id     VARCHAR NOT NULL,      -- links to vendor registry
  _load_timestamp         TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  _load_batch_id          VARCHAR NOT NULL,      -- pipeline run ID
  _source_file_name       VARCHAR,               -- SFTP / S3 source file
  _source_row_hash        VARCHAR NOT NULL,      -- SHA-256 of source row for dedup
  _permitted_use_version  VARCHAR NOT NULL,      -- version of DUA in effect at load time
  _classification         VARCHAR NOT NULL,      -- assigned at column level; stored here for table-level lineage
  _retention_expiry_date  DATE NOT NULL;         -- computed from retention policy
```

### 6.4 Vendor-Specific DQ Rules Template

```yaml
# config/vendors/{vendor_id}/dq_rules.yaml
vendor_id: "acme_data"
feed_name: "consumer_credit_v2"
bronze_table: "vendor_bronze.acme_data.raw_consumer_credit_v2"

rules:
  # Schema validation
  - rule_id: "VDQ-ACME-001"
    type: "schema_match"
    expected_schema_version: "2.1"
    severity: "CRITICAL"
    sla_hours: 1
    description: "Schema must match contracted version 2.1"

  # Freshness
  - rule_id: "VDQ-ACME-002"
    type: "freshness"
    column: "_load_timestamp"
    max_age_hours: 26                  # daily + 2hr buffer
    severity: "CRITICAL"
    sla_hours: 2
    description: "Daily feed must arrive within 26 hours of previous load"

  # Row volume
  - rule_id: "VDQ-ACME-003"
    type: "row_count_range"
    min_rows: 4500000
    max_rows: 5500000
    severity: "HIGH"
    sla_hours: 4
    description: "Daily record count must be within 10% of contracted volume"

  # PII completeness (critical columns)
  - rule_id: "VDQ-ACME-004"
    type: "not_null"
    column: "consumer_id"
    severity: "CRITICAL"
    sla_hours: 1
    description: "Consumer ID must never be null — primary key"

  - rule_id: "VDQ-ACME-005"
    type: "not_null"
    column: "score_date"
    severity: "HIGH"
    sla_hours: 4
    description: "Score date required for temporal joins"

  # Value validity
  - rule_id: "VDQ-ACME-006"
    type: "value_in_set"
    column: "score_band"
    allowed_values: ["A", "B", "C", "D", "E", "F"]
    severity: "HIGH"
    sla_hours: 4
    description: "Score band must be one of contracted values"

  # Duplication
  - rule_id: "VDQ-ACME-007"
    type: "uniqueness"
    columns: ["consumer_id", "score_date"]
    severity: "HIGH"
    sla_hours: 4
    description: "One record per consumer per date"

  # Lineage / provenance
  - rule_id: "VDQ-ACME-008"
    type: "not_null"
    column: "_permitted_use_version"
    severity: "CRITICAL"
    sla_hours: 1
    description: "Permitted use version must be stamped on every row"

# Failure actions
on_critical_failure:
  action: "block_silver_promotion"
  notify: ["dgo@company.com", "de-oncall@company.com"]
  open_incident: true
  incident_type: "INC-DQ"

on_high_failure:
  action: "allow_silver_with_flag"
  notify: ["de-oncall@company.com"]
  open_incident: false
```

### 6.5 Permitted Use Enforcement

The permitted use recorded at contract execution is stamped into metadata and enforced programmatically to prevent data from being used beyond licensed scope.

```python
# permitted_use_enforcer.py
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class PermittedUse:
    vendor_id: str
    contract_id: str
    version: str
    allowed_uses: list[str]           # e.g. ["internal_analytics", "ml_feature_engineering"]
    prohibited_uses: list[str]        # e.g. ["external_sharing", "model_training_generative_ai"]
    allowed_downstream_assets: list[str]   # specific table/model names
    pii_restriction: str              # "masked_only" | "full_access_with_dua" | "no_pii"
    geographic_restriction: Optional[str]  # e.g. "US_only"
    expiry_date: str                  # ISO date string


class PermittedUseEnforcer:
    """
    Called before any pipeline promotes vendor data from Bronze to Silver or higher.
    Blocks promotion if the intended use is not in the permitted use scope.
    Register new downstream assets via Collibra before promoting.
    """

    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self._cache: dict[str, PermittedUse] = {}

    def load_vendor(self, vendor_id: str) -> PermittedUse:
        if vendor_id not in self._cache:
            path = self.config_dir / "vendors" / vendor_id / "permitted_use.yaml"
            with open(path) as f:
                data = yaml.safe_load(f)
            self._cache[vendor_id] = PermittedUse(**data["permitted_use"])
        return self._cache[vendor_id]

    def assert_use_permitted(
        self,
        vendor_id: str,
        intended_use: str,
        target_asset: str,
        contains_pii: bool = False,
        geography: Optional[str] = None,
    ) -> None:
        """
        Raises PermittedUseViolation if the intended use is not allowed.
        Call this in every pipeline that promotes vendor data.
        """
        pu = self.load_vendor(vendor_id)

        # Check contract expiry
        from datetime import date
        if date.fromisoformat(pu.expiry_date) < date.today():
            raise PermittedUseViolation(
                f"Vendor {vendor_id} contract expired on {pu.expiry_date}. "
                f"Renew contract before promoting data."
            )

        # Check intended use
        if intended_use not in pu.allowed_uses:
            raise PermittedUseViolation(
                f"Use '{intended_use}' is not in permitted uses for vendor {vendor_id}. "
                f"Permitted: {pu.allowed_uses}"
            )

        if intended_use in pu.prohibited_uses:
            raise PermittedUseViolation(
                f"Use '{intended_use}' is explicitly prohibited for vendor {vendor_id}."
            )

        # Check downstream asset is registered
        if target_asset not in pu.allowed_downstream_assets:
            raise PermittedUseViolation(
                f"Asset '{target_asset}' is not in the registered downstream assets for "
                f"vendor {vendor_id}. Register in Collibra and update permitted_use.yaml "
                f"before promoting."
            )

        # Check PII restriction
        if contains_pii and pu.pii_restriction == "no_pii":
            raise PermittedUseViolation(
                f"Vendor {vendor_id} data cannot contain PII in target asset '{target_asset}'. "
                f"Apply masking before promotion."
            )

        # Check geography
        if geography and pu.geographic_restriction and geography not in pu.geographic_restriction:
            raise PermittedUseViolation(
                f"Vendor {vendor_id} data cannot be used for geography '{geography}'. "
                f"Restriction: {pu.geographic_restriction}"
            )

        logger.info(
            f"Permitted use check PASSED: vendor={vendor_id}, use={intended_use}, "
            f"target={target_asset}"
        )


class PermittedUseViolation(Exception):
    """Raised when a pipeline attempts to use vendor data outside permitted scope."""
    pass
```

### 6.6 Network and Access Controls

| Connection Type | Required Controls | Approval |
|---|---|---|
| SFTP (inbound) | Known-host fingerprint pinned; PGP encryption required for V1/V2; IP allowlist on our SFTP server | DE Lead + IT |
| REST API (outbound call) | TLS 1.2+; no self-signed certs; API key in secrets manager; rate limit enforced | DE Lead |
| Snowflake Secure Data Share | Inbound share database; no direct SELECT on share objects in production; CAB review for V1 | DE Lead + IT + CAB (V1) |
| S3 / Blob Storage (vendor pushes to our bucket) | Dedicated vendor-specific bucket; no vendor access to other buckets; server-side encryption; access logging enabled | DE Lead + IT |
| Direct database connection (vendor DB) | PrivateLink or VPN only; read-only service account; IP allowlist; CAB review required | DE Lead + IT + CAB |
| Vendor platform access (vendor accesses our Snowflake/Databricks) | Dedicated service account; MFA; read-only on specific objects only; access logged; 90-day max session; quarterly access certification | DE Lead + IT + DGO + CAB |

---

## 7. Ongoing Monitoring and Annual Review

### 7.1 Continuous Monitoring

The following automated checks run nightly via the VendorRiskMonitor (Section 4.5):

| Check | Signal | GREEN Threshold | AMBER Threshold | RED Threshold |
|---|---|---|---|---|
| DQ pass rate (7-day rolling) | % rules passing | ≥ 95% | 90–94% | < 90% |
| Freshness SLA breaches (7 days) | Count | 0 | 1–2 | ≥ 3 |
| Schema drift | Boolean | None | — | Detected |
| Row volume anomaly | Std deviations | ≤ 1.5σ | 1.5–2σ | > 2σ |
| Contract expiry | Days remaining | > 60 | 31–60 | ≤ 30 |
| Security cert expiry (SOC 2) | Days remaining | > 60 | 31–60 | ≤ 30 |
| Null rate on critical columns | % null | < 0.1% | 0.1–1% | > 1% |

**RED signal actions:**
- Alert sent to DE on-call and DGO immediately
- If schema drift or DQ failure: Silver promotion blocked automatically
- If contract expiry ≤ 30 days: DGO escalates to Legal and CDO

**AMBER signal actions:**
- Alert sent to DE team and DGO in next business day digest
- DGO creates tracking ticket; DE investigates within 2 business days

### 7.2 Periodic Review Schedule

| Review | Frequency | Owner | Participants | Output |
|---|---|---|---|---|
| V1 vendor review | Quarterly | DGO | DE Lead, Legal, CISO, Privacy | Quarterly risk scorecard per V1 vendor |
| V2 vendor review | Semi-Annual | DGO | DE Lead, Legal | Semi-annual risk scorecard |
| V3/V4 vendor review | Annual | DGO | DE Lead | Annual registry update |
| Annual security reassessment (V1/V2) | Annual | DGO + CISO | Vendor security contact | Updated risk assessment; fresh questionnaire |
| Contract renewal risk review | 90 days before expiry | Legal + DGO | CDO (V1) | Renewal terms assessment |
| Post-incident vendor review | Within 30 days of incident | DGO | CDO, Legal, CISO | Incident review report; continue/terminate decision |

### 7.3 Vendor Scorecard

Each V1 and V2 vendor receives a quarterly or semi-annual scorecard submitted to the CDO and GC.

```python
# vendor_scorecard_generator.py
from dataclasses import dataclass
from datetime import date
import snowflake.connector
import yaml


@dataclass
class VendorScorecard:
    vendor_id: str
    vendor_name: str
    tier: str
    period: str                   # e.g. "Q1-2026"
    dq_avg_pass_rate: float
    freshness_breach_count: int
    schema_drift_events: int
    data_volume_anomaly_count: int
    incident_count: int
    open_contractual_conditions: int   # unresolved "pass with conditions" items
    contract_expiry_date: str
    soc2_expiry_date: str
    overall_score: int            # 0–100
    overall_rating: str           # RED | AMBER | GREEN


class VendorScorecardGenerator:
    def __init__(self, snow_conn_params: dict):
        self.conn = snowflake.connector.connect(**snow_conn_params)
        self.cursor = self.conn.cursor()

    def generate(self, vendor_id: str, period_start: date, period_end: date) -> VendorScorecard:
        stats = self._query_period_stats(vendor_id, period_start, period_end)
        score = self._compute_score(stats)
        rating = "GREEN" if score >= 80 else "AMBER" if score >= 60 else "RED"

        return VendorScorecard(
            vendor_id=vendor_id,
            vendor_name=stats["vendor_name"],
            tier=stats["tier"],
            period=f"{period_start.strftime('%b %Y')}–{period_end.strftime('%b %Y')}",
            dq_avg_pass_rate=stats["avg_dq_pass_rate"],
            freshness_breach_count=stats["freshness_breaches"],
            schema_drift_events=stats["schema_drift_events"],
            data_volume_anomaly_count=stats["volume_anomalies"],
            incident_count=stats["incident_count"],
            open_contractual_conditions=stats["open_conditions"],
            contract_expiry_date=stats["contract_expiry"],
            soc2_expiry_date=stats["soc2_expiry"],
            overall_score=score,
            overall_rating=rating,
        )

    def _compute_score(self, stats: dict) -> int:
        score = 100
        score -= max(0, int((1 - stats["avg_dq_pass_rate"]) * 40))  # DQ: up to -40
        score -= min(20, stats["freshness_breaches"] * 4)           # Freshness: up to -20
        score -= min(15, stats["schema_drift_events"] * 5)          # Drift: up to -15
        score -= min(10, stats["incident_count"] * 5)               # Incidents: up to -10
        score -= min(10, stats["open_conditions"] * 3)              # Open conditions: up to -10
        return max(0, score)

    def _query_period_stats(self, vendor_id: str,
                            start: date, end: date) -> dict:
        sql = """
            SELECT
                v.vendor_name, v.tier,
                v.contract_expiry_date, v.soc2_expiry_date,
                AVG(h.dq_pass_rate_7d) AS avg_dq_pass_rate,
                SUM(h.freshness_sla_breaches_7d) AS freshness_breaches,
                COUNT_IF(h.schema_drift_detected) AS schema_drift_events,
                COUNT_IF(h.row_volume_anomaly) AS volume_anomalies
            FROM governance.vendor_registry.vendors v
            JOIN governance.vendor_monitoring.daily_health h
              ON v.vendor_id = h.vendor_id
            WHERE v.vendor_id = %(vendor_id)s
              AND h.check_date BETWEEN %(start)s AND %(end)s
            GROUP BY 1,2,3,4
        """
        self.cursor.execute(sql, {"vendor_id": vendor_id, "start": start, "end": end})
        row = self.cursor.fetchone()
        # incident_count and open_conditions queried separately
        return {
            "vendor_name": row[0], "tier": row[1],
            "contract_expiry": str(row[2]), "soc2_expiry": str(row[3]),
            "avg_dq_pass_rate": float(row[4] or 0),
            "freshness_breaches": int(row[5] or 0),
            "schema_drift_events": int(row[6] or 0),
            "volume_anomalies": int(row[7] or 0),
            "incident_count": 0, "open_conditions": 0,   # populated separately
        }
```

---

## 8. Incident Response — Vendor-Related Events

### 8.1 Vendor Incident Types

| Incident Type | Description | Severity Floor |
|---|---|---|
| **VINC-BREACH** | Vendor reports a breach of systems holding our data or data subjects' data | P1 |
| **VINC-PII-EXPOSURE** | Vendor delivers data containing unexpected PII beyond contracted scope | P1 |
| **VINC-DQ-CRITICAL** | Vendor data fails CRITICAL DQ rules; Silver promotion blocked | P2 |
| **VINC-DELIVERY-OUTAGE** | Vendor fails to deliver data within SLA window | P2 (T1 ML dependency) / P3 (other) |
| **VINC-SCHEMA-BREAK** | Vendor delivers schema change without required notice | P2 |
| **VINC-PERMITTED-USE** | Our systems detect use of vendor data outside permitted scope | P2 |
| **VINC-CONTRACT-EXPIRE** | Contract expires without renewal; data flow continues | P3 |
| **VINC-SUBPROCESSOR** | Vendor engages new subprocessor without notification | P3 |

### 8.2 Response Procedures by Incident Type

#### VINC-BREACH

```
IMMEDIATE (0–2 hours):
  1. Incident commander: CDO
  2. Notify: Privacy Officer, CISO, Legal (parallel — all within 1 hour)
  3. Determine: Which of our data was held by vendor? What was exposed?
  4. Preserve: All vendor notification communications as evidence
  5. Isolate: Suspend new data ingestion from vendor

CONTAIN (2–8 hours):
  6. Assess: Which internal assets use vendor data? Are they downstream-serving?
  7. Assess: Are data subjects affected? What is the regulatory exposure?
  8. Decision: Take downstream assets offline if exposure is uncontrolled

REGULATORY CLOCK:
  - GDPR: 72-hour supervisory authority notification window begins at our
    awareness — NOT at vendor's notification to us
  - CCPA: 45-day notification window for affected CA residents
  Legal owns regulatory notification decision (A). CDO signs off.

POST-INCIDENT:
  - Formal vendor review within 30 days
  - Continue/suspend/terminate vendor decision documented
  - Contract remediation if notification was late
```

#### VINC-PII-EXPOSURE

```
IMMEDIATE (0–1 hour):
  1. Block Silver promotion for affected feed immediately (DE on-call)
  2. Notify: DGO, Privacy Officer (within 1 hour)
  3. Identify: What PII columns arrived? Were they loaded to Bronze only or promoted?
  4. If promoted beyond Bronze: treat as VINC-BREACH

CONTAIN (1–4 hours):
  5. If Bronze only: quarantine table; revoke access to Bronze schema
  6. Notify vendor: document what was received and demand explanation
  7. DGO opens formal incident

RESOLUTION:
  8. Vendor must provide root cause and corrective action plan within 48 hours
  9. DQ rule added to detect unexpected PII columns on future deliveries
  10. Permitted use configuration updated
  11. Resume ingestion only after DGO sign-off
```

#### VINC-DQ-CRITICAL

```
IMMEDIATE (automated — pipeline block):
  1. Silver promotion blocked automatically by DQ gate
  2. Alert sent to DE on-call and DGO
  3. DE investigates within 2 hours (T1 ML dependency) / 4 hours (other)

CONTAIN:
  4. Notify downstream consumers of delayed/unavailable data
  5. Contact vendor within SLA window (per contract: 24hr for V1)
  6. Determine: is this a one-time delivery issue or schema/data change?

RESOLUTION:
  7. Vendor delivers corrected file or confirms root cause
  8. DQ re-run; if passes: promote with incident flag on affected rows
  9. If DQ fails 3 times in 30 days: escalate to DGO for vendor review
```

### 8.3 Vendor Incident Escalation Matrix

| Vendor Tier | P1 | P2 | P3 |
|---|---|---|---|
| **V1** | CDO + Privacy Officer + CISO + Legal immediately | CDO notified within 2 hours; DGO owns | DGO owns; CDO in weekly report |
| **V2** | CDO notified within 2 hours; DGO + Privacy + Legal | DGO owns; CDO notified within 4 hours | DGO owns |
| **V3/V4** | CDO notified within 4 hours | DGO + DE Lead | DE Lead |

---

## 9. Offboarding and Termination

### 9.1 Planned Offboarding Process

```
Offboarding trigger: Contract non-renewal, vendor replacement, business need cessation.
          │
          ▼
STAGE 1 — IMPACT ASSESSMENT (DGO — 5–10 days before termination date)
  □ Identify all internal assets that use vendor data
  □ Identify all downstream consumers of those assets
  □ Identify any T1 ML models with feature dependency on vendor data
  □ Determine replacement data source (if required)
  □ Document data assets that must be retired vs. migrated

STAGE 2 — CONSUMER NOTIFICATION (DGO + Domain leads — minimum notice)
  V1 vendor: 30 days minimum notice to all downstream consumers
  V2 vendor: 14 days minimum notice
  V3/V4 vendor: 7 days minimum notice

STAGE 3 — PIPELINE DECOMMISSION (DE — on or before termination date)
  □ Disable ingestion pipeline
  □ Update Collibra asset status to DEPRECATED
  □ Remove vendor schema from active queries
  □ Archive Bronze data per retention policy
  □ Update all downstream data contracts to remove vendor as source

STAGE 4 — DATA DISPOSAL (DE + DGO — within 30 days of termination)
  □ Execute data deletion per contract requirements
  □ Document deletion: which tables, which environments, deletion date
  □ Issue deletion certificate to vendor (if required by contract)
  □ Confirm deletion in all environments: dev, staging, prod, backups

STAGE 5 — ACCESS REVOCATION (IT — on termination date)
  □ Revoke all vendor access to our systems (service accounts, VPN, SFTP)
  □ Revoke our service account access to vendor systems
  □ Rotate any credentials shared with the vendor
  □ Close network connectivity (PrivateLink, VPN tunnels, IP allowlists)

STAGE 6 — REGISTRY UPDATE (DGO — within 5 days of completion)
  □ Update vendor registry status to TERMINATED
  □ File offboarding evidence package in audit repository
  □ Close any open contractual conditions as RESOLVED or WAIVED
```

### 9.2 Emergency Termination

Emergency termination (vendor breach, regulatory action, material security concern) follows an accelerated path:

```
Hour 0:   CDO + DGO decision to terminate
Hour 1:   IT revokes all vendor access to our systems immediately
Hour 2:   DE disables all ingestion pipelines
Hour 4:   Downstream consumers notified; affected assets flagged
Day 1:    Legal sends formal termination notice
Day 5:    Impact assessment and replacement planning complete
Day 30:   Data disposal certification issued
```

**Emergency termination authority:** CDO may authorize emergency termination unilaterally. For V1 vendors, Legal must be notified within 1 hour of the decision.

### 9.3 Data Retention After Termination

| Scenario | Retention Permitted | Duration | Controls |
|---|---|---|---|
| Data required for regulatory compliance (SOX, HIPAA records) | Yes | Per regulation | Isolated schema; access restricted to compliance team |
| Data required for active legal hold | Yes | Duration of hold + 90 days | Isolated schema; Legal notification required |
| Data backing a certified ML model still in production | Yes, until model is decommissioned | Per T1 model retention policy | Access restricted to ML team; DGO tracks |
| No active regulatory or legal requirement | No | Delete within 30 days of termination | Deletion certificate required |

---

## 10. Audit and Compliance

### 10.1 First Line of Defense — Monthly Self-Assessment

DE executes and attests to the following controls monthly:

| Control | Check | Pass Criterion |
|---|---|---|
| VND-01 | All active vendors are in the Vendor Registry with current status | 100% coverage |
| VND-02 | All V1/V2 vendors have a current (non-expired) executed contract | 100% non-expired |
| VND-03 | All V1/V2 vendors have a current SOC 2 or documented exception | 100% current |
| VND-04 | All vendor Bronze schemas have classification tags applied | 100% coverage |
| VND-05 | Permitted use configuration files exist for all active vendors | 100% coverage |
| VND-06 | No vendor data has been promoted to assets outside the registered downstream asset list | Zero violations |
| VND-07 | All vendor service accounts have been reviewed in the last 90 days | 100% reviewed |
| VND-08 | Vendor monitoring health dashboard shows no unresolved RED signals older than 5 business days | Zero unresolved RED |

### 10.2 Second Line of Defense — Quarterly Independent Audit

DGO executes independently of DE team attestations:

```sql
-- VND-AU-01: Vendors in pipelines but not in registry
SELECT DISTINCT _vendor_id
FROM vendor_bronze._all_vendor_tables
WHERE _vendor_id NOT IN (
    SELECT vendor_id FROM governance.vendor_registry.vendors
    WHERE status = 'ACTIVE'
);
-- Expected: zero rows

-- VND-AU-02: Vendor data in Silver/Gold without permitted use stamp
SELECT table_catalog, table_schema, table_name, COUNT(*) AS row_count
FROM information_schema.columns
WHERE column_name = '_permitted_use_version'
  AND table_schema NOT LIKE 'vendor_bronze%'
  AND table_catalog != 'vendor_bronze'
  AND column_default IS NULL
  AND is_nullable = 'YES';
-- Expected: zero rows where permitted_use_version is nullable outside Bronze

-- VND-AU-03: Expired contracts still with active pipelines
SELECT v.vendor_name, v.tier, v.contract_expiry_date, p.pipeline_name, p.last_run
FROM governance.vendor_registry.vendors v
JOIN governance.pipelines.pipeline_registry p ON v.vendor_id = p.vendor_id
WHERE v.contract_expiry_date < CURRENT_DATE()
  AND p.status = 'ACTIVE';
-- Expected: zero rows

-- VND-AU-04: V1 vendors without current SOC 2
SELECT vendor_name, tier, soc2_expiry_date
FROM governance.vendor_registry.vendors
WHERE tier = 'V1'
  AND (soc2_expiry_date IS NULL OR soc2_expiry_date < CURRENT_DATE());
-- Expected: zero rows (or documented exceptions)

-- VND-AU-05: Vendor access not recertified in 90 days
SELECT v.vendor_name, sa.service_account_name, sa.last_certified_date
FROM governance.vendor_registry.vendors v
JOIN governance.access.vendor_service_accounts sa ON v.vendor_id = sa.vendor_id
WHERE sa.last_certified_date < DATEADD('day', -90, CURRENT_DATE())
  AND sa.status = 'ACTIVE';
-- Expected: zero rows

-- VND-AU-06: PII in Bronze vendor tables with no masking policy at Silver
SELECT b.vendor_id, b.column_name, b.pii_tag
FROM governance.vendor_registry.vendor_pii_columns b
LEFT JOIN information_schema.policy_references pr
    ON b.column_name = pr.ref_column_name
    AND pr.policy_kind = 'MASKING_POLICY'
WHERE b.is_active = TRUE
  AND pr.ref_column_name IS NULL;
-- Expected: zero rows
```

### 10.3 Evidence Requirements

All vendor risk documentation is retained in a dedicated, access-controlled audit repository:

```
vendor-governance-evidence/
├── {vendor_id}/
│   ├── onboarding/
│   │   ├── intake_request.yaml
│   │   ├── risk_assessment_report.pdf
│   │   ├── security_questionnaire_responses.pdf
│   │   ├── soc2_report.pdf
│   ├── contracts/
│   │   ├── executed_mdsa_{date}.pdf
│   │   ├── executed_dua_{date}.pdf
│   │   ├── executed_dpa_{date}.pdf          # if applicable
│   │   └── executed_baa_{date}.pdf          # if applicable
│   ├── periodic_reviews/
│   │   ├── {YYYY}/
│   │   │   ├── {QN}_scorecard.pdf
│   │   │   └── annual_reassessment_{YYYY}.pdf
│   ├── incidents/
│   │   └── VINC-{ID}_{date}_summary.pdf
│   └── offboarding/
│       ├── impact_assessment.pdf
│       ├── consumer_notifications.pdf
│       └── data_deletion_certificate.pdf
```

**Retention requirements by document type:**

| Document | Retention Period |
|---|---|
| Executed contracts | 7 years from expiry |
| Risk assessments | 5 years |
| Deletion certificates | 7 years (GDPR / HIPAA) |
| Breach notifications | 7 years |
| Incident reports | 5 years |
| Audit evidence | 5 years |
| Access certification records | 3 years |


---

## 11. RACI

| Activity | CDO | DGO | DE-L | DE | Legal | CISO / InfoSec | Privacy Officer | DO | IT |
|---|---|---|---|---|---|---|---|---|---|
| **Intake and Classification** | | | | | | | | | |
| Vendor intake request submission | — | — | — | — | — | — | — | **A** | — |
| Vendor tier assignment | — | **A** | C | — | C | C | C | C | — |
| Initial data classification | — | **A** | C | R | — | — | C | C | — |
| Approval to proceed to risk assessment | C | **A** | C | — | — | C | C | C | — |
| **Risk Assessment** | | | | | | | | | |
| Security questionnaire issuance | — | **A** | — | — | — | C | — | — | — |
| SOC 2 review | — | C | — | — | — | **A** | — | — | — |
| Privacy program assessment | — | C | — | — | — | — | **A** | — | — |
| Sub-processor disclosure review | — | **A** | — | — | C | C | C | — | — |
| Risk assessment report sign-off (V1) | **A** | R | — | — | C | C | C | — | — |
| Risk assessment report sign-off (V2) | — | **A** | — | — | C | C | — | — | — |
| Pass / Fail decision | C | **A** | — | — | C | C | C | — | — |
| **Contract Execution** | | | | | | | | | |
| Contract negotiation | — | C | — | — | **A** | — | — | C | — |
| Data-specific clause review | — | **A** | — | — | R | — | C | — | — |
| DPA / GDPR clause review | — | C | — | — | C | — | **A** | — | — |
| BAA review | — | C | — | — | C | — | **A** | — | — |
| V1 contract final sign-off | **A** | R | — | — | R | C | C | R | — |
| V2/V3 contract final sign-off | — | C | — | — | **A** | — | — | C | — |
| Contract filed in repository | — | C | — | — | **A** | — | — | — | — |
| **Technical Setup** | | | | | | | | | |
| Bronze schema and pipeline build | — | C | **A** | R | — | — | — | — | C |
| Audit column standards implementation | — | C | **A** | R | — | — | — | — | — |
| DQ rules configuration | — | **A** | C | R | — | — | — | C | — |
| Permitted use configuration file | — | **A** | C | R | — | — | — | C | — |
| Network connection approval (V1/V2) | — | C | C | R | — | C | — | — | **A** |
| Service account creation | — | C | **A** | R | — | C | — | — | R |
| Go-live gate sign-off | — | **A** | R | R | — | — | — | C | — |
| **Ongoing Monitoring** | | | | | | | | | |
| Nightly automated health checks | — | I | **A** | R | — | — | — | — | — |
| RED signal response | — | C | **A** | R | — | — | — | I | — |
| Vendor registry maintenance | — | **A** | C | R | — | — | — | — | — |
| Quarterly V1 vendor review | C | **A** | R | — | C | C | C | C | — |
| Semi-annual V2 vendor review | — | **A** | R | — | C | — | — | C | — |
| Annual security reassessment | — | **A** | — | — | — | **A** | — | — | — |
| Contract renewal risk review | — | C | — | — | **A** | — | — | C | — |
| **Incident Response** | | | | | | | | | |
| VINC-BREACH — incident command | **A** | R | C | — | R | R | R | — | — |
| VINC-PII-EXPOSURE — first response | — | **A** | R | R | C | C | R | — | — |
| VINC-DQ-CRITICAL — first response | — | C | **A** | R | — | — | — | I | — |
| Regulatory notification decision | **A** | C | — | — | R | — | R | — | — |
| Vendor continue/terminate decision | **A** | R | C | — | C | C | C | R | — |
| **Offboarding** | | | | | | | | | |
| Impact assessment | — | **A** | R | R | — | — | — | C | — |
| Consumer notification | — | **A** | R | R | — | — | — | C | — |
| Pipeline decommission | — | C | **A** | R | — | — | — | — | — |
| Data deletion execution | — | **A** | C | R | — | — | — | — | C |
| Deletion certificate issuance | — | **A** | C | R | — | — | — | — | — |
| Access revocation | — | C | C | R | — | C | — | — | **A** |
| Registry status update | — | **A** | — | R | — | — | — | — | — |

---

## 12. Vendor Registry

### 12.1 Registry Schema

All active, pending, and terminated vendors are maintained in the Vendor Registry — both as a YAML source of truth (configuration-as-code) and as a Snowflake table for querying and monitoring.

```sql
-- governance.vendor_registry.vendors
CREATE OR REPLACE TABLE governance.vendor_registry.vendors (
    vendor_id               VARCHAR NOT NULL,       -- unique slug, e.g. 'acme_data'
    vendor_name             VARCHAR NOT NULL,
    tier                    VARCHAR NOT NULL,       -- V1 | V2 | V3 | V4
    status                  VARCHAR NOT NULL,       -- ACTIVE | PENDING | SUSPENDED | TERMINATED
    data_type               VARCHAR NOT NULL,       -- what kind of data they deliver
    classification          VARCHAR NOT NULL,       -- highest classification of delivered data
    contains_pii            BOOLEAN NOT NULL,
    contains_phi            BOOLEAN NOT NULL,
    contains_pci            BOOLEAN NOT NULL,

    -- Contract
    contract_id             VARCHAR,
    contract_type           VARCHAR,               -- MDSA | DPA | BAA | DUA | etc.
    contract_start_date     DATE,
    contract_expiry_date    DATE,
    auto_renews             BOOLEAN,
    renewal_notice_days     INTEGER,               -- days of notice required to terminate/not-renew

    -- Security certifications
    soc2_type2_available    BOOLEAN,
    soc2_expiry_date        DATE,
    iso27001_certified      BOOLEAN,
    last_pentest_date       DATE,
    pentest_findings_clean  BOOLEAN,

    -- Risk
    inherent_risk           VARCHAR,               -- CRITICAL | HIGH | MEDIUM | LOW
    residual_risk           VARCHAR,
    last_risk_assessment    DATE,
    next_risk_assessment    DATE,

    -- Delivery
    delivery_method         VARCHAR,               -- SFTP | API | SNOWFLAKE_SHARE | S3 | DB
    bronze_schema           VARCHAR,               -- e.g. 'vendor_bronze.acme_data'
    feed_names              ARRAY,                 -- list of feed names

    -- Ownership
    business_requestor      VARCHAR,               -- name of DO who requested
    dgo_owner               VARCHAR,               -- DGO analyst who owns this relationship
    de_owner                VARCHAR,               -- DE team member who owns pipeline
    legal_owner             VARCHAR,               -- attorney who owns contract

    -- Metadata
    onboarded_date          DATE,
    terminated_date         DATE,
    termination_reason      VARCHAR,
    collibra_asset_id       VARCHAR,               -- link to Collibra asset

    CONSTRAINT pk_vendors PRIMARY KEY (vendor_id)
);
```

### 12.2 Vendor YAML Configuration Source of Truth

```yaml
# config/vendors/acme_data/vendor.yaml
vendor_id: "acme_data"
vendor_name: "Acme Data Inc."
tier: "V1"
status: "ACTIVE"
data_type: "Consumer credit attributes"
classification: "RESTRICTED"
contains_pii: true
contains_phi: false
contains_pci: false

contract:
  contract_id: "ACME-2025-001"
  contract_type: "MDSA+DUA"
  start_date: "2025-01-15"
  expiry_date: "2026-12-31"
  auto_renews: false
  renewal_notice_days: 90

security:
  soc2_type2_available: true
  soc2_expiry_date: "2026-06-30"
  last_pentest_date: "2025-08-01"
  pentest_findings_clean: true

risk:
  inherent_risk: "CRITICAL"
  residual_risk: "HIGH"
  last_risk_assessment: "2025-01-10"
  next_risk_assessment: "2026-01-10"

delivery:
  method: "SFTP"
  bronze_schema: "vendor_bronze.acme_data"
  freshness_sla_hours: 24
  feeds:
    - name: "consumer_credit_v2"
      table: "vendor_bronze.acme_data.raw_consumer_credit_v2"
      critical_columns: ["consumer_id", "score_date", "score_value"]

ownership:
  business_requestor: "Jane Smith (ML Engineering)"
  domain_owner: "john.doe@company.com"
  dgo_owner: "dgo.analyst@company.com"
  de_owner: "de.engineer@company.com"
  legal_owner: "attorney@company.com"

downstream_assets:
  - "ml_features.credit.dim_credit_attributes"
  - "gold_risk.curated.fact_credit_risk"

collibra_asset_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

---

## 13. Configuration Reference

### 13.1 Vendor Monitoring GitHub Actions Workflow

```yaml
# .github/workflows/vendor_monitoring.yml
name: Vendor Risk Monitor — Nightly

on:
  schedule:
    - cron: "0 6 * * *"    # 6 AM UTC daily
  workflow_dispatch:

jobs:
  vendor-health-check:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements/vendor_monitoring.txt

      - name: Run vendor health checks
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.VENDOR_MONITOR_SERVICE_ACCOUNT }}
          SNOWFLAKE_PRIVATE_KEY: ${{ secrets.VENDOR_MONITOR_PRIVATE_KEY }}
          SLACK_WEBHOOK_ALERTS: ${{ secrets.SLACK_WEBHOOK_DATA_ALERTS }}
          DGO_EMAIL: ${{ secrets.DGO_ALERT_EMAIL }}
        run: |
          python -m vendor_governance.monitor \
            --config config/vendor_monitoring.yaml \
            --env prod

      - name: Upload health report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: vendor-health-report-${{ github.run_id }}
          path: reports/vendor_health_*.json
          retention-days: 90

      - name: Notify on RED signals
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: ${{ secrets.SLACK_CHANNEL_DATA_GOVERNANCE }}
          slack-message: |
            🚨 *Vendor Health Check: RED signals detected*
            Review the health report: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

### 13.2 Vendor Onboarding Collibra Workflow Trigger

```python
# collibra_vendor_workflow.py
import requests
from dataclasses import dataclass


@dataclass
class VendorOnboardingWorkflow:
    """Triggers the vendor onboarding Collibra workflow from the intake form."""

    collibra_base_url: str
    session: requests.Session
    workflow_definition_id: str     # configured in Collibra admin

    def trigger(self, intake: dict) -> str:
        """Submits a new vendor intake and returns the workflow instance ID."""
        payload = {
            "workflowDefinitionId": self.workflow_definition_id,
            "businessItemType": "Asset",
            "variables": [
                {"name": "vendorName", "type": "string",
                 "value": intake["vendor"]["name"]},
                {"name": "requestorEmail", "type": "string",
                 "value": intake["requestor"]["name"]},
                {"name": "classificationProposed", "type": "string",
                 "value": intake["data_description"]["classification_proposed"]},
                {"name": "containsPii", "type": "boolean",
                 "value": intake["data_description"]["contains_pii"]},
                {"name": "tier", "type": "string",
                 "value": "PENDING"},   # DGO assigns final tier in workflow
            ]
        }
        resp = self.session.post(
            f"{self.collibra_base_url}/rest/2.0/workflowInstances",
            json=payload
        )
        resp.raise_for_status()
        workflow_id = resp.json()["id"]
        return workflow_id
```

### 13.3 KPI Targets — Vendor Program

| KPI | Target | RED Threshold | Reporting Cadence |
|---|---|---|---|
| % V1/V2 vendors with current contract | 100% | < 100% | Monthly |
| % V1/V2 vendors with current SOC 2 | 100% | < 100% | Monthly |
| Vendor DQ average pass rate (all active feeds) | ≥ 95% | < 90% | Monthly |
| % vendor feeds with zero unresolved RED signals | 100% | < 95% | Weekly |
| % vendor service accounts recertified within 90 days | 100% | < 100% | Monthly |
| Time to complete V1 onboarding (intake to go-live) | ≤ 45 days | > 60 days | Quarterly |
| Breach notification receipt compliance (V1 vendors) | 100% within 48hr | Any late | Per incident |
| % offboarded vendors with deletion certificate | 100% | < 100% | Per offboarding |

---

## 14. Appendix

### Appendix A — Vendor Intake Request Template

Submit via Collibra governance workflow or use this YAML template:

```yaml
# Submit to DGO via Collibra "New Vendor Data Request" workflow
vendor:
  name: ""
  website: ""
  primary_contact: ""
  parent_company: ""

data_description:
  data_type: ""
  classification_proposed: ""         # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED
  contains_pii: false
  contains_phi: false
  contains_pci: false
  delivery_method: ""                 # SFTP | API | SNOWFLAKE_SHARE | S3 | Other
  delivery_frequency: ""              # Daily | Weekly | Monthly | Real-time | Ad-hoc
  estimated_volume_rows: 0
  geographic_scope: ""               # US | EU | Global | Other
  data_subjects: ""                  # Consumers | Employees | Business entities | None

intended_use:
  business_use_case: ""
  downstream_assets: []              # list planned table/model names
  used_in_t1_model: false
  used_in_regulatory_reporting: false
  used_in_external_facing_product: false

requestor:
  name: ""
  team: ""
  domain_owner_approval: false
  domain_owner_name: ""
```

### Appendix B — Security Questionnaire Outline (V1/V2)

The full questionnaire is maintained in the vendor governance evidence repository. Key sections:

| Section | Key Questions |
|---|---|
| **Organizational Security** | CISO or equivalent; security policy; employee security training; background checks |
| **Access Control** | MFA enforcement; least privilege; privileged access management; access review cycle |
| **Data Handling** | Encryption at rest and in transit; data classification; data minimization practices |
| **Sub-processors** | Full sub-processor list; jurisdictions; sub-processor audit requirements |
| **Incident Response** | IRP existence; notification procedures; recent incident history; tabletop exercise cadence |
| **Business Continuity** | BCP/DR existence; RTO/RPO; last test date |
| **Compliance and Certifications** | SOC 2 Type II; ISO 27001; PCI DSS; HIPAA; applicable regulatory certifications |
| **Privacy** | Privacy program; DPO appointment; DSAR process; cross-border transfer mechanisms |
| **Vulnerability Management** | Pentest cadence; CVE patching SLAs; vulnerability disclosure program |

### Appendix C — Related Documents

| Document | Location | Relationship |
|---|---|---|
| Cross-Domain RACI | `CROSS_DOMAIN_RACI.md` | Access provisioning and external access RACI |
| Data Governance Standards | `Data_Governance_Standards/03_data_governance_standards.md` | Classification tiers; data sharing standards |
| Data Incident Response Playbook | `DATA_INCIDENT_RESPONSE_PLAYBOOK.md` | INC-PII and INC-SEC response procedures (apply to vendor incidents) |
| Data Product Certification Framework | `DATA_PRODUCT_CERTIFICATION_FRAMEWORK.md` | Bronze/Silver/Gold gate requirements (vendor data must pass these) |
| DE Config and Change Management | `Data_Engineering_Standards/05_DE_Config_Change_Management.md` | Change tiers for new source onboarding and network connections |
| 2nd Line of Defense Strategy | `Data_Governance_Standards/04_2nd_line_of_defense_strategy.md` | 2LOD audit structure referenced in Section 10 |
| Master Library README | `README.md` | Program overview; gap register |

### Appendix D — Regulatory Quick Reference

| Regulation | Key Vendor Obligation | Our Obligation | Reference |
|---|---|---|---|
| GDPR | Processor agreement (Art. 28); breach notification to us within 72hr; sub-processor consent | DPA in place; 72hr supervisory authority notification | Art. 28, 33, 82 |
| CCPA / CPRA | Service provider agreement; no selling/sharing of CA consumer data | Contract prohibits sale/sharing; honor opt-outs | Cal. Civ. Code §1798.100 |
| HIPAA | BAA in place; equivalent safeguards; breach notification within 60 days | BAA executed; PHI handling standards | 45 CFR §164 |
| PCI DSS | In-scope vendors must be PCI compliant; access to CHD restricted | Vendor access controls; annual compliance confirmation | PCI DSS Req. 12.8 |
| SOX | Data integrity for financial reporting data; audit trail | Third-party controls documented; tested annually | SOX §302, §404 |

---

*Document Owner: Chief Data Officer + Data Governance Office*
*Reviewed: Annually and upon material vendor change or regulatory update*
*Questions or amendments: Raise a Collibra "Vendor Governance" workflow task to the DGO Program Manager*
