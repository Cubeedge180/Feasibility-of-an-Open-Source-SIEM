> Literature search notes (2026-10), copied from the project library. Early titles mention SMEs;
> the SME focus was dropped in decision D3.

# Related theses: top 5 master's theses closest to your thesis

Searched 2026-10-16. Master's level only. Ranked against your current title, *Feasibility of an Open-Source SIEM: A Comparative Study with Wazuh and Local LLM Triage* (RQ1 feasibility vs Wazuh, RQ2 local-LLM triage with a hallucination check, plus Sigma/ATT&CK coverage).

**How the level was checked.** For DiVA theses I read the line "Detta är en Master-uppsats …" on each record's uppsatser.se mirror. #4 is a Swedish civilingenjör degree project ("yrkesexamen på avancerad nivå"). That is second-cycle work, the same level as a master's thesis, but its label is not "Master". The Concordia thesis is a Master of Applied Science (stated in the record and the file name).

Bachelor-level and PhD theses are excluded. The bachelor list is still in [related-theses-top5.md](related-theses-top5.md).

---

## 1. Governance Constrained AI for SOC Alert Triage: Design and Evaluation of a Hybrid Deterministic–LLM Architecture

- **Friday Uchechukwu Uzodinma, Luleå University of Technology, 2026** · Master-uppsats
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-119721) · [abstract](https://www.uppsatser.se/uppsats/2ceecc3590/)

**What it does.** Wazuh does deterministic detection. A **local Mistral model in Ollama** reasons over the alerts. A Python governance layer limits how much the LLM can change escalation, using three mechanisms: *Policy Floors* (a minimum severity set by the rule), *Context Ceilings* and *Bounded AI Adjustment*. The method is Design Science Research.

**Evaluation.** 40 participants rated 7 synthetic SOC scenarios, giving 280 severity ratings. The system ran 30 trials per scenario under noisy, adversarial and multi-stage conditions. Human agreement was weak (Krippendorff's ordinal α = 0.611). The governance layer stepped in on 26 of 30 trials, with a mean Reasoning Divergence Score of 2.97. No single architecture was consistently closest to the human ratings. The author makes no claim of general superiority. The contribution is an auditable way to bound disagreement between rules and the LLM.

**Why first.** It is the same stack as yours (Wazuh plus local Ollama, no data leaving the network) and the same principle (the LLM is bounded and humans keep control).

**What to take.** Policy floors as a citable precedent for your schema-validated LLM output. Its weak human agreement means you should report inter-rater agreement on your ~80 hand-labelled alerts, or "correct severity" has no stable ground truth.

**How yours differs.** You use Sigma-as-code rather than Wazuh rules, real lab attacks rather than synthetic scenarios, and a pre-registered 2×2 grounding experiment rather than a governance layer.

---

## 2. LLM-assisted SOC Alert Analysis: A Design Space Evaluation of System Variants

- **Hannes Lundberg & Vincent Garbrant, Linköping University, 2026** · Master-uppsats
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-225104) · [abstract](https://www.uppsatser.se/uppsats/101290266c/)

**What it does.** An LLM agent triages SOC alerts with context tools exposed over the Model Context Protocol ("K-MCP"). The tools are based on analyst investigation factors from Kersten et al. The authors vary the prompts, the tool descriptions and how gradually evidence is released.

**Evaluation.** A 76-alert labelled set: benign alerts from their lab plus malicious alerts from the public **MORDOR 2019** dataset. Verdicts are scored with F1, precision and recall. Report quality is scored with **MESSALA**, an LLM-based report evaluator. The best variant reached **F1 0.942 ± 0.028**, against **0.711 ± 0.016** for the base version, over 3 runs. Almost all of the gain came from fewer false positives (12 down to about 1). Both caught 16 of 17 malicious alerts. Removing alert history *helped*: "more context is not always better".

**Why second.** It is the best model for how to run your RQ2 experiment. It varies one context factor at a time, as your 2×2 does, uses repeated runs with a ± spread, and scores the verdict and the explanation separately.

**What to take.** MORDOR as a public source of labelled malicious events, which makes part of your alert set reproducible. Report the ± over repeated runs. Its "context overreach" finding gives a reason to expect that your raw-JSON versus normalised-text factor will matter.

---

## 3. Triggering False Alarms in Computer Networks: Evaluating an IDS's Ability to Accurately Distinguish Attacks from Regular Computer Activity

- **Peter Daniel, KTH EECS, 2025** · Master-uppsats (Swedish title *Framkallande av falsklarm i datornätverk*)
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-369645) · [abstract](https://www.uppsatser.se/uppsats/3978c7db52/)

**What it does.** It studies Living-off-the-Land (LotL) binaries, which admins and attackers both use. The author finds overlapping techniques with **MITRE ATT&CK, LOLBAS and Sigma rules**, plus practitioner interviews and surveys. Benign admin tasks are automated in the CRATE cyber range, and malicious use is emulated with **Atomic Red Team**. Detection is measured with **Snort, Sysmon and Wazuh**.

**Findings.** Benign and malicious use can trigger the *same* signature. Every activity was captured, but telling them apart "required contextual analysis". The author recommends refining the signatures and adding context and anomaly detection.

**Why third.** It is a KTH thesis with almost exactly your toolchain (Sigma, ATT&CK, Atomic Red Team, Sysmon, Wazuh), built around false positives on benign activity.

**What to take.** Scripted admin activity that looks like an attack is a harder benign set than idle lab traffic, so use it in your 24 h benign run. Its "context needed" conclusion is a direct motivation for your LLM triage.

---

## 4. Extending an open-source SIEM platform with automated security testing

- **Simon Danielsson & Anton Melin, Blekinge Institute of Technology, 2026** · Uppsats för yrkesexamina på avancerad nivå (civilingenjör, second-cycle)
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:bth-30335) · [abstract](https://www.uppsatser.se/uppsats/c128a75e85/)

**What it does.** Using Design Science, it compares open-source SIEMs (**Wazuh, Elastic Security, Graylog**). It then extends the chosen one so it runs automated security tests, and compares that against a traditional DevSecOps pipeline using the same tools.

**Evaluation.** It counts the alerts generated and measures **configuration complexity as setup steps and lines of code**, plus interviews. All platforms could integrate external tools. Wazuh was the only one with native endpoint execution at no licence cost. The SIEM route produced the same alerts but needed more configuration. Interviewees found it easier to understand because of the visualisation.

**Why fourth.** It is a feasibility study of open-source SIEMs with Wazuh in the comparison, which is your RQ1 framing.

**What to take.** Setup steps and lines of configuration as an objective measure of effort for your feasibility criteria. Its platform comparison is a citable reason to use Wazuh as the baseline.

---

## 5. Improving SIEM Rules through Transformer-Based Rule Evasion Detection and Attribution

- **Erik Nordström & Hannes Widéen, Linköping University, 2025** · Master-uppsats · also a [Springer paper](https://link.springer.com/chapter/10.1007/978-3-032-33260-8_5)
- [DiVA urn](http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-220130) · [abstract](https://www.uppsatser.se/uppsats/e2af2f4f44/)

**What it does.** It embeds executed PowerShell commands and **Sigma** PowerShell rules with a transformer and compares them with cosine similarity. This finds evasions and identifies which rule was evaded. A random-forest "metamodel" picks the best LLM from a pool to suggest rule fixes.

**Results.** At least **24% of the 2025 Sigma rules could be evaded**. It caught 71% of hand-made evasions at under 1% false positives, and linked 98% of them to the right rule, which beats the earlier AMIDES system. 70% of rules were updated. In analyst feedback, 31% of the suggested fixes could replace the original rule with small edits.

**Why fifth.** It is the closest master's thesis on Sigma rule quality. It sets the limits on any "coverage %" claim you make from Sigma rules.

**What to take.** Cite it in threats to validity: a rule tagged with a technique is not the same as robust detection of that technique. That supports your dev/held-out technique split.

---

## Runners-up (master's level)

| Thesis | Source | Why useful | Why not top 5 |
|---|---|---|---|
| Ghaffarzadegan, *Automating Detection Lifecycle for APT Hunting: From CTI-Derived Sigma Rules to Infrastructure-Aware Rule Variants* (Concordia, MASc, 2026) [pdf](https://spectrum.library.concordia.ca/id/eprint/997106/1/Ghaffarzadegan_MA_S2026.pdf) | Google Scholar / OATD route | Detection-as-code with LLMs: AutoSigma turns CTI reports into Sigma rules (grounded in the existing Sigma repository, with an LLM-as-judge), and ARMS generates rule variants with RAG | Rule *generation*, not a SIEM; the abstract gives no numbers. I could not open the PDF (robots block) |
| Dengg, *Large language models for security operations: evaluating automated alert triage in cloud environments* (JKU Linz, 2025) [urn](https://resolver.obvsg.at/urn:nbn:at:at-ubl:1-94385) | Google Scholar / OATD route | A ReAct agent (GPT-4o, Claude) on 28 AWS GuardDuty findings, compared with human experts: 60.7% vs 39.3% accuracy. Removing tools cut accuracy by 71% | Cloud LLMs; the degree level was not stated in the record |
| Dubuc, *A Real-time Log Correlation System for SIEM* (KTH, 2021) [abstract](https://www.essays.se/essay/aa4e0f13ec/) | DiVA | A correlation engine for SIEM, useful for your detect/ module | Older; no LLM, no Sigma |
| Thorarensen, *A Performance Analysis of Intrusion Detection with Snort and Security Information Management* (Linköping, 2021) [abstract](https://www.essays.se/essay/b7770454d3/) | DiVA | Performance and throughput measurement of IDS plus SIEM | Network IDS only |
| Shinde, *Evaluating SIEM Solutions for SMEs* (NCI, MSc, 2025) [pdf](https://norma.ncirl.ie/9600/1/parthmadhukarshinde.pdf) | Google Scholar route | Compares Wazuh, ELK, Huntress and LimaCharlie on MTTD, MTTR, CPU, RAM and agent size | Weak attack set (mostly the EICAR test file) and inconsistent VM specs |
| Ramdan, *Evaluating DeepCASE in a Multi-detection-Systems Setting* (TU Delft, MSc, 2024) [record](https://repository.tudelft.nl/record/uuid:60b24b4a-d50e-402d-852f-89d425e9d232) | TU Delft | Alert workload cut by 87–96% with 0% false negatives; argues false negatives and workload are the metrics that matter | ML alert filtering, no LLM |

## Source-by-source (master's level)

| Source | Result |
|---|---|
| ETH Research Collection, EPFL Infoscience, TUM mediaTUM | They block automated reading, and indexed search found no master's thesis on SIEM, Sigma or LLM triage |
| TU Delft | DeepCASE (runner-up); nothing closer |
| KTH DiVA | Top 5 and three runners-up. #3 is KTH itself |
| DART-Europe | Closed on 3 Feb 2025 |
| EThOS | Holds PhD theses only |
| OATD, ResearchGate, Google Scholar | Searched via OpenAlex and web search: Concordia, JKU and NCI (runners-up). Scholar and OATD block direct access |
