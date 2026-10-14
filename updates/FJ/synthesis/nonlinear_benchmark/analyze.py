#!/usr/bin/env python3
"""Exact certificate and matched deterministic/MLP work analysis.

Uses only Python's standard library. Fourier arithmetic is floating-point and is
reported as a diagnostic, not an interval-verified reference solution.
"""
from __future__ import annotations

import cmath
import json
import math
from fractions import Fraction as Q
from pathlib import Path

OUT = Path(__file__).resolve().parent
D = 8
J = 16
H_Q = Q(1, 40)
EPS = 0.01
DELTA = 0.05


def certificate() -> dict:
    # e0 is the exact screened linear solution for each displayed Fourier mode.
    A = Q(5, 102) + Q(5, 103)
    lo, hi = 1 - A, 1 + A
    R = 25 * (6*A*A + 4*A**3 + A**4)
    lam = 1 + 100*lo**3
    Lam = 1 + 100*hi**3
    B2, B3, B4 = 150*hi**2, 100*hi, Q(25)
    h = H_Q
    P = B2*h**2 + B3*h**3 + B4*h**4
    Gamma = 2*B2*h + 3*B3*h**2 + 4*B4*h**3
    slack = lam*h - R - P
    # For any h >= 0, lambda*h - P(h) <= lambda*h - B2*h^2
    # <= lambda^2/(4*B2). A residual bound above this value cannot pass
    # the enclosure inequality for any tube radius.
    R_critical_upper = lam*lam/(4*B2)
    assert A < 1 and R > 0 and lam > 0 and Lam >= lam
    assert slack > 0 and Gamma < lam
    q_fj = 1 - (lam-Gamma)/Lam
    expected_nodes = Lam/(lam-Gamma)
    n_fj = math.ceil(2*float(h*h)/(EPS*EPS)*math.log(2/DELTA))

    vmid = (lam+Lam)/2
    lam_mlp = vmid/2
    L_mlp = (Lam-lam)/4 + Gamma/2
    q_mlp = L_mlp/lam_mlp
    assert L_mlp < lam_mlp
    # Exact MLP Corollary 3.11 bound after bounding its source integral by
    # (R/2)^2/(lambda-L). Here G(x,z) is the fixed-point integrand.
    mlp_constant = (R/2) / ((math.sqrt(float(lam_mlp))-math.sqrt(float(L_mlp)))
                            * math.sqrt(float(lam_mlp-L_mlp)))
    target_rms = math.sqrt(DELTA)*EPS
    threshold = ((math.sqrt(float(lam_mlp))+math.sqrt(float(L_mlp)))
                 /(math.sqrt(float(lam_mlp))-math.sqrt(float(L_mlp))))**2
    m_min = math.floor(threshold) + 1

    best = None
    mlp_search_max_M = 100_000
    for M in range(m_min, mlp_search_max_M + 1):
        beta = (1+(1+math.sqrt(M))*math.sqrt(float(q_mlp)))/math.sqrt(M)
        if beta >= 1:
            continue
        n = max(1, math.ceil(math.log(target_rms/mlp_constant)/math.log(beta)))
        if mlp_constant * beta**n > target_rms:
            n += 1
        # The full-history recursion includes one endpoint at every summand:
        # C_0=0; C_n=M^n + sum M^(n-k)(1+C_k+C_(k-1)).
        C = [0]*(n+1)
        for level in range(1, n+1):
            C[level] = M**level + sum(
                M**(level-k)*(1+C[k]+C[k-1]) for k in range(1, level)
            )
        candidate = (C[n], M, n, beta, mlp_constant*beta**n)
        if best is None or candidate[0] < best[0]:
            best = candidate
    assert best is not None

    # Lower bound for black-box certificate acquisition: an evaluator-only
    # verifier must rule out one smooth bump in each disjoint support ball.
    rho = Q(1, 8)
    centers_per_axis = math.floor(math.pi/float(rho))
    hidden_bump_locations = centers_per_axis**D

    return {
        "model": "-Delta u + u + 25 u^4 = 26 + 10 g(x), x in T^8",
        "g_definition": "(1/16) sum_j cos(k_j dot x + phase_j); k_j=e_j and e_j+e_(j+1 mod 8)",
        "dimension": D,
        "mode_count": J,
        "query": [0.21+0.19*i for i in range(D)],
        "predictor": "v=1+e0; e0=(10/16) sum_j cos(k_j dot x+phase_j)/(101+|k_j|^2)",
        "source_supplied_coeff_l1_certificate": "sum abs(source Fourier amplitudes) <= 1, hence |g|<=1",
        "certificate_exact_rationals": {
            "A_e0": str(A), "R": str(R), "lambda_lower": str(lam),
            "Lambda_proposal": str(Lam), "h": str(h), "B2": str(B2),
            "B3": str(B3), "B4": str(B4), "P_h": str(P),
            "Gamma_h": str(Gamma), "enclosure_slack": str(slack),
            "q_fj_upper": str(q_fj), "expected_nodes_per_query": str(expected_nodes),
            "largest_residual_bound_that_could_pass_any_tube_radius_upper": str(R_critical_upper),
        },
        "certificate_float_summary": {
            "R": float(R), "lambda_lower": float(lam), "Lambda_proposal": float(Lam),
            "h": float(h), "P_h": float(P), "Gamma_h": float(Gamma),
            "enclosure_slack": float(slack), "q_fj_upper": float(q_fj),
            "expected_nodes_per_query": float(expected_nodes),
            "mlp_lambda": float(lam_mlp), "mlp_L": float(L_mlp),
            "mlp_q_upper": float(q_mlp),
            "deterministic_first_correction_error_bound": float(q_mlp*float(h)),
        },
        "point_sampler_contract": {
            "epsilon": EPS, "confidence": 1-DELTA,
            "Hoeffding_samples": n_fj,
            "expected_endpoint_nodes_upper": n_fj*float(expected_nodes),
            "model_evaluator_cost_per_node": "8 Gaussian coordinates + 16 phases, each 8-term dot product and cosine, then scalar branch arithmetic",
            "build_and_certificate_cost": "16 mode entries; exact rational bounds use O(16*8) elementary coefficient operations; no grid/reference solve",
        },
        "published_elliptic_MLP_pointwise_certificate": {
            "source": "Beck, Gonon, Jentzen (2024), Corollary 3.11 and Theorem 3.16",
            "confidence_to_rms": target_rms,
            "M_threshold_strict": threshold,
            "minimum_integer_M_for_Theorem_3_16": m_min,
            "searched_integer_M_range": [m_min, mlp_search_max_M],
            "optimized_published_bound_choice": {
                "endpoint_nodes_per_realization": int(best[0]),
                "M": best[1], "level": best[2], "beta": best[3],
                "rms_bound": best[4],
                "one_endpoint_evaluator_cost": "same 16-mode v/r/V evaluation as point sampler; full-history MLP evaluates every recursion endpoint",
            },
            "scope_note": "This is the published uniform-bound certificate, not an empirical lower bound on a tuned MLP or a custom Fourier-aware implementation.",
        },
        "deterministic_comparator": {
            "constant_tangent": float(vmid),
            "first_Picard_correction": "e1=(-Delta+Vmid)^(-1) r; output v(xq)+e1(xq)",
            "certified_error_bound": float(q_mlp*float(h)),
            "target_met": float(q_mlp*float(h)) < EPS,
            "source_support_signed_modes": 32,
            "V_fourier_candidate_modes": 3825,
            "r_fourier_candidate_modes": 21487,
            "exact_sparse_convolution_complex_products": 32*32 + 465*32 + 465*465,
            "query_mode_evaluations": 21487,
            "warning": "The sparse Fourier correction arithmetic is floating point here; the analytic contraction error bound is exact once e1 is evaluated. No interval arithmetic is claimed.",
        },
        "black_box_certificate_obstruction": {
            "support_radius": str(rho),
            "centers_per_axis": centers_per_axis,
            "disjoint_hidden_bump_locations": hidden_bump_locations,
            "lower_bound": "An evaluator-only worst-case verifier making fewer than this many point queries cannot certify that a residual is zero / below a threshold that an unqueried smooth bump of height 10 violates.",
            "fixed_certificate_threshold": float(R_critical_upper),
            "height_10_fails_enclosure_for_every_tube_radius": Q(10) > R_critical_upper,
            "scope": "This applies only when no symbolic representation or supplied global majorant is available. The Fourier benchmark above supplies its coefficient representation, so its certificate is cheap.",
        },
    }


def sparse_fourier_diagnostic() -> dict:
    modes = []
    for i in range(D):
        k = [0]*D; k[i] = 1; modes.append((tuple(k), 1))
    for i in range(D):
        k = [0]*D; k[i] = 1; k[(i+1) % D] = 1; modes.append((tuple(k), 2))
    phases = [0.17*(j+1)+0.013*(j+1)*(j+1) for j in range(J)]
    E0 = {}
    for j, (k, norm2) in enumerate(modes):
        amplitude = (10/J)/(101+norm2)
        for sign in (1, -1):
            kk = tuple(sign*z for z in k)
            E0[kk] = amplitude*cmath.exp(1j*sign*phases[j])/2

    def conv(a, b):
        out = {}
        for ka, va in a.items():
            for kb, vb in b.items():
                key = tuple(x+y for x, y in zip(ka, kb))
                out[key] = out.get(key, 0j) + va*vb
        return out

    E2 = conv(E0, E0)
    E3 = conv(E2, E0)
    E4 = conv(E2, E2)
    residual = {}
    for source, scale in ((E2, -150), (E3, -100), (E4, -25)):
        for k, value in source.items():
            residual[k] = residual.get(k, 0j) + scale*value
    residual = {k: v for k, v in residual.items() if abs(v) > 1e-14}
    A = 5/102+5/103
    lam = 1+100*(1-A)**3
    Lam = 1+100*(1+A)**3
    Vmid = (lam+Lam)/2
    x = [0.21+0.19*i for i in range(D)]
    correction = 0j
    weighted_l1 = 0.0
    for k, value in residual.items():
        norm2 = sum(z*z for z in k)
        phase = sum(kk*xx for kk, xx in zip(k, x))
        correction += value/(Vmid+norm2)*cmath.exp(1j*phase)
        weighted_l1 += abs(value)/(Vmid+norm2)
    predictor = 1+sum((a*cmath.exp(1j*sum(kk*xx for kk, xx in zip(k, x)))).real
                       for k, a in E0.items())
    return {
        "fourier_support": {"e0_signed": len(E0), "e0_squared": len(E2),
                            "e0_cubed": len(E3), "e0_fourth": len(E4),
                            "residual": len(residual)},
        "sparse_convolution_product_count": 32*32+465*32+465*465,
        "query": [0.21+0.19*i for i in range(D)],
        "predictor_at_query": predictor,
        "constant_tangent_correction_at_query": correction.real,
        "deterministic_first_correction_estimate": predictor+correction.real,
        "l1_weighted_sup_bound_for_correction": weighted_l1,
        "warning": "Floating-point coefficient convolution and evaluation; not interval verified.",
    }


if __name__ == "__main__":
    result = certificate()
    result["sparse_fourier_diagnostic"] = sparse_fourier_diagnostic()
    (OUT/"analysis_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
