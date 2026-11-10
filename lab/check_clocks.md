# Clock checks

MTTD is a difference between timestamps from different machines (attack start
on an endpoint, alert time in the SIEM). All machines sync to one lab time
server, and the offsets are recorded at the start and end of every run.

## Time server

`lab/ntp/` runs chrony in Docker Desktop on the Mac. It serves the Docker
Desktop VM's clock, which is the clock the SIEM containers stamp events and
alerts with, so endpoint time and SIEM time come from the same source. It has
no upstream server, so it keeps working with the lab cut off from the internet.

```bash
NTP_BIND=<mac-lab-ip> docker compose -f lab/ntp/compose.yml up -d --build
```

Port 123 is privileged: once, enable Docker Desktop, Settings, Advanced,
"Allow privileged port forwarding to external machines", or the start fails
with "Cannot bind privileged port 123". Windows `w32tm` cannot use another port.

The Mac's lab address only exists while a UTM VM is running. `<mac-lab-ip>`
and the endpoint addresses are in the local VM record (`Licenta/lab-local/`),
never in git.

## Point the endpoints at it (once)

Windows (PowerShell as Administrator):

```powershell
Start-Service w32time   # stopped by default; /config fails with 0x80070426 otherwise
w32tm /config /manualpeerlist:"<mac-lab-ip>,0x8" /syncfromflags:manual /update
w32tm /resync
```

Kali:

```bash
sudo apt install -y chrony
sudo sed -i 's/^\(pool\|server\) /#&/' /etc/chrony/chrony.conf
echo "server <mac-lab-ip> iburst" | sudo tee -a /etc/chrony/chrony.conf
# Kali disables network services on install, so enable it explicitly
sudo systemctl enable --now chrony
chronyc sources
```

## Record offsets (start and end of every run)

Write the output to `eval/results/<run_id>/clocks.md` (replace addresses with
host names before committing; the pre-commit hook blocks private IPs).

| Where | Command | Value to record |
|---|---|---|
| Mac vs time server | `sntp <mac-lab-ip>` | offset (s) |
| Windows | `w32tm /stripchart /computer:<mac-lab-ip> /samples:5 /dataonly` | median offset (s) |
| Kali | `chronyc tracking` | "System time" offset (s) |
| SIEM container vs Mac | `date -u +%s.%N` in the ingest container and on the Mac, back to back | difference (s) |

Target: every offset under 1 s (lab-phase-plan W2). If one is larger, fix the
sync before the run, or record it and correct MTTD by the measured offset;
never correct silently.

Status: untested in this lab (written 2026-11-10).
