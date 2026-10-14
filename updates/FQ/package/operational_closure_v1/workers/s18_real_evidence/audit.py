#!/usr/bin/env python3
"""Audit measured SMA damper hysteresis in Zenodo record 17296336.

Uses only the Python standard library. The source ZIP is downloaded separately
from the URL recorded in REPORT.md; no synthetic observations enter the audit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ZIP_NAME = "Data_v1.0.0.zip"
ZIP_MD5 = "da06b1056528e8429e7f64e3019cb17b"
PREFIX = "Data.v1.0.0/02_SMAWD/"
FILES = {
    "8w_20mm_0p5Hz": "02_8wires_sin20mm_0p5Hz.csv",
    "8w_40mm_0p5Hz": "05_8wires_sin40mm_0p5Hz.csv",
    "4w_20mm_pre_EQ": "07_4wires_sin20mm_0p5Hz.csv",
    "4w_20mm_post_EQ": "09_4wires_sin20mm_0p5Hz_after_EQ.csv",
}


def read_trace(archive: zipfile.ZipFile, filename: str) -> dict[str, list[float]]:
    with archive.open(PREFIX + filename) as raw:
        rows = list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig")))
    expected = {"Time", "Actuator1_Disp", "Actuator1_Force"}
    if not rows or not expected.issubset(rows[0]):
        raise ValueError(f"Missing expected columns in {filename}")
    out = {key: [float(row[key]) for row in rows] for key in expected}
    times = out["Time"]
    if any(not math.isfinite(v) for col in out.values() for v in col):
        raise ValueError(f"Nonfinite value in {filename}")
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError(f"Nonincreasing time in {filename}")
    # Decimal timestamps in the CSV are rounded to varying precision.
    if any(abs((b - a) - 1 / 512) > 1e-6 for a, b in zip(times, times[1:])):
        raise ValueError(f"Unexpected sampling interval in {filename}")
    return out


def crossing_force(
    times: list[float], displacements: list[float], forces: list[float],
    start: float, end: float, target: float,
) -> dict[str, float]:
    """Linearly interpolate force at one crossing per branch in a full cycle."""
    found: dict[str, list[float]] = {"rising": [], "falling": []}
    for i in range(len(times) - 1):
        if not (start <= times[i] and times[i + 1] < end):
            continue
        x0, x1 = displacements[i], displacements[i + 1]
        if (x0 - target) * (x1 - target) >= 0:
            continue
        branch = "rising" if x1 > x0 else "falling"
        weight = (target - x0) / (x1 - x0)
        found[branch].append(forces[i] + weight * (forces[i + 1] - forces[i]))
    if any(len(values) != 1 for values in found.values()):
        raise ValueError(f"Expected one crossing per branch in [{start}, {end}); got {found}")
    return {branch: values[0] for branch, values in found.items()}


def cycle_work(times: list[float], x: list[float], force: list[float],
               start: float, end: float) -> float:
    indices = [i for i, t in enumerate(times) if start <= t < end]
    return sum(
        (force[a] + force[b]) * (x[b] - x[a]) / 2
        for a, b in zip(indices, indices[1:])
    )


def characterize(trace: dict[str, list[float]]) -> dict:
    t, x, f = (trace[key] for key in ("Time", "Actuator1_Disp", "Actuator1_Force"))
    cycles = []
    # The CSV has ten imposed 2 s periods in 0-20 s followed by rest. Exclude
    # the first and last periods, which contain onset/offset transients.
    for period_index in range(1, 9):
        start = 2.0 * period_index
        cross = crossing_force(t, x, f, start, start + 2.0, 10.0)
        cycles.append({
            "period_index_zero_based": period_index,
            "time_s": [start, start + 2.0],
            "force_at_10mm_rising_kN": cross["rising"],
            "force_at_10mm_falling_kN": cross["falling"],
            "branch_gap_kN": cross["rising"] - cross["falling"],
            "loop_work_kN_mm_equiv_J": cycle_work(t, x, f, start, start + 2.0),
        })
    gaps = [row["branch_gap_kN"] for row in cycles]
    work = [row["loop_work_kN_mm_equiv_J"] for row in cycles]
    return {
        "rows": len(t),
        "sample_interval_s": 1 / 512,
        "measured_displacement_range_mm": [min(x), max(x)],
        "measured_force_range_kN": [min(f), max(f)],
        "cycles": cycles,
        "gap_mean_kN": statistics.mean(gaps),
        "gap_min_kN": min(gaps),
        "gap_max_kN": max(gaps),
        "interpolated_pair_minimax_error_floor_kN": min(gaps) / 2,
        "loop_work_mean_J": statistics.mean(work),
    }


def lookup_test(trace: dict[str, list[float]], width_mm: float, lag_samples: int) -> dict:
    """Train two median lookup tables on 2-10 s; score both on 10-18 s."""
    t, x, f = (trace[key] for key in ("Time", "Actuator1_Disp", "Actuator1_Force"))
    static = defaultdict(list)
    history = defaultdict(list)
    for i, ti in enumerate(t):
        if not 2 <= ti < 10:
            continue
        b = round(x[i] / width_mm)
        branch = int(x[i] > x[i - lag_samples])
        static[b].append(f[i])
        history[(b, branch)].append(f[i])
    static_model = {key: statistics.median(values) for key, values in static.items()}
    history_model = {key: statistics.median(values) for key, values in history.items()}
    error_static, error_history = [], []
    missing = 0
    for i, ti in enumerate(t):
        if not 10 <= ti < 18:
            continue
        b = round(x[i] / width_mm)
        branch = int(x[i] > x[i - lag_samples])
        if b not in static_model or (b, branch) not in history_model:
            missing += 1
            continue
        error_static.append(abs(f[i] - static_model[b]))
        error_history.append(abs(f[i] - history_model[(b, branch)]))
    if not error_static:
        raise ValueError("No held-out observations covered by both models")
    return {
        "bin_width_mm": width_mm,
        "causal_lookback_samples": lag_samples,
        "causal_lookback_s": lag_samples / 512,
        "training_rows": sum(len(v) for v in static.values()),
        "test_rows_scored": len(error_static),
        "test_rows_missing_either_lookup": missing,
        "static_table_bins": len(static_model),
        "history_table_bins": len(history_model),
        "static_test_MAE_kN": statistics.mean(error_static),
        "history_test_MAE_kN": statistics.mean(error_history),
        "MAE_ratio_static_over_history": statistics.mean(error_static) / statistics.mean(error_history),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, default=HERE / "source" / ZIP_NAME)
    parser.add_argument("--output", type=Path, default=HERE / "RESULTS.json")
    args = parser.parse_args()
    source_bytes = args.zip.read_bytes()
    actual_md5 = hashlib.md5(source_bytes).hexdigest()
    if actual_md5 != ZIP_MD5:
        raise ValueError(f"Zenodo ZIP MD5 mismatch: {actual_md5}")
    with zipfile.ZipFile(io.BytesIO(source_bytes)) as archive:
        traces = {key: read_trace(archive, name) for key, name in FILES.items()}
    result = {
        "source_record": "https://doi.org/10.5281/zenodo.17296336",
        "source_zip_md5_verified": actual_md5,
        "source_zip_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "force_at_target_method": "linear interpolation between two measured samples bracketing +10 mm",
        "interior_periods": "2-18 s, eight complete 2 s periods, excluding first and last active periods",
        "trace_characterization": {key: characterize(trace) for key, trace in traces.items()},
        "within_trace_prediction_8w_20mm": lookup_test(traces["8w_20mm_0p5Hz"], 0.5, 16),
        "lookup_sensitivity_8w_20mm": [
            lookup_test(traces["8w_20mm_0p5Hz"], width, lag)
            for width in (0.25, 0.5, 1.0) for lag in (8, 16, 32)
        ],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "source_zip_md5_verified": actual_md5,
        "8w_20mm_min_gap_kN": result["trace_characterization"]["8w_20mm_0p5Hz"]["gap_min_kN"],
        "8w_20mm_mean_gap_kN": result["trace_characterization"]["8w_20mm_0p5Hz"]["gap_mean_kN"],
        "lookup": result["within_trace_prediction_8w_20mm"],
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
