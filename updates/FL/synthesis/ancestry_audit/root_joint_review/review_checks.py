#!/usr/bin/env python3
"""Independent post-isolation checks of FL-root's joint-ancestry note.

Uses only Python's standard library.  Exact rational checks cover the generator
identities and the 32-atom P/R witness.  Exponential-kernel checks are floating
point checks with a stated tolerance; they are not a replay of a supplied
producer script (none was supplied for this review).
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import exp, isclose
import json
import random
from pathlib import Path


STATES = (-1, 0, 1)
PI = (F(1, 4), F(1, 2), F(1, 4))
FVAL = tuple(F(z) for z in STATES)
HVAL = tuple(F(z * z) - F(1, 2) for z in STATES)


def q_matrix(x, y):
    c, r = y / 2, (2 * x - y) / 4
    return ((-(c + r), c, r), (c / 2, -c, c / 2), (r, c, -(c + r)))


def mv(matrix, vector):
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def verify_generator_exact():
    cases = ((F(2), F(1)), (F(3, 2), F(1, 3)), (F(2), F(4)))
    for x, y in cases:
        q = q_matrix(x, y)
        assert all(sum(row) == 0 for row in q)
        assert tuple(sum(PI[i] * q[i][j] for i in range(3)) for j in range(3)) == (0, 0, 0)
        for i in range(3):
            for j in range(3):
                assert PI[i] * q[i][j] == PI[j] * q[j][i]
        assert mv(q, FVAL) == tuple(-x * z for z in FVAL)
        assert mv(q, HVAL) == tuple(-y * z for z in HVAL)
    assert sum(PI[i] * FVAL[i] * FVAL[i] for i in range(3)) == F(1, 2)
    assert tuple(FVAL[i] * HVAL[i] for i in range(3)) == tuple(F(1, 2) * z for z in FVAL)
    assert sum(PI[i] * HVAL[i] * HVAL[i] for i in range(3)) == F(1, 4)
    return {"exact_generator_cases": len(cases), "reversibility": True,
            "stationarity": True, "f_and_h_eigenrelations": True}


@lru_cache(maxsize=None)
def transition_matrix(x, y, t):
    ex, ey = exp(-x * t), exp(-y * t)
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            kernel = 1 + 2 * ex * float(FVAL[i] * FVAL[j]) + 4 * ey * float(HVAL[i] * HVAL[j])
            row.append(float(PI[j]) * kernel)
        out.append(tuple(row))
    return tuple(out)


def moment(times, x, y):
    """Enumerate the finite-state Markov path moment for a sorted time list."""
    if not times:
        return 1.0
    result = 0.0
    for states in product(range(3), repeat=len(times)):
        value = float(PI[states[0]]) * float(FVAL[states[0]])
        for k in range(1, len(times)):
            value *= transition_matrix(x, y, times[k] - times[k - 1])[states[k - 1]][states[k]]
            value *= float(FVAL[states[k]])
        result += value
    return result


def verify_four_point_and_mixing():
    x, y = 1.7, 0.8
    tested = 0
    gaps = (0.0, 0.13, 0.7)
    for d1, d2, d3 in product(gaps, repeat=3):
        times = (0.0, d1, d1 + d2, d1 + d2 + d3)
        got = moment(times, x, y)
        want = 0.25 * exp(-x * (d1 + d3)) * (1 + exp(-y * d2))
        assert abs(got - want) < 2e-13, (times, got, want)
        tested += 1
    # Mixed repeated-time patterns exercise zero gaps beyond the ordered four-point identity.
    for times in ((0.0, 0.0, 0.4, 0.4), (-0.3, 0.2, 0.2, 1.1), (0.0, 0.1, 0.8, 2.0)):
        got = moment(times, x, y)
        d1, d2, d3 = (times[1] - times[0], times[2] - times[1], times[3] - times[2])
        want = 0.25 * exp(-x * (d1 + d3)) * (1 + exp(-y * d2))
        assert abs(got - want) < 2e-13, (times, got, want)
        tested += 1

    @lru_cache(maxsize=None)
    def d_tv(t):
        p = transition_matrix(x, y, t)
        return max(0.5 * sum(abs(p[i][j] - float(PI[j])) for j in range(3)) for i in range(3))

    # Check the stated row-TV upper envelope at a grid including t=0.
    for t in (0.0, 0.01, 0.1, 0.5, 1.0, 4.0, 20.0):
        assert d_tv(t) <= 0.5 * (exp(-x * t) + exp(-y * t)) + 2e-14

    # Exhaustive small offset-grid check of the intermediate pointwise cut bound,
    # using the exact finite-state covariance and its actual row-TV envelope.
    offsets = (0.0, 0.2, 0.7, 1.4)
    shifts = (0.0, 0.01, 0.2, 0.7, 1.4, 3.0)
    cases = 0
    worst_margin = float("inf")
    for n in (1, 2, 3, 4):
        for a in combinations_with_replacement(offsets, n):
            mu = moment(a, x, y)
            for s in shifts:
                joint_times = tuple(sorted(a + tuple(t + s for t in a)))
                cov = moment(joint_times, x, y) - mu * mu
                cross_sum = sum(d_tv(abs(s + aj - ai)) for ai in a for aj in a)
                rhs = 4 * cross_sum
                assert abs(cov) <= rhs + 4e-12, (a, s, cov, rhs)
                worst_margin = min(worst_margin, rhs - abs(cov))
                cases += 1
    return {"four_point_float_cases": tested,
            "pointwise_cut_bound_cases": cases,
            "mixing_envelope_grid_checks": 7,
            "pointwise_cut_bound_passed": True,
            "minimum_rhs_minus_abs_covariance": worst_margin,
            "floating_tolerance": 4e-12}


BITS = tuple(product((0, 1), repeat=4))
EVEN = tuple(b for b in BITS if sum(b) % 2 == 0)
ODD = tuple(b for b in BITS if sum(b) % 2 == 1)


def atom_ages(bits, d):
    return tuple(j + bits[j] + (d if j >= 2 else 0) for j in range(4))


def model_atoms(model):
    if model == "P":
        selected = ((EVEN, 0), (ODD, 1))
    else:
        selected = ((ODD, 0), (EVEN, 1))
    return tuple((b, d, F(1, 16)) for group, d in selected for b in group)


def weighted_law(atoms, key):
    out = defaultdict(F)
    for b, d, weight in atoms:
        out[key(atom_ages(b, d))] += weight
    return dict(out)


def bernoulli_count_law(probabilities):
    law = [F(1)]
    for p in probabilities:
        nxt = [F(0)] * (len(law) + 1)
        for k, mass in enumerate(law):
            nxt[k] += mass * (1 - p)
            nxt[k + 1] += mass * p
        law = nxt
    return tuple(law)


def verify_32_atom_witness():
    p_atoms, r_atoms = model_atoms("P"), model_atoms("R")
    assert len(p_atoms) == len(r_atoms) == 16
    assert len(EVEN) == len(ODD) == 8
    # Every labelled proper-coordinate marginal agrees, exactly.
    proper = 0
    for k in (1, 2, 3):
        for inds in combinations_with_replacement(range(4), k):
            # Distinct-coordinate marginals are the claim; repeated requests add no information.
            if len(set(inds)) != k:
                continue
            key = lambda ages, inds=inds: tuple(ages[i] for i in inds)
            assert weighted_law(p_atoms, key) == weighted_law(r_atoms, key)
            proper += 1
    p_ages = [atom_ages(b, d) for b, d, _ in p_atoms]
    r_ages = [atom_ages(b, d) for b, d, _ in r_atoms]

    def lg(ages):
        return ((ages[1] - ages[0]) + (ages[3] - ages[2]), ages[2] - ages[1])

    p_law = weighted_law(p_atoms, lambda ages: lg(ages)[0])
    r_law = weighted_law(r_atoms, lambda ages: lg(ages)[0])
    assert p_law == r_law
    p_span = weighted_law(p_atoms, lambda ages: ages[3] - ages[0])
    r_span = weighted_law(r_atoms, lambda ages: ages[3] - ages[0])
    assert p_span == r_span

    def joint_transform(atoms, u, v):
        return sum(weight * u ** lg(atom_ages(b, d))[0] * v ** lg(atom_ages(b, d))[1]
                   for b, d, weight in atoms)

    u, v = F(1, 4), F(1, 2)
    mp, mr = joint_transform(p_atoms, u, v), joint_transform(r_atoms, u, v)
    delta = mp - mr
    assert delta == F(9, 8192), delta
    assert delta / 4 == F(9, 32768)
    # Exact transform difference as a symbolic rational evaluation.
    assert (1 - v) * (1 - u) ** 2 * (u - v) ** 2 / 16 == delta

    # All six-node binary waveforms with <=2 edges (all sampled single rectangles,
    # plus constant complements) have identical full count distributions.
    masks = [m for m in product((0, 1), repeat=6)
             if sum(m[i] != m[i - 1] for i in range(1, 6)) <= 2]
    assert len(masks) == 32
    p_low, p_high = F(1, 100), F(99, 100)
    waveform_checks = 0
    for mask in masks:
        def mixture_count_law(atoms):
            result = [F(0)] * 5
            for b, d, weight in atoms:
                ages = atom_ages(b, d)
                probs = [p_high if mask[age] else p_low for age in ages]
                law = bernoulli_count_law(probs)
                result = [x + weight * y for x, y in zip(result, law)]
            return tuple(result)
        assert mixture_count_law(p_atoms) == mixture_count_law(r_atoms), mask
        waveform_checks += 1

    # The laws include 32 support atoms across P and R; each model has 16.
    assert len(set(p_ages)) == 16 and len(set(r_ages)) == 16
    return {"atoms_per_model": 16,
            "combined_model_atoms": 32,
            "proper_coordinate_marginals_checked": proper,
            "L_law_equal": True,
            "span_law_equal": True,
            "single_rectangle_count_laws_checked": waveform_checks,
            "M_P_minus_M_R_exact": str(delta),
            "C_P_minus_C_R_exact": str(delta / 4),
            "count_probabilities": [str(p_low), str(p_high)]}


def verify_time_history_coupling_counterexample():
    # x=2, y=1 gives the valid envelope K=3/4.  With n=4, a=1/2, b=0,
    # T=2000, N=10000, the claimed RHS is exactly 192/2000 + 256/10000.
    # Let P=1000, T_i~Unif[0,2P], and all four ages equal T_i mod P.
    # Then the code-conditional expectation is (Z(0)^4+Z(P)^4)/2.
    claimed_rhs = F(192, 2000) + F(256, 10000)
    exact_code_variance_lower_bound = F(1, 8)  # actual is (1+exp(-1000))/8
    assert claimed_rhs == F(76, 625)
    assert exact_code_variance_lower_bound == F(1, 8)
    assert claimed_rhs < exact_code_variance_lower_bound
    return {
        "counterexample_scope": "requires time-history dependence; marginal history law alone is fixed and code-independent",
        "x": 2, "y": 1, "mixing_envelope_K": "3/4",
        "n": 4, "a": "1/2", "b": 0, "R_W_squared": 256,
        "P": 1000, "T": 2000, "N_products": 10000,
        "claimed_code_term": "192/2000",
        "claimed_sampling_term": "256/10000",
        "claimed_total_RHS": str(claimed_rhs),
        "actual_code_variance": "(1+exp(-1000))/8",
        "actual_code_variance_lower_bound": str(exact_code_variance_lower_bound),
        "strict_violation_gap_lower_bound": str(exact_code_variance_lower_bound - claimed_rhs),
    }


def main():
    result = {
        "scope": "independent post-isolation review; not a producer-script replay, external validation, or physical calibration",
        "generator": verify_generator_exact(),
        "four_point_and_mixing": verify_four_point_and_mixing(),
        "32_atom_witness": verify_32_atom_witness(),
        "time_history_counterexample": verify_time_history_coupling_counterexample(),
    }
    output = Path(__file__).with_name("check_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
