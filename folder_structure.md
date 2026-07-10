# Quantitative Research Assistant — Folder Structure Reference

PROJECT_ROOT: the folder you opened in Claude Code (your current working directory)

Use this as a reference for the project layout. All paths are relative to the project root.

## Full directory tree

```
research/
├── README.md                          ← start here — what QRA is and how to use it
├── CLAUDE.md                          ← auto-loaded by Claude Code at every session start
├── folder_structure.md                ← this file
│
├── agent/
│   ├── system_prompt.md               ← QRA role, workflow, and guardrails
│   ├── system_prompt.sha256           ← hash of system_prompt.md — verified at every session start
│   ├── agent_manifest.sha256          ← hashes of all config files — verified at every session start
│   ├── init_check.sh                  ← runs at every session start — do not delete
│   ├── generate_manifest.py           ← regenerates agent_manifest.sha256 after config changes
│   ├── edge_cases.md                  ← edge-case overfit rules for deviations, REGRESS, and data change log
│   ├── ARCHITECTURE.md                ← design rationale for the FSM, gates, and validators
│   └── examples/                      ← reference examples the agent uses during the workflow
│       ├── analysis_plan_examples.md
│       ├── deviations_examples.md
│       ├── s1_intake_examples.md
│       └── state_log_examples.md
│
├── knowledge/                         ← domain reference files (loaded by agent on demand)
│   ├── INDEX.md                       ← load at every session start — maps files to workflow stages
│   ├── _audit_ground_truth_checklist.md ← internal QA checklist for reviewing agent outputs
│   ├── 01_research_design.md
│   ├── 02_sampling_and_power.md
│   ├── 03_measurement.md
│   ├── 04_statistical_methods.md
│   ├── 05_causal_inference.md
│   ├── 06_reporting_standards.md
│   ├── 07_ethics_and_privacy.md
│   ├── 08_reproducibility.md
│   ├── 09_ux_research_methods.md
│   ├── 10_ux_metrics_and_benchmarking.md
│   └── 11_triangulation_and_mixed_methods.md
│
├── scripts/
│   └── validators/                    ← deterministic enforcement scripts (agent runs these)
│       ├── README.md                  ← what each validator checks and what errors mean
│       ├── validate_project_state.py
│       ├── validate_locked_artifact.py
│       ├── validate_s5_script.py
│       ├── validate_results_md.py
│       └── validate_dry_run_byte_identical.py
│
├── .claude/                           ← hidden folder (show hidden files in your OS file manager to see it)
│   └── commands/
│       └── qra.md                     ← /qra slash command
│
└── studies/
    └── <study_name>/                  ← one folder per study, created automatically by /qra
        ├── project_state.md           ← active workflow state — do not edit by hand
        ├── state_log.jsonl            ← append-only audit trail of every state transition
        ├── deviations.md              ← log of any approved deviations from the locked plan
        ├── s1_intake.md
        ├── s2_research_questions.md
        ├── s3_design_and_method.md
        ├── s4_data_plan.md
        ├── analysis_plan_locked.md    ← locked at S6 approval — hash-verified, do not edit
        ├── data/
        │   ├── raw/                   ← drop your data file here using your file manager
        │   ├── interim/               ← cleaned data (agent writes)
        │   └── processed/             ← analysis-ready data (agent writes)
        ├── scripts/                   ← Python analysis scripts (agent writes and runs these)
        │   ├── s5_exploratory.py
        │   └── s7_primary_analysis.py
        ├── outputs/
        │   ├── tables/                ← .xlsx output files
        │   ├── figures/               ← .png chart files
        │   └── logs/                  ← script run logs
        ├── 05_exploratory/
        │   └── outputs/               ← exploratory plots and notes
        ├── report/
        │   ├── results.md             ← final results report (APA 7 format)
        │   └── results.docx           ← Word export — ready to share
        └── dry_run/                   ← pre-flight check outputs (agent writes, do not edit)
```

---

## Notes for new users

**Files the agent manages — do not edit by hand:**
- `project_state.md` — the agent's memory for the study. Editing it directly will corrupt the workflow state.
- `analysis_plan_locked.md` — locked at S6 approval and hash-verified. Any edit will cause a hash mismatch and halt the agent.
- `state_log.jsonl` — append-only audit trail. The agent writes to this; it is never edited.
- `dry_run/` — temporary outputs from the agent's pre-flight check before live analysis runs.
- `agent/system_prompt.sha256` and `agent/agent_manifest.sha256` — auto-managed hash files. Do not edit; the agent regenerates these when config files change.

**Files worth knowing about:**
- `deviations.md` — if anything changes from the locked analysis plan during S7, the agent logs it here. This file is reproduced in the final results report.
- `state_log.jsonl` — if something goes wrong and you need to understand what the agent did and when, this is the audit trail.
- `scripts/validators/README.md` — if the agent surfaces a validator error, start here to understand what it means.
- `agent/init_check.sh` — runs silently at every session start to verify the agent's configuration files. Do not delete it.
- `agent/generate_manifest.py` — regenerates `agent_manifest.sha256` if you ever update a config file and need to re-verify it. You will not need this under normal use.

**Adding your data (S5):**
1. Open your file manager and navigate to `studies/<study_name>/data/raw/`.
2. Copy or move your CSV or Excel file into that folder.
3. In the Claude Code chat, tell the agent the filename.

**Viewing results (S7):**
- Open `report/results.docx` from your file manager — it opens in Microsoft Word or any compatible word processor.
- Tables: `outputs/tables/` — open `.xlsx` files in Excel.
- Figures: `outputs/figures/` — open `.png` files in any image viewer.

**Hidden folder:**
`.claude/` is a hidden folder. To view it: on macOS press `Cmd+Shift+.` in Finder; on Windows enable 'Show hidden items' in File Explorer; on Linux press `Ctrl+H` in your file manager.
