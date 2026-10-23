#!/usr/bin/env python3
"""Small scalar admissions; the general theorem is the separate analytic proof."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def entropy(vals):
    return -sum(float(v) * math.log(float(v)) for v in vals if v)


def normalize(weights):
    total = sum(weights)
    return tuple(F(x, total) for x in weights)


def joint_kj(D, p):
    q, L = F(1, D * D), len(p)
    out = {}
    for k, pk in enumerate(p, 1):
        if not pk:
            continue
        for j in range(k, L + 1):
            out[(k, j)] = pk * q ** (j - k) * (1 if j == L else 1 - q)
    assert sum(out.values()) == 1
    return out


def scalar_admissions():
    counts = dict(priors=0, exact_joint_cells=0, entropy_identities=0,
                  posterior_cells=0, exact_mean_bounds=0)
    examples = []
    for D in range(2, 9):
        q = F(1, D * D)
        c = -math.log(1 - float(q)) - float(q / (1 - q)) * math.log(float(q))
        for L in range(2, 10):
            raw = [tuple(1 for _ in range(L)),
                   tuple(1 if k == 0 else 0 for k in range(L)),
                   tuple(1 if k == L - 1 else 0 for k in range(L)),
                   tuple(2 ** k for k in range(L)),
                   tuple(3 ** (L - 1 - k) for k in range(L)),
                   tuple(1 + ((k + 3) * (L + D + 1)) % 13 for k in range(L)),
                   tuple(999 if k == 0 else (1 if k == 1 else 0)
                         for k in range(L))]
            for weights in raw:
                p = normalize(weights)
                kj = joint_kj(D, p)
                pj, pg = defaultdict(F), defaultdict(F)
                for (k, j), val in kj.items():
                    pj[j] += val
                    pg[j - k] += val
                mean_g = sum(g * val for g, val in pg.items())
                assert mean_g <= q / (1 - q)
                C = entropy(kj.values()) - entropy(pj.values())
                assert -1e-12 <= C <= entropy(p) + 1e-12
                assert C <= entropy(pg.values()) + 1e-12 <= c + 1e-12
                direct_C = 0.0
                direct_hy = 0.0
                for j in range(1, L + 1):
                    sj = sum(p[k - 1] * q ** (j - k) for k in range(1, j + 1))
                    expected_j = sj if j == L else (1 - q) * sj
                    assert pj[j] == expected_j
                    if sj:
                        post = []
                        for k in range(1, j + 1):
                            val = p[k - 1] * q ** (j - k) / sj
                            assert kj.get((k, j), F(0)) / pj[j] == val
                            post.append(val)
                            counts['posterior_cells'] += 1
                        direct_C += float(pj[j]) * entropy(post)
                        one_label = q ** (L - j) * sj
                        multiplicity = (1 if j == L else
                                        (D * D - 1) * (D * D) ** (L - j - 1))
                        assert multiplicity * one_label == pj[j]
                        direct_hy -= multiplicity * float(one_label) * math.log(float(one_label))
                assert math.isclose(C, direct_C, rel_tol=1e-10, abs_tol=1e-12)
                EK = sum((k + 1) * val for k, val in enumerate(p))
                chain_hy = 2 * (L - float(EK)) * math.log(D) + entropy(p) - C
                assert math.isclose(direct_hy, chain_hy, rel_tol=1e-12, abs_tol=2e-12)
                U = float(EK) * math.log(D) - entropy(p) / 2 + C / 2
                assert U >= -1e-12
                counts['priors'] += 1
                counts['exact_joint_cells'] += len(kj)
                counts['entropy_identities'] += 2
                counts['exact_mean_bounds'] += 1
                if D == 2 and L in (2, 9) and weights == raw[-1]:
                    examples.append(dict(D=D, L=L, p=[str(x) for x in p],
                                         entropy=entropy(p), C=C, U=U))
    return counts, examples


def access_admissions():
    counts = dict(vector_access_cases=0, exact_cells=0)
    for D in (2, 3, 5):
        q = F(1, D * D)
        for L in range(2, 5):
            for p in (normalize([1] * L), normalize([2 ** k for k in range(L)])):
                kj = joint_kj(D, p)
                C = entropy(kj.values()) - entropy(
                    [sum(v for (_, j2), v in kj.items() if j2 == j)
                     for j in range(1, L + 1)])
                for mode in ('none', 'parity', 'full', 'random_erasure'):
                    joint = defaultdict(F)
                    for ((k1, j1), a), ((k2, j2), b) in product(kj.items(), repeat=2):
                        kv, jv = (k1, k2), (j1, j2)
                        if mode == 'none':
                            labels = ((0, F(1)),)
                        elif mode == 'parity':
                            labels = (((k1 + k2) % 2, F(1)),)
                        elif mode == 'full':
                            labels = ((kv, F(1)),)
                        else:
                            labels = ((('erased',), F(2, 3)), (kv, F(1, 3)))
                        for z, prob in labels:
                            joint[(kv, jv, z)] += a * b * prob
                    assert sum(joint.values()) == 1
                    kz, jz, pz = defaultdict(F), defaultdict(F), defaultdict(F)
                    for (kv, jv, z), val in joint.items():
                        kz[(kv, z)] += val
                        jz[(jv, z)] += val
                        pz[z] += val
                    hKZ = entropy(kz.values()) - entropy(pz.values())
                    hKJZ = entropy(joint.values()) - entropy(jz.values())
                    info = hKZ - hKJZ
                    pj = defaultdict(F)
                    for (jv, z), val in jz.items():
                        pj[jv] += val
                    iYZ = entropy(pj.values()) + entropy(pz.values()) - entropy(jz.values())
                    iKY = 2 * (entropy(p) - C)
                    assert math.isclose(info, iKY - iYZ, rel_tol=1e-10, abs_tol=3e-12)
                    assert hKJZ <= 2 * C + 3e-12
                    assert info >= -3e-12
                    assert info >= hKZ - 2 * C - 3e-12
                    if mode == 'full':
                        assert abs(info) <= 3e-12
                    counts['vector_access_cases'] += 1
                    counts['exact_cells'] += len(joint)
    return counts


def finite_separability_admissions():
    counts = dict(phase_moment_entries=0, isotropic_endpoints=0)
    examples = []
    for D in range(2, 9):
        for i, j, k, ell in product(range(D), repeat=4):
            exponents = [0] * D
            exponents[i] += 1
            exponents[j] -= 1
            exponents[k] -= 1
            exponents[ell] += 1
            phase_entry = F(int(all(e % 4 == 0 for e in exponents)), D * D)
            ident = int(i == k and j == ell)
            bellD = int(i == j and k == ell)
            delta = int(i == j == k == ell)
            assert phase_entry == F(ident + bellD - delta, D * D)
            endpoint = F(D, D + 1) * phase_entry + F(delta, D * (D + 1))
            assert endpoint == F(ident + bellD, D * (D + 1))
            counts['phase_moment_entries'] += 1
        p = F(1, D + 1)
        assert 1 - p == F(D, D + 1)
        counts['isotropic_endpoints'] += 1
        for exponent in (2, 4, 8, 16, 32):
            prob = F(1, (D + 1) * 2 ** exponent)
            hp = entropy([prob, 1 - prob])
            gap = float(prob) * math.log(D)
            examples.append(dict(D=D, p=str(prob), entropy=hp, exact_gap_nats=gap,
                                 gap_over_entropy=gap / hp))
    return counts, examples


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    c1, examples = scalar_admissions()
    c2 = access_admissions()
    c3, counterexamples = finite_separability_admissions()
    proof = HERE / 'PROOF.txt'
    result = dict(status='PASS', scope='finite admissions only; analytic proofs in PROOF.txt',
                  source_proof_sha256='41776adc6c19232d2db53adf4e628c680f61f6b7cf08b6ddd24c612db3cb633c',
                  lemma_proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),
                  counts={**c1, **c2, **c3}, prior_examples=examples,
                  low_entropy_exact_counterexamples=counterexamples)
    (HERE / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    timings = dict(wall_seconds=time.perf_counter() - wall,
                   cpu_seconds=time.process_time() - cpu)
    (HERE / 'TIMING.json').write_text(json.dumps(timings, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=result['status'], counts=result['counts'], **timings), sort_keys=True))


if __name__ == '__main__':
    main()
