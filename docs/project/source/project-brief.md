> **Snapshot** of the project brief as of 2026-11-04, copied from the project library.
> Where it differs from [`docs/thesis/research-design.md`](../../thesis/research-design.md) or the
> [decision log](../../thesis/decision-log.md), those files win (for example: PostgreSQL is the store,
> no Telegram approval, no Caldera chains, Python version per CI).

# Project goal: Accessible SIEM (bachelor thesis)

Thesis title (chosen 2026-10-14): **Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage**

The thesis has no SME focus; it targets organisations without a dedicated SOC.

## 1. Mission

Build, test and document a lightweight SIEM for organisations that cannot afford Splunk-class tools and have no dedicated SOC. The system must be easy to install (one agent, one `docker compose up`), use detection rules as code (Sigma, versioned in Git, tested in CI), and use a locally hosted LLM to explain each alert and suggest remediation without any data leaving the network.

The project serves two outputs: a working, demonstrable prototype (public GitHub repo, demo video) and the evidence for a bachelor thesis (measured results, comparison against a baseline).

## 2. Research questions

Updated 2026-10-14 (Option C in `thesis/thesis-plan.md`; exact version in the repo at `docs/thesis/research-design.md`):

1. **RQ1, feasibility (Björk 2022 refined):** can an organisation without a dedicated SOC run an open-source SIEM with local LLM triage that meets fixed thresholds for install effort, hardware, detection, noise, speed, privacy and cost, compared with Wazuh? ATT&CK coverage is one of the criteria.
2. **RQ2, grounding:** do alerts normalised to one text form (Danho 2026) and machine-structured playbooks (Nyman 2026) make the local LLM's triage less hallucinated and more correct? 2 x 2 experiment, hypotheses H1 and H2.

Scope cuts agreed with the plan: no Caldera chains, no resilience tests, dashboard approval only (no Telegram), ModSecurity optional, 24 h benign run.

## 3. Scope

### In scope (MVP, must ship)
- Log collection from Windows (Sysmon + Security events), Linux (auditd, auth.log), network (Suricata EVE JSON) and a vulnerable web app (ModSecurity audit logs).
- Ingestion API, normalization to a common schema (ECS-like), storage and search.
- Sigma rule engine: load rules from a Git-tracked folder, convert/evaluate them against normalized events, produce alerts with ATT&CK tags.
- Alert store plus a simple web dashboard (alert list, alert detail, ATT&CK coverage view).
- LLM triage: for each alert, generate a plain-language explanation, a severity assessment and remediation steps, using a local model through Ollama.
- Semi-automated response (SOAR-lite): proposed actions (block IP, disable account) executed only after human approval via Telegram or the dashboard.
- Automated test harness that runs attacks in the lab and computes the metrics below.
- CI pipeline: lint, rule unit tests (one positive and one negative event per rule), schema validation.

### Optional (only after MVP is done and measured)
- UEBA-lite behavioural baselines (login hours, volumes, locations).
- Pseudonymization of personal data (emails, IPs, national IDs) at ingestion, with audited reveal.
- Attack timeline / kill-chain graph reconstruction from correlated alerts.
- Edge filtering and dedup to reduce storage cost, with a cost comparison against Splunk/Elastic.

### Out of scope
- Production-grade multi-tenancy, HA clustering, commercial support features.
- Any testing against systems the author does not own. All attack simulation runs only inside the isolated lab.

## 4. Proposed architecture

Flow: attack tools -> isolated target lab -> sensors (Sysmon, auditd, Suricata, ModSecurity) -> shipper/agent -> ingestion API -> normalization -> storage -> Sigma detection -> alerts -> LLM triage -> SOAR-lite (human approval) -> metrics.

Suggested stack (change only with a written reason in `docs/decisions/`):
- Language: Python 3.12 for backend, detection engine and test harness.
- API: FastAPI. Queue: simple in-process or Redis Streams if needed.
- Storage: OpenSearch single node (events, alerts) or SQLite/PostgreSQL if OpenSearch proves too heavy. Decide in week 1 with a short benchmark.
- Sigma: `pySigma` with a custom backend or direct evaluation on the normalized schema.
- Agent/shipper: Vector or Fluent Bit config packaged with an installer script, so setup is one command per host.
- LLM: Ollama with a small instruction model, prompts versioned in `prompts/`, outputs validated against a JSON schema.
- Frontend: lightweight (HTMX or a small React app). No heavy design work.
- Packaging: Docker Compose for the server side.
- Lab: 4-5 VMs (Windows endpoint, Linux server, vulnerable web app such as DVWA or Juice Shop, Kali attacker, SIEM host) on an isolated host-only network.

## 5. Repository layout

```
siem/
  agent/            # shipper configs, installer scripts
  ingest/           # ingestion API
  normalize/        # parsers and common schema
  detect/           # Sigma loader, evaluator, alert builder
  rules/            # Sigma rules (one folder per ATT&CK tactic) + tests/
  triage/           # LLM client, prompts, output schema, evaluation set
  response/         # SOAR-lite actions and approval flow
  ui/               # dashboard
  lab/              # VM setup, network, attack playbooks (Atomic Red Team, Caldera)
  eval/             # harness, metrics computation, result tables
  docs/             # architecture, decisions, thesis notes
  .github/workflows/
```

## 6. Attack test matrix (MITRE ATT&CK)

Each row needs: technique, attack tool and test id, log source, Sigma rule, expected alert, result.

- Brute force / password spraying on SSH and RDP (T1110)
- Encoded PowerShell execution (T1059) and credential dumping (T1003)
- Persistence: scheduled tasks, Run keys (T1053, T1547)
- Defense evasion: log clearing, disabling security tooling (T1070, T1562)
- Discovery and lateral movement: port scan, SMB/RDP (T1046, T1021)
- Web attacks: SQLi, XSS, path traversal (T1190)
- C2 and exfiltration: beaconing, DNS tunneling (T1071, T1041)
- Ransomware-like behaviour using a harmless simulator (T1486)

## 7. Metrics and targets

Targets follow the TryHackMe "SOC Metrics and Objectives" room (SLA values and fix thresholds) and are measured automatically by `eval/`.

| Metric | Definition | Target | Fix trigger |
|---|---|---|---|
| MTTD | attack start -> alert in SIEM | <= 5 min | > 30 min |
| MTTA | alert created -> triage output delivered | <= 10 min | > 30 min |
| MTTR | alert created -> approved response executed | <= 60 min | > 4 h |
| Threat detection rate | detected / executed techniques | 100% | any miss becomes a finding |
| False positive rate | false alerts / total alerts on benign run | own target <= 20-30% | > 80% (room limit) |
| Alert escalation rate | alerts passed to a human / total | < 20% | > 50% |
| Alert volume | alerts per day on benign traffic | about 30 per analyst per day | flood, or zero alerts |

Additional thesis metrics: events per second ingested, ingestion latency, CPU/RAM use, LLM triage correctness and hallucination rate against a hand-labelled set, ATT&CK coverage percentage.

Baseline: Wazuh with default rules on the same lab and the same attack runs.

## 8. Evaluation phases

1. Rule unit tests in CI (positive and negative sample per rule).
2. End-to-end: run each technique, verify alert, severity and timing.
3. Full attack chains with Caldera, verify correlation and timeline.
4. 24-48 h benign traffic run to measure false positives and alert volume.
5. Performance and load tests.
6. Resilience: agent down, log loss, attacker deleting logs.
7. LLM evaluation on a labelled alert set (correctness, severity, hallucinations), with and without the LLM to show the delta.
8. Purple-team loop: missed technique -> new rule -> retest, with before/after coverage.

## 9. Milestones

- Oct-Nov: literature and tool review, final stack decision, lab built, repo and CI skeleton.
- Dec-Jan: end-to-end prototype (one endpoint log source -> Sigma alert -> dashboard).
- Feb-Mar: all log sources, full rule set, LLM triage, SOAR-lite.
- Apr: all test phases run, results collected, baseline comparison done.
- May: thesis writing, figures from `eval/` results.
- Jun: polish, demo video, defense.

## 10. Working rules for Claude Code

- Work in small, reviewable steps. Propose a plan before large changes and keep each commit focused.
- Every new rule ships with positive and negative test events. Every new module ships with tests.
- Never hardcode secrets. Use environment variables and an `.env.example`.
- Keep a `docs/decisions/` log (short ADRs) for stack choices and trade-offs, because the thesis needs the reasoning.
- Record every experiment: command, date, commit hash, raw output saved under `eval/results/`. Thesis numbers must be reproducible from these files.
- Attack tooling and playbooks are for the isolated lab only. Never target external systems, and never add code that scans or attacks anything outside the lab network.
- LLM outputs must be schema-validated, and responses never execute actions on their own. Any response action requires explicit human approval.
- Prefer boring, well-documented tools over clever ones. Scope control matters more than features.

## 11. Definition of done

- One-command install of the server stack and one-command agent install per host.
- All MVP components working end to end in the lab, with CI green.
- Attack test matrix complete with a results table and ATT&CK coverage chart.
- Metrics measured and compared against the Wazuh baseline, with limitations stated honestly.
- Public repo with README, architecture diagram, setup guide and a short demo video.
- Thesis-ready material: figures, tables and decision log exported from the repo.

## 12. First tasks for the first session

1. Create the repo skeleton from section 5 with a README stating the mission and scope.
2. Write `docs/decisions/0001-storage-choice.md` after a quick benchmark of OpenSearch vs SQLite/PostgreSQL on a sample of Sysmon logs.
3. Define the normalized event schema and write parsers for Sysmon and auth.log, with tests.
4. Implement the Sigma loader and evaluate three starter rules (brute force, encoded PowerShell, log clearing) on sample events.
5. Add the GitHub Actions workflow that runs lint and the rule tests.
