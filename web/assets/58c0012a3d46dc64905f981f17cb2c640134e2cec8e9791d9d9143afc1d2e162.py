"""Duplicated d=3 control only; not a C8 advance beyond the prime-d line theorem.

Retained as a prior finite control after the branch pivoted to the unexplored
d=5 non-line-constant channel. No new d=3 claim is made here.
"""
import sympy as s
from sympy.matrices import Matrix, eye, zeros, kronecker_product
from sympy import sqrt
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

d = 3
omega = (-1 + s.sqrt(-3)) / 2
X = Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
Z = Matrix.diag(1, omega, omega**2)
I = eye(3)
reps = [(0, 1), (1, 0), (1, 1), (1, 2)]

def matrix_power(A, n):
    out = eye(A.rows)
    for _ in range(n):
        out = out * A
    return out

def star_line(a, b):
    W = matrix_power(X, a) * matrix_power(Z, b)
    Wdag = W.conjugate().T
    pair = kronecker_product(W.T, Wdag) + kronecker_product(Wdag.T, W)
    return kronecker_product(pair, I) + kronecker_product(kronecker_product(W.T, I), Wdag) + kronecker_product(kronecker_product(Wdag.T, I), W)

def main():
    x = s.symbols("x")
    lines = [star_line(*g) for g in reps]
    basis = [(r, a, b) for r in range(3) for a in range(3) for b in range(3) if (a + b - r) % 3 == 0]
    ix = [9*r + 3*a + b for r, a, b in basis]
    for subset in ((0,), (0, 1), (0, 1, 2), (0, 1, 2, 3)):
        H = sum((lines[i] for i in subset), zeros(27))
        block = H.extract(ix, ix)
        K = QQ.algebraic_field(s.sqrt(-3))
        dm = DomainMatrix.from_Matrix(block).convert_to(K)
        coefficients = dm.charpoly()
        poly = s.Poly.from_list([K.to_sympy(c) for c in coefficients], gens=x, extension=s.sqrt(-3))
        print("subset", subset, "block_charpoly", s.factor(poly.as_expr(), extension=s.sqrt(-3)))

if __name__ == "__main__":
    main()
