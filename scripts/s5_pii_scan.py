#!/usr/bin/env python3
"""S5 PII scan — run before any other S5 operation (see system_prompt.md S5).

Usage:
    python3 scripts/s5_pii_scan.py studies/<study_name>/data/raw/<file>.csv

Checks every column for: email, phone (E.164 and common US formats), SSN,
credit card (Luhn), IP address, date-of-birth patterns, full-name patterns,
high-cardinality string columns, and free-text columns averaging > 40 chars.

Standard library only — runs before the per-study venv exists.
CSV is read natively; .xlsx requires openpyxl (use the study venv python,
or export the sheet to CSV first).

Exit codes: 0 = no hits, 1 = one or more hits (HALT per system prompt),
2 = usage or file-read error.
"""
import csv
import datetime
import re
import sys
from pathlib import Path

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
# E.164 (+ followed by 8-15 digits) or US formats that use separators/parens.
# Bare 10-digit integers are NOT matched (too many ID-column false positives);
# those are still caught by the Luhn, high-cardinality, and header checks.
PHONE_RE = re.compile(
    r"(\+\d{8,15}\b)|(\(\d{3}\)\s?\d{3}[\s\-.]\d{4})|(\b\d{3}[\-.\s]\d{3}[\-.\s]\d{4}\b)"
)
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
IP_RE = re.compile(
    r"\b(25[0-5]|2[0-4]\d|1?\d?\d)\.(25[0-5]|2[0-4]\d|1?\d?\d)"
    r"\.(25[0-5]|2[0-4]\d|1?\d?\d)\.(25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
DATE_RE = re.compile(r"\b(0?[1-9]|1[0-2])[/\-](0?[1-9]|[12]\d|3[01])[/\-](\d{2}|\d{4})\b")
ISO_DATE_RE = re.compile(r"\b(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")
NAME_RE = re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+$")
HEADER_HINT_RE = re.compile(
    r"e[\-_ ]?mail|phone|mobile|telephone|\bssn\b|social.?security|"
    r"credit.?card|card.?number|\bdob\b|birth|first.?name|last.?name|full.?name|"
    r"\baddress\b|\bip\b",
    re.IGNORECASE,
)


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def scan_column(header: str, values: list) -> list:
    hits = []
    non_empty = [v for v in values if v and v.strip()]
    if HEADER_HINT_RE.search(header or ""):
        hits.append("PII_COLUMN_NAME")
    if not non_empty:
        return hits
    joined = "\n".join(non_empty)
    if EMAIL_RE.search(joined):
        hits.append("EMAIL")
    if PHONE_RE.search(joined):
        hits.append("PHONE")
    if SSN_RE.search(joined):
        hits.append("SSN")
    if IP_RE.search(joined):
        hits.append("IP_ADDRESS")
    # Dates: only a plausible *birth* date is PII. Survey exports almost always
    # carry response timestamps (StartDate/EndDate) — flagging those would halt
    # every real study. A date is DOB-plausible if its year implies an adult
    # participant; header hints (dob/birth) are caught by PII_COLUMN_NAME above.
    this_year = datetime.date.today().year
    adult_birth_cutoff = this_year - 16

    def _to_year(token):
        y = int(token)
        if len(token) == 4:
            return y
        # Two-digit year: pivot on the current year ("24" → 2024, "85" → 1985).
        return 2000 + y if 2000 + y <= this_year else 1900 + y

    years = [_to_year(m.group(3)) for m in DATE_RE.finditer(joined)]
    years += [int(m.group(0)[:4]) for m in ISO_DATE_RE.finditer(joined)]
    if any(1900 <= y <= adult_birth_cutoff for y in years):
        hits.append("DATE_PATTERN (possible DOB — verify)")
    # Full names are near-unique per row; Likert text labels ("Strongly Agree")
    # repeat heavily. Require high uniqueness so label columns don't halt.
    name_matches = sum(1 for v in non_empty if NAME_RE.match(v.strip()))
    unique_ratio = len(set(non_empty)) / len(non_empty)
    if len(non_empty) >= 5 and name_matches / len(non_empty) >= 0.5 and unique_ratio >= 0.8:
        hits.append("FULL_NAME_PATTERN (heuristic)")
    for v in non_empty:
        digits = re.sub(r"\D", "", v)
        # Card IINs start with 2-6; this excludes epoch timestamps (start with 1)
        # and most numeric IDs that would otherwise pass Luhn by chance.
        if 13 <= len(digits) <= 19 and digits[0] in "23456" and luhn_ok(digits):
            hits.append("CREDIT_CARD_LUHN")
            break
    if len(non_empty) > 20 and len(set(non_empty)) > 0.8 * len(non_empty):
        # Numeric-looking columns (measurements, ratings) are exempt.
        numeric = sum(1 for v in non_empty if re.fullmatch(r"-?\d+(\.\d+)?", v.strip()))
        if numeric / len(non_empty) < 0.9:
            hits.append("HIGH_CARDINALITY_STRING")
    avg_len = sum(len(v) for v in non_empty) / len(non_empty)
    if avg_len > 40:
        hits.append("LONG_FREE_TEXT (avg > 40 chars)")
    return hits


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 2
    if path.suffix.lower() in (".xlsx", ".xls"):
        print(
            "ERROR: Excel input requires openpyxl. Run this scan with the study "
            "venv python (which has openpyxl installed), or export the sheet to "
            "CSV in data/raw/ and scan the CSV."
        )
        return 2

    try:
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except OSError as e:
        print(f"ERROR: could not read {path}: {e}")
        return 2

    if not rows or len(rows) < 2:
        print("ERROR: file is empty or contains only a header row.")
        return 2

    headers = list(rows[0])
    # Ragged files: some data rows may have MORE cells than the header
    # (unquoted commas). Those overflow cells must be scanned too, never
    # silently dropped — pad the header out to the widest row.
    width = max(len(headers), max(len(r) for r in rows[1:]))
    headers += [f"(unnamed column {i + 1})" for i in range(len(headers), width)]
    padded = [list(r) + [""] * (width - len(r)) for r in rows[1:]]
    columns = list(zip(*padded))

    print(f"PII SCAN REPORT — {path}")
    print(f"Rows: {len(rows) - 1}  |  Columns: {len(headers)}")
    print("=" * 60)
    any_hit = False
    for i, header in enumerate(headers):
        values = list(columns[i]) if i < len(columns) else []
        hits = scan_column(header, values)
        if hits:
            any_hit = True
            print(f"  [HIT] Column {i + 1} ({header!r}): {', '.join(hits)}")
    print("=" * 60)
    if any_hit:
        print(
            "PII HITS FOUND. HALT: user must reply ETHICS CONFIRMED (consent + "
            "privacy plan cover this data) or provide a de-identified file."
        )
        return 1
    print("PII scan PASSED — no hits. Safe to proceed to schema validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
