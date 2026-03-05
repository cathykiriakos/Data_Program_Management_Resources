# Business Intelligence Standards
## Binding Standards: Tableau | Power BI | Alteryx

**Document Owner:** Chief Data Office  
**Domain:** Business Intelligence  
**Version:** 1.0  
**Classification:** Internal — Binding Standard  
**Review Cycle:** Annual (or upon major platform or regulatory change)

---

> **Note:** These are binding standards. Exceptions require written approval from the BI COE Lead and Data Governance Lead. All exceptions are logged and reviewed quarterly.

---

## Table of Contents

1. [Data Source Standards](#1-data-source-standards)
2. [Access & Authentication Standards](#2-access--authentication-standards)
3. [Content Development Standards](#3-content-development-standards)
4. [Naming & Taxonomy Standards](#4-naming--taxonomy-standards)
5. [Performance Standards](#5-performance-standards)
6. [Security & Compliance Standards](#6-security--compliance-standards)
7. [Content Lifecycle Standards](#7-content-lifecycle-standards)
8. [Cost & Resource Standards](#8-cost--resource-standards)
9. [Change Management Standards](#9-change-management-standards)
10. [Zero-Tolerance Rules](#10-zero-tolerance-rules)

---

## 1. Data Source Standards

### STD-DS-001: Approved Data Sources Only

**Standard:** All BI content must connect exclusively to data sources listed in the Approved Data Source Registry. No unapproved connection may be used in any published content.

**Scope:** All tools (Tableau, Power BI, Alteryx), all tiers (T1–T3), all environments.

**Verification:** Quarterly audit of all data source connections across all workspaces.

---

### STD-DS-002: No Direct Source System Connections

**Standard:** BI tools may not connect directly to source/operational systems (ERP, CRM, HRMS, etc.) in any environment above development sandbox.

**Approved connection targets:**
- Snowflake Gold layer (via certified dataset / semantic model)
- Databricks Gold catalog (via certified dataset)
- Approved Power BI Dataflows
- Approved Tableau Published Data Sources

**Exception process:** Written approval from BI COE Lead + DE Lead. Temporary (max 90 days). Logged in exception register.

---

### STD-DS-003: Import Mode Restrictions

**Standard:** Import mode (data copied into BI tool memory) requires BI COE approval and a completed data minimization review before use in T1 or T2 content.

**Import mode approval checklist:**
- [ ] Business justification documented (why live/DirectQuery is insufficient)
- [ ] Data classification confirmed
- [ ] Column scope minimized — no columns beyond those needed for the report
- [ ] Row filter applied — data scoped to minimum time range / entity set needed
- [ ] Refresh schedule does not exceed source data refresh frequency
- [ ] PII handling reviewed and confirmed

**Default:** Live connection or DirectQuery is the preferred connection mode for all content.

---

### STD-DS-004: Service Account Credentials Only

**Standard:** No personal user credentials may be embedded in any published data source, Alteryx workflow connection, or scheduled refresh configuration. All automated connections must authenticate via service accounts managed by the BI COE.

---

## 2. Access & Authentication Standards

### STD-AUTH-001: Single Sign-On Mandatory

**Standard:** All BI tool authentication must be via corporate SSO (SAML 2.0 / OIDC with Okta or Azure AD). Local username/password authentication must be disabled on all platforms in non-sandbox environments.

---

### STD-AUTH-002: MFA Required

**Standard:** MFA is mandatory for all human users across all BI platforms. Tools that do not support native MFA must enforce it via Conditional Access at the IdP level.

---

### STD-AUTH-003: No Shared Accounts

**Standard:** Every user has an individual named account. Shared accounts (e.g., "finance-reports@company.com" used by multiple people) are strictly prohibited. Existing shared accounts must be migrated to individual accounts within 60 days of this standard's effective date.

---

### STD-AUTH-004: Access Provisioning via IdP Groups

**Standard:** All BI tool role assignments must be driven by IdP group membership. No direct role assignment inside BI tools except by the BI COE platform administrator for emergency break-glass accounts.

---

### STD-AUTH-005: External User Access Policy

**Standard:** Guest or external user access to any BI content requires:
- Written request from an internal sponsor (manager level or above)
- Data Governance Lead approval
- Scope limited to specific reports (never the underlying data source)
- Time-limited: maximum 90 days per grant; must be renewed
- Logged in the Access Register with sponsor, approver, scope, expiry

---

### STD-AUTH-006: Quarterly Access Recertification

**Standard:** All managers must certify their direct reports' BI tool access quarterly. Accounts not recertified within 10 business days of the recertification window are automatically suspended.

---

## 3. Content Development Standards

### STD-DEV-001: Build from Certified Datasets

**Standard:** T1 and T2 content must be built exclusively from certified datasets or approved published data sources. T3 self-service content must use certified datasets. Direct SQL connections in reports require BI COE approval.

---

### STD-DEV-002: Brand Template Required

**Standard:** All T1 and T2 content must be built from the current approved brand template. Deviations from the template (font, color palette, header/footer structure) require BI COE approval and update to the template if the change is valid.

**Template locations:**
- Tableau: `[Tableau Server] / BI Templates / Corporate Brand Template v{current}`
- Power BI: `[SharePoint] / BI COE / Templates / Corporate_Brand_Theme_{version}.json`
- Alteryx: `[Alteryx Gallery] / BI COE Templates / Corporate Report Template`

---

### STD-DEV-003: No Local Redefinition of Certified Metrics

**Standard:** No report may define a calculated measure that redefines a metric already defined in the semantic layer / certified dataset. Certified metrics include (but are not limited to):

- Revenue (Gross, Net, Recurring)
- Headcount (Active, FTE, Contractor)
- Customer metrics (Churn rate, NPS, LTV)
- Financial ratios (Margin %, EBITDA)
- Operational KPIs (as defined by domain owners)

If a report author believes the certified definition is incorrect, the correct path is to raise a metric definition change request to the BI COE — not to create a local override.

---

### STD-DEV-004: Report Publication Checklist

Every T1/T2 report must pass this checklist before publication:

```
□ Built from certified dataset (data source documented)
□ Brand template applied; no non-brand colors or fonts
□ Data classification label visible on every page / dashboard
□ "Last Refreshed" timestamp visible on every page
□ Report owner name and contact in footer
□ RLS verified — tested as non-privileged user
□ Column scope reviewed — no PII visible to general audience
□ All KPI definitions link to or match semantic layer definitions
□ Performance tested — page load < 5 seconds
□ Mobile layout configured (T1 reports)
□ Accessibility: color contrast passes WCAG AA; no color-only encoding
□ Registered in Report Registry
□ Prior version deprecated (if replacement)
□ Domain data owner sign-off obtained
□ BI COE certification applied
```

---

### STD-DEV-005: Version Control for BI Assets

**Standard:** All T1 certified report development must be managed via version-controlled deployment (Power BI deployment pipelines, Tableau REST API promotion — not manual publish).

For Power BI:
```
Development Workspace → Test Workspace → Production Workspace
(all promotion via deployment pipeline; no manual publish to production)
```

For Tableau:
```
Tableau Desktop → Tableau Server Dev Project → Tableau Server Prod Project
(promotion via Tableau REST API in CI/CD; no direct Desktop → Prod publish)
```

---

## 4. Naming & Taxonomy Standards

### 4.1 Workspace / Project Naming

**Power BI Workspaces:** `{Domain} - {Tier} [{ENV}]`
```
Finance - Production
Finance - Development
Certified Datasets (no domain prefix — org-wide)
```

**Tableau Projects:** `[{Classification}] {Domain} - {Tier}`
```
[CONFIDENTIAL] Finance - T1 Certified
[INTERNAL] Sales - T2 Governed
[INTERNAL] Self-Service - T3
```

### 4.2 Report Naming

**Standard:** `{Domain} | {Subject} | {Frequency/Type}`

```
Finance | Revenue Performance | Monthly
Sales | Pipeline Analysis | Weekly
HR | Headcount Summary | Daily
Operations | Fulfilment Metrics | Real-Time
```

**Rules:**
- No version numbers in report name (versioning in the registry)
- No dates in report name (use "monthly", "weekly", etc.)
- No tool name in report name
- No author name in report name

### 4.3 Dataset / Data Source Naming

**Standard:** `{Domain} - {Subject} Dataset [{Classification}]`

```
Finance - Revenue Dataset [CONFIDENTIAL]
Sales - Pipeline Dataset [INTERNAL]
HR - Headcount Dataset [RESTRICTED]
```

### 4.4 Measure / Column Naming in Reports

| Pattern | Example |
|---|---|
| Revenue measures | `[Gross Revenue]`, `[Net Revenue]`, `[Revenue YTD]` |
| Count measures | `[Customer Count]`, `[Order Count]` |
| Rate measures | `[Churn Rate %]`, `[Gross Margin %]` |
| Variance measures | `[Revenue vs Prior Year]`, `[Revenue vs Plan %]` |
| Date/time | `[Transaction Date]`, `[Report Period]`, `[As of Date]` |

**Rules:**
- Spaces allowed in display names; underscores for technical names
- Consistent use of `%` suffix for percentages in display names
- Currency amounts always include currency code in display name if multi-currency report
- Boolean fields: `Is Active`, `Has Orders` pattern

---

## 5. Performance Standards

### STD-PERF-001: Dashboard Load Time

| Content Tier | Max Initial Load | Max Page Navigation | Action if Breached |
|---|---|---|---|
| T1 Executive | 5 seconds | 3 seconds | Performance review required; not certifiable until resolved |
| T2 Domain | 8 seconds | 5 seconds | Optimization recommended; documented if exception |
| T3 Self-Service | 15 seconds | 10 seconds | User advised; no block |

---

### STD-PERF-002: Scheduled Refresh Windows

**Standard:** Scheduled data refreshes must be configured within the following windows to avoid contention:

| Refresh Type | Allowed Window | Rationale |
|---|---|---|
| Heavy extracts (>1M rows) | 12:00 AM – 5:00 AM (local) | Avoid business-hours warehouse contention |
| Standard refreshes | 12:00 AM – 7:00 AM (local) | Off-peak |
| High-frequency (hourly) | Any time | Must be DirectQuery; not extract |
| Real-time | DirectQuery only; no extract | Never |

---

### STD-PERF-003: Alteryx Workflow Runtime Limits

| Priority | Max Runtime | Escalation |
|---|---|---|
| P1 (critical business) | 4 hours | Auto-kill after 4 hours; alert BI COE |
| P2 (standard) | 2 hours | Auto-kill after 2 hours |
| P3 (non-urgent) | 1 hour | Auto-kill after 1 hour |
| Development | 30 minutes | Auto-kill after 30 minutes |

---

### STD-PERF-004: Visual Count Limits

| Dashboard Page | Max Recommended Visuals | Hard Maximum |
|---|---|---|
| Executive summary | 8 | 12 |
| Operational dashboard | 12 | 16 |
| Detail / drillthrough | 16 | 20 |

Exceeding the hard maximum requires BI COE approval and performance testing confirmation.

---

## 6. Security & Compliance Standards

### STD-SEC-001: Row-Level Security Mandatory for Multi-Audience Datasets

**Standard:** Any certified dataset accessed by users with different data scope (e.g., regional sales reps seeing only their region) must have RLS implemented and tested before publication.

**RLS test requirement:** Every RLS configuration must be tested as at least three different user personas before T1/T2 certification:
1. A user who should see a full scope
2. A user with a restricted scope
3. A user who should see nothing (invalid scope — confirm no data leakage)

---

### STD-SEC-002: PII Not Visible in Non-Restricted Reports

**Standard:** Any report intended for a general (non-RESTRICTED) audience must not display PII in any field, filter label, tooltip, or export. PII masking must be applied at the data source level (Snowflake dynamic masking or certified dataset column exclusion) — not in the report layer.

---

### STD-SEC-003: Data Classification Labeling

**Standard:** Every published report and dataset must have a data classification label applied and visible.

**Label placement:**
- Every dashboard page: label visible in header or footer
- Every paginated report: visible in header of every page
- Every export: embedded in document properties and watermark
- Every email subscription: stated in email subject and body

---

### STD-SEC-004: Audit Log Completeness

**Standard:** All BI platforms must emit audit logs for the events listed in the Best Practices document (§13.4). Logs must flow to the SIEM within 24 hours. Log gaps are treated as HIGH findings.

---

### STD-SEC-005: Encryption in Transit and at Rest

**Standard:** All BI tool connections must use TLS 1.2 or higher. All data at rest in BI tool storage (import mode datasets, dataflows, extracts) must be encrypted using platform-provided encryption. Customer-managed keys (CMK) required for RESTRICTED and TOP_SECRET classified data.

---

## 7. Content Lifecycle Standards

### STD-LC-001: Stale Content Archival

**Standard:** Content not viewed in 90 consecutive calendar days is automatically archived (removed from published state; metadata retained). Content owners are notified at 60 and 75 days.

**Reactivation:** Owner may request reactivation within 30 days of archival. After 30 days, content is permanently retired (metadata retained in registry for 3 years).

---

### STD-LC-002: Report Ownership Required

**Standard:** Every published T1 and T2 report must have a named owner who:
- Is a current employee with an active BI tool account
- Has accepted the Data Steward responsibilities for that report
- Is responsible for triggering the deprecation process if the report is no longer needed

Reports without a valid owner are flagged as HIGH findings and archived within 30 days.

---

### STD-LC-003: Report Deprecation Process

**Standard:** When a report is superseded or no longer needed:
1. Replacement report (if any) must be certified before old report is deprecated
2. Affected users notified 30 days before deprecation (T1) or 14 days (T2/T3)
3. Old report redirected to new report for 30 days (if tool supports redirect)
4. Report marked as "Deprecated" in the Report Registry with date, reason, and replacement link
5. Report removed from publication; metadata retained

---

### STD-LC-004: Semi-Annual Content Review

**Standard:** The BI COE conducts a semi-annual review of all T1 and T2 content:
- Confirms all reports are actively used (view count > 0)
- Confirms owner is still a current employee
- Confirms data source is still certified
- Confirms data classification is still correct
- Confirms no significant metric definition drift from semantic layer

---

## 8. Cost & Resource Standards

### STD-COST-001: Dedicated BI Warehouse / Capacity

**Standard:** BI workloads run on a **dedicated** compute resource (Snowflake BI warehouse, Power BI Premium capacity, Tableau Server resource pool). BI tools must not share compute with ELT/transformation workloads.

---

### STD-COST-002: Resource Monitor Mandatory

**Standard:** Every Snowflake warehouse used by BI tools must have a resource monitor configured with:
- Monthly credit quota aligned to budget
- Alert at 75% consumption
- Suspension at 100% consumption (with notification to BI COE)

---

### STD-COST-003: No High-Frequency Refreshes on Large Datasets

**Standard:** Datasets exceeding 1 million rows may not be scheduled to refresh more frequently than every 4 hours without BI COE approval and a documented business justification.

---

### STD-COST-004: Subscription Hygiene

**Standard:** Email subscriptions to reports for departed employees must be removed within 5 business days of the employee's departure. BI COE runs a quarterly subscription audit to identify and remove orphaned subscriptions.

---

## 9. Change Management Standards

### STD-CM-001: Change Tier Classification for BI

| Change Type | Tier | Approver | Lead Time |
|---|---|---|---|
| T3 self-service report (new/update) | Self-service | Creator | Immediate |
| T2 domain report update | Standard | Domain BI Lead (peer review) | Same day |
| New T2 domain report | Standard | Domain BI Lead + BI COE review | 3–5 days |
| New certified dataset | Minor | BI COE Lead + Data Governance | 5–10 days |
| T1 certified report update | Minor | BI COE Lead + domain owner | 5 days |
| New T1 certified report | Minor | BI COE Lead + domain owner + CDO | 5–10 days |
| RBAC / workspace restructure | Major | BI COE Lead + IT + CAB | 10–15 days |
| BI platform version upgrade | Major | BI COE Lead + IT + CAB | 10–15 days |
| New BI tool adoption | Major | CDO + IT + CAB | 15–30 days |
| External sharing enablement | Major | CDO + Legal + Privacy + CAB | 15+ days |

---

## 10. Zero-Tolerance Rules

The following standards have **no exception pathway**. Violations are escalated immediately to the BI COE Lead and Data Governance Lead:

| Rule | Violation Action |
|---|---|
| Direct connection to a production source system database from any BI tool | Immediate connection revocation; incident report; access review |
| Personal credentials embedded in a published data source or workflow | Immediate credential rotation; access review; re-training required |
| Shared accounts in any BI tool | Immediate account suspension; accounts separated before reinstatement |
| PII visible in a report accessible to users without RESTRICTED data role | Immediate report takedown; incident report; Privacy Officer notification |
| External sharing of RESTRICTED or TOP_SECRET classified content | Immediate access revocation; Privacy Officer + Legal notification; regulatory assessment |
| Publishing content without a data classification label in a regulated environment | Immediate takedown; owner re-training required before republication |
| Manually publishing to a T1 production workspace bypassing the deployment pipeline | Rollback; incident report; access review |

---

*These standards are binding across all BI tools, all environments, and all users. Non-compliance is escalated as defined above and may result in suspension of BI tool access pending remediation. Standards reviewed annually.*
