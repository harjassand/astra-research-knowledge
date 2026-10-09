#!/usr/bin/env python3
"""Root-supplied state for a directly checked LWW generator; exact sign."""
import json
import sympy as s

Q = s.Rational
I = s.eye(2)
checks = []


def equal(a, b, label):
    delta = a - b
    ok = (all(s.simplify(x) == 0 for x in delta) if isinstance(delta, s.MatrixBase)
          else s.simplify(delta) == 0)
    assert ok, (label, delta)
    checks.append(label)


def positive(value, label):
    assert value.is_Rational and value > 0, (label, value)
    checks.append(label)


V = s.Matrix([[0, 1], [2, 0]])
Qop = V.T * V
sigma = s.diag(1, 4) / 5
sqrt_sigma = s.diag(1, 2) / s.sqrt(5)
S = s.diag(1, s.sqrt(2)) / 5 ** Q(1, 4)


def LH(a):
    return (Qop * a + a * Qop) / 2 - V.T * a * V


def LS(a):
    return (Qop * a + a * Qop) / 2 - V * a * V.T


def L(a):
    return s.simplify(S.inv() * LS(S * a * S) * S.inv())


equal(LS(sigma), s.zeros(2), "source reference stationary")
equal(LH(I), s.zeros(2), "source Heisenberg generator unital")
equal(S.inv() * V * S, s.sqrt(2) * s.Matrix([[0, 1], [1, 0]]),
      "transformed jump orientation")
units = []
for i in range(2):
    for j in range(2):
        unit = s.zeros(2)
        unit[i, j] = 1
        units.append(unit)
        equal(sqrt_sigma * LH(unit) * sqrt_sigma,
              LS(sqrt_sigma * unit * sqrt_sigma), f"KMS generator intertwining {i}{j}")
matrix = s.Matrix([[s.trace(a.T * L(b)) for b in units] for a in units])
equal(matrix, s.Matrix([[4, 0, 0, -2], [0, Q(5, 2), -2, 0],
                        [0, -2, Q(5, 2), 0], [-2, 0, 0, 1]]),
      "exact weighted positive generator matrix")
assert matrix.eigenvals() == {0: 1, Q(1, 2): 1, Q(9, 2): 1, 5: 1}
checks.append("primitive spectrum exactly zero one half nine halves five")
equal(L(units[0]) * sigma, sigma * L(units[0]), "commutant preserved on first diagonal unit")
equal(L(units[3]) * sigma, sigma * L(units[3]), "commutant preserved on second diagonal unit")
assert s.simplify(sigma * L(units[1]) * sigma.inv()
                  - L(sigma * units[1] * sigma.inv())) != s.zeros(2)
checks.append("nonzero modular-frequency mixing despite commutant preservation")

rho = s.Matrix([[Q(1, 4), -Q(2, 5)], [-Q(2, 5), Q(3, 4)]])
equal(s.trace(rho), 1, "root-supplied actual state trace one")
equal(rho.det(), Q(11, 400), "actual state positive determinant")
positive(rho[0, 0], "actual state positive diagonal")
delta = LS(rho)
equal(delta, s.Matrix([[Q(1, 4), -Q(1, 5)], [-Q(1, 5), -Q(1, 4)]]),
      "actual state generator defect")
equal(s.trace(delta), 0, "defect trace zero")
equal(s.trace(delta * (2 * rho - I)), Q(7, 100), "spectral log contraction coefficient")
log_ratio = s.log((10 + s.sqrt(89)) / (10 - s.sqrt(89)))
log_rho = s.log(Q(11, 400)) * I / 2 + 5 * log_ratio * (2 * rho - I) / s.sqrt(89)
log_sigma = s.diag(-s.log(5), 2 * s.log(2) - s.log(5))
J = s.simplify(s.trace(delta * (log_rho - log_sigma)))
equal(J, s.log(2) / 2 + 7 * log_ratio / (20 * s.sqrt(89)),
      "actual entropy-production closed form")
root_rho = (rho + s.sqrt(11) * I / 20) / s.sqrt(1 + s.sqrt(11) / 10)
equal(root_rho * root_rho, rho, "physical root closed form squares to rho")
E = s.simplify(s.trace(root_rho * L(root_rho)))
equal(E, (10 - s.sqrt(11)) / (4 * (10 + s.sqrt(11))),
      "actual root-energy closed form")

# A coarse strict analytic upper bound already excludes FOUR by >1/100.
log2_series_upper = Q(2, 3) + Q(2, 81) + Q(1, 540)
positive(Q(7, 10) - log2_series_upper, "finite atanh log2 upper bound below seven tenths")
positive(89 - Q(943, 100) ** 2, "sqrt89 lower bound 943 over100")
positive(Q(236, 25) ** 2 - 89, "sqrt89 upper bound 236 over25")
ratio_upper = (10 + Q(236, 25)) / (10 - Q(236, 25))
equal(ratio_upper, Q(243, 7), "rational spectral log-ratio upper bound")
exponential_partial = sum((Q(18, 5) ** n / s.factorial(n) for n in range(9)), Q(0))
positive(exponential_partial - ratio_upper, "nine positive exp series terms imply log-ratio below18 over5")
positive(Q(10, 3) ** 2 - 11, "sqrt11 upper bound ten overthree")
equal((10 - Q(10, 3)) / (10 + Q(10, 3)), Q(1, 2),
      "four times energy strict lower bound one half")
J_upper = Q(7, 20) + Q(7, 20) / Q(943, 100) * Q(18, 5)
gap_upper = J_upper - Q(1, 2)
equal(gap_upper, -Q(309, 18860), "strict rational J minus4E upper bound")
positive(-Q(1, 100) - gap_upper, "gap below minus one hundredth")

print(json.dumps({
    'status': 'PASS_EXACT_SOURCE_CONSEQUENCE',
    'checks': len(checks),
    'assertions': checks,
    'J': str(J),
    'E': str(E),
    'strict_gap_upper_bound': str(gap_upper),
    'attribution': 'LWW published generator/reference; root supplied rho and proposed scalar forms; worker reconstructs forms and adds rational sign certificate',
    'scope': 'Actual primitive KMS generator, unamplified faithful state; commutant preservation is not globally sufficient for FOUR',
    'full_channel_selfcompatibility_claimed': False,
    'floating_point_used': False
}, indent=2))
