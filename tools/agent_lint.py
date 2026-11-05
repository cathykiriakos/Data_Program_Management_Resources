"""Agent charter lint.

Checks agent charters (SOUL.md or *.charter.md) against their registry rows.
A charter is a prompt, not an enforcement layer; this linter makes the bounds a
charter states testable by comparing them with the registry row and by applying
the tier rules from the AI-First Strategy Addendum.

Discovery: a directory is scanned for files named SOUL.md or *.charter.md and
every other file is ignored. A file passed explicitly is always linted. A
charter's row is registry_row.yaml in the same folder, or an entry keyed by
agent_id in registry.yaml in that folder.

Usage: python tools/agent_lint.py PATH [--today YYYY-MM-DD]
Exit code 0 when clean, 1 when any finding is reported, 2 on usage errors.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

from common import Finding, read_text, rel_posix, report

TIERS = ("T1", "T2", "T3", "T4")

REQUIRED_FIELDS = (
    "agent_id",
    "tier",
    "owner",
    "backup_owner",
    "purpose",
    "model_ref",
    "runtime",
    "identity",
    "data_classes",
    "tools",
    "review_date",
    "sunset_date",
    "enforcement_refs",
)
# Keys that must exist in the frontmatter but may be empty.
PRESENT_FIELDS = ("approval_gates", "assessor")

REQUIRED_SECTIONS = (
    "Purpose",
    "Authority",
    "Forbidden Actions",
    "Data Handling",
    "Tools and Scopes",
    "Approval and Escalation",
    "Memory Rules",
    "Voice",
    "Failure Behavior",
    "Assessor and Review",
    "Decommissioning",
)
ASSESSOR_SECTIONS = ("Rubric", "Sampling Rule", "Evidence Format", "Limits")

ROW_REQUIRED = ("agent_id", "tier", "tools", "data_classes", "approval_gates", "spend_cap_usd_month",
                "model", "enforcement", "status")
MODEL_ROW_FIELDS = ("provider", "id", "pinned_version", "family")
STATUSES = ("proposed", "active", "suspended", "retired")
PLACEHOLDER = re.compile(r"\{\{[^}\n]*\}\}")

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password|passwd|access[_-]?key)[A-Za-z0-9_]*[\"']?"
        r"\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+=.~]{16,}"
    ),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9_\-.=+/]{20,}"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}"),
)

TOOL_ACCESS_VALUES = ("read", "write")

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Return (frontmatter dict or None, body). Raises yaml.YAMLError on bad YAML."""
    match = FRONTMATTER.match(text)
    if not match:
        return None, text
    data = yaml.safe_load(match.group(1))
    return (data if isinstance(data, dict) else None), text[match.end():]


def _as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _tool_key(tool) -> tuple[str, str]:
    if isinstance(tool, dict):
        return str(tool.get("name", "")), str(tool.get("scope", ""))
    return str(tool), ""


def _write_tools(tools) -> set[tuple[str, str]]:
    return {
        _tool_key(t)
        for t in _as_list(tools)
        if isinstance(t, dict) and str(t.get("access", "")).lower() == "write"
    }


def check_tool_access(tools, label: str) -> list[Finding]:
    """Every tool entry must say read or write, so no tool escapes the write checks by spelling."""
    findings = []
    for tool in _as_list(tools):
        if not isinstance(tool, dict):
            continue
        access = str(tool.get("access", "")).strip().lower()
        if access not in TOOL_ACCESS_VALUES:
            shown = tool.get("access") if tool.get("access") not in (None, "") else "missing"
            findings.append(
                Finding("tool-access", label, None,
                        f"tool '{tool.get('name', '?')}' has access '{shown}'; use read or write")
            )
    return findings


def _redact(text: str) -> str:
    return text[:3] + "..." if len(text) > 3 else "..."


# ---------------------------------------------------------------- registry


def _rows_from_registry_yaml(data) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if isinstance(data, dict) and isinstance(data.get("agents"), (list, dict)):
        data = data["agents"]
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict) and row.get("agent_id"):
                rows[str(row["agent_id"])] = row
    elif isinstance(data, dict):
        for key, row in data.items():
            if isinstance(row, dict):
                rows[str(key)] = row
    return rows


def _load_yaml(path: Path):
    try:
        return yaml.safe_load(read_text(path))
    except yaml.YAMLError:
        return None


def folder_rows(folder: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    single = folder / "registry_row.yaml"
    if single.is_file():
        data = _load_yaml(single)
        if isinstance(data, dict) and data.get("agent_id"):
            rows[str(data["agent_id"])] = data
    multi = folder / "registry.yaml"
    if multi.is_file():
        for key, row in _rows_from_registry_yaml(_load_yaml(multi)).items():
            rows.setdefault(key, row)
    return rows


def build_index(base: Path) -> dict[str, dict]:
    index: dict[str, dict] = {}
    folders = {p.parent for p in base.rglob("registry_row.yaml")}
    folders |= {p.parent for p in base.rglob("registry.yaml")}
    for folder in sorted(folders):
        for key, row in folder_rows(folder).items():
            index.setdefault(key, row)
    return index


# ---------------------------------------------------------------- discovery


def discover(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return [
        p for p in sorted(path.rglob("*"))
        if p.is_file() and (p.name == "SOUL.md" or p.name.endswith(".charter.md"))
    ]


# ---------------------------------------------------------------- checks


def lint_charter(path: Path, label: str, index: dict[str, dict], today: date) -> list[Finding]:
    def F(check: str, message: str, line: int | None = None) -> Finding:
        return Finding(check, label, line, message)

    findings: list[Finding] = []
    text = read_text(path)

    findings += check_secrets(text, label)
    findings += check_placeholders(text, label)

    try:
        fm, body = parse_frontmatter(text)
    except yaml.YAMLError:
        return findings + [F("frontmatter", "frontmatter is not valid YAML")]
    if fm is None:
        return findings + [F("frontmatter", "no YAML frontmatter found")]

    for name in REQUIRED_FIELDS:
        if name not in fm or (_empty(fm[name]) and name != "tools"):
            findings.append(F("frontmatter", f"missing required field '{name}'"))
    for name in PRESENT_FIELDS:
        if name not in fm:
            findings.append(F("frontmatter", f"missing required field '{name}' (may be empty)"))

    headings = {m.group(1).strip() for m in H2.finditer(body)}
    is_assessor = str(fm.get("role", "")).lower() == "assessor"
    needed = REQUIRED_SECTIONS + (ASSESSOR_SECTIONS if is_assessor else ())
    for section in needed:
        if section not in headings:
            findings.append(F("section", f"missing section '{section}'"))
    if is_assessor and _empty(fm.get("target")):
        findings.append(F("frontmatter", "assessor charter is missing 'target' (agent_id)"))

    tier = fm.get("tier")
    if tier not in TIERS:
        findings.append(F("tier", f"tier '{tier}' is not one of T1, T2, T3, T4"))

    findings += check_dates(fm, label, today)

    gates = _as_list(fm.get("approval_gates"))
    tools = _as_list(fm.get("tools"))
    findings += check_tool_access(tools, label)
    findings += check_tier_rules(fm, tier, gates, tools, label)

    row = find_row(fm.get("agent_id"), path.parent, index)
    if row is None:
        findings.append(F("registry", f"no registry row for agent_id '{fm.get('agent_id')}'"))
        return findings
    findings += check_row(row, label)
    findings += check_row_text(row, label)
    findings += check_mirror(fm, row, tools, gates, label)
    findings += check_families(fm, row, is_assessor, path.parent, index, label)
    return findings


def check_secrets(text: str, label: str) -> list[Finding]:
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern in SECRET_PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding("secret", label, number,
                            f"possible secret ({_redact(match.group(0))}) found; remove it")
                )
                break
    return findings


def check_placeholders(text: str, label: str) -> list[Finding]:
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = PLACEHOLDER.search(line)
        if match:
            findings.append(
                Finding("placeholder", label, number,
                        f"placeholder {match.group(0)} was not replaced")
            )
    return findings


def check_row_text(row: dict, label: str) -> list[Finding]:
    """Secret and placeholder scans of the registry row, which has no line numbers here."""
    text = yaml.safe_dump(row, default_flow_style=False, sort_keys=False)
    findings = []
    for f in check_secrets(text, label) + check_placeholders(text, label):
        findings.append(
            Finding(f.check, label, None, f"registry row: {f.message}")
        )
    return findings


def check_dates(fm: dict, label: str, today: date) -> list[Finding]:
    findings = []
    if "review_date" in fm and not _empty(fm["review_date"]):
        review = _as_date(fm["review_date"])
        if review is None:
            findings.append(Finding("date", label, None, "review_date is not a valid YYYY-MM-DD date"))
        elif review < today:
            findings.append(
                Finding("date", label, None,
                        f"review_date {review.isoformat()} is before {today.isoformat()}")
            )
    if "sunset_date" in fm and not _empty(fm["sunset_date"]):
        sunset = _as_date(fm["sunset_date"])
        if sunset is None:
            findings.append(Finding("date", label, None, "sunset_date is not a valid YYYY-MM-DD date"))
        elif sunset < today:
            findings.append(
                Finding("date", label, None,
                        f"sunset_date {sunset.isoformat()} is before {today.isoformat()}; "
                        "renew or retire the agent")
            )
    return findings


def check_tier_rules(fm: dict, tier, gates: list, tools: list, label: str) -> list[Finding]:
    findings = []
    has_assessor = not _empty(fm.get("assessor"))
    if tier in ("T1", "T2"):
        if not has_assessor:
            findings.append(Finding("tier", label, None, f"{tier} requires an assessor agent"))
        if not gates:
            findings.append(Finding("tier", label, None, f"{tier} requires at least one approval gate"))
    elif tier == "T3":
        if not has_assessor and _empty(fm.get("second_reviewer")):
            findings.append(
                Finding("tier", label, None,
                        "T3 requires an assessor agent or a named second_reviewer")
            )
    owner, second = fm.get("owner"), fm.get("second_reviewer")
    if (tier in ("T1", "T2", "T3") and not _empty(owner) and not _empty(second)
            and str(owner).strip().lower() == str(second).strip().lower()):
        findings.append(
            Finding("tier", label, None,
                    f"second_reviewer '{str(second).strip()}' is the same as owner; "
                    "a second reviewer must be a different person or role")
        )
    if tier in ("T1", "T2", "T3") and not gates:
        for name, scope in sorted(_write_tools(tools)):
            findings.append(
                Finding("tier", label, None,
                        f"write tool '{name}' has no approval gate ({tier} charters need one)")
            )
    return findings


def find_row(agent_id, folder: Path, index: dict[str, dict]) -> dict | None:
    if _empty(agent_id):
        return None
    key = str(agent_id)
    return folder_rows(folder).get(key) or index.get(key)


def check_row(row: dict, label: str) -> list[Finding]:
    findings = check_tool_access(row.get("tools"), f"{label} (registry row)")
    for name in ROW_REQUIRED:
        if name not in row or (_empty(row[name]) and name not in ("tools", "data_classes", "approval_gates")):
            findings.append(Finding("registry", label, None, f"registry row missing '{name}'"))
    model = row.get("model")
    if "model" in row and not _empty(model):
        if isinstance(model, dict):
            for name in MODEL_ROW_FIELDS:
                if _empty(model.get(name)):
                    findings.append(Finding("registry", label, None, f"registry row model missing '{name}'"))
        else:
            findings.append(
                Finding("registry", label, None,
                        "registry row model must be a mapping with provider, id, pinned_version, family")
            )
    status = row.get("status")
    if not _empty(status) and str(status).strip().lower() not in STATUSES:
        findings.append(
            Finding("registry", label, None,
                    f"registry row status '{status}' is not one of {', '.join(STATUSES)}")
        )
    return findings


def check_mirror(fm: dict, row: dict, tools: list, gates: list, label: str) -> list[Finding]:
    findings = []
    if (
        not _empty(fm.get("tier"))
        and not _empty(row.get("tier"))
        and str(fm["tier"]).strip() != str(row["tier"]).strip()
    ):
        findings.append(
            Finding("mirror", label, None,
                    f"tier '{fm['tier']}' in the charter differs from '{row['tier']}' in the registry row")
        )
    enforcement = row.get("enforcement")
    keys = {str(k) for k in enforcement} if isinstance(enforcement, dict) else set()
    for ref in _as_list(fm.get("enforcement_refs")):
        if str(ref) not in keys:
            findings.append(
                Finding("mirror", label, None,
                        f"enforcement_refs entry '{ref}' has no matching key in the registry row's enforcement map")
            )
    charter_writes = _write_tools(tools)
    row_writes = _write_tools(row.get("tools"))
    for name, scope in sorted(charter_writes - row_writes):
        findings.append(
            Finding("mirror", label, None,
                    f"write tool '{name}' (scope '{scope}') is in the charter but not in the registry row")
        )
    for name, scope in sorted(row_writes - charter_writes):
        findings.append(
            Finding("mirror", label, None,
                    f"write tool '{name}' (scope '{scope}') is in the registry row but not in the charter")
        )
    for field, a, b in (
        ("data_classes", _as_list(fm.get("data_classes")), _as_list(row.get("data_classes"))),
        ("approval_gates", gates, _as_list(row.get("approval_gates"))),
    ):
        sa, sb = {str(x) for x in a}, {str(x) for x in b}
        for item in sorted(sa - sb):
            findings.append(
                Finding("mirror", label, None,
                        f"{field} entry '{item}' is in the charter but not in the registry row")
            )
        for item in sorted(sb - sa):
            findings.append(
                Finding("mirror", label, None,
                        f"{field} entry '{item}' is in the registry row but not in the charter")
            )
    return findings


def _family(row: dict | None) -> str | None:
    model = (row or {}).get("model")
    if isinstance(model, dict) and not _empty(model.get("family")):
        return str(model["family"])
    return None


def check_families(fm: dict, row: dict, is_assessor: bool, folder: Path,
                   index: dict[str, dict], label: str) -> list[Finding]:
    """An assessor's model family must differ from its target's family."""
    findings: list[Finding] = []
    if is_assessor:
        target_id, assessor_row, target_row = fm.get("target"), row, None
        if not _empty(target_id):
            target_row = find_row(target_id, folder, index)
        subject = f"target '{target_id}'"
    else:
        assessor_id = fm.get("assessor")
        if _empty(assessor_id):
            return findings
        assessor_row, target_row = find_row(assessor_id, folder, index), row
        subject = f"assessor '{assessor_id}'"
        if assessor_row is None:
            return [Finding("family", label, None, f"no registry row found for {subject}")]
    if target_row is None:
        return [Finding("family", label, None, f"no registry row found for {subject}")]
    a, t = _family(assessor_row), _family(target_row)
    if a is None or t is None:
        findings.append(Finding("family", label, None, f"model family missing for {subject}"))
    elif a == t:
        findings.append(
            Finding("family", label, None,
                    f"assessor and target share model family '{a}'; use a different family ({subject})")
        )
    return findings


# ---------------------------------------------------------------- driver


def run(path: Path, today: date) -> list[Finding]:
    path = Path(path)
    base = path if path.is_dir() else path.parent
    index = build_index(base)
    findings: list[Finding] = []
    for charter in discover(path):
        label = rel_posix(base, charter) if path.is_dir() else charter.name
        findings.extend(lint_charter(charter, label, index, today))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint agent charters against registry rows.")
    parser.add_argument("path", help="a charter file or a folder to scan")
    parser.add_argument("--today", default=None, help="date for review checks, YYYY-MM-DD")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    path = Path(args.path)
    if not path.exists():
        print(f"agent_lint: path not found: {path}", file=sys.stderr)
        return 2
    if args.today is None:
        today = date.today()
    else:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            print(f"agent_lint: --today must be YYYY-MM-DD, got '{args.today}'", file=sys.stderr)
            return 2
    return report("agent_lint", run(path, today))


if __name__ == "__main__":
    sys.exit(main())
