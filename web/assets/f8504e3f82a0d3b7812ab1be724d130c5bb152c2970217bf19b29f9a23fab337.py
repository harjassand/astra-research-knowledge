"""Acquire and verify a rank-perturbation certificate, then sample prefixes."""
from fractions import Fraction
from random import Random
from pathlib import Path
import json
from near_monomial_dp import G, determinant
from rank_monomial_mpo import counts, full_matrix


def qdiv(x, y):
    d = Fraction(y.abs2())
    return G(Fraction(x.re * y.re + x.im * y.im) / d,
             Fraction(x.im * y.re - x.re * y.im) / d)


def acquire_factor(F, p, d):
    n = len(F)
    assert sorted(p) == list(range(n)) and len(d) == n
    conv = lambda x: x if isinstance(x, G) else G(x)
    residual = [[conv(x) for x in row] for row in F]
    for i in range(n): residual[i][p[i]] -= conv(d[i])
    R = [row[:] for row in residual]
    pivots = []; rank = 0
    for j in range(n):
        pivot = next((i for i in range(rank, n) if R[i][j]), None)
        if pivot is None: continue
        R[rank], R[pivot] = R[pivot], R[rank]
        den = R[rank][j]
        R[rank] = [qdiv(x, den) for x in R[rank]]
        for i in range(n):
            if i == rank or not R[i][j]: continue
            scale = R[i][j]
            R[i] = [x - scale * y for x, y in zip(R[i], R[rank])]
        pivots.append(j); rank += 1
    U = [[residual[i][j] for j in pivots] for i in range(n)]
    V = [[R[a][j] for a in range(rank)] for j in range(n)]
    assert all(sum((U[i][a] * V[j][a] for a in range(rank)), G()) == residual[i][j]
               for i in range(n) for j in range(n))
    return U, V


def exact_sample(p, d, U, V, k, rng, activities=None):
    rows, cols = {}, {}
    states = ((0, 0), (1, 0), (0, 1))
    for i in range(len(p)):
        masses = []
        for ri, ci in states:
            rc, cc = dict(rows), dict(cols)
            rc[i], cc[i] = ri, ci
            z, _ = counts(p, d, U, V, activities, rc, cc)
            masses.append(Fraction(z[k]))
        total = sum(masses)
        if not total: raise ValueError('zero norm conditional sector')
        # Integerize arbitrary exact rational masses before fair-bit rejection.
        from math import lcm
        den = lcm(*(m.denominator for m in masses))
        weights = [int(m * den) for m in masses]
        draw = rng.randrange(sum(weights))
        for state, mass in zip(states, weights):
            if draw < mass:
                rows[i], cols[i] = state
                break
            draw -= mass
    return tuple(i for i, v in rows.items() if v), tuple(i for i, v in cols.items() if v)


def run_checks():
    p = [1, 2, 3, 0]
    d = [G(1), G(1, 1), G(-1), G(1)]
    U = [[G(1), G(0, 1)], [G(-1), G(1)], [G(1, 1), G(2)], [G(0), G(-1)]]
    V = [[G(1), G(-1)], [G(2), G(1, 1)], [G(0, 1), G(1)], [G(-1), G(0, 1)]]
    F = full_matrix(p, d, U, V)
    U2, V2 = acquire_factor(F, p, d)
    assert len(U2[0]) == 2
    assert full_matrix(p, d, U2, V2) == F
    z, _ = counts(p, d, U, V)
    zz, _ = counts(p, d, U2, V2)
    assert z == zz
    rng = Random(61304)
    samples = []
    for k in (1, 2):
        I, J = exact_sample(p, d, U2, V2, k, rng)
        assert not set(I) & set(J) and len(I) == len(J) == k
        assert determinant([[F[i][j] for j in J] for i in I]).abs2() > 0
        samples.append({'k': k, 'I': I, 'J': J})
    return {'status': 'PASS', 'seed': 61304, 'acquired_rank': 2,
            'exact_norms': [str(x) for x in zz], 'support_valid_samples': samples,
            'scope': 'One exact rational rank-factor acquisition and two support-valid prefix samples; not a statistical sampling benchmark.'}


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('rank_certificate_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
