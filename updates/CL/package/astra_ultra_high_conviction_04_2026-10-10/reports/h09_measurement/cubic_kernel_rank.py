"""Exact rank audit for the one-port cubic Volterra tensor map.

For distinct rational eigenvalues, this builds the common-denominator numerator
map from a fully symmetric 4-tensor to its third-order transfer function. It
also checks whether the map's nullspace intersects the fixed-partial-trace
constraint obeyed by tensors Gamma_ijkl=sum_a U_ai U_aj U_ak U_al.
Requires SymPy.
"""
from itertools import combinations_with_replacement, permutations

import sympy as sp


def tensor_map(n, eigenvalues=None):
    if eigenvalues is None:
        eigenvalues = list(range(1, n + 1))
    eigenvalues = list(map(sp.Rational, eigenvalues))
    assert len(set(eigenvalues)) == n

    s1, s2, s3 = sp.symbols("s1 s2 s3")
    z = sp.symbols("z")
    frequencies = (s1 + s2 + s3, s1, s2, s3)
    basis = combinations_with_replacement(range(n), 4)
    basis = list(basis)
    ell = [sp.prod(z + eigenvalues[m] for m in range(n) if m != i)
           for i in range(n)]

    columns = []
    monomial_set = set()
    for alpha in basis:
        expression = 0
        for ordered in set(permutations(alpha)):
            term = sp.prod(ell[index].subs({z: frequency})
                           for index, frequency in zip(ordered, frequencies))
            expression += term
        poly = sp.Poly(sp.expand(expression), s1, s2, s3)
        column = dict(poly.terms())
        monomial_set.update(column)
        columns.append(column)

    monomials = sorted(monomial_set)
    matrix = sp.Matrix([[column.get(monomial, 0) for column in columns]
                        for monomial in monomials])
    return basis, matrix


def trace_map(basis, c=None):
    n = max(max(alpha) for alpha in basis) + 1
    if c is None:
        c = [sp.Integer(1)] * n
    c = list(map(sp.Rational, c))
    assert len(c) == n and all(value != 0 for value in c)
    column_of = {alpha: j for j, alpha in enumerate(basis)}
    rows = []
    for i in range(n):
        for j in range(i, n):
            row = [sp.Integer(0)] * len(basis)
            for k in range(n):
                alpha = tuple(sorted((i, j, k, k)))
                row[column_of[alpha]] += 1 / (c[i] * c[j] * c[k] ** 2)
            rows.append(row)
    return sp.Matrix(rows)


def audit(n):
    basis, observation = tensor_map(n)
    trace = trace_map(basis)
    combined = observation.col_join(trace)
    obs_rank = observation.rank()
    physical_kernel_dim = len(basis) - combined.rank()
    print(f"n={n}: Sym^4 dimension={len(basis)}, H3 rank={obs_rank}, "
          f"H3 nullity={len(basis)-obs_rank}, "
          f"nullity after partial-trace constraint={physical_kernel_dim}")
    if n == 5:
        null = observation.nullspace()
        assert len(null) == 1
        assert trace * null[0] != sp.zeros(trace.rows, 1)
        print("  n=5: unique H3-null tensor violates the physical fixed-trace law")
    return observation, trace


if __name__ == "__main__":
    for dimension in range(2, 7):
        audit(dimension)
