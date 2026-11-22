> Literature search notes (2026-10), copied from the project library. Early titles mention SMEs;
> the SME focus was dropped in decision D3.

# Related theses: top 5 bachelor theses closest to "Accessible SIEM: detection-as-code and AI triage for SMEs"

Updated 2026-10-14, after you asked for **bachelor level only** (an SME focus is not required).

**How degree level was verified.** DiVA blocks automated reading. The level of each thesis was taken from its DiVA record as mirrored on uppsatser.se, where the line "Detta är en Kandidat-uppsats …" means a bachelor thesis. Every thesis below is confirmed first-cycle (bachelor) level. #5 is a first-cycle *professional* degree (högskoleingenjör), which is also bachelor level.

**What changed from the first list.** Checking the levels showed that four of the original five were master's theses, so they are removed: Uzodinma (Luleå), Daniel (KTH), Lundberg & Garbrant (Linköping) and Danielsson & Melin (Blekinge, advanced level). My earlier guess that Daniel was "probably bachelor" was wrong. Only Björk (KTH) stays.

All five are from DiVA, which covers KTH and about 50 other Swedish universities. The other nine sources had no bachelor thesis close to your topic; the source log is at the end.

---

## 1. Feasibility to implement a SIEM based on Open-source applications

- **Robin Björk, KTH EECS, 2022** · Kandidat-uppsats (bachelor)
- [DiVA record](http://www.diva-portal.org/smash/record.jsf?pid=diva2:1668180) · [abstract](https://www.uppsatser.se/uppsats/bc4e415877/)

**What it does.** It asks whether a *lightweight* SIEM can be built from open-source software, because commercial SIEMs are too expensive for smaller companies. The author studies logging and event correlation to choose components. The result is a small SIEM with "a few rules", a rule structure designed so new rules are easy to add, and a visual tool for alarms and logs. FortiSIEM is the reference point. Conclusion: the prototype works but does not reach FortiSIEM's standard.

**Why it ranks first.** It is the closest bachelor thesis to your system: one student, a lightweight SIEM, easy-to-add rules and a cost argument. It is your nearest direct predecessor (RQ1).

**What to take.** Its framing and its limits make a ready "prior work" paragraph. Its "rules that are easy to add" idea is what Sigma-in-Git with CI tests does in a standard way.

**How yours is stronger.** It reports no measured detection rate, no ATT&CK mapping and no attack runs; the comparison with FortiSIEM is qualitative. You add a standard rule language, CI-tested rules, measured MTTD, detection rate and false-positive rate, ATT&CK coverage, a Wazuh baseline and LLM triage.

---

## 2. Exploring Incident Management: A Comparative Study of Splunk Enterprise, Graylog Open and Syslog-ng and their Impact on MTTR

- **Gustav Dahlberg, Stockholm University, 2025** · Kandidat-uppsats (bachelor)
- [abstract](https://www.uppsatser.se/uppsats/80ab8c0781/)

**What it does.** It compares three SIEM tiers (advanced: Splunk ES; intermediate: Graylog Open; basic: syslog-ng). It uses **Invoke-AtomicRedTeam** to run attacks in a lab and computes **MTTD and MTTA from log timestamps**. MTTI (time to identify) is excluded on purpose, because it depends on the analyst's skill.

**Results.** The higher-tier systems detected *more slowly*: syslog-ng had the lowest MTTD, and Splunk's MTTD was 21% higher than Graylog's. Splunk was the most consistent, with about 25% lower standard deviation. Graylog beat Splunk on MTTA but had problems with alert reliability. Syslog-ng's MTTA was fixed at 30 minutes because it relies on manual review.

**Why it ranks second.** It is the best bachelor-level model for your **evaluation method**. It uses the same attack tool you plan to use, the same SOC metrics (MTTD and MTTA, like your TryHackMe-based targets), timestamps taken automatically from the logs, and a comparison of your system against established SIEMs.

**What to take.** Its timestamp-based MTTD and MTTA protocol, and reporting the standard deviation as well as the mean. Also its choice to leave out human-dependent times, which you can cite when you define MTTR as "alert to *approved* response".

---

## 3. Classification of Security Alerts Using Large Language Model Embeddings

- **Alexander Danho, KTH EECS, 2026** · Kandidat-uppsats (bachelor)
- [abstract](https://www.uppsatser.se/uppsats/6535d90272/)

**What it does.** SOCs receive alerts from many vendors, each in its own format. Grouping alerts by keyword matching breaks when a format changes. The author builds a pipeline that collects raw alerts from IT and OT networks and **normalises them into standard text descriptions**. LLM embeddings with zero-shot classification then sort the alerts into four environment categories and into **MITRE ATT&CK techniques**. It is tested with simulated attacks.

**Results.** 91.5% of alerts were placed in the correct environment category. The author states the limits plainly: simulated attacks and a small dataset.

**Why it ranks third.** It is the bachelor thesis closest to your **LLM triage** (RQ2). It also maps alerts to ATT&CK (RQ3), and its "normalise first, then reason" design matches your ECS-like normalisation step.

**What to take.** Normalising alerts to a single text form before the model sees them is a good pattern for your prompts. Its open statement of limitations (simulated attacks, small dataset) is a model for your own limitations section.

**How yours differs.** Danho classifies alerts. You generate explanations, severity and remediation steps with a generative local model, and you measure how often it hallucinates.

---

## 4. Ground Control to Major AI: Preparing CSOC SOPs for Reliable RAG-Based Decision Support

- **Noah Nyman, Halmstad University, 2026** · Kandidat-uppsats (bachelor)
- [abstract](https://www.uppsatser.se/uppsats/dfd89e2c6a/)

**What it does.** It builds a prototype RAG assistant over four of a SOC's standard operating procedures (SOPs). It compares the original, human-readable SOPs with versions restructured for the machine to read. It is tested on five scenarios for **grounding accuracy, hallucination rate and correctness of the procedure steps**, and analysts were interviewed about triage use.

**Results.** The restructured knowledge base won on every measure. Analysts said it cut the effort of reading through dense documentation, but warned about over-reliance. The conclusion is that RAG quality depends on how the knowledge is structured, not only on retrieval.

**Why it ranks fourth.** Its metrics match your RQ2 almost word for word: correctness, hallucination and useful remediation steps. It is a bachelor-sized template for scoring LLM outputs against a reference.

**What to take.** Its three-part scoring (grounded / hallucinated / steps correct) for your hand-labelled triage set. If you add remediation playbooks to the prompt, structure them for the machine as it recommends. Its point about over-reliance supports your rule that a human approves every action.

---

## 5. How effective are the IDS Snort and the EDR Wazuh at ransomware detection in small businesses? (*Hur effektiv är IDS Snort och EDR Wazuh för ransomware-detektion i småföretag?*)

- **Ilian Ilia, Mälardalen University, 2026** · Uppsats för yrkesexamina på grundnivå (first-cycle professional degree, bachelor level)
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-75828) · [abstract](https://www.uppsatser.se/uppsats/745eda2f4f/)

**What it does.** A controlled experiment in a virtual network that imitates a small company. It runs an attack chain (reconnaissance, intrusion attempts, ransomware-like behaviour) against Snort and **Wazuh**, with **default versus enhanced configuration**.

**Results.** Snort caught early network attacks (TCP and UDP scans) even with its basic settings. Both tools missed most later stages: brute force, payload delivery and simulated ransomware execution. Combining them added complexity without improving detection.

**Why it ranks fifth.** It is a bachelor-level measurement of **Wazuh with little configuration**, which is your baseline (RQ3). Its results tell you which techniques Wazuh's default rules will likely miss.

**What to take.** Its default-versus-enhanced comparison. Consider reporting Wazuh both "out of the box" and "lightly tuned", so your comparison is fair. Also its attack-stage-by-stage results table.

---

## Runners-up (all confirmed bachelor)

| Thesis | Why useful | Why not top 5 |
|---|---|---|
| Norris & Sabit, *NIDS Alert Classification with a CatBoost Classifier* (Linnaeus University, 2026) [abstract](https://www.uppsatser.se/uppsats/e374db2aaa/) | Lightweight ML triage built into a **Suricata** pipeline to fight alert fatigue (aimed at SMEs). It suppressed 98.9% of benign alerts with 99.0% recall, at under 1 ms per flow and 69 MB of RAM | Supervised ML on CIC-IDS2017, not an LLM; network alerts only |
| Akbari, *Log analysis and visualisation for proactive incident management: SIEM dashboard and automated alerts in Elastic Stack* (Mid Sweden University, 2026) [abstract](https://www.uppsatser.se/uppsats/8e85b9a209/) | A real deployment at an energy company (about 50 GB of logs a day): DSR method, 8 alert rules, brute-force and Kerberos detection, Teams notifications | Elastic configuration, not rules-as-code; no baseline |
| Strömberg, *SIEM: practical implementation of a security system* (Mid Sweden University, 2020) [abstract](https://www.uppsatser.se/uppsats/893ad336cd/) | A SIEM built from scratch in Python and Node.js with PostgreSQL storage, close to your own build | No evaluation reported |
| Jepsson & Tillman, *Operational cybersecurity: pros and cons of AI tools* (Luleå, 2023) [abstract](https://www.uppsatser.se/uppsats/03627fc17d/) | Expert interviews on AI across the NIST incident-handling steps. Benefits: fewer false positives, less analyst load. Risks: explainability, legal, input quality | Qualitative pre-study, no system |
| Schoenherr, Sandberg & Klackensjö, *IT Security in SMEs: SOC-functions Prioritization* (Jönköping, 2026) [abstract](https://www.uppsatser.se/uppsats/966ad880df/) | 9 interviews; EDR with automated response and phishing detection are the first SOC functions SMEs need | Qualitative; useful only for motivation |

---

## Source-by-source log

| # | Source | Result |
|---|---|---|
| 1 | ETH Zurich Research Collection | Blocks automated reading. Indexed search found no SIEM or SOC student theses; ETH mostly publishes PhD theses there. |
| 2 | EPFL Infoscience | Blocks automated reading. Only PhD work, papers and one unrelated master's thesis. |
| 3 | TU Delft Repository | Bachelor theses exist but are off-topic (e.g. alert-driven attack graphs, Constantinescu 2023). The closest match, the DeepCASE thesis, is a master's. |
| 4 | KTH DiVA | All top 5 come from here. #1 and #3 are KTH itself. Degree levels were checked through the uppsatser.se mirror of DiVA records. |
| 5 | TUM mediaTUM | Blocks automated reading. Only PhD dissertations on intrusion detection. |
| 6 | DART-Europe | Closed permanently on 3 Feb 2025 ([UCL notice](https://www.ucl.ac.uk/library/dart-europe-e-theses-portal-has-closed-down)). |
| 7 | EThOS | Back online, but holds only UK PhD theses, so no bachelor theses; its search also failed to load for me. |
| 8 | OATD | Its search returned an error. Indexed records showed nothing at bachelor level. |
| 9 | ResearchGate | Only papers, no bachelor theses. |
| 10 | Google Scholar | Blocks automated access. I used OpenAlex and web search instead; they only surfaced master's theses (NCI, Turku), now excluded. |

Some OpenAlex queries were refused by rate limiting (HTTP 429), and BASE blocked access with a bot check. The bachelor-level check relies on the DiVA level shown on uppsatser.se, which I read directly for each listed thesis.

## Mapping to your research questions

- **RQ1 (detection quality with minimal setup):** #1, #2, #5
- **RQ2 (LLM triage value):** #3, #4, plus Norris & Sabit for triage without an LLM
- **RQ3 (ATT&CK coverage vs Wazuh):** #5 (what Wazuh misses), #3 (ATT&CK mapping), #2 (how to compare against existing SIEMs)
