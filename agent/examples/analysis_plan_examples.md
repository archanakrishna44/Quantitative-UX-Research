# analysis_plan_locked.md — Examples

`analysis_plan_locked.md` is the frozen S6 pre-registered analysis plan. It MUST begin with a Predicate locks section. All modeling choices must derive from S2 and S4 alone. It lives at `studies/<study_name>/analysis_plan_locked.md`.

---

## CLEAN EXAMPLE

```markdown
# Analysis Plan (Locked) — mobile_nav_study
Locked at: 2025-11-10T16:45:02Z
Approved with token: APPROVED S6

---

## Predicate locks

| Artifact | Path | SHA-256 |
|----------|------|---------|
| s2_locked.md | studies/mobile_nav_study/s2_locked.md | a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856 |
| s3_locked.md | studies/mobile_nav_study/s3_locked.md | 7d2b1e48c93f056a14d8b72fc3e59a01d6b28374e5c9f012a3b74e8d25c9f103 |
| s4_locked.md | studies/mobile_nav_study/s4_locked.md | 5c8e3a92f1d047b6293e5d8c4f01a7b2e94d3c86f5a2019b7e3c84d1f2a56907 |

---

## 1. Primary analysis

**Derivation from locked artifacts:**
- S2 primary research question: "Is the task-success rate for the icon-only bottom-bar navigation
  design different from that of the icon-plus-label design among adult smartphone users?"
- S2 H0: task-success rate (icon-only) = task-success rate (icon-plus-label).
  H1: rates differ (non-directional).
- S4 primary outcome: task_success — binary (1/0), measured per task per participant.
  Unit of analysis: task-attempt (nested within participant).
- S4 measurement level: binary → logistic regression or chi-square.
- S3 study type: remote unmoderated tree test (Optimal Workshop); between-subjects design.

**Test specified:** Two-proportion z-test (equivalent to chi-square for 2x2 table) comparing
task-success proportions between the two conditions across all 8 tasks pooled.

- Software: Python 3.11.6 (scipy.stats.proportions_ztest)
- Random seed: 42
- Significance threshold: alpha = 0.05, two-tailed
- Effect size: Cohen's h, with 95% CI via bootstrap (n_boot = 10000, seed = 42)

## 2. Missing data

Participants who abandon all 8 tasks are excluded and noted in the reproducibility appendix.
For participants who abandon 1-7 tasks: available task-attempts are included. No imputation.
Assumption: task abandonment is missing-at-random with respect to condition assignment.

## 3. Outlier rule

Exclude task-attempts where time_on_task_seconds > median + 3xMAD (computed within condition
on the log scale). This applies to the time-on-task secondary analysis only — it does NOT affect
task_success coding. Expected exclusion rate <= 3%.

Pre-specified robustness check: re-run the primary z-test with zero exclusions and report both
results side-by-side.

## 4. Multiple-comparison plan

Confirmatory family: one test (primary two-proportion z-test).
No correction needed; family size = 1.

Pre-specified secondary tests (exploratory, labeled as such):
- Directness score (proportion of direct paths): two-proportion z-test, alpha = 0.05
- Time-on-task (log): Mann-Whitney U, alpha = 0.05
These are NOT part of the confirmatory family. Results are reported for completeness only.

## 5. Stopping rules

Not applicable — full sample collected before analysis.

## 6. Decision rule

Reject H0 if p < 0.05 (two-tailed) in the primary z-test.
Support rollout if task-success rate (icon-only) is non-inferior to icon-plus-label by >= 5
percentage points (pre-specified non-inferiority margin from S4 power analysis).

## 7. Environment

Python version: 3.11.6
requirements.txt: studies/mobile_nav_study/requirements.txt (generated at lock time)
Random seed: 42 (set in all scripts)
Dry-run output: studies/mobile_nav_study/dry_run/
```

Why this is clean:
- Begins with the mandatory Predicate locks table listing paths and SHA-256 hashes for all three upstream locked artifacts.
- Every modeling choice cites the S2 or S4 statement that drives it ("S2 primary research question", "S4 primary outcome", "S4 measurement level").
- The phrase "because the S5 data showed" does not appear anywhere.
- Outlier rule is expressed as executable pseudo-code with the variable named and the expected exclusion rate stated.
- Multiple-comparison plan is explicit: family size = 1, no correction needed; secondary tests are labeled exploratory and excluded from the family.
- Decision rule is operationalized, not vague.
- Environment section records Python version, requirements.txt location, random seed, and dry-run location.

---

## TRICKY EXAMPLE

```markdown
# Analysis Plan (Locked) — survey_sat_study
Locked at: 2025-11-12T11:22:09Z
Approved with token: APPROVED S6

---

## Predicate locks

| Artifact | Path | SHA-256 |
|----------|------|---------|
| s2_locked.md | studies/survey_sat_study/s2_locked.md | b1c4d7e29f3a056b8d2c4e7f1a3b5d8c2e4f6a0b1c3d5e7f9a2b4c6d8e0f2a4b |
| s3_locked.md | studies/survey_sat_study/s3_locked.md | 9e3f1a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f |
| s4_locked.md | studies/survey_sat_study/s4_locked.md | 2d4f6a8b0c2e4f6a8b0c2e4f6a8b0c2e4f6a8b0c2e4f6a8b0c2e4f6a8b0c2e4f |

---

## 1. Primary analysis

During S5 exploratory checks, the UMUX-Lite total score showed significant right-skew
(Shapiro-Wilk p = 0.003) and kurtosis = 4.7. Because the S5 data showed non-normality,
we are switching the primary test from an independent-samples t-test (originally planned)
to a Mann-Whitney U test.

- Software: Python 3.11.6 (scipy.stats.mannwhitneyu)
- Random seed: 42
- Significance threshold: alpha = 0.05, two-tailed

## 2. Missing data

Listwise deletion.

## 3. Outlier rule

Remove any participant whose UMUX-Lite score is more than 2 standard deviations from the mean.
We will decide the exact threshold after reviewing the full dataset.

## 4. Multiple-comparison plan

We will run three tests: UMUX-Lite score, SUS score, and a new NPS item we added after
looking at the data because stakeholders asked for it.

## 5. Decision rule

If p < 0.05 we will recommend the new design.
```

WHAT IS WRONG AND WHY IT FAILS:

1. **Primary test choice is justified by S5 data findings — explicitly forbidden.**
   Section 1 states: "Because the S5 data showed non-normality, we are switching the primary test."
   The S6 rule is unambiguous: "The phrase 'because the S5 data showed...' is forbidden as
   justification for the primary test specification." The primary test must be derivable from S2
   (outcome type, design structure) and S4 (measurement levels, expected distribution) alone.
   If a nonparametric fallback is needed, it must have been pre-specified in S4 as a contingency.
   A switch made after seeing actual distributional characteristics from real data contaminates the
   analysis with knowledge of outcomes and invalidates pre-registration. The fix is either:
   (a) use the S4-pre-specified contingency test if one exists, or (b) treat the Mann-Whitney as
   an exploratory robustness check alongside the originally planned t-test, with the t-test
   remaining primary.

2. **Outlier rule is not executable and is deferred to post-data inspection.**
   "We will decide the exact threshold after reviewing the full dataset" is explicitly prohibited.
   The S6 rule requires: "the exact rule as executable pseudo-code... the variable(s) it applies
   to, and the expected exclusion rate." An outlier rule decided after seeing the data is
   HARKing-adjacent and cannot be locked.

3. **Multiple-comparison plan adds an outcome variable introduced after data collection.**
   The NPS item was "added after looking at the data because stakeholders asked for it." This is
   outcome-switching. Any test added after the S6 lock is exploratory by definition — the system
   prompt states this explicitly: "any test added after lock is exploratory regardless of result."
   Adding it to the confirmatory family retroactively is a violation. It must be labeled
   exploratory or trigger a formal deviation with APPROVED DEVIATION token.

4. **Decision rule is incomplete.**
   "If p < 0.05 we will recommend the new design" does not specify which test drives the decision,
   nor does it address effect size thresholds or what happens with null results. The locked plan
   must operationalize what result supports or fails to support each hypothesis.
