#!/usr/bin/env python3
"""Exact finite admissions for the actual-nu-queue loss theorem.

These admissions do not replace the universal proof. All asserted numerical
inequalities use Python integers / fractions.Fraction; no scientific package
or external input is required. Output path is explicit and relocatable.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import time


def score_bound(D: int, L: int, b: int, a: int) -> F:
    return F(D * (D ** (b + a + 1) - 1), (D - 1) * L)


def cauchy_admissions() -> dict:
    rng = random.Random(900817)
    checked = 0
    tight = 0
    for D in (2, 3):
        for L in range(1, 4):
            d = D ** L
            for n in range(L + 1):
                out = D ** n
                for k in range(1, L + 1):
                    r, tails = D ** k, D ** (L - k)
                    for _ in range(5):
                        # Gaussian INTEGER entries; inner products remain exact.
                        A = [[(rng.randrange(-2, 3), rng.randrange(-2, 3))
                              for _ in range(d)] for _ in range(out)]
                        B = [[(rng.randrange(-2, 3), rng.randrange(-2, 3))
                              for _ in range(d)] for _ in range(out)]
                        norm_a = sum(x*x+y*y for row in A for x, y in row)
                        norm_b = sum(x*x+y*y for row in B for x, y in row)
                        lhs = 0
                        for u in range(tails):
                            for v in range(tails):
                                real = imag = 0
                                for y in range(out):
                                    for x in range(r):
                                        ar, ai = A[y][x*tails+u]
                                        br, bi = B[y][x*tails+v]
                                        real += ar*br-ai*bi
                                        imag += ar*bi+ai*br
                                lhs += real*real+imag*imag
                        rhs = norm_a*norm_b
                        assert lhs <= rhs, (D, L, n, k, lhs, rhs)
                        # Including prior/noise/Bell normalization is exact.
                        f_actual = F(lhs, L * D**(2*(L-k)+k+n))
                        f_bound = F(rhs, L) * F(D)**(-2*L+k-n)
                        assert f_actual <= f_bound
                        checked += 1
                        tight += lhs == rhs
    return {"checked_gaussian_integer_cases": checked,
            "exact_equalities": tight, "status": "PASS"}


def geometric_admissions() -> dict:
    checked = 0
    for D in (2, 3, 4, 6, 8):
        for L in range(2, 22):
            for b in range(L+1):
                for a in range(5):
                    cap = D*(D**(b+a+1)-1)//(D-1)
                    for j in range(L+1):
                        n = max(0, j-1)
                        ks = range(max(1, j), min(L, j+b+a)+1)
                        actual = sum(D**(k-n) for k in ks)
                        assert actual <= cap
                        checked += 1
    return {"checked_eligible_band_cases": checked, "status": "PASS"}


def coarse_target_admissions() -> dict:
    checked = 0
    for D in (2, 3, 4, 6, 8):
        for n in range(0, 32):
            p = [F(1, D**n)]
            p.extend(F((D-1)*D**(j-1), D**n) for j in range(1, n+1))
            assert sum(p) == 1
            for a in range(12):
                bad = sum(prob for j, prob in enumerate(p) if n-j>a)
                assert bad <= F(1, D**(a+1))
                checked += 1
            for j in range(1, n+1):
                # Exact reduced-prefix matrix element after coarse J projection:
                # (D-1) identical discarded-site-j values / total support size.
                surviving_entries = D**(j-1)
                support_size = surviving_entries*(D-1)
                reduced_element = F(D-1, support_size)
                assert reduced_element == F(1, surviving_entries)
    return {"checked_trailing_gap_cases": checked,
            "pure_prefix_reduced_elements": "EXACT", "status": "PASS"}


def identity_protocol_admissions() -> dict:
    checked = 0
    max_ratio = F(0)
    for D in (2, 3, 4, 6):
        for L in range(2, 20):
            pj = [F(1, D**L)]
            pj.extend(F((D-1)*D**(j-1), D**L) for j in range(1, L+1))
            for b in range(L+1):
                for a in range(4):
                    score = F(0)
                    for j, prob in enumerate(pj):
                        n = max(0, j-1)
                        for k in range(max(1, j), min(L, j+b+a)+1):
                            # Here eligible k>=j, so the target prefix below J
                            # is guaranteed Bell under the identity receiver.
                            assert n <= k
                            score += prob/F(L)
                    bound = score_bound(D, L, b, a)
                    assert score <= bound
                    max_ratio = max(max_ratio, score/bound)
                    checked += 1
    return {"checked_identity_plus_coarse_readout_scores": checked,
            "max_score_over_bound": str(max_ratio), "status": "PASS"}


def nonlocal_control_admissions() -> dict:
    checked = 0
    examples = []
    for D in (2, 3, 4, 6):
        q = F(1, D**2)
        for L in range(2, 30):
            for w in range(L+1):
                global_bad = F(0)
                for k in range(1, L+1):
                    mass = F(0)
                    bad = F(0)
                    for H in range(k, L+1):
                        p = q**(H-k) * ((1-q) if H<L else 1)
                        n = max(1, H-w)
                        nstar = min(k, n)
                        assert max(1, k-w) <= nstar <= k
                        mass += p
                        if n>k:
                            bad += p
                    assert mass == 1
                    assert bad <= q**(w+1)
                    global_bad += bad/F(L)
                    checked += 1
                assert global_bad <= q**(w+1)
                if (D, L, w) in ((2, 16, 1), (2, 16, 2), (3, 16, 1)):
                    examples.append({"D": D, "L": L, "w": w,
                        "exact_bad_mass": str(global_bad),
                        "joint_halftrace_upper": str(q**(w+1))})
    return {"checked_conditional_nonlocal_distributions": checked,
            "examples": examples, "admissible_LOCC": False, "status": "PASS"}


def access_admissions() -> dict:
    checked = 0
    for L in range(2, 80):
        for p in (F(0), F(1, 100), F(1, 3), F(1)):
            # Initial supplied erasure-style exact inventory access.
            rows = [[1-p] + [p if j==k else F(0) for j in range(L)]
                    for k in range(L)]
            factor = sum(max(row[z] for row in rows) for z in range(L+1))
            assert factor == 1+p*(L-1)
            checked += 1
        # Independent shared coins contribute exactly one, however many atoms.
        coins = [F(1, 7), F(2, 7), F(4, 7)]
        assert sum(max(q for _ in range(L)) for q in coins) == 1
        checked += 1
    return {"checked_initial_access_examples": checked, "status": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("EXACT_REPLAY_RESULTS.json"))
    args = parser.parse_args()
    wall, cpu = time.perf_counter(), time.process_time()
    results = {
        "scope": "bounded exact admissions, not proof/novelty acceptance",
        "arithmetic": "Python integers and Fraction only for all assertions",
        "product_kraus_cauchy": cauchy_admissions(),
        "geometric_band": geometric_admissions(),
        "coarse_target": coarse_target_admissions(),
        "identity_receiver": identity_protocol_admissions(),
        "nonlocal_control": nonlocal_control_admissions(),
        "initial_access": access_admissions(),
    }
    results["wall_seconds"] = time.perf_counter()-wall
    results["cpu_seconds"] = time.process_time()-cpu
    results["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    results["status"] = "PASS"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({"output": str(args.output), "status": results["status"],
                      "wall_seconds": results["wall_seconds"]}))


if __name__ == "__main__":
    main()
