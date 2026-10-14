#!/usr/bin/env python3
"""Independent exact audit of the mixed local/mean quartic gate theorem."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def main() -> None:
    q, v, b, c, theta = sp.symbols("q v b c theta", positive=True)
    a = 3 * b**2 / (16 * c)
    beta = (1 - theta) * b
    f0 = lambda x: a * x**2 / 2 - b * x**4 / 4 + c * x**6 / 6
    h = a * v + c * v**5

    # Independently factor the scalar summand in the stage-2 vector gap.
    D = (
        f0(q)
        - f0(v)
        + theta * b * (q**4 - v**4) / 4
        + beta * v**2 * (q**2 - v**2) / 2
        - h * (q - v)
    )
    P4 = q**4 + 2 * q**3 * v + 3 * q**2 * v**2 + 4 * q * v**3 + 5 * v**4
    K = a / 2 - beta * (q + v) ** 2 / 4 + c * P4 / 6
    assert sp.factor(D - (q - v) ** 2 * K) == 0

    # Verify the exact N=3 vector gap decomposition by direct expansion.
    xs = sp.symbols("x0:3", real=True)
    S2 = sum(x**2 for x in xs)
    hvec = a * v + c * v**5
    vector_energy = (
        sum(f0(x) - hvec * x + theta * b * x**4 / 4 for x in xs)
        + beta * S2**2 / (4 * len(xs))
    )
    ref_energy = (
        len(xs) * (f0(v) - hvec * v + theta * b * v**4 / 4)
        + beta * (len(xs) * v**2) ** 2 / (4 * len(xs))
    )
    D_i = lambda x: (
        f0(x) - f0(v) + theta * b * (x**4 - v**4) / 4
        + beta * v**2 * (x**2 - v**2) / 2 - hvec * (x - v)
    )
    assert sp.factor(
        vector_energy - ref_energy - sum(D_i(x) for x in xs)
        - beta * (S2 - len(xs) * v**2) ** 2 / (4 * len(xs))
    ) == 0

    # Sharp uniform-in-N scalar criterion: minimize K in y=v^2 at fixed t=q/v.
    t = sp.symbols("t", nonnegative=True)
    Pt = t**4 + 2 * t**3 + 3 * t**2 + 4 * t + 5
    R = Pt / (t + 1) ** 4
    assert sp.factor(sp.diff(R, t) - 2 * (t**3 - 3 * t - 8) / (t + 1) ** 5) == 0
    alpha_poly = t**3 - 3 * t - 8
    alpha = sp.CRootOf(alpha_poly, 0)
    assert alpha.is_real
    assert sp.simplify(alpha**3 - 3 * alpha - 8) == 0
    # The cubic decreases on [0,1], increases on [1,infinity), and crosses
    # between 2 and 3: this is the unique positive critical point of R.
    assert alpha_poly.subs(t, 1) < 0 and alpha_poly.subs(t, 2) < 0 and alpha_poly.subs(t, 3) > 0
    Rmin = sp.simplify(R.subs(t, alpha))
    theta_path = 1 - sp.sqrt(Rmin)
    y = sp.symbols("y", nonnegative=True)
    K_t = a / 2 - beta * (t + 1) ** 2 * y / 4 + c * Pt * y**2 / 6
    K_min = sp.factor(K_t.subs(y, 3 * beta * (t + 1) ** 2 / (4 * c * Pt)))
    K_min_expected = 3 * b**2 / (32 * c) * (1 - (beta / b) ** 2 / R)
    assert sp.factor(K_min - K_min_expected) == 0

    # The minimizing scale at t=alpha lies inside the prescribed path interval
    # 0<=v,q<=qB for every 0<=theta<=1.
    path_ratio_v = sp.factor((t + 1) ** 2 / Pt)
    path_ratio_q = sp.factor(t**2 * (t + 1) ** 2 / Pt)
    assert sp.factor(Pt - (t + 1) ** 2) == t**4 + 2 * t**3 + 2 * t**2 + 2 * t + 4
    assert sp.factor(Pt - t**2 * (t + 1) ** 2) == 2 * t**2 + 4 * t + 5
    # For theta<theta_path, K_min<0; one-site deviations add only O(1/N).
    defect_term = beta * (q**2 - v**2) ** 2 / (4 * sp.Symbol("N", positive=True))
    assert sp.limit(defect_term, sp.Symbol("N", positive=True), sp.oo) == 0

    # Check the tangent-compensated mixed gate removal identity exactly.
    B, U = sp.symbols("B U", positive=True)
    ys = sp.symbols("y0:4", real=True)
    Sy = sum(z**2 for z in ys)
    Gmix = theta * U * sum(z**4 for z in ys) / 4 + (1 - theta) * U * Sy**2 / (4 * len(ys))
    remainder = Gmix - U * len(ys) * B**4 / 4 - U * B**3 * sum(z - B for z in ys)
    positive_form = (
        theta * U * sum((z - B) ** 2 * (z**2 + 2 * B * z + 3 * B**2) for z in ys) / 4
        + (1 - theta) * U * (Sy - len(ys) * B**2) ** 2 / (4 * len(ys))
        + (1 - theta) * U * B**2 * sum((z - B) ** 2 for z in ys) / 2
    )
    assert sp.expand(remainder - positive_form) == 0

    # Uniform Hessian spectrum and the two distinct stability thresholds.
    theta_linear = 1 - sp.sqrt(sp.Rational(15, 16))
    theta_convex = 1 - sp.sqrt(sp.Rational(5, 12))
    theta_linear_equivalent = 1 - sp.sqrt(15) / 4
    assert sp.simplify(theta_linear - theta_linear_equivalent) == 0
    assert sp.simplify(theta_convex - (1 - sp.sqrt(15) / 6)) == 0
    assert 0 < float(theta_linear) < float(theta_path) < float(theta_convex) < 1
    # Full Hessian lower bound and its asymptotic sharpness as N grows.
    scalar_curvature_min = a - 9 * beta**2 / (20 * c)
    assert sp.simplify(scalar_curvature_min.subs(beta, b * (1 - theta_convex))) == 0

    # Exact finite-amplitude witness, computed from the defining energy only.
    n_num = 32
    th_num, v_num, w_num = sp.Rational(1, 10), sp.Rational(1, 4), sp.Rational(5, 8)
    b_num = c_num = 1
    a_num = sp.Rational(3, 16)
    beta_num = (1 - th_num) * b_num
    h_num = a_num * v_num + c_num * v_num**5
    base = lambda z: a_num * z**2 / 2 - b_num * z**4 / 4 + c_num * z**6 / 6
    E_num = lambda zs: (
        sum(base(z) - h_num * z + th_num * b_num * z**4 / 4 for z in zs)
        + beta_num * (sum(z**2 for z in zs)) ** 2 / (4 * len(zs))
    )
    delta = sp.factor(E_num([w_num] + [v_num] * (n_num - 1)) - E_num([v_num] * n_num))
    D_num = sp.factor(D.subs({q: w_num, v: v_num, b: b_num, c: c_num, theta: th_num}))
    mode_min = sp.factor(a_num - beta_num**2 / 5)
    assert delta == -sp.Rational(3969, 5242880)
    assert D_num == -sp.Rational(3969, 2621440)
    assert mode_min == sp.Rational(51, 2000)
    assert sp.simplify(delta - D_num - beta_num * (w_num**2 - v_num**2) ** 2 / (4 * n_num)) == 0

    # Coherent homogeneous-path ideal work is unchanged by the local/mean split.
    qb2 = 3 * b / (4 * c)
    qb = sp.sqrt(qb2)
    path_field_work = sp.integrate(a * v + c * v**5, (v, 0, qb))
    homogeneous_gate_work = b * qb2**2 / 4
    assert sp.simplify(path_field_work - homogeneous_gate_work) == 0

    result = {
        "status": "PASS",
        "source_under_audit": "work/FI-root/mixed_compliance_gate.py and work/FI-root/MIXED_GATE_RESULTS.json",
        "independent_method": "symbolic expansion and exact rational finite-cell energy evaluation; no source module imported",
        "exact_checks": {
            "stage2_vector_gap_decomposition": True,
            "scalar_Bregman_factorization": True,
            "threshold_derivative_and_cubic": True,
            "necessity_scale_inside_0_to_qB": True,
            "tangent_compensated_mixed_gate_removal_identity": True,
            "homogeneous_hessian_thresholds_ordered": True,
            "finite_amplitude_counterexample": True,
            "homogeneous_path_ideal_work_matches_scalar_gate": True,
        },
        "thresholds": {
            "alpha": "unique positive root of t^3-3t-8=0",
            "alpha_numeric": float(sp.N(alpha, 18)),
            "theta_global_path": float(sp.N(theta_path, 18)),
            "theta_homogeneous_linear_stability": float(theta_linear),
            "theta_full_functional_convexity_uniform_in_N": float(theta_convex),
            "proof_scope": "theta_global_path is the sharp sufficient/necessary threshold uniform over all N for the stated exact tangent path; necessity uses a one-site defect as N grows",
        },
        "finite_amplitude_counterexample": {
            "N": n_num,
            "theta": str(th_num),
            "reference_v": str(v_num),
            "one_site_alternative_q": str(w_num),
            "uniform_bias": str(h_num),
            "scalar_tangent_gap": str(D_num),
            "total_energy_difference": str(delta),
            "minimum_homogeneous_transverse_curvature": str(mode_min),
            "reference_and_alternative_within_qB": True,
        },
        "energy_boundary": {
            "coherent_path_ideal_field_work_per_site": "b*qB^4/4",
            "coherent_path_ideal_gate_return_per_site": "-b*qB^4/4",
            "net_reversible_work": 0,
            "finite_rate_losses_noise_and_actuator_costs": "not evaluated by this mixed-gate audit",
        },
        "qualification": "conditional control ansatz only; no acquired elastic kernel, constitutive law, prototype, novelty, physical energy advantage, or material performance claim",
    }
    out = Path(__file__).with_name("DELTA_MIXED_GATE_RESULTS.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
