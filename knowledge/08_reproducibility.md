---
scope: reference
modifies_workflow: false
---

# Reproducibility

## Why Reproducibility Matters
A study is reproducible if an independent researcher with the same data and scripts arrives at the same results. Reproducibility is the minimum bar — it does not guarantee the findings are correct, but it ensures they can be verified and built upon.

## Pre-Registration
Pre-registration means publicly committing to your hypotheses, design, and analysis plan before collecting or analyzing data.

**What to pre-register**:
- Research questions and hypotheses (directional or non-directional).
- Study design and sample size with power justification.
- Primary outcome variable and primary statistical test.
- Covariates and how they will be handled.
- Exclusion criteria and rules for handling outliers.
- Multiple comparison correction strategy.
- **Directionality**: whether each hypothesis test is one-tailed or two-tailed, and if one-tailed, the specified direction. Switching from two-tailed to one-tailed after seeing results is a researcher degree of freedom that effectively halves the p-value threshold without a pre-specified rationale, inflating Type I error.

**Where to pre-register**:
- **For product team UX research (internal studies not intended for publication)**: pre-registration happens internally. A time-stamped, locked document in your team's research repository (Confluence, Notion, Google Drive with version history, Dovetail) serves as the pre-registration artifact. The S6 locked analysis plan in this workflow IS your pre-registration. No external platform is required.
- **OSF (osf.io)** and **AsPredicted (aspredicted.org)**: appropriate only when the study will be written up for academic publication or shared publicly outside the organization. OSF supports embargo (you can lock the plan privately until publication). AsPredicted is short-form and fast for straightforward studies.
- Note: ClinicalTrials.gov is for clinical and health research — it is not an appropriate platform for UX research pre-registration.

**In this workflow**: the S6 locked analysis plan serves as the internal pre-registration. For studies intended for publication, register externally before S5 data collection.

**Exploratory vs. confirmatory**: anything analyzed beyond the pre-registered plan must be labeled as exploratory. Exploratory findings require replication before being treated as confirmatory.

## File and Folder Organization

Follow a consistent structure for every study (as defined in `folder_structure.md`):

```
studies/<study_name>/
├── data/raw/           ← original data, never modified
├── data/interim/       ← intermediate cleaned files
├── data/processed/     ← analysis-ready data
├── scripts/            ← all analysis scripts
├── outputs/            ← tables, figures, logs
└── report/             ← final written outputs
```

**Raw data is sacred**: never overwrite or modify files in `data/raw/`. All transformations happen in scripts that read from raw and write to interim or processed.

**Data file versioning**: if raw data is updated after initial collection (e.g., a second wave of survey responses arrives, a panel is topped up, or a data export is re-pulled with corrections), do not overwrite the original file. Save the new version as `raw_v2.csv` (or `raw_wave2.csv` if it is a distinct collection wave) and document the update in `data/raw/data_notes.md`. The `data_notes.md` entry should record: the date the new file was added, what changed or was added, and which scripts need to be re-run against the updated file.

## Scripts

### Naming Convention
- `s5_01_load_and_validate.py` — state prefix + sequence number + description.
- `s5_02_clean_and_transform.py`
- `s7_01_primary_analysis.py`
- `s7_02_sensitivity_analysis.py`

### Required Elements in Every Script
```python
# ============================================================
# Script: s7_01_primary_analysis.py
# Study: <study_name>
# State: S7 — Confirmatory Analysis
# Date: YYYY-MM-DD
# Python: 3.x | pandas: x.x | scipy: x.x | statsmodels: x.x
# Random seed: 42
# Description: Runs pre-registered primary analysis per
#              analysis_plan_locked.md
# ============================================================

import random
import numpy as np
random.seed(42)
np.random.seed(42)

DATA_PATH = "studies/<study_name>/data/processed/analysis_ready.csv"
OUTPUT_PATH = "studies/<study_name>/outputs/"
```

### Script Standards
- One script per major analysis step.
- Scripts are **idempotent**: running them twice produces the same output.
- No manual data edits outside scripts. If a manual fix is unavoidable, document it in a `data/raw/data_notes.md` file.
- All file paths use paths relative to the project root (the folder opened in Claude Code). Do not use absolute paths — they break on different machines.

## Package Version Pinning

At the start of every study, record package versions in `requirements.txt`:

```
pandas==2.1.0
numpy==1.25.2
scipy==1.11.2
statsmodels==0.14.0
pingouin==0.5.4
matplotlib==3.7.2
seaborn==0.12.2
openpyxl==3.1.2
```

**`pingouin`** is a recommended addition to every UX quant study environment. It provides more ergonomic APIs for t-tests, ANOVA, ICC, and correlation tests than raw scipy — returning results as tidy DataFrames with effect sizes and CIs included by default. Particularly useful for: paired and independent t-tests with Cohen's d, repeated-measures ANOVA, ICC for inter-rater reliability, and partial/semi-partial correlations. Install with `pip install pingouin`.

Generate with: `pip freeze > requirements.txt` (run after installing packages for the study).

To reproduce: `pip install -r requirements.txt`

## Random Seeds
- Set a seed at the top of every script that involves any random process (sampling, bootstrapping, train/test splits, simulations).
- Record the seed value in the script header and in the reproducibility appendix of the report.
- Use the same seed across related scripts in a study for consistency.

## The `project_state.md` File
Written and maintained by the QRA agent. Contains the audit trail of:
- Every state transition with timestamp.
- Every approval gate: what was approved, when, by whom (the researcher).
- Every deviation from the locked plan: what changed and why.
- Artifact locations: where the locked plan, raw data, scripts, and outputs live.

Do not edit `project_state.md` by hand. It is the agent's memory and the study's audit log.

## Reproducibility Appendix (include in every report)

At the end of the final report (`report/results.md`), include:

```
## Reproducibility Appendix

- **Software**: Python 3.11.4
- **Key packages**: pandas 2.1.0, scipy 1.11.2, statsmodels 0.14.0
- **Random seed**: 42 (set in all scripts)
- **Scripts**: studies/<study_name>/scripts/
  - s5_01_load_and_validate.py
  - s5_02_clean_and_transform.py
  - s7_01_primary_analysis.py
- **Data**: Raw data stored at studies/<study_name>/data/raw/ (not shared due to PII / available on request)
- **Analysis plan**: studies/<study_name>/analysis_plan_locked.md (locked YYYY-MM-DD)
- **Deviations from plan**: [none | list with justifications]
```

## Version Control for Analysis Scripts

Consider initializing a git repository in the study folder (`git init`) to track changes to analysis scripts over the course of the study. This provides a timestamped audit trail of script changes that supplements the pre-registration document.

At minimum:
- Commit the final analysis scripts before running confirmatory analysis (S7). This creates a timestamp that predates the results.
- If you make post-hoc deviations from the analysis plan (e.g., adding a covariate, changing the outlier rule), commit the modified scripts separately with a commit message documenting the deviation and its justification.
- The git log serves as a record of when each analytical decision was made, supporting the distinction between pre-registered and exploratory analyses.

This does not require a remote repository — a local git history is sufficient for audit purposes.

---

## Common Reproducibility Failures
- Overwriting the raw data file with a cleaned version.
- Manually editing cells in Excel before importing to Python.
- Not setting a random seed before bootstrapping or sampling.
- Using a relative file path that works on one machine but not another.
- Running scripts out of order and not noticing that an earlier output is stale.
- Saving figures without recording which script produced them.
