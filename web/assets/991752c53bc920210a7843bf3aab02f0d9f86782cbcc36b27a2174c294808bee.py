#!/usr/bin/env python3
"""Cost-bound calculator for the critical-spin product-preparation construction.

This is a high-precision numerical evaluation of explicit analytic bounds, not
an implementation or certification of the state-preparation sampler.
"""

import json
import math
import mpmath as mp


mp.mp.dps = 50


def logsumexp(xs):
    m = max(xs)
    return m + mp.log(sum(mp.exp(x - m) for x in xs))


def spin_finite_sum(N, M, B):
    """Evaluate the public D4 F_N and Addendum-A finite error certificate."""
    n = int(N)
    s2 = mp.mpf(n) ** mp.mpf("1.5")
    s = mp.mpf(n) ** mp.mpf("0.75")
    rows = []
    for j in range(n // 2 + 1):
        jj = mp.mpf(j)
        log_mult = (
            2 * mp.log(2 * jj + 1)
            - mp.log(n + 1)
            + mp.loggamma(n + 2)
            - mp.loggamma(n // 2 - jj + 1)
            - mp.loggamma(n // 2 + jj + 2)
        )
        log_a = log_mult + 2 * jj * (jj + 1) / n
        x = jj * (jj + 1) / s2
        ell = jj / s
        rows.append((log_a, x, ell))

    zbase = logsumexp([la - M * x for la, x, _ in rows])
    fnum = []
    enum = []
    for la, x, ell in rows:
        q = 6 * M * x + B * ell
        fnum.append(la + 5 * M * x + B * ell + 2 * mp.log(q) if q > 0 else mp.ninf)
        p = 2 * M * x + B * ell
        enum.append(la + M * x + B * ell + mp.log(p + p * p / 3) if p > 0 else mp.ninf)
    F_N = mp.exp(logsumexp(fnum) - zbase)
    E_N = (3 * M / (2 * s2)) * mp.exp(logsumexp(enum) - zbase)
    return F_N, E_N


def optimize_young(Msum, B, N, zlower):
    delta = mp.mpf("0.5") - mp.log(mp.cosh(1))
    a = delta / 16
    nroot = mp.sqrt(N)

    def bound(lam):
        lam = mp.mpf(lam)
        D = (Msum + lam) / 2
        alpha = delta * nroot / 4 - D - 1 / (4 * nroot)
        if alpha <= 0:
            return mp.inf
        core = mp.mpf("0.5") * mp.exp(D * D / (4 * a)) * (
            mp.sqrt(D / (2 * a)) * mp.sqrt(mp.pi / a)
            + mp.gamma(mp.mpf(3) / 4) * a ** (-mp.mpf(3) / 4)
        )
        tail = mp.sqrt(mp.pi) / (4 * alpha ** (mp.mpf(3) / 2))
        return (
            3
            * mp.exp(B * B / (4 * lam) + mp.mpf(1) / 6)
            * core
            / zlower
            + 3 * mp.exp(B * B / (4 * lam)) * tail / zlower
        )

    if B == 0:
        return mp.mpf(0), bound(mp.mpf("1e-100"))

    lo, hi = mp.mpf("1e-6"), mp.mpf(2)
    phi = (mp.sqrt(5) - 1) / 2
    x1 = hi - phi * (hi - lo)
    x2 = lo + phi * (hi - lo)
    for _ in range(220):
        if bound(x1) <= bound(x2):
            hi, x2 = x2, x1
            x1 = hi - phi * (hi - lo)
        else:
            lo, x1 = x1, x2
            x2 = lo + phi * (hi - lo)
    lam = (lo + hi) / 2
    return lam, bound(lam)


def main():
    M = mp.mpf("0.1")
    B = mp.mpf("0.2")
    N = 50000
    delta = mp.mpf("0.5") - mp.log(mp.cosh(1))
    a = delta / 16

    # Original displayed constants.
    L0 = mp.mpf(7) / 3 * mp.exp(-M / 2 - mp.mpf(1) / 12)
    Cg = mp.sqrt(mp.pi) / 4 * (mp.exp(mp.mpf(3) / 4) * 768 ** (mp.mpf(3) / 4) + 1)
    Dold = (6 * M + 1) / 2
    Ztilt = (
        mp.exp(mp.mpf(1) / 2 + 384 * Dold**2)
        * 1536 ** (mp.mpf(3) / 4)
        * mp.gamma(mp.mpf(3) / 4)
        / 4
        + mp.sqrt(mp.pi) / 4
    )
    K2old = 3 * mp.exp(B**2 / 4) * Ztilt / L0

    # Improved two-Maxwell seed envelope.
    beta = mp.sqrt(3 * a)
    Ccore = mp.exp(mp.mpf(11) / 12) * mp.sqrt(mp.pi) / (4 * beta ** (mp.mpf(3) / 2))
    alpha_seed = (delta * N - 1) / (4 * mp.sqrt(N))
    Ctail = mp.sqrt(mp.pi) / (4 * alpha_seed ** (mp.mpf(3) / 2))
    Zlower = mp.quad(
        lambda r: r**2 * mp.exp(-M * r**2 / 8 - r**4 / 192), [0, 8]
    )
    seed_attempts = (Ccore + Ctail) / Zlower

    # Same bound with an explicitly known anisotropy spectrum.  The chosen
    # example has eigenvalues (.10,-.08,.03), so shifting by .08 gives
    # C=A+.08I with trace .29, rather than the public worst-case 6M=.60.
    S_actual = mp.mpf("0.29")
    shift_actual = mp.mpf("0.08")
    Zlower_actual = mp.quad(
        lambda r: r**2 * mp.exp(-shift_actual * r**2 / 8 - r**4 / 192), [0, 8]
    )
    lam_star, K2new = optimize_young(S_actual, B, N, Zlower_actual)
    F_N, E_N = spin_finite_sum(N, M, B)

    # A separate full-output budget: E_sep + 2 eta + epsilon_num <= 0.1.
    eta = mp.mpf("0.049")
    eps = mp.mpf("0.001")
    m = int(mp.ceil(F_N / eta))
    R = int(mp.ceil(K2new / eta**2))
    p0inv = seed_attempts
    K = int(mp.ceil(p0inv * mp.log(16 * R / eps)))
    draw_cap = 3 * R * (K + m)
    L = mp.sqrt(2 * mp.log(32 * draw_cap / eps))
    sigma_max = 768 ** (mp.mpf(1) / 4) / mp.sqrt(2)
    LR = sigma_max * mp.sqrt(3) * (L + 1)
    Cr = sigma_max * mp.sqrt(3) + 2
    Ctau = sigma_max * mp.sqrt(3) + 4
    U = mp.sqrt(3 * S_actual * m / 8) / mp.mpf(N) ** mp.mpf("0.75")
    Q = U * LR + B / (4 * mp.mpf(N) ** mp.mpf("0.75"))
    Cpath = N * mp.exp(4 * Q) * (Ctau + 3 * mp.e * (U + 4 * m))
    La = mp.mpf("0.5") + shift_actual * LR / 4 + LR**3 / 48 + 2 * LR
    h = min(
        1 / (4 * (U + 4 * m)),
        eps / (256 * Cpath),
        eps / (128 * R * K * (La * Cr + 4)),
    )
    ell = int(mp.ceil(-mp.log(h, 2)))
    cdf_bisections = int(mp.ceil(mp.log((L + 1) / h, 2)))
    normals_expected = 3 * R * (m + p0inv)
    normals_max = draw_cap

    out = {
        "scope": "Numerical evaluation of explicit analytic bounds only; no sampler/compiler executed.",
        "case": {"N": N, "M_public": str(M), "B_public": str(B), "A_eigenvalues_example": ["0.10", "-0.08", "0.03"]},
        "delta": mp.nstr(delta, 14),
        "old_seed_expected_attempt_upper": mp.nstr(Cg / L0, 14),
        "new_seed_expected_attempt_upper": mp.nstr(seed_attempts, 14),
        "new_seed_components": {"core_envelope_mass": mp.nstr(Ccore, 14), "tail_envelope_mass": mp.nstr(Ctail, 14), "certified-form_lower-integral_numeric": mp.nstr(Zlower, 14)},
        "old_K2star": mp.nstr(K2old, 14),
        "new_data_dependent_K2_bound": mp.nstr(K2new, 14),
        "new_Young_parameter": mp.nstr(lam_star, 14),
        "new_K2_over_eta_squared_at_eta_0.1": mp.nstr(K2new / mp.mpf("0.01"), 14),
        "F_N_real_arithmetic_discretization_constant": mp.nstr(F_N, 14),
        "E_sep_public_finite_N_bound": mp.nstr(E_N, 14),
        "m_at_eta_0.1_upper_ceil_scale": mp.nstr(mp.ceil(F_N / mp.mpf("0.1")), 14),
        "proposal_count_at_eta_0.1_bound": mp.nstr(mp.ceil(K2new / mp.mpf("0.01")), 14),
        "scalar_update_product_at_eta_0.1_bound": mp.nstr(mp.ceil(K2new / mp.mpf("0.01")) * mp.ceil(F_N / mp.mpf("0.1")), 14),
        "target_0.1_budget": {
            "eta": str(eta),
            "numerical_epsilon": str(eps),
            "proved_target_error_form": "E_sep,N + 2*eta + epsilon",
            "m": m,
            "Rprop": R,
            "seed_attempt_cap_per_proposal": K,
            "normal_draw_cap": normals_max,
            "normal_draw_expected_upper_from_seed_attempt_bound": mp.nstr(normals_expected, 14),
            "normal_truncation_L": mp.nstr(L, 10),
            "path_radius_bound_LR": mp.nstr(LR, 10),
            "path_Q": mp.nstr(Q, 10),
            "dyadic_step_h_upper": mp.nstr(h, 10),
            "working_precision_bits_ell": ell,
            "inverse_CDF_bisection_count_per_normal_upper": cdf_bisections,
            "normal_uniform_bits_order_per_draw": mp.nstr(ell + L**2 + mp.log(L + 1, 2), 10),
            "expected_local_qubit_emissions_per_output_state": N,
            "gate_compilation": "excluded; native one-qubit preparation error/runtime is a supplied interface"
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
