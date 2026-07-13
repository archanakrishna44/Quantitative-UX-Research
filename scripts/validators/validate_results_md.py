#!/usr/bin/env python3
"""
validate_results_md.py — Check a results.md file for QRA reporting compliance.

Usage:
    python3 validate_results_md.py <path_to_results_md> [--causal-strategy <strategy>]

Causal strategy values:
    RCT_ITT, DiD, IV, RDD, propensity_matching, DAG_adjustment, none (default)

Exit codes:
    0 — All checks passed (PASS)
    1 — One or more checks failed (FAIL)
"""

import argparse
import os
import re
import sys


VALID_CAUSAL_STRATEGIES = {
    "RCT_ITT",
    "DiD",
    "IV",
    "RDD",
    "propensity_matching",
    "DAG_adjustment",
    "none",
}

# ---------------------------------------------------------------------------
# Check 1 — Causal language (only when causal_strategy == 'none')
# ---------------------------------------------------------------------------
CAUSAL_PHRASES = [
    r"\bcauses\b",
    r"\bcaused\b",
    r"\bdue to\b",
    r"\bdrove\b",
    r"\beffect of\b",
    r"\bimpact of\b",
    r"\bbecause of\b",
    r"\bled to\b",
    r"\bresulted in\b",
]

# ---------------------------------------------------------------------------
# Check 2 — Effect size without confidence interval
# ---------------------------------------------------------------------------
# Patterns that introduce an effect size value
EFFECT_SIZE_PATTERNS = [
    r"\bd\s*=",          # Cohen's d
    r"\bη²\s*=",         # eta-squared (unicode)
    r"\bη\^2\s*=",       # eta-squared (caret notation)
    r"\bη2\s*=",         # eta-squared (plain)
    r"\br\s*=",          # correlation r
    r"\bOR\s*=",         # odds ratio
    r"\bb\s*=",          # regression coefficient
    r"\bCohen",          # Cohen's d/f/w mentioned
]
# CI marker patterns — if either appears within 200 chars after the effect size, it's compliant
CI_MARKERS = [r"95%\s*CI", r"CI\s*\["]

# ---------------------------------------------------------------------------
# Check 5 — Small cell detection
# ---------------------------------------------------------------------------
# Heuristic: n = 1, 2, 3, or 4 (with optional space variants), or table cells with 1–4
SMALL_CELL_PATTERNS = [
    r"\bn\s*=\s*[1-4]\b",          # n = 1 through n = 4
    r"\|\s*[1-4]\s*\|",            # | 1 | through | 4 | in tables
    r"\|\s*[1-4]\s*$",             # trailing cell at end of line
]

# ---------------------------------------------------------------------------
# Check 6 — APA-7 result line (basic presence check)
# ---------------------------------------------------------------------------
# At least one line must contain a stat marker AND p = AND CI [
# Parametric markers: t(, F(, b =, OR =
# Non-parametric markers: χ²(, χ2(, H(, U =, W = (Kendall's W / Wilcoxon)
# rs = (Spearman), V = (Cramér's V)
APA_STAT_MARKERS = [
    r"\bt\(",            # t-test
    r"\bF\(",            # ANOVA / F-test
    r"\bb\s*=",          # regression coefficient
    r"\bOR\s*=",         # odds ratio
    r"\bχ²\s*\(",        # Friedman / chi-square (unicode)
    r"\bχ\^2\s*\(",      # chi-square (caret notation)
    r"\bχ2\s*\(",        # chi-square (plain)
    r"\bH\s*\(",         # Kruskal-Wallis H
    r"\bU\s*=",          # Mann-Whitney U
    r"\bW\s*=",          # Kendall's W / Wilcoxon
    r"\brs\s*=",         # Spearman's rs
    r"\bV\s*=",          # Cramér's V
]
APA_P_VALUE = r"p\s*="
APA_CI = r"CI\s*\["


def check_causal_language(lines, causal_strategy):
    """Return list of (lineno, phrase, line_text) for each causal language hit."""
    if causal_strategy != "none":
        return []
    hits = []
    compiled = [re.compile(p, re.IGNORECASE) for p in CAUSAL_PHRASES]
    for i, line in enumerate(lines, start=1):
        for pat, phrase_pat in zip(compiled, CAUSAL_PHRASES):
            m = pat.search(line)
            if m:
                # Extract the matched text for display
                hits.append((i, m.group(0), line.rstrip()))
    return hits


def check_effect_size_without_ci(content, lines):
    """
    Return list of (lineno, matched_text, context) for effect size mentions
    NOT followed by a CI marker within 200 characters.
    """
    findings = []
    compiled_es = [re.compile(p, re.IGNORECASE) for p in EFFECT_SIZE_PATTERNS]
    compiled_ci = [re.compile(p, re.IGNORECASE) for p in CI_MARKERS]

    for es_pat in compiled_es:
        for m in es_pat.finditer(content):
            start = m.start()
            # Look 200 chars ahead in the raw content
            window = content[start: start + 200]
            has_ci = any(ci_pat.search(window) for ci_pat in compiled_ci)
            if not has_ci:
                # Compute line number from offset
                lineno = content[:start].count("\n") + 1
                line_text = lines[lineno - 1].rstrip() if lineno <= len(lines) else ""
                findings.append((lineno, m.group(0).strip(), line_text))

    return findings


def check_section_heading(lines, keyword):
    """Return True if any heading line (starting with #) contains keyword (case-insensitive)."""
    kw_lower = keyword.lower()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") and kw_lower in stripped.lower():
            return True
    return False


def check_small_cells(lines):
    """Return list of (lineno, matched_text, line_text) for potential small cell hits."""
    findings = []
    compiled = [re.compile(p, re.IGNORECASE) for p in SMALL_CELL_PATTERNS]
    for i, line in enumerate(lines, start=1):
        for pat in compiled:
            m = pat.search(line)
            if m:
                findings.append((i, m.group(0).strip(), line.rstrip()))
                break  # one hit per line is enough
    return findings


def check_apa7_presence(lines):
    """
    Return True if a stat marker, p-value, and CI all appear within a 3-line window.
    APA-7 Markdown tables typically spread these across adjacent rows, so checking
    a single line causes false failures on valid output (finding #9).
    """
    stat_compiled = [re.compile(p, re.IGNORECASE) for p in APA_STAT_MARKERS]
    p_compiled = re.compile(APA_P_VALUE, re.IGNORECASE)
    ci_compiled = re.compile(APA_CI, re.IGNORECASE)

    for i in range(len(lines)):
        window = " ".join(lines[i:i + 3])
        has_stat = any(pat.search(window) for pat in stat_compiled)
        has_p = p_compiled.search(window)
        has_ci = ci_compiled.search(window)
        if has_stat and has_p and has_ci:
            return True
    return False


def validate(results_path, causal_strategy):
    if not os.path.isfile(results_path):
        print(f"ERROR: File not found: {results_path}")
        sys.exit(1)

    with open(results_path, "r", encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()

    check_results = {}  # check_name -> (passed: bool, details: list[str])

    # ------------------------------------------------------------------ check 1
    causal_hits = check_causal_language(lines, causal_strategy)
    if causal_strategy == "none":
        if causal_hits:
            details = [
                f"  Line {ln:>4}: '{phrase}' — {src}"
                for ln, phrase, src in causal_hits
            ]
            check_results["1_causal_language"] = (False, details)
        else:
            check_results["1_causal_language"] = (True, [])
    else:
        check_results["1_causal_language"] = (
            True,
            [f"  Skipped (causal strategy = '{causal_strategy}')."],
        )

    # ------------------------------------------------------------------ check 2
    es_hits = check_effect_size_without_ci(content, lines)
    if es_hits:
        # Deduplicate by (lineno, matched_text) — multiple patterns can match same text
        seen = set()
        deduped = []
        for hit in es_hits:
            key = (hit[0], hit[1])
            if key not in seen:
                seen.add(key)
                deduped.append(hit)
        details = [
            f"  Line {ln:>4}: '{matched}' not followed by CI within 200 chars — {src}"
            for ln, matched, src in deduped
        ]
        check_results["2_effect_size_ci"] = (False, details)
    else:
        check_results["2_effect_size_ci"] = (True, [])

    # ------------------------------------------------------------------ check 3
    has_deviations = check_section_heading(lines, "Deviations")
    check_results["3_deviations_section"] = (
        has_deviations,
        [] if has_deviations else ["  No section heading containing 'Deviations' found."],
    )

    # ------------------------------------------------------------------ check 4
    has_reproducibility = check_section_heading(lines, "Reproducibility")
    check_results["4_reproducibility_section"] = (
        has_reproducibility,
        []
        if has_reproducibility
        else ["  No section heading containing 'Reproducibility' found."],
    )

    # ------------------------------------------------------------------ check 5
    cell_hits = check_small_cells(lines)
    if cell_hits:
        details = [
            f"  Line {ln:>4}: '{matched}' — potential unsuppressed small cell — {src}"
            for ln, matched, src in cell_hits
        ]
        check_results["5_cell_suppression"] = (False, details)
    else:
        check_results["5_cell_suppression"] = (True, [])

    # ------------------------------------------------------------------ check 6
    apa_ok = check_apa7_presence(lines)
    check_results["6_apa7_compliance"] = (
        apa_ok,
        []
        if apa_ok
        else [
            "  No line found matching APA-7 pattern: "
            "stat marker (t(, F(, b =, OR =) paired with 'p =' and 'CI ['."
        ],
    )

    # ------------------------------------------------------------------ report
    print(f"\nResults compliance report: {results_path}")
    print(f"Causal strategy: {causal_strategy}")
    print("=" * 60)

    check_labels = {
        "1_causal_language": "Check 1 — Causal language ban",
        "2_effect_size_ci": "Check 2 — Effect size without CI",
        "3_deviations_section": "Check 3 — Deviations section present",
        "4_reproducibility_section": "Check 4 — Reproducibility section present",
        "5_cell_suppression": "Check 5 — Small cell suppression",
        "6_apa7_compliance": "Check 6 — APA-7 template compliance",
    }

    any_failed = False
    for key in sorted(check_results.keys()):
        passed, details = check_results[key]
        status = "PASS" if passed else "FAIL"
        if not passed:
            any_failed = True
        print(f"\n  {check_labels[key]}: {status}")
        for d in details:
            print(d)

    print()
    print("=" * 60)
    if any_failed:
        print("Overall result: FAIL")
    else:
        print("Overall result: PASS")
    print("=" * 60)

    return any_failed


def main():
    parser = argparse.ArgumentParser(
        description="Check a results.md file for QRA reporting compliance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "results_file",
        help="Path to the results.md file to validate.",
    )
    parser.add_argument(
        "--causal-strategy",
        default="none",
        choices=sorted(VALID_CAUSAL_STRATEGIES),
        help=(
            "Causal identification strategy recorded in the locked S6 plan. "
            "Default: none (associational language required)."
        ),
    )
    args = parser.parse_args()

    failed = validate(args.results_file, args.causal_strategy)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
