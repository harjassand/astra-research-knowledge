#!/usr/bin/env python3
"""Exact small-instance models and design compiler for recombinase branching.

The statistical functions implement the explicit conditional-independence
model Q_F = integral product_i Bernoulli(p_i(a)) dF(a).  They do not assert
that Bxb1 modules in a real cell satisfy that model.  The tree compiler is a
separate idealized architecture: each active node resolves a competing race,
then only its selected child is enabled.  Unresolved nodes remain an explicit
outcome so finite exposure is not silently treated as successful fate choice.
"""

from __future__ import annotations

import heapq
import itertools
import math
from collections.abc import Callable, Iterable, Mapping, Sequence


def total_variation(p: Sequence[float], q: Sequence[float]) -> float:
    if len(p) != len(q):
        raise ValueError("Probability vectors must have the same length")
    return 0.5 * sum(abs(float(a) - float(b)) for a, b in zip(p, q))


def parallel_fate_law(
    activities: Sequence[float],
    weights: Sequence[float],
    response_functions: Sequence[Callable[[float], float]],
) -> dict[tuple[int, ...], float]:
    """Evaluate a finite-support shared-exposure mixture of product laws."""
    if len(activities) != len(weights) or not activities:
        raise ValueError("Activities and weights must have the same nonzero length")
    if any(a < 0 for a in activities) or any(w < 0 for w in weights):
        raise ValueError("Activity and mixture weights must be nonnegative")
    if not math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("Mixture weights must sum to one")
    if not response_functions:
        raise ValueError("At least one module is required")

    law = {bits: 0.0 for bits in itertools.product((0, 1), repeat=len(response_functions))}
    for activity, weight in zip(activities, weights):
        ps = [float(fn(activity)) for fn in response_functions]
        if any(not 0.0 <= p <= 1.0 for p in ps):
            raise ValueError("Response probabilities must lie in [0, 1]")
        for bits in law:
            prob = weight
            for bit, p in zip(bits, ps):
                prob *= p if bit else 1.0 - p
            law[bits] += prob
    return law


def hazard_response(rate: float) -> Callable[[float], float]:
    """First-order activation response p(a)=1-exp(-rate*a)."""
    if rate < 0:
        raise ValueError("Rate must be nonnegative")
    return lambda activity: -math.expm1(-rate * activity)


def product_of_marginals(law: Mapping[tuple[int, ...], float]) -> dict[tuple[int, ...], float]:
    """Independent-bit law with the supplied law's one-bit marginals."""
    if not law:
        raise ValueError("Law cannot be empty")
    m = len(next(iter(law)))
    if any(len(bits) != m for bits in law):
        raise ValueError("All states must have equal dimension")
    marginals = [sum(q for bits, q in law.items() if bits[i]) for i in range(m)]
    result: dict[tuple[int, ...], float] = {}
    for bits in itertools.product((0, 1), repeat=m):
        prob = 1.0
        for bit, p in zip(bits, marginals):
            prob *= p if bit else 1.0 - p
        result[bits] = prob
    return result


def dkw_full_law_sample_bound(
    a_max: float,
    sum_lipschitz: float,
    epsilon_tv: float,
    delta: float,
) -> int:
    """Sufficient iid measured-activity sample size for TV <= epsilon.

    Assumes exact response curves, activity measured without error, and
    iid cells. DKW plus the 1-D W1 bound gives
    n >= (a_max*sum_i L_i)^2 log(2/delta)/(2 epsilon_tv^2).
    """
    if a_max < 0 or sum_lipschitz < 0 or epsilon_tv <= 0 or not 0 < delta < 1:
        raise ValueError("Invalid DKW bound inputs")
    bound = (a_max * sum_lipschitz) ** 2 * math.log(2.0 / delta) / (2.0 * epsilon_tv**2)
    return math.ceil(bound)


def response_rate_error_bound(
    a_max: float,
    rates: Sequence[float],
    rate_errors: Sequence[float],
    exposure_w1_error: float = 0.0,
) -> float:
    """TV bound for first-order hazards with rate and exposure-law errors.

    Since |d(1-exp(-k a))/dk| <= a_max and each hazard response is
    k-Lipschitz in a, product-law telescoping gives the displayed bound.
    """
    if (a_max < 0 or exposure_w1_error < 0 or len(rates) != len(rate_errors)
            or any(k < 0 for k in rates) or any(e < 0 for e in rate_errors)):
        raise ValueError("Errors and a_max must be nonnegative")
    return a_max * sum(rate_errors) + sum(rates) * exposure_w1_error


def one_hot_pairwise_obstruction(m: int) -> tuple[float, float]:
    """Return (target joint, parallel lower bound) for equal one-hot fates.

    Valid when p_i(a) and p_j(a) are both nondecreasing functions of the
    same scalar activity and modules are conditionally independent.
    """
    if m < 2:
        raise ValueError("At least two one-hot fates are required")
    marginal = 1.0 / m
    return 0.0, marginal * marginal


def competing_race_probabilities(k_left: float, k_right: float, integrated_activity: float) -> dict[str, float]:
    """Cause probabilities for hazards k_left*u(t), k_right*u(t).

    integrated_activity is A(T)=integral_0^T u(t)dt.  The left:right ratio,
    conditional on a reaction by T, is dose-invariant; finite-dose failures
    are returned explicitly as unresolved.
    """
    if k_left <= 0 or k_right <= 0 or integrated_activity < 0:
        raise ValueError("Rates must be positive and integrated activity nonnegative")
    total_rate = k_left + k_right
    event_probability = -math.expm1(-total_rate * integrated_activity)
    q_left = k_left / total_rate
    return {
        "left": q_left * event_probability,
        "right": (1.0 - q_left) * event_probability,
        "unresolved": 1.0 - event_probability,
        "left_given_event": q_left,
    }


def rare_target_assay_n_for_detection(probability: float, confidence: float) -> int:
    """Minimum iid cells to see a fate at least once with stated confidence."""
    if not 0.0 < probability <= 1.0 or not 0.0 < confidence < 1.0:
        raise ValueError("Probability and confidence must lie in (0, 1)")
    if probability == 1.0:
        return 1
    return math.ceil(math.log1p(-confidence) / math.log1p(-probability))


def rare_target_assay_n_for_relative_error(
    probability: float, relative_error: float, delta: float
) -> int:
    """Chernoff sufficient n for relative error of a rare fate probability."""
    if (not 0.0 < probability <= 1.0 or not 0.0 < relative_error <= 1.0
            or not 0.0 < delta < 1.0):
        raise ValueError("Invalid rare-target bound inputs")
    return math.ceil(3.0 * math.log(2.0 / delta) / (probability * relative_error**2))


def compile_huffman_tree(probabilities: Mapping[str, float]) -> tuple[dict, float]:
    """Compile a target categorical law to a minimum-mean-depth binary tree."""
    if not probabilities or any(p <= 0 for p in probabilities.values()):
        raise ValueError("All listed fate probabilities must be positive")
    if not math.isclose(sum(probabilities.values()), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("Fate probabilities must sum to one")

    heap: list[tuple[float, int, dict]] = []
    next_id = 0
    for fate, p in sorted(probabilities.items()):
        heap.append((p, next_id, {"fate": fate, "mass": p}))
        next_id += 1
    heapq.heapify(heap)
    if len(heap) == 1:
        return heap[0][2], 0.0
    while len(heap) > 1:
        p0, _, left = heapq.heappop(heap)
        p1, _, right = heapq.heappop(heap)
        mass = p0 + p1
        node = {
            "mass": mass,
            "left": left,
            "right": right,
            "left_probability": p0 / mass,
            "right_probability": p1 / mass,
        }
        heapq.heappush(heap, (mass, next_id, node))
        next_id += 1
    root = heap[0][2]
    depths: dict[str, int] = {}

    def walk(node: dict, depth: int) -> None:
        if "fate" in node:
            depths[node["fate"]] = depth
            node["depth"] = depth
            return
        node["depth"] = depth
        walk(node["left"], depth + 1)
        walk(node["right"], depth + 1)

    walk(root, 0)
    mean_depth = sum(probabilities[fate] * depths[fate] for fate in probabilities)
    return root, mean_depth


def tree_leaf_probabilities(tree: Mapping, resolved_only: bool = False) -> dict[str, float]:
    """Return ideal leaf law; if resolved_only, condition away unresolved mass."""
    out: dict[str, float] = {}

    def walk(node: Mapping, mass: float) -> None:
        if "fate" in node:
            out[str(node["fate"])] = out.get(str(node["fate"]), 0.0) + mass
            return
        if "left" not in node or "right" not in node:
            out["UNRESOLVED"] = out.get("UNRESOLVED", 0.0) + mass
            return
        event_probability = float(node.get("event_probability", 1.0))
        if not 0.0 <= event_probability <= 1.0:
            raise ValueError("event_probability must lie in [0, 1]")
        unresolved = mass * (1.0 - event_probability)
        if unresolved > 0.0:
            out["UNRESOLVED"] = out.get("UNRESOLVED", 0.0) + unresolved
        pl = float(node["left_probability"])
        pr = float(node["right_probability"])
        if not math.isclose(pl + pr, 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Conditional branch probabilities must sum to one")
        walk(node["left"], mass * event_probability * pl)
        walk(node["right"], mass * event_probability * pr)

    walk(tree, 1.0)
    if resolved_only:
        mass = sum(v for k, v in out.items() if k != "UNRESOLVED")
        if mass == 0:
            return {}
        return {k: v / mass for k, v in out.items() if k != "UNRESOLVED"}
    return out


def tree_node_count(tree: Mapping) -> int:
    if "fate" in tree:
        return 0
    return 1 + tree_node_count(tree["left"]) + tree_node_count(tree["right"])


def run_self_tests() -> dict[str, object]:
    # Shared exposure can produce an exponentially different high-order fate.
    law = parallel_fate_law([0.0, 1.0], [0.9, 0.1], [lambda a: 0.99 if a else 0.0] * 10)
    all_on = law[(1,) * 10]
    marginals = [sum(q for bits, q in law.items() if bits[i]) for i in range(10)]
    product_all_on = math.prod(marginals)
    assert math.isclose(sum(law.values()), 1.0, abs_tol=1e-12)
    assert math.isclose(all_on / product_all_on, 1e9, rel_tol=1e-8)

    # First-order hazard special case is the same mixture implementation.
    hazard = parallel_fate_law([0.25, 1.0], [0.4, 0.6], [hazard_response(0.7), hazard_response(1.2)])
    assert math.isclose(sum(hazard.values()), 1.0, abs_tol=1e-12)
    assert all(v >= 0 for v in hazard.values())

    target = {f"fate_{i}": 0.1 for i in range(10)}
    tree, mean_depth = compile_huffman_tree(target)
    leaves = tree_leaf_probabilities(tree)
    assert tree_node_count(tree) == 9
    assert max(abs(leaves[k] - target[k]) for k in target) < 1e-12
    assert math.isclose(mean_depth, 3.4, abs_tol=1e-12)
    target_joint, parallel_lower = one_hot_pairwise_obstruction(10)
    assert target_joint == 0 and math.isclose(parallel_lower, 0.01, abs_tol=1e-15)
    races = [competing_race_probabilities(1.0, 3.0, a) for a in (0.01, 0.2, 5.0)]
    assert all(math.isclose(race["left_given_event"], 0.25, abs_tol=1e-15) for race in races)
    assert all(math.isclose(r["left"] + r["right"] + r["unresolved"], 1.0, abs_tol=1e-12)
               for r in races)

    # Failure is retained as an explicit mass; a tree need not resolve every cell.
    failure_tree = {"mass": 1.0, "left_probability": 0.4,
                    "right_probability": 0.6, "event_probability": 0.8,
                    "left": {"fate": "A"}, "right": {"fate": "B"}}
    failure_law = tree_leaf_probabilities(failure_tree)
    assert failure_law == {"UNRESOLVED": 0.19999999999999996, "A": 0.32000000000000006,
                           "B": 0.48}
    return {
        "tests": 7,
        "shared_exposure_all_on": all_on,
        "product_marginal_all_on": product_all_on,
        "underprediction_factor": all_on / product_all_on,
        "huffman_leaf_count": len(leaves),
        "huffman_internal_nodes": tree_node_count(tree),
        "huffman_mean_depth": mean_depth,
        "one_hot_pairwise_gap": parallel_lower - target_joint,
        "dkw_example_n": dkw_full_law_sample_bound(1.0, 10.0, 0.05, 0.05),
        "rare_target_detection_n_at_1e-3_95pct": rare_target_assay_n_for_detection(0.001, 0.95),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_self_tests(), indent=2))
