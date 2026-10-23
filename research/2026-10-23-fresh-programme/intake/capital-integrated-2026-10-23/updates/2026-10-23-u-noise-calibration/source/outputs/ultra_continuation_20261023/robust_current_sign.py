"""Attainable current intervals under an unresolved pump/sensor split.
Synthetic population calculations; no measured covariance or confidence claim.
"""
from pathlib import Path
import json
import numpy as np
from thermal_bridge import lyap, adj

ROOT = Path(__file__).resolve().parent


def main():
    eye = np.eye(2)
    g = -.5 * eye - 1j * np.array([[0., .3], [.3, 0.]])
    q = [np.diag([1., 0.]), np.diag([0., 1.])]
    occupations = [.1, .02]
    thermal_d = sum(n * a for n, a in zip(occupations, q))
    thermal_c = lyap(g, thermal_d)
    thermal_j = np.array([np.trace(a @ (n * eye - thermal_c)).real
                          for n, a in zip(occupations, q)])
    rows = []
    for excess_covariance in [0., .005, .02, .1]:
        total_c = thermal_c + excess_covariance * eye
        excess_d = -(g @ total_c + total_c @ adj(g)) - thermal_d
        assert np.linalg.eigvalsh(excess_d).min() > -1e-13
        endpoints = []
        for a, n, j0 in zip(q, occupations, thermal_j):
            # L_G^*(a) solves G* R + R G = -a.
            response = lyap(adj(g), a)
            assert np.linalg.eigvalsh(response).min() > 0
            lower = float(j0 - np.trace(response @ excess_d).real)
            upper = float(j0)
            direct_lower = float(np.trace(a @ (n * eye - total_c)).real)
            assert abs(lower - direct_lower) < 1e-13
            endpoints.append({"lower": lower, "upper": upper,
                              "sign": "positive" if lower > 1e-12 else
                              "negative" if upper < -1e-12 else "unresolved"})
        # Every split is a valid independent OU sensor + physical pump model.
        for fraction in np.linspace(0, 1, 21):
            physical_c = thermal_c + lyap(g, fraction * excess_d)
            sensor_c = lyap(g, (1 - fraction) * excess_d)
            assert np.linalg.norm(physical_c + sensor_c - total_c) < 1e-12
            for a, n, interval in zip(q, occupations, endpoints):
                current = np.trace(a @ (n * eye - physical_c)).real
                assert interval["lower"] - 1e-12 <= current <= interval["upper"] + 1e-12
        rows.append({"excess_covariance": excess_covariance,
                     "bath_number_current_intervals": endpoints})

    # A stable active (squeezed) quadrature drift need not obey the passive
    # common-occupation response Delta C = Delta n I.
    squeezing = .5
    active_g = np.diag([-1 + squeezing, -1 - squeezing])
    active_delta = lyap(active_g, 2 * np.eye(2))
    assert np.allclose(active_delta, np.diag([2., 2 / 3]))
    assert not np.allclose(active_delta, np.eye(2))
    out = {
        "status": "Exact model-conditional interval and population synthetic checks; no empirical data",
        "thermal_number_currents": thermal_j.tolist(),
        "rows": rows,
        "attainability": "P+R=E, P,R PSD, with independent proper Gaussian pump and same-G sensor. All splits have identical full unmodulated observed laws and common additive coherent/thermal responses.",
        "general_covariance_order_bound": "For arbitrary independent stationary additive sensor noise, Cthermal <= Cphysical <= Cobserved gives the same number-current bounds, but endpoints need not be attainable outside the same-G class.",
        "finite_error_rule": "If a separate valid event certifies ||Chat-Cobserved||_F <= epsilon with all calibration exact, replace lower by n tr(Q)-tr(Q Chat)-||Q||_F epsilon. No such finite-trace event is established here.",
        "scope": "Fixed known G, Qi and occupations in physical coordinates. Positive number-current weights. Heat needs a calibrated energy observable; noncommuting energy/coupling requires the general signed-eigenvalue interval, not this monotone formula. Correlated additive sensor noise invalidates covariance order.",
        "active_common_shift_counterexample": {
            "G": active_g.tolist(), "thermal_diffusion_shift": (2 * eye).tolist(),
            "covariance_shift": active_delta.tolist(),
            "implication": "The passive thermal metric calibration cannot be carried unchanged to active/squeezed dynamics."
        }
    }
    (ROOT / "robust_current_results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
