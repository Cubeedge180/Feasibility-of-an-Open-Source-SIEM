-- 0004: human approval of response actions, and the audit log.
--
-- Design section 5: the model can only propose; nothing runs until a person approves it, and
-- every decision is logged. The constraints below make the database refuse an approval that
-- is not tied to a playbook step allowing exactly that action.

BEGIN;

CREATE TABLE approvals (
    approval_id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    triage_id           bigint      NOT NULL UNIQUE REFERENCES triage_outputs ON DELETE RESTRICT,
    alert_id            bigint      NOT NULL REFERENCES alerts ON DELETE RESTRICT,
    playbook_version_id bigint      NOT NULL,
    step_id             text        NOT NULL,
    response_action     text        NOT NULL
                        CHECK (response_action IN
                               ('block_ip', 'disable_account', 'isolate_host', 'kill_process')),
    target              text        NOT NULL CHECK (target <> ''), -- IP, account, host, PID
    decision            text        NOT NULL CHECK (decision IN ('approved', 'rejected')),
    decided_by          text        NOT NULL CHECK (decided_by <> ''),
    decided_at          timestamptz NOT NULL DEFAULT clock_timestamp(),
    reason              text,
    executed_at         timestamptz,
    execution_result    text,
    FOREIGN KEY (playbook_version_id, step_id) REFERENCES playbook_steps ON DELETE RESTRICT,
    CHECK (executed_at IS NULL OR decision = 'approved'),
    CHECK (executed_at IS NULL OR executed_at >= decided_at)
);

CREATE FUNCTION approvals_check() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    step_action text;
    triage_alert bigint;
BEGIN
    IF TG_OP = 'UPDATE' THEN
        -- A decision is final; only the execution result may be filled in, once.
        IF (NEW.triage_id, NEW.alert_id, NEW.playbook_version_id, NEW.step_id,
            NEW.response_action, NEW.target, NEW.decision, NEW.decided_by, NEW.decided_at,
            NEW.reason)
           IS DISTINCT FROM
           (OLD.triage_id, OLD.alert_id, OLD.playbook_version_id, OLD.step_id,
            OLD.response_action, OLD.target, OLD.decision, OLD.decided_by, OLD.decided_at,
            OLD.reason) THEN
            RAISE EXCEPTION 'approval % is final; only execution fields can change',
                OLD.approval_id;
        END IF;
        IF OLD.executed_at IS NOT NULL THEN
            RAISE EXCEPTION 'approval % was already executed', OLD.approval_id;
        END IF;
        RETURN NEW;
    END IF;

    SELECT response_action INTO step_action
    FROM playbook_steps
    WHERE playbook_version_id = NEW.playbook_version_id AND step_id = NEW.step_id;
    IF step_action IS DISTINCT FROM NEW.response_action THEN
        RAISE EXCEPTION 'playbook step % does not allow action %', NEW.step_id,
            NEW.response_action;
    END IF;

    SELECT alert_id INTO triage_alert FROM triage_outputs WHERE triage_id = NEW.triage_id;
    IF triage_alert IS DISTINCT FROM NEW.alert_id THEN
        RAISE EXCEPTION 'triage output % belongs to alert %, not %', NEW.triage_id,
            triage_alert, NEW.alert_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER approvals_check
    BEFORE INSERT OR UPDATE ON approvals
    FOR EACH ROW EXECUTE FUNCTION approvals_check();

CREATE TABLE audit_log (
    audit_id   bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    at         timestamptz NOT NULL DEFAULT clock_timestamp(),
    -- Who acted: the application sets it per transaction with
    --   SET LOCAL siem.actor = '<user>';
    -- otherwise the database user is recorded.
    actor      text        NOT NULL,
    db_user    text        NOT NULL DEFAULT session_user,
    operation  text        NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
    table_name text        NOT NULL,
    row_id     text,
    old_row    jsonb,
    new_row    jsonb
);

CREATE INDEX audit_log_table_row_idx ON audit_log (table_name, row_id);

CREATE FUNCTION audit_record() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    pk_column text := TG_ARGV[0];
    old_json  jsonb := CASE WHEN TG_OP <> 'INSERT' THEN to_jsonb(OLD) END;
    new_json  jsonb := CASE WHEN TG_OP <> 'DELETE' THEN to_jsonb(NEW) END;
BEGIN
    INSERT INTO audit_log (actor, operation, table_name, row_id, old_row, new_row)
    VALUES (
        COALESCE(NULLIF(current_setting('siem.actor', true), ''), session_user),
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(new_json, old_json) ->> pk_column,
        old_json,
        new_json
    );
    RETURN NULL;
END;
$$;

-- Events are not audited row by row: they are append-only input at high volume.
CREATE TRIGGER audit AFTER INSERT OR UPDATE OR DELETE ON rules
    FOR EACH ROW EXECUTE FUNCTION audit_record('rule_version_id');
CREATE TRIGGER audit AFTER INSERT OR UPDATE OR DELETE ON playbooks
    FOR EACH ROW EXECUTE FUNCTION audit_record('playbook_version_id');
CREATE TRIGGER audit AFTER INSERT OR UPDATE OR DELETE ON alerts
    FOR EACH ROW EXECUTE FUNCTION audit_record('alert_id');
CREATE TRIGGER audit AFTER INSERT OR UPDATE OR DELETE ON triage_outputs
    FOR EACH ROW EXECUTE FUNCTION audit_record('triage_id');
CREATE TRIGGER audit AFTER INSERT OR UPDATE OR DELETE ON approvals
    FOR EACH ROW EXECUTE FUNCTION audit_record('approval_id');

-- Append-only tables. A database superuser can still disable triggers; the design note
-- lists this limitation.
CREATE FUNCTION forbid_change() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '% is append-only (% refused)', TG_TABLE_NAME, TG_OP;
END;
$$;

CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON audit_log
    FOR EACH ROW EXECUTE FUNCTION forbid_change();
CREATE TRIGGER append_only_truncate BEFORE TRUNCATE ON audit_log
    FOR EACH STATEMENT EXECUTE FUNCTION forbid_change();
CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON triage_outputs
    FOR EACH ROW EXECUTE FUNCTION forbid_change();
CREATE TRIGGER append_only_truncate BEFORE TRUNCATE ON triage_outputs
    FOR EACH STATEMENT EXECUTE FUNCTION forbid_change();

INSERT INTO schema_migrations (version) VALUES ('0004_approvals_audit');

COMMIT;
