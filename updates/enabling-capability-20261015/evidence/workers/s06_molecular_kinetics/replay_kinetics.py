"""Independent molecular-rate replay using acquired CLN025 trajectory records.

Default inputs: published time-ordered state labels, not fitted force errors.
The safe reader permits only inert data containers and NumPy reconstruction.
No downloaded scientific code or pickle callbacks are executed.
"""
from pathlib import Path
import json
import pickle
import time
import numpy as np

HERE = Path(__file__).resolve().parent
DT_US = 1e-4  # 100 ps; published setting, checked against acquired XTC prefix.


class LegacyTrajectory:
    pass


class DataReader(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "utils" and name == "PathEnsembleTrajectory":
            return LegacyTrajectory
        if module in {"numpy", "numpy.core.multiarray", "numpy._core.multiarray"} and name in {
            "ndarray", "dtype", "_reconstruct", "scalar"
        }:
            return super().find_class(module, name)
        raise ValueError(f"Unsupported pickle global {module}.{name}")


def load_reference():
    with (HERE / "acquired/chignolin/reference/pe.h5").open("rb") as source:
        objects = DataReader(source).load()
    result = []
    for obj in objects:
        fields = vars(obj)
        get = lambda name: fields[f"_PathEnsembleTrajectory__{name}"]
        states = get("states")
        assert set(np.unique(states)) <= {"A", "B", "R"}
        assert len(states) == get("length") == len(get("committor_values"))
        assert np.all(get("weights") == 1)
        result.append({"name": get("file_name"), "states": states,
                       "committor": get("committor_values")})
    return result


def skeleton(states, stride=1):
    """First arrival in each alternating basin; R is the transition region."""
    sampled = states[::stride]
    indices = np.flatnonzero(sampled != "R")
    labels = sampled[indices]
    changes = np.r_[True, labels[1:] != labels[:-1]]
    return indices[changes] * stride, labels[changes]


def complete_intervals(records, stride=1, include_initial=False):
    ab, ba, events = [], [], []
    for record in records:
        indices, labels = skeleton(record["states"], stride)
        # The first observed basin may be occupied at initialization. Discard
        # its residence; start clocks at the first actual A<->B arrival.
        begin = 0 if include_initial else 1
        durations = np.diff(indices[begin:]) * DT_US
        ab.extend(durations[labels[begin+1:] == "B"])
        ba.extend(durations[labels[begin+1:] == "A"])
        events.append({"name": record["name"], "nframes": len(record["states"]),
                       "arrivals_frame": indices.tolist(), "basins": labels.tolist(),
                       "n_observed_switches": len(indices)-1})
    return np.array(ab), np.array(ba), events


def old_source_pairing(records):
    """Reimplement old production.ipynb cell59's additional pair truncation."""
    ab, ba = [], []
    for record in records:
        indices, labels = skeleton(record["states"])
        # The two physical transition directions are paired, and surplus
        # terminal transitions are omitted in the original 2023 convention.
        actual = indices[1:]
        destinations = labels[1:]
        j_ab = actual[destinations == "B"] * DT_US
        j_ba = actual[destinations == "A"] * DT_US
        count = min(len(j_ab), len(j_ba))
        j_ab, j_ba = j_ab[:count], j_ba[:count]
        if j_ab[0] < j_ba[0]:
            ab.extend(j_ab[1:] - j_ba[:-1])
            ba.extend(j_ba - j_ab)
        else:
            ab.extend(j_ab - j_ba)
            ba.extend(j_ba[1:] - j_ab[:-1])
    return np.array(ab), np.array(ba)


def summarize(intervals, rng):
    n = len(intervals)
    boot = 1 / np.mean(rng.choice(intervals, size=(10000, n), replace=True), axis=1)
    return {"n_complete_intervals": n, "total_complete_exposure_us": float(intervals.sum()),
            "mfpt_us": float(intervals.mean()), "rate_per_us": float(1/intervals.mean()),
            "empirical_iid_bootstrap_95_percent": np.quantile(boot, [.025, .975]).tolist(),
            "bootstrap_scope": "Resampled observed intervals; independence/tail adequacy not certified."}


def parse_incumbent_logs():
    """Extract source-reported controls; these are not independent reruns."""
    import re
    text = (HERE / "sources/14922168_notebook_cell73_stdout.txt").read_text()
    current, budget, rows = None, None, []
    for line in text.splitlines():
        match = re.search(r"loading AIMMD (\w+) run", line)
        if match:
            current = match[1]
        match = re.search(r"computational budget: ([0-9.eE+-]+)", line)
        if match:
            budget = float(match[1])
        match = re.search(r"Step\s+(\d+):\s+nT\s*=\s*(\d+)\s+kAB\s*=\s*([0-9.eE+-]+)\s+\(/ref\s*=\s*([0-9.eE+-]+)\),\s+kBA\s*=\s*([0-9.eE+-]+)\s+\(/ref\s*=\s*([0-9.eE+-]+)\)", line)
        if match and current:
            rows.append({"run": current, "requested_budget_us": budget, "step": int(match[1]),
                         "transition_paths": int(match[2]), "kAB_per_us": float(match[3]),
                         "kAB_over_source_ref": float(match[4]), "kBA_per_us": float(match[5]),
                         "kBA_over_source_ref": float(match[6]),
                         "status": "SOURCE_REPORTED_NOTEBOOK_OUTPUT_NOT_REPLAYED"})
    return rows


def main():
    started = time.perf_counter()
    records = load_reference()
    rng = np.random.default_rng(20261015)
    ab, ba, events = complete_intervals(records)
    old_ab, old_ba = old_source_pairing(records)
    stored_ab = np.load(HERE / "acquired/chignolin/reference/kAB.npy")[0]
    stored_ba = np.load(HERE / "acquired/chignolin/reference/kBA.npy")[0]
    assert np.isclose(1/old_ab.mean(), stored_ab, rtol=1e-12)
    assert np.isclose(1/old_ba.mean(), stored_ba, rtol=1e-12)
    # Event skeleton retains precisely the intervals used by the estimator.
    reconstructed = []
    for event in events:
        s = np.full(event["nframes"], "R")
        s[np.array(event["arrivals_frame"])] = event["basins"]
        reconstructed.append({"name": event["name"], "states": s})
    ab2, ba2, _ = complete_intervals(reconstructed)
    assert np.array_equal(ab, ab2) and np.array_equal(ba, ba2)
    stride_results = []
    for stride in [1, 10, 100, 1000, 10000]:
        a, b, ev = complete_intervals(records, stride)
        stride_results.append({"frame_interval_ns": DT_US*stride*1000,
                               "observed_switches": sum(e["n_observed_switches"] for e in ev),
                               "AB_intervals": len(a), "BA_intervals": len(b),
                               "kAB_per_us": float(1/a.mean()), "kBA_per_us": float(1/b.mean())})
    result = {"scientific_target": "CLN025 folding/unfolding under the supplied CHARMM22star/TIP3 MD model at 340K",
              "truth_scope": "MD benchmark. Not experimental rates, force-field validity, or novelty.",
              "frame_interval_us": DT_US, "trajectories": len(records),
              "frames": sum(len(r["states"]) for r in records),
              "acquired_duration_us": sum((len(r["states"])-1)*DT_US for r in records),
              "observed_switches": sum(e["n_observed_switches"] for e in events),
              "complete_alternating_arrival_convention": {"A_to_B_unfolding": summarize(ab,rng),
                                                          "B_to_A_folding": summarize(ba,rng)},
              "old_source_pair_truncation_replay": {"A_to_B_unfolding": summarize(old_ab,rng),
                                                    "B_to_A_folding": summarize(old_ba,rng),
                                                    "stored_kAB_per_us": float(stored_ab),
                                                    "stored_kBA_per_us": float(stored_ba)},
              "stride_controls": stride_results,
              "event_skeleton_exact_finite_record_replay": True,
              "new_physical_simulation_us": 0, "experimental_measurements": 0,
              "compute_seconds": time.perf_counter()-started,
              "inference_tokens": "UNKNOWN", "inference_cost": "UNKNOWN", "energy": "UNKNOWN"}
    (HERE / "KINETIC_REPLAY.json").write_text(json.dumps(result,indent=2))
    (HERE / "EVENT_SKELETON.json").write_text(json.dumps({"dt_us":DT_US,"records":events},indent=2))
    (HERE / "SOURCE_REPORTED_INCUMBENT_CONTROLS.json").write_text(json.dumps(parse_incumbent_logs(),indent=2))
    arrays = {}
    for i, r in enumerate(records):
        arrays[f"states_{i}"] = r["states"]
        arrays[f"committor_{i}"] = r["committor"]
    np.savez_compressed(HERE / "reference_arrays.npz", **arrays)
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
