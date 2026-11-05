"""Independently verify the planner's full acquired-table prediction path.

Boole quadrature exactly integrates the degree-five convolution integrand.
Seven exact samples identify each degree-six polynomial on the complete
breakpoint partition. No microscopic plant model is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"
sys.path.insert(0, str(BRIDGE))
from verify_step_prediction import boole_response, pval


def main():
    begin = time.perf_counter()
    tp = BRIDGE / "acquired_step_response.json"
    cp = HERE / "robust_planner_certificate.json"
    pp = HERE / "robust_planner_prediction_path.json"
    table, cert, path = (json.loads(p.read_text()) for p in (tp, cp, pp))
    table_hash = hashlib.sha256(tp.read_bytes()).hexdigest()
    cert_hash = hashlib.sha256(cp.read_bytes()).hexdigest()
    assert table_hash == path["acquired_table_sha256"] == cert["acquired_table_sha256"]
    assert cert_hash == path["planner_certificate_sha256"]
    assert path["force_program"] == cert["force_program"]
    times = [F(t) for t in table["times_exact"]]
    values = [F(x) for x in table["values_exact"]]
    baseline, T = F(table["deployment_baseline_exact"]), F(table["horizon_exact"])
    assert times[0] == 0 and times[-1] == T and values[0] == 0
    assert all(b > a for a, b in zip(times, times[1:]))
    ramps = [(F(r["start_exact"]), F(r["ramp_exact"]), F(r["increment_exact"]))
             for r in path["force_program"]]
    expected = {F(0), T}
    for start, h, c in ramps:
        assert start >= 0 and h > 0
        for knot in times:
            for b in (start + knot, start + h + knot):
                if 0 < b < T:
                    expected.add(b)
    expected = sorted(expected)
    segments = path["segments"]
    assert len(segments) == len(expected) - 1
    samples = boxes = 0
    last_end = None
    for i, segment in enumerate(segments):
        left, right = F(segment["left_exact"]), F(segment["right_exact"])
        assert (left, right) == (expected[i], expected[i + 1])
        coefficients = [F(c) for c in segment["coefficients_exact"]]
        assert 1 <= len(coefficients) <= 7
        if last_end is not None:
            assert pval(coefficients, left) == last_end
        for j in range(1, 8):
            t = left + (right - left) * F(j, 8)
            target = baseline
            for start, h, c in ramps:
                value, n = boole_response(times, values, t, start, h)
                target += c * value
                boxes += n
            assert pval(coefficients, t) == target
            samples += 1
        last_end = pval(coefficients, right)
    assert pval([F(c) for c in segments[0]["coefficients_exact"]], F(0)) == baseline
    assert last_end == F(cert["predicted_endpoint_exact"])
    variation = sum(abs(c) for start, h, c in ramps)
    bound = (F(table["readiness_error_exact"])
             + variation * F(table["response_error_exact"])
             + F(table.get("delivery_error_exact", "0")))
    assert variation == F(cert["actual_variation_exact"])
    assert bound == F(path["uniform_physical_error_bound_exact"])
    assert bound <= F(cert["uniform_physical_radius_for_all_candidates_exact"])
    result = {
        "verified": True,
        "method": "Exact Boole quadrature on each degree-five integration cell, seven-point degree-six polynomial identities, continuity, complete breakpoint partition and error composition.",
        "path_sha256": hashlib.sha256(pp.read_bytes()).hexdigest(),
        "table_sha256": table_hash,
        "planner_certificate_sha256": cert_hash,
        "segments": len(segments),
        "identity_points": samples,
        "degree_five_quadrature_boxes": boxes,
        "actual_variation_exact": str(variation),
        "uniform_physical_error_bound_exact": str(bound),
        "uniform_physical_error_bound": float(bound),
        "endpoint_physical_interval": [float(last_end - bound), float(last_end + bound)],
        "elapsed_seconds": time.perf_counter() - begin,
        "scope": "Acquired-table path arithmetic is exact. The retained physical bound is conditional on acquisition, readiness and finite command delivery; no second physical deployment is claimed."
    }
    (HERE / "robust_planner_path_verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
