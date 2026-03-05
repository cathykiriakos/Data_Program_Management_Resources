# Establishing an Effective Business Intelligence Program
## Ground-Up Strategy: Tableau | Power BI | Alteryx

**Document Owner:** Chief Data Office  
**Domain:** Business Intelligence  
**Version:** 1.0  
**Classification:** Internal — Program Standard

---

## Table of Contents

1. [Program Vision & Operating Model](#1-program-vision--operating-model)
2. [Ground-Up Build Strategy](#2-ground-up-build-strategy)
3. [BI Center of Excellence (COE) — Structure & Roles](#3-bi-center-of-excellence-coe--structure--roles)
4. [Platform Foundation Checklist](#4-platform-foundation-checklist)
5. [Self-Service Enablement Framework](#5-self-service-enablement-framework)
6. [Certified Dataset Program](#6-certified-dataset-program)
7. [Stakeholder Engagement & Change Management](#7-stakeholder-engagement--change-management)
8. [Maturity Model](#8-maturity-model)
9. [Roadmap Template](#9-roadmap-template)
10. [Governance Council Structure](#10-governance-council-structure)

---

## 1. Program Vision & Operating Model

### 1.1 Mission Statement

> The Business Intelligence program delivers trusted, governed, and performant analytics to every business consumer — through consistent standards, centralized semantic governance, and structured self-service — while protecting the organization from the regulatory, security, and operational risks of ungoverned data access.

### 1.2 The Cost of Getting This Wrong

Before defining how to build the program, it is worth quantifying the cost of not building it correctly:

| Problem | Consequence |
|---|---|
| No self-service governance | IT resolves 60–80% of analytics requests ad hoc; no scalability |
| Ungoverned self-service | Conflicting metrics, data trust collapse, security gaps |
| Direct DB connections from BI tools | Production system performance degradation; unbudgeted compute cost |
| Duplicate certified reports | Users confused about which is authoritative; reconciliation meetings become a standard agenda item |
| No branding standards | Reports look unofficial; executives distrust the data |
| No access process | PII exposed; regulatory findings; audit failures |
| No content lifecycle | Hundreds of stale, orphaned reports consuming server resources |

### 1.3 Target Operating Model — Federated Governance

```
┌─────────────────────────────────────────────────────────────────┐
│                    BI CENTER OF EXCELLENCE                       │
│                                                                  │
│  Owns: Platform, certified datasets, semantic layer, standards, │
│  branding, access policy, toolchain governance, COE backlog     │
│                                                                  │
│  Personas: BI Platform Engineer, Senior BI Developers,          │
│            Analytics Engineers, Data Governance Liaison         │
└───────────┬─────────────────────────────────┬───────────────────┘
            │ provides governed                │ enables
            │ data products                    │ structured self-service
    ┌───────▼──────────┐              ┌────────▼───────────┐
    │  DOMAIN BI LEADS  │              │  SELF-SERVICE USERS │
    │  (Finance, Sales, │              │  (Power users,       │
    │  HR, Ops, Risk)   │              │  business analysts)  │
    │                   │              │                      │
    │  Build governed   │              │  Explore and build   │
    │  domain reports   │              │  from certified      │
    │  from certified   │              │  datasets only;      │
    │  datasets         │              │  within guardrails   │
    └───────────────────┘              └──────────────────────┘
```

---

## 2. Ground-Up Build Strategy

### Phase 0 — Foundation (Weeks 1–4)

**Goal:** Platform is deployed, secured, and governed before any reports are built.

```
Week 1: BI tool environments provisioned; SSO configured
Week 2: RBAC skeleton deployed; access provisioning process live
Week 3: Branding templates created; Report Registry initialized
Week 4: Audit logging live; Approved Data Source Registry seeded
```

**Deliverables:**
- [ ] Tableau Server/Cloud or Power BI tenant configured with SSO (Okta/Azure AD)
- [ ] Alteryx Server configured with SSO
- [ ] Local authentication disabled on all platforms
- [ ] SCIM provisioning enabled for user lifecycle management
- [ ] Role-to-IdP group mapping configured (no direct tool provisioning)
- [ ] Workspace / project structure created per governance tiers (T1–T4)
- [ ] Branding theme files created and deployed (Tableau + Power BI)
- [ ] Report Registry initialized (even if empty)
- [ ] Approved Data Source Registry initialized
- [ ] Audit log pipeline to SIEM configured

---

### Phase 1 — Certified Dataset Foundation (Weeks 5–12)

**Goal:** The organization has a set of trusted, governed datasets that BI tools connect to — not raw tables.

```
Week 5–6:  Semantic layer connection established (dbt → Snowflake Gold)
Week 7–8:  Priority 1 certified datasets built (Finance + Sales — highest demand)
Week 9–10: RLS + masking policies tested; data classification labels applied
Week 11:   Data sources published in Tableau / Power BI; certified badge applied
Week 12:   Training delivered to Domain BI Leads on certified datasets
```

**Deliverables:**
- [ ] At least 3 certified datasets published for priority domains
- [ ] RLS validated for every published certified dataset
- [ ] PII masking confirmed in all non-restricted certified datasets
- [ ] All certified datasets registered in Approved Data Source Registry
- [ ] Domain BI Leads trained and onboarded

---

### Phase 2 — T1 Certified Report Suite (Weeks 13–22)

**Goal:** Core organizational reports (executive KPIs, operational metrics) built to T1 standard and replacing any legacy or ad hoc equivalents.

```
Week 13–14: Executive KPI dashboard (Finance, Revenue, Headcount)
Week 15–16: Sales Performance dashboard
Week 17–18: Operations / Supply Chain dashboard
Week 19–20: HR People Analytics dashboard
Week 21:    All T1 reports reviewed, certified, published
Week 22:    Legacy report deprecation plan communicated to users
```

**Deliverables:**
- [ ] T1 report suite published for all priority domains
- [ ] Each T1 report has a named owner, certified classification, registered entry
- [ ] All T1 reports reviewed and signed off by domain data owners
- [ ] Legacy competing reports identified; deprecation timeline communicated

---

### Phase 3 — Self-Service Enablement (Weeks 23–30)

**Goal:** Power users can build on certified datasets within guardrails; IT support burden decreases.

```
Week 23–24: Self-service training program built and delivered
Week 25–26: T3 self-service workspace structure configured
Week 27–28: Alteryx Gallery organized; approved connections published
Week 29:    Content lifecycle rules automated (90-day stale archival)
Week 30:    First quarterly content audit completed
```

**Deliverables:**
- [ ] Self-service training curriculum delivered
- [ ] T3 workspace available with guardrails configured
- [ ] Alteryx DCM connections published for approved sources
- [ ] Content lifecycle automation configured (stale report archival)
- [ ] Self-service intake process live (replaces ad hoc IT requests)

---

### Phase 4 — Operationalize & Scale (Ongoing)

- Quarterly governance reviews (Report Registry audit, access recertification)
- Monthly compute cost review
- Semi-annual certified dataset review (relevance and accuracy)
- Annual BI maturity assessment
- Continuous training: onboarding curriculum updated each quarter

---

## 3. BI Center of Excellence (COE) — Structure & Roles

### 3.1 Core COE Roles

| Role | Responsibilities | Key Skills |
|---|---|---|
| **BI Platform Engineer** | Tool administration, SSO, server performance, cost monitoring, CI/CD for BI assets | Tableau Server / Power BI admin, Python, REST APIs, cloud infrastructure |
| **Senior BI Developer** | T1 certified report development, semantic model design, branding enforcement, framework development | Advanced DAX / Tableau Calcs, data modeling, SQL, UX design |
| **Analytics Engineer** | Certified dataset development, dbt Gold model ownership, semantic layer maintenance | dbt, SQL, Snowflake/Databricks, Python |
| **BI Governance Analyst** | Report Registry management, access process, content lifecycle, audit preparation | Data governance, RBAC, audit processes, documentation |
| **Domain BI Lead** *(embedded in domain)* | T2 domain report development, self-service enablement for domain, liaison to COE | Domain expertise + BI tool proficiency |

### 3.2 RACI Matrix

| Activity | BI Platform Eng. | Sr. BI Dev. | Analytics Eng. | Governance Analyst | Domain BI Lead | IT/InfoSec |
|---|---|---|---|---|---|---|
| Tool provisioning & admin | **R/A** | I | I | I | I | C |
| SSO / RBAC configuration | **R** | I | I | C | I | **A** |
| Certified dataset development | C | R | **R/A** | I | C | I |
| T1 report development | C | **R/A** | C | I | I | I |
| T2 report development | I | C | C | I | **R/A** | I |
| Branding template ownership | C | **R/A** | I | I | I | I |
| Report Registry management | I | I | I | **R/A** | C | I |
| Access provisioning | C | I | I | **R/A** | I | R |
| Content lifecycle automation | **R/A** | I | I | C | I | I |
| Audit preparation | C | I | I | **R/A** | C | C |
| Self-service training | I | R | C | C | **A** | I |
| Cost monitoring | **R/A** | C | C | I | I | I |

---

## 4. Platform Foundation Checklist

### 4.1 Tableau Server / Tableau Cloud

```
□ Authentication
  □ SAML 2.0 configured with corporate IdP
  □ Local authentication disabled
  □ MFA enforced via IdP Conditional Access
  □ SCIM provisioning enabled
  □ Session timeout: 8 hours idle

□ Site Configuration
  □ Site role defaults set (Viewer for new users)
  □ Guest access disabled
  □ External sharing disabled by default
  □ Tableau Bridge configured (if on-premise data sources needed)

□ Project Structure
  □ Governance tier projects created (T1-Certified, T2-Governed, T3-Self-Service, T4-Sandbox)
  □ "Certified Data Sources" project created; locked to BI COE write access
  □ Default project permissions configured and locked

□ Data Source Controls
  □ Connector allowlist configured (Snowflake, Databricks approved; others require COE approval)
  □ Embedded credentials policy: service accounts only
  □ Personal credentials in published data sources: disabled

□ Content Lifecycle
  □ Stale content alert: configured at 90 days no views
  □ Usage statistics logging: enabled
  □ Subscription management: admin can view and remove all subscriptions

□ Monitoring & Audit
  □ Admin Insights: enabled and connected to monitoring dashboard
  □ Audit logs: exported to SIEM
  □ Resource monitoring dashboard: live
```

### 4.2 Power BI Tenant

```
□ Authentication
  □ Azure AD / Entra ID as sole identity provider
  □ Conditional Access policy: MFA required for Power BI
  □ Block legacy authentication protocols
  □ Service principal: governed via security group; not open

□ Tenant Settings (Power BI Admin Portal)
  □ "Allow users to sign up for Power BI individually" → DISABLED
  □ "External guest user access" → DISABLED (enable per-request only)
  □ "Export to Excel" → ENABLED (CONFIDENTIAL and below only)
  □ "Export to PDF" → ENABLED (all classifications; watermark applied)
  □ "Publish to web (public)" → DISABLED
  □ "Share content with external users" → DISABLED
  □ "Allow service principals to use Power BI APIs" → Via security group only

□ Workspace Structure
  □ Certified Datasets workspace: write access = BI COE only
  □ Domain production workspaces: created per domain
  □ Development workspaces: created per domain
  □ Sandbox workspace: time-limited; auto-cleaned

□ Sensitivity Labels (Microsoft Purview)
  □ Sensitivity labels enabled at tenant level
  □ Mandatory labeling enabled: reports cannot publish without label
  □ Label inheritance: dataset → report → export
  □ RESTRICTED label: block download, encrypt export, watermark

□ Premium Capacity (if applicable)
  □ Capacity metrics app deployed
  □ Memory thresholds configured (alert 70%, action 85%)
  □ Paginated reports capacity: separate node or configuration

□ Audit & Compliance
  □ Audit logs: flowing to Microsoft 365 compliance center
  □ Audit log retention: configured to regulatory minimum (1–7 years)
  □ Activity log API: connected to SIEM
```

### 4.3 Alteryx Server

```
□ Authentication
  □ SAML configured with corporate IdP
  □ Windows authentication disabled
  □ MFA enforced via IdP
  □ SCIM provisioning enabled

□ Data Connection Manager (DCM)
  □ DCM enabled
  □ All approved data connections created by BI COE / DE team
  □ User-created connections: require approval workflow
  □ Credentials: stored in DCM only; no embedded credentials in workflows

□ Gallery Configuration
  □ Collections created per domain (Finance, Sales, HR, etc.)
  □ "Public" collection disabled (no public access without approval)
  □ Workflow versioning: enabled
  □ Execution audit logging: enabled

□ Worker Node Configuration
  □ Max concurrent workflows per worker: configured
  □ Memory limit per workflow: configured
  □ Timeout policy: alert at 90 min; kill at 4 hours (default)
  □ Priority queues: configured (P1 for critical; P2 for standard)

□ Output Destinations
  □ Approved output destinations whitelist: configured
  □ Local/personal drive output: disabled for published workflows
  □ All output goes to: Snowflake Gold tables, ADLS/S3, approved file stores only
```

---

## 5. Self-Service Enablement Framework

### 5.1 The Structured Self-Service Model

Self-service is not "do whatever you want." It is **autonomy within defined boundaries**:

```
WHAT USERS CAN DO:
  ✅ Connect to certified datasets
  ✅ Build T3 reports for personal/team use
  ✅ Apply their own filters, drill paths, and layouts
  ✅ Create calculated fields that don't redefine certified metrics
  ✅ Export their own T3 reports (per classification rules)
  ✅ Request promotion of T3 to T2 (via BI COE review)

WHAT USERS CANNOT DO:
  ❌ Create direct connections to production databases
  ❌ Import source system tables directly into BI tools
  ❌ Redefine certified KPIs (Revenue, Headcount, etc.) locally
  ❌ Publish to T1 or T2 workspaces (COE and Domain BI Lead only)
  ❌ Share content externally without approval
  ❌ Access data outside their data scope
```

### 5.2 Self-Service Intake Process

Replace ad hoc IT/analytics requests with a structured intake:

```
User has analytics need
        │
        ▼
Search Report Registry: Does this report already exist?
    YES └→ Use existing report. If inadequate, raise enhancement request.
    NO  └→ Continue
        │
        ▼
Is the data available in a certified dataset?
    YES └→ User builds T3 report from certified dataset (self-service)
    NO  └→ Submit data request to BI COE (new certified dataset or column)
        │
        ▼
T3 report built by user
        │
        ▼
Used only by creator/team? → Stays as T3 (90-day expiry)
Broader audience needed?  → Submit T2 promotion request to Domain BI Lead
Org-wide?                 → Submit T1 promotion request to BI COE
```

### 5.3 Self-Service Training Curriculum

| Module | Audience | Duration | Delivery |
|---|---|---|---|
| BI Platform Orientation | All users | 1 hour | Self-paced e-learning |
| Data Governance for Business Users | All users | 1 hour | Self-paced e-learning |
| Tool Fundamentals (Power BI / Tableau) | All users | 4 hours | Self-paced e-learning |
| Working with Certified Datasets | Power users | 2 hours | Instructor-led |
| Building Compliant T3 Reports | Power users | 3 hours | Instructor-led + lab |
| Self-Service Data Policy | Power users | 1 hour | Self-paced e-learning |
| Advanced Analytics (Alteryx) | Alteryx users | 8 hours | Instructor-led + lab |
| Domain BI Lead Certification | Domain BI Leads | 2 days | Full program |

**Completion requirement:** All users must complete modules 1–3 before BI tool access is provisioned.

---

## 6. Certified Dataset Program

### 6.1 What Makes a Dataset "Certified"

A certified dataset is one that:
- Is built on the Gold layer of the data platform (not Bronze or Silver)
- Has been reviewed and approved by both the BI COE and the data domain owner
- Has RLS configured and tested
- Has data classification labels applied
- Has all PII columns appropriately masked for the target audience
- Is registered in the Approved Data Source Registry
- Has a named owner responsible for its accuracy and freshness
- Is refreshed on a defined schedule with SLA monitoring

### 6.2 Certification Process

```
1. PROPOSE
   └── Analytics Engineer or Senior BI Developer proposes new dataset
   └── Justification: business need, audience, data source, classification

2. DESIGN
   └── Dataset designed on top of Gold layer / semantic model
   └── RLS design reviewed with Data Governance Lead
   └── Column inclusion reviewed for data minimization

3. BUILD & TEST
   └── Dataset built on development workspace
   └── RLS tested as multiple user personas
   └── Data accuracy validated against source of truth

4. SECURITY REVIEW
   └── Data Governance Lead confirms RLS is correct
   └── Privacy Officer confirms PII handling is compliant
   └── Classification label applied

5. DOMAIN OWNER SIGN-OFF
   └── Data domain owner (e.g., Finance Controller) confirms accuracy

6. CERTIFY
   └── BI COE applies certification badge
   └── Dataset published to "Certified Datasets" workspace
   └── Registered in Approved Data Source Registry
   └── Review cadence set (6 months for CONFIDENTIAL; 12 months for INTERNAL)

7. COMMUNICATE
   └── Domain BI Leads and power users notified
   └── Data catalog entry updated with certified status
```

### 6.3 Certified Dataset Review

Every certified dataset is reviewed on its defined cadence:

```
Review Checklist:
  □ Dataset is still actively used (>0 connected reports)
  □ Underlying Gold layer model has not broken the schema
  □ RLS rules reflect current org structure (team changes, role changes)
  □ Column scope still appropriate (nothing added without review)
  □ Refresh schedule still meets consumer SLA
  □ Owner is still the correct person / team
  □ Data classification still correct
  □ No new PII columns added to the source that need masking

Actions if gaps found:
  - RLS gaps → immediate update + security review
  - Stale (no connected reports) → deprecate within 30 days
  - Owner changed → update registry; re-certify
```

---

## 7. Stakeholder Engagement & Change Management

### 7.1 Managing the Transition to Governed Self-Service

For organizations that currently have ungoverned BI environments, the transition is a **change management exercise** as much as a technical one.

**Common resistance points and responses:**

| Resistance | Response |
|---|---|
| "I need to connect directly to the database — it's faster" | Show users the certified dataset performance; optimize if genuinely insufficient; explain security and cost rationale |
| "My report is different from the certified one for a reason" | Review the difference; if the difference is valid, update the certified definition; if not, align to the standard |
| "This slows me down" | Quantify self-service intake time vs. IT request queue time; training removes friction |
| "I've always done it this way" | Acknowledge history; explain the business risk (regulatory, cost, trust) of continuing |
| "Why can't I just export to Excel?" | Clarify the policy (classification-dependent); offer alternatives like paginated reports or approved exports |

### 7.2 Communication Plan

| Milestone | Message | Audience | Channel |
|---|---|---|---|
| Program launch | "New BI governance program — here's what changes" | All employees | All-hands + email |
| Self-service training live | "Training available — required before access provisioned" | All BI users | Email + manager briefing |
| Certified datasets published | "New certified datasets available — start here" | Domain BI Leads + power users | Email + Confluence |
| Legacy report deprecation | "These reports are being replaced — here's what to use instead" | Affected users | Direct email + 30-day notice |
| Access recertification | "Your manager must re-confirm your BI access" | All users (via managers) | Email + ITSM task |

---

## 8. Maturity Model

Assess quarterly against this model:

| Dimension | Level 1 — Ad Hoc | Level 2 — Managed | Level 3 — Defined | Level 4 — Optimized |
|---|---|---|---|---|
| **Authentication** | Mixed; some shared accounts | All named accounts; some SSO | Full SSO + MFA; SCIM provisioning | Continuous access review; behavioral monitoring |
| **Data Sources** | Direct DB connections; no registry | Some certified datasets | Full certified dataset library; registry maintained | Self-service dataset request < 1 week |
| **Governance** | No policy | Policy exists; inconsistently applied | Policy enforced via platform controls | Automated compliance monitoring |
| **Content Quality** | No standards | Some standards documented | Branding + review checklist enforced | Automated brand validation in CI/CD |
| **Self-Service** | Uncontrolled | Basic guardrails | Structured self-service with intake process | Self-service satisfies 80%+ of analytics demand |
| **Compute Cost** | Unknown | Monitored manually | Resource monitors + alerts | Automated cost optimization; chargeback by team |
| **Report Lifecycle** | No lifecycle management | Manual reviews | Automated stale archival + quarterly audit | Predictive usage-based optimization |
| **Regulatory Compliance** | Reactive | Documented controls | Controls embedded in platform | Continuous audit evidence generation |

---

## 9. Roadmap Template

```
Q1 — Foundation
  Platform provisioning (Tableau / Power BI / Alteryx)
  SSO + MFA + SCIM
  Workspace / project structure
  Branding templates
  Access provisioning process
  Audit logging to SIEM

Q2 — Certified Datasets & T1 Reports
  Priority certified datasets (Finance, Sales)
  T1 executive dashboard suite
  RLS validation
  Report Registry live
  Domain BI Lead onboarding

Q3 — Self-Service Enablement
  Self-service training curriculum
  T3 workspace + guardrails
  Alteryx Gallery organization + DCM
  Content lifecycle automation (90-day stale)
  Legacy report deprecation (Phase 1)

Q4 — Governance Maturity
  Quarterly access recertification (first run)
  Compute cost chargeback reporting
  Sensitivity labels / Purview integration
  Self-service intake process metrics
  First annual BI maturity assessment
  → Target: Maturity Level 3

Year 2 — Optimization
  Predictive stale content detection
  Automated brand validation
  Self-service to T2 promotion pipeline
  AI-assisted dashboard insights (Copilot / Einstein)
  → Target: Maturity Level 4
```

---

## 10. Governance Council Structure

### 10.1 BI Governance Council

A **BI Governance Council** meets monthly to provide oversight, resolve disputes, and approve significant changes.

**Members:**
- BI COE Lead (chair)
- Data Governance Lead
- Domain representatives (Finance, Sales, HR, Operations, Risk)
- IT representative (platform/infrastructure)
- Privacy Officer (standing invite; required for RESTRICTED data changes)

**Agenda (standing):**
1. Report Registry review — new certifications, deprecations
2. Access exceptions — any non-standard access approved in the period
3. Compute cost review — trends, anomalies, optimization actions
4. Incident review — any BI security or data quality incidents
5. Policy update proposals — any proposed changes to BI governance policy
6. Maturity scorecard update

**Escalation path:**
COE Lead → BI Governance Council → Data Governance Lead → CDO → Board (if regulatory)

---

*Document controlled by the Chief Data Office and BI Center of Excellence. Changes require approval from the BI COE Lead and Data Governance Lead.*
