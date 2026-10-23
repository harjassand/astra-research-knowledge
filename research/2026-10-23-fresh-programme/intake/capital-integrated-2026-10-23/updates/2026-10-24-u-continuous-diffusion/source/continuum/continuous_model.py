"""One fixed, fully specified overdamped diffusion; no simulation result.

Circle length 3; mobility = temperature = diffusivity = 1.  The returned
potential is periodic.  `w` is its *tilted lift* offset, not a periodic
function: w(x+3)=w(x)-3*F.  All work must use `f` on the whole circle.
"""

from __future__ import annotations

import json
import math

import numpy as np

LENGTH = 3.0
FORCE = math.log(3.0 / 64.0) / 3.0
HEIGHT = 12.0
AMPLITUDE = 0.3
SLOW_FREQUENCY = 0.01
W_NODES = np.array(
    [0.0, 0.0, math.log(4.0 / 25.0), math.log(160.0),
     math.log(8.0 / 15.0), math.log(1600.0 / 3.0),
     math.log(64.0 / 3.0)]
)
F_NODES = np.array([1.0, 0.5, 0.0, 0.0, 0.0, 0.5, 1.0])
Q0 = np.array([[-3120., 480., 3.], [3000., -483., 10.],
               [120., 3., -13.]]) / 3000.0


def smoothstep(t):
    return t**3 * (10.0 + t * (-15.0 + 6.0 * t))


def smoothstep_prime(t):
    return 30.0 * t**2 * (1.0 - t)**2


def profiles(x):
    """Return V, V_x, periodic v, v_x, f, f_x for array-like x."""
    xp = np.mod(np.asarray(x, dtype=float), LENGTH)
    j = np.minimum(np.floor(2.0 * xp).astype(int), 5)
    t = 2.0 * xp - j
    dw = W_NODES[j + 1] - W_NODES[j]
    w = W_NODES[j] + dw * smoothstep(t)
    wx = 2.0 * dw * smoothstep_prime(t)
    r = np.clip(5.0 * t - 2.0, 0.0, 1.0)
    df = F_NODES[j + 1] - F_NODES[j]
    f = F_NODES[j] + df * smoothstep(r)
    fx = 10.0 * df * smoothstep_prime(r)
    V = 0.5 * (1.0 - np.cos(2.0 * math.pi * xp))
    Vx = math.pi * np.sin(2.0 * math.pi * xp)
    v = w + FORCE * xp
    vx = wx + FORCE
    return V, Vx, v, vx, f, fx


def potential(x, h, height=HEIGHT):
    V, Vx, v, vx, f, fx = profiles(x)
    return height * V + v - h * f, height * Vx + vx - h * fx


def kappa(height=HEIGHT):
    return math.pi * height * math.exp(-height)


def period(height=HEIGHT):
    return 2.0 * math.pi / (SLOW_FREQUENCY * kappa(height))


def waveform(t, height=HEIGHT):
    omega = SLOW_FREQUENCY * kappa(height)
    return (AMPLITUDE * np.cos(omega * t),
            -AMPLITUDE * omega * np.sin(omega * t))


def exact_node_rate_factors():
    """Arrhenius factors only: committed Kramers prefactor is separate."""
    vals = {}
    for i in range(3):
        # Forward lifted edge i -> i+1 and its reverse.
        wi = W_NODES[2 * i]
        ws = W_NODES[2 * i + 1]
        wj = W_NODES[2 * i + 2]
        vals[f"{i}->{(i+1)%3}"] = math.exp(wi - ws)
        vals[f"{(i+1)%3}->{i}"] = math.exp(wj - ws)
    return vals


def self_check():
    assert abs(W_NODES[-1] + 3.0 * FORCE) < 1e-14
    nodes = np.arange(6) / 2.0
    _, ux = potential(nodes, AMPLITUDE)
    assert np.max(np.abs(ux - FORCE)) < 1e-12
    assert np.allclose(profiles(nodes)[4], F_NODES[:-1])
    for i in range(3):
        for j in range(3):
            if i != j:
                assert abs(exact_node_rate_factors()[f"{j}->{i}"] - Q0[i, j]) < 1e-14
    slope_bound = ((40.0 / 9.0) * math.log(1000.0)
                   + (45.0 / 16.0) / math.sin(2.0 * math.pi / 5.0))
    assert HEIGHT * math.pi > slope_bound
    # Sampled controls supplement, rather than prove, the analytic bound.
    x = (np.arange(12000) + 0.5) / 4000.0
    drift0 = FORCE - potential(x, -AMPLITUDE)[1]
    drift1 = FORCE - potential(x, AMPLITUDE)[1]
    prescribed_sign = -np.sign(np.sin(2.0 * math.pi * x))
    assert np.all(drift0 * prescribed_sign > 0.0)
    assert np.all(drift1 * prescribed_sign > 0.0)
    return {
        "scope": "fixed model and algebra/sampling checks; no PDE result",
        "height": HEIGHT, "force": FORCE, "kappa": kappa(),
        "period": period(), "slope_bound": slope_bound,
        "height_pi": HEIGHT * math.pi,
        "arrhenius_factors": exact_node_rate_factors(),
        "control_total_variation": 4.0 * AMPLITUDE,
        "overdamped_constitutive_assumption": True,
        "finite_barrier_work_sign": "NOT_YET_TESTED",
    }


if __name__ == "__main__":
    print(json.dumps(self_check(), indent=2, sort_keys=True))
