"""Exact rational Q1/RT0 capacity brackets for a SYNTHETIC 2D cylinder.

Domain [0,1] x periodic [0,1], q=0/1 at the left/right faces.  Every
conductivity enclosure, matrix, linear solve, energy, divergence and flux
check uses fractions/integers. Decimal outputs are for display only.

The nonseparable smooth test conductivity is
 a(x,y) = ((9-(32-64*y*y*(1-y)*(1-y))*x*(1-x))/9)**power.
Its cellwise extrema are bounded exactly by separated interval extrema.
Primal energy uses the upper conductivity bound; dual inverse energy uses
the lower bound, so the resulting bracket encloses the TRUE continuous
smooth-conductivity capacity, not only a discrete graph quantity.

No measured physical system, acquired force field or novel theorem is
claimed by this demonstration. See CAPACITY_GEOMETRY_COMPLETION.txt.
"""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import argparse
import json
import time


def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def solve_exact(A, b):
    """Bareiss elimination after per-row exact denominator clearing."""
    n = len(b)
    if not n:
        return []
    rows = []
    for row, rhs in zip(A, b):
        den = 1
        for value in list(row) + [rhs]:
            den = lcm(den, value.denominator)
        rows.append([int(value * den) for value in list(row) + [rhs]])
    previous = 1
    for k in range(n - 1):
        if rows[k][k] == 0:
            pivot_row = next(i for i in range(k + 1, n) if rows[i][k])
            rows[k], rows[pivot_row] = rows[pivot_row], rows[k]
        pivot = rows[k][k]
        assert pivot != 0
        for i in range(k + 1, n):
            entry = rows[i][k]
            for j in range(k + 1, n + 1):
                numerator = pivot * rows[i][j] - entry * rows[k][j]
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0, "Bareiss division must be exact"
                rows[i][j] = quotient
            rows[i][k] = 0
        previous = pivot
    solution = [F(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        value = F(rows[i][n]) - sum(
            (F(rows[i][j]) * solution[j] for j in range(i + 1, n)), F(0)
        )
        solution[i] = value / rows[i][i]
    assert all(
        sum((a * x for a, x in zip(row, solution)), F(0)) == rhs
        for row, rhs in zip(A, b)
    )
    return solution


def quadratic(v, A):
    return sum(
        (v[i] * A[i][j] * v[j] for i in range(len(v)) for j in range(len(v))),
        F(0),
    )


def cell_coefficients(nx, ny, power, constant=None):
    if constant is not None:
        return {(i, j): (constant, constant) for i in range(nx) for j in range(ny)}

    def arch_extrema(left, right):
        ends = (left * (1 - left), right * (1 - right))
        high = F(1, 4) if left <= F(1, 2) <= right else max(ends)
        return min(ends), high

    result = {}
    for i in range(nx):
        sx_lo, sx_hi = arch_extrema(F(i, nx), F(i + 1, nx))
        for j in range(ny):
            sy_lo, sy_hi = arch_extrema(F(j, ny), F(j + 1, ny))
            cy_lo, cy_hi = 32 - 64 * sy_hi**2, 32 - 64 * sy_lo**2
            base_lo, base_hi = 9 - cy_hi * sx_hi, 9 - cy_lo * sx_lo
            assert 1 <= base_lo <= base_hi <= 9
            result[i, j] = ((base_lo / 9)**power, (base_hi / 9)**power)
    return result


def primal(nx, ny, coefficients):
    hx, hy = F(1, nx), F(1, ny)
    nodes = [(i, j) for i in range(nx + 1) for j in range(ny)]
    index = {node: k for k, node in enumerate(nodes)}
    K = zeros(len(nodes))
    mass = ((F(1, 3), F(1, 6)), (F(1, 6), F(1, 3)))
    deriv = ((1, -1), (-1, 1))
    local = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for (i, j), (_lo, hi) in coefficients.items():
        ids = [index[i + ex, (j + ey) % ny] for ex, ey in local]
        for k, (ex, ey) in enumerate(local):
            for l, (fx, fy) in enumerate(local):
                K[ids[k]][ids[l]] += hi * (
                    hy / hx * deriv[ex][fx] * mass[ey][fy]
                    + hx / hy * mass[ex][fx] * deriv[ey][fy]
                )
    interior = [index[i, j] for i in range(1, nx) for j in range(ny)]
    right = [index[nx, j] for j in range(ny)]
    A = [[K[i][j] for j in interior] for i in interior]
    rhs = [-sum((K[i][j] for j in right), F(0)) for i in interior]
    sol = solve_exact(A, rhs)
    q = [F(0) for _ in nodes]
    for idx in right:
        q[idx] = F(1)
    for idx, value in zip(interior, sol):
        q[idx] = value
    assert all(q[index[0, j]] == 0 and q[index[nx, j]] == 1 for j in range(ny))
    energy = quadratic(q, K)
    assert energy > 0
    return energy, q, nodes


def dual(nx, ny, coefficients):
    """RT0 unit currents via a periodic Q1 stream function, one gauge fixed."""
    hx, hy = F(1, nx), F(1, ny)
    psi_nodes = [(i, j) for i in range(nx + 1) for j in range(ny) if (i, j) != (0, 0)]
    index = {node: k for k, node in enumerate(psi_nodes)}
    n = len(psi_nodes)
    K, g, constant = zeros(n), [F(0) for _ in range(n)], F(0)

    def face(kind, i, j):
        if kind == 'x':
            terms = (((i, (j + 1) % ny), 1 / hy), ((i, j), -1 / hy))
            c = F(1)  # unit width in y; net first-coordinate flux is one
        else:
            terms = (((i + 1, j), -1 / hx), ((i, j), 1 / hx))
            c = F(0)
        row = {}
        for node, weight in terms:
            if node in index:
                k = index[node]
                row[k] = row.get(k, F(0)) + weight
        return c, {k: v for k, v in row.items() if v}

    for (i, j), (lo, _hi) in coefficients.items():
        pairs = [
            (face('x', i, j), face('x', i + 1, j)),
            (face('y', i, j), face('y', i, (j + 1) % ny)),
        ]
        for pair in pairs:
            for u in range(2):
                for v in range(2):
                    w = hx * hy / lo * (F(1, 3) if u == v else F(1, 6))
                    cu, bu = pair[u]
                    cv, bv = pair[v]
                    constant += w * cu * cv
                    for a, ba in bu.items():
                        g[a] += w * ba * cv
                        for b, bb in bv.items():
                            K[a][b] += w * ba * bb
    psi = solve_exact(K, [-v for v in g])

    def value(kind, i, j):
        c, row = face(kind, i, j)
        return c + sum((weight * psi[k] for k, weight in row.items()), F(0))

    energy = F(0)
    for (i, j), (lo, _hi) in coefficients.items():
        left, right = value('x', i, j), value('x', i + 1, j)
        bottom, top = value('y', i, j), value('y', i, (j + 1) % ny)
        assert hy * (right - left) + hx * (top - bottom) == 0
        energy += hx * hy / lo * (
            (left * left + left * right + right * right) / 3
            + (bottom * bottom + bottom * top + top * top) / 3
        )
    for i in range(nx + 1):
        assert hy * sum((value('x', i, j) for j in range(ny)), F(0)) == 1
    optimized = constant + sum((a * b for a, b in zip(g, psi)), F(0))
    assert energy == optimized > 0
    return energy, psi, psi_nodes


def encode_fraction(x):
    return {'numerator': str(x.numerator), 'denominator': str(x.denominator),
            'decimal': float(x), 'numerator_bits': x.numerator.bit_length(),
            'denominator_bits': x.denominator.bit_length()}


def run_case(n, power=1, constant=None):
    start = time.perf_counter()
    co = cell_coefficients(n, n, power, constant)
    upper, q, _ = primal(n, n, co)
    resistance, psi, _ = dual(n, n, co)
    lower = 1 / resistance
    assert 0 < lower <= upper
    if constant is not None:
        assert lower == upper == constant
    return {'synthetic': True, 'mesh': [n, n], 'power': power,
            'constant_conductivity': str(constant) if constant is not None else None,
            'capacity_lower': encode_fraction(lower),
            'capacity_upper': encode_fraction(upper),
            'bracket_ratio': encode_fraction(upper / lower),
            'all_divergence_flux_and_linear_solve_checks_exact': True,
            'primal_unknowns': (n - 1) * n,
            'dual_stream_unknowns': (n + 1) * n - 1,
            'elapsed_seconds': time.perf_counter() - start}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-grid', type=int, default=6)
    args = parser.parse_args()
    results = [run_case(2, constant=F(7, 3))]
    print(json.dumps({'constant_case': results[-1]['capacity_lower']['decimal'],
                      'exact': True}), flush=True)
    for power in (1, 4):
        for n in (2, 4, 6, 8):
            if n > args.max_grid:
                continue
            r = run_case(n, power)
            results.append(r)
            print(json.dumps({'mesh': n, 'power': power,
                              'lower': r['capacity_lower']['decimal'],
                              'upper': r['capacity_upper']['decimal'],
                              'ratio': r['bracket_ratio']['decimal'],
                              'seconds': r['elapsed_seconds']}), flush=True)
    path = Path(__file__).with_name('capacity_geometry_exact_results.json')
    path.write_text(json.dumps({'description': 'SYNTHETIC smooth nonseparable cylinder; exact rational continuous-capacity brackets',
                               'results': results}, indent=2) + '\n')


if __name__ == '__main__':
    main()
