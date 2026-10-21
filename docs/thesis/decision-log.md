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
| D7 | 2026-10-21 | Adopt the seven fixes from the defendability review | Lucian asked to add the review's findings to the design and plan | F8 criterion; object-under-test statement; independent references, benign alerts and wrong-playbook control; threshold derivation; Atomic Red Team and held-out Wazuh headline; provisional novelty; clustered statistics; Dec-Jan pilot and Feb-Mar labelling | RQ1, RQ2, hypotheses, 2x2 design | `research-design.md`, `thesis-plan.md`, schedule | Lucian; supervisor pending |

## Open decisions

- Supervisor approval of the F8 threshold.
- Supervisor approval of D1-D4 and of the threshold table.
- Whether the title should signal "lightweight, detection-as-code" (review fix 2).
