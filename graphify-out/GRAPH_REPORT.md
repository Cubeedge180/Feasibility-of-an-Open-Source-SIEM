# Graph Report - Feasibility-of-an-Open-Source-SIEM  (2026-11-23)

## Corpus Check
- 3 files · ~46,830 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 803 nodes · 1296 edges · 62 communities (46 shown, 16 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.86)
- Token cost: 417,278 input · 0 output

## Community Hubs (Navigation)
- Alert Normaliser and Research Design
- Code Review Workflow Skills
- Sigma Rule Evaluator
- Ollama Triage Client
- Bug Diagnosis Skill
- PostgreSQL Schema Migrations
- CI Pipeline
- Changelog and Eval Scripts
- Docker Compose Stack
- Module Design Vocabulary
- Lab Build and Ground Truth
- Sigma Rule Linter
- Triage Storage and LLM Papers
- Scope Cuts and Install Effort
- Security Log Cleared Rule
- Domain Docs and ADRs
- Related Work and Benign Runs
- Thesis Decision Log
- Defendability Review Fixes
- Brute Force Playbook
- T1685.005 Playbook
- Related Work and Benign Runs
- Thesis Claim Record
- 2x2 Triage Experiment
- Human Approval Architecture
- RQ2 Hypotheses and Measures
- Sigma Rule Linter
- YAML Lint Config
- NTP Time Server
- MVP Scope and Privacy
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Sigma Rule Linter
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- HITL Loop Script
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Changelog and Eval Scripts
- Pilot and Schedule Risk
- Graph Staleness Hook
- Fallback Ladder
- Hostile Questions
- Premortem
- Claude Code Toolkit
- Ingest Dependencies
- Python Package Config

## God Nodes (most connected - your core abstractions)
1. `Lab build guide` - 22 edges
2. `Thesis plan (Option C)` - 22 edges
3. `matches()` - 17 edges
4. `Lab phase plan (Nov 2026 - Apr 2027)` - 16 edges
5. `RQ1 feasibility scorecard (F1-F8)` - 16 edges
6. `Codebase Design Skill` - 16 edges
7. `Project overview` - 15 edges
8. `triage()` - 14 edges
9. `Setup Matt Pocock Skills` - 14 edges
10. `check()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Human in the loop response` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  README.md → docs/thesis/research-design.md
- `Destructive steps require approval` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  playbooks/README.md → docs/thesis/research-design.md
- `Evidence-check fixes (2026-11-23 audit)` --references--> `run_info()`  [EXTRACTED]
  CHANGELOG.md → triage/ollama_client.py
- `scipy==1.16.2` --conceptually_related_to--> `Wilcoxon signed-rank analysis with bootstrap CI`  [INFERRED]
  requirements-dev.txt → docs/thesis/research-design.md
- `Lab chrony time server (lab/ntp/)` --conceptually_related_to--> `D8 SIEM server in Docker Desktop on the Mac`  [INFERRED]
  lab/check_clocks.md → docs/thesis/decision-log.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Spec chain publishing to issue tracker** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, claude_issue_tracker [EXTRACTED 1.00]
- **Deep Module Vocabulary** — _claude_skills_codebase_design_skill_module, _claude_skills_codebase_design_skill_interface, _claude_skills_codebase_design_skill_depth, _claude_skills_codebase_design_skill_seam, _claude_skills_codebase_design_skill_adapter, _claude_skills_codebase_design_skill_leverage, _claude_skills_codebase_design_skill_locality [EXTRACTED 1.00]
- **Safeguards against H2 circularity** — docs_thesis_research_design_reference_labels, docs_thesis_research_design_wrong_playbook_control, docs_thesis_research_design_benign_run_24h, docs_thesis_defendability_review_fix3_h2_circularity [EXTRACTED 1.00]
- **RQ2 2x2 grounding experiment design** — docs_project_source_thesis_plan_rq2_grounding_experiment, docs_project_source_thesis_plan_h1_normalisation, docs_project_source_thesis_plan_h2_structured_playbooks, docs_project_source_thesis_plan_normalised_alert_text, docs_project_source_thesis_plan_machine_structured_playbooks [EXTRACTED 1.00]
- **Spec-to-Implementation Pipeline** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, _claude_skills_implement_spec_skill_implement_spec, _claude_skills_code_review_skill_code_review [EXTRACTED 1.00]
- **Related work chapter sources (thesis outline)** — docs_project_related_work_related_theses_top5_bjork_2022, docs_project_related_work_related_theses_top5_dahlberg_2025, docs_project_related_work_related_theses_top5_danho_2026, docs_project_related_work_related_theses_top5_nyman_2026, docs_project_related_work_related_theses_top5_ilia_2026 [EXTRACTED 1.00]
- **Triage experiment pipeline (normalise, model, validate, blind, score)** — triage_normalise_text, triage_ollama_client, triage_validate_output, eval_blind, eval_score_triage [EXTRACTED 1.00]
- **Atomic run to matched alert flow** — docs_lab_build_guide_atomic_red_team, docs_lab_build_guide_run_atomic_ps1, docs_lab_build_guide_ground_truth_log, docs_lab_build_guide_alert_matching_rule, docs_lab_phase_plan_match_alerts [INFERRED 0.85]
- **Human approval chain for response actions** — docs_thesis_research_design_human_approval, playbooks_readme_requires_approval_rule, response_readme_soar_lite, readme_human_in_the_loop, triage_validate_output [INFERRED 0.85]
- **Issue Tracker Backends** — _claude_skills_setup_matt_pocock_skills_issue_tracker_github_issue_tracker_github, _claude_skills_setup_matt_pocock_skills_issue_tracker_gitlab_issue_tracker_gitlab, _claude_skills_setup_matt_pocock_skills_issue_tracker_local_issue_tracker_local [INFERRED 0.95]

## Communities (62 total, 16 thin omitted)

### Community 0 - "Alert Normaliser and Research Design"
Cohesion: 0.07
Nodes (28): Research design and pre-registration, test_attack_tags(), test_deterministic_and_order_independent(), test_known_fields_are_labelled_with_their_source(), test_nested_ecs_fields(), test_no_event_value_is_lost(), test_destructive_step_without_approval_is_rejected(), test_every_rule_technique_has_a_playbook() (+20 more)

### Community 1 - "Code Review Workflow Skills"
Cohesion: 0.06
Nodes (48): Code Review Skill, Fixed Point (diff base), Spec Axis, Standards Axis, Redact Secrets, Grill Me Skill, Grill With Docs Skill, Design Tree (+40 more)

### Community 2 - "Sigma Rule Evaluator"
Cohesion: 0.08
Nodes (20): _eval(), load_rule(), _match_value(), matches(), _wildcard_regex(), rule(), test_exact_match_is_case_insensitive(), test_list_values_are_or() (+12 more)

### Community 3 - "Ollama Triage Client"
Cohesion: 0.10
Nodes (17): _client(), info(), prompt(), test_missing_model_raises(), test_non_json_output_is_kept_not_dropped(), test_request_fixes_temperature_seed_and_schema(), test_run_info_collects_digest_and_version(), test_run_info_refuses_dirty_tree() (+9 more)

### Community 4 - "Bug Diagnosis Skill"
Cohesion: 0.06
Nodes (30): Diagnosing Bugs Skill, HITL Loop Script (scripts/hitl-loop.template.sh), Phase 2: Reproduce + Minimise, Phase 3: Ranked Falsifiable Hypotheses, Phase 4: Instrument (tagged debug logs), Phase 5: Fix + Regression Test, Phase 6: Cleanup, ADR Format (+22 more)

### Community 5 - "PostgreSQL Schema Migrations"
Cohesion: 0.10
Nodes (27): playbook_steps, playbooks, rules, rules_enabled_idx, schema_migrations, alert_events, alert_events_event_idx, alerts (+19 more)

### Community 6 - "CI Pipeline"
Cohesion: 0.07
Nodes (37): env, ATTACK_DATA_BASE, ATTACK_VERSION, GITLEAKS_SHA256, GITLEAKS_VERSION, SIGMA_ATTACK_DATA, jobs, lint (+29 more)

### Community 7 - "Changelog and Eval Scripts"
Cohesion: 0.11
Nodes (20): Changelog, Reproducible triage calls (#5), Secret guards (gitleaks, pre-commit, CI scan), blind(), main(), _without_step_ids(), differences(), load() (+12 more)

### Community 8 - "Docker Compose Stack"
Cohesion: 0.07
Nodes (31): context, dockerfile, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, interval, retries, test (+23 more)

### Community 9 - "Module Design Vocabulary"
Cohesion: 0.10
Nodes (23): Parallel Review Sub-agents, Deepening (guide), Dependency Categories, In-process Dependency, Local-substitutable Dependency, Ports & Adapters (remote but owned), True External Dependency (Mock), Compare by Depth, Locality, Seam Placement (+15 more)

### Community 10 - "Lab Build and Ground Truth"
Cohesion: 0.13
Nodes (23): Lab build guide, Alert matching rule (same host, technique, 15 min window), Chrony time sync across lab VMs, F6 privacy egress packet capture, Ground-truth log (ground-truth.csv), Isolated lab network (no internet during runs), Kali VM reused as Linux endpoint, lab/run_atomic.ps1 ground-truth wrapper (planned) (+15 more)

### Community 11 - "Sigma Rule Linter"
Cohesion: 0.11
Nodes (8): main(), rule_files(), convert(), convert_line(), main(), test_convert_keeps_line_count_plus_header(), test_convert_line(), test_rule_with_only_missing_syscalls_is_commented_out()

### Community 12 - "Triage Storage and LLM Papers"
Cohesion: 0.20
Nodes (20): triage_outputs table (one row per LLM call), Björk 2022: Feasibility to implement a SIEM based on open-source applications, Danho 2026: Classification of security alerts using LLM embeddings, Nyman 2026: Preparing CSOC SOPs for RAG-based decision support, ECS-like normalized event schema, Thesis plan (Option C), F8 triage trustworthiness, Fallbacks if behind by end of February (+12 more)

### Community 13 - "Scope Cuts and Install Effort"
Cohesion: 0.12
Nodes (15): agent/: shipper configs and installer, 24 h benign run, Dahlberg 2025, F1 Install effort, F2 Hardware fit, F4 Noise, F5 Speed (MTTD/MTTA), F6 Privacy (+7 more)

### Community 14 - "Security Log Cleared Rule"
Cohesion: 0.11
Nodes (18): author, date, description, detection, condition, selection, falsepositives, id (+10 more)

### Community 15 - "Domain Docs and ADRs"
Cohesion: 0.16
Nodes (14): Domain docs (single-context), Domain Docs (agent guide), Single-context repo layout, Decision log (ADRs), ADR 0001 storage choice (planned), PostgreSQL storage and SQL-compiled detection, Detection loop over SQL views with watermarks, db/migrations mounted into docker-entrypoint-initdb.d (+6 more)

### Community 16 - "Related Work and Benign Runs"
Cohesion: 0.16
Nodes (15): Ollama native on the Mac (Metal GPU), Project overview, Detection as code (Sigma in Git, CI-tested), Private local LLM triage (no data leaves the network), Related theses: top 5 master's, Ghaffarzadegan 2026: AutoSigma CTI-derived Sigma rules, Lundberg & Garbrant 2026: LLM-assisted SOC alert analysis, MORDOR 2019 labelled dataset (+7 more)

### Community 17 - "Thesis Decision Log"
Cohesion: 0.14
Nodes (9): Decision log and controlled-change record, Bjork (KTH 2022), Ilia (Malardalen 2026), prereg-v1 freeze tag, RQ1 feasibility, Wazuh baseline, Neo23x0 auditd rules, SwiftOnSecurity sysmon-config (+1 more)

### Community 18 - "Defendability Review Fixes"
Cohesion: 0.21
Nodes (5): Defendability review against the Student's Guide, Clim & Aldrigo, Student's Guide to Research Projects, F8 Triage trustworthiness, Reference labels, Uzodinma (Lulea 2026)

### Community 19 - "Brute Force Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 20 - "T1685.005 Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 21 - "Related Work and Benign Runs"
Cohesion: 0.24
Nodes (11): Atomic Red Team / Invoke-AtomicRedTeam, 24 h benign run with activity plan, Runnability check before detection, Daniel 2025: Triggering false alarms (LotL, Sigma, Atomic, Wazuh), Danielsson & Melin 2026: Extending an open-source SIEM with automated testing, Nordström & Widéen 2025: Transformer-based Sigma rule evasion detection, Dahlberg 2025: Splunk, Graylog, syslog-ng and MTTR, ATT&CK attack test matrix (+3 more)

### Community 22 - "Thesis Claim Record"
Cohesion: 0.20
Nodes (7): Claim record, What would reopen the claim, Residual uncertainty, Nordstrom and Wideen (Sigma rule evasion), Atomic Red Team, F3 Detection, lab/: isolated lab setup

### Community 23 - "2x2 Triage Experiment"
Cohesion: 0.22
Nodes (9): C1 raw JSON, no playbook, C2 raw JSON + playbook, C3 normalised text, no playbook, C4 normalised text + playbook, 2x2 triage design (C1-C4), Nyman (Halmstad 2026), Remediation playbooks, response/: SOAR-lite actions and approval (+1 more)

### Community 24 - "Human Approval Architecture"
Cohesion: 0.25
Nodes (8): Database-enforced approval rules, Human in the loop (approval before any response), Project brief (snapshot), Definition of done, Proposed pipeline architecture, SOAR-lite semi-automated response, SOC metrics targets (MTTD/MTTA/MTTR, TryHackMe), Scope cuts for limited time

### Community 25 - "RQ2 Hypotheses and Measures"
Cohesion: 0.29
Nodes (7): Danho (KTH 2026), H1 normalised text lowers hallucination, H2 playbooks raise correct steps, RQ2 grounding experiment, Triage measures (grounded, hallucinated, steps_correct, severity_agree, unsafe), Wilcoxon signed-rank analysis with bootstrap CI, eval/: harness, metrics, analysis

### Community 27 - "YAML Lint Config"
Cohesion: 0.25
Nodes (7): extends, max, rules, document-start, line-length, truthy, check-keys

### Community 28 - "NTP Time Server"
Cohesion: 0.29
Nodes (6): name, build, ports, restart, services, ntp

### Community 29 - "MVP Scope and Privacy"
Cohesion: 0.33
Nodes (7): normalize/: parsers to ECS-like schema, Detection as code, Human in the loop response, MVP scope, Project README, Writing a rule workflow, Rule tests (positive/negative events)

### Community 30 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 31 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 32 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 33 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 34 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 35 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 36 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 37 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 38 - "Sigma Rule Linter"
Cohesion: 0.33
Nodes (6): detect/: Sigma detection engine, ingest/: FastAPI ingestion API, fastapi==0.142.2, Dev requirements (pysigma, pytest, scipy, jsonschema...), pysigma==1.5.1, scipy==1.16.2

### Community 39 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 40 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 41 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 42 - "HITL Loop Script"
Cohesion: 0.83
Nodes (3): capture(), hitl-loop.template.sh script, step()

### Community 43 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 44 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 45 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 46 - "Changelog and Eval Scripts"
Cohesion: 0.50
Nodes (4): 10-alert 2x2 pilot (January), Timeline, Phases Oct 2026 - Jun 2027, Status 2026-11-15 (no results measured)

## Knowledge Gaps
- **59 isolated node(s):** `accessible-siem`, `Versions to pin before prereg-v1`, `VMware Fusion Pro`, `Disk budget weekly check`, `Who does what (Lucian by hand, Claude code)` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 286 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Lab phase plan (Nov 2026 - Apr 2027)` connect `Lab Build and Ground Truth` to `Related Work and Benign Runs`, `Bug Diagnosis Skill`, `Changelog and Eval Scripts`, `Domain Docs and ADRs`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **What connects `accessible-siem`, `Versions to pin before prereg-v1`, `VMware Fusion Pro` to the rest of the system?**
  _59 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Alert Normaliser and Research Design` be split into smaller, more focused modules?**
  _Cohesion score 0.07364114552893045 - nodes in this community are weakly interconnected._
- **Why does `Claude Code toolkit` connect `Bug Diagnosis Skill` to `Code Review Workflow Skills`, `Domain Docs and ADRs`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Should `Code Review Workflow Skills` be split into smaller, more focused modules?**
  _Cohesion score 0.05858585858585859 - nodes in this community are weakly interconnected._
- **Why does `VM record kept outside the repo` connect `Bug Diagnosis Skill` to `Lab Build and Ground Truth`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Should `Sigma Rule Evaluator` be split into smaller, more focused modules?**
  _Cohesion score 0.0797872340425532 - nodes in this community are weakly interconnected._