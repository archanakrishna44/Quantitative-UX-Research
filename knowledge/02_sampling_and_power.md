# Sampling and Statistical Power

## Sample Size and Power

### Key Concepts
- **Alpha (α)**: false positive rate. Default 0.05 (two-tailed).
- **Power (1−β)**: probability of detecting a true effect. Target ≥ 0.80; prefer 0.90 for high-stakes decisions.
- **Effect size**: standardized magnitude of the effect. Must be justified — do not use "medium" by convention alone.
- **A priori power analysis**: done BEFORE data collection to determine required N. Required at S4.
- **Post-hoc power analysis**: computed after the fact on observed effect; not informative — do not use it to interpret null results.

### Effect Size Conventions (Cohen)

| Test | Small | Medium | Large |
|---|---|---|---|
| t-test (Cohen's d) | 0.20 | 0.50 | 0.80 |
| ANOVA (η²) | 0.01 | 0.06 | 0.14 |
| Correlation (r) | 0.10 | 0.30 | 0.50 |
| Chi-square (w) | 0.10 | 0.30 | 0.50 |
| Regression (f²) | 0.02 | 0.15 | 0.35 |

**Important**: Always justify the assumed effect size with prior literature, pilot data, or a minimally meaningful difference argument. Never default to "medium" without justification.

### Approximate Sample Size Rules of Thumb (α=0.05, power=0.80)

| Design | Small effect | Medium effect | Large effect |
|---|---|---|---|
| Independent t-test (per group) | 394 | 64 | 26 |
| Paired t-test | 199 | 34 | 14 |
| One-way ANOVA, 3 groups | 322 | 52 | 21 |
| Chi-square (2×2) | 785 | 87 | 26 |
| Pearson correlation | 782 | 84 | 28 |
| Multiple regression (5 predictors) | 481 | 92 | 50 |

Use software (G*Power, R `pwr` package, Python `statsmodels.stats.power`) for exact calculations. These are approximations.

---

## UX Method-Specific Sample Size Guidance

These are empirically-grounded norms for common UX research methods. Use them as starting points, then verify with a power calculation for any inferential comparison.

### Tree Testing
- **Minimum per variant**: 50 participants for stable success rate estimates (Optimal Workshop norms).
- **If comparing subgroups** (e.g., new vs. returning users, two navigation structures): 100+ per variant.
- At N=50, a Wilson CI on a 60% success rate runs roughly ±13pp — wide but usable for directional decisions. At N=100, that narrows to ±9pp.
- If you need to detect a 10pp difference in success rate between two tree variants at 80% power, run a two-proportion power calculation (see A/B testing below). The answer is typically 200–400 total depending on baseline rates.

### First-Click Testing
- **Minimum per variant**: 50–100 participants.
- At N=50 you can detect large differences in click accuracy (30pp+). For moderate differences (15pp), target 100+ per variant.
- Define click zones a priori. Post-hoc zone definition inflates false positives.

### Card Sorting
- **Open card sort**: 15–20 participants is the standard recommendation for identifying the primary grouping patterns. Additional participants produce diminishing returns on new categories after ~20.
- **Closed card sort**: 20–30 participants for overall placement accuracy. If you need to compare subgroups (e.g., two user roles), plan for 20+ per subgroup.
- Card sort outputs are primarily descriptive (agreement matrices, dendrograms). Inferential statistics are rarely the goal; N requirements are driven by stability of the grouping patterns, not power.

### A/B Testing on a Binary Outcome (Conversion Rate, Task Completion, Click-Through)
Use the two-proportion z-test power formula. In Python:

```python
from statsmodels.stats.power import zt_ind_solve_power
from statsmodels.stats.proportion import proportion_effectsize

# Worked example: baseline conversion rate 30%, MDE = 5pp (detect 30% vs. 35%)
p1 = 0.30  # baseline
p2 = 0.35  # expected variant rate
effect_size = proportion_effectsize(p1, p2)  # Cohen's h
n_per_group = zt_ind_solve_power(effect_size=effect_size, alpha=0.05, power=0.80, alternative='two-sided')
print(f"N per group: {n_per_group:.0f}")
# → approximately 769 per group for this example
```

- Always specify the Minimum Detectable Effect (MDE) before running a power calculation. MDE should be the smallest effect the team would act on, not the smallest detectable effect.
- Cohen's h is the effect size for proportion comparisons. Report it alongside the percentage point difference.
- Use G*Power (proportions section) or R's `pwr::pwr.2p.test()` as alternatives.

### Survey Benchmarking (SUS, UMUX-Lite, CSAT)
- **Rough minimum**: 8 participants. Gives you a mean but confidence intervals are very wide. Do not use for any comparative or publication-level claim.
- **Reliable estimate**: 40+ participants. Suitable for internal benchmarking and trend monitoring.
- **Detecting meaningful differences against a norm**: 100+ participants. To detect a 5-point SUS difference from a known benchmark (e.g., 68-point average) at 80% power, you typically need ~140–160 participants (d ≈ 0.33, based on SD ≈ 15).
- **Comparing two groups on SUS**: use an independent t-test power calculation with d estimated from the expected mean difference and SD ≈ 15.

### Unmoderated Remote Usability (Task Completion Rate)
- **For stable proportion estimates**: 100–200 participants.
- At N=100, a Wilson CI on a 70% completion rate is approximately [60%, 79%] — adequate for most benchmarking decisions.
- At N=200, that CI narrows to [63%, 76%].
- If comparing task completion across two variants, treat as a two-proportion test and power-calculate accordingly.

### Existing UX-Specific Notes (retained)
- **Qualitative usability testing**: 5 participants per distinct user segment for problem discovery (Nielsen heuristic — not appropriate for quant inference).
- **SUS score comparison**: to detect a 5-point difference (SD ≈ 15), need ~144 per group (medium-small effect, d ≈ 0.33).
- **Task success rate**: to detect a 10% difference from 70% baseline at 80% power: ~190 per group.
- **Benchmark study (single group vs. known norm)**: one-sample t-test; medium effect needs ~34.

---

## Screener Design and Quota Sampling

A screener that is too loose recruits the wrong people. A screener that is too tight takes weeks to fill. Design it carefully at S3.

**What makes a screener effective:**
- Screening questions use behavioral or situational framings, not self-report labels (e.g., "How often do you use mobile banking apps?" not "Are you a frequent mobile banking user?").
- Use pipeline/funnel questions: broad qualifier first, specific disqualifier second. This reduces participant dropout mid-screener.
- Do not reveal the desired answer in the question or its response options. Motivated participants will pattern-match.
- Keep screeners under 5 minutes. Longer screeners reduce completion rates and introduce self-selection bias.

**Define quotas before recruiting:**
- Specify target N per segment (age band, platform, user type, tenure) in the S3 design document.
- Hard quotas: stop recruiting a cell once it is full.
- Soft quotas: track proportions and adjust mid-field if a cell is over- or under-represented.

**Over-recruit by 20–30%:**
- Account for disqualification (screener failures after intake), no-shows, incomplete sessions, and data quality removals (e.g., speeders, straight-liners in surveys).
- Example: if you need 100 completes, recruit for 130. For a panel study with anticipated 15% attrition, recruit for 120 to land at 100 usable.

---

## Response Rate Inflation for Surveys

Do not design a survey study assuming everyone you invite will respond. Plan your outreach to account for non-response.

- **Panel platforms** (Prolific, UserTesting, Respondent): completion rates are high (70–90%) because participants are opt-in and motivated by incentives. Still, build in 10–20% buffer.
- **Email/CRM outreach to customers**: typical response rates are 5–20%. For a target N of 200, plan to send to 1,000–4,000 contacts.
- **In-product intercepts**: conversion from intercept to completed survey is often 2–10%. High volume compensates; calculate expected completes from your DAU/WAU before committing to this method.
- **Rule of thumb**: plan to invite 3–5× the target N for any survey not on a panel platform. For panel platforms, 1.2–1.5× is usually sufficient.
- Always record the number invited and the number completed. Report response rate in the Method section.

---

## Subgroup Analysis Cell Size Guidance

Subgroup analyses are frequently requested by stakeholders ("break this out by user type") and frequently underpowered. Flag this early.

- **N ≥ 30 per cell** for parametric tests (t-test, ANOVA) — the Central Limit Theorem starts to hold, and means are reasonably stable.
- **N ≥ 20 per cell** for non-parametric tests (Mann-Whitney, Wilcoxon) — rank-based tests are more robust to small N but still need adequate power.
- **N < 20 per cell**: descriptive reporting only. Report means/proportions with wide CIs and explicitly note that inferential tests are underpowered. Do not report p-values as primary evidence.
- **Planned vs. exploratory subgroup analyses**: planned subgroup tests (specified at S4/S6) are held to the power standard. Exploratory subgroup analyses (identified post-hoc) require Bonferroni or FDR correction and must be labeled exploratory.
- **Interaction vs. simple effects**: if you want to claim that an A/B effect differs by subgroup (e.g., "the variant worked better for new users"), test the interaction term — do not just compare p-values across subgroups separately. The interaction test requires substantially larger N than the main effect test.

---

## Survey Weighting and Non-Representative Samples

### What Post-Stratification Weighting Corrects For

When your achieved sample differs from your target population on known demographic dimensions (age, platform, geography, product tenure, or other variables you can measure), post-stratification weighting adjusts the contribution of each respondent so that the weighted sample matches the target population's known distribution. For example, if your target population is 60% mobile users but your sample is 40% mobile, you upweight mobile respondents and downweight desktop respondents to restore the correct ratio.

### When Weighting Is Needed

Weighting is appropriate in any survey where:
- The recruited sample differs from the target population on age, platform, geography, product tenure, or other known distributional dimensions.
- You have reliable population data (e.g., from product analytics or a census) against which to weight.
- You are making a population-level claim (e.g., "the average SUS score across our user base is X").

Weighting is less important for within-study comparisons (A vs. B) where both groups were recruited from the same pool.

### How to Apply Weights in Python

```python
import numpy as np

# Post-stratification weighting example
# Population is 60% mobile, 40% desktop; sample is 40% mobile, 60% desktop
# Compute weights: population proportion / sample proportion
pop_proportions = {'mobile': 0.60, 'desktop': 0.40}
sample_proportions = {'mobile': 0.40, 'desktop': 0.60}

# For each respondent, assign their platform's weight
# weights['mobile'] = 0.60 / 0.40 = 1.5; weights['desktop'] = 0.40 / 0.60 = 0.667
weights = {k: pop_proportions[k] / sample_proportions[k] for k in pop_proportions}

# Apply to an array of scores; respondent_weights is an array of per-row weights
scores = np.array([...])          # SUS scores
respondent_weights = np.array([...])  # weight per respondent based on platform

weighted_mean = np.average(scores, weights=respondent_weights)
```

For weighted regression (adjusting for multiple demographic dimensions simultaneously), use `statsmodels` with the `freq_weights` or `var_weights` parameter in OLS, or use survey-weighted regression via `statsmodels.stats.weightstats`.

### What Weighting Cannot Fix

- **Non-response bias on unknown characteristics**: if respondents differ from non-respondents in ways you cannot measure (e.g., engagement level, frustration), weighting on demographics will not correct for this.
- **Systematic exclusion of a user segment**: if an entire group never appears in your sample (e.g., users in a particular region who were never invited), weighting cannot recover their perspective.
- **Low-quality responses**: weighting amplifies the contribution of certain respondents — if those respondents are low-effort or speeders, their noise gets amplified.

### Plain-Language Framing

"Weighting adjusts who counts more in your average — it does not fix a fundamentally unrepresentative sample."

### Practical Note on Panel Platforms

Panel platforms such as Prolific and UserTesting are convenience samples. Weighting by demographics helps ensure your weighted estimates reflect a target population's age/gender/geography distribution, but it cannot make a panel sample equivalent to a probability sample. After weighting, claims remain limited to "among people similar to our weighted sample" rather than true population-level inference. State this limitation explicitly in the Method section.

---

## Sampling Methods

### Probability Sampling (preferred for generalization)
- **Simple random**: each member of population has equal chance. Gold standard.
- **Stratified**: population divided into strata; random sample from each. More efficient when strata differ on outcome.
- **Cluster**: sample clusters (e.g., teams, schools), then sample within. Efficient but requires cluster-robust analysis.
- **Systematic**: every kth element. Acceptable if list has no periodic pattern.

**Important note for product UX research**: probability sampling requires a complete sampling frame — a list of every member of the target population. In practice, product UX researchers almost never have access to a complete sampling frame. True probability sampling is structurally unavailable for most product teams. The practical standard is purposive or panel sampling with transparent description of how the sample was recruited and explicit qualification of generalizability claims.

### Non-Probability Sampling (common in practice; limits generalization)
- **Convenience**: whoever is available. Fast; cannot generalize to a defined population without strong justification.
- **Purposive**: intentionally selected for specific characteristics.
- **Snowball**: participants recruit others. Common for hard-to-reach populations.
- **Panel/opt-in**: platform-recruited (Prolific, MTurk, UserTesting). Faster than random; must characterize sample demographics in report.

### Generalizability Rules
- Probability sample → can make population-level claims with stated confidence.
- Non-probability sample → describe sample characteristics; limit claims to "among people similar to our sample."
- Never describe a convenience sample as representative without justification.

## Attrition and Dropout
- Report attrition rates by condition.
- Test whether dropouts differ from completers on key baseline variables.
- Use intention-to-treat (ITT) analysis as primary; per-protocol as sensitivity.
- MCAR, MAR, MNAR: state the missingness assumption and justify it.
