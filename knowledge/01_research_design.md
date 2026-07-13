---
scope: reference
modifies_workflow: false
---

# Research Design

## UX-Specific Design Decisions

Before choosing any design, answer these four questions. The answers drive everything else.

### 1. Attitudinal vs. Behavioral Research
- **Attitudinal**: what people say — satisfaction, perceived ease, preferences, intent. Measured via surveys, scales (SUS, UMUX-Lite, SEQ), and rating questions.
- **Behavioral**: what people do — task completion, navigation paths, click patterns, time-on-task, error rates. Measured via task-based studies, tree tests, first-click tests, analytics.
- Most studies benefit from layering both. A benchmark study that only collects SUS scores is missing the behavioral story. A tree test that reports success rates without a satisfaction check may miss the "right answer, wrong feeling" problem.

### 2. Within- vs. Between-Subjects for UX Studies
- **Between-subjects**: participants see only one condition (e.g., one navigation variant). Avoids carryover and learning effects. Requires more participants. Default for A/B testing.
- **Within-subjects**: participants experience multiple conditions (e.g., two card sort structures). More power with fewer participants. Risk of order effects — counterbalance the condition order. Good for preference comparisons when exposure to one design does not contaminate reaction to the next.
- Rule of thumb: if seeing design A would teach someone how to use design B, use between-subjects. If the two conditions are sufficiently independent, within-subjects is more efficient.

### 3. Moderated vs. Unmoderated
- **Moderated**: a researcher observes the session live or asynchronously with follow-up. Higher fidelity, richer qual layer, smaller N. Cannot scale to statistical power for most quant outcomes.
- **Unmoderated remote**: participants complete tasks independently on a platform (UserTesting, Maze, Optimal Workshop). Scales to quant-appropriate N (50–200+). Loss of observational depth. Requires airtight task wording — there is no one to clarify confusion.
- Quant benchmarking and tree testing are almost always unmoderated. Moderated sessions feed qual findings; they do not stand alone as quant evidence.

### 4. Benchmark vs. Comparative
- **Benchmark**: one design measured against a norm or prior score. Answers "how are we doing?" Use for tracking over time, hitting a product quality threshold.
- **Comparative**: two or more designs measured head-to-head. Answers "which is better?" Use for design decision points, A/B test interpretation, navigation variant selection.
- These require different power calculations. Comparative studies need more participants because you are detecting a difference, not just estimating a mean.

### 5. When a Quant Study Is Not Warranted (Qual-Only Path)
Go qual-only when:
- The research question is "why" or "how" — quant can tell you that something is broken but not why.
- N constraints make any quant result statistically unstable (N < 20 for most inferential tests).
- You are in early discovery and do not yet have a testable interface or prototype.
- The primary deliverable is a hypothesis or design brief, not a decision between defined options.
- The team already has clear directional data and needs depth, not confirmation.

Flagging the qual-only path is part of the QRA's job at S2/S3. Do not run a quant study to justify a decision that would be better served by five moderated sessions.

---

## UX Study Design Tradeoffs

| Study Type | What It Measures | Key Tradeoff | Minimum N |
|---|---|---|---|
| A/B test | Behavioral metric difference between two variants | Needs traffic/scale; week+ runtime to avoid novelty effects | Power-calculated (see 02_sampling) |
| Tree testing | Findability of information in a navigation structure | Fast and scalable; measures labels + hierarchy, not full UI | 50+ per variant |
| First-click testing | Whether users click the right place first | Good predictor of task success; not a full task test | 50–100+ per variant |
| Card sorting (open) | How users mentally group content | Generates IA hypotheses; dendrogram needs clean interpretation | 15–20 |
| Card sorting (closed) | Whether users can place items in predefined categories | Validates or challenges a proposed IA | 20–30+ for subgroup comparison |
| Survey benchmarking | Perceived usability, satisfaction, NPS, CSAT | Self-report bias; need N≥40 for reliable estimates, N≥100 to detect vs. norm | 40+ minimum, 100+ preferred |
| Analytics study | Behavioral patterns in existing product logs | No causal inference; correlation only; selection effects everywhere | Depends on event volume |
| Unmoderated task testing | Task completion, time-on-task, error rate | No probing; task wording is critical; use pilot to catch wording problems | 100–200 for stable proportions |

---

## Core Design Types

### Experimental
- **True experiment**: random assignment to conditions; strongest for causal inference.
- **Between-subjects**: different participants in each condition. Avoids carryover; requires larger N.
- **Within-subjects (repeated measures)**: same participants in all conditions. More power, smaller N; risk of order/carryover effects — use counterbalancing.
- **Factorial**: two or more IVs crossed; tests main effects and interactions.
- **Mixed design**: at least one between and one within factor.

### Quasi-Experimental
- No random assignment; researcher manipulates IV but cannot control group membership.
- Examples: pre-post with comparison group, interrupted time series, regression discontinuity.
- Weaker causal claims than true experiments; must address selection bias explicitly.
- In UX contexts: most commonly relevant for analytics-based studies where you cannot randomize (e.g., a feature rolled out to a cohort before quant was involved).

### Observational
- No manipulation. Researcher measures variables as they occur.
- **Cross-sectional**: one time point; fast, cheap; cannot establish temporal order.
- **Longitudinal / panel**: same participants over time; can establish temporal precedence; attrition is a threat.
- **Note**: epidemiological designs (case-control, cohort study in the clinical sense) are outside UX scope. If you encounter this framing, it maps loosely to retrospective observational and prospective panel designs respectively — but UX quant work rarely needs this framing.

---

## Triangulation Design

Triangulation means layering methods so that findings from one approach can be confirmed, extended, or complicated by another. In UX quant work, the most useful form is **quant over qual**: run qual first to understand what matters, then design quant to measure it at scale.

**What the QRA reasons about at S3 when designing a triangulated study:**

1. **What does the qual layer tell us to measure?** Qual findings should directly inform the choice of quant outcomes (e.g., if moderated sessions reveal that users fail to find the Settings page, tree testing is the right quant follow-up — not a SUS survey).

2. **Are the methods measuring the same construct?** Attitudinal quant (SUS) does not confirm behavioral qual findings (observed task failure). Layer carefully. A SUS score of 72 and a 55% task completion rate are telling different parts of the same story — not the same story twice.

3. **What is the convergence/divergence plan?** Before collecting data, state: if quant and qual findings agree, the conclusion is X. If they diverge, the follow-up question is Y. Divergence is often the most informative result.

4. **Sequence matters**: qual → quant → qual is stronger than quant alone. If the timeline only allows one method, qual is usually better for early-stage work; quant for decision-stage work.

5. **At S3, flag to the team** whether the planned study is a standalone quant benchmark, a quant-over-qual triangulation, or a quant-only comparative. This sets expectations for what the results can and cannot answer.

---

## Bias Identification and Mitigation

The following biases are structural threats to UX research validity. Each must be considered at S3 during study design. Unaddressed biases do not disappear — they become confounds in your data.

| Bias | What It Is | When It Threatens UX Research | Practical Mitigation |
|---|---|---|---|
| Social desirability bias | Participants respond in ways they believe are expected or socially acceptable rather than honestly. | Post-task satisfaction surveys, any attitudinal measure administered by a researcher. Inflates SUS and NPS scores in moderated contexts. | Use unmoderated data collection for attitudinal measures; administer scales asynchronously rather than in front of a researcher. |
| Acquiescence bias | Tendency to agree with statements regardless of content ("yes-saying"). | Likert scales with predominantly agree/disagree formats; scales without reverse-scored items. | Include reverse-scored items in attitudinal scales (SUS does this by design). Use balanced agree/disagree formats. |
| Recency/primacy bias | Participants' recall and ratings are disproportionately influenced by items presented first (primacy) or last (recency) in a list or session. | Post-session SUS administered after multiple tasks; multi-item surveys; card sorts. | Randomize item order where possible; administer SEQ after each task rather than at session end. |
| Demand characteristics | Participants infer the study's hypothesis and adjust behavior to confirm it. | Moderated sessions where researcher enthusiasm for one design is visible; A/B tests where variant purpose is obvious. | Use neutral task wording; blind moderators to hypotheses where possible; use unmoderated studies for behavioral outcomes. |
| Anchoring | First piece of information encountered disproportionately influences subsequent judgments. | Comparative studies where one design is always shown first; surveys with an introductory example that sets a scale reference point. | Counterbalance condition order in within-subjects designs; avoid providing scale anchors before participants form their own judgment. |
| Survivorship bias | Analysis based only on participants who completed the study, ignoring those who dropped out. | Unmoderated task studies with high dropout; longitudinal studies; funnel analytics. | Report completion rate and test whether dropouts differ from completers on key variables; use intention-to-treat analysis. |
| Sampling bias | The recruited sample systematically differs from the target population in ways that affect the outcome. | Any study using convenience sampling, panel platforms, or in-product intercepts; studies that over-recruit easy-to-reach user segments. | Define the target population precisely at S3; use purposive or quota sampling with transparent description of how the sample was recruited; explicitly qualify generalizability claims. |
| Leading question bias | Question wording that implies an expected or desired answer, nudging participants toward a particular response. | Task instructions that echo interface labels; survey questions phrased as "how easy was it to...?" instead of "how difficult or easy was it...?"; screener questions that reveal the desired answer. | Use goal-oriented task wording that does not echo interface labels; pilot-test survey questions for neutrality; have a colleague blind to the study's hypothesis review all question wording. |

---

## Validity Threats

| Validity Type | What It Means | Common Threats |
|---|---|---|
| Internal | Does IV cause DV in this study? | History, maturation, regression to mean, selection bias, attrition |
| External | Do findings generalize? | Convenience sample, WEIRD populations, lab vs. field |
| Construct | Do measures capture intended constructs? | Demand characteristics, mono-operation bias, method variance |
| Statistical conclusion | Are statistical inferences correct? | Low power, violated assumptions, fishing/p-hacking |

---

## Choosing a Design

1. Is the research question attitudinal or behavioral (or both)? → Select measures accordingly.
2. Is random assignment feasible? → Yes: experiment / A/B test. No: quasi-experimental or observational.
3. Is temporal order needed? → Yes: longitudinal or experiment. No: cross-sectional acceptable.
4. Is causation claimed? → Must have random assignment or a credible causal identification strategy.
5. What is the feasible N? → Small N favors within-subjects or qual-only path.
6. Is a quant study warranted at all? → If not, say so at S3.

## A Note on Probability Sampling in UX Research

Probability sampling — where every member of a target population has a known, non-zero probability of selection — is the statistical ideal for generalizable findings. Simple random sampling is often called the "gold standard." However, probability sampling requires a complete sampling frame (a list of every member of the target population). In practice, product UX researchers almost never have access to a complete sampling frame. True probability sampling is structurally unavailable for most product teams. The practical standard is purposive or panel sampling with transparent description of how the sample was recruited and explicit qualification of generalizability claims. Do not describe a panel or convenience sample as representative without directly addressing this limitation.

---

## Common Mistakes
- Calling a cross-sectional study "longitudinal" because it asks retrospective questions.
- Claiming causation from correlation without justification.
- Using a between-subjects design when within-subjects is feasible (wastes power).
- Ignoring attrition in longitudinal designs (attrition is rarely random).
- Running a quant study when the research question is fundamentally qualitative.
- Designing a benchmark study when the team actually needs to compare two variants (different power requirements, different analysis).
- Claiming a convenience or panel sample is representative of the target population without explicitly qualifying generalizability.
