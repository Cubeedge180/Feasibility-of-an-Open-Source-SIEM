# Timeline

Overview of the schedule from October 2026 to the defence in June 2027. The week-by-week lab plan
(who does what each week, checkpoints, risks) is [`docs/lab-phase-plan.md`](../lab-phase-plan.md);
lab weeks start on Monday, W1 = 2026-11-04 to 11-08, W26 = 2027-04-26 to 05-02.

## Phases

| When | Phase | Main work | Done when |
|---|---|---|---|
| Oct 2026 | Design | Research questions, thresholds, title, scope cuts, defendability review (D1-D7) | Design in `research-design.md` |
| Nov 2026 | Lab setup | Docker Desktop SIEM host, Windows and Kali endpoints, Sysmon/auditd, lab time server; parsers and Sigma loader | First real alert from a lab attack (W3 checkpoint) |
| Dec 2026 | Ground truth | Attack matrix with dev / held-out split, Atomic runner, alert matching, minimal dashboard | Attack runs produce matched alerts |
| Jan 2027 | Pilot | 2 x 2 triage pipeline on 10 alerts, including a floor/ceiling check on C1 | Pilot report; go / adjust |
| Feb-Mar 2027 | Build | Dev-set rules, ~80-alert set labelled before rating, approval flow, Wazuh install and 1 h tuning, prereg items (F2 derivation, sources, second rater) | Supervisor sign-off requested |
| Apr 2027 | Freeze and measure | Tags `rules-frozen` and `prereg-v1`; prototype pass, Wazuh pass, 24 h benign runs, 2 x 2 run and blind scoring | All F-criteria and H1/H2 measured |
| May 2027 | Writing | Analysis, figures from `eval/results/`, thesis text | Draft complete |
| Jun 2027 | Defence | Demo video, polish, defence | |

## Status (2026-11-15)

| Item | State |
|---|---|
| Research design, decision log D1-D10, claim record | Written; supervisor approval pending |
| Lab W1: SIEM host capped at 4 CPU / ~8 GB, stack healthy, ingest bound to the lab network only | Done |
| Lab W2: pinned Sysmon config (Windows), pinned auditd rules with an arm64 fix (Kali), lab NTP server, clock offsets checked | Done; files in PR #9 |
| Rules | 1 Sigma rule (`win_security_log_cleared`) and 2 playbooks |
| Measured results | None yet |

The status table is updated when a lab checkpoint is met; the [CHANGELOG](../../CHANGELOG.md) lists
each change by pull request.
