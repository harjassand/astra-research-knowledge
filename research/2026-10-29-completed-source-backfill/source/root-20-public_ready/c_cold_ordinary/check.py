"""Exact synthetic scalar audit. Writes only alongside this script.

The learner audit consumes three scalar centers with the declared error envelope.
Explicit source gradients and an optimum bracket are verifier-only calculations.
No empirical claim about a physical apparatus is made.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
from pathlib import Path


OUT = Path(__file__).resolve().parent
delta = F(1, 5)
x = (F(1, 50), F(1, 50))
steps = (F(1, 100), F(1, 100))
epsilon = F(1, 100_000_000)
prices = (F(1, 10), F(1, 20))
m = F(1)
L = (F(1), F(2))
B = (F(2), F(4))
e_norm_squared = F(2)  # Supplied for this synthetic fixture only.


def z_source(u):
    return (1 + u[0]) / (1 + 2 * u[0]) + (1 + u[1]) / (2 * (1 + 2 * u[1]))


def scalar_source(u):
    return F(3, 2) + 1 / z_source(u)


def invert_report(r):
    assert r - epsilon > F(3, 2)
    return 1 / (r + epsilon - F(3, 2)), 1 / (r - epsilon - F(3, 2))


def certificate(lower, upper):
    zero = -sum(xi * li for xi, li in zip(x, lower))
    vertex = [
        (delta - x[j]) * upper[j]
        - sum(x[i] * lower[i] for i in range(2) if i != j)
        for j in range(2)
    ]
    return max([zero] + vertex), [zero] + vertex


def gradient_bounds(intervals, caps):
    a0, b0 = intervals[0]
    lower = tuple((a0 - intervals[i + 1][1]) / steps[i] - prices[i] for i in range(2))
    upper = tuple(
        (b0 - intervals[i + 1][0]) / steps[i] - prices[i] + caps[i] * steps[i] / 2
        for i in range(2)
    )
    return lower, upper


def nearest(q, places=20):
    with localcontext() as ctx:
        ctx.prec = max(80, places + 20)
        return f"{Decimal(q.numerator) / Decimal(q.denominator):.{places}f}"


def directed(q, places=15, upper=False):
    scale = 10**places
    v = q * scale
    k = -((-v.numerator) // v.denominator) if upper else v.numerator // v.denominator
    sign = "-" if k < 0 else ""
    k = abs(k)
    return f"{sign}{k // scale}.{k % scale:0{places}d}"


def encode(q):
    return {"exact": str(q), "decimal": nearest(q)}


assert all(sum(x) + h <= delta for h in steps)
points = [x, (x[0] + steps[0], x[1]), (x[0], x[1] + steps[1])]
centers = tuple(scalar_source(u) for u in points)
intervals = tuple(invert_report(r) for r in centers)
for point, (a, b) in zip(points, intervals):
    assert a <= z_source(point) <= b

source_caps = tuple(e_norm_squared * (2 * li**2 / m**3 + bi / m**2) for li, bi in zip(L, B))
# Additional deduction in REPORT.md: no known norm or hidden dimension is needed.
local_caps = tuple(
    (2 * L[i] ** 2 / m**2 + B[i] / m) * max(intervals[0][1], intervals[i + 1][1])
    for i in range(2)
)
true_gradient = (
    1 / (1 + 2 * x[0]) ** 2 - prices[0],
    1 / (2 * (1 + 2 * x[1]) ** 2) - prices[1],
)

audits = {}
for name, caps in [("source_norm_cap", source_caps), ("scalar_local_cap", local_caps)]:
    lower, upper = gradient_bounds(intervals, caps)
    assert all(lower[i] <= true_gradient[i] <= upper[i] for i in range(2))
    bound, vertices = certificate(lower, upper)
    audits[name] = {
        "curvature_caps": [encode(v) for v in caps],
        "gradient_intervals": [
            {"lower": encode(lower[i]), "upper": encode(upper[i]),
             "outward_12dp": [directed(lower[i], 12), directed(upper[i], 12, upper=True)]}
            for i in range(2)
        ],
        "vertex_bounds_zero_then_e1_e2": [encode(v) for v in vertices],
        "regret_bound": encode(bound),
        "regret_bound_outward_15dp": directed(bound, upper=True),
    }

# Independent use of explicit synthetic formulas, not an input to the audit.
def reward(u):
    return z_source((F(0), F(0))) - z_source(u) - sum(c * ui for c, ui in zip(prices, u))


def full_dose_derivative(t):
    return 1 / (1 + 2 * t) ** 2 - prices[0] - (
        1 / (2 * (1 + 2 * (delta - t)) ** 2) - prices[1]
    )


# Both coordinate reward derivatives are positive throughout the simplex.
assert 1 / (1 + 2 * delta) ** 2 - prices[0] > 0
assert 1 / (2 * (1 + 2 * delta) ** 2) - prices[1] > 0
lo, hi = F(0), delta
assert full_dose_derivative(lo) > 0 > full_dose_derivative(hi)
for _ in range(80):
    mid = (lo + hi) / 2
    if full_dose_derivative(mid) > 0:
        lo = mid
    else:
        hi = mid
regret_lower = reward((lo, delta - lo)) - reward(x)
# Concavity gives an exact outward upper bracket without float optimization.
regret_upper = regret_lower + full_dose_derivative(lo) * (hi - lo)
tangent_gap, _ = certificate(true_gradient, true_gradient)
assert regret_lower <= regret_upper <= tangent_gap
for audit in audits.values():
    assert tangent_gap <= F(audit["regret_bound"]["exact"])

results = {
    "scope": "Synthetic exact-rational check; three simulated scalar centers, no physical acquisition",
    "n_scalar_reports": len(centers),
    "epsilon": encode(epsilon),
    "points": [[str(ui) for ui in point] for point in points],
    "reports": [
        {"r_center": encode(r), "Z_true": encode(z_source(point)),
         "Z_interval": [encode(a), encode(b)],
         "Z_interval_outward_12dp": [directed(a, 12), directed(b, 12, upper=True)]}
        for point, r, (a, b) in zip(points, centers, intervals)
    ],
    "audits": audits,
    "verifier_only": {
        "true_gradient": [encode(v) for v in true_gradient],
        "true_tangent_gap": encode(tangent_gap),
        "optimum_u1_interval": [encode(lo), encode(hi)],
        "actual_regret_interval_outward_15dp": [directed(regret_lower), directed(regret_upper, upper=True)],
        "candidate_reward": encode(reward(x)),
        "all_exact_assertions_passed": True,
    },
}
(OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
