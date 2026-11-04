# Agentic AI Landscape Snapshot

**Document Owner:** Data Program Management Library maintainers
**Classification:** Internal, volatile reference
**Version:** 1.0 | **Last Updated:** 2026-11
**Review Cycle:** Quarterly

> **Check before relying.** Every fact in this document was read on 2026-11-04 and goes stale on its own schedule. Dates, versions, licences and prices below are the only place in the pillar where they are stated. Other pillar documents describe durable practice and point here. Before the 2026-11-12 workshop, re-check the rows marked with a short shelf life: model retirement dates, AIUC-1, the MCP revision, Colorado and EU dates. Tags such as [S01] point to rows in SOURCES.md, which holds the URL, access date and confidence for each claim. A claim tagged to a row marked unverified or secondary only must not be taught as settled.

## How to read confidence

Confirmed means a primary page was fetched and the value was seen. Secondary only means a search summary, law firm note or vendor blog was the source. Unverified means no usable source was read, often because the primary page returned HTTP 403. Where this snapshot gives a fact from a secondary or unverified row, the text says so.

## Date conflicts from the earlier scan, resolved

| Item | Earlier conflict | Winning primary evidence | Tag |
|---|---|---|---|
| A2A v1.0 | March versus April 2026 | GitHub release v1.0.0 is dated 12 Mar 2026; v1.0.1 followed on 28 May 2026 | [S29] |
| Entra Agent ID general availability | 30 Apr versus 1 May 2026 | Microsoft Learn lists it under April 2026 and gives no day, so only the month is confirmed | [S35] |
| Five Eyes agentic guidance | 30 Apr versus 1 May 2026 | NCSC New Zealand page shows 1 May 2026; the PDF file path carries 30 Apr, so both dates are in circulation and 1 May is the stated publication date | [S08] |
| Anthropic Responsible Scaling Policy | 3.1 versus 3.4 | Version history shows 3.1 on 2 Apr 2026 and 3.4 effective 8 Jul 2026; 3.4 is current and both earlier reports were real versions at different times | [S22] |

## 1. Standards and regulation (read 2026-11-04)

The standards below are voluntary except where noted. For a small organisation the useful free baselines are the Five Eyes guidance, the OWASP agentic list and the NIST work in progress. AIUC-1 and ISO/IEC 42001 are certification routes that most small teams will use as vocabulary rather than adopt.

| Item | What was confirmed | Confidence | Tag |
|---|---|---|---|
| AIUC-1 | Quarterly releases. Latest is 15 Oct 2026: 5 new requirements, 5 new controls, 3 retired requirements, 78 core controls, no separate version number on the page. Open-weight controls cover testing after model changes (C002.4), source, integrity and licence verification (E006.2) and cyber evaluation of modified models. Third-party testing is one requirement per principle. Human approval for sensitive tool operations (D003.4) became core. Next release is 15 Jan 2027. The release page and the changelog disagree on one control number (F001.2 versus F001.3) and on how many requirements are new (5 versus 2 listed) | confirmed | [S01] [S02] [S03] [S04] |
| AIUC-1 structure | Five principles: Data and Privacy, Security, Safety, Reliability, Accountability. The earlier claim of six domains including Society was not seen | confirmed | [S05] |
| NIST AI RMF | Version 1.0 (26 Jan 2023) is current and is being revised under the White House AI Action Plan. Generative AI Profile (AI 600-1) dated 26 Jul 2024. Critical infrastructure profile is a concept note dated 7 Apr 2026 | confirmed | [S06] |
| NIST agent work | AI Agent Standards Initiative with three pillars: industry-led standards, community-led protocols, and research on agent identity and security evaluation. The NCCoE agent identity paper is still a draft concept paper. No final publication is listed, page last updated 14 Aug 2026. Agent overlays for SP 800-53 were not found | confirmed (overlays: unverified) | [S07] [S24] |
| Five Eyes joint guidance | Title "Careful Adoption of Agentic AI Services", dated 1 May 2026, co-authored by ASD ACSC, CISA, NSA, Canadian Cyber Centre, NCSC-NZ and NCSC-UK. Risk categories reported as privilege, design and configuration, behavioural, structural and accountability. The count of recommendations and their text were not read because CISA and the PDF returned HTTP 403 | date confirmed; categories secondary only; recommendation count unverified | [S08] [S09] [S10] |
| ISO/IEC 42001 | Certifiable AI management system (2023). The ISO page returned HTTP 403 | unverified | [S11] |
| OWASP Top 10 for Agentic Applications | Published 9 Dec 2025. ASI01 Agent Goal Hijack, ASI06 Memory and Context Poisoning and ASI10 Rogue Agents are named in OWASP roundups; the other seven names are not listed in this edition | date confirmed; names secondary only | [S12] [S13] |
| OWASP Top 10 for LLM Applications | 2025 edition is current; includes Supply Chain, Excessive Agency and Unbounded Consumption | confirmed | [S14] |
| MITRE ATLAS | Data repository tags techniques for an Agentic AI platform and has AI agent software categories. Version, date and technique counts were not shown and agent techniques were not reviewed | confirmed (limited) | [S15] |
| CSA | Agentic Trust Framework published 2 Feb 2026 under CC BY 4.0: identity, behavior, data governance, segmentation, incident response, plus a four-level maturity model; authored by a research fellow whose firm sells services in this area. MAESTRO and the autonomy levels framework were not fetched | ATF confirmed; others unverified | [S16] [S17] |
| EU AI Act, Digital Omnibus | Reg. (EU) 2026/1744 moves Annex III high-risk obligations to 2 Dec 2027 and Annex I to 2 Aug 2028. Art. 50(2) applies from 2 Dec 2026 for systems already on the market before 2 Aug 2026. New Art. 5 bans (non-consensual intimate imagery, child sexual abuse material generators) apply from 2 Dec 2026. Official Journal 24 Jul 2026 and entry into force 27 Jul 2026 appear only in search summaries. EUR-Lex returned no text, so confirm on the Official Journal before teaching dates | secondary only | [S18] [S19] |
| Colorado | SB26-189 signed 14 May 2026. It repeals and reenacts the SB24-205 protections for automated decision-making technology in consequential decisions. Developer obligations begin 1 Jan 2027, the attorney general must adopt disclosure rules by 1 Jan 2027, no new private right of action, 60-day cure notice before actions until 1 Jan 2030. Reported litigation and nonprofit coverage were not found on the bill page | confirmed (litigation, nonprofit coverage: unverified) | [S20] [S21] |
| Anthropic RSP | Version 3.4, effective 8 Jul 2026 | confirmed | [S22] |
| OpenAI Preparedness Framework, Google DeepMind Frontier Safety Framework | Version numbers and dates were not fetched | unverified | [S23] |

## 2. Identity and protocols (read 2026-11-04)

Protocol governance has consolidated: MCP, A2A, Agent Skills, AGENTS.md and goose are now all hosted by the Agentic AI Foundation under the Linux Foundation [S31] [S32]. Lock-in risk now sits more in proprietary agent builders than in these formats.

| Item | What was confirmed | Confidence | Tag |
|---|---|---|---|
| MCP revision | Current revision is 2026-07-28. Deprecated features stay at least twelve months before removal unless expedited | confirmed | [S25] |
| MCP authorization | Authorization is optional. HTTP transports should follow the spec, STDIO should not and instead reads credentials from the environment. Servers must publish Protected Resource Metadata (RFC 9728). Clients must send the RFC 8707 resource parameter and servers must reject tokens not issued for them. Client ID Metadata Documents are preferred, Dynamic Client Registration is deprecated. Clients must validate a returned iss value (RFC 9207); servers should send it and a later revision is expected to require it | confirmed | [S26] |
| MCP 2026-07-28 release | Stateless protocol, HTTP+SSE deprecated with a year-long transition, Dynamic Client Registration, roots, sampling and logging deprecated. Tasks, MCP Apps and Enterprise Managed Authorization are extensions. A stable date of 18 Jun 2026 for the last one was not found | confirmed (date: unverified) | [S27] [S28] |
| A2A | v1.0.0 on 12 Mar 2026, v1.0.1 on 28 May 2026. Joined the Agentic AI Foundation as a hosted project, AAIF post dated 17 Aug 2026. Signed agent cards prove the publisher, not what an agent may access | confirmed | [S29] [S30] |
| Agentic AI Foundation | Announced 9 Dec 2025 with MCP, goose and AGENTS.md. Hosts ten projects including Agent Skills, A2A, agentgateway, Open Responses and OpenSandbox | confirmed | [S31] [S32] |
| Agent Skills | Anthropic announced on 22 Oct 2026 that it is donating the standard to the foundation. The page claims over 70 platforms, 1 million skills and nearly 280 million installs; treat these as vendor claims | confirmed (counts are vendor claims) | [S33] |
| AGENTS.md | Stewarded by the foundation; the site claims over 60 thousand open-source projects | confirmed | [S34] |
| Microsoft Entra Agent ID | General availability in April 2026 (month only). Agent 365 is the unified registry and control plane. The price of about 15 USD per user per month was not found | confirmed (price: unverified) | [S35] [S36] |
| Okta | Agent SSO (Cross App Access) generally available 24 Aug 2026, included in core SSO at no extra cost. Okta for AI Agents generally available since May 2026 on a separate subscription | confirmed | [S37] |
| Auth0 | Auth0 for AI Agents and Auth for MCP general availability dates were not fetched | unverified | [S38] |

A markdown charter file is a prompt, not a control. Scopes, spend caps, tool allow-lists and approval gates have to be enforced in the identity provider, sandbox or proxy, and the charter mirrors them. This is the pillar's own design position, supported by the OWASP goal hijack and memory poisoning entries [S13].

## 3. Agent runtimes and tooling (read 2026-11-04)

Grades are the library's judgement from the evidence in the cited row, not endorsements. Teach: use as a worked example in a workshop. Trial: reasonable to pilot with a charter and approval gates. Watch: interesting, not yet recommended for client data. Avoid: do not use for agents that touch client data. The pillar stays runtime-neutral.

| Runtime | Grade | Licence | Why | Tag |
|---|---|---|---|---|
| Microsoft Agent Framework | teach | MIT | Active releases on Python and .NET (tags dated 30 Oct 2026), migration guides from AutoGen and Semantic Kernel; version 1.0 on 3 Apr 2026 is secondary only | [S39] [S40] |
| Claude Agent SDK (Python) | trial | MIT, plus Anthropic Commercial Terms | Maintained SDK that runs the Claude Code loop; ties you to one vendor's models and terms; release history not shown on the page | [S43] |
| OpenAI Agents SDK (Python) | trial | MIT | Provider-agnostic with guardrails, handoffs and tracing; release history not shown; OpenAI is retiring its hosted Agent Builder, so build on the SDK only | [S44] [S60] |
| Google ADK (Python) | trial | not shown on page | Frequent releases (v2.13.0, 22 Oct 2026); licence and 2.0 date not confirmed | [S41] |
| LangGraph | trial | not shown on page | Core package at 1.2.19 (30 Oct 2026); licence and 1.0 date not confirmed | [S42] |
| goose | trial | Apache-2.0 | Now an AAIF project, so governance is neutral; local agent aimed at developers | [S46] |
| OpenHands | watch | MIT | Self-hosted coding-agent control center; coding focus, little relevance to office work | [S47] |
| Letta | watch | Apache-2.0 | Self-improving memory is the feature and also the OWASP memory poisoning risk | [S45] [S13] |
| OpenClaw class | avoid for client data | MIT | Very large user base (about 394 thousand stars) but a public skill marketplace with a documented malicious-skill campaign and an untrusted-input warning in its own README | [S48] [S73] |

Tools named under the breadth cap, one per category plus close neighbours that were read:

| Category | Tool | Licence and ownership | Tag |
|---|---|---|---|
| Evaluation | Inspect AI (UK AI Security Institute) | MIT; over 200 pre-built evaluations | [S50] |
| Red team | garak (NVIDIA) | Apache-2.0 | [S51] |
| Red team | PyRIT (Microsoft) | MIT | [S52] |
| Red team and eval | promptfoo | MIT; now part of OpenAI, which also names it the migration path off its own retiring Evals platform, so weigh independence when auditing OpenAI models | [S53] [S60] |
| Observability | Langfuse | MIT except ee folders; part of ClickHouse since Jan 2026 | [S54] |
| Observability standard | OpenTelemetry GenAI agent spans | Development status, so expect change; create_agent and invoke_agent spans confirmed | [S56] |
| Guardrail | NeMo Guardrails (NVIDIA) | Apache-2.0; 0.24.1 | [S55] |
| Guardrail model | Llama Guard 4 12B, Prompt Guard 2 | Listed on the meta-llama organisation page; licence terms not read | [S57] |

The earlier claim for OpenClaw CVE counts and for Hermes Agent was not checked [S49].

## 4. Model families (read 2026-11-04)

Pin an exact model identifier in the registry, put the retirement date on a calendar and re-run evaluations before any cutover. Retirement dates move, and partner platforms such as Amazon Bedrock set their own schedules [S58].

### Hosted models

| Family | Terms and residency note | Retirement or deprecation dates seen | Tag |
|---|---|---|---|
| Anthropic Claude | Commercial terms. US-only inference by request (inference_geo us) at 1.1 times standard rates on Claude 4.6 and later; default is global routing; workspace geo is US only; eligible for zero data retention and HIPAA readiness | Sonnet 4.5 retires 30 Nov 2026 (replacement Sonnet 5.5); Opus 4.1 retired 5 Aug 2026; Opus 4.5 not sooner than 24 Nov 2026; Haiku 4.5 not sooner than 15 Oct 2026; Sonnet 5.5 not sooner than 28 Sep 2027; at least 60 days notice. API version 2026-10-21 removes temperature, top_p and top_k | [S58] [S59] [S62] |
| OpenAI | API data not used for training unless opted in; abuse logs kept up to 30 days; zero retention only for approved customers; in-region processing in the US and Europe, storage-only in other regions; 10 percent uplift on residency endpoints for eligible newer models; needs sales contact | GPT-5 family and o3 snapshots shut down 11 Dec 2026; Agent Builder, Evals platform and reusable prompts 30 Nov 2026; Assistants API 26 Aug 2026 | [S60] [S63] |
| Google Gemini | Residency terms not researched | gemini-2.0-flash shut down 1 Jun 2026; gemini-2.5-pro and 2.5-flash 1 Dec 2026; gemini-3.1-flash-lite 7 May 2027 (earliest dates) | [S61] [S64] |
| Microsoft-hosted | Claude on Foundry can use the US Data Zone deployment type with the same 1.1 times multiplier; Microsoft's own model terms not researched | Not researched | [S62] [S64] |

### Open-weight models

Self-hosting keeps data where you run the model, but it moves patching, provenance checking and evaluation to you. AIUC-1 now has controls for verifying the source, integrity and licence of open-weight models [S02]. Licence terms below are from the files or model cards named in SOURCES.md. Read the file for the exact checkpoint you download, because licences differ within one family.

| Family | Licence seen | Note | Confidence | Tag |
|---|---|---|---|---|
| DeepSeek V4.1 Flash | MIT (model card) | Release date from the earlier scan not seen | confirmed | [S65] |
| gpt-oss 120b | Apache 2.0 (model card) | | confirmed | [S66] |
| Gemma 4 31B instruction-tuned | apache-2.0 tag; a separate Gemma 4 licence document is linked and was not read | Check the linked document | confirmed | [S67] |
| Qwen3.8 | Flash-Next uses the Qwen Community License 1.0, which needs a separate licence for model-as-a-service and AI work assistant businesses and exempts internal use. 2.4T-A95B is reported as a custom licence and 27B as Apache 2.0, neither file read | Mixed licences inside one family | Flash-Next confirmed; others secondary only | [S68] [S69] |
| Mistral Large 4 | Mistral Ecosystem Open-Weight License, described by Mistral as modified MIT with a commercial licence needed for model-as-a-service businesses | Licence file not read | confirmed (vendor statement) | [S70] |
| Meta Llama | Per-generation community licences, gated download; newest family on the organisation page is Llama 4 | Terms from search summaries | secondary only | [S71] |

Other open-weight names from the earlier scan (Kimi, GLM, MiniMax, Muse Spark Open) and funder exclusions of models by country of origin were not verified and are not listed [S72].

## 5. Known incidents (read 2026-11-04)

| Incident | What was confirmed | Tag |
|---|---|---|
| ClawHub malicious skills | Koi Security audit reported 2 Feb 2026: 341 malicious skills among 2,857, 335 of them using fake prerequisites to install Atomic Stealer on macOS | [S73] |
| Skill scan by Snyk | 5 Feb 2026: 3,984 skills scanned, 76 confirmed malicious by human review, 91 percent of those using prompt injection | [S74] |
| MCP STDIO command injection | OX Security advisory, 15 Apr 2026: four families from one pattern of passing user-supplied commands to a subprocess; 14 CVE-tagged products listed plus three without CVEs; OX places the root cause in Anthropic's MCP SDK, and several vendors including Anthropic called it expected behaviour | [S75] |
| Other reported incidents | Context7 CVE, Red Hat Ansible Lightspeed CVE, Miasma worm and Cline npm compromise were not verified | [S76] |

Lesson that survives the detail: install-time trust is the practical hole. Allow-list skills and MCP servers, pin versions, and treat any STDIO server configuration as code execution.

## 6. Social-sector sources (read 2026-11-04)

| Source | What it offers | Confidence | Tag |
|---|---|---|---|
| Candid, responsible AI use policy guide (29 Jan 2026) | Plain-language policy outline: purpose and scope, values, data handling norms, when not to use AI, with examples such as eligibility decisions and client case notes | confirmed | [S77] |
| NTEN AI resource hub | Policy templates, vendor questions, equitable AI planning worksheet, and the NTEN and Bridgespan adoption and governance survey (917 respondents, summer 2026) | confirmed | [S78] |
| Fast Forward, 2026 AI for Humanity Report | 119 AI-powered nonprofits in 20 countries, with leader interviews; headline resourcing percentages from the earlier scan were not on the page | confirmed | [S79] |
| Project Evident, OutcomesAI | Technical assistance and tools, survey with Stanford HAI, grantmaker framework, aligned to the EDSAFE SAFE Benchmarks Framework | confirmed | [S80] |
| FERPA | Commentary says the school official exception is the usual route for vendors and that a consumer chatbot account does not meet it. The Department's student privacy home page shows no AI guidance | secondary only | [S81] |
| HIPAA | Agents handling health information need a business associate agreement. HHS pages returned HTTP 403 | unverified | [S82] |
| Consent for vulnerable populations, small-organisation cost data | No usable source found | unverified | [S83] |

## 7. Not covered in this edition

These were outside the breadth cap or could not be verified. They appear under Planned in the README.

- Runtimes: CrewAI, Temporal, Hermes Agent, Semantic Kernel (superseded by Microsoft Agent Framework per its repository), vLLM, Ollama and llama.cpp.
- Tools: DeepEval, Braintrust, LangSmith, Arize Phoenix, Open Policy Agent, agent benchmarks.
- Standards: MITRE ATLAS individual agent techniques, CSA MAESTRO, CSA autonomy levels, NIST SP 800-53 agent overlays, the remaining seven OWASP agentic entries by name.
- Platforms: Google and Microsoft data residency terms, Auth0 agent features, Microsoft Agent 365 pricing.
- Law: US federal preemption developments, Colorado litigation status, HIPAA Security Rule rulemaking, FERPA guidance for AI, state recording-consent rules.
- Models: Kimi, GLM, MiniMax and other open-weight families, per-token prices, funder rules on model origin.
- Social sector: consent standards for children, immigrants and survivors of violence, Stanford PACS work, foundation guidance, small-organisation cost data.

## 8. Things easy to miss

| # | Item | Source tag |
|---|---|---|
| 1 | Three vendors retire models or hosted tools within weeks of the workshop: Claude Sonnet 4.5 and OpenAI Agent Builder on 30 Nov 2026, Gemini 2.5 on 1 Dec 2026, GPT-5 snapshots on 11 Dec 2026 | [S58] [S60] [S61] |
| 2 | Anthropic API version 2026-10-21 returns an error if temperature, top_p or top_k is sent, so old code breaks on upgrade | [S59] |
| 3 | The MCP spec says STDIO servers should not use its authorization flow, and the OX advisory shows STDIO configuration is a code execution path that some vendors call expected behaviour | [S26] [S75] |
| 4 | MCP is now stateless and HTTP+SSE is deprecated, so a server built last year may need migration within a year | [S27] |
| 5 | Public skill registries carry real malware: 341 of 2,857 ClawHub skills in one audit | [S73] |
| 6 | Several open-weight licences (Qwen community licence, Mistral) need a commercial licence if you run a hosted assistant for others, even though internal use is free | [S68] [S70] |
| 7 | Data residency is opt-in and priced: Anthropic defaults to global routing and charges 1.1 times for US-only; OpenAI needs a sales contact and in-region inference exists only in the US and Europe | [S62] [S63] |
| 8 | AIUC-1 changes every quarter (next on 15 Jan 2027) and its own release page and changelog disagree on counts and one control number | [S03] [S04] |
| 9 | Tool independence: promptfoo is now part of OpenAI and Langfuse part of ClickHouse, so check who owns the tool that grades your agent | [S53] [S54] |
| 10 | Colorado's replacement law has developer duties from 1 Jan 2027 and attorney general rules due by the same date, so the 2026 text is not the last word | [S20] |

Two supporting points sit outside the ten. Model-based assessors are a sampling and triage aid, not a gate: a 2026 study of judge models found verdicts shift with prompt artifacts enough to change rankings [S84], and a survey of agent judging concludes it complements but does not replace human oversight [S85]. The earlier claims that persuasive nonsense fools judges and that a RAND study found no judge reliable were not found. Liability insurers are reported to be adding AI exclusions, so ask the broker before launch; this is unverified [S86].
