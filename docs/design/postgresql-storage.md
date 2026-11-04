# PostgreSQL storage and SQL-compiled detection

Status: draft, 2026-11-04. Decision by Lucian: PostgreSQL is the store for events, alerts,
rules, playbooks, triage outputs, approvals and the audit log. This note records how; the
research design (`docs/thesis/research-design.md`) is unchanged by it.

## Why PostgreSQL (short)

One container, no cluster to tune, fits the one-command install (F1) and the 4 vCPU / 8 GB
target (F2). JSONB plus GIN indexes covers schemaless event fields; constraints and triggers
let the database itself enforce the approval and reproducibility rules the thesis relies on.
Whether it sustains 500 events/s on the F2 hardware is **not measured yet**; the F2 load test
decides that, and its result goes into `docs/decisions/0001-storage-choice.md`.

## Deployment

- `docker-compose.yml` service `postgres`, image `postgres:17.11-alpine` pinned by digest.
  No host port is published; only services on the compose network reach it.
- `db/migrations/NNNN_*.sql` are mounted into `/docker-entrypoint-initdb.d`, so a plain
  `docker compose up -d` creates the schema on first start. That hook only runs on an empty
  data volume; once a second schema version is needed, a small runner (apply files whose
  version is missing from `schema_migrations`) replaces it. Each file records itself there.
- CI job `migrations` starts the compose service on a fresh volume and runs
  `db/tests/smoke.sql` (inserts one row per table, checks the refusals below, rolls back).

## Schema (db/migrations)

| Table | Purpose | Thesis link |
|---|---|---|
| `rules`, `playbooks`, `playbook_steps` | Each deployed version of a rule/playbook, keyed by content SHA-256 and Git commit | Rules frozen at a tagged commit; alerts point to exact rule text |
| `events` | Normalised events, fields in JSONB, `run_label` tags lab runs | F2 load, F4 benign run |
| `alerts`, `alert_events` | Alert per rule version, with the events behind it | `created_at` is the MTTD end point (F5) |
| `triage_outputs` | One row per LLM call: condition C1-C4, run number, wrong-playbook flag, model tag + digest, Ollama version, temperature, seed, prompt path + hash, exact input + hash, Git commit, raw and parsed output, validation result | RQ2 reproducibility; `created_at` is the MTTA end point (F5) |
| `approvals` | Human decision on a proposed `response_action` | Section 5 |
| `audit_log` | Every insert/update/delete on rules, playbooks, alerts, triage outputs, approvals, with actor | Section 5 "every decision is logged" |

Rules the database enforces:

- An approval must reference a playbook step whose `response_action` equals the approved
  action, and a step with a `response_action` must have `requires_approval` set.
- An approval decision is final; only the execution result can be added, once.
- `triage_outputs` and `audit_log` are append-only (update, delete and truncate are refused),
  so a re-run adds a row and can never replace an earlier one.
- The condition fixes the inputs: C1/C2 raw JSON, C3/C4 normalised; C2/C4 need a playbook,
  C1/C3 must not have one.
- The actor in the audit log comes from `SET LOCAL siem.actor = '<user>'`, set by the dashboard
  per transaction, falling back to the database user.

Limitation: a database superuser can disable triggers. The log is tamper-resistant against
the application, not against the database administrator. A hash chain or shipping the log
off-host would close that gap and is out of scope (D4).

## Detection: Sigma compiled to SQL

**Backend check (2026-11-04, PyPI JSON API and a web search).** There is no
`pySigma-backend-postgresql` (or `-postgres`, `-sql`) on PyPI. The only SQL backend from
SigmaHQ is `pySigma-backend-sqlite` (2.1.1 needs pySigma ≥ 2; 2.0.0 declares
`pysigma>=1.5.1,<2.0`, so it fits our pin `pysigma==1.5.1`). Outside pySigma, RSigma
(rsigma.io, v0.24.0, 2026-10-05) has a PostgreSQL/TimescaleDB backend that emits
`CREATE VIEW` statements over JSONB and supports Sigma correlation, but it is a separate
non-Python toolchain.

**Plan.** Write a small in-repo backend, `detect/pg_backend.py`, on pySigma's
`TextQueryBackend` (using the SQLite backend as the template), that turns a rule's condition
into a `WHERE` clause over `events.fields` (`fields->>'x' = ...`, `ILIKE` for
contains/startswith/endswith, `~` for `re`, `inet <<= cidr` for `cidr`), plus a processing
pipeline that maps Sigma field names and `logsource` onto the normalised schema. Then:

1. `python -m detect.compile` loads each rule from `rules/`, records it in `rules`, and creates
   `detect.r_<rule_id>` as a view: matching `events` rows for that logsource.
2. A detection loop (in the ingest service, every few seconds) selects from each view where
   `event_id > detect.watermarks.last_event_id`, inserts alerts and alert events, and moves the
   watermark, in one transaction. Identity order equals commit order only with a single
   writer (the ingest service); with several writers the loop needs a small lag margin.
3. Threshold and correlation rules (for example T1110.001: many failed logins from one source
   in N minutes) are PL/pgSQL functions in `detect`, kept in `rules/` next to their tests and
   recorded with `kind = 'threshold'`. Sigma correlation rules can move into the backend later.
4. CI keeps `detect/evaluator.py` as the test oracle: for every rule test event, the SQL view
   and the Python evaluator must agree. Unsupported Sigma features fail compilation loudly,
   as the evaluator does today.

New dependency when this is built: a PostgreSQL driver for the ingest service (to be chosen
and pinned in `ingest/requirements.txt`, with the reason), and `pySigma-backend-sqlite==2.0.0`
only if the backend reuses its code.

## Open points

- F2 load test on this schema (insert rate, view scan cost at 500 events/s; partitioning
  `events` by day only if needed).
- Retention for `events` (the 24 h benign run and attack runs are small; production retention
  is not a thesis question).
- Least-privilege database roles for ingest and dashboard (today one `siem` user).
