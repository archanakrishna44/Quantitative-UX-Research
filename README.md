# Quantitative Research Assistant (QRA)

A quantitative researcher for your UX team — built as a Claude Code agent. Bring it your project scope and it will suggest the right quantitative research methods, design the study, analyze your results, test for significance, and report its findings in a format ready to share with stakeholders.

---

## What QRA does

QRA functions as a quantitative research teammate on any UX project. You describe what you are trying to learn; QRA takes it from there — scoping the study, recommending the right method (survey, tree test, A/B test, usability benchmarking, analytics analysis, and more), writing the hypotheses, designing the analysis plan, and producing a defensible, reproducible result.

**What QRA handles:**
- Translating a UX project goal into a well-formed research question and hypotheses
- Recommending the appropriate quantitative method and statistical test for your situation
- Designing the full study: variables, sample size, data collection plan, and analysis approach
- Analyzing your data once collected: running the tests, checking assumptions, and interpreting results
- Producing a results report in APA 7 format and exporting it as a Word document

**What you handle:**
- Deploying the data collection instrument — setting up the survey, running the tree test, configuring the A/B test, or pulling the analytics export
- Bringing the collected data file back to QRA for analysis

QRA can also work alongside qualitative research. If your project includes a qualitative phase — interviews, diary studies, or similar — tell the agent during the initial scoping conversation. QRA will assess the situation and advise on sequencing. Sometimes qual first makes sense (e.g. interviews to generate hypotheses, then a survey to validate at scale); sometimes a quantitative baseline first makes the qualitative work sharper (e.g. a survey to identify segments before deciding who to interview and what to ask). QRA will recommend the stronger sequence with a brief rationale — you can accept or proceed with your original plan. You conduct the qualitative work independently; QRA handles the quantitative study.

The agent runs a strict seven-stage workflow and will not skip ahead. It will not run a statistical test before the analysis plan is approved. This is intentional: the design prevents the most common ways research findings become indefensible — hypothesising after results are known, running multiple tests and reporting only the one that worked, or writing conclusions that overstate what the data can support.

QRA is designed for UX researchers and product teams, not engineers. You do not write code or run scripts. Your interactions are:

1. Answer the agent's questions in chat.
2. Deploy your data collection instrument and collect responses independently.
3. Place your data file in the `data/raw/` folder inside your study directory.
4. Read the results in chat and open the Word document.

---

## Prerequisites

Before starting, confirm these are in place:

- **Claude Code** — desktop app or terminal; either works. QRA uses Claude Code's Bash tool to execute analysis scripts on your machine.
- **Python 3.10 or later** — required for the analysis scripts and validators. If it is not installed, download it from [python.org](https://www.python.org/downloads/). On Windows, check **"Add python.exe to PATH"** during installation.

That is the entire setup. Everything else (pandas, scipy, python-docx, pyyaml, and the other analysis packages) is installed automatically by the agent into a private per-study environment when you start a study — it does not touch your system Python.

---

## Getting the project onto your machine

Either works:

- **Download ZIP** (simplest): on the GitHub page, choose **Code → Download ZIP**, then unzip it anywhere you like.
- **git clone**, if you use git.

---

## How to start

1. Open the project in Claude Code:
   - **Desktop app:** choose **File → Open Folder** and select the project folder.
   - **Terminal:** open a terminal in the project folder and run `claude`.
2. In the chat panel, type:

   ```
   /qra
   ```

The agent runs a silent integrity check, loads its configuration, and greets you. It will ask whether you want to start a new study or resume an existing one.

**About permission prompts:** as you work, Claude Code will occasionally ask you to approve a command before the agent runs it on your machine. This is normal — it is Claude Code's built-in safety layer, not an error. The commands you will see create study folders, install analysis packages into a private per-study environment, and run the workflow's checking scripts. For the repeated checking-script commands, choosing "always allow" is expected and safe.

To start a new study, give it a short name — for example, `lender_satisfaction_q3`. The agent creates the study folder automatically and walks you through the first stage.

---

## The 7 stages

QRA moves through exactly one stage at a time. Each stage produces a specific output; four stages require your explicit written approval before the agent advances.

| Stage | Name | What happens | Approval required |
|-------|------|--------------|-------------------|
| S1 | Intake | You answer 8 questions about your study. The agent writes a one-paragraph framing summary. | Reply `FRAMING CONFIRMED` |
| S2 | Research Questions and Hypotheses | The agent writes a formal research question, null and alternative hypotheses, and defines the unit of analysis and population. | Reply `APPROVED S2` |
| S3 | Study Design and Method | The agent recommends a UX research method (survey, tree test, A/B test, analytics, etc.) and a matching statistical test, with a threat-to-validity table. | Reply `APPROVED S3` |
| S4 | Data Plan | The agent produces a variable table, recruitment criteria, power analysis, data collection procedure, and a privacy and ethics plan. | Reply `APPROVED S4` |
| S5 | Data Preparation and Exploratory Checks | You drop your data file into the `data/raw/` folder. The agent scans for PII, validates the data against the S4 plan, and produces descriptive statistics and exploratory plots. No statistical tests are run at this stage. | Reply `S5 ACCEPTED` |
| S6 | Pre-Registered Analysis Plan | The agent writes the complete analysis plan — exact test, model specification, outlier rules, missing-data handling, and decision rules for every hypothesis — and runs it on a synthetic dataset to confirm it executes correctly. | Reply `APPROVED S6` |
| S7 | Confirmatory Analysis and Reporting | The agent runs the locked plan on your data, writes `results.md` in APA 7 format, and exports `report/results.docx`. | Reply `STUDY CLOSED` |

The four stages marked above (S2, S3, S4, S6) are hard-halt gates. The agent will not advance past them on a casual "looks good" or "ok." It requires the exact token listed. At each gate, the agent also gives you a short plain-language summary of what you are approving — what the plan commits to, what it rules out, and what to double-check — so you never have to evaluate the statistics to approve with confidence. This is by design — see `agent/ARCHITECTURE.md` for the reasoning.

---

## Project structure

The full directory tree is documented in [`folder_structure.md`](folder_structure.md). A brief orientation:

- `agent/` — the agent's configuration: `system_prompt.md` (the full workflow definition) and `ARCHITECTURE.md` (design rationale).
- `knowledge/` — domain reference files covering research design, statistics, causal inference, ethics, and reproducibility. The agent loads these on demand.
- `.claude/commands/` — contains `qra.md`, the slash command file. This is a hidden folder; enable "show hidden files" in your file manager to see it.
- `scripts/validators/` — five Python scripts that enforce workflow rules as deterministic code. See [`scripts/validators/README.md`](scripts/validators/README.md) for what each one checks.
- `studies/<study_name>/` — one folder per research study, created automatically by the agent. Your data goes in `data/raw/`; results appear in `outputs/` and `report/`.

---

## Approval tokens

The agent accepts the following control tokens. These must be typed exactly as shown (they are not case-sensitive; surrounding whitespace and trailing punctuation are ignored).

| Token | When to use |
|-------|-------------|
| `FRAMING CONFIRMED` | Accept the S1 framing summary and advance to S2 |
| `APPROVED S2` | Approve the research question and hypotheses |
| `APPROVED S3` | Approve the study design and method |
| `APPROVED S4` | Approve the data plan |
| `S5 ACCEPTED` | Accept the data quality summary and advance to S6 |
| `APPROVED S6` | Approve the analysis plan and allow the analysis to run |
| `STUDY CLOSED` | Close and freeze the study after S7 is complete |
| `REGRESS TO S<n>` | Formally revert to an earlier stage (e.g. `REGRESS TO S3`) |
| `ETHICS CONFIRMED` | Confirm participant consent and data handling when PII is found in the data file |
| `APPROVED DEVIATION <id>` | Approve a declared deviation from the locked S6 plan |
| `REOPEN STUDY <name>` | Reopen a closed (ARCHIVED) study for amendments |
| `CREATE STUDY DIR` | Confirm creation of a new study directory |
| `SWITCH STUDY` | Confirm switching to a different active study |
| `CONFIRM PROMPT UPDATE` | Confirm a detected hash mismatch during session init and proceed |
| `CANCEL SESSION` | Abort the session when a hash mismatch is detected during init |

---

## Further reading

For a deeper look at how QRA is built and why it works the way it does:

- **[`agent/ARCHITECTURE.md`](agent/ARCHITECTURE.md)** — explains the reasoning behind the finite-state machine, the hard-halt gates, SHA-256 artifact locking, and the external validators. Start here if you want to understand why the agent is deliberate and strict.
