# agent/

The endpoint agent: [Fluent Bit](https://fluentbit.io) 5.1.3 with a pinned config, plus a
one-command installer per OS. Fluent Bit only collects and ships; parsing happens on the
server in `normalize/` (decision D11).

| OS | Installer | Ships | Tag |
|---|---|---|---|
| Windows (Arm64 or x64) | `windows/install.ps1` | Security and `Microsoft-Windows-Sysmon/Operational`, as event XML | `windows` |
| Debian / Kali | `linux/install.sh` | `/var/log/audit/audit.log` and `/var/log/auth.log` (installs rsyslog) | `auditd`, `auth` |

Each batch goes to `POST http://<ingest>:8000/v1/events` with `Authorization: Bearer <token>`
and the source tag in `X-Fluent-Tag`. Unsent batches wait in an on-disk buffer (500 MB cap,
oldest dropped first) and are retried without limit, so a sleeping Mac loses no events.

Run (elevated / as root, internet needed):

    # Windows, elevated PowerShell, from a copy of agent\windows
    powershell -ExecutionPolicy Bypass -File .\install.ps1 -IngestHost <mac-ip> -Token <token>

    # Kali, from a copy of agent/linux
    sudo ./install.sh --ingest-host <mac-ip> --token <token>

`<token>` is `INGEST_TOKEN` from the Mac's `.env`. Neither it nor the Mac's address goes in
git. The installer checks the ingest health endpoint first, verifies the download (SHA-256 on
Windows, apt signature on Linux), validates the config with `--dry-run`, then starts the
service.

Known limits: plain HTTP on the isolated lab network (the token is visible to anyone who can
sniff that network; TLS is out of scope, D4); the Linux repo codename is fixed to `bookworm`
because Kali has none of its own (override with `FLUENT_BIT_CODENAME`).
