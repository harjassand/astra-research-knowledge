"""Exact 6-state reversible kinetic-allostery pulse model.

States are (conformation i in {0,1,2}, distal ligand occupancy y in {0,1}).
The local intervention multiplies both directions of the 1<->2 conformational
edge by exp(theta), i.e. changes a barrier/attempt frequency without changing
the state energies. Propagation uses uniformization, requiring only NumPy.
"""

from __future__ import annotations

import json
import math
import numpy as np


AFFINITY = np.array([0.0, 0.0, math.log(30.0)])
ENERGY = np.array([0.0, 0.0, 2.0])
GAMMA = np.array([1.0, 0.08])
K_ON = 0.30


def state(i: int, y: int) -> int:
    return 2 * i + y


def generator(c: float, theta: float) -> np.ndarray:
    """Row generator. c is ligand concentration relative to a reference."""
    q = np.zeros((6, 6), dtype=float)
    for i in range(3):
        q[state(i, 0), state(i, 1)] = K_ON * c
        q[state(i, 1), state(i, 0)] = K_ON * math.exp(-AFFINITY[i])
    for i in range(2):
        gamma = GAMMA[i] * (math.exp(theta) if i == 1 else 1.0)
        da = AFFINITY[i + 1] - AFFINITY[i]
        de = ENERGY[i + 1] - ENERGY[i]
        for y in range(2):
            q[state(i, y), state(i + 1, y)] = gamma * math.exp(-0.5 * de + 0.5 * y * da)
            q[state(i + 1, y), state(i, y)] = gamma * math.exp(0.5 * de - 0.5 * y * da)
    np.fill_diagonal(q, -q.sum(axis=1))
    return q


def equilibrium(c: float) -> np.ndarray:
    weights = np.array([
        math.exp(-ENERGY[i] + y * (AFFINITY[i] + math.log(c)))
        for i in range(3) for y in range(2)
    ])
    return weights / weights.sum()


def propagate(mu: np.ndarray, q: np.ndarray, t: float) -> np.ndarray:
    """Uniformization of mu exp(Qt), with a conservative Poisson-tail cutoff."""
    nu = float(np.max(-np.diag(q)))
    if t == 0 or nu == 0:
        return mu.copy()
    p = np.eye(len(mu)) + q / nu
    # Split long intervals so exp(-z) remains representable and the Poisson
    # truncation stays numerically stable.
    pieces = max(1, math.ceil(nu * t / 300.0))
    dt = t / pieces
    z = nu * dt
    kmax = math.ceil(z + 14.0 * math.sqrt(z + 1.0) + 50.0)
    result = mu.copy()
    for _ in range(pieces):
        weight = math.exp(-z)
        term = result.copy()
        segment = weight * term
        for k in range(1, kmax + 1):
            term = term @ p
            weight *= z / k
            segment += weight * term
        result = segment / segment.sum()
    return result


def future_value(q: np.ndarray, f: np.ndarray, t: float) -> np.ndarray:
    """Return exp(Qt) f using the same uniformization scheme."""
    nu = float(np.max(-np.diag(q)))
    if t == 0 or nu == 0:
        return f.copy()
    p = np.eye(len(f)) + q / nu
    pieces = max(1, math.ceil(nu * t / 300.0))
    dt = t / pieces
    z = nu * dt
    kmax = math.ceil(z + 14.0 * math.sqrt(z + 1.0) + 50.0)
    result = f.copy()
    for _ in range(pieces):
        weight = math.exp(-z)
        term = result.copy()
        segment = weight * term
        for k in range(1, kmax + 1):
            term = p @ term
            weight *= z / k
            segment += weight * term
        result = segment
    return result


def theta_derivative(c: float, theta: float) -> np.ndarray:
    """Analytic derivative Q_theta for the locally scaled 1<->2 edge."""
    q = generator(c, theta)
    dq = np.zeros_like(q)
    for y in range(2):
        x, z = state(1, y), state(2, y)
        dq[x, z] = q[x, z]
        dq[z, x] = q[z, x]
    np.fill_diagonal(dq, -dq.sum(axis=1))
    return dq


def duhamel_response(mu: np.ndarray, q: np.ndarray, dq: np.ndarray,
                     f: np.ndarray, t: float, n_quad: int = 64) -> float:
    """Numerically integrate mu exp(sQ) Q' exp((T-s)Q) f."""
    nodes, weights = np.polynomial.legendre.leggauss(n_quad)
    total = 0.0
    for node, weight in zip(nodes, weights):
        s = 0.5 * t * (node + 1.0)
        rho = propagate(mu, q, s)
        u = future_value(q, f, t - s)
        total += weight * float(rho @ dq @ u)
    return 0.5 * t * total


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def main() -> None:
    f_active = np.array([1.0 if i == 2 else 0.0 for i in range(3) for _ in range(2)])
    f_bound = np.array([float(y) for _ in range(3) for y in range(2)])
    rows = []
    c_pre = 0.03
    mu = equilibrium(c_pre)
    for c in (0.3, 3.0):
        q0 = generator(c, 0.0)
        pi = equilibrium(c)
        assert np.max(np.abs(pi @ q0)) < 2e-14
        assert np.max(np.abs(propagate(pi, q0, 50.0) - pi)) < 2e-12
        for multiplier in (3.0, 10.0):
            theta = math.log(multiplier)
            q1 = generator(c, theta)
            assert np.max(np.abs(pi @ q1)) < 2e-14
            assert np.max(np.abs(propagate(pi, q1, 50.0) - pi)) < 2e-12
            for t in (1.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 30.0, 100.0):
                p0, p1 = propagate(mu, q0, t), propagate(mu, q1, t)
                a0, a1 = float(p0 @ f_active), float(p1 @ f_active)
                b0, b1 = float(p0 @ f_bound), float(p1 @ f_bound)
                rows.append({
                    "c_pre": c_pre, "c_post": c, "T": t,
                    "barrier_rate_multiplier": multiplier,
                    "active_p_theta0": a0, "active_p_perturbed": a1,
                    "active_log_odds_effect": logit(a1) - logit(a0),
                    "bound_p_theta0": b0, "bound_p_perturbed": b1,
                    "bound_log_odds_effect": logit(b1) - logit(b0),
                })
    result = {
        "model": {
            "states": "(i,y), i=0,1,2; y=0,1",
            "energies_over_kBT": "U(i,y)=epsilon_i-y*(a_i+ln(c))",
            "affinity_a": AFFINITY.tolist(),
            "conformation_energy_epsilon": ENERGY.tolist(),
            "base_conformational_attempt_rates": GAMMA.tolist(),
            "binding_on_rate": "0.30*c",
            "binding_off_rates": [K_ON * math.exp(-x) for x in AFFINITY],
            "intervention": "multiply both directions of i=1<->2 rates by exp(theta)",
            "barrier_rate_multipliers": [3.0, 10.0],
            "initial_ensemble": f"equilibrium at c_pre={c_pre}; at t=0 step concentration to c_post",
            "propagator": "uniformization; max residual checks in asserts",
        },
        "stationary_outputs_theta_invariant": {
            str(c): {
                "active_fraction": float(equilibrium(c) @ f_active),
                "bound_fraction": float(equilibrium(c) @ f_bound),
            } for c in (0.03, 0.3, 3.0)
        },
        "results": rows,
    }
    # Verify the local edge/committor derivative against a centered finite
    # difference for two independent remote readouts in one pulse condition.
    c_check, theta_check, t_check, h = 3.0, math.log(3.0), 10.0, 1e-5
    q_check = generator(c_check, theta_check)
    dq_check = theta_derivative(c_check, theta_check)
    derivative_checks = []
    for name, f in (("active", f_active), ("bound", f_bound)):
        path_integral = duhamel_response(mu, q_check, dq_check, f, t_check)
        p_plus = float(propagate(mu, generator(c_check, theta_check + h), t_check) @ f)
        p_minus = float(propagate(mu, generator(c_check, theta_check - h), t_check) @ f)
        centered_difference = (p_plus - p_minus) / (2.0 * h)
        error = abs(path_integral - centered_difference)
        assert error < 2e-9
        derivative_checks.append({
            "readout": name,
            "duhamel_local_edge_derivative": path_integral,
            "centered_finite_difference": centered_difference,
            "absolute_error": error,
        })
    result["duhamel_derivative_checks"] = derivative_checks
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
