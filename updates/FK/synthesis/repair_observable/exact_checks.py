"""Exact arithmetic for the scoped FCC visibility example in REPORT.md."""
from fractions import Fraction as Q
import json
from pathlib import Path

# Crystallographic direction components in conventional [h k l] coordinates.
b1 = (Q(1, 6), Q(-2, 6), Q(1, 6))
b2 = (Q(2, 6), Q(-1, 6), Q(-1, 6))
bp = (Q(1, 2), Q(-1, 2), Q(0))
zero = (Q(0), Q(0), Q(0))
# Illustrative ZnS/f.c.c. cover: the first two reflections are among the
# conditions used in the cited ZnS electric-glide work; (311) adds an
# out-of-plane allowed reflection to expose both listed fault shifts.
G = ((0, 2, -2), (2, 0, -2), (3, 1, 1))

def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))

def determinant3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))

def phases(v):
    return [dot(g, v) % 1 for g in G]

assert tuple(x + y for x, y in zip(b1, b2)) == bp
assert tuple(x + y for x, y in zip(bp, tuple(-z for z in bp))) == zero
assert determinant3(G) != 0

burgers_readouts = {"b1": [str(dot(g, b1)) for g in G], "b2": [str(dot(g, b2)) for g in G], "b_perfect": [str(dot(g, bp)) for g in G]}
assert all(any(dot(g, b) != 0 for g in G) for b in (b1, b2, bp))
assert len({tuple(burgers_readouts[k]) for k in burgers_readouts}) == 3

fault_classes = {"R=b1": phases(b1), "R=b2": phases(b2), "R=-b1": phases(tuple(-z for z in b1)), "R=-b2": phases(tuple(-z for z in b2))}
assert all(any(p != 0 for p in vals) for vals in fault_classes.values())
assert len({tuple(vals) for vals in fault_classes.values()}) == 2
assert tuple(fault_classes["R=b2"]) == tuple(fault_classes["R=-b1"])
assert tuple(fault_classes["R=b1"]) == tuple(fault_classes["R=-b2"])

result = {
    "scope": "exact visibility-design arithmetic for the supplied partial-reaction example and three listed ZnS/f.c.c. reflection indices; not microscopy, detection-completeness, or a universal assay",
    "b1": [str(x) for x in b1],
    "b2": [str(x) for x in b2],
    "b1_plus_b2": [str(x) for x in bp],
    "g_reflections": [list(g) for g in G],
    "reflection_matrix_determinant": str(determinant3(G)),
    "g_dot_b": burgers_readouts,
    "fault_phases_mod_1": {k: [str(x) for x in vals] for k, vals in fault_classes.items()},
    "checks": ["b1+b2 equals nonzero perfect b", "selected g vectors span three dimensions", "each listed nonzero b has at least one g dot b != 0", "listed Burgers vectors have distinct signed g dot b readouts", "each listed non-lattice fault shift has a nonintegral g dot R", "fault phase is modulo a lattice vector and aliases b2 with -b1 and b1 with -b2"],
}
Path(__file__).with_name("exact_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
