#!/usr/bin/env python3
"""Exact-algebra / numerical CTMC checks for the one-shot Janus DA scheme."""

from __future__ import annotations

from fractions import Fraction as F
from math import exp, isclose, sqrt


def eigen_rates(km: float, kf: float, ks: float) -> tuple[float, float]:
    K = kf + ks
    disc = (km + K) ** 2 - 4.0 * km * ks
    assert disc >= -1e-14
    root = sqrt(max(0.0, disc))
    return ((km + K - root) / 2.0, (km + K + root) / 2.0)


def survival_start_closed(t: float, km: float, kf: float, ks: float) -> float:
    """P(not L by t | start D), via the transient 2x2 eigenvalues."""
    lam_minus, lam_plus = eigen_rates(km, kf, ks)
    gap = lam_plus - lam_minus
    if gap <= 1e-12 * max(1.0, lam_plus):
        lam = 0.5 * (lam_plus + lam_minus)
        return exp(-lam * t) * (1.0 + lam * t)
    return (lam_plus * exp(-lam_minus * t) - lam_minus * exp(-lam_plus * t)) / gap


def direct_lock_start_open(tau: float, kf: float, ks: float) -> float:
    """P(first exit from U is L by tau), excluding return-to-D/reopen paths."""
    K = kf + ks
    if K == 0.0:
        return 0.0
    beta = ks / K
    return beta * (1.0 - exp(-K * tau))


def rk4_survival(t: float, km: float, kf: float, ks: float, steps: int = 200_000) -> float:
    """Independent numerical check of the three-state forward equations."""
    dt = t / steps
    d, u, locked = 1.0, 0.0, 0.0

    def rhs(x: tuple[float, float, float]) -> tuple[float, float, float]:
        d0, u0, _ = x
        return (-km * d0 + kf * u0,
                km * d0 - (kf + ks) * u0,
                ks * u0)

    for _ in range(steps):
        x = (d, u, locked)
        k1 = rhs(x)
        k2 = rhs(tuple(x[i] + 0.5 * dt * k1[i] for i in range(3)))
        k3 = rhs(tuple(x[i] + 0.5 * dt * k2[i] for i in range(3)))
        k4 = rhs(tuple(x[i] + dt * k3[i] for i in range(3)))
        d, u, locked = tuple(
            x[i] + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0
            for i in range(3)
        )
    assert abs(d + u + locked - 1.0) < 1e-9
    return d + u


def main() -> None:
    # Generic positive-rate fixture: eigenvalue survival equals independent
    # integration of the finite-state forward equations.
    km, kf, ks, t = 0.4, 0.8, 0.2, 1.3
    s_exact = survival_start_closed(t, km, kf, ks)
    s_rk4 = rk4_survival(t, km, kf, ks)
    assert abs(s_exact - s_rk4) < 2e-10

    # Repeated-root boundary kf=0 and km=ks=K gives Erlang-2 survival.
    t_deg = 0.7
    s_deg = survival_start_closed(t_deg, 1.0, 0.0, 1.0)
    assert isclose(s_deg, exp(-t_deg) * (1.0 + t_deg), rel_tol=1e-14)

    # Edge cases with no route to lock survive forever.
    assert survival_start_closed(100.0, 0.0, 2.0, 1.0) == 1.0
    assert isclose(survival_start_closed(100.0, 2.0, 3.0, 0.0), 1.0, abs_tol=1e-14)
    assert direct_lock_start_open(10.0, 0.0, 0.0) == 0.0

    # Direct first-exit probability from U is exactly beta*(1-exp(-K*tau)).
    tau, kf_r, ks_r = 20.0, 1.0 / 95.0, 0.2
    K_r = kf_r + ks_r
    beta_r = ks_r / K_r
    p_repair = direct_lock_start_open(tau, kf_r, ks_r)
    assert isclose(p_repair, beta_r * (1.0 - exp(-K_r * tau)), rel_tol=1e-14)

    # Exact odds-contrast identity for fixed kS and rational branch fractions.
    ks_q = F(1, 5)
    beta_i, beta_r_q = F(1, 100), F(19, 20)
    kf_i = ks_q * (1 - beta_i) / beta_i
    kf_r_q = ks_q * (1 - beta_r_q) / beta_r_q
    lhs = kf_i / kf_r_q
    odds_ratio = (beta_r_q / (1 - beta_r_q)) / (beta_i / (1 - beta_i))
    assert lhs == odds_ratio == F(1881)

    # Illustrative (not fitted) separation: rare intact opening plus a much
    # lower recontact return rate gives low finite storage risk and high direct
    # lock probability. Use exact survival for storage.
    km_i, kf_i_float, ks_float = 1e-7, 19.8, 0.2
    storage_time = 100_000.0
    storage_survival = survival_start_closed(storage_time, km_i, kf_i_float, ks_float)
    storage_lock_risk = 1.0 - storage_survival
    assert storage_lock_risk < 2e-4
    assert p_repair > 0.93

    # With unchanged rates, repair's direct probability cannot exceed beta;
    # the same beta that helps repair also enters long-time storage hazard.
    beta_i_float = ks_float / (kf_i_float + ks_float)
    assert direct_lock_start_open(1e6, kf_i_float, ks_float) <= beta_i_float + 1e-14

    print("PASS: transient survival, direct first-exit lock, and branch-odds checks")
    print(f"generic survival: eigen={s_exact:.12f}, RK4={s_rk4:.12f}")
    print(f"repeated-root survival e^(-t)(1+t): {s_deg:.12f}")
    print(f"fixed-kS branch contrast required: kF_intact/kF_recontact = {lhs} exactly")
    print(f"illustrative storage lock risk over {storage_time:g} time units: {storage_lock_risk:.6g}")
    print(f"illustrative recontact direct-lock probability over {tau:g} time units: {p_repair:.6f}")


if __name__ == "__main__":
    main()
