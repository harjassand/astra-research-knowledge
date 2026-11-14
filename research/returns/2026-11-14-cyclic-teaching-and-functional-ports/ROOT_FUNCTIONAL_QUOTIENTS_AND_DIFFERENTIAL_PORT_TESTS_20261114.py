"""Introduced exact port-network diagnostics; no producer artifacts or experiments."""
from fractions import Fraction as Q
import json
import math


def n(x):
    return {"exact": str(x), "float": float(x)}


def inv(a):
    size = len(a)
    m = [list(row) + [Q(i == j) for j in range(size)] for i, row in enumerate(a)]
    for i in range(size):
        pivot = next(j for j in range(i, size) if m[j][i])
        m[i], m[pivot] = m[pivot], m[i]
        d = m[i][i]
        m[i] = [x / d for x in m[i]]
        for j in range(size):
            if j != i:
                factor = m[j][i]
                m[j] = [m[j][k] - factor * m[i][k] for k in range(2 * size)]
    return [row[size:] for row in m]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def quadratic(a, x):
    return sum(x[i] * a[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))


def circuit_cases():
    z0 = [[Q(3), Q(2), Q(1)], [Q(2), Q(3), Q(1)], [Q(1), Q(1), Q(2)]]
    c, v = [Q(1), Q(0), -Q(1)], [Q(2), Q(1), -Q(1)]
    alpha, vv = Q(3), Q(6)
    y0 = inv(z0)
    rows = []
    for rho in (Q(1, 1000), Q(1, 10), Q(1), Q(3), Q(10), Q(100), Q(1000)):
        z = [[z0[i][j] - v[i] * v[j] / (rho + alpha) for j in range(3)] for i in range(3)]
        direct = inv([[y0[i][j] + c[i] * c[j] / rho for j in range(3)] for i in range(3)])
        assert z == direct
        z_merged = [[z0[i][j] - v[i] * v[j] / alpha for j in range(3)] for i in range(3)]
        assert quadratic(z_merged, c) == 0
        assert quadratic(z, c) == alpha * rho / (rho + alpha)
        rows.append({"rho": n(rho),
                     "weak_chord_omission_relative_to_actual_energy": n(alpha / rho),
                     "weak_chord_omission_absolute_operator_error": n(vv / (rho + alpha)),
                     "strong_chord_contraction_absolute_operator_error": n(vv * rho / (alpha * (rho + alpha))),
                     "strong_chord_contraction_relative_error_on_c": n(Q(1)),
                     "actual_energy_for_c": n(quadratic(z, c)),
                     "parameter_sensitivity_operator_norm": n(vv / ((rho + alpha) ** 2)),
                     "exact_formula_vs_direct_inverse_error": n(Q(0))})
    # A sequence of weak links is not automatically negligible collectively.
    budgets = [{"individually_declared_g_times_effective_resistance": n(Q(1, 1000)),
                "links": k, "sum_budget": n(Q(k, 1000))}
               for k in (1, 10, 100, 1000)]
    return {"scope": "INTRODUCED known unit-resistance backbone; no hidden-network acquisition",
            "Z0": [[n(x) for x in row] for row in z0], "cases": rows,
            "many_weak_link_budget": budgets}


def hydraulic_midpoints(pa, pb, main_r, leak_g):
    half_g = Q(2) / main_r
    a = [[2 * half_g + leak_g, -leak_g], [-leak_g, 2 * half_g + leak_g]]
    xy = matmul(inv(a), [[half_g * pa], [half_g * pb]])
    x, y = xy[0][0], xy[1][0]
    ain, aout = half_g * (pa - x), half_g * x
    bin_, bout = half_g * (pb - y), half_g * y
    cross = leak_g * (x - y)
    assert ain + bin_ == aout + bout
    assert ain - aout == cross
    assert bout - bin_ == cross
    return {"x": x, "y": y, "Ain": ain, "Aout": aout,
            "Bin": bin_, "Bout": bout, "cross": cross}


def hydraulic_cases():
    rows = []
    for g in (Q(0), Q(1, 100), Q(4, 197), Q(1, 10), Q(1), Q(10)):
        common = hydraulic_midpoints(Q(1), Q(1), Q(1), g)
        differential = hydraulic_midpoints(Q(1), Q(0), Q(1), g)
        frac = differential["cross"] / differential["Ain"]
        assert common["cross"] == 0 and common["Ain"] == common["Bin"] == 1
        assert frac == 2 * g / (4 + 3 * g)
        rows.append({"dimensionless_leak_g_times_main_R": n(g),
                     "common_mode_cross": n(common["cross"]),
                     "common_mode_Ain_and_Aout": n(common["Ain"]),
                     "differential_cross_fraction_of_Ain": n(frac),
                     "differential_flows": {k: n(v) for k, v in differential.items()}})
    eta = Q(1, 100)
    max_g_r = 4 * eta / (2 - 3 * eta)
    min_r_ratio = 1 / max_g_r
    measured_flow = Q(5)  # Introduced mL/min.
    max_channel_error = eta * measured_flow / (2 + eta)
    assert max_g_r == Q(4, 197) and min_r_ratio == Q(197, 4)
    mu, length, diameter = 0.001, 0.020, 0.0003
    resistance = 128 * mu * length / (math.pi * diameter ** 4)
    flow = 5e-6 / 60
    velocity = 4 * flow / (math.pi * diameter ** 2)
    return {"scope": "INTRODUCED linear incompressible network, all four boundary pressures controlled",
            "cases": rows, "accepted_cross_fraction": n(eta),
            "required_max_g_times_R": n(max_g_r),
            "required_min_leak_R_over_main_R": n(min_r_ratio),
            "per_channel_absolute_error_limit_mL_min_for_zero_observed_loss": n(max_channel_error),
            "straight_tube_illustration_only": {
                "mu_Pa_s": mu, "length_m": length, "clear_diameter_m": diameter,
                "ideal_Poiseuille_R_Pa_s_m3": resistance,
                "ideal_deltaP_at_5mL_min_Pa": resistance * flow,
                "introduced_density_kg_m3": 1000,
                "Reynolds_number": 1000 * velocity * diameter / mu,
                "required_leak_resistance_Pa_s_m3": float(min_r_ratio) * resistance,
                "limits": "Fully developed straight-tube model; no entrance, joint, wall, roughness, installed metrology or durability qualification."}}


print(json.dumps({"status": "EXACT_INTRODUCED_MODEL_DIAGNOSTICS_NOT_QUALIFIED_HARDWARE",
                  "resistive_quotient": circuit_cases(), "hydraulic_qualification": hydraulic_cases(),
                  "limits": ["Known model coefficients are supplied; their acquisition is not free.",
                             "Energy-error, absolute-output-error and parameter-error contracts differ.",
                             "Classical network identities are used; no new physical law or general teacher is claimed.",
                             "No original producer code, data, archive, source or component was recovered or executed."]}, indent=2))
