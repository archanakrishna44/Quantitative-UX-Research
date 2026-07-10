# Reporting Standards

## UX Research Reporting

This section covers how to report findings in the register the design team actually uses. Lead with the design question, not the statistical machinery. Numbers and methods belong in the report; the design team readout leads with meaning.

### Reporting SUS Findings

Include: score + percentile + grade + CI + comparison to norm or prior benchmark.

Example format:
> "The product scored 74.5 (SD = 12.3, n = 52), placing it at the 70th percentile relative to published SUS norms. The 95% CI [71.1, 77.9] falls above the 68-point average benchmark and does not overlap it, indicating a statistically meaningful advantage over the industry average. This corresponds to a 'Good' rating on the Bangor/Brooke grading scale."

Key requirements:
- Always report the mean with SD and N together — never a bare number.
- Report the CI. A score of 74 with CI [70, 78] is much more informative than a bare 74.
- State whether the CI overlaps the norm or prior score. Non-overlap is the practical significance test. **Important**: non-overlapping 95% CIs do imply p < .05, but OVERLAPPING 95% CIs do NOT imply non-significance. Two group CIs can overlap by up to approximately 25% and the difference can still be statistically significant at p = .05. For significance testing, run the test — do not rely on visual CI overlap alone.
- Reference the percentile from the normative database (Sauro & Lewis benchmarks are widely cited). Percentile is more intuitive for design teams than the raw score.
- If comparing to a prior study's SUS score: run an independent t-test (two different samples) or a one-sample t-test (compare your sample mean to the prior study's score as a known value). Report the test statistic and the difference in points.

### Reporting Task Completion Rate

Include: proportion + Wilson CI + comparison to benchmark or other condition.

Example format:
> "Task 2 completion rate was 62% (95% CI [49%, 74%]), below the 78% industry benchmark for this task type. The CI does not overlap the benchmark, indicating this is a meaningful gap. Task 1 and Task 3 completion rates were 84% and 79% respectively — both within acceptable range."

Key requirements:
- Report Wilson CIs, not Wald CIs (see `04_statistical_methods.md`).
- State the comparison point (benchmark, prior study, other variant) explicitly.
- Present completion rates for all tasks in a table — individual tasks in isolation are hard to interpret.
- If comparing two variants: report the difference in percentage points with a CI for the difference and a χ² or z-test result.

### Reporting A/B Test Results

Include: metric for each variant + difference in percentage points + CI for the difference + test statistic + p-value + effect size.

Example format:
> "Variant B increased checkout completion from 34% to 41%, a difference of 7 percentage points (95% CI [2pp, 12pp], χ²(1) = 5.8, p = .016, h = 0.14). This is a statistically significant result. The effect size (h = 0.14) is small by Cohen's conventions, but a 7pp lift on checkout completion represents meaningful business impact given the volume of transactions."

Key requirements:
- Lead with the metric and the practical change (percentage point difference), not the p-value.
- Report both the absolute difference (pp) and the effect size (Cohen's h for proportions).
- Interpret the effect size in context — small h does not mean unimportant if the base rate is high and the volume is large.
- State clearly whether the result supports a causal claim (if it was a valid randomized A/B test) or an associational finding.
- For continuous outcomes (time-on-task, engagement score): report means for each group, the difference, CI for the difference, t-statistic, p-value, and Cohen's d.

### Reporting Tree Test Results

Present success rate and directness together for each task in a table.

Example format:

| Task | Success Rate | 95% CI | Directness | 95% CI | Interpretation |
|---|---|---|---|---|---|
| Find account settings | 82% | [72%, 89%] | 74% | [63%, 83%] | Strong — minor indirect paths exist |
| Cancel subscription | 54% | [44%, 64%] | 41% | [31%, 52%] | Findability problem — both success and directness are low |
| Update payment method | 71% | [61%, 80%] | 68% | [58%, 77%] | Acceptable success; directness near parity — path is reasonably clear |

Key requirements:
- Always report both success rate and directness — not just one.
- Use Wilson CIs for all proportions.
- Include an interpretation column or note. Raw numbers without interpretation make tree test results hard to act on.
- If comparing two tree structures: report the difference in success rates with a CI and a two-proportion test.
- Flag tasks below 70% success rate as needing attention; flag tasks where success >> directness as misleading-label candidates.

---

## Design Team Readout

When presenting findings to a design team, product manager, or non-statistical stakeholder, do not lead with p-values, test names, or effect size indices. Use this structure instead:

1. **The design question**: restate what the study was trying to answer. "We wanted to know whether users could find subscription management in the new navigation structure."

2. **The finding in plain language**: state what the data shows, directly. "They mostly could not. Only 54% successfully found the cancellation path, well below the 80% threshold we set as acceptable."

3. **The number**: present the key metric with its uncertainty. "54% success rate (95% CI [44%, 64%])." One number, with confidence. Not a table of statistics.

4. **The confidence**: state how certain you are. "The CI does not include 80%, so we can say with confidence this is a real problem, not noise."

5. **The recommendation**: translate directly to a design action. "The label 'Account Options' is not working as an entry point for subscription management. We recommend testing a direct 'Subscription' label or elevating the link to the primary navigation."

**What p-values and test names should do in a design team context**: they should live in a Methods appendix or supporting documentation, not in the lead of a presentation. If a stakeholder asks "how confident are you?", the CI answers that question in plain language. If they ask "was it statistically significant?", answer yes/no and move on — do not walk through the test mechanics in the readout.

**When to break this rule**: if the research is being documented for a publication, an evidence repository, or a formal decision record, include full statistical reporting in the document body. Use your judgment about who the primary audience is.

---

## Formal Documentation and Academic Reporting

APA 7 statistical notation is appropriate for any formal write-up — including internal research documents — because it makes findings unambiguous and auditable. However, full APA manuscript formatting (running heads, abstract structure, reference list in APA style) is for academic publication only. For internal research repositories (Confluence, Notion, Dovetail, Google Drive): use the statistical reporting checklist below as your standard. Write in plain prose, not academic paper structure. The goal is clear, auditable reporting — not importing journal conventions into product documentation.

Apply the APA 7 conventions below when writing formal study documentation, evidence library entries, or any output intended for a research repository, publication, or external audience.

### APA 7 Statistical Reporting

#### General Rules
- Report exact p-values to 2–3 decimal places: p = .043, not p < .05.
- Exception: very small p-values reported as p < .001.
- Do not use a leading zero before the decimal for values bounded at 1 (r, p): r = .45, p = .032.
- Use a leading zero for values that can exceed 1 (means, SDs, Cohen's d): M = 0.45, d = 0.72.
- Always report effect sizes and confidence intervals alongside significance tests.
- Report degrees of freedom in parentheses: t(58) = 2.34.

#### Formatting Specific Statistics

**t-test**: t(df) = value, p = value, d = value, 95% CI [lower, upper]
Example: t(58) = 2.34, p = .023, d = 0.60, 95% CI [0.08, 1.12]

**F-test (ANOVA)**: F(df_between, df_within) = value, p = value, ω² = value
Example: F(2, 87) = 4.56, p = .013, ω² = .08

**Chi-square**: χ²(df, N = n) = value, p = value, V = value
Example: χ²(1, N = 120) = 5.43, p = .020, V = .21

**Correlation**: r(df) = value, p = value, 95% CI [lower, upper]
Example: r(98) = .34, p = .001, 95% CI [.15, .51]

**Regression**: Report R², adjusted R², F for model significance, then for each predictor: B (unstandardized), SE, β (standardized), t, p, 95% CI for B.

**Mann-Whitney U**: U = value, p = value, r = value (rank-biserial correlation)

#### Tables
- Every table needs a number and descriptive title above it.
- Notes below explain abbreviations, significance levels.
- Do not use vertical lines; minimize horizontal lines (APA style).

#### Figures
- Every figure needs a number and descriptive caption below it.
- Include error bars; label what they represent (SD, SE, 95% CI).
- Use colorblind-friendly palettes.

### Result Interpretation Language

#### What to say
- "The difference was statistically significant": t(58) = 2.34, p = .023.
- "The data are consistent with H1."
- "We observed a medium-sized effect (d = 0.60)."
- "Group A scored higher than Group B, on average (M_A = 4.2, SD = 0.8 vs. M_B = 3.7, SD = 0.9)."

#### What NOT to say
- "We proved that X causes Y" (unless RCT with manipulation).
- "The results confirm our hypothesis" (replication confirms; one study is consistent with).
- "There was no effect" (a non-significant result is not evidence of no effect; say "we did not find evidence of an effect").
- "Almost significant" (p = .06 is not significant at α = .05; do not hedge).
- "Highly significant" (avoid qualitative intensifiers on p-values).

### Sections of a Quantitative Research Report

#### Method
1. **Participants**: N, demographics, recruitment method, inclusion/exclusion criteria, attrition if applicable.
2. **Design**: design type, IVs, DVs, covariates, number of conditions.
3. **Materials/Instruments**: name of each measure, source, reliability (α or ω), validity evidence.
4. **Procedure**: chronological description of what participants did.

#### Results
1. Preliminary analyses: data quality, descriptives, assumption checks.
2. Primary analysis: pre-registered test, effect size, CI, interpretation.
3. Secondary analyses (clearly labeled).
4. Exploratory analyses (clearly labeled as exploratory, not confirmatory).

#### Discussion
1. Restate the research question and summarize the finding (not the statistics).
2. Relate to prior literature.
3. Limitations (design, sample, measurement — be honest).
4. Practical implications.
5. Future directions.

#### Limitations Section — Must Include
- Sample characteristics and limits to generalization.
- Whether the design supports causal inference.
- Measurement limitations (self-report, single-method).
- Any deviations from the pre-registered analysis plan.
- Statistical power if the primary result was non-significant.

### Reproducibility Appendix (include in all formal reports)
- Software and version: Python 3.11, pandas 2.1, scipy 1.11, statsmodels 0.14.
- Random seed used.
- Script file paths.
- Data availability statement (anonymized data location or access restrictions).
- Any manual data cleaning steps performed outside scripts.

---

## Data Visualization for UX Research Reporting

### Chart Type Selection

- **Bar charts**: for categorical comparisons (e.g., task completion rates across tasks, SUS scores by user segment). Bars must start at 0 — a truncated y-axis on a bar chart visually distorts the magnitude of differences.
- **Line charts**: for trends over time (e.g., NPS over quarters, retention curves). Truncation may be acceptable when showing change but must be labeled clearly (e.g., "y-axis starts at 60 to show change over time").
- **Scatter plots**: for correlations between two continuous variables (e.g., SUS vs. task completion rate). Always produce a scatter plot before reporting any correlation.
- **Forest plots**: for presenting multiple effect sizes with CIs side by side — useful when comparing results across tasks, segments, or studies. The horizontal layout with CI bars makes pattern recognition faster than a table.
- **Avoid pie charts** for more than 3 categories — human perception of area and angle is unreliable, and bar charts communicate the same information more accurately.
- **Avoid 3D charts, drop shadows, and decorative elements** that distort perception of values — these are visual noise that reduces accuracy of reading.

### Error Bars

- Always label what error bars represent. Options: 95% CI, SD, or SE. Unlabeled error bars are uninterpretable.
- **Use 95% CI as the default in research reporting** — it conveys the uncertainty range most relevant to inference.
- Never report SE bars without labeling them. SE bars are narrower than 95% CI bars by approximately half, which makes results appear more precise than they are. Many readers will mistake SE for CI if unlabeled.

### Truncated Axes

- Never truncate the y-axis on bar charts. Bars that do not start at zero visually inflate differences and mislead readers about effect size.
- For line charts showing change over time, truncation may be acceptable when the absolute range of values is narrow and the goal is to show change — but label the truncation explicitly (e.g., mark the axis break clearly).

### Color

- Use colorblind-friendly palettes. Recommended: Okabe-Ito palette (safe for the most common forms of color blindness), ColorBrewer sequential/diverging palettes.
- Never use red and green as the only differentiator between two conditions — this is invisible to protanopes and deuteranopes (approximately 8% of males).
- Ensure sufficient contrast between colors and background for accessibility. Test with a contrast checker.

### Labeling

- Label data points directly where possible rather than relying on legends. Direct labels reduce the cognitive load of legend-lookup and reduce misidentification.
- Write chart titles as findings, not descriptions. "Task 2 completion rate was below benchmark" is more useful than "Bar chart of completion rates." The title should convey the insight.
- Label axes with full variable names and units (e.g., "SUS Score (0–100)", "Time-on-Task (seconds)"), not variable codes.

---

### Reporting Checklist
- [ ] N reported at each analysis step (listwise deletion reduces N — report it).
- [ ] Effect size reported for every inferential test.
- [ ] 95% CI reported for primary effect.
- [ ] Assumption checks described.
- [ ] Multiple comparisons correction applied and stated.
- [ ] Deviations from pre-registered plan disclosed and justified.
- [ ] Limitations section present.
- [ ] Reproducibility appendix present.
- [ ] All charts start y-axis at 0 (bar charts) or truncation is labeled (line charts).
- [ ] Error bars are labeled with what they represent (95% CI, SD, or SE).
- [ ] Colorblind-friendly palette used.
