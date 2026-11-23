"""Windows event log records (Security, Sysmon) rendered as XML by Fluent Bit's winevtlog."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any

from normalize import Event, NormaliseError

NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"

SERVICES = {"Security": "security", "Microsoft-Windows-Sysmon/Operational": "sysmon"}

# Sysmon event ID to Sigma logsource category (Sigma's windows taxonomy).
# shortcut: 12-14 map to one category each, so rules with category registry_event do not
# match; add a category alias in detection when such a rule is added.
SYSMON_CATEGORIES = {
    1: "process_creation",
    2: "file_change",
    3: "network_connection",
    5: "process_termination",
    6: "driver_load",
    7: "image_load",
    8: "create_remote_thread",
    9: "raw_access_thread",
    10: "process_access",
    11: "file_event",
    12: "registry_add",
    13: "registry_set",
    14: "registry_rename",
    15: "create_stream_hash",
    17: "pipe_created",
    18: "pipe_created",
    19: "wmi_event",
    20: "wmi_event",
    21: "wmi_event",
    22: "dns_query",
    23: "file_delete",
    25: "process_tampering",
    26: "file_delete_detected",
}


def parse(record: dict[str, Any]) -> Event:
    # Fluent Bit does not document which key holds the XML, so take the value that is one.
    raw = next(
        (v for v in record.values() if isinstance(v, str) and v.lstrip().startswith("<Event")),
        None,
    )
    if raw is None:
        raise NormaliseError("no <Event> XML in record")
    try:
        # Stdlib ElementTree resolves no external entities; expat limits entity expansion.
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        raise NormaliseError(f"bad event XML: {e}") from e

    system = root.find(f"{NS}System")
    if system is None:
        raise NormaliseError("event XML has no System element")
    fields: dict[str, Any] = {}
    for child in system:
        name = _local(child.tag)
        if name == "Provider":
            fields["Provider_Name"] = child.get("Name")
        elif name == "TimeCreated":
            fields["TimeCreated"] = child.get("SystemTime")
        elif name == "Security":
            if child.get("UserID"):
                fields["UserID"] = child.get("UserID")
        elif name == "Execution":
            fields["ProcessID"], fields["ThreadID"] = child.get("ProcessID"), child.get("ThreadID")
        elif child.text is not None:
            fields[name] = child.text

    for data in root.iterfind(f"{NS}EventData/{NS}Data"):
        fields[data.get("Name") or "Data"] = data.text or ""
    for block in root.iterfind(f"{NS}UserData/*"):
        for child in block:
            fields[_local(child.tag)] = child.text or ""

    try:
        event_id = int(fields["EventID"])
        event_time = _parse_time(fields["TimeCreated"])
        host = fields["Computer"]
    except (KeyError, TypeError, ValueError) as e:
        raise NormaliseError(f"event XML lacks EventID, TimeCreated or Computer: {e}") from e
    fields["EventID"] = event_id

    service = SERVICES.get(fields.get("Channel", ""))
    category = SYSMON_CATEGORIES.get(event_id) if service == "sysmon" else None
    return Event(event_time, host, "windows", service, category, fields, raw)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_time(value: str) -> datetime:
    # Windows writes 7 fractional digits; datetime keeps 6.
    return datetime.fromisoformat(re.sub(r"(\.\d{6})\d+", r"\1", value))
