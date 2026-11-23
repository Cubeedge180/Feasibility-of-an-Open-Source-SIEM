# ingest/

FastAPI service that agents ship to. At start it reads every rule under `rules/` and records
each version with its Git commit in `rules`; edit a rule, then `docker compose restart ingest`.

- `GET /health`
- `POST /v1/events`: JSON array of Fluent Bit records, `Authorization: Bearer $INGEST_TOKEN`,
  `X-Fluent-Tag: windows|auditd|auth`. Each record is normalised (`normalize/`), stored in
  `events` with its raw text, and checked against the rules with `detect/evaluator.py`; a match
  writes an alert and its `alert_events` row in the same transaction. Unparseable records go
  to `ingest_rejects`. Returns `{"stored", "rejected", "alerts"}`.

Needs `DATABASE_URL` and `INGEST_TOKEN` (16+ characters); refuses to start without the token.
Tests: `tests/test_ingest.py` (set `TEST_DATABASE_URL` to a PostgreSQL admin URL to run the
database tests locally).
