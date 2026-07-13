---
scope: reference
modifies_workflow: false
---

# Measurement

## Attitudinal vs. Behavioral Measurement

This is one of the most fundamental distinctions in UX research. Get it right at S3 before choosing any instrument.

- **Attitudinal measures** capture what people say: perceived ease, satisfaction, trust, intent, preference. They are collected via surveys, rating scales, and verbal responses. Examples: SUS, UMUX-Lite, SEQ, NPS, Likert items.
- **Behavioral measures** capture what people do: whether they completed a task, how long it took, where they clicked first, whether they backtracked in a navigation tree. They are collected via task observation, instrumented prototypes, tree tests, first-click tests, and analytics.

**Why the distinction matters:**
- Attitudinal and behavioral measures frequently diverge. A product can score well on SUS while users still fail key tasks — or vice versa.
- Attitudinal measures are susceptible to social desirability bias, satisficing, and anchoring effects. Behavioral measures are susceptible to task wording effects, artificial test environments, and demand characteristics.
- Reporting a SUS score as evidence of usability is incomplete without behavioral data. Reporting task completion without a satisfaction measure misses the emotional dimension.
- At S3, decide which type of evidence the research question requires. If the question is "Can users find the checkout button?" → behavioral. If the question is "How satisfied are users with the onboarding experience?" → attitudinal. Most benchmark studies should include both.

---

## Behavioral UX Metrics

These are the core metrics for task-based and navigation-based studies. Define them operationally in the S4 data plan before data collection.

### Task Completion Rate
- **What it is**: the proportion of participants who successfully completed a defined task.
- **Scale**: binary (0 = fail, 1 = success) per participant per task.
- **Analysis**: proportion; report as percentage with confidence interval.
- **Recommended CI method**: Wilson confidence interval — more accurate than normal-approximation (Wald) CI, especially at N < 100 or when p is near 0 or 1.
  ```python
  from statsmodels.stats.proportion import proportion_confint
  lo, hi = proportion_confint(successes, n, alpha=0.05, method='wilson')
  ```
- **Comparison**: two-proportion z-test or Chi-square (2×2) for comparing two designs or groups.
- **Define success criteria a priori** in the S4 plan. What counts as a successful completion? Partial credit? Time limit? Unresolved ambiguity about success criteria is the most common source of task completion measurement error.

### Time-on-Task
- **What it is**: elapsed time from task start to task end (success or failure).
- **Scale**: ratio (seconds or milliseconds). True zero exists.
- **Distribution**: right-skewed. A small number of very slow participants stretches the mean upward. Do not report the mean alone.
- **Before parametric tests**: log-transform time values, check for approximate normality of the transformed values, then run the test on log-transformed data. Back-transform the means for reporting.
- **Report**: median + IQR as the primary summary statistic. Include mean + SD as supplementary for completeness and to match stakeholder expectations.
- **Comparison**: paired or independent t-test on log-transformed times; or Mann-Whitney U on raw times for non-parametric comparison.
- **Include only completers** in time-on-task analysis unless you have a specific reason to include failures (and if you do, state it explicitly and analyze separately).

### Error Rate
- **What it is**: the count of errors per task or per session.
- **Scale**: count. Poisson-distributed in many cases (low mean, non-negative integer).
- **Define error taxonomy a priori** in the S4 data plan. Categories might include: wrong path taken, incorrect input, system-triggered error, backtrack after incorrect node (for navigation tasks). Raters must apply the taxonomy reliably — check inter-rater reliability (Cohen's κ) if errors are rated by humans.
- **Analysis**: mean errors per task with SD; Poisson regression if modeling predictors of error count. For simple comparisons, Mann-Whitney U is often appropriate given the count/skewed nature of the data.
- **Report alongside task completion** — a task can be completed despite errors. Error rate tells you how costly the path was.

### Tree Test Success Rate
- **What it is**: the proportion of participants who selected the correct destination in a tree test task.
- **Scale**: binary per participant per task.
- **Analysis**: proportion; Wilson CI recommended (same formula as task completion rate above).
- **Interpretation guidance**: success rates below 70–75% on a tree test task generally indicate a findability problem worth addressing. Optimal Workshop's benchmark is roughly 80%+ for a well-designed structure on a clear task, but context matters — set your own benchmark at S3 based on the task's importance and the user population.
- **Compare across tasks** in a table. Tasks with low success rates flag specific navigation problems; tasks with high success rates confirm that structure.

### Tree Test Directness Score
- **What it is**: the proportion of participants who reached the correct destination without backtracking (i.e., navigated directly, no wrong turns corrected).
- **Scale**: binary per participant per task (direct = 1, indirect = 0).
- **Analysis**: proportion; Wilson CI.
- **Interpretation**: a task can have high success rate but low directness — meaning users eventually found the right answer but had to backtrack to do it. Low directness signals that the label or hierarchy is misleading even when users recover. High success + high directness = good. High success + low directness = functional but effortful. Low success = broken.
- **Report success rate and directness together** for each task.

### First-Click Accuracy
- **What it is**: the proportion of participants whose first click lands in the predefined target zone.
- **Scale**: binary per participant per task.
- **Analysis**: proportion; Wilson CI.
- **Define target zones a priori**. Post-hoc zone definition is p-hacking. Zones should correspond to meaningful UI regions, not be drawn around where clicks actually landed.
- **Why first click matters**: users who make a correct first click complete tasks successfully ~87% of the time. Users who make an incorrect first click complete tasks successfully only ~24% of the time (Spool, UIE Research). This ~3.6x difference makes first-click accuracy a strong early-stage diagnostic.

---

## Card Sorting Native Metrics

Card sorting produces structured outputs that require specific interpretation frameworks. These are not standard psychometric metrics — they are IA-specific analytical tools.

### Agreement Ratio (Standardization Score)
- **What it is**: for each card, the proportion of participants who placed it in the most popular category.
- **Range**: 0–1. A score of 1.0 means all participants agreed. A score of 0.25 means 25% of participants chose the modal category — low agreement.
- **Interpretation**: agreement ratios above 0.70 indicate that a card has a clear mental home for most users. Below 0.50 indicates ambiguity — the card may belong in multiple categories, or the card's label is confusing, or the category structure doesn't match the user's mental model.
- **Use it to prioritize**: cards with low agreement ratios are the ones to bring back to qual or redesign.

### Co-occurrence Matrix
- **What it is**: a matrix showing how frequently each pair of cards was placed in the same group by participants.
- **Values**: counts or proportions (0–1 when normalized by N).
- **Use**: identifies natural clusters. Cards that co-occur frequently belong together in the user's mental model. This feeds directly into IA design decisions.
- **Visualization**: heat map with hierarchical clustering applied to the co-occurrence matrix is the standard output. Most card sorting tools (Optimal Workshop, Maze) generate this automatically.

### Dendrogram
- **What it is**: a hierarchical clustering diagram derived from the co-occurrence matrix.
- **Interpretation**: the height at which two cards or clusters merge indicates how similar participants considered them. Lower merge height = stronger agreement. Higher merge height = looser grouping.
- **Threshold guidance**: there is no universal cutoff, but a common practice is to cut the dendrogram at 50–60% similarity to identify primary groupings for an initial IA proposal. Validate the chosen structure with a closed card sort or tree test.
- **Do not over-interpret small differences** in dendrogram merge heights, especially with N < 20. Cluster assignments can shift noticeably with small N changes.

### Standardization Matrix
- A matrix showing, for each card × category combination, what percentage of participants placed that card in that category.
- **Use**: identifies cards that are split across categories (e.g., 40% in Category A, 35% in Category B) — these are ambiguous items that need attention. Also shows whether proposed categories are clearly understood or overlap in participants' minds.

---

## Levels of Measurement

| Level | Properties | Examples | Allowed Statistics |
|---|---|---|---|
| Nominal | Categories only, no order | Gender, condition, platform | Mode, chi-square, frequency |
| Ordinal | Order, but intervals not equal | Likert items, satisfaction ratings | Median, rank tests |
| Interval | Equal intervals, no true zero | Temperature (°C), many scales | Mean, SD, t-test, ANOVA |
| Ratio | Equal intervals + true zero | Time, count, age | All statistics |

**Likert debate**: Single Likert items are ordinal. Summed/averaged Likert scales with ≥5 items and approximately normal distribution are often treated as interval — acceptable in practice if assumptions are checked.

## Reliability

### Internal Consistency
- **Cronbach's α**: most common. α ≥ 0.70 acceptable; ≥ 0.80 preferred for research; ≥ 0.90 for high-stakes.
- **Limitation**: α inflates with more items; not appropriate for multidimensional scales.
- **McDonald's ω**: preferred over α; handles multidimensionality better.

### Test-Retest Reliability
- Same measure administered twice; correlation between scores.
- **ICC (Intraclass Correlation Coefficient)**: better than Pearson for this purpose.
  - ICC < 0.50: poor; 0.50–0.75: moderate; 0.75–0.90: good; > 0.90: excellent.

### Inter-Rater Reliability
- **Cohen's κ**: for categorical ratings between two raters. κ < 0.20: slight; 0.21–0.40: fair; 0.41–0.60: moderate; 0.61–0.80: substantial; > 0.80: almost perfect.
- **Weighted κ**: for ordinal categories.
- **ICC**: for continuous ratings.

## Validity

| Type | Definition | How to Assess |
|---|---|---|
| Content | Items cover the full domain | Expert review, mapping to construct definition |
| Face | Appears to measure the construct | Participant feedback; not sufficient alone |
| Criterion (concurrent) | Correlates with gold-standard measure at same time | Correlation with established measure |
| Criterion (predictive) | Predicts future outcomes | Correlation with later outcome |
| Construct (convergent) | Correlates with similar measures | High r with theoretically related measures |
| Construct (discriminant) | Does NOT correlate with unrelated measures | Low r with theoretically unrelated measures |

## Validated UX Instruments

### System Usability Scale (SUS)
- 10 items, alternating positive/negative wording, 5-point Likert.
- Scoring: sum odd items subtract 5; sum 25 minus even items; multiply total by 2.5. Range: 0–100.
- Minimum N for stable mean: ≥ 12.

**Norms — Sauro (2011) percentile system (primary reference):**

| SUS Score | Percentile (approx.) | Grade | Interpretation |
|---|---|---|---|
| ≥ 80.3 | 90th | A (Excellent) | Top 10% of benchmarked products |
| 74–80.2 | 70th–89th | B (Good) | Above average |
| 68–73.9 | 50th–69th | C (Okay) | Average range |
| 51–67.9 | 15th–49th | D (Poor) | Below average |
| < 51 | < 15th | F (Awful) | Bottom 15% |

68 is the industry average across Sauro's database of 500+ products. 80.3 corresponds to the 90th percentile. 85+ is approximately the top 5–10% of benchmarked products.

**Important note on mixing norm systems**: The Bangor et al. (2009) adjective rating system (Good, Excellent, Best Imaginable) and the Sauro (2011) percentile system were developed independently from different datasets. Do not mix their thresholds. Use the Sauro percentile system for benchmarking; use the adjective ratings only as informal labels if at all.

### SUPR-Q (Standardized User Experience Percentile Rank Questionnaire)
- 8 items across 4 dimensions: Usability, Credibility, Loyalty, and Appearance.
- Items are rated on a 5-point Likert scale. The composite score (1–5) is converted to a percentile rank against a normative database of 200+ websites — raw scores are not directly interpretable without the percentile conversion.
- **When to use SUPR-Q over SUS**: SUPR-Q is designed for website quality benchmarking across multiple dimensions (including credibility and loyalty), making it more appropriate for competitive benchmarking of websites and for measuring holistic website quality. SUS is focused on perceived usability and is appropriate for any product type (desktop app, mobile app, website, hardware). If you need a task-focused usability score, use SUS. If you need to benchmark a website holistically against other websites, use SUPR-Q.
- **Normative database**: Sauro's normative database at MeasuringU (measuringu.com) is the primary source for percentile benchmarking. Scores are reported as percentile ranks relative to this database — a score at the 70th percentile means the website scored higher than 70% of the websites in the database.
- **Subscale reporting**: the 4 subscale scores (Usability, Credibility, Loyalty, Appearance) can be reported individually to identify which dimensions are above or below benchmark.

### UMUX-Lite
- 2-item version of UMUX. Fast; correlates highly with SUS.
- Formula: ((Item1 − 1) + (7 − Item2)) / 12 × 100.

### Single Ease Question (SEQ)
- Single 7-point item after each task: "Overall, how would you rate the difficulty of this task?"
- Mean ≥ 5.5 considered acceptable. Use with task success and time-on-task.

### NASA-TLX
- 6 subscales: Mental Demand, Physical Demand, Temporal Demand, Performance, Effort, Frustration.
- Raw TLX (averaging all 6 subscales equally) is the most commonly used version in UX research and HCI studies. The original weighted version (Hart & Staveland, 1988) requires a paired-comparison weighting task administered before each study, where participants compare all pairs of subscales to establish their personal importance weights. Unless you have a specific reason to use the weighted version, Raw TLX is the standard choice. It is simpler to administer and produces results comparable to the weighted version in most contexts.

### Net Promoter Score (NPS)
- Single 0–10 item. Promoters (9–10) minus Detractors (0–6) = NPS.
- NPS is a business metric, not a validated psychometric instrument. Use with caution in research contexts; pair with other measures.

## Common Measurement Mistakes
- Using a single item to measure a multidimensional construct.
- Treating a single Likert item as interval and computing means without acknowledging the assumption.
- Computing α on a scale that was designed to be multidimensional.
- Using NPS as the sole outcome in a usability study.
- Forgetting to reverse-score negatively worded items before computing composites.
- Reporting task completion without defining success criteria a priori.
- Reporting mean time-on-task without acknowledging right skew and without median + IQR.
- Interpreting tree test success rate without directness — you are missing half the story.
