#!/usr/bin/env python3
"""New Cycle10 exact Bell-diagonal admissions; no predecessor suite executes."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import math
import time


def entropy(probabilities):
    return -sum(float(p) * math.log(float(p)) for p in probabilities if p)


def posterior_data(D, L, power=2):
    q = Fraction(1, D**power)
    ps, hs, means, posteriors = [], [], [], []
    for j in range(1, L+1):
        z = sum((q**g for g in range(j)), Fraction(0))
        posterior = tuple(q**g/z for g in range(j))
        mean = sum((g*p for g, p in enumerate(posterior)), Fraction(0))
        expected_mean = q/(1-q)-j*q**j/(1-q**j)
        assert mean == expected_mean
        p = (1-q**j)/L if j < L else (1-q**L)/(L*(1-q))
        ps.append(p)
        hs.append(entropy(posterior))
        means.append(mean)
        posteriors.append(posterior)
    assert sum(ps) == 1
    return ps, hs, means, posteriors


def compact_data(D, L):
    """O(L) floating scalar evaluation, independent of large Hilbert space."""
    q = D**-2
    hgeo = -math.log1p(-q)-q/(1-q)*math.log(q)
    c = 0.0
    for j in range(1, L+1):
        qj = q**j
        hj = math.log1p(-qj)-math.log1p(-q)
        hj -= (q/(1-q)-j*qj/(1-qj))*math.log(q)
        pj = (1-qj)/L if j < L else (1-qj)/(L*(1-q))
        c += pj*hj
    b = (L+1)*math.log(D)/2
    a = q/(1-q)**2-q*math.log(q)/(1-q)**3
    assert -1e-11 <= hgeo-c <= a/L+1e-11
    return dict(D=D, L=L, preparation_supply_nats=b,
                conditional_entropy_nats=c, geometric_entropy_nats=hgeo,
                pooled_rate_upper_nats=b-math.log(L)/2+c/2,
                necessary_supply_deficit_nats=math.log(L)/2-c/2,
                remainder_upper_nats=a/L)


def exact_grouped_case(D, L):
    """Fractions for spectrum/posterior; floating only logarithm evaluation."""
    ps, hs, _, _ = posterior_data(D, L, 2)
    pshift, hshift, _, _ = posterior_data(D, L, 1)
    c = sum(float(p)*h for p, h in zip(ps, hs))
    cshift = sum(float(p)*h for p, h in zip(pshift, hshift))
    s = 0.0
    for j in range(1, L+1):
        eigenvalue = sum((Fraction(D**(2*k), L*D**(2*L))
                          for k in range(1, j+1)), Fraction(0))
        multiplicity = (D**2-1)*D**(2*(L-j-1)) if j < L else 1
        assert multiplicity*eigenvalue == ps[j-1]
        s -= float(multiplicity*eigenvalue)*math.log(float(eigenvalue))
    b = (L+1)*math.log(D)/2
    assert math.isclose(s, 2*(L-(L+1)/2)*math.log(D)+math.log(L)-c,
                        abs_tol=1e-11, rel_tol=1e-11)
    assert c <= cshift+1e-11
    assert math.isclose(compact_data(D, L)["conditional_entropy_nats"], c,
                        abs_tol=1e-11, rel_tol=1e-11)
    return dict(D=D, L=L, entropy_nats=s, posterior_entropy_nats=c,
                shift_posterior_entropy_nats=cshift,
                dephased_relative_entropy_nats=b-cshift+c)


def enumerate_case(D, L):
    """Independent enumeration of all Bell labels, including dephased spectrum."""
    joint = defaultdict(dict)
    jdist, hdist = defaultdict(Fraction), defaultdict(Fraction)
    entropy_sum, relative_sum = 0.0, 0.0
    count = 0
    for labels in product(range(D**2), repeat=L):
        j = 0
        for x in labels:
            if x != 0:
                break
            j += 1
        h = 0
        for x in labels:
            if x >= D:  # Encoding shift*D+phase.
                break
            h += 1
        if not j:
            continue
        by_k = {k: Fraction(1, L*D**(2*(L-k))) for k in range(1, j+1)}
        p = sum(by_k.values(), Fraction(0))
        zeta = sum((Fraction(1, L*D**(2*L-k))
                    for k in range(1, h+1)), Fraction(0))
        assert zeta > 0
        for k, value in by_k.items():
            joint[labels][k] = value
        jdist[j] += p
        hdist[h] += p
        entropy_sum -= float(p)*math.log(float(p))
        relative_sum += float(p)*math.log(float(p/zeta))
        count += 1
    assert sum(jdist.values()) == 1
    ps, hs, _, posteriors = posterior_data(D, L, 2)
    pshift, _, _, _ = posterior_data(D, L, 1)
    assert [jdist[j] for j in range(1, L+1)] == ps
    assert [hdist[h] for h in range(1, L+1)] == pshift
    cond = 0.0
    for labels, by_k in joint.items():
        p = sum(by_k.values(), Fraction(0))
        j = len(by_k)
        post = tuple(by_k[j-g]/p for g in range(j))
        assert post == posteriors[j-1]
        cond += float(p)*entropy(post)
    grouped = exact_grouped_case(D, L)
    assert math.isclose(entropy_sum, grouped["entropy_nats"], abs_tol=1e-10)
    assert math.isclose(cond, grouped["posterior_entropy_nats"], abs_tol=1e-10)
    assert math.isclose(relative_sum, grouped["dephased_relative_entropy_nats"],
                        abs_tol=1e-10)
    return dict(D=D, L=L, nonzero_Bell_strings=count,
                exact_posterior_identities=sum(len(v) for v in joint.values()))


def main():
    start, cpu = time.perf_counter(), time.process_time()
    enumerated = [enumerate_case(D, L) for D, maxL in ((2, 6), (3, 4), (4, 3), (6, 3))
                  for L in range(1, maxL+1)]
    grouped = [exact_grouped_case(D, L) for D in (2, 3, 4, 6, 10)
               for L in (1, 2, 3, 5, 10, 30, 100)]
    table = [compact_data(D, L) for D in (2, 3, 4, 6, 10)
             for L in (2, 10, 100, 1000, 10000)]
    root = Path(__file__).resolve().parent
    proof = root/"PROOF.txt"
    result = dict(status="PASS", source_proof_sha256=sha256(proof.read_bytes()).hexdigest(),
                  counted_new_jobs_only=True,
                  enumerated_cases=enumerated, grouped_cases=grouped,
                  asymptotic_table=table,
                  total_nonzero_Bell_strings=sum(x["nonzero_Bell_strings"] for x in enumerated),
                  total_exact_posterior_identities=sum(x["exact_posterior_identities"]
                                                       for x in enumerated),
                  wall_seconds=time.perf_counter()-start,
                  cpu_seconds=time.process_time()-cpu)
    (root/"RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(status=result["status"], enumerated_cases=len(enumerated),
                         grouped_cases=len(grouped), formula_cases=len(table),
                         total_nonzero_Bell_strings=result["total_nonzero_Bell_strings"],
                         total_exact_posterior_identities=result["total_exact_posterior_identities"],
                         wall_seconds=result["wall_seconds"], cpu_seconds=result["cpu_seconds"])))


if __name__ == "__main__":
    main()
