---
scope: reference
modifies_workflow: false
---

# Ethics and Privacy

## Research Ethics Principles (Belmont Report)
- **Respect for persons**: participants are autonomous agents; protect those with diminished autonomy. Requires informed consent.
- **Beneficence**: do not harm; maximize benefits and minimize risks.
- **Justice**: distribute research burdens and benefits fairly; do not exploit vulnerable populations.

## When IRB (or Equivalent) Review is Required
- Any research involving human subjects — data collection about living people for generalizable knowledge.
- Includes surveys, interviews, usability studies, behavioral observation, analysis of existing records.
- **Exempt categories** (varies by institution): anonymous surveys with no sensitive topics, observation in public settings, analysis of existing publicly available data. Verify with your IRB — do not self-exempt.
- **Industry / non-academic research**: may fall under organizational ethics review rather than IRB. Check with your legal/compliance team.

## Informed Consent Requirements
Participants must be told:
1. Purpose of the study (in plain language).
2. What they will be asked to do and how long it will take.
3. Risks and benefits.
4. That participation is voluntary and they can withdraw at any time without penalty.
5. How data will be stored, who will have access, and when it will be destroyed.
6. Who to contact with questions.

Consent must be documented (signed form or electronic record) unless IRB grants a waiver.

---

## UX Research-Specific Ethics

### Session Recording Consent

Screen recording, audio recording, and video recording require explicit, specific consent — even on panel platforms that obtain a general research participation consent.

- The consent form or study brief must state: (a) that the session will be recorded, (b) what type of recording (screen, audio, video, or combination), (c) what the recording will be used for (internal team review, design decision-making, highlight reel for stakeholders), and (d) who will view it (the core research team only, or also product/design/engineering stakeholders).
- "We may record this session" is not sufficient. Be specific about use and audience.
- If a recording will be retained beyond the standard platform retention window, or shared with third parties (e.g., a client or external partner), this must be explicitly disclosed and consented to.
- Participants have the right to request deletion of their recording after the session. Have a process for this and state it in the consent form.

### Panel Platform Consent Coverage

Prolific, UserTesting, Respondent, and similar platforms obtain general consent to participate in research as part of their user agreements. This covers: completing tasks, answering survey questions, and participating in the standard study flow on-platform.

This general consent does NOT cover:
- Retention of session recordings beyond the platform's standard data retention period.
- Use of recordings, quotes, or data in publications, conference presentations, or public-facing reports.
- Sharing video or audio clips with third parties (clients, partner organizations, press).
- Reuse of data in a future study with a different purpose.

If any of these apply to your study, provide a supplemental consent form that covers the additional uses explicitly. Do not assume platform consent is sufficient for non-standard uses.

### Analytics and Behavioral Data Repurposed for Research

Data collected for product operations — event logs, clickstreams, funnel analytics, session replays, A/B test logs — may constitute human subjects research when repurposed as a study instrument, depending on jurisdiction and your organization's IRB or ethics scope.

Flag this explicitly at S1 intake when analytics data is the primary study instrument. Specifically:
- If you are analyzing existing behavioral data to answer a research question about user behavior (not just a business analytics question), check whether this requires ethics review under your organization's policies.
- GDPR and CCPA have implications for secondary use of behavioral data — data collected for product purposes may require separate consent to use for research purposes.
- Session replay tools (FullStory, Hotjar, etc.) capture detailed behavioral data that may include incidental PII (typed content, visible personal details). Confirm that your organization's privacy policy and user ToS covers the use of this data for research before incorporating it into a study.
- Document the data source, original collection purpose, and research use case in the S4 data plan.

### A/B Test Ethics

Most product A/B tests are covered by a product's terms of service (users consent to feature variation as part of normal product use) and do not require explicit research consent. This follows standard industry practice and IRB guidance for minimal-risk product experiments.

However, the following conditions require IRB or ethics board review regardless of method:

- **Deception**: if participants are misled about the purpose of the interaction or shown deliberately false information as part of the manipulation.
- **Health-adjacent interventions**: if the A/B test involves health information, wellness features, mental health content, or any intervention where the variant could affect a participant's wellbeing.
- **Vulnerable populations**: if the product's user base includes children, individuals with cognitive disabilities, or other protected groups, and the test involves a design change that could differentially affect them.
- **Coercive designs**: if the variant under test includes a dark pattern, urgency manipulation, or design element intended to exploit cognitive biases in ways that could cause harm.

Flag at S3 if any of these conditions apply to the A/B test design. Do not proceed without ethics clearance.

### Incentive Platform Norms

Incentive levels affect data quality as well as participant welfare. Under-incentivizing harms participants; over-incentivizing attracts low-effort responses.

- **Prolific**: follow Prolific's fair pay guidelines. As of 2024–2025, Prolific requires a minimum of £9.00/hour (approximately $11–12 USD equivalent, adjusted for current exchange rates). Studies paying below this rate are flagged by Prolific and may be removed. Calculate study time accurately based on pilot testing — do not estimate low.
- **UserTesting**: standard panel sessions compensate approximately $10 per 20-minute session (rates vary by panel and study type). Check current UserTesting rate guidance before launching.
- **Respondent**: B2B and professional panels typically pay $50–$150+ per hour depending on seniority and specialization. Use Respondent's recommended rates for the target professional profile.
- **Over-incentivizing**: very high incentives relative to the task can attract participants who rush through tasks to collect compensation. For survey studies, this manifests as straight-lining and speeders. For task studies, it can inflate task completion rates (motivated completion rather than genuine usability).
- **Under-incentivizing on Prolific**: paying below fair rates harms platform reputation and produces lower-quality responses because it filters toward participants with fewer options. Always pay at or above Prolific's minimum.
- **Contingent incentives**: never make payment contingent on specific responses ("you must complete the entire survey to be paid"). Payment should be contingent on good-faith participation, not on completing tasks successfully or giving particular answers.

**Note on platform rate currency**: platform rates and guidelines change frequently. Always verify current fair pay guidelines directly at the platform's researcher help center before setting incentives for a new study. The figures above reflect rates as of 2024–2025 and may be outdated.

---

## PII (Personally Identifiable Information)

### Direct Identifiers (never collect or retain unless essential and IRB-approved)
- Full name
- Email address
- Phone number
- Exact home or work address
- Date of birth (day + month + year combined)
- Social Security Number / national ID
- IP address (in some jurisdictions)
- Device IDs, cookies used for re-identification
- Facial images or biometrics

### Indirect / Quasi-Identifiers (can re-identify when combined)
- Age (especially if > 85 or very specific)
- ZIP/postal code
- Employer name + job title + gender
- Rare diagnosis or condition
- Small cell sizes in cross-tabulations (N < 5 in a cell may re-identify)

### Data Handling Rules
- **Collect minimum necessary**: only variables justified by the analysis plan.
- **Separate identifiers from data**: use participant IDs; store the ID-to-name linkage separately with restricted access.
- **Encrypt data at rest and in transit**.
- **Anonymize before analysis**: if names/emails are not needed for analysis, remove them before the data file is shared with the analysis system.
- **Retention**: destroy direct identifiers on the schedule specified in the consent form (commonly 3–7 years for research data; shorter for identifiers alone).

## GDPR / CCPA Considerations (when applicable)
- **GDPR** (EU): establishes six lawful bases for processing personal data: consent, legitimate interests, performance of a contract, compliance with a legal obligation, protection of vital interests, and performance of a public task. For UX research specifically, the relevant bases are: consent (explicit opt-in), legitimate interests (internal research where privacy impact is proportionate and does not override participant rights), and contract (data collected as part of a service relationship). When in doubt, use consent — it is the most defensible basis and gives participants the clearest rights. Data subjects have rights to access, rectification, erasure, portability. Privacy by design required.
- **CCPA** (California): right to know what data is collected, right to delete, right to opt out of sale.
- If participants are in the EU or California, consult legal/privacy counsel before collecting data.

## Vulnerable Populations
Require additional protections:
- Children/minors: parental consent + child assent (age-appropriate).
- Pregnant individuals, prisoners, cognitively impaired individuals: heightened scrutiny.
- Employees of the sponsoring organization: voluntary participation may be coerced; additional safeguards needed.
- Economically disadvantaged: incentive amounts should not be unduly coercive.

## Incentives
- Must be proportionate to time and effort — not so large as to be coercive.
- Disclose incentives in consent form.
- Do not make incentives contingent on specific responses.

## Data Breach Protocol
If a data breach occurs during a study:
1. Stop data collection immediately.
2. Notify your IRB/ethics board.
3. Notify affected participants if required by law.
4. Document what happened and what data was exposed.
5. Do not use potentially compromised data without review.

## Ethics Checklist (complete at S3/S4)
- [ ] IRB / ethics review status confirmed (approved / exempt / not applicable — documented).
- [ ] Informed consent procedure defined.
- [ ] Session recording consent explicitly included if recording is planned.
- [ ] Panel platform consent coverage verified; supplemental consent form prepared if needed.
- [ ] Analytics data source and secondary use flagged if applicable.
- [ ] A/B test ethics conditions checked (deception, health-adjacent, vulnerable populations).
- [ ] PII handling plan documented in data plan.
- [ ] Minimum necessary data collection confirmed.
- [ ] Incentive amount and justification documented; platform fair pay guidelines checked.
- [ ] Data retention and destruction schedule specified.
- [ ] Vulnerable population protections addressed (if applicable).
- [ ] Data breach protocol known.
