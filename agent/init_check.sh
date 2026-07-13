#!/bin/bash
# QRA session init — runs all integrity checks in one Bash call.
# Exit 0 = all clear. Exit 1 = failure (output describes what failed).
# Output protocol (consumed by CLAUDE.md Session Initialization):
#   INIT ERROR     — environment problem (e.g. Python missing). NOT a tamper warning.
#   HASH MISMATCH  — a config file's contents changed since last verified.
#   RESUME: study=<name> state=<S>   — most recently modified active study.
#   OTHER ACTIVE STUDY: study=<name> state=<S> — additional active studies, if any.
#   NO ACTIVE STUDY: begin at S1
#   INIT OK        — all checks passed.

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

# 0. Resolve a Python 3 interpreter. `python3` is frequently absent on Windows
# (Git Bash); fall back to `python`, then the `py` launcher.
PY=""
for CAND in python3 python "py -3"; do
  if $CAND -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then
    PY="$CAND"
    break
  fi
done
if [ -z "$PY" ]; then
  echo "INIT ERROR: no Python 3 interpreter found (tried python3, python, py -3)."
  echo "  Install Python 3.10+ from python.org, restart the session, and re-run."
  exit 1
fi

# 1 + 2. Verify system_prompt.sha256 and every file in agent_manifest.sha256.
# Paths are passed as arguments — never interpolated into Python source.
$PY - "$PROJECT_ROOT" <<'PYEOF'
import hashlib, json, os, sys

root = sys.argv[1]
fail = False

def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# system_prompt.sha256
sp = os.path.join(root, "agent", "system_prompt.md")
sp_hash_file = os.path.join(root, "agent", "system_prompt.sha256")
try:
    stored = open(sp_hash_file, encoding="utf-8").read().strip()
    actual = sha256(sp)
except OSError as e:
    print(f"INIT ERROR: cannot read {e.filename}: {e.strerror}")
    fail = True
else:
    if stored != actual:
        print("HASH MISMATCH: agent/system_prompt.md has changed since last verified.")
        print(f"  stored: {stored}")
        print(f"  actual: {actual}")
        fail = True

# agent_manifest.sha256
manifest_path = os.path.join(root, "agent", "agent_manifest.sha256")
try:
    manifest = json.loads(open(manifest_path, encoding="utf-8").read())
except OSError as e:
    print(f"INIT ERROR: cannot read agent/agent_manifest.sha256: {e.strerror}")
    fail = True
    manifest = {}
except ValueError as e:
    print(f"INIT ERROR: agent/agent_manifest.sha256 is not valid JSON: {e}")
    fail = True
    manifest = {}
for rel_path, stored_hash in manifest.items():
    full_path = os.path.join(root, *rel_path.split("/"))
    try:
        actual_hash = sha256(full_path)
    except OSError:
        print(f"HASH MISMATCH: {rel_path} not found")
        fail = True
        continue
    if actual_hash != stored_hash:
        print(f"HASH MISMATCH: {rel_path} has changed since last verified.")
        print(f"  stored: {stored_hash}")
        print(f"  actual: {actual_hash}")
        fail = True

sys.exit(1 if fail else 0)
PYEOF
[ $? -ne 0 ] && FAIL=1

# 3. Check for active studies — only if integrity checks passed.
# Studies live at studies/<study_name>/project_state.md. No PyYAML needed:
# the two keys are extracted with a line regex. ARCHIVED studies are skipped.
if [ $FAIL -eq 0 ]; then
  $PY - "$PROJECT_ROOT" <<'PYEOF'
import glob, os, re, sys

root = sys.argv[1]
paths = glob.glob(os.path.join(root, "studies", "*", "project_state.md"))
paths.sort(key=os.path.getmtime, reverse=True)

def read_key(text, key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip("\"'") if m else None

active = []
for p in paths:
    try:
        text = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    state = read_key(text, "current_state") or "UNKNOWN"
    if state == "ARCHIVED":
        continue
    study = read_key(text, "study_name") or os.path.basename(os.path.dirname(p))
    active.append((study, state))

if not active:
    print("NO ACTIVE STUDY: begin at S1")
else:
    study, state = active[0]
    print(f"RESUME: study={study} state={state}")
    for study, state in active[1:]:
        print(f"OTHER ACTIVE STUDY: study={study} state={state}")
PYEOF
fi

if [ $FAIL -eq 0 ]; then
  echo "INIT OK"
fi
exit $FAIL
