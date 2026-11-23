"""Ingestion API. Fluent Bit agents POST batches of raw records; each record is normalised,
stored and checked against the Sigma rules in the same transaction (decision D11)."""

from __future__ import annotations

import hmac
import os
import threading
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

import psycopg
from fastapi import Body, FastAPI, Header, HTTPException

from detect.lint import rule_files
from ingest.store import DeployedRule, register_rules, store_batch

REPO = Path(__file__).resolve().parent.parent


def git_commit(repo: Path) -> str:
    """Commit of the checkout the rules are read from (no git binary needed in the image)."""
    git = repo / ".git"
    head = (git / "HEAD").read_text().strip()
    if not head.startswith("ref: "):
        return head  # detached HEAD
    ref = head[5:]
    if (git / ref).is_file():
        return (git / ref).read_text().strip()
    for line in (git / "packed-refs").read_text().splitlines():
        if line.endswith(" " + ref):
            return line.split()[0]
    raise RuntimeError(f"cannot resolve {ref} in {git}")


class State:
    token: str
    database_url: str
    rules: list[DeployedRule]
    conn: psycopg.Connection | None = None
    # shortcut: one connection, one writer at a time; enough at lab rates, revisit after F2.
    lock = threading.Lock()

    def connection(self) -> psycopg.Connection:
        if self.conn is None or self.conn.closed or self.conn.broken:
            self.conn = psycopg.connect(self.database_url)
        return self.conn


state = State()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    state.token = os.environ.get("INGEST_TOKEN", "")
    if len(state.token) < 16:
        raise RuntimeError("INGEST_TOKEN must be set to a random value of 16+ characters")
    state.database_url = os.environ["DATABASE_URL"]
    with state.lock:
        state.rules = register_rules(state.connection(), rule_files(), REPO, git_commit(REPO))
    yield
    if state.conn is not None:
        state.conn.close()


app = FastAPI(title="SIEM ingest", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/events", status_code=201)
def ingest_events(
    records: Annotated[list[dict[str, Any]], Body()],
    x_fluent_tag: Annotated[str, Header()],
    authorization: Annotated[str, Header()] = "",
) -> dict[str, int]:
    if not hmac.compare_digest(authorization.encode(), f"Bearer {state.token}".encode()):
        raise HTTPException(status_code=401, detail="bad or missing token")
    with state.lock:
        return store_batch(state.connection(), x_fluent_tag, records, state.rules)
