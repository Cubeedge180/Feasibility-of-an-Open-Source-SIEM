-- 0005: records the normaliser could not parse. Kept, not dropped, so lost events show up
-- as a per-run data-quality count instead of disappearing from the evidence.

BEGIN;

CREATE TABLE ingest_rejects (
    reject_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    received_at timestamptz NOT NULL DEFAULT now(),
    tag         text        NOT NULL,              -- shipper source tag (windows, auditd, auth)
    error       text        NOT NULL,
    record      jsonb       NOT NULL               -- the record exactly as shipped
);

CREATE INDEX ingest_rejects_received_at_idx ON ingest_rejects (received_at);

INSERT INTO schema_migrations (version) VALUES ('0005_ingest_rejects');

COMMIT;
