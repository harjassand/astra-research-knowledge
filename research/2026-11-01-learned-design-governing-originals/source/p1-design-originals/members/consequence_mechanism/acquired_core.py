"""Noisy acquisition and execution of a robust optimization core.

Python/numpy executable companion to ACQUIRED_OPTIMIZATION_CORE.txt.
The learner receives an energy-measurement interface, n, degree/edge bounds,
field scope and requested regret. It never receives the graph or coefficients.
Two acquired graph routes are implemented: four-point tomography and sparse
random-sign group discovery. Component optimization is explicit enumeration.
The fixture generator and verifier alone inspect the true coefficients.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


class EnergyExperiment:
    """Actual Gaussian noise draws; all represented energy samples are drawn.

    Preparing each new full configuration charges its changed control bits.
    Repeated measurements at an unchanged configuration do not charge another
    preparation. Initial preparation charges n bits. No source/reset is hidden.
    """

    def __init__(self, b, edges, sigma, seed):
        self._b = np.asarray(b, dtype=float)
        self._edges = [(int(i), int(j), float(w)) for i, j, w in edges]
        self.sigma = float(sigma)
        self.rng = np.random.default_rng(seed)
        self.samples = 0
        self.preparation_bit_changes = 0
        self.preparations = 0
        self._last = None

    def _energy(self, x):
        return float(self._b @ x + sum(w * x[i] * x[j]
                                     for i, j, w in self._edges))

    def measure_mean(self, x, repetitions=1):
        x = np.asarray(x, dtype=np.int8)
        if self._last is None:
            self.preparation_bit_changes += len(x)
            self.preparations += 1
        else:
            changed = int(np.count_nonzero(x != self._last))
            self.preparation_bit_changes += changed
            self.preparations += int(changed > 0)
        self._last = x.copy()
        self.samples += repetitions
        noise = self.rng.normal(0.0, self.sigma, repetitions).mean()
        return self._energy(x) + float(noise)


def paired_fields(experiment, n, vertices, repetitions):
    plus = np.ones(n, dtype=np.int8)
    minus = -plus
    ep = experiment.measure_mean(plus, repetitions)
    em = experiment.measure_mean(minus, repetitions)
    result = {}
    for i in vertices:
        xp = plus.copy()
        xm = minus.copy()
        xp[i] = -1
        xm[i] = +1
        epi = experiment.measure_mean(xp, repetitions)
        emi = experiment.measure_mean(xm, repetitions)
        result[i] = (ep - epi + emi - em) / 4.0
    return result


def dense_incident_tomography(experiment, n, core, tau, failure):
    """Conventional four-point acquisition; no useful graph is supplied."""
    core_set = set(core)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
             if i in core_set or j in core_set]
    count = max(1, len(pairs) + len(core))
    # Every coefficient and retained field has error <= tau/4 on this event.
    repeats = max(1, math.ceil(8 * experiment.sigma**2 / tau**2
                              * math.log(2 * count / failure)))
    plus = np.ones(n, dtype=np.int8)
    minus = -plus
    ep = experiment.measure_mean(plus, repeats)
    em = experiment.measure_mean(minus, repeats)
    singles = {}
    for i in range(n):
        x = plus.copy()
        x[i] = -1
        singles[i] = experiment.measure_mean(x, repeats)
    fields = {}
    for i in core:
        x = minus.copy()
        x[i] = +1
        emi = experiment.measure_mean(x, repeats)
        fields[i] = (ep - singles[i] + emi - em) / 4.0
    edges = {}
    for i, j in pairs:
        x = plus.copy()
        x[i] = -1
        x[j] = -1
        eij = experiment.measure_mean(x, repeats)
        estimate = (ep - singles[i] - singles[j] + eij) / 4.0
        if abs(estimate) > tau:
            edges[i, j] = estimate
    return fields, edges, {"route": "four_point", "repetitions": repeats,
                           "possible_incident_pairs": len(pairs)}


def sparse_incident_discovery(experiment, n, core, degree_bound,
                              tau, failure, seed):
    """Noisy random-sign group discovery with an explicit work cap."""
    rng = np.random.default_rng(seed)
    u = len(core)
    trials = math.ceil(12 * math.log(8 * n * max(1, u) / failure))
    repeats = max(1, math.ceil(8 * experiment.sigma**2 / tau**2
                              * math.log(16 * n * max(1, u)
                                         * trials / failure)))
    max_groups = 1 + 2 * degree_bound * math.ceil(math.log2(max(2, n)))
    directed = {}
    groups_visited = 0
    sign_trials = 0

    def signed_group_mean(i, group, signs):
        x = np.ones(n, dtype=np.int8)
        x[group] = signs
        xi = x.copy()
        xi[i] = -1
        other = x.copy()
        other[group] *= -1
        other_i = other.copy()
        other_i[i] = -1
        return (experiment.measure_mean(x, repeats)
                - experiment.measure_mean(xi, repeats)
                - experiment.measure_mean(other, repeats)
                + experiment.measure_mean(other_i, repeats)) / 4.0

    for i in core:
        todo = [[j for j in range(n) if j != i]]
        row_groups = 0
        while todo:
            group = todo.pop()
            if not group:
                continue
            row_groups += 1
            groups_visited += 1
            if row_groups > max_groups:
                raise RuntimeError("Acquisition work cap exceeded; no answer certified")
            positive = False
            for _ in range(trials):
                signs = rng.choice(np.array([-1, 1], dtype=np.int8), len(group))
                value = signed_group_mean(i, group, signs)
                sign_trials += 1
                if abs(value) > tau:
                    positive = True
                    break
            if not positive:
                continue
            if len(group) == 1:
                j = group[0]
                value = signed_group_mean(i, group, np.array([1], dtype=np.int8))
                if abs(value) > tau:
                    directed[i, j] = value
            else:
                middle = len(group) // 2
                todo.extend([group[:middle], group[middle:]])
    edges = {}
    for (i, j), value in directed.items():
        key = min(i, j), max(i, j)
        if (j, i) in directed:
            value = (value + directed[j, i]) / 2.0
        edges[key] = value
    field_repeats = max(1, math.ceil(experiment.sigma**2 / (2 * tau**2)
                                    * math.log(4 * max(1, u) / failure)))
    fields = paired_fields(experiment, n, core, field_repeats)
    return fields, edges, {"route": "random_sign_groups", "trials_cap": trials,
                           "repetitions": repeats, "groups_visited": groups_visited,
                           "actual_sign_trials": sign_trials,
                           "row_group_cap": max_groups,
                           "field_repetitions": field_repeats}


def connected_components(vertices, edges):
    adjacency = {i: [] for i in vertices}
    for i, j in edges:
        if i in adjacency and j in adjacency:
            adjacency[i].append(j)
            adjacency[j].append(i)
    unseen = set(vertices)
    components = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        stack = [start]
        component = []
        while stack:
            i = stack.pop()
            component.append(i)
            for j in adjacency[i]:
                if j in unseen:
                    unseen.remove(j)
                    stack.append(j)
        components.append(sorted(component))
    return components


@dataclass
class AcquiredCore:
    n: int
    pinned: dict
    core: list
    fields: dict
    edges: dict
    components: list
    field_scope: float
    regret_budget: float
    tau: float
    degree_bound: int

    def solve(self, h, component_cap=24):
        h = np.asarray(h, dtype=float)
        if len(h) != self.n or np.max(np.abs(h)) > self.field_scope + 1e-14:
            raise ValueError("Query lies outside the acquired field scope")
        if any(len(c) > component_cap for c in self.components):
            raise RuntimeError("Computational core exceeds the declared enumeration budget")
        x = np.zeros(self.n, dtype=np.int8)
        for i, value in self.pinned.items():
            x[i] = value
        enumerated = 0
        for component in self.components:
            cset = set(component)
            local_fields = {i: self.fields[i] + h[i] for i in component}
            internal_edges = []
            for (i, j), weight in self.edges.items():
                if i in cset and j in cset:
                    internal_edges.append((i, j, weight))
                elif i in cset and j in self.pinned:
                    local_fields[i] += weight * self.pinned[j]
                elif j in cset and i in self.pinned:
                    local_fields[j] += weight * self.pinned[i]
            best_value = math.inf
            best_assignment = None
            for signs in itertools.product((-1, 1), repeat=len(component)):
                assignment = dict(zip(component, signs))
                value = (sum(local_fields[i] * assignment[i] for i in component)
                         + sum(w * assignment[i] * assignment[j]
                               for i, j, w in internal_edges))
                enumerated += 1
                if value < best_value:
                    best_value = value
                    best_assignment = assignment
            for i, value in best_assignment.items():
                x[i] = value
        return x, enumerated


def acquire(experiment, n, degree_bound, edge_bound, field_scope,
            epsilon_per_site, coarse_radius, failure=.01, route="four_point",
            group_seed=781):
    failures = failure / 3
    coarse_n = max(1, math.ceil(experiment.sigma**2 / (2 * coarse_radius**2)
                                * math.log(2 * n / failures)))
    coarse = paired_fields(experiment, n, range(n), coarse_n)
    threshold = degree_bound * edge_bound + field_scope + coarse_radius
    pinned = {i: -1 if value > 0 else 1 for i, value in coarse.items()
              if abs(value) > threshold}
    core = [i for i in range(n) if i not in pinned]
    tau = epsilon_per_site * n / (2 * (1 + 2 * degree_bound) * max(1, len(core)))
    before_fine = experiment.samples
    if not core:
        fields, edges, details = {}, {}, {"route": "empty_core"}
    elif route == "four_point":
        fields, edges, details = dense_incident_tomography(
            experiment, n, core, tau, failures)
    elif route == "random_sign_groups":
        fields, edges, details = sparse_incident_discovery(
            experiment, n, core, degree_bound, tau, failures, group_seed)
    else:
        raise ValueError(route)
    components = connected_components(core, edges)
    acquired = AcquiredCore(n, pinned, core, fields, edges, components,
                            field_scope, epsilon_per_site * n, tau, degree_bound)
    details.update({"coarse_repetitions": coarse_n,
                    "coarse_samples": before_fine,
                    "fine_samples": experiment.samples - before_fine,
                    "total_energy_samples": experiment.samples,
                    "preparation_bit_changes": experiment.preparation_bit_changes,
                    "preparations": experiment.preparations,
                    "pinned_count": len(pinned), "core_size": len(core),
                    "component_sizes": [len(c) for c in components],
                    "retained_edges": len(edges), "tau": tau,
                    "regret_budget": epsilon_per_site * n})
    return acquired, details


def make_fixture(n, weak_vertices, seed):
    rng = np.random.default_rng(seed)
    # Unknown to the learner: an extensively frustrated degree-four graph.
    pair_set = set()
    for i in range(n):
        for distance in (1, 2):
            j = (i + distance) % n
            pair_set.add((min(i, j), max(i, j)))
    edges = [(i, j, float(rng.choice((-1, 1)) * rng.uniform(.04, .20)))
             for i, j in sorted(pair_set)]
    b = rng.choice((-1, 1), n) * rng.uniform(3., 4., n)
    b[list(weak_vertices)] = rng.uniform(-.025, .025, len(weak_vertices))
    return b, edges


def exact_truth_minimum(b, edges, h, pinned=None):
    n = len(b)
    pinned = {} if pinned is None else pinned
    free = [i for i in range(n) if i not in pinned]
    x = np.ones(n, dtype=np.int8)
    for i, value in pinned.items():
        x[i] = value
    best = math.inf
    best_x = None
    for signs in itertools.product((-1, 1), repeat=len(free)):
        x[free] = signs
        value = float((b + h) @ x + sum(w*x[i]*x[j] for i, j, w in edges))
        if value < best:
            best, best_x = value, x.copy()
    return best, best_x


def verify_fixture(n, weak_vertices, route, seed, queries,
                   full_enumeration=False):
    b, edges = make_fixture(n, weak_vertices, seed)
    oracle = EnergyExperiment(b, edges, sigma=.0005, seed=seed+1)
    acquired, details = acquire(oracle, n, 4, .20, .10, .02, .05,
                                route=route, group_seed=seed+2)
    truth_edges = {(i, j): w for i, j, w in edges}
    true_degree = [0] * n
    true_radius = np.zeros(n)
    for i, j, w in edges:
        true_degree[i] += 1
        true_degree[j] += 1
        true_radius[i] += abs(w)
        true_radius[j] += abs(w)
    # Independent verification of the proof's factual certificate conditions.
    assert max(true_degree) <= acquired.degree_bound
    assert all(abs(b[i]) > true_radius[i] + acquired.field_scope
               and a == -np.sign(b[i]) for i, a in acquired.pinned.items())
    false_edges = set(acquired.edges) - set(truth_edges)
    assert not false_edges
    retained_error = max((abs(w-truth_edges[e]) for e, w in acquired.edges.items()),
                         default=0.)
    omitted = {e: abs(w) for e, w in truth_edges.items()
               if any(i in acquired.core for i in e) and e not in acquired.edges}
    max_omitted = max(omitted.values(), default=0.)
    field_error = max((abs(acquired.fields[i]-b[i]) for i in acquired.core), default=0.)
    assert retained_error <= acquired.tau
    assert max_omitted <= 2 * acquired.tau
    assert field_error <= acquired.tau

    rng = np.random.default_rng(seed+3)
    max_regret = 0.
    max_assignments = 0
    previous = np.ones(n, dtype=np.int8)
    for t in range(queries):
        # Later fields explicitly depend on earlier outputs.
        h = acquired.field_scope * (.70 * rng.uniform(-1, 1, n)
                                   + .30 * previous * (-1 if t % 2 else 1))
        answer, enumerated = acquired.solve(h)
        max_assignments = max(max_assignments, enumerated)
        truth_pins = None if full_enumeration else acquired.pinned
        optimum, _ = exact_truth_minimum(b, edges, h, truth_pins)
        value = float((b+h) @ answer
                      + sum(w * answer[i] * answer[j] for i, j, w in edges))
        regret = value - optimum
        assert regret >= -1e-10
        assert regret <= acquired.regret_budget + 1e-10
        max_regret = max(max_regret, regret)
        previous = answer
    details.update({"n": n, "adaptive_queries_verified": queries,
                    "verification": "full_true_enumeration" if full_enumeration
                      else "true_coefficients_and_proved_pins_then_exact_enumeration",
                    "max_observed_regret": max_regret,
                    "max_enumerated_assignments_per_query": max_assignments,
                    "full_configuration_count": str(2**n),
                    "max_retained_coefficient_error": retained_error,
                    "max_omitted_incident_edge": max_omitted,
                    "max_core_field_error": field_error,
                    "false_retained_edges": len(false_edges),
                    "unlearned_pinned_pinned_edges": sum(
                        i in acquired.pinned and j in acquired.pinned
                        for i, j, _ in edges)})
    return details


def main():
    small = verify_fixture(14, [2, 3, 4, 8, 9], "four_point", 121, 8,
                           full_enumeration=True)
    sparse = verify_fixture(12, [2, 3, 7], "random_sign_groups", 779, 5,
                            full_enumeration=True)
    # Large state space, two residual islands. No enumeration of the ambient
    # 2^160 configurations occurs; the verifier also checks pinning directly.
    large = verify_fixture(160, list(range(10, 16)) + list(range(80, 86)),
                           "four_point", 1901, 12, full_enumeration=False)
    output = {"status": "all proof conditions and adaptive-regret checks passed",
              "novelty": "No speedup over a strong conventional persistency route claimed",
              "fixtures": [small, sparse, large]}
    target = Path(__file__).with_name("acquired_core_results.json")
    target.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
