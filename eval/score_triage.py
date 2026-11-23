"""Score the 2 x 2 triage experiment from the blinded ratings.

Usage: python -m eval.score_triage <key.csv> <ratings.csv> <alerts.csv> <out.json>

<alerts.csv> has columns alert_id,technique: the one ATT&CK technique whose
playbook and rule each alert belongs to (benign alerts: the technique of the
rule that fired), taken from the reference labels.

Implements the analysis fixed in docs/thesis/research-design.md, section 4.5:

- For each alert and measure, the main effect of a factor is the mean over the
  two cells with the factor minus the mean over the two cells without it.
  Normalised text: (C3 + C4) / 2 - (C1 + C2) / 2.
  Playbook:        (C2 + C4) / 2 - (C1 + C3) / 2.
- H1: normalised text lowers the hallucination rate (one-sided, "less").
- H2: playbooks raise the share of correct steps (one-sided, "greater").
- Test: Wilcoxon signed-rank on the per-alert differences, zero differences
  dropped. Reported with the mean difference, a bootstrap 95% CI and the
  matched-pairs rank-biserial correlation as effect size.
- Every other measure x factor pair is reported two-sided as exploratory.
- Clustering (section 4.5): variants of one technique are correlated, so each
  test is repeated on per-technique mean differences, with a bootstrap CI that
  resamples whole techniques. Where the two verdicts disagree, the clustered
  one is the one the claim relies on (claim_supported).
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, wilcoxon

MEASURES = {
    "grounded": "fraction",
    "hallucinated": "binary",
    "steps_correct": "fraction",
    "severity_agree": "binary",
    "unsafe": "binary",
}
FACTORS = {
    "normalised_text": (("C3", "C4"), ("C1", "C2")),
    "playbook": (("C2", "C4"), ("C1", "C3")),
}
HYPOTHESES = {
    "H1": ("normalised_text", "hallucinated", "less"),
    "H2": ("playbook", "steps_correct", "greater"),
}
ALPHA = 0.05
BOOTSTRAP_SAMPLES = 10_000
SEED = 20261014


def load(key_path: Path, ratings_path: Path) -> dict[str, dict[str, dict[str, float]]]:
    """Ratings as {alert_id: {condition: {measure: value}}}; raises on bad input."""
    with key_path.open(encoding="utf-8", newline="") as f:
        key = {row["output_id"]: row for row in csv.DictReader(f)}
    with ratings_path.open(encoding="utf-8", newline="") as f:
        ratings = list(csv.DictReader(f))

    data: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
    for row in ratings:
        output_id = row["output_id"]
        if output_id not in key:
            raise ValueError(f"{output_id} is not in the key")
        values = {}
        for measure, kind in MEASURES.items():
            raw = (row.get(measure) or "").strip()
            if not raw:
                raise ValueError(f"{output_id}: {measure} is not rated")
            value = float(raw)
            if not 0 <= value <= 1 or (kind == "binary" and value not in (0, 1)):
                raise ValueError(f"{output_id}: {measure}={raw} is out of range")
            values[measure] = value
        k = key[output_id]
        if k["condition"] in data[k["alert_id"]]:
            raise ValueError(f"{k['alert_id']} has two ratings for {k['condition']}")
        data[k["alert_id"]][k["condition"]] = values

    unrated = set(key) - {row["output_id"] for row in ratings}
    if unrated:
        raise ValueError(
            f"{len(unrated)} output(s) in the key are not rated: {sorted(unrated)[:5]}"
        )

    for alert_id, cells in data.items():
        missing = {"C1", "C2", "C3", "C4"} - set(cells)
        if missing:
            raise ValueError(f"{alert_id} has no rating for {sorted(missing)}")
    return dict(data)


def load_techniques(path: Path, data: dict) -> dict[str, str]:
    """{alert_id: technique} for every rated alert; raises on a gap or a duplicate."""
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    techniques: dict[str, str] = {}
    for row in rows:
        alert_id, technique = row["alert_id"].strip(), (row.get("technique") or "").strip()
        if alert_id in techniques:
            raise ValueError(f"{alert_id} is listed twice in {path.name}")
        techniques[alert_id] = technique
    missing = sorted(a for a in data if not techniques.get(a))
    if missing:
        raise ValueError(f"{len(missing)} rated alert(s) have no technique: {missing[:5]}")
    return {a: techniques[a] for a in data}


def differences(data, factor: str, measure: str) -> np.ndarray:
    with_, without = FACTORS[factor]
    return np.array(
        [
            np.mean([cells[c][measure] for c in with_])
            - np.mean([cells[c][measure] for c in without])
            for _, cells in sorted(data.items())
        ]
    )


def _signed_rank(d: np.ndarray, alternative: str) -> dict:
    """Wilcoxon signed-rank with zero differences dropped, plus rank-biserial r."""
    nonzero = d[d != 0]
    if len(nonzero) == 0:
        p, r = 1.0, 0.0
    else:
        p = float(wilcoxon(nonzero, alternative=alternative).pvalue)
        ranks = rankdata(np.abs(nonzero))
        r = float((ranks[nonzero > 0].sum() - ranks[nonzero < 0].sum()) / ranks.sum())
    return {"n_nonzero": int(len(nonzero)), "p_value": p, "rank_biserial": r}


def _ci95(boot: np.ndarray) -> list[float]:
    return [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))]


def test(d: np.ndarray, alternative: str) -> dict:
    rng = np.random.default_rng(SEED)
    boot = rng.choice(d, size=(BOOTSTRAP_SAMPLES, len(d)), replace=True).mean(axis=1)
    return {
        "n_alerts": len(d),
        "mean_difference": float(d.mean()),
        "ci95": _ci95(boot),
        "alternative": alternative,
    } | _signed_rank(d, alternative)


def clustered_test(d: np.ndarray, techniques, alternative: str) -> dict:
    """The same test on per-technique means, with a technique-clustered bootstrap CI.

    The CI is for the per-alert mean difference, but each resample draws whole
    techniques (with all their alerts), so correlated variants count once.
    """
    labels, index = np.unique(np.asarray(techniques), return_inverse=True)
    sums = np.bincount(index, weights=d)
    counts = np.bincount(index)
    rng = np.random.default_rng(SEED)
    draw = rng.integers(0, len(labels), size=(BOOTSTRAP_SAMPLES, len(labels)))
    boot = sums[draw].sum(axis=1) / counts[draw].sum(axis=1)
    return {
        "n_techniques": len(labels),
        "mean_difference": float(d.mean()),
        "ci95": _ci95(boot),
        "alternative": alternative,
    } | _signed_rank(sums / counts, alternative)


def _with_clustered(d: np.ndarray, techniques, alternative: str) -> dict:
    result = test(d, alternative)
    clustered = clustered_test(d, techniques, alternative)
    clustered["supported"] = clustered["p_value"] < ALPHA
    result["supported"] = result["p_value"] < ALPHA
    result["clustered"] = clustered
    result["agree"] = result["supported"] == clustered["supported"]
    return result


def score(data, techniques: dict[str, str]) -> dict:
    cells = {
        c: {m: float(np.mean([a[c][m] for a in data.values()])) for m in MEASURES}
        for c in ("C1", "C2", "C3", "C4")
    }
    order = [techniques[a] for a in sorted(data)]  # same order as differences()
    hypotheses = {}
    for name, (factor, measure, alternative) in HYPOTHESES.items():
        result = _with_clustered(differences(data, factor, measure), order, alternative)
        result |= {
            "factor": factor,
            "measure": measure,
            "claim_supported": result["clustered"]["supported"],
        }
        hypotheses[name] = result
    primary = {(f, m) for f, m, _ in HYPOTHESES.values()}
    exploratory = [
        {"factor": f, "measure": m} | _with_clustered(differences(data, f, m), order, "two-sided")
        for f in FACTORS
        for m in MEASURES
        if (f, m) not in primary
    ]
    return {
        "alpha": ALPHA,
        "cell_means": cells,
        "hypotheses": hypotheses,
        "exploratory": exploratory,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.splitlines()[2])
        return 2
    data = load(Path(argv[0]), Path(argv[1]))
    result = score(data, load_techniques(Path(argv[2]), data))
    Path(argv[3]).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for name, h in result["hypotheses"].items():
        c = h["clustered"]
        verdict = "supported" if h["claim_supported"] else "not supported"
        print(
            f"{name} ({h['factor']} -> {h['measure']}): mean diff {h['mean_difference']:+.3f}, "
            f"per-alert p={h['p_value']:.4f}, clustered p={c['p_value']:.4f} "
            f"({c['n_techniques']} techniques) -> {verdict}"
            + ("" if h["agree"] else " [per-alert and clustered disagree; claim uses clustered]")
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
