"""Triage client: fixed temperature/seed and full metadata. Ollama is stubbed."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from triage import ollama_client
from triage.ollama_client import RunInfo, chat_request, model_digest, run_info, triage

MODEL = "example-model:7b"
DIGEST = "abc123"


def _client(sent: list[dict[str, Any]], content: str = '{"alert_id": "A1"}') -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": MODEL, "digest": DIGEST}]})
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.40.14"})
        if request.url.path == "/api/chat":
            sent.append(json.loads(request.content))
            return httpx.Response(200, json={"message": {"role": "assistant", "content": content}})
        return httpx.Response(404)

    return httpx.Client(base_url="http://ollama.test", transport=httpx.MockTransport(handler))


@pytest.fixture
def info() -> RunInfo:
    return RunInfo(MODEL, DIGEST, "0.40.14", "deadbeef", 7)


@pytest.fixture
def prompt(tmp_path: Path) -> Path:
    path = tmp_path / "triage_v1.txt"
    path.write_text("You triage alerts.", encoding="utf-8")
    return path


def test_request_fixes_temperature_seed_and_schema() -> None:
    body = chat_request(MODEL, "sys", "alert", seed=7)
    assert body["options"] == {"temperature": 0, "seed": 7}
    assert body["format"] == ollama_client.SCHEMA
    assert body["stream"] is False


def test_triage_record_has_reproducibility_metadata(info: RunInfo, prompt: Path) -> None:
    sent: list[dict[str, Any]] = []
    record = triage(_client(sent), info, prompt, "alert text", "A1", "C3", run=1)
    assert sent[0]["options"] == {"temperature": 0, "seed": 7}
    assert record["output"] == {"alert_id": "A1"}
    assert record["model_digest"] == DIGEST
    assert record["ollama_version"] == "0.40.14"
    assert record["prompt_sha256"] == hashlib.sha256(b"You triage alerts.").hexdigest()
    assert record["git_commit"] == "deadbeef"
    assert (record["condition"], record["run"], record["seed"]) == ("C3", 1, 7)


def test_non_json_output_is_kept_not_dropped(info: RunInfo, prompt: Path) -> None:
    record = triage(_client([], content="not json"), info, prompt, "x", "A1", "C1", run=1)
    assert record["output"] is None
    assert record["raw_output"] == "not json"


def test_unknown_condition_rejected(info: RunInfo, prompt: Path) -> None:
    with pytest.raises(ValueError):
        triage(_client([]), info, prompt, "x", "A1", "C5", run=1)


def test_missing_model_raises() -> None:
    with pytest.raises(LookupError):
        model_digest(_client([]), "other:8b")


def test_run_info_collects_digest_and_version(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ollama_client, "git_commit", lambda: "deadbeef")
    got = run_info(_client([]), MODEL, seed=7)
    assert got == RunInfo(MODEL, DIGEST, "0.40.14", "deadbeef", 7)
