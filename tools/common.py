"""Shared helpers for the library and agent linters."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Folders that never take part in index or reference checks.
EXCLUDED_TOP_LEVEL = {".git", ".github", ".pytest_cache", "docs", "tools", "__pycache__"}

# Prose rules apply to new text only: the agentic pillar and the refresh ledger.
PROSE_SCOPE_DIRS = ("Agentic_AI_Standards",)
PROSE_SCOPE_FILES = ("REFRESH_LEDGER.md",)

PROSE_ALLOW_MARKER = "lint:allow"


@dataclass(frozen=True)
class Finding:
    check: str
    path: str
    line: int | None
    message: str

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"[{self.check}] {where} {self.message}"


def iter_markdown(root: Path, include_excluded: bool = False):
    """Yield every Markdown file under root, skipping excluded top-level folders."""
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        top = rel.parts[0]
        if not include_excluded and len(rel.parts) > 1 and top in EXCLUDED_TOP_LEVEL:
            continue
        if any(part.startswith(".") and part not in (".",) for part in rel.parts[:-1]):
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel_posix(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


# Dash characters are built from code points so this file stays dash-free.
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)

BANNED_WORD_PATTERN = re.compile(
    r"\b("
    r"delv(?:e|es|ed|ing)|"
    r"leverag(?:e|es|ed|ing)|"
    r"foster(?:s|ed|ing)?|"
    r"cultivat(?:e|es|ed|ing)|"
    r"unleash(?:es|ed|ing)?|"
    r"navigat(?:e|es|ed|ing)|"
    r"bolster(?:s|ed|ing)?|"
    r"propel(?:s|led|ling)?|"
    r"harness(?:es|ed|ing)?|"
    r"underscor(?:e|es|ed|ing)|"
    r"showcas(?:e|es|ed|ing)|"
    r"embrac(?:e|es|ed|ing)|"
    r"robust(?:ly|ness)?|"
    r"nuanced|"
    r"intricate(?:ly)?|"
    r"multifaceted|"
    r"comprehensive(?:ly)?|"
    r"unparalleled|"
    r"cutting-edge|"
    r"transformative"
    r")\b",
    re.IGNORECASE,
)
