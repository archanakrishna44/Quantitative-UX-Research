#!/usr/bin/env python3
"""
validate_dry_run_byte_identical.py — Verify re-running an analysis script on
the same synthetic dataset produces byte-identical outputs to the S6 dry-run.

Usage:
    python3 validate_dry_run_byte_identical.py <dry_run_dir> <current_output_dir>

Exit codes:
    0 — All files match exactly (PASS)
    1 — One or more files differ, are missing, or an error occurred (FAIL)
"""

import argparse
import os
import re
import sys


# Lines beginning with a date prefix (YYYY-MM-DD) are stripped before
# comparing .log and .txt files.
DATE_LINE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

# File extensions treated as timestamp-tolerant (line-by-line comparison
# after stripping date-prefixed lines)
TIMESTAMP_TOLERANT_EXTENSIONS = {".log", ".txt"}


def _is_timestamp_tolerant(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in TIMESTAMP_TOLERANT_EXTENSIONS


def _collect_files(root_dir):
    """Return a dict of {relative_path: absolute_path} for all files under root_dir."""
    file_map = {}
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            abs_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(abs_path, root_dir)
            file_map[rel_path] = abs_path
    return file_map


def _compare_binary(path_a, path_b):
    """Return True if two files are byte-identical."""
    chunk_size = 65536
    with open(path_a, "rb") as fa, open(path_b, "rb") as fb:
        while True:
            chunk_a = fa.read(chunk_size)
            chunk_b = fb.read(chunk_size)
            if chunk_a != chunk_b:
                return False
            if not chunk_a:
                return True


def _strip_date_lines(path):
    """Read a file as text and return lines with date-prefixed lines removed."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return None
    return [l for l in lines if not DATE_LINE_RE.match(l)]


def _compare_timestamp_tolerant(path_a, path_b):
    """
    Compare two log/txt files line-by-line after stripping date-prefix lines.
    Return True if the stripped content is identical.
    """
    lines_a = _strip_date_lines(path_a)
    lines_b = _strip_date_lines(path_b)
    if lines_a is None or lines_b is None:
        return False
    return lines_a == lines_b


def validate(dry_run_dir, current_output_dir):
    # Existence checks
    for label, path in [("dry_run_dir", dry_run_dir), ("current_output_dir", current_output_dir)]:
        if not os.path.isdir(path):
            print(f"ERROR: {label} does not exist or is not a directory: {path}")
            sys.exit(1)

    dry_run_files = _collect_files(dry_run_dir)
    current_files = _collect_files(current_output_dir)

    matching = []
    differing = []    # list of (rel_path, detail)
    missing = []      # files in dry_run but not in current_output

    for rel_path, dry_abs in sorted(dry_run_files.items()):
        if rel_path not in current_files:
            missing.append(rel_path)
            continue

        curr_abs = current_files[rel_path]

        if _is_timestamp_tolerant(rel_path):
            match = _compare_timestamp_tolerant(dry_abs, curr_abs)
            method = "line-by-line (timestamp-tolerant)"
        else:
            match = _compare_binary(dry_abs, curr_abs)
            method = "byte-identical"

        if match:
            matching.append((rel_path, method))
        else:
            dry_size = os.path.getsize(dry_abs)
            curr_size = os.path.getsize(curr_abs)
            size_diff = curr_size - dry_size
            sign = "+" if size_diff >= 0 else ""
            differing.append(
                (
                    rel_path,
                    f"size dry={dry_size} bytes, current={curr_size} bytes "
                    f"(diff {sign}{size_diff}), method={method}",
                )
            )

    # Files present in current but not in dry_run (informational only — not a failure)
    extra_in_current = sorted(set(current_files.keys()) - set(dry_run_files.keys()))

    # ------------------------------------------------------------------ report
    print(f"\nDry-run byte-identity verification")
    print(f"  Reference (dry-run) : {dry_run_dir}")
    print(f"  Current output      : {current_output_dir}")
    print("=" * 60)

    print(f"\n  Files compared      : {len(dry_run_files)}")
    print(f"  Matching            : {len(matching)}")
    print(f"  Differing           : {len(differing)}")
    print(f"  Missing from current: {len(missing)}")
    print(f"  Extra in current    : {len(extra_in_current)}")

    if matching:
        print(f"\nMatching files ({len(matching)}):")
        for rel_path, method in matching:
            print(f"  [MATCH]  {rel_path}  ({method})")

    if differing:
        print(f"\nDiffering files ({len(differing)}):")
        for rel_path, detail in differing:
            print(f"  [DIFF]   {rel_path}")
            print(f"           {detail}")

    if missing:
        print(f"\nMissing from current output ({len(missing)}):")
        for rel_path in missing:
            print(f"  [MISS]   {rel_path}")

    if extra_in_current:
        print(f"\nExtra files in current output (not in dry-run baseline):")
        for rel_path in extra_in_current:
            print(f"  [EXTRA]  {rel_path}")

    print()
    print("=" * 60)

    failed = bool(differing or missing or extra_in_current)
    if failed:
        print("Overall result: FAIL")
        if differing or missing:
            print(
                "\nThe analysis script or environment has drifted since S6 locking.\n"
                "Investigate differing/missing files before executing the live analysis."
            )
        if extra_in_current:
            print(
                "\nExtra output files were produced that were not in the S6 dry-run baseline.\n"
                "These may represent undisclosed analysis. Each extra file must be\n"
                "acknowledged as a registered deviation before the validator can pass."
            )
    else:
        print("Overall result: PASS — all dry-run outputs reproduced exactly.")

    print("=" * 60)
    return failed


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Verify that re-running an analysis script on the same synthetic "
            "dataset produces byte-identical outputs to the S6 dry-run."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "dry_run_dir",
        help="Path to the S6 dry-run output directory.",
    )
    parser.add_argument(
        "current_output_dir",
        help="Path to the current re-run output directory to compare against.",
    )
    args = parser.parse_args()

    failed = validate(args.dry_run_dir, args.current_output_dir)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
