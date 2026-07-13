---
scope: reference
modifies_workflow: false
---

# UX Research Methods — S3 Reference

This file supports the QRA's S3 method recommendation. Use it to match research goals to the right method, understand what data each method produces, and identify the appropriate statistical test. For statistical test details, see `04_statistical_methods.md`.

---

## Method Selection Matrix

Use this table as a first-pass lookup. Then read the full method entry for detail.

| Research Goal | Recommended Method | Data Type | Primary Stat Test |
|---|---|---|---|
| Validate IA / navigation structure | Tree Testing | Binary (success/fail), proportion (directness) | Wilson CI for proportions; Chi-square for group comparison |
| Identify where users first click / label clarity | First-Click Testing | Binary (hit/miss), continuous (time) | Wilson CI; one-sample proportion test vs. benchmark |
| Measure perceived usability / satisfaction | Survey Benchmarking (SUS, UMUX-Lite, SEQ) | Continuous (scaled scores) | One-sample t-test vs. norm; independent t-test for A vs. B |
| Compare two design variants at scale | A/B Testing | Binary or continuous outcome | Chi-square / Fisher's (binary); Welch's t-test (continuous) |
| Compare multiple element combinations | Multivariate Testing (MVT) | Binary or continuous outcome | Logistic regression; ANOVA with interaction terms |
| Understand how users naturally group content | Card Sorting (Open) | Agreement matrix, dendrogram | Cluster analysis; agreement ratio |
| Validate a proposed category structure | Card Sorting (Closed) | Placement accuracy (proportion) | Wilson CI; Chi-square vs. expected |
| Behavioral patterns at scale (funnels, retention) | Web & App Analytics | Count, rate, continuous | Funnel conversion tests; cohort analysis; regression |
| Screen and qualify participants | Participant Screener | Categorical (qualify/disqualify) | Frequency counts; quota tracking — no inferential test |
| Attitudinal baseline / prevalence estimates | Survey Benchmarking (custom scales) | Continuous or ordinal | One-sample t-test; Spearman correlation |

---

## 1. Participant Screeners

### What question it answers
"Are these the right people for the study?" A screener qualifies or disqualifies candidates before they enter any study. It also functions as a standalone instrument when the goal is to understand who your user population is demographically or behaviorally.

### What data it produces
- **Data type**: Categorical (qualify / disqualify flags), nominal and ordinal demographics, behavioral frequencies ("how often do you...").
- **Native metrics**: Quota fill rate per segment, screener pass rate, demographic distribution of qualified pool.
- **Output format**: Flat CSV with one row per respondent, pass/fail flag column, quota tracking spreadsheet.

### Typical sample size
- Send screeners to 5–10× your target study N to account for disqualification and dropout.
- For a 50-person survey, plan to screen 250–500 candidates.
- No minimum N for statistical inference — screeners are not inferential instruments.

### Key validity threats
- **Socially desirable responding**: participants guess the "right" answers to qualify.
- **Speeder/straight-liner responses**: use attention checks and trap questions.
- **Quota gaming**: if quotas are visible (some panels show them), participants may misrepresent to qualify.
- **Recruiter-introduced bias**: panel platforms oversample certain demographics; check representativeness.

### Statistical tests
Screeners do not require inferential tests. Use frequency counts and proportions to confirm quota fills. If comparing demographic composition across two pools, use Chi-square.

### Triangulation with qualitative
Screen participants for moderated sessions and unmoderated quant studies using the same criteria. Consistent screeners across studies let you compare findings across a stable population definition.

### Common misuses / when NOT to use
- Do NOT use screener data to draw conclusions about product experience — screeners measure who the person is, not how they behave with the product.
- Do NOT skip a screener for A/B tests or tree tests where population characteristics affect outcomes.

### Platforms / tools
Qualtrics, SurveyMonkey Audience, UserTesting panel, Respondent.io, Prolific, UserZoom, dscout.

---

## 2. Survey-Based Benchmarking

### What question it answers
"How do users feel about this product, task, or experience — and how does that compare to a standard or prior measurement?" Covers attitudinal data: perceived usability, satisfaction, task difficulty, Net Promoter, and custom scales.

### What data it produces
- **Data type**: Continuous (scaled scores after formula application), ordinal (raw Likert), binary (NPS detractor/promoter).
- **Native metrics**: SUS score (0–100), UMUX-Lite score (0–100 after conversion), SEQ score (1–7 per task), NPS (−100 to +100), custom scale composites.
- **Output format**: Survey export CSV; one row per respondent; columns for each item and computed composite scores.

### Typical sample size
- SUS / UMUX-Lite: minimum 8 for a rough estimate; 20–30 for stable estimates; 40+ for reliable detection of a meaningful difference vs. a benchmark (see `02_sampling_and_power.md`).
- SEQ (per task): 20–40 participants per task; more if comparing across task groups.
- NPS: 200+ to produce stable scores; unreliable at small N.
- Custom Likert scales: 100+ for scale validation (factor analysis); 30–50 for benchmarking if Cronbach's α is pre-established.
- Published norm (Sauro): SUS requires n ≥ 12 for a meaningful one-sample comparison.

### Key validity threats
- **Response bias**: acquiescence (tendency to agree), extreme responding, social desirability. Mitigate with reverse-scored items.
- **Order effects**: survey fatigue inflates negative ratings late in a long survey. Put benchmark scales immediately after the relevant tasks.
- **Construct validity**: SUS and UMUX-Lite measure perceived usability, not actual usability. Do not substitute for behavioral data.
- **Timing**: post-task SEQ should be administered immediately after each task, not at end of study.

### Statistical tests
- **One sample vs. norm**: one-sample t-test (SUS mean vs. 68; SEQ mean vs. 5.5). Report t, df, p, Cohen's d, 95% CI.
- **Two independent groups (A vs. B)**: Welch's independent samples t-test.
- **Pre-post within same group**: paired t-test.
- **Ordinal / non-normal**: Mann-Whitney U (two groups) or Wilcoxon signed-rank (paired). Use if N < 20 and distribution is unknown.
- **Correlation with behavioral metrics**: Spearman's ρ (SUS vs. task completion rate, for example).

See `04_statistical_methods.md` for full test guidance.

### Triangulation with qualitative
Survey scales tell you the size of a satisfaction problem. Moderated sessions tell you why. A typical sequence: run a benchmark survey → identify low-scoring tasks or dimensions → use those as focus areas for follow-up moderated sessions. Alternatively, survey items can be designed to probe themes surfaced in prior discovery interviews.

### Common misuses / when NOT to use
- Do NOT use NPS as a primary UX outcome metric. It is ordinal, non-normal, and highly sensitive to context effects (see `10_ux_metrics_and_benchmarking.md`).
- Do NOT administer SUS without a defined product or prototype to evaluate. SUS is not a general brand or concept measure.
- Do NOT mix SUS items with unrelated scale items between items 1 and 10 — the ten items must be presented as a block.
- Do NOT use single-item custom scales as a reliability-tested substitute for SUS unless you have validated them for your context.

### Platforms / tools
Qualtrics, SurveyMonkey, Typeform, Google Forms (for simple use), UserZoom (integrated with usability sessions), Maze (post-task SEQ natively), UserTesting (post-task surveys), Medallia.

---

## 3. A/B Testing

### What question it answers
"Which of two variants performs better on a defined metric?" A/B testing randomly assigns users to two experiences (A = control, B = treatment) and measures whether the treatment causes a meaningful difference in a target outcome.

### What data it produces
- **Binary outcomes**: conversion rate, task completion rate, click-through rate. One row per user with a 0/1 flag.
- **Continuous outcomes**: time on task, revenue per session, scroll depth, engagement score. One row per user with a numeric value.
- **Output format**: event-log CSV or database export; typically rows = sessions or users; columns = variant assignment + outcome variables.

### Typical sample size
- Determined entirely by a priori power analysis. Do not start a test without calculating required N.
- Rule of thumb for binary outcomes: detecting a 5 percentage-point lift from a 50% baseline at α = 0.05, power = 0.80 requires approximately 800 users per arm (1,600 total).
- For continuous outcomes, use Cohen's d and a two-sample t-test power calculation.
- Do NOT peek and stop early (increases false positive rate). Use a pre-specified stopping rule or sequential testing correction (e.g., O'Brien-Fleming).

### Key validity threats
- **Novelty effect**: users behave differently with a new design simply because it is new. Run tests long enough to let novelty wear off (typically 1–2 full business cycles).
- **Sample Ratio Mismatch (SRM)**: if actual traffic split deviates from intended split, the randomization is compromised. Always check SRM before reporting.
- **Interference / SUTVA violations**: network effects, shared sessions, or cannibalization across variants contaminate estimates.
- **Multiple testing**: testing many metrics simultaneously inflates false positive rate. Pre-specify one primary metric; apply Bonferroni or Holm-Bonferroni to secondary metrics.
- **Selection bias**: if randomization happens post-action (e.g., only logged-in users), results don't generalize to all users.

### Statistical tests
- **Binary outcome**: Chi-square test (or Fisher's exact if expected cell count < 5). Report Cohen's h and 95% CI for the difference in proportions. Effect size: Cohen's h = 2 × arcsin(√p1) − 2 × arcsin(√p2). Benchmarks: h = 0.20 small, 0.50 medium, 0.80 large. For a 2×2 contingency table, Cohen's h is the appropriate effect size for proportion comparisons — not Cramér's V, which is used for multi-cell contingency tables with no inherent directionality.
- **Continuous outcome**: Welch's independent samples t-test. Report Cohen's d and 95% CI for the mean difference. If distribution is heavily skewed (e.g., revenue), consider Mann-Whitney U or a log transform.
- **Logistic regression**: use when you need to adjust for covariates (device type, prior behavior) or when simple proportions oversimplify the outcome.

See `04_statistical_methods.md` for test details.

### Triangulation with qualitative
A/B tests tell you that B performs differently; they almost never tell you why. Pair with post-test survey items (e.g., SEQ, open-text feedback) or follow-up moderated sessions targeting the winning variant's friction points. Analytics can reveal which user segments drove the result.

### Modern Experimentation Platforms and Always-Valid Inference

Statsig, Eppo, and Amplitude Experiment implement always-valid inference (AVI) — specifically mSPRT (mixture Sequential Probability Ratio Test) — which allows continuous monitoring of A/B results without inflating Type I error. When using these platforms, continuous monitoring is valid by design and the traditional "do not peek" rule does not apply. The statistical guarantee is maintained regardless of when you check results.

For teams running A/B tests outside these platforms (manual Chi-square on a spreadsheet, custom Python scripts without sequential correction): the traditional fixed-horizon rule still applies. Commit to your sample size N before launch and do not check results until the target N is reached.

### Common misuses / when NOT to use
- Do NOT run an A/B test when you cannot randomize (e.g., you can only serve one variant at a time, before/after). Use an interrupted time-series or quasi-experimental design instead.
- Do NOT test cosmetic differences so small that you have no theory for why they would produce a behavioral difference.
- Do NOT use A/B testing as a substitute for formative design evaluation. A/B tests confirm; they don't discover.
- Do NOT stop a test as soon as p < 0.05 is reached when using a fixed-horizon design outside an AVI platform — this is p-hacking by peeking.

### Platforms / tools
- **Statsig, Eppo, Amplitude Experiment**: primary platforms used at product companies for server-side and client-side A/B testing with built-in always-valid inference (AVI/mSPRT). Continuous monitoring is valid by design on these platforms.
- **Optimizely and VWO (Visual Website Optimizer)**: for web-layer experimentation where a visual editor or DOM-level injection is needed.
- **LaunchDarkly**: feature flag management integrated with experimentation; supports gradual rollouts and targeted flag exposure.
- **Note**: GA4 (Google Analytics 4) does not have native A/B testing capability — a separate experimentation layer is required. Google Optimize is sunset and should not be used.

---

## 4. Multivariate Testing (MVT)

### What question it answers
"Which combination of multiple simultaneously-varied elements produces the best outcome?" MVT tests all combinations of changes (e.g., headline × hero image × CTA button) in a single experiment.

### What data it produces
Same format as A/B testing: one row per user, variant assignment (as a multi-factor combination code), and outcome variable(s).

### Typical sample size
MVT is traffic-hungry. A full factorial design with 3 elements × 2 variants each = 8 cells. To detect a 5-point conversion lift per cell at adequate power, you need the same per-cell N as an A/B test — so 8× the traffic of a single A/B test. Fractional factorial designs reduce this requirement but limit which interactions can be estimated.

Rule: if you cannot fill each cell with at least 200–300 users in a reasonable time window, run sequential A/B tests instead.

### Key validity threats
All threats from A/B testing apply, plus:
- **Interaction effects**: if elements interact (e.g., headline A works better with image B but not C), main-effects-only analysis will miss this. Model interactions explicitly.
- **Cell imbalance**: traffic spikes or technical errors can leave some combinations under-sampled. Check cell N before analysis.
- **Interpretation complexity**: stakeholders struggle to act on interaction findings. Plan your presentation before running.

### Statistical tests
- **ANOVA with interaction terms** (if continuous outcome): report main effects and interaction F-statistics, η² per factor, post-hoc comparisons with correction.
- **Logistic regression with interaction terms** (if binary outcome): report ORs with 95% CIs for each factor and interaction.
- Pre-specify whether you are testing main effects only or main effects + interactions.

See `04_statistical_methods.md` for ANOVA and logistic regression guidance.

### MVT vs. A/B: decision rule

| Condition | Use A/B | Use MVT |
|---|---|---|
| Testing one change at a time | Yes | No |
| Enough traffic to power all cells | No | Yes |
| Interaction effects are scientifically important | No | Yes |
| Team wants a clear "winner" quickly | Yes | No |
| Multiple changes need to ship together | Maybe | Yes |

### Common misuses / when NOT to use
- Do NOT run MVT on low-traffic pages or apps — you will never reach statistical power per cell.
- Do NOT use MVT when you have no a priori theory about why any of the elements matter.
- Do NOT report "the winning combination" without checking whether interactions were significant — the best combination in isolation may not be the best in combination.

### Platforms / tools
Same as A/B: Optimizely, VWO, Adobe Target, Statsig.

---

## 5. Tree Testing

### What question it answers
"Can users find what they're looking for in this navigation structure?" Tree testing isolates the information architecture (IA) by stripping away visual design and asking users to locate targets within a text-based hierarchy.

### What data it produces
- **Data type**: Binary (correct/incorrect final destination), proportion (directness score).
- **Native metrics**:
  - **Success rate**: proportion of participants who reached the correct destination. This is the primary metric.
  - **Directness score**: proportion of participants who reached the correct destination without any backtracking.
  - **Time on task**: time to reach a final destination (right-skewed; treat as secondary).
  - **First-click data**: which node participants chose first for a given task.
- **Output format**: Platform export CSV; one row per participant per task; columns for first click, final destination, success flag, directness flag, time.

### Typical sample size
- Optimal Workshop published norms: 50 participants per tree test study is the widely cited minimum for stable estimates.
- For subgroup comparisons (e.g., two user segments), plan 50 per group.
- For formative IA work (iterating on a tree), 20–30 per round is acceptable.

### Key validity threats
- **Stripping visual context**: users in a real product have visual affordances (icons, hierarchy, color) that aid navigation. Tree test results may underestimate real-world findability.
- **Task wording bias**: if task wording matches a label in the tree, participants follow the matching text rather than genuine mental models. Use goal-oriented task wording, not label-echoing wording.
- **Artificial linearity**: participants can only move forward and backward in the hierarchy — this removes spatial and cross-link navigation patterns present in real products.
- **Satisficing**: participants may stop at a plausible but incorrect node. Success/fail definitions must be pre-specified.

### Statistical tests
- **Success rate (primary)**: Wilson confidence interval (not normal approximation). This is the correct method for proportions from small-to-moderate N. Report point estimate + 95% Wilson CI.
- **Directness score**: Wilson CI.
- **Comparing two trees or two groups**: Chi-square test for each task (success rates). Apply Holm-Bonferroni correction across tasks.
- **Time on task**: median + IQR; if comparing groups, Mann-Whitney U (right-skewed distribution).

See `10_ux_metrics_and_benchmarking.md` for Wilson CI formula and directness interpretation thresholds.

### Interpreting success + directness together

| Success Rate | Directness Score | Interpretation |
|---|---|---|
| High | High | Destination is easy to find; structure is clear |
| High | Low | Users eventually find it but struggle — the path is confusing even if the destination is correct |
| Low | High | Users go confidently to the wrong place — a label or category name is misleading |
| Low | Low | Users are lost — the IA structure is fundamentally misaligned with mental models |

### Triangulation with qualitative
Tree test data shows what happened; card sorting (open) shows why categories are grouped the way they are in users' minds. Typical sequence: open card sort to understand mental models → design tree from those groupings → tree test to validate the structure. Follow-up moderated sessions can probe the specific failure nodes identified in tree test results.

### Common misuses / when NOT to use
- Do NOT use tree testing as a replacement for card sorting. Tree testing validates a proposed structure; card sorting generates one.
- Do NOT tree test a structure that hasn't been informed by any user research — you'll just confirm a bad IA is bad.
- Do NOT test a tree with more than 4–5 levels of depth without splitting into focused subtrees; deep trees produce fatigue and unreliable data.

### Platforms / tools
Optimal Workshop (Treejack) — industry standard. UserZoom, Maze (limited tree test support), UXtweak.

---

## 6. First-Click Testing

### What question it answers
"Where do users click first when trying to complete a task, and does that first click predict success?" Users who make a correct first click complete tasks ~87% of the time; users who make an incorrect first click complete the same tasks only ~24% of the time (Spool, UIE Research) — a 3.6x difference. First-click testing is the most efficient method for evaluating navigation and label clarity.

### What data it produces
- **Data type**: Binary (correct/incorrect target zone), continuous (time to first click).
- **Native metrics**:
  - **First-click accuracy**: proportion of participants clicking within the pre-defined correct target zone.
  - **Time-to-first-click**: time from image display to first click (right-skewed).
  - **Click heatmap**: visual distribution of clicks across the interface screenshot.
- **Output format**: Platform export CSV with coordinates, zone label, hit/miss flag, and time per participant per task. Heatmap as PNG.

### Typical sample size
- 20–40 participants per task for stable first-click accuracy estimates.
- If testing multiple tasks in one session, 40–50 is recommended.
- Norms from Optimal Workshop and Chalkmark: 40 participants considered a reliable benchmark.

### Key validity threats
- **Static images vs. live interface**: participants interact with screenshots, not clickable prototypes. Dynamic navigation behaviors (hover states, animations) are not captured.
- **Target zone definition subjectivity**: if target zones overlap or are ambiguously defined, hit/miss scoring is unreliable. Define zones a priori before data collection, not after seeing results.
- **Task wording**: same bias as tree testing — echoing interface labels in task wording inflates accuracy.
- **Screen size / device**: click coordinates on mobile vs. desktop may not be comparable. Stratify by device if mixed.

### Statistical tests
- **First-click accuracy (primary)**: Wilson confidence interval.
- **Comparing two designs or groups**: Chi-square for each task. Apply Holm-Bonferroni correction across tasks.
- **Time-to-first-click**: median + IQR; Mann-Whitney U for group comparison.
- **One sample vs. benchmark**: one-sample proportion test (z-test for proportion) vs. a pre-specified benchmark rate (e.g., "at least 70% should land on the correct zone").

See `04_statistical_methods.md` for proportion tests and `10_ux_metrics_and_benchmarking.md` for benchmark-setting guidance.

### Triangulation with qualitative
First-click accuracy shows which design elements confuse users; it cannot explain why. Follow up low-accuracy tasks in moderated sessions asking participants to think aloud about what they expected to find and why they clicked where they did. This combination is highly efficient for label and navigation iteration.

### Common misuses / when NOT to use
- Do NOT use first-click testing to evaluate complex multi-step workflows — it only captures the first decision point.
- Do NOT interpret a high first-click accuracy alone as proof of usability. A correct first click is necessary but not sufficient for task completion.
- Do NOT define target zones post-hoc by looking at the click heatmap — this is equivalent to HARKing.

### Platforms / tools
Optimal Workshop (Chalkmark) — standard. Maze, UserZoom, Lyssna (formerly UsabilityHub), UXtweak.

---

## 7. Card Sorting — Open and Closed

### What question it answers
- **Open card sort**: "How do users naturally group and label this content?" Generates IA hypotheses from users' mental models.
- **Closed card sort**: "Does the proposed category structure match how users expect content to be organized?" Validates an existing or proposed IA.

### What data it produces

**Open card sort:**
- **Data type**: Categorical group assignments per card, free-text group labels.
- **Native metrics**:
  - **Agreement ratio** per card-pair (proportion of participants who placed two cards in the same group).
  - **Similarity matrix**: N × N matrix of agreement ratios across all card pairs.
  - **Dendrogram**: hierarchical cluster analysis output showing natural groupings.
  - **Label frequency**: how participants named their groups.
- **Output format**: Similarity matrix CSV, dendrogram PNG, group-label frequency table.

**Closed card sort:**
- **Data type**: Binary placement (correct/incorrect category per card), proportion.
- **Native metrics**:
  - **Placement accuracy per card**: proportion placing each card in the expected category.
  - **Standardization matrix**: for each card, distribution of placements across all categories.
- **Output format**: Placement CSV with one row per participant per card, category chosen, hit/miss flag.

### Typical sample size
- Open card sort: 15–20 participants is widely cited (Nielsen Norman Group; Optimal Workshop) as sufficient to reveal dominant groupings. Diminishing returns beyond 30.
- Closed card sort: 20–30 participants for stable placement proportions.
- If comparing two user segments, 15–20 per segment.

### Key validity threats
- **Card set design**: too many cards (> 40–50) causes fatigue and artificial groupings. Group or hierarchy cards in rounds if the content set is large.
- **Label ambiguity in closed sort**: if category labels are unclear, participants choose randomly rather than by mental model. Pre-test labels.
- **Participant expertise**: domain novices and experts produce different sort patterns. Segment if mixing expertise levels.
- **Forced categorization**: closed sort forces a choice even when a participant has no strong opinion. Treat near-random placement distributions as a signal of ambiguity.

### Statistical tests

**Open card sort:**
- **Dendrogram reading**: set a similarity threshold (typically 40–60% agreement) to define cluster boundaries. Document the threshold a priori.
- **Cluster analysis**: hierarchical clustering (Ward's method or average linkage) on the similarity matrix. Output is the dendrogram.
- **Agreement ratio**: report as proportion + Wilson CI for each card-pair of interest.

**Closed card sort:**
- **Placement accuracy**: Wilson CI per card.
- **Chi-square goodness-of-fit**: test whether placements across categories differ from uniform (random) distribution, per card.
- **Expected placement accuracy benchmark**: pre-specify a minimum acceptable placement rate (e.g., ≥ 70% correct). Use one-sample proportion test.

See `04_statistical_methods.md` for Chi-square and proportion tests.

### Triangulation with qualitative
Card sorting is inherently a mixed-methods instrument. Open card sorts are commonly run alongside a think-aloud protocol in moderated sessions to capture reasoning (not just grouping behavior). Remote unmoderated card sorts produce the quantitative patterns; moderated sessions explain the why behind surprising groupings. Typical combined workflow: unmoderated open sort (n=20) → qualitative moderated sessions (n=5) focused on the most ambiguous groupings → closed sort to validate the refined structure.

### Common misuses / when NOT to use
- Do NOT use an open card sort as a substitute for tree testing. Card sorting generates structure; tree testing validates it.
- Do NOT interpret a dendrogram without a pre-specified similarity threshold — the same data can produce very different "natural groupings" depending on where you cut the tree.
- Do NOT run a closed card sort on a structure that was never informed by user data — you'll just confirm your own assumptions.
- Do NOT include more than 40 cards in a single sort without a moderation strategy; fatigue-driven sorts are noise, not signal.

### Platforms / tools
- **Optimal Workshop (OptimalSort)**: industry standard for open and closed card sorts. Produces similarity matrices, dendrograms, and standardization matrices natively.
- **UXtweak and Maze**: strong alternatives with integrated study-building and analysis.
- **Lyssna (formerly UsabilityHub)**: lightweight card sorts integrated with other unmoderated methods (first-click, preference tests).
- **Qualtrics**: supports custom card sort implementations for teams already on the platform, though without native dendrogram output.

---

## 8. Web and App Analytics

### What question it answers
"What are users actually doing in the product at scale?" Analytics provides behavioral data from real users in real contexts — not a controlled study environment. It answers prevalence, sequencing, and retention questions that no controlled study can answer at comparable scale.

### What data it produces
- **Data type**: Count, rate (proportion), continuous (session duration, scroll depth), time-to-event (retention curves).
- **Native metrics**:
  - **Funnel conversion rate**: proportion of users who complete each step in a defined sequence.
  - **Drop-off rate**: proportion who exit at each funnel step.
  - **Retention rate**: proportion of users who return after a defined interval (Day 1, Day 7, Day 30).
  - **Engagement metrics**: DAU/MAU ratio, session length, feature activation rate, pages per session.
  - **Error events**: server-side or client-side error event counts per session.
  - **Heatmaps / session recordings**: click density and scroll depth overlays (qualitative-adjacent).
- **Output format**: Dashboard exports, event-log CSVs, cohort analysis tables, funnel visualization outputs.

### Typical sample size
Analytics is generally not sample-limited — you work with whatever traffic your product generates. The relevant question is whether the data covers a representative time window (avoid holiday seasons, marketing spikes, or major product releases in the measurement period unless that context is the research question).

### Key validity threats
- **Confounding**: analytics cannot establish causation. A drop in funnel conversion rate after a redesign could reflect the design change, a concurrent marketing shift, a technical bug, or seasonal variation. Causation requires an A/B test or a quasi-experimental design (see `05_causal_inference.md`).
- **Instrumentation errors**: events that fire incorrectly, double-fire, or don't fire produce corrupt data. Validate your tracking implementation before drawing conclusions.
- **Cohort composition drift**: user populations shift over time. Comparing this month's retention to last year's may be comparing different populations.
- **Survivorship bias**: users who reach later funnel steps are not representative of users who entered the funnel.
- **Definition inconsistency**: "session," "active user," and "conversion" are often defined differently across tools. Always document the exact definition used.
- **Privacy / consent gaps**: cookie consent and ad-blocking can differentially remove certain user segments, skewing behavioral data (see `07_ethics_and_privacy.md`).

### When analytics replaces a controlled study — and when it doesn't

| Analytics is sufficient when... | A controlled study is still needed when... |
|---|---|
| You need prevalence at scale (e.g., what % of users reach checkout) | You need to know if a design change caused a behavioral shift |
| You need sequencing data (what do users do before drop-off) | You need to understand why users are dropping off |
| You are monitoring a product health metric over time | You are evaluating a new design before launch |
| You need to identify which user segments behave differently | You need to attribute behavior to a specific design element |

### Statistical tests
- **Funnel step comparison**: Chi-square for conversion rate differences across cohorts or segments.
- **Retention curves**: Kaplan-Meier survival analysis; log-rank test for group comparisons.
- **Engagement metrics (continuous)**: Welch's t-test or Mann-Whitney U for group comparisons.
- **Regression on behavioral outcomes**: logistic regression (binary retention), Poisson/negative binomial (count outcomes), OLS (continuous engagement).
- **Time series**: interrupted time series analysis for pre/post comparisons without randomization (see `05_causal_inference.md`).

See `04_statistical_methods.md` for test details.

### Triangulation with qualitative
Analytics surfaces the what and where of behavioral problems. Moderated sessions, diary studies, and contextual inquiry surface the why. A high-value workflow: identify a drop-off anomaly in analytics → design a moderated session specifically targeting that step → surface the mental model or usability failure driving the drop → A/B test the fix using analytics as the measurement layer.

### Common misuses / when NOT to use
- Do NOT claim a design change caused a metric shift if the change was not randomized. Report it as "associated with" or use a pre-registered quasi-experimental design.
- Do NOT compare funnel conversion rates across time periods with different traffic composition, feature state, or tracking implementation without adjusting for those differences.
- Do NOT use session recordings or heatmaps as quantitative evidence — treat them as hypothesis-generating (qualitative-adjacent) tools, not confirmatory metrics.
- Do NOT ignore instrumentation validation. Analytics findings are only as trustworthy as your event schema.

### Platforms / tools
Google Analytics 4 (GA4), Amplitude, Mixpanel, Heap, FullStory (behavioral + session recording), Hotjar (heatmaps + session recordings), Looker / Tableau (visualization), BigQuery / Snowflake (raw event data), Segment (data pipeline).

---

## 9. Eye Tracking

### What question it answers
"Where do users look on this interface, and what draws or fails to draw their visual attention?" Eye tracking measures the gaze behavior of participants interacting with a UI, revealing attention patterns, reading order, and areas of visual confusion.

### What data it produces
- **Fixation count per AOI (Area of Interest)**: how many times participants fixated on a defined region. Higher fixation count on a CTA may indicate attention or confusion.
- **Fixation duration per AOI**: total time spent fixating on a region. Long fixation duration on an error message may indicate reading difficulty; long duration on a navigation element may indicate confusion.
- **Time-to-first-fixation on an AOI**: how quickly participants' gaze reached a defined region. A key metric for attention and visual hierarchy validation.
- **Saccade patterns**: the movement paths between fixations. Long saccades indicate scanning; short saccades indicate local processing.
- **Gaze heatmaps**: aggregate visualization of fixation density across the interface. The primary output for communicating results to design teams.

### When to use
- Validating visual hierarchy (e.g., does the primary CTA attract attention before secondary elements?).
- Studying reading patterns on text-heavy pages.
- Detecting banner blindness (users systematically ignoring ad-adjacent or styled elements).
- Comparing attention to key interface elements across two design variants.
- Studying cognitive load through fixation duration patterns.

### Typical N
30+ participants for reliable aggregate heatmaps. Below N=20, gaze heatmaps are highly influenced by individual variation. For group comparisons (e.g., two design variants), apply standard power analysis to the primary fixation metric.

### Validity threats
- **Calibration accuracy**: poor calibration (gaze not accurately tracked to screen position) introduces systematic noise. Validate calibration at the start of each session.
- **Lab vs. real environment**: participants in a lab setting may behave differently than in their natural context. Eye tracking in the wild (via remote webcam-based tools) reduces ecological validity concerns but reduces calibration accuracy.
- **Participant fatigue**: prolonged eye tracking sessions are fatiguing; plan sessions under 45 minutes.
- **AOI definition subjectivity**: AOIs must be defined a priori before data collection. Post-hoc AOI drawing around fixation clusters is hypothesis-after-results.

### Platforms / tools
- **Tobii Pro**: hardware-based; high accuracy; lab setting.
- **iMotions**: multi-sensor platform integrating eye tracking with other biometrics.
- **Sticky (RealEye, Lumen Research)**: remote webcam-based eye tracking approximations — lower accuracy than hardware but enables large unmoderated samples. Appropriate for heatmap-level insights, not precise fixation timing.

### Key limitation
Eye tracking shows where users look, not what they understand or decide. A fixation on the correct button does not mean the user understood its purpose. Always pair eye tracking with behavioral outcomes (task completion, first-click accuracy) and qualitative probing to interpret gaze patterns.

### Statistical analysis
- **Fixation counts per AOI**: Poisson regression (count outcome) or Mann-Whitney U for non-parametric group comparison.
- **Fixation duration**: right-skewed; log-transform before parametric tests; Mann-Whitney U as non-parametric alternative.
- **Time-to-first-fixation**: survival analysis (event = first fixation on AOI) with Kaplan-Meier and log-rank test for group comparison; or Mann-Whitney U for simple group comparison.

---

## 10. MaxDiff (Maximum Difference Scaling)

### What question it answers
"Which of these items are most and least important/preferred?" MaxDiff produces a ranked importance or preference scale among a set of items, with genuine discrimination between items. It is the best method when you need to prioritize features, messages, value propositions, or attributes and Likert scales produce inflated scores across all items.

### What data it produces
- **Utility/importance scores**: a probability score (0–1) for each item representing its relative importance. Scores sum to 1 across all items, enabling direct proportional comparison.
- **Item ranking**: items ordered by utility score. The distance between scores reflects the magnitude of preference differences.
- **Output format**: utility score per item per respondent (from the multinomial logit model) aggregated to group-level means for reporting.

### When to use MaxDiff over Likert
- When Likert scales produce inflated scores across all items and you need genuine discrimination (e.g., every feature scores 4.2–4.5 out of 5 and you still need to prioritize).
- When you need to rank items for resource allocation decisions — MaxDiff produces rankings with relative importance weights, not just ordinal rankings.
- When the number of items to evaluate exceeds what participants can meaningfully rate simultaneously (MaxDiff can handle 10–40+ items by presenting small subsets).

### How it works
Participants see subsets of items (typically 3–5 at a time) and select the "best" and "worst" from each set. The design ensures each item appears across multiple sets, and each participant evaluates a balanced subset of all combinations. Responses are analyzed using a multinomial logit model to produce utility scores — the best-worst choices reveal the relative distance between items more precisely than direct ratings.

### Typical N
150–300 participants for stable utility score estimates. Fewer participants produce wider uncertainty around item rankings, particularly for items with similar utility scores.

### Platforms / tools
- **Qualtrics**: built-in MaxDiff module handles design generation and analysis natively. Most accessible for teams already on Qualtrics.
- **Sawtooth Software**: the research standard for conjoint and MaxDiff; more configurable but requires more setup.
- **1000minds**: web-based administration of paired comparison tasks; outputs importance scores.

### Output and reporting
Report utility scores as percentages (probabilities) that sum to 100% across all items. Visualize as a ranked horizontal bar chart with uncertainty bands. Items close together in utility score require larger N to distinguish reliably — note this for stakeholders.

---

## 11. Diary Studies (Quantitative Component)

### What question it answers
"How do users' behaviors, experiences, and context change over time in naturalistic settings?" Diary studies capture longitudinal behavioral data in real-world contexts that no lab study can replicate — frequency of behavior, triggers, emotional states, and context of use across days or weeks.

### What data it produces (quantitative component)
- **Frequency of behavior**: count of incidents per day or per time period (e.g., number of times a user encountered an error, used a workaround, or completed a specific task).
- **Incident counts by type**: structured taxonomies of events participants self-report.
- **Self-reported ratings over time**: satisfaction, frustration, or effort ratings collected at each diary entry — producing a longitudinal series of attitudinal measures.
- **Context of use patterns**: structured fields for location, device, situation — enabling analysis of behavioral patterns by context.
- **Output format**: one row per diary entry; columns for participant ID, entry date/time, rating items, structured categorical fields, and any free-text open-ended fields (analyzed separately as qual).

### Study entry design for quantitative analysis
- Use closed-ended prompts, rating scales, binary indicators, and structured categorical fields that produce directly analyzable data. Open-ended prompts produce qual data and require separate analysis.
- Example structured entry: "Did you encounter an error today? (Yes/No)" + "If yes, how severe was it? (1–5 scale)" + "What context were you in? (Work/Personal/Travel)".
- Minimize entry burden — longer entries reduce compliance. Target 2–5 minutes per entry.

### ESM vs. Traditional Diary Studies
- **Experience Sampling Method (ESM)**: uses random or event-triggered prompts delivered in-the-moment (e.g., via mobile app notification). Captures experience at the moment of occurrence, reducing retrospective recall bias. Better for capturing emotional states and context accurately.
- **Traditional diary studies**: participants complete entries at pre-specified times (end of day, after a task). Slightly more retrospective but easier to comply with for low-frequency behaviors.
- ESM reduces retrospective bias but increases participant burden and attrition.

### Managing compliance and attrition
- Compliance rates in diary studies typically range from 60–80% of expected entries. Design the analysis plan assuming 20–30% missing entries.
- Attrition (participants who drop out entirely before study end) requires intention-to-treat (ITT) analysis as the primary approach — analyze all enrolled participants, treating dropout as a missing data event, not simply excluding them.
- Test whether dropout participants differ from completers on baseline characteristics before assuming data is missing at random (MAR).

### Statistical approaches
- **Longitudinal mixed-effects models**: the appropriate primary analysis for repeated measures with variable compliance. Fixed effects capture the average trajectory; random effects account for individual differences in baseline and rate of change. Use `statsmodels.formula.api` (`mixedlm`) or `lme4` in R.
- **ICC (Intraclass Correlation Coefficient)**: assess within-person vs. between-person variance. A high ICC (> 0.50) indicates that most variance is between people (stable individual differences); a low ICC indicates that most variance is within people over time (change is the signal).
- **Compliance tracking**: report completion rates by day and by participant. Visualize the compliance pattern — compliance that degrades over time suggests participant fatigue and must be acknowledged in the limitations.

---

## Quick Reference: Method × Key Threats × Primary Stats

| Method | Top 2 Validity Threats | Primary Stat for Main Metric |
|---|---|---|
| Participant Screener | Social desirability; panel composition bias | Frequency counts; Chi-square for quota comparison |
| Survey Benchmarking | Response bias; construct validity of self-report | One-sample t-test vs. norm; Welch's t-test A vs. B |
| A/B Testing | Novelty effect; peeking outside AVI platforms | Chi-square (binary); Welch's t-test (continuous) |
| MVT | Traffic starvation; interaction effects missed | ANOVA with interactions; logistic regression |
| Tree Testing | Task wording bias; visual context stripped | Wilson CI; Chi-square across groups |
| First-Click Testing | Target zone defined post-hoc; static image limitation | Wilson CI; one-sample proportion test |
| Card Sort (Open) | Card set fatigue; threshold set post-hoc | Agreement ratio + Wilson CI; dendrogram / cluster |
| Card Sort (Closed) | Forced choice with no opinion; label ambiguity | Wilson CI per card; Chi-square goodness-of-fit |
| Web & App Analytics | Confounding; instrumentation error | Chi-square (funnel); Kaplan-Meier (retention) |
| Eye Tracking | Calibration accuracy; AOI defined post-hoc | Poisson regression or Mann-Whitney (fixation counts); survival analysis (time-to-first-fixation) |
| MaxDiff | Insufficient N for stable utility scores; item set too large | Multinomial logit utility scores; ranked bar chart with uncertainty |
| Diary Studies | Compliance attrition; retrospective recall bias | Mixed-effects models (longitudinal); ICC (within vs. between variance) |
