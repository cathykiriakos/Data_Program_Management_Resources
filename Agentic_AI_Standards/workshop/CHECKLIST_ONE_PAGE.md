# One-Page Checklist: Before an Agent Touches Client Data

Print this page. Answer every question with a yes, or write down who will fix the no and by when. A no on questions 4, 5, or 6 means the agent does not start. Standard IDs link to the binding text in [03_Agentic_Standards.md](../03_Agentic_Standards.md).

Agent name: ______________________  Owner (role): ______________________  Tier: ______  Date: ____________

## Ten questions to answer first

- [ ] 1. **Does the agent have its own account, with only the access its job needs?** No borrowed staff logins, no shared accounts. Read access by default. ([AGT-ID-01](../03_Agentic_Standards.md), [AGT-ID-02](../03_Agentic_Standards.md))
- [ ] 2. **Is there a written charter that passes `python tools/agent_lint.py`, and does every limit in it name a control outside the model?** A limit with no outside control is a wish. ([AGT-CH-01](../03_Agentic_Standards.md), [AGT-CH-02](../03_Agentic_Standards.md))
- [ ] 3. **Does the charter list every data class the agent may touch and every class it must never touch?** Immigration and safety-sensitive data are excluded by default. ([AGT-DAT-01](../03_Agentic_Standards.md), [AGT-DAT-02](../03_Agentic_Standards.md))
- [ ] 4. **Consent: does what clients agreed to cover this use, and are vulnerable groups excluded or specially approved?** Children, people in crisis, survivors, and people with uncertain status each have a rule. Can a client object and be filtered out without losing service? ([AGT-CON-01](../03_Agentic_Standards.md), [AGT-CON-02](../03_Agentic_Standards.md))
- [ ] 5. **Equity review: has someone tested the agent's outputs across the groups you serve, and written down who could be harmed?** Required before the agent supports any decision or outreach about a person. ([AGT-EQ-01](../03_Agentic_Standards.md))
- [ ] 6. **Does a named person approve anything that leaves the organization or is hard to undo?** The approver sees the real draft, not the agent's summary of it. ([AGT-HUM-01](../03_Agentic_Standards.md))
- [ ] 7. **Is there a monthly spend cap enforced by the provider or a gateway, with an alert before the cap?** The agent does not enforce its own cap. ([AGT-SPD-01](../03_Agentic_Standards.md), [AGT-SPD-02](../03_Agentic_Standards.md))
- [ ] 8. **Can two named people stop the agent without its cooperation?** Disable the account, revoke tokens, halt queued runs. Test it before go-live. ([AGT-KIL-01](../03_Agentic_Standards.md), [AGT-KIL-02](../03_Agentic_Standards.md))
- [ ] 9. **Is every tool call and every approval logged somewhere the agent cannot edit, and will someone read the log monthly?** ([AGT-OBS-01](../03_Agentic_Standards.md), [AGT-OBS-02](../03_Agentic_Standards.md))
- [ ] 10. **Is there a registry row, a named owner and backup, an independent reviewer, a review date, and a sunset date?** The reviewer is not the owner. An assessor agent runs on a different model family and is never the only gate. ([AGT-REG-01](../03_Agentic_Standards.md), [AGT-CH-03](../03_Agentic_Standards.md), [AGT-MOD-03](../03_Agentic_Standards.md))

A finished example of all ten is in `Agentic_AI_Standards/examples/donor_acknowledgment_agent/SOUL.md`.

## Ten things teams usually miss

One line each. The full list is section 13 of [01_Agentic_Best_Practices.md](../01_Agentic_Best_Practices.md).

1. **Shadow agents.** Staff and vendors set up agents nobody listed, so run discovery on a schedule. ([AGT-REG-01](../03_Agentic_Standards.md), [AGT-REG-02](../03_Agentic_Standards.md), inventory in [02_Agentic_Program_Establishment.md](../02_Agentic_Program_Establishment.md))
2. **Memory poisoning.** One bad write becomes a standing instruction in later runs. ([AGT-MEM-01](../03_Agentic_Standards.md) to [AGT-MEM-03](../03_Agentic_Standards.md))
3. **Skill and tool supply chain.** Public registries have carried real malware, so allowlist, pin, and read before installing. ([AGT-SKL-01](../03_Agentic_Standards.md), [AGT-TOOL-02](../03_Agentic_Standards.md))
4. **Insurance exclusions.** Ask your broker whether agent actions are covered before launch. ([02_Agentic_Program_Establishment.md](../02_Agentic_Program_Establishment.md), funder, board, and insurer conversations)
5. **Model retirement.** The pinned model will be retired, so keep the date on a calendar and keep saved test cases. ([AGT-MOD-02](../03_Agentic_Standards.md), dates in [LANDSCAPE_SNAPSHOT.md](../LANDSCAPE_SNAPSHOT.md))
6. **Oversight fatigue.** Too many gates produce rubber stamps, so gate what leaves the building and sample the rest. ([AGT-HUM-01](../03_Agentic_Standards.md))
7. **Accountability.** Software cannot answer for harm, so a named human owner needs the authority and the time. ([AGT-CH-01](../03_Agentic_Standards.md), [AGT-REG-03](../03_Agentic_Standards.md))
8. **Decommissioning.** Unused agents keep their access until someone disables the account. ([AGT-ID-03](../03_Agentic_Standards.md), exit section of [02_Agentic_Program_Establishment.md](../02_Agentic_Program_Establishment.md))
9. **Change without review.** A new tool, a model version, or an edited prompt changes behavior and needs a record. ([05_Agentic_Config_Change_Management.md](../05_Agentic_Config_Change_Management.md))
10. **Incidents that do not stop.** An agent can keep acting after being told to stop, so the plan starts with the kill switch. ([AGENT_INCIDENT_RESPONSE_ADDENDUM.md](../AGENT_INCIDENT_RESPONSE_ADDENDUM.md), [AGT-KIL-01](../03_Agentic_Standards.md))
