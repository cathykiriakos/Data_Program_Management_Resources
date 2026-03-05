# Data Governance: Configuration-Based Practices & Change Management
> **Role:** Chief Data Officer | **Platform:** Snowflake / Databricks / Collibra  
> **Version:** 2.0 | **Last Updated:** 2026-03

---

## How to Use This Document

This document is written for two audiences. Use the table below to find your section:

| Section | For You If... |
|---|---|
| **Part A — Business & Executive Guide (Sections 1–3)** | You lead a team, own a data domain, sit on the Governance Council, or collaborate with IT change managers. No technical background required. |
| **Part B — Technical Implementation Guide (Sections 4–7)** | You are an engineer, architect, or platform specialist responsible for building and deploying governance configurations. |

---

# PART A — BUSINESS & EXECUTIVE GUIDE

---

## 1. What Is "Configuration-Based Governance" and Why Does It Matter?

### The Simple Idea

Think of governance configuration like a company policy manual — except instead of a PDF sitting on a shared drive that rarely gets updated, our governance rules are written as **structured digital settings** that automatically apply themselves across our data systems.

When a rule changes, we update the setting in a controlled, approved way. The system applies it everywhere it needs to go — automatically, consistently, and with a full record of who approved it and when.

> **The bottom line:** Our data rules are reliable and repeatable. They don't depend on any individual knowing the right thing to do — they are built into the systems themselves.

---

### What This Means for the Business

| Without Configuration-Based Governance | With Configuration-Based Governance |
|---|---|
| Rules live in people's heads or in documents nobody reads | Rules are enforced automatically by the systems |
| Changes happen inconsistently across teams | Every change goes through a defined, auditable approval process |
| Hard to prove to auditors what was in place and when | Every change is logged with who approved it and when |
| One person leaving can break governance | Rules are documented and replicable by the whole team |
| Changes feel risky — people avoid them | Changes are tested safely in a sandbox before reaching production |
| Governance feels like overhead | Governance becomes invisible infrastructure that just works |

---

## 2. Collibra: The Governance Command Center

### What Collibra Is

**Collibra is the central platform where all governance decisions are made, documented, and tracked.** It is the system that business users, data stewards, domain owners, and executives interact with — not the underlying databases directly.

Think of it like this: Snowflake and Databricks are the **warehouses where your data physically lives**. Collibra is the **operations center** — the place where you manage what data exists, who owns it, what it means, who can access it, and whether it's trustworthy.

```
  ┌─────────────────────────────────────────────────────┐
  │           COLLIBRA — Governance Command Center      │
  │                                                     │
  │   • Who owns this data?        Business Glossary   │
  │   • What does it mean?         Data Catalog        │
  │   • Is it trustworthy?         Data Quality        │
  │   • Who can access it?         Access Workflows    │
  │   • Where did it come from?    Lineage             │
  └──────────────────┬──────────────────────────────────┘
                     │  Rules and policies flow down
          ┌──────────▼──────────────┐
          │  Snowflake  Databricks  │  ← Data physically lives here.
          │  (enforcement layer)    │    Controls are enforced here.
          └─────────────────────────┘
```

### What Different Roles Do in Collibra

**Data Stewards** use Collibra to:
- Register and describe data assets they own
- Review and approve glossary terms in their domain
- Monitor data quality scores and respond to incidents
- Certify access lists each quarter

**Domain Owners** use Collibra to:
- See a health summary of all data in their domain
- Review and escalate governance risks
- Approve or reject access requests for sensitive data

**Executives and the CDO** use Collibra to:
- View the governance health dashboard across all domains
- Track open risks and audit findings
- Confirm program maturity is progressing
- Sign off on critical policy changes

**Data Consumers (analysts, report builders)** use Collibra to:
- Search for data they need — like a Google for your company's data
- Understand what data means before using it
- See where data came from (lineage) to build trust in numbers
- Submit access requests through a formal, tracked workflow

---

## 3. Change Management: How Governance Rules Get Updated

### Why Every Change Goes Through a Process

Changes to governance rules — even small ones — can have ripple effects: a DQ threshold that's too strict can block a critical report; an access policy change can expose sensitive data or inadvertently lock someone out. The change management process exists to **catch these impacts before they reach production**.

### The Three-Stage Approval Flow

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  STAGE 1: SUBMIT           STAGE 2: REVIEW         STAGE 3: DEPLOY
 │  ─────────────────         ────────────────         ───────────────
 │  Anyone proposes a         Approvers assess         Approved change
 │  change. They fill         risk and sign off.       is automatically
 │  in what's changing,       No approval = no         applied. A full
 │  why, and who's            change proceeds.         audit record is
 │  affected.                                          created.
 └──────────────────────────────────────────────────────────────────┘
```

All changes — even low-risk ones — are logged. This means at any point, we can answer the auditor's question: *"What was your data masking policy on March 1st, 2025, and who approved it?"*

### Risk-Based Approval: We Match Oversight to Impact

Not every change requires the same level of scrutiny. We size the approval process to the actual risk:

| Risk Level | Plain-English Example | Approval Path | Typical Timeline |
|---|---|---|---|
| 🟢 **Low** | Adding a quality check to a new report | Data Steward | Same day |
| 🟡 **Medium** | Changing how strict a quality threshold is | Steward + Data Governance Office | 2–3 days |
| 🟠 **High** | Changing who can see a dataset | DGO + CISO | 5 days |
| 🔴 **Critical** | Renaming or removing a core data field | CDO + Domain Owner + Full CAB | 10 days |
| 🔴 **Regulatory** | Changing masking on a field with SSNs or card numbers | CISO + Legal + DGO | 10 days + Legal review |

### The Change Advisory Board (CAB)

For high-risk and critical changes, a standing **Change Advisory Board (CAB)** reviews and approves before anything is applied to production. The data governance track of CAB meets weekly.

**Who sits on CAB:**

| Role | Why They're There |
|---|---|
| IT Change Manager (chair) | Ensures the process is followed correctly |
| Data Architect | Assesses technical risk and downstream impact |
| DGO Representative | Assesses governance and compliance implications |
| Domain Owner | Business accountability for the affected domain |
| CISO Representative | Required for any change affecting access or sensitive data |

> **Note for executives:** CDO sign-off is required on any Critical-rated change. This is intentional — it ensures senior visibility on decisions that carry material risk.

### What a Good Change Request Captures

A well-written change request answers five questions:

1. **What** is changing — described in plain language, not technical jargon
2. **Why** it is changing — the business justification
3. **Who is affected** — downstream teams, reports, and pipelines
4. **What could go wrong** — a brief risk assessment
5. **How to reverse it** — a tested rollback plan

All requests are stored in the ITSM system (e.g., ServiceNow or Jira) and linked to the corresponding technical change in Git and Collibra.

---

# PART B — TECHNICAL IMPLEMENTATION GUIDE

---

## 4. Governance-as-Code Architecture

### Core Principle

All governance configurations are:
- **Declarative** — described in YAML/JSON config files, not hardcoded scripts
- **Version-controlled** — stored in Git with full change history
- **Peer-reviewed** — changes require pull request (PR) approval before merge
- **Automated** — applied via CI/CD pipelines on approved merge
- **Auditable** — every change traceable to a person, ticket, and timestamp

### Repository Structure

```
governance-config/
├── collibra/
│   ├── domains.yaml              # Domain hierarchy, owners, stewards
│   ├── asset_types.yaml          # Custom Collibra asset type definitions
│   ├── workflows.yaml            # Workflow configuration (tasks, routing)
│   └── glossary_terms.yaml       # Business glossary term definitions
├── classification/
│   ├── tag_definitions.yaml      # Classification tier tag definitions
│   └── masking_policies.yaml     # Masking rules per classification tier
├── dq/
│   ├── rules_registry.yaml       # All DQ rules: owner, severity, SLA, asset
│   └── thresholds.yaml           # KPI alert thresholds
├── access/
│   ├── roles.yaml                # RBAC role definitions per domain
│   └── row_policies.yaml         # Row-level security rules
├── lifecycle/
│   ├── retention_policies.yaml   # Retention schedule by classification
│   └── archival_rules.yaml       # Archival triggers
├── monitoring/
│   ├── kpi_config.yaml           # KPI query definitions
│   └── alert_thresholds.yaml     # Alert routing configuration
└── README.md
```

---

## 5. Collibra Integration Pattern

### 5.1 Collibra REST API Manager

```python
# collibra_governance_manager.py
# Config-driven Collibra API wrapper — repeatable across all governance operations

import yaml
import requests
import logging

logger = logging.getLogger(__name__)


class CollibraGovernanceManager:
    """
    Manages Collibra assets, classifications, glossary terms, and workflows
    via the Collibra REST API. All configurations are driven from YAML files.
    """

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({"Content-Type": "application/json"})

    # ─── Asset Management ────────────────────────────────────────────

    def upsert_asset(self, domain_id: str, asset: dict) -> dict:
        """Create or update a catalog asset in Collibra."""
        payload = {
            "name": asset["name"],
            "displayName": asset.get("display_name", asset["name"]),
            "typeId": asset["type_id"],
            "domainId": domain_id,
            "statusId": asset.get("status_id"),
            "description": asset.get("description", ""),
        }
        resp = self.session.post(
            f"{self.base_url}/rest/2.0/assets", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def set_asset_attribute(
        self, asset_id: str, attribute_type_id: str, value: str
    ) -> dict:
        """Set a metadata attribute (classification, owner, SLA) on an asset."""
        payload = {
            "assetId": asset_id,
            "typeId": attribute_type_id,
            "value": value,
        }
        resp = self.session.post(
            f"{self.base_url}/rest/2.0/attributes", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    # ─── Glossary Management ─────────────────────────────────────────

    def publish_glossary_terms(self, config_path: str):
        """Bulk publish glossary terms from YAML config into Collibra."""
        with open(config_path) as f:
            config = yaml.safe_load(f)

        for term in config["terms"]:
            logger.info(f"Publishing glossary term: {term['name']}")
            asset = self.upsert_asset(
                domain_id=config["glossary_domain_id"],
                asset={
                    "name": term["name"],
                    "display_name": term["name"],
                    "type_id": config["business_term_type_id"],
                    "description": term["definition"],
                }
            )
            if "owner" in term:
                self.set_asset_attribute(
                    asset_id=asset["id"],
                    attribute_type_id=config["owner_attribute_type_id"],
                    value=term["owner"]
                )

    # ─── Classification Sync to Snowflake ────────────────────────────

    def sync_classification_to_snowflake(
        self,
        snowflake_conn,
        snowflake_table: str,
        snowflake_column: str,
        classification_tier: str
    ):
        """
        Push a Collibra classification decision to a Snowflake column tag.
        Triggered after classification is set or updated in Collibra.
        """
        tag_map = {
            "PUBLIC": "PUBLIC",
            "INTERNAL": "INTERNAL",
            "CONFIDENTIAL": "CONFIDENTIAL",
            "RESTRICTED": "RESTRICTED"
        }
        tag_value = tag_map.get(classification_tier, "INTERNAL")
        sql = f"""
            ALTER TABLE {snowflake_table}
            MODIFY COLUMN {snowflake_column}
            SET TAG governance.classification_tier = '{tag_value}';
        """
        snowflake_conn.cursor().execute(sql)
        logger.info(
            f"Synced classification '{tag_value}' to "
            f"{snowflake_table}.{snowflake_column}"
        )

    # ─── Workflow Triggers ────────────────────────────────────────────

    def trigger_steward_task(
        self,
        workflow_id: str,
        asset_id: str,
        task_type: str,
        message: str
    ) -> dict:
        """Trigger a Collibra workflow task — DQ incident, access review, etc."""
        payload = {
            "workflowDefinitionId": workflow_id,
            "businessItemId": asset_id,
            "businessItemType": "Asset",
            "taskType": task_type,
            "message": message
        }
        resp = self.session.post(
            f"{self.base_url}/rest/2.0/workflowInstances", json=payload
        )
        resp.raise_for_status()
        return resp.json()
```

### 5.2 Collibra Domain & Glossary Configuration

```yaml
# collibra/domains.yaml
governance_domains:
  - name: "Finance"
    description: "Financial data assets including revenue, GL, and reporting"
    owner_email: "finance_data_owner@company.com"
    steward_email: "finance_steward@company.com"
    classification_default: "CONFIDENTIAL"
    collibra_community: "Enterprise Data"

  - name: "Customer"
    description: "Customer master data, CRM, and interaction data"
    owner_email: "customer_data_owner@company.com"
    steward_email: "customer_steward@company.com"
    classification_default: "RESTRICTED"
    collibra_community: "Enterprise Data"

  - name: "Operations"
    description: "Supply chain, fulfillment, and operational metrics"
    owner_email: "ops_data_owner@company.com"
    steward_email: "ops_steward@company.com"
    classification_default: "INTERNAL"
    collibra_community: "Enterprise Data"
```

```yaml
# collibra/glossary_terms.yaml
glossary_domain_id: "<collibra-glossary-domain-uuid>"
business_term_type_id: "<collibra-business-term-type-uuid>"
owner_attribute_type_id: "<collibra-owner-attribute-uuid>"

terms:
  - name: "Annual Recurring Revenue (ARR)"
    definition: >
      The annualized value of all active subscription contracts.
      Calculated as monthly recurring revenue multiplied by 12.
      Excludes one-time fees and professional services revenue.
    domain: "Finance"
    owner: "finance_steward@company.com"
    synonyms: ["ARR", "Annualized Revenue"]
    related_assets:
      - "prod_finance.curated.revenue_summary"

  - name: "Customer Lifetime Value (CLV)"
    definition: >
      The total net revenue expected from a customer over the full
      duration of their relationship with the company.
    domain: "Customer"
    owner: "customer_steward@company.com"
    synonyms: ["LTV", "CLTV"]
```

---

## 6. Snowflake & Databricks Configuration Templates

### 6.1 Snowflake — Dynamic Data Masking

```sql
-- Applies to: columns with RESTRICTED classification (set in Collibra, synced here)
CREATE OR REPLACE MASKING POLICY governance.policies.mask_pii
  AS (val STRING) RETURNS STRING ->
    CASE
      WHEN IS_ROLE_IN_SESSION('RESTRICTED_READ') THEN val
      WHEN IS_ROLE_IN_SESSION('COMPLIANCE_AUDIT') THEN val
      ELSE '***MASKED***'
    END;

ALTER TABLE prod_customer.curated.customers
  MODIFY COLUMN ssn
  SET MASKING POLICY governance.policies.mask_pii;
```

### 6.2 Snowflake — Row Access Policy

```sql
CREATE OR REPLACE ROW ACCESS POLICY governance.policies.finance_domain_access
  AS (domain_code STRING) RETURNS BOOLEAN ->
    CASE
      WHEN IS_ROLE_IN_SESSION('FINANCE_READ') AND domain_code = 'FINANCE' THEN TRUE
      WHEN IS_ROLE_IN_SESSION('SYSADMIN') THEN TRUE
      WHEN IS_ROLE_IN_SESSION('DATA_GOVERNANCE_AUDIT') THEN TRUE
      ELSE FALSE
    END;
```

### 6.3 Python Config Deployer

```python
# deploy_governance_config.py
import yaml, json, logging, argparse, os
import snowflake.connector
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GovernanceConfigDeployer:
    """
    Deploys governance configurations to Snowflake from YAML source of truth.
    Triggered via CI/CD on merge to main in the governance-config repo.
    """

    def __init__(self, config_dir: str, conn_params: dict, dry_run: bool = False):
        self.config_dir = Path(config_dir)
        self.conn = snowflake.connector.connect(**conn_params)
        self.dry_run = dry_run
        self.change_log = []

    def deploy_all(self):
        self.deploy_tags()
        self.deploy_retention_configs()
        self._write_change_log()

    def deploy_tags(self):
        config_path = self.config_dir / "classification" / "tag_definitions.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        for tag in config["tags"]:
            sql = (
                f"CREATE OR REPLACE TAG {tag['database']}.{tag['schema']}.{tag['name']} "
                f"ALLOWED_VALUES {', '.join(repr(v) for v in tag['allowed_values'])} "
                f"COMMENT = '{tag.get('description', '')}';"
            )
            self._execute(sql, f"Deploy tag: {tag['name']}")

    def deploy_retention_configs(self):
        config_path = self.config_dir / "lifecycle" / "retention_policies.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        for policy in config["retention_policies"]:
            for asset in policy["assets"]:
                sql = (
                    f"ALTER TABLE {asset} "
                    f"SET DATA_RETENTION_TIME_IN_DAYS = {policy['retention_days']};"
                )
                self._execute(sql, f"Set retention on {asset}")

    def _execute(self, sql: str, description: str):
        if self.dry_run:
            logger.info(f"[DRY RUN] {description}")
        else:
            logger.info(f"Executing: {description}")
            self.conn.cursor().execute(sql)
            self.change_log.append({"description": description, "sql": sql})

    def _write_change_log(self):
        log_path = Path("deployment_log.json")
        with open(log_path, "w") as f:
            json.dump(
                {"deployed_at": datetime.utcnow().isoformat(),
                 "dry_run": self.dry_run,
                 "changes": self.change_log},
                f, indent=2
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-dir", required=True)
    parser.add_argument("--env", choices=["dev", "qa", "prod"], required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn_params = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": "GOVERNANCE_DEPLOYER",
        "warehouse": "GOVERNANCE_WH"
    }
    GovernanceConfigDeployer(args.config_dir, conn_params, args.dry_run).deploy_all()
```

---

## 7. CI/CD Pipeline for Governance Configs

```yaml
# .github/workflows/governance_deploy.yml
name: Governance Config Deployment

on:
  push:
    branches: [main]
    paths: ['governance-config/**']
  pull_request:
    branches: [main]
    paths: ['governance-config/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate YAML configs
        run: python scripts/validate_governance_configs.py
      - name: Dry-run to DEV
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER_DEV }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD_DEV }}
        run: |
          python deploy_governance_config.py \
            --config-dir governance-config --env dev --dry-run

  deploy_dev:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to DEV
        run: |
          python deploy_governance_config.py \
            --config-dir governance-config --env dev

  deploy_prod:
    needs: deploy_dev
    runs-on: ubuntu-latest
    environment: production   # Manual approval gate required in GitHub
    steps:
      - name: Deploy to PROD
        run: |
          python deploy_governance_config.py \
            --config-dir governance-config --env prod
```

---

## 8. Change Request Template (for IT / CAB Submission)

```markdown
## Data Governance Change Request

**Change ID:** GCR-[YYYY]-[NNN]
**Requested By:** [Name, Team]
**Request Date:** [Date]
**Target Environment:** DEV / QA / PROD
**Change Window:** [Date/Time or CAB Date]

### Change Description
[Plain language — what is changing, why, and what business need it serves]

### Change Type
- [ ] New DQ rule (Collibra DQ + YAML registry)
- [ ] Modified DQ threshold
- [ ] New/updated classification tag (Collibra → Snowflake/Databricks sync)
- [ ] Modified access policy (Collibra policy → platform RBAC)
- [ ] Schema change (additive — low risk)
- [ ] Schema change (breaking — requires CDO sign-off)
- [ ] Masking policy change
- [ ] Retention policy change
- [ ] Collibra workflow, attribute, or domain configuration change
- [ ] Other: ___

### Risk Assessment
**Risk Level:** Low / Medium / High / Critical
**Downstream Impact:** [Affected consumers, dashboards, or pipelines]
**Collibra Impact:** [Any Collibra assets, workflows, or attributes changing?]
**DQ Rule Impact:** [Will any quality rules break or need updating?]
**Access Impact:** [Will any user's access change — gain or lose?]

### Testing Evidence
- [ ] Validated in DEV environment
- [ ] Collibra staging environment tested (if applicable)
- [ ] DQ checks pass post-change in DEV
- [ ] Downstream consumer tested
- [ ] Rollback plan documented and tested

### Approvals Required
- [ ] Data Steward: ___________
- [ ] DGO Representative: ___________
- [ ] IT Change Manager: ___________
- [ ] CISO (if access or masking change): ___________
- [ ] CDO (if breaking or regulatory change): ___________

### Rollback Plan
[Step-by-step procedure to reverse this change if issues arise in PROD]

### Reference Links
- GitHub Pull Request: [link]
- Collibra Change Record: [link]
- ITSM Ticket: [link]
```

---

*Document Owner: Data Governance Office + IT Change Management | Review Cycle: Annual*
