"""Conventional two-drift colored-sensor cancellation at a finite lag.
Known calibrated propagators are supplied; no physical actuator is demonstrated.
"""
from pathlib import Path
import json
import numpy as np
from thermal_bridge import lyap, expm, adj

ROOT = Path(__file__).resolve().parent


def main():
    eye = np.eye(2)
    g0 = np.array([[-.5, -.3j], [-.3j, -.8]], complex)
    delta = .7
    g1 = g0 - delta * eye
    # Physical diffusion changes substantially and is not given to the decoder.
    c0 = lyap(g0, np.array([[.1, .01j], [-.01j, .03]]))
    c1 = lyap(g1, np.array([[.4, .02], [.02, .07]]))
    sensor_g = np.diag([-.11 + .2j, -.07 - .1j])
    sensor_c = lyap(sensor_g, .1 * eye)
    d0 = (c0 + sensor_c) - (c1 + sensor_c)
    rows = []
    for lag in [.001, .1, 1., 10.]:
        e0, e1 = expm(g0 * lag), expm(g1 * lag)
        sensor_lag = expm(sensor_g * lag) @ sensor_c
        dt = (e0 @ c0 + sensor_lag) - (e1 @ c1 + sensor_lag)
        estimate = np.linalg.solve(e0 - e1, dt - e0 @ d0)
        assert np.linalg.norm(estimate - c1) < 1e-10
        rows.append({
            "lag": lag,
            "covariance_C1_error_F": float(np.linalg.norm(estimate - c1)),
            "inverse_absolute_gain": float(np.linalg.norm(np.linalg.inv(e0 - e1), 2)),
            "relative_condition_number": float(np.linalg.cond(e0 - e1)),
            "exact_E_error_bound_coefficients": {
                "lag_difference_error": float(np.linalg.norm(np.linalg.inv(e0), 2)
                                               / abs(1 - np.exp(-delta * lag))),
                "zero_lag_difference_error": float(1 / abs(1 - np.exp(-delta * lag)))
            }
        })
    out = {"status": "Synthetic population identity; ordinary calibrated two-regime control comparator",
           "sensor_scope": "Independent common sensor covariance kernel at every used lag; fixed instantaneous physical readout gauge. Sensor changes or unknown exposure violate this calculation.",
           "diffusion_scope": "No common physical diffusion assumption: the two positive diffusion matrices differ.",
           "clock_scope": "Known propagators suffice for covariance. Physical diffusion/current rates still require known continuous generators.",
           "rows": rows}
    (ROOT / "finite_lag_results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
