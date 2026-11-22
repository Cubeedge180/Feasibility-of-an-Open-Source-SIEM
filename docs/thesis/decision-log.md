# Decision log and controlled-change record

One row per consequential decision about the problem, scope, method, title or
claim. Each row records the trigger, the exact change, what stays the same,
what it affects, and who approved it. Rows are added, never edited; a later
change gets a new row that refers to the earlier one.

"Approved by" is `Lucian` for decisions the author took alone and `pending`
where the supervisor's approval is still needed. Supervisor approval is not
recorded until it exists.

| # | Date | Decision | Trigger | Exact change | Unchanged core | Affects | Approved by |
|---|---|---|---|---|---|---|---|
| D1 | 2026-10-14 | Choose research design Option C | Plan showed the three earlier RQs described a system without a falsifiable claim | RQ1 feasibility scorecard with pre-set thresholds vs Wazuh; RQ2 2x2 triage experiment; old ATT&CK-coverage RQ folded into RQ1 | Building the prototype and comparing it with a baseline | `thesis-plan.md`, `research-design.md` | Lucian; supervisor pending |
| D2 | 2026-10-14 | Set the thesis title | Lucian chose a title that names Wazuh and local LLM triage | Title becomes "Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage" | Open-source SIEM with detection as code and local LLM triage | Title, abstract, introduction | Lucian; supervisor pending |
| D3 | 2026-10-14 | Drop the SME focus | Lucian wanted the title and RQs without an SME requirement; SME relevance could not be evidenced within the time available | Target context becomes "organisations without a dedicated SOC"; SME removed from title and RQs | Problem of no SOC and no budget for commercial tools | Problem statement and motivation; the relevance evidence now has to come from sources on organisations without a SOC | Lucian; supervisor pending |
| D4 | 2026-10-14 | Cut scope for time | Bachelor-sized scope with limited time | No Caldera attack chains, no resilience tests, no Telegram approval; ModSecurity optional; 24 h benign run; one model | Everything RQ1 and RQ2 need | Attack matrix, limitations section | Lucian; supervisor pending |
| D5 | 2026-10-14 | Pre-register thresholds and analysis | A claim with thresholds fixed after the fact is not falsifiable | `research-design.md` frozen by tag `prereg-v1` before final runs (planned April 2027); later changes only as dated amendments | The thresholds and tests as drafted | Final measurement runs | Lucian |
| D6 | 2026-10-21 | Review the design against the Student's Guide | Lucian asked whether the topic is defendable | Verdict: defendable with seven fixes, listed in `defendability-review.md`. Adopted in D7 | The whole design | Fixes 1-7, schedule | Lucian |
| D8 | 2026-11-04 | SIEM server runs in Docker Desktop on the Mac | Lab build on a 24 GB Mac; Lucian judged speed variation not that important compared with building a separate server VM | Both SIEM stacks run in Docker Desktop on the Mac, one at a time, VM capped at 4 CPU / 8 GB; replaces the dedicated server VM in `lab-build-guide.md` section 2. F2 is measured on the capped Docker Desktop VM; F6 counts only the SIEM containers' traffic, with Docker Desktop usage statistics and auto-update off; F7 notes Docker Desktop licence terms | F2 thresholds (4 vCPU / 8 GB, 500 events/s), F6 zero-outbound threshold, one SIEM per pass from the same endpoint snapshot | F2, F6, F7 measurement procedure and limitations; `docs/lab-phase-plan.md` | Lucian; supervisor pending |
| D9 | 2026-11-04 | One SIEM per pass, same procedure from the same snapshot | Both SIEMs plus endpoints do not fit in 24 GB RAM at once (`lab-build-guide.md` section 2) | Endpoints revert to snapshot `ready`; prototype pass, then Wazuh pass, with the same Atomic wrapper, matrix and benign plan; endpoints run only the agent of the SIEM under test. "Same attack runs" becomes "same attack procedure from the same snapshot" | Wazuh as reference, held-out headline comparison, F3-F5 thresholds | F3-F5 comparison wording, limitations | Lucian; supervisor pending |
| D10 | 2026-11-04 | Ollama runs natively on the Mac; triage replayed if RAM is short | Docker Desktop on macOS has no GPU passthrough (`lab-build-guide.md` section 1); RAM budget is about 24 GB with everything running | Ollama installed natively, bound to the lab-network address only. If memory pressure turns yellow during an attack run, Ollama is stopped and triage runs afterwards on the stored alerts; MTTA is then reported as measured on replay | One 7-8B model, temperature 0, fixed seed, F5 MTTA threshold | F2 (model host reported as extra hardware), F5 MTTA, F7 | Lucian; supervisor pending |
| D7 | 2026-10-21 | Adopt the seven fixes from the defendability review | Lucian asked to add the review's findings to the design and plan | F8 criterion; object-under-test statement; independent references, benign alerts and wrong-playbook control; threshold derivation; Atomic Red Team and held-out Wazuh headline; provisional novelty; clustered statistics; Dec-Jan pilot and Feb-Mar labelling | RQ1, RQ2, hypotheses, 2x2 design | `research-design.md`, `thesis-plan.md`, schedule | Lucian; supervisor pending |

## Open decisions

- Supervisor approval of the F8 threshold.
- Supervisor approval of D1-D4 and of the threshold table.
- Whether the title should signal "lightweight, detection-as-code" (review fix 2).
