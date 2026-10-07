#!/usr/bin/env python3
"""Small reproducible arithmetic audit of STOPPED_DIFFUSION cost constants.

This evaluates only displayed bounds and the proposed larger inner ball; it
does not simulate the SDE or certify the theorem/algorithm.
"""
import json
import math
from pathlib import Path


def record(M: float, B: float, N: int, theta: float = 0.99) -> dict:
    L = 2 * M + 1
    T = 3 * L
    lam = M + 1
    # Positive root of (1-x)^2-Lx=0, written without cancellation.
    xstar = 2 / (L + 2 + math.sqrt(L * L + 4 * L))
    x_new = theta * xstar
    r_new = math.sqrt(x_new)
    gap_new = (1 - x_new) ** 2 - L * x_new
    gap_identity = (1 - theta) * (1 - theta * xstar * xstar)

    x_old = 1 / (16 * (L + 1))
    r_old = math.sqrt(x_old)
    a_old = 2 * math.atanh(r_old / 2)
    a_new = 2 * math.atanh(r_new / 2)
    delta = 0.5 - math.log(math.cosh(1))
    kappa_old = min(a_old**4 / 768, delta / 4)
    # STOPPED_DIFFUSION's radial exponent, strengthened by the quartic bound
    # f(u)>=delta*u^4 on 0<=u<=1 (the companion L08 INITIAL lemma).
    kappa_new = min(delta * a_new**4 / 16, delta / 4)

    h = L * math.sqrt(N) / 4 + L / (2 * math.sqrt(N)) + B * N**0.25 / 2
    kappa1_old = r_old**2 / (256 * L)
    kappa1_new = r_new**2 / (256 * L)
    beta_old = T * r_old / (2 * math.sqrt(N)) + 3 * T * r_old / (4 * N**1.5) + B / (2 * N**0.75)
    beta_new = T * r_new / (2 * math.sqrt(N)) + 3 * T * r_new / (4 * N**1.5) + B / (2 * N**0.75)

    return {
        "input": {"M": M, "B": B, "N": N, "theta": theta},
        "constants": {"Lambda": lam, "Lc": L, "Tc_upper": T, "delta": delta},
        "old_ball": {
            "r0": r_old,
            "seed_exponent_kappa0": kappa_old,
            "kappa0_times_N": kappa_old * N,
            "hit_exponent_kappa1_N15": kappa1_old * N**1.5,
            "drift_beta": beta_old,
            "r0_over_8": r_old / 8,
        },
        "theta_root_ball": {
            "xstar": xstar,
            "r0": r_new,
            "ellipticity_lower_bound": gap_new,
            "ellipticity_identity_check": gap_identity,
            "seed_radius_a0": a_new,
            "seed_exponent_kappa0": kappa_new,
            "kappa0_times_N": kappa_new * N,
            "hit_exponent_kappa1_N15": kappa1_new * N**1.5,
            "drift_beta": beta_new,
            "r0_over_8": r_new / 8,
        },
        "weight_cap": {
            "hN": h,
            "exp_hN": math.exp(h),
            "log10_exp_hN": h / math.log(10),
            "global_rejection_proposals_if_trace_lower_1_over_2": 2 * math.exp(h),
            "binary_integer_bits_for_weight_value": math.ceil(h / math.log(2)),
            "bits_for_logweight_range_plus_fractional_p": {
                "formula": "ceil(log2(hN+1))+p",
                "at_p_40": math.ceil(math.log2(h + 1)) + 40,
            },
        },
        "proposed_seed_envelope": {
            "seed_quartic_coefficient_c": delta / 16,
            "net_seed_quadratic_coefficient_after_g": (L - lam) / 16,
            "note": "g(R) leading R^2 coefficient is L/16; heat seed contributes -Lambda/16; quartic tail remains integrable.",
        },
        "scope": "Formula evaluation only; no interval proof, sampler, SDE solver, or local-qubit run.",
    }


def main() -> None:
    cases = [record(0.1, 0.2, 50_000), record(0.1, 0.2, 1_000_000)]
    for item in cases:
        gap = item["theta_root_ball"]["ellipticity_lower_bound"]
        identity = item["theta_root_ball"]["ellipticity_identity_check"]
        assert abs(gap - identity) < 1e-12
        assert gap > 0
    out = {"scope": "Displayed-bound arithmetic only; see sibling report for proof and implementation gaps.", "cases": cases}
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
