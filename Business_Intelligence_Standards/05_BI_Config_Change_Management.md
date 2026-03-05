# BI Configuration-Based Practices & Change Management
## Working with IT Change Managers: Tableau | Power BI | Alteryx

**Document Owner:** Chief Data Office  
**Domain:** Business Intelligence  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Config-First BI Operations](#1-config-first-bi-operations)
2. [Report & Dataset Configuration Standards](#2-report--dataset-configuration-standards)
3. [Environment Promotion Pipelines](#3-environment-promotion-pipelines)
4. [IT Change Management Integration](#4-it-change-management-integration)
5. [Branding as Configuration](#5-branding-as-configuration)
6. [Access Provisioning as Configuration](#6-access-provisioning-as-configuration)
7. [Monitoring & Alert Configuration](#7-monitoring--alert-configuration)
8. [Change Classification Reference](#8-change-classification-reference)

---

## 1. Config-First BI Operations

### 1.1 Philosophy

BI governance without configuration management is not governance — it is aspiration. The same config-first principle that governs data engineering pipelines must apply to BI operations:

| BI Concern | Config-Driven Approach |
|---|---|
| Who has access to which workspace | IdP group membership YAML; not manual tool assignment |
| What data sources are approved | Approved Data Source Registry YAML in Git |
| Which reports exist and who owns them | Report Registry YAML in Git |
| Branding standards | Theme JSON / template XML in Git |
| Resource monitors and compute budgets | Terraform or SQL scripts in Git |
| Scheduled refresh windows | Deployment config in Git |
| Sensitivity labels and their behavior | Purview policy config in Git |

### 1.2 What This Enables

- **Repeatability:** Every workspace can be rebuilt from config if a disaster recovery is needed.
- **Auditability:** Every change to access, standards, or configuration is a Git commit with author and timestamp.
- **Change control:** IT change managers can review a Terraform plan or config diff — not a verbal description of changes made in a UI.
- **Drift detection:** Automated comparison of actual platform state vs. declared config catches unauthorized manual changes.

---

## 2. Report & Dataset Configuration Standards

### 2.1 Report Registry as Code

The Report Registry is the authoritative record of all BI content. It is maintained as YAML files in a version-controlled repository.

```yaml
# report_registry/finance/revenue_performance.yaml
report:
  id: "RPT-2024-047"
  name: "Monthly Revenue Performance"
  version: "2.1.0"
  tier: T1
  tool: power_bi
  workspace: "Finance - Production"
  dataset_id: "DS-001"
  url: "https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}"

owner:
  name: "Finance BI Lead"
  email: "finance-bi@company.com"
  team: "Finance"
  backup_owner: "senior-bi-dev@company.com"

classification:
  level: CONFIDENTIAL
  pii_contains: false
  regulatory_use: true
  regulatory_frameworks: ["SOX"]

audience:
  groups:
    - "Finance Team"
    - "FP&A"
    - "Executive Leadership"
  rls_applied: true
  external_sharing: false

schedule:
  refresh_cron: "0 5 * * *"       # 5 AM UTC daily
  sla_available_by: "06:00 UTC"
  timezone: UTC

lifecycle:
  status: active                   # draft | active | deprecated | archived
  certified: true
  certification_date: "2024-01-15"
  certification_by: "BI COE Lead"
  last_reviewed: "2024-07-15"
  next_review: "2025-01-15"
  replace_reports: []              # IDs of deprecated reports this replaces
  
performance:
  target_load_seconds: 4
  max_load_seconds: 5
  last_performance_test: "2024-07-10"
  last_performance_result_seconds: 3.8
```

### 2.2 Approved Data Source Registry as Code

```yaml
# data_source_registry/finance_revenue_dataset.yaml
data_source:
  id: "DS-001"
  name: "Finance Revenue Dataset"
  version: "3.0.0"
  
platform:
  tool: power_bi
  workspace: "Certified Datasets"
  dataset_id: "{power_bi_dataset_guid}"   # Set at deployment time

underlying_source:
  platform: snowflake
  account: "myorg-prod.snowflakecomputing.com"
  database: "PROD_FINANCE_GOLD"
  schema: "finance"
  primary_tables:
    - "fact_revenue"
    - "dim_customer"
    - "dim_product"
    - "dim_date"
  dbt_models:
    - "finance.fact_revenue"
    - "finance.dim_customer"

connection:
  type: directquery            # directquery | import | live_connection
  service_account_secret: "prod/powerbi/svc_finance_pbi"
  gateway: null                # null = cloud-to-cloud; set for on-prem

security:
  rls_enabled: true
  rls_roles:
    - name: "RegionalSalesRLS"
      description: "Users see only their assigned region(s)"
      filter_table: "dim_user_region_access"
      filter_column: "region_code"
      current_user_column: "user_email"
  ols_enabled: false           # Object-level security
  classification: CONFIDENTIAL
  pii_contains: false

governance:
  owner: "BI COE - Finance Analytics"
  domain: "DOMAIN_FINANCE"
  approved_audiences:
    - "Finance Team"
    - "FP&A"
    - "Executive Leadership"
  approved_date: "2024-01-15"
  next_review: "2025-01-15"
  status: active
  certified: true
```

---

## 3. Environment Promotion Pipelines

### 3.1 Power BI Deployment Pipeline Configuration

Power BI content promotion is managed via deployment pipelines configured in code, not manual publish-to-workspace.

```python
# powerbi_deploy.py
# Promotes Power BI content through deployment pipeline stages

import requests
import os
import json
import time

class PowerBIDeployer:
    """
    Config-driven Power BI deployment pipeline manager.
    All promotion is via API — no manual publish to production.
    """

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.token = self._get_token(tenant_id, client_id, client_secret)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _get_token(self, tenant_id, client_id, client_secret) -> str:
        resp = requests.post(
            f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "https://analysis.windows.net/powerbi/api/.default"
            }
        )
        return resp.json()["access_token"]

    def deploy_stage(
        self,
        pipeline_id: str,
        source_stage: int,      # 0=dev, 1=test, 2=prod
        target_stage: int,
        artifact_ids: list[str],
        allow_purge: bool = False
    ) -> dict:
        """Deploy specific artifacts from one pipeline stage to the next."""
        payload = {
            "sourceStageOrder": source_stage,
            "artifactsToDeploy": {
                "reports": [{"id": aid} for aid in artifact_ids]
            },
            "options": {
                "allowPurgeData": allow_purge,
                "allowOverwriteArtifact": True
            }
        }
        resp = requests.post(
            f"{self.BASE_URL}/pipelines/{pipeline_id}/deploy",
            headers=self.headers,
            json=payload
        )
        resp.raise_for_status()
        return resp.json()

    def bind_dataset_to_gateway(
        self,
        dataset_id: str,
        datasource_bindings: list[dict]
    ) -> None:
        """
        Apply environment-specific data source bindings post-deploy.
        Bindings are defined in config — not hardcoded.
        """
        requests.post(
            f"{self.BASE_URL}/datasets/{dataset_id}/Default.BindToGateway",
            headers=self.headers,
            json={"gatewayObjectId": None, "datasourceObjectIds": datasource_bindings}
        ).raise_for_status()


# Usage in CI/CD:
# deployer = PowerBIDeployer(tenant_id, client_id, client_secret)
# deployer.deploy_stage(pipeline_id="xxx", source_stage=1, target_stage=2, artifact_ids=["yyy"])
```

### 3.2 Tableau Promotion via REST API

```python
# tableau_promote.py
# Promotes Tableau workbooks from dev project to prod project via REST API

import tableauserverclient as TSC

def promote_workbook(
    server: TSC.Server,
    workbook_name: str,
    source_project: str,
    target_project: str,
    validation_checklist_passed: bool
) -> TSC.WorkbookItem:
    """
    Promotes a workbook from source project to target project.
    Requires checklist sign-off before promotion to production.
    
    Returns the new workbook item in the target project.
    """
    if not validation_checklist_passed:
        raise PermissionError(
            "Publication checklist must be signed off before promoting to production."
        )

    # Find source workbook
    all_wbs, _ = server.workbooks.get()
    source_wbs = [
        wb for wb in all_wbs
        if wb.name == workbook_name and wb.project_name == source_project
    ]
    if not source_wbs:
        raise ValueError(f"Workbook '{workbook_name}' not found in '{source_project}'")

    source_wb = source_wbs[0]

    # Download source workbook
    server.workbooks.download(source_wb.id, filepath=f"/tmp/{workbook_name}.twbx")

    # Find target project
    all_projects, _ = server.projects.get()
    target_projects = [p for p in all_projects if p.name == target_project]
    if not target_projects:
        raise ValueError(f"Target project '{target_project}' not found")

    # Publish to target
    new_wb = TSC.WorkbookItem(project_id=target_projects[0].id, name=workbook_name)
    published = server.workbooks.publish(
        new_wb,
        f"/tmp/{workbook_name}.twbx",
        TSC.Server.PublishMode.Overwrite
    )
    return published
```

### 3.3 CI/CD Pipeline for BI Assets

```yaml
# .github/workflows/bi_cicd.yml
name: BI Content Deployment

on:
  pull_request:
    branches: [main]
    paths:
      - 'bi/**'
      - 'report_registry/**'
      - 'data_source_registry/**'
  push:
    branches: [main]
    paths:
      - 'bi/**'
      - 'report_registry/**'
      - 'data_source_registry/**'

jobs:
  # ── 1. Validate Registry Files ──────────────────────────────────
  validate-registry:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install pyyaml jsonschema
      - name: Validate Report Registry YAML
        run: python scripts/validate_report_registry.py --dir report_registry/
      - name: Validate Data Source Registry YAML
        run: python scripts/validate_datasource_registry.py --dir data_source_registry/

  # ── 2. Brand Compliance Check ────────────────────────────────────
  brand-compliance:
    runs-on: ubuntu-latest
    needs: [validate-registry]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install lxml
      - name: Validate Tableau Workbook Branding
        run: |
          for twb in bi/tableau/**/*.twb; do
            python scripts/tableau_brand_validator.py --file "$twb"
          done
      - name: Validate Power BI Theme File
        run: python scripts/powerbi_theme_validator.py --file bi/powerbi/theme/corporate_theme.json

  # ── 3. Deploy to Production (on merge to main) ──────────────────
  deploy-production:
    runs-on: ubuntu-latest
    needs: [brand-compliance]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install msal requests
      - name: Deploy Power BI via Deployment Pipeline
        env:
          PBI_TENANT_ID: ${{ secrets.PBI_TENANT_ID }}
          PBI_CLIENT_ID: ${{ secrets.PBI_CLIENT_ID }}
          PBI_CLIENT_SECRET: ${{ secrets.PBI_CLIENT_SECRET }}
        run: python scripts/powerbi_deploy.py --env prod --pipeline-id ${{ vars.PBI_PIPELINE_ID }}
      - name: Promote Tableau Workbooks
        env:
          TABLEAU_SERVER: ${{ secrets.TABLEAU_SERVER_URL }}
          TABLEAU_TOKEN_NAME: ${{ secrets.TABLEAU_TOKEN_NAME }}
          TABLEAU_TOKEN_VALUE: ${{ secrets.TABLEAU_TOKEN_VALUE }}
        run: python scripts/tableau_promote.py --env prod
```

---

## 4. IT Change Management Integration

### 4.1 BI Change Tiers

| Change | Tier | Lead Time | Process |
|---|---|---|---|
| T3 self-service report created or updated | Self-service | Immediate | No ticket; user policy acknowledgment |
| T2 domain report update (no schema change) | Standard | Same day | PR review + Domain BI Lead approval |
| New T2 report published | Standard | 3–5 days | PR review + BI COE review + domain owner |
| New T1 certified report | Minor | 5–10 days | BI COE review + domain owner + change ticket |
| Certified dataset update (additive column) | Minor | 5 days | BI COE + DE Lead review + change ticket |
| RLS rule change on certified dataset | Minor | 5 days | Data Governance review + change ticket |
| Workspace restructure / project rename | Minor | 5–10 days | BI COE + IT + change ticket |
| Sensitivity label policy change | Major | 10–15 days | Data Governance + IT + CAB |
| New BI platform environment | Major | 10–15 days | BI COE + IT + InfoSec + CAB |
| SSO reconfiguration | Major | 10–15 days | BI COE + IT + InfoSec + CAB |
| External sharing enablement | Major | 15+ days | CDO + Legal + Privacy + CAB |
| BI tool version upgrade | Major | 10–15 days | BI COE + IT + CAB |
| New BI tool adoption | Major | 30+ days | CDO + IT + Procurement + CAB |

### 4.2 Change Request Template — BI Minor Change

```markdown
## BI Minor Change Request

**Ticket ID:** CHG-BI-YYYY-NNN
**Requestor:** [Name, Team]
**Date Submitted:** YYYY-MM-DD
**Target Deployment Date:** YYYY-MM-DD

### Change Summary
[Plain English: what is changing, why, and who is impacted]

### Affected BI Assets
- [ ] Report(s): [name, tier, tool]
- [ ] Dataset(s): [name, tool]
- [ ] Workspace(s): [name, tool]
- [ ] Branding/theme files
- [ ] Access/permissions
- [ ] Scheduled refresh configuration
- [ ] Resource monitors

### Data Source Impact
- [ ] No change to underlying data source
- [ ] New column(s) added to certified dataset
- [ ] RLS rule change — describe:
- [ ] Data classification change — describe:

### Security Review
- [ ] No PII impact
- [ ] PII impact — Privacy Officer notified: Yes / No

### Testing Evidence
- Tested in development workspace: Yes / No
- RLS tested as restricted user: Yes / No (if applicable)
- Performance tested (load time): ___ seconds
- Brand compliance validated: Yes / No

### Downstream Consumer Impact
- [ ] No downstream reports affected
- [ ] Affected reports: [list]
- [ ] Consumers notified: Yes / No — Date: ___

### Rollback Plan
[Steps to revert within 30 minutes]

### Approvals
- Domain BI Lead: _____________ Date: _______
- BI COE Lead: _____________ Date: _______
- Data Governance Lead: _____________ Date: _______ (required for RLS/classification changes)
```

---

## 5. Branding as Configuration

### 5.1 Brand Theme as Code

Branding standards are declared in version-controlled config files. They are deployed as code, not set manually in tool UIs.

```python
# brand_config.py
"""
Single source of truth for all BI branding standards.
All theme files generated from this config — never edited directly.
"""

from dataclasses import dataclass, field

@dataclass
class BrandConfig:
    # Typography
    primary_font: str = "Calibri"
    secondary_font: str = "Calibri"
    heading_size: int = 14
    body_size: int = 11
    caption_size: int = 9

    # Colors
    primary_color: str = "#1A3A5C"
    secondary_color: str = "#2E6DA4"
    accent_color: str = "#F5A623"
    success_color: str = "#7ED321"
    warning_color: str = "#F5A623"
    error_color: str = "#D0021B"
    neutral_light: str = "#F5F5F5"
    neutral_dark: str = "#1A1A1A"
    background_color: str = "#FFFFFF"

    # Data palette (categorical)
    data_colors: list[str] = field(default_factory=lambda: [
        "#1A3A5C", "#2E6DA4", "#4A90D9",
        "#F5A623", "#D0021B", "#7ED321",
        "#9B59B6"
    ])

    # Logo
    logo_path: str = "assets/logo_official.svg"
    logo_dark_path: str = "assets/logo_dark.svg"

    # Classification watermark styles
    classification_colors: dict = field(default_factory=lambda: {
        "PUBLIC":       {"bg": "#E8F5E9", "text": "#2E7D32"},
        "INTERNAL":     {"bg": "#E3F2FD", "text": "#1565C0"},
        "CONFIDENTIAL": {"bg": "#FFF8E1", "text": "#F57F17"},
        "RESTRICTED":   {"bg": "#FFEBEE", "text": "#B71C1C"},
        "TOP_SECRET":   {"bg": "#1A1A1A", "text": "#FFFFFF"},
    })

    # Layout
    header_height_px: int = 60
    footer_height_px: int = 40


def generate_powerbi_theme(config: BrandConfig) -> dict:
    """Generate Power BI JSON theme file from brand config."""
    return {
        "name": "Corporate Brand Theme",
        "dataColors": config.data_colors,
        "background": config.background_color,
        "foreground": config.neutral_dark,
        "tableAccent": config.secondary_color,
        "visualStyles": {
            "*": {
                "*": {
                    "fontFamily": [{"value": config.primary_font}],
                    "fontSize": [{"value": config.body_size}],
                }
            },
            "title": {
                "*": {
                    "fontFamily": [{"value": config.primary_font}],
                    "fontSize": [{"value": config.heading_size}],
                    "fontBold": [{"value": True}],
                    "fontColor": [{"value": {"solid": {"color": config.primary_color}}}]
                }
            }
        }
    }


def generate_tableau_color_palette(config: BrandConfig) -> str:
    """Generate Tableau preferences XML block for brand colors."""
    colors_xml = "\n".join(
        f'        <color-palette name="Corporate Brand" type="ordered-sequential">'
    )
    for color in config.data_colors:
        colors_xml += f'\n            <color>{color}</color>'
    colors_xml += "\n        </color-palette>"
    return colors_xml
```

### 5.2 Theme Deployment Automation

```python
# deploy_brand_theme.py
"""
Deploys brand theme to Power BI tenant via Admin API.
Run as part of CI/CD when brand_config.py changes.
"""

import json
import requests
from brand_config import BrandConfig, generate_powerbi_theme

def deploy_powerbi_organizational_theme(token: str, config: BrandConfig) -> None:
    """Apply org-wide theme to Power BI tenant."""
    theme_dict = generate_powerbi_theme(config)
    theme_json = json.dumps(theme_dict)
    
    response = requests.post(
        "https://api.powerbi.com/v1.0/myorg/admin/organizationalVisuals",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "themeName": "Corporate Brand Theme",
            "themeJson": theme_json,
            "backgroundImageAlignment": "Center",
            "backgroundImageFit": "Normal"
        }
    )
    response.raise_for_status()
    print("Organizational theme deployed successfully.")
```

---

## 6. Access Provisioning as Configuration

### 6.1 IdP Group Configuration as Code

Access to BI tools is declared in config and applied via SCIM/IdP automation — not manually in the BI tool UI.

```yaml
# iam/bi_groups.yaml
# Defines all IdP groups and their BI tool role mappings
# Managed by the BI COE; any change triggers a PR review

groups:
  - group_id: "bi-viewer-all"
    display_name: "BI - Viewer - All Employees"
    description: "Default viewer access for all employees; T1 reports only"
    tool_mappings:
      - tool: power_bi
        role: viewer
        workspaces: ["Finance - Production", "Sales - Production", "HR - Production"]
      - tool: tableau
        site_role: Viewer
        projects: ["[INTERNAL] All - T1 Certified"]

  - group_id: "bi-creator-finance"
    display_name: "BI - Creator - Finance"
    description: "Finance team power users; T3 self-service and T2 domain building"
    tool_mappings:
      - tool: power_bi
        role: member
        workspaces: ["Finance - Production", "Finance - Development", "Certified Datasets"]
      - tool: tableau
        site_role: Creator
        projects: ["[CONFIDENTIAL] Finance - T1", "[INTERNAL] Finance - T2", "T3-Self-Service"]

  - group_id: "bi-coe"
    display_name: "BI - COE"
    description: "BI Center of Excellence team; full platform access"
    tool_mappings:
      - tool: power_bi
        role: admin
        workspaces: ["ALL"]
      - tool: tableau
        site_role: SiteAdministratorCreator
        projects: ["ALL"]
      - tool: alteryx
        role: curator
        collections: ["ALL"]
```

```python
# sync_bi_access.py
"""
Syncs IdP group → BI tool role mapping from config.
Runs as part of nightly automation and on config change.
"""

import yaml
from pathlib import Path

def load_group_config(config_path: str) -> list[dict]:
    with open(config_path) as f:
        return yaml.safe_load(f)["groups"]

def sync_powerbi_workspace_access(
    group_config: list[dict],
    pbi_client,   # initialized Power BI API client
) -> None:
    """Apply workspace role assignments from config to Power BI."""
    for group in group_config:
        for mapping in group.get("tool_mappings", []):
            if mapping["tool"] != "power_bi":
                continue
            for workspace_name in mapping["workspaces"]:
                if workspace_name == "ALL":
                    # Apply to all workspaces — use with caution (COE only)
                    continue
                pbi_client.add_group_to_workspace(
                    workspace_name=workspace_name,
                    group_id=group["group_id"],
                    role=mapping["role"]
                )
```

---

## 7. Monitoring & Alert Configuration

### 7.1 Alert Configuration as Code

```yaml
# monitoring/bi_alerts.yaml
alerts:
  - name: "BI Warehouse Budget Alert"
    type: snowflake_resource_monitor
    warehouse: "BI_PROD_WH"
    monthly_credit_quota: 500
    triggers:
      - threshold_pct: 75
        action: notify
        notify:
          - type: email
            to: ["bi-platform@company.com"]
          - type: slack
            channel: "#data-platform-alerts"
      - threshold_pct: 90
        action: notify
        notify:
          - type: pagerduty
            severity: warning
      - threshold_pct: 100
        action: suspend_warehouse

  - name: "Stale Content Weekly Scan"
    type: custom_script
    schedule: "0 9 * * 1"     # Monday 9 AM
    script: "scripts/stale_content_scan.py"
    parameters:
      days_threshold: 60        # Warn at 60 days
      archive_threshold: 90
    notify_on_findings:
      - type: slack
        channel: "#bi-governance"
      - type: email
        to: ["bi-coe@company.com"]

  - name: "Refresh Failure Alert"
    type: power_bi_service_hook
    event: "DatasetRefreshFailed"
    workspaces: ["Finance - Production", "Sales - Production", "HR - Production"]
    notify:
      - type: pagerduty
        severity: high
      - type: email
        to: ["bi-platform@company.com", "data-engineering@company.com"]

  - name: "Unauthorized Data Source Detected"
    type: custom_script
    schedule: "0 6 * * *"     # Daily 6 AM
    script: "scripts/datasource_compliance_check.py"
    notify_on_findings:
      - type: pagerduty
        severity: critical
      - type: slack
        channel: "#data-alerts-prod"
```

### 7.2 Refresh SLA Monitoring

```python
# refresh_sla_monitor.py
"""
Monitors Power BI dataset refresh completion against SLA.
Alerts if refresh has not completed by the defined SLA time.
"""

import requests
from datetime import datetime, timezone
from dateutil import parser as dateparser

def check_refresh_sla(
    dataset_id: str,
    sla_utc_hour: int,
    sla_utc_minute: int,
    token: str,
    slack_webhook: str
) -> None:
    """Check if a dataset has refreshed by its SLA time. Alert if not."""
    now = datetime.now(timezone.utc)
    sla_time = now.replace(hour=sla_utc_hour, minute=sla_utc_minute, second=0)

    if now < sla_time:
        return  # SLA not due yet

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes?$top=1",
        headers=headers
    )
    refreshes = resp.json().get("value", [])
    if not refreshes:
        _send_alert(slack_webhook, dataset_id, "No refresh history found")
        return

    last_refresh = refreshes[0]
    last_end = dateparser.parse(last_refresh.get("endTime", "1900-01-01"))
    status = last_refresh.get("status", "Unknown")

    if last_end.date() < now.date() or status != "Completed":
        _send_alert(
            slack_webhook, dataset_id,
            f"SLA breached. Last refresh: {last_end.isoformat()} | Status: {status}"
        )

def _send_alert(webhook: str, dataset_id: str, message: str) -> None:
    import requests as r
    r.post(webhook, json={
        "text": f"🚨 *BI Refresh SLA Breach*\nDataset: `{dataset_id}`\n{message}"
    })
```

---

## 8. Change Classification Reference

Quick reference for the BI COE team and IT Change Managers:

| Change | Tier | Approver(s) | Lead Time | CAB |
|---|---|---|---|---|
| T3 self-service report — create or update | Self-service | Creator | Immediate | No |
| T2 domain report — logic update | Standard | Domain BI Lead peer review | Same day | No |
| T2 domain report — new publication | Standard | Domain BI Lead + BI COE | 3–5 days | No |
| T1 certified report — content update | Minor | BI COE Lead + domain owner | 5 days | No |
| T1 certified report — new publication | Minor | BI COE Lead + domain owner | 5–10 days | No |
| Certified dataset — additive column | Minor | BI COE + DE Lead | 5 days | No |
| Certified dataset — RLS rule change | Minor | BI COE + Data Governance | 5 days | No |
| Data classification label change | Minor | BI COE + Data Governance | 5 days | No |
| Refresh schedule change | Minor | BI COE + Domain owner | 3 days | No |
| Brand theme update (minor) | Minor | BI COE Lead | 5 days | No |
| Brand theme update (major rebrand) | Major | CDO + Communications + IT + CAB | 15+ days | Yes |
| Workspace restructure | Minor | BI COE + IT | 5–10 days | No |
| IdP group / access model change | Major | BI COE + IT + InfoSec + CAB | 10–15 days | Yes |
| SSO reconfiguration | Major | BI COE + IT + InfoSec + CAB | 10–15 days | Yes |
| Sensitivity label policy change | Major | Data Governance + IT + CAB | 10–15 days | Yes |
| External sharing enablement | Major | CDO + Legal + Privacy + CAB | 15+ days | Yes |
| BI tool version upgrade | Major | BI COE + IT + CAB | 10–15 days | Yes |
| New BI tool addition | Major | CDO + IT + Procurement + CAB | 30+ days | Yes |
| Emergency fix (refresh failure, data error in T1) | Emergency | BI COE Lead (verbal) + retrospective ticket | Immediate | Retrospective |

---

*This document is maintained by the BI Center of Excellence and reviewed jointly with IT Change Management on a quarterly basis. Changes to the change tier table require joint approval from the BI COE Lead and IT Change Management.*
