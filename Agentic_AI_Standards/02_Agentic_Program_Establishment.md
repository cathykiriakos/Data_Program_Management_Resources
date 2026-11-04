# Agentic AI Program Establishment
## Operating Model, Tracks, and a 90 Day Build for Small Teams

**Document Owner:** Chief AI Officer (CAIO) or the Data Program Management Lead where no CAIO exists
**Classification:** Internal: Program Standard
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual, plus a review when the organization adds its first T1 or T2 agent

> **Purpose:** This guide shows how to stand up a governed agent program in an organization that may have no security staff and a handful of people. It defines the roles, the lean and full tracks, a phased build for the first 30, 60, and 90 days, how to find the agents already running, how to talk to funders, boards, and insurers, how to plan a budget without inventing numbers, and how to measure maturity and retire agents cleanly.

---

## Table of Contents

1. [Operating Model and Roles](#1-operating-model-and-roles)
2. [Lean Track and Full Track](#2-lean-track-and-full-track)
3. [Phased Build](#3-phased-build)
4. [Agent Inventory and Shadow Agent Discovery](#4-agent-inventory-and-shadow-agent-discovery)
5. [Funder, Board, and Insurer Conversations](#5-funder-board-and-insurer-conversations)
6. [Budget Inputs](#6-budget-inputs)
7. [Maturity Model](#7-maturity-model)
8. [Exit and Decommissioning](#8-exit-and-decommissioning)

---

## 1. Operating Model and Roles

The program rests on a few named people. In a small organization one person may hold several roles, and that is acceptable with one exception: the reviewer of an agent's work should not be the person who built it, except for T4 agents, where the owner reviews.

The roles of Chief AI Officer (CAIO) and AI Risk Lead come from the AI-First Strategy Addendum, Part 6 (`AI_FIRST_STRATEGY_ADDENDUM.md`). This pillar reuses them and adds the Agent Owner and a reviewer role.

| Role | Source | What the role does in this program |
|---|---|---|
| CAIO | Addendum Part 6 | Owns the agent program and its standards. Approves T1 and T2 agents and any exception to a MUST standard. Reports to the executive director and the board. In an organization with no CAIO, the Data Program Management Lead or the executive director holds this role. |
| AI Risk Lead | Addendum Part 6 | Maintains the tier assignments, reviews equity and consent assessments, checks the registry against the real systems, and escalates incidents. In a small organization this may be the data lead or a trusted outside advisor. |
| Agent Owner | New in this pillar | One named person for each agent. Signs the charter, answers for what the agent does, reviews its log, approves changes within the agent's tier, and decides when to retire it. Each agent also has a named backup owner. |
| Reviewer | New in this pillar | The person or assessor agent that checks the agent's sampled work. For T1 to T3 the reviewer is independent of the builder. For T4 the owner reviews. See the Auditing Guide (04). |
| Approver | Per agent | The person named in a charter's approval gate who decides on held actions. Often a program staff member who understands the work, not the owner. |
| IT or platform contact | Existing | Creates and disables the agent's identity, sets scopes and budgets, and holds the infrastructure side of enforcement. May be an outside provider. |

The Agent Owner is the most important of these. Accountability for an agent that acts cannot rest with software, and a named human who knows the agent's purpose, limits, and log is the answer to "who is responsible." An owner needs authority to pause the agent, time to review its output, and an understanding of what it can do. An owner who cannot read the charter or the log is an owner in name only.

Decision rights, in short: the owner proposes and maintains, the reviewer checks, the approver decides held actions, the AI Risk Lead assigns the tier and checks the facts, and the CAIO approves T1 and T2 agents and exceptions. A person who is both owner and approver for an agent that writes externally should be a flagged exception, because it removes the second set of eyes from the gate.

---

## 2. Lean Track and Full Track

The pillar offers two tracks. The lean track is for teams of one to ten staff running T3 and T4 agents. The full track is for T1 and T2 agents, and for larger organizations that want the stronger evidence. The tiers themselves are defined in section 3.1.1 of the addendum. Tier assignment does not change with the track: an agent that handles client health data is T1 or T2 whatever the size of the team, and so is on the full track. A small team that needs a T1 or T2 agent must either meet the full track or decide not to run the agent.

The table lists what each tier requires under each track. "Charter" means a charter that passes `tools/agent_lint.py`. "Registry row" means a complete row with its enforcement map.

| Requirement | T4 lean | T3 lean | T3 full | T2 full | T1 full |
|---|---|---|---|---|---|
| Charter, passing the linter | Required | Required | Required | Required | Required |
| Registry row with enforcement map | Required | Required | Required | Required | Required |
| Own scoped service account | Required | Required | Required | Required | Required |
| Approval gate on external writes and sends | Required | Required | Required | Required | Required, plus at least one gate even on read only agents |
| Spend cap and alert | Required | Required | Required | Required | Required |
| Kill switch drilled | Before go-live, then yearly | Before go-live, then twice a year | Before go-live, then twice a year | Before go-live, then quarterly | Before go-live, then quarterly |
| Reviewer | The owner | A second person using the boundary assessor rubric as a checklist, or an assessor agent | An assessor agent plus a named second person for sampled findings | An assessor agent and a named human approver | An assessor agent and a named human approver |
| Review cadence | Monthly owner review | Monthly review | Monthly review, assessor sampling each cycle | Monthly review, assessor sampling each cycle | Monthly review, assessor sampling each cycle |
| Adversarial testing | Not required | Not required | Per addendum tier cadence | Per addendum tier cadence | Per addendum tier cadence |
| AIUC-1 alignment | Not required | Not required | Optional | Required | Required |
| Equity review (agents touching decisions about people) | Required | Required | Required | Required | Required |
| Consent and vulnerable population check | Required | Required | Required | Required | Required |
| CAIO approval before go-live | No | No | No | Yes | Yes |

Three notes on the table.

The assessor is never the only gate. A model-based assessor is a sampling and triage aid, and the Auditing Guide (04) explains its limits. Deterministic checks and human approval are the gates for T1, T2, and any external write.

The lean track is not a lighter standard of care. It is the same standards with fewer layers of evidence, applied to agents whose potential harm is lower. An agent that does not qualify for the lean track on tier grounds does not qualify because the team is small.

If a lean agent grows, for example by gaining access to a more sensitive data class, it moves to a higher tier and to the full track before the change goes live. The Config and Change Management guide (05) treats that as a tier change that needs approval.

---

## 3. Phased Build

The phases below suit a small team starting from nothing. Each phase ends with something visible. Do not skip ahead, since later phases depend on the earlier ones.

### 3.1 Days 1 to 30: See and Decide

| Step | Outcome |
|---|---|
| Name the CAIO equivalent, the AI Risk Lead, and a backup for each | A one-page roles list approved by the executive director |
| Adopt the addendum tiers and the data classes in the Agentic Standards (03) | Tier and data class definitions the team can apply |
| Run the discovery exercise in section 4 | A first inventory of agents, automations, and AI tools in use, including those that staff and volunteers set up |
| Stop or pause anything that holds sensitive client data in a tool with no vendor review | Fewer unmanaged exposures |
| Set an interim rule | No new agent that touches client data goes live without a charter and an owner |
| Ask the insurance broker the questions in section 5 | Written answers on file |
| Choose the first agent | One T3 or T4 agent with clear value and low harm potential, such as a drafting assistant that cannot send |

### 3.2 Days 31 to 60: Build One Governed Agent

| Step | Outcome |
|---|---|
| Create the agent's identity in the existing identity provider, with scopes that grant read access and draft creation only | A service account that is not a person's login |
| Write the charter from `templates/SOUL.template.md` and the registry row from `registry.schema.yaml` | Both files complete, with every bound naming its enforcing control |
| Run `python tools/agent_lint.py` on the charter folder and fix every finding | A passing lint |
| Set a spend cap and an alert at the provider or through a proxy | Cost bounded by the provider, not only by the charter |
| Record the model pin, and save a small set of test cases | Ability to re-test after a model change |
| Name the reviewer and run the first review | A written review in the registry log |
| Run the kill switch drill once | A dated drill record |
| Complete the equity review and consent check if the agent touches decisions about people | The record in the charter |

### 3.3 Days 61 to 90: Operate and Extend

| Step | Outcome |
|---|---|
| Run two monthly reviews on the first agent | A trend, even a short one, of review findings |
| Register every agent found in discovery, even those you plan to retire | A complete inventory, with a decision per item: adopt, replace, or retire |
| Bring the next one or two agents through the same steps | Three agents or fewer under governance, which is enough for a small team to learn the process |
| Report to the board or a committee using the measures in the KPI guide (06) | A first board update |
| Run a tabletop exercise on the incident addendum (`AGENT_INCIDENT_RESPONSE_ADDENDUM.md`) | A practiced response and a list of fixes |
| Set the first scheduled landscape check, using `LANDSCAPE_SNAPSHOT.md` | A date on the calendar for refreshing volatile facts |

By day 90 a small team should have a governed first agent, a complete inventory, a tested stop procedure, a board report, and a named person for each role. The point is a sustainable routine and not a large portfolio. Adding a fourth agent before the first three are reviewed on schedule is a sign to slow down.

---

## 4. Agent Inventory and Shadow Agent Discovery

An organization cannot govern agents it does not know about. In most organizations the first inventory finds more than the leadership expected, because AI features are built into tools people already use and because individuals can set up automations in minutes.

Treat discovery as a repeated activity with several sources. A first pass can take a week and needs no special tools.

| Source | What to look for |
|---|---|
| Staff and volunteer survey | A short, non-punitive survey asking what AI tools, assistants, bots, and automations people use for work, including personal accounts |
| Identity provider | Applications that were granted access to the organization's accounts, service accounts, and app registrations, especially those created by individuals and those with mail, file, or database scopes |
| Admin consoles of core systems | Connected apps, installed integrations, API tokens, and automation recipes in the CRM, email, file storage, and case management system |
| Billing and expense records | Subscriptions and usage charges for AI products and model providers |
| Network and browser records, where they exist | Traffic to model provider addresses from work devices |
| Vendors and partners | Whether they use AI on your data, and under what terms |
| Incoming work products | Documents or messages that appear to have been produced by an agent without disclosure |

For each finding, make one decision, record it, and tell the person who set it up:

1. **Adopt.** Register it, name an owner, write the charter, move it to its own identity, and meet the standards for its tier.
2. **Replace.** Move the function to a governed agent or to an approved tool, with a date.
3. **Retire.** Disable it, revoke its access, and note the outcome.

Make the amnesty explicit. If staff fear punishment, they will hide the agents, and the inventory will be wrong. The aim is to see them. Registration should be quick: a short intake form that creates a draft registry row with the tier assigned afterward by the AI Risk Lead.

Schedule discovery again at least twice a year, and whenever a new platform is adopted. Compare the identity provider's application list against the registry. An application the identity provider shows and the registry lacks is a candidate shadow agent. A registry row whose identity no longer exists is a stale row. Both are findings for the quarterly registry check.

---

## 5. Funder, Board, and Insurer Conversations

Three audiences will ask about the program, and the registry and the review log answer most of what they want.

### 5.1 Funders

Funders want to know whether their money, and the data of the people they care about, are handled responsibly. Prepare a one-page summary that says which agents run, what each does, which data classes each touches, who owns each, how each is reviewed, and what is not allowed. If a grant covers a program that uses an agent, check the grant terms on data use and on AI before launch, and where the terms are silent, ask. Disclose AI use that affects beneficiaries. Funder expectations differ, so ask each funder what it needs and fold the answers into the board report.

### 5.2 Board

The board holds the oversight duty. Give it a short quarterly view built from the KPI guide (06): the number of registered agents by tier, the share with an owner and a current review, incidents and near misses, exceptions granted, and any change in tier or data class. Ask the board to approve the risk appetite: which tiers the organization will run, and which populations and data classes are excluded from agent use. Have one board member or advisor with technology or risk experience act as the contact. The board should see bad news early, so report near misses as well as incidents.

### 5.3 Insurer and broker

Ask the broker for written answers to these questions before the first production launch and at each renewal:

| Question | Why it matters |
|---|---|
| Do our current policies exclude or limit claims arising from the use of AI systems, including actions taken by an agent? | Some policies now carry AI exclusions, and silence in a policy does not guarantee cover |
| Does cyber cover extend to an incident caused by an agent acting under compromised instructions? | The agent acted with real credentials, and an insurer may treat that differently from an external hack |
| Do directors and officers, employment practices, and professional liability policies have AI exclusions? | Decisions about people may fall under those lines |
| What controls does the insurer require, ask about, or reward? | Your registry, logs, and approval gates may reduce the premium or satisfy a condition |
| Do vendors who host our models or agents carry cover, and are we named or protected in their terms? | Cover may sit with the vendor |
| What notice does the insurer require after an agent incident? | Late notice can void a claim |

Record the answers in the program file. If the insurer's answer limits what agents may do, put the limit into the charters of the affected agents and into the risk appetite statement the board approves.

---

## 6. Budget Inputs

No price list appears in this pillar, because prices change and differ by organization. Use the table as a worksheet. Each line is an input the owner fills in from vendor quotes, current invoices, or staff time estimates, and the total is then a number you can defend.

| Line | Input to enter | Source for the number |
|---|---|---|
| Model usage, per agent per month | Expected volume multiplied by the provider's current rate, plus a margin | Provider pricing page, test runs |
| Spend cap, per agent | Set at a multiple of expected usage that stops runaway cost but allows normal peaks | Registry field `spend_cap_usd_month` |
| Identity provider add-ons for agent identities | Quote, if the current plan does not cover service accounts | Identity provider or reseller |
| Secrets storage | Cost, or none if the existing tool covers it | Current plan |
| Logging and retention | Storage for logs for the retention period set in AGT-OBS-02 | Current plan or quote |
| Sandbox or hosting for agents | Hosting for the runtime, or for open-weight models, compute | Hosting quote |
| Staff time for owners | Hours per agent per month for review, multiplied by loaded hourly cost | HR and finance |
| Staff time for reviewers and approvers | Hours per month for sampling and approvals | HR and finance |
| Program lead time | Hours per month for inventory, registry checks, reporting | HR and finance |
| Training | Cost of workshop time and materials for owners and approvers | Internal estimate |
| Adversarial testing (full track) | Quote from a provider, or internal hours | Quote |
| External assessment or certification (full track, optional) | Quote from an assessor | Assessor quote |
| Legal and insurance review | Hours or fees for contract, licence, and policy review | Counsel, broker |
| Contingency | A set percentage chosen by the owner | Owner |

For most small teams the dominant cost is staff time, not software. Budget the owner's review hours first. A program that has no time for reviews does not have a program.

---

## 7. Maturity Model

Use five levels as a self-assessment. Each level has a test that a board member could verify.

| Level | Name | Test |
|---|---|---|
| 1 | Unmanaged | Agents exist, nobody has a full list, and credentials may be borrowed |
| 2 | Inventoried | A registry lists every known agent with an owner and a tier. Shadow agent discovery has been run once. |
| 3 | Chartered | Every agent has a charter that passes the linter, its own identity, a spend cap, and a named reviewer. Monthly reviews happen. |
| 4 | Verified | The enforcement map has been checked against the real systems by someone other than the owner. Kill switch drills are on schedule. Sampled reviews are logged and findings close. |
| 5 | Assured | For T1 and T2 agents, independent testing and an external assessment support the claims, and changes pass the review path in the Config and Change Management guide (05). |

Most small teams should aim for level 3 across all agents, and level 4 for any agent that writes externally. Level 5 is for the full track. Being at level 3 for every agent is a better position than level 5 for one agent and level 1 for the rest, because shadow agents are a larger risk than gaps in the evidence for a governed one.

The program's level is the level of its weakest agent, not its best.

---

## 8. Exit and Decommissioning

Every agent will end. Plan for it when you create it, since the charter requires a sunset date and a retirement checklist. Agents also end for reasons other than the plan: the model is retired, the owner leaves, the funding stops, a review fails, or an incident occurs.

The basic steps, which the charter's Decommissioning section lists in the agent's own words:

| Step | Detail |
|---|---|
| Stop | Disable the agent's identity first, so it cannot act while the rest proceeds |
| Revoke | Remove scopes, tokens, keys, tool connections, and any approvals in other systems |
| Preserve | Export the logs and the charter for the retention period. Keep the registry row, marked retired, with the date and reason. |
| Purge | Delete the agent's memory and any client data it stored, according to the data class rules |
| Notify | Tell users, approvers, partners, and funders if the agent's function changes |
| Transfer | Move the function to another agent or to staff, and update procedures |
| Review | Note lessons learned in the registry, and update the standards if the retirement showed a gap |

Three triggers deserve explicit rules. A sunset date that passes without a renewal decision is a retirement, and the identity is disabled. An owner who leaves must hand the agent to a named new owner within a set time, and until then the backup owner holds it, and if neither exists the agent is paused. A model provider's retirement notice starts a migration clock owned by the Agent Owner, as described in the Config and Change Management guide (05).

Vendor exit is its own concern. Before committing to a hosted service, know how to export the agent's definitions, logs, and memory, and what the vendor deletes when the contract ends. Keep your own copies of charters, test cases, and logs so a vendor change does not erase the record.
