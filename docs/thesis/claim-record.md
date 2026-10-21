# Claim record

Status: **draft**. The wording of the claim is fixed before the final runs and
updated only through a dated entry in the change log below. The claim is
written backwards from the evidence: it says only what the planned
measurements in `research-design.md` can support.

## Strongest supported claim (if every must criterion is met)

In a lab with simulated attacks, a Sigma-based prototype with local LLM triage
meets F1-F8 on this attack matrix, on the stated hardware and with the stated
model. It is not shown to work in a real organisation or to replace a SOC.

Scope words that must stay in the claim: *lab*, *simulated attacks*, *this
attack matrix*, *this hardware*, *this model*.

## Weaker fallback (if some must criteria fail)

The prototype meets the criteria listed as met in the scorecard and fails the
others. The thesis reports which criteria failed, by how much, and what the
data suggests about why. For RQ2, a null result for H1 or H2 is reported as
"no measurable effect for this model and this alert set".

## Rejected stronger claim

"Organisations without a dedicated SOC can replace a commercial SIEM or a SOC
with this system." Rejected because the evidence is lab-only, covers about 12
techniques, uses one model, and measures no real staff or real traffic.

Also rejected: any general ATT&CK coverage figure, and any statement that the
prototype detects better than Wazuh outside the held-out technique set.

## Residual uncertainty

- Simulated attacks and a generated benign run may not resemble a real network.
- The author wrote the rules, playbooks and reference labels.
- About 80 alerts, one 7-8B model, one second rater on 20% of outputs.
- Wazuh tuning is limited to one hour.
- Thresholds are the author's, approved by the supervisor (to be recorded).

## What would reopen the claim

- A must criterion is missed by a margin larger than run-to-run variation.
- Held-out detection is much lower than development-set detection, which
  would indicate the rules were fitted to the tests.
- Rater agreement (Cohen's kappa) is too low for hallucination to be trusted.
- Reference labels or playbooks are found to be copied from each other.

## Change log

| Date | Change | Reason | Approved by |
|---|---|---|---|
| 2026-10-21 | First draft | Defendability review against the Student's Guide | pending |
