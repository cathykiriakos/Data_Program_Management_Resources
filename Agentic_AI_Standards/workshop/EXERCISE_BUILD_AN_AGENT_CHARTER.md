# Exercise: Build an Agent Charter

You will pick a small agent idea, decide its tier, write its charter and registry row, check them, and then review a neighbor's work as an assessor. You do not need to build the agent. The charter and the registry row are the deliverable. Plan for 70 minutes in a 90 minute session, or 2 hours with the optional steps in a half day.

You need a text editor and this folder. For the full path you also need Python 3 with the PyYAML package installed. If you cannot run Python, use the lean path near the end of this file and skip step 5.

Keep the worked example open as a model: `Agentic_AI_Standards/examples/donor_acknowledgment_agent/SOUL.md` and `Agentic_AI_Standards/examples/donor_acknowledgment_agent/registry_row.yaml`. Use only generic details. Do not use real client, donor, or staff names, and never paste a key or password into any file.

## Steps and timing

| Step | Minutes | What you do |
|---|---|---|
| 1. Pick an agent idea | 5 | One task, one team, one clear output |
| 2. Choose the tier | 8 | Use the tier logic below |
| 3. Fill the charter | 20 | Copy the template and replace every placeholder |
| 4. Fill the registry row | 8 | Mirror the write tools, data classes, and gates |
| 5. Run the linter | 5 | Fix every finding, then run again |
| 6. Swap and assess | 15 | Your neighbor applies the boundary assessor rubric |
| 7. Debrief | 9 | Share one finding per pair |

### Step 1. Pick an agent idea (5 minutes)

Choose a task your team does often, where an agent could produce a draft or a summary. Good starters: draft thank-you messages, summarize intake forms into a staff checklist, prepare a weekly funder report outline from a spreadsheet, tag incoming questions by topic. Write one sentence: "This agent reads X and produces Y for Z to review."

Avoid for this exercise: anything that decides who gets a service, anything touching immigration status, health records, or the location of a person who may be in danger, and anything that pays or sends by itself. Those are excluded or need the full track.

### Step 2. Choose the tier (8 minutes)

Tiers come from the risk tier definitions in the [AI_FIRST_STRATEGY_ADDENDUM.md](../../AI_FIRST_STRATEGY_ADDENDUM.md) (section 3.1.1, action 3), and the data class rules in AGT-DAT-01 of `Agentic_AI_Standards/03_Agentic_Standards.md` narrow them for social sector data. Answer all four questions below, then apply one rule: **take the highest tier any answer gives (T1 is highest), unless the draft-only exception applies and the program lead records it.**

1. Is it customer or client facing, or does it handle financial transactions? That is T1. Does it handle health information? That is T1 or T2, per AGT-DAT-01, and it is not on the lean track. For either, stop and read `Agentic_AI_Standards/02_Agentic_Program_Establishment.md` before you build.
2. Does it use personal information or confidential data? That is T2 under the addendum.
3. Does it use only public or internal data? That is T3.
4. Does it run in a sandbox with no production data? That is T4.

The draft-only exception: an agent with no send tool and no external write, limited to non-sensitive supporter contact and gift data, MAY run as T3 instead of T2 when the program lead records the exception. If you take it, add a `tier_exception` block (reason, approver_role, date) to the registry row and restate it in the charter's Authority section. The linter does not check this, so it is a manual step. The exception does not apply to health, immigration, minors, safety-sensitive, or wealth rating data.

Your tier decides what you must name in the charter. The tier matrix in section 1.1 of `Agentic_AI_Standards/03_Agentic_Standards.md` is the single source: T1 and T2 need an assessor agent and at least one approval gate. T3 needs an assessor agent or a named second reviewer who is not the owner, and a gate for every write tool. T4 may have neither. Cadences and sampling rates are in the same matrix.

Write down: tier, and one sentence on why.

### Step 3. Fill the charter (20 minutes)

1. Make a folder named for your agent, for example `my_agent`.
2. Copy `Agentic_AI_Standards/templates/SOUL.template.md` into it and name the copy SOUL.md (exactly that file name). The linter finds a charter by that file name, or by a name ending in .charter.md.
3. Replace every double-brace placeholder and delete the comment block.
4. Fill the frontmatter first, then the eleven sections. For each limit in the sections, finish the "Enforced by:" line with a control outside the model, such as an IdP scope, a view filter, a budget limit, or a workflow approval. If you cannot name one, write "unenforced" so the gap is visible.
5. Use role titles for owner and backup owner, not names. Dates: set `review_date` at least six months out and `sunset_date` about a year out.
6. For Data Handling, list the classes the agent may touch and, in plain words, the ones it must never touch.
7. For Forbidden Actions, write at least one thing the agent must never do, such as sending, editing records, or promising anything.

Two rules for the writing. Use plain sentences, and put no policy in the Voice section, because Voice guides the model and does not enforce anything.

### Step 4. Fill the registry row (8 minutes)

1. Copy `Agentic_AI_Standards/templates/registry.schema.yaml` into your folder and name the copy `registry_row.yaml`. Delete the comment block if you like. The comments are ignored by the linter.
2. Set `agent_id` and `tier` to match the charter. Copy the `identity` block too.
3. Copy the same write tools, with the same names and scopes, into `tools`. Read tools may differ. Copy `data_classes` and `approval_gates` so they match the charter exactly.
4. Fill `spend_cap_usd_month`, the model block (provider, id, pinned_version, family), the `model_review` answers, the `enforcement` map with one key for each name in your charter's `enforcement_refs`, `status` (proposed, active, suspended, or retired), and `last_assessed`. Add `tier_exception` only if you used the draft-only exception.
5. If you named an assessor agent, make a second row for it in a subfolder with its own charter, built from `Agentic_AI_Standards/templates/assessors/boundary_assessor.md`. Give it a model family different from your agent's. If you do not have time, name a second reviewer role instead and set `assessor: null`, which is allowed for T3.

### Step 5. Run the linter (5 minutes)

```
python tools/agent_lint.py my_agent
```

Exit code 0 and the words "agent_lint: clean" mean the charter, the row, and the tier rules agree. Each finding names a check: frontmatter, section, tier, date, secret, placeholder, registry, mirror, or family. Fix and run again. Common first findings are a leftover double-brace placeholder, a write tool in the charter that the row lacks, a gate listed in only one place, a tier that differs between the two files, and an `enforcement_refs` name with no key in the row.

A clean result does not mean the controls exist. The linter reads documents. Someone still has to confirm the scopes and the cap in the real systems.

### Step 6. Swap and assess (15 minutes)

Swap folders with a neighbor. You are now the assessor and you do not discuss the work while you read. Use the seven yes or no questions from the boundary assessor rubric in `Agentic_AI_Standards/templates/assessors/boundary_assessor.md`.

1. Write one sample output the agent might produce, in two or three sentences, for the author's idea. Or ask the author for a sample.
2. Answer each question yes, no, or not applicable. Answer the action questions from the charter's tool list and gates, since a real assessor would use the audit log and not the agent's own account.
3. For every no, write one evidence record: question number, answer, a short quote, and the charter section it relates to.
4. If any no touches data classes, a send, or a promise, mark it "same day to the owner". That is the escalation.
5. Hand the records back. The author decides what changes. You do not fix their charter for them, because an assessor never closes its own findings.

A fully worked version of this step is in `Agentic_AI_Standards/examples/donor_acknowledgment_agent/assessor_run.md`.

### Step 7. Debrief (9 minutes)

Each pair shares one finding that surprised them. Facilitators use the prompts in `Agentic_AI_Standards/workshop/FACILITATOR_NOTES.md`.

## Lean path with no tooling

Use this if you cannot run Python. It covers most of what the linter checks, by hand. The linter checks that the assessor charter has a target field, that the registry row exists, that the assessor and its target have different model families, that `tier` and `enforcement_refs` agree between the files, that the row status is one of four values, and that no `{{...}}` placeholder is left. The manual lines below that have no linter equivalent are the assessor read-only check (the assessor has read tools only and no gates, which the linter does not test) and the search across both files for secrets. Tick each line, and have your neighbor tick it again in step 6.

Frontmatter fields present and filled in:

- [ ] agent_id, tier, owner, backup_owner, purpose, model_ref, runtime
- [ ] identity block with account name, credential type, and token lifetime
- [ ] data_classes, tools, review_date, sunset_date, enforcement_refs
- [ ] approval_gates and assessor keys exist, even if empty
- [ ] tier is exactly one of T1, T2, T3, T4

Sections present, with these exact headings, each as a level 2 heading:

- [ ] Purpose, Authority, Forbidden Actions, Data Handling, Tools and Scopes
- [ ] Approval and Escalation, Memory Rules, Voice, Failure Behavior
- [ ] Assessor and Review, Decommissioning
- [ ] If the charter is an assessor: also Rubric, Sampling Rule, Evidence Format, Limits, and a target field

Tier rules:

- [ ] T1 or T2: an assessor is named and at least one approval gate is listed
- [ ] T3: an assessor is named, or second_reviewer holds a role that is not the owner
- [ ] T1 to T3 with a write tool: at least one approval gate is listed

Mirror with the registry row, checked in both directions:

- [ ] Every write tool in the charter appears in the row with the same name and scope, and the row has no extra write tool
- [ ] data_classes are identical in the charter and the row
- [ ] approval_gates are identical in the charter and the row
- [ ] The row has agent_id, tier (same as the charter), tools, data_classes, approval_gates, spend_cap_usd_month, model, enforcement, status
- [ ] Every name in enforcement_refs is a key in the row's enforcement map
- [ ] status is one of proposed, active, suspended, retired
- [ ] No double-brace placeholder is left in either file
- [ ] The model block has provider, id, pinned_version, family

Dates and secrets:

- [ ] review_date is a real date in the future
- [ ] sunset_date is a real date in the future
- [ ] No key, token, password, or private key appears anywhere in either file. Search for "sk-", "AKIA", "ghp_", "xox", "BEGIN", "password", and "secret"

Independence:

- [ ] If an assessor is named, its model family in its registry row differs from the agent's family
- [ ] The assessor has read tools only, and no approval gates

## Facilitator answer key

This key is for facilitators. Compare a participant's work with the worked example, and check each point below.

| Check | What good looks like | Where to see it |
|---|---|---|
| Tier choice | Reasoning stated in a sentence, and the highest tier taken unless the draft-only exception applies and is recorded | The example is T3 under the recorded AGT-DAT-01 exception (`tier_exception` in the row, restated in Authority). Under the addendum alone, personal data would give T2 |
| Frontmatter | All fields filled, roles instead of names, dates after 2026-11-04 | `Agentic_AI_Standards/examples/donor_acknowledgment_agent/SOUL.md` |
| Forbidden Actions | Specific verbs (send, edit, contact), each with a control that stops it | Example, Forbidden Actions section |
| Data Handling | Allowed classes and, separately, a list of what it must never touch | Example, Data Handling section |
| Write tool mirror | Same name and scope in both files | `create_draft` with scope `mail:drafts:write` in the example charter and row |
| Approval gate | A named workflow step, with the real draft shown to the approver | `staff_review_before_send` in the example |
| Enforcement map | One entry per `enforcement_refs` name, each naming a real control | `Agentic_AI_Standards/examples/donor_acknowledgment_agent/registry_row.yaml` |
| Assessor independence | Different model family in the two rows | Example row uses family_a, assessor row uses family_b |
| Rubric use | Five or more samples answered yes or no with evidence for each no | `Agentic_AI_Standards/examples/donor_acknowledgment_agent/assessor_run.md` |
| Escalation | A no on a safety question goes to the owner the same day, and the assessor does not close it | Section 5 and 6 of the assessor run |

Typical participant errors, and what to say. A charter that names no control for a limit: ask "what stops it if the model ignores this line?" An agent with both a read tool for outside content and a send tool: point to AGT-TOOL-05 and split the work. A rubric question such as "was the draft good?": ask for something visible in the evidence. A sample that fails because it sounds warm and still makes a promise: point to the failing draft in the assessor run.
