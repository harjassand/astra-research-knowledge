"""Acquire rational all-time moments and recovery firing-cost bounds.

No simulation is run. These numbers implement the analytic bounds in
moment_cost_derivation.txt. Numerical bounds are deliberately conservative.
"""
from fractions import Fraction as F
from math import comb, isqrt
import json
import pathlib
from robust_three_layer_certificate import acquire, potential, serialized, ceil_rat


def shifted_poisson_moment(n, mean, p):
    # Stirling numbers of the second kind; E[Poisson(mean)^k]=Touchard_k(mean).
    row = [1]
    moments = [F(1)]
    for k in range(1, p + 1):
        row = [0] + [((row[j - 1] if j - 1 < len(row) else 0)
                      + (j * row[j] if j < len(row) else 0))
                     for j in range(1, k + 1)]
        moments.append(sum(F(v) * mean**j for j, v in enumerate(row)))
    return sum(F(comb(p, k)) * n**(p - k) * moments[k] for k in range(p + 1))


def birth_interval_bound(rate_moment, p):
    if p < 2:
        raise ValueError("Use integer p>=2")
    a = (2**(p - 2)) * (p - 1)
    b = (2**(p - 2)) * (p + 1)
    d = p * (2**(p - 2))
    return F(2**(2 * a), a) * (b * rate_moment + d)


def survivor_moment(n, births_p, gate_upper, kill_decay, p):
    return gate_upper * (2**(p - 1)) * (
        n**p + births_p * (1 + F(p) / kill_decay)**p)


def ceil_sqrt(value):
    if value < 0:
        raise ValueError("Nonnegative rational required")
    result = isqrt(value.numerator // value.denominator)
    return result if result * result * value.denominator >= value.numerator else result + 1


def acquire_moments(cert, state, p):
    if len(state) != len(cert["names"]) or any(not isinstance(n, int) or n < 0 for n in state):
        raise ValueError("Nonnegative integer count vector required")
    x = dict(zip(cert["names"], state))
    bounds, birth_bounds, tag_rates = {}, {}, {}
    for i, (birth, death) in cert["root_rates"].items():
        mean = birth[1] / death[0]
        bounds[i] = shifted_poisson_moment(x[i], mean, p)
    for j, parents in cert["mid_edges"].items():
        alpha_sum = sum(z[0][1] for z in parents.values())
        rate_p = alpha_sum**(p - 1) * sum(
            z[0][1] * bounds[i] for i, z in parents.items())
        births_p = birth_interval_bound(rate_p, p)
        gate = 1 + cert["mid_data"][j]["c"]
        decay = cert["mid_data"][j]["gamma"] / gate
        bounds[j] = survivor_moment(x[j], births_p, gate, decay, p)
        birth_bounds[j] = births_p
        tag_rates[j] = decay
    for k, z in cert["leaf_data"].items():
        rate_p = z["alpha"][1]**p * bounds[z["parent"]]
        births_p = birth_interval_bound(rate_p, p)
        gate = 1 + z["c"] / z["s"]
        decay = z["gamma"] / gate
        bounds[k] = survivor_moment(x[k], births_p, gate, decay, p)
        birth_bounds[k] = births_p
        tag_rates[k] = decay
    return {"p": p, "uniform_species_moments": bounds,
            "unit_birth_count_moments": birth_bounds,
            "uniform_tagged_lifetime_decay": tag_rates}


def acquire_return_cost(cert, state):
    m4 = acquire_moments(cert, state, 4)
    d = len(cert["names"])
    n4 = d**3 * sum(m4["uniform_species_moments"].values())
    b = sum(z[0][1] for z in cert["root_rates"].values())
    linear = (sum(z[1][1] for z in cert["root_rates"].values())
              + sum(z[0][1] for parents in cert["mid_edges"].values()
                    for z in parents.values())
              + sum(z["alpha"][1] for z in cert["leaf_data"].values()))
    quadratic = (sum(z[1][1] for parents in cert["mid_edges"].values()
                     for z in parents.values())
                 + sum(z["beta"][1] for z in cert["leaf_data"].values()))
    q2 = 3 * (b**2 + (linear**2 + quadratic**2) * n4)
    w0 = 1 + potential(cert, state)
    radius = max(1, ceil_rat((2 * (cert["C"] + cert["lambda"])
                             / cert["lambda"] - 1) / cert["min_weight"]))
    ceiling = ceil_sqrt(q2 * w0)
    cost = 4 * ceiling / cert["lambda"]
    if sum(state) < radius:
        cost = F(0)  # First entry is immediate from an already admitted state.
    return {"fourth_moment_certificate": m4,
            "uniform_total_count_fourth_moment": n4,
            "uniform_total_intensity_second_moment": q2,
            "W_initial": w0, "exponential_return_core_radius": radius,
            "return_exponent": cert["lambda"] / 2,
            "expected_reaction_firings_before_first_core_entry_upper": cost}


if __name__ == "__main__":
    path = pathlib.Path(__file__)
    checks = json.loads(path.with_name("robust_three_layer_checks.json").read_text())
    cert = acquire(checks["certificates"][1]["spec"])
    # Independent exact known Poisson moment identity, not simulation.
    assert shifted_poisson_moment(0, F(1), 4) == 15
    assert shifted_poisson_moment(0, F(2), 4) == 94
    assert ceil_sqrt(F(81, 16)) == 3
    assert ceil_sqrt(F(9, 1)) == 3
    state = [0, 0, 6000]
    report = acquire_return_cost(cert, state)
    report["initial_state"] = state
    report["status"] = "EXPLICIT_ANALYTIC_BOUND_ACQUIRED_NOT_SIMULATED"
    destination = path.with_name("moment_cost_certificate.json")
    destination.write_text(json.dumps(serialized(report), indent=2) + "\n")
    print(json.dumps(serialized({k: v for k, v in report.items()
                                  if k != "fourth_moment_certificate"}), indent=2))
