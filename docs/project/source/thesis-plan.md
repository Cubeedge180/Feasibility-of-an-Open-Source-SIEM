> **Snapshot** of the thesis plan (Option C) as of 2026-11-04, copied from the project library.
> [`docs/thesis/research-design.md`](../../thesis/research-design.md) is the source of truth for RQs,
> thresholds and analysis; this file explains how the design was reached.

# Thesis plan: what the work will prove

Thesis title (chosen 2026-10-14): **Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage**. No SME focus: the target is organisations without a dedicated SOC.

Draft, 2026-10-14. Lucian picked **Option C** on 2026-10-14. The repo version of the design, with exact thresholds and analysis, is `docs/thesis/research-design.md`; it is the source of truth from now on.

## 1. The problem with the current plan

The current three research questions describe a system and measure it. They do not state a claim that the results could prove wrong. A thesis "proves something" when it says in advance what result would count as success or failure, and then runs the test. This plan does that in two ways:

- **A feasibility claim with pass/fail thresholds** (Björk's question, made testable).
- **A controlled experiment on the LLM triage** (Danho's and Nyman's ideas, turned into hypotheses).

Both are written down and committed to the repo before any final measurement (a short "pre-registration"), so nobody can say the thresholds were picked after seeing the numbers.

## 1b. Review against the Student's Guide (2026-10-21)

The topic was checked against Clim & Aldrigo's *Student's Guide to Research Projects, Theses and Dissertations* (full report: `defendability-review.md`). Verdict: **defendable at bachelor level**, with seven fixes, now folded into this plan and into `research-design.md`:

1. One claim, not two studies: RQ2's result on the full system feeds a new must-criterion **F8 (triage trustworthiness)**. Build-and-evaluate is the dominant route.
2. The object under test is the lightweight Sigma + local LLM prototype. Wazuh is itself an open-source SIEM, so it is the reference, not the competitor in a "feasibility" claim.
3. H2 was close to circular, because the author writes playbooks and reference steps. Reference steps are now written independently, benign alerts have "no action" as the reference, and a wrong-playbook control measures over-reliance.
4. Thresholds need a source: derive F2 from an assumed organisation size, cite sources for F3-F5 and F8, get supervisor approval.
5. Attacks come from Atomic Red Team; the headline Wazuh comparison is on the held-out set only; the benign run follows a documented plan.
6. Novelty is provisional. Uzodinma (Luleå 2026, Wazuh with local Mistral) is the closest prior work.
7. The 80 alerts are 12 techniques × 5 variants, so the statistics are also reported per technique and with a clustered bootstrap.

Also added: `docs/thesis/claim-record.md` (claim, fallback, rejected claim) and `docs/thesis/decision-log.md` (title and SME-focus changes with trigger and approval).

## 2. Candidate research ideas

### Option A: Feasibility, made measurable (Björk refined)

> *Is it feasible for an organisation without a dedicated SOC to run an open-source SIEM, where "feasible" means meeting fixed thresholds for install effort, hardware, detection, noise, speed and privacy?*

Björk (KTH 2022) asked the same question but answered it qualitatively ("works, but not FortiSIEM standard"). The refinement is to define feasibility as a scorecard of criteria, each with a threshold set before testing, and to compare against Wazuh on the same lab runs. The verdict is per criterion: met or not met.

- Strength: a direct, clearly better successor to the top-ranked thesis. Low risk.
- Weakness: it is mainly engineering evaluation. The LLM part is only one more criterion.

### Option B: Does grounding the model reduce hallucination? (Danho + Nyman)

> *Does giving a local LLM (a) alerts normalised to one text form and (b) machine-structured remediation playbooks reduce hallucination and improve remediation correctness, compared with raw alert JSON and no playbook?*

A 2 × 2 experiment on the same hand-labelled alert set, scored with Nyman's three measures. The SIEM is the testbed, not the result.

- Strength: a real, falsifiable hypothesis with a statistical test. The most "provable" option.
- Weakness: on its own it drops Björk's feasibility frame, which you said you want to keep.

### Option C (recommended): Feasibility as the frame, the grounding experiment as the proof

> **Main question.** *Can an organisation without a dedicated SOC run an open-source SIEM with local LLM triage that meets fixed feasibility thresholds?*
>
> **The hypothesis tested inside it.** *Normalised alert text and machine-structured playbooks make the local LLM's triage measurably more grounded and more correct.*

This is the same system build as A and B together; only the evaluation is split into two clear parts. It keeps Björk's concept (RQ1), uses Danho's normalisation and Nyman's scoring and playbooks as the experiment (RQ2), and the human-approval rule becomes a design requirement backed by Nyman's over-reliance finding.

**Why C.** It answers "is this feasible?" with numbers instead of an opinion, and it contains one experiment whose result is not known in advance. Each part alone is bachelor-sized; together they fit if the scope cuts in section 6 are accepted. The old RQ3 (ATT&CK coverage vs Wazuh) is folded into RQ1 as a criterion, so the thesis has two research questions instead of three.

The rest of this plan assumes Option C. Options A and B are each a subset of it.

## 3. RQ1: Feasibility scorecard (Björk's idea, refined)

Every criterion is measured in the lab and judged against a threshold fixed in the pre-registration. "Feasible" means all **must** criteria are met.

| # | Criterion | How it is measured | Threshold | Type |
|---|---|---|---|---|
| F1 | Install effort | Timed fresh install of the server (`docker compose up`) and the agent on each host, 3 repetitions, steps counted | 1 command each, ≤ 15 min server, ≤ 5 min per agent | must |
| F2 | Hardware fit | CPU and RAM on the SIEM host during the attack runs and a load test; sustained events per second | Runs on 4 vCPU / 8 GB RAM, ≥ 500 EPS sustained | must |
| F3 | Detection | Detection rate over the attack matrix, and ATT&CK coverage % of the tested techniques; same runs against Wazuh default and lightly tuned (Ilia's method) | ≥ 80% of techniques detected; report the difference vs Wazuh | must |
| F4 | Noise | False-positive rate and alerts per day over a 24 h benign run | FP rate ≤ 30%, ≤ 30 alerts/day | must |
| F5 | Speed | MTTD and MTTA from log timestamps (Dahlberg's method), mean and standard deviation | median MTTD ≤ 5 min, MTTA ≤ 10 min | must |
| F6 | Privacy | Egress firewall log and packet capture on the SIEM host during a full run | zero outbound connections | must |
| F7 | Cost | Licence cost plus hardware estimate, compared with the published price of one commercial option | €0 licence | report |
| F8 | Triage trustworthiness | Hallucination and unsafe-suggestion rates of the full system (C4 in RQ2) | hallucinated ≤ 10% of outputs; unsafe = 0 where the reference has no destructive step | must |

Thresholds must be justified before testing: F2 derived from an assumed small-organisation size, sources for F3-F5 and F8, supervisor approval recorded in the decision log. Attack procedures come from Atomic Red Team, and the benign run follows a documented activity plan.

Fairness rules for the Wazuh comparison: same lab, same attack runs, same benign traffic window. The headline comparison is on the held-out techniques only. Wazuh is reported "out of the box" and "lightly tuned" (one hour of documented changes), as Ilia did.

Guard against overfitting the rules: the attack matrix is split into a **development set** (rules are written and tuned against it) and a **held-out set** of techniques the rules are not tuned on. Rules are frozen at a tagged commit before the final run, and detection is reported for both sets separately.

## 4. RQ2: The grounding experiment (Danho's and Nyman's ideas)

### 4.1 Hypotheses

- **H1 (normalisation, from Danho).** Alerts converted to one standard text form produce fewer hallucinated outputs than the same alerts given as raw JSON.
- **H2 (structured playbooks, from Nyman).** Adding machine-structured playbooks to the prompt raises the share of correct remediation steps compared with no playbook.
- Null result is a valid finding: if H1 or H2 fails, the thesis reports that and discusses why.

### 4.2 Design: 2 × 2, every alert seen in every condition

| | No playbook | Structured playbook |
|---|---|---|
| **Raw alert JSON** | C1 (baseline) | C2 |
| **Normalised alert text** | C3 | C4 (full system) |

- One local 7-8B instruction model through Ollama, temperature 0, fixed seed, prompts versioned in `triage/prompts/`. Each condition is run 3 times to check output stability; only run 1 is rated by hand (320 ratings, not 960).
- The same alerts go through all four conditions, so comparisons are paired.

### 4.3 The labelled triage set

- Built from real lab alerts: every attack run plus a sample of false positives from the benign run, target **80 alerts** (about 12 techniques × 5 variants, plus about 20 benign false positives).
- For each alert Lucian writes a reference label: what happened, correct severity, whether it is a true or false positive, and the correct playbook steps.
- Labels are written and committed **before** any model output is scored.
- Reference steps are written independently of the playbooks (before them, or from MITRE mitigations or vendor guidance), so H2 does not just measure copying. Benign alerts have "no action" as the reference.
- Wrong-playbook control: about 10 alerts also run with a deliberately wrong playbook; the share of outputs that follow it is reported as over-reliance. Not part of the H1/H2 tests.
- The set is built from development-phase alerts in Feb-Mar, so labelling does not wait for the April rule freeze.

### 4.4 Scoring (Nyman's three measures, plus two)

Each output is scored blind to its condition (outputs shuffled and condition hidden by a script).

| Measure | Definition | Scale |
|---|---|---|
| Grounded | Share of factual claims in the explanation supported by the alert fields or the playbook | 0-1 per output |
| Hallucinated | At least one invented or contradicted fact (IP, user, host, process, technique, tool) | yes/no per output |
| Steps correct | Share of proposed remediation steps that match the reference steps for that alert | 0-1 per output |
| Severity agreement | Model severity equals the reference severity | yes/no |
| Unsafe suggestion | Proposes a destructive or irreversible action the reference does not include | yes/no |

To make scoring partly automatic, the output schema forces the model to **cite the alert fields and playbook step ids it relies on**. A script checks that every cited field exists and every step id is real; the human rater handles the rest. A second rater (a classmate) scores a random 20% so inter-rater agreement (Cohen's kappa) can be reported.

### 4.5 Analysis

- For each alert, the effect of a factor is the mean of the two cells with it minus the mean of the two cells without it.
- H1: effect of normalised text on hallucination, Wilcoxon signed-rank test, one-sided.
- H2: effect of playbooks on steps correct, Wilcoxon signed-rank test, one-sided.
- Variants of one technique are correlated, so repeat each test on per-technique means and with a technique-clustered bootstrap CI; if they disagree, rely on the clustered result.
- No LLM acts as judge.
- Report effect sizes and 95% confidence intervals, not only p-values. With 80 paired alerts a medium effect is detectable; a small one may not be, and that goes in the limitations.

## 5. How the three borrowed ideas live in the system

### 5.1 Danho: one text form before the model sees the alert

A deterministic function builds the same sentence-style description for every alert from the normalised (ECS-like) fields, for example:

> At 2027-02-03 14:02:11 UTC, host WS01 (Windows 11) recorded: Security event log cleared by user CORP\bob using wevtutil.exe. Rule "Security Event Log Cleared" (T1685.005, Defense Impairment) matched on EventID 1102. Source IP: none.

It is code, not a model, so the same alert always gives the same text. This is the C3/C4 input. The thesis limitations section follows Danho's model: say plainly that attacks were simulated and the dataset is small.

### 5.2 Nyman: playbooks structured for the machine

One YAML file per ATT&CK technique in `playbooks/`, validated in CI against a schema:

```yaml
technique: T1110.001
title: SSH password brute force
indicators: [many failed logins from one source IP, same target user]
steps:
  - id: T1110.001-1
    phase: investigate
    action: Check whether any login from the source IP succeeded after the failures.
    destructive: false
  - id: T1110.001-2
    phase: contain
    action: Block the source IP at the host firewall.
    response_action: block_ip
    destructive: true
    requires_approval: true
```

The model is asked to pick and cite step ids, not to invent steps. Short, labelled fields are what Nyman found models use most reliably.

### 5.3 Nyman's over-reliance point: a human approves every action

- The model can only **propose** a `response_action` that exists in a playbook. Nothing runs until a person clicks Approve in the dashboard.
- Every approval and rejection is logged with the alert id and timestamp, so MTTR (alert to approved response) is measurable.
- The "unsafe suggestion" measure in 4.4 shows how often a blind-trust setup would have done harm, which is the evidence for the approval rule.

## 6. Scope cuts for limited time

Kept: everything RQ1 and RQ2 need. Cut or moved to "only if time is left":

| Item | Decision | Reason |
|---|---|---|
| Log sources | Keep Sysmon + Windows Security, Linux auth.log/auditd, Suricata. ModSecurity becomes optional | Enough for about 12 techniques |
| Caldera full attack chains | Cut | Not needed for either RQ |
| Resilience tests (agent down, log loss) | Cut, mention as future work | Not needed for either RQ |
| Telegram approval | Cut, dashboard approval only | Same evidence, less code |
| UEBA, pseudonymisation, timeline graph, edge filtering | Stay optional | Unchanged |
| Benign run | 24 h instead of 24-48 h | Enough for F4 |
| Second LLM model | Optional robustness check | One model answers H1/H2 |

Fallbacks if behind by end of February: one run instead of three for F1 and F2, no second model; then keep F3, F4, F6 against Wazuh plus the full RQ2. If the local model proves unusable, fall back to a pure Björk-style scorecard (Option A).

## 7. What changes in the repo (after an option is picked)

1. `docs/thesis/preregistration.md`: RQs, hypotheses, thresholds, dev/held-out technique split, analysis plan. Committed and tagged before measurement.
2. `triage/normalise_text.py` + tests: alert to standard text (5.1).
3. `playbooks/` + `playbooks/schema.json` + CI validation (5.2).
4. `triage/output_schema.json`: explanation, severity, cited fields, cited step ids, proposed action.
5. `triage/run_experiment.py`: runs the four conditions and saves raw outputs under `eval/results/`.
6. `eval/triage_set/`: alert set and reference labels; `eval/blind.py` to shuffle and hide conditions; `eval/score_triage.py` for automatic checks and statistics.
7. `eval/feasibility.py`: computes F1-F7 from the raw run files into one scorecard table.
8. `response/`: approval queue and log (5.3).

## 8. Timeline (to June 2027)

| When | Work |
|---|---|
| Oct-Nov 2026 | Pick option, write pre-registration, build lab, finish normalisation and Sysmon/auth.log parsers |
| Dec 2026-Jan 2027 | End-to-end: endpoint log to Sigma alert to dashboard; text normaliser; first playbooks. **Pilot of the whole 2 × 2 pipeline on 10 alerts**, including a floor/ceiling check on C1 |
| Feb-Mar 2027 | All kept log sources, dev-set rules, LLM triage with schema, approval flow, Wazuh lab install. Build and label the 80-alert set from development-phase alerts |
| Apr 2027 | Freeze rules (tag). Final attack runs, benign run, feasibility measurements, held-out Wazuh comparison, run the 2 × 2 experiment, score |
| May 2027 | Analysis and writing |
| Jun 2027 | Demo video, polish, defence |

## 9. Thesis outline

1. Introduction: cost of SIEM, organisations without a SOC; research questions.
2. Background: SIEM, Sigma and detection-as-code, ATT&CK, LLMs and hallucination.
3. Related work: Björk (frame), Dahlberg (timing method), Danho (normalisation), Nyman (scoring and playbooks), Ilia (Wazuh baseline).
4. Method: lab, attack matrix and dev/held-out split, feasibility criteria, 2 × 2 experiment, scoring, statistics, pre-registration.
5. System design: architecture, normaliser, playbooks, approval flow.
6. Results: feasibility scorecard vs Wazuh; H1 and H2 results.
7. Discussion: what is feasible and what is not; when grounding helps; over-reliance.
8. Limitations (Danho's model, stated openly): simulated attacks in a lab, not a real organisation; small alert set (80, in 12 technique clusters); one model; the author wrote the rules and the labels; one main rater; Wazuh tuning limited to one hour; thresholds are the author's choice until approved. The claim and the claim rejected are in `claim-record.md`.
9. Conclusion and future work.

## 10. Open choices for Lucian

- ~~Which option: A, B or C~~ Decided: C.
- Whether the feasibility thresholds in section 3 match what your supervisor expects; they are a starting point taken from the TryHackMe SOC targets already in the goal file.
- Whether a classmate can act as second rater for 20% of the triage set.
- Supervisor approval of the threshold table including F8, and of the decision-log entries.
- Whether the title should signal "lightweight, detection-as-code" (review fix 2).
- Which university rules apply (the Student's Guide is written for ASE Bucharest).
