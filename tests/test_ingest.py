"""Ingest API: token check, normalise, store, detect inline, keep rejects."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ingest.app import app, git_commit

SAMPLES = Path(__file__).parent / "samples"
TOKEN = "test-token-not-secret"
AUTH = {"Authorization": f"Bearer {TOKEN}"}


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_git_commit_reads_this_checkout():
    assert len(git_commit(Path(__file__).resolve().parent.parent)) == 40


@pytest.fixture
def client(database_url: str, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("INGEST_TOKEN", TOKEN)
    with TestClient(app) as c:
        yield c


def _query(database_url: str, sql: str) -> list[tuple]:
    import psycopg

    with psycopg.connect(database_url) as conn:
        return conn.execute(sql).fetchall()


def _windows(name: str) -> dict:
    return {"System": (SAMPLES / name).read_text(encoding="utf-8").strip(), "host": "win"}


def test_security_log_cleared_raises_alert(client: TestClient, database_url: str):
    response = client.post(
        "/v1/events",
        json=[_windows("win_security_1102.xml"), _windows("win_sysmon_1.xml")],
        headers={**AUTH, "X-Fluent-Tag": "windows"},
    )

    assert response.status_code == 201
    assert response.json() == {"stored": 2, "rejected": 0, "alerts": 1}
    [(title, severity, techniques, host, summary)] = _query(
        database_url,
        "SELECT r.title, a.severity, a.technique_ids, a.host, a.summary"
        " FROM alerts a JOIN rules r USING (rule_version_id)",
    )
    assert (title, severity, techniques, host) == (
        "Windows Security Event Log Cleared",
        "high",
        ["T1685.005"],
        "WIN-LAB01",
    )
    assert summary["fields"] == {"EventID": 1102, "Provider_Name": "Microsoft-Windows-Eventlog"}
    [(event_id, raw)] = _query(
        database_url,
        "SELECT e.fields->>'EventID', e.raw FROM alert_events JOIN events e USING (event_id)",
    )
    assert event_id == "1102" and raw.startswith("<Event")


def test_unparseable_record_goes_to_rejects(client: TestClient, database_url: str):
    response = client.post(
        "/v1/events",
        json=[
            {"log": "garbage", "host": "kali"},
            {"log": (SAMPLES / "auditd.log").read_text(), "host": "kali"},
        ],
        headers={**AUTH, "X-Fluent-Tag": "auditd"},
    )

    assert response.json() == {"stored": 1, "rejected": 1, "alerts": 0}
    assert _query(database_url, "SELECT tag, record->>'log' FROM ingest_rejects") == [
        ("auditd", "garbage")
    ]


@pytest.mark.parametrize(
    "headers", [{}, {"Authorization": "Bearer wrong"}, {"Authorization": TOKEN}]
)
def test_bad_token_is_refused(client: TestClient, database_url: str, headers: dict):
    response = client.post(
        "/v1/events",
        json=[_windows("win_security_1102.xml")],
        headers={**headers, "X-Fluent-Tag": "windows"},
    )

    assert response.status_code == 401
    assert _query(database_url, "SELECT count(*) FROM events") == [(0,)]


def test_rules_are_registered_once_across_restarts(database_url: str, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("INGEST_TOKEN", TOKEN)
    for _ in range(2):
        with TestClient(app):
            pass
    assert _query(database_url, "SELECT count(*) FROM rules") == [(1,)]


def test_startup_refuses_without_token(database_url: str, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.delenv("INGEST_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="INGEST_TOKEN"):
        with TestClient(app):
            pass


def test_record_the_database_refuses_does_not_block_the_batch(
    client: TestClient, database_url: str
):
    # PostgreSQL jsonb and text refuse NUL; without isolation the shipper would retry forever.
    good = (SAMPLES / "auth.log").read_text().strip()
    response = client.post(
        "/v1/events",
        json=[
            {"log": good.replace("ssh2", "ssh2\u0000"), "host": "kali"},
            {"log": good, "host": "kali"},
        ],
        headers={**AUTH, "X-Fluent-Tag": "auth"},
    )

    assert response.json() == {"stored": 1, "rejected": 1, "alerts": 0}
    [(error,)] = _query(database_url, "SELECT error FROM ingest_rejects")
    assert "database refused" in error
