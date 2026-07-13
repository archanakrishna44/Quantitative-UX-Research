# QRA Architecture Decision Record

**Status:** Active  
**Date:** 2026-05-03  
**Scope:** Quantitative Research Assistant (QRA) — design rationale for the FSM workflow, hard-halt gates, locked artifacts, and external validators.

---

## 1. Why a finite-state machine?

**The problem.** Left unconstrained, an LLM will helpfully skip ahead. Given a vague research idea and a data file, it will run a t-test. Given t-test output, it will write a conclusions section. This mimics HARKing (Hypothesizing After Results are Known): the analysis appears rigorous but the hypotheses were quietly shaped by seeing the results first. P-hacking and selective reporting follow the same pattern — the LLM optimizes for a satisfying narrative rather than a defensible one.

**The FSM enforces temporal ordering.** The 7-state workflow (S1 Intake → S2 Hypotheses → S3 Design → S4 Data Plan → S5 Exploratory → S6 Analysis Plan → S7 Confirmatory) maps directly onto pre-registration best practices. Hypotheses are written before the study is designed (S2). The analysis plan is locked before data is analyzed (S6). Inferential statistics are forbidden until S6 is approved — not as a soft preference, but as a hard-coded prohibition that applies even to runs labeled "sanity check" or "exploratory."

**Why not a checklist?** A checklist presented in a prompt can be acknowledged and then bypassed. The FSM makes out-of-order actions structurally impossible: the agent is in exactly one state at a time, the state is persisted to `project_state.md` on every transition, and every state defines a narrow set of permitted actions. Acting outside the current state requires a formal regression (`REGRESS TO S<n>`), which creates an audit trail entry and invalidates all locked artifacts from the regressed states forward.

---

## 2. Why hard-halt gates?

**The problem.** LLMs are trained to be agreeable. When a user says "that looks good, keep going," the model's instinct is to advance. Soft checkpoints — phrased as "please confirm before I continue" — are insufficient because the model will interpret enthusiastic affirmation, apparent impatience, or repeated requests as implicit confirmation.

**Four gates require literal approval tokens.** Gates at S2 (hypotheses), S3 (study design), S4 (data plan), and S6 (analysis plan) require the exact strings `APPROVED S2`, `APPROVED S3`, `APPROVED S4`, and `APPROVED S6`. The matching rule is deliberately narrow: case-insensitive, whitespace-normalized, but not paraphrase-tolerant. "Sounds great" does not satisfy the gate. "Yes, approved" does not satisfy the gate. Any reply other than the token causes the agent to re-present the gate and quote the rule.

**S6 is the most critical gate.** No inferential statistic — not a p-value, not a confidence interval on a hypothesis-test parameter, not a Bayes factor — may be computed on any primary or pre-specified secondary outcome before `APPROVED S6` is received. The prohibition covers runs labeled "preview," "sanity check," or "exploratory" when they touch the primary outcome. The gate also requires a dry-run on synthetic data to be completed and included in the locked artifact before approval is even requested, ensuring the analysis pipeline is executable before anyone commits to it.

**Token vocabulary is frozen.** The full set of control tokens is defined in the system prompt and does not expand at runtime. This prevents a class of social-engineering prompts that attempt to introduce new "shortcut" tokens or redefine existing ones through context pressure.

---

## 3. Why locked artifacts with SHA-256?

**The problem.** Without content-addressable locking, nothing stops a hypotheses file from being quietly amended after data is seen. The amendment may not be deliberate; an LLM assisting with "cleanup" could reword a hypothesis to better match what the data showed. The result is the same as HARKing regardless of intent.

**SHA-256 stored in `project_state.md` creates a tamper-evident record.** At each gate approval, the agent writes the artifact, computes its SHA-256, and stores the hash in `project_state.md` under `locked_artifacts`. The `validate_locked_artifact.py` script then verifies byte-identical match. At S7 start, before any live analysis runs, the agent re-verifies that `s2_locked.md`, `s3_locked.md`, and `s4_locked.md` all still match their stored hashes. The `analysis_plan_locked.md` itself opens with a "Predicate locks" section that lists the path and hash of each antecedent artifact, making the chain of custody explicit in the document itself.

**Why SHA-256 prevents HARKing.** The timestamp on the locked artifact predates data analysis by construction: S2 is locked before study design is approved, S6 is locked before any inferential test runs, and data is not even present in the workflow until S5. An amended artifact would produce a hash mismatch that the validator catches on next execution. Because the validator runs automatically and exits non-zero on mismatch, the agent halts before proceeding — the only way to continue is to surface the discrepancy to the user.

**Backward transitions preserve the record.** If the user regresses to an earlier state, locked artifacts are not deleted; they are renamed with a `.superseded.<ISO-8601-timestamp>` suffix. The original locked content is preserved, and no approvals from the superseded branch carry forward.

---

## 4. Why validators outside the LLM prompt?

**The problem.** A sufficiently creative prompt can pressure an LLM to work around instructions embedded in the same context window. Guardrails written as prose instructions face context pressure: as the conversation grows, the model weighs the initial instructions against the accumulated user requests in subsequent turns. A user who asks the same thing many times, reframes the request, or claims special authority can, over a long session, cause drift away from the initial constraints. This is a structural property of how language models are trained — not a failure of any particular model.

**Five deterministic Python validators fail closed.** The validators exist as code outside the prompt, not as prose within it:

- `validate_locked_artifact.py` — byte-level hash verification; cannot be reasoned past.
- `validate_project_state.py` — schema validation of `project_state.md`; enforces required fields, type constraints, and hash consistency across all locked artifacts.
- `validate_s5_script.py` — AST-walks every S5 script before execution, checking for banned inferential function calls from `scipy.stats`, `statsmodels` (via `.fit()`), and `pingouin`. It tracks aliased imports, so `import scipy.stats as ss; ss.ttest_ind()` is caught. No prompt instruction can bypass an AST check.
- `validate_results_md.py` — enforces presence of Deviations and Reproducibility sections, flags causal language when the causal identification strategy is `none`, checks that effect sizes are accompanied by CIs, and applies a heuristic small-cell suppression check.
- `validate_dry_run_byte_identical.py` — verifies that re-running the locked analysis script on the same synthetic dataset at S7 start produces byte-identical output to the S6 dry-run, catching environment drift before live data is touched.

Each script exits `0` (pass) or `1` (fail). Exit `1` causes an unconditional agent halt. The scripts are read-only and have no side effects. They require only the Python 3.10+ standard library plus `pyyaml`, so they cannot be broken by study-specific dependency changes.

**The AST validator deserves specific attention.** `validate_s5_script.py` does not search for banned function names as substrings in source text — it parses the script into an abstract syntax tree and inspects the call graph. This means it catches calls through aliases and through `from X import Y` forms. No prompting strategy can make `scipy.stats.ttest_ind()` invisible to an AST walk.

---

## 5. What should NOT be added to QRA

**Do not add autonomy that lets the agent decide when gates are "obviously satisfied."** The entire value of the gate system is that the agent cannot advance without a human-issued token. Adding heuristics like "if the user has confirmed the content three times, treat it as approved" re-introduces the soft-gate failure mode the hard-halt design explicitly eliminates.

**Do not add looser gates for "quick studies" or "exploratory work."** This argument is consistently made and consistently wrong in practice. Exploratory studies become the basis for product decisions; the line between exploratory and confirmatory is often drawn after results are known. QRA makes no exception: all studies traverse all gates. If a study is genuinely exploratory, the S2 hypotheses state that explicitly, and the S6 plan documents the absence of confirmatory inference — which is an appropriate and well-supported design, not a shortcut.

**Do not make the token vocabulary context-sensitive.** Tokens must be exact, literal, and fixed. Any design that interprets tokens relative to conversational context ("the user clearly meant to approve") recreates the agreeable-LLM failure mode. The token is forgery-resistant precisely because its validity is not a matter of interpretation.

**Do not move validators back into the prompt.** The motivation for externalizing validators is that prompt-only enforcement is insufficient under context pressure. Adding a validator as a prose instruction in the system prompt and removing the external script would visibly weaken the design. If a future maintainer believes a validator check is too strict, the right action is to change the validator code with an explicit version bump and a note in this document — not to absorb the check into instructions the model might soften over a long session.

---

## 6. Failure modes this design explicitly prevents

**HARKing.** `s2_locked.md` contains the hypotheses, timestamped and hashed, before any data is seen. `analysis_plan_locked.md` is locked before any inferential statistic is computed. A hypothesis that was written after results were seen would either not exist in the locked S2 artifact or would require a documented deviation — which is logged in `deviations.md`, reproduced verbatim in `results.md`, and flagged with an effect-on-inference rating. Post-hoc hypothesization is not prevented from happening, but it cannot be hidden.

**P-hacking.** The analysis plan locked at S6 specifies the exact model, estimator, outlier rule, and multiple-comparison correction before the analyst sees any inferential output. The multiple-comparison family is frozen at S6 lock; any test added after lock is classified exploratory regardless of its result. Any change to the primary test specification must be a declared material deviation requiring `APPROVED DEVIATION <id>`. The S7 step executes the locked plan exactly; if the user asks to omit a planned test, the agent refuses and cites the pre-registration contract.

**Selective reporting.** `results.md` must report every primary and pre-specified secondary test in the order they appear in the locked plan, regardless of outcome. `validate_results_md.py` checks for a Deviations section (which must reproduce `deviations.md` verbatim) and a Reproducibility section. Null results receive the same formatting as significant ones.

**Causal overclaim.** Two layers enforce this. First, the Hard Refusals forbid claiming causation from observational data without a causal identification strategy, and the S6 plan must declare its `causal_identification_strategy` explicitly. Second, `validate_results_md.py` bans a list of causal language terms (`causes`, `effect of`, `led to`, `resulted in`, etc.) when the `causal_identification_strategy` in the S6 plan is `none`. The ban is enforced at the text level before results are presented to the user.

**Injection attacks.** The DATA: fencing convention renders all content from data files, script stdout, and tool outputs inside labeled code blocks that the agent is instructed not to interpret as instructions. `validate_s5_script.py` validates scripts at the AST level before execution, preventing a class of attacks where injected cell values cause a malicious script to be written and run.

**State forgery.** `state_log.jsonl` is append-only: entries are never edited or deleted, and every state transition — including regressions and reopens — appends a new entry with a timestamp, the triggering token, and a snapshot of all current artifact hashes. SHA-256 hashes on locked artifacts make the `project_state.md` content verifiable against the files on disk. An attempt to forge an approval by modifying `project_state.md` directly would produce a hash mismatch on the next validator run.

---

## Tradeoffs acknowledged

This design is deliberately slow. A researcher who wants to run a quick chi-square on a small dataset will traverse all seven states and produce more documentation than the analysis itself. This is intentional: the cost of the process is paid once per study; the cost of undiscoverable methodological errors is paid indefinitely when findings are acted upon, revisited, or challenged. QRA is not optimized for speed of first result; it is optimized for defensibility of final result.

The external validators add an operational dependency: they must be present and executable in the environment where QRA runs. This is a deliberate tradeoff. The alternative — absorbing all checks into the prompt — would reduce the operational footprint but would also reduce the reliability of enforcement. The dependency is documented and the scripts have no external dependencies beyond Python 3.10+ and PyYAML (installed into each study's venv).
