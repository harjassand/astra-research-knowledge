#!/usr/bin/env python3
"""Deterministic constructive module isomorphism over F2.

Explicit splitter/Fitting algorithm of Ciocanea-Teodorescu, arXiv:1512.08365,
Section 2 (and its Brooksbank--Luks ancestry). No module elements, matrix
combinations, or field elements are enumerated. Matrices are column bitsets.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_field_root'))
from field_descent import (bits, xor_all, linear_apply, compose, flat, unflat,
                          span, solve, nullspace_rows, kernel_columns)


def identity(n):
    return [1 << i for i in range(n)]


def inverse(A):
    n = len(A)
    if len(span(A)) != n:
        return None
    return [solve(A, 1 << i) for i in range(n)]


def basis(vectors):
    return [v for v, _ in span(vectors).values()]


def matrix_basis(matrices, n):
    return [unflat(v, n) for v in basis([flat(A, n) for A in matrices])]


def matrix_power(A, k):
    out = identity(len(A))
    while k:
        if k & 1:
            out = compose(out, A)
        A = compose(A, A)
        k >>= 1
    return out


def hom_basis(source, target, m, n):
    """Hom from an m-dimensional to an n-dimensional module.

    Lists contain corresponding generator actions; no explicit ring basis is
    needed. The answer is the full F2-linear solution space B F = F A.
    """
    if len(source) != len(target):
        raise ValueError('generator lists have different lengths')
    rows = []
    for A, B in zip(source, target):
        if len(A) != m or len(B) != n:
            raise ValueError('invalid module action dimension')
        B_rows = [sum(((col >> i) & 1) << j for j, col in enumerate(B))
                  for i in range(n)]
        for j in range(m):
            for i in range(n):
                row = B_rows[i] << (n*j)
                for k in bits(A[j]):
                    row ^= 1 << (n*k+i)
                rows.append(row)
    return [[(v >> (n*j)) & ((1 << n)-1) for j in range(m)]
            for v in nullspace_rows(rows, m*n)]


def nonnilpotent_in_left_ideal(I, R, n, stats=None):
    """Return x in I that is not nilpotent, or None if I is nilpotent.

    R is a matrix algebra and I a left ideal. Stabilized ideal powers yield
    J^2=J. Descending principal left ideals then manufacture x*a=a != 0.
    """
    if stats is None:
        stats = {}
    I = matrix_basis(I, n)
    if not I:
        return None
    J = I
    for _ in range(len(R)+1):
        K = matrix_basis([compose(x, y) for x in J for y in I], n)
        stats['ideal_power_steps'] = stats.get('ideal_power_steps', 0) + 1
        if not K:
            return None
        if len(K) == len(J):
            J = K
            break
        J = K
    else:
        raise AssertionError('left-ideal powers did not stabilize')
    a = next((a for a in J if any(any(compose(x, a)) for x in J)), None)
    if a is None:
        raise AssertionError('nonzero idempotent ideal has zero square')
    for _ in range(len(R)+1):
        Ja = matrix_basis([compose(x, a) for x in J], n)
        Ra = matrix_basis([compose(x, a) for x in R], n)
        coeff = solve([flat(x, n) for x in Ja], flat(a, n))
        if coeff is not None:
            coeff = solve([flat(compose(x, a), n) for x in J], flat(a, n))
            if coeff is None:
                raise AssertionError('lost principal ideal solution')
            x = unflat(linear_apply([flat(z, n) for z in J], coeff), n)
            if compose(x, a) != a or not any(a):
                raise AssertionError('invalid nonnilpotent certificate')
            return x
        if len(Ja) >= len(Ra):
            raise AssertionError('principal ideal descent failed')
        a = next((c for c in Ja if any(any(compose(x, c)) for x in J)), None)
        if a is None:
            raise AssertionError('idempotent ideal has no descent witness')
        stats['principal_ideal_steps'] = stats.get('principal_ideal_steps', 0)+1
    raise AssertionError('principal left ideals did not descend')


def restrict_actions(actions, subspace):
    out = []
    for A in actions:
        B = [solve(subspace, linear_apply(A, x)) for x in subspace]
        if any(x is None for x in B):
            raise AssertionError('subspace is not a submodule')
        out.append(B)
    return out


def module_isomorphism(source, target, n, stats=None):
    """Manufacture an invertible intertwiner or return None.

    Both module dimensions are n. Enumeration is only over linear bases.
    Recursion decreases dimension. Output is verified against every action.
    """
    if stats is None:
        stats = {}
    if n == 0:
        return []
    F = hom_basis(source, target, n, n)
    if not F:
        return None
    stats['hom_systems'] = stats.get('hom_systems', 0)+1
    # A basis member may already be an isomorphism. This is a bounded shortcut,
    # never the only way to construct one.
    for f in F:
        if len(span(f)) == n:
            stats['direct_basis_isomorphisms'] = stats.get('direct_basis_isomorphisms', 0)+1
            return f
    G = hom_basis(target, source, n, n)
    R = hom_basis(source, source, n, n)
    stats['hom_systems'] += 2
    for f in F:
        products = [compose(g, f) for g in G]
        s = nonnilpotent_in_left_ideal(products, R, n, stats)
        if s is None:
            continue
        coeff = solve([flat(x, n) for x in products], flat(s, n))
        if coeff is None:
            raise AssertionError('splitter left original ideal')
        g = unflat(linear_apply([flat(x, n) for x in G], coeff), n)
        t = compose(f, g)
        sp, tp = matrix_power(s, n), matrix_power(t, n)
        U = basis(sp)
        W = kernel_columns(sp)
        V = kernel_columns(tp)
        fU = [linear_apply(f, u) for u in U]
        if not U or len(U)+len(W) != n or len(fU)+len(V) != n:
            raise AssertionError('incorrect Fitting decomposition')
        if len(span(U+W)) != n or len(span(fU+V)) != n:
            raise AssertionError('Fitting summands are not complementary')
        stats['splitters'] = stats.get('splitters', 0)+1
        subiso = module_isomorphism(restrict_actions(source, W),
                                   restrict_actions(target, V), len(W), stats)
        if subiso is None:
            return None
        images = fU+[linear_apply(V, x) for x in subiso]
        result = compose(images, inverse(U+W))
        if len(span(result)) != n:
            raise AssertionError('constructed module isomorphism is singular')
        if any(compose(B, result) != compose(result, A)
               for A, B in zip(source, target)):
            raise AssertionError('constructed map is not an intertwiner')
        return result
    return None


def selftest():
    # Matrix algebra M_2(F2) on its regular left module: standard Hom basis
    # consists of rank-two maps, so direct basis inspection cannot solve it.
    n = 4
    generators = []
    for i in range(2):
        for j in range(2):
            generators.append([1 << (2*i+l) if k == j else 0
                               for k in range(2) for l in range(2)])
    mixing = [3, 6, 12, 8]
    inv = inverse(mixing)
    target = [compose(mixing, compose(A, inv)) for A in generators]
    stats = {}
    result = module_isomorphism(generators, target, n, stats)
    assert result is not None and len(span(result)) == n
    assert all(compose(B, result) == compose(result, A)
               for A, B in zip(generators, target))
    assert module_isomorphism([[0, 0]], [[1, 0]], 2) is None
    return stats


if __name__ == '__main__':
    print(selftest())
