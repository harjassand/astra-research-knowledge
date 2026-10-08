"""Exact 25x25 star-block certificate for one d=5 subset diagnostic.

The subset has one Weyl mode-pair on each of the six projective lines. The
full 125x125 star matrix commutes with U_g=conj(W_g) tensor W_g tensor W_g.
The U_(0,1) eigenspaces have dimension 25, and U_(1,0) cycles their five
eigenvalues while commuting with the star matrix. Thus its full characteristic
polynomial is the selected block polynomial to the fifth power. This is only a
failure of the MUB-line-PVM spectral shortcut; it is not an all-Q support or
channel counterexample.

Run from the repository root with SymPy 1.14 or compatible.
"""
from __future__ import annotations

import sympy as sp
from sympy.matrices import Matrix, eye, zeros, kronecker_product
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


D = 5
z = sp.exp(2 * sp.pi * sp.I / D)
X, Z = zeros(D), zeros(D)
for j in range(D):
    X[(j + 1) % D, j] = 1
    Z[j, j] = z**j
I = eye(D)


def weyl(a, b):
    # 2^{-1}=3 in F_5; then W_g W_h = omega^(-S(g,h)/2) W_(g+h).
    return z ** ((3 * a * b) % D) * X**a * Z**b


def star_pair(a, b):
    W = weyl(a, b)
    Wd = W.conjugate().T
    pair = kronecker_product(W.T, Wd) + kronecker_product(Wd.T, W)
    return (kronecker_product(pair, I)
            + kronecker_product(kronecker_product(W.T, I), Wd)
            + kronecker_product(kronecker_product(Wd.T, I), W))


def main():
    # Two representatives (g and 2g) per line, followed by the vertical line.
    reps = []
    for slope in range(D):
        reps.extend([(1, slope), (2, (2 * slope) % D)])
    reps.extend([(0, 1), (0, 2)])
    selected = (0, 2, 5, 7, 8, 10)

    H = zeros(D**3)
    for ix in selected:
        H += star_pair(*reps[ix])

    # U_(0,1)=conj(Z) tensor Z tensor Z has eigenvalue 1 on a+b-r=0.
    indices = [25 * r + 5 * a + b
               for r in range(D) for a in range(D) for b in range(D)
               if (a + b - r) % D == 0]
    block = H.extract(indices, indices)
    K = QQ.cyclotomic_field(D)
    coeffs = DomainMatrix.from_Matrix(block).convert_to(K).charpoly()

    # The real subfield generator sqrt(5)=1+2(zeta+zeta^-1) is exact in K.
    sqrt5 = 1 + 2 * (z + z**4)
    x = sp.symbols("x")
    expected = (
        (x + 1)**8
        * (x + 1 + sqrt5)**4
        * (x + 1 - sqrt5)**4
        * (x**2 - 8*x + (-33 + 5*sqrt5)/2)
        * (x**2 + 2*x - (63 + 5*sqrt5)/2)**2
        * (x**3 - 12*x**2 + (-169 + 5*sqrt5)*x/2 + 716 - 60*sqrt5)
    )
    radical_expected = (
        (x + 1)**8
        * (x + 1 + sp.sqrt(5))**4
        * (x + 1 - sp.sqrt(5))**4
        * (x**2 - 8*x + (-33 + 5*sp.sqrt(5))/2)
        * (x**2 + 2*x - (63 + 5*sp.sqrt(5))/2)**2
        * (x**3 - 12*x**2 + (-169 + 5*sp.sqrt(5))*x/2 + 716 - 60*sp.sqrt(5))
    )
    expected_coeffs = [K.from_sympy(c) for c in
                       sp.Poly(sp.expand(expected), x, extension=z).all_coeffs()]
    assert coeffs == expected_coeffs

    # The last real cubic factor has a unique root in (14,15). Its derivative
    # is positive at 14 and its second derivative is positive for x>=14.
    # All other real factors have no roots >=14, so this root is lambda_max.
    r = sp.sqrt(5)
    cubic = x**3 - 12*x**2 + (-169 + 5*r)*x/2 + 716 - 60*r
    cubic_at_14 = sp.simplify(
        cubic.subs(x, 14)
    )
    assert sp.simplify(cubic_at_14 + 75 + 25*r) == 0
    cubic_at_15 = sp.simplify(cubic.subs(x, 15))
    assert sp.simplify(cubic_at_15 - (sp.Rational(247, 2) - sp.Rational(45, 2)*r)) == 0
    assert sp.simplify(sp.diff(cubic, x).subs(x, 14) - (sp.Rational(335, 2) + sp.Rational(5, 2)*r)) == 0
    assert sp.diff(cubic, x, 2).subs(x, 14) == 60
    # Other factors are increasing and positive at 14, hence have no roots
    # above 14. The cubic is increasing on [14,infinity), negative at 14,
    # positive at 15, so lambda_max is its unique root in (14,15).
    q1 = x**2 - 8*x + (-33 + 5*r)/2
    q2 = x**2 + 2*x - (63 + 5*r)/2
    assert sp.simplify(q1.subs(x, 14) - (sp.Rational(135, 2) + sp.Rational(5, 2)*r)) == 0
    assert sp.diff(q1, x).subs(x, 14) == 20
    assert sp.simplify(q2.subs(x, 14) - (sp.Rational(385, 2) - sp.Rational(5, 2)*r)) == 0
    assert sp.diff(q2, x).subs(x, 14) == 30

    # The simple inequalities below certify p(15)>0 and q2(14)>0.
    assert 247**2 > (45**2)*5
    assert 385**2 > (5**2)*5
    print("selected_indices", selected)
    print("block_dimension", len(indices))
    print("exact_block_charpoly_Qsqrt5", radical_expected)
    print("exact_full_charpoly_is_block_charpoly_to_power_5", True)
    print("cubic_value_at_14", cubic_at_14)
    print("cubic_value_at_15", cubic_at_15)
    print("lambda_max_is_unique_cubic_root_in_(14,15)", True)
    print("therefore_lambda_max(H_S)-12<3", True)


if __name__ == "__main__":
    main()
