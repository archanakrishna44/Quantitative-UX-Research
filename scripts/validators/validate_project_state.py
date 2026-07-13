#!/usr/bin/env python3
"""
validate_project_state.py — Schema-validate a QRA project_state.md YAML file.

Usage:
    python3 validate_project_state.py <path_to_project_state.md> [study_root_dir]

Exit codes:
    0 — All checks passed (PASS)
    1 — One or more violations found (FAIL)
"""

import argparse
import datetime
import hashlib
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml")
    sys.exit(1)


VALID_STATES = {"S1", "S2", "S3", "S4", "S5", "S6", "S7", "ARCHIVED"}
VALID_GATE_STATUSES = {"open", "approved", "n/a"}
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
ISO8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$"
)


def check_iso8601(value):
    """Return True if value looks like an ISO-8601 datetime string."""
    if not isinstance(value, str):
        return False
    return bool(ISO8601_RE.match(value.strip()))


def validate(state_path, study_root):
    violations = []
    warnings = []

    # ------------------------------------------------------------------ load
    if not os.path.isfile(state_path):
        print(f"ERROR: File not found: {state_path}")
        sys.exit(1)

    with open(state_path, "r", encoding="utf-8") as fh:
        raw = fh.read()

    # project_state.md is a YAML file; strip the outermost markdown code fence
    # only — do not remove interior backtick lines inside YAML block scalars
    # (finding #15).
    stripped = raw.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        # Remove only the first line (opening fence) and last line (closing fence)
        end = len(lines) - 1
        while end > 0 and lines[end].strip() == "```":
            end -= 1
        stripped = "\n".join(lines[1:end + 1])

    try:
        doc = yaml.safe_load(stripped)
    except yaml.YAMLError as exc:
        print(f"ERROR: YAML parse error in {state_path}:\n  {exc}")
        sys.exit(1)

    if not isinstance(doc, dict):
        print("ERROR: YAML root must be a mapping (dict).")
        sys.exit(1)

    # -------------------------------------------------------- required fields
    required_fields = [
        "study_name",
        "current_state",
        "entered_at",
        "gate_status",
        "locked_artifacts",
        "last_user_approval_token",
        "deviations_count",
        "primary_data_file",
        "data_hash",
        "session_id",
        "prompt_loaded_at",
        "open_questions",
        "assumptions",
    ]

    for field in required_fields:
        if field not in doc:
            violations.append(f"Missing required field: '{field}'")

    if violations:
        # Cannot safely validate further without required fields present
        _print_report(violations, warnings, state_path)
        return bool(violations)

    # -------------------------------------------------------- study_name
    study_name = doc["study_name"]
    if not isinstance(study_name, str) or not study_name.strip():
        violations.append("'study_name' must be a non-empty string.")

    # -------------------------------------------------------- current_state
    current_state = doc["current_state"]
    if current_state not in VALID_STATES:
        violations.append(
            f"'current_state' must be one of {sorted(VALID_STATES)}; got: {current_state!r}"
        )

    # -------------------------------------------------------- entered_at
    # PyYAML deserializes unquoted YAML dates (e.g. 2026-07-10) as datetime.date
    # objects, not strings. Accept both datetime.date and datetime.datetime as
    # valid, in addition to ISO-8601 strings (finding #13).
    entered_at = doc["entered_at"]
    entered_at_ok = (
        isinstance(entered_at, (datetime.date, datetime.datetime))
        or check_iso8601(str(entered_at) if entered_at is not None else "")
    )
    if not entered_at_ok:
        violations.append(
            f"'entered_at' must be an ISO-8601 datetime string; got: {entered_at!r}"
        )

    # -------------------------------------------------------- gate_status
    gate_status = doc["gate_status"]
    if gate_status not in VALID_GATE_STATUSES:
        violations.append(
            f"'gate_status' must be one of {sorted(VALID_GATE_STATUSES)}; got: {gate_status!r}"
        )

    # -------------------------------------------------------- locked_artifacts
    locked_artifacts = doc["locked_artifacts"]
    if locked_artifacts is None:
        locked_artifacts = {}
    if not isinstance(locked_artifacts, dict):
        violations.append("'locked_artifacts' must be a dict (mapping) or empty.")
    else:
        for artifact_path, sha_value in locked_artifacts.items():
            # SHA-256 value check
            if not isinstance(sha_value, str) or not SHA256_RE.match(sha_value):
                violations.append(
                    f"'locked_artifacts[{artifact_path!r}]' must be a 64-character hex SHA-256 "
                    f"string; got: {sha_value!r}"
                )
            # File existence check (if study_root provided)
            if study_root:
                full_path = os.path.join(study_root, artifact_path)
                if not os.path.isfile(full_path):
                    violations.append(
                        f"Locked artifact not found on disk: {full_path}"
                    )
                else:
                    # Verify the hash matches the file on disk
                    computed = _sha256_file(full_path)
                    if isinstance(sha_value, str) and SHA256_RE.match(sha_value):
                        if computed.lower() != sha_value.lower():
                            violations.append(
                                f"Hash mismatch for locked artifact '{artifact_path}': "
                                f"stored={sha_value}, computed={computed}"
                            )

    # -------------------------------------------------------- last_user_approval_token
    token = doc["last_user_approval_token"]
    if token is not None and not isinstance(token, str):
        violations.append(
            f"'last_user_approval_token' must be a string or null; got: {type(token).__name__}"
        )

    # -------------------------------------------------------- deviations_count
    deviations_count = doc["deviations_count"]
    if not isinstance(deviations_count, int) or deviations_count < 0:
        violations.append(
            f"'deviations_count' must be an integer >= 0; got: {deviations_count!r}"
        )

    # -------------------------------------------------------- primary_data_file
    pdf = doc["primary_data_file"]
    if pdf is not None and not isinstance(pdf, str):
        violations.append(
            f"'primary_data_file' must be a string or null; got: {type(pdf).__name__}"
        )

    # -------------------------------------------------------- data_hash
    data_hash = doc["data_hash"]
    if data_hash is not None:
        if not isinstance(data_hash, str) or not SHA256_RE.match(data_hash):
            violations.append(
                f"'data_hash' must match ^[a-f0-9]{{64}}$ or be null; got: {data_hash!r}"
            )

    # -------------------------------------------------------- session_id
    session_id = doc["session_id"]
    if not isinstance(session_id, str) or not session_id.strip():
        violations.append("'session_id' must be a non-empty string.")

    # -------------------------------------------------------- prompt_loaded_at
    pla = doc["prompt_loaded_at"]
    if pla is not None:
        if not check_iso8601(str(pla)):
            violations.append(
                f"'prompt_loaded_at' must be an ISO-8601 string or null; got: {pla!r}"
            )

    # -------------------------------------------------------- open_questions
    open_questions = doc["open_questions"]
    if open_questions is None:
        open_questions = []
    if not isinstance(open_questions, list):
        violations.append("'open_questions' must be a list.")
    else:
        for i, item in enumerate(open_questions):
            _check_question_or_assumption(item, "open_questions", i, violations)

    # -------------------------------------------------------- assumptions
    assumptions = doc["assumptions"]
    if assumptions is None:
        assumptions = []
    if not isinstance(assumptions, list):
        violations.append("'assumptions' must be a list.")
    else:
        for i, item in enumerate(assumptions):
            _check_question_or_assumption(item, "assumptions", i, violations)

    # -------------------------------------------------------- sequencing_note (optional)
    if "sequencing_note" in doc:
        sequencing_note = doc["sequencing_note"]
        if sequencing_note is not None and sequencing_note != "quant_first_accepted":
            violations.append(
                f"sequencing_note must be null or 'quant_first_accepted', got: {sequencing_note!r}"
            )

    _print_report(violations, warnings, state_path)
    return bool(violations)


def _check_question_or_assumption(item, field_name, index, violations):
    """Validate a single open_questions or assumptions entry."""
    if not isinstance(item, dict):
        violations.append(
            f"'{field_name}[{index}]' must be a dict; got: {type(item).__name__}"
        )
        return
    for required_key in ("id", "text", "raised_at_state"):
        if required_key not in item:
            violations.append(
                f"'{field_name}[{index}]' is missing required key: '{required_key}'"
            )
    # resolved_at_state is optional — no error if absent.
    # Extra keys are deliberately tolerated (forward-compatible).


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _print_report(violations, warnings, state_path):
    print(f"\nValidation report for: {state_path}")
    print("=" * 60)

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN]  {w}")

    if violations:
        print(f"\nVIOLATIONS ({len(violations)}):")
        for v in violations:
            print(f"  [FAIL]  {v}")
        print(f"\nResult: FAIL — {len(violations)} violation(s) found.")
    else:
        print("\nAll checks passed.")
        print("Result: PASS")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Schema-validate a QRA project_state.md YAML file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "state_file",
        help="Path to the project_state.md file to validate.",
    )
    parser.add_argument(
        "study_root",
        nargs="?",
        default=None,
        help="(Optional) Study root directory for resolving locked_artifact paths.",
    )
    args = parser.parse_args()

    failed = validate(args.state_file, args.study_root)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
