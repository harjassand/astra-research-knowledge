"""Reproduce the exact 4x4 composed-operator factorization in the report."""
import sympy as sp

P1 = P2 = sp.Matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
])
Q1 = sp.Matrix([
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
])
Q2 = sp.Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, -1],
])
A1, A2 = P1 * Q1, P2 * Q2
A3 = sp.Matrix([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1],
])
M = A3 * A2 * A1
Omega = sp.Matrix([
    [-3, 0],
    [-3, 3],
    [0, -2],
    [2, -3],
])
Psi = sp.Matrix([
    [-2, -3, 1, -2],
    [2, 3, -2, -2],
])
Y, Z = M * Omega, Psi * M
G = Psi * Y

# The two independent rows of G give a square exact solve for X.
independent_rows = list(G.T.rref()[1])
X = G[independent_rows, :].inv() * Z[independent_rows, :]

assert [A1.rank(), A2.rank(), A3.rank(), M.rank()] == [3, 3, 3, 2]
assert Y.rank() == G.rank() == 2
assert G * X == Z
assert Y * X == M
print("local ranks:", A1.rank(), A2.rank(), A3.rank())
print("global rank:", M.rank())
print("G:", G)
print("X:", X)
print("exact residual M - YX:", M - Y * X)
