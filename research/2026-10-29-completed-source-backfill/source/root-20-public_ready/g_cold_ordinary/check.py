"""Small independent check of the value-only two-query action.

The proof in REPORT.md establishes the ideal-real distributional claims.
This executable verifies the affine fixture exactly and exercises a floating
implementation. It makes no finite-bit continuous-TV or exact-Gaussian claim.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path
import random


def action(g, c, s, v, z0, radial_normals):
    nv = math.sqrt(sum(x * x for x in v))
    if nv == 0:
        return [0.0 for _ in v], 0
    u = [x / nv for x in v]
    projection = sum(x * y for x, y in zip(u, z0))
    zp = [z - projection * ui for z, ui in zip(z0, u)]
    r = s * math.sqrt(sum(a * a for a in radial_normals))
    # A specified bounded null-event repair, retaining exact affine actions.
    if r == 0:
        r = s
    plus = [ci + s * zi + r * ui for ci, zi, ui in zip(c, zp, u)]
    minus = [ci + s * zi - r * ui for ci, zi, ui in zip(c, zp, u)]
    gp, gm = g(plus), g(minus)
    return [nv * (a - b) / (2 * r) for a, b in zip(gp, gm)], 2


A = ((F(1, 2), F(1, 4)), (F(1, 4), F(1, 3)))
b = (F(1), F(-1))
v = (F(2), F(-1))


def affine(x):
    return [sum(a * z for a, z in zip(row, x)) + bi for row, bi in zip(A, b)]


expected = [sum(a * z for a, z in zip(row, v)) for row in A]
assert expected == [F(3, 4), F(1, 6)]
# Choose R=sqrt(5) and s Z_perp=(2,4); then R*u=v and the
# prefactor ||v||/(2R)=1/2, so all endpoint arithmetic is rational.
gplus, gminus = affine((F(5), F(5))), affine((F(1), F(7)))
exact_action = [(x - y) / 2 for x, y in zip(gplus, gminus)]
assert exact_action == expected
norm_sq = sum(x * x for x in expected)
assert norm_sq == F(85, 144)

rng = random.Random(20261027)
target = [float(x) for x in expected]
L = (5 + math.sqrt(10)) / 12
bound = L * math.sqrt(5)
errors, counts, norms = [], [], []
for _ in range(4096):
    z0 = [rng.gauss(0, 1) for _ in range(2)]
    a3 = [rng.gauss(0, 1) for _ in range(3)]
    got, calls = action(affine, [1.0, 2.0], 2.0, [2.0, -1.0], z0, a3)
    errors.append(math.sqrt(sum((x - y) ** 2 for x, y in zip(got, target))))
    counts.append(calls)
    norms.append(math.sqrt(sum(x * x for x in got)))
assert max(errors) < 1e-12
assert max(norms) <= bound + 1e-12
assert set(counts) == {2}
zero_radius, zero_radius_calls = action(
    affine, [1.0, 2.0], 2.0, [2.0, -1.0], [0.3, -0.4], [0.0, 0.0, 0.0]
)
assert max(abs(x - y) for x, y in zip(zero_radius, target)) < 1e-12
zero_v, zero_v_calls = action(
    affine, [1.0, 2.0], 2.0, [0.0, 0.0], [0.3, -0.4], [1.0, 0.0, 0.0]
)
assert zero_v == [0.0, 0.0] and zero_v_calls == 0

# A globally 1-Lipschitz conservative field need not give a common
# realized linear action when the same natural seeds are reused.
def sine_field(x):
    return [math.sin(x[0]), 0.0]

common = ([0.0, 0.0], 1.0, [0.0, 0.0], [1.0, 0.0, 0.0])
js = []
for direction in ([1.0, 0.0], [0.0, 1.0], [1.0, 1.0]):
    js.append(action(sine_field, common[0], common[1], direction, common[2], common[3])[0])
nonlinearity = js[2][0] - js[0][0] - js[1][0]
assert abs(nonlinearity) > 0.07

result = {
    "exact": {
        "g_c": [str(x) for x in affine((F(1), F(2)))],
        "chosen_endpoints": [[5, 5], [1, 7]],
        "g_plus": [str(x) for x in gplus],
        "g_minus": [str(x) for x in gminus],
        "action": [str(x) for x in exact_action],
        "action_norm_squared": str(norm_sq),
    },
    "floating_diagnostic": {
        "seed": 20261027,
        "draws": len(errors),
        "query_count_each": sorted(set(counts)),
        "max_l2_error": max(errors),
        "max_action_norm": max(norms),
        "sharp_L": L,
        "L_times_vnorm": bound,
        "zero_radius_repair_action": zero_radius,
        "zero_radius_repair_queries": zero_radius_calls,
        "zero_direction_queries": zero_v_calls,
    },
    "conservative_nonlinear_common_seed_witness": {
        "J_e1": js[0], "J_e2": js[1], "J_e1_plus_e2": js[2],
        "additivity_defect_first_coordinate": nonlinearity,
    },
    "status": "PASS; finite diagnostics supplement the analytic proof only",
}
Path(__file__).with_name("check_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
