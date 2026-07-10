# deviations.md — Examples

`deviations.md` is an append-only YAML list. Each entry is a YAML mapping block separated by `---`. The file lives at `studies/<study_name>/deviations.md`.

---

## CLEAN EXAMPLE

```yaml
- id: DEV-001
  timestamp: "2025-11-14T09:32:17Z"
  locked_text: >
    Primary analysis: Mann-Whitney U test comparing task-success proportions between
    icon-only and icon-plus-label conditions. Outlier rule: exclude observations
    where response_time > median + 3×MAD (computed within condition).
    Significance threshold: α = 0.05 (two-tailed). Family size = 1; no correction needed.
  actual_action: >
    Outlier rule applied as specified, but the MAD was computed on the pooled sample
    rather than within-condition, because one condition had n = 4 after exclusions,
    making within-condition MAD unreliable. Pooled MAD was used instead.
  reason: >
    Within-condition outlier computation is unreliable at n < 5. Pooled MAD is a
    documented fallback for small cells; switching to pooled MAD does not alter the
    primary test statistic.
  effect_on_inference: minor
  user_approval_token: "APPROVED DEVIATION DEV-001"
```

Why this is clean:
- All required fields are present: `id`, `timestamp`, `locked_text`, `actual_action`, `reason`, `effect_on_inference`, `user_approval_token`.
- `locked_text` is a verbatim quote from `analysis_plan_locked.md`.
- `effect_on_inference` uses one of the three permitted values: `none`, `minor`, `material`.
- `user_approval_token` records the exact token the user supplied, confirming the deviation was approved before execution.
- The deviation is narrow in scope — it adjusts a computational detail of a pre-specified outlier rule; it does not introduce a new variable, a new test, or a new outcome.

---

## TRICKY EXAMPLE

```yaml
- id: DEV-002
  timestamp: "2025-11-15T14:07:44Z"
  locked_text: >
    Primary outcome: tree-test task success rate (binary: 1 = correct destination reached,
    0 = incorrect or gave-up). Secondary outcomes: directness score and time-on-task
    (log-transformed). No other outcome variables are included in the confirmatory family.
  actual_action: >
    Added "confidence rating" (1–7 Likert scale, collected post-task) as a secondary
    outcome and ran a Wilcoxon signed-rank test on it. Confidence was not in the S4
    variable list. Results showed a statistically significant difference (p = 0.03)
    favouring the icon-plus-label condition on confidence, which was included in
    results.md.
  reason: >
    The client asked about confidence after data collection. The variable was present
    in the dataset because the survey tool collected it by default.
  effect_on_inference: material
```

WHAT IS WRONG AND WHY IT FAILS:

1. **`user_approval_token` field is missing entirely.**
   The field is required for every deviation entry. Its absence means there is no recorded evidence that the user supplied `APPROVED DEVIATION DEV-002` before the action was executed. Per the S7 rule: "Material deviations require the user to reply with `APPROVED DEVIATION <id>` before execution." Running the test and writing results without this token violates the hard-halt protocol. Even for `minor` or `none` effect deviations the field must be present (it records the absence of a required token or the token that was supplied).

2. **The deviation smuggles in a new outcome variable that was not in S4.**
   The S4 variable list explicitly closes the confirmatory family. Adding "confidence rating" as a secondary outcome post-data is outcome-switching — a form of HARKing. The deviation mechanism exists to document and approve *deviations from the locked plan*, not to expand the confirmatory outcome set after seeing the data. The correct handling is either: (a) label the confidence analysis as exploratory, clearly separated from the confirmatory section in `results.md`, or (b) formally regress to S4, amend the variable list, re-run S5 and S6 gates, and re-lock the analysis plan — which at this point would be invalid because data have already been seen.

   The `effect_on_inference` field correctly says `material`, but without the approval token and with an unlawful outcome expansion, the entry cannot be executed at all — it should have been halted before the Wilcoxon test was run.
