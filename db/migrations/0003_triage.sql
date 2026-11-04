-- 0003: LLM triage outputs, with everything needed to reproduce or audit a run.
--
-- Rows are append-only (see 0004): a re-run adds a row with a new run_number, so a worse
-- run can never be silently replaced by a better one.

BEGIN;

CREATE TABLE triage_outputs (
    triage_id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    alert_id            bigint      NOT NULL REFERENCES alerts ON DELETE RESTRICT,
    created_at          timestamptz NOT NULL DEFAULT clock_timestamp(), -- F5: MTTA end point
    -- Experiment bookkeeping. NULL condition = live triage outside the 2x2 experiment,
    -- which uses the full system's setup (C4).
    condition           text        CHECK (condition IN ('C1', 'C2', 'C3', 'C4')),
    run_number          smallint    NOT NULL DEFAULT 1 CHECK (run_number >= 1),
    wrong_playbook      boolean     NOT NULL DEFAULT false,        -- control runs (4.2)
    -- Model and runtime.
    model_tag           text        NOT NULL,                      -- e.g. name:tag
    model_digest        text        NOT NULL CHECK (model_digest ~ '^[0-9a-f]{64}$'),
    ollama_version      text        NOT NULL,
    temperature         numeric     NOT NULL CHECK (temperature >= 0),
    seed                bigint      NOT NULL,
    -- Prompt and inputs.
    prompt_path         text        NOT NULL,                      -- e.g. triage/prompts/...
    prompt_sha256       text        NOT NULL CHECK (prompt_sha256 ~ '^[0-9a-f]{64}$'),
    input_format        text        NOT NULL CHECK (input_format IN ('raw_json', 'normalised')),
    playbook_version_id bigint      REFERENCES playbooks ON DELETE RESTRICT,
    input_text          text        NOT NULL,                      -- exact text sent
    input_sha256        text        NOT NULL CHECK (input_sha256 ~ '^[0-9a-f]{64}$'),
    git_commit          text        NOT NULL CHECK (git_commit ~ '^[0-9a-f]{40}$'),
    -- Output.
    output              jsonb,                                     -- NULL if unparseable
    output_raw          text        NOT NULL,                      -- as returned by Ollama
    schema_valid        boolean     NOT NULL,                      -- triage/output_schema.json
    validation_errors   text[]      NOT NULL DEFAULT '{}',         -- triage.validate_output
    latency_ms          integer     CHECK (latency_ms >= 0),
    -- The design's conditions fix the inputs: C1/C2 raw JSON, C3/C4 normalised text;
    -- C2/C4 with a playbook, C1/C3 without.
    CHECK (condition IS NULL
           OR (condition IN ('C1', 'C2')) = (input_format = 'raw_json')),
    CHECK (condition IS NULL OR condition = 'C2' OR condition = 'C4'
           OR playbook_version_id IS NULL),
    CHECK (condition NOT IN ('C2', 'C4') OR playbook_version_id IS NOT NULL),
    CHECK (NOT wrong_playbook OR playbook_version_id IS NOT NULL),
    CHECK (output IS NOT NULL OR NOT schema_valid),
    UNIQUE (alert_id, condition, wrong_playbook, run_number, model_digest, prompt_sha256)
);

CREATE INDEX triage_outputs_alert_idx ON triage_outputs (alert_id);

INSERT INTO schema_migrations (version) VALUES ('0003_triage');

COMMIT;
