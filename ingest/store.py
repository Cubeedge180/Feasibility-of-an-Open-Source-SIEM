"""Database writes for ingest: rule versions, events, alerts and rejects (db/migrations)."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg
from psycopg.types.json import Jsonb
from sigma.rule import SigmaRule

from detect.evaluator import applies, condition_fields, matches
from normalize import Event, NormaliseError, normalise

TECHNIQUE = re.compile(r"^t\d{4}(\.\d{3})?$")


@dataclass(frozen=True)
class DeployedRule:
    rule_version_id: int
    rule: SigmaRule
    fields: frozenset[str]  # copied into the alert summary


def register_rules(
    conn: psycopg.Connection, paths: list[Path], repo: Path, commit: str
) -> list[DeployedRule]:
    """Record each rule file's exact text in `rules` (once per content hash) and return them."""
    deployed = []
    with conn.transaction():
        for path in paths:
            text = path.read_text(encoding="utf-8")
            rule = SigmaRule.from_yaml(text)
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            row = (
                conn.execute(
                    "INSERT INTO rules (rule_id, kind, title, level, technique_ids, logsource,"
                    " source_path, source_text, source_sha256, compiler, git_commit)"
                    " VALUES (%s, 'sigma', %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    " ON CONFLICT (rule_id, source_sha256) DO NOTHING RETURNING rule_version_id",
                    (
                        rule.id,
                        rule.title,
                        rule.level.name.lower(),
                        [
                            t.name.upper()
                            for t in rule.tags
                            if t.namespace == "attack" and TECHNIQUE.match(t.name)
                        ],
                        Jsonb({k: v for k, v in rule.logsource.to_dict().items() if v}),
                        str(path.relative_to(repo)),
                        text,
                        sha,
                        "detect.evaluator (Python, inline at ingest)",
                        commit,
                    ),
                ).fetchone()
                or conn.execute(
                    "SELECT rule_version_id FROM rules WHERE rule_id = %s AND source_sha256 = %s",
                    (rule.id, sha),
                ).fetchone()
            )
            deployed.append(DeployedRule(row[0], rule, frozenset(condition_fields(rule))))
    return deployed


def store_batch(
    conn: psycopg.Connection, tag: str, records: list[dict[str, Any]], rules: list[DeployedRule]
) -> dict[str, int]:
    """Normalise, store and evaluate one shipper batch in one transaction."""
    counts = {"stored": 0, "rejected": 0, "alerts": 0}
    with conn.transaction():
        for record in records:
            try:
                event = normalise(tag, record)
                with conn.transaction():  # savepoint: a refused record must not block the batch
                    counts["alerts"] += _store_event(conn, event, record, rules)
                counts["stored"] += 1
            except NormaliseError as e:
                _reject(conn, tag, str(e), record)
                counts["rejected"] += 1
            except psycopg.DataError as e:
                _reject(conn, tag, f"database refused the event: {e}", record)
                counts["rejected"] += 1
    return counts


def _store_event(
    conn: psycopg.Connection, event: Event, record: dict[str, Any], rules: list[DeployedRule]
) -> int:
    """Insert the event and an alert per matching rule; return the number of alerts."""
    (event_id,) = conn.execute(
        "INSERT INTO events (event_time, host, agent_id, product, service, category, fields, raw)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING event_id",
        (
            event.event_time,
            event.host,
            record.get("host"),
            event.product,
            event.service,
            event.category,
            Jsonb(event.fields),
            event.raw,
        ),
    ).fetchone()
    alerts = 0
    for d in rules:
        if applies(d.rule, event.product, event.service, event.category) and matches(
            d.rule, event.fields
        ):
            _raise_alert(conn, d, event, event_id)
            alerts += 1
    return alerts


def _reject(conn: psycopg.Connection, tag: str, error: str, record: dict[str, Any]) -> None:
    # NUL is the one character jsonb refuses; drop it so the reject itself can be stored.
    clean = json.loads(json.dumps(record).replace("\\u0000", ""))
    conn.execute(
        "INSERT INTO ingest_rejects (tag, error, record) VALUES (%s, %s, %s)",
        (tag, error, Jsonb(clean)),
    )


def _raise_alert(conn: psycopg.Connection, d: DeployedRule, event: Event, event_id: int) -> None:
    summary = {
        "title": d.rule.title,
        "fields": {k: event.fields[k] for k in sorted(d.fields) if k in event.fields},
    }
    (alert_id,) = conn.execute(
        "INSERT INTO alerts (rule_version_id, first_event_time, last_event_time, host, severity,"
        " technique_ids, summary)"
        " SELECT %s, %s, %s, %s, level, technique_ids, %s FROM rules WHERE rule_version_id = %s"
        " RETURNING alert_id",
        (
            d.rule_version_id,
            event.event_time,
            event.event_time,
            event.host,
            Jsonb(summary),
            d.rule_version_id,
        ),
    ).fetchone()
    conn.execute(
        "INSERT INTO alert_events (alert_id, event_id) VALUES (%s, %s)", (alert_id, event_id)
    )
