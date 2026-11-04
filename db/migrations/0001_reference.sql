-- 0001: migration bookkeeping, detection rules and remediation playbooks.
--
-- Rules and playbooks live in Git (rules/, playbooks/). The loader copies each version it
-- deploys into these tables, keyed by content hash, so every alert and every triage output can
-- point at the exact rule text and playbook text that produced it, plus the Git commit.

BEGIN;

CREATE TABLE schema_migrations (
    version    text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now()
);

-- Generated SQL for Sigma rules (views) and procedural threshold/correlation rules
-- (PL/pgSQL functions) go in their own schema, so they can be dropped and regenerated
-- from Git without touching data.
CREATE SCHEMA detect;

CREATE TABLE rules (
    rule_version_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rule_id         uuid        NOT NULL,              -- Sigma `id`
    kind            text        NOT NULL CHECK (kind IN ('sigma', 'threshold', 'correlation')),
    title           text        NOT NULL,
    level           text        NOT NULL
                    CHECK (level IN ('informational', 'low', 'medium', 'high', 'critical')),
    technique_ids   text[]      NOT NULL DEFAULT '{}', -- e.g. {T1685.005}
    logsource       jsonb       NOT NULL DEFAULT '{}', -- Sigma logsource block
    source_path     text        NOT NULL,              -- path in the repo, e.g. rules/...yml
    source_text     text        NOT NULL,              -- the YAML (or SQL) as committed
    source_sha256   text        NOT NULL CHECK (source_sha256 ~ '^[0-9a-f]{64}$'),
    compiled_sql    text,                              -- what was generated into schema detect
    compiler        text,                              -- e.g. 'pysigma==1.5.1 + detect.pg_backend'
    git_commit      text        NOT NULL CHECK (git_commit ~ '^[0-9a-f]{40}$'),
    enabled         boolean     NOT NULL DEFAULT true,
    loaded_at       timestamptz NOT NULL DEFAULT now(),
    UNIQUE (rule_id, source_sha256)
);

CREATE INDEX rules_enabled_idx ON rules (rule_id) WHERE enabled;

CREATE TABLE playbooks (
    playbook_version_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    technique           text        NOT NULL CHECK (technique ~ '^T[0-9]{4}(\.[0-9]{3})?$'),
    title               text        NOT NULL,
    attack_version      text        NOT NULL,
    body                jsonb       NOT NULL,          -- the YAML file parsed to JSON
    source_sha256       text        NOT NULL CHECK (source_sha256 ~ '^[0-9a-f]{64}$'),
    git_commit          text        NOT NULL CHECK (git_commit ~ '^[0-9a-f]{40}$'),
    loaded_at           timestamptz NOT NULL DEFAULT now(),
    UNIQUE (technique, source_sha256)
);

-- One row per playbook step. Approvals reference a step, so a human can only approve an
-- action that a playbook step allows (design section 5).
CREATE TABLE playbook_steps (
    playbook_version_id bigint  NOT NULL REFERENCES playbooks ON DELETE RESTRICT,
    step_id             text    NOT NULL,              -- e.g. T1110.001-3
    position            integer NOT NULL,
    phase               text    NOT NULL,
    action              text    NOT NULL,
    destructive         boolean NOT NULL,
    requires_approval   boolean NOT NULL DEFAULT false,
    response_action     text
                        CHECK (response_action IN
                               ('block_ip', 'disable_account', 'isolate_host', 'kill_process')),
    PRIMARY KEY (playbook_version_id, step_id),
    -- A step that can trigger an automated action must be gated by a human.
    CHECK (response_action IS NULL OR requires_approval)
);

INSERT INTO schema_migrations (version) VALUES ('0001_reference');

COMMIT;
