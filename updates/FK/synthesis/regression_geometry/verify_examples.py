"""Independent exact checks for the regression-geometry counterexamples.

This script only uses definitions printed in REPORT.md.  It does not import
the incoming producer verifier or any Astra package code.
"""

from itertools import product
from pathlib import Path
import json

import sympy as sp


OUT = Path(__file__).with_name("check_results.json")


def check_singular_constraint_geometry():
    eps = sp.symbols("eps", positive=True)
    x0, y1, y2 = sp.symbols("x0 y1 y2", real=True)
    q1_expr = y1**2 - y2**2
    q2_expr = y1 * y2
    constraint_jacobian = sp.Matrix([q1_expr, q2_expr]).jacobian([x0, y1, y2])
    assert constraint_jacobian.subs({x0: 1, y1: 0, y2: 0}) == sp.zeros(2, 3)
    e0 = sp.Matrix([1, 0, 0])
    probs = [sp.Rational(3, 8), sp.Rational(1, 8), sp.Rational(1, 4), sp.Rational(1, 4)]
    us = [sp.Matrix([1, 0]), sp.Matrix([-1, 0]), sp.Matrix([0, 1]), sp.Matrix([0, -1])]
    EU = sum((p * u for p, u in zip(probs, us)), sp.zeros(2, 1))
    Eq1 = sum((p * (u[0] ** 2 - u[1] ** 2) for p, u in zip(probs, us)), sp.S.Zero)
    Eq2 = sum((p * u[0] * u[1] for p, u in zip(probs, us)), sp.S.Zero)
    Ev2 = sum((p * u.dot(u) for p, u in zip(probs, us)), sp.S.Zero)

    atoms = []
    for sign in (-1, 1):
        for p, u in zip(probs, us):
            x = sp.Matrix([sign, eps * sign * u[0], eps * sign * u[1]])
            atoms.append((sp.Rational(1, 2) * p, x))
    mean = sum((p * x for p, x in atoms), sp.zeros(3, 1))
    z = sum((p * x[0] * sp.Matrix(x[1:]) for p, x in atoms), sp.zeros(2, 1))
    v = sum((p * (x[1] ** 2 + x[2] ** 2) for p, x in atoms), sp.S.Zero)
    q1mean = sum((p * (x[1] ** 2 - x[2] ** 2) for p, x in atoms), sp.S.Zero)
    q2mean = sum((p * x[1] * x[2] for p, x in atoms), sp.S.Zero)

    assert EU == sp.Matrix([sp.Rational(1, 4), 0])
    assert Eq1 == Eq2 == 0 and Ev2 == 1
    assert mean == sp.zeros(3, 1)
    assert sp.simplify(q1mean) == sp.simplify(q2mean) == 0
    assert z == sp.Matrix([eps / 4, 0])
    assert sp.simplify(v - eps**2) == 0
    assert sp.simplify(z.norm() / v - 1 / (4 * eps)) == 0
    return {
        "balanced_quadratics": True,
        "mean_zero": True,
        "constraint_jacobian_at_e0_zero": True,
        "v": "eps^2",
        "z": "(eps/4, 0)",
        "ratio_norm_z_over_v": "1/(4 eps)",
    }


def check_multi_constraint_finsler_failure():
    # q_j=x_j^2-x_1^2, j=2,...,5; Q has C5 edge couplings.
    vals = []
    for sig in product((-1, 1), repeat=5):
        q = [sig[j] ** 2 - sig[0] ** 2 for j in range(1, 5)]
        assert all(v == 0 for v in q)
        edge_sum = sum(sig[j] * sig[(j + 1) % 5] for j in range(5))
        qstar = sp.Integer(3) + edge_sum
        vals.append(qstar)
    assert min(vals) == 0

    min_eig = sp.Rational(3, 5) - (1 + sp.sqrt(5)) / 4
    assert sp.simplify(min_eig - (7 - 5 * sp.sqrt(5)) / 20) == 0
    assert 7**2 < (5**2) * 5
    assert min_eig.is_negative
    return {
        "minimum_Q_on_common_null_cone_signs": "0",
        "averaged_psd_candidate_min_eigenvalue": "(7-5*sqrt(5))/20 < 0",
        "psd_plus_multipliers_representation": False,
    }


def check_tangent_contact_law():
    e = sp.symbols("e", positive=True)
    m = sp.Integer(9)
    w = 1 - sp.Rational(3, 2) * e
    t = sp.Rational(9, 2) * m**2 * e / w
    a, b, c, d = sp.symbols("a b c d", real=True)
    xx = sp.Matrix([a, b, c, d])
    I = sp.Matrix([1, 0, 0, 1])
    u = a**2 + c**2
    vcol = b**2 + d**2
    det = a * d - b * c
    G = 3 * (u + vcol - 2 * det) ** 2 + sp.Rational(35, 24) * u**2 + det**2 - sp.Rational(5, 2) * det * u
    grad = sp.Matrix([sp.diff(G, z) for z in xx])
    Hess = sp.hessian(G, xx)
    aa, bb, cc, dd = sp.symbols("aa bb cc dd", real=True)
    P0 = sp.Rational(1, 2) * (3 * aa - 2 * dd) ** 2 + sp.Rational(5, 6) * cc**2
    P0_hessian = sp.hessian(P0, [aa, bb, cc, dd])
    assert P0_hessian.rank() == 2
    assert P0_hessian * sp.Matrix([0, 1, 0, 0]) == sp.zeros(4, 1)

    Rt = sp.Matrix([0, 1, t, 0])
    S = sp.Matrix([1, 0, 0, sp.Rational(3, 2)])
    atoms = [
        (w / 2, Rt),
        (w / 2, -Rt),
        (e, m * S),
        (e / 2, -2 * m * S),
    ]

    def at(expr, atom):
        return expr.subs(dict(zip(xx, atom)))

    def E(expr):
        return sp.factor(sum((p * at(expr, atom) for p, atom in atoms), sp.S.Zero))

    meanX = sum((p * atom for p, atom in atoms), sp.zeros(4, 1))
    qmean = E(det)
    beta = E((grad.T * I)[0])
    h = E((I.T * Hess * I)[0])
    cmean = E(G)
    directional_gap = sp.factor(cmean - beta**2 / (2 * h))

    assert meanX == sp.zeros(4, 1)
    assert sp.factor(qmean) == 0
    assert sp.factor(beta - sp.Rational(5, 4) * e * m**3) == 0
    assert sp.factor(h - sp.Rational(135, 8) * m**4 * e**2 / w) == 0
    assert sp.limit(directional_gap, e, 0, dir="+") == -sp.Rational(3, 4)
    assert sp.limit(E(a**2 + c**2 + d**2), e, 0, dir="+") == 0
    assert sp.limit(E((a**2 + c**2 + d**2) ** 2), e, 0, dir="+") == 0
    assert sp.limit(E(b**2), e, 0, dir="+") == 1
    assert sp.limit(E(b**4), e, 0, dir="+") == 1

    e0 = sp.Rational(1, 10**6)
    assert directional_gap.subs(e, e0) < 0

    Hbar = sum((p * Hess.subs(dict(zip(xx, atom))) for p, atom in atoms), sp.zeros(4))
    pivots = [sp.factor(Hbar[:j, :j].det()).subs(e, e0) for j in range(1, 5)]
    assert all(v > 0 for v in pivots)

    C = sum((p * atom * atom.T for p, atom in atoms), sp.zeros(4))
    K = m**2 * e * sp.Matrix([[3, 9], [9, sp.Rational(27, 4)]])
    fit = w * b**2 + w * t**2 * c**2 + (sp.Matrix([a, d]).T * K * sp.Matrix([a, d]))[0]
    diff = sp.factor((xx.T * C * xx)[0] - fit)
    assert sp.factor(diff + 9 * m**2 * e * det) == 0
    Ktest = (w * sp.eye(2) - K).subs(e, e0)
    assert Ktest[0, 0] > 0 and Ktest.det() > 0 and t.subs(e, e0) < 1

    return {
        "mean_zero": True,
        "determinant_balance": True,
        "beta": "(5/4) eps m^3",
        "h": "(135/8) m^4 eps^2 / (1-3 eps/2)",
        "directional_gap_limit": "-3/4",
        "tangent_remainder_rank": 2,
        "negative_at_eps_1e-6": True,
        "averaged_hessian_positive_definite_at_eps_1e-6": True,
        "adaptive_line": "e12, unique among rank-one lines for sufficiently small eps",
    }


results = {
    "singular_constraint_geometry": check_singular_constraint_geometry(),
    "multi_constraint_finsler_failure": check_multi_constraint_finsler_failure(),
    "tangent_contact_law": check_tangent_contact_law(),
    "scope": "Exact identities and explicit finite laws only; no universal theorem or PDE compatibility is certified by this script.",
}
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(f"PASS: wrote {OUT.name}; three exact example groups checked")
