#!/usr/bin/env python3
"""Exact checks for signed transport; no LP oracle or floating arithmetic."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


def mat(a):
    return [[F(v) for v in row] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inv(a):
    n = len(a)
    aug = [list(row) + ident for row, ident in zip(a, eye(n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        d = aug[j][j]
        aug[j] = [v/d for v in aug[j]]
        for i in range(n):
            if i != j:
                d = aug[i][j]
                aug[i] = [v-d*w for v, w in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def nonnegative(a):
    return all(v >= 0 for row in a for v in row)


def sub(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def serial(a):
    return [[str(v) for v in row] for row in a]


def repair(q, r0, v):
    assert mul(q, [[w] for w in v]) == [[F(0)] for _ in q]
    assert all(w > 0 for w in v)
    assert mul(q, r0) == eye(len(q))
    shifts = [max([F(0)] + [-r0[j][i]/v[j] for j in range(len(v))])
              for i in range(len(q))]
    result = [[r0[j][i] + v[j]*shifts[i] for i in range(len(q))]
              for j in range(len(v))]
    assert nonnegative(result)
    assert mul(q, result) == eye(len(q))
    return result, shifts


def main():
    checks = {}
    q = mat([[1, 1, -1], [-1, 1, 0], [0, -1, 1]])
    qi = inv(q)
    assert qi == mat([[1, 0, 1], [1, 1, 1], [1, 1, 2]])
    checks['signed_inverse_positive_example'] = {'Q': serial(q), 'inverse': serial(qi)}

    # Row/column permutations only permute inverse entries and cannot repair signs.
    q = [[F(v, 2) for v in row]
         for row in [[1, -1, 1], [1, 1, -1], [-1, 1, 1]]]
    qi = inv(q)
    assert qi == mat([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    bad = []
    for rr in combinations(range(3), 2):
        for cc in combinations(range(3), 2):
            h = inv(sub(q, rr, cc))
            assert h is None or not nonnegative(h)
            bad.append({'rows': rr, 'cols': cc, 'inverse': None if h is None else serial(h)})
    checks['no_two_by_two_acquisition'] = {'Q': serial(q), 'inverse': serial(qi), 'subblocks': bad}

    # A rectangular block has an explicit nonnegative right inverse but no
    # square inverse-positive basis, even though every triple is invertible.
    q = mat([[5, 5, -3, -3], [2, -4, 6, 0], [-4, 2, 0, 6]])
    r = mat([[F(1, 8), F(3, 32), F(1, 32)],
             [F(1, 8), F(1, 32), F(3, 32)],
             [F(1, 24), F(5, 32), F(5, 96)],
             [F(1, 24), F(5, 96), F(5, 32)]])
    assert mul(q, r) == eye(3) and nonnegative(r)
    bases = []
    for cc in combinations(range(4), 3):
        h = inv(sub(q, range(3), cc))
        assert h is not None and not nonnegative(h)
        bases.append({'cols': cc, 'inverse': serial(h)})
    checks['right_inverse_without_monotone_basis'] = {'Q': serial(q), 'R': serial(r), 'bases': bases}

    q = mat([[1, -2, 1], [-2, 1, 1]])
    h = inv(sub(q, range(2), range(2)))
    r0 = h + [[F(0), F(0)]]
    r, shifts = repair(q, r0, [F(1)]*3)
    checks['positive_circulation_repair'] = {'Q': serial(q), 'R0': serial(r0),
                                             'R': serial(r), 'shifts': [str(v) for v in shifts]}

    # The repair operation is feasible but need not maximize profit, even with
    # a supplied positive circulation and a finite optimum.
    q = mat([[1, 1, -1]])
    r0 = mat([[1], [0], [0]])
    r, shifts = repair(q, r0, [F(1), F(1), F(2)])
    p = mat([[1, 2, -3]])
    x = mat([[1]])
    u = mul(r, x)
    alternative = mat([[0], [1], [0]])
    assert mul(q, alternative) == x
    assert mul(p, u) == [[F(1)]] and mul(p, alternative) == [[F(2)]]
    # Eliminating u1 = 1-u2+u3 gives profit 1+u2-2u3 <= 2-u3 <=2.
    checks['repair_misses_finite_optimum'] = {'Q': serial(q), 'p': serial(p),
                                            'repair': serial(u), 'better': serial(alternative),
                                            'optimum': '2'}

    # A literal instance of the all-ones-circulation LP embedding.
    a = mat([[1, 1]])
    c = mat([[1, 2]])
    q = mat([[1, 1, -2]])
    p = mat([[1, 2, -4]])
    assert mul(q, mat([[1], [1], [1]])) == [[F(0)]]
    assert mul(p, mat([[0], [1], [0]])) == [[F(2)]]
    # Q u=1 gives u1+u2=1+2t; p u=1+u2-2t<=2, equality forces u1=0,
    # but t remains neutral for this M. Choose M=5 for strict forced t=0.
    p = mat([[1, 2, -5]])
    assert mul(p, mat([[0], [1], [0]])) == [[F(2)]]
    checks['all_ones_circulation_embedding_example'] = {'Q': serial(q), 'p': serial(p),
                                                       'unique_optimal_appended_rate': '0'}

    # A negative-profit supplied circulation does not rule out another
    # positive-profit recession direction.
    q = mat([[1, 1, -1]])
    p = mat([[4, 0, -3]])
    v = mat([[1], [1], [2]])
    d = mat([[1], [0], [1]])
    assert mul(q, v) == [[F(0)]] and mul(q, d) == [[F(0)]]
    assert mul(p, v) == [[F(-2)]] and mul(p, d) == [[F(1)]]
    checks['negative_anchor_does_not_certify_boundedness'] = {
        'Q': serial(q), 'p': serial(p), 'negative_anchor': serial(v),
        'profitable_recession': serial(d)}

    # The augmented objective-resource block loses the positive circulation.
    q_aug = mat([[1, 1, -1], [1, 2, -3]])
    null = mat([[1], [-2], [-1]])
    assert mul(q_aug, null) == mat([[0], [0]])
    assert inv(sub(q_aug, range(2), range(2))) is not None
    assert any(row[0] < 0 for row in null) and any(row[0] > 0 for row in null)
    checks['objective_augmentation_mixed_nullspace'] = {
        'augmented_Q': serial(q_aug), 'nullspace_generator': serial(null)}

    # Discarding the most negative cost coordinate discards the unique optimum.
    q = mat([[100, 1, -101]])
    p = mat([[-10, -1, 1]])
    best = mat([[F(1, 100)], [0], [0]])
    assert mul(q, mat([[1], [1], [1]])) == [[F(0)]]
    assert mul(q, best) == [[F(1)]] and mul(p, best) == [[F(-1, 10)]]
    assert p[0].index(min(p[0])) == 0
    # Substitution into the objective gives -1/10 -(9/10)u2 -(91/10)u3.
    residual = [F(0), -F(9, 10), -F(91, 10)]
    assert p[0] == [-F(1, 10)*q[0][j] + residual[j] for j in range(3)]
    checks['cheapest_coordinate_is_indispensable'] = {
        'Q': serial(q), 'p': serial(p), 'unique_optimum': serial(best),
        'optimal_profit': '-1/10'}

    # In corank one the minimal scalar repair is globally optimal for negative
    # circulation profit. Here all solutions are (-1,-1,0)+t*(1,1,1), t>=1.
    q = mat([[1, -2, 1], [-2, 1, 1]])
    p = mat([[1, 0, -2]])
    u0 = mat([[-1], [-1], [0]])
    v = mat([[1], [1], [1]])
    assert mul(q, u0) == mat([[1], [1]])
    assert mul(q, v) == mat([[0], [0]]) and mul(p, v) == [[F(-1)]]
    t = max(-row[0] for row in u0)
    best = [[u0[j][0] + t*v[j][0]] for j in range(3)]
    assert t == 1 and best == mat([[0], [0], [1]])
    assert mul(p, best) == [[F(-2)]]
    checks['corank_one_exact_optimal_repair'] = {
        'Q': serial(q), 'p': serial(p), 'particular_solution': serial(u0),
        'circulation': serial(v), 'optimal_scalar': str(t), 'optimum': serial(best)}

    dest = Path(__file__).with_name('checks.json')
    dest.write_text(json.dumps(checks, indent=2) + '\n')
    print(f'PASS: {len(checks)} exact check groups; wrote {dest}')


if __name__ == '__main__':
    main()
