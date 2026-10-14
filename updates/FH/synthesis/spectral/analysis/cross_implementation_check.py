"""Compare the independent global matrix with the safe-copy source recursion."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPLAY = HERE.parent / "replay" / "producer_copy"
sys.path.insert(0, str(HERE))
from independent_checks import SEQ_A, SEQ_B, rp_transfer  # noqa: E402

spec = importlib.util.spec_from_file_location("producer_optical_model", REPLAY / "optical_model.py")
if spec is None or spec.loader is None:
    raise RuntimeError("could not load the frozen safe-copy optical model")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)

rows = np.genfromtxt(REPLAY / "reference_spectrum.csv", delimiter=",", names=True)
nu_grid = rows["wavenumber_cm1"]
q_csv = 2e7
freq_diffs = []
for name, seq in (("A", SEQ_A), ("B", SEQ_B)):
    source = producer.rp(nu_grid, q_csv, seq)
    independent = np.array([rp_transfer(float(nu), q_csv, seq) for nu in nu_grid])
    delta = np.abs(source - independent)
    rel = delta / np.maximum(np.maximum(np.abs(source), np.abs(independent)), 1e-300)
    freq_diffs.append({
        "sequence": name,
        "points": int(len(nu_grid)),
        "max_abs_complex_reflection_difference": float(delta.max()),
        "max_relative_complex_reflection_difference": float(rel.max()),
    })

q_grid = np.geomspace(1.2e6, 4e8, 801)
static_diffs = []
for ideal in (False, True):
    for name, seq in (("A", SEQ_A), ("B", SEQ_B)):
        source = producer.rp(0, q_grid, seq, ideal=ideal)
        independent = rp_transfer(0, q_grid, seq, ideal_mass_only=ideal)
        delta = np.abs(source - independent)
        rel = delta / np.maximum(np.maximum(np.abs(source), np.abs(independent)), 1e-300)
        static_diffs.append({
            "ideal_mass_match": ideal,
            "sequence": name,
            "points": int(len(q_grid)),
            "max_abs_complex_reflection_difference": float(delta.max()),
            "max_relative_complex_reflection_difference": float(rel.max()),
        })

out = {
    "status": "Independent global amplitude matrix compared with unchanged safe-copy source recursion.",
    "frequency_spectrum": {"q_per_m": q_csv, "rows": freq_diffs},
    "static_q_sweep": {"q_min_per_m": float(q_grid.min()), "q_max_per_m": float(q_grid.max()), "rows": static_diffs},
}
(HERE / "cross_implementation_results.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
