# Is the thesis defendable? Review against the Student's Guide

Date: 2026-10-21. Sources: Clim & Aldrigo, *Student's Guide to Research Projects, Theses and Dissertations* (ASE Bucharest edition, chapters 1-6 read closely, chapters 7-9 skimmed for the defence rules), the current `docs/thesis/research-design.md`, and `thesis-plan.md`.

## Verdict

**Defendable at bachelor level, with seven fixes.** The design already does the things the guide cares most about: it names a baseline (Wazuh), fixes thresholds before measuring, keeps a development and a held-out split, treats a null result as reportable, and lists limitations up front. The guide would send it back at the Design Gate for the weaknesses below, not stop it at the Problem Gate. No alternative topic is needed. A fallback ladder is at the end in case time runs short.

Caveat: the guide is written for ASE Bucharest (40-page bachelor limit, ASE forms). Lucian's own university rules and supervisor override it. The method advice (gates, claim bounding, evaluation) is general.

## How the topic scores on the guide's own tests

| Guide test | Result |
|---|---|
| Title test (remove AI, Python, model, platform: is a problem left?) | Pass. Organisations without a SOC cannot triage alerts or afford a commercial SIEM. |
| Access test (can the evidence be obtained and used lawfully?) | Pass. Everything is lab-generated, no personal data, local model. Green. |
| Counter-result test (what finding would count against the idea?) | Pass. Thresholds F1-F6 can fail, H1 and H2 can fail. |
| Route fit | Partial. Two routes are mixed. See fix 1. |
| Bachelor level (justified baseline, bounded tests, modest local contribution) | Pass. Upper end of bachelor size. |
| Novelty stated as provisional | Needs care. See fix 6. |

## Where a committee will attack, and the cheap fix

**1. Two studies, one claim (hybrid-route warning).** The guide says a hybrid route is justified only when both parts answer one question, and names "two incomplete studies without integration" as the failure. Today RQ1 (build and measure) and RQ2 (2x2 experiment) are joined only by the title.
*Fix:* add a must-criterion **F8, triage trustworthiness**, taken from the C4 condition of RQ2 (for example hallucination rate and unsafe-suggestion rate below a stated limit). Then RQ2 is the evidence for one feasibility criterion and the thesis has one claim. Name build-and-evaluate as the dominant route and the experiment as a nested controlled comparison.

**2. "Open-source SIEM vs Wazuh" invites the question "Wazuh already is one."** A committee member will ask why feasibility needs proving when Wazuh exists.
*Fix:* say in the introduction that the object under test is the lightweight Sigma-based prototype with local LLM triage, and Wazuh is the reference. The contribution is detection-as-code plus grounded triage at low install cost, not "a SIEM". Optional: put "lightweight, detection-as-code" in the title. That is Lucian's decision.

**3. H2 is close to circular.** The author writes the playbooks and also the reference "correct steps". A model that copies the playbook will match the reference by construction, so H2 may only measure copying.
*Fix, three cheap parts:* (a) write the reference steps before the playbooks, or from an outside source such as MITRE mitigations or vendor guidance; (b) include the ~20 benign alerts where the right answer is "no action", so copying is penalised; (c) add a small negative control, about 10 alerts given a deliberately wrong playbook, and report how often the model follows it. (c) is also direct evidence for the human-approval rule.

**4. Thresholds need a source and a derivation.** "TryHackMe SOC targets" is a weak authority, and 500 events/s has no stated reason. The guide says the source and limits of every reference must be recorded (oracle problem).
*Fix:* derive F2 from an assumed small-organisation size (for example 50 endpoints times a measured events/s per endpoint), cite one or two published sources for F3-F5, and get the supervisor to approve the table before `prereg-v1`. Record it in the decision log.

**5. The detection claim rests on one author, one lab.** The author writes rules, picks the attack matrix and writes labels. The related-work finding that Sigma rules can be evaded (Nordström and Widéen) limits any coverage claim.
*Fix:* take the attack procedures from an outside catalogue (Atomic Red Team) so the author did not choose the tests; make the Wazuh comparison on the **held-out set only** as the headline; define in advance who or what generates the 24 h benign traffic, since FP rate depends on it. State that coverage is "of the tested techniques in this lab", never general coverage.

**6. Novelty must stay provisional.** The master's-level related work already contains Wazuh plus local Mistral via Ollama (Uzodinma, Luleå 2026). The guide warns against gap-spotting and against "first study ever".
*Fix:* in the literature chapter, state the gap as the combination (Sigma as code in CI, a factorial grounding experiment, thresholds fixed in advance), and name Uzodinma as the closest prior work with what differs.

**7. Statistics treat 80 alerts as independent, but they are 12 techniques times 5 variants.** Variants of one technique are correlated, which makes the Wilcoxon p-values too optimistic.
*Fix:* add a technique-clustered bootstrap CI, or run the test on per-technique means as a robustness check, and report both. About 20 lines in `eval/score_triage.py`.

## Schedule risk (the most likely real failure)

April 2027 holds the rule freeze, final attack runs, the 24 h benign run, labelling 80 alerts, the 2x2 run and scoring. That is too much for one month.
*Fix:* RQ2 does not need the held-out set. Build and label the triage set from development-phase alerts in Feb-Mar, and run a **10-alert pilot of the whole 2x2 pipeline in Dec-Jan** (the guide's "vertical slice" feasibility test). Keep only the F-criteria measurements and the held-out Wazuh comparison for April.

## Things from the guide worth adding to the thesis

- **Claim record with a rejected claim.** One page in the repo: strongest supported claim, weaker fallback, one deliberately rejected stronger claim, residual uncertainty. Draft: *"In a lab with simulated attacks, a Sigma-based prototype meets F1-F8 on this attack matrix; it is not shown to work in a real organisation or to replace a SOC."*
- **Decision log and controlled-change record.** The title change and dropping the SME focus are exactly the kind of change the guide wants logged with trigger, change and approval.
- **TRACE record of AI use.** The guide, and ASE rules it cites, require disclosed, verified AI use and that the student can explain and reproduce every decisive step without the chat. This project uses Claude for code and planning, so keep a short log and make sure Lucian can explain the normaliser, the scoring script and every reference label himself. The reference labels must be Lucian's own work.
- **Premortem.** Three failure mechanisms, earliest warning, one response each (guide section 2.6). Suggested: model too weak so every condition hallucinates (floor effect); Wazuh lab install eats March; labelling takes longer than planned.
- **Supervisor working agreement.** Which decisions need written approval (thresholds, scope cuts, title).
- **Demo as evidence path.** In the defence, show the chain from a Sigma rule through CI test, alert, normalised text, triage output and approval log, then the scorecard, not a product tour.
- **Floor and ceiling check for RQ2.** If a 7-8B model hallucinates almost always or almost never in the pilot, H1 cannot be tested. Check this in the pilot and, if needed, pick another model before `prereg-v1`.

## Fallback ladder (guide's continue / narrow / pivot)

- **Continue** as designed if the Dec-Jan pilot works.
- **Narrow** if by end of February the Wazuh lab or labelling is behind: drop F1 and F2 repetitions to one run each, drop F8's second model, keep F3, F4, F6 against Wazuh and the full RQ2.
- **Pivot** only if the local model proves unusable: keep RQ1 as a pure Björk-style scorecard (plan Option A), still defendable and low risk.

## Hostile questions to rehearse

1. Wazuh is open source and already a SIEM. What did you contribute?
2. Who chose the attack techniques, who wrote the rules, who wrote the labels? Why is this not circular?
3. Why 500 events/s and 30% false positives?
4. H2 says playbooks improve steps. You wrote both. What stops this being copying?
5. What result would have made you say "not feasible"?
6. Which parts of the code and the labels did you write yourself, and can you explain the scoring script?
