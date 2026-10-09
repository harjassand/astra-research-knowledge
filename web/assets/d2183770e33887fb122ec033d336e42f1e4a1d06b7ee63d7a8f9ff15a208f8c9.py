"""Exact small-matrix replay only; not a power-theorem verification."""
import json
import sympy as s

sigma = s.diag(s.Rational(4, 5), s.Rational(1, 5))
sigma_inv_half = s.diag(s.sqrt(5) / 2, s.sqrt(5))
rho = s.Matrix([[1, 1], [1, 1]]) / 2
pi_plus = s.Matrix([[4, 2], [2, 1]]) / 5
pi_minus = s.Matrix([[4, -2], [-2, 1]]) / 5
assert (pi_plus + pi_minus) / 2 == sigma
assert pi_plus * pi_plus == pi_plus
assert pi_minus * pi_minus == pi_minus
assert rho * rho == rho
effects = [sigma_inv_half * pi * sigma_inv_half / 2
           for pi in [pi_plus, pi_minus]]
assert effects[0] == rho
assert effects[0] + effects[1] == s.eye(2)
out = sum((pi * s.trace(M * rho)
           for pi, M in zip([pi_plus, pi_minus], effects)), s.zeros(2))
Bplus = s.Matrix([[2 / s.sqrt(5), s.sqrt(s.Rational(2, 5))],
                  [s.sqrt(s.Rational(2, 5)), 1 / s.sqrt(5)]])
Bminus = s.Matrix([[2 / s.sqrt(5), -s.sqrt(s.Rational(2, 5))],
                   [-s.sqrt(s.Rational(2, 5)), 1 / s.sqrt(5)]])
implemented = s.simplify((Bplus * rho * Bplus + Bminus * rho * Bminus) / 2)
assert implemented == s.Matrix([[s.Rational(3, 5), s.Rational(2, 5)],
                                 [s.Rational(2, 5), s.Rational(3, 10)]])
defect = out - implemented**2
assert defect == s.Matrix([[28, 4], [4, -5]]) / 100
assert defect[1, 1] == -s.Rational(1, 20)
energy = 1 - s.trace(rho * implemented)
err_square = s.simplify(-s.det(out - rho))
assert energy == s.Rational(3, 20)
assert err_square == s.Rational(1, 10)
assert err_square <= 2 * energy
print(json.dumps({
    "status": "EXACT_ROUTE_REFUTATION_PASS",
    "negative_expectation": str(defect[1, 1]),
    "half_trace_error_squared": str(err_square),
    "correct_KMS_root_energy": str(energy),
    "scalar_e2_le_2E_refuted": False,
    "actual_power_theorem_refuted": False,
}, indent=2))
