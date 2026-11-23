"""Call a local Ollama model for one triage output, reproducibly.

Every call uses temperature 0, a fixed seed and structured output against
output_schema.json (docs/thesis/research-design.md, section 4.1). Every result
record carries what is needed to reproduce or audit it: model tag and digest,
Ollama version, prompt file hash, seed, condition, run and git commit.

The model only proposes. Nothing here runs a response action.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from triage.validate_output import SCHEMA

DEFAULT_SEED = 20261014
CONDITIONS = {"C1", "C2", "C3", "C4"}


@dataclass(frozen=True)
class RunInfo:
    """Facts about the setup, collected once per batch of triage calls."""

    model: str
    model_digest: str
    ollama_version: str
    git_commit: str
    seed: int


def git_commit(repo: Path | None = None) -> str:
    """Current commit, with "-dirty" appended if tracked files have changes."""
    cwd = repo or Path(__file__).resolve().parent.parent
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return f"{commit}-dirty" if status else commit


def model_digest(client: httpx.Client, model: str) -> str:
    """Digest of an exact model tag as the Ollama server reports it (/api/tags)."""
    response = client.get("/api/tags")
    response.raise_for_status()
    for entry in response.json().get("models", []):
        if entry.get("name") == model or entry.get("model") == model:
            return str(entry["digest"])
    raise LookupError(f"model {model!r} is not pulled on this Ollama server")


def ollama_version(client: httpx.Client) -> str:
    response = client.get("/api/version")
    response.raise_for_status()
    return str(response.json()["version"])


def run_info(
    client: httpx.Client, model: str, seed: int = DEFAULT_SEED, allow_dirty: bool = False
) -> RunInfo:
    """Setup facts for a batch. Refuses uncommitted code unless allow_dirty (pilot only):

    results must name the exact commit, and triage_outputs.git_commit accepts only a
    clean 40-hex commit, so a dirty run would fail later, after the model time is spent.
    """
    commit = git_commit()
    if commit.endswith("-dirty") and not allow_dirty:
        raise RuntimeError(f"tracked files have uncommitted changes ({commit}); commit first")
    return RunInfo(
        model=model,
        model_digest=model_digest(client, model),
        ollama_version=ollama_version(client),
        git_commit=commit,
        seed=seed,
    )


def chat_request(model: str, system_prompt: str, user_content: str, seed: int) -> dict[str, Any]:
    """The /api/chat body. Temperature and seed are fixed here, not by the caller."""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "format": SCHEMA,
        "stream": False,
        "options": {"temperature": 0, "seed": seed},
    }


def triage(
    client: httpx.Client,
    info: RunInfo,
    prompt_file: Path,
    user_content: str,
    alert_id: str,
    condition: str,
    run: int,
) -> dict[str, Any]:
    """One triage output plus its reproducibility metadata, as one results record.

    The record keeps the fields eval/blind.py reads (alert_id, condition, run,
    output), plus the exact input text sent and its SHA-256 (triage_outputs needs
    both). If the model returns text that is not JSON, output is None and the raw
    text is kept, so the failure is counted, not dropped.
    """
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition {condition!r}")
    prompt = prompt_file.read_bytes()
    body = chat_request(info.model, prompt.decode("utf-8"), user_content, info.seed)
    started = time.monotonic()
    response = client.post("/api/chat", json=body)
    latency_ms = round((time.monotonic() - started) * 1000)
    response.raise_for_status()
    raw = response.json()["message"]["content"]
    try:
        output = json.loads(raw)
    except json.JSONDecodeError:
        output = None
    return {
        "alert_id": alert_id,
        "condition": condition,
        "run": run,
        "output": output,
        "raw_output": raw,
        "model": info.model,
        "model_digest": info.model_digest,
        "ollama_version": info.ollama_version,
        "prompt_file": prompt_file.name,
        "prompt_sha256": hashlib.sha256(prompt).hexdigest(),
        "input_text": user_content,
        "input_sha256": hashlib.sha256(user_content.encode("utf-8")).hexdigest(),
        "latency_ms": latency_ms,
        "seed": info.seed,
        "temperature": 0,
        "git_commit": info.git_commit,
        "created_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
