import re
import shutil
from datetime import date
from pathlib import Path

import pytest
import yaml

import agent_lint as al

REPO = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures" / "agents"
TEMPLATES = REPO / "Agentic_AI_Standards" / "templates"
TODAY = date(2026, 11, 4)


@pytest.fixture
def valid(tmp_path):
    dest = tmp_path / "valid"
    shutil.copytree(FIXTURES / "valid", dest)
    return dest


def lint(path, today=TODAY):
    return al.run(Path(path), today)


def msgs(findings):
    return [f.render() for f in findings]


def edit(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {path}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_valid_fixture_has_no_findings():
    assert msgs(lint(FIXTURES / "valid")) == []


def test_missing_section_names_the_section(valid):
    edit(valid / "SOUL.md", "## Forbidden Actions", "## Something Else")
    out = msgs(lint(valid))
    assert len(out) == 1 and "Forbidden Actions" in out[0]


def test_missing_frontmatter_field_is_reported(valid):
    edit(valid / "SOUL.md", "backup_owner: Development Coordinator\n", "")
    out = msgs(lint(valid))
    assert len(out) == 1 and "backup_owner" in out[0]


def test_invalid_tier_is_reported(valid):
    edit(valid / "SOUL.md", "tier: T3", "tier: T9")
    assert any("tier" in m for m in msgs(lint(valid)))


def test_broken_fixture_gives_mirror_error_naming_tool():
    out = msgs(lint(FIXTURES / "broken"))
    assert len(out) == 1
    assert "mirror" in out[0] and "send_email" in out[0]


def test_registry_only_write_tool_is_a_mirror_error(valid):
    row = valid / "registry_row.yaml"
    edit(row, "  - {name: create_draft",
         '  - {name: post_social, scope: "social:post", access: write}\n  - {name: create_draft')
    out = msgs(lint(valid))
    assert any("mirror" in m and "post_social" in m for m in out)


def test_data_class_and_gate_drift_are_mirror_errors(valid):
    edit(valid / "registry_row.yaml", "[donor_contact, gift_history]", "[donor_contact]")
    edit(valid / "registry_row.yaml", "[staff_review_before_send]", "[other_gate]")
    out = msgs(lint(valid))
    assert any("mirror" in m and "gift_history" in m for m in out)
    assert any("mirror" in m and "staff_review_before_send" in m for m in out)


def test_t2_without_assessor_is_an_error(valid):
    edit(valid / "SOUL.md", "tier: T3", "tier: T2")
    edit(valid / "SOUL.md", "assessor: assessor-conformance-001", "assessor: null")
    out = msgs(lint(valid))
    assert any("T2" in m and "assessor" in m for m in out)


def test_t2_without_approval_gate_is_an_error(valid):
    edit(valid / "SOUL.md", "tier: T3", "tier: T2")
    edit(valid / "SOUL.md", "approval_gates: [staff_review_before_send]", "approval_gates: []")
    edit(valid / "registry_row.yaml", "[staff_review_before_send]", "[]")
    assert any("approval gate" in m for m in msgs(lint(valid)))


def test_t3_needs_assessor_or_second_reviewer(valid):
    edit(valid / "SOUL.md", "assessor: assessor-conformance-001", "assessor: null")
    assert any("T3" in m for m in msgs(lint(valid)))
    edit(valid / "SOUL.md", "second_reviewer: null", "second_reviewer: Board Treasurer")
    assert msgs(lint(valid)) == []


def test_t4_may_omit_assessor_and_gates(valid):
    edit(valid / "SOUL.md", "tier: T3", "tier: T4")
    edit(valid / "registry_row.yaml", "tier: T3", "tier: T4")
    edit(valid / "SOUL.md", "assessor: assessor-conformance-001", "assessor: null")
    edit(valid / "SOUL.md", "approval_gates: [staff_review_before_send]", "approval_gates: []")
    edit(valid / "registry_row.yaml", "[staff_review_before_send]", "[]")
    assert msgs(lint(valid)) == []


def test_review_date_in_the_past_is_an_error(valid):
    out = msgs(lint(valid, today=date(2027, 3, 2)))
    assert len(out) == 1 and "review_date" in out[0]


def test_review_date_equal_to_today_passes(valid):
    assert msgs(lint(valid, today=date(2027, 3, 1))) == []


def test_missing_sunset_date_is_an_error(valid):
    edit(valid / "SOUL.md", "sunset_date: 2027-11-01\n", "")
    out = msgs(lint(valid))
    assert len(out) == 1 and "sunset_date" in out[0]


def test_secret_is_reported_without_echoing_it(valid):
    secret = "sk-" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    edit(valid / "SOUL.md", "Warm, plain, short.", f"Warm, plain, short. key {secret}")
    out = msgs(lint(valid))
    assert len(out) == 1 and "secret" in out[0].lower()
    assert secret not in out[0] and secret[:12] not in out[0]


def test_assessor_on_same_family_is_an_error(valid):
    edit(valid / "assessor" / "registry_row.yaml", "family_b", "family_a")
    out = msgs(lint(valid))
    assert out and all("family" in m for m in out)


def test_write_tool_without_gate_on_t3_is_an_error(valid):
    edit(valid / "SOUL.md", "approval_gates: [staff_review_before_send]", "approval_gates: []")
    edit(valid / "registry_row.yaml", "[staff_review_before_send]", "[]")
    out = msgs(lint(valid))
    assert any("create_draft" in m and "approval gate" in m for m in out)


def test_assessor_charter_requires_extra_sections(valid):
    edit(valid / "assessor" / "SOUL.md", "## Sampling Rule", "## Sampling")
    out = msgs(lint(valid))
    assert len(out) == 1 and "Sampling Rule" in out[0]


def test_missing_registry_row_is_an_error(valid):
    (valid / "registry_row.yaml").unlink()
    out = msgs(lint(valid))
    assert any("registry" in m for m in out)


def test_registry_yaml_keyed_by_agent_id_is_supported(tmp_path):
    folder = tmp_path / "multi"
    folder.mkdir()
    shutil.copy(FIXTURES / "broken" / "SOUL.md", folder / "a.charter.md")
    row = (FIXTURES / "broken" / "registry_row.yaml").read_text(encoding="utf-8")
    indented = "".join("    " + line + "\n" for line in row.splitlines())
    (folder / "registry.yaml").write_text(
        "agents:\n  donor-ack-002:\n" + indented, encoding="utf-8"
    )
    out = msgs(lint(folder))
    assert len(out) == 1 and "send_email" in out[0]


def test_discovery_ignores_other_markdown(valid):
    (valid / "NOTES.md").write_text("no frontmatter here\n", encoding="utf-8")
    (valid / "SOUL.template.md").write_text("junk\n", encoding="utf-8")
    assert msgs(lint(valid)) == []


def test_tier_differing_between_charter_and_row_is_a_mirror_error(valid):
    edit(valid / "registry_row.yaml", "tier: T3", "tier: T2")
    out = msgs(lint(valid))
    assert len(out) == 1 and "mirror" in out[0] and "tier" in out[0]


def test_enforcement_ref_without_a_row_key_is_an_error(valid):
    edit(valid / "SOUL.md", "[idp_scope_mail_drafts_only, runtime_budget_alert]",
         "[idp_scope_mail_drafts_only, runtime_budget_alert, no_such_control]")
    out = msgs(lint(valid))
    assert len(out) == 1 and "no_such_control" in out[0]


def test_extra_row_enforcement_key_is_allowed(valid):
    edit(valid / "registry_row.yaml", "enforcement:\n",
         "enforcement:\n  extra_control: something else\n")
    assert msgs(lint(valid)) == []


def test_model_must_be_a_mapping_with_four_fields(valid):
    row = valid / "registry_row.yaml"
    text = row.read_text(encoding="utf-8")
    start, end = text.index("model:"), text.index("enforcement:")
    row.write_text(text[:start] + "model: model-a-large\n" + text[end:], encoding="utf-8")
    out = msgs(lint(valid))
    assert any("registry" in m and "model" in m and "mapping" in m for m in out)


def test_model_missing_a_field_is_an_error(valid):
    edit(valid / "registry_row.yaml", "  family: family_a\n", "")
    out = msgs(lint(valid))
    assert any("model" in m and "family" in m for m in out)


def test_registry_status_must_be_a_known_value(valid):
    edit(valid / "registry_row.yaml", "status: active", "status: live")
    out = msgs(lint(valid))
    assert len(out) == 1 and "status" in out[0] and "live" in out[0]


@pytest.mark.parametrize("status", ["proposed", "active", "suspended", "retired"])
def test_registry_status_known_values_pass(valid, status):
    edit(valid / "registry_row.yaml", "status: active", f"status: {status}")
    assert msgs(lint(valid)) == []


def test_secret_in_registry_row_is_reported_without_echoing_it(valid):
    secret = "sk-" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    edit(valid / "registry_row.yaml", "budget alert at 80 percent", f"budget alert {secret}")
    out = msgs(lint(valid))
    assert len(out) == 1 and "secret" in out[0].lower() and "registry" in out[0].lower()
    assert secret not in out[0] and secret[:12] not in out[0]


def test_sunset_date_in_the_past_is_an_error(valid):
    out = msgs(lint(valid, today=date(2027, 11, 2)))
    assert any("sunset_date" in m for m in out)


def test_sunset_date_equal_to_today_passes(valid):
    out = msgs(lint(valid, today=date(2027, 11, 1)))
    assert not any("sunset_date" in m for m in out)


def test_placeholder_left_in_charter_is_an_error(valid):
    edit(valid / "SOUL.md", "Warm, plain, short.", "Warm, plain, {{tone}}.")
    out = msgs(lint(valid))
    assert len(out) == 1 and "placeholder" in out[0] and "{{tone}}" in out[0]


def test_placeholder_left_in_registry_row_is_an_error(valid):
    edit(valid / "registry_row.yaml", "budget alert at 80 percent", "budget alert at {{pct}} percent")
    out = msgs(lint(valid))
    assert len(out) == 1 and "placeholder" in out[0] and "registry" in out[0].lower()


@pytest.mark.parametrize("value", ["Program Operations Lead", "  program operations LEAD "])
def test_second_reviewer_equal_to_owner_is_an_error(valid, value):
    edit(valid / "SOUL.md", "second_reviewer: null", f"second_reviewer: {value}")
    out = msgs(lint(valid))
    assert len(out) == 1 and "second_reviewer" in out[0] and "owner" in out[0]


def test_t4_second_reviewer_may_equal_owner(valid):
    edit(valid / "SOUL.md", "tier: T3", "tier: T4")
    edit(valid / "registry_row.yaml", "tier: T3", "tier: T4")
    edit(valid / "SOUL.md", "second_reviewer: null", "second_reviewer: Program Operations Lead")
    assert msgs(lint(valid)) == []


# Template lint: fill placeholders and confirm the templates themselves are clean.


def fill(text, values=None):
    values = values or {}
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), "sample"), text)


def test_soul_template_lints_clean_when_filled(tmp_path):
    values = {
        "tier": "T3",
        "assessor_agent_id": "assessor-conformance-001",
        "review_date": "2027-03-01",
        "sunset_date": "2027-11-01",
        "agent_id": "tmpl-001",
    }
    folder = tmp_path / "worker"
    folder.mkdir()
    text = fill((TEMPLATES / "SOUL.template.md").read_text(encoding="utf-8"), values)
    (folder / "SOUL.md").write_text(text, encoding="utf-8")
    fm = al.parse_frontmatter(text)[0]
    assert [t for t in fm["tools"] if t["access"] == "write"], "template shows a write tool"
    row = {
        "agent_id": "tmpl-001",
        "tier": "T3",
        "tools": fm["tools"],
        "data_classes": fm["data_classes"],
        "approval_gates": fm["approval_gates"],
        "spend_cap_usd_month": 10,
        "model": {"provider": "p", "id": "m", "pinned_version": "v1", "family": "family_a"},
        "enforcement": {ref: "control" for ref in fm["enforcement_refs"]},
        "status": "active",
        "last_assessed": "2026-10-01",
    }
    (folder / "registry_row.yaml").write_text(yaml.safe_dump(row), encoding="utf-8")
    shutil.copytree(FIXTURES / "valid" / "assessor", tmp_path / "assessor")
    edit(tmp_path / "assessor" / "SOUL.md", "target: donor-ack-001", "target: tmpl-001")
    out = msgs(lint(tmp_path))
    assert out == [], out


@pytest.mark.parametrize("name", ["charter_conformance_assessor.md", "boundary_assessor.md"])
def test_assessor_templates_lint_clean_when_filled(tmp_path, name):
    values = {
        "agent_id": "assessor-x-001",
        "target_agent_id": "donor-ack-001",
        "review_date": "2027-03-01",
        "sunset_date": "2027-11-01",
        "tier": "T3",
        "owner": "Owner Role",
        "second_reviewer": "Reviewer Role",
    }
    folder = tmp_path / "valid"
    shutil.copytree(FIXTURES / "valid", folder)
    a = folder / "assessor"
    text = fill((TEMPLATES / "assessors" / name).read_text(encoding="utf-8"), values)
    (a / "SOUL.md").write_text(text, encoding="utf-8")
    fm = al.parse_frontmatter(text)[0]
    row = yaml.safe_load((a / "registry_row.yaml").read_text(encoding="utf-8"))
    row.update(
        agent_id="assessor-x-001",
        tools=fm["tools"],
        data_classes=fm["data_classes"],
        approval_gates=fm["approval_gates"],
        tier=fm["tier"],
        enforcement={ref: "control" for ref in fm["enforcement_refs"]},
    )
    (a / "registry_row.yaml").write_text(yaml.safe_dump(row), encoding="utf-8")
    edit(folder / "SOUL.md", "assessor-conformance-001", "assessor-x-001")
    out = msgs(lint(folder))
    assert out == [], out


def test_explicit_template_path_is_linted_and_reports_placeholders():
    out = msgs(lint(TEMPLATES / "assessors" / "boundary_assessor.md"))
    assert out  # unfilled placeholders are not valid values


# CLI


def test_cli_exit_codes(capsys):
    assert al.main([str(FIXTURES / "valid"), "--today", "2026-11-04"]) == 0
    assert al.main([str(FIXTURES / "broken"), "--today", "2026-11-04"]) == 1
    printed = capsys.readouterr().out
    assert "send_email" in printed
    assert al.main([str(FIXTURES / "nope")]) == 2


def test_cli_bad_date_is_usage_error():
    assert al.main([str(FIXTURES / "valid"), "--today", "11/04/2026"]) == 2
