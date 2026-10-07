#!/usr/bin/env python3
"""
Finite diagnostic for the suppressed-subclone information-starvation checkpoint.

This is a scaling sanity check, not biological validation.
It verifies:
  (i) fixed-noise bulk observation Fisher information ~ eps^2,
 (ii) background-free resistant-clone Poisson counts ~ eps,
(iii) ideal relative/log observation ~ eps^0,
 (iv) additive assay background produces a low-signal eps^2 -> high-signal eps crossover.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

def simulate(eps, theta=0.012, T=120.0, npts=500):
    K = 1.0
    rS = 0.025
    rR = theta
    d = 0.004
    drug_effect = 0.85
    D = 1.0
    n0 = 0.5
    R0 = n0 * eps
    S0 = n0 - R0
    t = np.linspace(0.0, T, npts)

    def rhs(_, y):
        S, R = y
        total = S + R
        return [
            rS * S * (1.0 - total / K) * (1.0 - drug_effect * D) - d * S,
            rR * R * (1.0 - total / K) - d * R,
        ]

    sol = solve_ivp(
        rhs, [0.0, T], [S0, R0], t_eval=t, rtol=1e-11, atol=1e-13
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return t, sol.y[0], sol.y[1]

def sensitivities(eps, theta=0.012, h=1e-6):
    t, Sp, Rp = simulate(eps, theta + h)
    _, Sm, Rm = simulate(eps, theta - h)
    _, S, R = simulate(eps, theta)
    dS = (Sp - Sm) / (2.0 * h)
    dR = (Rp - Rm) / (2.0 * h)
    return t, S, R, dS, dR

def fit_slope(xs, ys, k):
    return float(np.polyfit(np.log(xs[:k]), np.log(np.asarray(ys)[:k]), 1)[0])

eps_grid = np.logspace(-5, -1, 13)
bulk_fi, count_fi, log_fi = [], [], []

for eps in eps_grid:
    t, S, R, dS, dR = sensitivities(eps)
    dtotal = dS + dR
    bulk_fi.append(float(np.trapezoid(dtotal**2, t)))
    count_fi.append(float(np.trapezoid(dR**2 / np.maximum(R, 1e-300), t)))
    log_fi.append(float(np.trapezoid((dR / np.maximum(R, 1e-300))**2, t)))

ode_slopes = {
    "bulk_fixed_noise": fit_slope(eps_grid, bulk_fi, 7),
    "direct_poisson_count": fit_slope(eps_grid, count_fi, 7),
    "ideal_log_relative": fit_slope(eps_grid, log_fi, 7),
}

theta = 0.01
T = 100.0
t = np.linspace(0.0, T, 10001)
eps_bg = np.logspace(-8, -1, 50)

def background_fi(eps, background):
    f = eps * np.exp(theta * t)
    df_dtheta = t * f
    return float(np.trapezoid(df_dtheta**2 / (background + f), t))

background_slopes = {}
for background in [0.0, 1e-4]:
    vals = np.array([background_fi(e, background) for e in eps_bg])
    background_slopes[str(background)] = {
        "low_eps": float(np.polyfit(np.log(eps_bg[:10]), np.log(vals[:10]), 1)[0]),
        "high_eps": float(np.polyfit(np.log(eps_bg[-10:]), np.log(vals[-10:]), 1)[0]),
    }

result = {
    "status": "finite_diagnostic_not_proof",
    "ode_eps_grid": eps_grid.tolist(),
    "ode_slopes": ode_slopes,
    "background_slopes": background_slopes,
    "expected_exponents": {
        "bulk_fixed_noise": 2.0,
        "direct_poisson_count": 1.0,
        "ideal_log_relative": 0.0,
        "background_low_signal": 2.0,
        "background_high_signal": 1.0,
    },
}

assert abs(ode_slopes["bulk_fixed_noise"] - 2.0) < 0.01
assert abs(ode_slopes["direct_poisson_count"] - 1.0) < 0.01
assert abs(ode_slopes["ideal_log_relative"]) < 0.01
assert abs(background_slopes["0.0"]["low_eps"] - 1.0) < 0.01
assert abs(background_slopes["0.0001"]["low_eps"] - 2.0) < 0.01
assert abs(background_slopes["0.0001"]["high_eps"] - 1.0) < 0.02

print(json.dumps(result, indent=2, sort_keys=True))
