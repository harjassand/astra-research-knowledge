#!/usr/bin/env python3
"""Exact rational verifier for the three-site directed guarded-switching fixture.

This checks rate-polynomial identities, strict directed-flux face margins,
finite-volume constants, the nonexistence of a common one-dimensional diagonal
certificate inside the safe cube, and a rounded risk-bound example. It is a
fixture verifier, not a general stochastic safety proof.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ALPHAS = (F(1), F(2), F(3))
CYCLE_RATE = F(1, 1000)
SITES = len(ALPHAS)
ELL = F(1, 100)
SAFE = (F(1, 10), F(9, 10))
GUARD = (F(9, 20), F(11, 20))
INITIAL = F(1, 2)

# (reactant order, concentration jump, exact rate coefficient)
MODES = {
    "mode_1": {
        "box": (F(1, 5), F(3, 5)),
        "reactions": ((0, 1, F(741, 4000)),
                      (2, 1, F(19, 10)),
                      (1, -1, F(439, 400)),
                      (3, -1, F(1))),
        "reaction_margins": {"lower": F(3663, 125000),
                             "upper": F(21, 4000)},
    },
    "mode_2": {
        "box": (F(2, 5), F(9, 10)),
        "reactions": ((0, 1, F(7, 500)),
                      (2, 1, F(6, 5)),
                      (1, -1, F(27, 80)),
                      (3, -1, F(1))),
        "reaction_margins": {"lower": F(7, 1000),
                             "upper": F(5103, 125000)},
    },
}


def monomial(x: F, order: int) -> F:
    return x**order


def factorial_error_bound(order: int, upper: F) -> F:
    if order < 2:
        return F(0)
    # For one species E_y(U) = binom(y,2) U^(y-1).
    return F(order * (order - 1), 2) * upper ** (order - 1)


def ceil_fraction(x: F) -> int:
    return (x.numerator + x.denominator - 1) // x.denominator


def fmt(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def reaction_drift(mode: dict, x: F) -> F:
    return sum((k * monomial(x, y) * nu for y, nu, k in mode["reactions"]), F(0))


def reaction_coefficients(mode: dict) -> list[F]:
    coeffs = [F(0)] * 4
    for y, nu, k in mode["reactions"]:
        coeffs[y] += nu * k
    return coeffs


def bernstein_coefficients_on_interval(coeffs: list[F], lo: F, hi: F) -> list[F]:
    """Return exact degree-d Bernstein coefficients after x=lo+(hi-lo)t."""
    degree = len(coeffs) - 1
    width = hi - lo
    power = [F(0)] * (degree + 1)
    for k in range(degree + 1):
        power[k] = sum((coeffs[j] * math.comb(j, k) * lo ** (j - k) * width**k
                        for j in range(k, degree + 1)), F(0))
    return [sum((power[k] * F(math.comb(i, k), math.comb(degree, k))
                 for k in range(i + 1)), F(0)) for i in range(degree + 1)]


def face_data(mode_name: str, mode: dict, site: int, side: str) -> dict:
    low, high = mode["box"]
    U = high
    alpha = ALPHAS[site]
    gamma_rxn = mode["reaction_margins"][side]
    if side == "lower":
        migration = -(ELL * CYCLE_RATE) / alpha
        collar = (low, low + ELL)
        pcoeff = reaction_coefficients(mode)
    else:
        migration = -(ELL * CYCLE_RATE) / alpha
        collar = (high - ELL, high)
        pcoeff = [-z for z in reaction_coefficients(mode)]
    pcoeff[0] -= gamma_rxn
    bernstein = bernstein_coefficients_on_interval(pcoeff, *collar)
    assert all(z >= 0 for z in bernstein), (mode_name, site, side, bernstein)
    margin = gamma_rxn + migration
    assert margin > 0

    D = sum((k * abs(nu) * factorial_error_bound(y, U)
             for y, nu, k in mode["reactions"]), F(0)) / alpha
    reaction_B = sum((k * nu * nu * U**y for y, nu, k in mode["reactions"]), F(0)) / alpha
    # The directed cycle has one incoming and one outgoing edge at every site.
    hopping_B = U * (2 * CYCLE_RATE) / (alpha * alpha)
    B = reaction_B + hopping_B
    J = F(1, 1) / alpha  # reactions and transfers all move one molecule at a site
    mu = margin / 2
    theta = min(F(1, 1) / J, mu / (3 * B))
    assert theta > 0 and B > 0 and J > 0
    return {
        "mode": mode_name,
        "site_1based": site + 1,
        "side": side,
        "reaction_margin": fmt(gamma_rxn),
        "migration_margin": fmt(migration),
        "effective_margin": fmt(margin),
        "factorial_correction_D": fmt(D),
        "jump_bound_J": fmt(J),
        "quadratic_bound_B": fmt(B),
        "theta": fmt(theta),
        "collar_width": fmt(ELL),
        "initial_guard_gap": fmt(F(1, 20)),
        "reaction_margin_bernstein_coefficients": [fmt(z) for z in bernstein],
        "V0_face": ceil_fraction(2 * D / margin),
    }, (margin, D, J, B, theta)


def mode_constants(name: str, mode: dict) -> dict:
    low, high = mode["box"]
    rows = []
    raw = []
    for i in range(SITES):
        for side in ("lower", "upper"):
            row, constants = face_data(name, mode, i, side)
            rows.append(row)
            raw.append(constants)
    V0 = max(1, *(ceil_fraction(2 * D / margin) for margin, D, _J, _B, _theta in raw))
    theta_min = min(theta for _margin, _D, _J, _B, theta in raw)
    c_star = theta_min * ELL
    activity_reaction = sum((alpha * sum((k * high**y for y, _nu, k in mode["reactions"]), F(0))
                             for alpha in ALPHAS), F(0))
    activity_hop = SITES * CYCLE_RATE * high
    Lambda = activity_reaction + activity_hop
    return {
        "V0": V0,
        "theta_min": fmt(theta_min),
        "c_star": fmt(c_star),
        "Lambda": fmt(Lambda),
        "face_constants": rows,
    }, raw


def accept_switch(current_mode: str, target_mode: str, measured: tuple[F, ...], error: F = F(0)) -> bool:
    """Fail-closed supervisor: require source-box and robust target-core membership."""
    if current_mode not in MODES or target_mode not in MODES or current_mode == target_mode:
        return False
    if len(measured) != SITES or error < 0:
        return False
    src_lo, src_hi = MODES[current_mode]["box"]
    dst_lo, dst_hi = MODES[target_mode]["box"]
    d = F(1, 20)
    g_lo, g_hi = GUARD
    for y in measured:
        true_lo, true_hi = y - error, y + error
        if true_lo < src_lo or true_hi > src_hi:
            return False
        if true_lo < dst_lo + d or true_hi > dst_hi - d:
            return False
        if true_lo < g_lo or true_hi > g_hi:
            return False
    return True


def no_common_interval_inside_safe_cube() -> dict:
    """Prove incompatible endpoint signs on the diagonal slice.

    On the diagonal x_1=x_2=x_3, balanced directed circulation vanishes and
    each mode reduces to its scalar reaction drift. Any common invariant set
    containing the guard intersects that diagonal in [a,b] with
    a<=9/20, b>=11/20, and [a,b] subset [1/10,9/10].
    """
    # mode 1 lower inwardness with a<=.45 forces a<=.3; mode 2 lower
    # inwardness with a in [.1,.45] forces a>=.35.
    a_mode1_possible = (SAFE[0], F(3, 10))
    a_mode2_possible = (F(7, 20), GUARD[0])
    lower_intersection_nonempty = max(a_mode1_possible[0], a_mode2_possible[0]) <= min(
        a_mode1_possible[1], a_mode2_possible[1])
    # Upper face signs likewise conflict: mode 1 requires b<=.65 in safe S,
    # while mode 2 requires b>=.8, with b>=.55.
    b_mode1_possible = (GUARD[1], F(13, 20))
    b_mode2_possible = (F(4, 5), SAFE[1])
    upper_intersection_nonempty = max(b_mode1_possible[0], b_mode2_possible[0]) <= min(
        b_mode1_possible[1], b_mode2_possible[1])
    assert not lower_intersection_nonempty
    assert not upper_intersection_nonempty
    return {
        "balanced_cycle_preserves_diagonal": True,
        "mode_1_scalar_roots": ["3/10", "13/20", "19/20"],
        "mode_2_scalar_roots": ["1/20", "7/20", "4/5"],
        "common_lower_inward_endpoint_exists": lower_intersection_nonempty,
        "common_upper_inward_endpoint_exists": upper_intersection_nonempty,
        "conclusion": "no common inward interval on the diagonal inside the safe cube containing the guard",
    }


def main() -> None:
    output = {
        "fixture": "3-site heterogeneous-volume one-way directed cycle; two guarded local CRN modes",
        "alpha": [fmt(x) for x in ALPHAS],
        "directed_edges": [
            {"source": 1, "target": 2, "coefficient": fmt(CYCLE_RATE)},
            {"source": 2, "target": 3, "coefficient": fmt(CYCLE_RATE)},
            {"source": 3, "target": 1, "coefficient": fmt(CYCLE_RATE)},
        ],
        "safe_interval": [fmt(x) for x in SAFE],
        "guard_interval": [fmt(x) for x in GUARD],
        "initial_uniform_concentration": fmt(INITIAL),
        "common_certificate_obstruction": no_common_interval_inside_safe_cube(),
        "supervisor_checks": {
            "initial_guard_switch_mode_1_to_2": accept_switch("mode_1", "mode_2", (INITIAL,) * SITES),
            "reject_outside_guard": not accept_switch("mode_1", "mode_2", (F(3, 5),) * SITES),
            "reject_measurement_error_that_consumes_guard": not accept_switch("mode_1", "mode_2", (INITIAL,) * SITES, F(1, 10)),
        },
        "modes": {},
    }
    V0 = 1
    c_star = None
    lambda_max = F(0)
    face_count = 2 * SITES
    for name, mode in MODES.items():
        constants, _raw = mode_constants(name, mode)
        V0 = max(V0, constants["V0"])
        c_here = F(constants["c_star"])
        c_star = c_here if c_star is None else min(c_star, c_here)
        lambda_max = max(lambda_max, F(constants["Lambda"]))
        output["modes"][name] = constants

    # Choose a lattice-compatible volume and a finite exponential horizon.
    # α_i V/2 is integral for every site when V is even.
    V = 20_000_000
    assert V >= V0 and V % 2 == 0
    segment_cap = 2  # initial segment plus at most one accepted switch
    c_float = float(c_star)
    T = math.exp(c_float * V / 2)
    guard_gap = F(1, 20)
    theta_global = min(F(face["theta"]) for mode_data in output["modes"].values()
                       for face in mode_data["face_constants"])
    initial_term = segment_cap * face_count * math.exp(-float(theta_global * guard_gap * V))
    generator_term = 2 * face_count * float(lambda_max) * V * T * math.exp(-c_float * V)
    assert all(output["supervisor_checks"].values())
    output["risk_example"] = {
        "volume_V": V,
        "minimum_volume_V0": V0,
        "switch_segments_including_initial": segment_cap,
        "horizon_T": T,
        "T_definition": "exp(c_star*V/2)",
        "c_star": fmt(c_star),
        "theta_global": fmt(theta_global),
        "risk_bound_initial_term": initial_term,
        "risk_bound_generator_term": generator_term,
        "risk_bound_total": initial_term + generator_term,
        "upper_bound_on_expected_candidate_events": float(lambda_max) * V * T,
        "exact_probability_certification": "formula uses exact rational margins; printed exponentials rounded with Python math.exp, not directed interval arithmetic",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
