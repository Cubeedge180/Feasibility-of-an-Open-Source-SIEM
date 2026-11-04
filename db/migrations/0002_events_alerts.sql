-- 0002: normalised events, alerts and detection progress.

BEGIN;

-- One row per normalised event. `fields` holds the event under the normalised field names;
-- the pySigma processing pipeline maps Sigma field names (e.g. EventID) onto them when rules
-- are compiled to views.
CREATE TABLE events (
    event_id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    received_at timestamptz NOT NULL DEFAULT now(),    -- when ingest stored it
    event_time  timestamptz NOT NULL,                  -- timestamp inside the event
    host        text        NOT NULL,
    agent_id    text,
    product     text,                                  -- Sigma logsource.product
    service     text,                                  -- Sigma logsource.service
    category    text,                                  -- Sigma logsource.category
    fields      jsonb       NOT NULL,
    raw         text,                                  -- original line or XML, if kept
    run_label   text                                   -- lab run tag (attack/benign run id)
);

-- BRIN suits append-only, time-ordered data and stays small at F2's event rate.
CREATE INDEX events_event_time_brin ON events USING brin (event_time);
CREATE INDEX events_logsource_idx ON events (product, service, category);
CREATE INDEX events_fields_gin ON events USING gin (fields jsonb_path_ops);
CREATE INDEX events_run_label_idx ON events (run_label) WHERE run_label IS NOT NULL;

CREATE TABLE alerts (
    alert_id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rule_version_id  bigint      NOT NULL REFERENCES rules ON DELETE RESTRICT,
    created_at       timestamptz NOT NULL DEFAULT clock_timestamp(), -- F5: MTTD end point
    first_event_time timestamptz NOT NULL,
    last_event_time  timestamptz NOT NULL,
    host             text,
    severity         text        NOT NULL
                     CHECK (severity IN ('informational', 'low', 'medium', 'high', 'critical')),
    technique_ids    text[]      NOT NULL DEFAULT '{}',
    summary          jsonb       NOT NULL DEFAULT '{}', -- key fields shown to analyst and LLM
    status           text        NOT NULL DEFAULT 'new'
                     CHECK (status IN ('new', 'triaged', 'acknowledged', 'closed')),
    CHECK (first_event_time <= last_event_time)
);

CREATE INDEX alerts_created_at_idx ON alerts (created_at);
CREATE INDEX alerts_status_idx ON alerts (status) WHERE status <> 'closed';

-- Events that make up an alert (one for a single-event Sigma match, many for a threshold).
CREATE TABLE alert_events (
    alert_id bigint NOT NULL REFERENCES alerts ON DELETE CASCADE,
    event_id bigint NOT NULL REFERENCES events ON DELETE RESTRICT,
    PRIMARY KEY (alert_id, event_id)
);

CREATE INDEX alert_events_event_idx ON alert_events (event_id);

-- Highest event_id each rule version has already been evaluated against, so the detection
-- loop only scans new events and never raises the same alert twice.
CREATE TABLE detect.watermarks (
    rule_version_id bigint      PRIMARY KEY REFERENCES rules ON DELETE CASCADE,
    last_event_id   bigint      NOT NULL DEFAULT 0,
    updated_at      timestamptz NOT NULL DEFAULT now()
);

INSERT INTO schema_migrations (version) VALUES ('0002_events_alerts');

COMMIT;
