# Graph Report - Feasibility-of-an-Open-Source-SIEM  (2026-11-23)

## Corpus Check
- 131 files · ~52,059 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 974 nodes · 1620 edges · 78 communities (56 shown, 22 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.86)
- Token cost: 115,126 input · 0 output

## Community Hubs (Navigation)
- Lab Build and Ground Truth
- Sigma Rule Evaluator
- Blinding and Scoring Scripts
- CI Pipeline
- Ollama Triage Client
- Docker Compose Stack
- PostgreSQL Schema Migrations
- Module Design Vocabulary
- Defendability Review Fixes
- Lab Phase Weekly Plan
- Playbook Tests
- Normaliser Event Model
- Wazuh Baseline and Telemetry
- Ingest API Tests
- Fluent Bit Agent Design
- 2x2 Triage Experiment
- Security Log Cleared Rule
- Ingest API
- Thesis Claim Record
- Alert Normaliser Tests
- ADR and Glossary Formats
- Ingest Store and Rule Registry
- Code Review Skill
- Issue Tracker Backends
- PostgreSQL Storage Design
- Bug Diagnosis Skill
- Brute Force Playbook
- T1685.005 Playbook
- Triage Output Validation
- Normaliser Tests
- Agent Template Tests
- Implement Spec Workflow
- GitHub Issue Tracker Rules
- SQL-Compiled Detection Plan
- Changelog and Agent Docs
- Schema Smoke Test
- Claude Code Toolkit
- Domain Docs and ADRs
- Test Database Fixture
- YAML Lint Config
- Grilling Skills
- Early Thesis Decisions
- NTP Time Server
- Clustered Scoring and Prereg
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
- Ingest Rejects Table
- Pilot and Schedule Risk
- Linux Agent Installer
- Graphify Stale Hook
- Fallback Ladder
- Hostile Questions
- Premortem
- AI Use Record
- Python Package Config

## God Nodes (most connected - your core abstractions)
1. `Lab phase plan (Nov 2026 - Apr 2027)` - 24 edges
2. `Thesis plan (Option C)` - 22 edges
3. `Lab build guide` - 21 edges
4. `matches()` - 19 edges
5. `Codebase Design Skill` - 16 edges
6. `Project overview` - 15 edges
7. `RQ1 feasibility scorecard (F1-F8)` - 15 edges
8. `normalise()` - 15 edges
9. `PostgreSQL storage and SQL-compiled detection (design note)` - 15 edges
10. `triage()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Detection loop with detect.watermarks` --semantically_similar_to--> `POST /v1/events endpoint`  [INFERRED] [semantically similar]
  docs/design/postgresql-storage.md → ingest/README.md
- `Where the evidence comes from` --references--> `clustered_test()`  [INFERRED]
  docs/thesis/claim-record.md → eval/score_triage.py
- `Human in the loop response` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  README.md → docs/thesis/research-design.md
- `Destructive steps require approval` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  playbooks/README.md → docs/thesis/research-design.md
- `Technique-clustered robustness check` --references--> `clustered_test()`  [INFERRED]
  docs/thesis/research-design.md → eval/score_triage.py

## Import Cycles
- 2-file cycle: `normalize/__init__.py -> normalize/linux.py -> normalize/__init__.py`
- 2-file cycle: `normalize/__init__.py -> normalize/windows.py -> normalize/__init__.py`

## Hyperedges (group relationships)
- **Spec chain publishing to issue tracker** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, claude_issue_tracker [EXTRACTED 1.00]
- **Deep Module Vocabulary** — _claude_skills_codebase_design_skill_module, _claude_skills_codebase_design_skill_interface, _claude_skills_codebase_design_skill_depth, _claude_skills_codebase_design_skill_seam, _claude_skills_codebase_design_skill_adapter, _claude_skills_codebase_design_skill_leverage, _claude_skills_codebase_design_skill_locality [EXTRACTED 1.00]
- **Safeguards against H2 circularity** — docs_thesis_research_design_reference_labels, docs_thesis_research_design_wrong_playbook_control, docs_thesis_research_design_benign_run_24h, docs_thesis_defendability_review_fix3_h2_circularity [EXTRACTED 1.00]
- **RQ2 2x2 grounding experiment design** — docs_project_source_thesis_plan_rq2_grounding_experiment, docs_project_source_thesis_plan_h1_normalisation, docs_project_source_thesis_plan_h2_structured_playbooks, docs_project_source_thesis_plan_normalised_alert_text, docs_project_source_thesis_plan_machine_structured_playbooks [EXTRACTED 1.00]
- **Spec-to-Implementation Pipeline** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, _claude_skills_implement_spec_skill_implement_spec, _claude_skills_code_review_skill_code_review [EXTRACTED 1.00]
- **Related work chapter sources (thesis outline)** — docs_project_related_work_related_theses_top5_bjork_2022, docs_project_related_work_related_theses_top5_dahlberg_2025, docs_project_related_work_related_theses_top5_danho_2026, docs_project_related_work_related_theses_top5_nyman_2026, docs_project_related_work_related_theses_top5_ilia_2026 [EXTRACTED 1.00]
- **Atomic run to matched alert flow** — docs_lab_build_guide_atomic_red_team, docs_lab_build_guide_run_atomic_ps1, docs_lab_build_guide_ground_truth_log, docs_lab_build_guide_alert_matching_rule [INFERRED 0.85]
- **Technique-clustered scoring flow** — eval_readme_alerts_csv, eval_score_triage_load_techniques, eval_score_triage_clustered_test, docs_thesis_research_design_technique_clustering [INFERRED 0.85]
- **Issue Tracker Backends** — _claude_skills_setup_matt_pocock_skills_issue_tracker_github_issue_tracker_github, _claude_skills_setup_matt_pocock_skills_issue_tracker_gitlab_issue_tracker_gitlab, _claude_skills_setup_matt_pocock_skills_issue_tracker_local_issue_tracker_local [INFERRED 0.95]
- **Event pipeline: agent ships, ingest normalises, detects and stores** — agent_readme_fluent_bit_agent, ingest_readme_post_v1_events, normalize_readme_server_side_normalisers, docs_design_postgresql_storage_events_table, docs_design_postgresql_storage_alerts_table, changelog_ingest_rejects_table [EXTRACTED 1.00]
- **Lab decisions driven by the 24 GB Mac (D8, D9, D10)** — docs_thesis_decision_log_d8_docker_desktop, docs_thesis_decision_log_d9_one_siem_per_pass, docs_thesis_decision_log_d10_ollama_native, docs_lab_phase_plan_p1_docker_desktop_server, docs_lab_phase_plan_p2_one_siem_per_pass, docs_lab_phase_plan_p3_ollama_native_replay [EXTRACTED 1.00]
- **Triage reproducibility and evidence controls** — docs_design_postgresql_storage_triage_outputs_table, changelog_reproducible_triage_calls, changelog_blinded_outputs, changelog_run_info_dirty_guard, docs_design_postgresql_storage_db_enforced_rules [INFERRED 0.85]

## Communities (78 total, 22 thin omitted)

### Community 0 - "Lab Build and Ground Truth"
Cohesion: 0.06
Nodes (68): Lab build guide, Alert matching rule (same host, technique, 15 min window), Atomic Red Team / Invoke-AtomicRedTeam, 24 h benign run with activity plan, Chrony time sync across lab VMs, F6 privacy egress packet capture, Ground-truth log (ground-truth.csv), Isolated lab network (no internet during runs) (+60 more)

### Community 1 - "Sigma Rule Evaluator"
Cohesion: 0.06
Nodes (24): applies(), condition_fields(), walk(), _eval(), load_rule(), _match_value(), matches(), _wildcard_regex() (+16 more)

### Community 2 - "Blinding and Scoring Scripts"
Cohesion: 0.09
Nodes (28): H2 playbooks raise correct steps, Reference labels, Wilcoxon signed-rank analysis with bootstrap CI, blind(), main(), _without_step_ids(), alerts.csv (alert_id, technique), eval/: harness, metrics, analysis (+20 more)

### Community 3 - "CI Pipeline"
Cohesion: 0.05
Nodes (47): env, ATTACK_DATA_BASE, ATTACK_VERSION, GITLEAKS_SHA256, GITLEAKS_VERSION, POSTGRES_PASSWORD, POSTGRES_USER, SIGMA_ATTACK_DATA (+39 more)

### Community 4 - "Ollama Triage Client"
Cohesion: 0.11
Nodes (17): _client(), info(), prompt(), test_missing_model_raises(), test_non_json_output_is_kept_not_dropped(), test_request_fixes_temperature_seed_and_schema(), test_run_info_collects_digest_and_version(), test_run_info_refuses_dirty_tree() (+9 more)

### Community 5 - "Docker Compose Stack"
Cohesion: 0.06
Nodes (38): context, dockerfile, postgres, DATABASE_URL, INGEST_TOKEN, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+30 more)

### Community 6 - "PostgreSQL Schema Migrations"
Cohesion: 0.12
Nodes (26): playbook_steps, playbooks, rules, rules_enabled_idx, schema_migrations, alert_events, alert_events_event_idx, alerts (+18 more)

### Community 7 - "Module Design Vocabulary"
Cohesion: 0.10
Nodes (23): Parallel Review Sub-agents, Deepening (guide), Dependency Categories, In-process Dependency, Local-substitutable Dependency, Ports & Adapters (remote but owned), True External Dependency (Mock), Compare by Depth, Locality, Seam Placement (+15 more)

### Community 8 - "Defendability Review Fixes"
Cohesion: 0.08
Nodes (22): What would reopen the claim, Defendability review against the Student's Guide, Nordstrom and Wideen (Sigma rule evasion), Clim & Aldrigo, Student's Guide to Research Projects, Atomic Red Team, 24 h benign run, Dahlberg 2025, F1 Install effort (+14 more)

### Community 9 - "Lab Phase Weekly Plan"
Cohesion: 0.11
Nodes (18): Lab plan, week 1-2 lab setup and secret guards (#9), Lab phase plan (Nov 2026 - Apr 2027), Attack matrix (lab/attack-matrix.csv, ~12 kept techniques), Dev / held-out technique split and ready snapshots, Disk budget weekly check, Where each F-criterion (F1-F8) is logged, Ground-truth wrapper (run_atomic.ps1) and match_alerts.py, Lab as of 2026-11-04 (Mac M4 Pro, win, lin, Docker Desktop) (+10 more)

### Community 10 - "Playbook Tests"
Cohesion: 0.15
Nodes (10): test_attack_tags(), test_destructive_step_without_approval_is_rejected(), test_every_rule_technique_has_a_playbook(), test_playbook_valid(), attack_tags(), load(), load_all(), playbook_files() (+2 more)

### Community 11 - "Normaliser Event Model"
Cohesion: 0.19
Nodes (8): Event, NormaliseError, _line(), parse_auditd(), parse_auth(), _local(), parse(), _parse_time()

### Community 12 - "Wazuh Baseline and Telemetry"
Cohesion: 0.13
Nodes (13): Bjork (KTH 2022), Ilia (Malardalen 2026), RQ1 feasibility, Wazuh baseline, convert(), convert_line(), main(), Neo23x0 auditd rules (+5 more)

### Community 13 - "Ingest API Tests"
Cohesion: 0.16
Nodes (11): git_commit(), client(), _query(), test_bad_token_is_refused(), test_git_commit_reads_this_checkout(), test_record_the_database_refuses_does_not_block_the_batch(), test_rules_are_registered_once_across_restarts(), test_security_log_cleared_raises_alert() (+3 more)

### Community 14 - "Fluent Bit Agent Design"
Cohesion: 0.19
Nodes (13): Fluent Bit 5.1.3 endpoint agent, linux/install.sh installer (Debian/Kali), windows/install.ps1 installer, ingest_rejects table (migration 0005), Week 3 agent, normalisers and inline detection (PR, D11), rules, playbooks, playbook_steps tables, GET /health endpoint, FastAPI ingest service (+5 more)

### Community 15 - "2x2 Triage Experiment"
Cohesion: 0.14
Nodes (15): C1 raw JSON, no playbook, C2 raw JSON + playbook, C3 normalised text, no playbook, C4 normalised text + playbook, Danho (KTH 2026), 2x2 triage design (C1-C4), Nyman (Halmstad 2026), RQ2 grounding experiment (+7 more)

### Community 16 - "Security Log Cleared Rule"
Cohesion: 0.11
Nodes (18): author, date, description, detection, condition, selection, falsepositives, id (+10 more)

### Community 17 - "Ingest API"
Cohesion: 0.13
Nodes (4): health(), ingest_events(), lifespan(), State

### Community 18 - "Thesis Claim Record"
Cohesion: 0.16
Nodes (10): Claim record, Where the evidence comes from, Residual uncertainty, H1 normalised text lowers hallucination, prereg-v1 freeze tag, Research design and pre-registration, Triage measures (grounded, hallucinated, steps_correct, severity_agree, unsafe), response/: SOAR-lite actions and approval (+2 more)

### Community 19 - "Alert Normaliser Tests"
Cohesion: 0.26
Nodes (9): test_deterministic_and_order_independent(), test_known_fields_are_labelled_with_their_source(), test_nested_ecs_fields(), test_no_event_value_is_lost(), flatten(), get_field(), normalise(), _present() (+1 more)

### Community 20 - "ADR and Glossary Formats"
Cohesion: 0.16
Nodes (11): ADR Format, Sequential ADR Numbering (docs/adr/NNNN-slug.md), GLOSSARY.md Format, GLOSSARY-MAP.md (multi-context), Challenge Terms Against Glossary, Domain Modeling Skill, Lazy Creation of GLOSSARY.md and docs/adr/, Offer ADRs Sparingly (+3 more)

### Community 21 - "Ingest Store and Rule Registry"
Cohesion: 0.26
Nodes (6): DeployedRule, _raise_alert(), register_rules(), _reject(), store_batch(), _store_event()

### Community 22 - "Code Review Skill"
Cohesion: 0.21
Nodes (12): Code Review Skill, Fixed Point (diff base), Spec Axis, Standards Axis, Implement Skill, TDD Anti-patterns (implementation-coupled, tautological, horizontal slicing), Rules of the Loop (red before green, refactor in review), TDD Skill (+4 more)

### Community 23 - "Issue Tracker Backends"
Cohesion: 0.23
Nodes (14): Issue Tracker: GitHub (gh CLI), GitHub Native Issue Dependencies (blocking), PRs as a Request Surface Flag, Wayfinding Operations (GitHub), Issue Tracker: GitLab (glab CLI), GitLab Native Blocking Link, Wayfinding Operations (GitLab), Issue Tracker: Local Markdown (.scratch/) (+6 more)

### Community 24 - "PostgreSQL Storage Design"
Cohesion: 0.18
Nodes (11): Reproducible triage calls (#5), PostgreSQL storage and SQL-compiled detection (design note), alerts and alert_events tables, approvals table, audit_log table (siem.actor), events table (JSONB fields, run_label), db/migrations via docker-entrypoint-initdb.d, Storage open points (F2 load test, retention, least-privilege roles) (+3 more)

### Community 25 - "Bug Diagnosis Skill"
Cohesion: 0.15
Nodes (10): Diagnosing Bugs Skill, HITL Loop Script (scripts/hitl-loop.template.sh), Phase 2: Reproduce + Minimise, Phase 3: Ranked Falsifiable Hypotheses, Phase 4: Instrument (tagged debug logs), Phase 5: Fix + Regression Test, Phase 6: Cleanup, Redact Secrets (+2 more)

### Community 26 - "Brute Force Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 27 - "T1685.005 Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 28 - "Triage Output Validation"
Cohesion: 0.32
Nodes (7): test_action_must_match_its_step(), test_action_step_must_be_in_steps(), test_good_output_passes(), test_invented_field_and_step(), test_no_playbook_condition(), test_schema_violation(), check()

### Community 29 - "Normaliser Tests"
Cohesion: 0.32
Nodes (7): normalise(), sample(), test_auditd_record(), test_auth_log_line(), test_sysmon_process_creation(), test_unparseable_records_raise(), test_windows_security_log_cleared()

### Community 30 - "Agent Template Tests"
Cohesion: 0.23
Nodes (4): test_buffering_survives_outages(), test_installer_fills_every_placeholder(), test_migration_is_transactional_and_records_itself(), test_migrations_are_numbered_without_gaps()

### Community 31 - "Implement Spec Workflow"
Cohesion: 0.20
Nodes (10): Implement Spec Skill, Implementer Subagent (worktree per ticket), Integration Branch, Merger Subagent, Ticket Task Graph, Vertical Slices / Tracer Bullets, Blocking Edges, Local Ticket / Issue Templates (+2 more)

### Community 32 - "GitHub Issue Tracker Rules"
Cohesion: 0.18
Nodes (7): ready-for-agent Label, Spec Template (problem, solution, user stories, decisions, testing, scope), To Spec Skill, Issue tracker (GitHub Issues), Issue tracker: GitHub, Native GitHub issue dependencies for blocking, Wayfinder map issue with child tickets

### Community 33 - "SQL-Compiled Detection Plan"
Cohesion: 0.22
Nodes (8): Detection loop with detect.watermarks, pySigma-backend-sqlite 2.0.0, RSigma PostgreSQL/TimescaleDB backend, Threshold/correlation rules as PL/pgSQL (T1110.001), Code track alongside lab weeks, fastapi==0.142.2 / uvicorn==0.54.0, psycopg[binary]==3.3.9, pysigma==1.5.1

### Community 34 - "Changelog and Agent Docs"
Cohesion: 0.22
Nodes (6): Evidence-check fixes from the 2026-11-23 audit, GitHub area labels (area: lab, thesis, detection, triage, infra, security), PostgreSQL schema and storage design (#7), run_info() refuses uncommitted code, Sigma rule win_security_log_cleared, W3: prototype agent, first end-to-end alert

### Community 36 - "Claude Code Toolkit"
Cohesion: 0.33
Nodes (8): agent-skills plugin (addyosmani), Claude Code toolkit, diagnosing-bugs skill, graphify knowledge graph, graphify-stale Stop hook, ponytail plugin, /ponytail-review, tdd skill

### Community 37 - "Domain Docs and ADRs"
Cohesion: 0.32
Nodes (6): Domain docs (single-context), Domain Docs (agent guide), Single-context repo layout, Decision log (ADRs), ADR 0001 storage choice (planned), docs/ index

### Community 39 - "YAML Lint Config"
Cohesion: 0.25
Nodes (7): extends, max, rules, document-start, line-length, truthy, check-keys

### Community 40 - "Grilling Skills"
Cohesion: 0.38
Nodes (6): Grill Me Skill, Grill With Docs Skill, Design Tree, Decision Frontier (rounds), Grilling Skill, User-invoked skills

### Community 42 - "NTP Time Server"
Cohesion: 0.29
Nodes (6): name, build, ports, restart, services, ntp

### Community 43 - "Clustered Scoring and Prereg"
Cohesion: 0.33
Nodes (3): Knowledge graph and clustered scoring (#13), April freeze (rules-frozen, prereg-v1) and final runs, Dev tooling (pytest, httpx, ruff, yamllint, jsonschema, scipy)

### Community 44 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 45 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 46 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 47 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 48 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 49 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 50 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 51 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 52 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 53 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 54 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 55 - "HITL Loop Script"
Cohesion: 0.83
Nodes (3): capture(), hitl-loop.template.sh script, step()

### Community 56 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 57 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 58 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

## Knowledge Gaps
- **78 isolated node(s):** `accessible-siem`, `C1 raw JSON, no playbook`, `ui/: dashboard`, `Strömberg 2020: SIEM practical implementation (Python, PostgreSQL)`, `Fixed Point (diff base)` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 362 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Project overview` connect `Lab Build and Ground Truth` to `PostgreSQL Storage Design`, `Lab Phase Weekly Plan`, `Domain Docs and ADRs`?**
  _High betweenness centrality (0.213) - this node is a cross-community bridge._
- **What connects `accessible-siem`, `C1 raw JSON, no playbook`, `ui/: dashboard` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Lab Build and Ground Truth` be split into smaller, more focused modules?**
  _Cohesion score 0.05593561368209256 - nodes in this community are weakly interconnected._
- **Should `Sigma Rule Evaluator` be split into smaller, more focused modules?**
  _Cohesion score 0.06397306397306397 - nodes in this community are weakly interconnected._
- **Should `Blinding and Scoring Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.09176470588235294 - nodes in this community are weakly interconnected._
- **Should `CI Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.051418439716312055 - nodes in this community are weakly interconnected._
- **Should `Ollama Triage Client` be split into smaller, more focused modules?**
  _Cohesion score 0.1064102564102564 - nodes in this community are weakly interconnected._