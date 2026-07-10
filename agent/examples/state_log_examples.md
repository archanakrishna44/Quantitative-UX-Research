# state_log.jsonl — Examples

`state_log.jsonl` is append-only. Each line is a self-contained JSON object. It lives at `studies/<study_name>/state_log.jsonl`. Never edit or delete prior entries.

Required fields per entry: `timestamp`, `from_state`, `to_state`, `trigger`, `approval_token`, `artifact_hashes`.

---

## CLEAN EXAMPLE

```jsonl
{"timestamp":"2025-11-08T10:14:33Z","from_state":"S1","to_state":"S2","trigger":"user_approval","approval_token":"FRAMING CONFIRMED","artifact_hashes":{}}
{"timestamp":"2025-11-08T14:52:01Z","from_state":"S2","to_state":"S3","trigger":"user_approval","approval_token":"APPROVED S2","artifact_hashes":{"studies/mobile_nav_study/s2_locked.md":"a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856"}}
{"timestamp":"2025-11-09T09:31:44Z","from_state":"S3","to_state":"S4","trigger":"user_approval","approval_token":"APPROVED S3","artifact_hashes":{"studies/mobile_nav_study/s2_locked.md":"a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856","studies/mobile_nav_study/s3_locked.md":"7d2b1e48c93f056a14d8b72fc3e59a01d6b28374e5c9f012a3b74e8d25c9f103"}}
{"timestamp":"2025-11-09T16:05:22Z","from_state":"S4","to_state":"S5","trigger":"user_approval","approval_token":"APPROVED S4","artifact_hashes":{"studies/mobile_nav_study/s2_locked.md":"a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856","studies/mobile_nav_study/s3_locked.md":"7d2b1e48c93f056a14d8b72fc3e59a01d6b28374e5c9f012a3b74e8d25c9f103","studies/mobile_nav_study/s4_locked.md":"5c8e3a92f1d047b6293e5d8c4f01a7b2e94d3c86f5a2019b7e3c84d1f2a56907"}}
{"timestamp":"2025-11-10T11:19:55Z","from_state":"S5","to_state":"S6","trigger":"user_approval","approval_token":"S5 ACCEPTED","artifact_hashes":{"studies/mobile_nav_study/s2_locked.md":"a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856","studies/mobile_nav_study/s3_locked.md":"7d2b1e48c93f056a14d8b72fc3e59a01d6b28374e5c9f012a3b74e8d25c9f103","studies/mobile_nav_study/s4_locked.md":"5c8e3a92f1d047b6293e5d8c4f01a7b2e94d3c86f5a2019b7e3c84d1f2a56907"}}
{"timestamp":"2025-11-10T16:45:02Z","from_state":"S6","to_state":"S7","trigger":"user_approval","approval_token":"APPROVED S6","artifact_hashes":{"studies/mobile_nav_study/s2_locked.md":"a3f9c2d84e1b7056f3a291cc4d5e8f02b7a14e93d6c80571b2e4f9a3c1d07856","studies/mobile_nav_study/s3_locked.md":"7d2b1e48c93f056a14d8b72fc3e59a01d6b28374e5c9f012a3b74e8d25c9f103","studies/mobile_nav_study/s4_locked.md":"5c8e3a92f1d047b6293e5d8c4f01a7b2e94d3c86f5a2019b7e3c84d1f2a56907","studies/mobile_nav_study/analysis_plan_locked.md":"e9d1c3a7b5f24086e1a3c5d7f9b2e4a6c8d0f2b4e6a8c0d2f4b6e8a0c2d4f6b8"}}
```

Why this is clean:
- Every entry is valid JSON on a single line.
- `timestamp` is ISO-8601 with timezone (Z = UTC).
- `from_state` and `to_state` use the exact state labels defined in the schema (S1-S7, ARCHIVED).
- `trigger` is one of the three permitted values: user_approval, user_request, auto.
- `approval_token` records the exact token the user supplied at each gate; S1->S2 records "FRAMING CONFIRMED" (the soft-gate token), all hard gates record "APPROVED S<n>".
- `artifact_hashes` is cumulative — it includes hashes of all locked artifacts known at the time of transition, not just the one just locked.
- The sequence is contiguous: S1->S2->S3->S4->S5->S6->S7, with no skipped states.

---

## TRICKY EXAMPLE

```jsonl
{"timestamp":"2025-11-08T10:14:33Z","from_state":"S1","to_state":"S2","trigger":"user_approval","approval_token":"FRAMING CONFIRMED","artifact_hashes":{}}
{"timestamp":"2025-11-08T14:52:01Z","from_state":"S2","to_state":"S3","trigger":"user_approval","approval_token":"APPROVED S2","artifact_hashes":{"studies/survey_sat_study/s2_locked.md":"b1c4d7e29f3a056b8d2c4e7f1a3b5d8c2e4f6a0b1c3d5e7f9a2b4c6d8e0f2a4b"}}
{"timestamp":"2025-11-09T09:31:44Z","from_state":"S3","to_state":"S6","trigger":"user_request","approval_token":null,"artifact_hashes":{"studies/survey_sat_study/s2_locked.md":"b1c4d7e29f3a056b8d2c4e7f1a3b5d8c2e4f6a0b1c3d5e7f9a2b4c6d8e0f2a4b","studies/survey_sat_study/s3_locked.md":"9e3f1a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f"}}
```

WHAT IS WRONG AND WHY IT FAILS:

1. **Forward skip from S3 directly to S6 — states S4 and S5 are missing.**
   The third entry records a transition from_state "S3" to_state "S6", jumping over S4 (Data Plan
   and Operationalization) and S5 (Data Preparation and Exploratory Checks). Both S4 and S6 are
   HARD-HALT gates. S4 must produce a locked artifact (s4_locked.md) and requires the token
   APPROVED S4 before any data is handled. S5 requires a PII scan and data quality checks before
   the analysis plan can be written. A skip of this kind means: no variable operationalization was
   approved, no power analysis was produced, no PII scan was run, and no data quality summary
   was accepted. The analysis plan written in S6 has no predicate locks for s4_locked.md and no
   data_hash in project_state.md — both mandatory. This transition must be refused; the agent
   must require the user to proceed through S4 then S5 in order before entering S6.

2. **`approval_token` is null for a hard-halt gate transition.**
   The S3->S6 entry records `"approval_token": null`. The Operating Rules require that on every
   state transition the approval_token field records the token that authorized the transition.
   A null value means either: (a) no approval was sought, or (b) the agent advanced automatically
   without waiting for the user — both are violations of the hard-halt protocol. Even for
   non-gate transitions (trigger = auto), the field must be present; it should record null only
   when the transition is legitimately automatic (e.g., an internal bookkeeping entry). A gate
   transition — especially one crossing two HARD-HALT gates — cannot have a null approval_token.
   The correct values would be: a separate S3->S4 entry with "APPROVED S3", a separate S4->S5
   entry with "APPROVED S4", and a separate S5->S6 entry with "S5 ACCEPTED", each on its own line.

3. **`artifact_hashes` in the S3->S6 entry omits s4_locked.md.**
   Because S4 was skipped, s4_locked.md was never produced, so it cannot appear in artifact_hashes.
   This is a downstream consequence of the illegal skip — the hash map is incomplete, and any
   subsequent validator check will fail because the required predicate locks for S6 are absent.
