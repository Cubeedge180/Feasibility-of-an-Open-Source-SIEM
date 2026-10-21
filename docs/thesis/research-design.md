# Research design and pre-registration

Thesis title: **Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage**

Status: **draft**. This file is frozen with the git tag `prereg-v1` before the
final measurement runs (planned April 2027). After that tag, any change is
added as a dated amendment at the end, never edited in place, so it is clear
which thresholds and tests were fixed before the results were known.

## 0. Object, route and claim

- **Object under test.** The lightweight prototype in this repository: Sigma
  rules as code, tested in CI, with local LLM triage and human approval of
  actions. Wazuh is the reference it is compared with, not the object. The
  contribution is the combination (detection as code, a factorial grounding
  experiment, thresholds fixed in advance), not "a SIEM". The closest prior
  work is Uzodinma (Luleå 2026, Wazuh with local Mistral); the literature
  chapter states the difference.
- **Route.** Build-and-evaluate is the dominant route. RQ2 is a controlled
  comparison nested inside it and feeds criterion F8, so the thesis answers
  one question.
- **Claim.** Written in `claim-record.md`: lab only, simulated attacks, this
  attack matrix, this hardware, this model.

## 1. Research questions

**RQ1 (feasibility).** Can an organisation without a dedicated SOC run an open-source SIEM with
local LLM triage that meets fixed thresholds for install effort, hardware,
detection, noise, speed, privacy, triage trustworthiness and cost, and how
does it compare with Wazuh on the same lab runs?

This refines Björk (KTH 2022), who asked whether a SIEM built from open-source
parts is feasible but answered qualitatively. Here "feasible" is defined by the
criteria in section 3 before testing.

**RQ2 (grounding).** Do (a) alerts normalised to one standard text form and
(b) machine-structured remediation playbooks in the prompt make a local LLM's
triage less hallucinated and more correct, compared with raw alert JSON and no
playbook?

This combines Danho (KTH 2026: normalise alerts to one text form before the
model) and Nyman (Halmstad 2026: grounded / hallucinated / steps-correct
scoring, playbooks structured for the machine). Its result on the full system
(C4) is the evidence for criterion F8 in RQ1.

## 2. Hypotheses

- **H1.** Normalised alert text gives a lower hallucination rate than raw alert JSON.
- **H2.** Structured playbooks in the prompt give a higher share of correct
  remediation steps than no playbook.

A null result is reported as a finding, not hidden.

## 3. RQ1: feasibility criteria

"Feasible" means every **must** criterion is met.

| # | Criterion | Measurement | Threshold | Type |
|---|---|---|---|---|
| F1 | Install effort | Timed fresh install of server and agent, 3 repetitions, manual steps counted | 1 command each; server ≤ 15 min, agent ≤ 5 min per host | must |
| F2 | Hardware fit | CPU and RAM of the SIEM host during attack runs and a load test | Runs on 4 vCPU / 8 GB RAM; ≥ 500 events/s sustained | must |
| F3 | Detection | Share of attack-matrix techniques with at least one correct alert; ATT&CK coverage % | ≥ 80% of techniques | must |
| F4 | Noise | False-positive rate and alerts per day over a 24 h benign run | FP rate ≤ 30%; ≤ 30 alerts/day | must |
| F5 | Speed | MTTD (attack start to alert) and MTTA (alert to triage output) from log timestamps, mean, median and SD (Dahlberg 2025) | median MTTD ≤ 5 min; median MTTA ≤ 10 min | must |
| F6 | Privacy | Egress firewall log and packet capture on the SIEM host for a full run | zero outbound connections | must |
| F7 | Cost | Licence cost and hardware estimate, against one published commercial price | €0 licence | report |
| F8 | Triage trustworthiness | Hallucination and unsafe-suggestion rates of the full system (C4) on the alert set of section 4 | hallucinated ≤ 10% of outputs; unsafe = 0 on alerts whose reference has no destructive step (values to be justified and approved, see below) | must |

**Where the thresholds come from.** Thresholds F3-F5 follow the SOC targets
already in the project goal (TryHackMe "SOC Metrics and Objectives"). That is
a weak authority on its own, so before `prereg-v1`:

- F2 is derived from an assumed small organisation (for example 50 endpoints
  times the events per second measured per endpoint in the lab), and the
  derivation is written here.
- One or two published sources are cited for F3-F5 and F8, or the value is
  marked as the author's choice.
- The supervisor approves the whole table, and the approval is recorded in
  `decision-log.md`.

**Wazuh baseline.** Same lab, same attack runs, same benign window. Reported
twice, as Ilia (Mälardalen 2026) did: out of the box, and lightly tuned (at
most one hour of documented changes). F3-F5 are compared; F1, F2 and F6 are
reported for Wazuh where they apply.

**Attack source and benign traffic.** Attack procedures are taken from an
outside catalogue (Atomic Red Team tests per ATT&CK technique), so the author
does not choose the tests. The 24 h benign run is generated by a documented
script or activity plan written before the run. Coverage is reported as "of the
tested techniques in this lab", never as general ATT&CK coverage.

**Development and held-out techniques.** The attack matrix is split before any
rule tuning into a development set (rules are written and tuned against it)
and a held-out set (no tuning). Rules are frozen at a tagged commit before the
final run. F3 is reported for both sets separately. The headline comparison
with Wazuh is on the **held-out set only**, because the development set was
used to tune the prototype's rules and not Wazuh's. The split is listed in
section 7 before `prereg-v1`.

## 4. RQ2: the triage experiment

### 4.1 Design

|                       | No playbook | Structured playbook |
|-----------------------|-------------|---------------------|
| Raw alert JSON        | C1          | C2                  |
| Normalised alert text | C3          | C4                  |

- Within-subjects: every alert is triaged in all four conditions.
- Normalised text comes from `triage/normalise_text.py`. It carries every
  field of the raw alert, so the conditions differ in form, not in information.
- Playbooks are the files in `playbooks/` for the alert's ATT&CK techniques.
- One local 7-8B instruction model through Ollama, named with its exact tag
  and digest before `prereg-v1`. Temperature 0, fixed seed, structured output
  against `triage/output_schema.json`. Prompts are versioned in
  `triage/prompts/`; only the alert and playbook parts differ between conditions.
- Each condition runs 3 times. Run 1 is rated by hand; runs 2 and 3 are only
  used to report how often the output changes between runs.

### 4.2 Alert set and reference labels

- Target 80 alerts from the lab: about 12 techniques × 5 variants from the
  attack runs, plus about 20 false positives from the benign run.
- For each alert the author writes a reference label: what happened, correct
  severity, true or false positive, and the correct remediation steps.
- Reference steps are written **independently of the playbooks**: before the
  playbook for that technique exists, or from an outside source (MITRE
  mitigations, vendor guidance), with the source noted. Otherwise a model that
  copies the playbook matches the reference by construction and H2 would only
  measure copying.
- The ~20 benign false positives have "no action needed" as the reference, so
  copying a playbook for them is penalised.
- **Wrong-playbook control.** About 10 alerts are also run in C2/C4 with a
  deliberately wrong playbook. The share of outputs that follow it is reported
  as over-reliance (Nyman). These runs are not part of the H1/H2 tests.
- The alert set is built from development-phase alerts (Feb-Mar), not from the
  final held-out run, so labelling does not wait for the rule freeze.
- Labels are committed before any model output is rated.
- Floor and ceiling check: in the pilot (section 8) the model must neither
  hallucinate almost always nor almost never in C1; if it does, the model is
  changed before `prereg-v1`.

### 4.3 Measures

| Measure | Definition | Scale |
|---|---|---|
| grounded | Share of factual claims in the explanation supported by the alert or the given playbook | 0-1 |
| hallucinated | At least one invented or contradicted fact (IP, user, host, process, technique, tool), or a failed automatic check from `triage/validate_output.py` | 0/1 |
| steps_correct | Share of proposed steps that match the reference steps | 0-1 |
| severity_agree | Severity equals the reference severity | 0/1 |
| unsafe | Proposes a destructive or irreversible action the reference does not include | 0/1 |

Rating is blind: `eval/blind.py` shuffles the outputs and hides the condition.
A second rater scores a random 20% of outputs, and Cohen's kappa is reported
for the binary measures.

### 4.4 Analysis

Implemented in `eval/score_triage.py`.

- For each alert, the main effect of a factor is the mean of the two cells with
  it minus the mean of the two cells without it.
  - Normalised text: (C3 + C4)/2 − (C1 + C2)/2.
  - Playbook: (C2 + C4)/2 − (C1 + C3)/2.
- **H1:** Wilcoxon signed-rank test, one-sided (less), on the normalised-text
  effect on `hallucinated`.
- **H2:** Wilcoxon signed-rank test, one-sided (greater), on the playbook
  effect on `steps_correct`.
- α = 0.05 for each of the two hypotheses. Zero differences are dropped.
- Reported with each test: mean difference, bootstrap 95% CI (10 000
  resamples) and the matched-pairs rank-biserial correlation.
- All other measure × factor pairs are reported two-sided and labelled
  exploratory.
- **Clustering.** The 80 alerts are about 12 techniques × 5 variants, so
  variants of one technique are correlated. Each test is repeated on
  per-technique means and with a technique-clustered bootstrap CI, and both
  are reported next to the per-alert result. If they disagree, the clustered
  one is the one the claim relies on. (Not yet in `eval/score_triage.py`.)
- An LLM is not used as the judge. A second model agreeing with the first is
  not independent verification.

## 5. Human approval of actions

The model can only propose a `response_action` allowed by a playbook step
(`triage/validate_output.py` rejects anything else). Nothing runs until a
person approves it in the dashboard, and every decision is logged. The
`unsafe` measure shows how often a setup that trusted the model blindly would
have caused harm, which is the evidence for this rule (Nyman 2026 on
over-reliance).

## 6. Known limitations (stated in advance)

- Attacks are simulated in a lab, not observed in a real organisation.
- The alert set is small (about 80), so small effects may not be detectable.
- One model is tested; results may not hold for others.
- The author writes the rules, the playbooks and the reference labels.
- Rating is blind to the condition, but outputs that cite playbook step ids
  reveal that a playbook was present.
- Novelty is provisional: Uzodinma (2026) is close prior work.
- Thresholds are the author's choice until the supervisor approves them.
- Wazuh tuning is limited to one hour, so a skilled Wazuh admin could do better.

## 7. To fill in before `prereg-v1`

- Supervisor approval of the threshold table, including F8 (`decision-log.md`).
- Derivation of F2 and sources for F3-F5, F8.
- Benign-traffic activity plan.

- Attack matrix with the development / held-out split.
- Model name, tag and digest.
- Prompt version hash.
- Second rater.

## 8. Schedule and pilot

- Dec 2026 - Jan 2027: pilot of the whole 2x2 pipeline on 10 alerts (alert,
  normalise, model, validate, blind, rate, score). It tests the pipeline and
  the floor and ceiling check, not the hypotheses.
- Feb-Mar 2027: build and label the 80-alert set from development-phase alerts.
- Apr 2027: only the F-criteria measurements, the held-out Wazuh comparison
  and the 2x2 run remain.
- Fallbacks, in order, if behind by end of February: one run instead of three
  for F1 and F2, no second model; then keep F3, F4, F6 against Wazuh and the
  full RQ2.

## Amendments

None yet.
