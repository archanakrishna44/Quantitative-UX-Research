---
scope: reference
modifies_workflow: false
---

# UX Metrics and Benchmarking — S4 Reference

This file supports the QRA's S4 operationalization step. It covers how each UX metric behaves statistically, how to define it a priori, published benchmark norms, and how to make valid benchmark comparisons. For statistical test mechanics, see `04_statistical_methods.md`. For method-to-metric alignment, see `09_ux_research_methods.md`.

---

## Metric Properties at a Glance

| Metric | Distribution | Level of Measurement | Correct CI Method | Recommended Summary Stats |
|---|---|---|---|---|
| Task completion rate | Binomial | Binary (0/1) | Wilson CI | Proportion + 95% Wilson CI |
| Time-on-task | Right-skewed (log-normal) | Continuous | t-test on log-transformed values | Geometric mean, median, IQR |
| Error rate | Poisson (count per session/task) | Count | Poisson CI or exact CI | Mean count, median, range |
| Tree test success rate | Binomial | Binary (0/1) | Wilson CI | Proportion + 95% Wilson CI |
| Tree test directness score | Binomial | Binary (0/1) | Wilson CI | Proportion + 95% Wilson CI |
| First-click accuracy | Binomial | Binary (0/1) | Wilson CI | Proportion + 95% Wilson CI |
| Time-to-first-click | Right-skewed | Continuous | t-test on log-transformed values | Geometric mean, median, IQR |
| SUS score | Approximately normal at n ≥ 20 | Continuous (0–100) | Standard t-interval | Mean, SD, 95% CI |
| UMUX-Lite score | Approximately normal at n ≥ 20 | Continuous (0–100) | Standard t-interval | Mean, SD, 95% CI |
| SEQ score | Ordinal (1–7); treat as continuous at n ≥ 20 | Ordinal → Continuous | Standard t-interval | Mean, SD, 95% CI per task |
| NPS | Non-normal, trimodal | Ordinal (−100 to +100) | Bootstrap CI | Score + bootstrap 95% CI |
| Custom Likert composite | Approximately normal if α ≥ 0.70 and n ≥ 20 | Continuous (after aggregation) | Standard t-interval | Mean, SD, Cronbach's α |

---

## Behavioral Metrics

### Task Completion Rate

**What it is**: the proportion of participants who successfully complete a defined task. The single most fundamental UX performance metric.

**Level of measurement**: binary (success = 1, fail = 0) per participant per task.

**Distribution**: binomial. Do NOT assume normality for small N. The normal approximation CI (p ± 1.96 × SE) is unreliable when N < 30 or when the proportion is near 0 or 1.

**Correct CI method: Wilson interval.** Formula:
- Lower bound: (2np + z² − z√(z² + 4np(1−p))) / (2(n + z²))
- Upper bound: (2np + z² + z√(z² + 4np(1−p))) / (2(n + z²))
- Where z = 1.96 for 95% CI, n = sample size, p = observed proportion.
- Most statistical software (scipy.stats.proportion_confint with method='wilson') computes this directly. Use it.

**Defining "success" a priori**: before data collection, document:
- The specific task wording participants will receive.
- The exact end state or action that constitutes success (e.g., "participant lands on the checkout confirmation page" — not "participant seems satisfied").
- Whether partial completions (e.g., reached the right page but through an incorrect path) count as success or failure. Pre-specify this.
- The scoring protocol for ambiguous cases.

**Industry benchmark norms** (Sauro & Dumas, 2009; MeasuringU):
- Average task completion rate across usability studies: approximately 78%.
- A task completion rate below 70% is a strong signal of a usability problem worth prioritizing.
- Above 90% is considered good for high-stakes tasks (e.g., completing a purchase, filing a form).
- These norms apply to moderated and unmoderated usability sessions, not tree tests (which have their own norms).

**Statistical tests**:
- One sample vs. benchmark: one-sample proportion test (z-test). Report z, p, and Wilson CI.
- Two independent groups: Chi-square (or Fisher's exact if expected cell count < 5). Report Cramér's V.
- Pre/post within same participants: McNemar's test.

See `04_statistical_methods.md` for test guidance.

---

### Time-on-Task

**What it is**: elapsed time from task start to task end (defined end state — success or failure). A secondary metric; interpret alongside completion rate, not in isolation.

**Level of measurement**: continuous, measured in seconds.

**Distribution**: strongly right-skewed. A small number of participants who struggle will take very long times, pulling the mean up. The normal distribution assumption is routinely violated. Do NOT report the mean without acknowledging skew.

**Correct analysis approach**:
1. Log-transform time values before any parametric analysis (natural log or log base 10).
2. Run t-test or ANOVA on log-transformed values.
3. Back-transform the mean of log times to get the **geometric mean** (this is your primary summary statistic for time).
4. Always report **median and IQR** alongside the geometric mean in any design-team report.

**Outlier handling**:
- Pre-specify the rule before data collection. Recommended rule: cap values exceeding 3× the task median. Document the cap value and the number of observations capped.
- Do NOT simply delete outliers — cap and document.
- Participants who abandoned the task (never reached the end state) are typically excluded from time analysis; pre-specify this rule.

**Reporting format**: "Geometric mean time-on-task was 47s (median: 42s, IQR: 31–68s). Three observations (8%) were capped at the pre-specified 3× median threshold (126s)."

**Statistical tests**:
- Two-group comparison: Welch's t-test on log-transformed values (back-transform CIs for reporting).
- Non-parametric alternative if you prefer: Mann-Whitney U on raw values.
- Correlation with completion rate: Spearman's ρ (not Pearson — the relationship is not linear).

---

### Error Rate

**What it is**: count of errors made during a task or session. Must be defined a priori. Common error types: wrong navigation choices, form submission errors, help-seeking events, task restarts.

**Level of measurement**: count (non-negative integer) per task or per session.

**Distribution**: Poisson (for rare errors) or negative binomial (if variance > mean — overdispersion is common in UX error data).

**Defining errors a priori**:
- Create an error taxonomy before data collection listing each countable error type.
- Decide whether you will count errors per task, per session, or as a rate (errors per minute).
- Decide whether repeated attempts at the same action count as one error or multiple.
- For unmoderated studies, limit error tracking to server-logged events (form validation failures, 404 hits, back-button use at defined steps) — behavioral observation errors require a moderator.

**Reporting**: mean errors per task (or session) + SD, range, and the error taxonomy counts.

**Industry benchmark** (Sauro, 2016; MeasuringU): average of approximately 0.7 errors per task across usability studies; roughly 10% of tasks are completed without any errors. Use these as rough reference points — error rates vary substantially by task complexity, product domain, and error taxonomy definition. Set your own benchmark at S3 based on the task type and the product context.

**Statistical tests**:
- Comparing two designs on error rate: Poisson regression or Mann-Whitney U (if distribution is overdispersed).
- If error counts are small and distribution is highly skewed: use negative binomial regression.
- See `04_statistical_methods.md` for count data test guidance.

---

### Tree Test Success Rate

**What it is**: proportion of participants who reached the correct final destination in a tree test task. The primary metric for tree testing.

**Level of measurement**: binary (correct/incorrect destination) per participant per task.

**CI method**: Wilson interval (same as task completion rate — see above).

**Interpreting directness alongside success:**

| Success Rate | Directness Score | What This Means | Design Action |
|---|---|---|---|
| ≥ 80% | ≥ 70% | IA working well | No structural change needed |
| ≥ 80% | < 50% | Users find it eventually but path is confusing | Revisit intermediate labels and signposting |
| < 70% | ≥ 70% | Users confidently go to the wrong place | A label or category name is actively misleading |
| < 70% | < 50% | Users are lost — no confident path | Fundamental IA mismatch with mental models |

**Thresholds for action** (Optimal Workshop and MeasuringU norms):
- Success rate < 70% on any task = strong signal of an IA problem.
- Directness score < 50% on a task with high success rate = label clarity problem.
- First click on the correct top-level node: if < 50%, the top-level structure is misaligned.

---

### Tree Test Directness Score

**What it is**: proportion of participants who reached the correct destination without any backtracking (never reversed direction up the tree after descending).

**Level of measurement**: binary (direct/not direct) per participant per task.

**CI method**: Wilson interval.

**Threshold**: a directness score below 50% on a task that has high success rate is a navigation clarity problem — users are finding the destination despite the structure, not because of it.

---

### First-Click Accuracy

**What it is**: proportion of participants whose first click falls within the pre-defined correct target zone on a screenshot or wireframe.

**Level of measurement**: binary (hit/miss) per participant per task. Target zones must be defined before data collection.

**CI method**: Wilson interval.

**Threshold** (from Spool's research): tasks where first-click accuracy is ≥ 80% predict high task completion rates. Tasks where first-click accuracy falls below 50% are strong candidates for redesign before a full usability study.

**Pre-specifying target zones**: for each task, document the exact pixel region(s) that constitute a correct first click before any data collection. If two elements are equally correct first clicks, include both in the target zone definition. Do NOT add zones after seeing the heatmap — this is hypothesis-after-results.

---

### Time-to-First-Click

**What it is**: elapsed time from image display to the participant's first click.

**Distribution**: right-skewed. Same handling as time-on-task.

**Reporting**: geometric mean + median + IQR. Long time-to-first-click combined with low accuracy indicates high visual confusion. Long time-to-first-click combined with high accuracy may indicate deliberate scanning — use qualitative follow-up to distinguish.

---

## Attitudinal Metrics and Validated Scales

### SUS (System Usability Scale)

**What it is**: a 10-item post-task or post-session questionnaire measuring perceived usability. The most widely used and benchmarked UX scale. Each item rated 1–5 (strongly disagree → strongly agree).

**Scoring formula** (must be applied exactly — do NOT skip this):
1. For odd-numbered items (1, 3, 5, 7, 9): subtract 1 from the raw score.
2. For even-numbered items (2, 4, 6, 8, 10): subtract the raw score from 5.
3. Sum all 10 adjusted scores and multiply by 2.5.
4. Result is a single score from 0 to 100.

**Interpretation norms** — Sauro (2011) percentile system. This is the sole normative reference for SUS benchmarking. Based on 500+ products in the MeasuringU database.

| SUS Score | Percentile (approx.) | Grade | Interpretation |
|---|---|---|---|
| ≥ 80.3 | 90th | A (Excellent) | Top 10% of benchmarked products |
| 74–80.2 | 70th–89th | B (Good) | Above average |
| 68–73.9 | 50th–69th | C (Okay) | Average range |
| 51–67.9 | 15th–49th | D (Poor) | Below average |
| < 51 | < 15th | F (Awful) | Bottom 15% |

**Key number: 68 is the industry average SUS score across Sauro's database of 500+ products.** 80.3 is the 90th percentile. 85+ is approximately the top 5–10%.

**Note on the Bangor et al. (2009) adjective scale**: the adjective rating system (Acceptable/Good/Excellent) uses different thresholds derived from a different dataset. Do not mix the Bangor et al. adjective thresholds with the Sauro percentile thresholds — they are not interchangeable. Use the Sauro percentile system for benchmarking.

**When to compare to industry norm vs. prior study**:
- Compare to 68 (industry norm) when you have no prior baseline and need to contextualize the score for stakeholders.
- Compare to your own prior study score (independent samples t-test) when you want to measure whether a redesign improved perceived usability. This is more sensitive than the industry norm comparison.
- Do NOT compare to both and report only the favorable comparison.

**Statistical test**: one-sample t-test vs. 68 for the industry norm comparison. Report t, df, p, Cohen's d, and 95% CI for the mean SUS score.

**Administration rule**: administer SUS as a single block of 10 items immediately after the participant completes all tasks. Do NOT intersperse other questions between SUS items.

---

### UMUX-Lite

**What it is**: a 2-item alternative to SUS. Faster to administer but slightly less reliable than SUS. Suitable when brevity is critical and a rough benchmark is sufficient.

**Items**:
1. "[This system's] capabilities meet my requirements." (7-point scale: 1 = strongly disagree, 7 = strongly agree)
2. "[This system] is easy to use." (7-point scale: same anchors)

**Scoring formula**:
- Raw score = (Item 1 + Item 2 − 2) / 12 × 100
- Result is 0–100.

**SUS conversion formula** (Sauro & Lewis, 2015):
- Converted SUS = 0.65 × UMUX-Lite score + 22.9
- Use this to plot UMUX-Lite results on SUS norms when comparing to benchmarks reported as SUS scores.

**When to use UMUX-Lite over SUS**: when the study is embedded in a longer survey and every additional item is a completion-rate risk; when you have used UMUX-Lite consistently across prior studies and want longitudinal comparability.

---

### SEQ (Single Ease Question)

**What it is**: a single-item post-task difficulty rating. "Overall, how would you rate the difficulty of this task?" on a 7-point scale (1 = Very Difficult, 7 = Very Easy).

**Level of measurement**: ordinal (single item); treat as continuous for group-level analysis when n ≥ 20.

**Norm** (Sauro & Dumas, 2009): the mean SEQ across task types is approximately 5.5 on the 7-point scale. A task scoring below 5.5 is considered harder than average.

**Threshold for action**: SEQ ≤ 4.5 on any task = strong signal of a perceived difficulty problem warranting investigation.

**Administration rule**: administer the SEQ immediately after each task — before the participant starts the next task. Post-session aggregation across tasks is acceptable for reporting but loses task-level granularity.

**Aggregating across tasks**: take the mean SEQ across tasks for a session-level perceived difficulty score. Weight tasks equally unless task importance differs, in which case document the weighting rule a priori.

**Statistical tests**:
- One task vs. norm (5.5): one-sample t-test. Report t, df, p, Cohen's d, 95% CI.
- Task A vs. Task B within same participants: paired t-test (or Wilcoxon signed-rank if N < 20).
- Two design variants: Welch's independent samples t-test per task; apply Holm-Bonferroni correction across tasks.

---

### NPS (Net Promoter Score)

**What it is**: a single-item loyalty question: "How likely are you to recommend [product/service] to a friend or colleague?" rated 0–10. Promoters = 9–10; Passives = 7–8; Detractors = 0–6. NPS = % Promoters − % Detractors.

**Calculation**: NPS ranges from −100 to +100.

**Why NPS is a weak primary UX metric**:
- The 0–10 scale is treated as if it were interval, but the Promoter/Passive/Detractor cut points are arbitrary.
- The scoring formula discards the Passive segment entirely, losing variance.
- NPS is highly sensitive to industry, country, and cultural response norms — industry benchmarks vary widely.
- NPS correlates poorly with behavioral loyalty in UX research contexts (vs. customer relationship contexts).
- NPS is a leading indicator of business outcomes, not a measure of usability or user experience quality.
- Requires very large N (200+) for stable estimates; confidence intervals are wide at typical UX study sample sizes.

**When to include NPS**: if stakeholders have an existing NPS tracking program and want UX study scores to connect to that system — for continuity only.

**When to exclude NPS**: when the study goal is to measure usability, task difficulty, or satisfaction with a specific feature. Use SUS, UMUX-Lite, or SEQ instead.

**Statistical test if used**: report as score + bootstrap 95% CI (not standard t-interval — distribution is trimodal and non-normal). Do NOT use a t-test on raw NPS scores.

**Industry benchmark context (MeasuringU)**:
- Consumer software NPS average: approximately +21%.
- B2B software NPS average: approximately +24%.
- Website NPS average: approximately −14%.
These benchmarks are highly context-dependent. Compare to benchmarks from your own industry and user segment rather than general tech averages where possible. NPS norms vary substantially by product category, delivery channel, and customer relationship type.

---

### Custom Likert Scales

**When to use over validated instruments**:
- The construct you need to measure (e.g., trust, perceived value, brand perception) is not covered by SUS, UMUX-Lite, or SEQ.
- You have domain-specific content that validated scales cannot capture.

**Reliability requirement**:
- Compute Cronbach's α before relying on a composite score. α ≥ 0.70 is the minimum acceptable threshold for UX research composites.
- If α < 0.70, examine inter-item correlations — remove the item with the lowest item-total correlation and recheck.
- If α cannot reach 0.70, do NOT aggregate items into a composite. Analyze items separately or treat the scale as exploratory.
- For new scales, factor analysis (EFA) should precede Cronbach's α computation to confirm the scale is unidimensional. Document this step in the analysis plan.

**Scoring**:
- Reverse-score negatively-worded items before computing the composite.
- Report the composite as a mean of items (not a sum) so the scale remains interpretable on the original response range.

**Statistical tests**: same as SUS once reliability is confirmed — one-sample t-test for benchmarking, Welch's t-test or Mann-Whitney U for group comparisons.

---

## Benchmarking

### Setting a Benchmark Before Data Collection

A benchmark is only valid if it is set before you see the data. Benchmarks set after looking at results are a form of HARKing (see `08_reproducibility.md`).

**Pre-specification checklist**:
- [ ] Benchmark value and source documented in the analysis plan (S6).
- [ ] Rationale: why is this the right target? (Published norm, prior study, business requirement, expert judgment with justification.)
- [ ] Direction: one-tailed (we expect to exceed the benchmark) or two-tailed (we are testing whether we differ from it).
- [ ] Minimum Detectable Effect (MDE): what is the smallest difference from the benchmark that would be practically meaningful?

**Sources for benchmarks**:
- SUS: industry average = 68 (Sauro, 2011; MeasuringU).
- SEQ: average task score = 5.5 (Sauro & Dumas, 2009).
- Task completion rate: industry average ≈ 78% (Sauro & Dumas, 2009).
- Tree test success rate: platform norms vary; MeasuringU reports average success rates across published tree tests at approximately 65–75%.
- First-click accuracy: no single published norm; use your own prior study data or a design-team-specified target (e.g., "at least 60% correct first clicks on the primary navigation").
- Time-on-task: no universal norm; use prior study data for the same or similar task.

### One-Sample Benchmark Comparison

Use when you are comparing your study result to a published norm or a pre-specified target.

- **Continuous metric (SUS, SEQ)**: one-sample t-test. H0: mean = benchmark value. Report t, df, p, Cohen's d, 95% CI.
- **Proportion (task completion, tree test success, first-click accuracy)**: one-sample proportion test (z-test for proportions). Report z, p, Wilson CI, effect size (h = 2 arcsin(√p₁) − 2 arcsin(√p₂) — Cohen's h).
- See `04_statistical_methods.md` for test mechanics.

### Comparative Benchmark: Current Study vs. Prior Study

Use when you want to measure whether a redesign improved outcomes compared to a previously measured baseline.

- **Same task, same population, same measurement instrument**: independent samples t-test (if participants differ across studies) or paired t-test (if same participants, pre/post design).
- **Proportions across two studies**: Chi-square for independent proportions.

**What makes a valid comparison**:
- Same task wording (or documented changes and their expected directional effects).
- Same population (same screener criteria, same recruiting channel).
- Same measurement instrument (same SUS version, same SEQ wording, same success/failure definition for task completion).
- Same study context (same prototype fidelity, same moderated vs. unmoderated condition).

If any of these differ, the comparison is compromised. Note the limitation explicitly in the study report.

### Published Benchmark Databases

- **MeasuringU (Jeff Sauro)**: largest public repository of SUS, UMUX-Lite, task completion, and time-on-task norms across industries and product types. Available at measuringu.com.
- **Nielsen Norman Group**: publishes benchmark data from proprietary studies; norms on task success rates and satisfaction for enterprise and consumer digital products.
- **Optimal Workshop**: publishes aggregate statistics on tree test and card sort outcomes from their platform user base.

When citing a benchmark, always cite the source, year, population it was based on, and whether the benchmark is appropriate for your study's population and context.

---

## Google HEART Framework and Goals-Signals-Metrics

### The HEART Dimensions

The HEART framework (Rodden, Hutchinson & Fu, 2010; Google) provides five dimensions for defining a product measurement framework. Not all five dimensions are required in every study — teams select the 2–3 most relevant to their product area.

| Dimension | What It Captures | Example Metric |
|---|---|---|
| Happiness | Attitudinal satisfaction, subjective experience | SUS score, NPS, custom satisfaction rating |
| Engagement | Behavioral depth of interaction — how much users interact, not just whether they do | Session frequency, feature activation rate, depth of usage |
| Adoption | New users starting to use a product or feature | % of new users who activate a feature within 7 days |
| Retention | Returning users — the product's ability to bring users back | Day-7 retention, weekly active users / monthly active users ratio |
| Task Success | Efficiency and effectiveness — can users accomplish their goals? | Task completion rate, time-on-task, error rate |

### Goals-Signals-Metrics (GSM) Process

The GSM process operationalizes HEART dimensions into measurable outcomes:

1. **Goal**: define the user behavior you want to affect. ("We want users to successfully complete their first report without seeking help.")
2. **Signal**: identify behavioral or attitudinal indicators that the goal is being met. ("Users who complete the first report within 10 minutes without triggering the help panel.")
3. **Metric**: select a specific, measurable operationalization of that signal. ("% of new users who complete their first report in under 10 minutes without a help event, measured via product analytics.")

### When to Use HEART

- Defining a product metrics framework at the start of a design cycle.
- Aligning research objectives to product KPIs so that research outputs map to business decisions.
- Structuring a measurement roadmap across multiple studies.
- Communicating research scope to stakeholders using a shared vocabulary.

### Common Implementation

Teams select 2–3 HEART dimensions most relevant to their product area (e.g., a productivity tool may emphasize Task Success and Happiness; a social product may emphasize Engagement and Retention). For each selected dimension, define 1–3 GSM pairs. The resulting metric definitions become the inputs to the S3 research design decision.

### Practical Note

HEART is a framework for defining what to measure, not a measurement instrument itself. Once metrics are defined through the GSM process, standard quantitative methods apply (task completion rates, SUS, analytics-based behavioral metrics). Do not cite HEART as a method in the Method section of a report — cite the specific instruments used.

**Source**: Rodden, K., Hutchinson, H., & Fu, X. (2010). Measuring the user experience on a large scale: user-centered metrics for web applications. CHI 2010. Google. Widely adopted across the technology industry.

---

## Key Driver Analysis

### What It Is

Key driver analysis uses standardized regression coefficients (beta weights) from a linear regression to rank the relative importance of predictor variables in explaining variance in an outcome variable. The outcome is typically overall satisfaction (SUS, NPS, CSAT) or task success. The predictors are the sub-dimensions or factors that might drive that outcome.

**Example question**: "Which dimensions of the experience — speed, reliability, visual design, or feature richness — most predict whether users will recommend this product?"

### When to Use

- "Which satisfaction dimensions are most responsible for our overall NPS score?"
- "What aspects of the experience most predict whether users return (retention)?"
- "If we could only fix one thing, what would move the needle most on SUS?"

Key driver analysis is a prioritization tool. It ranks predictors by their contribution to an outcome — enabling teams to focus improvement efforts on the highest-leverage dimensions.

### How to Run in Python

Standardize all predictors (z-scores) before running OLS regression. The standardized betas are directly comparable importance weights — a beta of 0.40 means that a 1 SD increase in that predictor is associated with a 0.40 SD increase in the outcome, controlling for other predictors.

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

# Standardize all predictors
df['speed_z'] = stats.zscore(df['speed_rating'])
df['reliability_z'] = stats.zscore(df['reliability_rating'])
df['design_z'] = stats.zscore(df['design_rating'])

# Standardize the outcome too (for fully standardized solution)
df['sus_z'] = stats.zscore(df['sus_score'])

# Run OLS
model = smf.ols('sus_z ~ speed_z + reliability_z + design_z', data=df).fit()
print(model.summary())  # Coefficients are the standardized betas
```

Report standardized betas with 95% CIs in a ranked table. Visualize as a horizontal bar chart of standardized betas with error bars.

### Limitations

- Key driver analysis identifies **correlation-based importance**, not causal importance. A predictor with a high standardized beta is strongly associated with the outcome — it does not necessarily cause it.
- **Multicollinearity** between predictors inflates uncertainty in individual beta estimates and can distort importance rankings. Check VIF (variance inflation factor) for all predictors before interpreting the key driver results. VIF > 5 warrants examination; VIF > 10 is severe and makes individual beta estimates unreliable.
- Results are sensitive to which predictors are included in the model. Adding or removing a correlated predictor can change other betas substantially.
