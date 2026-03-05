# Data Governance Best Practices
> **Role:** Chief Data Officer | **Platform:** Snowflake / Databricks / Collibra  
> **Version:** 2.0 | **Last Updated:** 2026-03

---

## 1. Executive Summary

Data Governance is the formal orchestration of people, processes, and technology to enable the trusted, consistent use of data across an organization. As CDO, the goal is to establish a **repeatable, configurable governance framework** that scales across business units, data domains, and evolving technology stacks.

---

## 2. Core Principles

| Principle | Description |
|---|---|
| **Ownership** | Every data asset has a named owner accountable for quality, access, and lifecycle |
| **Fitness for Purpose** | Data is governed to the level its business criticality demands |
| **Transparency** | Data lineage, definitions, and rules are documented and discoverable |
| **Least Privilege** | Access is granted based on role, need, and sensitivity classification |
| **Automation First** | Manual governance processes are candidates for automation |
| **Iterative Improvement** | Governance matures through measured, incremental milestones |

---

## 3. Governance Framework Pillars

### 3.1 Data Ownership & Stewardship

```
CDO (Executive Sponsor)
 └── Data Domain Owners (Business Unit Leads)
      └── Data Stewards (Operational Owners)
           └── Data Custodians (Technical Owners / Engineering)
```

**Best Practices:**
- Define ownership at the **domain level** (Finance, Marketing, Operations, etc.)
- Assign stewardship to individuals, not teams — accountability must be personal
- Document owner/steward assignments in a **Data Catalog** — Collibra is the primary platform for ownership workflows, with Snowflake and Databricks serving as technical enforcement layers
- Use **Collibra Workflows** to automate ownership assignment requests, stewardship onboarding, and escalation routing
- Review ownership assignments **quarterly** and on org changes — Collibra's built-in task management drives this cadence automatically

---

### 3.2 Data Classification & Sensitivity

Define a tiered classification schema applied to all datasets:

| Tier | Label | Description | Example |
|---|---|---|---|
| 1 | **Public** | No restrictions | Published reports |
| 2 | **Internal** | Internal use only | Operational metrics |
| 3 | **Confidential** | Business-sensitive | Revenue forecasts |
| 4 | **Restricted** | Regulated / PII / PCI / HIPAA | SSN, Card Numbers |

**Best Practices:**
- Tag classification at the **column level** in Snowflake (`COLUMN_TAG`) or Databricks Unity Catalog — Collibra is the **system of record** for classification decisions
- Use **Collibra Data Intelligence Cloud** to assign and manage classification attributes centrally; push those decisions downstream to Snowflake and Databricks via API integration
- Automate classification scanning using Collibra's built-in data profiling or connected tools like Informatica
- Enforce access controls downstream from classification (not the other way around)

---

### 3.3 Data Quality Standards

Data quality is governed across six dimensions:

| Dimension | Definition | KPI Example |
|---|---|---|
| **Completeness** | Required fields are populated | % non-null on critical fields |
| **Accuracy** | Data reflects real-world values | Error rate vs. source of truth |
| **Consistency** | Same data means the same thing everywhere | Cross-system reconciliation rate |
| **Timeliness** | Data available when needed | SLA breach rate |
| **Uniqueness** | No unintended duplicates | Duplicate record rate |
| **Validity** | Data conforms to defined rules/formats | Schema violation rate |

**Best Practices:**
- Define DQ rules in a **central rules registry** — Collibra Data Quality (formerly Owl Analytics) is the primary DQ platform; rules are also version-controlled in YAML as code
- Run DQ checks at **ingestion, transformation, and consumption** layers; results feed back into Collibra for steward visibility
- Surface DQ scores in **Collibra's Data Health dashboards** — stewards receive task notifications on failures without needing to monitor pipelines directly
- Escalate failed DQ rules to the owning steward within defined SLAs using **Collibra Workflow automation**

---

### 3.4 Metadata Management

**Best Practices:**
- Treat metadata as a **first-class data product**
- **Collibra is the authoritative metadata hub** — all business definitions, ownership, classification, and SLA metadata lives here first
- Capture: business definitions, technical lineage, quality scores, owner, classification, SLA
- Enforce metadata completeness as a **gate** before assets are published to consumers — Collibra Workflows can block certification until required fields are complete
- Use a **Glossary-first** approach: define business terms in the **Collibra Business Glossary** before building pipelines

---

### 3.5 Data Lineage

**Best Practices:**
- Capture lineage automatically via pipeline tooling (dbt, Databricks Delta Live Tables, Snowflake lineage) — all lineage surfaces in **Collibra's lineage graph** via native connectors
- Collibra provides **end-to-end lineage** from source systems through Snowflake/Databricks transformations to BI reports — no manual lineage mapping required for supported connectors
- Require lineage visibility at minimum **3 hops upstream** from any governed asset
- Audit lineage quarterly for orphaned assets or undocumented transformations
- Expose lineage in Collibra for self-service consumers — analysts can trace where any number came from without involving engineering

---

### 3.6 Access Control & Entitlements

**Best Practices:**
- Implement **Role-Based Access Control (RBAC)** as the baseline
- Layer **Attribute-Based Access Control (ABAC)** for sensitive/regulated data
- Use Snowflake **Row Access Policies** and **Column-level Security** natively
- Use Databricks **Unity Catalog** row/column filters for equivalent enforcement
- Enforce the **joiner/mover/leaver** process — access must be reviewed and revoked on role change
- Run quarterly **Access Certification** reviews (stewards attest to access lists)

---

### 3.7 Lifecycle Management

**Best Practices:**
- Define **retention policies** per data classification and regulatory requirement
- Automate archival and deletion using Snowflake `TIME_TRAVEL` configuration and Databricks Delta `VACUUM`
- Require a **Data Impact Assessment** for any new sensitive data domain onboarded
- Document the full lifecycle: ingest → store → process → publish → archive → delete

---

## 4. Technology Stack Alignment

### Collibra (Governance System of Record)
Collibra serves as the **central command layer** for all governance activity. It is where business users, stewards, and executives interact with governance — not the database platforms directly.

| Collibra Capability | Governance Use |
|---|---|
| **Data Intelligence Cloud** | Central catalog — all asset metadata, ownership, classification |
| **Business Glossary** | Authoritative definitions for all governed terms |
| **Workflow Engine** | Automates stewardship tasks, approvals, access requests, certifications |
| **Data Lineage** | End-to-end visual lineage from source → Snowflake/Databricks → reports |
| **Data Quality (Owl Analytics)** | Rule-based and ML-assisted DQ monitoring with steward alerts |
| **Policy Manager** | Publish and enforce data policies; link policies to data assets |
| **Access Governance** | Access request workflows linked to classification and policy |
| **Collibra Connect** | Native connectors to Snowflake, Databricks, dbt, Tableau, and more |

### Collibra ↔ Snowflake Integration
| Flow | Mechanism | Result |
|---|---|---|
| Asset discovery | Collibra Snowflake connector (automated scan) | Tables/columns auto-populated in catalog |
| Classification sync | Collibra tags → Snowflake Object Tags via API | Classification enforced at DB layer |
| Lineage | Snowflake query lineage → Collibra lineage graph | Visual end-to-end lineage |
| DQ results | Collibra DQ → Snowflake result tables | DQ scores queryable in Snowflake |
| Access policy | Collibra policy decision → Snowflake RBAC roles | Access aligned to policy |

### Collibra ↔ Databricks Integration
| Flow | Mechanism | Result |
|---|---|---|
| Asset discovery | Collibra Unity Catalog connector | Delta tables/schemas auto-catalogued |
| Lineage | OpenLineage events from Databricks → Collibra | Pipeline lineage visible in Collibra |
| Classification | Collibra attributes → Unity Catalog tags | Consistent classification across platforms |
| DQ results | Collibra DQ on Delta tables | DQ scores visible to stewards in Collibra |

### Snowflake (Technical Enforcement Layer)
| Capability | Governance Use |
|---|---|
| Object Tagging | Receive classification tags pushed from Collibra |
| Row/Column Policies | Enforce access decisions made in Collibra |
| Data Sharing | Governed external data distribution |
| Access History | Audit trail fed back to Collibra for access monitoring |
| Dynamic Data Masking | Sensitive field masking aligned to Collibra classification |

### Databricks (Technical Enforcement Layer)
| Capability | Governance Use |
|---|---|
| Unity Catalog | Receives metadata and classification from Collibra |
| Column-level Security | Enforces field-level access per Collibra policy |
| Audit Logs | Access events surfaced in Collibra for compliance reporting |
| Tags & Comments | Synced bidirectionally with Collibra attributes |

---

## 5. Governance Anti-Patterns to Avoid

| Anti-Pattern | Risk | Mitigation |
|---|---|---|
| Governance by committee only | No accountability | Assign individual owners |
| Governance after the fact | Technical debt | Shift-left governance at design |
| Manual-only processes | Non-scalable | Automate DQ, classification, access review |
| Shadow data marts | Ungoverned proliferation | Enforce a certified data product model |
| No escalation path | Stale issues | Define SLA-backed escalation matrix |

---

## 6. Maturity Model

| Level | Description | Indicators |
|---|---|---|
| **1 - Initial** | Ad hoc, reactive | No catalog, no owners, inconsistent definitions |
| **2 - Developing** | Defined ownership, basic standards | Catalog exists, some DQ checks, partial lineage |
| **3 - Defined** | Org-wide policies, enforced standards | Full classification, DQ gates, RBAC enforced |
| **4 - Managed** | Measured and monitored | KPI dashboards, SLA reporting, audit cycles |
| **5 - Optimizing** | Continuous improvement, automation | ML-assisted classification, self-healing DQ |

---

## 7. Key Metrics (KPIs)

| KPI | Target | Frequency |
|---|---|---|
| % Data Assets with Assigned Owner | > 95% | Monthly |
| % Critical Fields with DQ Rules | 100% | Monthly |
| DQ Pass Rate (Critical Assets) | > 99% | Daily |
| % Assets Classified | > 98% | Monthly |
| Access Certification Completion Rate | 100% | Quarterly |
| Mean Time to Resolve DQ Incident | < 2 business days | Monthly |
| Lineage Coverage (governed assets) | > 90% | Monthly |
| Policy Exceptions Open > 30 days | 0 | Weekly |

---

## 8. Tooling Reference

| Function | Primary Tool | Supporting Tools |
|---|---|---|
| Data Catalog & Governance Hub | **Collibra Data Intelligence Cloud** | Snowflake Native Catalog, Unity Catalog |
| Business Glossary | **Collibra Business Glossary** | — |
| Data Quality | **Collibra DQ (Owl Analytics)** | Great Expectations, dbt tests, Soda |
| Lineage | **Collibra Lineage** | dbt, OpenLineage, Snowflake lineage |
| Governance Workflows | **Collibra Workflow Engine** | ServiceNow (for IT change management) |
| Access Management | Snowflake RBAC/ABAC, Databricks Unity Catalog | Collibra Access Governance |
| Policy Enforcement | **Collibra Policy Manager** | OPA, Immuta, Privacera |
| Monitoring & Alerting | **Collibra DQ dashboards** | Monte Carlo, Bigeye, custom BI dashboards |

---

*Document Owner: Chief Data Officer | Review Cycle: Semi-Annual*
