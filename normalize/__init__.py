"""Turn raw shipper records into events that keep the log's own (Sigma) field names.

Fluent Bit tags each record with its input: `windows` (Security and Sysmon, rendered as XML),
`auditd` (/var/log/audit/audit.log) and `auth` (/var/log/auth.log). See agent/README.md.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any


class NormaliseError(ValueError):
    """The record cannot be turned into an event; ingest stores it in ingest_rejects."""


@dataclass(frozen=True)
class Event:
    event_time: datetime
    host: str
    product: str  # Sigma logsource.product
    service: str | None  # Sigma logsource.service
    category: str | None  # Sigma logsource.category
    fields: dict[str, Any]
    raw: str


def normalise(tag: str, record: dict[str, Any]) -> Event:
    from normalize import linux, windows

    parsers: dict[str, Callable[[dict[str, Any]], Event]] = {
        "windows": windows.parse,
        "auditd": linux.parse_auditd,
        "auth": linux.parse_auth,
    }
    if tag not in parsers:
        raise NormaliseError(f"unknown source tag: {tag!r}")
    return parsers[tag](record)
