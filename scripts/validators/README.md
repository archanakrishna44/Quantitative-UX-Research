# QRA Validator Scripts

Shared, read-only validator scripts used by the Quantitative Research Assistant (QRA) across all studies. These scripts move enforcement out of the LLM system prompt and into deterministic code that fails closed.

All scripts:
- Accept arguments via `argparse`
- Print a human-readable report to stdout
- Exit `0` on pass, `1` on fail
- Never modify files (read-only)
- Require Python 3.10+ with standard library only (`pyyaml` is allowed)

---

## Scripts

### `validate_project_state.py`

Schema-validates a `project_state.md` YAML file against the QRA schema.

**Usage:**
```
python3 validate_project_state.py <path_to_project_state.md> [study_root_dir]
```

The optional `study_root_dir` argument enables file-existence and hash-match checks for every entry in `locked_artifacts`.

**Checks:**
- All required fields are present
- `current_state` is one of: `S1, S2, S3, S4, S5, S6, S7, ARCHIVED`
- `entered_at` and `prompt_loaded_at` are ISO-8601 datetime strings
- `gate_status` is one of: `open, approved, n/a`
- `locked_artifacts` is a dict of path → 64-char hex SHA-256
- `data_hash` matches `^[a-f0-9]{64}$` or is null
- `deviations_count` is an integer >= 0
- `open_questions` and `assumptions` entries each contain `id`, `text`, `raised_at_state`
- When `study_root_dir` is provided: each locked artifact file exists on disk and its computed SHA-256 matches the stored value

**Exit codes:** `0` = PASS, `1` = FAIL

---

### `validate_locked_artifact.py`

Verifies that a file's SHA-256 hash matches the hash stored in `project_state.md`.

**Usage:**
```
python3 validate_locked_artifact.py <artifact_path> <expected_sha256>
```

**Output:** Prints computed hash, expected hash, and MATCH or MISMATCH.

**Exit codes:** `0` = MATCH, `1` = MISMATCH or file not found

---

### `validate_s5_script.py`

AST-walks a Python script intended for S5 exploratory analysis and rejects any calls to banned inferential functions. Run this before executing any S5 script.

**Usage:**
```
python3 validate_s5_script.py <path_to_python_script>
```

**Banned patterns (any of these = FAIL):**
- `scipy.stats` hypothesis tests: `ttest_1samp`, `ttest_ind`, `ttest_rel`, `f_oneway`, `kruskal`, `mannwhitneyu`, `wilcoxon`, `chi2_contingency`, `fisher_exact`, `spearmanr`, `pearsonr`, `kendalltau`, `ks_2samp`, `shapiro`, `normaltest`, `anderson`
- `.fit()` calls on any object when `statsmodels` is imported (except `statsmodels.stats.power` objects)
- `pingouin` functions: `ttest`, `anova`, `ancova`, `rm_anova`, `mixed_anova`, `manova`, `pairwise_tests`, `mediation_analysis`, `logistic_regression`
- Any `.pvalue` attribute access
- Import of `pymc`, `bambi`, or `stan`

Aliased imports are tracked (e.g., `import scipy.stats as ss; ss.ttest_ind()` is caught).
Direct imports are tracked (e.g., `from scipy.stats import ttest_ind; ttest_ind()` is caught).

**Allowed (not flagged):** `scipy.stats.describe`, `.mean`, `.std`, `.sem`, `.skew`, `.kurtosis`, `pandas` descriptive methods, `matplotlib`, `seaborn`, `statsmodels.stats.power`.

**Exit codes:** `0` = PASS, `1` = FAIL

---

### `validate_results_md.py`

Checks a `results.md` file for compliance with QRA reporting rules.

**Usage:**
```
python3 validate_results_md.py <path_to_results_md> [--causal-strategy <strategy>]
```

`--causal-strategy` values: `RCT_ITT`, `DiD`, `IV`, `RDD`, `propensity_matching`, `DAG_adjustment`, `none` (default: `none`)

**Checks:**

| # | Check | Notes |
|---|-------|-------|
| 1 | Causal language ban | Only runs when `--causal-strategy none`. Flags: `causes`, `caused by`, `effect of`, `impact of`, `because of`, `led to`, `resulted in` |
| 2 | Effect size without CI | Flags `d =`, `η² =`, `r =`, `OR =`, `b =`, `Cohen` not followed by `95% CI` or `CI [` within 200 characters |
| 3 | Missing Deviations section | Checks for a `#` heading containing "Deviations" (case-insensitive) |
| 4 | Missing Reproducibility section | Checks for a `#` heading containing "Reproducibility" (case-insensitive) |
| 5 | Small cell suppression | Heuristic scan for `n = [1-4]` or `| [1-4] |` patterns; false positives acceptable, false negatives are not |
| 6 | APA-7 template compliance | At least one line must contain a stat marker (`t(`, `F(`, `b =`, `OR =`) paired with `p =` and `CI [` |

**Exit codes:** `0` = all checks PASS, `1` = one or more checks FAIL

---

### `validate_dry_run_byte_identical.py`

Verifies that re-running an analysis script on the same synthetic dataset produces byte-identical outputs to the S6 dry-run. Run this at S7 start before executing the live analysis.

**Usage:**
```
python3 validate_dry_run_byte_identical.py <dry_run_dir> <current_output_dir>
```

**Logic:**
- Recursively lists all files in `dry_run_dir`
- For each file, finds the corresponding file in `current_output_dir` (same relative path)
- Compares byte-by-byte for binary files
- For `.log` and `.txt` files: compares line-by-line after stripping lines that begin with `YYYY-MM-DD` (timestamp-tolerant)
- Reports: matched files, differing files (with size difference), missing files, and extra files (informational)
- Fails if any file differs or is missing from the current output

**Exit codes:** `0` = all files match (PASS), `1` = any file differs or is missing (FAIL)

---

## When to run each validator

| State | Validator | Trigger |
|-------|-----------|---------|
| S5 — before executing any exploratory script | `validate_s5_script.py` | Before every `python3` execution in S5 |
| S6 — before requesting approval | `validate_project_state.py` | Before presenting locked plan for approval |
| S6 — after writing each locked artifact | `validate_locked_artifact.py` | After writing `analysis_plan_locked.md` (and s2/s3/s4 equivalents) |
| S7 — before live analysis execution | `validate_dry_run_byte_identical.py` | At S7 start |
| S7 — after producing results | `validate_results_md.py` | Before presenting results to the user |

---

## Notes

- Scripts are **read-only** and will never modify any file.
- Scripts use only the Python 3.10+ standard library plus `pyyaml`.
- Per-study analysis scripts live in `studies/<study_name>/scripts/` — do not place them here.
- All paths in locked_artifacts within `project_state.md` are resolved relative to `study_root_dir` when that argument is supplied to `validate_project_state.py`.
