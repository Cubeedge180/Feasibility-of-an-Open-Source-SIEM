# How to write the thesis: model, chapter outline and code mapping

Prepared 2026-11-05 for Lucian (ASE CSIE, Informatică Economică in English, licență 2027).
Thesis: *Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage*.

## 1. Is there a public ASE thesis to copy the shape from?

**No full-text ASE licență thesis is public.** This was already established on 2026-11-04 (see `research/ase-similar-theses.md`), and today's search found nothing new:

- ASE CSIE graduates do publish their **code** on GitHub, but not the thesis text. Examples: [Zorilă 2026, *Dezvoltarea unei aplicații Web educaționale dedicate studiului mecanicii*](https://github.com/mariazorila4/Orbitea-Aplicatie_Web_Educationala_dedicata_Studiului_Mecanicii) (CSIE, Informatică Economică 2026; the README names the thesis, no PDF seen at the top level), [DenisAndreiC/smart-home-backend](https://github.com/DenisAndreiC/smart-home-backend) ("Lucrare de licență CSIE 2026", IoT backend), [pitearares/planner](https://github.com/pitearares/planner) ("Licenta ASE CSIE 2026"). These show what a CSIE licență **repository** looks like, which is smaller than yours. *Repo contents beyond the description not checked (GitHub access is limited from here).*
- The Swedish bachelor theses in `research/related-theses-top5.md` (Björk 2022, Dahlberg 2025, etc.) are the best topic match, but DiVA now has a bot check, so their full texts could not be opened today. *Their chapter structure below is the standard Swedish IMRaD shape, not read from the PDFs.* Open Björk's PDF yourself and look at the table of contents; it is the closest model for "build a lightweight SIEM, compare it with a reference".

**Best way to get a real ASE example:** ask your coordinator for one or two past licență theses they supervised (ideally a software/implementation one), or ask the ASE library whether licență theses can be consulted on site. *Neither route verified.*

So the outline below is built from the **official ASE rules** plus two **public guides from sister Economic Informatics departments** that are much more specific about how to present code.

## 2. The rules that apply (sources)

| Source | What it says that matters for you |
|---|---|
| ASE [*Ghid de bune practici*](https://mefc.ase.ro/wp-content/uploads/2021/01/Ghid-de-bune-practici-A4.pdf) (linked from the [CSIE licență page](https://csie.ase.ro/student-csie/examen-licenta/)) | Licență **about 40 pages at 1.5 spacing** (approximate, depends on topic). Body = theoretical part **30-50%**, empirical part **50-70%** (method, then results and discussion), then conclusions. Cover, title page, table of contents (3 heading levels), lists of tables and figures. Introduction states problem, importance, originality and aim, and does not review literature. Results presented without comment, discussion separate. Conclusions give contribution, limitations, future work, without repeating results. **Harvard author-date citations** (Popescu, 2000, p. 20). Annexes optional, numbered, cited as (Anexa 1). Says it is good practice, not a binding standard. No font or margin rules. |
| [CSIE licență page](https://csie.ase.ro/student-csie/examen-licenta/) | PDF named `NUME_PRENUME_ACRONIM PROGRAM_PROFESORCOORDONATOR.PDF`. Title identical on the web page, the coordinator request and the exam request. **Anexa 3 (AI/IAG declaration) goes in the body immediately after the table of contents**, and is also submitted separately signed ([Anexa 3 form](https://csie.ase.ro/wp-content/uploads/2026/06/ANEXA-3-IAG.docx), [Senate decision 38/2026](https://senat.ase.ro/wp-content/uploads/2026/20260325/Hot.Senat%20nr.%2038%20din%2025.03.2026_Aprob.ghid%20utiliz.%20instrument.%20IAG.pdf)). Anexa 1 data protection and [Anexa 2 originality](https://csie.ase.ro/wp-content/uploads/2026/06/ANEXA-2-declaratie-originalitate-lucrare-IULIE-2026-1.docx) are separate. No English-track-specific rules. |
| [UBB FSEGA, Dept. of Economic Informatics, licență guide](https://econ.ubbcluj.ro/departamente/departamente/fisiere/Ghid%20licenta%20departament.pdf) (not ASE, but the same programme at Cluj; the most concrete public guide on code) | Chapters: Introduction, Methodology, Literature, Business/requirements analysis, Design, Implementation, Evaluation, Conclusions. **Analysis and design chapters: diagrams only, no code or screenshots. Implementation chapter: short representative code fragments, no full source; every screenshot backed by the code that produces it.** Diagrams must match what was built, name the real components and technologies, and use UML/BPMN/ER. Every tool and library used goes into the bibliography with its official URL. One language only. At least 30 pages of original content. |
| [ASE Moldova, Cibernetică și Informatică Economică, guide](https://old.ase.md/files/catedre/imi/Indrumar_ElabTezaLic_CIE.pdf) (different university, same field) | Max 70 pages body. Justify language and DBMS choice against alternatives. Module diagram of how components interact. Show output on a concrete example to prove the program works. Annotated source listing in annexes. Figures numbered by chapter (Fig. 3.1, title below), tables (Table 3.1, title above). A4, 12 pt, 1.5 spacing, margins left 3 cm, right 1.5, top and bottom 2. Use these formatting values only if your coordinator gives none. |

**Ask your coordinator** (one email): page target (ASE says ~40; your topic probably needs 45-55), font/margins, citation style (Harvard per ASE guide vs IEEE, common in CS), whether code listings go in annexes or only a repo link, and whether there is a CSIE Word template.

## 3. Recommended outline with page budget

About **48 pages of body** (introduction to conclusions). Theory (ch. 1-2) is about 30% of the body and empirical (ch. 3-7) about 70%, which fits the ASE 30-50 / 50-70 rule. If the coordinator insists on 40, cut ch. 1 to 6 pages, ch. 5 to 5 and ch. 6 to 7.

Front matter (not counted): cover, title page, table of contents, **Anexa 3 AI declaration (right after the TOC)**, abstract (English, ~1 page), lists of figures and tables, abbreviations (SIEM, SOC, EPS, MTTD, ATT&CK, LLM, ...).

| # | Chapter | Pages | What it contains | Evidence from the repo |
|---|---|---|---|---|
| — | **Introduction** | 3 | Problem: SIEM cost and organisations with no SOC. Aim, RQ1 and RQ2 in one sentence each, originality (pre-registered scorecard vs Wazuh + controlled LLM experiment; none in ASE work found). Method in one paragraph (Design Science Research). Last paragraph previews the chapters. No literature, no results. | `docs/thesis/research-design.md` §0-1, `docs/thesis/claim-record.md` |
| 1 | **Theoretical background** | 8 | SIEM pipeline (collect, normalise, store, correlate, alert, respond). Detection-as-code: Sigma, pySigma, rules in Git with tests. MITRE ATT&CK (v19, tactic split). SOC metrics (MTTD, MTTA, FP rate). LLMs, local inference (Ollama), hallucination, grounding/RAG, structured output. Human-in-the-loop and over-reliance. | Concepts only, no code. Cite tool docs (Sigma, pySigma, Ollama, Wazuh, PostgreSQL) with URLs. |
| 2 | **Related work** | 4 | One paragraph each, then a comparison table (who, what, baseline, LLM?, measured?). International: Björk 2022, Dahlberg 2025, Danho 2026, Nyman 2026, Ilia 2026, Uzodinma 2026 (closest prior work). Romanian/ASE: Măcăneață 2024 (IE journal), Bardaș 2025/2026, Corpodean & Ghiran 2026 (UBB, at ASE's IE conference). End with the gap your thesis fills. | `research/related-theses-top5.md`, `research/related-theses-master-top5.md`, `research/ase-similar-theses.md` |
| 3 | **Research method** | 6 | DSR frame (artefact + evaluation). RQs and hypotheses H1, H2. Pre-registration and git tag `prereg-v1`. Lab: VMs, Docker Desktop caps, one SIEM per pass from the same snapshot (D8-D10). Attack source: Atomic Red Team, dev vs held-out techniques. Benign 24 h run. Criteria F1-F8 with thresholds and their sources. 2x2 design, alert set (~80, benign alerts, wrong-playbook control), scoring (grounded, hallucinated, steps correct, unsafe), blinding, Wilcoxon, clustering by technique. Write in the past tense. | `research-design.md` §2-5 and §8, `decision-log.md`, `docs/lab-build-guide.md`, `thesis/methodology-recommendation.docx`. **No lab IPs or credentials in the thesis**, use placeholders as in the repo. |
| 4 | **System analysis and design** | 6 | Requirements (functional: ingest, detect, triage, approve; non-functional: one-command install, 4 vCPU/8 GB, no egress). Architecture/deployment diagram naming the real containers. Data model (ER diagram of the PostgreSQL schema). Sequence diagram: event → Sigma alert → normalised text → LLM with playbook → schema check → human approval → action. Design decisions with alternatives rejected (Python vs others, PostgreSQL vs SQLite/Oracle, pySigma vs own engine, local vs cloud LLM). **Diagrams only, no code** (UBB rule). | `docker-compose.yml`, `docs/design/postgresql-storage.md`, `db/migrations/*.sql`, `playbooks/schema.json`, `triage/output_schema.json`, `docs/decisions/` |
| 5 | **Implementation** | 7 | One section per own component, each with 1-2 short listings (10-25 lines) and the output they produce. Say clearly what is reused (Sigma rules format, pySigma, Ollama, shippers) and what you wrote. See the listing plan in §4. Testing: unit tests, rule positive/negative tests, CI jobs. | `ingest/`, `triage/normalise_text.py`, `detect/`, `rules/`, `triage/ollama_client.py`, `triage/validate_output.py`, `triage/playbooks.py`, `playbooks/*.yml`, `response/`, `ui/`, `.github/workflows/ci.yml`, `tests/` |
| 6 | **Results** | 8 | No interpretation here. 6.1 Lab and install (F1, F2, F6, F7 tables). 6.2 Detection, noise, speed vs Wazuh out of the box and lightly tuned, held-out set first (F3-F5). 6.3 Triage experiment: per-condition rates, H1 and H2 tests, effect sizes, per-technique clusters, inter-rater check. 6.4 F8 and the final scorecard (pass/fail per criterion). 2-3 screenshots of the dashboard showing a real alert with its triage, each tied to code in ch. 5. | `eval/results/`, `eval/score_triage.py`, `eval/blind.py`, harness outputs, pcap/egress logs |
| 7 | **Discussion and limitations** | 4 | What is feasible and what is not, and why. When grounding helps and when it does not. Comparison with Björk, Dahlberg, Nyman, Uzodinma. Limitations stated openly (lab not a real company, one model, ~80 alerts, author wrote rules and playbooks, one main rater, Wazuh tuning capped at 1 h, thresholds partly author's choice). Threats to validity. | `research-design.md` §6, `claim-record.md`, `defendability-review.md` |
| — | **Conclusions** | 2 | Answer RQ1 and RQ2 in plain words, contribution, future work (Caldera chains, more models, real deployment). No new results. | |
| — | Bibliography | — | Harvard (or what the coordinator says). Include every tool and library with official URL. Verify every reference online (the methodology doc's references are still unverified). | |
| — | Annexes | — | A1 pre-registration (frozen version). A2 full threshold table and its sources. A3 one complete playbook + schema. A4 prompt templates per condition. A5 lab inventory with placeholders (no IPs). A6 full result tables per alert / technique. A7 repo URL, commit tag, how to reproduce (`docker compose up`, `pytest`). Only add an annotated source listing if the coordinator asks; otherwise the tagged repo is the source. | |

## 4. Which code goes into the thesis (implementation chapter listing plan)

Show **your own** code, short and representative, each with the output it produces. Around 8-10 listings in total:

1. **Sigma rule + its test events**: `rules/defense_impairment/win_security_log_cleared.yml` with `rules/tests/win_security_log_cleared/positive.json` and `negative.json`. Shows detection-as-code.
2. **Rule linting/testing**: the core of `detect/lint.py` or `detect/evaluator.py` (ATT&CK tag check against pinned 19.2).
3. **CI**: the `lint`, `test` and `migrations` jobs from `.github/workflows/ci.yml` (one excerpt), plus a screenshot of a green run.
4. **Normaliser**: the main function of `triage/normalise_text.py`, with one raw JSON alert and the text it becomes side by side. This is the H1 manipulation, so it deserves the most space.
5. **Playbook**: `playbooks/T1110.001.yml` and the loader/check in `triage/playbooks.py` (only actions in a playbook can be proposed).
6. **LLM call**: the request in `triage/ollama_client.py` showing pinned model, temperature and seed (reproducibility).
7. **Output validation**: `triage/validate_output.py` against `triage/output_schema.json`, with one rejected output.
8. **Approval flow**: the function that refuses to run an action without a recorded approval (`response/`, not written yet), plus the audit row from `db/migrations/0004_approvals_audit.sql`.
9. **Evaluation**: the blinding step (`eval/blind.py`) and the Wilcoxon part of `eval/score_triage.py`.
10. Optional: one SQL migration excerpt (`0002_events_alerts.sql`) if the coordinator values the database part (PL/pgSQL).

Do not paste full files, generated code or config dumps. Put a one-line caption and a reference to the repo path and tag under each listing.

## 5. Code a thesis like this still needs (gaps against the outline)

From the current `main` (checked 2026-11-05). These are what the chapters above assume exists:

| Needed for | Missing now | Notes |
|---|---|---|
| Ch. 5, 6.1 | **Parsers** in `normalize/` (Sysmon, Windows Security, auth.log, Suricata) to the ECS-like schema | Only a README exists. |
| Ch. 5 | **Ingest** beyond `/health` (`ingest/app.py` is 10 lines), writing events to PostgreSQL | |
| Ch. 5 | **Alert builder** in `detect/`: run pySigma rules on stored events, write alerts with ATT&CK tags | Evaluator and lint exist. |
| Ch. 5 | **Agent/shipper config** in `agent/` and the one-command installer (F1) | README only. |
| Ch. 4-5 | **Approval flow** in `response/` and a minimal **dashboard** in `ui/` (alert list, detail with triage, approve button) | README only. Keep the UI small. |
| Ch. 6 | **Measurement harness**: MTTD/MTTA from timestamps, FP rate and alerts/day, CPU/RAM sampling, EPS load test, egress check | `eval/` has only triage scoring. |
| Ch. 6 | **Wazuh comparison scripts**: export Wazuh alerts, map to techniques, same metrics | |
| Ch. 6.3 | **Clustered analysis** by technique in `eval/score_triage.py` | Offered earlier, not yet requested. |
| Ch. 3, 6 | Triage **prompts** per condition in `triage/prompts/` | Folder is empty. |
| Ch. 6 | More rules and playbooks: one per technique in the attack matrix | 1 rule and 2 playbooks today. |

## 6. Writing tips specific to this thesis

- Write chapters 3 and 4 first (now-January), because they follow from the pre-registration; write chapter 1-2 in parallel with the lab work; chapters 6-7 only after the April runs.
- Keep the two RQs as one claim: the scorecard (RQ1) includes F8, which is fed by the triage experiment (RQ2).
- One language only (English). Impersonal or "this thesis" style; methodology in the past tense.
- Every figure and table numbered (Fig. 4.1), captioned, referred to by number, readable in black and white.
- Declare in Anexa 3 both uses of AI: Claude as a coding and drafting assistant, and the local LLM as the object of the experiment.
- Similarity limits at ASE are CS1 ≤ 30%, CS2 ≤ 5% (sistemantiplagiat.ro). If you reuse text from your own repo docs (`research-design.md`), cite the repo.

## Unverified items

- Swedish theses' chapter structure (DiVA full texts behind a bot check today).
- Whether CSIE has its own Word template or font/margin rules (none linked on the CSIE page).
- Contents of the ASE CSIE GitHub repositories beyond their descriptions.
- Whether the ASE library lets students consult past licență theses.
