"""Exact transcription checks; the general claims are proved in report.md."""
import itertools
import json
from pathlib import Path
import sympy as s


def phase(t):
    return s.cancel((1 + s.I * t) / (1 - s.I * t))


def unnormalized(a, b):
    return s.Matrix([[a, b], [-s.conjugate(b), s.conjugate(a)]])


r = 5
a = [phase(s.Rational(u + 1)) for u in range(r)]
b = [phase(s.Rational(v + r + 1)) for v in range(r)]
c = [[unnormalized(a[u], b[v]) for v in range(r)] for u in range(r)]
y = s.BlockMatrix(c).as_explicit()
assert y.rank() == 4
for row in c:
    for block in row:
        assert s.simplify(block * block.conjugate().T) == 2 * s.eye(2)
        assert s.simplify(block.det()) == 2

count = 0
for u, uu in itertools.permutations(range(r), 2):
    for v, vv in itertools.permutations(range(r), 2):
        w = c[u][v] * c[uu][v].conjugate().T * c[uu][vv] * c[u][vv].conjugate().T / 4
        w = w.applyfunc(s.cancel)
        assert s.simplify((s.eye(2) - w).det()) != 0
        d_a = s.simplify((a[u] - a[uu]) * s.conjugate(a[u] - a[uu]))
        d_b = s.simplify((b[v] - b[vv]) * s.conjugate(b[v] - b[vv]))
        assert s.simplify(s.trace(w) / 2 - (1 - d_a * d_b / 8)) == 0
        count += 1

summary = {
    "scope": "Exact rational-complex transcription checks, not whole-group microstates",
    "r": r,
    "D": 2,
    "unitary_blocks_checked": r * r,
    "block_array_rank": int(y.rank()),
    "full_rank_rectangle_differences_checked": count,
    "false_permutation_lower_bound_at_lambda_zero": str(s.Rational(r*r*2, 2*r-1)),
    "trace_formula_checks": count,
}
Path(__file__).with_name("local_unitary_checks.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
