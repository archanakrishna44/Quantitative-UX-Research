# Causal Inference

## When Is a Causal Claim Justified?

In UX quant work, almost always only when you ran a randomized A/B test.

If you did not randomize participants to conditions, you cannot make a causal claim. Full stop. Analytics data, survey data, tree test data, and unmoderated task data are all observational or quasi-experimental at best. They support associations, not causes. The rest of this file explains the rules, the one strong exception (the A/B test), and the rare advanced methods that exist for situations where randomization is impossible.

---

## A/B Test Causal Interpretation

A well-executed A/B test is the UX team's primary tool for justified causal claims. When the design supports it, state the conclusion directly.

### When the A/B test supports a causal claim:
- Participants were randomly assigned to control and variant.
- Assignment was at the user level (not session or device level, unless explicitly designed that way and you understand the implications).
- The sample ratio mismatch (SRM) check passes — see below.
- The test ran long enough to avoid novelty effects — typically 1–2 full business cycles (e.g., two weeks for a weekly-pattern product).
- No external events occurred mid-test that would differentially affect one group.

### How to state the causal conclusion correctly:
- "The redesigned checkout flow caused a 7 percentage point increase in purchase completion rate (95% CI [2pp, 12pp], p = .016)."
- "The change in primary navigation label caused a significant improvement in findability (tree test success rate increased from 61% to 79%, χ²(1) = 8.4, p = .004, h = 0.38)."
- The key words are "caused" and "increased/decreased/changed." These are appropriate only when the A/B test design is valid.

### Note on Continuous Monitoring and Always-Valid Inference

Traditional fixed-horizon A/B tests require committing to a sample size before launch; checking results before reaching that N inflates Type I error. Modern experimentation platforms (Statsig, Eppo, Amplitude Experiment) implement always-valid inference (AVI/mSPRT), which allows continuous monitoring without inflating false positive rates. When using these platforms, the "do not peek" rule does not apply — their built-in sequential testing is valid by design. See `04_statistical_methods.md` for a full explanation. If running an A/B test outside these platforms, the fixed-horizon rule still applies.

### What to say when SRM is detected:
- Sample Ratio Mismatch means the observed allocation between control and variant differs meaningfully from the intended ratio (e.g., you targeted 50/50 but got 55/45). SRM usually indicates a data pipeline problem, assignment bug, or session-level contamination.
- When SRM is detected: do not report causal results. Report: "SRM was detected (expected 50/50, observed [X/Y]). This test's causal validity is compromised. Results should be treated as exploratory. Recommend investigating the assignment mechanism before re-running."
- Check SRM with a Chi-square goodness-of-fit test on the allocation counts.

---

## SUTVA and Spillover: Limits on A/B Test Causal Claims

SUTVA (Stable Unit Treatment Value Assumption) states that one participant's treatment should not affect another participant's outcome. When SUTVA is violated, the A/B test's causal logic breaks down.

**Network effects**: if control and variant users interact with each other (e.g., a social feature, a marketplace), the variant's effect can spill over to the control group. This inflates or deflates the measured difference. Network A/B tests require specialized designs (cluster randomization, ego-network randomization).

**Shared sessions**: if the same user can appear in both control and variant (e.g., assignment is cookie-based and the user clears cookies), SUTVA is violated. Use user-ID-level assignment wherever possible.

**Novelty effects**: users in the variant group often respond to change itself, not to the design change. A new layout gets higher engagement for the first week simply because it is new. Run tests long enough (typically 2+ full business cycles) to let novelty effects decay before drawing conclusions.

**Hawthorne effects**: if users know they are being observed or tested, they may behave differently. In most product A/B tests this is not a concern (users are unaware of the test). In instrumented usability studies, it can be.

**How to flag these in reporting**: include a "Causal Assumptions" section in the analysis. Note which SUTVA conditions were checked and which are assumed but unverifiable.

---

## Analytics and Observational Data: Associational Language Only

Any finding from analytics data, behavioral logs, clickstream analysis, or funnel analysis is associational, not causal.

**Why**: in observational data, users self-select into behaviors. Users who reach the checkout page are different from users who do not. Users who use feature X are different from users who do not. These differences — not the feature or the page — may explain the outcome.

**Correct language for analytics findings:**
- "Users who completed onboarding were 2.3× more likely to return in the following week."
- "Funnel drop-off at step 3 was associated with longer time spent on step 2."
- "Users on mobile showed lower task completion rates in the app."

**Incorrect language for analytics findings:**
- "Completing onboarding caused higher retention." (You do not know this — users who complete onboarding may be inherently more motivated.)
- "The slow step 2 caused users to drop off." (You do not know this — maybe users who drop off arrived with lower intent.)
- "Mobile caused lower completion." (Mobile users are a different population.)

**The test**: can you imagine a confounding variable that would explain the relationship without any causal effect? If yes — and in analytics data, you almost always can — use associational language.

---

## The Core Problem (Causal Logic)

Correlation does not imply causation. To claim X causes Y, you need:
1. **Covariation**: X and Y are associated.
2. **Temporal precedence**: X precedes Y.
3. **Elimination of alternatives**: no plausible third variable explains the XY relationship.

Observational studies can satisfy 1 and 2 but struggle with 3. Experiments with random assignment address all three.

## Language Rules

| Situation | Correct Phrasing | Incorrect Phrasing |
|---|---|---|
| Valid A/B test result | "Variant B caused a 7pp increase in conversions." | "Variant B was associated with more conversions." (undersells the design) |
| Analytics finding | "Users who used feature X retained at higher rates." | "Feature X caused higher retention." |
| Survey correlation | "SUS score was correlated with task completion rate (r = .42)." | "Higher perceived usability led to better task performance." |
| Pre/post without control | "SUS scores increased from 68 to 74 after the redesign." | "The redesign caused a 6-point SUS improvement." |
| Observational regression | "Platform type predicted error rate (β = 0.34)." | "Platform type caused more errors." |

---

## DAGs (Directed Acyclic Graphs)

A DAG maps causal assumptions. Use it to identify:
- **Confounders**: common causes of X and Y → must be adjusted for.
- **Mediators**: variables on the causal path from X to Y → adjusting blocks the effect (usually do not adjust for mediators in a total-effect analysis).
- **Colliders**: common effects of X and Y → do NOT adjust for colliders (opens a spurious association).

Draw the DAG before collecting data. The DAG determines which covariates to include in regression.

## Mediation Analysis
- Tests whether X affects Y through a mediator M: X → M → Y.
- **Baron-Kenny steps**: largely superseded by bootstrapped indirect effects.
- **In Python**: use `pingouin.mediation_analysis()` which returns the indirect effect with bootstrapped CIs directly, or implement bootstrapped indirect effects manually using `statsmodels`. Example:
  ```python
  import pingouin as pg
  results = pg.mediation_analysis(data=df, x='IV', m='mediator', y='DV', n_boot=1000)
  # Returns direct, indirect, and total effects with bootstrapped CIs
  ```
- **In R**: the `mediation` package or `lavaan` for SEM-based approaches.
- Note: the PROCESS macro (Hayes) is an SPSS/SAS-specific tool and is not applicable to Python-based workflows.
- Report: indirect effect with 95% bootstrapped CI; if CI excludes 0, mediation is supported.
- Do NOT interpret mediation as causal without a strong design (ideally experimental manipulation of M).

## Moderation Analysis
- Tests whether the effect of X on Y differs by levels of a moderator W: X × W interaction.
- In regression: include X, W, and the X×W product term.
- If interaction is significant: probe simple slopes at levels of W (mean ± 1 SD, or meaningful subgroups).
- Report: the interaction term β, p, and simple slopes.

---

## Advanced Causal Methods — Rarely Applicable in UX Team Context

These methods exist for observational studies where randomization is impossible. They are included for completeness but are rarely the right tool for a design team's quant work. If a stakeholder requests one of these methods, confirm that a simpler design (an A/B test or a clearly framed observational analysis with associational language) would not address the question first.

### Interrupted Time Series (ITS)

**Most practically relevant quasi-experimental method for product analytics work.** When a feature rolls out to all users simultaneously — with no holdout group — a pre-post comparison is the only available design. ITS models this correctly.

**How ITS works**:
1. Fit a regression on pre-launch data to establish the baseline trend (level and slope over time).
2. Estimate the change in level (the immediate effect at the intervention point) and the change in slope (change in trajectory after the intervention).
3. The model accounts for autocorrelation in time series data — observations near in time are not independent, and standard regression ignores this.

**In Python**: use `statsmodels.tsa.stattools` for stationarity checks and fit the ITS model using OLS with appropriate lag structure, or segment regression via `statsmodels.formula.api`. In R, the `its.analysis` package handles ITS models directly.

**Key limitation**: ITS cannot rule out concurrent events as alternative explanations. Seasonality, other product changes launching simultaneously, or external events that happen to coincide with the intervention can produce the same pattern as a true treatment effect. Acknowledge this explicitly in the limitations section and document what concurrent events were checked and ruled out.

### Regression to the Mean in Pre-Post Designs

When participants are selected because they scored extreme — very low satisfaction, very high error rate, very poor task completion — subsequent measurements will tend toward the average regardless of any intervention. This is regression to the mean, a statistical artifact of selecting on extreme scores.

**Why it matters**: if you recruit users who are struggling (low SUS, frequent errors) and measure them again after an intervention, their scores will improve on average even if the intervention had zero effect. The selection criterion guarantees some reversion toward the mean.

**Mitigation**: use a control group (a group with equivalent pre-intervention scores who receive no treatment). The control group's score change from pre to post estimates how much improvement is due to regression to the mean alone; the treatment group's additional improvement above that baseline is the treatment effect.

**If no control group is available**: acknowledge regression to the mean explicitly as an alternative explanation in the limitations section. Do NOT present pre-post improvement as evidence of treatment efficacy in the absence of a control group.

### Difference-in-Differences (DiD)
- **When**: you have pre/post data for a treated and an untreated group.
- **Assumption**: parallel trends — treated and control groups would have followed the same trajectory absent treatment.
- **Estimate**: (Post_treated − Pre_treated) − (Post_control − Pre_control).

### Regression Discontinuity Design (RDD)
- **When**: treatment is assigned by a threshold on a continuous running variable (e.g., score above 70 gets intervention).
- **Assumption**: units just above and below the threshold are similar except for treatment.
- **Estimate**: the discontinuity in the outcome at the threshold.

### Instrumental Variables (IV)
- **When**: there is a variable (instrument) that affects X but has no direct effect on Y except through X, and is not related to confounders.
- **Hard to find a valid instrument** — requires strong justification.

### Propensity Score Methods
- **Propensity score**: probability of treatment given observed covariates.
- **Matching**: match treated and control units on propensity score; compare outcomes.
- **Weighting (IPW)**: weight observations by inverse of propensity score.
- **Limitation**: only controls for observed confounders. Unobserved confounders remain a threat.

### Sensitivity Analysis
- For any causal claim from observational data, ask: how strong would an unmeasured confounder need to be to explain away the result?
- Tools: E-value (VanderWeele & Ding), Rosenbaum bounds for matched studies.
- Always include a sensitivity analysis section when making causal claims from observational data.

---

## Common Causal Inference Mistakes
- Adjusting for a mediator when estimating the total effect of X on Y.
- Adjusting for a collider (introduces bias).
- Claiming causation from a cross-sectional correlation.
- Ignoring selection bias in convenience samples.
- Treating "controlling for" as synonymous with "removing confounding" — adjustment only removes confounding for measured variables.
- Using causal language for analytics findings ("the feature caused higher engagement").
- Failing to check SRM before reporting A/B test causal conclusions.
- Running a test too short and attributing novelty effects to the design change.
