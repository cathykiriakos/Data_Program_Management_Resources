# AI-First Strategy Addendum
## Building an Agentic AI Program on a Governed Data Foundation

> **Document Type:** Addendum to CDO 2-Year Roadmap
> **Role:** Chief AI Officer / Chief Data Officer
> **Platform Stack:** Snowflake · Databricks · Collibra · GitHub Actions · Azure DevOps · Databricks Asset Bundles · dbt Cloud
> **Version:** 1.0 | **Last Updated:** 2026-03
> **Classification:** Internal — Executive Strategy
> **Primary Standard:** AIUC-1 (AI Agent Security, Safety & Reliability Standard)
> **Supporting Frameworks:** NIST AI RMF 1.0 · ISO/IEC 42001 · EU AI Act · MITRE ATLAS · SR 11-7 · BCBS 239 · HIPAA · SOX · GDPR · CCPA

---

## Executive Summary

This addendum extends the organization's Data Governance 2-Year Roadmap into a fully operational **AI-First Strategy**. It maps the existing data program library — spanning Data Engineering, Data Governance, Business Intelligence, and Machine Learning — onto the **Agentic AI Readiness Map** (12 Capabilities × 5 Stages), and anchors every control, audit checkpoint, and CI/CD gate to the **AIUC-1 standard**: the world's first certifiable security, safety, and reliability framework for AI agents.

The central thesis is that **a governed data platform is not merely a prerequisite for AI — it is the governance control plane for AI**. The same standards, audit structures, RBAC models, CI/CD pipelines, and KPI frameworks established for data must be extended — not replaced — to govern agentic systems.

> *"AIUC-1 translates high-level governance and regulatory expectations into concrete, testable controls across security, privacy, safety, reliability, accountability, and societal impact — making it particularly well-suited for organizations deploying autonomous or customer-facing AI agents."*
> — CompliancePoint, AIUC-1 Overview (2026)

### Strategic Commitments

1. No agentic workload enters production without a corresponding entry in the AI Model Registry (Collibra-anchored), mapping all six AIUC-1 domains
2. All agentic CI/CD pipelines inherit the data governance-as-code philosophy: config-driven, YAML-injected, and gated at every promotion stage
3. AIUC-1 certification readiness is a Year 2 program milestone, treated as the organization's "SOC 2 for AI agents"
4. The Three Lines of Defense (3LOD) audit structure is extended to cover agent behavior, not just data quality
5. Every regulated industry obligation (SOX, SR 11-7, HIPAA, BCBS 239, GDPR, CCPA) is explicitly mapped to an AIUC-1 control before any agent is promoted to production

---

## Part 1: Framework Architecture

### 1.1 How the Frameworks Interlock

```
┌───────────────────────────────────────────────────────────────────┐
│                      REGULATORY LANDSCAPE                         │
│  SOX · SR 11-7 · BCBS 239 · HIPAA · GDPR · CCPA · EU AI Act     │
└─────────────────────────────┬─────────────────────────────────────┘
                              │ Compliance obligations
┌─────────────────────────────▼─────────────────────────────────────┐
│                     STRATEGIC FRAMEWORKS                          │
│    NIST AI RMF (GOVERN · MAP · MEASURE · MANAGE)                  │
│    ISO/IEC 42001 · MITRE ATLAS threat taxonomy                    │
└─────────────────────────────┬─────────────────────────────────────┘
                              │ Principles → Controls
┌─────────────────────────────▼─────────────────────────────────────┐
│                  AIUC-1 STANDARD (Certifiable)                    │
│  A. Data & Privacy  B. Security  C. Safety  D. Reliability        │
│  E. Accountability  F. Society                                    │
│  50+ testable controls · Quarterly adversarial testing · Annual   │
└─────────────────────────────┬─────────────────────────────────────┘
                              │ Implementation
┌─────────────────────────────▼─────────────────────────────────────┐
│              DATA PROGRAM LIBRARY (Existing Foundation)           │
│  Data Engineering · Data Governance (Collibra) · BI · ML         │
│  Snowflake RBAC · Databricks Unity Catalog · Collibra Lineage     │
└─────────────────────────────┬─────────────────────────────────────┘
                              │ Governance-as-code
┌─────────────────────────────▼─────────────────────────────────────┐
│                   CI/CD & AGENTIC RUNTIME                         │
│  GitHub Actions · Azure DevOps · Databricks Asset Bundles         │
│  dbt Cloud · Collibra API · MLflow · Snowflake Cortex             │
└───────────────────────────────────────────────────────────────────┘
```

### 1.2 AIUC-1 Six-Domain Summary

| Domain | Code | Focus | Key Requirements |
|--------|------|--------|------------------|
| **Data & Privacy** | A | PII protection, data policies, agent data access scope | A001–A007: Input/output policies, PII leakage prevention, IP protection |
| **Security** | B | Adversarial robustness, prompt injection, access control | B001–B009: Red-teaming, jailbreak detection, RBAC, endpoint protection |
| **Safety** | C | Harmful output prevention, human-in-the-loop, kill switches | Output moderation, fail-safes, escalation triggers |
| **Reliability** | D | Consistent behavior, error handling, drift detection | Performance gates, fallback logic, monitoring |
| **Accountability** | E | Incident response, change governance, vendor due diligence | E001–E017: Failure plans, audit logs, regulatory compliance docs |
| **Society** | F | Bias, fairness, societal impact, disclosure | Bias auditing, equitable outcomes, transparency |

### 1.3 Agentic AI Readiness Map — Stage-to-Data-Program Mapping

| Stage | Primary Data Program Dependency | AIUC-1 Domains in Scope | Minimum Governance Gate |
|-------|--------------------------------|--------------------------|--------------------------|
| **Stage 1 — Foundation** | DE Program Establishment, DG Standards | E (Accountability) | AI Asset Registry initialized in Collibra |
| **Stage 2 — Chatbots** | BI Certified Datasets, DG Data Classification | A, B, E | PII masking verified; RBAC enforced; input/output policies documented |
| **Stage 3 — Workflows** | ML Program, DE Pipelines, Semantic Layer | A, B, C, D, E | Human-in-the-loop gates; agent action boundary YAML; CI/CD gates active |
| **Stage 4 — Autonomous** | Full ML Governance, 2LOD Audit, DQ SLAs | A, B, C, D, E, F | Quarterly adversarial testing; AIUC-1 pre-certification audit; SR 11-7 model card |
| **Stage 5 — Multi-Agent** | Federated Governance Model, Cross-Domain RACI | All domains (full) | AIUC-1 certification achieved; annual renewal; multi-agent boundary contracts |

---

## Part 2: Data Foundation as AI Governance Control Plane

Before any stage advancement, the data program library must supply the following verified capabilities. These are hard gates.

### 2.1 Data Foundation Readiness Checklist (Pre-AI)

**Data Engineering (ref: DE Program Library v1.0)**

```yaml
# ai_readiness_gate_DE.yaml
data_engineering_gates:
  medallion_architecture:
    bronze_layer_complete: true
    silver_layer_complete: true
    gold_layer_complete: true          # Required before any agent consumes data
  pipeline_governance:
    lineage_documented: true           # Collibra lineage for all Tier 1 assets
    iac_drift_incidents_monthly: 0     # Zero IaC drift — AIUC-1 E004
    sla_breach_rate: "<1%"
  data_quality:
    dq_gates_in_cicd: true             # Agents cannot consume ungated data
    gold_metadata_completeness: "100%"
    dq_pass_rate_critical: ">=99.5%"
```

**Data Governance (ref: DG Standards v2.0 / Collibra)**

```yaml
data_governance_gates:
  catalog:
    asset_ownership_coverage: ">=95%"   # AIUC-1 E004 — accountability
    pii_columns_classified: "100%"      # AIUC-1 A006 — PII leakage prevention
    rbac_certified_quarterly: true      # AIUC-1 B007 — access privileges
  classification:
    restricted_data_tagged: true
    confidential_data_tagged: true
    public_data_tagged: true
  lineage:
    tier1_lineage_complete: true        # AIUC-1 E015 — activity logging requires lineage
    end_to_end_lineage_for_ai_features: true
```

**Machine Learning (ref: ML Standards v1.0)**

```yaml
ml_governance_gates:
  registry:
    model_registry_active: true         # All models registered before production
    model_cards_published: true         # AIUC-1 E017 — system transparency
    model_tier_framework_defined: true  # T1–T4 risk tiers
  monitoring:
    drift_detection_active: true        # AIUC-1 D-series — reliability
    performance_gates_defined: true
    champion_challenger_documented: true
```

### 2.2 Collibra as the AI Governance Control Plane

Collibra extends its role as the data governance control plane to become the single system of record for all AI governance artifacts:

```
COLLIBRA AI GOVERNANCE EXTENSIONS
─────────────────────────────────
Data Asset Catalog
  └── AI Model Registry (extended: agent entries)
       ├── Agent ID, version, owner, tier (T1–T4)
       ├── AIUC-1 domain compliance status (A–F)
       ├── Regulatory obligation mapping (SOX / HIPAA / GDPR / SR 11-7)
       ├── Data lineage: training data → feature store → model → agent output
       ├── Last adversarial test date and result (AIUC-1 B001)
       └── Certification status (pre-cert / certified / expired)

Business Glossary
  └── AI Terms Glossary (new)
       ├── Hallucination, prompt injection, jailbreak, agent boundary
       ├── Human-in-the-loop, human-on-the-loop, kill switch
       └── Agentic risk tier definitions

Policy Center
  └── AI Acceptable Use Policy (AIUC-1 E010)
  └── Agent Input Data Policy (AIUC-1 A001)
  └── Agent Output Data Policy (AIUC-1 A002)
  └── Vendor Due Diligence Policy (AIUC-1 E006)
```

---

## Part 3: Stage-by-Stage Agentic AI Strategy

---

### Stage 1 — Foundation

> *"Isolated AI experiments, ad-hoc scripts and pilots, fragmented data and tooling, no shared SLOs or governance for models or agents."*

**Objective:** Establish the AI governance skeleton before the first agent is deployed. Governance cannot be retrofitted — it must be designed in.

#### 3.1.1 Stage 1 Actions

**1. Initialize the AI Asset Registry in Collibra** — every experiment, script, and pilot is registered. This operationalizes AIUC-1 E015 (log model activity) from day one.

**2. Author the AI Acceptable Use Policy** (AIUC-1 E010) — covers what data agents may access, who may deploy them, and what automated actions are prohibited without human approval.

**3. Define Agent Risk Tiers** — extend the existing ML model tier framework (T1–T4) to agentic systems:

```yaml
# agent_risk_tiers.yaml
agent_risk_tiers:
  T1_critical:
    description: "Customer-facing agent; handles financial transactions or PHI"
    aiuc1_domains_required: [A, B, C, D, E, F]
    human_in_loop: mandatory
    adversarial_testing_cadence: quarterly
    regulatory_mapping: [SOX, SR_11-7, HIPAA, GDPR]
    cicd_gate: block_on_any_failure

  T2_significant:
    description: "Internal agent; accesses PII or confidential business data"
    aiuc1_domains_required: [A, B, C, D, E]
    human_in_loop: required_for_high_impact_actions
    adversarial_testing_cadence: semi_annual
    regulatory_mapping: [GDPR, CCPA, SOX]
    cicd_gate: block_on_A_B_E_failure

  T3_moderate:
    description: "Internal agent; accesses only public or internal data"
    aiuc1_domains_required: [B, D, E]
    human_in_loop: recommended
    adversarial_testing_cadence: annual
    regulatory_mapping: [internal_policy]
    cicd_gate: warn_on_failure

  T4_experimental:
    description: "Sandbox; no production data access; isolated environment"
    aiuc1_domains_required: [E]
    human_in_loop: optional
    adversarial_testing_cadence: as_needed
    regulatory_mapping: []
    cicd_gate: none
```

**4. Establish Vendor Due Diligence Process** (AIUC-1 E006) — for every foundation model provider, document: data handling and PII controls, training data provenance, data residency options (E011), security certifications (SOC 2 Type II, ISO 27001), and model card availability (E017).

**5. Document Processing Locations** (AIUC-1 E011) — for each regulated data classification:

```yaml
# processing_locations.yaml
processing_locations:
  PHI_data:
    allowed_regions: [us-east-1, us-west-2]
    on_prem_fallback: required_if_no_BAA
    regulatory_basis: HIPAA_164.312

  PII_EU_residents:
    allowed_regions: [eu-west-1, eu-central-1]
    cross_border_transfer: sccs_required
    regulatory_basis: GDPR_Art_44

  financial_data_sox:
    allowed_regions: [us-east-1, us-west-2]
    audit_trail_retention_years: 7
    regulatory_basis: SOX_Section_802
```

#### 3.1.2 Stage 1 CI/CD Foundation — GitHub Actions

```yaml
# .github/workflows/ai_governance_foundation.yml
name: AI Governance Foundation Gate

on:
  push:
    paths: ['agents/**', 'models/**', 'configs/agent_*.yaml']

jobs:
  aiuc1_registry_check:
    name: "AIUC-1 E015 — Registry Compliance"
    runs-on: ubuntu-latest
    steps:
      - name: Validate agent is registered in Collibra
        run: |
          python scripts/governance/check_agent_registry.py \
            --agent-id ${{ env.AGENT_ID }} \
            --collibra-url ${{ secrets.COLLIBRA_URL }} \
            --token ${{ secrets.COLLIBRA_TOKEN }}

  aiuc1_tier_check:
    name: "Agent Risk Tier Validation"
    runs-on: ubuntu-latest
    steps:
      - name: Validate risk tier assignment exists
        run: |
          python scripts/governance/validate_agent_tier.py \
            --config configs/agent_${{ env.AGENT_ID }}.yaml

  aiuc1_processing_location_check:
    name: "AIUC-1 E011 — Data Processing Location"
    runs-on: ubuntu-latest
    steps:
      - name: Check data residency compliance
        run: |
          python scripts/governance/check_processing_location.py \
            --agent-config configs/agent_${{ env.AGENT_ID }}.yaml \
            --location-policy configs/processing_locations.yaml
```

#### 3.1.3 Stage 1 → Stage 2 Advancement Gate

```
GATE: Stage 1 Complete
─────────────────────────────────────────────
☐ AI Asset Registry live in Collibra
☐ Agent risk tier framework (T1–T4) published
☐ Vendor due diligence complete for all LLM providers in use (AIUC-1 E006)
☐ AI Acceptable Use Policy published and signed by leadership (AIUC-1 E010)
☐ Data processing locations documented (AIUC-1 E011)
☐ AI governance team chartered (minimum: CAIO/CDO, AI Risk Lead, Legal)
☐ Gold layer DQ pass rate ≥ 99.5% (data foundation prerequisite)
☐ Collibra PII classification coverage = 100% (AIUC-1 A006 prerequisite)
─────────────────────────────────────────────
Approver: CDO + CAIO + Legal
```

---

### Stage 2 — Chatbots

> *"Single-channel chatbots handling FAQs and simple flows in production, basic guardrails and intent metrics, minimal backend integration."*

**Objective:** Deploy the first production-grade, governed, conversational agent. Every AIUC-1 control relevant to text-generation capability agents is validated before launch.

#### 3.2.1 Stage 2 AIUC-1 Control Activation

| AIUC-1 Control | ID | Implementation |
|----------------|-----|----------------|
| Establish input data policy | A001 | Snowflake dynamic data masking on chatbot input tables; policy in Collibra |
| Prevent PII leakage | A006 | Collibra DQ rule: scan agent outputs for PII patterns before logging |
| Prevent unauthorized agent actions | B006 | Databricks Unity Catalog permissions; Snowflake row access policies |
| Enforce user access privileges | B007 | RBAC: chatbot service account scoped to read-only certified Gold tables |
| Real-time input filtering | B005 | Prompt injection detection layer (e.g. LakeraGuard, NeMo Guardrails) |
| Limit output over-exposure | B009 | Response filtering: PII redaction, length limits, confidence thresholds |
| AI failure plan for harmful outputs | E002 | Playbook linked from Collibra AI Registry |
| AI failure plan for hallucinations | E003 | Escalation: low-confidence → human handoff → incident log |
| Log model activity | E015 | All inputs/outputs logged to Snowflake audit table |
| AI disclosure mechanisms | E016 | "You are interacting with an AI assistant" — mandatory first response |

#### 3.2.2 Agent Configuration Standard (YAML)

Every agent is deployed from a version-controlled, CI/CD-gated YAML configuration file — extending the governance-as-code philosophy from the data program to agent deployments.

```yaml
# agents/chatbot_v1.yaml
agent:
  id: "AGENT-001"
  name: "Customer Service Assistant v1"
  tier: T2
  stage: 2
  version: "1.0.0"
  owner: "customer_experience_team"
  collibra_asset_id: "COL-AG-00001"

# AIUC-1 A-series: Data & Privacy
data_policy:
  input:                                      # AIUC-1 A001
    allowed_data_sources:
      - snowflake.gold.customer_faq_kb        # Approved Gold layer only
      - snowflake.gold.product_catalog
    prohibited_data_sources:
      - "*.silver.*"
      - "*.bronze.*"
    pii_masking: enabled                      # AIUC-1 A006
    retention_days: 90
    training_use: false                       # Opt-out by default (A001)
  output:                                     # AIUC-1 A002
    pii_redaction: enabled
    ip_protection: enabled                    # AIUC-1 A004
    ownership: organization
    deletion_supported: true

# AIUC-1 B-series: Security
security:
  rbac_role: "chatbot_readonly_role"          # AIUC-1 B007
  input_filtering:                            # AIUC-1 B005
    prompt_injection_detection: enabled
    jailbreak_detection: enabled
    provider: "lakera_guard"
  output_limits:                              # AIUC-1 B009
    max_tokens: 500
    confidence_threshold: 0.75
    pii_scan_before_delivery: true
  endpoint_rate_limiting: enabled             # AIUC-1 B004

# AIUC-1 C-series: Safety
safety:
  human_in_loop:
    trigger: "confidence < 0.60 OR topic IN [legal, medical, financial_advice]"
    action: "route_to_human_agent"
  harmful_content_filter: enabled
  kill_switch:
    enabled: true
    trigger: "error_rate > 5% in 5min window"
    action: "disable_agent_route_all_to_human"

# AIUC-1 D-series: Reliability
reliability:
  fallback_response: "I'm unable to assist with that right now. Please contact support."
  timeout_seconds: 10
  retry_attempts: 2
  monitoring:
    drift_detection: enabled
    performance_dashboard: "collibra://dashboards/AGENT-001"

# AIUC-1 E-series: Accountability
accountability:
  failure_plans:
    security_breach: "runbooks/ai_security_breach_playbook.md"   # E001
    harmful_output: "runbooks/ai_harmful_output_playbook.md"     # E002
    hallucination: "runbooks/ai_hallucination_playbook.md"       # E003
  activity_logging:                                               # E015
    destination: "snowflake.audit.agent_activity_log"
    include_inputs: true
    include_outputs: true
    retention_years: 7
  disclosure:                                                     # E016
    mandatory_first_message: "You are interacting with an AI assistant. This conversation may be reviewed for quality."
  regulatory_compliance:                                          # E012
    applicable_laws: [GDPR, CCPA]
    data_protection_strategy: "configs/data_protection.yaml"

# AIUC-1 F-series: Society
society:
  bias_monitoring: enabled
  equitable_outcomes_review: quarterly
  transparency_report: annual
```

#### 3.2.3 Stage 2 CI/CD Pipeline — Full AIUC-1 Gate

```yaml
# .github/workflows/chatbot_deployment.yml
name: Chatbot Agent — AIUC-1 Governance Gate

on:
  pull_request:
    paths: ['agents/**', 'runbooks/**']

jobs:
  data_privacy_gate:
    name: "AIUC-1 A — Data & Privacy Validation"
    runs-on: ubuntu-latest
    steps:
      - name: A001 — Input data policy valid
        run: python scripts/aiuc1/validate_input_policy.py --config $AGENT_CONFIG

      - name: A006 — PII leakage prevention configured
        run: python scripts/aiuc1/check_pii_controls.py --config $AGENT_CONFIG

      - name: A003 — Data access scoped to approved sources only
        run: python scripts/aiuc1/validate_data_sources.py \
               --config $AGENT_CONFIG \
               --approved-catalog configs/approved_data_sources.yaml

  security_gate:
    name: "AIUC-1 B — Security Validation"
    runs-on: ubuntu-latest
    steps:
      - name: B006 — Agent action boundary enforced
        run: python scripts/aiuc1/check_agent_boundaries.py --config $AGENT_CONFIG

      - name: B007 — RBAC role exists and is scoped correctly
        run: python scripts/aiuc1/validate_rbac.py \
               --role $(yq '.security.rbac_role' $AGENT_CONFIG) \
               --snowflake-conn ${{ secrets.SNOWFLAKE_CONN }}

      - name: B004/B005 — Rate limiting and input filtering enabled
        run: python scripts/aiuc1/check_security_controls.py --config $AGENT_CONFIG

  safety_gate:
    name: "AIUC-1 C — Safety Controls Validation"
    runs-on: ubuntu-latest
    steps:
      - name: Kill switch configured
        run: python scripts/aiuc1/check_kill_switch.py --config $AGENT_CONFIG

      - name: Human-in-loop trigger documented
        run: python scripts/aiuc1/check_human_in_loop.py --config $AGENT_CONFIG

  accountability_gate:
    name: "AIUC-1 E — Accountability Validation"
    runs-on: ubuntu-latest
    steps:
      - name: E001-E003 — All failure playbooks exist
        run: |
          for playbook in security_breach harmful_output hallucination; do
            python scripts/aiuc1/check_playbook.py \
              --type $playbook --config $AGENT_CONFIG
          done

      - name: E015 — Activity logging to approved destination
        run: python scripts/aiuc1/check_activity_logging.py --config $AGENT_CONFIG

      - name: E016 — AI disclosure message present
        run: python scripts/aiuc1/check_disclosure.py --config $AGENT_CONFIG

      - name: E012 — Regulatory compliance documented
        run: python scripts/aiuc1/check_regulatory_mapping.py --config $AGENT_CONFIG

      - name: Collibra Registry — Agent record current
        run: python scripts/governance/sync_agent_to_collibra.py \
               --config $AGENT_CONFIG \
               --collibra-url ${{ secrets.COLLIBRA_URL }}
```

#### 3.2.4 2LOD Audit — Stage 2 (Python)

```python
# scripts/audit/stage2_2lod_audit.py
"""
Stage 2 — 2LOD Quarterly Audit
Maps to AIUC-1 domains A, B, E
"""

from dataclasses import dataclass
from typing import Optional
import snowflake.connector


@dataclass
class AuditFinding:
    control: str
    status: str       # PASS | FAIL
    severity: Optional[str]
    detail: str


class Stage2AgentAudit:
    """
    Quarterly 2LOD audit for Stage 2 chatbot agents.
    Validates AIUC-1 controls A006, B007, E015 from independent data sources.
    """

    def __init__(self, config: dict):
        self.config = config
        self.conn = snowflake.connector.connect(**config["snowflake"])

    def audit_pii_leakage(self) -> AuditFinding:
        """AIUC-1 A006 — Scan 90-day output sample for PII patterns."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS violations
            FROM audit.agent_activity_log
            WHERE agent_id = %(id)s
              AND created_at >= DATEADD(day, -90, CURRENT_TIMESTAMP())
              AND (
                REGEXP_COUNT(output_text, '\\b\\d{3}-\\d{2}-\\d{4}\\b') > 0
                OR REGEXP_COUNT(output_text, '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+') > 0
                OR REGEXP_COUNT(output_text, '\\b\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}\\b') > 0
              )
        """, {"id": self.config["agent_id"]})
        count = cursor.fetchone()[0]
        return AuditFinding(
            "A006", "PASS" if count == 0 else "FAIL",
            "CRITICAL" if count > 0 else None,
            f"{count} PII pattern matches found in output logs"
        )

    def audit_rbac_scope(self) -> AuditFinding:
        """AIUC-1 B007 — Verify service account has only approved grants."""
        cursor = self.conn.cursor()
        cursor.execute("SHOW GRANTS TO ROLE %(role)s", {"role": self.config["rbac_role"]})
        grants = cursor.fetchall()
        write_grants = [g for g in grants if any(
            p in str(g) for p in ["INSERT", "UPDATE", "DELETE", "CREATE"]
        )]
        return AuditFinding(
            "B007", "PASS" if not write_grants else "FAIL",
            "HIGH" if write_grants else None,
            f"{len(write_grants)} unauthorized write grants found"
        )

    def audit_log_completeness(self) -> AuditFinding:
        """AIUC-1 E015 — Verify 100% output logging coverage."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(CASE WHEN output_text IS NULL THEN 1 ELSE 0 END) AS missing
            FROM audit.agent_activity_log
            WHERE agent_id = %(id)s
              AND created_at >= DATEADD(day, -90, CURRENT_TIMESTAMP())
        """, {"id": self.config["agent_id"]})
        missing = cursor.fetchone()[0] or 0
        return AuditFinding(
            "E015", "PASS" if missing == 0 else "FAIL",
            "HIGH" if missing > 0 else None,
            f"{missing} log entries missing output content"
        )

    def run(self) -> dict:
        findings = [
            self.audit_pii_leakage(),
            self.audit_rbac_scope(),
            self.audit_log_completeness()
        ]
        return {
            "agent_id": self.config["agent_id"],
            "stage": 2,
            "overall": "PASS" if all(f.status == "PASS" for f in findings) else "FAIL",
            "findings": [vars(f) for f in findings]
        }
```

#### 3.2.5 Stage 2 → Stage 3 Advancement Gate

```
GATE: Stage 2 Complete
─────────────────────────────────────────────
☐ At least one chatbot in production ≥ 30 days with no P1 incidents
☐ AIUC-1 A001, A002, A006 controls verified by 1LOD
☐ AIUC-1 B005, B006, B007 controls verified by 1LOD
☐ AIUC-1 E015, E016 controls verified by 2LOD audit
☐ All failure playbooks (E001–E003) tested via tabletop exercise
☐ Quarterly bias review (F-series) completed
☐ Regulatory mapping documented (E012): GDPR/CCPA at minimum
☐ Collibra AI Registry entry current and complete
─────────────────────────────────────────────
Approver: CDO + CAIO + InfoSec + Legal
```

---

### Stage 3 — Workflows

> *"Orchestrated agents run multi-step workflows via APIs, using process maps, playbooks and real-time data on a shared platform."*

**Objective:** Extend governance to multi-step, API-integrated agents that can take actions. AIUC-1 Safety controls (C-series) become critical infrastructure at this stage.

#### 3.3.1 The Three Agent Boundary Contracts

At Stage 3, agents stop being conversational and start being **operational**. Three boundary contracts must be enforced in YAML and verified in CI/CD:

```
AGENT BOUNDARY CONTRACT
────────────────────────────────────────────────
1. DATA BOUNDARY (AIUC-1 A003)
   What data can the agent read/write?
   → Enforced via Snowflake RBAC + Databricks UC permissions
   → Verified in CI/CD before every deployment
   → Logged to Collibra lineage graph

2. ACTION BOUNDARY (AIUC-1 B006)
   What tools/APIs can the agent call?
   → Enforced via tool allowlist in agent config YAML
   → API gateway with agent identity (service principal)
   → Audit log of every tool invocation

3. AUTHORITY BOUNDARY (AIUC-1 C-series)
   What decisions require human approval?
   → Defined in agent config: dollar thresholds, data
     classifications, record counts
   → Enforced at runtime: action pauses, escalates, waits
   → Human decision logged with rationale
────────────────────────────────────────────────
```

#### 3.3.2 Workflow Agent Configuration (YAML)

```yaml
# agents/workflow_agent_v1.yaml
agent:
  id: "AGENT-003"
  name: "Finance Reconciliation Workflow Agent"
  tier: T1
  stage: 3
  version: "1.0.0"
  regulatory_scope: [SOX, BCBS_239]

# AIUC-1 A003 — Data Boundary
data_boundary:
  read_access:
    - snowflake.gold.finance.transactions
    - snowflake.gold.finance.ledger
  write_access:
    - snowflake.gold.finance.reconciliation_results
  prohibited:
    - "*.silver.*"
    - "*.bronze.*"
  pii_access: false

# AIUC-1 B006 — Action Boundary (Tool Allowlist)
action_boundary:
  allowed_tools:
    - name: "query_snowflake"
      scope: read_only
      tables: [transactions, ledger]
    - name: "write_reconciliation_result"
      scope: write
      table: reconciliation_results
      max_records_per_run: 10000
    - name: "send_alert_email"
      scope: notify_only
      recipients_allowed: [finance_team@company.com]
  prohibited_tools:
    - delete_records
    - modify_schema
    - external_api_calls
    - file_system_access

# AIUC-1 C-series — Authority Boundary (Human-in-the-Loop)
authority_boundary:
  auto_approve_conditions:
    - condition: "variance_pct < 0.01 AND record_count < 1000"
      action: auto_approve_and_log
  human_required_conditions:
    - condition: "variance_pct >= 0.01"
      action: pause_and_escalate
      escalation_contact: finance_controller@company.com
      sla_hours: 4
    - condition: "regulatory_flag = true"    # SOX-flagged transactions
      action: mandatory_human_review
      escalation_contact: sox_compliance@company.com
      sla_hours: 2
  kill_switch:
    trigger: "error_rate > 2% in 10min window OR any SOX_flag_error"
    action: halt_workflow_alert_oncall
```

#### 3.3.3 CI/CD Pipeline — Azure DevOps (Stage 3)

```yaml
# azure-pipelines-workflow-agent.yml
trigger:
  branches: [main]
  paths:
    include: ['agents/workflow_*', 'configs/boundaries_*']

stages:
  - stage: AIUC1_Governance_Gate
    displayName: "AIUC-1 Full Control Validation"
    jobs:
      - job: DataBoundaryValidation
        displayName: "AIUC-1 A003 — Data Boundary"
        steps:
          - script: |
              python scripts/aiuc1/validate_data_boundary.py \
                --config $(agentConfig) \
                --snowflake-conn $(SNOWFLAKE_CONN)
            displayName: "Verify access scoped to approved sources"

      - job: ActionBoundaryValidation
        displayName: "AIUC-1 B006 — Action Boundary"
        steps:
          - script: |
              python scripts/aiuc1/validate_tool_allowlist.py \
                --config $(agentConfig) \
                --master-allowlist configs/approved_tools.yaml
            displayName: "Verify all tools are on the approved allowlist"

      - job: AuthorityBoundaryValidation
        displayName: "AIUC-1 C — Human-in-the-Loop Triggers"
        steps:
          - script: |
              python scripts/aiuc1/validate_hitl_triggers.py --config $(agentConfig)
            displayName: "Verify human escalation paths are defined and reachable"

      - job: RegulatoryComplianceCheck
        displayName: "AIUC-1 E012 — Regulatory Mapping (SOX)"
        steps:
          - script: |
              python scripts/aiuc1/check_sox_controls.py \
                --config $(agentConfig) \
                --sox-control-matrix configs/sox_control_matrix.yaml
            displayName: "SOX control mapping for T1 financial agents"

  - stage: Databricks_Asset_Bundle_Deploy
    displayName: "Databricks Asset Bundle — Governed Deploy"
    dependsOn: AIUC1_Governance_Gate
    condition: succeeded()
    jobs:
      - job: BundleDeploy
        steps:
          - script: |
              databricks bundle validate --config databricks.yml
              databricks bundle deploy --target staging
            displayName: "Deploy to staging"

          - script: |
              python scripts/governance/register_deployment.py \
                --agent-id $(AGENT_ID) \
                --environment staging \
                --collibra-url $(COLLIBRA_URL)
            displayName: "Register deployment in Collibra AI Registry"
```

#### 3.3.4 dbt Cloud — Data Quality Contracts for Agent Consumption

```yaml
# models/gold/finance/schema.yml
models:
  - name: transactions
    description: "Certified Gold layer — approved for T1 agent consumption"
    config:
      contract:
        enforced: true          # Schema cannot drift — agents depend on this
    constraints:
      - type: not_null
        columns: [transaction_id, amount, created_at]
      - type: unique
        columns: [transaction_id]
    meta:
      aiuc1_approved_agents: [AGENT-003]
      governance_tier: T1
      data_classification: CONFIDENTIAL
      collibra_asset_id: "COL-DS-00045"
      last_2lod_audit: "2026-01-15"
```

#### 3.3.5 Stage 3 → Stage 4 Advancement Gate

```
GATE: Stage 3 Complete
─────────────────────────────────────────────
☐ At least one workflow agent in production ≥ 60 days
☐ All three boundary contracts enforced in YAML and CI/CD
☐ AIUC-1 B001 — first adversarial testing engagement completed
☐ AIUC-1 C-series — kill switch triggered and recovered in drill
☐ AIUC-1 E004 — formal change approval for agent config changes
☐ SOX/BCBS 239 control mapping complete for T1 workflow agents
☐ Collibra lineage: training data → feature → agent → output documented
☐ 2LOD quarterly audit completed with 0 critical findings
─────────────────────────────────────────────
Approver: CDO + CAIO + InfoSec + Compliance + Internal Audit
```

---

### Stage 4 — Autonomous

> *"Agents hold bounded decision rights in production, with human-in-the-loop for edge cases, explicit policies, risk tiers and monitoring."*

**Objective:** Deploy agents that make bounded autonomous decisions. This stage activates the full AIUC-1 control set and mandates third-party adversarial testing (B001).

#### 3.4.1 Stage 4 — Full AIUC-1 Activation

```
AIUC-1 MANDATORY CONTROL ACTIVATION — STAGE 4
─────────────────────────────────────────────────────────────────
DOMAIN A: DATA & PRIVACY (All 7 mandatory controls)
  A001 ✓ Input data policy — Collibra-registered, CI/CD-enforced
  A002 ✓ Output data policy — deletion/opt-out workflow documented
  A003 ✓ Data collection limited — UC + Snowflake RBAC enforced
  A004 ✓ IP/trade secret protection — output filtering active
  A005 ✓ Cross-customer isolation — tenant boundary enforced
  A006 ✓ PII leakage prevention — automated + quarterly 2LOD test
  A007 ✓ IP violation prevention — output copyright scan active

DOMAIN B: SECURITY (All 6 mandatory controls)
  B001 ✓ Adversarial testing — 3rd party quarterly (MITRE ATLAS)
  B004 ✓ Endpoint scraping prevention — rate limits + quotas
  B006 ✓ Unauthorized action prevention — tool allowlist enforced
  B007 ✓ User access privileges — RBAC quarterly certification
  B008 ✓ Deployment environment protection — encryption + access
  B009 ✓ Output over-exposure prevention — response filtering

DOMAIN C: SAFETY
  Kill switch: tested, documented, drilled
  Human-in-the-loop: all edge cases defined and operational
  Harmful output filter: active on all text-generation outputs

DOMAIN D: RELIABILITY
  Drift detection: active, thresholds set per agent tier
  Performance gates: agent auto-pauses on breach
  Fallback logic: documented in YAML and tested

DOMAIN E: ACCOUNTABILITY (All 17 controls mapped)
  E001–E003: All three failure playbooks tested quarterly
  E004: Formal CAB approval for T1 agent config changes
  E006: All LLM vendors re-assessed semi-annually
  E010: AI AUP enforced; violations tracked
  E011: Data residency verified quarterly
  E012: Regulatory compliance matrix maintained
  E015: Activity logs: 100% coverage, 7-year retention
  E016: AI disclosure: 100% of user-facing interactions

DOMAIN F: SOCIETY
  Bias audit: semi-annual; findings in Collibra
  Equitable outcomes review: by demographic segment
  Transparency report: published annually
─────────────────────────────────────────────────────────────────
```

#### 3.4.2 AIUC-1 B001 — Adversarial Testing Program (YAML Config)

```yaml
# configs/adversarial_testing_program.yaml
adversarial_testing:
  cadence: quarterly
  provider: third_party_accredited_auditor    # e.g. Schellman, NCC Group
  scope_per_agent_tier:
    T1: full_scope          # 2000+ scenarios per AIUC-1 B001
    T2: standard_scope      # 500+ scenarios
    T3: basic_scope         # 100+ scenarios

  test_categories:                            # MITRE ATLAS aligned
    prompt_injection:
      direct: true
      indirect: true          # Via tool outputs, retrieved documents
    jailbreaks:
      role_play: true
      context_manipulation: true
      encoding_evasion: true
    data_exfiltration:
      pii_extraction: true
      cross_tenant: true
    hallucination_triggers:
      financial_advice: true
      medical_advice: true
      legal_advice: true
    tool_abuse:
      unauthorized_tool_calls: true
      scope_expansion: true
      chained_exploitation: true

  evidence_requirements:
    test_report: required
    remediation_plan: required_if_critical_finding
    retest_after_remediation: required
    collibra_registry_update: required
    board_notification: if_critical_finding_in_T1
```

#### 3.4.3 SR 11-7 Model Risk Management — Agentic Extension

| SR 11-7 Requirement | Agentic AI Implementation | AIUC-1 Mapping |
|---------------------|--------------------------|-----------------|
| Model development documentation | Agent design doc + YAML config in Collibra | E017 |
| Validation by independent party | 2LOD quarterly audit + 3rd party adversarial test | B001, E008 |
| Ongoing monitoring | Drift detection + performance dashboard | D-series |
| Model inventory | Collibra AI Asset Registry | E015 |
| Change management | CAB approval for T1 agent config changes | E004 |
| Conceptual soundness | Agent design review: boundary contracts | B006 |

#### 3.4.4 HIPAA Compliance — Healthcare Agent Controls

```yaml
# configs/hipaa_agent_controls.yaml
hipaa_controls:
  minimum_necessary:                          # 45 CFR 164.514(d)
    implementation: "Snowflake column-level masking; Databricks UC column permissions"
    aiuc1_mapping: A003

  audit_controls:                             # 45 CFR 164.312(b)
    all_phi_access_logged: true
    log_destination: "snowflake.audit.phi_access_log"
    log_retention_years: 6
    aiuc1_mapping: E015

  transmission_security:                      # 45 CFR 164.312(e)
    encryption_in_transit: TLS_1_3
    encryption_at_rest: AES_256
    aiuc1_mapping: B008

  business_associate_agreement:              # Required for all LLM providers
    required_for: [openai, anthropic, snowflake_cortex, databricks]
    aiuc1_mapping: E006
```

#### 3.4.5 Stage 4 → Stage 5 Advancement Gate

```
GATE: Stage 4 Complete
─────────────────────────────────────────────
☐ All AIUC-1 mandatory controls across domains A–F implemented
☐ AIUC-1 B001 — two consecutive quarterly adversarial tests: 0 critical findings
☐ AIUC-1 pre-certification audit passed (accredited auditor)
☐ SR 11-7 model risk documentation complete (FS organizations)
☐ HIPAA BAAs signed for all LLM providers handling PHI (healthcare orgs)
☐ BCBS 239 lineage: agent outputs traceable to source data (FS orgs)
☐ GDPR/CCPA: deletion workflow for agent-generated personal data tested
☐ Internal Audit (3LOD) has reviewed the agentic AI program
☐ Board/Risk Committee briefed on agentic AI risk posture
─────────────────────────────────────────────
Approver: CDO + CAIO + CRO + General Counsel + Internal Audit + Board Risk Committee
```

---

### Stage 5 — Multi-Agent

> *"Coordinated agent teams handle complex journeys, negotiating tasks/hand-offs with observability, governance and guardrails."*

**Objective:** Govern networks of collaborating agents. AIUC-1 certification becomes the external trust signal to regulators, customers, and partners.

#### 3.5.1 Multi-Agent Governance Principles

1. **Every agent in the network is independently registered** in Collibra — no agent is governed only by virtue of being orchestrated by another
2. **Inter-agent communication is governed** — agent-to-agent messages are logged with the same standards as agent-to-human
3. **Trust is not inherited** — a T1 orchestrator cannot grant subagents elevated access; each operates only within its own boundary contract
4. **The orchestrator does not bypass controls** — AIUC-1 controls apply to orchestrators and subagents independently

#### 3.5.2 Multi-Agent Boundary Contract (YAML)

```yaml
# agents/multi_agent_orchestrator.yaml
orchestrator:
  id: "AGENT-010"
  tier: T1
  stage: 5
  agents_in_network:
    - agent_id: "AGENT-011"
      role: data_retrieval
      max_tier: T2
      communication_logged: true
    - agent_id: "AGENT-012"
      role: report_generation
      max_tier: T2
      communication_logged: true
    - agent_id: "AGENT-013"
      role: notification
      max_tier: T3
      communication_logged: true

  network_governance:
    trust_model: zero_trust             # No inherited trust between agents
    handoff_logging: enabled            # AIUC-1 E015 — all handoffs logged
    cross_agent_pii: prohibited         # AIUC-1 A005
    authority_ceiling: T1               # Network cannot exceed T1 controls
    kill_switch:
      scope: entire_network
      trigger: "any_agent_critical_error OR network_error_rate > 3%"

  observability:
    trace_all_handoffs: true
    agent_spans_to_snowflake: true
    alerting:
      alert_on: [agent_failure, boundary_violation, anomalous_behavior]
```

#### 3.5.3 AIUC-1 Certification Path

```
AIUC-1 CERTIFICATION TIMELINE
─────────────────────────────────────────────────────────────
Weeks 1–2:   Scoping questionnaire with accredited auditor
             → Determine which agents and capabilities are in scope
             → Map T1/T2 agents to full vs. reduced control sets

Weeks 3–6:   Operational control review
             → All AIUC-1 E-series documentation reviewed
             → Policy review: AUP, data policies, vendor DDs
             → Evidence collection: CI/CD logs, Collibra exports

Weeks 7–8:   Technical testing (adversarial evaluation)
             → 2000+ scenarios for T1 agents (B001)
             → Jailbreak, prompt injection, data exfiltration tests
             → Tool abuse and scope expansion tests

Week 9:      Findings review and remediation
             → Critical findings: immediate remediation required
             → High findings: 30-day remediation plan

Week 10:     Certification decision
             → Certificate issued (valid 12 months)
             → Quarterly technical testing begins (ongoing)

Ongoing:     Annual renewal + quarterly testing
             → Certificate expiry = agents taken offline
             → Treated with same urgency as SOC 2 renewal
─────────────────────────────────────────────────────────────
```

---

## Part 4: AIUC-1 Control Validator — Reusable Python Implementation

```python
# scripts/aiuc1/control_validator.py
"""
AIUC-1 Control Validator — Config-Driven, CI/CD-Injectable
Validates any agent YAML configuration against the AIUC-1 mandatory control set.
Usage: python control_validator.py --config agents/my_agent.yaml
"""

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import yaml
import json


@dataclass
class ControlResult:
    control_id: str
    control_name: str
    status: str          # PASS | FAIL | WARN | NOT_APPLICABLE
    severity: Optional[str] = None   # CRITICAL | HIGH | MEDIUM | LOW
    detail: str = ""
    remediation: str = ""


class AIUC1ControlValidator:
    """
    Validates an agent config YAML against all AIUC-1 mandatory controls.
    Parameterized by agent tier (T1–T4) to apply the correct control set.
    All checks are config-driven: add new checks without modifying caller code.
    """

    TIER_REQUIRED_DOMAINS = {
        "T1": ["A", "B", "C", "D", "E", "F"],
        "T2": ["A", "B", "C", "D", "E"],
        "T3": ["B", "D", "E"],
        "T4": ["E"],
    }

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.tier = self.config.get("agent", {}).get("tier", "T3")
        self.results: list[ControlResult] = []

    # ── DOMAIN A ──────────────────────────────────────────────────────

    def check_A001_input_data_policy(self) -> ControlResult:
        """A001 — Input data policy must be documented."""
        dp = self.config.get("data_policy", {}).get("input", {})
        if dp.get("allowed_data_sources") and dp.get("retention_days"):
            return ControlResult("A001", "Input Data Policy", "PASS")
        return ControlResult(
            "A001", "Input Data Policy", "FAIL", "CRITICAL",
            "No input data policy found.",
            "Add data_policy.input with allowed_data_sources and retention_days."
        )

    def check_A006_pii_leakage(self) -> ControlResult:
        """A006 — PII leakage prevention must be enabled."""
        output = self.config.get("data_policy", {}).get("output", {})
        pii_scan = self.config.get("security", {}).get("output_limits", {}).get("pii_scan_before_delivery")
        if output.get("pii_redaction") and pii_scan:
            return ControlResult("A006", "PII Leakage Prevention", "PASS")
        return ControlResult(
            "A006", "PII Leakage Prevention", "FAIL", "CRITICAL",
            "PII redaction not enabled.",
            "Set data_policy.output.pii_redaction=true and security.output_limits.pii_scan_before_delivery=true."
        )

    # ── DOMAIN B ──────────────────────────────────────────────────────

    def check_B006_action_boundary(self) -> ControlResult:
        """B006 — Unauthorized agent actions must be prevented via tool allowlist."""
        boundary = self.config.get("action_boundary", {})
        if boundary.get("allowed_tools") and boundary.get("prohibited_tools") is not None:
            return ControlResult("B006", "Action Boundary Enforced", "PASS")
        return ControlResult(
            "B006", "Action Boundary Enforced", "FAIL", "CRITICAL",
            "No action_boundary defined.",
            "Add action_boundary.allowed_tools and action_boundary.prohibited_tools."
        )

    def check_B007_rbac(self) -> ControlResult:
        """B007 — RBAC role must be explicitly assigned."""
        if self.config.get("security", {}).get("rbac_role"):
            return ControlResult("B007", "User Access Privileges (RBAC)", "PASS")
        return ControlResult(
            "B007", "User Access Privileges (RBAC)", "FAIL", "HIGH",
            "No RBAC role assigned.",
            "Set security.rbac_role to an explicitly scoped service role."
        )

    # ── DOMAIN C ──────────────────────────────────────────────────────

    def check_C_kill_switch(self) -> ControlResult:
        """C-series — Kill switch must be configured."""
        kill = self.config.get("safety", {}).get("kill_switch", {})
        if kill.get("enabled") and kill.get("trigger") and kill.get("action"):
            return ControlResult("C-KillSwitch", "Kill Switch Configured", "PASS")
        return ControlResult(
            "C-KillSwitch", "Kill Switch Configured", "FAIL", "CRITICAL",
            "Kill switch not configured.",
            "Add safety.kill_switch with enabled=true, trigger, and action."
        )

    def check_C_human_in_loop(self) -> ControlResult:
        """C-series — Human-in-the-loop triggers required for T1/T2."""
        if self.config.get("safety", {}).get("human_in_loop"):
            return ControlResult("C-HITL", "Human-in-the-Loop Defined", "PASS")
        if self.tier in ["T3", "T4"]:
            return ControlResult("C-HITL", "Human-in-the-Loop Defined", "NOT_APPLICABLE")
        return ControlResult(
            "C-HITL", "Human-in-the-Loop Defined", "FAIL", "HIGH",
            f"{self.tier} agent missing human-in-the-loop configuration.",
            "Add safety.human_in_loop with trigger conditions and escalation path."
        )

    # ── DOMAIN E ──────────────────────────────────────────────────────

    def check_E001_E003_failure_plans(self) -> ControlResult:
        """E001–E003 — All three failure playbooks must be present and files must exist."""
        plans = self.config.get("accountability", {}).get("failure_plans", {})
        required = ["security_breach", "harmful_output", "hallucination"]
        missing_keys = [p for p in required if not plans.get(p)]
        if missing_keys:
            return ControlResult(
                "E001-E003", "Failure Plans Present", "FAIL", "HIGH",
                f"Failure plans missing: {missing_keys}",
                "Add accountability.failure_plans for all three failure types."
            )
        missing_files = [plans[p] for p in required if not Path(plans[p]).exists()]
        if missing_files:
            return ControlResult(
                "E001-E003", "Failure Plans Present", "FAIL", "HIGH",
                f"Playbook files not found: {missing_files}",
                "Create the referenced playbook markdown files."
            )
        return ControlResult("E001-E003", "Failure Plans Present", "PASS")

    def check_E015_activity_logging(self) -> ControlResult:
        """E015 — Activity logging must be enabled with approved destination."""
        log = self.config.get("accountability", {}).get("activity_logging", {})
        if all([log.get("destination"), log.get("include_inputs"),
                log.get("include_outputs"), log.get("retention_years")]):
            return ControlResult("E015", "Activity Logging", "PASS")
        return ControlResult(
            "E015", "Activity Logging", "FAIL", "CRITICAL",
            "Activity logging incomplete.",
            "Add accountability.activity_logging with destination, include_inputs, include_outputs, retention_years."
        )

    def check_E016_disclosure(self) -> ControlResult:
        """E016 — AI disclosure mechanism for external-facing agents."""
        if self.config.get("accountability", {}).get("disclosure", {}).get("mandatory_first_message"):
            return ControlResult("E016", "AI Disclosure Mechanism", "PASS")
        if self.tier in ["T3", "T4"]:
            return ControlResult("E016", "AI Disclosure Mechanism", "WARN",
                                 detail="Consider adding disclosure for internal agents.")
        return ControlResult(
            "E016", "AI Disclosure Mechanism", "FAIL", "HIGH",
            "No AI disclosure message configured.",
            "Add accountability.disclosure.mandatory_first_message."
        )

    # ── RUNNER ────────────────────────────────────────────────────────

    def run_all(self) -> dict:
        """Run all applicable controls and return structured report."""
        required_domains = self.TIER_REQUIRED_DOMAINS.get(self.tier, ["E"])
        checks = [
            ("A", self.check_A001_input_data_policy),
            ("A", self.check_A006_pii_leakage),
            ("B", self.check_B006_action_boundary),
            ("B", self.check_B007_rbac),
            ("C", self.check_C_kill_switch),
            ("C", self.check_C_human_in_loop),
            ("E", self.check_E001_E003_failure_plans),
            ("E", self.check_E015_activity_logging),
            ("E", self.check_E016_disclosure),
        ]
        for domain, check in checks:
            if domain in required_domains:
                self.results.append(check())

        failures = [r for r in self.results if r.status == "FAIL"]
        critical = [r for r in failures if r.severity == "CRITICAL"]
        return {
            "agent_id": self.config.get("agent", {}).get("id"),
            "tier": self.tier,
            "overall_status": "PASS" if not failures else "FAIL",
            "critical_findings": len(critical),
            "total_findings": len(failures),
            "results": [vars(r) for r in self.results]
        }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="aiuc1_report.json")
    args = parser.parse_args()

    validator = AIUC1ControlValidator(args.config)
    report = validator.run_all()

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Overall: {report['overall_status']} | "
          f"Critical: {report['critical_findings']} | "
          f"Total Findings: {report['total_findings']}")

    # Non-zero exit for CI/CD gate enforcement
    exit(1 if report["overall_status"] == "FAIL" else 0)
```

---

## Part 5: Regulatory Compliance Matrix

| Regulation | Key Requirement for Agents | AIUC-1 Control | Data Program Evidence |
|------------|---------------------------|-----------------|----------------------|
| **SOX** | Audit trails for financial data used in agent decisions | E015 | Snowflake audit tables; 7-yr retention |
| **SOX** | Change management for T1 agents touching financial data | E004 | CAB approval records |
| **SR 11-7** | Independent model validation | B001 | Third-party adversarial test report |
| **SR 11-7** | Model inventory and ongoing monitoring | E015, D-series | Collibra AI Registry + drift dashboards |
| **BCBS 239** | Data lineage: risk data from source to agent output | E015 + Collibra lineage | End-to-end lineage graph |
| **HIPAA** | Minimum necessary PHI access | A003 | Snowflake column masking config |
| **HIPAA** | PHI access audit logs | E015 | Snowflake PHI audit log; 6-yr retention |
| **HIPAA** | BAA with LLM providers | E006 | Signed BAA documents |
| **GDPR** | Lawful basis for personal data processing | A001 | Data processing register |
| **GDPR** | Right to deletion of agent-generated personal data | A002 | Deletion workflow tests |
| **GDPR** | Data residency | E011 | Processing locations YAML |
| **CCPA** | Opt-out of AI training on user data | A001, A002 | Training opt-out controls |
| **EU AI Act** | Human oversight for high-risk AI | C-series | Human-in-the-loop trigger config |
| **EU AI Act** | Technical documentation for high-risk AI | E012, E017 | System cards + model docs in Collibra |
| **FDA 21 CFR Part 11** | Electronic records integrity | E015 + D-series | Tamper-evident audit logs |

---

## Part 6: Governance Operating Model

### 6.1 RACI — Agentic AI Program

| Activity | CDO | CAIO | AI Risk Lead | Data Engineering | InfoSec | Legal | Internal Audit |
|----------|-----|------|-------------|-----------------|---------|-------|----------------|
| Set AI governance policy | A | R | C | I | C | C | I |
| Maintain AI Asset Registry | A | R | C | R | I | I | I |
| Define agent risk tiers | A | R | R | C | C | C | I |
| Author agent YAML configs | I | A | C | R | C | I | I |
| Run CI/CD governance gates | I | A | C | R | R | I | I |
| Conduct adversarial testing (B001) | I | A | R | I | R | I | C |
| Conduct 2LOD audit | C | C | C | I | I | I | A/R |
| Vendor due diligence (E006) | C | A | R | I | R | R | I |
| Regulatory compliance mapping | C | A | R | I | I | R | C |
| AIUC-1 certification pursuit | A | R | C | C | C | C | C |
| Board/risk committee reporting | A | R | C | I | I | C | C |

### 6.2 CAIO KPI Dashboard

| KPI | Target | AIUC-1 Domain | Frequency |
|-----|--------|---------------|-----------|
| Agent registry coverage | 100% | E015 | Monthly |
| AIUC-1 mandatory control coverage (T1/T2) | 100% | All | Monthly |
| Critical adversarial test findings | 0 post-remediation | B001 | Quarterly |
| Agent PII leakage incidents | 0 | A006 | Monthly |
| Unauthorized agent action incidents | 0 | B006 | Monthly |
| Human-in-the-loop escalation SLA met | ≥ 99% | C-series | Monthly |
| Activity log completeness | 100% | E015 | Weekly |
| Vendor due diligence currency | 100% assessed within 12 months | E006 | Quarterly |
| AIUC-1 certification status | Certified / Pre-cert in progress | All | Annual |
| Regulatory findings from examiners | 0 critical | E012 | As-needed |

---

## Part 7: Two-Year AI Strategy Roadmap

```
YEAR 1 — GOVERN & DEPLOY (Stages 1–2)

Q1: FOUNDATION
 ├── AI Asset Registry live in Collibra (AIUC-1 E015)
 ├── Agent risk tier framework published (T1–T4)
 ├── AI Acceptable Use Policy signed by leadership (E010)
 ├── Vendor due diligence: all LLM providers assessed (E006)
 ├── Data processing locations documented (E011)
 └── AI governance CI/CD pipeline template deployed

Q2: FIRST AGENT
 ├── Stage 2 chatbot live in production
 ├── AIUC-1 A, B, E mandatory controls enforced in CI/CD
 ├── 1LOD monthly self-assessment process operational
 ├── Activity logging 100% coverage confirmed (E015)
 ├── AI disclosure mechanism live (E016)
 └── First tabletop exercise: failure plan drill (E001–E003)

Q3: WORKFLOW AGENTS
 ├── Stage 3: first workflow agent in production
 ├── Three boundary contracts enforced in YAML and CI/CD
 ├── dbt Cloud + Snowflake DQ contracts active for agent data
 ├── First 2LOD quarterly audit of agentic AI program
 ├── SOX/HIPAA regulatory control mapping complete
 └── MITRE ATLAS threat model documented for T1 agents

Q4: ADVERSARIAL TESTING
 ├── First third-party adversarial test (AIUC-1 B001)
 ├── Pre-certification readiness assessment with accredited auditor
 ├── All critical findings remediated
 ├── Full AIUC-1 mandatory control gap analysis complete
 └── Year 2 AI roadmap approved by board

──────────────────────────────────────────────────────────────

YEAR 2 — SCALE & CERTIFY (Stages 3–5)

H1: AUTONOMOUS AGENTS + CERTIFICATION
 ├── Stage 4: first autonomous agent in production
 ├── Full AIUC-1 six-domain control set active
 ├── AIUC-1 formal certification audit (Schellman or equivalent)
 ├── AIUC-1 certificate achieved
 ├── Quarterly adversarial testing program operational
 ├── 3LOD (Internal Audit) completes AI program review
 └── Board Risk Committee briefed on certified AI posture

H2: MULTI-AGENT + OPTIMIZATION
 ├── Stage 5: multi-agent network in production
 ├── Zero-trust inter-agent governance model operational
 ├── Federated AI governance: domain teams own their agents
 ├── AIUC-1 first annual renewal
 ├── DCAM/DAMA maturity benchmark includes AI dimension
 └── AI program retrospective + Year 3 roadmap
```

---

## References

| Source | Document | Relevance |
|--------|----------|-----------|
| AIUC | aiuc-1.com (2026) | Primary control standard — all agentic AI controls |
| NIST | AI RMF 1.0 (NIST AI 100-1, 2023) | Strategic GOVERN/MAP/MEASURE/MANAGE lifecycle |
| NIST | AI 600-1 GenAI Profile (2024) | GenAI-specific risk categories |
| ISO | ISO/IEC 42001 | AI Management System (AIUC-1 operationalizes) |
| MITRE | ATLAS (atlas.mitre.org) | Adversarial threat taxonomy for AI (B001 testing) |
| OWASP | LLM Top 10 | LLM vulnerability taxonomy |
| Federal Reserve | SR 11-7 (2011) | Model risk management for financial institutions |
| Basel Committee | BCBS 239 (2013) | Risk data aggregation and lineage |
| HHS | HIPAA Security Rule (45 CFR 164) | PHI handling by AI agents |
| Congress | SOX Section 802 (2002) | Audit trail retention |
| European Commission | EU AI Act (2024/1689) | High-risk AI obligations |
| European Commission | GDPR (2016/679) | Personal data processing by AI agents |
| California | CCPA (Cal. Civ. Code §1798) | Consumer data rights |
| Internal | Data Program Library v2.0 (DE, DG, BI, ML) | Foundational standards this addendum extends |
| Hogan Lovells | Agentic AI in Financial Services (2026) | Regulatory horizon scanning |
| Mayer Brown | Governance of Agentic AI Systems (2026) | Governance component framework |
| IAPP | AI Governance in the Agentic Era (2026) | Risk-based guardrail design |

---

*Document Version History*

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03 | CAIO / CDO Office | Initial release — AIUC-1 aligned, all five stages |

*Next Review: 2026-Q3 — triggered by AIUC-1 quarterly changelog update or regulatory change*
