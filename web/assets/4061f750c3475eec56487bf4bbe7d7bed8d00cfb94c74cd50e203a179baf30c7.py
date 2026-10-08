"""Exact rational checks for the scoped two-phase CTMC alias."""
import sympy as s

S = s.Matrix([[1, 0], [s.Rational(1, 4), s.Rational(3, 4)]])
TA = s.Matrix([[-3, 1], [0, -1]])
rA = s.Matrix([2, 1])
aA = s.Matrix([[1, 0]])
TB = s.Matrix([[-s.Rational(11, 4), s.Rational(3, 4)],
               [s.Rational(7, 12), -s.Rational(5, 4)]])
rB = s.Matrix([2, s.Rational(2, 3)])
aB = s.Matrix([[1, 0]])

assert S.inv() * TA * S == TB
assert aA * S == aB
assert S.inv() * rA == rB
assert TA * s.ones(2, 1) + rA == s.zeros(2, 1)
assert TB * s.ones(2, 1) + rB == s.zeros(2, 1)
assert all(T[i, j] > 0 for T in (TA, TB) for i in range(2) for j in range(2) if i != j and T[i, j] != 0)
assert all(x > 0 for x in list(rA) + list(rB))

z = s.symbols('z', nonnegative=True)
laplace = s.factor((aA * (z * s.eye(2) - TA).inv() * rA)[0])
assert laplace == (2*z + 3)/((z + 1)*(z + 3))

u = s.symbols('u', nonnegative=True)
pA2 = (s.exp(-u) - s.exp(-3*u))/2
pB2 = s.Rational(3, 4)*pA2
gap = s.simplify(pA2-pB2)
tstar = s.log(3)/2
assert s.simplify(gap.subs(u, tstar) - 1/(12*s.sqrt(3))) == 0
assert s.simplify(s.diff(gap, u).subs(u, tstar)) == 0
n_min = s.ceiling(2*s.log(20)/(1/(12*s.sqrt(3)))**2)
assert n_min == 2589

print({"laplace": laplace, "max_gap": gap.subs(u, tstar), "t_star": tstar, "n_hoeffding": n_min})
