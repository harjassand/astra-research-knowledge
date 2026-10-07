"""Exact checks for the qubit arbitrary-preparation instrument/Petz cap.

The universal upper bound is proved analytically in revisions/REV2.txt.
This script verifies the tetrahedral moments, optimizer value, and exact
comparisons at the attained endpoint using SymPy arithmetic.
"""
import sympy as sp

sqrt = sp.sqrt
one = sp.Integer(1)
a = 1 / sqrt(5)
q = sqrt(1 - a**2)
s = sp.simplify((1 + 2 * q + a) / 6)
lam = sp.simplify(s**2)
expected_s = (1 + sqrt(5)) / 6
expected_lam = (3 + sqrt(5)) / 18
assert sp.simplify(q - 2 / sqrt(5)) == 0
assert sp.simplify(s - expected_s) == 0
assert sp.simplify(lam - expected_lam) == 0
assert sp.simplify(sp.Rational(2, 3) - lam - (9 - sqrt(5)) / 18) == 0

# Tetrahedron vertices n=(signs)/sqrt(3), sign product +1.
signs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
mean = [sum(v[i] for v in signs) for i in range(3)]
second = [[sum(v[i] * v[j] for v in signs) for j in range(3)] for i in range(3)]
assert mean == [0, 0, 0]
assert second == [[4 if i == j else 0 for j in range(3)] for i in range(3)]
# With n_i=sign_i/sqrt(3), the equally weighted second moment is I/3.

# For each 0<=a<=1, the Lüders Bloch shrink and prepare-branch shrink are
# t_L=(1+2*sqrt(1-a^2))/3 and t_Q=a/3. On [0,1/sqrt(5)] the scalar map
# increases continuously from 1/2 to the optimizer, so its square fills
# [1/4,(3+sqrt(5))/18]. The derivative and endpoint comparisons are exact.
a_sym = sp.symbols('a', nonnegative=True)
q_sym = sqrt(1 - a_sym**2)
s_sym = (1 + 2 * q_sym + a_sym) / 6
ds = sp.factor(sp.diff(s_sym, a_sym))
assert sp.simplify(ds.subs(a_sym, a)) == 0
assert sp.simplify(ds - (1 - 2 * a_sym / q_sym) / 6) == 0
assert sp.simplify(s_sym.subs(a_sym, 0) - sp.Rational(1, 2)) == 0
assert sp.simplify(s_sym.subs(a_sym, a) - expected_s) == 0
# The derivative is nonnegative up to a=1/sqrt(5): equivalently
# sqrt(1-a^2)>=2a, which holds there by squaring nonnegative sides.
assert sp.simplify(2 * q + a - sqrt(5)) == 0

print("exact tetrahedral branch checks passed")
print("C shrink = (1+sqrt(5))/6; Phi shrink = (3+sqrt(5))/18")
print("universal qubit-cloner shrink 2/3 is strictly above the cap")
