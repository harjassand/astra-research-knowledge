#!/usr/bin/env python3
"""Bounded exact-rational admissions for the collective actual-queue obstruction.

These finite calculations check the elementary latent-source identities and the
resulting analytic bound. They are not a substitute for the proof in the report.
Python standard library only; no sampled quantum hardware or optimization oracle.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, log
from pathlib import Path
import json
import time


def bell_law(D, L):
    """Unmeasured mathematical Bell-basis law; site 1 is the fixed Bell seed."""
    law = []
    q = D * D
    for y in product(range(q), repeat=L - 1):
        conditional = []
        for k in range(1, L + 1):
            conditional.append(F(1, q ** (L - k)) if all(z == 0 for z in y[: k - 1]) else F(0))
        py = sum(conditional, F(0)) / L
        if py:
            posterior = [v / (L * py) for v in conditional]
            law.append((y, py, posterior))
    assert sum(row[1] for row in law) == 1
    assert all(sum(row[2]) == 1 for row in law)
    c = F(D * D - 1, D ** (2 * L) - 1)
    assert min(row[2][0] for row in law) == c
    return law, c


def optimal_classical_event(D, L, r, s):
    """Exact upper envelope over every latent-Y -> selected-set strategy.

    Conditional on Yvec, selecting the s lowest posterior Pr(K_a=1|Y_a)
    maximizes the event of selecting >=s positions with none having K_a=1.
    Any receiver plus any final quantum measurement is such a stochastic channel.
    """
    law, c = bell_law(D, L)
    answer = F(0)
    for rows in product(law, repeat=r):
        py = F(1)
        for row in rows:
            py *= row[1]
        probs = sorted((row[2][0] for row in rows))
        success = F(1)
        for p1 in probs[:s]:
            success *= 1 - p1
        answer += py * success
    bound = (1 - c) ** s
    assert answer <= bound
    return {"D": D, "L": L, "r": r, "s": s,
            "optimal_event_probability_exact": str(answer),
            "posterior_bound_exact": str(bound)}


def beta(D, L, w):
    return sum((1 - F(1, D ** max(0, k - w - 1)) for k in range(1, L + 1)), F(0)) / L


def pointwise_error_bound(D, L, w, r):
    _, c = bell_law(D, L)
    b = beta(D, L, w)
    if not b:
        return {"D": D, "L": L, "w": w, "r": r, "bound": 0.0, "s": 0}
    probs = [F(comb(r, j)) * b ** j * (1 - b) ** (r - j) for j in range(r + 1)]
    assert sum(probs) == 1
    tail = F(1)
    best = F(0)
    arg = 0
    for s in range(1, r + 1):
        tail -= probs[s - 1]
        bound = tail - (1 - c) ** s
        if bound > best:
            best, arg = bound, s
    return {"D": D, "L": L, "w": w, "r": r,
            "c_exact": str(c), "beta_exact": str(b),
            "bound": float(best), "s": arg,
            "exact_numerator_bits": best.numerator.bit_length(),
            "exact_denominator_bits": best.denominator.bit_length()}


def projection_identity_admission():
    """Check the Gram-exponent identities underlying the root finite-r lemma.

    <v_i,v_j> = a^|i-j|, a=D^-1/2. For j<=k<l, the proposed
    projection a^(l-k) v_k has exactly the required Gram inner product.
    The equality is the integer exponent identity, valid for all D>=2.
    """
    count = 0
    for L in range(2, 33):
        for k in range(L):
            for ell in range(k + 1, L + 1):
                for j in range(k + 1):
                    assert abs(j - ell) == (ell - k) + abs(j - k)
                    count += 1
    return {"PASS": True, "Gram_exponent_identities": count,
            "projection_norm_squared": "D^(-(ell-k))"}


def main():
    start = time.perf_counter()
    exact = [optimal_classical_event(D, L, r, s)
             for D, L, r in [(2, 2, 4), (2, 3, 3), (3, 2, 3)]
             for s in range(1, r + 1)]
    bounds = [pointwise_error_bound(2, 2, 0, r) for r in [1, 4, 16, 64, 256, 1024]]
    bounds += [pointwise_error_bound(2, 3, 1, r) for r in [16, 64, 256, 1024]]
    result = {"status": "PASS", "scope": "bounded exact-rational admission, not theorem acceptance",
              "latent_source_and_optimal_event_checks": exact,
              "pointwise_global_error_lower_bounds": bounds,
              "root_projection_admission": projection_identity_admission(),
              "runtime_seconds": time.perf_counter() - start,
              "dependencies": "Python standard library", "hardware": "local CPU only"}
    destination = Path(__file__).with_name("REPLAY_RESULT.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "path": str(destination),
                      "bounds": bounds, "runtime_seconds": result["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
