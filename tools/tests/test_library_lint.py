from pathlib import Path

import library_lint as ll

EM = chr(0x2014)
EN = chr(0x2013)

HEADER = (
    "# Title\n\n"
    "**Document Owner:** Owner\n"
    "**Classification:** Internal\n"
    "**Version:** 1.0 | **Last Updated:** 2026-11\n"
    "**Review Cycle:** Annual\n\n"
)


def write(root: Path, rel: str, text: str = "x\n") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def messages(findings):
    return [f.render() for f in findings]


def test_clean_tree_has_no_findings(tmp_path):
    write(tmp_path, "README.md", "Index: `Domain/DOM_README.md` `Domain/01_Doc.md`\n")
    write(tmp_path, "Domain/DOM_README.md", "Docs: 01_Doc.md\n")
    write(tmp_path, "Domain/01_Doc.md", "see `DOM_README.md`\n")
    assert ll.run(tmp_path) == []


def test_unindexed_root_file_is_reported(tmp_path):
    write(tmp_path, "README.md", "Nothing here\n")
    write(tmp_path, "GUIDE.md")
    out = messages(ll.check_index(tmp_path))
    assert len(out) == 1 and "GUIDE.md" in out[0]


def test_unindexed_domain_file_is_reported(tmp_path):
    write(tmp_path, "README.md", "Domain/DOM_README.md\n")
    write(tmp_path, "Domain/DOM_README.md", "only this\n")
    write(tmp_path, "Domain/02_Missing.md")
    out = messages(ll.check_index(tmp_path))
    assert len(out) == 1 and "02_Missing.md" in out[0]


def test_subfolder_file_must_be_named_in_domain_readme(tmp_path):
    write(tmp_path, "README.md", "Pillar/PILLAR_README.md\n")
    write(tmp_path, "Pillar/PILLAR_README.md", "lists SOUL.template.md only\n")
    write(tmp_path, "Pillar/templates/SOUL.template.md")
    write(tmp_path, "Pillar/templates/other.md")
    out = messages(ll.check_index(tmp_path))
    assert len(out) == 1 and "other.md" in out[0]


def test_docs_and_tools_are_excluded_from_index(tmp_path):
    write(tmp_path, "README.md", "x\n")
    write(tmp_path, "docs/plans/plan.md")
    write(tmp_path, "tools/tests/fixtures/f.md")
    assert ll.check_index(tmp_path) == []


def test_missing_backtick_reference_is_reported_with_line(tmp_path):
    write(tmp_path, "README.md", "ok\n\nsee `nowhere.md` here\n")
    out = messages(ll.check_references(tmp_path))
    assert len(out) == 1
    assert "README.md:3" in out[0] and "nowhere.md" in out[0]


def test_bare_basename_in_another_folder_is_accepted(tmp_path):
    write(tmp_path, "README.md", "see `01_Doc.md`\n")
    write(tmp_path, "Domain/01_Doc.md")
    assert ll.check_references(tmp_path) == []


def test_ambiguous_bare_basename_is_reported(tmp_path):
    write(tmp_path, "README.md", "see `01_Doc.md`\n")
    write(tmp_path, "A/01_Doc.md")
    write(tmp_path, "B/01_Doc.md")
    out = messages(ll.check_references(tmp_path))
    assert len(out) == 1 and "ambiguous" in out[0].lower()


def test_reference_relative_to_own_folder_resolves(tmp_path):
    write(tmp_path, "README.md", "x\n")
    write(tmp_path, "A/one.md", "see `sub/two.md`\n")
    write(tmp_path, "A/sub/two.md")
    write(tmp_path, "B/sub/two.md")
    assert ll.check_references(tmp_path) == []


def test_wildcard_and_placeholder_references_are_skipped(tmp_path):
    write(tmp_path, "README.md", "`runbooks/ai_*_playbook.md` and `<name>.md`\n")
    assert ll.check_references(tmp_path) == []


def test_folder_with_space_or_ampersand_is_reported(tmp_path):
    (tmp_path / "KPIs & Benchmarking").mkdir()
    (tmp_path / "Vendor Risk").mkdir()
    (tmp_path / "Good_Folder").mkdir()
    out = messages(ll.check_folder_names(tmp_path))
    assert len(out) == 2


def test_prose_rules_flag_dashes_and_banned_words_in_pillar(tmp_path):
    body = f"one {EM} two\nthree {EN} four\nWe leverage it.\nA robust plan.\n"
    write(tmp_path, "Agentic_AI_Standards/01_Doc.md", body)
    out = messages(ll.check_prose(tmp_path))
    assert len(out) == 4
    assert any(":1" in m for m in out) and any("leverage" in m for m in out)


def test_prose_rules_ignore_legacy_tools_and_docs(tmp_path):
    body = f"a {EM} b leverage\n"
    write(tmp_path, "Legacy/01.md", body)
    write(tmp_path, "tools/note.md", body)
    write(tmp_path, "docs/plans/p.md", body)
    assert ll.check_prose(tmp_path) == []


def test_prose_rules_cover_refresh_ledger(tmp_path):
    write(tmp_path, "REFRESH_LEDGER.md", f"x {EM} y\n")
    assert len(ll.check_prose(tmp_path)) == 1


def test_prose_allow_marker_skips_line(tmp_path):
    write(tmp_path, "Agentic_AI_Standards/01_Doc.md", f"quote {EM} here lint:allow\n")
    assert ll.check_prose(tmp_path) == []


def test_missing_version_header_is_reported_for_numbered_doc(tmp_path):
    text = HEADER.replace("**Version:** 1.0 | ", "")
    write(tmp_path, "Agentic_AI_Standards/01_Doc.md", text)
    out = messages(ll.check_headers(tmp_path))
    assert len(out) == 1 and "Version" in out[0]


def test_template_files_do_not_need_headers(tmp_path):
    write(tmp_path, "Agentic_AI_Standards/templates/SOUL.template.md", "no header\n")
    assert ll.check_headers(tmp_path) == []


def test_complete_header_passes(tmp_path):
    write(tmp_path, "Agentic_AI_Standards/01_Doc.md", HEADER)
    assert ll.check_headers(tmp_path) == []


def test_main_exit_codes(tmp_path, capsys):
    write(tmp_path, "README.md", "ok\n")
    assert ll.main(["--root", str(tmp_path)]) == 0
    write(tmp_path, "STRAY.md")
    assert ll.main(["--root", str(tmp_path)]) == 1
    assert "STRAY.md" in capsys.readouterr().out
