"""Independent exact verification from literal F and rational JSON; stdlib only.

Does not import any search, symbolic compiler, numerical solver, or prior checker.
The implications and all-degree completeness argument are in PRIMARY_PROOF.md.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
import argparse
import hashlib
import json
from pathlib import Path
import time

N = 8


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(*polynomials):
    result = {}
    for p in polynomials:
        for e, c in p.items():
            result[e] = result.get(e, F(0)) + c
    return clean(result)


def scale(p, c):
    return clean({e: c * v for e, v in p.items()})


def mul(p, q):
    result = {}
    for e, c in p.items():
        for f, d in q.items():
            g = tuple(x + y for x, y in zip(e, f))
            result[g] = result.get(g, F(0)) + c * d
    return clean(result)


def product(polynomials):
    p = {(0,) * N: F(1)}
    for q in polynomials:
        p = mul(p, q)
    return p


def diff(p, j):
    result = {}
    for e, c in p.items():
        if e[j]:
            g = list(e)
            g[j] -= 1
            result[tuple(g)] = c * e[j]
    return result


def var(j):
    e = [0] * N
    e[j] = 1
    return {tuple(e): F(1)}


def invariants(y):
    a, b, c, d = y
    return (add(mul(a, a), mul(c, c)),
            add(mul(b, b), mul(d, d)),
            add(mul(a, b), mul(c, d)),
            add(mul(a, d), scale(mul(b, c), -1)))


def energy(y):
    u, v, w, q = invariants(y)
    return add(mul(u, u), mul(v, v), scale(mul(w, w), 3),
               scale(mul(q, q), F(113, 10)),
               scale(mul(q, add(u, scale(v, -1))), 4))


def positive_ldl(Q):
    n = len(Q)
    L = [[F(i == j) for j in range(n)] for i in range(n)]
    D = []
    for j in range(n):
        pivot = Q[j][j] - sum(L[j][k] ** 2 * D[k] for k in range(j))
        assert pivot > 0, (j, pivot)
        D.append(pivot)
        for i in range(j + 1, n):
            L[i][j] = (Q[i][j] - sum(L[i][k] * D[k] * L[j][k]
                                    for k in range(j))) / pivot
    assert all(Q[i][j] == sum(L[i][k] * D[k] * L[j][k]
                              for k in range(n))
               for i in range(n) for j in range(n))
    return D


def main(write_receipt=False):
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    path = root / 'EXACT_MULTIPLIER_SUPPORT.json'
    raw = path.read_bytes()
    record = json.loads(raw)
    assert record['tau'] == '113/10'
    assert record['coefficient_vector'] == [
        '1', '1', '113/10', '-83/10', '0', '0', '4', '-4', '0']
    a = [var(j) for j in range(4)]
    x = [var(j + 4) for j in range(4)]
    apx = [add(t, s) for t, s in zip(a, x)]
    f = energy(a)
    u, v, w, q = invariants(a)
    qx = invariants(x)[3]
    normx = add(*(mul(t, t) for t in x))
    bregman = add(energy(apx), scale(f, -1),
                   *(scale(mul(diff(f, j), x[j]), -1) for j in range(4)))
    selector = add(scale(add(u, scale(v, -1)), F(record['alpha'])),
                   scale(q, F(record['delta'])))
    target = mul(normx, add(bregman, scale(mul(selector, qx), -1)))
    z = [product([ai, x[j], x[k]]) for ai in a for j, k in cwr(range(4), 2)]
    z += [product([x[i], x[j], x[k]]) for i, j, k in cwr(range(4), 3)]
    Q = [[F(c) for c in row] for row in record['gram']]
    n = len(z)
    assert n == 60 and len(Q) == n and all(len(row) == n for row in Q)
    assert all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n))
    rebuilt = {}
    span = set()
    for i in range(n):
        for j in range(i, n):
            zz = mul(z[i], z[j])
            span.update(zz)
            rebuilt = add(rebuilt, scale(zz, Q[i][j] * (1 if i == j else 2)))
    assert target == rebuilt
    assert len(span) == 658 == record['exact_polynomial_equations']
    assert all((sum(e[:4]), sum(e[4:])) in {(2, 4), (1, 5), (0, 6)}
               for e in span)
    rho = F(record['gram_margin'])
    assert rho == F(1, 200)
    D = positive_ldl([[Q[i][j] - (rho if i == j else 0)
                       for j in range(n)] for i in range(n)])
    assert D == list(map(F, record['shifted_LDL_pivots']))
    assert F(record['strict_QC_gap']) == rho / 6 == F(1, 1200)
    assert F(record['background_quadratic_coefficient']) == rho / 2 == F(1, 400)
    # Independent exact SOS decomposition of the energy itself (not its support).
    assert f == add(mul(add(u, scale(v, -1), scale(q, 2)),
                        add(u, scale(v, -1), scale(q, 2))),
                    scale(mul(w, w), 5), scale(mul(q, q), F(93, 10)))

    # Byte-identical snapshot of the parent certificate. Verify all TEN selector
    # directions, eliminating any need to assume a symmetry-reduced selector.
    dual_path = root / 'external_inputs' / 'PARENT_EXACT_SUPPORT_SEPARATOR.json'
    dual_raw = dual_path.read_bytes()
    dual = json.loads(dual_raw)
    assert dual['input_nine_coefficients'] == record['coefficient_vector']
    order = [tuple(e) for e in dual['monomial_order']]
    assert len(order) == len(set(order))
    ell = dict(zip(order, map(F, dual['lambda'])))
    assert len(ell) == len(dual['lambda'])

    def pairing(p):
        assert set(p) <= set(ell)
        return sum((c * ell[e] for e, c in p.items()), F(0))

    z2 = [mul(ai, xj) for ai in a for xj in x]
    z2 += [mul(x[i], x[j]) for i, j in cwr(range(4), 2)]
    assert len(z2) == 26
    moment = [[pairing(mul(t, s)) for s in z2] for t in z2]
    assert moment == [[F(c) for c in row] for row in dual['moment26']]
    dual_D = positive_ldl(moment)
    assert dual_D == list(map(F, dual['positive_ldl_pivots']))
    selector_pairings = [pairing(product([a[i], a[j], qx]))
                         for i, j in cwr(range(4), 2)]
    assert selector_pairings == [0] * 10
    gap = pairing(bregman)
    assert gap == F(dual['energy_pairing']) == -F(39, 125000)

    # Explicit full35-dimensional coefficient-box stability radius.
    # A quartic monomial has 11 Bregman coefficients counting multiplicity;
    # multiplying by |X|² costs a factor4. A one-entry Gram lift is available
    # for every one of the658 possible resulting monomials (span above).
    sensitivity = []
    bregman_l1_bounds = []
    for indices in cwr(range(4), 4):
        h = product([a[j] for j in indices])
        hp = product([apx[j] for j in indices])
        bh = add(hp, scale(h, -1),
                 *(scale(mul(diff(h, j), x[j]), -1) for j in range(4)))
        assert sum(abs(c) for c in bh.values()) == 11
        assert sum(abs(c) for c in mul(normx, bh).values()) == 44
        assert set(mul(normx, bh)) <= span
        bregman_l1_bounds.append(44)
        sensitivity.append(abs(pairing(bh)))
    assert len(sensitivity) == 35 and sum(bregman_l1_bounds) == 1540
    dual_sensitivity = sum(sensitivity, F(0))
    assert dual_sensitivity > 0
    positive_radius = F(1, 616000)
    negative_radius = (-gap) / (2 * dual_sensitivity)
    radius = min(positive_radius, negative_radius)
    assert radius > 0

    output = {
        'status': 'EXACT_PC_AND_ALL_DEGREE_SOS_PC_SEPARATION_VERIFIED',
        'positive_certificate_sha256': hashlib.sha256(raw).hexdigest(),
        'parent_dual_sha256': hashlib.sha256(dual_raw).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'literal_energy': 'u^2+v^2+3w^2+(113/10)q^2+4q(u-v)',
        'positive_identity': 'EXACT_FROM_LITERAL_ENERGY',
        'positive_features': n, 'exact_coefficient_span': len(span),
        'positive_shift': str(rho), 'positive_LDL_pivots': len(D),
        'selector_alpha': record['alpha'], 'selector_delta': record['delta'],
        'QC_L4_gap': str(rho / 6), 'QC_background_L2_gap': str(rho / 2),
        'dual_features': len(z2), 'dual_LDL_pivots': len(dual_D),
        'dual_energy_pairing': str(gap),
        'all_ten_quadratic_selector_pairings': list(map(str, selector_pairings)),
        'quartic_coefficient_norm': 'unweighted monomial coefficient l_infinity in four entries',
        'positive_Gram_l1_sensitivity_bound': 1540,
        'dual_absolute_coefficient_sensitivity': str(dual_sensitivity),
        'open_neighborhood_closed_box_radius': str(radius),
        'perturbed_Gram_margin': str(rho - 1540 * radius),
        'perturbed_dual_pairing_upper_bound': str(gap + radius * dual_sensitivity),
        'full_homogeneous_quartic_dimensions': 35,
        'maximum_positive_pivot_bits': max(max(abs(d.numerator).bit_length(),
                                                d.denominator.bit_length()) for d in D),
        'imports': 'PYTHON_STDLIB_ONLY',
        'wall_seconds': time.monotonic() - start,
        'scope': 'GLOBAL_PC_AND_QC_BUT_NOT_POLYNOMIAL_SOS_PC; NOT_MORREY_OR_GENERAL_NINE_COEFFICIENT_QC',
    }
    if write_receipt:
        (root / 'VERIFY_SECTOR.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-receipt', action='store_true',
                        help='replace the saved receipt; default replay is read only')
    main(parser.parse_args().write_receipt)
