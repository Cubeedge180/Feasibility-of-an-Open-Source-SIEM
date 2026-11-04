# Lab build guide

How to build the thesis lab on an Apple-silicon Mac so that the prototype and
the Wazuh baseline see the same attacks (Atomic Red Team) and the same 24 h
benign window, with ground-truth timestamps for F1-F8 in
[research-design.md](thesis/research-design.md).

Status: plan, written 2026-11-04. Nothing here is built yet. Claims marked
**(unverified)** were not confirmed from a primary source and must be checked
in the pilot (Dec 2026 - Jan 2027). Every version in section 9 is filled in
and committed before `prereg-v1`.

## 1. Shape of the lab

```
                    Mac (host, macOS)
   ┌──────────────────────────────────────────────────────────┐
   │  Ollama (native, Metal GPU), bound to the lab network     │
   │                                                          │
   │  lab network 10.10.0.0/24, private to the Mac, no route   │
   │  to the internet during runs                              │
   │   ├─ siem    10.10.0.10  Ubuntu 24.04 arm64, 4 vCPU/8 GB   │
   │   │          prototype: docker compose up                 │
   │   ├─ wazuh   10.10.0.20  Ubuntu 24.04 arm64, 4 vCPU/8 GB   │
   │   │          Wazuh single-node docker                      │
   │   ├─ win     10.10.0.30  Windows 11 on Arm, 2-4 vCPU/6 GB  │
   │   │          Sysmon + prototype agent + Wazuh agent       │
   │   │          + Invoke-AtomicRedTeam                       │
   │   └─ lin     10.10.0.40  Ubuntu 24.04 arm64, 2 vCPU/2 GB   │
   │              auditd + both agents + Atomic Red Team       │
   └──────────────────────────────────────────────────────────┘
```

Key choices and why:

- **Both SIEMs watch the same endpoints at the same time.** Each endpoint runs
  the prototype agent and the Wazuh agent side by side, so one Atomic test
  execution produces one ground-truth row that both systems are scored
  against. This is the fairest reading of "same attack runs". If the two
  agents interfere (CPU, event loss), fall back to running the matrix twice
  from the same snapshot, once per SIEM, and record that in
  `docs/thesis/decision-log.md`.
- **Same size for both SIEM VMs** (4 vCPU / 8 GB, the F2 threshold). Wazuh's
  own minimum for the single-node Docker host is 4 cores, 8 GB RAM and 50 GB
  disk, on AMD64 or ARM64 hosts [W1], so it fits the same box.
- **Ollama runs natively on the Mac, not in Docker or a VM.** Docker Desktop on
  macOS has no GPU passthrough, so Ollama in a container runs on CPU only
  [O1]; the same holds for any VM on the Mac. Native Ollama uses the Apple GPU.
  Consequence for the thesis: F2 measures the SIEM VM without the model, and
  the model host is reported as extra hardware in F2 and F7. Record this as a
  decision before `prereg-v1`, because it changes what "runs on 4 vCPU / 8 GB"
  means.

## 2. Hardware: what your Mac can do

Rough RAM budget with everything running at once (estimates, not measured):

| Part | RAM |
|---|---|
| siem VM | 8 GB |
| wazuh VM | 8 GB |
| win VM | 4-6 GB |
| lin VM | 2 GB |
| Ollama with a 7-8B model, 4-bit **(unverified, measure in pilot)** | 5-6 GB |
| macOS itself | 4 GB |
| **Total** | **31-34 GB** |

Disk: plan for 200 GB free (Wazuh alone asks for 50 GB [W1]; Windows VM about
64 GB; snapshots grow).

What to do by Mac memory size:

| Mac RAM | Plan |
|---|---|
| 36 GB or more | Everything at once as in section 1. |
| 24-32 GB | Shrink win to 4 GB and lin to 1.5 GB; run Ollama only during triage, not during the attack and benign runs (MTTA is then measured in a separate replay step, record it). |
| 16-18 GB | Cannot run both SIEMs at once. Run the matrix twice from snapshots (prototype pass, then Wazuh pass), or add a cheap second machine (below). |

### This lab: MacBook Pro M4 Pro, 24 GB, UTM

Both SIEMs plus both endpoints already need about 21-22 GB before macOS and
the model, so the Mac would swap, and swapping corrupts the F2 and F5
numbers. The plan for this Mac is therefore **one SIEM at a time**:

1. Revert endpoints to `ready`, start the prototype VM only, run the attack
   matrix, then the benign run. Ground truth goes to `ground-truth.csv`.
2. Revert endpoints to `ready`, start the Wazuh VM only, and run the same
   matrix with the same wrapper and the same benign activity plan.
3. Endpoints run only the agent of the SIEM in that pass.
4. Ollama runs natively on the Mac, at the same time as the prototype pass
   (about 8 + 4 + 1.5 + 6 + 4 ≈ 23.5 GB, tight; if memory pressure turns
   yellow, close every other app; if it still swaps, run triage as a replay
   after the attack run and record that MTTA was measured on replay).

This changes "same attack runs" to "same attack procedure from the same
snapshot". Write that into `decision-log.md` and the limitations. The
alternative that keeps one shared run is the second machine below.

With UTM: use the **QEMU backend** for the Windows VM (Arm64 guest, no
emulation), and keep repeatable states by **cloning each VM while it is shut
down** (`clean-os`, `ready`, ...) instead of relying on snapshots, because
UTM's built-in snapshots need UTM 5, which was a pre-release at time of
writing [U2]. For the lab network use Host Only if you are on macOS 26 or later
[U1]; otherwise use Shared Network and block internet on each VM with its
firewall during runs **(unverified for the QEMU backend, check in pilot)**.
Switching to VMware Fusion stays an option if cloning becomes a chore.
On macOS 27 (this Mac runs 27.2) UTM 5 snapshots also work for
Apple-Virtualization VMs [U2], so cloning is only needed on UTM 4.

Disk, decided 2026-11-04: free space on the Mac rather than buy an external
drive. To keep the footprint small:

- **Reuse the existing Kali VM as the Linux endpoint (`lin`).** Kali is
  Debian-based; install `auditd`, PowerShell 7 and the agents there. Kali is
  not a named Wazuh agent platform **(unverified; the Debian package should
  install, check in pilot)**.
- **One server VM for both SIEMs.** Because each pass runs one SIEM, the
  prototype stack and the Wazuh stack live in the same Ubuntu VM (4 vCPU /
  8 GB) and only one is started at a time (`docker compose down` the other).
  This also makes F2 the same box for both.
- Budget: server VM about 60 GB (Wazuh asks for 50 GB [W1]), Windows 11 VM
  64 GB (the Windows 11 minimum), plus 20-30 GB for snapshots, so **free
  about 150 GB** before starting.

Second-machine option: a used x86 mini PC (for example 8-core, 32 GB) running
Proxmox VE removes every Windows-on-Arm question in section 4. Cost is a few
hundred euros second hand **(unverified, check local prices)**. Only worth it
if the pilot shows that Atomic tests or the Wazuh Windows agent do not work on
Windows on Arm.

## 3. Virtualisation on the Mac

Recommended: **VMware Fusion Pro**. Broadcom made Fusion and Workstation free
for commercial, educational and personal use from 11 November 2024 [V1]. It
has mature snapshots and a "private to my Mac" network, both needed here.

Alternative: **UTM** (free, open source). Its Apple-Virtualization backend has
a Host Only network only on macOS 26 and later [U1], and snapshots arrived in
UTM 5.0, which is still a pre-release; for Apple-Virtualization VMs they need
macOS 27 [U2]. Use UTM only if you are already on those versions.

Parallels Desktop also works but is paid, which counts against F7.

Steps (Fusion):

1. Install Fusion. Create a custom network (Settings, Network) named `lab`,
   "private to my Mac", subnet 10.10.0.0/24, DHCP off. Give every VM static IPs
   from section 1.
2. Give each VM a second NIC on NAT for setup only (packages, Docker images,
   Atomic prerequisites). Disconnect that NIC before any measured run, except
   for the F6 run (section 7).
3. Turn off Mac sleep during long runs: `caffeinate -dimsu` in a terminal for
   the 24 h benign run, and keep the Mac on power.

## 4. Endpoint VMs

### 4.1 Windows 11 on Arm (win)

- ISO: Microsoft publishes an official Windows 11 Arm64 ISO and says it is for
  people who want to build a Windows on Arm VM [M1]. You still need a licence;
  check what your university gives students **(unverified)**.
- **Sysmon:** use the Arm64 binary `Sysmon64a.exe` from the Sysinternals
  download. The x64 `Sysmon64.exe` installs, but its driver is blocked on Arm,
  because emulation covers only user-mode code and drivers must be Arm64
  [M2][M3]. Windows 11 also ships a built-in Sysmon since update KB5077241
  (Feb 2026), off by default [M4]; use the Sysinternals one for both SIEMs so
  the config is identical and versioned.
- Sysmon config: pick one public config (for example SwiftOnSecurity
  `sysmon-config` or Olaf Hartong `sysmon-modular`), pin the commit hash, and
  keep a copy in `lab/endpoints/windows/`.
- **Wazuh agent:** Wazuh publishes one Windows agent package, listed as
  32/64-bit, with no Arm64 build (version 4.14.9 at time of writing) [W2]. It
  should run under x64 emulation because it is user-mode **(unverified, first
  thing to test in the pilot)**. If it does not, use the second-machine option
  in section 2.
- **Microsoft Defender:** it will block many Atomic tests. Turn off real-time
  and tamper protection on this lab VM only, and state it in the limitations,
  since a real endpoint would have it on.
- Atomic tests that drop x64 tools (for example credential dumpers) run under
  emulation as long as they are user-mode; any test that loads a kernel driver
  will fail on Arm [M2]. Handle this in the attack matrix (section 5).

### 4.2 Linux endpoint (lin)

- Ubuntu Server 24.04 arm64. Install `auditd` with one public rule set (for
  example Florian Roth's `auditd` rules), pinned by commit.
- Wazuh publishes Linux agent packages for arm64 **(unverified for the exact
  version, check the packages list [W3])**.
- Install PowerShell 7 (`pwsh`) so Invoke-AtomicRedTeam runs the same way as on
  Windows; the framework supports Linux and macOS as well as Windows [A1].

### 4.3 Time

MTTD is a difference of timestamps taken on different machines, so clocks must
agree. Run `chrony` as a server on the siem VM, point every other VM to it
(Windows: `w32tm /config /manualpeerlist:10.10.0.10 /syncfromflags:manual
/update`), log all times in UTC, and record the offset (`chronyc tracking`,
`w32tm /stripchart`) at the start and end of each run.

## 5. The two SIEMs

### 5.1 Prototype (siem VM)

1. Install Docker Engine and the compose plugin.
2. `git clone` this repo at the tagged rule freeze, `cp .env.example .env`,
   `docker compose up -d`. This is the F1 server install; time it (section 7).
3. Install the agent on win and lin with the one-command installer from
   `agent/` (to be built). This is the F1 agent install.
4. Point the triage client at Ollama on the Mac (`http://10.10.0.1:11434`,
   see 5.3).

### 5.2 Wazuh (wazuh VM)

1. Set `vm.max_map_count=262144` persistently (the Linux default 65530 is too
   low) [W1].
2. Clone `wazuh-docker` at the release tag you pin, then deploy the single-node
   stack (indexer, manager, dashboard) following [W1]. Ports used: 1514, 1515,
   514/udp, 55000, 9200, 443 [W1].
3. Install the Wazuh agent on win and lin and enrol them with the manager.
4. On win, add the Sysmon channel to the agent's `ossec.conf` as a
   `localfile` with `log_format` `eventchannel` and location
   `Microsoft-Windows-Sysmon/Operational` **(unverified wording, check the
   Wazuh docs for your version)**. Without this Wazuh never sees Sysmon events
   and the comparison is unfair.
5. Snapshot `wazuh-default`. For the "lightly tuned" variant, spend at most one
   hour on documented changes, commit them to `lab/wazuh/tuning/`, and
   snapshot `wazuh-tuned`.

### 5.3 Ollama (Mac)

- Install the macOS app or binary, pin the version, and pull the one 7-8B
  model named in the research design. Record tag and digest.
- By default Ollama binds 127.0.0.1:11434; set `OLLAMA_HOST` to make it listen
  on the lab interface [O1]. Bind it only to the Fusion `lab` network address,
  never 0.0.0.0, so it is not reachable from your home network.
- The repo's `docker-compose.yml` still has an `llm` profile with
  `ollama/ollama:latest`. For the lab, use the native install; if the profile
  stays, pin the image tag.

## 6. Running the attacks

### 6.1 Attack matrix

1. List candidate ATT&CK techniques that have Atomic tests for Windows or
   Linux and that your log sources (Sysmon, Security, auditd) can see.
2. **Runnability check, before any detection is looked at:** run each
   candidate test once on the endpoint with no SIEM involved and keep only
   tests that execute (Arm, missing prerequisites). Record dropped tests and
   the reason in `lab/attack-matrix.csv`. This is not tuning, because no
   detection result is used.
3. Split the remaining techniques into development and held-out sets (for
   example random with a fixed seed, committed), as section 3 of the research
   design requires.

### 6.2 Install and run Atomic Red Team

On each endpoint, with internet on (setup NIC), install the framework and
atomics as described in the Invoke-AtomicRedTeam wiki [A2], then fetch every
prerequisite once:

```powershell
Invoke-AtomicTest T1059.001 -TestNumbers 1 -GetPrereqs
```

Then disconnect the setup NIC and take the snapshot `ready` (section 8).

Per test, the useful parameters are `-TestNumbers` or `-TestGuids` to select a
test, `-CheckPrereqs`, `-Cleanup`, `-TimeoutSeconds`, and `-ExecutionLogPath`
for the execution log; the default logger records start and stop time per test
and a Syslog logger also exists [A1].

### 6.3 Ground-truth log

The ground truth is one row per executed test, written by a small wrapper
(to be added as `lab/run_atomic.ps1`), not reconstructed later:

| Column | Example |
|---|---|
| run_id | `final-2027-04-10` |
| technique | `T1059.001` |
| test_guid | from the atomic YAML |
| endpoint | `win` |
| set | `dev` or `held-out` |
| start_utc | `2027-04-10T09:15:02.123Z` |
| end_utc | `2027-04-10T09:15:09.880Z` |
| exit_code | `0` |
| cleanup_ok | `true` |

Rules:

- Wait a fixed gap (for example 5 minutes) between tests so alerts can be
  matched to one test, and run `-Cleanup` after each.
- Write the CSV to `eval/results/<run_id>/ground-truth.csv`, together with
  the Invoke-AtomicTest execution log, the commit hash and the snapshot names.
- Matching rule, fixed before the run: an alert counts for a test if it is on
  the same host, carries the test's technique (or a parent technique), and its
  timestamp is within `start_utc` and `start_utc + 15 min`.

## 7. Capturing F1-F8

| Criterion | How to capture it in this lab |
|---|---|
| F1 install | From the `clean-os` snapshot, screen-record and time three fresh installs of server and agent per system; count manual steps from the recording. |
| F2 hardware | Sample CPU and RAM on the siem VM every 10 s during runs (`docker stats --no-stream` or `pidstat` into CSV). Load test: replay recorded events to the ingest API at rising rates and note the highest rate held for 10 minutes with no loss. |
| F3 detection | Join alerts from both SIEMs to `ground-truth.csv` with the matching rule (6.3). Report dev and held-out separately; the Wazuh comparison uses held-out only. |
| F4 noise | 24 h benign run from the `ready` snapshot, following the activity plan written before the run (for example a scheduled script that browses, edits files, installs and updates software, logs in and out). Every alert in that window is a false positive unless the plan explains it. |
| F5 speed | MTTD = alert time minus `start_utc`; MTTA = triage output time minus alert time. Both SIEMs from the same run. |
| F6 privacy | One full run with the NAT NIC connected, so the SIEM could reach the internet if it tried. Capture with `tcpdump` on the siem VM's NAT interface and on the Mac's interface to the lab network (for Ollama); any packet to a non-lab address fails F6. Without an upstream route the test would pass trivially. |
| F7 cost | Licences (all €0 here except Windows on the endpoint, which is part of the organisation, not the SIEM) plus the hardware estimate, against one published commercial price. |
| F8 triage | From the RQ2 run on C4, not from the lab directly. |

Store raw files under `eval/results/<run_id>/` so every number can be rebuilt.

## 8. Snapshots and repeatability

Take these snapshots on every VM, and write their names in each run's results:

| Snapshot | State |
|---|---|
| `clean-os` | OS installed and updated, nothing else. Start of every F1 timing. |
| `ready` | Agents, Sysmon/auditd, Atomic prerequisites, time sync; setup NIC off. Start of every attack and benign run. |
| `wazuh-default`, `wazuh-tuned` | The two Wazuh baseline states. |
| `rules-frozen` | siem VM at the tagged rule freeze. |

Before each run: revert endpoints to `ready`, revert or restart the SIEMs,
check clocks, then start. Export the VM settings (vCPU, RAM, disk) into
`lab/vms.md` so someone else can rebuild the same sizes.

## 9. Versions to pin before `prereg-v1`

| Component | Version | Source checked |
|---|---|---|
| macOS, Mac model, RAM | MacBook Pro M4 Pro, 24 GB; macOS version to fill in | |
| VMware Fusion | | |
| Ubuntu (siem, wazuh, lin) | 24.04 arm64 | |
| Windows 11 on Arm build | | [M1] |
| Sysmon (`Sysmon64a.exe`) and config commit | | |
| auditd rules commit | | |
| Wazuh (docker tag, agent) | 4.14.9 current at time of writing | [W2] |
| Invoke-AtomicRedTeam and atomics commit | | [A1] |
| Ollama and model tag + digest | | |
| This repo commit / tag | | |

## 10. Cost

| Item | Cost |
|---|---|
| VMware Fusion | €0 [V1] |
| Ubuntu, Wazuh, Sysmon, Atomic Red Team, Ollama, open models | €0 |
| Windows 11 licence for the endpoint VM | check university licence **(unverified)** |
| Mac | already owned |
| Optional used x86 mini PC (section 2) | a few hundred euros **(unverified)** |

## 11. Build order (fits the Dec-Jan pilot)

1. Fusion, lab network, siem and lin VMs, time sync.
2. Wazuh VM, agent on lin; one Linux Atomic test seen by both SIEMs.
3. win VM with `Sysmon64a.exe`; check the Wazuh agent runs on Arm (the main
   risk). Decide here whether the second machine is needed.
4. Ground-truth wrapper and matching script; one end-to-end MTTD number.
5. Ollama native, triage of one alert end to end (the RQ2 pilot needs this).
6. Runnability check, attack matrix and split, snapshots `ready`.
7. Short benign run (2 h) to test the activity plan before the 24 h run.

## Sources

- [W1] Wazuh Docker deployment (requirements, ports, `vm.max_map_count`): https://documentation.wazuh.com/current/docker/wazuh-container.html
- [W2] Wazuh WPK list (Windows agent 32/64-bit only, 4.14.9): https://documentation.wazuh.com/current/user-manual/agent/agent-management/remote-upgrading/wpk-files/wpk-list.html
- [W3] Wazuh packages list: https://documentation.wazuh.com/current/installation-guide/packages-list.html
- [O1] Ollama FAQ (no GPU in Docker Desktop on macOS; `OLLAMA_HOST`): https://github.com/ollama/ollama/blob/main/docs/faq.md
- [V1] Broadcom makes Fusion and Workstation free for all users: https://www.computing.co.uk/news/2024/broadcom-gives-away-vmware-fusion-and-workstation-for-free
- [U1] UTM network modes: https://docs.getutm.app/settings-apple/devices/network/
- [U2] UTM v5.0.6 release notes (snapshots): https://newreleases.io/project/github/utmapp/UTM/release/v5.0.6
- [M1] Microsoft, Download Windows 11 for Arm-based PCs: https://www.microsoft.com/en-us/software-download/windows11arm64
- [M2] Microsoft, How x86 emulation works on Arm (drivers must be Arm64): https://learn.microsoft.com/windows/arm/apps-on-arm-x86-emulation
- [M3] Microsoft Q&A, Sysmon on a Windows 11 Arm VM (use `Sysmon64a.exe`): https://learn.microsoft.com/en-us/answers/questions/1144832/sysmon-installation-problem-virtual-win11-arm
- [M4] IT-Connect on KB5077241 (built-in Sysmon, Feb 2026): https://www.it-connect.fr/windows-11-la-mise-a-jour-kb5077241-ajoute-sysmon-et-les-outils-rsat-sur-les-machines-arm/
- [A1] Invoke-AtomicTest source, v2.3.0 (parameters, loggers, platforms): https://powershellgallery.com/packages/Invoke-AtomicRedTeam/2.3.0/Content/Public/Invoke-AtomicTest.ps1
- [A2] Invoke-AtomicRedTeam wiki (installation), link not opened in this session **(unverified)**: https://github.com/redcanaryco/invoke-atomicredteam/wiki
