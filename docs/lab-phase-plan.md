# Lab phase plan (Nov 2026 - Apr 2027)

Ordered, week-by-week plan from "lab is set up" to the `prereg-v1` freeze and
the final runs. It applies [lab-build-guide.md](lab-build-guide.md) and
[research-design.md](thesis/research-design.md) to the lab as it exists on
2026-11-04. The research design wins wherever this file disagrees with it.

Status: plan, written 2026-11-04. Nothing in it is measured. Each week has a
checkpoint; do not start the next block until it passes, or write down why.

**Who does what.** *Lucian* = by hand (anything inside a VM GUI, Docker
Desktop settings, UTM, installs that need internet, running attacks).
*Claude* = code, configs, scripts, docs and checks in this repo. Claude does
not run attacks or change VMs unless Lucian asks for that step.

## 0. Lab as of 2026-11-04 and how this plan differs from the guide

| Part | State | Note |
|---|---|---|
| Mac | MacBook Pro M4 Pro, 24 GB RAM, 12 CPU; APFS about 32 GB unallocated, System Settings 406.69 GB available (rest is purgeable) | RAM is the main constraint; disk relies on macOS releasing purgeable space |
| `win` | Windows 11 on Arm VM in UTM, 4 GB RAM, installed | Sysmon and agents not yet installed |
| `lin` | Existing Kali VM (reused as Linux endpoint, per guide section 2) | auditd, pwsh, agents not yet installed |
| Server | Docker Desktop 4.98.0 on the Mac (engine 29.9.2, compose v5.6.1); VM at 12 CPU / ~7.7 GiB | Cap to 4 CPU / 8 GB in W1 |
| Prototype | Repo `main` at 08bdd7d: ingest, PostgreSQL schema, 1 rule (`win_security_log_cleared`), 2 playbooks | No agent, no ground-truth wrapper yet |
| Wazuh | Not deployed | |
| Ollama | Native install planned on the Mac; no 7-8B model chosen | |

Changes to the guide, logged in `decision-log.md` as D8 (P1), D9 (P2) and
D10 (P3), approved by Lucian, supervisor pending:

- **P1. Server = Docker Desktop on the Mac, both SIEM stacks, one at a time**
  (Lucian, 2026-11-04: speed variation is not that important). A dedicated
  Linux server VM was considered and not chosen. Consequences, stated as
  limitations and handled in the runs:
  - F2: the Docker Desktop VM is capped at **4 CPU / 8 GB** and F2 is measured
    on that VM; it shares the Mac with the endpoint VMs and Ollama, so report
    the Mac model and memory pressure per run.
  - F6: Docker Desktop itself may connect out (update checks, sign-in,
    usage statistics; unverified). Turn off usage statistics and automatic
    updates, stay signed out, and capture traffic of the SIEM containers'
    own network, so Docker Desktop's traffic is not counted as SIEM traffic.
  - F7: Docker Desktop licence terms for organisations are unverified; the
    thesis states that the stack also runs on Docker Engine on Linux (€0)
    and that this deployment was not measured.
- **P2. One SIEM per pass** (already in guide section 2): same Atomic procedure
  from the same endpoint snapshot, prototype pass then Wazuh pass. "Same
  attack runs" becomes "same attack procedure from the same snapshot".
- **P3. Ollama native on the Mac, triage as replay if RAM is short.** Budget:
  Docker 8 + win 4 + lin 2 + Ollama ~6 + macOS ~4 ≈ 24 GB, i.e. all of it. If
  memory pressure turns yellow during an attack run, stop Ollama and run
  triage afterwards; MTTA is then measured on replay, and that is recorded.

## 1. Disk budget (check every week)

| Item | Estimate (unverified, measure it) |
|---|---|
| Wazuh single-node images + indexer data for the runs | 5-10 GB |
| Prototype images + PostgreSQL data | 1-3 GB |
| One 7-8B model, 4-bit | about 5 GB |
| VM snapshots (`clean-os`, `ready` on win and lin) | 5-15 GB |

About 32 GB is unallocated; the rest relies on macOS releasing purgeable space. Rules:

- Run `df -h /System/Volumes/Data` at the start of each week; if under 15 GB
  free, stop and free space before continuing (`docker system df`, old
  images, Downloads). Snapshots are kept, clones are not (a full clone of the
  Windows VM costs tens of GB).
- Only one SIEM's data volume on disk during a pass when space is short; export
  results to `eval/results/<run_id>/` first, then `docker compose down -v`.

## 2. Plan by week

Weeks start on Monday. W1 is the rest of this week.

### November: verify and wire the lab

**W1 (Nov 4-8): verify what exists, make the server side reachable**

| Who | Step |
|---|---|
| Lucian | Docker Desktop, Settings: Resources 4 CPU / 8 GB memory; General: usage statistics off, automatic updates off. Apply and restart. |
| Lucian | Note in a reply: UTM version, Windows build (`winver`), Kali version, each VM's network mode and IP, free disk. |
| Lucian | From win and lin, `ping <mac-ip-on-UTM-network>` (on UTM Shared Network usually the `.1` address of the VM's subnet, unverified). |
| Lucian | Take a UTM snapshot `clean-os` of win and lin (shut down first). If snapshots are not offered for the QEMU backend, tell Claude before cloning (disk). |
| Claude | Write the VM record (sizes, IPs, network mode, versions) to `../lab-local/vms.md` in the Licenta folder, outside the repo: real IPs never go into git. |
| Claude | Compose: bind ingest to the Mac's UTM-network address via `.env` (not 0.0.0.0), check with `docker compose config --quiet`. |
| Both | `docker compose up -d` on the Mac (Lucian; image pulls need internet); from win, `Invoke-WebRequest http://<mac-ip>:8000/health` returns OK. |

Checkpoint W1: Docker capped at 4/8, both endpoints reach the ingest health check,
`clean-os` snapshots exist, local VM record written.

**W2 (Nov 9-15): endpoint telemetry and clocks**

| Who | Step |
|---|---|
| Claude | Add `lab/endpoints/windows/sysmon-config.xml` (one public config, pinned commit) and `lab/endpoints/linux/audit.rules` (pinned commit), with source and hash in `lab/README.md`. |
| Lucian | win: install `Sysmon64a.exe` (Arm64 build, not `Sysmon64.exe`) with that config; check events appear in `Microsoft-Windows-Sysmon/Operational`. |
| Lucian | lin: install `auditd` and load the rules; install PowerShell 7. |
| Lucian | Time: use the Mac as NTP server for the lab (Claude writes the commands), point win (`w32tm`) and lin at it, all logs in UTC. |
| Claude | `lab/check_clocks.md`: how to record the offset at start and end of each run. |

Checkpoint W2: Sysmon and auditd events visible locally on each endpoint;
clock offset under 1 s on both (target; record the value).

**W3 (Nov 16-22): prototype agent**

| Who | Step |
|---|---|
| Claude | Build `agent/`: shipper config (Vector or Fluent Bit, pinned version) for Sysmon + Security on Windows and auditd + auth.log on Linux, and a one-command installer per OS. Tests for the parsers that are already in scope. |
| Lucian | Run the installer on win and lin (needs internet for the download). |
| Both | Events land in PostgreSQL; `win_security_log_cleared` fires on a hand-cleared Security log (`wevtutil cl Security` on win, a benign manual test, not an Atomic run). |

Checkpoint W3: one real end-to-end alert from win stored in the database.

**W4 (Nov 23-29): Wazuh baseline and the Arm risk**

| Who | Step |
|---|---|
| Lucian | `docker compose down` the prototype. Clone `wazuh-docker` at a pinned tag, deploy single-node in Docker Desktop (Claude prepares the commands; `vm.max_map_count=262144` must be set inside Docker Desktop's VM, how on 4.98 is unverified). |
| Lucian | Install the Wazuh agent on win (x64 under emulation, guide 4.1) and on Kali (Debian package). Add the Sysmon channel to the win agent's `ossec.conf`. |
| Claude | `lab/wazuh/README.md`: pinned tag, ports, agent config, and the `wazuh-default` state description. |
| Both | **Go/no-go:** does the Wazuh agent run and forward Sysmon on Windows on Arm? |

Checkpoint W4: Wazuh shows events from both endpoints. If the Windows agent
fails, stop here and decide (fix, Linux-only Wazuh comparison, or the
second-machine option in guide section 2). Record the decision.

### December: ground truth, attack matrix, first triage

**W5 (Nov 30 - Dec 6): ground-truth wrapper and matching**

| Who | Step |
|---|---|
| Claude | `lab/run_atomic.ps1`: runs one Atomic test, writes one row to `eval/results/<run_id>/ground-truth.csv` (columns in guide 6.3), waits the fixed gap, runs `-Cleanup`. |
| Claude | `eval/match_alerts.py`: joins alerts (prototype and Wazuh exports) to ground truth with the fixed rule (same host, technique or parent, within `start_utc + 15 min`); unit tests. |
| Lucian | Install Invoke-AtomicRedTeam and the atomics on win and lin at a pinned commit (internet on). |

**W6 (Dec 7-13): candidate list and runnability check**

| Who | Step |
|---|---|
| Claude | `lab/attack-matrix.csv` with 20-25 candidate techniques that have Atomic tests and are visible in Sysmon / Security / auditd. Must include the two techniques that already have playbooks (T1110.001, and T1685.005 as the repo labels it). Columns: technique, test GUID, platform, log source, playbook, kept, drop reason. |
| Lucian | With Claude's go and Defender real-time/tamper protection off on win only: run each candidate once with **no SIEM looking** (runnability check, guide 6.1). Record executes / fails and why. |
| Claude | Mark kept and dropped tests in the CSV. Target about 12 kept techniques (the RQ2 alert set needs ~12 × 5). |

Checkpoint W6: about 12 runnable techniques; dropped ones listed with reasons.

**W7 (Dec 14-20): dev / held-out split, `ready` snapshots**

| Who | Step |
|---|---|
| Claude | Split kept techniques into development and held-out with a fixed, committed seed (script in `lab/`), and write the split into research-design section 7 (allowed before the tag). |
| Lucian | Fetch all Atomic prerequisites (`-GetPrereqs`), then cut internet on the endpoints and take UTM snapshot `ready` on win and lin. |
| Claude | Choose a candidate 7-8B model with Lucian; pull happens by hand (Lucian), Claude records tag and digest from `/api/tags`. |

**W8 (Dec 21-27): buffer / holidays.** Only `df` and a backup of `eval/results/`.

### January: the 10-alert pilot (research design section 8)

**W9 (Dec 28 - Jan 3): first end-to-end MTTD.** Lucian runs 2-3 dev-set
techniques through `run_atomic.ps1` against the prototype; Claude runs the
matcher and reports one MTTD per test (pilot, not a result).

**W10 (Jan 4-10): triage of one alert end to end.** Ollama native on the Mac,
bound to the UTM-network address only. Claude wires triage to the stored alert
with temperature 0 and a fixed seed, and checks that the results file records
model digest, prompt hash, seed, condition, run, commit.

**W11 (Jan 11-17): pilot alert set.** 10 alerts from dev-set runs (about 8
attack + 2 benign). Lucian writes the reference labels **before** looking at
the playbooks for those techniques, sources noted. Claude commits labels first.

**W12 (Jan 18-24): run the 2x2 on 10 alerts.** All four conditions, 3 runs;
`eval/blind.py`, Lucian rates run 1 blind, `eval/score_triage.py` runs.
Floor/ceiling check on C1: if the model hallucinates almost always or almost
never, change the model now.

**W13 (Jan 25-31): pilot review.** Short benign run (2 h) with a draft activity
plan (`lab/benign-plan.md`, Claude drafts, Lucian checks it is realistic).
Claude writes a pilot note: what broke, what changed, open items for prereg.

Checkpoint end of January: pipeline works end to end on 10 alerts; model kept
or replaced; benign plan tested.

### February - March: build the alert set, Wazuh tuning, prereg items

| Week | Lucian | Claude |
|---|---|---|
| W14 (Feb 1-7) | Run dev-set techniques, variants 1-2 | Dev-set rules (one rule + tests + playbook per new technique) |
| W15 (Feb 8-14) | Variants 3-4 | Rules, `match_alerts.py` fixes |
| W16 (Feb 15-21) | Variant 5; 24 h benign run (dev) to harvest ~20 benign FPs | F2 load-test replay script; resource sampler (`docker stats` to CSV every 10 s) |
| W17 (Feb 22-28) | **Fallback check** (research design section 8): if behind, apply fallbacks in order | Status note: alert count vs target 80 |
| W18 (Mar 1-7) | Reference labels for all ~80 alerts, written from MITRE / vendor sources, not the playbooks | Commit labels before any rating; pick ~10 wrong-playbook control alerts |
| W19 (Mar 8-14) | Wazuh: max 1 h documented tuning, snapshot/export `wazuh-tuned` | `lab/wazuh/tuning/` with the exact changes |
| W20 (Mar 15-21) | Second rater found and briefed | F2 derivation text, sources for F3-F5 and F8 (only sources actually opened) |
| W21 (Mar 22-28) | F1 rehearsal: one timed install of each system from `clean-os` | Final benign activity plan; F6 capture procedure (`tcpdump` commands) |
| W22 (Mar 29 - Apr 4) | Review research-design section 7 is complete; supervisor sign-off requested | Prompt version hash, model digest, versions table (guide section 9) filled |

### April: freeze and final runs

| Week | Step |
|---|---|
| W23 (Apr 5-11) | Freeze: rules tag (`rules-frozen`) and `prereg-v1` on research-design.md. Only after Lucian says the supervisor items are in place, or records that they are not. |
| W24 (Apr 12-18) | Prototype pass: F1 (3 timed installs), held-out + dev attack matrix from `ready`, F2 sampling, F6 run with internet reachable and a capture of the SIEM containers' network. |
| W25 (Apr 19-25) | Wazuh pass from the same `ready` snapshot: default, then tuned. 24 h benign run per SIEM (F4). |
| W26 (Apr 26 - May 2) | 2x2 run on the 80-alert set, blind rating, second rater on 20%, scoring incl. clustered bootstrap (still to be added to `eval/score_triage.py`, Claude, by March). |

## 3. Run order for each measured pass

1. `df` check, close other apps, `caffeinate -dimsu`, Mac on power.
2. Revert win and lin to `ready`. Start only the SIEM under test, with only its
   agent enabled on the endpoints.
3. Record clock offsets, VM sizes, commit, snapshot names in
   `eval/results/<run_id>/run.md`.
4. Run the matrix with `run_atomic.ps1` (fixed gap, cleanup after each).
5. Export alerts, stop sampling, record clock offsets again.
6. Never re-run and keep only the better run; a failed run is kept and
   labelled.

## 4. Where each F-criterion is logged

| Criterion | File under `eval/results/<run_id>/` | Captured in week |
|---|---|---|
| F1 | `f1-install.csv` (system, rep, start, end, manual steps) + screen recordings kept outside the repo | W21 rehearsal, W24-25 |
| F2 | `f2-resources.csv` (10 s samples), `f2-load.csv` | W16 script, W24-25 |
| F3 | `ground-truth.csv`, `alerts-*.csv`, `matched.csv` | W24-25 |
| F4 | `benign-alerts.csv` + `benign-plan.md` used | W25 |
| F5 | from `matched.csv` (MTTD) and triage records (MTTA) | W24-26 |
| F6 | `f6-*.pcap` summary, list of non-lab destinations | W24 |
| F7 | `f7-cost.md` | any time |
| F8 | from the C4 cells of the 2x2 run | W26 |

## 5. Risks and their checkpoints

| Risk | Checked in | If it fails |
|---|---|---|
| Disk runs out | Every week | Free space before continuing; drop clones, prune images |
| Wazuh Windows agent does not work on Arm | W4 | Decide fix / Linux-only Wazuh comparison / second machine; log it |
| Atomic tests fail on Arm (drivers, x64 tools) | W6 | Drop with reason before any detection is looked at |
| RAM pressure with Ollama | W10, W24 | Triage as replay, record it |
| Docker Desktop VM shares the Mac with endpoints and Ollama | W1, W24 | Report Mac model and memory pressure per run as a limitation |
| Behind schedule end of Feb | W17 | Fallbacks from research design section 8 |
