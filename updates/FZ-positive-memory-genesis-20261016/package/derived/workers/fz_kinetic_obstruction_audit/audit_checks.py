"""Bounded independent algebraic audit. No stochastic simulations or FSP runs.

Fixed matrices have size at most four. Exact assertions use SymPy rationals.
The few deadline illustrations evaluate the proved 2x2/3x3 formulas with mpmath;
they are numerical illustrations, not interval certificates.
"""
from pathlib import Path
import json
import platform
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parent
k, d = s.symbols("k d", positive=True)
checks = []


def check(name, value):
    assert bool(value), name
    checks.append(name)


def kmatrix(S, a, escape=k):
    n = S.rows
    Sa = S * a
    return s.Matrix(n, n, lambda i, j: S[i, j] * (Sa[i] + escape) /
                    ((1 + escape) ** 2 * a[j]))


a2 = s.Matrix([1 + d, 1 - d])
M2 = s.zeros(2)
for i in range(2):
    j = 1 - i
    M2[i, j] = a2[i] / a2[j]
    M2[i, i] = (a2[j] + k) / a2[i] - 2 * (1 + k)
ctcrit = k / (4 * (1 + k))
check("CT determinant independently rebuilt", s.factor(M2.det() -
      (k + 2) * (k - 4 * (1 + k) * d ** 2) / (1 - d ** 2)) == 0)
trace_formula = (-2 - 2 * k + (6 + 4 * k) * d ** 2) / (1 - d ** 2)
check("CT trace independently rebuilt", s.factor(s.trace(M2) - trace_formula) == 0)
trace_at_boundary = s.factor((-2 - 2 * k + (6 + 4 * k) * ctcrit) / (1 - ctcrit))
check("CT boundary trace strictly negative", trace_at_boundary.is_negative)
K2 = kmatrix(s.Matrix([[0, 1], [1, 0]]), a2)
rho2 = s.factor(K2[0, 1] * K2[1, 0])
gap2 = k * (k + 2) * ((1 + k) ** 2 -
       ((1 + k) ** 2 + 1) * d ** 2) / ((1 + k) ** 4 * (1 - d ** 2))
check("embedded two-state stability gap", s.factor(1 - rho2 - gap2) == 0)

# Row-stochastic, zero-diagonal, nonuniform irreducible routing.
S = s.Matrix([[0, s.Rational(1, 3), s.Rational(2, 3)],
              [s.Rational(1, 4), 0, s.Rational(3, 4)],
              [s.Rational(2, 5), s.Rational(3, 5), 0]])
f = s.Matrix([2, -1, 3])
p0, p1, p2 = s.symbols("p0 p1 p2")
pi_col = s.Matrix([p0, p1, p2])
sol = s.solve(list((S.T - s.eye(3)) * pi_col) + [sum(pi_col) - 1],
              [p0, p1, p2])
pi = pi_col.subs(sol).T
var = S * f.applyfunc(lambda x: x ** 2) - (S * f).applyfunc(lambda x: x ** 2)
sigma2 = s.factor((pi * var)[0])
a = s.ones(3, 1) + d * f
K0 = kmatrix(S, a, s.Integer(0))
check("routing K first derivative annihilates one", all(
      s.diff(z, d).subs(d, 0) == 0 for z in K0 * s.ones(3, 1)))
check("routing K second row coefficient equals conditional variance", all(
      s.factor(s.diff((K0 * s.ones(3, 1))[i], d, 2).subs(d, 0) / 2 - var[i]) == 0
      for i in range(3)))
characteristic = s.factor(((1 + sigma2 * d ** 2) * s.eye(3) - K0).det())
check("stationary variance coefficient cancels eigenvalue equation through order two",
      all(s.factor(s.diff(characteristic, d, j).subs(d, 0)) == 0 for j in range(3)))
check("escape derivative is minus one at exact committor", all(
      s.factor(z) == 0 for z in kmatrix(S, s.ones(3, 1)) - S / (1 + k)))

# An irreducible period-two chain can branch without changing relative routing.
Sp = s.Matrix([[0, 0, s.Rational(1, 2), s.Rational(1, 2)],
               [0, 0, s.Rational(1, 2), s.Rational(1, 2)],
               [s.Rational(1, 2), s.Rational(1, 2), 0, 0],
               [s.Rational(1, 2), s.Rational(1, 2), 0, 0]])
ap = s.Matrix([1 + d, 1 + d, 1 - d, 1 - d])
Kp0 = kmatrix(Sp, ap, s.Integer(0))
check("periodic branching exception K0 equals S", all(s.factor(z) == 0 for z in Kp0 - Sp))
Kp = kmatrix(Sp, ap)
check("periodic branching exception has two-state Perron-square law",
      s.factor(4 * Kp[0, 2] * Kp[2, 0] - rho2) == 0)
fp = s.Matrix([1, -1, 0, 0])
vp = Sp * fp.applyfunc(lambda x: x ** 2) - (Sp * fp).applyfunc(lambda x: x ** 2)
check("periodic branching with within-row variation has positive coefficient",
      sum(vp) / 4 == s.Rational(1, 2))

# Sharp Cauchy-Schwarz example; the analytic proof applies to arbitrary paths.
P = [s.Rational(1, 2), s.Rational(1, 2)]
C = [s.Integer(1), s.Integer(4)]
Z = sum(P[i] / s.sqrt(C[i]) for i in range(2))
Q = [P[i] / s.sqrt(C[i]) / Z for i in range(2)]
work = sum(Q[i] * C[i] for i in range(2))
moment = sum(P[i] ** 2 / Q[i] for i in range(2))
check("cost-aware equality proposal", work * moment ==
      sum(P[i] * s.sqrt(C[i]) for i in range(2)) ** 2)

# Exact finite-distribution check of the tail-sum identity used for clock integration.
r = s.symbols("r", positive=True)
pmf = [s.Rational(1, 4)] * 4
tail_sum = sum(r ** n * sum(pmf[n + 1:]) ** 2 for n in range(3))
minimum_sum = sum(pmf[i] * pmf[j] * sum(r ** n for n in range(min(i, j)))
                  for i in range(4) for j in range(4))
check("clock integrated scalar tail identity", s.expand(tail_sum - minimum_sum) == 0)

mp.mp.dps = 70
ks, ds = s.Rational(1, 10 ** 6), s.Rational(1, 100)


def mp_matrix(mat):
    return mp.matrix([[mp.mpf(str(s.N(mat[i, j], 75)))
                       for j in range(mat.cols)] for i in range(mat.rows)])


def deadline_values(M, normalized_b, original_escape, original_total):
    mm = mp_matrix(M)
    bb = mp_matrix(normalized_b)
    ee = mp.expm(mm)
    val = mp.lu_solve(mm, (ee - mp.eye(mm.rows)) * bb)
    hit = -mp.expm1(-original_escape)
    eigs = mp.eig(mm, left=False, right=False)
    alpha = max(mp.re(z) for z in eigs)
    return {"T": "1", "original_total_rate": str(original_total),
            "alpha": mp.nstr(alpha, 35),
            "exp_alpha_T": mp.nstr(mp.exp(alpha), 35),
            "second_moment_divided_by_p_squared": [mp.nstr(x, 35) for x in val],
            "second_moment_divided_by_success_by_T_squared":
                [mp.nstr(x / hit ** 2, 35) for x in val],
            "ratio_to_exact_eventual_committor_deadline_second_moment":
                [mp.nstr(x / hit, 35) for x in val],
            "exact_eventual_committor_deadline_normalized_second_moment": mp.nstr(1 / hit, 35)}


M2_num = M2.subs({k: ks, d: ds})
b2 = ks * a2.subs(d, ds)
two_deadline = deadline_values(M2_num, b2, mp.mpf("0.000001"), 1 + ks)
a3 = s.Matrix([1 + d, 1, 1 - d])
K3 = s.zeros(3)
b3 = s.zeros(3, 1)
for i in range(3):
    den = sum(a3[j] for j in range(3) if j != i) + k
    b3[i] = k * den / (2 + k) ** 2
    for j in range(3):
        if i != j:
            K3[i, j] = den / ((2 + k) ** 2 * a3[j])
clock_M3 = ((2 + k) * (K3 - s.eye(3))).subs({k: ks, d: ds})
clock_b3 = ((2 + k) * b3).subs({k: ks, d: ds})
triangle_deadline = deadline_values(clock_M3, clock_b3, mp.mpf("0.000001"), 2 + ks)

result = {"scope": "Exact finite algebra plus numerical evaluation of proved deadline formulas; no simulation",
          "exact_checks_passed": len(checks), "checks": checks,
          "ct_trace_at_boundary": str(trace_at_boundary),
          "nonuniform_routing_stationary_distribution": [str(x) for x in pi],
          "nonuniform_routing_sigma_squared": str(sigma2),
          "two_state_deadline_illustration": two_deadline,
          "triangle_clock_preserving_deadline_illustration": triangle_deadline,
          "runtime": {"python": sys.version, "platform": platform.platform(),
                      "sympy": s.__version__, "mpmath": mp.__version__}}
(ROOT / "audit_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
