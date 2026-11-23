"""Agent templates: every placeholder is filled by its installer, and the W3 decisions hold."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parent.parent / "agent"
CASES = [("windows", "install.ps1"), ("linux", "install.sh")]


@pytest.mark.parametrize(("os_dir", "installer"), CASES)
def test_installer_fills_every_placeholder(os_dir: str, installer: str) -> None:
    template = (AGENT / os_dir / "fluent-bit.conf").read_text(encoding="utf-8")
    script = (AGENT / os_dir / installer).read_text(encoding="utf-8")
    placeholders = set(re.findall(r"@[A-Z_]+@", template))
    assert placeholders == {"@INGEST_HOST@", "@INGEST_PORT@", "@INGEST_TOKEN@", "@AGENT_HOST@"}
    assert all(p in script for p in placeholders)


@pytest.mark.parametrize(("os_dir", "installer"), CASES)
def test_buffering_survives_outages(os_dir: str, installer: str) -> None:
    template = (AGENT / os_dir / "fluent-bit.conf").read_text(encoding="utf-8")
    assert re.search(r"Retry_Limit\s+no_limits", template)
    assert re.search(r"storage\.total_limit_size\s+500M", template)
    assert len(re.findall(r"storage\.type\s+filesystem", template)) == template.count("[INPUT]")


def test_windows_channels_are_separate_inputs_and_restart_on_clear() -> None:
    template = (AGENT / "windows" / "fluent-bit.conf").read_text(encoding="utf-8")
    channels = re.findall(r"^\s*Channels\s+(\S+)$", template, re.MULTILINE)
    assert channels == ["Security", "Microsoft-Windows-Sysmon/Operational"]
    assert len(set(re.findall(r"^\s*DB\s+(\S+)$", template, re.MULTILINE))) == 2
    script = (AGENT / "windows" / "install.ps1").read_text(encoding="utf-8")
    assert "EventID=1102" in script and "Restart-Service fluent-bit" in script
