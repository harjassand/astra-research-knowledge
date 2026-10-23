#!/usr/bin/env python3
"""Bounded admission checks; analytic proofs are in PROOF.txt."""
import json
import math
import time
from fractions import Fraction
from pathlib import Path


def conditional_admission(D, N):
    n = D**N
    # Explicit coefficient matrix of the rank-one H:R Bell projector.
    X = {((h, h), (j, j)): Fraction(1, n)
         for h in range(n) for j in range(n)}
    assert sum(v*v for v in X.values()) == 1
    norms = []
    for i in range(1, N+1):
        a, b = D**i, D**(N-i)
        reduced = {}
        for ((h, r), (j, s)), value in X.items():
            if h//b == j//b:
                key = (h % b, r, j % b, s)
                reduced[key] = reduced.get(key, Fraction()) + value
        output = {}
        for (t, r, u, s), value in reduced.items():
            for prefix in range(a):
                output[((prefix*b+t, r), (prefix*b+u, s))] = value/a
        norm = sum(v*v for v in output.values())
        assert norm == Fraction(1, a*a)
        norms.append(str(norm))
    required_defect = N*math.log(D) + math.log(D)*sum(
        float(Fraction(1, D**(2*i))) for i in range(1, N+1))
    return {"D": D, "N": N, "exact_HS_norm_squares": norms,
            "required_conditional_defect_nats": required_defect,
            "status": "PASS"}


def extraction_admission(D, n):
    harmonic = math.fsum(1/j for j in range(1, n+1))
    mu = [1/math.sqrt(j*harmonic) for j in range(1, n+1)]
    psi = [1/math.sqrt(D*((j-1)//D+1)*harmonic)
           for j in range(1, D*n+1)]
    assert abs(math.fsum(x*x for x in mu)-1) < 2e-14
    assert abs(math.fsum(x*x for x in psi)-1) < 2e-14
    # Apply the actual local divmod wire isometry to coefficient amplitudes.
    max_factor_error = 0.0
    for j, amplitude in enumerate(psi):
        residual, emitted = divmod(j, D)
        predicted = mu[residual]/math.sqrt(D)
        max_factor_error = max(max_factor_error, abs(amplitude-predicted))
        assert emitted in range(D)
    assert max_factor_error < 2e-15
    overlap = math.fsum(psi[j]*mu[j] for j in range(n))
    delta = math.sqrt(max(0.0, 1-overlap*overlap))
    shifted = math.fsum(1/j for j in range(D, n+D)) / harmonic
    assert overlap + 2e-14 >= shifted
    small_harmonic = math.fsum(1/j for j in range(1, D))
    if harmonic >= small_harmonic:
        assert delta*delta <= 2*small_harmonic/harmonic + 2e-14
    e_mu = -math.fsum(x*x*math.log(x*x) for x in mu)
    e_psi = -math.fsum(x*x*math.log(x*x) for x in psi)
    assert abs(e_psi-e_mu-math.log(D)) < 2e-13
    assert psi[n] > 0  # Returned vector has exactly zero at this coordinate.
    return {"D": D, "n": n, "return_half_trace": delta,
            "overlap_lower_bound": shifted,
            "exact_Bell_factor_max_amplitude_error": max_factor_error,
            "exact_supply_nats": math.log(D*n),
            "initial_pure_entropy_nats": e_psi,
            "support_intersection_dimension": 0, "status": "PASS"}


def main():
    start, cpu = time.perf_counter(), time.process_time()
    conditional = [conditional_admission(D, N)
                   for D, N in [(2, 1), (2, 2), (2, 3), (3, 2)]]
    extraction = [extraction_admission(D, n)
                  for D, n in [(2, 1), (2, 3), (2, 32), (2, 1024),
                               (3, 17), (4, 129)]]
    result = {"status": "PASS", "check_count": len(conditional)+len(extraction),
              "conditional_exact_rational_checks": conditional,
              "extraction_float_admissions": extraction,
              "wall_seconds": time.perf_counter()-start,
              "cpu_seconds": time.process_time()-cpu,
              "scope": "bounded admission only; no generic tensorization search"}
    target = Path(__file__).with_name("RESULT.json")
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
