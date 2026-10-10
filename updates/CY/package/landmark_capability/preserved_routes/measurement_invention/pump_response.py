#!/usr/bin/env python3
"""Reproduce a low-bandwidth stochastic-pump measurement example.

The hidden system is a three-state ring.  The only reported observable is the
net number of crossings of edge 0 -> 1 over one drive cycle.  The state path is
never used by the measurement protocol.  A fourth-order Runge-Kutta solver
integrates the master equation and the first two derivatives of the tilted
generator, giving the exact finite-state mean and variance up to integration
error.

No third-party packages are required.
"""

from __future__ import annotations

import json
import math
from typing import Callable, Sequence

TAU = 2.0 * math.pi
EDGES = ((0, 1), (1, 2), (2, 0))
MONITORED_EDGE = (0, 1)


def generator(theta: float, energy_amp: float, barrier_amp: float,
              energy_only: bool = False, barrier_only: bool = False):
    """Return Q0, Q1, Q2 using column probability vectors.

    E_i and B_ij are dimensionless energies (beta=1), with local-detailed-
    balance rates k_{i->j}=exp(E_i-B_ij), k_{j->i}=exp(E_j-B_ij).
    Q1/Q2 are derivatives at chi=0 of the tilted generator for the net count
    on the oriented edge 0->1; the escape-rate diagonal is not tilted.
    """
    energies = [0.0, energy_amp * math.cos(theta), 0.0]
    barriers = [0.0, 0.0, 0.0]
    if not energy_only:
        barriers[0] = barrier_amp * math.sin(theta)
    if barrier_only:
        energies = [0.0, 0.0, 0.0]

    q0 = [[0.0] * 3 for _ in range(3)]
    q1 = [[0.0] * 3 for _ in range(3)]
    q2 = [[0.0] * 3 for _ in range(3)]
    for k, (i, j) in enumerate(EDGES):
        forward = math.exp(energies[i] - barriers[k])
        reverse = math.exp(energies[j] - barriers[k])
        q0[j][i] += forward
        q0[i][i] -= forward
        q0[i][j] += reverse
        q0[j][j] -= reverse

        # Edge 0->1 has counting increment +1; reverse crossing is -1.
        if (i, j) == MONITORED_EDGE:
            q1[j][i] += forward
            q2[j][i] += forward
            q1[i][j] -= reverse
            q2[i][j] += reverse
    return q0, q1, q2


def matvec(a: Sequence[Sequence[float]], x: Sequence[float]) -> list[float]:
    return [sum(a[i][j] * x[j] for j in range(3)) for i in range(3)]


def rhs(t: float, y: Sequence[float], period: float, orientation: int,
        energy_amp: float, barrier_amp: float,
        energy_only: bool = False, barrier_only: bool = False) -> list[float]:
    theta = orientation * TAU * t / period
    q0, q1, q2 = generator(theta, energy_amp, barrier_amp,
                           energy_only=energy_only,
                           barrier_only=barrier_only)
    p = y[0:3]
    m1 = y[3:6]
    m2 = y[6:9]
    dp = matvec(q0, p)
    dm1 = [x + z for x, z in zip(matvec(q0, m1), matvec(q1, p))]
    dm2 = [x + 2.0 * z + w for x, z, w in
           zip(matvec(q0, m2), matvec(q1, m1), matvec(q2, p))]
    return dp + dm1 + dm2


def rk4_step(t: float, y: Sequence[float], dt: float, period: float,
             orientation: int, energy_amp: float, barrier_amp: float,
             energy_only: bool = False,
             barrier_only: bool = False) -> list[float]:
    def f(tt: float, yy: Sequence[float]) -> list[float]:
        return rhs(tt, yy, period, orientation, energy_amp, barrier_amp,
                   energy_only, barrier_only)

    k1 = f(t, y)
    y2 = [y[i] + 0.5 * dt * k1[i] for i in range(9)]
    k2 = f(t + 0.5 * dt, y2)
    y3 = [y[i] + 0.5 * dt * k2[i] for i in range(9)]
    k3 = f(t + 0.5 * dt, y3)
    y4 = [y[i] + dt * k3[i] for i in range(9)]
    k4 = f(t + dt, y4)
    return [y[i] + dt * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
            for i in range(9)]


def one_cycle(p: Sequence[float], period: float, orientation: int,
              energy_amp: float, barrier_amp: float, steps: int,
              energy_only: bool = False,
              barrier_only: bool = False) -> tuple[list[float], float, float]:
    y = list(p) + [0.0] * 6
    dt = period / steps
    for n in range(steps):
        y = rk4_step(n * dt, y, dt, period, orientation, energy_amp,
                     barrier_amp, energy_only, barrier_only)
    mean = sum(y[3:6])
    raw_second = sum(y[6:9])
    variance = raw_second - mean * mean
    return y[:3], mean, variance


def run_protocol(period: float, orientation: int, energy_amp: float = 0.7,
                 barrier_amp: float = 0.7, steps: int = 3000,
                 cycles_to_periodic: int = 30,
                 energy_only: bool = False,
                 barrier_only: bool = False) -> dict[str, float]:
    # Relax to the periodic stationary distribution at the protocol phase.
    p = [1.0, 0.0, 0.0]
    for _ in range(cycles_to_periodic):
        p, _, _ = one_cycle(p, period, orientation, energy_amp, barrier_amp,
                            steps, energy_only, barrier_only)
    p_end, mean, variance = one_cycle(
        p, period, orientation, energy_amp, barrier_amp, steps,
        energy_only, barrier_only)
    return {
        "mean_net_count_per_cycle": mean,
        "variance_net_count_per_cycle": variance,
        "periodic_state_residual_l1": sum(abs(a - b) for a, b in zip(p, p_end)),
    }


def run_continuous_block(period: float, orientation: int, energy_amp: float,
                         barrier_amp: float, steps: int, cycles: int,
                         cycles_to_periodic: int = 30) -> dict[str, float]:
    """Count current over consecutive cycles, retaining inter-cycle covariance."""
    p = [1.0, 0.0, 0.0]
    for _ in range(cycles_to_periodic):
        p, _, _ = one_cycle(p, period, orientation, energy_amp, barrier_amp,
                            steps)
    y = p + [0.0] * 6
    dt = period / steps
    for n in range(cycles * steps):
        y = rk4_step(n * dt, y, dt, period, orientation,
                     energy_amp, barrier_amp)
    total_mean = sum(y[3:6])
    total_variance = sum(y[6:9]) - total_mean * total_mean
    return {
        "cycles": float(cycles),
        "mean_net_count_per_cycle": total_mean / cycles,
        "variance_rate_per_cycle": total_variance / cycles,
    }


def max_departure_rate(energy_amp: float, barrier_amp: float,
                       points: int = 20001) -> float:
    maximum = 0.0
    for n in range(points):
        theta = TAU * n / (points - 1)
        q0, _, _ = generator(theta, energy_amp, barrier_amp)
        for i in range(3):
            maximum = max(maximum, -q0[i][i])
    return maximum


def result() -> dict:
    energy_amp = 0.7
    barrier_amp = 0.7
    period = 15.0
    fwd = run_protocol(period, +1, energy_amp, barrier_amp)
    rev = run_protocol(period, -1, energy_amp, barrier_amp)
    fwd_block = run_continuous_block(period, +1, energy_amp, barrier_amp,
                                     steps=3000, cycles=25)
    rev_block = run_continuous_block(period, -1, energy_amp, barrier_amp,
                                     steps=3000, cycles=25)
    e_null = run_protocol(period, +1, energy_amp, barrier_amp,
                          energy_only=True)
    b_null = run_protocol(period, +1, energy_amp, barrier_amp,
                          barrier_only=True)

    delta = fwd["mean_net_count_per_cycle"] - rev["mean_net_count_per_cycle"]
    block_delta = (fwd_block["mean_net_count_per_cycle"] -
                   rev_block["mean_net_count_per_cycle"])
    per_arm_cycles_5sigma = 25.0 * (
        fwd_block["variance_rate_per_cycle"] +
        rev_block["variance_rate_per_cycle"]
    ) / (block_delta * block_delta)
    max_rate = max_departure_rate(energy_amp, barrier_amp)
    return {
        "model": {
            "states": 3,
            "topology": "ring 0->1->2->0 with reverse edges",
            "rate_law": "k(i->j)=exp(E_i-B_ij), beta=1, attempt rate=1",
            "control": "E1=0.7 cos(theta), B01=0.7 sin(theta), theta=orientation*2*pi*t/T",
            "readout": "net count on edge 0->1 integrated over one full cycle",
            "period": period,
            "cycle_frequency": 1.0 / period,
            "max_departure_rate": max_rate,
        },
        "forward": fwd,
        "reverse": rev,
        "continuous_block_25_cycles": {
            "forward": fwd_block,
            "reverse": rev_block,
            "variance_estimator": "Var(total net count over 25 consecutive cycles)/25; includes finite inter-cycle covariance",
        },
        "single_knob_nulls": {
            "vary_energy_only": e_null,
            "vary_barrier_only": b_null,
        },
        "orientation_odd_signal_counts_per_cycle": delta,
        "orientation_even_leakage_counts_per_cycle": (
            fwd["mean_net_count_per_cycle"] +
            rev["mean_net_count_per_cycle"]
        ) / 2.0,
        "approx_cycles_per_orientation_for_5sigma": per_arm_cycles_5sigma,
        "approx_total_cycles_for_5sigma": 2.0 * per_arm_cycles_5sigma,
        "integration": {
            "method": "RK4 on tilted-generator moment equations",
            "steps_per_cycle": 3000,
            "cycles_to_periodic_state": 30,
            "external_dependencies": [],
        },
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
