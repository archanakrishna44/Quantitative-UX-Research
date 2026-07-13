---
scope: reference
modifies_workflow: false
---

Now I have sufficient research to compile the comprehensive checklist. Let me synthesize all findings into a structured document.

---

# Comprehensive Knowledge Checklist: UX Quantitative Researcher

**Purpose:** Ground-truth checklist for auditing a UX knowledge base against authoritative industry and academic standards.
**Compiled:** May 2026 | **Sources:** Nielsen Norman Group, MeasuringU/Sauro & Lewis, Optimal Workshop, UXPA, industry job descriptions (Amazon, Google, Meta, Citi), practitioner publications.

**Depth scale used throughout:**
- **Awareness** — Knows the term, knows when to use it, can describe it generally
- **Working knowledge** — Can apply it independently with acceptable accuracy; makes appropriate methodological choices
- **Expert** — Can evaluate edge cases, train others, defend methodological choices, adapt methods to novel contexts

**Variation flag notation:** [VARIES] = practice differs significantly by company size, industry, or team composition.

---

## Domain 1: UX Research Methods

### 1.1 Quantitative Usability Testing (Benchmarking Studies)

**What it is:** Structured task-based studies with large samples (typically 35–100+ participants) designed to produce statistically reliable performance metrics — completion rates, time-on-task, error rates, and satisfaction scores. Distinguished from qualitative usability testing by its intent: measuring rather than exploring.

**Expected depth:** Working knowledge to Expert

**Required competencies:**
- Design realistic, unambiguous task scenarios with clear success criteria defined before data collection
- Distinguish formative (problem-finding, small samples) from summative (benchmarking, large samples) study goals and select appropriate sample sizes for each
- Understand when to run moderated vs. unmoderated quantitative studies and what each sacrifices
- Define what constitutes task success vs. partial credit vs. failure — and document it before running the study
- Combine performance metrics (completion, time, errors) with perception metrics (SEQ, SUS) in the same study
- Understand the relationship between SUS post-test scores and actual task performance (correlation ~r=0.24; only ~6% of variance explained)
- Know how to set up pre-registered benchmarks before launching so results can be compared longitudinally

**Source:** [NN/G Quantitative UX Research Methods](https://www.nngroup.com/articles/quantitative-user-research-methods/); [MeasuringU Task-Based Metrics](https://measuringu.com/task-based-metrics/)

---

### 1.2 Surveys and Questionnaires

**What it is:** Structured instruments used to measure user attitudes, behaviors, satisfaction, and demographics at scale. One of the highest-leverage quantitative methods in practice because of low cost and scalability.

**Expected depth:** Expert (surveys are the single most commonly expected competency for this role)

**Required competencies:**
- Write unbiased, clear survey items — avoid double-barreled questions, leading questions, loaded language, and acquiescence bias
- Select appropriate response scales (Likert 5-point vs. 7-point, unipolar vs. bipolar, agree-disagree vs. frequency), know psychometric implications of each
- Distinguish between exploratory surveys (hypothesis generation) and confirmatory surveys (hypothesis testing) and design accordingly
- Design screening questions (screeners) to ensure representative or targeted recruitment; understand inclusion/exclusion logic
- Understand sampling strategy — random, stratified, quota, convenience — and know which introduces what biases
- Apply survey weighting to correct for non-representative samples when probability sampling is not feasible
- Understand panel bias, response rate effects, and how survey context affects answers
- Use standardized validated instruments where appropriate rather than building custom questionnaires from scratch (see Domain 2)
- Pilot-test surveys using cognitive interviewing to find comprehension failures before launch
- Know the difference between cross-sectional and longitudinal survey designs

**Source:** [MeasuringU](https://measuringu.com); [Carl J. Pearson self-study guide](https://carljpearson.com/learn-quantitative-ux-research-self-study-resources/); [Sauro & Lewis, *Quantifying the User Experience* 2nd ed.]

---

### 1.3 A/B Testing and Multivariate Testing

**What it is:** Controlled experiments in live products where users are randomly assigned to see different versions of a feature, UI element, or flow. Results are compared using behavioral metrics to determine which version performs better.

**Expected depth:** Working knowledge (Expert for roles with access to live product infrastructure)

**Required competencies:**
- Formulate testable hypotheses with a clearly defined primary metric and pre-specified success threshold before data collection begins
- Understand statistical requirements: minimum detectable effect (MDE), required sample size, statistical power (typically 80%), and significance threshold (alpha, typically 0.05)
- Recognize and explain the multiple comparisons problem (family-wise error rate inflation) when running multivariate tests — know corrections (Bonferroni, Benjamini-Hochberg)
- Distinguish between one-sided and two-sided hypothesis tests and know when each is appropriate
- Identify and prevent peeking (stopping a test early because results look significant) — understand sequential testing or pre-commitment to sample size
- Understand novelty effects (temporary engagement spikes on new features) and how they contaminate results
- Know when A/B testing is inappropriate: low-traffic products, ethical constraints, interdependencies between variants
- Distinguish statistical significance from practical significance (effect size vs. p-value)
- Work with product and engineering teams to implement correct randomization — understand unit of randomization (user vs. session vs. device) and why it matters

**Source:** [NN/G Quantitative UX Research Methods](https://www.nngroup.com/articles/quantitative-user-research-methods/); Sauro & Lewis; [UXR Guild Statistical Tests Guide](https://uxrguild.com/use-statistical-tests-ux-research/)

---

### 1.4 Analytics and Behavioral Data Analysis

**What it is:** Analysis of passively collected interaction data from live products — clicks, navigation paths, funnel drop-offs, feature usage, retention, session behavior. Does not require active participant recruitment.

**Expected depth:** Working knowledge to Expert [VARIES — heavily organization-dependent]

**Required competencies:**
- Define and interpret key behavioral metrics: DAU/MAU, session length, feature adoption, funnel conversion rates, churn, retention curves, time-to-first-key-action
- Understand the difference between event-based analytics (Amplitude, Mixpanel) and pageview-based analytics (Google Analytics) and what each captures
- Write SQL queries to extract and aggregate behavioral data from product databases — this is a hard requirement at most tech companies
- Distinguish correlation from causation in observational data — understand confounders and selection effects
- Know the limitations of analytics: analytics shows what users do, not why; it cannot explain intention or emotional state
- Apply cohort analysis to understand how behavior changes over time for users acquired at different periods
- Identify and account for survivorship bias in retention analyses
- Use funnel analysis and path analysis to find friction points — know how to set up event taxonomies that make this possible
- Understand instrumentation requirements: work with engineers on event logging schemas so that research questions are answerable before data collection begins

**Source:** [NN/G Quantitative UX Research Methods](https://www.nngroup.com/articles/quantitative-user-research-methods/); [MeasuringU]; industry job descriptions (Amazon, Citi)

---

### 1.5 Tree Testing

**What it is:** A method for evaluating information architecture in isolation from visual design. Participants navigate a text-only site hierarchy to complete tasks. Measures directness, success rate, and where users go wrong.

**Expected depth:** Working knowledge

**Required competencies:**
- Design tree testing tasks that are unambiguous, represent realistic user goals, and avoid labeling cues (landmark bias)
- Interpret output metrics: directness score (proportion who reached destination without backtracking), success rate, first-click accuracy, and node-by-node path data
- Understand the validated finding that correct first click predicts ~70% overall task success; incorrect first click predicts only ~24% success — and use first-click data diagnostically
- Distinguish between a navigation problem (users go to the wrong place) and a labeling problem (correct destination but wrong label) using path analysis
- Know when tree testing is appropriate vs. card sorting vs. first-click testing
- Understand sample size requirements: typically 50–100 participants per tree to achieve stable results on directness metrics

**Source:** [Optimal Workshop Tree Testing](https://www.optimalworkshop.com/tag/tree-testing); [Optimal Workshop first-click research](https://blog.optimalworkshop.com/does-the-first-click-really-matter-treejack-says-yes/)

---

### 1.6 Card Sorting

**What it is:** A method where participants group and optionally label content items, revealing their mental models and natural categorization schemes. Used to inform or validate information architecture.

**Expected depth:** Working knowledge

**Required competencies:**
- Distinguish open card sorting (participant-created categories, generative) from closed card sorting (researcher-provided categories, evaluative)
- Know when card sorting precedes vs. follows tree testing: card sorting informs architecture creation; tree testing validates architecture
- Analyze quantitative outputs: agreement scores (percentage of participants who made the same grouping), dendrogram interpretation, similarity matrix
- Understand the limitations: card sorting surfaces mental models but not navigation behavior; users may group content differently than they navigate it
- Know appropriate sample sizes: 20–30 participants typically sufficient for open sorts; 30–50 for closed sorts

**Source:** [Optimal Workshop Card Sorting](https://www.optimalworkshop.com/tag/card-sorting); [NN/G]

---

### 1.7 First-Click Testing

**What it is:** Participants see a static screenshot or prototype and click where they would go to complete a task. The first click location is recorded. Used to validate navigation, labeling, and layout before building functional prototypes.

**Expected depth:** Working knowledge

**Required competencies:**
- Understand the empirical basis: people who get the first click right are approximately 3x more likely to complete the full task successfully (Bailey & Wolfson, 2009; validated by Optimal Workshop with millions of responses)
- Set up first-click studies with realistic task framing and appropriate stimuli fidelity
- Interpret heatmaps and click distribution data statistically — not just visually
- Use chi-square tests to compare click distributions across design variants or user segments

**Source:** [Optimal Workshop first-click guide](https://www.optimalworkshop.com/101-guides/card-sorting-101/how-to-create-your-first-click-test); [Optimal Workshop first-click research](https://blog.optimalworkshop.com/does-the-first-click-really-matter-treejack-says-yes/)

---

### 1.8 Eye Tracking

**What it is:** Specialized equipment tracks participants' eye movements and fixations across an interface. Used to study attention distribution, reading patterns, visual hierarchy, and scan paths.

**Expected depth:** Awareness to Working knowledge [VARIES — high cost limits usage outside well-resourced labs]

**Required competencies:**
- Understand output metrics: fixation count, fixation duration, time-to-first-fixation on AOI (area of interest), revisit count, saccade patterns
- Know the sample size requirement: 30+ participants for reliable heat map data
- Understand equipment calibration requirements and how poor calibration degrades data quality
- Interpret gaze plots and attention maps; know that heat maps aggregate data and can obscure individual variation
- Know when eye tracking adds value vs. when first-click or analytics data is sufficient

**Source:** [NN/G Quantitative UX Research Methods](https://www.nngroup.com/articles/quantitative-user-research-methods/)

---

### 1.9 Diary Studies (Quantitative Component)

**What it is:** Participants self-report behaviors, experiences, or events over an extended period (days to weeks). Can be structured for quantitative analysis when using Likert items, frequency counts, or event logs.

**Expected depth:** Working knowledge

**Required competencies:**
- Design structured diary entries that yield analyzable quantitative data (e.g., rating scales, event frequencies)
- Manage compliance and attrition in longitudinal designs — know that completion rates degrade significantly over multi-week studies
- Distinguish diary studies from Experience Sampling Methods (ESM) — ESM prompts are researcher-triggered, diary entries are participant-triggered
- Apply appropriate longitudinal statistical methods to diary data (repeated measures, multilevel modeling at awareness level)

**Source:** [NN/G Diary Studies](https://www.nngroup.com/articles/diary-studies/)

---

### 1.10 Desirability Studies

**What it is:** Participants select descriptive words (e.g., from a provided word bank like Microsoft's Product Reaction Cards) to characterize their perception of a design's aesthetic, brand alignment, or emotional tone. Word frequencies are counted and compared.

**Expected depth:** Awareness to Working knowledge

**Required competencies:**
- Know the Microsoft Product Reaction Cards methodology and its limitations
- Apply chi-square tests to compare word selection frequencies across design variants or user segments
- Understand that desirability studies measure perception, not usability — and position findings accordingly

**Source:** [NN/G Quantitative UX Research Methods](https://www.nngroup.com/articles/quantitative-user-research-methods/)

---

### 1.11 MaxDiff (Maximum Difference Scaling)

**What it is:** A survey methodology where respondents repeatedly choose the best and worst options from small subsets of a larger item set. Produces interval-scaled preference scores that are more discriminating than Likert ratings.

**Expected depth:** Working knowledge [VARIES — more common in larger research teams and market research contexts]

**Required competencies:**
- Understand when MaxDiff is preferable to Likert-scale priority rating: when items cluster at the top, when social desirability bias inflates ratings, when forced trade-offs produce more honest preferences
- Design a MaxDiff survey with appropriate number of items per set, number of sets per respondent, and total respondents needed
- Interpret utility scores and confidence intervals on relative preference
- Distinguish MaxDiff from conjoint analysis: MaxDiff ranks individual items; conjoint analysis evaluates combinations of attributes

**Source:** [Bentley UX Center MaxDiff Guide](https://www.bentley.edu/centers/user-experience-center/how-use-max-diff-survey-analysis-feature-prioritization); [MeasuringU/Sauro KDA, Cluster, and Factor Analysis](https://measuringu.com/wp-content/uploads/2021/08/KDA_CA_FA_Google2021.pdf)

---

## Domain 2: UX Metrics and Measurement

### 2.1 Task Completion Rate

**What it is:** The proportion of participants who successfully complete a task given a specified success criterion. The fundamental behavioral usability metric.

**Calculation:** Number of successful completions / total attempts × 100. Binary (pass/fail) is the most common form; partial credit scoring is used when tasks have intermediate states.

**Interpretation:** Industry benchmark across 1,100+ tasks is 78% (MeasuringU). Scores below 60% typically indicate serious usability problems requiring redesign. Scores above 90% are high-performing.

**Statistical treatment:** Because completion rates are proportions from binary data, they require different statistical handling than continuous data:
- Confidence intervals: use the adjusted Wald method (not normal approximation) for small samples; Clopper-Pearson for conservative estimates
- Comparisons: use chi-square test or Fisher's exact test (for small samples), not t-test
- Never apply t-tests directly to proportions

**Expected depth:** Expert

**Source:** [MeasuringU UX Benchmarks](https://measuringu.com/ux-benchmarks/); Sauro & Lewis *Quantifying the User Experience* Ch. 3–4

---

### 2.2 Time on Task

**What it is:** How long it takes a participant to attempt a task from start to defined endpoint. Measures efficiency.

**Calculation:** Clock time in seconds or minutes from task presentation to final action. Decide before the study whether to measure completion time only (completers) or all attempts including failures.

**Statistical treatment — critical:** Task time data is positively skewed (can't be less than 0 seconds; rare slow users extend the tail). Requires special handling:
- Use geometric mean (equivalent to mean of log-transformed times) rather than arithmetic mean for central tendency
- Log-transform times before computing confidence intervals and running parametric tests
- Report median alongside geometric mean for non-statistician audiences

**Benchmarks:** Highly task-specific; comparison to a prior baseline or competitor benchmark is more meaningful than absolute values.

**Expected depth:** Working knowledge to Expert

**Source:** [MeasuringU Task-Based Metrics](https://measuringu.com/task-based-metrics/); Sauro & Lewis Ch. 5

---

### 2.3 Error Rate

**What it is:** Count or rate of incorrect actions per task attempt. Measures learnability and design clarity.

**Calculation:** Errors per task (mean errors/task), or proportion of tasks with at least one error. Industry benchmark: average 0.7 errors per task; only 10% of tasks are error-free.

**Expected depth:** Working knowledge

**Source:** [MeasuringU UX Benchmarks](https://measuringu.com/ux-benchmarks/)

---

### 2.4 System Usability Scale (SUS)

**What it is:** A 10-item Likert questionnaire (5-point scale) measuring perceived usability. The most widely used standardized usability questionnaire. Free, validated, reliable with small samples.

**Calculation:**
- Odd items (1,3,5,7,9): subtract 1 from user's response
- Even items (2,4,6,8,10): subtract user's response from 5
- Sum all adjusted scores × 2.5 → 0–100 scale

**Interpretation and benchmarking:**
- Average SUS across 500+ datasets: 68
- Above 80.3: Grade A (top ~10%); treat as "excellent"
- 68–80: Grade B–C; above average to average
- 51–68: Grade D; below average
- Below 51: Grade F
- Interpret via percentile rank, not raw score as percentage
- SUS reliably correlates with user satisfaction; does NOT strongly predict task performance (r=0.24)

**Statistical notes:**
- Reliable with as few as 8–12 participants for point estimates; wider CIs with small samples
- Treat as an interval scale for analysis purposes; compute confidence intervals around mean scores
- Do not compare SUS scores across fundamentally different product types without appropriate normalization

**Expected depth:** Expert

**Source:** [MeasuringU SUS Guide](https://measuringu.com/sus/); [SUS Item Benchmarks (Sauro, 2015)](https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Sauro_Feb2015.pdf)

---

### 2.5 UMUX-Lite (Usability Metric for User Experience — Lite)

**What it is:** A 2-item questionnaire measuring perceived usability. Shorter alternative to SUS, designed for contexts where survey length matters (mobile, intercept surveys).

**Calculation:** Two items on 7-point scales; apply regression correction to align with SUS scoring (UMUX-LITEr) for comparability against SUS benchmarks.

**When to use:** When brevity is required; when administering post-task; when SUS is too long for the study context.

**Expected depth:** Working knowledge

**Source:** [Measuring Perceived Usability: SUS, UMUX-LITE (Sauro & Lewis)](https://www.researchgate.net/publication/281161362_Measuring_Perceived_Usability_The_SUS_UMUX-LITE_and_AltUsability)

---

### 2.6 Single Ease Question (SEQ)

**What it is:** A single 7-point question asked after each task: "How difficult or easy did you find the task?" Measures perceived task difficulty at the task level.

**Calculation:** Mean across participants on 7-point scale (1=Very difficult, 7=Very easy). Compute confidence interval.

**Benchmarks:** Across 200+ tasks, the average SEQ score is 5.5 — significantly above the scale midpoint of 4. A task scoring below 4.5 is a meaningful usability concern; below 4.0 is serious.

**Relationship to SUS:** SUS is administered post-test (study level); SEQ is administered post-task (task level). They measure related but distinct constructs — use both in the same study for multi-level insight.

**Expected depth:** Expert

**Source:** [NN/G Beyond NPS: Measuring Perceived Usability](https://www.nngroup.com/articles/measuring-perceived-usability/); [MeasuringU UX Benchmarks](https://measuringu.com/ux-benchmarks/)

---

### 2.7 SUPR-Q (Standardized User Experience Percentile Rank Questionnaire)

**What it is:** An 8-item questionnaire measuring four dimensions of website quality: usability, trust/credibility, appearance, and loyalty (including NPS). Produces a percentile rank against a normative database of 200+ websites.

**Calculation:** Raw SUPR-Q = average of component scores on 1–5 scale; NPS item is divided by 2 to normalize to same scale. Percentile rank is derived by comparing against normative database.

**When to use:** Website quality measurement, competitive benchmarking, longitudinal tracking.

**Expected depth:** Working knowledge

**Source:** [MeasuringU]; [Fuzzy Math SUPR-Q Guide](https://fuzzymath.com/blog/suprq-design-metric/)

---

### 2.8 Net Promoter Score (NPS)

**What it is:** Single question: "How likely are you to recommend [product/service] to a friend or colleague?" on a 0–10 scale. NPS = % Promoters (9–10) minus % Detractors (0–6).

**Industry benchmarks (MeasuringU):** Consumer software NPS: +21%; Website NPS: -14%.

**Critical limitations the UX quant researcher must know:**
- NPS correlates weakly with actual behavior in many product contexts
- The promoter/passive/detractor cutoffs are arbitrary and not validated across cultures
- NPS conflates the product experience with brand loyalty and price perceptions
- Should be tracked longitudinally and compared against benchmarks — a single number is not actionable without context

**Expected depth:** Working knowledge

**Source:** [MeasuringU UX Benchmarks](https://measuringu.com/ux-benchmarks/)

---

### 2.9 Google HEART Framework Metrics

**What it is:** A five-dimension framework (Happiness, Engagement, Adoption, Retention, Task Success) for selecting and defining user-centered metrics for large-scale web products. Paired with a Goals-Signals-Metrics (GSM) process for operationalizing product goals into measurable metrics.

**Dimensions:**
- **Happiness:** Attitudinal metrics (satisfaction ratings, NPS, SUS)
- **Engagement:** Behavioral intensity (session frequency, depth of use, features used per session)
- **Adoption:** New user growth, feature uptake by existing users
- **Retention:** Return rate, churn, subscription renewal
- **Task Success:** Completion rate, time-on-task, error rate

**GSM process:** Goal → Signal (observable indicator) → Metric (quantified signal). Forces explicit operationalization before data collection.

**Expected depth:** Working knowledge — awareness of framework is universal; operationalization competency expected at most tech companies.

**Source:** [Google Research: User-Centered Metrics for Web Applications](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/); [HEART Framework overview](https://www.heartframework.com/)

---

### 2.10 NASA-TLX (Task Load Index)

**What it is:** A 6-dimension workload questionnaire measuring mental demand, physical demand, temporal demand, performance, effort, and frustration. Used when cognitive load is a key research question (enterprise software, safety-critical systems, complex workflows).

**Expected depth:** Awareness to Working knowledge [VARIES — more common in enterprise, defense, automotive, medical device UX research]

**Source:** [NN/G Measuring Perceived Usability](https://www.nngroup.com/articles/measuring-perceived-usability/)

---

## Domain 3: Statistics and Significance Testing

### 3.1 Foundational Statistical Concepts

**Expected depth:** Expert — these are non-negotiable for the role

| Concept | What the researcher must be able to do |
|---|---|
| Confidence intervals | Compute and interpret CI for proportions (adjusted Wald), means, and differences. Explain width vs. confidence trade-off. Know that CI width depends on sample size and variance, not population size. |
| P-values | Define correctly: probability of observing results this extreme if null hypothesis were true. Not: the probability the null is true. Identify misinterpretations. |
| Statistical power | Define as probability of correctly detecting a true effect. Know the standard target (80%) and what drives power: sample size, effect size, alpha level. |
| Effect size | Report effect sizes alongside p-values. Know Cohen's d (standardized mean difference) for continuous outcomes; odds ratio / relative risk for proportions. Know benchmarks: d=0.2 small, 0.5 medium, 0.8 large. |
| Statistical vs. practical significance | Distinguish clearly: a p<0.001 result with d=0.05 may be irrelevant to design decisions. |
| Type I and Type II errors | Define alpha (false positive rate) and beta (false negative rate). Explain the trade-off and how it affects study design decisions. |
| Null hypothesis significance testing (NHST) | Understand both the utility and widely documented limitations of NHST; know alternatives (Bayesian inference at awareness level). |

**Source:** [MeasuringU Five Hard Quant Concepts](https://measuringu.com/five-hard-quant/); Sauro & Lewis *Quantifying the User Experience* Ch. 3, 6; [UXR Guild Stats Guide](https://uxrguild.com/use-statistical-tests-ux-research/)

---

### 3.2 Test Selection: When to Use Which Test

The core competency is not memorizing tests but selecting the correct test based on:
1. Research question (relationship, difference, prediction)
2. Number of groups/conditions
3. Data type (nominal, ordinal, interval/ratio)
4. Distribution assumptions (normal vs. non-normal)
5. Study design (independent samples vs. repeated measures)

**Expected depth:** Working knowledge to Expert

**Decision framework:**

**For completion rate / proportion data (binary outcomes):**
- Single condition vs. target: one-sample binomial test or one-sample z-test for proportions
- Two independent conditions: chi-square test of independence or Fisher's exact test (preferred when any expected cell count < 5)
- Two conditions, same participants: McNemar's test

**For task time / continuous data (after log transform if skewed):**
- Two independent groups: independent samples t-test
- Two conditions, same participants: paired t-test
- More than two groups: one-way ANOVA; post-hoc Tukey HSD for pairwise comparisons
- Non-normal data / ordinal: Mann-Whitney U (independent), Wilcoxon signed-rank (paired), Kruskal-Wallis (multi-group)

**For Likert / satisfaction scale data:**
- Treat 5–7 point scales as approximately interval for parametric tests when n>15 per group (common practice; contested in academic literature) [VARIES]
- Conservative approach: use Mann-Whitney U / Wilcoxon for Likert data
- SUS and similar composite scores: treat as interval, use t-tests

**For relationships:**
- Pearson's r: linear relationship between two continuous, normally distributed variables
- Spearman's rho: ordinal data or when normality cannot be assumed
- Multiple regression: continuous or binary outcome with multiple predictors
- Logistic regression: binary outcome (task success/failure) with continuous or categorical predictors

**For key driver analysis:**
- Linear regression with standardized betas to rank drivers of satisfaction or loyalty
- Know how to interpret and report importance scores

**Source:** [UXR Guild Statistical Tests Guide](https://uxrguild.com/use-statistical-tests-ux-research/); [Advanced Statistics UXR Guild](https://uxrguild.com/using-advanced-statistics-ux-research/); Sauro & Lewis

---

### 3.3 Sample Size Planning

**Expected depth:** Expert — this is one of the most commonly deficient skills in the field

**Three distinct sample size problems, requiring different approaches:**

1. **Problem detection (formative usability testing):** The "5 users" heuristic applies ONLY to this scenario — finding problems that affect ≥31% of the population with 85% confidence. For less prevalent problems, more users are needed. Formula: n = log(1-confidence) / log(1-p)

2. **Benchmarking / estimation with desired precision:** Driven by desired margin of error (e.g., ±5% on completion rate) and confidence level (95%). Larger samples needed for narrow confidence intervals.

3. **Comparative studies (A/B, design comparison):** Driven by power analysis. Inputs: desired power (0.80), alpha (0.05), expected effect size (small/medium/large). Use G*Power or equivalent. Common error: failing to conduct power analysis before study launch.

**Additional concepts:**
- Know that sample size affects CI width more than it affects point estimates
- Know that population size has minimal effect on required sample size for large populations (a common misconception)
- Plan for attrition in longitudinal studies

**Source:** [MeasuringU Five Hard Quant Concepts](https://measuringu.com/five-hard-quant/); Sauro & Lewis Ch. 6–7

---

### 3.4 Advanced Statistical Methods (Expected at Senior Level)

**Expected depth:** Working knowledge at senior/staff level; Awareness at mid-level [VARIES by company]

| Method | When used in UX research |
|---|---|
| Regression (linear and logistic) | Key driver analysis (which satisfaction dimensions predict overall NPS or SUS); predicting task success from user characteristics |
| ANOVA / ANCOVA | Multi-group comparisons; controlling for covariates in usability studies |
| Factor analysis | Validating psychometric structure of UX questionnaires; dimensionality reduction for large survey batteries |
| Cluster analysis | User segmentation; persona development from behavioral or attitudinal data; card sort analysis (hierarchical clustering / dendrograms) |
| Multilevel modeling (mixed models) | Nested data structures — e.g., tasks within participants within sessions; longitudinal diary studies |
| Bayesian inference | Quantifying evidence for null hypotheses; updating priors with new study data; increasingly used in tech industry experimentation platforms [VARIES] |

**Source:** [MeasuringU KDA, Cluster, and Factor Analysis slides](https://measuringu.com/wp-content/uploads/2021/08/KDA_CA_FA_Google2021.pdf); [Advanced Statistics UXR Guild](https://uxrguild.com/using-advanced-statistics-ux-research/)

---

### 3.5 Multiple Comparisons and Corrections

**What it is:** When running multiple statistical tests on the same dataset, the probability of at least one false positive grows. At alpha=0.05, running 20 tests expects one false positive by chance.

**Expected depth:** Working knowledge

**Required competencies:**
- Know when multiple comparisons inflation is a real concern vs. when it can be reasonably ignored (exploratory vs. confirmatory analyses)
- Apply Bonferroni correction (divide alpha by number of tests) as conservative option
- Apply Benjamini-Hochberg procedure (controls false discovery rate, less conservative) when appropriate
- Understand family-wise error rate vs. false discovery rate trade-off

**Source:** Sauro & Lewis; [UXR Guild Advanced Statistics](https://uxrguild.com/using-advanced-statistics-ux-research/)

---

## Domain 4: Research Design

### 4.1 Between-Subjects vs. Within-Subjects Designs

**Expected depth:** Expert

**Between-subjects:** Each participant is in only one condition. Advantages: no carryover effects, no practice effects. Disadvantages: more participants needed, higher individual variance.

**Within-subjects (repeated measures):** Same participants across all conditions. Advantages: controls individual differences, more statistical power per participant. Disadvantages: order effects, practice effects, fatigue effects, carryover effects.

**Counterbalancing:** In within-subjects designs, randomize condition order across participants to distribute order effects. Full counterbalancing (all permutations) is ideal; Latin Square is used when the number of conditions makes full counterbalancing impractical. The UX quant researcher must be able to design and implement a counterbalanced protocol correctly.

**When to use each:**
- Between-subjects when tasks or designs are highly similar and learning/exposure effects would contaminate comparisons
- Within-subjects when individual differences are large relative to effect size and carryover can be managed

**Source:** Sauro & Lewis; [UXtweak Counterbalancing](https://www.uxtweak.com/ux-glossary/counterbalancing/)

---

### 4.2 Screener Design and Recruitment

**Expected depth:** Working knowledge to Expert

**Required competencies:**
- Write screeners that identify target participants without revealing who "should" qualify (avoids coached responses)
- Define inclusion/exclusion criteria based on target user populations — avoid over-narrow screeners that undermine representativeness
- Understand panel sources (Prolific, UserTesting, Qualtrics panels, intercept recruitment) and their respective biases
- Know the professional respondent problem: frequent survey-takers on panels produce lower-quality, faster responses — build in attention checks and response-time filters
- Apply stratified or quota sampling when key subgroups (e.g., different user roles, platforms) must be represented
- Understand the difference between a representative sample (mirrors population demographics) and a purposive sample (targets specific user types) — and which is appropriate for a given research question

**Source:** [User Interviews: Surveys for UX Research](https://www.userinterviews.com/ux-research-field-guide-chapter/surveys); [DeveloperUX: Survey Bias in UX Research](https://developerux.com/2025/03/05/how-to-identify-and-fix-survey-bias-in-ux-research/)

---

### 4.3 Operationalization and Measurement Validity

**Expected depth:** Working knowledge

**Required competencies:**
- Translate research questions into measurable constructs — define operationally what will be measured before study design
- Distinguish face validity (does it look like it measures what it claims to), construct validity (does it actually measure the latent construct), and criterion validity (does it correlate with external benchmarks)
- Understand test-retest reliability and internal consistency (Cronbach's alpha) for survey instruments
- Know which established instruments have published validity and reliability evidence (SUS, UMUX-Lite, SUPR-Q, SEQ) vs. custom items that require validation

**Source:** Sauro & Lewis; [Carl J. Pearson self-study resources](https://carljpearson.com/learn-quantitative-ux-research-self-study-resources/)

---

### 4.4 Bias Identification and Mitigation

**Expected depth:** Working knowledge to Expert

**Bias types and mitigations:**

| Bias | What it is | Mitigation |
|---|---|---|
| Social desirability bias | Respondents answer how they think they should rather than how they feel | Anonymous surveys; indirect question wording; behavioral measures over stated attitudes |
| Acquiescence bias | Tendency to agree regardless of content | Balanced scales; reverse-coded items |
| Recency bias | Post-task ratings influenced by most recent task experience | Randomize task order; collect ratings immediately after each task |
| Leading questions | Question wording implies a desired answer | Neutral language; pilot testing with cognitive interviews |
| Demand characteristics | Participants detect researcher expectations and respond accordingly | Blind study design; between-subjects designs for sensitive comparisons |
| Survivorship bias in analytics | Only users who stayed are visible in retention data | Cohort tracking; explicit non-user analysis |
| Sampling bias | Sample does not represent target population | Representative recruitment; survey weighting |
| Anchoring | Initial presented options influence subsequent judgments | Randomize item/option order |

**Source:** [DeveloperUX Survey Bias](https://developerux.com/2025/03/05/how-to-identify-and-fix-survey-bias-in-ux-research/); Sauro & Lewis; [Carl J. Pearson survey weighting](https://carljpearson.com/why-you-should-use-survey-weights-in-ux-research/)

---

### 4.5 Mixed Methods Integration (Triangulation)

**Expected depth:** Working knowledge

**Three integration designs:**
1. **Explanatory sequential:** Quantitative study → qualitative follow-up to explain findings. Example: survey shows low satisfaction on feature X → interviews to understand why.
2. **Exploratory sequential:** Qualitative exploration → quantitative validation at scale. Example: interviews surface themes → survey measures prevalence.
3. **Convergent parallel:** Both methods simultaneously; integrate findings in analysis.

**Required competencies:**
- Understand that qual and quant answer different questions — quant measures "how much/how many"; qual explains "why/how"
- Use triangulation to strengthen claims: when both methods converge, confidence increases; when they diverge, additional investigation is warranted
- Know the limits of triangulation: agreement between methods does not guarantee truth; both may be measuring the same systematic error

**Source:** [NN/G Mixed Methods Research](https://www.nngroup.com/articles/mixed-methods-research/); [NN/G Triangulation](https://www.nngroup.com/articles/triangulation-better-research-results-using-multiple-ux-methods/)

---

### 4.6 Longitudinal and Tracking Study Design

**Expected depth:** Awareness to Working knowledge [VARIES]

**Required competencies:**
- Design longitudinal studies that track the same metrics over time to detect genuine change vs. random variation
- Understand regression to the mean as an artifact in pre-post designs without control groups
- Apply test-retest reliability concepts to determine whether score changes are meaningful vs. noise
- Design cohort studies that follow user groups from acquisition to understand behavior evolution

---

## Domain 5: Tools and Platforms

### 5.1 Survey Platforms

| Tool | Primary use | Expected depth |
|---|---|---|
| Qualtrics | Enterprise survey research; complex skip logic; academic-standard data export; integration with panels | Working knowledge to Expert — most common enterprise standard |
| SurveyMonkey / Momentive | SMB and consumer research; panel access | Awareness to Working knowledge |
| Google Forms | Internal research; quick pilots | Awareness |
| Typeform | Conversational surveys; higher completion rates | Awareness |

**Source:** [Citi JD requirements](https://jobs.citi.com/job/new-york/ux-quantitative-researcher/287/93528702816); [Qualtrics UX Research Tools](https://www.qualtrics.com/articles/strategy-research/ux-research-tools/)

---

### 5.2 Moderated and Unmoderated Testing Platforms

| Tool | Primary use | Expected depth |
|---|---|---|
| UserTesting | Unmoderated video testing at scale; tree testing; surveys | Working knowledge |
| Maze | Unmoderated prototype testing; first-click; tree testing; surveys | Working knowledge |
| Lookback | Moderated and unmoderated sessions with recording | Awareness to Working knowledge |
| Optimal Workshop | Tree testing (Treejack), card sorting (OptimalSort), first-click (Chalkmark), surveys | Working knowledge |
| Lyssna (formerly UsabilityHub) | First-click, design preference, 5-second tests | Awareness |
| UserZoom / Userlytics | Enterprise unmoderated testing | Awareness |

**Source:** [Looppanel Best UX Research Tools 2025](https://www.looppanel.com/blog/best-ux-research-tools); [Maze UX Research Tools Guide](https://maze.co/guides/ux-research/tools/)

---

### 5.3 Product Analytics Platforms

| Tool | Primary use | Expected depth |
|---|---|---|
| Amplitude | Behavioral event analytics; funnel analysis; retention; cohort analysis | Working knowledge — standard at most product companies |
| Mixpanel | Event-based analytics; funnels; A/B test analysis | Working knowledge |
| Google Analytics / GA4 | Web traffic and behavior; conversion tracking | Working knowledge |
| Looker / Tableau / Power BI | Data visualization; dashboard creation; cross-source reporting | Working knowledge |
| Fullstory / Hotjar | Session replay; heatmaps; click maps | Awareness |

**[VARIES]:** Amplitude/Mixpanel competency expected at tech product companies; traditional enterprises may use Adobe Analytics, Tealeaf, or proprietary systems.

**Source:** Industry job descriptions; [Looppanel tool guide](https://www.looppanel.com/blog/best-ux-research-tools)

---

### 5.4 Statistical Analysis Software

| Tool | Primary use | Expected depth |
|---|---|---|
| Python (pandas, scipy, statsmodels, pingouin) | Data manipulation, statistical testing, visualization, scripting reproducible analyses | Working knowledge — increasingly required at tech companies |
| R | Statistical computing; psychometrics; advanced modeling; visualization (ggplot2) | Working knowledge — expected at research-heavy organizations |
| SQL | Querying behavioral databases; extracting event logs; joining user tables | Working knowledge — hard requirement at most tech companies |
| SPSS | Survey data analysis; psychometrics | Working knowledge — more common in traditional enterprise and government |
| Excel / Google Sheets | Quick analyses; reporting; data cleaning | Working knowledge — universal baseline |
| MATLAB / SAS | Niche use in enterprise and academic contexts | Awareness |
| G*Power | Power analysis and sample size calculation | Working knowledge |

**[VARIES]:** Python/R/SQL are hard requirements at FAANG and most tech product companies. SPSS may suffice at market research firms or traditional enterprises.

**Source:** [Amazon Sr. Quant UXR JD](https://amazon.jobs/en/jobs/10382576/sr-quantitative-ux-researcher-applied-ai-solutions); [Citi JD](https://jobs.citi.com/job/new-york/ux-quantitative-researcher/287/93528702816); [Carl J. Pearson self-study](https://carljpearson.com/learn-quantitative-ux-research-self-study-resources/)

---

### 5.5 Data Visualization Tools

| Tool | Primary use | Expected depth |
|---|---|---|
| Tableau | Interactive dashboards; executive reporting; cross-source visualization | Working knowledge |
| Looker / Looker Studio | Web-based dashboards; Google ecosystem integration | Working knowledge |
| Python (matplotlib, seaborn, plotly) | Programmatic visualization in analysis workflows | Working knowledge |
| R (ggplot2) | Publication-quality statistical graphics | Working knowledge |
| PowerPoint / Google Slides | Communicating findings in executive presentations | Expert — this is where most stakeholder communication happens |
| Figma | Annotated UI screenshots for issue documentation | Awareness |

---

### 5.6 Research Repository and Operations Tools

| Tool | Primary use | Expected depth |
|---|---|---|
| Dovetail / EnjoyHQ | Tagging qualitative and quantitative research; searchable insight repository | Awareness to Working knowledge |
| Airtable / Notion | Lightweight research tracking and documentation | Awareness |
| Confluence / SharePoint | Enterprise documentation of research findings | Awareness |

**Source:** [NN/G Research Repositories](https://www.nngroup.com/articles/research-repositories/)

---

## Domain 6: Reporting and Communication

### 6.1 Structuring Research Reports

**Expected depth:** Expert — communication is often cited as the most undervalued quant skill

**Required competencies:**
- Lead with insights and implications, not methodology — stakeholders need to know what to do, not how you ran the study
- Tailor report depth to audience: executive summary (1–2 pages, narrative-led, action-focused) vs. detailed technical report (full methodology, statistical output, confidence intervals) vs. design team readout (annotated visuals, task-level findings, direct design recommendations)
- Document methodology with enough detail for replication — future researchers will run the same benchmarking study
- Present quantitative findings with confidence intervals, not just point estimates — single numbers without uncertainty ranges are incomplete
- Include effect sizes alongside significance results
- Contextualize all numbers against benchmarks (internal historical data, industry norms) — a 72% completion rate is meaningful only relative to a comparison point

**Source:** [User Interviews: Writing Research Reports](https://www.userinterviews.com/ux-research-field-guide-chapter/how-to-write-effective-reports-and-presentations); [NN/G Quant Research in Practice](https://www.nngroup.com/articles/quant-research-practice/)

---

### 6.2 Data Visualization Principles

**Expected depth:** Working knowledge

**Required competencies:**
- Select the right chart type for the data relationship: bar charts for comparisons, line charts for trends over time, scatter plots for correlations, dot plots or forest plots for effect sizes with confidence intervals
- Show variability: error bars, confidence interval ribbons, box plots — never report a mean without its uncertainty
- Avoid common visualization errors: 3D charts, dual-axis charts (unless carefully justified), truncated y-axes that exaggerate differences, pie charts for more than 4–5 categories
- Design for accessibility: sufficient color contrast, not relying on color alone to encode meaning
- Know the four goals of data visualization: showing relationships, distributions, composition, and comparisons — and choose encoding accordingly

**Source:** [UX Collective on data visualization for research reporting]

---

### 6.3 Communicating Statistical Concepts to Non-Technical Audiences

**Expected depth:** Expert

**Required competencies:**
- Translate confidence intervals into plain language: "We're 95% confident the true completion rate is between 68% and 84%"
- Explain statistical significance without using the word "significant" alone — clarify "statistically significant" vs. "meaningfully different for product decisions"
- Use analogies and visual demonstrations rather than formulas for executive audiences
- Know when to lead with qualitative quotes to give life to quantitative findings — pairing a 72% completion rate with a representative user struggle clip increases organizational impact
- Build decision frameworks around data: "If completion rate is above X, proceed; if below Y, redesign; the uncertainty zone between X and Y requires additional research"

**Source:** [NN/G Quant Research in Practice](https://www.nngroup.com/articles/quant-research-practice/); industry job descriptions

---

### 6.4 Dashboards and Continuous Measurement

**Expected depth:** Awareness to Working knowledge [VARIES]

**Required competencies:**
- Build or co-design research dashboards that give product teams ongoing visibility into key UX metrics
- Define the update cadence and data pipeline requirements before building
- Distinguish instrumentation (what events are logged) from analysis (what those events mean)
- Know when a dashboard is the right output vs. a one-time report

---

## Domain 7: Ethics and Privacy

### 7.1 Informed Consent

**Expected depth:** Working knowledge

**Required competencies:**
- Obtain informed consent before collecting any data from human participants
- Consent must cover: study purpose (may be partially disclosed in deception designs, with post-study debrief), what data is collected and how it will be stored, whether recordings will be made, right to withdraw at any time without penalty, how data will be used (internal only vs. published), whether findings will be attributed to participants
- Use plain, accessible language — not legal jargon that participants cannot understand
- Keep consent documentation separate from study data to protect confidentiality
- Know that digital consent (checkbox, e-signature) is valid; it must be freely given, not coerced by gating compensation on consent

**Source:** [NN/G Informed Consent](https://www.nngroup.com/articles/informed-consent/); [Smashing Magazine Ethics in UX Research](https://www.smashingmagazine.com/2020/12/ethical-considerations-ux-research/)

---

### 7.2 Participant Privacy and Data Protection

**Expected depth:** Working knowledge

**Required competencies:**
- Understand GDPR requirements if handling data from EU residents: lawful basis for processing, explicit opt-in consent, right to erasure, data minimization principle, mandatory breach notification
- Understand CCPA/CPRA if handling data from California residents: opt-out rights, data deletion rights, category disclosure requirements, retention period specifications
- Apply data minimization: collect only what is necessary for the research question; do not retain raw participant data beyond its useful life
- Store participant data with appropriate access controls; do not share raw data containing PII with stakeholders
- Anonymize or pseudonymize data before analysis where possible
- Have explicit data retention policies for research recordings, transcripts, and survey responses

**Source:** [User Interviews GDPR Guide](https://www.userinterviews.com/blog/the-user-researchers-guide-to-gdpr); [GDPR for User Research - Consent Kit](https://consentkit.com/gdpr-for-user-research)

---

### 7.3 Vulnerable Populations and Sensitive Topics

**Expected depth:** Working knowledge

**Required competencies:**
- Recognize when participants belong to protected or vulnerable groups: minors, people with cognitive or psychiatric conditions, people in crisis, economically distressed individuals
- Know that special justification, additional safeguards, and potentially IRB or legal review are required for research with vulnerable populations
- Prepare emotionally for participants who disclose sensitive personal information — know how to handle unexpected disclosures professionally and compassionately
- Avoid research designs that could harm participants — including privacy harms from detailed behavioral tracking without adequate consent

**Source:** [Smashing Magazine Ethics in UX Research](https://www.smashingmagazine.com/2020/12/ethical-considerations-ux-research/)

---

### 7.4 IRB and Institutional Review

**Expected depth:** Awareness [VARIES — most industry UX research does not go through IRB, but academic or published research may require it]

**Required competencies:**
- Know what IRB review is and when it applies (research intended for publication, research with sensitive populations, federally funded research)
- Know that most internal product research does not require IRB — but the ethical principles underlying IRB (beneficence, justice, respect for persons from the Belmont Report) apply regardless
- Apply peer review of research protocols as a substitute for IRB in commercial contexts

**Source:** [Smashing Magazine Ethics in UX Research](https://www.smashingmagazine.com/2020/12/ethical-considerations-ux-research/)

---

## Domain 8: Commonly Expected but Often Overlooked Competencies

### 8.1 Survey Weighting

**What it is:** Applying statistical weights to correct for non-representative samples in survey data. When a sample over-represents certain demographic groups, raw aggregates are biased; weighting adjusts each respondent's contribution to reflect population proportions.

**Why it is overlooked:** Many practitioners use convenient but non-representative panels (e.g., UserTesting panels skew younger and more tech-savvy) without correcting for this. Reporting raw means from a non-representative sample as if they represent "all users" is a common validity error.

**Expected depth:** Working knowledge for senior roles

**Source:** [Carl J. Pearson on survey weights](https://carljpearson.com/why-you-should-use-survey-weights-in-ux-research/)

---

### 8.2 Instrumentation and Event Taxonomy Design

**What it is:** Working with engineers before product launch to define what events get logged, with what properties, at what granularity. Research questions can only be answered by data that was tracked.

**Why it is overlooked:** Many researchers inherit data without understanding its instrumentation — leading to misinterpretation of events that were not defined with research in mind.

**Expected depth:** Working knowledge for roles with analytics responsibilities

---

### 8.3 Psychometrics and Scale Validation

**What it is:** The science of measuring psychological constructs. Includes: item writing, factor analysis to assess dimensionality, reliability analysis (Cronbach's alpha, test-retest reliability), and criterion validity testing.

**Why it is overlooked:** Researchers often build custom survey instruments without validating them — treating untested Likert items as if they reliably measure the intended construct.

**Expected depth:** Working knowledge — especially for roles creating new measurement instruments

**Source:** [Sauro & Lewis Ch. 8 (Standard Usability Questionnaires)]; [Factor Analysis — MeasuringU](https://measuringu.com/wp-content/uploads/2022/02/Factor-Analysis.pdf)

---

### 8.4 Pre-Registration and Reproducibility

**What it is:** Documenting hypotheses, primary metrics, sample size plans, and analysis approach before data collection begins. Prevents post-hoc p-hacking and HARKing (Hypothesizing After Results are Known).

**Why it is overlooked:** Industry research culture rarely requires pre-registration; academic standards have not fully transferred to product research. However, leading tech companies (Google, Meta) increasingly apply pre-registration discipline to their experimentation pipelines.

**Expected depth:** Awareness broadly; Working knowledge at senior levels in data-mature organizations

---

### 8.5 Practical Significance and Effect Size Communication

**What it is:** Reporting not just whether a difference is statistically significant, but whether it is large enough to matter for product decisions — and communicating this to non-statistician stakeholders.

**Why it is overlooked:** Many practitioners report p-values and declare significance without computing or communicating effect sizes. A 3-point SUS improvement may be statistically significant with n=500 participants but represent no meaningful change in user experience.

**Expected depth:** Expert — this is one of the primary knowledge deficits observed in the field

**Source:** [MeasuringU Five Hard Quant Concepts](https://measuringu.com/five-hard-quant/); [Sauro & Lewis Ch. 9 (Controversies in Measurement and Statistics)]

---

### 8.6 Research Operations (ReOps)

**What it is:** The systems, processes, and infrastructure that enable research to scale efficiently: participant recruitment pipelines, consent management, research repositories, insight taxonomy, research planning processes, stakeholder communication cadences.

**Why it is overlooked:** Individual contributors often focus on study execution but do not invest in the systems that make research reusable and organizationally impactful.

**Expected depth:** Awareness broadly; Working knowledge at staff/principal level

**Source:** [NN/G Research Repositories](https://www.nngroup.com/articles/research-repositories/)

---

### 8.7 Connecting UX Metrics to Business Metrics

**What it is:** The ability to demonstrate the business value of UX improvements by linking usability metrics (completion rate, SUS, error rate) to business outcomes (conversion rate, customer support costs, churn, revenue). This is the mechanism by which UX research gains organizational influence.

**Why it is overlooked:** UX researchers are trained in user metrics but rarely trained in business case construction. The NN/G finding that 43% of organizations evaluate design success based on stakeholder satisfaction rather than actual measurement reflects this gap.

**Expected depth:** Working knowledge — required to influence product and business roadmaps

**Source:** [NN/G Quant Research in Practice](https://www.nngroup.com/articles/quant-research-practice/); NN/G "Measuring UX and ROI" course

---

### 8.8 AI and Automated Research Tools — Critical Evaluation

**What it is:** An emerging competency to evaluate when AI-assisted research tools (automated transcript analysis, AI-generated survey questions, AI-coded themes) introduce bias, reduce validity, or produce hallucinated findings.

**Why it is overlooked:** 80% of researchers use AI tools, but many lack a framework for assessing where AI assistance is safe vs. where it compromises research integrity.

**Expected depth:** Working knowledge — increasingly required as AI tools proliferate in research workflows

**Source:** [User Researcher Skills 2025 — Teal](https://www.tealhq.com/skills/user-researcher)

---

## Summary: Competency Priority Matrix

| Domain | Minimum bar (mid-level) | Senior / Staff bar |
|---|---|---|
| Usability testing (benchmarking) | Working knowledge | Expert |
| Surveys and screener design | Working knowledge | Expert |
| A/B testing | Awareness to Working knowledge | Working knowledge |
| Analytics and SQL | Working knowledge | Expert |
| Tree testing / card sorting | Working knowledge | Working knowledge |
| Core UX metrics (SUS, SEQ, NPS, completion, time) | Expert | Expert |
| HEART / GSM framework | Working knowledge | Expert |
| Confidence intervals and CIs for proportions | Working knowledge | Expert |
| Test selection (t-test, chi-square, Mann-Whitney) | Working knowledge | Expert |
| Sample size and power analysis | Working knowledge | Expert |
| Effect size and practical significance | Working knowledge | Expert |
| Between/within subjects + counterbalancing | Working knowledge | Expert |
| Mixed methods integration | Awareness | Working knowledge |
| Python or R for analysis | Awareness | Working knowledge |
| SQL for behavioral data | Working knowledge | Expert |
| Qualtrics | Working knowledge | Expert |
| Visualization and reporting | Working knowledge | Expert |
| Ethics, consent, GDPR/CCPA | Working knowledge | Working knowledge |
| Survey weighting | Awareness | Working knowledge |
| Psychometrics / scale validation | Awareness | Working knowledge |
| Regression / key driver analysis | Awareness | Working knowledge |
| Factor / cluster analysis | Awareness | Working knowledge |
| Research ops and repositories | Awareness | Working knowledge |
| Business metric linkage | Awareness | Working knowledge |

---

Sources:
- [Nielsen Norman Group: Quantitative UX Research Methods Overview](https://www.nngroup.com/articles/quantitative-user-research-methods/)
- [Nielsen Norman Group: Quant Research in Practice](https://www.nngroup.com/articles/quant-research-practice/)
- [Nielsen Norman Group: Mixed Methods Research](https://www.nngroup.com/articles/mixed-methods-research/)
- [Nielsen Norman Group: Triangulation](https://www.nngroup.com/articles/triangulation-better-research-results-using-multiple-ux-methods/)
- [Nielsen Norman Group: Informed Consent](https://www.nngroup.com/articles/informed-consent/)
- [Nielsen Norman Group: Research Repositories](https://www.nngroup.com/articles/research-repositories/)
- [Nielsen Norman Group: Measuring Perceived Usability (SEQ, SUS, NASA-TLX)](https://www.nngroup.com/articles/measuring-perceived-usability/)
- [MeasuringU: Measuring Usability with SUS](https://measuringu.com/sus/)
- [MeasuringU: 10 Benchmarks for UX Metrics](https://measuringu.com/ux-benchmarks/)
- [MeasuringU: Five Critical Quantitative UX Concepts](https://measuringu.com/five-hard-quant/)
- [MeasuringU: KDA, Cluster, and Factor Analysis (Sauro & Lewis, Google 2021)](https://measuringu.com/wp-content/uploads/2021/08/KDA_CA_FA_Google2021.pdf)
- [Sauro, 2015: SUS Item Benchmarks (UXPA Journal)](https://uxpajournal.org/wp-content/uploads/sites/7/pdf/JUS_Sauro_Feb2015.pdf)
- [Sauro & Lewis: Measuring Perceived Usability: SUS, UMUX-LITE (ResearchGate)](https://www.researchgate.net/publication/281161362_Measuring_Perceived_Usability_The_SUS_UMUX-LITE_and_AltUsability)
- [Sauro & Lewis: Quantifying the User Experience (Amazon)](https://www.amazon.com/Quantifying-User-Experience-Practical-Statistics/dp/0128023082)
- [Google Research: User-Centered Metrics for Web Applications (HEART Framework)](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/)
- [HEART Framework Reference Site](https://www.heartframework.com/)
- [Optimal Workshop: Tree Testing](https://www.optimalworkshop.com/tag/tree-testing)
- [Optimal Workshop: Card Sorting vs. Tree Testing](https://www.optimalworkshop.com/blog/card-sorting-vs-tree-testing-whats-the-best)
- [Optimal Workshop: Does First Click Matter?](https://blog.optimalworkshop.com/does-the-first-click-really-matter-treejack-says-yes/)
- [UXR Guild: Statistical Tests in UX Research](https://uxrguild.com/use-statistical-tests-ux-research/)
- [UXR Guild: Advanced Statistics in UX Research](https://uxrguild.com/using-advanced-statistics-ux-research/)
- [Carl J. Pearson: Learn Quantitative UX Research Self-Study Resources](https://carljpearson.com/learn-quantitative-ux-research-self-study-resources/)
- [Carl J. Pearson: Why Use Survey Weights in UX Research](https://carljpearson.com/why-you-should-use-survey-weights-in-ux-research/)
- [Counting Stuff: What's a Quantitative UX Researcher, 2025 Edition](https://www.counting-stuff.com/whats-a-quantitative-user-experience-ux-researcher-2025-edition/)
- [Amazon Sr. Quantitative UX Researcher Job Description](https://amazon.jobs/en/jobs/10382576/sr-quantitative-ux-researcher-applied-ai-solutions)
- [Citi UX Quantitative Researcher Job Description](https://jobs.citi.com/job/new-york/ux-quantitative-researcher/287/93528702816)
- [Smashing Magazine: Ethical Considerations in UX Research](https://www.smashingmagazine.com/2020/12/ethical-considerations-ux-research/)
- [User Interviews: GDPR Guide for User Researchers](https://www.userinterviews.com/blog/the-user-researchers-guide-to-gdpr)
- [GDPR for User Research — Consent Kit](https://consentkit.com/gdpr-for-user-research)
- [UXPA: Usability Body of Knowledge](https://uxpa.org/usability-body-of-knowledge-2/)
- [Bentley UX Center: MaxDiff Survey Analysis for Feature Prioritization](https://www.bentley.edu/centers/user-experience-center/how-use-max-diff-survey-analysis-feature-prioritization)
- [Looppanel: 35 Best UX Research Tools 2025](https://www.looppanel.com/blog/best-ux-research-tools)
- [Maze: UX Research Tools Guide](https://maze.co/guides/ux-research/tools/)
- [DeveloperUX: How to Identify and Fix Survey Bias in UX Research](https://developerux.com/2025/03/05/how-to-identify-and-fix-survey-bias-in-ux-research/)
- [Fuzzy Math: Using SUPR-Q as a Design Metric](https://fuzzymath.com/blog/suprq-design-metric/)
- [Teal: User Researcher Skills 2025](https://www.tealhq.com/skills/user-researcher)
