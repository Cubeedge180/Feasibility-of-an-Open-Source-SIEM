"""Linux records from Fluent Bit tail inputs: auditd log lines and rsyslog auth.log lines."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from normalize import Event, NormaliseError

AUDIT_HEADER = re.compile(
    r"^(?:node=(?P<node>\S+) )?type=(?P<type>\S+) msg=audit\((?P<ts>\d+\.\d+):(?P<serial>\d+)\):\s*"
)
AUDIT_PAIR = re.compile(r'(\w+)=("[^"]*"|\S+)')
# rsyslog's default file format on Debian 12+ (RFC 3339 time). The old "Nov 23 10:00:00" form
# has no year or zone, so it is rejected rather than guessed.
AUTH_LINE = re.compile(
    r"^(?P<ts>\d{4}-\d\d-\d\dT\S+) (?P<host>\S+) (?P<program>[^\s\[:]+)(?:\[(?P<pid>\d+)\])?: "
    r"(?P<message>.*)$"
)


def parse_auditd(record: dict[str, Any]) -> Event:
    line = _line(record)
    m = AUDIT_HEADER.match(line)
    if m is None:
        raise NormaliseError("not an auditd record")
    host = m["node"] or record.get("host")
    if not host:
        raise NormaliseError("auditd record has no host (set it in the shipper config)")
    # shortcut: one event per record line; records of one syscall share `serial` but are not
    # merged. Merge in normalize if a rule ever needs fields from two record types.
    fields: dict[str, Any] = {"type": m["type"], "serial": int(m["serial"])}
    fields.update((k, v.strip('"')) for k, v in AUDIT_PAIR.findall(line[m.end() :]))
    event_time = datetime.fromtimestamp(float(m["ts"]), UTC)
    return Event(event_time, host, "linux", "auditd", None, fields, line)


def parse_auth(record: dict[str, Any]) -> Event:
    line = _line(record)
    m = AUTH_LINE.match(line)
    if m is None:
        raise NormaliseError("auth.log line not in RFC 3339 rsyslog format")
    try:
        event_time = datetime.fromisoformat(m["ts"])
    except ValueError as e:
        raise NormaliseError(f"bad auth.log time: {e}") from e
    if event_time.tzinfo is None:
        raise NormaliseError("auth.log time has no zone")
    fields: dict[str, Any] = {"program": m["program"], "message": m["message"]}
    if m["pid"]:
        fields["pid"] = int(m["pid"])
    return Event(event_time.astimezone(UTC), m["host"], "linux", "auth", None, fields, line)


def _line(record: dict[str, Any]) -> str:
    line = record.get("log")
    if not isinstance(line, str):
        raise NormaliseError("record has no `log` line")
    return line.rstrip("\n")
