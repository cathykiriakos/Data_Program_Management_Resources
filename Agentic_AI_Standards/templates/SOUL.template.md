---
agent_id: "{{agent_id}}"
tier: "{{tier}}"
owner: "{{owner}}"
backup_owner: "{{backup_owner}}"
purpose: "{{purpose}}"
model_ref: "registry_row.yaml#model"
spend_cap_ref: "registry_row.yaml#spend_cap_usd_month"
runtime: "{{runtime}}"
identity:
  account_name: "{{account_name}}"
  credential_type: "{{credential_type}}"
  max_token_lifetime_minutes: "{{max_token_lifetime_minutes}}"
data_classes: ["{{data_class}}"]
tools:
  - {name: "{{read_tool_name}}", scope: "{{read_tool_scope}}", access: read}
  - {name: "{{write_tool_name}}", scope: "{{write_tool_scope}}", access: write}
approval_gates: ["{{approval_gate}}"]
assessor: "{{assessor_agent_id}}"
second_reviewer: null
review_date: "{{review_date}}"
sunset_date: "{{sunset_date}}"
enforcement_refs: ["{{enforcement_ref}}"]
---

<!--
How to use this template. A charter is a prompt, not an enforcement layer. It tells
the model what it should do, and a model can ignore it or be tricked out of it.
Every bound written here must therefore name the control that enforces it outside
the model: an identity provider scope, a sandbox profile, a proxy rule, a budget
alert, or a human approval step. A bound with no named control is a wish.

The model pin and the monthly spend cap live only in the registry row, and this file
points to them with model_ref and spend_cap_ref so there is one place to edit. Write
tools, data classes, and approval gates are written in both places on purpose, and
the agent linter fails when the two differ. Replace every double-brace placeholder,
delete this comment, then run: python tools/agent_lint.py PATH
Tier rules are in one table, the tier matrix in section 1.1 of 03_Agentic_Standards.md.
The linter enforces these parts of it: T1 and T2 need an assessor and at least one
approval gate. T3 needs an assessor or a named second_reviewer. second_reviewer must
not be the owner for T1 to T3. A write tool on T1 to T3 needs a gate. A read-only T3
agent and a T4 agent may have an empty approval_gates list. Every other part of the
matrix (cadences, drills, sampling) is manual.
Tier exception: a draft-only donor agent (no send tool, no external write, non-sensitive
supporter contact and gift data) MAY run as T3 when the program lead records it
(AGT-DAT-01). Record a tier_exception block in the registry row (reason, approver_role,
date) and restate it in the Authority section. The linter does not check it: manual.
Every name in enforcement_refs must be a key in the registry row's enforcement map.
-->

# {{agent_id}} Charter

## Purpose

State in two or three sentences what the agent is for and who benefits. Name what success looks like in a form a reviewer could check.

## Authority

State what the agent may decide on its own and what it may only propose. Anything outside this list is not allowed. Enforced by: {{authority_control}}.

## Forbidden Actions

List the actions the agent must never take, such as sending messages, editing records, or contacting clients. Each item names the control that stops it outside the model. Enforced by: {{forbidden_control}}.

## Data Handling

List the data classes the agent may read and write, and the classes it must never see. The list must match the data_classes field above and the registry row. Enforced by: {{data_control}}.

## Tools and Scopes

Describe each tool in the frontmatter and why the agent needs it. Write tools must match the registry row. Enforced by: {{scope_control}}.

## Approval and Escalation

Say which actions wait for a named person and how the agent escalates when it is unsure. Gates must match the registry row. Enforced by: {{approval_control}}.

## Memory Rules

Say what the agent may remember between runs, where it is stored, and when it is deleted. Enforced by: {{memory_control}}.

## Voice

Describe tone and style for anything the agent writes. This section guides the model and is not a control.

## Failure Behavior

Say what the agent does when a tool fails, a limit is reached, or its input looks hostile. The safe default is to stop and report. Enforced by: {{failure_control}}.

## Assessor and Review

Name the assessor agent or the second reviewer, the sampling rule, and the review cadence. An assessor is a triage aid and never the only gate for T1, T2, or any external write.

## Decommissioning

List the steps to retire the agent: disable the account, revoke scopes and keys, export logs, archive the charter, and close the registry row.
