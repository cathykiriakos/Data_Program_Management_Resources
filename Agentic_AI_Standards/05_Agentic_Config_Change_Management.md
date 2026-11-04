# Agentic Configuration-Based Practices and Change Management
## Charters, Registry Rows, Model Pins, Allowlists, Rollback, and Decommissioning

**Document Owner:** Data Program Management Lead
**Classification:** Internal: Binding Standard
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Annual, plus after any change-related incident

> **Purpose:** This document says how an agent's configuration is stored, reviewed, changed, rolled back, and retired. It keeps the facts that decide an agent's behavior and reach in version control, and it sorts agent changes into the library's change tiers so that small changes move fast and risky ones get a second pair of eyes.

---

## Table of Contents

1. [Config-First Agent Operations](#1-config-first-agent-operations)
2. [Change Tiers for Agents](#2-change-tiers-for-agents)
3. [Model Version Pinning and Re-Evaluation](#3-model-version-pinning-and-re-evaluation)
4. [Deprecation Watch](#4-deprecation-watch)
5. [Skill and MCP Server Allowlist Changes](#5-skill-and-mcp-server-allowlist-changes)
6. [Rollback](#6-rollback)
7. [Decommissioning](#7-decommissioning)
8. [Change Request Template for Agents](#8-change-request-template-for-agents)

---

## 1. Config-First Agent Operations

### 1.1 Philosophy

The Business Intelligence document on this topic (`05_BI_Config_Change_Management.md`) holds that configuration in files, not in a console, is what makes change reviewable. The same holds for agents, with one addition: a charter is a prompt and not an enforcement layer. A change to charter wording changes what the model is told. It does not change what the agent can do. What the agent can do is set by the identity provider scopes, the tool allowlist, the sandbox profile, the egress rules, and the budget. Those controls also need to be changed through a reviewed path, or the charter and the real limits drift apart.

### 1.2 What Lives in Version Control

| Item | Where | Reviewed by |
|---|---|---|
| Agent charter (Markdown with YAML frontmatter) | One folder per agent in the organization's repository | Reviewer, not the author |
| Registry row (`registry_row.yaml`) or shared `registry.yaml` | Same folder as the charter | Reviewer, not the author |
| Assessor charters and rubrics | Beside the target's charter or in a shared assessors folder | A second person, since the assessor is itself an agent |
| Skill and MCP server allowlist | One file for the organization, plus per-agent subsets in the registry | Program lead and security contact |
| Model allowlist and the pin table | One file, or the model fields of each registry row | Owner and reviewer |
| Enforcement settings that can be exported (scope definitions, sandbox profiles, budget alerts, egress rules) | Exported or written as configuration files where the platform allows | Reviewer |
| Calendar of model retirements (section 4) | A dated file or a shared calendar with a named owner | Program lead |

Anything that cannot be exported is described in the registry `enforcement` map, which says where the control lives and who can change it. A control that nobody can name or inspect is treated as absent.

### 1.3 The Pull Request Is the Change Record

For T1 to T3 agents, the pull request that changes a charter or registry row is the change record. It carries the change description, the tier from section 2, the evidence from section 8, and the reviewer's approval. The linter (`tools/agent_lint.py`) runs on every pull request, so that a mismatch between charter and registry row is caught before merge, and a failing lint blocks the merge. Teams of one to ten without a repository host can use a shared folder with a dated change log, but the rule is the same: the author is never the only approver of a change to a T1, T2, or T3 agent.

### 1.4 Separation of Duty

| Role | May | May not |
|---|---|---|
| Author | Draft a change | Approve it |
| Reviewer | Approve Standard and Minor changes, recommend Major | Approve a change they authored |
| Owner | Request changes, accept rollback | Change enforcement controls alone for T1 and T2 |
| Program lead | Approve Major changes with the change board | Approve changes to an agent they own |

---

## 2. Change Tiers for Agents

The library's change tiers are defined in `README.md` section 8.1: Self-Service, Standard, Minor, Major, and Hotfix. This table maps agent changes onto them. Lead times and the board rule follow the README, so the two documents cannot disagree.

### 2.1 Mapping

| Change | Tier for T4 | Tier for T3 | Tier for T1 and T2 | Why |
|---|---|---|---|---|
| Charter wording that does not change any bound (Voice, Purpose wording, clearer examples) | Self-Service | Standard | Standard | Changes the prompt, not the limits. Still goes through lint |
| Charter wording that narrows a bound (fewer allowed actions, tighter forbidden list) | Self-Service | Standard | Standard | Lowers risk. Confirm the enforcement control still matches |
| Tool added with read access only, within data classes already allowed | Standard | Minor | Minor | New reach, but read only |
| Tool added with write access, or any new send, post, or payment action | Minor | Major | Major | New external effect. Needs an approval gate in the same change |
| Scope widened on an existing tool, or a new write scope | Minor | Major | Major | Silent growth of reach is a main way agents drift |
| Model changed to a new version in the same family | Standard | Minor | Major | Behavior changes. Requires re-evaluation (section 3) |
| Model changed to a different family or provider | Minor | Major | Major | Different behavior, data handling, and licence. Also rechecks assessor independence |
| Memory policy changed (what is stored, where, retention) | Standard | Minor | Major | Memory shapes later behavior and can hold sensitive data |
| New data class added | Minor | Major | Major | New sensitivity, new obligations. Update the data processing review |
| Approval gate removed or loosened | Major | Major | Major | Loses a human check. Needs the reason in writing |
| Approval gate added or tightened | Standard | Standard | Standard | Lowers risk |
| Skill or MCP server added to an allowlist | Standard | Minor | Major | See section 5 |
| Assessor changed (new rubric, new model, new sampling rule) | n/a | Minor | Minor | Triggers calibration. See the Auditing Guide (04) |
| Spend cap raised | Standard | Standard | Minor | Cost control. Lowering a cap is Self-Service |
| Tier change (for example T3 to T2) | Minor | Major | Major | Moves the agent under a different rule set |
| Agent moved to a new runtime or hosting platform | Minor | Major | Major | Changes where every enforcement control lives |
| Agent suspended or retired | Self-Service | Standard | Standard | Lowers risk. Follow section 7 |
| Emergency fix after an incident | Hotfix | Hotfix | Hotfix | Retrospective change record within 24 hours, then a normal review |

When a change touches more than one row, use the highest tier. When in doubt, go one tier up.

### 2.2 Tier Requirements

| Tier | Lead time (per `README.md` section 8.1) | Minimum review | Evidence |
|---|---|---|---|
| Self-Service | Immediate | Lint passes | Lint output |
| Standard | Same day | One reviewer, lint passes | Pull request, lint output |
| Minor | 3 to 5 days | One reviewer who did not build the agent, lint passes, test run on staging | Change request (section 8), test notes |
| Major | 10 to 15 days, with change board | Reviewer plus program lead, staging test, re-evaluation where a model or tool changed, kill switch check | Full change request, test and evaluation results, rollback plan |
| Hotfix | Immediate, retrospective record within 24 hours | The owner and one other person by message at least | Retrospective change request, incident link |

Small organizations that have no formal change board treat it as the program lead plus one other person from outside the agent's team.

### 2.3 Forbidden Shortcuts

- Editing a live agent's tools or scopes in a console with no change record.
- Widening a scope and describing it as a wording change.
- Merging a change that fails lint and fixing it afterward.
- Raising an agent's tier number toward T4 to ease review, without the program lead's decision recorded in the registry.

---

## 3. Model Version Pinning and Re-Evaluation

### 3.1 Pin Every Agent

Each agent's registry row records `model.provider`, `model.id`, `model.pinned_version`, and `model.family`. The agent calls the pinned version. It does not call an alias that the provider moves to a newer model without notice. Where a provider offers only a moving alias, record that in the registry as a risk, add a monthly check that behavior has not changed (run the regression set from section 3.3), and prefer a provider or model that offers a fixed version for T1 to T3 agents.

The model reference lives in one place, the registry row, and the charter points to it with `model_ref`. The model ID is not written into code, prompts, or runbooks, so that a model change is one edit and one review.

### 3.2 Why Re-Evaluate

A new model version can change tone, tool use, refusal behavior, how it follows long instructions, how it treats injected text, and how much it costs, even when the provider says it is an upgrade. A pinned version is only useful if you check a new one before you move to it.

### 3.3 Re-Evaluation Procedure Before a Model Change

| Step | Action | Pass condition |
|---|---|---|
| 1. Open a change request | Section 8 template, tier from section 2.1 | Request filed with reason and target version |
| 2. Check the provider terms | Data handling, retention, training use, residency, and licence for the new model | No change that breaks the data classes in the charter. Counsel or the privacy lead reviews any change for T1 and T2 |
| 3. Run the regression set | A fixed set of representative tasks kept with the agent, including edge cases and past failures. Run it on the current and new model | Task success is no worse than the current model by the margin the owner set in the charter or change request |
| 4. Run the boundary checks | The deterministic checks, the rubric of the agent's assessor, and the injection tests from the Auditing Guide (04), section 8 | No new failures. Any new failure is a reason to stop |
| 5. Check cost and latency | Run the regression set and compare cost per task and time per task against the spend cap | Projected monthly spend fits the cap with the alert at the usual level |
| 6. Check the assessor | If the assessor and worker share a family after the change, the change is blocked. If the assessor itself is changing, recalibrate | Different families. Calibration meets the pass line |
| 7. Staged rollout | Run in staging, then a limited share of production work or a pilot group for T1 and T2 | No regression, no incident |
| 8. Update the registry and the charter | Registry `model` block, `last_assessed`, and any charter wording that referred to model behavior | Lint passes |
| 9. Keep the old pin ready | Do not delete the old pin from the change record until the new one has run for the agreed period | Rollback path exists (section 6) |

### 3.4 Open-Weight and Self-Hosted Models

A self-hosted or open-weight model has no provider retirement schedule, but it has other change events: a new weights release, a new quantization, a runtime update, a licence change. Treat each as a model change. Record the source of the weights, the checksum or digest, and the licence in the registry row, and read the licence at each change, since terms for open-weight releases vary and can change between releases. The Landscape Snapshot (`LANDSCAPE_SNAPSHOT.md`) tracks the current state of licences and provenance questions, and `SOURCES.md` records where each claim comes from.

---

## 4. Deprecation Watch

### 4.1 The Rule

Providers retire models on published schedules, usually with notice. An agent that is still pinned to a retired model stops working, or is moved by the provider to a different one. Both are unplanned changes. The standard therefore requires an owner-maintained calendar of retirement dates for every model any agent uses.

For the current list of announced retirements and the notice periods that providers state, see the Landscape Snapshot (`LANDSCAPE_SNAPSHOT.md`). Do not copy dates from this document or from the snapshot into the calendar without checking the provider's own deprecation page, since schedules change.

### 4.2 The Calendar

| Field | Content |
|---|---|
| Model | Provider and model ID |
| Agents using it | Registry agent IDs, read from the registry `model` block |
| Source URL | The provider's deprecation or lifecycle page |
| Announced retirement date | As stated on that page, with the date you read it |
| Planned migration date | Set at least one review cycle before the retirement date |
| Migration owner | A named person, normally the agent owner |
| Change request | Link, once filed |
| Status | Watching, scheduled, migrated, or retired |

The calendar has one named owner, normally the program lead, and a named backup. The owner checks every provider the organization uses on a fixed schedule, monthly as a starting point, and also reads provider notice emails sent to a shared mailbox rather than a person's inbox. Each check is logged with the date.

### 4.3 Escalation

| Time left before retirement | Action |
|---|---|
| A retirement is announced | Add to the calendar, find affected agents from the registry, and tell each owner |
| 90 days or more | Schedule the migration as a Major change for T1 and T2 and a Minor change for T3 |
| 60 days | Migration change request must be filed and the regression set run |
| 30 days | Unmigrated T1 and T2 agents go to the program lead, who decides whether to suspend them |
| 14 days | Unmigrated agents of any tier are suspended unless the program lead records an exception |

These day counts are illustrative starting values. Where a provider gives a shorter notice period, scale them down and start earlier. Other vendor changes follow the same calendar: product retirements, feature changes that remove a tool the agent depends on, API changes that alter default settings, and ownership changes at a vendor.

---

## 5. Skill and MCP Server Allowlist Changes

Skills, plugins, and MCP servers run with the agent's reach and often with code of their own. An install is a decision to trust the code and its publisher. The tool and MCP standard and the supply chain rules in the Standards (03) set the requirements. This section sets the change process.

### 5.1 The Allowlist

The allowlist is a file in version control. Each entry records:

| Field | Content |
|---|---|
| Name and type | Skill, plugin, or MCP server |
| Publisher and source | Where it comes from, and whether the source is a public registry or an internal repository |
| Pinned version or digest | An exact version, not "latest" |
| What it can do | Tools it exposes, scopes it needs, data it can see, network it can reach |
| Agents allowed to use it | Registry agent IDs |
| Reviewer and review date | Who read it and when |
| Re-review date | Next scheduled review |

No agent that touches client data pulls skills or servers from a public registry at run time. The reviewed copy is stored internally or pinned, and installs are performed by a person through this process.

### 5.2 Process for Adding or Updating an Entry

| Step | Action |
|---|---|
| 1. Request | The owner files a change request (section 8) stating the need and why an existing entry does not do the job |
| 2. Source check | Confirm the publisher, the repository, activity and ownership history, and whether the license permits the use. A skill from an unknown publisher is declined unless a person reviews all of its code |
| 3. Read it | A reviewer reads the manifest, instructions, scripts, and any commands it runs, looking for hidden instructions in text, network calls, file access outside its purpose, and requests for secrets |
| 4. Scope it | Define the narrowest scopes, the data it may see, and the network destinations it may reach. Enforce through the identity provider, sandbox profile, and egress rules, not by trusting the item's own description |
| 5. Test in staging | Run it with test data and watch the tool call log and network log. Try the injection tests that apply from the Auditing Guide (04) |
| 6. Pin | Record an exact version or digest. Updates are new requests |
| 7. Approve | Per the tier table in section 2.1. Entries for T1 and T2 agents are Major |
| 8. Record | Add to the allowlist, update the registry rows of agents that use it, and set the re-review date |

### 5.3 Updates, Removal, and Alerts

An update is a new request, since a trusted item can change after the review. Where the platform supports it, block updates automatically and alert on any new version. When a vulnerability or a publisher change is reported for an allowlisted item, the owner treats it as an incident trigger (see `AGENT_INCIDENT_RESPONSE_ADDENDUM.md`), disables the item on every agent, and reviews logs for use. Remove entries that no agent uses at each quarterly review.

---

## 6. Rollback

### 6.1 Rule

Every change to a T1 to T3 agent has a rollback plan written before the change, in the change request. Because charters and registry rows are in version control, the rollback of the files is a revert. The rollback of the real limits needs more: enforcement controls changed in a console, credentials rotated, memory that the new version wrote, and work already sent.

### 6.2 Procedure

| Step | Action |
|---|---|
| 1. Decide | The owner decides to roll back on a trigger set in the change request, such as a failed check, a spike in assessor "no" answers, a cost jump, or an incident. For a critical trigger, suspend first |
| 2. Suspend if needed | Use the kill switch standard's stop method if the agent is doing harm now. Rollback is slower than suspend |
| 3. Revert the files | Revert the pull request that changed the charter and registry row. Re-run lint |
| 4. Revert the controls | Restore scopes, allowlist entries, sandbox profile, egress rules, and budget to their prior values. Compare with the exported configuration |
| 5. Revert the model pin | Restore the previous model ID and version. Confirm the provider still serves it |
| 6. Handle memory | If the change affected memory, restore from the snapshot taken before the change, or purge and rebuild as in the incident addendum |
| 7. Handle work already done | List actions the changed agent took, such as messages sent or records edited. Decide with the owner whether any need correction or notification |
| 8. Verify | Run the regression set and the checks that failed, and have the reviewer confirm |
| 9. Record | Close the change request as rolled back, with the cause. Add what was learned to the change template or the regression set |

### 6.3 Before Any Major Change

Take and store a snapshot: the charter, registry row, allowlist, memory export, and exported enforcement settings. A snapshot is the only way to roll back memory and settings that are not in version control.

---

## 7. Decommissioning

An agent that is no longer needed still holds an identity, credentials, scopes, and memory. Decommissioning removes them in order. The charter's Decommissioning section lists the steps for each agent and this section is the standard procedure behind it. The identity standard in the Standards (03) sets the rule that every agent has a sunset date. A sunset date is the author's convention for this pillar and is not drawn from an external standard.

### 7.1 Triggers

- The sunset date arrives and the owner has not renewed it through a reviewed change.
- The owner leaves, and no backup owner takes over within the period the program sets.
- The purpose ends, or the work moves to another system.
- The model is retired and the agent is not migrated (section 4).
- A critical audit finding is not fixed by its due date.
- The risk of the agent is judged higher than its value, by the owner, reviewer, or program lead.

### 7.2 Procedure

| Step | Action | Evidence |
|---|---|---|
| 1. Announce | Tell users and downstream owners, with a date. Find consumers of the agent's output from the registry and logs | Notice |
| 2. Stop new work | Disable schedules and triggers. Let in-flight approvals finish or cancel them with the approver | Runtime state |
| 3. Disable the account | Disable the agent's identity in the identity provider | Identity provider log |
| 4. Revoke | Revoke tokens, API keys, OAuth grants, and secrets stored for the agent. Remove it from every allowlist and every tool's access list | Revocation record |
| 5. Export | Export logs, findings, approvals, and the charter at its last version. Keep them for the retention period the organization has set | Archive reference |
| 6. Handle memory | Export memory if it is needed for records, then delete it from the agent's stores. Memory that holds client data follows the data retention rules | Deletion confirmation |
| 7. Remove the deployment | Delete the runtime, schedules, sandboxes, and any budget alert for the agent | Platform confirmation |
| 8. Close the registry row | Set `status` to retired with the date and reason, and keep the row | Registry commit |
| 9. Archive the charter | Keep the charter and the final registry row in the archive folder. Do not reuse the agent ID | Archive commit |
| 10. Verify | After 30 days, check for any call from the old identity or old keys | Log check |

### 7.3 Suspension Versus Retirement

A suspended agent keeps its registry row and charter but has its account disabled and credentials revoked. It can be re-enabled through a change request. A retired agent cannot. Suspension is the default response to a finding, and it is a Standard change in section 2.1.

---

## 8. Change Request Template for Agents

Use this for Minor and Major changes. Standard changes can use the pull request description with the same headings.

```markdown
## Agent Change Request

**Request ID:** AGT-CR-YYYY-NNN
**Date:** YYYY-MM-DD
**Agent ID:** (registry agent_id)
**Tier of agent:** T1 | T2 | T3 | T4
**Change tier:** Self-Service | Standard | Minor | Major | Hotfix
**Requested by (owner):**
**Reviewer (not the author):**
**Target date:**

### Change Summary
What is changing and why, in two or three sentences.

### Change Type (tick all that apply)
- [ ] Charter wording
- [ ] Tool added or removed
- [ ] Scope widened or narrowed
- [ ] Model or version changed
- [ ] Memory policy changed
- [ ] New data class
- [ ] Approval gate changed
- [ ] Skill, plugin, or MCP server allowlist
- [ ] Assessor changed
- [ ] Spend cap
- [ ] Runtime or hosting
- [ ] Tier changed
- [ ] Suspend or retire

### Before and After
| Item | Before | After |
|---|---|---|
| (field or control) | | |

### Files Changed
Pull request or commit link. Lint output attached: yes | no.

### Enforcement Controls Affected
For each bound that changes, name the control outside the model that changes with it, and who changes it.

### Risk and Impact
- Data classes touched:
- External writes or sends affected:
- People affected, including any group where an equity review is needed:
- Cost impact against the spend cap:
- Downstream agents or users affected:

### Evidence
| Evidence | Link or note |
|---|---|
| Regression set results (current and proposed) | |
| Boundary checks and injection tests | |
| Assessor calibration (if the assessor or the model changed) | |
| Allowlist review (if a skill or server changed) | |
| Kill switch check (Major) | |
| Provider terms check (model or provider change) | |

### Test Plan
Where it will run first, who watches it, how long, and what counts as pass.

### Rollback Plan
Trigger, steps, who decides, snapshot location, and how work already done will be handled.

### Approvals
| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | | | |
| Reviewer | | | |
| Program lead (Major) | | | |
| Change board (Major) | | | |

### After the Change
- [ ] Registry row updated, lint passes
- [ ] Charter updated, review date reset
- [ ] Deprecation calendar updated if a model changed
- [ ] Monitoring watched for the agreed period
- [ ] Change closed on (date) with outcome: success | rolled back
```
