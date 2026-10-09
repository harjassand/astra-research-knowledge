#!/usr/bin/env python3
"""Finite simulations for an adaptive two-patch predator-prey mechanism.

The ecological state is (x1, x2, q): focal-prey density in patch 1, alternate-
prey density in patch 2, and the consumer's adaptive allocation to prey 1.
External stress u(t) acts on prey 2. The deterministic equations have a real
Allee basin boundary; the stochastic version is a density-dependent birth-
death process with an absorbing zero-count state. This is model evidence only.
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
    turnover: float = 1.0


def ramp(t: float, amplitude: float, duration: float) -> float:
    if amplitude <= 0:
        return 0.0
    if duration <= 0:
        return amplitude
    return amplitude * min(max(t / duration, 0.0), 1.0)


def rhs(state: np.ndarray, t: float, amplitude: float, ramp_duration: float,
        p: Params, gate_open: bool = True):
    x1, x2, q = state
    u = ramp(t, amplitude, ramp_duration)
    q_effective = q if gate_open else 0.0
    g1 = p.r1 * (x1 - p.allee) * (1.0 - x1) - p.predation * q_effective
    g2 = p.r2 * (1.0 - x2) - u
    q_target = p.alpha * max(0.0, 1.0 - x2)
    return np.array([x1 * g1,
                     x2 * g2,
                     p.gamma * (q_target - q) if gate_open else 0.0], dtype=float)


def deterministic(amplitude: float, ramp_duration: float, x10: float, p: Params,
                  horizon: float, dt: float, gate_open: bool = True):
    n = int(math.ceil(horizon / dt))
    t = np.linspace(0.0, n * dt, n + 1)
    y = np.zeros((n + 1, 3), dtype=float)
    y[0] = (x10, 1.0, 0.0)
    for i in range(n):
        ti, yi = t[i], y[i]
        k1 = rhs(yi, ti, amplitude, ramp_duration, p, gate_open)
        k2 = rhs(yi + 0.5 * dt * k1, ti + 0.5 * dt, amplitude,
                 ramp_duration, p, gate_open)
        k3 = rhs(yi + 0.5 * dt * k2, ti + 0.5 * dt, amplitude,
                 ramp_duration, p, gate_open)
        k4 = rhs(yi + dt * k3, ti + dt, amplitude, ramp_duration, p, gate_open)
        y[i + 1] = yi + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        y[i + 1, :2] = np.clip(y[i + 1, :2], 0.0, 1.0)
        y[i + 1, 2] = np.clip(y[i + 1, 2], 0.0, p.alpha)
    return t, y


def stochastic_tau_leap(amplitude: float, ramp_duration: float, x10: float,
                        p: Params, N: int, horizon: float, dt: float,
                        rng: np.random.Generator, gate_open: bool = True):
    """Tau-leap approximation to a density-dependent demographic CTMC.

    For each patch, birth/death intensities are N*x*(turnover+positive/negative
    part of the deterministic per-capita drift). Their difference reproduces
    the ODE drift exactly. At zero counts, birth intensity is zero, so extinction
    is absorbing. q follows the measured patch-2 density between event batches.
    """
    n1 = max(1, int(round(x10 * N)))
    n2 = N
    q = 0.0
    steps = int(math.ceil(horizon / dt))
    crossed_allee = False
    true_extinction = False
    min_density = n1 / N
    peak_q = 0.0
    for j in range(steps):
        t = j * dt
        x1, x2 = n1 / N, n2 / N
        u = ramp(t, amplitude, ramp_duration)
        q_effective = q if gate_open else 0.0
        g1 = p.r1 * (x1 - p.allee) * (1.0 - x1) - p.predation * q_effective
        g2 = p.r2 * (1.0 - x2) - u
        b1, d1 = p.turnover + max(g1, 0.0), p.turnover + max(-g1, 0.0)
        b2, d2 = p.turnover + max(g2, 0.0), p.turnover + max(-g2, 0.0)
        birth1 = rng.binomial(n1, 1.0 - math.exp(-b1 * dt)) if n1 else 0
        death1 = rng.binomial(n1, 1.0 - math.exp(-d1 * dt)) if n1 else 0
        birth2 = rng.binomial(n2, 1.0 - math.exp(-b2 * dt)) if n2 else 0
        death2 = rng.binomial(n2, 1.0 - math.exp(-d2 * dt)) if n2 else 0
        n1 = max(0, n1 + birth1 - death1)
        n2 = max(0, n2 + birth2 - death2)
        x1, x2 = n1 / N, n2 / N
        if gate_open:
            target = p.alpha * max(0.0, 1.0 - x2)
            q += (target - q) * (1.0 - math.exp(-p.gamma * dt))
            q = min(max(q, 0.0), p.alpha)
        else:
            q = 0.0
        crossed_allee = crossed_allee or (x1 <= p.allee)
        min_density = min(min_density, x1)
        peak_q = max(peak_q, q)
        if n1 == 0:
            true_extinction = True
            break
    return {
        "crossed_allee": crossed_allee,
        "true_extinction": true_extinction,
        "final_density": n1 / N,
        "minimum_density": min_density,
        "peak_adaptive_diet": peak_q,
    }


def wilson(k: int, n: int, z: float = 1.96):
    phat = k / n
    den = 1.0 + z * z / n
    center = (phat + z * z / (2 * n)) / den
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / den
    return [max(0.0, center - half), min(1.0, center + half)]


def run(seed: int, reps: int, dt: float):
    p = Params()
    horizon = 160.0
    critical_q = p.r1 * (1.0 - p.allee) ** 2 / (4.0 * p.predation)
    critical_u = p.r2 * critical_q / p.alpha
    cases = [
        {"label": "R_fast_same_endpoint", "amplitude": 0.09, "ramp_duration": 0.1,
         "x10": 0.225, "gate_open": True},
        {"label": "R_slow_same_endpoint", "amplitude": 0.09, "ramp_duration": 100.0,
         "x10": 0.225, "gate_open": True},
        {"label": "B_slow_above_frozen_fold", "amplitude": 0.14, "ramp_duration": 100.0,
         "x10": 0.225, "gate_open": True},
        {"label": "N_demographic_only", "amplitude": 0.0, "ramp_duration": 0.0,
         "x10": 0.30, "gate_open": True},
        {"label": "R_fast_gate_closed_control", "amplitude": 0.09, "ramp_duration": 0.1,
         "x10": 0.225, "gate_open": False},
    ]
    rng = np.random.default_rng(seed)
    results = []
    for case in cases:
        _, traj = deterministic(case["amplitude"], case["ramp_duration"],
                                case["x10"], p, horizon, min(dt, 0.01),
                                case["gate_open"])
        det_cross = bool(np.any(traj[:, 0] <= p.allee))
        det_row = {
            "label": case["label"],
            "amplitude": case["amplitude"],
            "ramp_duration": case["ramp_duration"],
            "initial_x1": case["x10"],
            "gate_open": case["gate_open"],
            "deterministic_crossed_allee": det_cross,
            "deterministic_min_x1": float(traj[:, 0].min()),
            "deterministic_final_x1": float(traj[-1, 0]),
            "deterministic_peak_q": float(traj[:, 2].max()),
        }
        stochastic_rows = []
        for N in (80, 320, 1280):
            outcomes = [stochastic_tau_leap(
                case["amplitude"], case["ramp_duration"], case["x10"], p,
                N, horizon, dt, rng, case["gate_open"])
                for _ in range(reps)]
            k_allee = sum(int(o["crossed_allee"]) for o in outcomes)
            k_ext = sum(int(o["true_extinction"]) for o in outcomes)
            stochastic_rows.append({
                "N": N,
                "replicates": reps,
                "allee_crossings": k_allee,
                "allee_crossing_risk": k_allee / reps,
                "allee_crossing_wilson_95": wilson(k_allee, reps),
                "true_extinctions": k_ext,
                "extinction_risk": k_ext / reps,
                "extinction_wilson_95": wilson(k_ext, reps),
                "mean_min_density": float(np.mean([o["minimum_density"] for o in outcomes])),
                "mean_final_density": float(np.mean([o["final_density"] for o in outcomes])),
            })
        det_row["finite_population"] = stochastic_rows
        results.append(det_row)

    # Linearization at the healthy state (x1,x2,q)=(1,1,0), with d=1-x2.
    # All diagonal entries are negative and fixed, but off-diagonal transfer
    # creates a non-normal transient from d to q to focal-prey decline.
    a = p.r1 * (1.0 - p.allee)
    A = np.array([[-a, -p.predation, 0.0],
                  [0.0, -p.gamma, p.gamma * p.alpha],
                  [0.0, 0.0, -p.r2]])
    eig = np.linalg.eigvals(A)

    return {
        "status": "finite model diagnostic; not empirical evidence",
        "parameters": asdict(p),
        "seed": seed,
        "replicates_per_population_scale": reps,
        "time_step": dt,
        "horizon": horizon,
        "static_fold": {
            "critical_q": critical_q,
            "critical_u": critical_u,
            "condition": "u < r2 and c*alpha*u/r2 < r1*(1-allee)^2/4 for a positive focal-prey equilibrium",
        },
        "linearization": {
            "state_order": ["focal prey deviation", "adaptive diet shift", "alternate-prey deficit"],
            "matrix": A.tolist(),
            "eigenvalues": [[float(e.real), float(e.imag)] for e in eig],
            "all_eigenvalues_strictly_stable": bool(np.all(eig.real < 0)),
            "nonnormal": bool(not np.allclose(A.T @ A, A @ A.T)),
        },
        "cases": results,
        "limitations": [
            "The stochastic results use a tau-leap approximation to a density-dependent birth-death CTMC.",
            "No shared environmental shocks, dispersal, consumer abundance dynamics, or observation error are simulated.",
            "Population-scale conclusions require per-capita rates, spatial geometry, and external-driver distributions to remain comparable across N.",
            "The access gate is a model intervention; a field enclosure would need a sham gate and spillover measurement.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1509)
    ap.add_argument("--replicates", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.02)
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
