# Agentic AI KPIs, Benchmarking and Scorecard
## Measuring Whether Agents Stay Governed

**Document Owner:** Data Program Management Lead
**Classification:** Internal: Program Standard
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual, with targets reviewed after the first two quarters of data

> **Purpose:** This document defines the measures that show whether the agent program is under control. Each measure has a definition, a calculation described against the fields in the charter and registry row, targets by agent tier, a frequency, and an owner. It ships no collector code: a small team can compute every measure from the registry, the findings log, the approval log, and the provider bill with a spreadsheet.

---

## Table of Contents

1. [KPI Framework Overview](#1-kpi-framework-overview)
2. [Full KPI Registry](#2-full-kpi-registry)
3. [Calculation Notes](#3-calculation-notes)
4. [Agent Scorecard: Monthly Template](#4-agent-scorecard-monthly-template)
5. [Benchmarking Reference](#5-benchmarking-reference)
6. [Tier-Gated and Lean Track Targets](#6-tier-gated-and-lean-track-targets)
7. [Reading the Numbers](#7-reading-the-numbers)

---

## 1. KPI Framework Overview

### 1.1 Perspectives

Agent KPIs are grouped into four perspectives. They correspond to the questions a board member, funder, or insurer is likely to ask.

| Perspective | Question | KPIs |
|---|---|---|
| Ownership and currency | Does every agent have a person, a current charter, and an end date? | AG-OC-01, AG-OC-02 |
| Independent review | Is each agent checked by someone other than its builder, and can the checker be trusted? | AG-IR-01, AG-IR-02, AG-IR-03 |
| Safety and response | Do bounds hold, and when they fail, how fast do we stop it? | AG-SR-01, AG-SR-02 |
| Cost | Do agents stay inside the money set aside for them? | AG-CO-01 |

### 1.2 KPI Ownership Model

| Perspective | Primary owner | Reporting cadence | Audience |
|---|---|---|---|
| Ownership and currency | Program lead | Monthly | Executive sponsor, agent owners |
| Independent review | Reviewer lead (or the second person in a small team) | Monthly | Program lead, executive sponsor |
| Safety and response | Program lead, with the incident commander | Monthly, and per incident | Executive sponsor, board committee for T1 and T2 |
| Cost | Finance contact with the program lead | Monthly | Executive sponsor, funders where relevant |

### 1.3 Where the Numbers Come From

| Source | Fields used |
|---|---|
| Registry (rows from `registry.schema.yaml`) | `agent_id`, `tier`, `status`, `last_assessed`, `spend_cap_usd_month`, `model.family`, `approval_gates`, `tools` |
| Charter frontmatter | `owner`, `backup_owner`, `review_date`, `sunset_date`, `assessor`, `second_reviewer` |
| Assessor findings log | Run id, question, answer, supporting reference (evidence format in the Auditing Guide, `04_Agentic_Auditing_Guide.md`) |
| Approval log | Approver, decision, time shown, time decided |
| Incident log | Severity, time detected, time disabled, agent ID |
| Provider billing and budget alerts | Spend by agent identity |

The library's KPI documents for other domains are in `KPIs_and_Benchmarking/`, and this document follows their layout so that scorecards can be read side by side.

---

## 2. Full KPI Registry

Only active agents (registry `status` is active) count in the denominators unless a definition says otherwise. Targets are by agent tier and are illustrative starting values, set in section 6, since no published benchmark exists for small agent programs. Each KPI is calculated per agent tier and in total.

### 2.1 Ownership and Currency

| KPI ID | Metric | Definition | Calculation against registry and charter fields | Target T1 and T2 | Target T3 | Target T4 | Frequency | Owner |
|---|---|---|---|---|---|---|---|---|
| AG-OC-01 | Charter currency | Share of active agents whose charter is within its review period and passes the agent linter | Count active agents where charter `review_date` is today or later and `tools/agent_lint.py` reports no errors, divided by all active agents | 100% | 100% | 90% or more | Monthly | Program lead |
| AG-OC-02 | Named owner and sunset date coverage | Share of active agents that have a named owner, a named backup owner, and a sunset date that has not passed | Count active agents with non-empty `owner`, non-empty `backup_owner`, and `sunset_date` later than today, divided by all active agents. Also count agents found in the identity provider or runtime that have no registry row, and report that count beside the share | 100%, zero unregistered | 100%, zero unregistered | 100%, zero unregistered | Monthly | Program lead |

### 2.2 Independent Review

| KPI ID | Metric | Definition | Calculation against registry and charter fields | Target T1 and T2 | Target T3 | Target T4 | Frequency | Owner |
|---|---|---|---|---|---|---|---|---|
| AG-IR-01 | Assessor coverage | Share of active agents that have independent review in place and have been reviewed in the last period | Count active agents where charter `assessor` or `second_reviewer` is set, the assessor's `model.family` differs from the agent's `model.family` (where an assessor agent is used), and registry `last_assessed` falls inside the period set for the tier (illustrative: 30 days for T1 and T2, 45 for T3), divided by all active agents of that tier | 100% | 100% | Not required (report only) | Monthly | Reviewer lead |
| AG-IR-02 | Approval gate override and rubber-stamp rate | Two rates. The override rate is how often a person changes or rejects what the agent proposed. The rubber-stamp rate is how often approvals look automatic | Override rate: approvals with a changed or rejected decision, divided by all approvals decided in the period. Rubber-stamp rate: approvals decided faster than a floor set per gate (for example the time needed to read the item), plus approvals granted in a batch, divided by all approvals decided. Count per agent with at least a set minimum of approvals | Overrides: watched, no target. Rubber-stamp: below 5% | Rubber-stamp below 10% | Not applicable | Monthly | Reviewer lead |
| AG-IR-03 | Assessor agreement with human reviewers | Share of sampled assessor answers that match an independent human reading of the same item | Items re-labeled by a person in the period where the human answer equals the assessor answer, divided by all items re-labeled. Also report assessor "yes" answers where the human said "no" as a separate count | 90% or more, and the separate count trending down | 85% or more | Not applicable | Monthly | Reviewer lead |

### 2.3 Safety and Response

| KPI ID | Metric | Definition | Calculation against registry and charter fields | Target T1 and T2 | Target T3 | Target T4 | Frequency | Owner |
|---|---|---|---|---|---|---|---|---|
| AG-SR-01 | Incidents by severity | Count of agent incidents in the period at each level of the severity ladder in `AGENT_INCIDENT_RESPONSE_ADDENDUM.md`, plus the count of repeat incidents with the same cause | Incident log entries with an agent ID, grouped by severity and by registry `tier`. Repeat is any incident whose cause matches an earlier closed one | Severity 1 and 2: zero. Repeat: zero | Severity 1: zero. Severity 2: reviewed individually | Reported, not targeted | Monthly and per incident | Program lead |
| AG-SR-02 | Mean time to disable | Average time from the decision to stop an agent to confirmed stop, from incidents and from kill switch drills | For each incident or drill, time of confirmed stop (no new tool calls, credentials revoked) minus time of the decision to disable. Average over the period. Report incidents and drills separately, and report the longest single time | 15 minutes or less (illustrative) | 60 minutes or less (illustrative) | One business day or less | Monthly and per drill | Program lead |

### 2.4 Cost

| KPI ID | Metric | Definition | Calculation against registry and charter fields | Target T1 and T2 | Target T3 | Target T4 | Frequency | Owner |
|---|---|---|---|---|---|---|---|---|
| AG-CO-01 | Spend against cap | Spend for each agent as a share of its monthly cap, and the count of agents with no enforced cap | Provider billing for the agent's identity in the month, divided by registry `spend_cap_usd_month`. Count active agents with a cap that is not enforced by the provider budget or alert, using the registry `enforcement` map | Each agent at or below 100%. Alert fired at 80% reached a named person. No agent without a cap | Same | Same | Monthly | Finance contact with program lead |

---

## 3. Calculation Notes

### 3.1 Ground Rules

- Calculate from the registry as it stands at month end, and keep a dated copy of the registry with each scorecard so the number can be checked later.
- Use the registry `tier` at the end of the month. A tier change is a change request, so the history is in version control.
- Report counts with the share. A share of 100% on two agents and a share of 100% on forty carry different weight.
- An agent that exists in the identity provider or runtime and not in the registry counts as a failure in AG-OC-02 and is excluded from the others until registered. The aim is to make shadow agents visible, not to hide them from the score.
- Suspended agents are listed but not counted in the denominators. Retired agents are not counted.

### 3.2 Approval Metrics

The override and rubber-stamp rate pair works only if the gate shows the approver the action, the target, and the data. The time floor for each gate is set by the reviewer from a trial: have the person read ten typical items carefully and use the shortest sensible time. A very high rubber-stamp rate means one of three things: the gate fires too often, the approver is not reading, or the agent is correct. Check the first two before accepting the third. If the gate fires too often, reduce the gates to the few high-impact actions, as the program standards for approvals require, because approvals that fire constantly get approved without being read.

A zero override rate is not a good sign by itself. It can mean the agent is accurate or that nobody is checking.

### 3.3 Assessor Agreement

Agreement is meaningful only if the human re-labels items without seeing the assessor's answer first. The re-labeled set is drawn the same way every month (the calibration procedure in the Auditing Guide, section 5) and includes forced items. Report agreement for each rubric question when the overall figure falls below target, since a bad question drags down the total and the fix is to rewrite that question.

### 3.4 Time to Disable

Both clock times come from logs and not from memory. The starting time is the recorded decision to disable. The stopping time is the first log moment after which no tool calls occur and old credentials are refused. Drills from section 9 of the Auditing Guide supply the data between incidents, so the KPI is never empty.

### 3.5 Severity and Counts

Counts here are for incidents, not for audit findings. Findings have their own severity table in the Auditing Guide, section 11.2. Keep the two separate so that an organization with many findings and no incidents is not read as having a bad incident record.

---

## 4. Agent Scorecard: Monthly Template

```markdown
# Agent Program Scorecard: [Month YYYY]

Registry copy used: (link to dated copy)
Active agents: T1 [n] | T2 [n] | T3 [n] | T4 [n]   Suspended: [n]   Retired this month: [n]

## Ownership and Currency
| KPI | Target | T1/T2 | T3 | T4 | Status |
|---|---|---|---|---|---|
| AG-OC-01 Charter currency | per tier | X% | X% | X% | On track / At risk / Off track |
| AG-OC-02 Owner and sunset coverage | 100% | X% | X% | X% | |
| Unregistered agents found | 0 | [n] | [n] | [n] | |

## Independent Review
| KPI | Target | T1/T2 | T3 | Status |
|---|---|---|---|---|
| AG-IR-01 Assessor coverage | per tier | X% | X% | |
| AG-IR-02 Override rate (info) | none | X% | X% | |
| AG-IR-02 Rubber-stamp rate | per tier | X% | X% | |
| AG-IR-03 Assessor agreement | per tier | X% | X% | |
| Assessor "yes" where human said "no" | trending down | [n] | [n] | |

## Safety and Response
| KPI | Target | T1/T2 | T3 | T4 | Status |
|---|---|---|---|---|---|
| AG-SR-01 Severity 1 incidents | 0 | [n] | [n] | [n] | |
| AG-SR-01 Severity 2 incidents | 0 for T1/T2 | [n] | [n] | [n] | |
| AG-SR-01 Severity 3 and 4 incidents | reported | [n] | [n] | [n] | |
| AG-SR-01 Repeat incidents | 0 | [n] | [n] | [n] | |
| AG-SR-02 Mean time to disable (incidents) | per tier | [min] | [min] | [min] | |
| AG-SR-02 Mean time to disable (drills) | per tier | [min] | [min] | [min] | |

## Cost
| KPI | Target | Result | Status |
|---|---|---|---|
| AG-CO-01 Agents over cap | 0 | [n] | |
| AG-CO-01 Agents with no enforced cap | 0 | [n] | |
| Agents above 80% of cap | reported | [n] | |

## Actions
| Item | Owner | Due |
|---|---|---|
| | | |

## Commentary (three sentences at most)
```

---

## 5. Benchmarking Reference

### 5.1 Status of Benchmarks

No published benchmark was found for these measures in small or mid-sized nonprofit programs. Every target in this document is an **illustrative starting target**. It is a reasonable first line to draw, and the organization should revise it after two quarters of its own data. Do not quote these figures to a funder, board, or insurer as an industry norm. Where a figure comes from a published source, it is listed in `SOURCES.md` with its access date, and anything volatile is in the Landscape Snapshot (`LANDSCAPE_SNAPSHOT.md`).

### 5.2 Illustrative Starting Targets

| Measure | Illustrative starting point | Basis |
|---|---|---|
| Charter currency, T1 and T2 | 100% | A charter past its review date is an unreviewed agent. Set by this pillar, not by an outside standard |
| Owner and sunset coverage | 100% | Set by this pillar. The sunset date is this pillar's own convention |
| Assessor coverage, T1 to T3 | 100% | The independence rule in the pillar goals |
| Assessor agreement with human reviewers | 85 to 90% by tier | Starting values. Tighten after calibration data exists |
| Rubber-stamp rate | Below 5 to 10% by tier | Starting values. The floor time per gate matters more than the percentage |
| Mean time to disable | 15 minutes for T1 and T2, 60 minutes for T3 | Starting values. Drills will show what your setup can do |
| Spend at or below cap | 100% | A cap that is exceeded is not a cap |

### 5.3 Internal Benchmarks

The most useful comparison is with the organization's own history. After two quarters, use the trend by tier and the spread between agents. Set each target at the level the best-run agent already reaches, then raise it as the program matures. Compare with peer organizations only when you know they measure the same way, and agree definitions in writing first.

### 5.4 Reference Points From Other Frameworks

The AIUC-1 KPI table in the addendum, Part 6.2, lists measures for larger programs, including registry coverage, escalation SLA, and activity log completeness. For a program that is aiming at AIUC-1 alignment, use that table in addition to this one. This document does not reproduce it.

---

## 6. Tier-Gated and Lean Track Targets

### 6.1 Full Track

The targets in section 2 apply to T1 and T2 agents in the full track. T3 agents use the T3 column.

### 6.2 Lean Track

A team of one to ten staff measures less, and measures it by hand. Four numbers are enough to start, and the rest wait until there are more agents.

| Measure | How a small team gets it | Target |
|---|---|---|
| Agents with a named owner and a sunset date | Count rows in the registry file against the list of agent accounts in the identity provider | 100% |
| Agents reviewed this month | Count T3 agents where the second person signed off, and T4 agents the owner read | 100% of T3, report T4 |
| Time to disable | Run the kill switch drill, time it, write it down | 60 minutes or less for T3 |
| Spend against cap | Read the provider budget page | At or below cap, with the alert on |

### 6.3 Maturity Gating

| Program stage | Measures required |
|---|---|
| Starting (first agents) | AG-OC-02 and AG-CO-01, plus the lean track four |
| Established (several T3 agents, any T2) | Add AG-OC-01, AG-IR-01, AG-SR-01, AG-SR-02 |
| Full (any T1, or assessor agents in use) | Add AG-IR-02 and AG-IR-03 |

---

## 7. Reading the Numbers

A KPI is a prompt for a question and not an answer. The most useful reads are these.

- A falling override rate with a rising rubber-stamp rate suggests approvers have stopped reading. Check the approval screens and the number of gates.
- High assessor agreement with a high yes rate can mean the rubric is too easy. Add harder items to the calibration set.
- A mean time to disable that is good in drills and poor in incidents means the drills are too easy or the people on call differ from those who drill.
- Spend near the cap each month means the cap is working or the agent is growing. Look at tasks per month before raising the cap, and raise it through a change request.
- Zero incidents for a long period can mean good control or poor detection. Check that the log and alerting reach a named person, and that red-team tests still find things.
