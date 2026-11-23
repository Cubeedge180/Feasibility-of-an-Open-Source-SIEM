# Changelog

What changed in this repository, newest first, one entry per pull request. Each pull request also
carries GitHub labels (`area: lab`, `area: thesis`, `area: detection`, `area: triage`,
`area: infra`, `area: security`, `documentation`) so changes can be filtered on GitHub.

No measured results exist yet; entries describe code, documents and lab setup only.

## Unreleased (open pull requests)

- **Week 3 agent, normalisers and inline detection** (this PR, D11): `agent/` has Fluent Bit 5.1.3
  configs and one-command installers for Windows (Security + Sysmon) and Kali (auditd + auth.log,
  installs rsyslog), with an on-disk buffer and token auth. `normalize/` parses event XML, auditd
  and auth.log into events with native Sigma field names. `POST /v1/events` stores each event with
  its raw record, runs the Sigma rules inline and writes alerts in the same transaction;
  unparseable records go to the new `ingest_rejects` table (migration 0005). CI runs the ingest
  tests against PostgreSQL.
- **Knowledge graph and clustered scoring** (#13): `graphify-out/` holds a graphify knowledge graph
  of code and docs, kept current by a Stop hook (`.claude/hooks/graphify-stale.sh`).
  `score_triage` takes a required `alerts.csv` (one technique per alert) and repeats every test on
  per-technique means with a technique-clustered bootstrap CI; `claim_supported` is the clustered
  verdict (research design 4.5). Claim record and decision log link to the design and the code.
- **Evidence-check fixes from the 2026-11-23 audit** (this PR): blinded outputs no longer show
  `playbook_step_id` (it revealed C2/C4 to the rater); `score_triage` refuses key outputs with no
  rating; Sigma `|re|i`, `|re|m`, `|re|s` flags are honoured; triage records store input text,
  input SHA-256 and latency; `run_info()` refuses uncommitted code unless `allow_dirty=True`.
- **Project overview and changelog** (this PR): `docs/project/` with goal, approach, timeline and
  an index of all documents; snapshots of the project brief and thesis plan; literature search
  notes; this changelog; a "What's new" section in the README.
- **Lab plan, week 1-2 lab setup and secret guards** (#9): week-by-week lab plan
  (`docs/lab-phase-plan.md`), decisions D8-D10 (SIEM on Docker Desktop, one SIEM per pass, native
  Ollama with triage replay), pinned Sysmon and auditd configs with an arm64 audit-rule converter,
  lab time server (`lab/ntp/`), gitleaks config, pre-commit hook and CI secret scan.
- **Thesis structure model** (#8): ASE rules, chapter outline and mapping of chapters to code.

## 2026-11-04

- **PostgreSQL schema and storage design** (#7): `db/migrations/`,
  `docs/design/postgresql-storage.md`.
- **Lab build guide for an Apple-silicon Mac** (#6): `docs/lab-build-guide.md`.
- **Reproducible triage calls** (#5): Ollama image pinned by digest; triage calls send
  temperature 0 and a fixed seed and record model digest, prompt hash and commit.

## 2026-10-21

- **Claim record, decision log and defendability review** (#4): `docs/thesis/claim-record.md`,
  `decision-log.md`, `defendability-review.md`; seven review fixes adopted (D7).

## 2026-10-14

- **Thesis title set, SME focus dropped** (#3): decisions D2 and D3.
- **Research design, playbooks and triage experiment tooling** (#2):
  `docs/thesis/research-design.md`, `playbooks/` with schema, alert-to-text normaliser, blinding
  and scoring scripts.

## 2026-10-04

- **Repository scaffold** (#1): layout, first Sigma rule (`win_security_log_cleared`) with tests,
  rule linting, CI.
