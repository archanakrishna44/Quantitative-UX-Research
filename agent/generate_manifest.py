#!/usr/bin/env python3
"""Generate agent_manifest.sha256 — run whenever any agent config file changes."""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FILES = [
    "agent/system_prompt.md",
    "CLAUDE.md",
    ".claude/commands/qra.md",
]

manifest = {}
for rel in FILES:
    p = ROOT / rel
    if p.exists():
        manifest[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    else:
        print(f"ERROR: tracked file not found: {rel}")
        sys.exit(1)

out = ROOT / "agent" / "agent_manifest.sha256"
out.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Manifest written to {out}")
for k, v in manifest.items():
    print(f"  {k}: {v}")
