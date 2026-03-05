# Business Intelligence Best Practices
## Tableau | Power BI | Alteryx | Self-Service Analytics

**Document Owner:** Chief Data Office  
**Domain:** Business Intelligence  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Guiding Philosophy & BI Operating Model](#1-guiding-philosophy--bi-operating-model)
2. [Self-Service Analytics Governance](#2-self-service-analytics-governance)
3. [Authentication & Identity Standards](#3-authentication--identity-standards)
4. [Data Access Controls — Row & Column Level Security](#4-data-access-controls--row--column-level-security)
5. [Visualization Best Practices](#5-visualization-best-practices)
6. [Organizational Branding Standards](#6-organizational-branding-standards)
7. [Report & Dashboard Governance](#7-report--dashboard-governance)
8. [Compute & Server Cost Management](#8-compute--server-cost-management)
9. [Tool-Specific Standards — Tableau](#9-tool-specific-standards--tableau)
10. [Tool-Specific Standards — Power BI](#10-tool-specific-standards--power-bi)
11. [Tool-Specific Standards — Alteryx](#11-tool-specific-standards--alteryx)
12. [Data Minimization & Need-to-Know Principle](#12-data-minimization--need-to-know-principle)
13. [Regulated Environment Controls](#13-regulated-environment-controls)
14. [Incident & Breach Considerations for BI](#14-incident--breach-considerations-for-bi)

---

## 1. Guiding Philosophy & BI Operating Model

### 1.1 Mission

> The BI program exists to deliver **trusted, governed, performant** analytics to every business consumer — through consistent visualization standards, controlled self-service, and centralized semantic governance — without creating unsustainable operational burden on IT or data engineering teams.

### 1.2 The Self-Service Paradox

Uncontrolled self-service analytics is one of the most common and costly failures in enterprise data programs. The pattern is predictable:

```
Phase 1 — "We want self-service"
    ↓
Phase 2 — No governance defined; anyone can publish anything
    ↓
Phase 3 — Hundreds of conflicting reports; no one knows which is "right"
    ↓
Phase 4 — IT flooded with support requests; compute costs spike
    ↓
Phase 5 — CDO mandates a crackdown; users lose trust in data
    ↓
Phase 6 — Back to IT-controlled reporting, worse than Phase 1
```

This document breaks that cycle by defining **governed self-service** — structured autonomy within clear boundaries.

### 1.3 Federated BI Operating Model

```
┌──────────────────────────────────────────────────────────────────┐
│  CENTRAL BI COE (Center of Excellence)                          │
│  Owns: Semantic layer, certified datasets, branding standards,   │
│  platform governance, access policy, server management           │
└───────────────────────────┬──────────────────────────────────────┘
                            │ provides governed data products
                            │ (certified datasets, semantic models)
              ┌─────────────┴──────────────┐
              │                            │
┌─────────────▼──────────┐   ┌────────────▼────────────┐
│  DOMAIN BI LEADS        │   │  SELF-SERVICE CONSUMERS  │
│  (Finance, Sales, HR)   │   │  (Business analysts,     │
│  Build governed domain  │   │  power users)            │
│  dashboards from        │   │  Explore and build from  │
│  certified datasets     │   │  approved certified       │
│  only                   │   │  datasets only            │
└─────────────────────────┘   └──────────────────────────┘
```

### 1.4 BI Governance Tiers

| Tier | Content Type | Publisher | Data Source Allowed | Audience |
|---|---|---|---|---|
| **T1 — Certified** | Executive dashboards, regulatory reports | BI COE | Semantic layer / Gold only | Org-wide |
| **T2 — Governed** | Domain operational dashboards | Domain BI Lead | Certified datasets only | Domain + leadership |
| **T3 — Self-Service** | Ad hoc analysis, exploration | Power users | Certified datasets only | Individual / team |
| **T4 — Sandbox** | Exploratory, unpublished | Any analyst | Any approved source | Creator only |

**Rule:** T1 and T2 content is **published and maintained** by named owners. T3 content is time-limited (90 days) and auto-archived if not promoted. T4 content never leaves the sandbox workspace.

---

## 2. Self-Service Analytics Governance

### 2.1 The IT Load Problem — Defined

When self-service analytics lacks governance, IT and data engineering teams absorb the consequences:

| Ungoverned Behavior | IT/DE Impact |
|---|---|
| Users connect directly to production databases | Unplanned query load; performance degradation for operational systems |
| Users duplicate reports with slightly different logic | Support tickets for "why are my numbers different?" |
| Users extract data to Excel / local files | Data governance gap; PII in unmanaged environments |
| Users create live connections to large tables | Warehouse/server cost spikes; cluster timeouts |
| Users share reports externally without approval | Data leak risk; regulatory violation |
| Abandoned reports continue to run on schedule | Ghost compute consumption; server degradation |

### 2.2 Governed Self-Service Policy Summary

| Policy | Rule |
|---|---|
| **Approved data sources only** | Users may only connect to certified datasets or semantic layer objects. Direct database connections require written approval from the BI COE and the Data Engineering Lead. |
| **No direct production DB connections** | No BI tool may connect directly to source system databases (ERP, CRM, etc.) in production. |
| **No personal data extracts** | Extracts to local files (CSV, Excel) require manager approval and are logged. PII extracts are prohibited without the Privacy Officer's written sign-off. |
| **Content ownership required** | Every published report must have a named owner. Reports without a valid owner are archived within 30 days. |
| **No duplicate key metrics** | Revenue, headcount, churn, and other certified KPIs may only be defined in the semantic layer. Reports may not redefine these metrics locally. |
| **90-day self-service lifespan** | T3 self-service reports auto-archive if not viewed in 90 days or not promoted to T2. |
| **External sharing prohibited by default** | Content may not be shared outside the organization without the Data Governance Lead's approval and a logged exception. |

### 2.3 Approved Data Source Registry

All BI tool data sources must be registered in the **Approved Data Source Registry** before use in any published content:

```yaml
# approved_data_source_registry.yaml
# Managed by BI COE; version-controlled

data_sources:
  - id: "DS-001"
    name: "Finance Semantic Model"
    platform: power_bi          # power_bi | tableau | alteryx
    type: certified_dataset     # certified_dataset | live_connection | import
    underlying_source: "PROD_FINANCE_GOLD.finance (Snowflake)"
    owner: "BI COE - Finance"
    classification: CONFIDENTIAL
    pii_contains: false
    row_level_security: true
    approved_audiences:
      - "Finance Team"
      - "FP&A"
      - "Executive Leadership"
    approved_date: "2024-01-15"
    next_review_date: "2025-01-15"
    status: active

  - id: "DS-002"
    name: "Sales Performance Dataset"
    platform: tableau
    type: certified_dataset
    underlying_source: "PROD_SALES_GOLD.sales (Snowflake)"
    owner: "BI COE - Sales"
    classification: INTERNAL
    pii_contains: false
    row_level_security: true
    approved_audiences:
      - "Sales Team"
      - "Revenue Operations"
      - "Executive Leadership"
    approved_date: "2024-01-15"
    next_review_date: "2025-01-15"
    status: active
```

---

## 3. Authentication & Identity Standards

### 3.1 Universal Authentication Rules

| Rule | Standard |
|---|---|
| **SSO required** | All BI tools must authenticate exclusively via corporate SSO (Okta / Azure AD / Entra ID). Username/password login must be disabled. |
| **MFA enforced** | Multi-factor authentication is mandatory for all users of all BI platforms. |
| **No shared accounts** | Every user has an individual named account. Shared "department" accounts are prohibited. |
| **Service accounts for automation** | Scheduled refreshes and automated workflows use service accounts, not personal accounts. Service accounts are not interactive. |
| **Guest/external users** | Require explicit approval from the Data Governance Lead. Time-limited (max 90 days). Access scoped to specific reports only — never the underlying data source. |
| **Session timeout** | All BI platform sessions timeout after 8 hours of inactivity (or per tool capability). |

### 3.2 Tableau Authentication

```
Authentication Flow:
  User → Tableau Server / Cloud → SAML 2.0 → Okta/Azure AD → MFA → Tableau
  
Required Configuration:
  - SAML configured with IdP-initiated and SP-initiated sign-on
  - Local authentication disabled in Tableau Server settings
  - SCIM provisioning enabled for automated user lifecycle management
  - Group membership in IdP maps directly to Tableau site roles (see below)
```

**Tableau Site Role Mapping:**

| IdP Group | Tableau Site Role | Capability |
|---|---|---|
| `bi-viewer` | Viewer | View and interact with published content only |
| `bi-explorer` | Explorer | View, interact, and create limited content from certified sources |
| `bi-creator` | Creator | Full authoring; Desktop license; publish to governed workspaces |
| `bi-site-admin` | Site Administrator Creator | Site configuration; managed by BI COE only |

### 3.3 Power BI Authentication

```
Authentication Flow:
  User → Power BI Service → Azure AD / Entra ID → MFA → Power BI
  
Required Configuration:
  - Tenant-level: "Allow service principals to use Power BI APIs" → Controlled via security group
  - Disable: "Allow users to sign up for Power BI individually" (prevent shadow IT)
  - Disable: "External guest user access" at tenant level (enable only via approval process)
  - Enable: "Azure AD Conditional Access" for Power BI service
  - Enable: "Block download of reports" for RESTRICTED classification data
```

**Power BI License & Role Mapping:**

| User Type | License | Workspace Role | Capability |
|---|---|---|---|
| Executive / occasional viewer | Power BI Free (in Premium capacity) | Viewer | View certified content only |
| Business analyst | Power BI Pro | Member | View, interact, build from certified datasets |
| Power user / domain BI lead | Power BI Pro | Contributor | Build and publish to governed workspaces |
| BI COE | Power BI Premium Per User | Admin | Full platform administration |

### 3.4 Alteryx Authentication

```
Authentication Flow:
  User → Alteryx Server → SAML 2.0 → Okta/Azure AD → MFA → Alteryx
  
Required Configuration:
  - Windows Authentication disabled; SAML required
  - SCIM integration for user provisioning
  - Gallery access controlled by role (Artisan vs. Viewer)
  - All scheduled workflows run under service account credentials only
```

**Alteryx Role Mapping:**

| IdP Group | Alteryx Role | Capability |
|---|---|---|
| `alteryx-viewer` | Viewer | Run published apps and workflows |
| `alteryx-member` | Member | Run, upload, and share workflows within collections |
| `alteryx-artisan` | Artisan | Full workflow design and publishing |
| `alteryx-curator` | Curator | Collection management |
| `alteryx-admin` | Server Admin | Platform administration (BI COE only) |

### 3.5 Access Provisioning Process

No user receives BI tool access without following this process:

```
1. Manager submits access request in ITSM tool (ServiceNow / Jira)
   └── Specifies: user, tool, role, business justification, data scope needed

2. BI COE reviews request
   └── Verifies business justification
   └── Confirms role is appropriate (least privilege)
   └── Confirms data classification is appropriate for requester

3. Data Governance Lead approves (for CONFIDENTIAL or RESTRICTED data access)

4. Access provisioned via IdP group membership (not directly in BI tool)
   └── All provisioning is IdP-driven; direct tool provisioning is not allowed

5. Access logged in Access Register with timestamp and approver

6. User notified with onboarding resources

7. Quarterly access review — manager re-certifies all direct reports' access
```

---

## 4. Data Access Controls — Row & Column Level Security

### 4.1 Principle: Least-Privilege Data Access

> **Users see only the data they need to perform their role.** This applies to rows (business unit, geography, customer segment) and columns (PII fields, financial details, compensation data).

This is not just a security principle — it also directly reduces compute cost. Smaller, scoped datasets run faster, use less memory, and put less pressure on underlying infrastructure.

### 4.2 Row-Level Security (RLS)

RLS must be implemented at the **semantic layer or certified dataset level** — not per individual report. This ensures the rule travels with the data product regardless of how it is consumed.

#### Snowflake Row Access Policies (Source-Level RLS)

```sql
-- Row access policy: users see only rows for their assigned region
CREATE ROW ACCESS POLICY governance.policies.rls_by_region
AS (region_code VARCHAR) RETURNS BOOLEAN ->
    EXISTS (
        SELECT 1
        FROM governance.access_maps.user_region_access ura
        WHERE ura.username = CURRENT_USER()
          AND ura.region_code = region_code
    );

-- Apply to the Gold table that BI tools query
ALTER TABLE prod_sales_gold.sales.fact_revenue
    ADD ROW ACCESS POLICY governance.policies.rls_by_region
    ON (region_code);
```

#### Power BI Row-Level Security

```
RLS Implementation Pattern (Power BI):
  1. Define RLS roles in Power BI Desktop on the certified dataset
  2. Publish dataset to workspace
  3. Assign users/groups to RLS roles in Power BI Service (not Desktop)
  4. Test as different roles before publishing

DAX filter example — Sales RLS by region:
  [region_code] = LOOKUPVALUE(
      UserRegionMapping[region_code],
      UserRegionMapping[email],
      USERPRINCIPALNAME()
  )
```

#### Tableau Row-Level Security

```
RLS Implementation Pattern (Tableau):
  1. User filter via ISMEMBEROF() or USERNAME() — applied at data source level
  2. OR: use entitlement table joined to data source (preferred for large teams)

Entitlement table approach (preferred):
  - Maintain user_access_entitlements table in Snowflake
  - Join to dataset in published data source
  - USERNAME() function passes Tableau authenticated user to the filter
  - Entitlement table managed by BI COE; updated via IdP SCIM

Calculated field example:
  [Region] = IF ISMEMBEROF("Sales-APAC") THEN "APAC"
             ELSEIF ISMEMBEROF("Sales-EMEA") THEN "EMEA"
             ELSE "ALL" END
```

### 4.3 Column-Level Security (CLS)

#### Rules for Column Restriction

| Column Sensitivity | Who Can View | Implementation |
|---|---|---|
| PII (name, email, SSN, DOB) | Named individuals with privacy training completion | Snowflake dynamic masking + CLS in semantic layer |
| Compensation / salary | HR leadership + named approvers only | Separate certified dataset; not in general HR dataset |
| Financial results (pre-close) | Finance leadership + named FP&A only | Time-gated access policy; locked until close date |
| M&A / Deal information | Executive + named deal team only | Separate isolated workspace; no general BI access |
| Clinical / health data | Named clinical roles + HIPAA-trained users | Separate workspace; BAA required; audit every access |

#### Power BI Column Restriction via Object-Level Security (OLS)

```
OLS Implementation:
  1. Create RLS role in Power BI Desktop
  2. Define table/column OLS rules (restrict columns per role)
  3. Publish to service; assign users to roles
  4. Users in restricted role see column as blank or [Restricted]

Note: OLS is additive with RLS — both can apply simultaneously.
```

#### Snowflake Dynamic Data Masking (enforced at source)

```sql
-- Masking policy — SSN visible only to HR_RESTRICTED role
CREATE MASKING POLICY governance.policies.mask_ssn
AS (val VARCHAR) RETURNS VARCHAR ->
    CASE
        WHEN IS_ROLE_IN_SESSION('HR_RESTRICTED_ROLE') THEN val
        WHEN IS_ROLE_IN_SESSION('HR_ANALYST_ROLE') THEN '***-**-' || RIGHT(val, 4)
        ELSE '***-**-****'
    END;

ALTER TABLE prod_hr_gold.hr.dim_employee
    MODIFY COLUMN ssn
    SET MASKING POLICY governance.policies.mask_ssn;
```

### 4.4 Data Minimization in BI Tools

**Rule: Only include the columns you need in every report/dataset.**

This is enforced through:

1. **Certified dataset design:** BI COE builds certified datasets with only the columns appropriate for the target audience. PII columns are excluded by default; included only in restricted variants.

2. **Report review checklist:** Before T1/T2 publication, the BI lead confirms every column in the report has a named business purpose.

3. **Live connection preferred over import:** Import mode copies data into BI tool memory — creating an uncontrolled data copy. Live connections (DirectQuery / Live Connection) leave data in the governed platform.

```
Connection Mode Priority:
  1. Live Connection to semantic model (Power BI) / published data source (Tableau)
  2. DirectQuery to Snowflake/Databricks Gold layer (when live connection insufficient)
  3. Import mode — requires BI COE approval + data classification review
  4. Manual data entry / local files — PROHIBITED for any shared or published content
```

---

## 5. Visualization Best Practices

### 5.1 Core Principles

| Principle | Practice |
|---|---|
| **Tell the story, not the data** | Every visualization answers a specific question. If you can't state the question, the visualization shouldn't exist. |
| **Context before detail** | Lead with the headline KPI; provide drill paths to detail — don't start with detail. |
| **Fewer, better** | A dashboard with 8 focused visuals outperforms one with 25 cluttered ones. |
| **Color has meaning** | Color communicates status, category, or magnitude — never decoration. |
| **Labels over legends** | Direct labels on data points are faster to read than legends requiring lookup. |
| **Consistent scales** | Never change axis scales between versions of the same report without prominent notation. |
| **Accessibility first** | Every visualization must be readable by users with color vision deficiencies. |

### 5.2 Chart Selection Guide

| Question Type | Recommended Chart | Avoid |
|---|---|---|
| How much? (single value) | KPI card / big number | Pie chart |
| How does X compare to Y? | Bar chart (horizontal for long labels) | 3D charts |
| How has X changed over time? | Line chart | Area chart (unless showing composition) |
| What is the distribution? | Histogram / box plot | Pie chart |
| What is the composition? | Stacked bar / treemap | 3D pie |
| What is the relationship? | Scatter plot | Bubble chart with >4 variables |
| Where is it? | Map / filled map | Map for non-geographic data |
| How does X rank? | Sorted bar chart | Word cloud |
| How close to a target? | Bullet chart / progress bar | Gauge |

### 5.3 Dashboard Layout Standards

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Logo | Report Title | Date Range | Last Refreshed  │ ← Always present
├──────────────┬──────────────┬──────────────┬────────────────┤
│  KPI Card 1  │  KPI Card 2  │  KPI Card 3  │  KPI Card 4    │ ← Top-row KPIs
├──────────────┴──────────────┴──────────────┴────────────────┤
│                                                              │
│       PRIMARY VISUALIZATION (60% of canvas height)          │ ← Main story
│                                                              │
├────────────────────────────┬────────────────────────────────┤
│  SUPPORTING VIZ 1          │  SUPPORTING VIZ 2              │ ← Supporting context
└────────────────────────────┴────────────────────────────────┘
│  FOOTER: Data Source | Classification Label | Owner | Help  │ ← Always present
└─────────────────────────────────────────────────────────────┘
```

**Layout Rules:**
- Filters always on the left or top — never floating
- Navigation elements consistent across all pages of a multi-page report
- Data classification label always visible (required for regulated environments)
- "Last refreshed" timestamp always visible — users must know data freshness
- Help / contact link always present — reduces support ticket volume

### 5.4 Color Standards

- **Status colors:** Red = alert/negative, Amber = warning/caution, Green = positive/on-track. Never reverse these.
- **Categorical palettes:** Maximum 7 categories per visualization. Beyond 7, use "Other" grouping.
- **Sequential palettes:** Single hue, light-to-dark for magnitude.
- **Diverging palettes:** For data with a meaningful midpoint (e.g., variance to plan: red → white → green).
- **Accessibility:** All color combinations must pass WCAG AA contrast ratio (4.5:1 minimum). Never rely on color alone — use shape or label as secondary encoding.

### 5.5 KPI Definition Standards

**Rule: KPIs shown in BI tools must be defined in the semantic layer. No local KPI definitions.**

Every displayed KPI must have:
- Business name (e.g., "Net Revenue")
- Plain-English definition (e.g., "Gross revenue minus returns, discounts, and allowances, in USD")
- Calculation source (e.g., "dbt metric: `net_revenue` in `finance_metrics.yml`")
- Owner (e.g., "Finance — Controller's office")
- Last validated date

These are published in the data catalog and linked from every report tooltip.

---

## 6. Organizational Branding Standards

### 6.1 Why Automated Branding Matters

Inconsistent visual presentation:
- Erodes trust in data (reports that look unofficial are treated as unofficial)
- Creates accessibility failures
- Violates corporate communication standards in regulated industries
- Increases per-report design time unnecessarily

The solution is **template-enforced branding** — engineers and analysts build in pre-styled templates; branding is not optional.

### 6.2 Brand Component Registry

| Component | Standard | Tool-Specific Implementation |
|---|---|---|
| Primary font | Corporate approved (e.g., Inter, Calibri) | Embedded in all templates |
| Primary color | `#[Hex]` (from brand guide) | Defined in theme files |
| Secondary palette | 6-color approved palette | Theme file |
| Logo | Official SVG only | Pre-placed in all templates; locked |
| Header style | Defined in template | Locked layer in Tableau; header in PBI |
| Footer style | Defined in template | Locked layer; auto-populated |
| Classification watermark | Auto-applied by data classification | Policy-driven (see §13) |

### 6.3 Tableau — Enforcing Branding via Templates

```
Implementation:
  1. BI COE creates and maintains a Tableau Workbook Template (.twbx)
     - Pre-loaded with brand color palette
     - Logo locked as image in header layout container
     - Font definitions baked into all text objects
     - Footer with data source, classification, owner fields pre-templated
     - Hosted on Tableau Server in a locked "BI Templates" project

  2. All T1 and T2 workbook development MUST start from the template
     (enforced via deployment checklist, not technically lockable in Tableau)

  3. Theme file (.twb XML) extracted and stored in Git
     — any change to brand standards triggers a PR review

  4. Automated check in PR pipeline:
     — Python script reads .twb XML and validates font, color values match brand spec
```

```python
# tableau_brand_validator.py
import xml.etree.ElementTree as ET

APPROVED_FONTS = {"Inter", "Calibri", "Arial"}
APPROVED_PRIMARY_COLOR = "#1A3A5C"
BRAND_PALETTE = {
    "#1A3A5C", "#2E6DA4", "#4A90D9", "#F5A623", "#D0021B", "#7ED321"
}

def validate_tableau_workbook(twb_path: str) -> list[str]:
    """Validate Tableau workbook against brand standards. Returns list of violations."""
    tree = ET.parse(twb_path)
    root = tree.getroot()
    violations = []

    # Check fonts
    for style in root.iter("style-rule"):
        for format_elem in style.iter("format"):
            font = format_elem.get("font-family", "")
            if font and font not in APPROVED_FONTS:
                violations.append(f"Non-approved font: '{font}'")

    # Check colors
    for color_elem in root.iter("color"):
        hex_val = color_elem.get("value", "")
        if hex_val and hex_val.upper() not in {c.upper() for c in BRAND_PALETTE}:
            violations.append(f"Non-brand color: '{hex_val}'")

    return violations
```

### 6.4 Power BI — Enforcing Branding via JSON Theme

```json
{
  "name": "Corporate Brand Theme v2.1",
  "dataColors": [
    "#1A3A5C", "#2E6DA4", "#4A90D9", "#F5A623", "#D0021B", "#7ED321"
  ],
  "background": "#FFFFFF",
  "foreground": "#1A1A1A",
  "tableAccent": "#2E6DA4",
  "visualStyles": {
    "*": {
      "*": {
        "fontFamily": [{"value": "Calibri"}],
        "fontSize": [{"value": 11}],
        "labelColor": [{"value": {"solid": {"color": "#1A1A1A"}}}]
      }
    },
    "title": {
      "*": {
        "fontFamily": [{"value": "Calibri"}],
        "fontSize": [{"value": 14}],
        "fontBold": [{"value": true}],
        "fontColor": [{"value": {"solid": {"color": "#1A3A5C"}}}]
      }
    }
  }
}
```

**Deployment approach:**
- Theme JSON is version-controlled in Git
- Deployed to Power BI via Admin API or organizational theme setting
- All workspaces in the tenant have the theme applied as **organizational default**
- Report authors may not override the organizational theme for T1/T2 content

### 6.5 Alteryx — Report Branding

For Alteryx-generated output reports (PDF, Excel, HTML):
- Use the approved Report Tool template with corporate header/footer
- Template stored in Alteryx Server gallery under "BI COE Templates" collection
- All client-facing output uses the approved Reporting macro from the gallery

---

## 7. Report & Dashboard Governance

### 7.1 Report Inventory & Ownership

Every published report must be registered in the **Report Registry**:

```yaml
# report_registry entry
report:
  id: "RPT-2024-047"
  name: "Monthly Revenue Performance"
  tier: T1                        # T1 | T2 | T3
  tool: power_bi                  # power_bi | tableau | alteryx
  workspace: "Finance - Executive"
  url: "https://app.powerbi.com/..."
  owner:
    name: "Finance BI Lead"
    email: "finance-bi@company.com"
    team: "Finance"
  data_sources:
    - "DS-001: Finance Semantic Model"
  classification: CONFIDENTIAL
  audience:
    - "Finance Team"
    - "Executive Leadership"
  schedule: "Refreshes daily at 5:00 AM UTC"
  sla_freshness: "Available by 6:00 AM UTC"
  last_reviewed: "2024-01-15"
  next_review: "2024-07-15"       # Reviewed every 6 months for T1
  certified: true
  certification_date: "2024-01-15"
  certification_by: "BI COE Lead"
  active: true
```

### 7.2 Report Lifecycle

```
DRAFT → REVIEW → CERTIFIED → PUBLISHED → [REVIEW CYCLE] → DEPRECATED → ARCHIVED

DRAFT:      Developer building in sandbox workspace
REVIEW:     BI COE quality review (brand, accuracy, data source, security)
CERTIFIED:  BI COE sign-off; added to Report Registry
PUBLISHED:  Live in production workspace; accessible to defined audience
DEPRECATED: Superseded by newer version; redirects to replacement
ARCHIVED:   No longer accessible; metadata retained in registry for 3 years
```

### 7.3 Anti-Duplication Policy

**Rule: No two certified (T1/T2) reports may define the same primary business metric differently.**

Before certifying any new report:
1. BI COE searches the Report Registry for existing reports covering the same metric.
2. If a report already exists: the new report must reuse the same certified dataset and metric definition — not create a new one.
3. If the existing report is inadequate: a formal **report replacement request** is submitted; the existing report is deprecated upon certification of the replacement.
4. All organization-level KPIs are documented in the **Metric Catalog** (maintained by BI COE in the data catalog).

**Why this matters:**
- Two reports showing different "Revenue" numbers destroy user trust
- Duplicate reports double the compute cost for no analytical value
- IT spends disproportionate time resolving reconciliation disputes

### 7.4 Report Review Checklist (Pre-Publication)

```
□ Data source is an approved certified dataset (not a direct DB connection)
□ Report built from the brand template
□ Data classification label visible on every page
□ "Last Refreshed" timestamp visible
□ Owner name and contact present in footer
□ All KPIs defined in the semantic layer (no local calculated measures for certified metrics)
□ Row-level security applied and tested as a non-privileged user
□ Column-level restrictions verified — no PII visible to general audience
□ No sensitive data in report title, description, or filter labels
□ Mobile layout tested (for T1 reports)
□ Accessibility check passed (color contrast, alt-text on images)
□ Performance tested — page load < 5 seconds on standard connection
□ Registered in Report Registry
□ Prior version deprecated (if replacement)
```

---

## 8. Compute & Server Cost Management

### 8.1 The Cost Problem in Unmanaged BI

| Behavior | Cost Impact |
|---|---|
| Live DirectQuery on unoptimized large tables | Snowflake/Databricks credit burn per query |
| Import mode scheduled refresh on 50M row dataset | Memory + processing cost on Premium capacity |
| 200 users opening same large dashboard simultaneously | Query fan-out multiplies warehouse cost |
| Abandoned scheduled reports refreshing at 5-minute intervals | Continuous compute waste |
| Alteryx workflows joining large tables without filters | Cluster overload; delays for other users |
| Duplicate reports refreshing the same underlying data | 2–10x unnecessary query volume |

### 8.2 Query Performance Standards

| Metric | Standard | Action if Breached |
|---|---|---|
| Dashboard initial load | < 5 seconds | Performance review required before T1 certification |
| DirectQuery response | < 10 seconds | Escalate to DE for query optimization or materialized view |
| Scheduled refresh duration | < 30 minutes | Review model design; consider aggregation tables |
| Alteryx workflow runtime | < 2 hours | Break into modular workflows; optimize joins |
| Report page render | < 3 seconds | Reduce visual count; use aggregations |

### 8.3 Snowflake Cost Controls for BI Workloads

```sql
-- Dedicated BI warehouse with resource monitor
CREATE WAREHOUSE BI_PROD_WH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    MAX_CLUSTER_COUNT = 5
    SCALING_POLICY = 'ECONOMY'
    COMMENT = 'Dedicated BI tool warehouse. Do not use for ELT jobs.';

-- Resource monitor — alert at 75%, suspend at 100%
CREATE RESOURCE MONITOR bi_monthly_monitor
    WITH CREDIT_QUOTA = 500           -- Adjust to actual monthly allocation
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE BI_PROD_WH SET RESOURCE_MONITOR = bi_monthly_monitor;
```

### 8.4 Power BI Premium Capacity Management

```
Capacity Monitoring Best Practices:
  □ Enable Premium Capacity Metrics app
  □ Set memory thresholds: alert at 70% sustained; action at 85%
  □ Identify top CPU-consuming datasets weekly
  □ Enforce large dataset storage format for datasets > 1GB
  □ Schedule heavy refreshes off-peak (overnight)
  □ Use incremental refresh for datasets with historical depth
  □ Paginated reports run on dedicated capacity nodes — monitor separately
```

### 8.5 Tableau Server Resource Management

```
Resource Recommendations:
  □ Background task concurrency: limit to (CPU cores / 2) for balance
  □ VizQL sessions: set max concurrent sessions per user (typically 4)
  □ Extract refresh concurrency: limit parallel refreshes in off-peak windows
  □ Data engine cache: monitor and tune; stale cache = wasted memory
  □ Unused views: auto-archive after 90 days of zero views
  □ Subscription emails: audit quarterly; remove for departed users
  □ Server-side rendering: use for embedding to reduce client load
```

### 8.6 Alteryx Server Resource Management

```
Resource Controls:
  □ Worker node concurrency: set max simultaneous workflows per worker
  □ Priority queuing: executive / business-critical workflows get P1 queue
  □ Memory limits per workflow: enforce via server configuration
  □ Long-running workflow policy: alert at 90 min; kill at 4 hours (unless exempted)
  □ Data connection pooling: use Alteryx Data Connection Manager to share connections
  □ Schedule consolidation: audit quarterly; eliminate redundant runs
```

---

## 9. Tool-Specific Standards — Tableau

### 9.1 Tableau Server/Cloud Architecture Standards

```
Environment Tier:
  Tableau Desktop (authoring) → Tableau Server Dev → Tableau Server Prod

Project Hierarchy:
  Site
  └── [Classification] Projects
        └── [Domain] Workbooks
              └── [Report Name] Views

Project permissions inherited from site; exceptions logged.
```

### 9.2 Published Data Source Requirements

All published data sources must:
- Live in the "Certified Data Sources" project (managed by BI COE)
- Have a named owner and description
- Have the certification badge applied by the BI COE
- Be the **only** data source used by T1/T2 workbooks — no ad hoc connections
- Embed credentials via service account only (no personal credential embedding)
- Use **Tableau Extract** or **Live Connection** to Snowflake — no direct ODBC to source systems

### 9.3 Performance: Tableau-Specific

```
Extract vs. Live Connection Decision:
  Use Live Connection when:
    - Data freshness < 4 hours required
    - Dataset < 10M rows after filtering
    - Snowflake or Databricks is the source (natively optimized)
  
  Use Extract when:
    - Data > 10M rows
    - Complex cross-database joins required
    - Offline viewing needed (field users)
    - Source system cannot handle BI query load

Extract Refresh Schedule:
  - Never more frequently than the source data refreshes
  - Stagger refresh times to avoid simultaneous warehouse hits
  - Large extracts (>5M rows): use incremental refresh + full weekly refresh
```

### 9.4 Tableau Governance via REST API

```python
# tableau_governance.py
# Automated governance tasks via Tableau REST API

import tableauserverclient as TSC

def get_stale_workbooks(
    server: TSC.Server,
    days_inactive: int = 90
) -> list[TSC.WorkbookItem]:
    """Return workbooks not viewed in N days — candidates for archival."""
    from datetime import datetime, timedelta, timezone

    cutoff = datetime.now(timezone.utc) - timedelta(days=days_inactive)
    all_workbooks, _ = server.workbooks.get()

    return [
        wb for wb in all_workbooks
        if wb.updated_at and wb.updated_at < cutoff
    ]

def audit_uncertified_datasources(server: TSC.Server) -> list[dict]:
    """Find data sources without certification — policy violation."""
    all_ds, _ = server.datasources.get()
    return [
        {"name": ds.name, "project": ds.project_name, "owner": ds.owner_id}
        for ds in all_ds
        if not ds.certified
    ]
```

---

## 10. Tool-Specific Standards — Power BI

### 10.1 Workspace Architecture

```
Tenant
├── Admin Workspace (BI COE internal — hidden from users)
├── Certified Datasets Workspace (read-only for consumers; write for BI COE)
├── [Domain] - Production Workspace   (T1/T2 content; managed by Domain BI Lead)
├── [Domain] - Development Workspace  (T3 content; creator-accessible)
└── Sandbox Workspace                 (T4; auto-cleaned every 30 days)
```

### 10.2 Dataflow & Dataset Standards

```
Data Architecture in Power BI:
  Snowflake/Databricks Gold layer
      └── Power BI Dataflow (shared, reusable data prep)
            └── Power BI Certified Dataset (single source of truth per domain)
                  └── Power BI Reports (many reports from one dataset)

Rules:
  - Never import data directly from Bronze or Silver layers into Power BI
  - Never create report-level calculated tables that duplicate Dataflow logic
  - Dataflows owned and managed by BI COE
  - One certified dataset per domain; reports connect to it — never create copies
```

### 10.3 DAX Standards

```dax
// Good: Measure with clear naming, explicit filter context, formatted
Net Revenue = 
CALCULATE(
    SUM( FactRevenue[gross_revenue] ) - SUM( FactRevenue[returns_amount] ),
    FactRevenue[is_voided] = FALSE
)

// Good: Time intelligence using date table
Revenue YTD = 
TOTALYTD( [Net Revenue], DimDate[date] )

// Bad: Hardcoded values in measures
// Revenue 2024 = CALCULATE( SUM(...), YEAR(date) = 2024 )  ← Never hardcode years

// Required: All measures have a description in the dataset
// Required: Measures organized in display folders by business area
// Required: Format string defined on every measure (currency, %, number)
```

### 10.4 Power BI Deployment Pipelines

```
Development Workspace → Test Workspace → Production Workspace
     (Dev stage)           (Test stage)      (Prod stage)

Rules:
  - All promotion via deployment pipeline (not manual publish)
  - Dataset rules applied at each stage (environment-specific data source bindings)
  - Pre-deployment: automated test report checks pass
  - Post-deployment: BI COE verifies data freshness and visual render
```

---

## 11. Tool-Specific Standards — Alteryx

### 11.1 Alteryx Usage Boundary

Alteryx is a **data preparation and analytics automation** tool — not a BI visualization tool. Its role in the data ecosystem is:

```
Alteryx IS appropriate for:
  ✅ Complex data blending from approved sources
  ✅ Statistical analysis, predictive modeling (business user)
  ✅ Automated report generation (PDF/Excel output)
  ✅ Data quality workflows feeding back to the data platform
  ✅ Self-service ETL for business users (with governance)

Alteryx is NOT appropriate for:
  ❌ Interactive dashboards (use Tableau or Power BI)
  ❌ Direct connections to production operational databases
  ❌ PII data processing without privacy review sign-off
  ❌ Workflows storing output to personal drives or unmanaged locations
  ❌ Replacing governed data engineering pipelines (Snowflake/Databricks)
```

### 11.2 Alteryx Workflow Standards

```
Every published Alteryx workflow must:
  □ Be stored in the Alteryx Server Gallery (not personal Desktop)
  □ Have a named owner and business description
  □ Use only approved data connections (from Data Connection Manager)
  □ Write output only to approved locations (Gold layer tables or approved file stores)
  □ Include a Comment tool at the start documenting: purpose, inputs, outputs, owner
  □ Use the Analytics Team macro library for common operations (not rebuild ad hoc)
  □ Pass the Alteryx Workflow Review checklist before production scheduling
```

### 11.3 Alteryx Data Connection Manager

All Alteryx data connections must be defined in the **Data Connection Manager (DCM)**:
- Credentials stored in DCM only — never embedded in workflows
- DCM connections authenticated via service account credentials
- No personal credentials in any shared or scheduled workflow
- Connections reviewed quarterly; unused connections removed

---

## 12. Data Minimization & Need-to-Know Principle

### 12.1 Policy Statement

> **Data in BI tools should be the minimum necessary to answer the business question.** Broad access to sensitive data "just in case" is not a valid business justification.

### 12.2 Implementation Checklist for Every Certified Dataset

```
□ Does this dataset include PII? If yes — documented justification required.
□ Are all PII columns masked for non-privileged users?
□ Are columns not needed by any current report excluded from the dataset?
□ Is the row scope filtered to only the rows relevant to the intended audience?
□ Is import mode used? If yes — data minimization review completed.
□ Has a data classification label been applied?
□ Is the dataset reviewed every 6 months for relevance?
```

### 12.3 Import Mode Data Minimization (Power BI)

When import mode is required, apply aggressive filtering:

```dax
// In Power Query (M language) — filter before import, not after
// BAD: Import 50M rows, filter in DAX
// GOOD: Filter in query folding at source

let
    Source = Snowflake.Databases("account.snowflakecomputing.com"),
    FactRevenue = Source{[Name="PROD_FINANCE_GOLD"]}[Data]
        {[Schema="finance"]}[Data]{[Name="fact_revenue"]}[Data],
    // Filter: only last 2 years of data needed for this report
    FilteredRows = Table.SelectRows(
        FactRevenue,
        each [transaction_date] >= Date.AddYears(DateTime.LocalNow(), -2)
    ),
    // Select only required columns — never SELECT *
    SelectedColumns = Table.SelectColumns(
        FilteredRows,
        {"revenue_key", "transaction_date", "gross_revenue",
         "net_revenue", "customer_key", "product_key", "region_code"}
    )
in
    SelectedColumns
```

---

## 13. Regulated Environment Controls

### 13.1 Classification Watermarking

In regulated environments (financial services, healthcare, government), all BI output must carry a **data classification watermark**. This applies to:
- Dashboards viewed in browser
- Exported PDFs
- Scheduled email subscriptions
- Embedded analytics in applications

**Implementation:**

| Tool | Classification Watermark Implementation |
|---|---|
| Power BI | Sensitivity labels (Microsoft Purview Information Protection) applied to datasets propagate to all reports and exports automatically |
| Tableau | Static text objects in footer layout container on every dashboard; script enforces presence via XML validation |
| Alteryx | Report tool header/footer template includes classification field, auto-populated from workflow metadata |

### 13.2 Microsoft Purview Integration (Power BI)

```
Configuration:
  1. Enable sensitivity labels in Power BI admin portal
  2. Define label taxonomy matching data classification policy:
     PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | TOP_SECRET
  3. Enable mandatory labeling — reports cannot be published without a label
  4. Configure label inheritance: dataset label propagates to all connected reports
  5. Configure protection actions:
     RESTRICTED: Encrypt exports; watermark PDFs; disable screenshot
     TOP_SECRET: Block export entirely; no download; audit every view
```

### 13.3 Export & Download Controls

| Classification | View in Browser | Export to PDF | Export to Excel | Download PBIX/TWB | Email Subscription |
|---|---|---|---|---|---|
| PUBLIC | ✅ | ✅ | ✅ | ✅ (BI COE only) | ✅ |
| INTERNAL | ✅ | ✅ | ✅ | ❌ | ✅ (internal only) |
| CONFIDENTIAL | ✅ | ✅ (watermarked) | ✅ (row-limited) | ❌ | Approval required |
| RESTRICTED | ✅ | ✅ (encrypted + watermarked) | ❌ | ❌ | ❌ |
| TOP_SECRET | ✅ (audit logged) | ❌ | ❌ | ❌ | ❌ |

### 13.4 Audit Logging Requirements

Every BI platform must emit audit logs capturing:

| Event | Tableau | Power BI | Alteryx |
|---|---|---|---|
| User login / logout | ✅ | ✅ | ✅ |
| Report/dashboard view | ✅ | ✅ | ✅ |
| Data source access | ✅ | ✅ | ✅ |
| Export / download | ✅ | ✅ | ✅ |
| Permission change | ✅ | ✅ | ✅ |
| Failed access attempt | ✅ | ✅ | ✅ |
| Scheduled refresh | ✅ | ✅ | ✅ |
| Workflow execution (Alteryx) | N/A | N/A | ✅ |

**Audit log retention:** Minimum 1 year online; 3 years archived. Exported to SIEM (Splunk, Sentinel) within 24 hours for regulated workloads.

### 13.5 Regulatory Compliance Mapping

| Regulation | Key BI Controls Required |
|---|---|
| **SOX** | Access controls, audit trail for financial reports, change log for certified reports |
| **HIPAA** | PHI column masking, access logging, BAA with tool vendors, encryption at rest and in transit |
| **GDPR / CCPA** | PII minimization, right-to-erasure capability (no PII in extracts), data residency controls |
| **PCI-DSS** | Cardholder data never in BI tool; audit log of any access to payment-adjacent data |
| **FINRA / MiFID II** | Trade data access logging, 7-year retention of audit records, insider threat monitoring |

---

## 14. Incident & Breach Considerations for BI

### 14.1 BI-Specific Breach Scenarios

| Scenario | Detection | Response |
|---|---|---|
| User exports RESTRICTED data to personal device | DLP alert; Power BI audit log | Disable account; escalate to Privacy Officer within 1 hour |
| Report misconfiguration exposes another user's data | User report; audit log review | Immediate report takedown; RLS review; incident report |
| Credentials embedded in Alteryx workflow pushed to Git | Secret scan alert in CI/CD | Immediate credential rotation; review all exposed workflows |
| Unapproved external guest accesses CONFIDENTIAL report | IdP login anomaly alert | Revoke access; review how guest was provisioned |
| Malicious SQL injection via DirectQuery parameter | Query anomaly detection | Block report; review query history; escalate to InfoSec |

### 14.2 BI Incident Response Checklist

```
□ Identify scope: which report, dataset, data classification, affected users
□ Take report offline immediately (if active exposure)
□ Preserve audit logs before any remediation
□ Notify Data Governance Lead and Privacy Officer within 1 hour (RESTRICTED/TOP_SECRET)
□ Notify CDO within 4 hours
□ Assess regulatory notification obligation (GDPR: 72-hour clock starts)
□ Root cause analysis within 5 business days
□ Corrective controls implemented and tested
□ Post-incident review documented and shared with governance committee
```

---

*Document controlled by the Chief Data Office and BI Center of Excellence. Reviewed annually and upon any major platform change or regulatory update.*
