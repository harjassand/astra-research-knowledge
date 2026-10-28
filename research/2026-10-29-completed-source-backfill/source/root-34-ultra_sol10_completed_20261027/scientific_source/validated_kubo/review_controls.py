"""Independent kernel replay, complex-observable and scalar controls.

The parent physical block builder is reused read-only for its625-state
trace. Validation is recomputed with certify_kubo.py; producer.certify_block
is not called, and no producer output is written.
"""
import importlib.util
import json
import time
from fractions import Fraction as F

import numpy as np
import scipy.linalg as la
from certify_kubo import (ROOT, HQ, VQ, S, Interval, exp_interval, psi_fixed,
                         fixed_interval, validate_proposal, certify_correlations, serial)


def overlap(a, b):
    return max(a.lo, b.lo) <= min(a.hi, b.hi)


def scalar_controls():
    cases = [F(0), F(1, 1 << 160), F(1, 1 << 40), F(1, 3), F(1, 2),
             F(1), F(3), F(30), F(80)]
    rows = []
    for x in cases:
        direct = Interval(F(1), F(1)) if x == 0 else (1 + -exp_interval(-x)) * (1 / x)
        stable = fixed_interval(*psi_fixed(x))
        assert overlap(stable, direct)
        assert 0 <= stable.lo <= stable.hi <= 1
        rows.append({"x": serial(x), "stable_width": serial(stable.hi - stable.lo),
                     "subtractive_width": serial(direct.hi - direct.lo),
                     "overlap_independent_identity": True})
    assert psi_fixed(F(0)) == (S, S)
    return rows


def complex_pauli_control():
    # H=sigma_y, A=sigma_x, B=sigma_z; H^2=A^2=B^2=I.
    zero = np.zeros((2, 2), dtype=object)
    hy_im = np.array([[0, -1], [1, 0]], dtype=object)
    hx_re = np.array([[0, 1], [1, 0]], dtype=object)
    hz_re = np.array([[1, 0], [0, -1]], dtype=object)
    vals, vecs = la.eigh(np.asarray(hy_im, dtype=float) * 1j)
    vr = np.rint(vecs.real * VQ).astype(np.int64)
    vi = np.rint(vecs.imag * VQ).astype(np.int64)
    lam = np.rint(vals * HQ).astype(np.int64)
    record = validate_proposal(zero, hy_im * HQ, F(0), vr, vi, lam)
    obs = {"x": (hx_re, zero, 1, F(1)), "z": (hz_re, zero, 1, F(1)),
           "y": (zero, hy_im, 1, F(1))}
    pairs = [("x", "x"), ("x", "z"), ("y", "y")]
    beta = F(3, 2)
    certified = certify_correlations(record, obs, pairs, beta)
    references = {"x,x": (exp_interval(beta) + -exp_interval(-beta)) * (1 / beta),
                  "x,z": Interval(F(0), F(0)),
                  "y,y": exp_interval(beta) + exp_interval(-beta)}
    assert certified["trace"].contains(references["y,y"])
    for name, ref in references.items():
        assert certified["correlations"][name]["physical_interval"].contains(ref)
    infinite_temperature = certify_correlations(record, obs, pairs, F(0))
    for name, exact in {"x,x": 2, "x,z": 0, "y,y": 2}.items():
        assert infinite_temperature["correlations"][name]["physical_interval"].contains(Interval(F(exact), F(exact)))
    return {"model": "H=sigma_y; observables sigma_x,sigma_z,sigma_y; beta=3/2",
            "complex_V_nonzero": bool(np.any(vi)),
            "exact_reference_formulas": {"x,x": "(exp(beta)-exp(-beta))/beta",
                                          "x,z": "0", "y,y": "exp(beta)+exp(-beta)"},
            "intervals": {name: certified["correlations"][name]["physical"] for name in references},
            "delta": serial(record["delta"]), "beta0_trace_controls": True,
            "all_exact_reference_intervals_contained": True}


def parent_trace_replay():
    path = ROOT.parent / "parent" / "validated_twist_trace" / "certify.py"
    spec = importlib.util.spec_from_file_location("read_only_parent_trace_builder", path)
    producer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(producer)
    stored = json.loads((path.parent / "TRACE_CERTIFICATE.json").read_text())
    saved_by_mag = {row["magnetization"]: row for row in stored["sector_records"]}
    begin = time.monotonic()
    controls = [F(0), F(0), F(0)]
    trace = Interval(F(0), F(0))
    trace_original = Interval(F(0), F(0))
    rows = []
    n, beta = 4, F(3)
    for mag in range(-2 * n, 2 * n + 1):
        qr, qi, eta, moments = producer.sector(n, mag)
        controls = [x + y for x, y in zip(controls, moments)]
        vals, vecs = la.eigh((qr + 1j * qi) / HQ, check_finite=False)
        vr = np.rint(vecs.real * VQ).astype(np.int64)
        vi = np.rint(vecs.imag * VQ).astype(np.int64)
        lam = np.rint(vals * HQ).astype(np.int64)
        record = validate_proposal(qr, qi, eta, vr, vi, lam)
        proposal = sum((exp_interval(-beta * e) for e in record["lam"]), Interval(F(0), F(0)))
        growth = exp_interval(beta * record["delta"]).hi
        trace += Interval(proposal.lo / growth, proposal.hi * growth)
        growth_original = exp_interval(beta * record["delta_original"]).hi
        trace_original += Interval(proposal.lo / growth_original, proposal.hi * growth_original)
        equal = all(F(saved_by_mag[mag][key]) == record[key]
                    for key in ("epsilon", "eta", "residual"))
        equal = equal and F(saved_by_mag[mag]["delta"]) == record["delta_original"]
        rows.append({"magnetization": mag, "dimension": len(qr),
                     "epsilon": serial(record["epsilon"]), "delta": serial(record["delta"]),
                     "delta_original": serial(record["delta_original"]),
                     "original_exact_bounds_equal_to_stored_run": equal})
    assert controls == [F(0), F(30000), F(0)]
    assert sum(row["dimension"] for row in rows) == 625
    saved_trace = Interval(F(stored["trace_lower"]), F(stored["trace_upper"]))
    assert overlap(trace, saved_trace)
    return {"status": "INDEPENDENT_VALIDATION_KERNEL_REPLAY_PASS",
            "producer_source_read_only": str(path),
            "physical_builder": "reviewed producer exact block builder, reused read-only",
            "validation_kernel": "independent certify_kubo.py exact Gram/residual/scalar implementation",
            "all_states": 625, "sectors": rows, "trace": trace.record(),
            "trace_original_polar_bound": trace_original.record(),
            "relative_width": serial((trace.hi - trace.lo) / trace.lo),
            "width_improvement_from_Hermitian_Sylvester_bound": serial((trace_original.hi-trace_original.lo)/(trace.hi-trace.lo)),
            "overlap_stored_interval": True,
            "new_interval_contained_in_stored": saved_trace.contains(trace),
            "exact_controls": [serial(x) for x in controls],
            "seconds": time.monotonic() - begin}


def main():
    start = time.monotonic()
    output = {"scalar_psi_controls": scalar_controls(),
              "complex_observable_control": complex_pauli_control(),
              "parent_trace_review_replay": parent_trace_replay()}
    output["total_seconds"] = time.monotonic() - start
    (ROOT / "CONTROL_REPLAY.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": "ALL_CONTROLS_PASS", "scalar_cases": len(output["scalar_psi_controls"]),
                      "complex_observable_reference": output["complex_observable_control"]["all_exact_reference_intervals_contained"],
                      "parent_trace": output["parent_trace_review_replay"]["trace"]["display_only"],
                      "parent_trace_seconds": output["parent_trace_review_replay"]["seconds"],
                      "total_seconds": output["total_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
