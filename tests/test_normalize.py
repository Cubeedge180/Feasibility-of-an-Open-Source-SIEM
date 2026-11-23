"""Normalisers: raw shipper records (Fluent Bit) to events with native Sigma field names."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from normalize import NormaliseError, normalise

SAMPLES = Path(__file__).parent / "samples"


def sample(name: str) -> str:
    return (SAMPLES / name).read_text(encoding="utf-8").strip()


def test_windows_security_log_cleared() -> None:
    xml = sample("win_security_1102.xml")
    # Fluent Bit's XML rendering key is not documented, so the normaliser finds the XML itself.
    event = normalise("windows", {"System": xml, "host": "ignored"})

    assert event.event_time == datetime(2026, 11, 23, 10, 15, 30, 123456, tzinfo=UTC)
    assert event.host == "WIN-LAB01"
    assert (event.product, event.service, event.category) == ("windows", "security", None)
    assert event.fields["EventID"] == 1102
    assert event.fields["Provider_Name"] == "Microsoft-Windows-Eventlog"
    assert event.fields["Channel"] == "Security"
    assert event.fields["SubjectUserName"] == "labadmin"  # from UserData, namespace stripped
    assert event.raw == xml


def test_sysmon_process_creation() -> None:
    event = normalise("windows", {"Event": sample("win_sysmon_1.xml")})

    assert (event.product, event.service, event.category) == (
        "windows",
        "sysmon",
        "process_creation",
    )
    assert event.fields["Image"] == r"C:\Windows\System32\wevtutil.exe"
    assert event.fields["CommandLine"] == "wevtutil cl Security"
    assert event.fields["Hashes"] == ""


def test_auditd_record() -> None:
    line = sample("auditd.log")
    event = normalise("auditd", {"log": line, "host": "kali"})

    assert event.event_time == datetime(2026, 11, 23, 10, 20, 0, 123000, tzinfo=UTC)
    assert event.host == "kali"
    assert (event.product, event.service) == ("linux", "auditd")
    assert event.fields["type"] == "SYSCALL"
    assert event.fields["serial"] == 456
    assert event.fields["exe"] == "/usr/bin/bash"
    assert event.fields["key"] == "susp_activity"
    assert event.fields["AUID"] == "lucian"  # enriched part after the 0x1d separator
    assert event.raw == line


def test_auth_log_line() -> None:
    event = normalise("auth", {"log": sample("auth.log"), "host": "kali"})

    assert event.event_time == datetime(2026, 11, 23, 10, 30, 1, 654321, tzinfo=UTC)
    assert event.host == "kali"
    assert (event.product, event.service) == ("linux", "auth")
    assert event.fields["program"] == "sshd"
    assert event.fields["pid"] == 2345
    assert event.fields["message"].startswith("Failed password for invalid user admin")


@pytest.mark.parametrize(
    ("tag", "record"),
    [
        ("windows", {"log": "not xml"}),
        ("windows", {"System": "<Event><System></System></Event>"}),  # no time or EventID
        ("auditd", {"log": "garbage", "host": "kali"}),
        ("auditd", {"log": sample("auditd.log")}),  # no host
        ("auth", {"log": "Nov 23 10:00:00 kali sshd[1]: no year", "host": "kali"}),
        ("unknown", {"log": "x"}),
    ],
)
def test_unparseable_records_raise(tag: str, record: dict) -> None:
    with pytest.raises(NormaliseError):
        normalise(tag, record)
