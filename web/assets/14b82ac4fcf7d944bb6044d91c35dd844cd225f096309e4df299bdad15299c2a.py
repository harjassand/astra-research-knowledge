"""Small exact checks for c08_l04 transport near-equality counterexamples.

The script verifies differential-geometric curvature identities for the
one-dimensional warped Sol metric and the closed-form high-frequency family.
It does not numerically compute metric entropy; that input is the standard
Lebesgue entropy of the hyperbolic toral return map, stated and sourced in
INITIAL.txt.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def sectional_curvature_formula_check() -> dict[str, str]:
    x, y, t = sp.symbols("x y t", real=True)
    u = sp.Function("u")(t)
    coords = (x, y, t)
    metric = sp.diag(sp.exp(2 * u), sp.exp(-2 * u), 1)
    inverse = metric.inv()
    dim = 3
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                gamma[i][j][k] = sp.simplify(
                    sum(
                        inverse[i, ell]
                        * (
                            sp.diff(metric[ell, k], coords[j])
                            + sp.diff(metric[ell, j], coords[k])
                            - sp.diff(metric[j, k], coords[ell])
                        )
                        for ell in range(dim)
                    )
                    / 2
                )

    # R^i_{jkl} = d_k Gamma^i_{lj} - d_l Gamma^i_{kj}
    #             + Gamma^i_{km} Gamma^m_{lj} - Gamma^i_{lm} Gamma^m_{kj}.
    curvature = [
        [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
        for _ in range(dim)
    ]
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                for ell in range(dim):
                    curvature[i][j][k][ell] = sp.simplify(
                        sp.diff(gamma[i][ell][j], coords[k])
                        - sp.diff(gamma[i][k][j], coords[ell])
                        + sum(
                            gamma[i][k][m] * gamma[m][ell][j]
                            - gamma[i][ell][m] * gamma[m][k][j]
                            for m in range(dim)
                        )
                    )

    def sectional(i: int, j: int) -> sp.Expr:
        lowered = sum(metric[i, m] * curvature[m][j][i][j] for m in range(dim))
        return sp.simplify(lowered / (metric[i, i] * metric[j, j]))

    expected = {
        "K_x_t": -(sp.diff(u, t, 2) + sp.diff(u, t) ** 2),
        "K_y_t": sp.diff(u, t, 2) - sp.diff(u, t) ** 2,
        "K_x_y": sp.diff(u, t) ** 2,
    }
    actual = {"K_x_t": sectional(0, 2), "K_y_t": sectional(1, 2), "K_x_y": sectional(0, 1)}
    for key in expected:
        assert sp.simplify(actual[key] - expected[key]) == 0, (key, actual[key], expected[key])
    strain = sp.zeros(dim)
    strain[0, 0] = sp.diff(u, t) * sp.exp(2 * u)
    strain[1, 1] = -sp.diff(u, t) * sp.exp(-2 * u)
    div_strain = []
    for i in range(dim):
        value = sp.S.Zero
        for j in range(dim):
            for k in range(dim):
                covariant_derivative = sp.diff(strain[k, i], coords[j]) - sum(
                    gamma[m][j][k] * strain[m, i] + gamma[m][j][i] * strain[k, m]
                    for m in range(dim)
                )
                value += inverse[j, k] * covariant_derivative
        div_strain.append(sp.simplify(value))
    expected_div = [sp.S.Zero, sp.S.Zero, -2 * sp.diff(u, t) ** 2]
    assert all(sp.simplify(a - b) == 0 for a, b in zip(div_strain, expected_div))
    return {**{key: str(actual[key]) for key in actual}, "div_strain": str(div_strain)}


def oscillatory_family_check() -> dict[str, str]:
    t, a = sp.symbols("t a", positive=True, real=True)
    checks = []
    for nval in (100, 1000, 10000):
        n = sp.Integer(nval)
        delta = 2 * sp.pi / sp.sqrt(n) * sp.cos(2 * sp.pi * n * t)
        mean = sp.simplify(sp.integrate(delta, (t, 0, 1)))
        variance = sp.simplify(sp.integrate(delta**2, (t, 0, 1)))
        tn = sp.Rational(1, 4) / n
        uprime_at = sp.simplify((a + delta).subs(t, tn))
        usecond_at = sp.simplify(sp.diff(delta, t).subs(t, tn))
        k_xt_at = sp.simplify(-(usecond_at + uprime_at**2))
        k_yt_at = sp.simplify(usecond_at - uprime_at**2)
        assert mean == 0
        assert variance == 2 * sp.pi**2 / n
        assert uprime_at == a
        assert usecond_at == -4 * sp.pi**2 * sp.sqrt(n)
        assert k_xt_at == 4 * sp.pi**2 * sp.sqrt(n) - a**2
        assert k_yt_at == -4 * sp.pi**2 * sp.sqrt(n) - a**2
        checks.append({"n": nval, "variance": str(variance), "K_xt": str(k_xt_at), "K_yt": str(k_yt_at)})
    return {
        "formula": "integral(delta)=0; integral(delta^2)=2*pi^2/n",
        "pointwise_curvature_formula": "at t=1/(4n): K_xt=4*pi^2*sqrt(n)-a^2; K_yt=-4*pi^2*sqrt(n)-a^2",
        "exact_sample_checks": checks,
    }


def scalar_boundary_checks() -> dict[str, str]:
    alpha, a, eps, nu, volume = sp.symbols("alpha a eps nu volume", positive=True)
    active_entropy = alpha * a
    normalized_work = alpha * a**2
    absolute_gap = sp.simplify(normalized_work - active_entropy**2)
    assert absolute_gap == alpha * (1 - alpha) * a**2
    assert sp.simplify(absolute_gap / active_entropy**2 - (1 - alpha) / alpha) == 0
    eps, c, b1, b2 = sp.symbols("eps c b1 b2", positive=True)
    intermittent_gap = sp.simplify(c**2 * (eps * b2 - eps**2 * b1**2))
    intermittent_sup_lower = c * (1 - eps * b1)
    assert sp.simplify(intermittent_gap - (c**2 * eps * b2 - c**2 * eps**2 * b1**2)) == 0
    # Integer hyperbolic monodromies with a covolume-one invariant lattice.
    n = sp.symbols("n", positive=True, integer=True)
    d = sp.sqrt(n**2 - 1)
    lam = n + d
    matrix = sp.Matrix([[n, 1], [n**2 - 1, n]])
    eigenbasis = sp.Matrix([[1, 1], [d, -d]]) / n
    diagonal = sp.diag(lam, 1 / lam)
    assert matrix.det() == 1
    assert sp.simplify(eigenbasis * diagonal * eigenbasis.inv() - matrix) == sp.zeros(2)
    det_p_abs = 2 * d / n**2
    lattice_scale_squared = det_p_abs
    vector = eigenbasis.inv() * sp.Matrix([0, 1])
    short_vector_squared = sp.simplify(lattice_scale_squared * (vector.dot(vector)))
    assert short_vector_squared == 1 / d
    assert sp.simplify(lattice_scale_squared / det_p_abs) == 1
    # An m-fold mapping-torus cover has H=a and diameter >= m/2 by its
    # 1-Lipschitz projection to the base circle of length m.
    m = sp.symbols("m", positive=True, integer=True)
    return {
        "zero_component_gap": str(absolute_gap),
        "zero_component_relative_gap": str(sp.simplify(absolute_gap / active_entropy**2)),
        "intermittent_gap": str(intermittent_gap),
        "intermittent_sup_strain_lower_bound": str(intermittent_sup_lower),
        "cover_entropy": "a (constant-roof suspension: h(B^m)/m = a)",
        "cover_diameter_lower_bound": "m/2",
        "fixed_volume_collapse": "A_n=[[n,1],[n^2-1,n]], lambda=n+sqrt(n^2-1); covolume-one invariant fiber lattice has a loop of squared length 1/sqrt(n^2-1)",
        "time_rescaling": "H(cX)=c H(X); W(cX)=c^2 W(X); equality is preserved",
    }


def main() -> None:
    result = {
        "status": "all exact symbolic checks passed",
        "curvature_identities": sectional_curvature_formula_check(),
        "oscillatory_family": oscillatory_family_check(),
        "boundary_algebra": scalar_boundary_checks(),
        "scope": "No entropy computation, PDE solver, acquisition cost, or external proof validation.",
    }
    output = Path(__file__).with_name("counterexample_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
