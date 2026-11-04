# Agentic AI Standards
## Domain README: Document Index and Navigation Guide

**Domain Owner:** Data Program Management Lead
**Platform:** Agent runtimes, identity providers, and model providers (vendor neutral)
**Version:** 1.0 | **Last Updated:** 2026-11
**Classification:** Internal, Program Reference
**Review Cycle:** Annual, plus a dated landscape check before each workshop

> **Purpose:** This domain defines how an organization stands up a governed agent: one identity per agent, a written charter that states its bounds and names the control that enforces each one, a registry row, and a review step that is independent of the builder. It reuses the risk tiers and boundary contracts from the AI-First Strategy Addendum.

---

## Document Index

| Document | Version | Status | Description |
|---|---|---|---|
| `SOUL.template.md` | 1.0 | Active | Charter template: frontmatter fields and the eleven required sections |
| `registry.schema.yaml` | 1.0 | Active | Schema and commented example for one registry row |
| `charter_conformance_assessor.md` | 1.0 | Active | Assessor charter that checks sampled work against the target's own charter |
| `boundary_assessor.md` | 1.0 | Active | Assessor charter that checks sampled work against the three boundary contracts |

Templates live in `templates/` and assessor charters in `templates/assessors/`. The agent linter, `tools/agent_lint.py`, checks a charter against its registry row.
