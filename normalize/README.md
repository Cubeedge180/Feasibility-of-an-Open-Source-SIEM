# normalize/

Server-side parsers that turn the raw records Fluent Bit ships into events
(`normalize.Event`), keeping each log's own field names so Sigma rules match them as written
(decision D11, no ECS mapping).

| Tag | Module | Source | Sigma logsource |
|---|---|---|---|
| `windows` | `windows.py` | Security and Sysmon event XML | `windows` / `security` or `sysmon` (+ category from the Sysmon event ID) |
| `auditd` | `linux.py` | one auditd record line (enriched part after `0x1d` included) | `linux` / `auditd` |
| `auth` | `linux.py` | rsyslog line with RFC 3339 time | `linux` / `auth` (`program`, `pid`, `message`) |

A record that cannot be parsed raises `NormaliseError`; ingest keeps it in `ingest_rejects`.
Tests: `tests/test_normalize.py` with samples in `tests/samples/`.
