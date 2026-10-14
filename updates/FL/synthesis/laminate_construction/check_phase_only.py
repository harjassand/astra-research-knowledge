#!/usr/bin/env python3
"""Exact finite checks for the phase-only modulation laminate construction.

The proof and quantitative estimates are in REPORT.md.  This checker verifies
the N=8 exact conditional-average atoms, their barycentre, the full splitting
tree, a support-bound instance, the source frozen-manifest hashes, and the
rank-two P/Q obstruction for the genuinely transverse example.  Numerical
support norms are diagnostics; the uniform bounds in REPORT.md are analytic.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[1]
SRC = WORK / "work" / "FL-sources" / "global"
checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)
    print(f"PASS {len(checks):02d}: {label}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Recheck every payload listed by the immutable incoming global manifest.
manifest_path = SRC / "MANIFEST.json"
manifest = json.loads(manifest_path.read_text())
manifest_rows = {}
for row in manifest["files"]:
    p = SRC / row["name"]
    data = p.read_bytes()
    check(len(data) == row["bytes"], f"source byte count: {row['name']}")
    check(hashlib.sha256(data).hexdigest() == row["sha256"],
          f"source SHA-256: {row['name']}")
    manifest_rows[row["name"]] = row["sha256"]


# The phase-only family: V=(cos,sin), r=1+1/2 cos(theta), k=e_1.
theta = sp.symbols("theta", real=True)
a = sp.Rational(1, 2)
V = sp.Matrix([sp.cos(theta), sp.sin(theta)])
W = sp.diff(V, theta)
r = 1 + a * sp.cos(theta)
G = sp.simplify(sp.diff(r, theta) * V + r * W)
check(sp.simplify(G - sp.Matrix([
    -sp.sin(theta) - a * sp.sin(2 * theta),
    sp.cos(theta) + a * sp.cos(2 * theta),
])) == sp.zeros(2, 1), "closed form for phase derivative G")
check(sp.simplify(sp.integrate(G, (theta, 0, 2 * sp.pi))) == sp.zeros(2, 1),
      "zero barycentre of the continuous law")

N = 8
h = 2 * sp.pi / N
atoms: list[sp.Matrix] = []
for j in range(N):
    left = j * h
    right = (j + 1) * h
    avg = sp.simplify(sp.integrate(G, (theta, left, right)) / h)
    atoms.append(avg)

mean = sp.simplify(sum(atoms, sp.zeros(2, 1)) / N)
check(mean == sp.zeros(2, 1), "N=8 conditional-average law has exact barycentre")

# Every pair of matrix atoms has a common right factor e_1, hence rank at most 1.
matrix_atoms = [sp.Matrix([[v[0], 0], [v[1], 0]]) for v in atoms]
all_pairwise_rank_one = True
for i in range(N):
    for j in range(N):
        all_pairwise_rank_one &= sp.simplify(
            (matrix_atoms[i] - matrix_atoms[j]).det()
        ) == 0
check(all_pairwise_rank_one, "all atom differences are rank at most one")

# Balanced binary tree, recursively splitting each group barycentre.
tree_nodes = 0
max_depth = 0


def build_tree(indices: tuple[int, ...], depth: int = 0) -> sp.Matrix:
    global tree_nodes, max_depth
    max_depth = max(max_depth, depth)
    if len(indices) == 1:
        return atoms[indices[0]]
    cut = len(indices) // 2
    left_ids, right_ids = indices[:cut], indices[cut:]
    left_mean = sp.simplify(sum((atoms[i] for i in left_ids), sp.zeros(2, 1)) / len(left_ids))
    right_mean = sp.simplify(sum((atoms[i] for i in right_ids), sp.zeros(2, 1)) / len(right_ids))
    node_mean = sp.simplify(sum((atoms[i] for i in indices), sp.zeros(2, 1)) / len(indices))
    lam = sp.Rational(len(left_ids), len(indices))
    check(sp.simplify(lam * left_mean + (1 - lam) * right_mean - node_mean)
          == sp.zeros(2, 1), f"tree barycentre at depth {depth}, size {len(indices)}")
    diff = sp.Matrix([[left_mean[0] - right_mean[0], 0],
                      [left_mean[1] - right_mean[1], 0]])
    check(sp.simplify(diff.det()) == 0,
          f"rank-one split at depth {depth}, size {len(indices)}")
    tree_nodes += 1
    build_tree(left_ids, depth + 1)
    build_tree(right_ids, depth + 1)
    return node_mean


root_mean = build_tree(tuple(range(N)))
check(root_mean == sp.zeros(2, 1), "splitting tree root equals affine barycentre")
check(tree_nodes == N - 1 and max_depth == 3,
      "N=8 tree has seven splits and depth three")

# The analytic support bound is |G| <= 1+a = 3/2. Check this exact instance
# numerically as a finite fixture; the global proof uses convexity of the norm.
norms = [float(sp.N(sp.sqrt((v.T * v)[0]), 30)) for v in atoms]
check(max(norms) <= 1.5 + 1e-12,
      "N=8 atoms satisfy the analytic 3/2 support bound (numeric fixture)")

# For this example |G'| <= 1+2a = 2. Conditional averaging on width h gives
# W_1 <= |G'| h/2 = 2*pi/N; store this exact symbolic bound.
w1_bound = sp.simplify((1 + 2 * a) * h / 2)
check(w1_bound == 2 * sp.pi / N, "symbolic W1 rate is 2*pi/N")

# Transverse amplitude obstruction to treating the pointwise P,Q terms as a
# rank-one split: k=e_2, r=1+1/2 cos x, and V=(cos y,sin y).
x, y = sp.symbols("x y", real=True)
rv = 1 + a * sp.cos(x)
rx = sp.diff(rv, x)
Vxy = sp.Matrix([sp.cos(y), sp.sin(y)])
Wxy = sp.Matrix([-sp.sin(y), sp.cos(y)])
k = sp.Matrix([0, 1])
grad_r = sp.Matrix([rx, 0])
P = Wxy * k.T * rv
Q = Vxy * grad_r.T
det_p_minus_q = sp.trigsimp(sp.expand_trig((P - Q).det()))
check(sp.trigsimp(det_p_minus_q + rv * rx) == 0,
      "det(P-Q) = -r*r_x for transverse modulation")
check(sp.simplify(det_p_minus_q.subs({x: sp.pi / 2, y: 0})) == sp.Rational(1, 2),
      "transverse P,Q terms are not rank-one connected at x=pi/2")

result = {
    "scope": "Exact finite symbolic checks plus finite support diagnostic; analytic estimates are stated and proved in REPORT.md.",
    "source_global_manifest_sha256": sha256(manifest_path),
    "source_payload_hashes_rechecked": manifest_rows,
    "example": {
        "V": ["cos(theta)", "sin(theta)"],
        "r": "1 + (1/2) cos(theta)",
        "G": ["-sin(theta) - (1/2) sin(2 theta)",
              "cos(theta) + (1/2) cos(2 theta)"],
        "N": N,
        "atoms": [[str(sp.simplify(v[0])), str(sp.simplify(v[1]))] for v in atoms],
        "barycentre": [str(mean[0]), str(mean[1])],
        "max_atom_norm_numeric": max(norms),
        "tree_internal_splits": tree_nodes,
        "tree_depth": max_depth,
        "W1_bound": str(w1_bound),
        "gradient_bound": "3/2",
    },
    "transverse_obstruction": {
        "det_P_minus_Q": "-r*r_x",
        "example_value_at_x_pi_over_2_y_0": str(det_p_minus_q.subs({x: sp.pi / 2, y: 0})),
    },
    "checks": checks,
}
(ROOT / "checker_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"WROTE checker_results.json; {len(checks)} checks passed.", flush=True)
