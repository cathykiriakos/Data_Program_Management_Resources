# Agentic AI Best Practices
## Identity, Charters, Oversight, and Safe Operation of AI Agents

**Document Owner:** Chief AI Officer (CAIO) or the Data Program Management Lead where no CAIO exists
**Classification:** Internal: Program Standard
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual, plus a review after any agent incident or major runtime change

> **Purpose:** This document explains the practices behind the binding standards in the Agentic Standards (03). It is written for people who run small teams, hold sensitive client data, and answer to funders and boards. It covers how much freedom to give an agent, why a written charter is not a control, how to give each agent its own identity, where human approval earns its cost, and the mistakes that teams repeat.

---

## Table of Contents

1. [How to Use This Document](#1-how-to-use-this-document)
2. [The Autonomy Ladder](#2-the-autonomy-ladder)
3. [A Charter Is a Prompt](#3-a-charter-is-a-prompt)
4. [Agent Identity and Least Privilege](#4-agent-identity-and-least-privilege)
5. [Human Oversight Without Approval Fatigue](#5-human-oversight-without-approval-fatigue)
6. [Memory and Context Hygiene](#6-memory-and-context-hygiene)
7. [Prompt Injection and Data Exfiltration](#7-prompt-injection-and-data-exfiltration)
8. [The Equity Review Step](#8-the-equity-review-step)
9. [Choosing a Model](#9-choosing-a-model)
10. [Choosing a Runtime](#10-choosing-a-runtime)
11. [Social Sector Realities](#11-social-sector-realities)
12. [Anti-Patterns](#12-anti-patterns)
13. [Things Teams Usually Miss](#13-things-teams-usually-miss)

---

## 1. How to Use This Document

The pillar has three layers. This document gives the reasoning. The Program Establishment guide (02) says who does what and in what order. The Agentic Standards (03) are the binding rules, each with an ID such as AGT-ID-01. When a standard feels arbitrary, the matching section here should explain why it exists.

This pillar reuses the vocabulary of the AI-First Strategy Addendum (`AI_FIRST_STRATEGY_ADDENDUM.md`) instead of restating it. Risk tiers T1 to T4 are defined in section 3.1.1 of the addendum. The three boundary contracts (data, action, authority) are in section 3.3.1. Multi-agent principles are in section 3.5.1. The roles of CAIO and AI Risk Lead come from Part 6. This pillar adds one role, the Agent Owner, described in the Program Establishment guide (02).

Anything that changes quickly, such as regulation dates, standard versions, model lists, runtime maturity, and reported incidents, is kept in `LANDSCAPE_SNAPSHOT.md` and traced to primary sources in `SOURCES.md`. This document describes practice that should hold up when those facts change. Where a practice depends on a current fact, it says so and points to the snapshot.

---

## 2. The Autonomy Ladder

An agent is software that decides its own next step. The more steps it takes without a person looking, the more a single mistake costs, and the harder it is to notice the mistake. The sensible way to give an agent freedom is to raise it one rung at a time and to require evidence before each rise.

The addendum describes five stages of maturity for an organization, from Foundation to Multi-Agent. The ladder below describes the freedom granted to one agent, and it lines up with those stages. An organization at Stage 2 should not run an agent on a rung that belongs to Stage 4, because the controls that make the higher rung safe do not exist yet.

| Rung | What the agent may do | Addendum stage | Evidence needed to climb to the next rung |
|---|---|---|---|
| 0. Registered | Nothing in production. It exists in the registry, with an owner, so it is counted. | Stage 1, Foundation | Charter written, registry row complete, charter passes `tools/agent_lint.py` |
| 1. Answers | Reads approved sources and answers questions. Writes nothing outside its own conversation. | Stage 2, Chatbots | A sample of real conversations reviewed with no boundary breaches |
| 2. Prepares | Drafts, summarizes, and queues work for a person to approve. Cannot send, post, edit records, or spend money. | Stage 3, Workflows | Approvers accept most drafts without edits, and the rate is recorded |
| 3. Acts with approval | Performs external writes after a named person approves each one, or each batch. | Stage 3, Workflows | Gate decisions logged, no unapproved writes found in an audit of the log |
| 4. Acts within limits | Performs low-impact, reversible actions alone, inside hard limits, and is sampled afterward. High-impact actions still wait for a person. | Stage 4, Autonomous | Sampled review is clean over several cycles and the kill switch has been drilled |
| 5. Coordinates | Directs other agents. Each one keeps its own identity, charter, and limits. | Stage 5, Multi-Agent | Multi-agent principles in addendum 3.5.1 met |

Three points keep the ladder honest. First, climbing is a decision recorded in the registry, made by the Agent Owner and approved by whoever the program names for that tier, and not something that happens because the agent seems to be doing well. Second, stepping down is routine. If sampled work shows drift, drop the agent one rung while the cause is found. Third, most small-organization agents belong on rungs 1 to 3 and should stay there. A donor acknowledgment drafter that never sends anything is a good agent. An agent that sends acknowledgments on its own is a different, riskier agent that needs a different justification.

---

## 3. A Charter Is a Prompt

Every agent in this pillar has a charter, a Markdown file that states its purpose, owner, authority, forbidden actions, data classes, tools, approval gates, memory rules, assessor, and review dates. The template is `templates/SOUL.template.md`. A charter is useful because it makes intent explicit, gives reviewers something to check work against, and gives the Agent Owner something to sign.

A charter is also text that is given to a language model, and that fact limits what it can do. The model may read it, weigh it against everything else in its context, and still do something else. Hostile content in a web page, an email, a document, or a stored memory can talk the model out of its instructions. A charter that says "never send email" prevents nothing if the agent's account is able to send email. The sentence describes what the owner wants. The permission describes what can happen.

The practice that follows is simple and has no exceptions. Every bound in a charter must name the control outside the model that enforces it. A bound with no named control is a wish, and the charter should say so honestly instead of implying protection that does not exist. Typical enforcement layers are:

- an identity provider scope that grants only what the agent needs, so a forbidden action fails with an authorization error
- a sandbox or container profile that limits files, processes, and network
- an egress proxy or allowlist that limits where data can go
- a provider budget limit or proxy quota that stops spending
- an approval step in a workflow tool that a person must complete before an action runs
- a deterministic check in code, such as a schema validation or a limit on records changed per run

The template reflects this. Each charter section that states a bound carries an "Enforced by" line. The one section that is only guidance, Voice, says so.

The bridge between the prose and the control is the mirror check. Three harm-bearing facts appear twice, once in the charter and once in the agent's registry row: write-capable tools with their scopes, data classes, and approval gates. The linter, `tools/agent_lint.py`, fails when the two disagree. The check does not prove that the identity provider holds the scope the registry row names, because the linter cannot see the identity provider. What it does is stop the charter and the registry from drifting apart silently, and it forces a person to write down, in the registry's enforcement map, where each bound lives. The enforcement map is what an auditor then checks against the real system. The Auditing Guide (04) describes how.

Two fields avoid duplication. The model pin and the monthly spend cap live only in the registry row, and the charter points to them. Teams then edit each fact in one place.

Persona files deserve a specific warning. Some agent runtimes use a single file, often called a soul file, to hold personality, tone, opinions, and boundaries together. That layout invites people to put policy into the persona. Policy that lives only in a persona file is policy that a persona-level attack can remove. This pillar keeps voice in one short section of the charter and keeps every bound in a section with a named control.

---

## 4. Agent Identity and Least Privilege

Each agent has its own identity in the organization's existing identity provider. That identity is a service account, an application registration, or the equivalent in whatever system the organization already runs. It is never a staff member's login, a shared team mailbox password, or a personal access token from a staff account.

The reasons are practical. When an agent acts as a person, the audit log shows the person did it, and nobody can tell afterward which actions were the agent's. When that person leaves, the agent's access either disappears unexpectedly or, worse, persists because nobody remembers it exists. When the agent is compromised, the attacker holds the person's full access and not a narrow slice. And when a funder or insurer asks who authorized an action, "a staff member's credentials were used by software" is a poor answer.

Least privilege for an agent has four parts.

**Narrow scopes.** Grant the minimum set of permissions for the task, and prefer read scopes. If the agent drafts emails, give it a scope that creates drafts and not one that sends. If it reads a donor database, give it read access to the tables it needs and not the whole system. The choice between a draft scope and a send scope is the single most effective control in many small-organization agents, because it turns "the agent sent something wrong" into "the agent drafted something wrong that a person caught."

**Short-lived credentials.** Prefer tokens that expire within the length of a task over long-lived keys. Where the platform only offers long-lived keys, record the lifetime in the charter's `identity` block, rotate on a schedule, and keep the key in a secrets store and not in any file the agent can read.

**One agent, one identity.** Two agents sharing an account cannot be separated in the log, cannot be revoked independently, and cannot have different scopes. When an orchestrator delegates to a subagent, the subagent keeps its own identity and its own limits, and does not inherit the orchestrator's access. The addendum states this as "trust is not inherited" in section 3.5.1.

**A lifecycle.** The identity is created when the registry row is approved, reviewed at each review date, and disabled when the agent is retired or its sunset date passes without renewal. Disabling the identity is the first step in decommissioning, because it ends the agent's ability to act even if some other step is missed.

Cryptographic identity schemes for agents, such as signed agent cards or workload identity frameworks, are worth knowing about but are not needed until agents from different organizations start calling each other. A small team should get the basics right first: a separate service account, scoped, short-lived where possible, and logged.

---

## 5. Human Oversight Without Approval Fatigue

A human approval step is a control only while the human is paying attention. People who are asked to approve fifty actions a day approve them without reading, and the gate then costs time and gives false comfort. This is approval fatigue, and it is the most common way a well-designed oversight step fails in practice.

The design response is to gate few actions and make each one count. Government guidance on adopting agents also places the decision with the designers: the people who build the agent decide in advance which actions need sign-off, and the agent does not decide for itself.

Choose gates by looking at the action and not the agent. Good candidates are actions that:

- leave the organization, such as sending an email, posting publicly, or submitting a form to a funder
- are hard to reverse, such as deleting records, merging records, or issuing a payment
- affect a person's access to a service, money, housing, or status
- touch a protected population described in standard AGT-CON-02

Actions that are internal, reversible, and low in impact should not need a gate. They should be sampled later by the review step in the Auditing Guide (04). Sampling catches drift without making a person click through every item.

A gate works better when the approval screen shows what the person needs to decide. Show the proposed action, the data it uses, and the reason, in a form that fits on one screen. Batch similar low-risk items so one decision covers a clearly bounded set, and say how many items the batch holds. Never let the agent compose the only description of its own action that the approver sees, since an agent that has been manipulated will describe a bad action in a reassuring way. Where possible, show the raw outgoing message or the raw record change.

Measure the gate. If approvers accept nearly every request in seconds, either the gate is on the wrong action or the people have stopped reading. Both are findings. The KPIs in the KPI guide (06) include approval rate and time to decide for this reason.

Last, give approvers the right to say no without consequence and a way to flag an agent. An oversight culture that treats every rejection as friction will get rubber stamps.

---

## 6. Memory and Context Hygiene

Many agents keep notes between runs: a file of preferences, a database of past conversations, a summary of what happened last week. Memory makes an agent useful, and it also gives an attacker a durable place to plant instructions. Text written into memory once is read back in every later session, perhaps by a different user, long after the original source is gone. This is memory poisoning, and the agent does not experience it as an attack. It experiences it as something it remembers.

Four habits reduce the risk.

**Record provenance.** Every memory entry should say where it came from: which user, which document, which tool result, or which run. Entries that came from untrusted content (web pages, inbound email, uploaded files) are labeled as such and are never treated as instructions.

**Review before it sticks.** For T1 to T3 agents, new durable memory should be reviewable, either by a person on a schedule or by the assessor as part of sampling. An agent that writes memory unattended and is never checked is an unreviewed memory, and it is on the list of anti-patterns below.

**Expire and purge.** Memory has a retention period set in the charter. Entries older than the period are deleted. Client data does not belong in memory at all unless the charter says so and the data class rules allow it. When a client asks for deletion, or an agent is retired, the memory is part of what gets purged.

**Keep memory small and separate.** A short, curated set of facts is easier to review than a transcript archive. Memory for one agent is not shared with another agent unless the charters of both permit it, because shared memory is a path by which a compromise in one spreads to the other.

The same discipline applies to context in general. What an agent reads in a run is what it acts on. Pull in the minimum data the task needs, and do not give an agent a whole folder when it needs one file.

---

## 7. Prompt Injection and Data Exfiltration

A language model cannot reliably tell instructions from data. Any text the agent reads may contain instructions, and some of them will be followed. Prompt injection is the name for this problem, and it is not fixed by a better prompt. It has to be managed by limiting what a manipulated agent can do.

The risk is highest when an agent combines three things: access to private data, exposure to content from outside the organization, and a way to send data out. With all three, an attacker only needs to put text in front of the agent, for example in an inbound email or a web page, and ask it to forward private data to an outside address. Remove any one of the three and the attack loses most of its power. The design question for each agent is therefore which of the three it can do without.

Practical controls, in the order a small team can adopt them:

1. Do not give agents that read untrusted content any write or send ability. Split the work into two agents when needed: one reads and summarizes, with no outbound tools, and one acts on the structured result after a person has looked at it.
2. Restrict outbound network access to an allowlist of destinations the agent needs. This is the egress control in standard AGT-SBX-02. An agent that cannot reach an arbitrary web address cannot post data to one.
3. Treat all tool output, retrieved documents, and inbound messages as data. Strip or neutralize markup that can carry hidden instructions or cause automatic loading of remote content, such as images that fetch from a URL.
4. Limit the volume the agent can read or write in one run, so a hijacked run cannot pull out the whole database.
5. Log every tool call, so an exfiltration attempt can be found and its scope measured. The observability standard AGT-OBS-01 sets what to record.
6. Test. The Auditing Guide (04) includes adversarial checks in which test content tries to redirect the agent. For T1 and T2 agents, the full track adds a recurring adversarial test.

Data exfiltration also happens without an attacker. An agent that pastes client details into a hosted tool that retains inputs, or that sends a document to a model provider whose terms allow training on inputs, has exfiltrated the data by design. The model choice and data class standards address this, and the vendor review in the addendum (E006) is where those terms get read.

---

## 8. The Equity Review Step

Before an agent touches a decision about people, the organization reviews who could be harmed or excluded. A decision about people includes who gets a service, who is prioritized, who is flagged, who receives outreach, whose application advances, and what a person is told about their own case. Agents that only handle internal logistics do not need the step. Agents that influence any of those decisions do, even when a person makes the final call, because people tend to follow the suggestion they are given.

The step has four parts, and a short written record covers them.

1. **Name who could be harmed or excluded.** List the groups the organization serves and the ways the agent could disadvantage each. Think about language, literacy, disability, immigration status, age, housing stability, access to technology, and any group the programs exist to serve. Include people the data does not represent well, because an agent trained or prompted on typical cases will handle atypical ones poorly.
2. **Test the outputs across those groups.** Run the agent on realistic cases that differ along the dimensions you listed and compare the results. For a drafting or triage agent, this can be a modest set of paired examples that differ only in a name, a language, or a stated circumstance, reviewed by a person who knows the community. The goal is to find patterns, not to prove the agent is fair.
3. **Decide and record.** Record in the charter, under Authority, what was reviewed, by whom, on what date, what was found, and what was done about it. If the agent will make recommendations that affect access to a service, say whether a person reviews each one.
4. **Repeat on change.** Repeat the review when the model, the prompt, the data source, or the population changes, and at each scheduled review.

Equity review does not replace the consent and vulnerable population rules in standard AGT-CON-01 to AGT-CON-03. It sits beside them. Those rules decide whether an agent may touch certain people's data at all. The equity review asks, for the cases where it may, whether the agent treats everyone served fairly. Where the review finds a harm that cannot be fixed, the correct outcome is to narrow the agent's role or not run it.

---

## 9. Choosing a Model

Model choice is a governance decision as much as a technical one. The agent's behavior, its data exposure, its cost, and its continuity all depend on it. Two broad options exist, and many organizations will use both.

**Hosted frontier models** are run by a provider and called over the network. They usually give the strongest results and the least operational work. In exchange, client data leaves the organization's systems, the provider's terms govern what happens to it, and the provider can change or retire a model on its own schedule.

**Open-weight models** are downloaded and run on infrastructure the organization controls or rents. They offer control over where data goes and independence from one provider's retirement schedule. They cost more in setup and maintenance, usually need someone who can run them, and carry their own risks of provenance and licence terms.

Whichever kind is chosen, review these seven points before an agent goes into production, and record the answers in the registry.

| Question | What to establish |
|---|---|
| Provenance | Who published the model, where it was obtained, and how it was verified. For open weights, use the publisher's official source, verify checksums, and prefer file formats that cannot run code when loaded. |
| Licence | The terms for commercial and nonprofit use, restrictions on use cases, attribution duties, and whether the terms can change on later versions. Have someone able to read a licence review it. Licence terms differ across model families and have changed between versions of the same family, so read the file that ships with the exact version. |
| Data handling | For hosted models: retention, training use, who at the provider can see inputs, and whether a business agreement is available for regulated data. For open weights: where the data goes in your own stack. |
| Data residency | Where processing and storage happen, and whether the data classes the agent handles are allowed there. The addendum's vendor due diligence (E006, E011) covers this. |
| Version pinning | Pin to a specific model version in the registry, not to a moving alias. A silent change in the model behind an alias changes the agent's behavior without any change in your files. |
| Deprecation | How much notice the provider gives, what the migration path is, and who owns re-testing before cutover. Providers retire models. Plan for it. |
| Lock-in | How hard it is to move the agent to another model. Keep prompts, tool definitions, and evaluation cases in files you own, and keep model identifiers in configuration, so a switch is a configuration change plus a re-test. |

Some funders, public agencies, and partners have rules about where a model was developed or where data may be processed. Ask early, because a model that fails such a rule cannot be fixed later by configuration. The sources for current licence terms and provider retirement schedules are in `LANDSCAPE_SNAPSHOT.md`, and they should be checked again before any agent is approved, because they change.

A related choice is the assessor's model. An assessor agent should run on a different model family than the agent it reviews, so the two do not share the same blind spots and biases. Model-based judges show known biases, including a preference for outputs from their own family, and they can be persuaded by confident wrong answers. The Auditing Guide (04) covers the limits in detail. The practical consequence for model choice is that the organization needs access to at least two model families, and the choice of the worker model constrains the choice of assessor.

---

## 10. Choosing a Runtime

An agent runtime is the software that runs the loop: it sends the model a prompt, receives a request to use a tool, runs the tool, and feeds back the result. It also manages memory, tools, and sometimes sandboxing. Examples include software development kits from the major model providers, open-source orchestration libraries, enterprise agent frameworks, and personal-agent applications that run on a desktop. This pillar names no product as the right choice. Choose against criteria, and treat any list of products as dated.

| Criterion | Question to ask |
|---|---|
| Permission model | Can each agent run under its own identity with scoped credentials, or does everything run as one user? |
| Approval support | Does the runtime pause for human approval on chosen tool calls, with a record of the decision? |
| Sandboxing | Can code and shell commands run in an isolated environment, with file and network limits? |
| Tool governance | Can tools be allowlisted, pinned, and reviewed, and can the runtime be stopped from loading tools at run time from untrusted places? |
| Logging | Does it produce a complete log of prompts, tool calls, results, and decisions that the organization keeps itself? |
| Spend control | Can token or call budgets be set per agent and enforced? |
| Memory control | Is memory inspectable, editable, and deletable, and is its provenance recorded? |
| Supply chain | How are plug-ins and skills distributed, who vets them, and is there a way to restrict installation to an approved list? |
| Maintenance | Is it actively maintained, with a security contact and a record of fixing reported flaws promptly? |
| Portability | Do its agent definitions, skills, and tool connections use open conventions, so moving to another runtime is an effort and not a rewrite? |
| Operating burden | Can your team actually run and patch it? |

Maturity differs sharply across the field. Established vendor development kits and enterprise frameworks tend to have documented permission models and security processes. Some personal-agent runtimes with public skill marketplaces have a history of security flaws and malicious third-party skills, and they were not built with the controls this pillar requires. A runtime that cannot meet the standards in the Agentic Standards (03) for identity, tool governance, logging, and spend caps is not suitable for any agent that handles client data, however popular it is. `LANDSCAPE_SNAPSHOT.md` holds the dated assessment of specific runtimes, with a grade for maturity.

Interoperability conventions matter more than product names for long-term planning. Protocols for connecting agents to tools, file conventions for agent instructions, and packaging formats for skills have been moved under neutral foundations. Lock-in tends to sit in proprietary agent builders and hosted workflow tools, and less in these open conventions. Prefer open conventions where they meet the requirements, and keep the enforcement layer, meaning identity, sandbox, egress, and budget, in systems you control.

---

## 11. Social Sector Realities

The practices above assume capacity that many organizations do not have. The following realities shape how the standards should be applied.

**Small teams.** An organization may have one person who handles data, IT, and AI. Segregation of duties is hard. This pillar addresses that with a lean track in the Program Establishment guide (02) in which a second person, an assessor agent, or both stand in for a separate review function. The principle is that the person who built an agent should not be the only person who ever checks its work. For a team of one, a peer from another organization, a board member with relevant experience, or a volunteer can serve as the second reviewer.

**Sensitive client data.** Social-sector data often covers people at their most vulnerable: health conditions, immigration status, experience of violence, housing, children's records. A breach does more than create a fine. It can put a person in danger. The data class and consent standards in the Agentic Standards (03) reflect this, and the default for the most sensitive classes is that agents do not touch them without specific approval.

**Funders and boards.** Funders increasingly ask how organizations use AI, and boards carry the oversight duty. The registry gives both a concrete answer to "what agents do we run, who owns them, and what can they do." The Program Establishment guide (02) includes a section on those conversations.

**Insurance.** Some insurers have added exclusions for AI-related claims or have left it unclear whether existing policies cover them. An agent that takes an unauthorized action raises different questions than a chatbot that says something wrong. Ask the broker, in writing, whether the organization's policies cover claims arising from an AI agent's actions, whether any exclusion applies, and what the insurer requires as controls. Do this before launch and again at renewal.

**Volunteers and partners.** Volunteers and partner organizations often use their own tools on the organization's data. Agent use by them falls under the same rules, and the shadow-agent discovery step in the Program Establishment guide (02) should include them.

**Limited budgets.** The standards that matter most cost little: separate accounts, narrow scopes, a draft-only default, a spend cap, a registry, and a monthly look at the log. The costly items, such as adversarial testing programs and external certification, apply to the full track and to higher tiers. Spend effort on the first group before the second.

---

## 12. Anti-Patterns

These patterns appear repeatedly. Each one is a reason to stop and fix before going further.

**Borrowed staff credentials.** An agent runs under a staff member's login or token. The log cannot separate agent actions from staff actions, access cannot be revoked without disrupting a person, and a compromise yields the person's full access. Fix: a dedicated identity with scoped access (AGT-ID-01).

**Public skill registries on agents that touch client data.** Skills and plug-ins from open marketplaces have included malicious items, and a skill is code and instructions that the agent will run with the agent's access. Fix: install only reviewed items from an internal allowlist, pinned to a version (AGT-SKL-01 and AGT-SKL-02).

**Persona files that carry policy.** Rules such as "never share client data" live only in a personality file. Fix: write the bound in the charter with a named control outside the model, and keep voice as guidance only (AGT-CH-02).

**Unreviewed memory.** The agent writes its own long-term notes, and nobody reads them. Fix: provenance, review, expiry (AGT-MEM-01 to AGT-MEM-03).

**Unlimited spend.** The agent has no cost cap, and a loop or an attack runs up a large bill. Fix: a cap enforced by the provider or a proxy, with an alert before the cap (AGT-SPD-01).

**One agent with every permission.** A single general-purpose agent can read the database, send email, and edit the website, because that was easier than building three. Fix: split by function so each agent has the narrowest scopes for its task, and a compromise has limited reach (AGT-ID-02).

**Approval on everything.** A gate on every action, which people stop reading. Fix: gate few, high-impact actions and sample the rest.

**Charter as compliance theater.** A charter is filled in to satisfy a checklist, with no one checking whether the stated controls exist. Fix: the registry's enforcement map and the audit that tests it (04).

**Testing only the happy path.** The agent is tried on friendly examples. Fix: include hostile and edge-case inputs in review.

---

## 13. Things Teams Usually Miss

These items rarely appear in a first plan and cause trouble later. Each has a home in the standards or the Program Establishment guide (02).

**Agent sprawl and shadow agents.** Staff, volunteers, and vendors create agents and automations outside any list. The organization cannot govern what it cannot see. Run discovery on a schedule, and make registration easy enough that people do it. See the inventory section of 02 and AGT-REG-01.

**Memory poisoning.** One bad write persists and affects later sessions and other users. See section 6 and AGT-MEM-01 to AGT-MEM-03.

**Skill and tool supply chain.** Install-time trust is the largest practical gap. A plug-in, a skill, or a tool server brings code and instructions from someone else into your agent's access. Allowlist, pin, and review. See AGT-TOOL-01 to AGT-TOOL-04 and AGT-SKL-01 to AGT-SKL-02.

**Insurance exclusions.** Coverage for agent actions may be excluded or unclear. Ask before launch. See section 11.

**Model retirement.** The model an agent depends on will be retired. Without a pinned version, a recorded owner, and saved test cases, retirement becomes an emergency. See section 9 and AGT-MOD-02.

**Oversight fatigue.** Too many gates produce rubber stamps. See section 5.

**Accountability when an agent acts.** When an agent causes harm, someone must answer for it. Name a human Agent Owner in the charter and the registry, and make sure that person has the authority and time to do the job. Responsibility cannot be assigned to software.

**Cost runaway.** A loop, a retry storm, or an attack can generate a large bill within hours. Caps and alerts are cheap. See AGT-SPD-01 and AGT-SPD-02.

**Decommissioning.** Agents that are no longer needed keep their access. Every charter has a sunset date and a retirement checklist, and the program disables identities for agents that pass their sunset date unrenewed. See AGT-ID-03 and the exit section of 02.

**Change without review.** A new tool, a new model version, an edited charter, or a changed prompt alters the agent's behavior. The Config and Change Management guide (05) treats each as a change that is recorded and, for higher tiers, reviewed.

**Incidents.** Agents fail in ways that conventional incident plans do not cover, such as an agent that keeps acting after it is told to stop. The incident addendum (`AGENT_INCIDENT_RESPONSE_ADDENDUM.md`) adds the agent-specific steps. The kill switch standard (AGT-KIL-01) is what makes the first step possible.
