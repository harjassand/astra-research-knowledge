"""Bounded diagnostics for c05_s03's spin window and exact iid boundary.

Fraction fixtures verify transcription; floating scalar histograms verify
the finite formula's numerical behavior. Neither replaces the all-N proof.
All output stays adjacent to this owned script. No full 2**N state is built.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json
import math
import time


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def outer(x, y):
    return [[a*b for b in y] for a in x]


def add(x, y, sign=1):
    return [[a+sign*b for a, b in zip(rx, ry)] for rx, ry in zip(x, y)]


def mul(x, y):
    return [[sum(x[i][k]*y[k][j] for k in range(len(y)))
             for j in range(len(y[0]))] for i in range(len(x))]


def mv(x, y):
    return [dot(row, y) for row in x]


def tr(x):
    return [list(row) for row in zip(*x)]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def cross_matrix(m):
    x, y, z = m
    return [[F(0), -z, y], [z, F(0), -x], [-y, x, F(0)]]


def det(x):
    if len(x) == 1:
        return x[0][0]
    return sum((-1)**j*x[0][j]*det([row[:j]+row[j+1:] for row in x[1:]])
               for j in range(len(x)))


def psd_exact(x):
    assert x == tr(x)
    for size in range(1, len(x)+1):
        for ids in combinations(range(len(x)), size):
            assert det([[x[i][j] for j in ids] for i in ids]) >= 0


def rational_drift_and_psd():
    axes = [(F(0), F(0), F(1)), (F(3, 5), F(0), F(4, 5)),
            (F(1, 3), F(2, 3), F(2, 3))]
    points = [tuple(F(i, 12) for i in p) for p in product([-1, 0, 1], repeat=3)]
    points += [(F(1, 4), F(0), F(0)), (F(0), F(-1, 4), F(0))]
    drift_count = 0
    for n in axes:
        assert dot(n, n) == 1
        rn = cross_matrix(n)
        for m in points:
            u = dot(n, m)
            v = [ni-u*mi for ni, mi in zip(n, m)]
            r = mv(rn, m)
            jv = [[-m[i]*n[j]-u*int(i == j) for j in range(3)] for i in range(3)]
            lhs = [a-b for a, b in zip(mv(jv, v), mv(rn, r))]
            rhs = [-2*u*vi for vi in v]
            assert lhs == rhs
            drift_count += 1
    rotations = [eye(3), [[F(3, 5), F(-4, 5), F(0)],
                         [F(4, 5), F(3, 5), F(0)], [F(0), F(0), F(1)]]]
    psd_count = 0
    for M in [F(0), F(1), F(5)]:
        shift = 2*M+1
        eigs = [-M+shift, M/2+shift, M+shift]
        L, cmin = 3*M+1, M+1
        for R in rotations:
            assert mul(R, tr(R)) == eye(3)
            diag = [[eigs[i]*int(i == j) for j in range(3)] for i in range(3)]
            C = mul(mul(R, diag), tr(R))
            for m in points:
                assert dot(m, m) <= F(1, 16)
                P = add(eye(3), outer(m, m), -1)
                cm = cross_matrix(m)
                D = add(mul(mul(P, C), P), mul(mul(cm, C), tr(cm)), -1)
                low = [[F(177, 256)*cmin*int(i == j) for j in range(3)] for i in range(3)]
                high = [[L*int(i == j) for j in range(3)] for i in range(3)]
                psd_exact(add(D, low, -1))
                psd_exact(add(high, D, -1))
                psd_count += 1
    return {"drift_fraction_fixtures": drift_count, "PSD_fraction_fixtures": psd_count,
            "scope": "Exact rational transcription checks, not all-parameter proof."}


def mass_fraction(N, lo, p):
    hi = N-lo
    return sum(F(math.comb(N, k))*p**k*(1-p)**(N-k) for k in range(lo, hi+1))


def central_intervals():
    count = 0
    for N in range(2, 25):
        for lo in range(1, N//2+1):
            center = mass_fraction(N, lo, F(1, 2))
            for i in range(17):
                assert mass_fraction(N, lo, F(i, 16)) <= center
                count += 1
    return {"exact_rational_central_mass_checks": count,
            "scope": "Small finite fixtures; analytic derivative proof supplies all N,p."}


def binomial_histogram(N):
    # Only N+1 scalar weights; normalize after a log-domain computation.
    log_two = math.log(2.0)
    log_fact = math.lgamma(N+1)
    logs = [log_fact-math.lgamma(k+1)-math.lgamma(N-k+1)-N*log_two
            for k in range(N+1)]
    peak = max(logs)
    raw = [math.exp(v-peak) for v in logs]
    norm = math.fsum(raw)
    return [v/norm for v in raw]


def scalar_boundary(N, kappa):
    pn = binomial_histogram(N)
    weights = [math.exp(-kappa*(k-N/2)**2/N) for k in range(N+1)]
    zn = math.fsum(p*g for p, g in zip(pn, weights))
    qn = [p*g/zn for p, g in zip(pn, weights)]
    dn = math.fsum(abs(q-p) for p, q in zip(pn, qn))/2
    ids = [k for k, g in enumerate(weights) if g >= zn]
    event = math.fsum(qn[k]-pn[k] for k in ids)
    assert abs(dn-event) < 2e-14
    assert all(k in ids for k in range(min(ids), max(ids)+1))
    assert min(ids)+max(ids) == N
    beta = 1+kappa/2
    a = math.sqrt(2*math.log(beta)/kappa)
    limit = math.erf(a*math.sqrt(beta)/math.sqrt(2))-math.erf(a/math.sqrt(2))
    return {"N": N, "kappa": kappa, "normalizer": zn,
            "exact_formula_float_evaluation": dn, "limiting_distance": limit,
            "absolute_limit_difference": abs(dn-limit),
            "central_event": [min(ids), max(ids)],
            "event_formula_residual": abs(dn-event)}


def constants():
    r0 = 0.25
    a0 = math.log(9/7)
    delta = 0.5-math.log(math.cosh(1))
    kappa0 = min(a0**4/768, delta/4)
    U0 = (8/3)*math.sinh(1)+16*math.sqrt(math.pi)*delta**(-1.5)
    C0 = (3/7)*math.exp(1/12)*U0
    eps0 = min(1/56, kappa0/16, 3*r0*r0/1024)
    return {"r0": r0, "a0": a0, "delta": delta, "kappa0": kappa0,
            "C0": C0, "epsilon0": eps0,
            "scope": "Floating evaluations; exact expressions are in the proof."}


def main():
    start = time.perf_counter()
    data = {"worker": "c05_s03", "scope": "Bounded diagnostics only; universal proofs are in 03_spin_growing_window_and_exact_boundary.txt.",
            "drift_and_psd": rational_drift_and_psd(), "central_intervals": central_intervals(),
            "constants": constants(),
            "boundary": [scalar_boundary(N, k) for k in [0.5, 2.0, 10.0]
                         for N in [2, 4, 20, 100, 500, 2000, 10000]]}
    data["runtime_seconds"] = time.perf_counter()-start
    Path(__file__).with_suffix(".json").write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"runtime_seconds": data["runtime_seconds"],
                      "fraction_fixture_counts": [data["drift_and_psd"]["drift_fraction_fixtures"],
                                                   data["drift_and_psd"]["PSD_fraction_fixtures"],
                                                   data["central_intervals"]["exact_rational_central_mass_checks"]],
                      "kappa2_N10000": [r for r in data["boundary"] if r["kappa"] == 2.0 and r["N"] == 10000][0],
                      "constants": data["constants"]}, indent=2))


if __name__ == "__main__":
    main()
