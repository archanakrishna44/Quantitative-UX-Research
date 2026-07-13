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

# Keep the standalone system_prompt hash in sync — init_check.sh verifies both.
sp_out = ROOT / "agent" / "system_prompt.sha256"
sp_out.write_text(manifest["agent/system_prompt.md"] + "\n")
print(f"System prompt hash written to {sp_out}")

for k, v in manifest.items():
    print(f"  {k}: {v}")
