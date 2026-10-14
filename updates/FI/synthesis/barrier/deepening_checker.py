#!/usr/bin/env python3
"""Exact scalar identities and scoped finite-time/noise consequences.

This checker is independent of the supplied sampled-root verifier. It proves
the polynomial identities symbolically, evaluates the normalized U=0.55 b
case, and records asymptotic one-coordinate Gibbs/Laplace diagnostics. Those
finite-volume diagnostics are conditional on the stated scalar model; they
are not a physical BaTiO3 prediction.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def bisect_root(fn, lo: float, hi: float, iterations: int = 200) -> float:
    flo, fhi = fn(lo), fn(hi)
    if flo * fhi > 0:
        raise ValueError("root is not bracketed")
    for _ in range(iterations):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def main() -> None:
    q, b, c, u, U, C, K, alpha, e0 = sp.symbols(
        "q b c u U C K alpha e0", positive=True
    )
    a = sp.Rational(3, 16) * b**2 / c
    qb2 = sp.Rational(3, 4) * b / c
    f0 = a * q**2 / 2 - b * q**4 / 4 + c * q**6 / 6
    assert sp.factor(f0 - c * q**2 * (q**2 - qb2) ** 2 / 6) == 0

    # Middle-stage lower Hessian bound and the requested partial gate.
    mu = a - sp.Rational(9, 20) * (b - U) ** 2 / c
    partial = sp.Rational(11, 20) * b
    mu_partial = sp.factor(mu.subs(U, partial))
    assert sp.simplify(mu_partial / a - sp.Rational(257, 500)) == 0
    threshold_fraction = 1 - sp.sqrt(sp.Rational(5, 12))
    assert sp.simplify(mu.subs(U, threshold_fraction * b)) == 0

    # Tangent compensation is the Bregman divergence of G(q)=q^4/4.
    # Use B as an independent symbol to keep the factorization exact.
    B = sp.symbols("B", positive=True)
    bregman_B = q**4 / 4 - B**4 / 4 - B**3 * (q - B)
    assert sp.factor(bregman_B) == (q - B) ** 2 * (q**2 + 2 * B * q + 3 * B**2) / 4

    # Local elastic shunt elimination, plus a prestretched reference spring.
    e = sp.symbols("e", real=True)
    estar = C * alpha * q**2 / (C + K)
    elastic = C * (e - alpha * q**2) ** 2 / 2 + K * e**2 / 2
    uK = 2 * alpha**2 * C * K / (C + K)
    elastic_min = sp.simplify(elastic.subs(e, estar))
    assert sp.simplify(elastic_min - uK * q**4 / 4) == 0
    assert sp.simplify(sp.diff(elastic_min, K) - estar**2 / 2) == 0

    estar_pre = (C * alpha * q**2 + K * e0) / (C + K)
    elastic_pre = C * (e - alpha * q**2) ** 2 / 2 + K * (e - e0) ** 2 / 2
    elastic_pre_min = sp.simplify(elastic_pre.subs(e, estar_pre))
    pre_expansion = uK * q**4 / 4 - uK * e0 * q**2 / (2 * alpha) + uK * e0**2 / (4 * alpha**2)
    assert sp.simplify(elastic_pre_min - pre_expansion) == 0
    assert sp.simplify(
        sp.diff(elastic_pre_min, K) - (estar_pre - e0) ** 2 / 2
    ) == 0

    # Reversible control work and a constant-friction finite-time floor.
    qb = sp.sqrt(qb2)
    field_work = sp.integrate(a * q - b * q**3 + c * q**5 + U * q**3, (q, 0, qb))
    gate_return = -U * qb2**2 / 4
    assert sp.simplify(field_work - U * qb2**2 / 4) == 0
    assert sp.simplify(field_work + gate_return) == 0
    zeta, tau = sp.symbols("zeta tau", positive=True)
    ratio = sp.simplify((zeta * qb2 / tau) / (U * qb2**2 / 4))
    ratio_partial = sp.simplify(ratio.subs(U, partial))
    tau_rel = zeta / a
    assert sp.simplify(ratio_partial - sp.Rational(20, 11) * tau_rel / tau) == 0

    # The mean-only clamp has a different zero-mean Hessian from a local gate.
    mean_mode_min = a - (3 * b - U) ** 2 / (20 * c)
    assert sp.simplify(mean_mode_min.subs(U, b) + a / 15) == 0
    mean_mode_partial = sp.factor(mean_mode_min.subs(U, partial) / a)
    assert sp.simplify(mean_mode_partial + sp.Rational(901, 1500)) == 0

    # For a two-site graph Laplacian, adding PSD onsite margins to a PSD
    # coupling preserves the strong-convexity lower bound.
    x1, x2, kappa = sp.symbols("x1 x2 kappa", nonnegative=True)
    shifted_two_site_hessian = sp.Matrix([[x1 + kappa, -kappa], [-kappa, x2 + kappa]])
    assert sp.simplify(shifted_two_site_hessian.det() - (x1 * x2 + kappa * (x1 + x2))) == 0

    # Positive semidefinite nonlocal quartic kernels need not be convex in q.
    q1, q2 = sp.symbols("q1 q2", real=True)
    J = sp.Matrix([[1, -1], [-1, 1]])
    rvec = sp.Matrix([q1**2, q2**2])
    G = sp.expand((rvec.T * J * rvec)[0] / 4)
    H_G = sp.hessian(G, (q1, q2))
    H_example = H_G.subs({q1: 1, q2: 0})
    assert sp.factor(G - (q1**2 - q2**2) ** 2 / 4) == 0
    assert J.eigenvals() == {sp.Integer(0): 1, sp.Integer(2): 1}
    assert H_example == sp.diag(3, -1)

    # Scalar finite-volume Gibbs/Laplace weights at exact coexistence.
    # Contributions scale as 1/sqrt(f''(q_i)): a at 0 and 4a at +/-qB.
    p0, pplus, pminus = sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 4)
    entropy_nats = -sum(float(p) * math.log(float(p)) for p in (p0, pplus, pminus))
    assert abs(entropy_nats - 1.5 * math.log(2)) < 1e-15

    # Under the final tangent-compensated removal h=u qB^3, small-u Laplace
    # ratios are p0/pB ~ 2 exp(-3x/4), pminus/pB ~ exp(-2x),
    # x = V u qB^4/(k_B T). Find the asymptotic 99%-occupancy threshold.
    eps = 0.01
    initial_x_star = 4 * math.log((1 - eps) / eps)
    def bad_to_good_ratio(x: float) -> float:
        return 2 * math.exp(-0.75 * x) + math.exp(-2 * x)
    target = eps / (1 - eps)
    x_star = bisect_root(lambda x: bad_to_good_ratio(x) - target, 0.0, 100.0)

    # During the strongly convex middle stage, Brascamp-Lieb gives
    # Var(q) <= kBT/(V mu); report the scale-free width condition.
    mu_over_a = sp.Rational(257, 500)

    # Exact scalar mean-field parameter screen from the supplied coefficient
    # choice. It is reproduced by the original verifier and remains conditional.
    b_num, c_num = 6.76e8, 6 * 2.37e9
    a_num = 3 * b_num**2 / (16 * c_num)
    qb_num = math.sqrt(3 * b_num / (4 * c_num))
    U_num = 0.55 * b_num
    mu_num = a_num - 9 * (b_num - U_num) ** 2 / (20 * c_num)

    result = {
        "scope": "symbolic scalar identities plus conditional one-coordinate finite-volume asymptotics",
        "exact_checks": {
            "coexistence_factorization": True,
            "middle_curvature_partial_gate_mu_over_a": "257/500",
            "minimum_gate_fraction_for_strong_convexity": float(threshold_fraction),
            "tangent_bregman_factorization": True,
            "zero_preload_elimination": True,
            "preload_quadratic_shift_and_work_term": True,
            "ideal_quasistatic_field_gate_work_cancellation": True,
            "finite_time_dissipation_ratio_partial_gate": "(20/11)*(tau_relax/tau)",
            "mean_only_gate_at_U_equals_b_mode_minimum": "-a/15",
            "mean_only_gate_at_U_0.55b_mode_minimum_over_a": "-901/1500",
            "local_gate_plus_psd_graph_coupling_sufficient_condition": True,
            "positive_semidefinite_kernel_nonconvex_countermodel": True,
        },
        "finite_time": {
            "dynamics": "zeta*qdot = h - (f0'(q)+U*q^3), constant zeta, exact monotone q:0->qB in tau",
            "dissipation_density_lower_bound": "zeta*qB^2/tau",
            "partial_gate_fraction": 0.55,
            "loss_over_ideal_circulated_work_lower_bound": "(20/11)*(tau_relax/tau)",
            "excluded_costs": ["shunt hysteresis", "dielectric loss", "leakage", "actuator and field-generation losses", "heat transfer"],
        },
        "compatibility_kernel_countermodel": {
            "kernel": [[1, -1], [-1, 1]],
            "kernel_eigenvalues": [0, 2],
            "gate": "G(q1,q2)=(q1^2-q2^2)^2/4 >= 0",
            "hessian_at_q1_1_q2_0": [[3, 0], [0, -1]],
            "general_hessian": "diag(J*r)+2*diag(q)*J*diag(q), r_i=q_i^2",
            "sufficient_convexity_condition": "symmetric PSD J with entrywise J_ij>=0",
            "scope": "abstract nonlocal quartic countermodel, not a BaTiO3 compatibility kernel",
        },
        "finite_volume_noise": {
            "model": "single uniform scalar coordinate with Gibbs density proportional exp(-V*f/(kBT)); Laplace approximation around the three nondegenerate coexistence wells",
            "zero_control_well_probabilities_asymptotic": {"q=0": 0.5, "q=+qB": 0.25, "q=-qB": 0.25},
            "coarse_grained_equilibrium_entropy_nats": entropy_nats,
            "restricted_state_free_energy_costs_from_equilibrium": {"select_q0": "kBT*ln(2)", "select_plus_qB": "kBT*ln(4)"},
            "initial_gate_engagement": {
                "x_definition": "x=V*u*qB^4/(kBT)",
                "small_u_polar_to_central_ratio": "exp(-x/4) + o(1)",
                "epsilon_target": eps,
                "x_threshold_for_central_phase_probability_at_least_1_minus_epsilon": initial_x_star,
                "interpretation": "the u=0 initial equilibrium is a mixture; selecting q=0 with high confidence requires gate work or prior state preparation",
            },
            "middle_stage_variance_bound": "Var(q) <= kBT/(V*mu)",
            "middle_stage_mu_over_a_at_U_0.55b": str(mu_over_a),
            "terminal_tangent_removal": {
                "x_definition": "x=V*u*qB^4/(kBT)",
                "small_u_laplace_ratios": {"central_to_plus_phase": "2*exp(-3*x/4) + o(1)", "minus_to_plus_phase": "exp(-2*x) + o(1)"},
                "epsilon_target": eps,
                "x_threshold_for_plus_phase_probability_at_least_1_minus_epsilon": x_star,
                "residual_gate_requirement": "u >= x_threshold*kBT/(V*qB^4), asymptotically",
                "residual_bias_requirement": "h=u*qB^3 >= x_threshold*kBT/(V*qB), asymptotically",
                "interpretation": "high-confidence equilibrium phase selection is incompatible with taking both controls fully to zero; full restoration requires finite-time metastable retention or other boundary selection, with lifetime and work separately measured",
            },
            "limitations": ["uniform single-coordinate model only", "Laplace asymptotics do not resolve domains or nucleation", "not a BaTiO3 prediction"],
        },
        "conditional_BaTiO3_coefficient_choice": {
            "source_table_B": -1.69e8,
            "source_table_D": 2.37e9,
            "mapped_b": b_num,
            "mapped_c": c_num,
            "coexistence_set_a": a_num,
            "polarization_qB_C_per_m2": qb_num,
            "U_0.55b": U_num,
            "mu_same_units_as_a": mu_num,
            "status": "reproduced only as the stated frozen Table 1 coefficient choice; primary Table 1/end-note sextic sign discrepancy unresolved",
        },
    }
    out = Path(__file__).with_name("deepening_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
