"""Continuous nonlinear control from acquired inner/outer hypographs.

Only node intervals, polynomial coefficients, source bounds and known prices
are read. No source reactions or microscopic parameters are requested.
"""
from fractions import Fraction as F
from math import isqrt


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def sqrt_bounds(x, bits=64):
    assert x >= 0
    scale = 1 << bits
    lo = isqrt((x.numerator * scale * scale) // x.denominator)
    hi = lo if F(lo * lo, scale * scale) == x else lo + 1
    return F(lo, scale), F(hi, scale)


def phi(value, utility):
    assert value > 0
    if utility == "compliance":
        return -1 / value
    assert utility == "conductance"
    return value


def lower_cost_hull(values, costs):
    """Lower convex hull in the (response, linear-cost) plane."""
    best = {}
    for i, (x, y) in enumerate(zip(values, costs)):
        if x not in best or y < best[x][0]:
            best[x] = (y, i)
    chain = []
    for x, (y, i) in sorted(best.items()):
        point = (x, y, i)
        while len(chain) >= 2:
            a, b = chain[-2:]
            cross = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])
            if cross > 0:
                break
            chain.pop()
        chain.append(point)
    return chain


def optimize_hull(values, costs, utility="compliance"):
    chain = lower_cost_hull(values, costs)
    assert chain and all(x > 0 for x, _, _ in chain)
    candidates = [(phi(x, utility) - cost, (index, index, F(0)), x)
                  for x, cost, index in chain]
    upper_candidates = [x[0] for x in candidates]
    for a, b in zip(chain, chain[1:]):
        xa, ca, ia = a
        xb, cb, ib = b
        slope = (cb - ca) / (xb - xa)
        intercept = ca - slope * xa
        if utility == "compliance" and slope > 0 and 1 / (xb * xb) <= slope <= 1 / (xa * xa):
            slo, shi = sqrt_bounds(slope)
            upper_candidates.append(-2 * slo - intercept)
            target = min(xb, max(xa, 1 / shi))
            mix = (target - xa) / (xb - xa)
            cost = ca + mix * (cb - ca)
            candidates.append((phi(target, utility) - cost, (ia, ib, mix), target))
    chosen = max(candidates, key=lambda x: x[0])
    return {
        "certified_optimum_upper": max(upper_candidates),
        "feasible_hull_value": chosen[0],
        "mixture": chosen[1],
        "response_coordinate": chosen[2],
        "hull_vertices": len(chain),
    }


def finite_command(u, bits):
    scale = 1 << bits
    return [F((x * scale).__floor__(), scale) for x in u]


def certify_task(law, prices, baseline_lower, dac_bits=20, utility="compliance"):
    """Optimize inner and outer response-cost hulls; certify a finite command."""
    assert len(prices) == law.n and baseline_lower > 0
    if law.bernstein_coefficients is None:
        law.transform()
    costs = [dot(prices, u) for u in law.nodes]
    lower = [max(baseline_lower, iv[0]) for iv in law.intervals]
    bounds = law.uniform_bounds()
    E = bounds["interpolation_uniform_error"]
    positive_upper = [max(baseline_lower, iv[1] + law.bernstein_bias) for iv in law.intervals]
    polynomial_upper = [max(baseline_lower, b + E) for b in law.bernstein_coefficients]
    inner = optimize_hull(lower, costs, utility)
    positive = optimize_hull(positive_upper, costs, utility)
    polynomial = optimize_hull(polynomial_upper, costs, utility)
    root = sqrt_bounds(law.delta * law.kappa)[1]
    lipschitz = law.G ** 2 * (1 + root / 2) ** 2
    candidates = []
    for origin, description in (("inner", inner), ("positive_upper", positive),
                                ("polynomial_upper", polynomial)):
        i, j, mix = description["mixture"]
        exact = [(1 - mix) * a + mix * b for a, b in zip(law.nodes[i], law.nodes[j])]
        actual = finite_command(exact, dac_bits)
        discrepancy = sum(abs(a - b) for a, b in zip(exact, actual))
        jensen_lower = (1 - mix) * lower[i] + mix * lower[j] - lipschitz * discrepancy
        prediction = law.predict(actual)
        j_lower = max(baseline_lower, jensen_lower, prediction["intersection_interval"][0])
        objective_lower = phi(j_lower, utility) - dot(prices, actual)
        candidates.append({
            "origin": origin, "nodes": (i, j), "mix": mix, "ideal_command": exact,
            "command": actual, "actuation_l1": discrepancy,
            "actuation_response_allowance": lipschitz * discrepancy,
            "jensen_J_lower": jensen_lower, "certified_J_lower": j_lower,
            "objective_lower_without_baseline": objective_lower,
            "prediction": prediction,
        })
    chosen = max(candidates, key=lambda x: x["objective_lower_without_baseline"])
    global_upper = min(positive["certified_optimum_upper"], polynomial["certified_optimum_upper"])
    return {
        "utility": utility, "prices": prices,
        "candidate": chosen, "candidate_options": candidates,
        "inner_hull": inner, "positive_upper_hull": positive,
        "polynomial_upper_hull": polynomial,
        "global_objective_upper_without_baseline": global_upper,
        "continuous_simplex_regret": max(F(0), global_upper - chosen["objective_lower_without_baseline"]),
        "extra_source_readings": 0,
        "maximum_proposal_support": min(law.n, 2 * law.k),
        "scope": "All continuous commands in the dose simplex; deterministic mixture, no microscopic source.",
    }
