# Graph Report - Feasibility-of-an-Open-Source-SIEM  (2026-11-23)

## Corpus Check
- 122 files · ~47,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 804 nodes · 1313 edges · 62 communities (47 shown, 15 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 70 edges (avg confidence: 0.86)
- Token cost: 494,922 input · 0 output

## Community Hubs (Navigation)
- Ollama Triage Client
- Alert Normaliser and Research Design
- Sigma Rule Evaluator
- Ingest API
- Arm64 Auditd Rules
- Blinding and Scoring Scripts
- Security Log Cleared Rule
- Brute Force Playbook
- T1685.005 Playbook
- YAML Lint Config
- NTP Time Server
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- HITL Loop Script
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Graph Staleness Hook
- PostgreSQL Schema Migrations
- CI Pipeline
- Python Package Config
- Docker Compose Stack
- Code Review Workflow Skills
- Lab Build and Ground Truth
- Triage Storage and LLM Papers
- Scope Cuts and Install Effort
- Domain Docs and ADRs
- Project Overview and Local LLM
- Defendability Review Fixes
- 2x2 Triage Experiment
- Attack Matrix and Benign Runs
- Claim, Evidence and Pre-registration
- MVP Scope and Privacy
- Wazuh Baseline and Telemetry
- Human Approval Architecture
- RQ2 Hypotheses and Measures
- Thesis Claim Record
- Bug Diagnosis Skill
- Project Timeline
- Pilot and Schedule Risk
- Fallback Ladder
- Hostile Questions
- Premortem
- Claude Code Toolkit
- Ingest Dependencies
- Module Design Vocabulary

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
10. `Decision log and controlled-change record` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Human in the loop response` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  README.md → docs/thesis/research-design.md
- `Destructive steps require approval` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  playbooks/README.md → docs/thesis/research-design.md
- `Evidence-check fixes (2026-11-23 audit)` --references--> `run_info()`  [EXTRACTED]
  CHANGELOG.md → triage/ollama_client.py
- `scipy==1.16.2` --conceptually_related_to--> `Wilcoxon signed-rank analysis with bootstrap CI`  [INFERRED]
  requirements-dev.txt → docs/thesis/research-design.md
- `To Spec Skill` --references--> `Issue tracker (GitHub Issues)`  [INFERRED]
  .claude/skills/to-spec/SKILL.md → CLAUDE.md

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

## Communities (62 total, 15 thin omitted)

### Community 3 - "Ollama Triage Client"
Cohesion: 0.10
Nodes (17): RunInfo, prompt(), info(), _client(), run_info(), test_missing_model_raises(), test_non_json_output_is_kept_not_dropped(), test_request_fixes_temperature_seed_and_schema() (+9 more)

### Community 0 - "Alert Normaliser and Research Design"
Cohesion: 0.06
Nodes (28): get_field(), load(), main(), rule_files(), test_attack_tags(), test_deterministic_and_order_independent(), test_known_fields_are_labelled_with_their_source(), test_nested_ecs_fields() (+20 more)

### Community 2 - "Sigma Rule Evaluator"
Cohesion: 0.08
Nodes (20): load_rule(), rule(), _eval(), _match_value(), matches(), _wildcard_regex(), test_exact_match_is_case_insensitive(), test_list_values_are_or() (+12 more)

### Community 16 - "Ingest API"
Cohesion: 0.14
Nodes (7): health(), fastapi==0.142.2, pysigma==1.5.1, scipy==1.16.2, detect/: Sigma detection engine, ingest/: FastAPI ingestion API, Dev requirements (pysigma, pytest, scipy, jsonschema...)

### Community 19 - "Arm64 Auditd Rules"
Cohesion: 0.24
Nodes (6): convert(), convert_line(), main(), test_convert_keeps_line_count_plus_header(), test_convert_line(), test_rule_with_only_missing_syscalls_is_commented_out()

### Community 7 - "Blinding and Scoring Scripts"
Cohesion: 0.13
Nodes (17): blind(), main(), _without_step_ids(), differences(), load(), main(), score(), test() (+9 more)

### Community 13 - "Security Log Cleared Rule"
Cohesion: 0.11
Nodes (18): author, date, description, detection, condition, selection, falsepositives, id (+10 more)

### Community 20 - "Brute Force Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 21 - "T1685.005 Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 28 - "YAML Lint Config"
Cohesion: 0.25
Nodes (7): extends, max, rules, document-start, line-length, truthy, check-keys

### Community 30 - "NTP Time Server"
Cohesion: 0.29
Nodes (6): name, build, ports, restart, services, ntp

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

### Community 38 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

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

### Community 5 - "PostgreSQL Schema Migrations"
Cohesion: 0.10
Nodes (27): playbook_steps, playbooks, rules, rules_enabled_idx, schema_migrations, alert_events, alert_events_event_idx, alerts (+19 more)

### Community 6 - "CI Pipeline"
Cohesion: 0.07
Nodes (37): env, ATTACK_DATA_BASE, ATTACK_VERSION, GITLEAKS_SHA256, GITLEAKS_VERSION, SIGMA_ATTACK_DATA, jobs, lint (+29 more)

### Community 8 - "Docker Compose Stack"
Cohesion: 0.07
Nodes (31): context, dockerfile, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, interval, retries, test (+23 more)

### Community 1 - "Code Review Workflow Skills"
Cohesion: 0.06
Nodes (48): Fixed Point (diff base), Spec Axis, Standards Axis, Redact Secrets, Design Tree, Decision Frontier (rounds), Handoff Document (in OS temp dir, suggested skills, redacted), Implementer Subagent (worktree per ticket) (+40 more)

### Community 10 - "Lab Build and Ground Truth"
Cohesion: 0.13
Nodes (23): Alert matching rule (same host, technique, 15 min window), Chrony time sync across lab VMs, F6 privacy egress packet capture, Ground-truth log (ground-truth.csv), Isolated lab network (no internet during runs), Kali VM reused as Linux endpoint, lab/run_atomic.ps1 ground-truth wrapper (planned), Sysmon64a.exe (Arm64 Sysmon) (+15 more)

### Community 11 - "Triage Storage and LLM Papers"
Cohesion: 0.20
Nodes (20): triage_outputs table (one row per LLM call), ECS-like normalized event schema, F8 triage trustworthiness, Fallbacks if behind by end of February, H1: normalised text reduces hallucination, H2: structured playbooks raise correct steps, 80-alert labelled triage set, Machine-structured YAML playbooks (+12 more)

### Community 12 - "Scope Cuts and Install Effort"
Cohesion: 0.12
Nodes (15): 24 h benign run, F1 Install effort, F2 Hardware fit, F4 Noise, F5 Speed (MTTD/MTTA), F6 Privacy, F7 Cost, Feasibility criteria F1-F8 (+7 more)

### Community 14 - "Domain Docs and ADRs"
Cohesion: 0.16
Nodes (14): Domain docs (single-context), Single-context repo layout, ADR 0001 storage choice (planned), Detection loop over SQL views with watermarks, db/migrations mounted into docker-entrypoint-initdb.d, detect/pg_backend.py Sigma-to-SQL backend (planned), PostgreSQL as the single store, pySigma-backend-sqlite (+6 more)

### Community 15 - "Project Overview and Local LLM"
Cohesion: 0.16
Nodes (15): Ollama native on the Mac (Metal GPU), Detection as code (Sigma in Git, CI-tested), Private local LLM triage (no data leaves the network), MORDOR 2019 labelled dataset, Policy Floors (bounded LLM severity), Student's Guide defendability review (seven fixes), Project overview, Related theses: top 5 master's (+7 more)

### Community 17 - "Defendability Review Fixes"
Cohesion: 0.22
Nodes (5): F8 Triage trustworthiness, Reference labels, Defendability review against the Student's Guide, Clim & Aldrigo, Student's Guide to Research Projects, Uzodinma (Lulea 2026)

### Community 18 - "2x2 Triage Experiment"
Cohesion: 0.18
Nodes (11): C1 raw JSON, no playbook, C2 raw JSON + playbook, C3 normalised text, no playbook, C4 normalised text + playbook, 2x2 triage design (C1-C4), Human in the loop response, Remediation playbooks, response/: SOAR-lite actions and approval (+3 more)

### Community 22 - "Attack Matrix and Benign Runs"
Cohesion: 0.24
Nodes (11): Atomic Red Team / Invoke-AtomicRedTeam, 24 h benign run with activity plan, Runnability check before detection, ATT&CK attack test matrix, Development / held-out technique split, RQ1 feasibility scorecard (F1-F8), Wazuh baseline (default and lightly tuned), Daniel 2025: Triggering false alarms (LotL, Sigma, Atomic, Wazuh) (+3 more)

### Community 23 - "Claim, Evidence and Pre-registration"
Cohesion: 0.29
Nodes (6): Where the evidence comes from, Residual uncertainty, prereg-v1 freeze tag, Claim record, Decision log and controlled-change record, Research design and pre-registration

### Community 24 - "MVP Scope and Privacy"
Cohesion: 0.22
Nodes (9): Reproducible triage calls (#5), Secret guards (gitleaks, pre-commit, CI scan), Detection as code, MVP scope, Writing a rule workflow, Changelog, normalize/: parsers to ECS-like schema, Project README (+1 more)

### Community 25 - "Wazuh Baseline and Telemetry"
Cohesion: 0.20
Nodes (7): RQ1 feasibility, Wazuh baseline, Neo23x0 auditd rules, SwiftOnSecurity sysmon-config, Pinned endpoint telemetry configs, Bjork (KTH 2022), Ilia (Malardalen 2026)

### Community 26 - "Human Approval Architecture"
Cohesion: 0.25
Nodes (8): Database-enforced approval rules, Human in the loop (approval before any response), Definition of done, Proposed pipeline architecture, SOAR-lite semi-automated response, SOC metrics targets (MTTD/MTTA/MTTR, TryHackMe), Scope cuts for limited time, Project brief (snapshot)

### Community 27 - "RQ2 Hypotheses and Measures"
Cohesion: 0.29
Nodes (7): H1 normalised text lowers hallucination, H2 playbooks raise correct steps, RQ2 grounding experiment, Triage measures (grounded, hallucinated, steps_correct, severity_agree, unsafe), Wilcoxon signed-rank analysis with bootstrap CI, eval/: harness, metrics, analysis, Danho (KTH 2026)

### Community 29 - "Thesis Claim Record"
Cohesion: 0.33
Nodes (5): What would reopen the claim, Atomic Red Team, F3 Detection, lab/: isolated lab setup, Nordstrom and Wideen (Sigma rule evasion)

### Community 4 - "Bug Diagnosis Skill"
Cohesion: 0.06
Nodes (30): HITL Loop Script (scripts/hitl-loop.template.sh), Phase 2: Reproduce + Minimise, Phase 3: Ranked Falsifiable Hypotheses, Phase 4: Instrument (tagged debug logs), Phase 5: Fix + Regression Test, Phase 6: Cleanup, Sequential ADR Numbering (docs/adr/NNNN-slug.md), GLOSSARY-MAP.md (multi-context) (+22 more)

### Community 46 - "Project Timeline"
Cohesion: 0.50
Nodes (4): 10-alert 2x2 pilot (January), Phases Oct 2026 - Jun 2027, Status 2026-11-15 (no results measured), Timeline

### Community 9 - "Module Design Vocabulary"
Cohesion: 0.10
Nodes (23): Parallel Review Sub-agents, Dependency Categories, In-process Dependency, Local-substitutable Dependency, Ports & Adapters (remote but owned), True External Dependency (Mock), Compare by Depth, Locality, Seam Placement, Adapter (+15 more)

## Knowledge Gaps
- **58 isolated node(s):** `accessible-siem`, `Fixed Point (diff base)`, `Integration Branch`, `Merger Subagent`, `PRs as a Request Surface Flag` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 285 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Lab phase plan (Nov 2026 - Apr 2027)` connect `Lab Build and Ground Truth` to `Bug Diagnosis Skill`, `Domain Docs and ADRs`, `Project Timeline`, `Project Overview and Local LLM`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **What connects `accessible-siem`, `Fixed Point (diff base)`, `Integration Branch` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ollama Triage Client` be split into smaller, more focused modules?**
  _Cohesion score 0.09872241579558652 - nodes in this community are weakly interconnected._
- **Why does `Claude Code toolkit` connect `Bug Diagnosis Skill` to `Code Review Workflow Skills`, `Domain Docs and ADRs`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Should `Alert Normaliser and Research Design` be split into smaller, more focused modules?**
  _Cohesion score 0.05926251097453907 - nodes in this community are weakly interconnected._
- **Why does `VM record kept outside the repo` connect `Bug Diagnosis Skill` to `Lab Build and Ground Truth`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Should `Sigma Rule Evaluator` be split into smaller, more focused modules?**
  _Cohesion score 0.0797872340425532 - nodes in this community are weakly interconnected._