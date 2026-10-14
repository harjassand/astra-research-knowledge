"""Bounded numerical audit of the ideal infinite-degree sinh selector.

This is an implementation check, not a finite-bit exact sampler or proof.
The theorem and exact-real termination argument are in KILLED_TANGENT_THEOREM.md.
"""
import json
import math


def masses(a, h):
    even = a * (math.cosh(h) - 1.0) / h
    odd = (math.sinh(h) - h) / h
    return even, odd


def choose_degree(a, h, u, max_degree=10000):
    even, odd = masses(a, h)
    total = even + odd
    if not (0.0 <= u < 1.0) or total <= 0.0:
        raise ValueError("requires a unit variate and positive nonlinear mass")
    target = u * total
    cumulative = 0.0
    for m in range(2, max_degree + 1):
        coefficient = a if m % 2 == 0 else 1.0
        if coefficient:
            cumulative += coefficient * h ** (m - 1) / math.factorial(m)
        if target < cumulative:
            return m, cumulative, total
    raise RuntimeError("bounded audit did not cross the cumulative series")


def mean_degree(a, h):
    even_mass, odd_mass = masses(a, h)
    mu_even = h * math.sinh(h) / (math.cosh(h) - 1.0)
    mu_odd = h * (math.cosh(h) - 1.0) / (math.sinh(h) - h)
    return (even_mass * mu_even + odd_mass * mu_odd) / (even_mass + odd_mass)


def factorial_series_mass(a, h, max_degree=100):
    return sum(
        (a if m % 2 == 0 else 1.0) * h ** (m - 1) / math.factorial(m)
        for m in range(2, max_degree + 1)
    )


def run():
    h_values = [0.01, 0.2, 0.5, math.log(2.0) - 1e-6]
    a_values = [0.0, 0.3, 1.0]
    u_values = [0.0, 0.1, 0.5, 0.9, 0.999999]
    rows = []
    max_degree = 0
    max_terms = 0
    for h in h_values:
        for a in a_values:
            even_mass, odd_mass = masses(a, h)
            total = even_mass + odd_mass
            series_total = factorial_series_mass(a, h)
            # Sinh enclosure at its extremal residual threshold and |tanh(v)|=1.
            delta = 2.0 * h + 1.0 - math.exp(h)
            event_mass = delta / h + total
            worst_case_event_mass = delta / h + sum(masses(1.0, h))
            offspring_bound = math.exp(h) - 1.0
            mu = mean_degree(a, h)
            assert 0.0 < delta
            # This loose diagnostic tolerance covers cancellation at small h;
            # it is not an outward-rounding certificate.
            assert worst_case_event_mass <= 1.0 + 3e-14
            assert offspring_bound < 1.0
            assert mu < 4.0
            # cosh(h)-1 and sinh(h)-h lose relative precision for small h.
            assert abs(series_total - total) <= 1e-14 * max(1.0, total)
            for u in u_values:
                m, cumulative, formula_total = choose_degree(a, h, u)
                # Crossing the target bounds the unvisited tail by its target gap.
                assert cumulative >= u * formula_total
                assert formula_total - cumulative <= (1.0 - u) * formula_total + 3e-15
                max_degree = max(max_degree, m)
                max_terms = max(max_terms, m - 1)
            rows.append({
                "h": h,
                "A_abs_tanh_v": a,
                "even_mass": even_mass,
                "odd_mass": odd_mass,
                "nonlinear_mass": total,
                "factorial_series_mass_through_degree_100": series_total,
                "closed_form_mass_abs_gap": abs(series_total - total),
                "source_plus_nonlinear_probability_at_delta_bound_for_A": event_mass,
                "worst_case_probability_at_delta_bound_over_A_le_1": worst_case_event_mass,
                "offspring_mean_bound": offspring_bound,
                "conditional_mean_degree_formula": mu,
                "sampled_degrees_for_fixed_unit_variates": [
                    choose_degree(a, h, u)[0] for u in u_values
                ],
            })
    return {
        "method": "ordinary-float bounded inverse-series audit; not an exact sampler",
        "cases": len(rows),
        "fixed_unit_variates": u_values,
        "maximum_degree_in_this_grid": max_degree,
        "maximum_terms_inspected_in_this_grid": max_terms,
        "assertions": [
            "closed-form even/odd nonlinear masses match cumulative factorial series",
            "extremal source plus nonlinear event mass is at most one within stated float tolerance",
            "offspring mean bound is below one for h < log(2)",
            "conditional mean degree formula is below four",
            "all tested inverse-series selections crossed in finite degree",
        ],
        "cases_detail": rows,
        "limitations": [
            "floating-point checks do not certify transcendental inequalities",
            "fixed variates do not establish distributional correctness",
            "no finite-bit exact categorical sampler or path sampler is supplied",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
