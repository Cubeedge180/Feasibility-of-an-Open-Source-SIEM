# Project overview

Start here. This folder explains what the project is for, how it is evaluated, and when each
part happens. The detailed, binding documents live elsewhere and are linked below.

Thesis: *Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage*
(bachelor thesis, prototype and evidence in this repository).

## 1. Goal

Build, test and document a lightweight SIEM for organisations that cannot afford Splunk-class
tools and have no dedicated SOC:

- **Easy to install:** one agent per host, one `docker compose up` for the server.
- **Detection as code:** Sigma rules versioned in Git, each with positive and negative test
  events, linted and tested in CI.
- **Private triage:** a locally hosted LLM (Ollama) explains each alert and proposes remediation.
  No data leaves the network.
- **Human in the loop:** response actions are only proposed; nothing runs without approval.

Two outputs: a working, demonstrable prototype (this repo plus a demo video) and measured
evidence for the thesis, compared against a Wazuh baseline.

## 2. Approach

Route: **build and evaluate**. The object under test is this prototype; Wazuh is the reference.

| Question | What it asks | How it is answered |
|---|---|---|
| RQ1, feasibility | Can an organisation without a SOC run this system? | Scorecard F1-F8 (install, hardware, detection, noise, speed, privacy, cost, triage trust), each with a threshold fixed in advance; "feasible" = every *must* criterion met. Same lab runs against Wazuh; headline comparison on held-out techniques only. |
| RQ2, grounding | Do normalised alert text (H1) and structured playbooks (H2) make local-LLM triage less hallucinated and more correct? | 2 x 2 within-subjects experiment on ~80 hand-labelled lab alerts, one 7-8B model, temperature 0, fixed seed, blind rating, one-sided Wilcoxon tests. |

Attacks come from Atomic Red Team and run only inside the isolated lab. The thresholds, hypotheses
and analysis are pre-registered: `research-design.md` is frozen by the git tag `prereg-v1` before
the final runs, and later changes are only dated amendments.

Claim limits: lab, simulated attacks, this attack matrix, this hardware, this model. No claim
that it replaces a SOC or a commercial SIEM. **No results have been measured yet.**

## 3. Timeline

See [timeline.md](timeline.md) for the month-by-month plan and the current status.
Week-by-week lab steps are in [`docs/lab-phase-plan.md`](../lab-phase-plan.md).

## 4. Where to read more

| Document | Role |
|---|---|
| [`docs/thesis/research-design.md`](../thesis/research-design.md) | **Source of truth** for RQs, thresholds and analysis |
| [`docs/thesis/decision-log.md`](../thesis/decision-log.md) | Every design decision (D1, D2, ...) with trigger and approval |
| [`docs/thesis/claim-record.md`](../thesis/claim-record.md) | The allowed claim, the fallback, the rejected claims |
| [`docs/thesis/defendability-review.md`](../thesis/defendability-review.md) | Review against the Student's Guide; seven fixes adopted (D7) |
| [`docs/lab-build-guide.md`](../lab-build-guide.md) | How the lab is built (VMs, Sysmon, Wazuh, Atomic, measurement) |
| [`docs/lab-phase-plan.md`](../lab-phase-plan.md) | Week-by-week lab plan, Nov 2026 - Apr 2027 |
| [`docs/design/postgresql-storage.md`](../design/postgresql-storage.md) | Storage design (PostgreSQL) |
| [`source/project-brief.md`](source/project-brief.md) | Original project brief (snapshot; partly superseded) |
| [`source/thesis-plan.md`](source/thesis-plan.md) | How the research design was reached (Options A-C) |
| [`related-work/`](related-work/) | Literature search notes: closest bachelor and master's theses |
| [`CHANGELOG.md`](../../CHANGELOG.md) | What changed, by pull request |

Not in the repo on purpose: the methodology Word document (superseded by `research-design.md`)
and all real lab details (IP addresses, hostnames, machine details), which stay on the author's
machine only.
