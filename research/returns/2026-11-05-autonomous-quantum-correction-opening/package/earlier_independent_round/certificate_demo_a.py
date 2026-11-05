"""Exact local Poisson-certificate checks; no numerical dynamics extrapolation."""
import json
from pathlib import Path
import sympy as s

I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
sm = s.Matrix([[0, 1], [0, 0]])

def at(a, site):
    factors = [I, I, I]
    factors[site] = a
    return s.kronecker_product(*factors)

def lindblad(a, h, jumps):
    out = s.I * (h * a - a * h)
    for v in jumps:
        vv = v.conjugate().T * v
        out += v.conjugate().T * a * v - (vv * a + a * vv) / 2
    return s.simplify(out)

J = s.Rational(1, 256)
h = sum((at(X, j) for j in range(3)), s.zeros(8))
h += J * (at(Z, 0) * at(Z, 1) + at(Z, 1) * at(Z, 2))
jumps = [2 * at(sm, j) for j in range(3)]
target = (I - s.Rational(2, 3) * Y + s.Rational(2, 3) * Z) / 2
assert target.trace() == 1
assert target.det() == s.Rational(1, 36)

specs = {
    "X": (X, X / 2, s.Integer(0), 2 * J, s.Rational(1, 4)),
    "Y": (Y, Y / 3 - Z / 6, -s.Rational(2, 3), 4 * J / 3, s.Rational(5, 36)),
    "Z": (Z, (Y + Z) / 6, s.Rational(2, 3), 2 * J / 3, s.Rational(1, 18)),
}
results = {}
for label, (a, b, mean, radius, b2) in specs.items():
    assert s.simplify(b * b - b2 * I) == s.zeros(2)
    residual = s.simplify(at(a, 1) + lindblad(at(b, 1), h, jumps) - mean * s.eye(8))
    ev = residual.eigenvals()
    assert all(value.is_real for value in ev)
    assert max(abs(value) for value in ev) == radius
    assert s.simplify(s.trace(target * a)) == mean
    results[label] = {
        "mean": str(mean), "residual_norm": str(radius),
        "B_norm_squared": str(b2),
        "residual_eigenvalues": {str(value): mult for value, mult in ev.items()},
    }

assert 5 < s.Rational(81, 16)  # sqrt(5)<9/4
assert 2 < s.Rational(9, 4)    # sqrt(2)<3/2
norm_sum_upper = s.Rational(9, 8)
T = s.Integer(1000)
eta = s.Rational(1, 1000)
residual_sum = sum((entry[3] for entry in specs.values()), s.Integer(0))
continuous_bound = s.simplify(residual_sum + (2 / T + eta) * norm_sum_upper)
assert continuous_bound == s.Rational(19, 1000)
assert 16 + 8 * J + 3 * eta < 17
mesh = s.Rational(1, 10000)
grid_bound = continuous_bound + 17 * mesh / 2
assert grid_bound == s.Rational(397, 20000) < s.Rational(1, 50)

# Exact observable agreement need not imply instantaneous relaxation.
assert X + lindblad(-Y, Z / 2, []) == s.zeros(2)

out = {
    "status": "all exact symbolic checks passed", "coupling_J": str(J),
    "target": [[str(v) for v in row] for row in target.tolist()],
    "certificates": results, "T": str(T), "eta": str(eta),
    "continuous_diamond_upper": str(continuous_bound),
    "grid_spacing": str(mesh), "number_grid_points": str(T / mesh),
    "discrete_diamond_upper": str(grid_bound),
    "closed_rotation_countertest": "X + L(-Y) = 0; initial |+> has <X>(t)=cos(t)",
}
Path(__file__).with_name("certificate_demo_a_results.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
