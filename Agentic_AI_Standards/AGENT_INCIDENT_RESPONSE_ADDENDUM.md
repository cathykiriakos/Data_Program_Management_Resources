# Agent Incident Response Addendum
## Severity, First Hour, Memory Purge, Communications, and Blameless Review for Agent Incidents

**Document Owner:** Data Program Management Lead
**Classification:** Internal: Restricted Distribution
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Semi-annual, after any S1 or S2 incident, and after each kill switch drill that fails

> **Purpose:** This addendum adds what is specific to agents to the Data Incident Response Playbook (`DATA_INCIDENT_RESPONSE_PLAYBOOK.md`). It does not replace the playbook. Use the playbook for the universal first response, the escalation matrix, evidence preservation, and the incident register, and use this addendum for the agent-specific severity ladder, the first-hour actions, memory handling, and the review that follows. It does not state any legal notification deadline.

---

## Table of Contents

1. [Scope and Relationship to the Playbook](#1-scope-and-relationship-to-the-playbook)
2. [Agent Severity Ladder](#2-agent-severity-ladder)
3. [First Hour Actions](#3-first-hour-actions)
4. [Memory Purge and Rebuild](#4-memory-purge-and-rebuild)
5. [Communications](#5-communications)
6. [Notification Clocks: Required Step Before Relying on Any Clock](#6-notification-clocks-required-step-before-relying-on-any-clock)
7. [Post-Incident Charter and Registry Update](#7-post-incident-charter-and-registry-update)
8. [Blameless Review Template](#8-blameless-review-template)

---

## 1. Scope and Relationship to the Playbook

### 1.1 What Counts as an Agent Incident

An agent incident is any event where an agent acted outside its charter, was made to act outside it, exposed data it should not have, held or used access it should not have, or could not be stopped when it should have been. It also covers events outside the agent that put the agent at risk, such as a compromised skill or server, a leaked credential, or a model retirement that breaks a live agent.

Typical triggers:
- A boundary assessor reports a "no" on a safety question that a person confirms.
- An agent sends, posts, edits, or pays outside its approval gates.
- Content the agent read contained instructions and the agent followed them.
- Memory contains false or hostile entries.
- An agent credential, skill, or MCP server is reported compromised.
- Spend runs past the cap with no alert reaching a person.
- A kill switch drill shows the agent can still act after disable.
- A person, partner, or client reports odd behavior from something the agent sent.

### 1.2 How to Use the Two Documents

| Need | Where |
|---|---|
| Open an incident record, name the commander, preserve evidence, contain, communicate status | Playbook, section 2 (universal first response) |
| Who to escalate to and when | Playbook, section 4 (escalation matrix) |
| Evidence preservation detail | Playbook, section 5 |
| Credentials or secret exposure | Playbook, section 3.8, together with section 3 of this addendum |
| PII or sensitive data exposure | Playbook, section 3.2, together with sections 3 and 6 here |
| Unauthorized access | Playbook, section 3.3 |
| Post-incident process and register | Playbook, sections 6 and 10 |
| Agent-specific severity, memory, charter update, review | This addendum |

The incident commander role in the playbook applies. In a small organization, the commander is the program lead or the executive sponsor, and the agent owner is a responder and not the commander for an incident involving their own agent.

---

## 2. Agent Severity Ladder

The playbook's P1 to P4 levels describe data and platform incidents. Agents add two things the playbook's levels do not capture: an agent can keep acting while you respond, and it can act in the name of the organization. This ladder uses the tier of the agent and the nature of what it did. When an incident fits both ladders, use the higher level and record both.

| Level | Meaning | Agent examples | Playbook equivalent | Response targets (illustrative starting values) |
|---|---|---|---|---|
| S1 Critical | Harm to people or exposure of sensitive data has happened or is under way, or an agent cannot be stopped | A T1 or T2 agent sent client data to an outside party. Credential in use by an unknown party. Kill switch failed during an incident. Agent took an unapproved external action affecting clients | P1 | Disable within 15 minutes of decision. Commander and executive sponsor informed within 30 minutes |
| S2 High | A bound was crossed with external effect, or a control failed, and no confirmed exposure yet | Agent sent messages that its gate should have held. Skill or MCP server on an allowlist reported compromised. Injection followed with a tool call, contained before leaving the organization | P2 | Disable within 1 hour. Commander informed within 1 hour |
| S3 Medium | A bound was crossed inside the organization, or a control gap is found, with no external effect | Agent wrote to an internal record outside its scope. Memory holds hostile or false entries, caught before use. Spend cap exceeded by a small amount and caught | P3 | Disable or restrict within 4 hours. Owner and reviewer informed the same day |
| S4 Low | Near miss or housekeeping, no effect | Assessor flagged a prompt injection that the agent ignored. Charter past its review date on a T3 agent. Alert reached no one but the cap held | P4 | Owner fixes within the review cycle |

### 2.1 Rules for Setting the Level

- An agent that cannot be disabled when you try is S1, whatever it was doing.
- Any external write or send outside the approval gates is at least S2.
- Any exposure of a restricted data class to a party not allowed it is at least S1 until counsel or the privacy lead says otherwise. Data classes are set in the charter and the Standards (03).
- Raise the level, never lower it, while facts are unclear. Lower it in the review with the reason recorded.
- The tier of the agent raises the floor. An S3 event on a T1 agent is reviewed as S2.

### 2.2 Agent Incident Types

| Type | Description |
|---|---|
| INC-HIJ | Goal hijack or prompt injection that changed what the agent did |
| INC-TOOL | Tool misuse, or action outside the tool and scope list |
| INC-ID | Credential or identity misuse, or borrowed staff credentials found |
| INC-SUP | Compromised skill, plugin, or MCP server |
| INC-MEM | Memory or context poisoning |
| INC-EXF | Data sent where it should not go |
| INC-GATE | Approval gate bypassed or approvals rubber-stamped past a bad action |
| INC-KILL | Kill switch or stop method failed |
| INC-COST | Spend runaway |
| INC-ROGUE | Agent persisted after disable, or an unregistered agent found |

These sit beside the playbook's incident taxonomy and use the same incident register.

---

## 3. First Hour Actions

The first hour has one aim: stop the agent from acting, and keep what you need to understand what happened. Contain first and investigate second, as in the playbook. Where an agent is involved, stopping and preserving have to happen in the right order, because some stop methods destroy evidence.

### 3.1 Checklist

| Step | Action | By when | Done by | Note |
|---|---|---|---|---|
| 1 | Open an incident record in the playbook's register and name the incident commander. Record the agent ID, tier, and time of detection | 10 min | First person to notice | Use the agent's registry row for owner and tier |
| 2 | **Disable the agent.** Use the stop method written in its charter or runbook: disable the account in the identity provider and stop the runtime and any schedules or triggers. Record the exact time | 15 min for S1, 1 hour for S2 | Owner or any trained responder | Do not wait for a root cause. An agent that is disabled can be re-enabled |
| 3 | **Revoke credentials.** Revoke tokens, API keys, OAuth grants, and any secrets the agent could read. Rotate any secret that appeared in a prompt, a log, or memory. Confirm an old token is refused | 30 min | Identity administrator | If a skill or MCP server is suspected, disable it on every agent that uses it |
| 4 | **Freeze and snapshot memory.** Set memory to read-only if the platform allows. Take a copy of the agent's memory, context files, vector stores, and scratch files. Do not delete or edit anything yet | 30 min | Owner with the platform administrator | Wiping memory now destroys the evidence of what changed it and when |
| 5 | **Preserve logs.** Export and lock the agent's tool call log, approval log, assessor findings, model provider request logs, network and egress logs, and the identity provider's sign-in log for the agent identity. Record the time range | 45 min | Platform administrator | Move copies where the agent owner cannot edit them. Provider logs may expire on their own schedule, so export first |
| 6 | Record what the agent did. List actions in the period: messages sent, records changed, files written, payments, calls to other agents | 60 min | Owner and reviewer | Use the audit log and not the agent's own account |
| 7 | Contain downstream. Pause other agents that take input from this one. Warn people who may act on its output | 60 min | Commander | Trust is not inherited, so a downstream agent must check what it receives, but pause when unsure |
| 8 | Set the severity level using section 2 and tell the people the playbook's escalation matrix names | 60 min | Commander | See section 5 for who hears what |
| 9 | Start the notification check in section 6 if any restricted data may have left the organization | Start within the hour | Commander with counsel and the privacy lead | Do not wait for the investigation to end |

### 3.2 Things Not to Do

- Do not ask the agent to explain itself and treat the answer as evidence. Its account may be wrong or shaped by hostile text.
- Do not delete messages the agent sent before listing and saving them.
- Do not re-enable the agent to test a theory. Reproduce in a staging copy.
- Do not use a staff member's credentials to look into the agent's systems if an admin account for that purpose exists.
- Do not change the charter before the review. Record it as it was at the time of the incident.

### 3.3 If the Agent Cannot Be Stopped

Go one level out each time: the runtime, then the host or service, then the network path or egress rule, then the provider account or key. Revoking the provider key is a blunt step that stops every agent using it, so tell the commander before doing it. Treat the failure as INC-KILL and as S1.

---

## 4. Memory Purge and Rebuild

Memory can hold the cause of an incident: a poisoned entry, a false fact, an instruction written by hostile content. It can also hold sensitive data the agent should not have kept. A restored agent that reloads a poisoned memory repeats the incident.

### 4.1 When to Purge

| Situation | Action |
|---|---|
| Memory contains an entry that came from outside content and tells the agent how to behave | Purge that entry and everything written in the same session, then review |
| Memory contains data of a class the charter does not allow | Purge it and treat as a data exposure for section 6 |
| The source of memory entries cannot be traced | Treat the whole memory as untrusted and rebuild |
| Memory is intact and traceable | Keep it, with a review of recent entries |

### 4.2 Purge Procedure

| Step | Action |
|---|---|
| 1. Confirm the snapshot | The frozen copy from the first hour is complete and stored where the owner cannot edit it |
| 2. Find the first bad entry | Using timestamps and provenance, find the earliest poisoned or wrong entry and which run wrote it. Everything after it is suspect |
| 3. Decide the scope | Remove only the suspect entries if provenance is good. Remove all memory written since the first bad entry if it is not. Remove everything if the first entry cannot be found |
| 4. Purge in the live stores | Delete from every place memory lives: files, databases, vector stores, caches, and any copies in other agents' context |
| 5. Check other agents | Search other agents' memory and shared stores for the same content |
| 6. Verify | Search for the removed text and for the hostile instruction pattern. Confirm none remain |
| 7. Keep the snapshot | Keep the frozen copy as evidence under the retention rule, with access limited to the review team. If it holds restricted data, store it under that data class's controls |

### 4.3 Rebuild Procedure

1. Decide what the agent needs to remember. Reread the charter's Memory Rules. Rebuild only what the rules allow.
2. Restore from a source a person trusts: the last good snapshot from before the first bad entry, or a clean set prepared from the organization's own records.
3. Tag each rebuilt entry with its source and date. Memory entries without a source are not loaded.
4. Have a person read the rebuilt memory before the agent returns to service. For T1 and T2 agents the reviewer reads it. For T3 agents the owner and a second person read it.
5. Return the agent to service in staging first, then production at reduced reach, as set in the change process in `05_Agentic_Config_Change_Management.md`. Start with a tighter assessor sample for a period set by the reviewer.
6. If memory is not needed for the agent to do its job, consider setting memory off. The simplest memory policy is none.

---

## 5. Communications

### 5.1 Principles

- Say what is known, what is not known, and when the next update is due. Do not guess at cause.
- Do not describe an agent action as the decision of a named staff member, or the reverse. Say what happened and who is responsible for the response.
- Use plain language. Avoid terms that suggest an agent chose or intended anything.
- Do not paste client data, prompts, or logs into messages. Point to the incident record.
- Check statements about legal duties with counsel before sending them.

### 5.2 Who Hears What

| Audience | When | What they get | Who sends |
|---|---|---|---|
| Incident commander and agent owner | At detection | Agent ID, tier, what was seen, time | Detector |
| Executive sponsor | S1 within 30 minutes, S2 within the day | Level, effect, actions taken, next update time | Commander |
| Privacy lead and counsel | At once if any restricted data may have left | Data classes, systems, people potentially affected, time range | Commander |
| Reviewer and program lead | S1 to S3 the same day | Findings so far, plan for the review | Commander |
| Staff who use the agent | When the agent is disabled | The agent is off, what to do instead, who to ask | Owner |
| Downstream agent owners | At containment | Pause notice and scope | Commander |
| People or partners who received agent output | After counsel and the executive sponsor agree | What was sent in error, what to disregard or delete, who to contact | Executive sponsor or designee |
| Clients or people whose data was affected | As counsel advises, see section 6 | A plain statement of what happened and what they can do | Executive sponsor and counsel |
| Funders, partners under contract, insurer | As agreements require. Check agreements and policy terms for notice duties | Facts and actions, in the form the agreement asks | Executive sponsor |
| Board or committee | S1, and S2 for T1 and T2 | Summary, effect, actions, and review date | Executive sponsor |
| AI or platform vendor | When the cause may lie with them, or for a compromised product | Technical details through their security contact | Owner and platform administrator |

### 5.3 Holding Statement

Use something close to this for outside parties until facts are confirmed, after counsel has reviewed it.

> We identified unexpected behavior in an automated assistant we use for [function] on [date]. We turned it off, and we are reviewing what it did. We will tell you what we find and what, if anything, you need to do, by [date]. You can reach [name] at [contact] with questions.

### 5.4 Insurance

Many organizations have found that policies treat automated systems differently from standard software, and cover may be narrower than expected. At the start of any S1 or S2 incident the executive sponsor asks the broker whether the incident should be notified under any policy. Policy terms and notice periods differ, so read the policy and ask the broker, and do not rely on this addendum for the answer. The Landscape Snapshot (`LANDSCAPE_SNAPSHOT.md`) records the latest information the pillar has on insurance exclusions, with the source.

---

## 6. Notification Clocks: Required Step Before Relying on Any Clock

> **Required.** Before the organization relies on any notification deadline for an agent incident, whether from a statute, a regulation, a contract, or a funder agreement, **confirm it with counsel**. This addendum states no statutory deadline and nothing here is legal advice.
>
> **The notification table in the Data Incident Response Playbook (`DATA_INCIDENT_RESPONSE_PLAYBOOK.md`, section 9) has not been reviewed since March 2026.** It also has no category for AI or agent incidents. Treat it as a prompt for questions, not as a current answer. Laws on data breach, health information, education records, immigration data, and automated decision-making change often and differ by place.

### 6.1 Procedure

| Step | Action | Owner |
|---|---|---|
| 1 | At the start of the incident, the commander notes in the incident record whether any restricted data class (as defined in the charter) may have been read, written, or sent by the agent | Commander |
| 2 | If yes, or unknown, ask counsel which laws, contracts, and agreements apply to the data classes, the people affected, and where they live. Give counsel the data classes, systems, time range, and number of people potentially affected | Commander and privacy lead |
| 3 | Counsel states in writing which clocks apply, when each starts, and who must be told. Record the answer, the name, and the date in the incident record | Counsel |
| 4 | Put each clock and its start time in the incident record with a named person responsible | Commander |
| 5 | Use the playbook's section 9 only as a checklist of questions to ask, never as the source of a deadline | Commander |
| 6 | If counsel cannot be reached within the time you have, tell the executive sponsor, and do not decide that no clock applies | Commander |

### 6.2 What to Tell Counsel About Agents

The questions below are specific to agents and are often missed.

- Which identity did the agent use, and what could it reach?
- What did it read, write, send, or store, and where does memory hold copies?
- Did a model provider or tool vendor receive the data, and under what terms?
- Did the agent act on content from an outside party?
- Did any person receive output that they might have relied on to make a decision about someone?
- Are children, people seeking safety, or people with immigration risk among those affected?

The owner of the playbook's notification table should schedule a review of it with counsel, and add an AI incident category. That work is outside this addendum, and is recorded as a deferred item in the program plan.

---

## 7. Post-Incident Charter and Registry Update

Every S1, S2, and S3 incident, and any S4 that shows a gap, ends with a change to the files that govern the agent. This closes the loop: the charter and registry row say what the agent should do and what limits it, and an incident shows where they were wrong or the controls were missing.

### 7.1 Procedure

| Step | Action | Evidence |
|---|---|---|
| 1 | Link the incident record to the agent's registry row (add the incident ID to a notes field or the change log) | Registry commit |
| 2 | For each bound that failed, ask: was the bound missing, was it written but not enforced, or was the control there and bypassed? | Review notes |
| 3 | Add or fix the enforcement control outside the model first. A new line in the charter alone is not a fix | Control change record |
| 4 | Update the charter: forbidden actions, approval gates, tools and scopes, data handling, memory rules, and failure behavior as the incident shows | Pull request |
| 5 | Update the registry row to match: tools, data classes, approval gates, enforcement map, and status | Pull request, lint output |
| 6 | Update the assessor: add or tighten a rubric question that would have caught it, add the item to the calibration set, and re-run calibration | Rubric version, calibration record |
| 7 | Add the attack or failure to the red-team scenarios for the target and for similar agents | Test plan |
| 8 | Update allowlists, runbooks, and the deprecation calendar if a skill, server, or model was involved | Allowlist commit |
| 9 | Review other agents with the same tools, model, skill, or pattern, and apply the fix where it fits | List of agents checked |
| 10 | Re-enable the agent through the change process, at the tier the change requires (a gate removed or loosened is Major) | Change request |
| 11 | Reset the charter review date, and set the sunset date again if the agent was rebuilt | Charter commit |

### 7.2 Decide Whether to Keep the Agent

An incident may show that the agent should not continue. Ask whether the value of the work justifies the control burden, and whether the failure was one the organization can detect and stop. Retirement follows `05_Agentic_Config_Change_Management.md`, section 7.

---

## 8. Blameless Review Template

Hold the review within 5 business days of resolution for S1 and S2, and within 10 for S3. The aim is to learn what in the system allowed the event, and not to judge any person's conduct. People are asked what they saw and what they expected, and are not asked why they did not do better. Include the owner, the reviewer, the commander, and someone from outside the agent's team. A facilitator who was not part of the response runs the session.

```markdown
## Agent Incident Review

**Incident ID:**
**Agent ID and tier:**
**Level (S1 to S4):** at detection | at close
**Date detected / date resolved:**
**Review date and facilitator:**
**Participants:**

### Summary
Three or four sentences: what happened, what the effect was, who and what was affected.

### Timeline
| Time | Event | Source (log, message, person) |
|---|---|---|
| | Agent first acted outside bounds | |
| | Detected | |
| | Decision to disable | |
| | Confirmed stop | |
| | Credentials revoked | |
| | Memory frozen | |
| | Notification check started | |
| | Resolved | |

### Effect
- Data classes involved:
- People or groups affected:
- External actions taken:
- Cost:
- Time to detect, time to disable (feeds the mean time to disable measure):

### What We Learned
- What worked:
- What surprised us:
- Where did the system make the wrong thing easy?
- Which bound failed: missing, written but not enforced, or bypassed?
- Did the assessor flag anything beforehand? If not, why not?
- Did an approval gate fire? What did the approver see?
- Did the stop method work as written?

### Contributing Factors
List conditions, not people: unclear scope, missing control, a gate that fired too often, no alert, no backup owner, an unreviewed skill, an unpinned model, and so on.

### Actions
| Action | Type (control, charter, registry, assessor, test, training) | Owner | Due | Change request |
|---|---|---|---|---|
| | | | | |

### Charter and Registry Update
- [ ] Enforcement control added or fixed
- [ ] Charter updated and lint passes
- [ ] Registry row updated and lint passes
- [ ] Assessor rubric and calibration updated
- [ ] Red-team scenario added
- [ ] Other agents with the same pattern checked
- [ ] Review date reset

### Notification Check
- Was any restricted data involved? yes | no | unknown
- Counsel confirmed which clocks apply: yes | no (name, date)
- Playbook table used only as a question list: yes
- Insurer notice considered with the broker: yes | no

### Sign-Off
| Role | Name | Date |
|---|---|---|
| Commander | | |
| Owner | | |
| Reviewer | | |
| Executive sponsor (S1, S2) | | |
```
