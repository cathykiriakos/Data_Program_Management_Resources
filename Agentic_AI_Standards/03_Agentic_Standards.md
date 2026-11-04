# Agentic AI Standards
## Binding Standards: Identity, Charter, Tools, Memory, Sandbox, Data, Consent

**Document Owner:** Chief AI Officer (CAIO) or the Data Program Management Lead where no CAIO exists
**Classification:** Internal: Binding Standard
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual, plus a review after any agent incident or when a dated fact in the landscape snapshot changes a requirement

> **Purpose:** These are the binding rules for every agent the organization builds, buys, or allows to touch its data. Each standard has an ID, a requirement in MUST or SHOULD language, a rationale, and an enforcement layer that names the control outside the model. Exceptions require written approval from the CAIO, are logged in the registry, and are reviewed quarterly.

---

## Table of Contents

1. [How to Read These Standards](#1-how-to-read-these-standards)
2. [Identity](#2-identity)
3. [Charter](#3-charter)
4. [Registry](#4-registry)
5. [Tool and MCP Governance](#5-tool-and-mcp-governance)
6. [Skill and Plugin Intake](#6-skill-and-plugin-intake)
7. [Memory](#7-memory)
8. [Secrets](#8-secrets)
9. [Sandbox and Egress](#9-sandbox-and-egress)
10. [Observability and Audit Log](#10-observability-and-audit-log)
11. [Kill Switch](#11-kill-switch)
12. [Spend Cap](#12-spend-cap)
13. [Model Selection and Version Pinning](#13-model-selection-and-version-pinning)
14. [Data Class Handling](#14-data-class-handling)
15. [Consent and Vulnerable Populations](#15-consent-and-vulnerable-populations)
16. [Equity Review and Human Oversight](#16-equity-review-and-human-oversight)
17. [Multi-Agent Handoffs](#17-multi-agent-handoffs)
18. [Conformance Checklist](#18-conformance-checklist)

---

## 1. How to Read These Standards

MUST means the requirement is binding and an exception needs written approval. SHOULD means the requirement applies unless the Agent Owner records a reason in the registry that the AI Risk Lead accepts. Tiers T1 to T4 are those in section 3.1.1 of the AI-First Strategy Addendum (`AI_FIRST_STRATEGY_ADDENDUM.md`). Where a standard applies to certain tiers only, it says so. The reasoning behind each standard is in the Best Practices (01), and the roles are in the Program Establishment guide (02).

The enforcement layer line is the core of each standard. A charter is a prompt, and a prompt does not enforce anything (see section 3 of 01). The line names where the bound is actually held: an identity provider, a sandbox, a proxy, a budget control, a workflow approval, a deterministic check, or a review that a person performs. Where the only enforcement is a human review, the line says "manual" so nobody believes a technical control exists.

Time-sensitive facts such as protocol revisions, regulatory dates, and provider retirement schedules are in `LANDSCAPE_SNAPSHOT.md` with sources in `SOURCES.md`. The standards below say to consult the snapshot and do not repeat its facts.

Standards that appear in the charter's `data_classes`, `tools`, and `approval_gates` fields are mirrored in the registry row, and `tools/agent_lint.py` compares them. Section 18 maps each standard to the lint check that tests it, or to "manual" where none does.

### 1.1 Tier Matrix

This is the one table of tier requirements. Every other document in this pillar (02, 04, 05, the schema and template comments, the workshop) points here and must agree with it. A cell marked "linted" is checked by `tools/agent_lint.py`. Every other cell is manual, which means a person checks it at review or audit.

| Tier | Assessor | Second reviewer | Approval gates | Review cadence | Kill switch drill | Sampling |
|---|---|---|---|---|---|---|
| T1 | Assessor agent required (linted). Never the only gate | A named human reviewer who is not the owner or the builder | At least one, even on a read-only agent (linted) | Monthly owner log review and self-check, with assessor sampling each cycle | Quarterly | 25 percent of runs, minimum 50, plus forced items |
| T2 | Assessor agent required (linted). Never the only gate | A named human approver who is not the owner | At least one (linted) | Monthly owner log review and self-check, with assessor sampling each cycle | Quarterly | 20 percent of runs, minimum 30, plus forced items |
| T3 | An assessor agent or a named second reviewer (linted). The full track uses both | Named, and not the owner (linted). On the full track this person also reads the assessor's findings | One for every write tool (linted). A read-only T3 agent may have none | Monthly owner log review and self-check | Twice a year | 10 percent of runs, minimum 20, plus forced items. With no assessor agent the second reviewer samples the same way |
| T4 | Optional | None. The owner reviews (see the T4 caveat below) | Not required. A T4 agent runs with no production data and has no external write | Monthly owner log review and self-check | Yearly | The owner reads a small sample each month. No forced items |

Notes on the matrix.

- Forced items are every run with an external write or send, an error, a refusal, or an approval override. They are added to the random sample in full. A cap on forced items is not allowed, because the runs most likely to hold a failure must not be dropped to fit a number. The percentages and minimums are starting values: an organization MAY raise them and MUST NOT lower them without recording the reason in the assessor charter's Sampling Rule.
- The lean track (02, section 2) is T3 and T4 only. T3 on the lean track needs an assessor agent or a named second reviewer. The full track adds both an assessor agent and a named second person for sampled findings.
- An assessor that reads production data is T3 or higher. T4 is for an environment with no production data (AGT-SBX-01), so a T4 assessor can only read test material.
- T4 caveat: the owner reviews a T4 agent, so the check that `second_reviewer` differs from `owner` applies to T1 to T3 only. Nobody else sees a T4 agent's work, which is why it is kept to a sandbox with no production data.
- The linter reads documents. It does not check reviewer independence for T1 and T2, cadences, sampling rates, drills, or the tier exception in AGT-DAT-01. Those are manual.

---

## 2. Identity

### AGT-ID-01: One Dedicated Identity per Agent

**Requirement:** Each agent MUST run under its own identity in the organization's identity provider. An agent MUST NOT use a staff member's login, a shared account, or a personal token. The identity name MUST be recorded in the charter's `identity` block and the registry.

**Rationale:** A borrowed credential hides the agent's actions among a person's, cannot be revoked without disrupting that person, and gives an attacker the person's full access.

**Enforcement layer:** Identity provider. The account is created by the IT or platform contact, and a monthly comparison of the provider's application and service account list against the registry finds any agent running under another identity (manual check, see AGT-REG-02).

### AGT-ID-02: Least Privilege Scopes

**Requirement:** An agent's scopes MUST be the minimum needed for its stated purpose. An agent SHOULD hold read scopes by default. A write scope MUST be listed in the charter with its access marked write, and MUST have an approval gate for T1 to T3 agents. Where the platform offers a draft or propose scope separate from a send or commit scope, the agent MUST be given the draft scope unless the charter justifies more.

**Rationale:** The scope decides what a manipulated agent can do. Splitting functions across agents keeps any one compromise small.

**Enforcement layer:** Identity provider scopes and application permissions. The charter's Tools and Scopes section and the registry's `tools` list state the same write tools, and the mirror check fails when they differ.

### AGT-ID-03: Credential Lifetime and Lifecycle

**Requirement:** Agent credentials SHOULD be short-lived and no longer than the longest single task. Where long-lived keys are unavoidable, the lifetime MUST be recorded in `max_token_lifetime_minutes`, the key MUST be rotated on a schedule set by the owner, and the key MUST live in a secrets store (AGT-SEC-01). The identity MUST be disabled when the agent is retired or when its `sunset_date` passes without a renewal decision. When an agent's owner leaves, the agent MUST be reassigned to a named owner or paused.

**Rationale:** Short lifetimes shrink the window for stolen credentials. Identities that outlive their agents become unmonitored access paths.

**Enforcement layer:** Identity provider token policy and a calendar or ticket for rotation and sunset review. The linter checks that `sunset_date` is present and not in the past, and that `review_date` is not in the past. Token lifetime and disabling the identity are manual.

---

## 3. Charter

### AGT-CH-01: Every Agent Has a Charter That Passes the Linter

**Requirement:** Every agent MUST have a charter based on `templates/SOUL.template.md`, stored beside its registry row. The charter MUST carry all required frontmatter fields and all required sections, and MUST pass `python tools/agent_lint.py` before the agent goes live and before every change is merged. The tier matrix in section 1.1 sets what each tier requires. In short, T1 and T2 charters MUST name an assessor agent and at least one approval gate. A T3 charter MUST name an assessor agent or a named second reviewer who is not the owner. A T4 charter MAY name neither.

**Rationale:** A written charter makes the agent's intent checkable and gives the Agent Owner something to sign. The linter catches missing parts early and applies the tier rules from the addendum.

**Enforcement layer:** `tools/agent_lint.py` in CI or as a required step before approval. The linter tests the document, not the systems it describes, which is why AGT-CH-02 exists.

### AGT-CH-02: Every Bound Names a Control Outside the Model

**Requirement:** Each bound stated in a charter (authority limits, forbidden actions, data limits, tool scopes, approval gates, memory rules, failure behavior) MUST name the control outside the model that enforces it, using the "Enforced by" line in the template. A bound with no such control MUST be marked as unenforced. Policy MUST NOT be placed in the Voice section or in any persona file. Every entry in the charter's `enforcement_refs` MUST be a key in the registry's `enforcement` map. The map MAY hold more keys than the charter lists.

**Rationale:** A charter is injected context and can be overridden by hostile content or a poisoned memory. Only a control outside the model holds when the model does not comply.

**Enforcement layer:** The registry `enforcement` map, checked against the real system at audit by someone other than the owner (Auditing Guide, 04). The linter checks that `enforcement_refs` is present and that every entry has a matching key in the row's `enforcement` map (it does not require the reverse). Whether the named control exists is manual.

### AGT-CH-03: Review and Sunset Dates

**Requirement:** A charter MUST carry a `review_date` that is not in the past and a `sunset_date`. The Agent Owner MUST review the charter at each review date and either renew it with a new date or retire the agent. A charter MUST NOT contain a secret, key, or password.

**Rationale:** An agent no one reviews drifts. A secret in a charter is readable by the model and by anyone with file access.

**Enforcement layer:** `tools/agent_lint.py` date and secret checks, run in CI on a schedule so that expiry raises a failure.

---

## 4. Registry

### AGT-REG-01: One Registry Row per Agent Before First Run

**Requirement:** Every agent MUST have a registry row in `registry_row.yaml` beside its charter, or an entry keyed by `agent_id` in a `registry.yaml` for a multi-agent folder, before it first runs against any non-test data. The row MUST follow `templates/registry.schema.yaml`, including tier, identity, tools, data classes, approval gates, spend cap, model pin with family, model review answers, enforcement map, and status. Every agent found by discovery MUST be registered or retired (see 02, section 4).

**Rationale:** An agent that is not listed cannot be owned, reviewed, or retired. The registry is the organization's answer to funders, boards, and insurers about what runs.

**Enforcement layer:** `tools/agent_lint.py` registry checks for row completeness, a `model` mapping with all four fields, and a `tier` equal to the charter's. The linter does not check `identity` or `model_review` in the row. The discovery procedure in the Program Establishment guide (02) for completeness of the inventory (manual).

### AGT-REG-02: Registry Reconciliation

**Requirement:** The AI Risk Lead MUST reconcile the registry against the identity provider's service accounts and application registrations, the connected-app lists of core systems, and billing records at least quarterly. Each difference MUST be resolved as adopt, replace, or retire.

**Rationale:** Shadow agents appear between reconciliations and nowhere else will reveal them.

**Enforcement layer:** Manual reconciliation with a dated record in the registry log. Identity provider exports reduce the effort.

### AGT-REG-03: Registry Status and Assessment Record

**Requirement:** The row's `status` MUST be one of proposed, active, suspended, or retired, and MUST be changed when the agent's state changes. `last_assessed` MUST be updated after each review. An agent whose `last_assessed` is older than its review cadence MUST be flagged to the AI Risk Lead.

**Rationale:** A status that is out of date makes the inventory untrustworthy, and a stale assessment date shows a review that did not happen.

**Enforcement layer:** `tools/agent_lint.py` checks that `status` is present and is one of the four values. Currency of the value is manual.

---

## 5. Tool and MCP Governance

### AGT-TOOL-01: Tool Allowlist

**Requirement:** An agent MUST be able to call only tools listed in its charter and registry row. Tools MUST be configured by an administrator and MUST NOT be added by the agent or by content the agent reads. Each tool MUST be marked read or write, and anything that sends, posts, edits, deletes, or pays MUST be marked write.

**Rationale:** The set of tools is the set of actions an attacker can trigger.

**Enforcement layer:** Runtime or gateway tool allowlist configured by the administrator, plus identity provider scopes. The linter compares write tools between charter and registry.

### AGT-TOOL-02: Pinned and Reviewed Tool Servers

**Requirement:** Each tool server, including any server speaking the Model Context Protocol (MCP), MUST be pinned to a specific version or a verified digest and MUST be reviewed before first use and at each version change. The review MUST read what the tool does, what it can reach, and what it sends out. Tool descriptions and schemas MUST be treated as untrusted input that can contain instructions, and changes to them MUST trigger re-review.

**Rationale:** A tool server is code that runs with your agent's access. Tool descriptions are read by the model and have been used to carry hidden instructions.

**Enforcement layer:** Lockfile, container image digest, or runtime configuration that refuses unpinned versions. Review record in the change log (05). Manual for the review itself.

### AGT-TOOL-03: Authorization for Remote Tool Servers

**Requirement:** A remote tool server MUST authenticate the agent using the authorization method defined by the current revision of the MCP specification or an equivalent standard method, with tokens limited to that server (audience-bound) and to the scopes the agent needs. A server MUST NOT receive a token issued for a different service. The current specification revision and its requirements are in `LANDSCAPE_SNAPSHOT.md`.

**Rationale:** Token reuse across services lets one compromised server act against another system as the agent.

**Enforcement layer:** Identity provider and the tool server's own authorization configuration. Manual review of the configuration at intake.

### AGT-TOOL-04: No Untrusted Local Process Servers

**Requirement:** An agent MUST NOT launch a tool server as a local process (for example over standard input and output, known as STDIO) from a source the organization has not reviewed. Locally launched servers MUST come from a pinned, reviewed package, run inside the sandbox of AGT-SBX-01, and run with no more access than the agent has. Configuration files that define tool servers MUST be treated as code, change-controlled, and not editable by the agent. Configuration found in a downloaded project or repository MUST NOT be trusted automatically.

**Rationale:** A locally launched server executes commands on the host. Several reported flaws in agent tooling arise from configuration that causes a command to run, and automatic loading of configuration from untrusted projects has been used as an attack path.

**Enforcement layer:** Sandbox and host policy that restricts which executables can launch, plus file permissions that make the tool configuration read-only to the agent.

### AGT-TOOL-05: Read Versus Write Separation

**Requirement:** An agent that reads content from outside the organization (inbound email, web pages, uploaded files, public posts) MUST NOT also hold a write or send tool unless a human approval gate stands between the two. The design SHOULD split reading and acting into two agents.

**Rationale:** An agent that reads untrusted text, holds private data, and can send data out can be turned against its owner. Removing any one of those removes most of the risk.

**Enforcement layer:** Identity scopes and gateway rules per agent, plus the approval gate. The Auditing Guide (04) tests this combination.

---

## 6. Skill and Plugin Intake

### AGT-SKL-01: Approved Sources Only

**Requirement:** Skills, plugins, extensions, and prompt packs MUST come from an internal allowlist. An agent that touches client data MUST NOT install from a public registry or marketplace at run time, and MUST NOT install anything on its own. An item from outside the allowlist MUST go through intake (AGT-SKL-02) before it is added.

**Rationale:** Skills carry instructions and sometimes code, and the agent runs them with its own access. Public registries have contained malicious items, and install-time trust is the main practical gap.

**Enforcement layer:** Runtime setting that disables or restricts installation to the allowlist, and filesystem permissions that stop the agent from writing to its own skill directory.

### AGT-SKL-02: Intake Review and Pinning

**Requirement:** Intake for a skill or plugin MUST include: identifying the publisher; reading all instructions, scripts, and install steps; checking what it requests access to, what network destinations it contacts, and what it writes; testing it in the sandbox with no client data; recording its version or content digest; and naming who approved it. Updates MUST repeat the review for changed content. Instructions that tell a user or agent to run a command to install a "prerequisite" MUST be treated as a warning sign.

**Rationale:** Most malicious skills depend on a person or an agent following setup instructions without reading them.

**Enforcement layer:** Change record in the Config and Change Management guide (05), a content digest or version pin in the runtime configuration, and a sandbox with no client data for the test. Review is manual.

---

## 7. Memory

### AGT-MEM-01: Provenance

**Requirement:** Each durable memory entry MUST record its source (user, document, tool result, or run) and the date written. Entries derived from untrusted content MUST be marked as such and MUST NOT be treated as instructions. Where the runtime cannot record provenance, the agent MUST NOT keep durable memory.

**Rationale:** Provenance lets a reviewer find and remove poisoned entries and lets the agent treat low-trust entries as data.

**Enforcement layer:** Memory store schema or runtime setting that requires source fields, and write permissions on the memory store. Manual review where the runtime lacks the feature.

### AGT-MEM-02: Review

**Requirement:** For T1 to T3 agents, durable memory MUST be reviewed on the schedule set in the charter, and at least at each monthly review. The reviewer MUST be someone other than the agent. New memory written by an agent that reads untrusted content SHOULD be held for review before it is used in later runs.

**Rationale:** Memory is where a single bad input becomes a standing instruction.

**Enforcement layer:** Review step in the Auditing Guide (04), and a held-for-review queue in the memory store where the runtime supports it. Manual otherwise.

### AGT-MEM-03: Expiry and Purge

**Requirement:** The charter MUST state a retention period for memory. Entries older than that period MUST be deleted. Client data MUST NOT be stored in memory unless the charter and the data class rules (AGT-DAT-01) allow it. Memory MUST be purged when the agent is retired and on a verified client deletion request. Memory MUST NOT be shared between agents unless both charters permit it.

**Rationale:** Retention without limit compounds both privacy and poisoning risk.

**Enforcement layer:** Scheduled deletion job or store-level time-to-live, and the decommissioning checklist. The job's existence is verified at audit.

---

## 8. Secrets

### AGT-SEC-01: Secrets Stay Out of Agent Reach

**Requirement:** Keys, tokens, passwords, and connection strings MUST be kept in a secrets manager or the platform's secret store and injected at run time. They MUST NOT appear in a charter, a prompt, a skill, a memory file, a tool description, a repository, or a log. The agent SHOULD receive a credential only for the call it is making and SHOULD NOT be able to read the secret store.

**Rationale:** Anything the model can read, a manipulated model can disclose.

**Enforcement layer:** Secrets manager access policy, secret scanning on repositories, and log redaction rules. The linter's secret pattern check covers charters and registry rows only.

### AGT-SEC-02: Rotation and Exposure Response

**Requirement:** Secrets MUST be rotated on the schedule set by the owner and immediately after any suspected exposure, including a secret that appeared in a log, a prompt, or an agent output. A rotation record MUST be kept.

**Rationale:** An exposed secret stays valid until someone changes it.

**Enforcement layer:** Secrets manager rotation policy and incident procedure in the incident addendum (`AGENT_INCIDENT_RESPONSE_ADDENDUM.md`).

---

## 9. Sandbox and Egress

### AGT-SBX-01: Isolated Execution

**Requirement:** An agent that can run code, shell commands, or file operations MUST do so in an isolated environment (a container, virtual machine, or equivalent) with only the files it needs, no access to other agents' files or to the host, and no access to credentials beyond its own. T4 agents MUST run only in an environment with no production data.

**Rationale:** Code execution is the highest-impact capability. Isolation limits what a hijacked agent can reach.

**Enforcement layer:** Container or virtual machine profile, file mounts, and host policy. Verified by inspection at audit.

### AGT-SBX-02: Egress Allowlist

**Requirement:** Outbound network access from an agent's environment MUST be limited to an allowlist of destinations the agent needs. All other destinations MUST be blocked and attempts MUST be logged. Agents that handle client data MUST NOT be able to reach arbitrary web addresses. Rendering of remote content, such as automatic image loading in agent output, MUST be disabled where the agent handles client data.

**Rationale:** Exfiltration needs a destination. Blocking unlisted destinations stops many attacks even when the model has been manipulated.

**Enforcement layer:** Network firewall, egress proxy, or platform network policy.

---

## 10. Observability and Audit Log

### AGT-OBS-01: Log Every Tool Call and Decision

**Requirement:** Each agent MUST produce a log held outside the agent's control that records, for every run: the agent identity, time, the inputs by reference, each tool call with its arguments and result status, each approval request and the human decision with the approver's identity, the model and version used, and cost. The log MUST be tamper-evident or write-only for the agent. The log MUST NOT be a store of client data beyond what the data class rules allow.

**Rationale:** Without a log, an incident cannot be scoped, a review cannot sample, and an audit cannot test anything. Accountability depends on a record of who approved what.

**Enforcement layer:** Gateway or runtime logging to a store the agent cannot modify, with access limited to the owner, reviewer, and AI Risk Lead.

### AGT-OBS-02: Retention and Review

**Requirement:** Logs MUST be kept for a period set by the organization's records policy, and not shorter than one full review cycle plus the time needed to investigate an incident. The Agent Owner MUST look at the log at least monthly. Alerts MUST exist for spend threshold, repeated denied actions, and egress denials.

**Rationale:** Logs that nobody reads or that expire before they are needed do not protect anything.

**Enforcement layer:** Log store retention policy and alert rules. The monthly review is recorded in the registry (manual).

---

## 11. Kill Switch

### AGT-KIL-01: Stop Without the Agent's Cooperation

**Requirement:** Each agent MUST have a documented way to stop it that does not depend on the agent obeying an instruction. At minimum the procedure MUST disable the agent's identity, revoke or expire its tokens, and halt any scheduled or queued runs. The charter or registry MUST name who may trigger it and how, and at least two people MUST be able to.

**Rationale:** An agent that has been manipulated may ignore a request to stop. Access control is the stop that holds.

**Enforcement layer:** Identity provider account disable, token revocation, and runtime stop command, held by named people.

### AGT-KIL-02: Drill Cadence

**Requirement:** The kill switch MUST be tested before go-live and then at the cadence in the tier matrix (section 1.1): quarterly for T1 and T2, twice a year for T3, yearly for T4. A drill MUST confirm the agent can no longer act, and the time taken MUST be recorded. A failed drill MUST be fixed and repeated.

**Rationale:** An untested stop procedure often fails when needed, because credentials were renamed, people left, or a second path to the system was added.

**Enforcement layer:** Calendar entry owned by the AI Risk Lead and a dated drill record in the registry log (manual).

---

## 12. Spend Cap

### AGT-SPD-01: Cap Enforced Outside the Agent

**Requirement:** Each agent MUST have a monthly spend cap recorded in the registry as `spend_cap_usd_month`. The cap MUST be enforced by the model provider's budget limit, a gateway or proxy quota, or the platform's cost controls, and not by the agent. The cap MUST include model calls, tool services that bill by use, and compute.

**Rationale:** A loop, a retry storm, or an attack can generate cost faster than a person reads reports.

**Enforcement layer:** Provider budget limit or proxy quota that stops calls at the cap.

### AGT-SPD-02: Alerts and Rate Limits

**Requirement:** An alert MUST fire to the Agent Owner before the cap is reached, and a rate or concurrency limit SHOULD bound the cost of a runaway loop within a single hour. A cap that is reached MUST be treated as an event to review before it is raised.

**Rationale:** An alert gives a chance to act before the stop, and a rate limit protects against fast failures that a monthly cap would permit.

**Enforcement layer:** Provider alerting and gateway rate limits.

---

## 13. Model Selection and Version Pinning

### AGT-MOD-01: Model Review Before Approval

**Requirement:** Before an agent is approved, the model MUST be reviewed for provenance, licence terms for the organization's use, data handling terms (retention, training use, access by the provider), data residency, and fit for the data classes in use. For hosted models handling regulated data, a vendor agreement that covers the data MUST be in place. For open-weight models, the weights MUST come from the publisher's official source, MUST have their checksums verified, and SHOULD use file formats that do not execute code on load. The licence file for the exact version MUST be read and filed. The answers MUST be recorded in the registry. Current licence and provider facts are in `LANDSCAPE_SNAPSHOT.md` and MUST be re-checked at each review.

**Rationale:** The model decides where data goes and under what terms. Licence terms differ across families and change across versions.

**Enforcement layer:** Procurement and vendor review (addendum E006 and E011), and an artifact store or hash check for open-weight files. Manual review of terms.

### AGT-MOD-02: Pin the Version

**Requirement:** The registry MUST record `provider`, `id`, `pinned_version`, and `family` for each model. Production agents MUST call a pinned version and MUST NOT use a moving alias. A version change MUST pass the change path in the Config and Change Management guide (05), including re-running the saved test cases. The Agent Owner MUST track the provider's retirement notices and start migration when a notice is received.

**Rationale:** A silent change behind an alias changes behavior with no change in your files. A retired model stops the agent.

**Enforcement layer:** Runtime or gateway configuration that rejects unpinned model identifiers, and a tracked list of retirement dates.

### AGT-MOD-03: Assessor Independence

**Requirement:** An assessor agent MUST run on a different model family than the agent it reviews, and the registry MUST record both families. An assessor MUST NOT be the only gate for a T1 or T2 agent or for any external write.

**Rationale:** Model judges share blind spots and favor their own family's output. They are triage aids and not gates.

**Enforcement layer:** `family` fields in the registry rows, and the approval gate for the action. The Auditing Guide (04) states the limits.

### AGT-MOD-04: Exit Plan for Hosted and Open-Weight Models

**Requirement:** The registry or program file SHOULD record how the agent would move to another model: where prompts, tool definitions, and test cases are stored, and who would do the work. Model identifiers SHOULD live in configuration.

**Rationale:** Lock-in and provider change are certain over the life of an agent.

**Enforcement layer:** Repository structure and configuration. Manual review.

---

## 14. Data Class Handling

### AGT-DAT-01: Classify and Limit

**Requirement:** Each agent MUST declare in `data_classes` every class it may read or write, and MUST NOT touch any class not declared. The classes MUST be mapped to the organization's data classification policy. The table sets the minimum handling for the classes that social-sector agents most often meet. An organization MAY add classes but MUST NOT weaken the minimums.

| Data class | Minimum handling for agents |
|---|---|
| Client | Allowed only for an agent whose purpose requires it. Own identity, egress allowlist, no use of models whose terms allow training on inputs, no storage in memory without charter permission, logging that does not copy the data. Tier T2 or higher for decisions about the person. |
| Health | T1 or T2 only. A vendor agreement that covers the data MUST exist before the first use, and the model and tool vendors MUST be inside it. Minimum necessary data. No consumer-grade tools. |
| Education | Tier T2 or higher. Access only as the education records rules and the institution's agreements allow, and only for the purposes they permit. |
| Immigration | Excluded from agent use by default. An exception requires CAIO approval, a legal review, and a recorded assessment of the harm if the data is exposed. |
| Safety sensitive (survivors of violence, people in hiding, protected locations, informants) | Excluded from agent use by default. An exception requires CAIO approval, a recorded safety assessment, and a documented override under AGT-CON-03. Location and contact data MUST NOT be sent to a hosted model. |
| Financial and donor | Allowed for a purpose-bound agent with draft-only actions. Payment actions need a gate for every transaction. |
| Staff and personnel | Not in scope for agents without HR and legal approval. |
| Public and internal | Allowed for T3 and T4 agents. |

**Tier exception for draft-only donor agents.** A draft-only agent (no send tool and no external write) limited to non-sensitive supporter contact and gift data MAY run as T3 when the program lead records the exception. The exception is recorded as a `tier_exception` field in the registry row (reason, approver role, date) and is restated in the charter's Authority section. It does not cover wealth or capacity ratings, free-text relationship notes, or any health, immigration, minor, or safety-sensitive record, and it ends if the agent gains a send tool or any external write. It does not remove the equity review in AGT-EQ-01. The linter does not check `tier_exception`: the check is manual, and the AI Risk Lead confirms it at audit.

**Rationale:** A breach of the sensitive classes can put a person in danger. Defaults should be set to exclude rather than to allow.

**Enforcement layer:** Data platform permissions, identity scopes, and query filters that withhold the excluded classes from the agent's access. The linter compares `data_classes` between charter and registry. The `tier_exception` record is manual.

### AGT-DAT-02: Minimize and Mask

**Requirement:** An agent SHOULD receive the minimum fields it needs. Where a task can work with masked or pseudonymous values, the agent MUST be given those values and not the originals. Free-text fields that may hold sensitive details SHOULD be excluded unless the task requires them.

**Rationale:** Data an agent never sees cannot be leaked or misused.

**Enforcement layer:** Views, masking policies, or an intermediate service that serves only permitted fields.

---

## 15. Consent and Vulnerable Populations

### AGT-CON-01: Consent Covers the Use

**Requirement:** Before an agent processes client data, the organization MUST confirm that the consent given by the client, or the legal basis relied on, covers this use. Consent language MUST say, in plain terms and in the languages the organization serves, that AI tools may process the person's information, what they do with it, whether a person reviews results, whether data goes to an outside provider, and how to object. Consent for service delivery MUST NOT be assumed to cover use of data to train or tune a model. Clients MUST be able to object, and an objection MUST route the person's records out of agent processing without loss of service.

**Rationale:** A person who agreed to receive help did not necessarily agree to have their story processed by software run by a third party. Trust in the service depends on honoring the difference.

**Enforcement layer:** A consent flag in the client record that the data platform uses to filter records out of the agent's access, and an objection procedure owned by the program. Manual review of consent language by the AI Risk Lead and counsel.

### AGT-CON-02: Protected Populations Need Extra Approval or Exclusion

**Requirement:** Records of the following populations MUST NOT be processed by an agent without the extra approval described here, and MUST be excluded where an exclusion is stated:

| Population | Rule |
|---|---|
| Children and minors | Agent processing requires approval of the AI Risk Lead and the program head, and guardian consent where the law or the program's terms require it. Decisions about the child, such as eligibility or risk flags, MUST NOT be made or recommended by an agent without human review of every case. |
| Immigrants and people with uncertain status | Excluded by default (see AGT-DAT-01). |
| Survivors of violence, people in hiding | Excluded by default (see AGT-DAT-01). |
| Patients and people receiving health services | Allowed only on a T1 or T2 agent with the vendor agreement in AGT-DAT-01, with human review of any recommendation. |
| People with limited capacity to consent, and people in crisis | Agent use limited to tasks that do not rely on their consent. Human review of every output that reaches them. |
| Any group the program names as at risk of serious harm if exposed | Treated as protected under this standard. |

An organization MAY add populations and MUST NOT remove those listed.

**Rationale:** The people these programs serve often cannot easily object, and the cost of error falls on them.

**Enforcement layer:** Data platform filters keyed to a population flag, identity scopes that withhold the records, and approval gates for any permitted case. Population flag accuracy is checked manually at audit.

### AGT-CON-03: Who May Override

**Requirement:** An exclusion or extra-approval rule in AGT-CON-02 or AGT-DAT-01 MAY be overridden only by the CAIO together with the AI Risk Lead, in writing, for a named agent, a named purpose, and a fixed period. Overrides for children and for safety-sensitive data MUST also have the written agreement of the head of the program concerned and, where the organization has counsel, its legal review. Each override MUST be logged in the registry and reported to the board at its next meeting. An Agent Owner, an approver, or a vendor MUST NOT grant an override.

**Rationale:** The people who want the agent to work are least able to judge the risk to the people it affects.

**Enforcement layer:** Registry log of overrides, with the override date and expiry written in the charter, and board reporting. Manual.

---

## 16. Equity Review and Human Oversight

### AGT-EQ-01: Equity Review Before Touching Decisions About People

**Requirement:** Before an agent is used for or in support of a decision about a person (access to a service, priority, flagging, outreach, eligibility, or what a person is told about their own case), the Agent Owner MUST complete an equity review. The review MUST name who could be harmed or excluded, test the agent's outputs across the groups the organization serves, and record the date, reviewer, findings, and actions in the charter under Authority. The review MUST be repeated when the model, prompt, data source, or population changes, and at each scheduled review.

**Rationale:** Systems that work on average can fail specific groups, and the people affected rarely get the chance to say so.

**Enforcement layer:** Manual review by the AI Risk Lead before approval. The charter record is checked at audit.

### AGT-HUM-01: Gates on High-Impact Actions

**Requirement:** An approval gate MUST stand before any action that leaves the organization, is hard to reverse, or affects a person's access to a service, money, housing, or status. Gates SHOULD NOT be placed on low-impact reversible actions, which are sampled instead. The approval request MUST show the proposed action and data in a form the approver can judge, and MUST NOT rely on a description written only by the agent. The approver's identity and decision MUST be logged.

**Rationale:** Few gates, each taken seriously, protect better than many gates that are not read.

**Enforcement layer:** Workflow approval step in the runtime or business system that blocks the action until a named person approves, and the approval log (AGT-OBS-01).

---

## 17. Multi-Agent Handoffs

### AGT-MUL-01: Each Agent Governed on Its Own

**Requirement:** Where agents hand work to other agents, the principles in section 3.5.1 of the addendum (`AI_FIRST_STRATEGY_ADDENDUM.md`) apply and MUST be met. In addition, each agent in the chain MUST have its own identity, charter, and registry row, and a subagent MUST NOT receive credentials or scopes from its orchestrator.

**Rationale:** Trust that flows downward through a chain turns one compromise into all of them.

**Enforcement layer:** Separate identities and scopes per agent in the identity provider, and registry rows per agent.

### AGT-MUL-02: Handoff Content Is Untrusted Input

**Requirement:** Messages from one agent to another MUST be logged under AGT-OBS-01 and SHOULD be limited to structured fields. The receiving agent MUST treat free-text content from another agent as data and not as instructions. A handoff that carries client data MUST be allowed by the receiving agent's declared data classes.

**Rationale:** An agent that has been manipulated can pass the manipulation to the next agent in plain text.

**Enforcement layer:** Schema validation at the handoff point, gateway logging, and each receiving agent's own scopes and data class limits.

---

## 18. Conformance Checklist

The linter `tools/agent_lint.py` tests documents and not live systems. A pass means the charter, the registry row, and the tier rules are consistent. It does not mean the controls exist. The checks named in the table are those the tool reports: frontmatter (required fields), section (required sections), tier (tier rules, including a second reviewer who is not the owner), date (review and sunset dates), secret (charters and registry rows), placeholder (a left-over double-brace placeholder in a charter or row), registry (row completeness, model mapping, status value), mirror (agreement between charter and row on tier, write tools, data classes, approval gates, and enforcement references), and family (assessor independence). Where a standard has no matching check, the column says manual, and the audit procedure in the Auditing Guide (04) is the test.

| Standard | Topic | Lint check that tests it | Remaining test |
|---|---|---|---|
| AGT-ID-01 | Dedicated identity | frontmatter (identity block present in the charter) | manual: identity provider comparison, and the registry `identity` block is not checked |
| AGT-ID-02 | Least privilege | mirror (write tools), tier (write tool needs gate) | manual: scope inspection |
| AGT-ID-03 | Credential lifetime and lifecycle | frontmatter, date (sunset_date present and not past) | manual: token lifetime, rotation, and disabling the identity |
| AGT-CH-01 | Charter passes linter | frontmatter, section, tier, placeholder | none |
| AGT-CH-02 | Bound names a control | frontmatter (enforcement_refs present), mirror (each ref has a key in the row's enforcement map; extra row keys allowed) | manual: content and real-system check |
| AGT-CH-03 | Review and sunset dates, no secrets | date, secret | none |
| AGT-REG-01 | Registry row | registry (row completeness, tier, model mapping), mirror (tier), placeholder | manual: discovery completeness, `identity` and `model_review` content |
| AGT-REG-02 | Reconciliation | manual | manual |
| AGT-REG-03 | Status and assessment record | registry (status present and one of the four values) | manual: currency, and `last_assessed` |
| AGT-TOOL-01 | Tool allowlist | mirror (write tools) | manual: runtime configuration |
| AGT-TOOL-02 | Pinned and reviewed tool servers | manual | manual |
| AGT-TOOL-03 | Remote tool authorization | manual | manual |
| AGT-TOOL-04 | No untrusted local process servers | manual | manual |
| AGT-TOOL-05 | Read and write separation | manual | manual: design review of whether the agent reads outside content and also holds a write tool |
| AGT-SKL-01 | Approved sources only | manual | manual |
| AGT-SKL-02 | Intake review and pinning | manual | manual |
| AGT-MEM-01 | Memory provenance | manual | manual |
| AGT-MEM-02 | Memory review | manual | manual |
| AGT-MEM-03 | Memory expiry and purge | manual | manual |
| AGT-SEC-01 | Secrets out of reach | secret (charters and registry rows) | manual: repositories, logs, store policy |
| AGT-SEC-02 | Rotation and exposure response | manual | manual |
| AGT-SBX-01 | Isolated execution | manual | manual |
| AGT-SBX-02 | Egress allowlist | manual | manual |
| AGT-OBS-01 | Log every call | manual | manual |
| AGT-OBS-02 | Retention and review | manual | manual |
| AGT-KIL-01 | Stop without cooperation | manual | manual |
| AGT-KIL-02 | Drill cadence | manual | manual |
| AGT-SPD-01 | Cap enforced outside agent | registry (spend_cap_usd_month present) | manual: provider setting. The charter's `spend_cap_ref` pointer is not checked |
| AGT-SPD-02 | Alerts and rate limits | manual | manual |
| AGT-MOD-01 | Model review | manual | manual: the `model_review` answers in the row are not checked |
| AGT-MOD-02 | Pin the version | registry (model is a mapping with provider, id, pinned_version, family) | manual: runtime rejects aliases |
| AGT-MOD-03 | Assessor independence | family | manual: an assessor is never the only gate |
| AGT-MOD-04 | Exit plan | manual | manual |
| AGT-DAT-01 | Classify and limit | mirror (data_classes) | manual: platform permissions, and the `tier_exception` record |
| AGT-DAT-02 | Minimize and mask | manual | manual |
| AGT-CON-01 | Consent covers the use | manual | manual |
| AGT-CON-02 | Protected populations | manual | manual |
| AGT-CON-03 | Who may override | manual | manual |
| AGT-EQ-01 | Equity review | manual | manual |
| AGT-HUM-01 | Gates on high-impact actions | mirror (approval_gates), tier (gate required by tier and for write tools) | manual: workflow blocks action |
| Tier matrix (section 1.1) | Assessor, second reviewer, gates, cadence, drills, sampling | tier (assessor, gates, second reviewer not the owner), mirror (tier equal in charter and row) | manual: T1 and T2 reviewer independence, cadence, drills, sampling, forced items |
| AGT-MUL-01 | Each agent governed on its own | registry (a row per agent) | manual |
| AGT-MUL-02 | Handoff content is untrusted | manual | manual |

Most standards are tested by people. That is the honest state of the art at this scale, and it is the reason the Auditing Guide (04) exists. Use the checklist at each review, and record in the registry which standards were tested, by whom, and how.
