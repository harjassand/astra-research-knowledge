"""Task G: exact affine algebra and a small numerical execution check.

The floating draws test this implementation only. Exact unbiasedness and the
all-execution bound are proved in REPORT.md; no continuous-law TV or finite-bit
claim is inferred from these calculations. Uses only the Python standard library.
"""

from fractions import Fraction as Q
from pathlib import Path
import json
import math
import random


A = ((Q(1, 2), Q(1, 4)), (Q(1, 4), Q(1, 3)))
b = (Q(1), Q(-1))
c = (Q(1), Q(2))
v = (Q(2), Q(-1))
s = Q(2)


def mv(matrix, vector):
    return tuple(sum(a * x for a, x in zip(row, vector)) for row in matrix)


def g_exact(x):
    return tuple(a + shift for a, shift in zip(mv(A, x), b))


target = mv(A, v)
exact_cases = []
# Zperp=(t,2t) is perpendicular to v. Write R=q*||v||, so that
# x_plus/minus=c+s*Zperp +/- q*v and the entire affine check is rational.
for q, t in [(Q(1), Q(0)), (Q(1, 3), Q(-2)), (Q(7, 4), Q(5, 6))]:
    center = (c[0] + s * t, c[1] + 2 * s * t)
    xp = tuple(x + q * w for x, w in zip(center, v))
    xm = tuple(x - q * w for x, w in zip(center, v))
    gp, gm = g_exact(xp), g_exact(xm)
    value = tuple((x - y) / (2 * q) for x, y in zip(gp, gm))
    assert value == target
    exact_cases.append({
        "R_over_norm_v": str(q), "Zperp": [str(t), str(2 * t)],
        "x_plus": list(map(str, xp)), "x_minus": list(map(str, xm)),
        "g_plus": list(map(str, gp)), "g_minus": list(map(str, gm)),
        "J": list(map(str, value)),
    })


def action(g, center, scale, direction, z0, radius_normals):
    nv = math.sqrt(sum(x * x for x in direction))
    if nv == 0:
        return [0.0] * len(direction), 0
    u = [x / nv for x in direction]
    projection = sum(x * y for x, y in zip(u, z0))
    zp = [x - projection * y for x, y in zip(z0, u)]
    radius = scale * math.sqrt(sum(x * x for x in radius_normals))
    # A null-event fallback with the same two-query interface and bound.
    # Replacing a zero radius by s leaves the ideal distribution unchanged.
    if radius == 0:
        radius = scale
    xp = [x + scale * z + radius * y for x, z, y in zip(center, zp, u)]
    xm = [x + scale * z - radius * y for x, z, y in zip(center, zp, u)]
    gp, gm = g(xp), g(xm)
    return [nv * (x - y) / (2 * radius) for x, y in zip(gp, gm)], 2


def g_float(x):
    return [0.5 * x[0] + 0.25 * x[1] + 1,
            0.25 * x[0] + x[1] / 3 - 1]


rng = random.Random(20261027)
samples = []
for _ in range(1000):
    z0 = [rng.gauss(0, 1) for _ in range(2)]
    a = [rng.gauss(0, 1) for _ in range(3)]
    value, calls = action(g_float, [1, 2], 2, [2, -1], z0, a)
    assert calls == 2
    samples.append(value)

fallback, fallback_calls = action(g_float, [1, 2], 2, [2, -1], [0, 0], [0, 0, 0])
zero, zero_calls = action(g_float, [1, 2], 2, [0, 0], [0, 0], [0, 0, 0])
assert zero == [0, 0] and zero_calls == 0

L = (5 + math.sqrt(10)) / 12
bound = L * math.sqrt(5)
expected = list(map(float, target))
max_error = max(abs(x - y) for row in samples for x, y in zip(row, expected))
max_norm = max(math.sqrt(sum(x * x for x in row)) for row in samples)
assert max_error < 1e-12
assert max_norm <= bound
assert max(abs(x - y) for x, y in zip(fallback, expected)) < 1e-12
assert fallback_calls == 2

result = {
    "exact_algebra": {
        "A": [[str(x) for x in row] for row in A],
        "g(c)": list(map(str, g_exact(c))),
        "H_s(c)": "A for every c and s>0",
        "Av": list(map(str, target)),
        "norm_Av_squared": str(sum(x * x for x in target)),
        "eigenvalues_A": ["(5-sqrt(10))/12", "(5+sqrt(10))/12"],
        "L_min": L, "norm_Av": math.sqrt(85) / 12,
        "L_min_times_norm_v": bound,
        "rational_endpoint_cases": exact_cases,
    },
    "floating_implementation_check": {
        "seed": 20261027, "draws": len(samples),
        "query_count_each_nonzero_action": 2,
        "max_abs_error_from_Av": max_error,
        "max_observed_norm": max_norm,
        "sample_mean": [sum(row[i] for row in samples) / len(samples) for i in range(2)],
        "null_radius_fallback": {"J": fallback, "queries": fallback_calls},
        "zero_direction": {"J": zero, "queries": zero_calls},
        "scope": "Finite floating implementation diagnostic; not the proof of unbiasedness, law, or universal bound.",
    },
}
out = Path(__file__).resolve().parent / "CHECK.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
