-- Smoke test for db/migrations on a fresh database. Run by CI (job `migrations`) with
--   psql -v ON_ERROR_STOP=1 -f db/tests/smoke.sql
-- Everything runs in one transaction that is rolled back, so the database stays empty.
-- Data here is synthetic (documentation IP range, made-up hashes).

\set ON_ERROR_STOP 1
BEGIN;

DO $$
BEGIN
    ASSERT (SELECT count(*) FROM schema_migrations) = 4, 'expected 4 applied migrations';
END;
$$;

SET LOCAL siem.actor = 'smoke-test';

INSERT INTO rules (rule_id, kind, title, level, technique_ids, source_path, source_text,
                   source_sha256, git_commit)
VALUES ('6f1c2d9e-8b4a-4f3e-9c71-2a5d0e8b7c41', 'sigma', 'Windows Security Event Log Cleared',
        'high', '{T1685.005}', 'rules/defense_impairment/win_security_log_cleared.yml',
        'title: ...', repeat('a', 64), repeat('1', 40));

INSERT INTO playbooks (technique, title, attack_version, body, source_sha256, git_commit)
VALUES ('T1110.001', 'Password guessing', '19.2', '{}', repeat('b', 64), repeat('1', 40));

INSERT INTO playbook_steps (playbook_version_id, step_id, position, phase, action, destructive,
                            requires_approval, response_action)
SELECT playbook_version_id, 'T1110.001-3', 3, 'contain', 'Block the source IP.', true, true,
       'block_ip'
FROM playbooks;

INSERT INTO events (event_time, host, product, service, fields, run_label)
VALUES (now(), 'lab-win-01', 'windows', 'security',
        '{"EventID": 1102, "Provider_Name": "Microsoft-Windows-Eventlog"}', 'smoke');

INSERT INTO alerts (rule_version_id, first_event_time, last_event_time, host, severity)
SELECT rule_version_id, now(), now(), 'lab-win-01', 'high' FROM rules;

INSERT INTO alert_events (alert_id, event_id)
SELECT alert_id, event_id FROM alerts, events;

INSERT INTO triage_outputs (alert_id, condition, model_tag, model_digest, ollama_version,
                            temperature, seed, prompt_path, prompt_sha256, input_format,
                            playbook_version_id, input_text, input_sha256, git_commit, output,
                            output_raw, schema_valid)
SELECT alert_id, 'C4', 'model:tag', repeat('c', 64), '0.0.0', 0, 42,
       'triage/prompts/x.txt', repeat('d', 64), 'normalised', playbook_version_id, 'input',
       repeat('e', 64), repeat('1', 40), '{"severity": "high"}', '{"severity": "high"}', true
FROM alerts, playbooks;

INSERT INTO approvals (triage_id, alert_id, playbook_version_id, step_id, response_action,
                       target, decision, decided_by)
SELECT triage_id, alert_id, playbook_version_id, 'T1110.001-3', 'block_ip', '192.0.2.10',
       'approved', 'analyst'
FROM triage_outputs;

UPDATE approvals SET executed_at = clock_timestamp(), execution_result = 'ok';

DO $$
BEGIN
    ASSERT (SELECT count(*) FROM audit_log WHERE actor = 'smoke-test') = 6,
        'expected 6 audited changes (rule, playbook, alert, triage, approval insert + update)';
END;
$$;

-- Each block must fail; the expected error is caught, anything else aborts the test.
CREATE FUNCTION pg_temp.expect_error(stmt text, label text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    BEGIN
        EXECUTE stmt;
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'ok, refused: %', label;
        RETURN;
    END;
    RAISE EXCEPTION 'not refused: %', label;
END;
$$;

SELECT pg_temp.expect_error(
    $q$UPDATE triage_outputs SET seed = 1$q$, 'triage output is append-only');
SELECT pg_temp.expect_error(
    $q$DELETE FROM audit_log$q$, 'audit log is append-only');
SELECT pg_temp.expect_error(
    $q$TRUNCATE audit_log$q$, 'audit log cannot be truncated');
SELECT pg_temp.expect_error(
    $q$UPDATE approvals SET decision = 'rejected'$q$, 'approval decision is final');
SELECT pg_temp.expect_error(
    $q$UPDATE approvals SET execution_result = 'again'$q$, 'approval executes once');
SELECT pg_temp.expect_error(
    $q$INSERT INTO approvals (triage_id, alert_id, playbook_version_id, step_id,
                              response_action, target, decision, decided_by)
       SELECT triage_id, alert_id, playbook_version_id, 'T1110.001-3', 'isolate_host',
              'lab-win-01', 'approved', 'analyst'
       FROM triage_outputs$q$,
    'action not allowed by the playbook step');
SELECT pg_temp.expect_error(
    $q$INSERT INTO playbook_steps (playbook_version_id, step_id, position, phase, action,
                                   destructive, requires_approval, response_action)
       SELECT playbook_version_id, 'T1110.001-9', 9, 'contain', 'x', true, false, 'block_ip'
       FROM playbooks$q$,
    'response action without approval gate');
SELECT pg_temp.expect_error(
    $q$INSERT INTO triage_outputs (alert_id, condition, model_tag, model_digest,
                                   ollama_version, temperature, seed, prompt_path,
                                   prompt_sha256, input_format, input_text, input_sha256,
                                   git_commit, output_raw, schema_valid)
       SELECT alert_id, 'C3', 'm', repeat('c', 64), '0', 0, 42, 'p', repeat('d', 64),
              'raw_json', 'i', repeat('e', 64), repeat('1', 40), '', false
       FROM alerts$q$,
    'C3 must use normalised input');
SELECT pg_temp.expect_error(
    $q$INSERT INTO triage_outputs (alert_id, condition, model_tag, model_digest,
                                   ollama_version, temperature, seed, prompt_path,
                                   prompt_sha256, input_format, input_text, input_sha256,
                                   git_commit, output_raw, schema_valid)
       SELECT alert_id, 'C4', 'm', repeat('c', 64), '0', 0, 42, 'p', repeat('d', 64),
              'normalised', 'i', repeat('e', 64), repeat('1', 40), '', false
       FROM alerts$q$,
    'C4 needs a playbook');

ROLLBACK;
\echo smoke test passed
