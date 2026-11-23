# Graph Report - Feasibility-of-an-Open-Source-SIEM  (2026-11-23)

## Corpus Check
- 122 files · ~47,500 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 816 nodes · 1361 edges · 64 communities (50 shown, 14 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 80 edges (avg confidence: 0.87)
- Token cost: 598,644 input · 0 output

## Community Hubs (Navigation)
- Alert Normaliser and Research Design
- Sigma Rule Evaluator
- Blinding and Scoring Scripts
- Ollama Triage Client
- PostgreSQL Schema Migrations
- CI Pipeline
- Ingest API
- Module Design Vocabulary
- Docker Compose Stack
- Lab Build and Ground Truth
- 2x2 Triage Experiment
- Project Overview and Local LLM
- Security Log Cleared Rule
- Domain Docs and ADRs
- Triage Storage and LLM Papers
- Code Review Skill
- Grilling Skills
- ADR and Glossary Formats
- Issue Tracker Backends
- Claim, Evidence and Pre-registration
- Scope Cuts and Install Effort
- MVP Scope and Privacy
- Bug Diagnosis Skill
- Brute Force Playbook
- T1685.005 Playbook
- Defendability Review Fixes
- Wazuh Baseline and Telemetry
- Claude Code Toolkit
- Human Approval Architecture
- YAML Lint Config
- GitHub Issue Tracker Rules
- Thesis Claim Record
- NTP Time Server
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Attack Matrix and Benign Runs
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- HITL Loop Script
- Skill Agent Metadata
- Skill Agent Metadata
- Skill Agent Metadata
- Project Timeline
- Pilot and Schedule Risk
- Fallback Ladder
- Hostile Questions
- Premortem
- AI Use Record
- Ingest Dependencies
- Python Package Config

## God Nodes (most connected - your core abstractions)
1. `Lab build guide` - 22 edges
2. `Thesis plan (Option C)` - 22 edges
3. `matches()` - 17 edges
4. `Lab phase plan (Nov 2026 - Apr 2027)` - 17 edges
5. `RQ1 feasibility scorecard (F1-F8)` - 16 edges
6. `Codebase Design Skill` - 16 edges
7. `clustered_test()` - 16 edges
8. `Project overview` - 15 edges
9. `Decision log and controlled-change record` - 15 edges
10. `triage()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Human in the loop response` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  README.md → docs/thesis/research-design.md
- `Destructive steps require approval` --semantically_similar_to--> `Human approval of actions`  [INFERRED] [semantically similar]
  playbooks/README.md → docs/thesis/research-design.md
- `Technique-clustered robustness check` --references--> `load_techniques()`  [INFERRED]
  docs/thesis/research-design.md → eval/score_triage.py
- `Knowledge graph and clustered scoring (#13)` --references--> `clustered_test()`  [INFERRED]
  CHANGELOG.md → eval/score_triage.py
- `Lab phase plan (Nov 2026 - Apr 2027)` --references--> `clustered_test()`  [INFERRED]
  docs/lab-phase-plan.md → eval/score_triage.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Spec chain publishing to issue tracker** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, claude_issue_tracker [EXTRACTED 1.00]
- **Deep Module Vocabulary** — _claude_skills_codebase_design_skill_module, _claude_skills_codebase_design_skill_interface, _claude_skills_codebase_design_skill_depth, _claude_skills_codebase_design_skill_seam, _claude_skills_codebase_design_skill_adapter, _claude_skills_codebase_design_skill_leverage, _claude_skills_codebase_design_skill_locality [EXTRACTED 1.00]
- **Safeguards against H2 circularity** — docs_thesis_research_design_reference_labels, docs_thesis_research_design_wrong_playbook_control, docs_thesis_research_design_benign_run_24h, docs_thesis_defendability_review_fix3_h2_circularity [EXTRACTED 1.00]
- **RQ2 2x2 grounding experiment design** — docs_project_source_thesis_plan_rq2_grounding_experiment, docs_project_source_thesis_plan_h1_normalisation, docs_project_source_thesis_plan_h2_structured_playbooks, docs_project_source_thesis_plan_normalised_alert_text, docs_project_source_thesis_plan_machine_structured_playbooks [EXTRACTED 1.00]
- **Spec-to-Implementation Pipeline** — _claude_skills_setup_matt_pocock_skills_skill_setup_matt_pocock_skills, _claude_skills_to_spec_skill_to_spec, _claude_skills_to_tickets_skill_to_tickets, _claude_skills_implement_spec_skill_implement_spec, _claude_skills_code_review_skill_code_review [EXTRACTED 1.00]
- **Related work chapter sources (thesis outline)** — docs_project_related_work_related_theses_top5_bjork_2022, docs_project_related_work_related_theses_top5_dahlberg_2025, docs_project_related_work_related_theses_top5_danho_2026, docs_project_related_work_related_theses_top5_nyman_2026, docs_project_related_work_related_theses_top5_ilia_2026 [EXTRACTED 1.00]
- **Atomic run to matched alert flow** — docs_lab_build_guide_atomic_red_team, docs_lab_build_guide_run_atomic_ps1, docs_lab_build_guide_ground_truth_log, docs_lab_build_guide_alert_matching_rule, docs_lab_phase_plan_match_alerts [INFERRED 0.85]
- **Technique-clustered scoring flow** — eval_readme_alerts_csv, eval_score_triage_load_techniques, eval_score_triage_clustered_test, docs_thesis_research_design_technique_clustering [INFERRED 0.85]
- **Issue Tracker Backends** — _claude_skills_setup_matt_pocock_skills_issue_tracker_github_issue_tracker_github, _claude_skills_setup_matt_pocock_skills_issue_tracker_gitlab_issue_tracker_gitlab, _claude_skills_setup_matt_pocock_skills_issue_tracker_local_issue_tracker_local [INFERRED 0.95]

## Communities (64 total, 14 thin omitted)

### Community 0 - "Alert Normaliser and Research Design"
Cohesion: 0.07
Nodes (29): response/: SOAR-lite actions and approval, test_attack_tags(), test_deterministic_and_order_independent(), test_known_fields_are_labelled_with_their_source(), test_nested_ecs_fields(), test_no_event_value_is_lost(), test_destructive_step_without_approval_is_rejected(), test_every_rule_technique_has_a_playbook() (+21 more)

### Community 1 - "Sigma Rule Evaluator"
Cohesion: 0.08
Nodes (20): _eval(), load_rule(), _match_value(), matches(), _wildcard_regex(), rule(), test_exact_match_is_case_insensitive(), test_list_values_are_or() (+12 more)

### Community 2 - "Blinding and Scoring Scripts"
Cohesion: 0.10
Nodes (25): Code track alongside lab weeks, blind(), main(), _without_step_ids(), eval/: harness, metrics, analysis, _ci95(), clustered_test(), differences() (+17 more)

### Community 3 - "Ollama Triage Client"
Cohesion: 0.10
Nodes (17): _client(), info(), prompt(), test_missing_model_raises(), test_non_json_output_is_kept_not_dropped(), test_request_fixes_temperature_seed_and_schema(), test_run_info_collects_digest_and_version(), test_run_info_refuses_dirty_tree() (+9 more)

### Community 4 - "PostgreSQL Schema Migrations"
Cohesion: 0.10
Nodes (27): playbook_steps, playbooks, rules, rules_enabled_idx, schema_migrations, alert_events, alert_events_event_idx, alerts (+19 more)

### Community 5 - "CI Pipeline"
Cohesion: 0.07
Nodes (37): env, ATTACK_DATA_BASE, ATTACK_VERSION, GITLEAKS_SHA256, GITLEAKS_VERSION, SIGMA_ATTACK_DATA, jobs, lint (+29 more)

### Community 6 - "Ingest API"
Cohesion: 0.07
Nodes (14): main(), rule_files(), detect/: Sigma detection engine, health(), ingest/: FastAPI ingestion API, fastapi==0.142.2, convert(), convert_line() (+6 more)

### Community 7 - "Module Design Vocabulary"
Cohesion: 0.09
Nodes (23): Parallel Review Sub-agents, Deepening (guide), Dependency Categories, In-process Dependency, Local-substitutable Dependency, Ports & Adapters (remote but owned), True External Dependency (Mock), Compare by Depth, Locality, Seam Placement (+15 more)

### Community 8 - "Docker Compose Stack"
Cohesion: 0.07
Nodes (31): context, dockerfile, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, interval, retries, test (+23 more)

### Community 9 - "Lab Build and Ground Truth"
Cohesion: 0.13
Nodes (24): Lab build guide, Alert matching rule (same host, technique, 15 min window), 24 h benign run with activity plan, Chrony time sync across lab VMs, F6 privacy egress packet capture, Ground-truth log (ground-truth.csv), Isolated lab network (no internet during runs), Kali VM reused as Linux endpoint (+16 more)

### Community 10 - "2x2 Triage Experiment"
Cohesion: 0.11
Nodes (17): C1 raw JSON, no playbook, C2 raw JSON + playbook, C3 normalised text, no playbook, C4 normalised text + playbook, Danho (KTH 2026), 2x2 triage design (C1-C4), H1 normalised text lowers hallucination, H2 playbooks raise correct steps (+9 more)

### Community 11 - "Project Overview and Local LLM"
Cohesion: 0.13
Nodes (19): Atomic Red Team / Invoke-AtomicRedTeam, Ollama native on the Mac (Metal GPU), Project overview, Detection as code (Sigma in Git, CI-tested), Private local LLM triage (no data leaves the network), Related theses: top 5 master's, Daniel 2025: Triggering false alarms (LotL, Sigma, Atomic, Wazuh), Ghaffarzadegan 2026: AutoSigma CTI-derived Sigma rules (+11 more)

### Community 12 - "Security Log Cleared Rule"
Cohesion: 0.11
Nodes (18): author, date, description, detection, condition, selection, falsepositives, id (+10 more)

### Community 13 - "Domain Docs and ADRs"
Cohesion: 0.16
Nodes (14): Domain docs (single-context), Domain Docs (agent guide), Single-context repo layout, Decision log (ADRs), ADR 0001 storage choice (planned), PostgreSQL storage and SQL-compiled detection, Detection loop over SQL views with watermarks, db/migrations mounted into docker-entrypoint-initdb.d (+6 more)

### Community 14 - "Triage Storage and LLM Papers"
Cohesion: 0.23
Nodes (18): triage_outputs table (one row per LLM call), Danho 2026: Classification of security alerts using LLM embeddings, Nyman 2026: Preparing CSOC SOPs for RAG-based decision support, ECS-like normalized event schema, Thesis plan (Option C), Fallbacks if behind by end of February, H1: normalised text reduces hallucination, H2: structured playbooks raise correct steps (+10 more)

### Community 15 - "Code Review Skill"
Cohesion: 0.16
Nodes (15): Code Review Skill, Fixed Point (diff base), Spec Axis, Standards Axis, Implement Skill, Implementer Subagent (worktree per ticket), TDD Anti-patterns (implementation-coupled, tautological, horizontal slicing), Rules of the Loop (red before green, refactor in review) (+7 more)

### Community 16 - "Grilling Skills"
Cohesion: 0.16
Nodes (15): Grill Me Skill, Grill With Docs Skill, Design Tree, Decision Frontier (rounds), Grilling Skill, Implement Spec Skill, Integration Branch, Merger Subagent (+7 more)

### Community 17 - "ADR and Glossary Formats"
Cohesion: 0.16
Nodes (11): ADR Format, Sequential ADR Numbering (docs/adr/NNNN-slug.md), GLOSSARY.md Format, GLOSSARY-MAP.md (multi-context), Challenge Terms Against Glossary, Domain Modeling Skill, Lazy Creation of GLOSSARY.md and docs/adr/, Offer ADRs Sparingly (+3 more)

### Community 18 - "Issue Tracker Backends"
Cohesion: 0.21
Nodes (15): Issue Tracker: GitHub (gh CLI), GitHub Native Issue Dependencies (blocking), PRs as a Request Surface Flag, Wayfinding Operations (GitHub), Issue Tracker: GitLab (glab CLI), GitLab Native Blocking Link, Wayfinding Operations (GitLab), Issue Tracker: Local Markdown (.scratch/) (+7 more)

### Community 19 - "Claim, Evidence and Pre-registration"
Cohesion: 0.21
Nodes (8): Knowledge graph and clustered scoring (#13), graphify-stale.sh script, Claim record, Where the evidence comes from, Residual uncertainty, Decision log and controlled-change record, prereg-v1 freeze tag, Research design and pre-registration

### Community 20 - "Scope Cuts and Install Effort"
Cohesion: 0.14
Nodes (11): agent/: shipper configs and installer, 24 h benign run, Dahlberg 2025, F1 Install effort, F4 Noise, F5 Speed (MTTD/MTTA), Feasibility criteria F1-F8, TryHackMe SOC Metrics and Objectives (+3 more)

### Community 21 - "MVP Scope and Privacy"
Cohesion: 0.16
Nodes (12): Changelog, Reproducible triage calls (#5), Secret guards (gitleaks, pre-commit, CI scan), F6 Privacy, F7 Cost, normalize/: parsers to ECS-like schema, Detection as code, MVP scope (+4 more)

### Community 22 - "Bug Diagnosis Skill"
Cohesion: 0.15
Nodes (10): Diagnosing Bugs Skill, HITL Loop Script (scripts/hitl-loop.template.sh), Phase 2: Reproduce + Minimise, Phase 3: Ranked Falsifiable Hypotheses, Phase 4: Instrument (tagged debug logs), Phase 5: Fix + Regression Test, Phase 6: Cleanup, Redact Secrets (+2 more)

### Community 23 - "Brute Force Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 24 - "T1685.005 Playbook"
Cohesion: 0.15
Nodes (12): attack_version, false_positive_hints, indicators, steps, action, destructive, id, phase (+4 more)

### Community 25 - "Defendability Review Fixes"
Cohesion: 0.26
Nodes (5): F8 triage trustworthiness, Defendability review against the Student's Guide, Clim & Aldrigo, Student's Guide to Research Projects, F2 Hardware fit, Uzodinma (Lulea 2026)

### Community 26 - "Wazuh Baseline and Telemetry"
Cohesion: 0.20
Nodes (7): Bjork (KTH 2022), Ilia (Malardalen 2026), RQ1 feasibility, Wazuh baseline, Neo23x0 auditd rules, SwiftOnSecurity sysmon-config, Pinned endpoint telemetry configs

### Community 27 - "Claude Code Toolkit"
Cohesion: 0.33
Nodes (8): agent-skills plugin (addyosmani), Claude Code toolkit, diagnosing-bugs skill, graphify knowledge graph, graphify-stale Stop hook, ponytail plugin, /ponytail-review, tdd skill

### Community 28 - "Human Approval Architecture"
Cohesion: 0.25
Nodes (8): Database-enforced approval rules, Human in the loop (approval before any response), Project brief (snapshot), Definition of done, Proposed pipeline architecture, SOAR-lite semi-automated response, SOC metrics targets (MTTD/MTTA/MTTR, TryHackMe), Scope cuts for limited time

### Community 29 - "YAML Lint Config"
Cohesion: 0.25
Nodes (7): extends, max, rules, document-start, line-length, truthy, check-keys

### Community 30 - "GitHub Issue Tracker Rules"
Cohesion: 0.29
Nodes (4): Issue tracker (GitHub Issues), Issue tracker: GitHub, Native GitHub issue dependencies for blocking, Wayfinder map issue with child tickets

### Community 31 - "Thesis Claim Record"
Cohesion: 0.33
Nodes (5): What would reopen the claim, Nordstrom and Wideen (Sigma rule evasion), Atomic Red Team, F3 Detection, lab/: isolated lab setup

### Community 32 - "NTP Time Server"
Cohesion: 0.29
Nodes (6): name, build, ports, restart, services, ntp

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
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 40 - "Skill Agent Metadata"
Cohesion: 0.33
Nodes (5): interface, display_name, short_description, policy, allow_implicit_invocation

### Community 41 - "Attack Matrix and Benign Runs"
Cohesion: 0.33
Nodes (6): Runnability check before detection, Danielsson & Melin 2026: Extending an open-source SIEM with automated testing, Nordström & Widéen 2025: Transformer-based Sigma rule evasion detection, Ilia 2026: Snort and Wazuh for ransomware detection, Development / held-out technique split, Wazuh baseline (default and lightly tuned)

### Community 42 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 43 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 44 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 45 - "HITL Loop Script"
Cohesion: 0.83
Nodes (3): capture(), hitl-loop.template.sh script, step()

### Community 46 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 47 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 48 - "Skill Agent Metadata"
Cohesion: 0.50
Nodes (3): interface, display_name, short_description

### Community 49 - "Project Timeline"
Cohesion: 0.50
Nodes (4): 10-alert 2x2 pilot (January), Timeline, Phases Oct 2026 - Jun 2027, Status 2026-11-15 (no results measured)

## Knowledge Gaps
- **58 isolated node(s):** `accessible-siem`, `Fixed Point (diff base)`, `Integration Branch`, `Merger Subagent`, `PRs as a Request Surface Flag` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 288 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Lab phase plan (Nov 2026 - Apr 2027)` connect `Lab Build and Ground Truth` to `Blinding and Scoring Scripts`, `Project Overview and Local LLM`, `Domain Docs and ADRs`, `Project Timeline`, `GitHub Issue Tracker Rules`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **What connects `accessible-siem`, `Fixed Point (diff base)`, `Integration Branch` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Alert Normaliser and Research Design` be split into smaller, more focused modules?**
  _Cohesion score 0.07062146892655367 - nodes in this community are weakly interconnected._
- **Why does `Claude Code toolkit` connect `Claude Code Toolkit` to `Grilling Skills`, `Domain Docs and ADRs`, `GitHub Issue Tracker Rules`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Should `Sigma Rule Evaluator` be split into smaller, more focused modules?**
  _Cohesion score 0.0797872340425532 - nodes in this community are weakly interconnected._
- **Why does `VM record kept outside the repo` connect `GitHub Issue Tracker Rules` to `Lab Build and Ground Truth`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Should `Blinding and Scoring Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.10338164251207729 - nodes in this community are weakly interconnected._