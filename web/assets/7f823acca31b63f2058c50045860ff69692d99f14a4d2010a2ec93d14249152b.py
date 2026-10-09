#!/usr/bin/env python3
"""Reproducible model diagnostics for adaptive trophic attack-debt tipping.

This is a constructed two-patch model, not empirical validation. The optional
loss-memory term is a falsifiable hypothesis: recent alternate-prey loss
temporarily raises the shared consumer's attack pressure on focal prey.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class Params:
    r1: float = 1.2
    r2: float = 1.0
    allee: float = 0.22
    gamma: float = 0.8
    alpha: float = 1.0
    predation: float = 1.5
    beta_loss_memory: float = 3.0
    kappa_memory: float = 0.3
    demographic_turnover: float = 1.0


def stress(t: float, amplitude: float, ramp_duration: float) -> float:
    if amplitude <= 0.0:
        return 0.0
    if ramp_duration <= 0.0:
        return amplitude
    return amplitude * min(max(t / ramp_duration, 0.0), 1.0)


def allee_growth(x: float, p: Params) -> float:
    return p.r1 * (x - p.allee) * (1.0 - x)


def vector_field(y: np.ndarray, t: float, amplitude: float,
                 ramp_duration: float, p: Params, beta: float | None = None,
                 gate_open: bool = True):
    x1, x2, q, s = y[:4]
    u = stress(t, amplitude, ramp_duration)
    dx2 = x2 * (p.r2 * (1.0 - x2) - u)
    # s is a decaying memory of the realized alternate-prey loss flux.
    loss_flux = max(0.0, -dx2)
    beta_eff = p.beta_loss_memory if beta is None else beta
    q_target = p.alpha * max(0.0, 1.0 - x2) + beta_eff * s
    q_attack = q if gate_open else 0.0
    dx1 = x1 * (allee_growth(x1, p) - p.predation * q_attack)
    dq = p.gamma * (q_target - q)
    ds = loss_flux - p.kappa_memory * s
    # Exposure and nonlinear compensatory growth, for the exact log identity.
    return np.array([dx1, dx2, dq, ds, q_attack,
                     (x1 - p.allee) * (1.0 - x1)])


def rk4_step(y, t, dt, amplitude, ramp_duration, p, beta, gate_open):
    f = vector_field
    k1 = f(y, t, amplitude, ramp_duration, p, beta, gate_open)
    k2 = f(y + 0.5 * dt * k1, t + 0.5 * dt, amplitude,
           ramp_duration, p, beta, gate_open)
    k3 = f(y + 0.5 * dt * k2, t + 0.5 * dt, amplitude,
           ramp_duration, p, beta, gate_open)
    k4 = f(y + dt * k3, t + dt, amplitude, ramp_duration, p, beta, gate_open)
    return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def static_fold(p: Params):
    q_fold = p.r1 * (1.0 - p.allee) ** 2 / (4.0 * p.predation)
    u_fold = p.r2 * q_fold / p.alpha
    return q_fold, u_fold


def static_roots(u: float, p: Params):
    qeq = p.alpha * u / p.r2
    disc = (1.0 - p.allee) ** 2 - 4.0 * p.predation * qeq / p.r1
    if disc < 0.0 or u >= p.r2:
        return None
    root = math.sqrt(max(0.0, disc))
    return ((1.0 + p.allee - root) / 2.0,
            (1.0 + p.allee + root) / 2.0)


def deterministic_case(case: dict, p: Params, horizon: float, dt: float):
    y = np.array([case["x10"], 1.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    n = int(math.ceil(horizon / dt))
    min_x = y[0]
    peak_q = 0.0
    peak_s = 0.0
    first_allee = None
    first_low_root = None
    max_log_identity_error = 0.0
    q_fold, _ = static_fold(p)
    roots = static_roots(case["amplitude"], p)
    low_root = roots[0] if roots else None
    for i in range(n):
        t = i * dt
        before = y.copy()
        y = rk4_step(y, t, dt, case["amplitude"], case["ramp_duration"],
                     p, case.get("beta"), case.get("gate_open", True))
        y[:4] = np.maximum(y[:4], 0.0)
        # RK stages remain inside the ecological range for these parameters;
        # clipping only removes roundoff-scale negatives.
        y[0:2] = np.minimum(y[0:2], 1.0)
        min_x = min(min_x, y[0])
        peak_q = max(peak_q, y[2])
        peak_s = max(peak_s, y[3])
        if first_allee is None and before[0] > p.allee >= y[0]:
            first_allee = t + dt
        if (low_root is not None and first_low_root is None
                and t + dt >= case["ramp_duration"]
                and before[0] > low_root >= y[0]):
            first_low_root = t + dt
        if p.allee <= y[0] <= 1.0:
            log_error = (math.log(y[0] / case["x10"])
                         - p.r1 * y[5] + p.predation * y[4])
            max_log_identity_error = max(max_log_identity_error, abs(log_error))
    row = {
        "label": case["label"],
        "stress_endpoint": case["amplitude"],
        "ramp_duration": case["ramp_duration"],
        "initial_focal_density": case["x10"],
        "loss_memory_gain": p.beta_loss_memory if case.get("beta") is None else case["beta"],
        "consumer_access_gate_open": case.get("gate_open", True),
        "minimum_focal_density": float(min_x),
        "first_crossing_of_allee_boundary": first_allee,
        "first_crossing_of_final_low_equilibrium": first_low_root,
        "peak_attack_pressure": float(peak_q),
        "peak_effective_attack_pressure": float(peak_q if case.get("gate_open", True) else 0.0),
        "peak_loss_memory": float(peak_s),
        "final_state": [float(v) for v in y[:4]],
        "max_log_identity_residual_before_underflow": max_log_identity_error,
        "static_equilibria_at_endpoint": list(roots) if roots else None,
        "time_above_static_fold_attack_pressure": None,
        "attack_debt_at_allee_hit": None,
        "required_log_margin_at_allee": math.log(case["x10"] / p.allee),
    }
    # Re-run the deterministic path only as needed for two exact path summaries.
    y = np.array([case["x10"], 1.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    above_fold_time = 0.0
    debt_at_hit = None
    for i in range(n):
        t = i * dt
        before = y.copy()
        y = rk4_step(y, t, dt, case["amplitude"], case["ramp_duration"],
                     p, case.get("beta"), case.get("gate_open", True))
        y[:4] = np.maximum(y[:4], 0.0)
        y[0:2] = np.minimum(y[0:2], 1.0)
        if (y[2] if case.get("gate_open", True) else 0.0) > q_fold:
            above_fold_time += dt
        if debt_at_hit is None and before[0] > p.allee >= y[0]:
            debt_at_hit = p.predation * y[4] - p.r1 * y[5]
    row["time_above_static_fold_attack_pressure"] = above_fold_time
    row["attack_debt_at_allee_hit"] = debt_at_hit
    return row


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return [None, None]
    phat = k / n
    den = 1.0 + z * z / n
    center = (phat + z * z / (2.0 * n)) / den
    half = z * math.sqrt(phat * (1.0 - phat) / n + z * z / (4.0 * n * n)) / den
    return [max(0.0, center - half), min(1.0, center + half)]


def stochastic_case(amplitude, ramp_duration, x10, p, N, reps, horizon, dt,
                    rng, beta=None, gate_open=True):
    """Tau-leap diagnostic with absorbing zero counts; not empirical evidence."""
    beta_eff = p.beta_loss_memory if beta is None else beta
    outcomes = []
    for _ in range(reps):
        n1 = max(1, int(round(N * x10)))
        n2 = N
        q = 0.0
        s = 0.0
        crossed = False
        extinct = False
        for j in range(int(math.ceil(horizon / dt))):
            t = j * dt
            x1, x2 = n1 / N, n2 / N
            u = stress(t, amplitude, ramp_duration)
            g1 = allee_growth(x1, p) - p.predation * (q if gate_open else 0.0)
            g2 = p.r2 * (1.0 - x2) - u
            turn = p.demographic_turnover
            b1, d1 = turn + max(g1, 0.0), turn + max(-g1, 0.0)
            b2, d2 = turn + max(g2, 0.0), turn + max(-g2, 0.0)
            born1 = rng.poisson(n1 * b1 * dt) if n1 else 0
            died1 = rng.binomial(n1, 1.0 - math.exp(-d1 * dt)) if n1 else 0
            born2 = rng.poisson(n2 * b2 * dt) if n2 else 0
            died2 = rng.binomial(n2, 1.0 - math.exp(-d2 * dt)) if n2 else 0
            n1 = max(0, n1 + born1 - died1)
            n2 = max(0, n2 + born2 - died2)
            # s responds to the modelled stress-driven expected loss flux;
            # demographic birth/death noise is isolated in n1,n2 counts.
            loss_flux = max(0.0, -x2 * g2)
            s = s * math.exp(-p.kappa_memory * dt)
            if p.kappa_memory > 0.0:
                s += (loss_flux / p.kappa_memory) * (1.0 - math.exp(-p.kappa_memory * dt))
            x2_new = n2 / N
            target = p.alpha * max(0.0, 1.0 - x2_new) + beta_eff * s
            q = target + (q - target) * math.exp(-p.gamma * dt)
            crossed = crossed or n1 / N <= p.allee
            if n1 == 0:
                extinct = True
                break
        outcomes.append((crossed, extinct, n1 / N))
    k_cross = sum(int(row[0]) for row in outcomes)
    k_ext = sum(int(row[1]) for row in outcomes)
    return {
        "population_scale_N": N,
        "replicates": reps,
        "allee_crossings": k_cross,
        "allee_crossing_risk": k_cross / reps,
        "allee_crossing_wilson_95": wilson(k_cross, reps),
        "absorbing_extinctions": k_ext,
        "extinction_risk": k_ext / reps,
        "extinction_wilson_95": wilson(k_ext, reps),
        "mean_final_density": float(np.mean([row[2] for row in outcomes])),
    }


def equilibrium_spectrum(u: float, p: Params):
    roots = static_roots(u, p)
    if not roots:
        return {"endpoint": u, "exists": False}
    xminus, xplus = roots
    x2 = 1.0 - u / p.r2
    lam_x = p.r1 * xplus * (1.0 + p.allee - 2.0 * xplus)
    # At the loss-flux kink s=0, the one-sided Jacobian has the same diagonal
    # eigenvalues; off-diagonal trophic links make it triangular/nonnormal.
    vals = [lam_x, -p.r2 * x2, -p.gamma, -p.kappa_memory]
    return {
        "endpoint": u,
        "exists": True,
        "low_unstable_equilibrium": xminus,
        "high_stable_equilibrium": xplus,
        "one_sided_jacobian_eigenvalues": vals,
        "largest_real_eigenvalue": max(vals),
    }


def one_sided_transient_response(u: float, p: Params, beta: float,
                                 horizon: float = 20.0, dt: float = 0.001):
    """Linearized loss-pulse gain at the high equilibrium, for dx2(0)>0.

    A small positive alternate-prey displacement above its stressed equilibrium
    naturally declines back toward that equilibrium, so the positive-part loss
    flux is active on this side. Reported state responses are derivatives per
    unit-density perturbation, not finite perturbations.
    """
    roots = static_roots(u, p)
    if roots is None:
        return {"endpoint": u, "exists": False}
    _, xplus = roots
    x2eq = 1.0 - u / p.r2
    loss_rate = p.r2 * x2eq
    lam_x = p.r1 * xplus * (1.0 + p.allee - 2.0 * xplus)
    # State order is (x1, x2, q, s). This is the one-sided Jacobian for
    # perturbations above x2*, where spontaneous return decay makes L>0.
    J = np.array([
        [lam_x, 0.0, -p.predation * xplus, 0.0],
        [0.0, -loss_rate, 0.0, 0.0],
        [0.0, -p.gamma * p.alpha, -p.gamma, p.gamma * beta],
        [0.0, loss_rate, 0.0, -p.kappa_memory],
    ], dtype=float)
    v = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    samples = [(0.0, *v)]
    steps = int(math.ceil(horizon / dt))
    for i in range(steps):
        h = min(dt, horizon - i * dt)
        k1 = J @ v
        k2 = J @ (v + 0.5 * h * k1)
        k3 = J @ (v + 0.5 * h * k2)
        k4 = J @ (v + h * k3)
        v = v + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        samples.append(((i + 1) * h, *v))
    arr = np.asarray(samples)
    return {
        "endpoint": u,
        "exists": True,
        "beta_loss_memory": beta,
        "linearization_side": "dx2(0)>0; positive-part alternate-prey loss active",
        "initial_tangent_per_unit_dx2": [0.0, 1.0, 0.0, 0.0],
        "state_order": ["x1", "x2", "q", "s"],
        "one_sided_jacobian": J.tolist(),
        "eigenvalues": np.real_if_close(np.linalg.eigvals(J)).astype(float).tolist(),
        "peak_positive_q_response_per_unit_dx2": float(np.max(arr[:, 3])),
        "time_of_peak_positive_q_response": float(arr[int(np.argmax(arr[:, 3])), 0]),
        "minimum_q_response_per_unit_dx2": float(np.min(arr[:, 3])),
        "maximum_x1_response_per_unit_dx2": float(np.max(arr[:, 1])),
        "time_of_maximum_x1_response": float(arr[int(np.argmax(arr[:, 1])), 0]),
        "minimum_x1_response_per_unit_dx2": float(np.min(arr[:, 1])),
        "time_of_minimum_x1_response": float(arr[int(np.argmin(arr[:, 1])), 0]),
        "interpretation": "finite stable eigenvalues coexist with transient trophic gain; local tangent only",
    }


def run(seed: int, reps: int, dt: float):
    p = Params()
    horizon = 160.0
    q_fold, u_fold = static_fold(p)
    cases = [
        {"label": "R_fast_from_healthy_attractor", "amplitude": 0.09,
         "ramp_duration": 0.1, "x10": 1.0},
        {"label": "R_slow_same_endpoint_from_healthy_attractor", "amplitude": 0.09,
         "ramp_duration": 100.0, "x10": 1.0},
        {"label": "R_intermediate_ramp_3", "amplitude": 0.09,
         "ramp_duration": 3.0, "x10": 1.0},
        {"label": "R_intermediate_ramp_4", "amplitude": 0.09,
         "ramp_duration": 4.0, "x10": 1.0},
        {"label": "R_fast_no_loss_memory_control", "amplitude": 0.09,
         "ramp_duration": 0.1, "x10": 1.0, "beta": 0.0},
        {"label": "R_fast_consumer_access_gate_closed", "amplitude": 0.09,
         "ramp_duration": 0.1, "x10": 1.0, "gate_open": False},
        {"label": "B_slow_ramp_to_superfold_held", "amplitude": 0.14,
         "ramp_duration": 100.0, "x10": 1.0},
        # This reproduces the earlier basin-state contrast and labels it
        # correctly: it starts close to the Allee separator, not at an attractor.
        {"label": "near_separator_fast_basin_state", "amplitude": 0.09,
         "ramp_duration": 0.1, "x10": 0.225, "beta": 0.0},
        {"label": "near_separator_slow_basin_state", "amplitude": 0.09,
         "ramp_duration": 100.0, "x10": 0.225, "beta": 0.0},
    ]
    det = [deterministic_case(c, p, horizon, dt) for c in cases]
    rng = np.random.default_rng(seed)
    noise_horizon = 10.0
    noise_open = [stochastic_case(0.0, 0.0, 1.0, p, N, reps,
                                  noise_horizon, max(dt, 0.005), rng,
                                  gate_open=True)
                  for N in (80, 320, 1280)]
    noise_closed = [stochastic_case(0.0, 0.0, 1.0, p, N, reps,
                                   noise_horizon, max(dt, 0.005), rng,
                                   gate_open=False)
                    for N in (80, 320, 1280)]
    allee_noise = [stochastic_case(0.0, 0.0, 0.30, p, N, reps,
                                   noise_horizon, max(dt, 0.005), rng,
                                   gate_open=False)
                   for N in (80, 320, 1280)]
    return {
        "status": "finite model diagnostic only; proposed loss-memory law is unvalidated",
        "parameters": asdict(p),
        "seed": seed,
        "stochastic_replicates_per_N": reps,
        "deterministic_time_step": dt,
        "deterministic_horizon": horizon,
        "fold": {
            "q_fold": q_fold,
            "u_fold": u_fold,
            "formula": "u_B = r2*r1*(1-allee)^2/(4*predation*alpha)",
            "subfold_endpoint_roots": static_roots(0.09, p),
        },
        "frozen_equilibrium_spectra": [
            equilibrium_spectrum(0.0, p), equilibrium_spectrum(0.09, p),
        ],
        "one_sided_transient_response_at_subfold_endpoint": {
            "with_loss_memory": one_sided_transient_response(
                0.09, p, p.beta_loss_memory),
            "without_loss_memory": one_sided_transient_response(0.09, p, 0.0),
            "numerical_step": 0.001,
            "horizon": 20.0,
        },
        "deterministic_cases": det,
        "demographic_noise_diagnostics": {
            "stress_endpoint": 0.0,
            "horizon": noise_horizon,
            "healthy_initial_state_with_adaptive_access_open": noise_open,
            "same_state_with_consumer_access_gate_closed": noise_closed,
            "near_allee_initial_state_with_gate_closed": allee_noise,
        },
        "limitations": [
            "The recent-loss memory s and its gain beta are a falsifiable candidate, not an empirically established ecological law.",
            "The stochastic process is a tau-leap approximation to density-dependent birth/death dynamics; q and s follow expected stress-driven loss, not noisy abundance differences.",
            "No common environmental noise, dispersal, consumer abundance dynamics, or observation error is simulated.",
            "A high-field mesocosm must measure attack pressure and loss flux and use a sham access gate; independent tanks are randomized, not assumed to be exact ecosystem clones.",
            "Scaling demographic risk with N assumes comparable per-capita rates and spatial geometry; shared shocks do not vanish with N.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1509)
    ap.add_argument("--replicates", type=int, default=120)
    ap.add_argument("--dt", type=float, default=0.01)
    ap.add_argument("--output", type=str, default="")
    args = ap.parse_args()
    result = run(args.seed, args.replicates, args.dt)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered + "\n")
    print(rendered)


if __name__ == "__main__":
    main()
