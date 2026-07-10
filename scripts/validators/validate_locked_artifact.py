#!/usr/bin/env python3
"""
validate_locked_artifact.py — Verify a file's SHA-256 hash matches the stored hash.

Usage:
    python3 validate_locked_artifact.py <artifact_path> <expected_sha256>

Exit codes:
    0 — Hash matches (MATCH)
    1 — Hash mismatch, file not found, or argument error (MISMATCH / ERROR)
"""

import argparse
import hashlib
import os
import sys


def sha256_file(path):
    """Compute SHA-256 of a file and return lowercase hex digest."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(artifact_path, expected_hash):
    print(f"\nLocked artifact verification")
    print("=" * 60)
    print(f"  File   : {artifact_path}")
    print(f"  Expected: {expected_hash.lower()}")

    # File existence check
    if not os.path.exists(artifact_path):
        print(f"  Computed: <file not found>")
        print(f"\n  Result  : MISMATCH — file does not exist at the given path.")
        print("=" * 60)
        return False

    if not os.path.isfile(artifact_path):
        print(f"  Computed: <path is not a regular file>")
        print(f"\n  Result  : MISMATCH — path exists but is not a regular file.")
        print("=" * 60)
        return False

    computed = sha256_file(artifact_path)
    print(f"  Computed: {computed}")

    match = computed.lower() == expected_hash.lower()
    if match:
        print(f"\n  Result  : MATCH — hash verified.")
    else:
        print(f"\n  Result  : MISMATCH — hash does not match stored value.")
        print(f"            The artifact may have been modified since locking.")

    print("=" * 60)
    return match


def main():
    parser = argparse.ArgumentParser(
        description="Verify the SHA-256 hash of a locked artifact file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "artifact_path",
        help="Path to the artifact file to verify.",
    )
    parser.add_argument(
        "expected_sha256",
        help="Expected SHA-256 hex digest (64 lowercase hex characters).",
    )
    args = parser.parse_args()

    # Basic format check on the supplied hash
    if len(args.expected_sha256) != 64 or not all(
        c in "0123456789abcdefABCDEF" for c in args.expected_sha256
    ):
        print(
            f"ERROR: expected_sha256 must be a 64-character hex string; "
            f"got {len(args.expected_sha256)} characters: {args.expected_sha256!r}"
        )
        sys.exit(1)

    ok = validate(args.artifact_path, args.expected_sha256)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
