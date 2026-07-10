# Triangulation and Mixed Methods — S3 Reference

This file supports the QRA's S3 recommendation when a team is running both quantitative and qualitative work, or when the QRA must decide whether quant adds value to a planned qual study. For method-specific data and statistics, see `09_ux_research_methods.md` and `04_statistical_methods.md`.

---

## Why Triangulation Matters

Neither quant nor qual is sufficient alone for most design questions.

- Quant tells you how many users are affected and whether a difference is real.
- Qual tells you why something is happening and what mental models or contextual factors drive behavior.
- Triangulation builds a more complete, defensible picture — and surfaces when methods disagree (which is often the most interesting finding).

The goal is not to confirm that both methods say the same thing. The goal is to answer the research question with greater confidence and nuance than either method could achieve alone.

---

## Four Triangulation Patterns

### 1. Convergent Validation

**When to use**: you have a qualitative finding (theme, pattern, model) and you want to know how prevalent it is in the broader population, or whether it is statistically significant.

**Logic**: quant and qual address the same question in parallel or sequence, then findings are compared.

**Example**: moderated sessions reveal that three distinct mental models drive checkout abandonment. A follow-up survey includes items operationalizing each model. Analysis shows Model B accounts for 62% of abandoners — confirming its prevalence and prioritizing it for design attention.

**What convergence means**: when both methods point in the same direction, confidence in the finding increases substantially. You can now say both "we observed this behavior and heard this reasoning" and "this pattern affects a measurable proportion of users."

**What convergence does NOT mean**: that the finding is necessarily causal, universal, or actionable without further context.

**Important caveat on convergence**: convergence between methods increases confidence only if the two methods have independent error structures. If both methods share the same systematic bias — for example, both the survey and the usability test used the same leading framing, or both were administered by the same researcher whose enthusiasm for one design was visible — then convergence may reflect shared error rather than truth. Before concluding that convergence validates a finding, ask: could both methods be wrong in the same direction for the same reason? If the answer is yes, convergence adds less to your confidence than it appears to.

---

### 2. Explanatory (Quant → Qual)

**When to use**: you have a quantitative anomaly or result you cannot explain from the data alone.

**Logic**: quant first establishes the what; qual follows to explain the why.

**Example**: A/B test shows Variant B has 12% lower task completion than Variant A. The difference is statistically significant (Chi-square, p = 0.003) but the behavioral log data does not reveal where users are dropping off. Follow-up moderated sessions reveal that a new label in Variant B contradicts users' existing mental model — they interpret it as a different section of the product.

**Key sequence**: run quant → analyze results → identify the anomaly or unexplained pattern → design qual study specifically targeted at that pattern. The qual probe should be tightly scoped; do not run open-ended discovery when you have a specific quant finding to explain.

---

### 3. Exploratory (Qual → Quant)

**When to use**: you are in early research phases and do not yet have specific hypotheses. Qual generates the hypotheses; quant tests them at scale.

**Logic**: qual first surfaces themes, pain points, or mental models → quant study is designed around those specific themes to measure prevalence and significance.

**Example**: contextual inquiry sessions with 8 users identify three navigation strategies for finding account settings. The team cannot tell which strategy is most common or which predicts success. A tree test with 60 participants, designed around the three strategies identified in the sessions, measures which path is most used and which produces the highest success rate.

**What this prevents**: designing a quant study around the wrong variables because no one checked whether those variables were meaningful to users first.

---

### 4. Discordant Findings

**When to use**: you run both methods and they disagree.

**What discordance looks like**: the survey shows high satisfaction (SUS = 82), but moderated sessions consistently surface significant frustration with a specific workflow. Or a tree test shows high success rates, but moderated users verbally express confusion about the same navigation structure.

**What discordance means**: do NOT average the findings. Do NOT suppress the conflict. Do NOT default to whichever method you trust more.

**Investigate the source of divergence**:
- Are the methods measuring the same construct? (SUS measures overall perceived usability — moderated sessions may be surfacing a specific workflow issue that doesn't dominate overall satisfaction.)
- Are the populations the same? (Panel survey respondents may differ systematically from recruited moderated participants.)
- Are the tasks or contexts the same? (Tree test success may reflect the test environment; moderated sessions reflect a more realistic context.)
- Is there a timing difference? (One method may reflect a prior version; the other a current one.)

**When discordance is the finding**: if two valid methods persistently disagree after investigating the above, that IS the finding. Report it as: "Quantitative benchmarking indicates [X]; qualitative sessions suggest [Y]. These patterns may reflect [specific methodological difference or population characteristic]. We recommend [additional investigation or design team judgment call]."

---

## Common Mixed-Methods Study Structures

### Structure 1: Qual First → Quant at Scale

**Pattern**: discovery interviews or contextual inquiry → survey benchmark or tree test.

**When to use**: early in a design cycle, before a defined research question exists. Qual scopes the problem; quant measures prevalence.

**Coordination**: the quant study is designed after (not during) the qual phase. Allow time for qual analysis before finalizing quant instruments. Budget: qual typically 2–4 weeks; quant instrument design and fielding 2–4 more weeks.

**Common mistake**: rushing the quant instrument into the field before the qual data is analyzed — this defeats the purpose of the sequence.

---

### Structure 2: Quant First → Qual to Explain

**Pattern**: analytics anomaly, A/B test result, or survey benchmark → moderated sessions.

**When to use**: you have a metric that is underperforming and you need to understand why before designing a fix.

**Coordination**: the qual study must be scoped around the specific quant finding. Do not run open-ended sessions — run targeted sessions with tasks that mirror the quant study's failing scenarios.

**Output**: the quant result sets the stakes ("22% of users fail to complete checkout"); the qual provides the explanation ("three specific mental model mismatches drive the failure, each requiring different design solutions").

---

### Structure 3: Concurrent

**Pattern**: quant survey and moderated sessions run simultaneously.

**When to use**: when timeline constraints prevent sequencing, or when the team wants both prevalence data and explanatory depth from the same study period.

**Coordination requirements**:
- Screener criteria must be identical across both studies.
- Participants should not overlap (if a person does the survey and a moderated session, their survey data may be influenced by the moderated experience or vice versa).
- Analysis order: analyze each method independently before comparing findings. Do not let early qual findings bias quant analysis coding.

**Risk**: concurrent design sacrifices the ability to let one method inform the other. You get breadth and depth simultaneously but lose the iterative refinement advantage of sequencing.

---

## What Quant Can and Cannot Do

### Quant can:
- Measure the prevalence of a behavior or attitude in a defined population.
- Test whether a difference between two conditions is statistically significant.
- Benchmark a metric against a published norm or a prior measurement.
- Detect which A/B variant performs better on a defined outcome.
- Quantify how much a metric changed over time.
- Provide evidence that a problem is widespread, not just present.

### Quant cannot:
- Explain why a pattern exists.
- Reveal mental models, user goals, or contextual factors.
- Surface unknown problems (quant can only measure what you thought to measure).
- Capture nuance, edge cases, or workarounds users have invented.
- Tell you what to design — only whether a design change achieved a measurable effect.

---

## What Qual Can and Cannot Do

### Qual can:
- Explain the why behind a behavioral pattern.
- Surface problems the team hadn't anticipated measuring.
- Reveal mental models, user expectations, and contextual factors.
- Generate hypotheses for future quant testing.
- Capture nuance, emotional response, and language users use.

### Qual cannot:
- Establish prevalence (n = 8 sessions does not tell you how many of your 2 million users are affected).
- Test statistical significance of a difference.
- Benchmark against a norm.
- Confirm that a finding is representative of the population.
- Replace a power-analyzed confirmatory study when a high-stakes decision requires statistical evidence.

---

## Setting Expectations with the Design Team

Use these frames when the team conflates the two methods or expects one to do the other's job.

**If the team says "our qual sessions found users hated X — we don't need a survey":**
"The sessions tell us why users struggled with X, and that's valuable. What they can't tell us is how widespread that struggle is — whether it affects 5% or 50% of your users. If that number changes the priority or the business case, a benchmark survey will answer it. If the team is already aligned on fixing X regardless of prevalence, the survey may not add value."

**If the team says "the A/B test said B won — we're done":**
"The test tells you B outperformed A on [specific metric] with statistical confidence. It doesn't tell you why — which means you can't reliably extend the design principle to other parts of the product. A quick round of moderated sessions on the winning variant would give the team the mental model behind the result."

**If the team says "we ran a survey and got an 80 SUS — our users are happy":**
"SUS measures overall perceived usability, so an 80 is good context. But SUS doesn't surface which specific tasks or flows are dragging that number down, and it doesn't capture users who abandoned before completing the study. Pairing the SUS score with SEQ task-level ratings and a session or two focused on the lowest-rated tasks would give you something actionable."

---

## Presenting Mixed-Method Findings to a Design Team

### Lead with the design question, not the method

Wrong: "Our one-sample t-test against the SUS norm of 68 showed t(34) = 2.4, p = 0.02, and the tree test produced 64% success rates with Wilson CIs of [57%, 71%]."

Right: "We have two signals that the account navigation needs work. Users are finding it harder to use than industry average — SUS scored 61, below the 68 benchmark. And the tree test confirmed that only 64% of users can locate Account Settings on their first try, with many going to the wrong section before correcting course."

### Integrate, don't sequence

Don't present quant findings in one section and qual findings in another. Integrate them around each design question.

Template: "[X% of participants] struggled with [this step] [quant], and in the sessions we observed [specific pattern or model] driving that confusion [qual]. Together, these findings suggest [design implication]."

### Name conflicts, don't suppress them

If quant and qual point in different directions, state that explicitly. Suppressing methodological conflict produces misleading findings and undermines the team's ability to make a well-calibrated decision.

"The SUS score suggests overall perceived usability is near average (score: 67). At the same time, sessions consistently surfaced significant frustration with the reporting workflow — a pattern that may not dominate the SUS score because it affects a specific user segment. We recommend a task-level SEQ study focused on reporting to measure whether that segment's experience is dragging the aggregate."

### Avoid p-values and test names in design team readouts

In the findings document or presentation for a design team:
- Translate "p < 0.05" to "this difference is unlikely to be due to chance."
- Translate "Mann-Whitney U, p = 0.02" to "users on mobile took significantly longer on this task than desktop users."
- Reserve statistical notation for the appendix or the analysis plan document — not the main finding narrative.

---

## QRA Reasoning Guide: Does Quant Add Value Here?

Use this logic at S3 to decide whether to recommend quant-only, qual-only, or both.

### Recommend quant-only when:
- The research question is well-specified and can be directly operationalized without a qualitative foundation — either because you have a clear hypothesis from prior work or because existing product knowledge defines the constructs precisely.
- Prior qualitative work has already established the constructs to measure and the team is moving to validation or prevalence estimation at scale.
- Timeline and budget preclude a qual component.
- The decision is high-stakes enough to require statistical confidence, not just directional evidence.

**Important**: do NOT recommend quant-only as the starting point for early-stage or exploratory research questions. The absence of prior qualitative work is precisely the condition that calls for qual first — to identify what is worth measuring before committing to an instrument. Starting with quant in exploratory contexts means measuring the wrong things with high statistical confidence.

### Recommend qual-only when:
- The team does not yet know what questions to ask quantitatively.
- The research goal is generative (discover what problems exist) rather than evaluative (confirm a specific problem is widespread or fixed).
- The expected N for quant is too small to power any reasonable statistical test.
- The construct is too nuanced or contextual to operationalize in a survey or unmoderated task.

### Recommend both when:
- The team has qual themes that need prevalence data before prioritization decisions.
- A quant anomaly needs an explanatory follow-up.
- Stakeholders require statistical evidence AND the team needs to understand what's driving the pattern.
- The decision will affect a large user population and warrants both rigor and depth.

### Recommend quant as primary, qual as secondary when:
- The core deliverable is a benchmark score or a significance test result.
- Qual will be used to add color and explain anomalies but will not change the primary finding.
- Label the primary study explicitly: "The tree test is the confirmatory study. The three follow-up moderated sessions are exploratory and will inform design iteration — they are not confirmatory."

### Recommend qual as primary, quant as secondary when:
- The team is in early discovery and needs to understand the problem space before they can write valid survey items or design a tree test.
- Quant will be used to validate prevalence of specific themes, not to answer the core research question.
- Label accordingly: "The discovery interviews are the primary study. The follow-up benchmark survey will measure prevalence of the three themes we identify."
