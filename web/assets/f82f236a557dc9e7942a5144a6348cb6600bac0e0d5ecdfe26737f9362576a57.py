#!/usr/bin/env python3
"""Finite diagnostics for sol_marginal_xxz/RESULT.txt.

Integer/Fraction checks for forms, cube coefficients, norm loss, and contact
inequality; NumPy checks for trigonometric/eigenvalue identities. No sampler
or all-size numerical certification. Analytic proofs remain load-bearing.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import factorial, pi
from pathlib import Path
import json
import random
import numpy as np


def configs(S, m):
    return list(combinations(range(1, S + 1), m))


def lattice_graph(S, m):
    xx = configs(S, m)
    index = {x: i for i, x in enumerate(xx)}
    edges = set()
    boundary = []
    contacts = []
    for i, x in enumerate(xx):
        occupied = set(x)
        boundary.append(int(1 in occupied) + int(S in occupied))
        contacts.append(sum(a + 1 in occupied for a in occupied))
        for a in x:
            if a + 1 <= S and a + 1 not in occupied:
                y = tuple(sorted((occupied - {a}) | {a + 1}))
                edges.add(tuple(sorted((i, index[y]))))
    return xx, sorted(edges), boundary, contacts


def matrix(S, m, boundary=True):
    xx, edges, bb, ww = lattice_graph(S, m)
    h = np.zeros((len(xx), len(xx)))
    for i, j in edges:
        h[i, i] += 2
        h[j, j] += 2
        h[i, j] -= 2
        h[j, i] -= 2
    if boundary:
        h[np.diag_indices(len(xx))] += 2 * np.array(bb)
    return h, xx, ww


def exact_energy(v, edges, bb):
    return 2 * sum((v[i] - v[j]) ** 2 for i, j in edges) + 2 * sum(b * a * a for b, a in zip(bb, v))


def main():
    stats = Counter()
    rng = random.Random(20261008)
    numerical = {'max_sine_identity_error': 0., 'min_ground_gap_residual': 0.,
                 'min_block_spin_form_residual': 0., 'min_cube_form_residual': 0.}

    # Full matrices/eigenvalues only through dimension126 in one particle block.
    for L in range(2, 11):
        S = L - 1
        phi = np.sin(pi * np.arange(1, L) / L)
        eps = 4 * (1 - np.cos(pi / L))
        for m in range(S + 1):
            h, xx, contacts = matrix(S, m)
            f = np.array([np.prod([phi[a - 1] for a in x]) for x in xx])
            target = []
            for x in xx:
                occupied = set(x)
                target.append(m * eps + 2 * sum(
                    phi[a] / phi[a - 1] + phi[a - 1] / phi[a] - 2
                    for a in x if a + 1 in occupied))
            err = float(np.max(np.abs((h @ f) / f - target)))
            assert err < 2e-12
            numerical['max_sine_identity_error'] = max(numerical['max_sine_identity_error'], err)
            eig = np.linalg.eigvalsh(h)
            resid = float(eig[0] - m * eps)
            assert resid > -2e-12
            numerical['min_ground_gap_residual'] = min(numerical['min_ground_gap_residual'], resid)
            stats['numeric_sine_identity_and_ground_sector_checks'] += 1

    # Exact rational contact-density and norm-loss fixtures, including clustered
    # basis states, uniform vectors and arbitrary signs. Fractions avoid square
    # roots by squaring only when the positive-side comparison is nontrivial.
    for L in range(3, 10):
        S = L - 1
        for m in range(2, S + 1):
            xx, edges, bb, ww = lattice_graph(S, m)
            fixture = [[F(1)] * len(xx)]
            for at in range(min(5, len(xx))):
                v = [F(0)] * len(xx)
                v[at] = 1
                fixture.append(v)
            for _ in range(12):
                v = [F(rng.randint(-5, 5), rng.randint(1, 5)) for _ in xx]
                if not any(v):
                    v[0] = 1
                fixture.append(v)
            for v in fixture:
                norm = sum(a * a for a in v)
                energy = exact_energy(v, edges, bb)
                W = sum(w * a * a for w, a in zip(ww, v))
                base = F(4 * m * (m - 1), S) * norm
                coef_sq = F(8 * m * (m - 1) ** 2)
                if W > base:
                    assert (W - base) ** 2 <= coef_sq * energy * norm
                stats['exact_contact_density_fixtures'] += 1
                image_norm = F(0)
                for x, a in zip(xx, v):
                    y = tuple(t - k for k, t in enumerate(x))
                    r = Counter(y)
                    denominator = 1
                    for value in r.values():
                        denominator *= factorial(value)
                    image_norm += a * a / denominator
                assert norm - image_norm <= W
                assert 0 < image_norm <= norm
                stats['exact_cube_norm_loss_fixtures'] += 1

    # Exhaustive exact local edge/ghost preimage coefficients in the gap map.
    for L in range(2, 13):
        S = L - 1
        for m in range(1, min(4, S) + 1):
            n = L - m
            ys = list(combinations_with_replacement(range(1, n + 1), m))
            assert len(ys) == len(configs(S, m))
            mfac = factorial(m)
            for y in ys:
                r = Counter(y)
                den = 1
                for value in r.values():
                    den *= factorial(value)
                w = mfac // den
                loss = 1 - F(1, den)
                assert 0 <= loss <= sum(a - 1 for a in r.values())
                for endpoint in (1, n):
                    if endpoint in r:
                        assert 0 < F(w * r[endpoint], mfac) <= 1
                        stats['exact_ghost_preimage_coefficients'] += 1
                for value in r:
                    if value >= n:
                        continue
                    rr = r.copy()
                    rr[value] -= 1
                    if not rr[value]:
                        del rr[value]
                    rr[value + 1] += 1
                    den2 = 1
                    for count in rr.values():
                        den2 *= factorial(count)
                    w2 = mfac // den2
                    count_edge = w * r[value]
                    assert count_edge == w2 * rr[value + 1]
                    assert 0 < F(count_edge, mfac) <= 1
                    stats['exact_hop_preimage_coefficients'] += 1

    # Direct pullback K*B K comparison as a numerical control for the exact
    # coefficient proof, with no attempt to call K an isometry.
    for L in range(2, 10):
        S = L - 1
        for m in range(1, min(4, S) + 1):
            n = L - m
            h, xx, ww = matrix(S, m)
            yy = [tuple(t - k for k, t in enumerate(x)) for x in xx]
            ix = {y: i for i, y in enumerate(yy)}
            b = np.eye(len(xx)) * (4 * m)
            D = []
            for i, y in enumerate(yy):
                r = Counter(y)
                den = np.prod([factorial(t) for t in r.values()])
                D.append(1 / den)
                for value, count in r.items():
                    if value >= n:
                        continue
                    z = list(y)
                    z.remove(value)
                    z.append(value + 1)
                    j = ix[tuple(sorted(z))]
                    off = -2 * np.sqrt(count * (r[value + 1] + 1))
                    b[i, j] = b[j, i] = off
            sqrtD = np.sqrt(D)
            pull = sqrtD[:, None] * b * sqrtD[None, :]
            resid = float(np.linalg.eigvalsh(h - pull)[0])
            assert resid > -3e-12
            numerical['min_cube_form_residual'] = min(numerical['min_cube_form_residual'], resid)
            stats['numeric_cube_form_comparisons'] += 1

    # Weak SU(2) spin-deficit comparison via complete-graph exchange, all
    # sectors through6spins. Hpath >= (2/ell^3) Hcomplete analytically.
    for ell in range(1, 7):
        for m in range(ell + 1):
            path, xx, _ = matrix(ell, m, boundary=False)
            ix = {x: i for i, x in enumerate(xx)}
            complete = np.zeros_like(path)
            edges = set()
            for i, x in enumerate(xx):
                occ = set(x)
                for a in x:
                    for q in range(1, ell + 1):
                        if q not in occ:
                            y = tuple(sorted((occ - {a}) | {q}))
                            edges.add(tuple(sorted((i, ix[y]))))
            for i, j in edges:
                complete[i, i] += 2
                complete[j, j] += 2
                complete[i, j] -= 2
                complete[j, i] -= 2
            resid = float(np.linalg.eigvalsh(path - (2 / ell ** 3) * complete)[0])
            assert resid > -3e-12
            numerical['min_block_spin_form_residual'] = min(numerical['min_block_spin_form_residual'], resid)
            stats['numeric_block_spin_deficit_comparisons'] += 1

    # Exact sine-profile Taylor coefficients, with lambda_c factored out.
    # E(A sinpi x) atlambda_c: quartic (lambda_c-3kappa)/128;
    # sextic (15kappa-lambda_c)/4608. Atkappa=lambda_c/3 it is1/1152.
    quartic_at_departure = (F(1) - 3 * F(1, 3)) / 128
    sextic_at_departure = (15 * F(1, 3) - 1) / 4608
    assert quartic_at_departure == 0 and sextic_at_departure == F(1, 1152)
    assert (1 - 3 * F(1, 2)) / 128 < 0

    receipt = {'status': 'PASS', 'counts': dict(stats), 'numerical_diagnostics': numerical,
               'classical_departure_coefficients_in_lambda_c_units': {
                   'quartic': str(quartic_at_departure), 'sextic': str(sextic_at_departure)},
               'maximum_numeric_sector_dimension': 126,
               'scope': 'Finite form/constant diagnostics only; no all-size tail test, continuum certificate, sampler or quantum phase classification'}
    path = Path(__file__).parent
    (path / 'CHECKS.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
