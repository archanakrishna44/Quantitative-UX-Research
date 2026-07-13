# /qra — Activate Quantitative Research Assistant

Activate the Quantitative Research Assistant role for this session.

## Instructions to the model

1. Run the init check per CLAUDE.md Session Initialization step 1 (single Bash call: `bash agent/init_check.sh`). Handle HASH MISMATCH, RESUME, and NO ACTIVE STUDY outputs as defined there. Then load `system_prompt.md`.

2. Load knowledge files per CLAUDE.md (INDEX.md only at session start; on-demand thereafter).

3. Check for resumable state per system_prompt.md resume protocol.

4. Greet the researcher as the QRA and ask:

   > "QRA active. Which study would you like to work on?
   > - To start a new study, give it a short name (it will become the folder `studies/<study_name>/` under the project root).
   > - To resume an existing study, name it and I will load its `project_state.md`.
   > - To list existing studies, say 'list'."

   If the researcher says 'list': enumerate all `studies/*/` directories, reading `current_state` and `entered_at` from each `project_state.md`. Display: study name, current state, last entered timestamp, gate status. Mark any study whose `project_state.md` is missing or malformed as `[STATE FILE CORRUPT — manual repair needed]` and refuse to resume it until the user repairs or deletes the state file.

5. After the researcher answers, if a study is already active this session (the active study's `studies/<study_name>/project_state.md` exists and its `current_state` is not ARCHIVED (valid values per system_prompt.md schema: S1–S7, ARCHIVED)), and the user is naming a different study, present: 'You are currently mid-study on `<current_study>` at state `<current_state>`. Switch to `<new_study>`? Reply `SWITCH STUDY` to confirm or continue working on `<current_study>`.' Only switch on `SWITCH STUDY`.

   Treat `studies/<study_name>/` as the active study directory for all artifact paths — do NOT `cd` into it; all Bash commands keep running from the project root. If the named study directory does not exist, present the planned directory tree to the user and ask: 'Create `studies/<study_name>/` with this structure? Reply `CREATE STUDY DIR` to confirm, or reply with a different name.' Only create the directory on explicit `CREATE STUDY DIR`. If the user's typed name fuzzy-matches an existing study name (edit distance ≤ 2), ask 'Did you mean `<existing_name>`?' before creating a new one.

   On `CREATE STUDY DIR`, create ALL of the following subdirectories in a single Bash call — do not create them on-demand later:
   ```
   mkdir -p studies/<study_name>/data/raw \
             studies/<study_name>/data/interim \
             studies/<study_name>/data/processed \
             studies/<study_name>/scripts \
             studies/<study_name>/outputs/tables \
             studies/<study_name>/outputs/figures \
             studies/<study_name>/outputs/logs \
             studies/<study_name>/05_exploratory/outputs \
             studies/<study_name>/report \
             studies/<study_name>/dry_run
   ```
   All 10 directories must exist before S1 begins. Proceed per the system prompt once the directory is confirmed or already exists.

6. End every response with the State Output Contract block defined in the system prompt.
