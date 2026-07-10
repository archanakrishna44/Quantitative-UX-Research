# s1_intake.md — Examples

## CLEAN EXAMPLE

```markdown
# S1 Intake — mobile_nav_study

| question_id | question | response | assumed_if_blank |
|-------------|----------|----------|-----------------|
| 1 | What is the study about? | We want to understand how users navigate the redesigned mobile app bottom-bar. Specifically, whether the new icon-only layout affects navigation success compared to the current icon-plus-label layout. | — |
| 2 | What decision or action is this meant to support? | The product team is deciding whether to ship the icon-only bottom bar to all users. The study will either greenlight the rollout or trigger a revision before launch. | — |
| 3 | Is there prior work or existing data we should build on? | A previous tree test (Q2 2024) showed a 63% overall task success rate with the labelled layout. We are using that as the baseline. | — |
| 4 | What is the data situation? | No data collected yet. Planning a remote unmoderated tree test via Optimal Workshop. Participants complete 8 navigation tasks. | — |
| 5 | What are the practical constraints? | Need results within 3 weeks. Recruiting budget covers ~120 participants through User Interviews panel. No access to UserZoom. | — |
| 6 | IRB and ethics | Internal UX research, no medical or sensitive data. Company research ops confirmed this falls within blanket IRB waiver for product usability studies. | — |
| 7 | Who will read or act on the findings? | Mobile design team and the VP of Product. Summary deck required; statistical appendix optional. | — |
| 8 | Anything else? | Stakeholders have already expressed a strong preference for the icon-only design. Want the study to be rigorous enough to push back if the data don't support it. | — |
```

Why this is clean:
- All 8 question IDs are present with no gaps.
- No cell is blank without an entry in `assumed_if_blank`.
- No INFERRED cells — every response came directly from the user.
- Research topic is framed associationally: the study examines whether layout *affects* navigation success, not whether it *causes* improvement.
- Constraints, audience, and prior work are all populated.
- Ethics/IRB status is stated explicitly rather than left blank.

---

## TRICKY EXAMPLE

```markdown
# S1 Intake — checkout_friction_study

| question_id | question | response | assumed_if_blank |
|-------------|----------|----------|-----------------|
| 1 | What is the study about? | We want to prove that the new streamlined checkout flow causes fewer drop-offs than the legacy flow. | — |
| 2 | What decision or action is this meant to support? | Ship the new checkout to all users. | — |
| 3 | Is there prior work or existing data we should build on? | Analytics show a 12% cart-abandonment rate on the legacy flow. | — |
| 4 | What is the data situation? | We will run an A/B test in production with real transactions. | — |
| 5 | What are the practical constraints? | Two weeks, no recruiting budget — using live traffic only. | — |
| 6 | IRB and ethics | | INFERRED — please confirm: assumed standard product A/B test exempt from formal IRB review. |
| 7 | Who will read or act on the findings? | Product and engineering leads. | — |
| 8 | Anything else? | | INFERRED — please confirm: no additional constraints noted. |
```

WHAT IS WRONG AND WHY IT FAILS:

1. **Causal language in the research framing (question_id 1).**
   The response says "prove that the new checkout flow *causes* fewer drop-offs." The word "causes" is causal language. At S1 the framing has not yet been reviewed for causal identification strategy — no randomized design has been confirmed, no DAG has been drawn, and no causal identification strategy has been recorded in any locked artifact. The S1 framing must use associational language: "associated with," "predicts," "is related to," or "differs from." Using causal language in S1 primes the downstream hypotheses (S2) and analysis plan (S6) toward overclaiming. If the A/B test is properly randomized and analyzed as an ITT, causal language may become appropriate later — but it must be earned at S3/S4, not assumed in intake.

   Correct phrasing: "We want to understand whether the new streamlined checkout flow is associated with lower drop-off rates compared to the legacy flow."

2. **IRB cell is blank with an INFERRED assumption, not a confirmed response.**
   The IRB field (question_id 6) is empty and the `assumed_if_blank` column carries an unconfirmed inference. Per the S1 rule, any assumed answer must be marked 'INFERRED — please confirm' *and confirmed before S2*. This is present — but the tricky failure is that a live-traffic A/B test with real financial transactions may not qualify for a blanket product-UX waiver. The agent should flag this assumption for explicit IRB confirmation before transitioning, not silently carry it forward.
