#!/bin/bash
# QRA session init — runs all integrity checks in one Bash call.
# Exit 0 = all clear. Exit 1 = mismatch (output describes what failed).

export PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

# 1. Verify system_prompt.sha256
STORED=$(cat "$PROJECT_ROOT/agent/system_prompt.sha256" 2>/dev/null)
ACTUAL=$(python3 -c "import hashlib; print(hashlib.sha256(open('$PROJECT_ROOT/agent/system_prompt.md','rb').read()).hexdigest())" 2>/dev/null)
if [ "$STORED" != "$ACTUAL" ]; then
  echo "HASH MISMATCH: system_prompt.md has changed since last verified."
  echo "  stored: $STORED"
  echo "  actual: $ACTUAL"
  FAIL=1
fi

# 2. Verify agent_manifest.sha256 (all 3 config files)
python3 - <<'PYEOF'
import json, hashlib, sys, os
root = os.environ.get('PROJECT_ROOT', '')
if not root:
    print("ERROR: PROJECT_ROOT environment variable is not set.")
    sys.exit(1)
manifest_path = os.path.join(root, "agent/agent_manifest.sha256")
try:
    manifest = json.loads(open(manifest_path).read())
except Exception as e:
    print(f"MANIFEST ERROR: cannot read agent_manifest.sha256 — {e}")
    sys.exit(1)
fail = False
for rel_path, stored_hash in manifest.items():
    full_path = os.path.join(root, rel_path)
    try:
        actual_hash = hashlib.sha256(open(full_path, "rb").read()).hexdigest()
    except FileNotFoundError:
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

# 3. Check for active study (project_state.md in cwd)
if [ -f "./project_state.md" ]; then
  STATE=$(python3 -c "import yaml,sys; d=yaml.safe_load(open('./project_state.md')); print(d.get('current_state','UNKNOWN'))" 2>/dev/null || echo "PARSE ERROR")
  STUDY=$(python3 -c "import yaml,sys; d=yaml.safe_load(open('./project_state.md')); print(d.get('study_name','unknown'))" 2>/dev/null || echo "unknown")
  echo "RESUME: study=$STUDY state=$STATE"
else
  echo "NO ACTIVE STUDY: begin at S1"
fi

if [ $FAIL -eq 0 ]; then
  echo "INIT OK"
fi
exit $FAIL
