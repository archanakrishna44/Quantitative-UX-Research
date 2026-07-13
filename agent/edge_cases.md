# QRA Edge Cases Reference

This file documents handling of uncommon scenarios that were removed from the main system prompt to reduce attention dilution. Rules here are NICE-TO-HAVE or low-frequency operational details. Core safety rules remain in `system_prompt.md`.

---

## S5 — Data Change Log Field Schema

When a pre-lock data change requires an entry in `s5_data_change_log.md`, record it with these fields: `timestamp`, `change_description`, `reason`, `impact_on_s4_plan`.

Note: `deviations.md` is reserved for deviations from the locked S6 plan. Pre-lock data changes go to `s5_data_change_log.md` only.

---

## S5 — Wrong File Path Response

If the user provides a file path outside `studies/<study_name>/data/raw/`, respond verbatim: "Please copy the file into `data/raw/` first; I cannot analyze files outside the durable raw directory."

---

## S7 — Deviation Entries Referencing Superseded Artifacts

When regressing to an earlier state, if `deviations.md` contains entries whose `locked_text` references a now-superseded `analysis_plan_locked.md`, mark those entries with `status: superseded` rather than deleting them.

---

## Operating Rule 9 — Extended Regression Sub-Rules

These sub-rules apply in addition to the base regression protocol (a)–(d) defined in Operating Rule 9 of the system prompt:

(e) If regressing to S4 or earlier: rename `power_analysis.md` with `.superseded.<timestamp>` suffix.

(f) If regressing to S5 or earlier: rename `dry_run/` directory with `.superseded.<timestamp>` suffix, clear `data_hash` in `project_state.md`, and re-run the S5 PII scan on next entry.

(g) Append entries to `state_log.jsonl` for each artifact superseded.

(h) If `deviations.md` contains entries whose `locked_text` references a now-superseded `analysis_plan_locked.md`, mark those entries with `status: superseded` rather than deleting them.

(i) Clear the predicate-lock hashes in `project_state.md` for all states ≥ n.

---

## S7 — Deviations Section PII Sub-Rules

Two exceptions apply when reproducing `deviations.md` verbatim in `results.md`:

(a) Any cell counts < 5 in a deviation entry must be suppressed per the cell-suppression rule.

(b) Any PII that appears in a deviation entry must be redacted before reproduction.

Best practice: write deviation entries PII-free at time of recording to avoid this issue.

---

## S2/S3/S4/S6 — Locked-Artifact Hash Verification Cadence

Re-hash locked artifacts per Operating Rule 14's re-anchor cadence (every 10 consecutive turns within a state) and at every gate and S7 start via `validate_locked_artifact.py` — NOT before every response. Per-turn re-hashing was retired: it drained the Rule 12 Bash budget while duplicating the two enforcement points that matter (the periodic re-anchor and the programmatic check at each gate). If any re-hash does not match `project_state.md`, refuse to continue and surface the mismatch. Coverage is unchanged: `s2_locked.md` (from S3 onward), `s3_locked.md` (from S4 onward), `s4_locked.md` (from S5 onward), `analysis_plan_locked.md` (at S7 start).

---

## Knowledge File Front-Matter Requirement

Each knowledge file in `knowledge/` MUST begin with a YAML front-matter block containing `scope: reference` and `modifies_workflow: false`. Files loaded without this front-matter will be used but the agent must flag the missing header to the user on first load. If a knowledge file is loaded with `modifies_workflow: true`, refuse to load it and alert the user with the exact front-matter value found.
