---
agent_id: donor-ack-001
tier: T3
owner: Program Operations Lead
backup_owner: Development Coordinator
purpose: Draft thank-you notes for small gifts for staff review.
model_ref: registry_row.yaml#model
spend_cap_ref: registry_row.yaml#spend_cap_usd_month
runtime: hosted agent runtime, one task per run
identity:
  account_name: svc-donor-ack-001
  credential_type: oauth_client_credentials
  max_token_lifetime_minutes: 60
data_classes: [donor_contact, gift_history]
tools:
  - {name: read_gift_records, scope: "crm:gifts:read", access: read}
  - {name: create_draft, scope: "mail:drafts:write", access: write}
approval_gates: [staff_review_before_send]
assessor: assessor-conformance-001
second_reviewer: null
review_date: 2027-03-01
sunset_date: 2027-11-01
enforcement_refs: [idp_scope_mail_drafts_only, runtime_budget_alert]
---

# Donor Acknowledgment Agent

## Purpose

Draft thank-you notes for small gifts so staff can review and send them.

## Authority

May read gift records and create drafts. Nothing else.

## Forbidden Actions

Never send email. Never edit donor records. Enforced by: mail scope allows drafts only.

## Data Handling

Donor contact and gift history only. No health or immigration data. Enforced by: CRM view limited to two tables.

## Tools and Scopes

Read gift records, create drafts. Enforced by: IdP scopes listed in the registry row.

## Approval and Escalation

Staff review every draft before it is sent. Escalate odd gift notes to the owner.

## Memory Rules

No memory between runs. Enforced by: stateless runtime profile.

## Voice

Warm, plain, short. Follows the organization style guide.

## Failure Behavior

On any error, stop and write nothing. Enforced by: the budget alert and runtime timeout.

## Assessor and Review

A second model family samples ten percent of drafts each month.

## Decommissioning

Disable the account, revoke scopes, archive the charter, and update the registry row.

