import csv
import json
import random

import numpy as np
import pytest

from eval.blind import RATING_COLUMNS, blind
from eval.score_triage import clustered_test, load, load_techniques, score
from eval.score_triage import test as per_alert_test


def _records(n_alerts=40):
    return [
        {"alert_id": f"A{a}", "condition": c, "run": run, "output": {"n": a}}
        for a in range(n_alerts)
        for c in ("C1", "C2", "C3", "C4")
        for run in (1, 2)
    ]


def test_blind_hides_condition_and_keeps_one_run():
    blinded, key = blind(_records(), seed=1, run=1)
    assert len(blinded) == 160
    assert all(set(b) == {"output_id", "alert_id", "output"} for b in blinded)
    assert {k["run"] for k in key} == {1}
    assert len({b["output_id"] for b in blinded}) == 160


def test_blind_hides_playbook_step_ids():
    output = {
        "steps": [{"action": "Disable the account.", "playbook_step_id": "T1685.005-3"}],
        "proposed_action": {
            "response_action": "disable_account",
            "playbook_step_id": "T1685.005-3",
        },
    }
    records = [{"alert_id": "A1", "condition": "C4", "run": 1, "output": output}]
    blinded, _ = blind(records, seed=1, run=1)
    assert "playbook_step_id" not in json.dumps(blinded)
    assert blinded[0]["output"]["steps"][0]["action"] == "Disable the account."
    assert output["steps"][0]["playbook_step_id"] == "T1685.005-3"  # input left intact


def test_blind_keeps_unparseable_output():
    blinded, _ = blind([{"alert_id": "A1", "condition": "C1", "run": 1, "output": None}], 1, 1)
    assert blinded[0]["output"] is None


def _write(tmp_path, effect: bool):
    _, key = blind(_records(), seed=1, run=1)
    rng = random.Random(2)
    with (tmp_path / "key.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["output_id", "alert_id", "condition", "run"])
        w.writeheader()
        w.writerows(key)
    with (tmp_path / "ratings.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["output_id", *RATING_COLUMNS])
        for k in key:
            normalised = k["condition"] in ("C3", "C4")
            playbook = k["condition"] in ("C2", "C4")
            p_halluc = 0.1 if effect and normalised else 0.5
            steps = 0.9 if effect and playbook else 0.5
            w.writerow([k["output_id"], 1, int(rng.random() < p_halluc), steps, 1, 0])
    with (tmp_path / "alerts.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["alert_id", "technique"])
        w.writerows([f"A{a}", f"T{a % 8}"] for a in range(40))
    data = load(tmp_path / "key.csv", tmp_path / "ratings.csv")
    return data, load_techniques(tmp_path / "alerts.csv", data)


def test_effects_are_detected(tmp_path):
    result = score(*_write(tmp_path, effect=True))
    assert result["hypotheses"]["H1"]["supported"]
    assert result["hypotheses"]["H1"]["mean_difference"] < 0
    assert result["hypotheses"]["H2"]["supported"]


def test_no_effect_is_not_supported(tmp_path):
    result = score(*_write(tmp_path, effect=False))
    assert not result["hypotheses"]["H2"]["supported"]
    assert result["hypotheses"]["H2"]["p_value"] == 1.0


def test_missing_rating_is_an_error(tmp_path):
    _write(tmp_path, effect=False)
    rows = (tmp_path / "ratings.csv").read_text().splitlines()
    (tmp_path / "ratings.csv").write_text("\n".join(rows[:-1]) + "\n")
    with pytest.raises(ValueError, match="not rated"):
        load(tmp_path / "key.csv", tmp_path / "ratings.csv")


def test_alert_missing_from_ratings_is_an_error(tmp_path):
    _write(tmp_path, effect=False)
    with (tmp_path / "key.csv").open(newline="") as f:
        key = list(csv.DictReader(f))
    dropped = {k["output_id"] for k in key if k["alert_id"] == key[0]["alert_id"]}
    rows = (tmp_path / "ratings.csv").read_text().splitlines()
    kept = [r for r in rows if r.split(",")[0] not in dropped]
    (tmp_path / "ratings.csv").write_text("\n".join(kept) + "\n")
    with pytest.raises(ValueError, match="not rated"):
        load(tmp_path / "key.csv", tmp_path / "ratings.csv")


def test_clustered_ci_is_wider_when_variants_of_a_technique_are_identical():
    # 8 techniques x 5 identical variants: only 8 independent values, not 40.
    d = np.repeat([-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2], 5)
    techniques = np.repeat([f"T{i}" for i in range(8)], 5)
    per_alert_ci = np.diff(per_alert_test(d, "less")["ci95"])[0]
    clustered = clustered_test(d, techniques, "less")
    assert np.diff(clustered["ci95"])[0] > 1.5 * per_alert_ci


def test_clustered_wilcoxon_uses_one_value_per_technique():
    d = np.repeat([-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2], 5)
    techniques = np.repeat([f"T{i}" for i in range(8)], 5)
    clustered = clustered_test(d, techniques, "less")
    assert clustered["n_techniques"] == 8
    assert clustered["n_nonzero"] == 7


def test_alert_missing_from_alerts_csv_is_an_error(tmp_path):
    data, _ = _write(tmp_path, effect=False)
    rows = (tmp_path / "alerts.csv").read_text().splitlines()
    kept = [r for r in rows if not r.startswith("A3,")]
    (tmp_path / "alerts.csv").write_text("\n".join(kept) + "\n")
    with pytest.raises(ValueError, match="A3"):
        load_techniques(tmp_path / "alerts.csv", data)
