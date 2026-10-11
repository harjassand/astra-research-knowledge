"""Scoped algebra diagnostics for RESULT.md; these do not certify its theorem."""

import hashlib
import json
from pathlib import Path
import random

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent
rng = random.Random(11012026)


def hs2(a):
    return sp.simplify(sp.trace(a.conjugate().T * a))


commutator_cases = 0
spread_cases = 0
for d in range(2, 7):
    spectra = [[d - 1] + [-1] * (d - 1),
               [1] * (d - 1) + [-(d - 1)],
               [2 * j - d + 1 for j in range(d)]]
    for _ in range(8):
        raw = [rng.randrange(-5, 6) for _ in range(d)]
        spectra.append([d * x - sum(raw) for x in raw])
    for spectrum in spectra:
        spectrum = sorted(spectrum, reverse=True)
        if not any(spectrum):
            continue
        h = sp.diag(*spectrum)
        gap, j0 = max((spectrum[j] - spectrum[j + 1], j)
                      for j in range(d - 1))
        j = j0 + 1
        assert gap * gap * d * (d - 1)**2 >= hs2(h)
        spread_cases += 1
        p = sp.diag(*([1] * j + [0] * (d - j)))
        u = sp.eye(d)
        for _ in range(4):
            pair = rng.randrange(d - 1)
            g = sp.eye(d)
            if rng.randrange(2):
                g[pair, pair] = sp.Rational(3, 5)
                g[pair + 1, pair + 1] = sp.Rational(3, 5)
                g[pair, pair + 1] = -sp.Rational(4, 5)
                g[pair + 1, pair] = sp.Rational(4, 5)
            else:
                g[pair, pair] = sp.Rational(3, 5) + sp.I * sp.Rational(4, 5)
                g[pair + 1, pair + 1] = sp.conjugate(g[pair, pair])
            u = g * u
        assert hs2(u * h * u.conjugate().T - h) == hs2(u * h - h * u)
        residual = sp.simplify(hs2(u * h - h * u)
                               - gap * gap * hs2(u * p * u.conjugate().T - p))
        assert residual >= 0
        commutator_cases += 1

grassmann_cases = 0
for d in range(2, 6):
    for j in range(1, d):
        z = sp.Matrix(d - j, j,
                      lambda a, b: (rng.randrange(-2, 3)
                                    + sp.I * rng.randrange(-2, 3)) / sp.Integer(50))
        w = sp.eye(j).col_join(z)
        q = w * (w.conjugate().T * w).inv() * w.conjugate().T
        p = sp.diag(*([1] * j + [0] * (d - j)))
        a = z.conjugate().T * z
        delta2 = hs2(p - q)
        assert delta2 == sp.simplify(2 * sp.trace(a * (sp.eye(j) + a).inv()))
        assert delta2 <= 1
        assert hs2(z) <= delta2
        grassmann_cases += 1

# An exact barycentric row for a generic rational projector and the actual
# d=2 alphabet gate, selected numerically and then verified over rationals.
grid = []
for chart in range(2):
    for a in range(-4, 5):
        for b in range(-4, 5):
            z = [sp.Integer(1), sp.Rational(a, 4) + sp.I * sp.Rational(b, 4)]
            if chart:
                z.reverse()
            z = sp.Matrix(z)
            p = z * z.conjugate().T / (z.conjugate().T * z)[0]
            bloch = sp.Matrix([2 * sp.re(p[0, 1]), -2 * sp.im(p[0, 1]),
                               p[0, 0] - p[1, 1]])
            grid.append(bloch)
initial = grid[5 * 9 + 6]
rotation = sp.Matrix([[1, 0, 0], [0, sp.Rational(3, 5), -sp.Rational(4, 5)],
                       [0, sp.Rational(4, 5), sp.Rational(3, 5)]])
alpha = sp.Rational(3, 4)
target = alpha * rotation * initial
grid_float = np.array([list(x) for x in grid], dtype=float)
target_float = np.array([float(x) for x in target] + [1.0])
certificate = None
for _ in range(20000):
    ids = rng.sample(range(len(grid)), 4)
    a = np.vstack([grid_float[ids].T, np.ones(4)])
    try:
        weights = np.linalg.solve(a, target_float)
    except np.linalg.LinAlgError:
        continue
    if np.min(weights) < 1e-9:
        continue
    exact_a = sp.Matrix.vstack(sp.Matrix.hstack(*(grid[i] for i in ids)), sp.ones(1, 4))
    if exact_a.det() == 0:
        continue
    exact_w = exact_a.inv() * target.col_join(sp.Matrix([1]))
    assert all(w >= 0 for w in exact_w)
    assert sum(exact_w) == 1
    assert all(sp.simplify(x) == 0 for x in
               sp.Matrix.hstack(*(grid[i] for i in ids)) * exact_w - target)
    certificate = {"vertex_indices": ids,
                   "weights": [str(sp.simplify(w)) for w in exact_w],
                   "initial_bloch": [str(sp.simplify(x)) for x in initial],
                   "target_bloch": [str(sp.simplify(x)) for x in target],
                   "alpha": str(alpha)}
    break
assert certificate is not None

report = {
    "status": "PASS",
    "scope": "Exact finite symbolic fixtures and one rational barycentric row; not universal proof or priority certification",
    "spectral_spread_cases": spread_cases,
    "commutator_projection_cases": commutator_cases,
    "grassmann_graph_cases": grassmann_cases,
    "barycentric_row": certificate,
    "source_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT / "diagnostics.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
