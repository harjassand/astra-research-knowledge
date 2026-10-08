#!/usr/bin/env python3
"""Exact low-dimensional Racah and mixed-comparator checks for Spin(7).

Only SymPy exact algebra is used: radicals, polynomial determinants of the
multiplicity matrices (sizes at most 4), and rational polynomial identities.
There is no 512-dimensional numerical grid or floating-point calculation.
"""

from __future__ import annotations

import sympy as sp


def zero(expr: sp.Expr) -> bool:
    return sp.expand(sp.simplify(expr)) == 0


def require_identity(label: str, lhs: sp.Expr, rhs: sp.Expr) -> None:
    diff = lhs - rhs
    if isinstance(diff, sp.MatrixBase):
        diff = diff.applyfunc(lambda e: sp.factor(sp.expand(e)))
        if any(not zero(entry) for entry in diff):
            raise AssertionError(f"{label} failed: {diff}")
    else:
        diff = sp.factor(sp.expand(diff))
        if not zero(diff):
            raise AssertionError(f"{label} failed: {diff}")
    print(f"PASS {label}: difference = 0")


a, b, g, x = sp.symbols("alpha beta gamma x", real=True)
sqrt = sp.sqrt
print(f"Exact algebra backend: SymPy {sp.__version__}")

# Racah matrices in the channel orders listed in SPIN7_MIXED_AUDIT.md.
F8 = sp.Matrix(
    [
        [1, sqrt(7), sqrt(21), sqrt(35)],
        [sqrt(7), -5, 3 * sqrt(3), -sqrt(5)],
        [sqrt(21), 3 * sqrt(3), 1, -sqrt(15)],
        [sqrt(35), -sqrt(5), -sqrt(15), 3],
    ]
) / 8
F48 = sp.Matrix(
    [[1, sqrt(5), sqrt(10)], [sqrt(5), -3, sqrt(2)], [sqrt(10), sqrt(2), -2]]
) / 4
F112a = sp.Matrix([[-1, sqrt(3)], [sqrt(3), 1]]) / 2
F112b = sp.Matrix([[1]])

blocks = [
    ("8", [0, 1, 2, 3], F8),
    ("48", [1, 2, 3], F48),
    ("112a", [2, 3], F112a),
    ("112b", [3], F112b),
]

for name, _, F in blocks:
    require_identity(f"F_{name} symmetric", F, F.T)
    require_identity(f"F_{name} involution", F * F, sp.eye(F.rows))

q = [7 * a + 21 * b + 35 * g, -5 * a + 9 * b - 5 * g,
     3 * a + b - 5 * g, -a - 3 * b + 3 * g]
X = 4 * a + 12 * b + 18 * g


def signed_charpoly(F: sp.Matrix, channels: list[int], sign: int) -> sp.Expr:
    """Characteristic polynomial of D+FDF restricted to F=sign."""
    D = sp.diag(*(q[j] for j in channels))
    M = sp.simplify(D + F * D * F.T)
    eigenspace = (F - sign * sp.eye(F.rows)).nullspace()
    if not eigenspace:
        return sp.Integer(1)
    V = sp.Matrix.hstack(*eigenspace)
    # Coordinates of M|_{im V}; this works even if V is not orthonormal.
    gram = V.T * V
    restricted = sp.simplify(gram.inv() * V.T * M * V)
    require_identity(
        f"swap sign {sign}, channel invariance, dim {F.rows}",
        M * V,
        V * restricted,
    )
    return sp.factor((x * sp.eye(V.cols) - restricted).det())


expected = {
    ("8", 1): x**2 - 2 * X * x - 140 * g**2,
    ("8", -1): x**2 - (32 * b + 20 * g) * x
    - 48 * a**2 - 240 * a * g + 240 * b**2 + 240 * b * g - 300 * g**2,
    ("48", 1): x + 6 * a - 10 * b + 6 * g,
    ("48", -1): x**2 - (4 * b - 8 * g) * x
    - 20 * a**2 + 40 * a * g - 12 * b**2 + 16 * b * g - 20 * g**2,
    ("112a", 1): x + 4 * b - 2 * g,
    ("112a", -1): x - 4 * a + 6 * g,
    ("112b", 1): x + 2 * a + 6 * b - 6 * g,
}

char_count = 0
for name, channels, F in blocks:
    for sign in (1, -1):
        actual = signed_charpoly(F, channels, sign)
        if actual == 1:  # The 112b block has no antisymmetric multiplicity.
            continue
        require_identity(
            f"chi_{name},{'+' if sign > 0 else '-'} reconstructed",
            actual,
            expected[(name, sign)],
        )
        char_count += 1
assert char_count == 7
print("PASS all seven output-swap characteristic polynomials reconstructed")

# Exact square-factor identities used to compare the star root with the two
# branches of Tr(Q)+S_can(Q).
A = 8 * a + 24 * b + 38 * g
B = 7 * a + 21 * b + 42 * g
root_rad = X**2 + 140 * g**2
require_identity(
    "A-branch mixed square factor",
    (A - X) ** 2 - root_rad,
    16 * g * (a + 3 * b - 4 * g),
)
require_identity(
    "B-branch mixed square factor",
    (B - X) ** 2 - root_rad,
    7 * (4 * g - a - 3 * b) * (a + 3 * b + 4 * g),
)

# Root dominance over the other nontrivial swap blocks, as exact polynomials.
Z8 = 3 * a**2 + 15 * a * g + b**2 + 5 * b * g + 25 * g**2
require_identity(
    "8-minus root square comparison",
    (8 * a + 8 * b + 26 * g) ** 2 - 16 * Z8,
    4 * (4 * a**2 + 32 * a * b + 44 * a * g + 12 * b**2
         + 84 * b * g + 69 * g**2),
)
Z48 = 5 * (a - g) ** 2 + 4 * (b - g) ** 2
require_identity(
    "48-minus root square comparison",
    (4 * a + 11 * b + 20 * g) ** 2 - Z48,
    11 * a**2 + 88 * a * b + 170 * a * g + 117 * b**2
    + 448 * b * g + 391 * g**2,
)

# The five support tests and transfer constraints used by the common map.
l1, l2, l3, x1, x2, x3 = sp.symbols("lambda1 lambda2 lambda3 x1 x2 x3", real=True)
# Substitute x_l=2 lambda_l-1 and verify each exact conversion.
require_identity("axis-1 lambda/x conversion", 8 - 14 * l1,
                 (1 - 7 * (2 * l1 - 1)))
require_identity("axis-2 lambda/x conversion", 24 - 42 * l2,
                 3 * (1 - 7 * (2 * l2 - 1)))
require_identity("axis-3 lambda/x conversion", 42 - 70 * l3,
                 7 * (1 - 5 * (2 * l3 - 1)))
require_identity(
    "mixed test 4Pi1+Pi3 slack",
    70 - (56 * l1 + 70 * l3),
    7 * (1 - 4 * (2 * l1 - 1) - 5 * (2 * l3 - 1)),
)
require_identity(
    "mixed test (4/3)Pi2+Pi3 slack",
    70 - (56 * l2 + 70 * l3),
    7 * (1 - 4 * (2 * l2 - 1) - 5 * (2 * l3 - 1)),
)

# For r=max(0,x1,x2), the endpoint cases certify mu3 >= x3 exactly.
r = sp.symbols("r", real=True)
mu3 = (7 - 28 * r) / 35  # q=7r in the endpoint mixture
require_identity("comparator active x1 case", (mu3 - x3).subs(r, x1),
                 (1 - 4 * x1 - 5 * x3) / 5)
require_identity("comparator active x2 case", (mu3 - x3).subs(r, x2),
                 (1 - 4 * x2 - 5 * x3) / 5)
require_identity("comparator r=0 case", mu3.subs(r, 0) - x3,
                 (1 - 5 * x3) / 5)
require_identity("comparator vector-sector transfer", (7 - 4 * (7 * r)) / 35, mu3)
print("PASS comparator constraints: r=max(0,x1,x2) gives mu1=mu2=r and the three exact mu3 slacks above")
qmix = 7 * r
mu1 = qmix / 7
mu2 = qmix / 7
require_identity("comparator transfer mu1", mu1, r)
require_identity("comparator transfer mu2", mu2, r)
require_identity("comparator transfer mu3 from endpoint mixture",
                 qmix * sp.Rational(3, 35) + (1 - qmix) * sp.Rational(1, 5), mu3)

require_identity("A-B branch sign", A - B, a + 3 * b - 4 * g)
require_identity("A-X nonnegative coefficient form", A - X, 4 * a + 12 * b + 20 * g)
require_identity("B-X nonnegative coefficient form", B - X, 3 * a + 9 * b + 24 * g)

# Explicit check that the two mixed tests are sharp for h=Tr(Q)+S_can(Q)=70.
def h_value(aa: sp.Expr, bb: sp.Expr, gg: sp.Expr) -> sp.Expr:
    xx = X.subs({a: aa, b: bb, g: gg})
    return sp.simplify(xx + sqrt(xx**2 + 140 * gg**2))

require_identity("h(4,0,1)=70", h_value(4, 0, 1), 70)
require_identity("h(0,4/3,1)=70", h_value(0, sp.Rational(4, 3), 1), 70)
require_identity("TrQ on both mixed tests", 7 * 4 + 21 * 0 + 35 * 1, 63)
require_identity("TrQ on second mixed test", 7 * 0 + 21 * sp.Rational(4, 3) + 35, 63)
require_identity("canonical support on first mixed test", max(4 + 3, 7), 7)
require_identity("canonical support on second mixed test", max(sp.Rational(4, 3) * 3 + 3, 7), 7)

print(f"PASS exact checker complete: {char_count} characteristic polynomials; no floats or broad grid used")
