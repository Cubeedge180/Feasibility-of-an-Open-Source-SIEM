# Endpoint telemetry configs

Pinned copies of the public configs used on the lab endpoints. Both SIEMs read
the same telemetry, so these files are part of the fair comparison. Do not edit
them in place; to change one, fetch a new upstream commit, update this table and
log it in `docs/thesis/decision-log.md`.

| File | Source | Commit | SHA-256 | Licence |
|---|---|---|---|---|
| `windows/sysmonconfig-export.xml` | [SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config) | `1836897f12fbd6a0a473665ef6abc34a6b497e31` (2021-10-17, source version 74) | `055febc600e6d7448cdf3812307275912927a62b1f94d0d933b64b294bc87162` | CC BY 4.0 (stated in the file header) |
| `linux/audit.rules` | [Neo23x0/auditd](https://github.com/Neo23x0/auditd) | `6111069472c26c4120002933b67cef9855dfbad5` (2026-05-04) | `922b43e7b7c4ce386749a0e63c3a228a13854277de2ef092eddb536a8fa4142e` | Apache-2.0 |
| `linux/audit.rules.arm64` | Derived from `linux/audit.rules` by `python -m lab.arm64_audit_rules` | same | `ac78b8301a4d9b1acc1c422478dd5adf666f26c04da9703a990c81cac5418038` | Apache-2.0 |

Notes:

- Windows on Arm needs the Arm64 Sysmon binary `Sysmon64a.exe` from the
  Sysinternals `Sysmon.zip` (lab-build-guide 4.1). Record its version.
- The SwiftOnSecurity config was last changed in 2021; it requires Sysmon 13 or
  later (file header). Newer event types added to Sysmon since then are not
  configured by it.
- **Kali on arm64 loads `audit.rules.arm64`, not `audit.rules`.** The upstream
  rules list legacy syscalls (`open`, `chmod`, `mkdir`, ...) next to the modern
  `*at` forms. aarch64 has no legacy syscalls, so auditctl rejected each such
  `arch=b64` rule as a whole and the modern syscalls in it were lost too
  (observed 2026-11-10: 184 rules loaded, "Syscall name unknown" errors).
  `lab/arm64_audit_rules.py` removes only the missing names from `arch=b64`
  rules; `arch=b32` rules and everything else are unchanged. Both SIEMs read
  the same auditd log, so the comparison stays fair.
- Remaining load messages are expected: "No such file or directory" for watched
  paths that do not exist on Kali, "Rule exists" for duplicates in the upstream
  file, and "Old style watch rules are slower" warnings. The file starts with
  `-i`, so these do not abort the load. Record the loaded rule count
  (`auditctl -l | wc -l`) in the local VM record.
- The upstream file keeps `-e 2` (immutable) commented out; leave it that way in
  the lab so rules can be reloaded without a reboot.

Install steps: see W2 in [docs/lab-phase-plan.md](../../docs/lab-phase-plan.md)
and the commands posted with it.
