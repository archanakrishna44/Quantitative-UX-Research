---
scope: reference
modifies_workflow: false
---

# Statistical Methods

## UX Study Type → Statistical Test (Quick Lookup)

Use this table to identify the right test for common UX study outputs before reaching for the decision tree below.

| Study Type | Data Produced | Recommended Test | Effect Size to Report |
|---|---|---|---|
| Tree test (single task vs. benchmark) | Binary success per participant | One-proportion z-test or binomial test | — (report proportion + Wilson CI) |
| Tree test (two structures compared) | Binary success per participant, two groups | Two-proportion z-test or Chi-square (2×2) | Cohen's h |
| First-click test (vs. target accuracy) | Binary accuracy per participant | One-proportion z-test or binomial test | — (report proportion + Wilson CI) |
| First-click test (two designs compared) | Binary accuracy per participant, two groups | Two-proportion z-test or Chi-square (2×2) | Cohen's h |
| Card sort | Co-occurrence matrix, agreement ratios | Descriptive only (dendrogram, heat map) | Agreement ratio per card |
| A/B test — binary outcome (conversion, task completion, click-through) | Binary per participant per condition | Two-proportion z-test (primary); Chi-square (2×2) equivalent | Cohen's h; also report pp difference |
| A/B test — continuous outcome (time-on-task, revenue, engagement score) | Continuous per participant per condition | Independent t-test (Welch's) or Mann-Whitney U | Cohen's d |
| Survey benchmark vs. norm (SUS, UMUX-Lite) | Continuous scale score, one group | One-sample t-test | Cohen's d |
| Survey benchmark vs. prior study | Continuous scale score, two time points or two groups | Independent t-test (Welch's) or paired t-test (if same panel) | Cohen's d |

---

## Decision Tree: Which Test to Use

```
What is your outcome variable?
│
├── Continuous
│   ├── One group vs. known value → One-sample t-test
│   ├── Two independent groups → Independent t-test (Welch's default)
│   ├── Two paired/matched groups → Paired t-test
│   ├── 3+ independent groups → One-way ANOVA
│   ├── 3+ groups + covariate → ANCOVA
│   ├── Repeated measures → Repeated-measures ANOVA / mixed-effects
│   └── Continuous predictor(s) → Linear regression / OLS
│
├── Binary (Yes/No, Success/Fail, Conversion)
│   ├── Comparing two proportions (A/B test, two-variant task comparison)
│   │   ├── N ≥ 20 per cell → Two-proportion z-test or Chi-square (2×2)
│   │   └── N < 20 per cell → Fisher's Exact test
│   ├── Single proportion vs. known value → One-proportion z-test or binomial test
│   ├── Predictor(s) → Logistic regression
│   └── Matched pairs → McNemar's test
│
├── Count / Rate
│   └── Predictors → Poisson regression (negative binomial if overdispersed)
│
├── Ordinal
│   ├── Two independent groups → Mann-Whitney U
│   ├── Two paired groups → Wilcoxon signed-rank
│   ├── 3+ independent groups → Kruskal-Wallis
│   └── 3+ repeated → Friedman test
│
└── Time-to-event → Cox proportional hazards / Kaplan-Meier
```

---

## Two-Proportion z-Test for A/B Testing

When comparing two conversion rates, task completion rates, or success rates, the two-proportion z-test is the most direct approach for a 2×2 binary outcome. Chi-square is mathematically equivalent for a 2×2 table and gives the same p-value — use either; the two-proportion z-test more naturally produces a proportion difference with CI.

```python
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import numpy as np

# Example: Variant A: 102/300 conversions; Variant B: 123/300 conversions
count = np.array([102, 123])
nobs  = np.array([300, 300])

stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')
diff = count[1]/nobs[1] - count[0]/nobs[0]

# Wilson CI for each proportion
ci_a = proportion_confint(count[0], nobs[0], method='wilson')
ci_b = proportion_confint(count[1], nobs[1], method='wilson')

print(f"Proportion A: {count[0]/nobs[0]:.3f} {ci_a}")
print(f"Proportion B: {count[1]/nobs[1]:.3f} {ci_b}")
print(f"Difference: {diff:.3f}")
print(f"z = {stat:.3f}, p = {p_value:.4f}")
```

**What to report**: both proportions with individual Wilson CIs + the difference in percentage points + CI for the difference + z (or χ²) + p-value + Cohen's h.

**Cohen's h for proportions**:
```python
from statsmodels.stats.proportion import proportion_effectsize
h = proportion_effectsize(count[1]/nobs[1], count[0]/nobs[0])
```

Conventions: h = 0.20 small, 0.50 medium, 0.80 large.

**When to use Fisher's Exact instead**: if N < 20 per cell, the chi-square approximation is unreliable. Use `scipy.stats.fisher_exact()`.

---

## Wilson Confidence Intervals for Proportions

Use Wilson CIs (not Wald/normal-approximation CIs) whenever:
- N < 100, or
- The proportion is near 0 or 1 (e.g., 90%+ success rate or 5% error rate).

The Wald CI (`p ± 1.96 * sqrt(p(1-p)/n)`) can produce intervals outside [0, 1] and is systematically inaccurate at small N and extreme proportions. Wilson CIs do not have this problem.

```python
from statsmodels.stats.proportion import proportion_confint

# Wilson CI for a single proportion
successes = 43
n = 70
lo, hi = proportion_confint(successes, n, alpha=0.05, method='wilson')
print(f"{successes/n:.1%} (95% CI [{lo:.1%}, {hi:.1%}])")
```

Report format: "62% (95% Wilson CI [50%, 73%])".

---

## Scatter Plot Guidance for Correlation Analysis

Before running any Pearson or Spearman correlation, produce a scatter plot. This is not optional — it is the only way to verify that the statistical test is appropriate.

**Always produce a scatter plot because:**
- A non-linear but monotonic relationship looks different from a linear one. Pearson r will underestimate a curved association.
- Outliers can inflate or deflate Pearson r dramatically. A scatter plot makes them visible.
- Heteroscedasticity (variance that fans out as x increases) violates regression assumptions and is immediately visible in a scatter plot but invisible in a correlation coefficient alone.

**What to look for:**
- **Linearity**: does the cloud of points follow a roughly straight line? If curved, use Spearman ρ or transform a variable.
- **Outliers**: points far from the main cluster. Identify them, do not silently remove them — report them and run the analysis with and without.
- **Heteroscedasticity**: does the vertical spread of points increase (or decrease) as x increases? If yes, flag in the assumption check and consider robust regression.
- **Clustering**: distinct sub-clusters may indicate a moderator variable worth examining.

**Labeling in S5 exploratory outputs:**
- Title the plot with the two variable names and the study state: e.g., "EXPLORATORY: SUS Score vs. Task Completion Rate (N=87, S5 descriptive check)".
- Add the Pearson r and Spearman ρ as text annotations on the plot.
- If a trend line is added, label it as OLS fit with 95% CI band, and note that this is exploratory, not from the pre-registered analysis plan.

---

## Parametric Tests

### Independent Samples t-test
- **Use**: compare means of two independent groups.
- **Default**: Welch's t-test (does not assume equal variances). Do NOT default to Student's t-test.
- **Assumptions**: independence, approximately normal distribution (or large N by CLT), continuous outcome.
- **Report**: t(df), p, Cohen's d, 95% CI for the difference in means.

### Paired t-test
- **Use**: compare two related measurements (pre/post, matched pairs).
- **Assumptions**: differences are approximately normally distributed.
- **Report**: t(df), p, Cohen's d (for difference scores), 95% CI.

### One-Way ANOVA
- **Use**: compare means across 3+ independent groups.
- **Assumptions**: independence, normality within groups, homogeneity of variance (Levene's test).
- **Post-hoc tests**: Tukey HSD (equal n, equal variance); Games-Howell (unequal variance).
- **Report**: F(df_between, df_within), p, η² or ω² (prefer ω²), post-hoc comparisons with corrected p.

### Linear Regression (OLS)
- **Use**: predict a continuous outcome from one or more predictors.
- **Assumptions**: linearity, independence, homoscedasticity, normality of residuals, no perfect multicollinearity.
- **Report**: R², adjusted R², F-test for model, β (unstandardized) and β* (standardized) for each predictor, 95% CI for β.

### Logistic Regression
- **Use**: predict a binary outcome.
- **Report**: Odds Ratios (OR) with 95% CI, and the following model fit statistics:
  - **Discrimination**: AUC (area under the ROC curve). AUC > 0.7 acceptable, > 0.8 good, > 0.9 excellent.
  - **Calibration**: calibration plot (predicted vs. observed probabilities in deciles) to assess how well predicted probabilities match actual event rates.
  - **Pseudo-R²**: Nagelkerke R² as a rough effect size for comparative purposes.
  - **Do NOT use the Hosmer-Lemeshow goodness-of-fit test**: it produces unreliable results due to sensitivity to arbitrary grouping choices (the number and boundaries of groups affect the p-value) and has been largely deprecated in applied statistics. Use AUC and calibration plots instead.

## Non-Parametric Alternatives

| Parametric | Non-Parametric Alternative | When to Use |
|---|---|---|
| Independent t-test | Mann-Whitney U | Non-normal, ordinal, or small N |
| Paired t-test | Wilcoxon signed-rank | Non-normal differences |
| One-way ANOVA | Kruskal-Wallis | Non-normal, 3+ groups |
| Repeated-measures ANOVA | Friedman test | Non-normal repeated measures |
| Pearson correlation | Spearman correlation | Non-linear monotonic, ordinal, outliers |

## Effect Sizes (always report alongside p-values)

| Test | Effect Size Measure | Small | Medium | Large |
|---|---|---|---|---|
| t-test | Cohen's d | 0.20 | 0.50 | 0.80 |
| ANOVA | η² or ω² | 0.01 | 0.06 | 0.14 |
| Chi-square | Cramér's V | 0.10 | 0.30 | 0.50 |
| Two proportions | Cohen's h | 0.20 | 0.50 | 0.80 |
| Correlation | r | 0.10 | 0.30 | 0.50 |
| Regression | f² | 0.02 | 0.15 | 0.35 |
| Mann-Whitney | rank-biserial r | 0.10 | 0.30 | 0.50 |

**Note on Cramér's V thresholds**: the thresholds above (0.10 small, 0.30 medium, 0.50 large) apply when df_min = 1 (a 2×2 table). For larger tables, the benchmarks decrease with increasing table dimensions:
- 3×3 table (df_min = 2): 0.07 small, 0.21 medium, 0.35 large.
- 4×4 table (df_min = 3): 0.06 small, 0.17 medium, 0.29 large.
Always report the table dimensions alongside Cramér's V.

**Note on ω² vs. η² for ANOVA**: the η² thresholds (0.01 small, 0.06 medium, 0.14 large) apply to both η² and ω². Prefer ω² as the reported effect size because it is a less biased estimator — η² tends to overestimate the population effect size, particularly with small samples. ω² will be slightly smaller than η² for the same dataset, which is the expected and correct behavior. Thresholds: ω² < 0.01 negligible, 0.01 small, 0.06 medium, 0.14 large.

## Confidence Intervals
- Always report 95% CI for the primary effect estimate.
- A CI that excludes 0 (for differences) or 1 (for ratios) is consistent with statistical significance at α=0.05.
- Wide CIs indicate imprecision — flag if the CI spans both practically meaningful and trivial effects.
- Use Wilson CIs for proportions (see section above). Use standard CIs for means and differences in means.

## Assumption Checks

| Assumption | Test | If Violated |
|---|---|---|
| Normality | Shapiro-Wilk (N<50), visual inspection (Q-Q plot) for larger N | Use non-parametric alternative or robust estimator |
| Homogeneity of variance | Levene's test | Use Welch's t-test / Games-Howell post-hoc |
| Independence | Design-based judgment | Use clustered SEs or mixed-effects model |
| Linearity | Residual vs. fitted plot | Transform variables or add polynomial terms |
| Homoscedasticity | Residual vs. fitted plot, Breusch-Pagan | Use heteroscedasticity-robust SEs |
| Multicollinearity | VIF (> 10 is severe; > 5 worth examining) | Remove or combine predictors |

## Multiple Comparisons
- When running k tests, family-wise error rate = 1 − (1−α)^k.
- **Bonferroni**: divide α by number of tests. Conservative; use when tests are independent.
- **Holm-Bonferroni**: sequentially adjusted; more powerful than Bonferroni.
- **Benjamini-Hochberg (FDR)**: controls false discovery rate; preferred for exploratory work with many tests.
- Always report both raw and corrected p-values.
- Pre-specify which correction will be used in the S6 analysis plan.

## Correlation
- **Pearson r**: linear relationship between two continuous variables.
- **Spearman ρ**: monotonic relationship; use with ordinal data or outliers.
- Correlation ≠ causation. Never imply causal direction from a correlation alone.
- Report r, p, 95% CI, and N.
- Always produce a scatter plot before reporting any correlation (see Scatter Plot Guidance above).

## Sequential Testing and Always-Valid Inference (A/B Testing)

### The Traditional Problem

Fixed-horizon A/B tests require committing to a sample size N before launch. The statistical guarantee (α = 0.05 false positive rate) only holds if you check results exactly once — at the pre-specified N. Peeking at interim results and stopping early when p < 0.05 inflates the true Type I error rate substantially above the nominal α level.

### The Modern Solution: Always-Valid Inference

Always-valid inference (AVI) methods — specifically the mSPRT (mixture Sequential Probability Ratio Test) — allow continuous monitoring of an A/B test without inflating the false positive rate. The test remains valid regardless of when you check results because the statistical guarantee holds at every sample size simultaneously.

### Industry Implementation

Statsig, Eppo, and Amplitude Experiment implement always-valid inference as their default or recommended testing mode. When using these platforms, continuous monitoring is valid by design and the "do not peek" rule does not apply. The sequential testing is built into the test engine.

### When Fixed-Horizon Still Applies

Fixed-horizon rules (commit to N before launch, do not check results early) still apply when:
- You are NOT using a platform with built-in AVI.
- You are running a one-time study outside of an experimentation platform (e.g., manual Chi-square test on a spreadsheet, custom Python script without sequential correction).

### O'Brien-Fleming Alpha Spending

An alternative approach for fixed-horizon tests with planned interim analyses. Distributes the alpha budget across pre-specified interim looks using a boundary that is conservative early and relaxes over time. Originates from clinical trial methodology and is less commonly used in product experimentation than AVI. Use when you want planned interim looks with statistical discipline but are not using an AVI platform.

### Plain-Language Framing

"If your company uses Statsig, Eppo, or Amplitude Experiment, their built-in sequential testing handles the peeking problem for you. If you are running an A/B test outside these platforms, commit to your sample size before launch and do not check results until you hit it."

---

## Bayesian Inference: An Alternative to NHST

This section is provided at an awareness level. The QRA workflow is built on frequentist NHST (null hypothesis significance testing), but Bayesian methods offer a complementary framework that is increasingly common in applied research contexts.

**Core distinction**: Bayesian methods quantify evidence as a posterior distribution over hypotheses rather than producing a binary reject/fail-to-reject decision. Instead of asking "Is p < 0.05?", Bayesian analysis asks "Given the data, how probable is H1 relative to H0, and what is the plausible range of the effect?"

**Bayes factors**: a Bayes factor (BF10) expresses the relative evidence for H1 vs. H0. BF10 = 3 means the data are 3× more likely under H1 than H0. BF10 = 10 is considered strong evidence; BF10 < 1/3 is evidence for H0. Unlike p-values, Bayes factors can quantify evidence for the null.

**In Python**: the `pingouin` package returns BF10 for t-tests by default. Example:
```python
import pingouin as pg
result = pg.ttest(group_a, group_b, alternative='two-sided')
# result contains 'BF10' column alongside t, df, p-val, Cohen's d, CI
```

**Bayesian credible intervals**: directly interpretable as probability statements. A 95% credible interval means "there is a 95% probability that the true parameter falls in this range, given the data and prior." This is the interpretation most stakeholders intuitively expect from a "confidence interval" — but frequentist CIs do not support this interpretation.

**When to use Bayesian inference**: when sample sizes are small and NHST has low power; when stakeholders want to know "how likely is H1" rather than just "is p < 0.05"; when you want to accumulate evidence across studies rather than treat each study in isolation; when quantifying evidence for a null effect is meaningful (e.g., demonstrating that two designs are equivalent).

---

## Common Statistical Mistakes
- Using Student's t-test when Welch's is safer by default.
- Reporting p-values without effect sizes.
- Interpreting a non-significant result as "no effect" (absence of evidence ≠ evidence of absence).
- Treating p < 0.05 as the only criterion for importance (statistical vs. practical significance).
- Running tests on data before the analysis plan is locked (p-hacking risk).
- Using pairwise deletion for missing data without justification.
- Using Wald CIs for proportions near 0 or 1 — use Wilson CIs instead.
- Running a Chi-square on a 2×2 A/B table and failing to report Cohen's h or the percentage point difference — the effect size is what the team needs to make a decision.
- Peeking at A/B test results before reaching the pre-specified N when using a fixed-horizon test outside an AVI platform.
