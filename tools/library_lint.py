"""Library hygiene lint.

Checks index drift, backticked cross-references, folder names, prose rules for
newly authored files, and header fields for the agentic pillar documents.

Usage: python tools/library_lint.py [--root PATH]
Exit code 0 when clean, 1 when any finding is reported.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import (
    BANNED_WORD_PATTERN,
    EM_DASH,
    EN_DASH,
    PROSE_ALLOW_MARKER,
    PROSE_SCOPE_DIRS,
    PROSE_SCOPE_FILES,
    Finding,
    iter_markdown,
    read_text,
    rel_posix,
)

BACKTICK_MD = re.compile(r"`([^`\n]+?\.md)`")
SKIP_REF_CHARS = ("*", "<", ">", "{", "}", "http://", "https://", "$")

HEADER_FIELDS = (
    ("Document Owner", ("Document Owner", "Domain Owner")),
    ("Classification", ("Classification",)),
    ("Version", ("Version",)),
    ("Last Updated", ("Last Updated",)),
    ("Review Cycle", ("Review Cycle",)),
)
HEADER_SCOPE_PATTERN = re.compile(
    r"^Agentic_AI_Standards/(0[1-6]_[^/]+\.md|AGENTIC_README\.md|AGENT_INCIDENT_RESPONSE_ADDENDUM\.md)$"
)


def _top_level(rel: Path) -> str | None:
    return rel.parts[0] if len(rel.parts) > 1 else None


def check_index(root: Path) -> list[Finding]:
    """Every root file and domain file must be named in a README.

    Root files are named in README.md. Files directly in a domain folder are
    named in README.md or that folder's README. Files in subfolders of a domain
    are named in that folder's README.
    """
    findings: list[Finding] = []
    root_readme = root / "README.md"
    root_text = read_text(root_readme) if root_readme.exists() else ""
    for path in iter_markdown(root):
        rel = path.relative_to(root)
        if rel.as_posix() == "README.md":
            continue
        top = _top_level(rel)
        if top is None:
            if path.name not in root_text:
                findings.append(
                    Finding("index", rel.as_posix(), None, "not named in README.md")
                )
            continue
        domain_dir = root / top
        readmes = [p for p in domain_dir.glob("*README.md")]
        if path in readmes:
            if path.name not in root_text and rel.as_posix() not in root_text:
                findings.append(
                    Finding("index", rel.as_posix(), None, "domain README not named in README.md")
                )
            continue
        text = "".join(read_text(p) for p in readmes)
        if len(rel.parts) == 2:
            text += root_text
        if path.name not in text:
            findings.append(
                Finding("index", rel.as_posix(), None, "not named in its README index")
            )
    return findings


def _build_basename_index(root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in root.rglob("*.md"):
        if ".git" in path.relative_to(root).parts:
            continue
        index.setdefault(path.name, []).append(path)
    return index


def check_references(root: Path) -> list[Finding]:
    """Backticked *.md references must resolve to a real file.

    A reference passes when it resolves from the repo root, from the file's own
    folder, or by a unique basename match. It fails when the basename is
    missing or ambiguous.
    """
    findings: list[Finding] = []
    basenames = _build_basename_index(root)
    for path in iter_markdown(root):
        rel = rel_posix(root, path)
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            for match in BACKTICK_MD.finditer(line):
                ref = match.group(1).strip()
                if any(token in ref for token in SKIP_REF_CHARS) or " " in ref:
                    continue
                if (root / ref).is_file() or (path.parent / ref).is_file():
                    continue
                matches = basenames.get(Path(ref).name, [])
                if not matches:
                    message = f"`{ref}` does not exist"
                elif "/" in ref:
                    if any(m.relative_to(root).as_posix().endswith(ref) for m in matches):
                        continue
                    message = f"`{ref}` is in a different folder"
                elif len(matches) == 1:
                    continue
                else:
                    message = f"`{ref}` is ambiguous ({len(matches)} files)"
                findings.append(Finding("reference", rel, number, message))
    return findings


def check_folder_names(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_dir() or rel.parts[0] in {".git", "__pycache__", ".pytest_cache"}:
            continue
        if " " in path.name or "&" in path.name:
            findings.append(
                Finding("folder-name", rel.as_posix(), None, "folder name has a space or ampersand")
            )
    return findings


def _prose_files(root: Path):
    for name in PROSE_SCOPE_FILES:
        path = root / name
        if path.is_file():
            yield path
    for folder in PROSE_SCOPE_DIRS:
        base = root / folder
        if base.is_dir():
            yield from sorted(base.rglob("*.md"))


def check_prose(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _prose_files(root):
        rel = rel_posix(root, path)
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if PROSE_ALLOW_MARKER in line:
                continue
            if EM_DASH in line:
                findings.append(Finding("prose", rel, number, "em dash"))
            if EN_DASH in line:
                findings.append(Finding("prose", rel, number, "en dash"))
            for hit in BANNED_WORD_PATTERN.finditer(line):
                findings.append(
                    Finding("prose", rel, number, f"banned word '{hit.group(0).lower()}'")
                )
    return findings


def check_headers(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_markdown(root, include_excluded=False):
        rel = rel_posix(root, path)
        if not HEADER_SCOPE_PATTERN.match(rel):
            continue
        head = "\n".join(read_text(path).splitlines()[:25])
        for label, accepted in HEADER_FIELDS:
            if not any(f"**{name}:**" in head for name in accepted):
                findings.append(
                    Finding("header", rel, None, f"missing header field '{label}'")
                )
    return findings


CHECKS = (check_index, check_references, check_folder_names, check_prose, check_headers)


def run(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for check in CHECKS:
        findings.extend(check(root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    findings = run(root)
    for finding in findings:
        print(finding.render())
    if findings:
        print(f"\n{len(findings)} finding(s).")
        return 1
    print("library_lint: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
