"""Finite checks for hidden parity inference and noisy-evidence hardness.

This is a proof-mechanism check, not a scalable implementation claim.
The graph is reconstructed from the observed parity matrix by enumerating
nonseparating cocircuits; production polynomial recognition is available in CMR.
The Kac-Ward determinant is floating point, checked against exact enumeration.
The paper-level exact arithmetic route uses rational Pfaffian elimination.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


class SmallGraph:
    """Only the simple-graph operations used by the finite checks."""

    def __init__(self):
        self.nodes = set()
        self.edge_data = {}

    def add_nodes_from(self, vertices):
        self.nodes.update(vertices)

    def add_edge(self, u, v, **data):
        self.nodes.update((u, v))
        self.edge_data[tuple(sorted((u, v)))] = data

    @property
    def edges(self):
        return list(self.edge_data)

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        return len(self.edge_data)

    def has_edge(self, u, v):
        return tuple(sorted((u, v))) in self.edge_data


def complete_graph(n):
    graph = SmallGraph()
    graph.add_nodes_from(range(n))
    for u, v in itertools.combinations(range(n), 2):
        graph.add_edge(u, v)
    return graph


def wheel_graph(n):
    graph = SmallGraph()
    for u in range(1, n):
        graph.add_edge(0, u)
        graph.add_edge(u, 1 if u == n - 1 else u + 1)
    return graph


def small_planar_embedding(graph):
    """Find an explicit straight-line certificate for these <=5-vertex fixtures.

    Failure to find a drawing is not a general nonplanarity certificate. The
    rejected fixture is K5, independently excluded by Euler's edge bound.
    """
    n = graph.number_of_nodes()
    if n >= 3 and graph.number_of_edges() > 3 * n - 6:
        return False, None
    points = [(0, 0), (-3, -2), (3, -2), (3, 2), (-3, 2)]
    if n > len(points):
        raise ValueError("Small finite embedding check only")
    nodes = sorted(graph.nodes)

    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

    for assignment in itertools.permutations(points, n):
        pos = dict(zip(nodes, assignment))
        valid = True
        for u, v in graph.edges:
            a, b = pos[u], pos[v]
            for w in nodes:
                if w in (u, v):
                    continue
                c = pos[w]
                if cross(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]):
                    valid = False
            if not valid:
                break
        if not valid:
            continue
        for (u, v), (w, z) in itertools.combinations(graph.edges, 2):
            if len({u, v, w, z}) < 4:
                continue
            a, b, c, d = pos[u], pos[v], pos[w], pos[z]
            if cross(a, b, c)*cross(a, b, d) < 0 and cross(c, d, a)*cross(c, d, b) < 0:
                valid = False
                break
        if valid:
            return True, pos
    return False, None


def parity(x):
    return int(x).bit_count() & 1


def rank(columns):
    basis = {}
    for value in columns:
        x = int(value)
        while x:
            j = x.bit_length() - 1
            if j in basis:
                x ^= basis[j]
            else:
                basis[j] = x
                break
    return len(basis)


def matroid_connected(columns):
    """Finite exact connectedness check using the connectivity rank function."""
    m = len(columns)
    if m <= 1:
        return True
    r = rank(columns)
    # For this tiny verification only; no polynomial runtime is claimed here.
    for bits in range(1, 1 << (m - 1)):
        left = [columns[j] for j in range(m) if bits >> j & 1]
        right = [columns[j] for j in range(m) if not (bits >> j & 1)]
        if rank(left) + rank(right) == r:
            return False
    return True


def recover_three_connected_graph(columns, dimension):
    """Recover vertex stars of a small 3-connected graphic matroid.

    All graph knowledge comes from the column matrix, not the generator graph.
    This deliberately exponential independent check mirrors a known recognition
    characterization; it is not a substitute for the polynomial CMR algorithm.
    """
    m = len(columns)
    cocycles = sorted({sum(parity(a & c) << i for i, c in enumerate(columns))
                       for a in range(1, 1 << dimension)})
    cocycles = [c for c in cocycles if c]
    cocircuits = [c for c in cocycles if not any(d != c and d & c == d for d in cocycles)]
    stars = [c for c in cocircuits if matroid_connected(
        [v for i, v in enumerate(columns) if not (c >> i & 1)]
    )]
    graph = SmallGraph()
    graph.add_nodes_from(range(len(stars)))
    for e in range(m):
        endpoints = [j for j, c in enumerate(stars) if c >> e & 1]
        if len(endpoints) != 2:
            raise ValueError("Fixture is outside the admitted 3-connected recognition case")
        graph.add_edge(*endpoints, label=e)
    return graph, stars


def kw_partition(graph, weights):
    """Floating Kac-Ward partition function of a simple planar graph.

    weights maps undirected edges to two nonnegative parity weights. Fixtures
    use strictly positive weights. Isolated components are included.
    """
    if not graph.edges:
        return float(2 ** graph.number_of_nodes())
    planar, positions = small_planar_embedding(graph)
    if not planar:
        raise ValueError("Nonplanar graph")
    oriented = [(u, v) for u, v in graph.edges for u, v in ((u, v), (v, u))]
    edge_data = {frozenset(e): tuple(weights[frozenset(e)]) for e in graph.edges}
    matrix = np.eye(len(oriented), dtype=complex)
    for i, (u, v) in enumerate(oriented):
        start = complex(*(np.asarray(positions[v]) - np.asarray(positions[u])))
        for j, (a, b) in enumerate(oriented):
            if a != v or b == u:
                continue
            finish = complex(*(np.asarray(positions[b]) - np.asarray(positions[a])))
            theta = np.angle(finish / start)
            w0, w1 = edge_data[frozenset((a, b))]
            t = (w0 - w1) / (w0 + w1)
            matrix[i, j] -= t * np.exp(0.5j * theta)
    determinant = np.linalg.det(matrix)
    if abs(determinant.imag) > 1e-9 * max(1.0, abs(determinant.real)):
        raise ArithmeticError("Unexpected imaginary determinant")
    prefactor = 2.0 ** graph.number_of_nodes()
    for w0, w1 in edge_data.values():
        prefactor *= (w0 + w1) / 2.0
    return float(prefactor * math.sqrt(max(0.0, determinant.real)))


def enumerated_partition(graph, weights):
    nodes = list(graph.nodes)
    index = {v: j for j, v in enumerate(nodes)}
    total = 0.0
    for x in range(1 << len(nodes)):
        p = 1.0
        for u, v in graph.edges:
            p *= weights[frozenset((u, v))][((x >> index[u]) ^ (x >> index[v])) & 1]
        total += p
    return total


def hidden_planar_and_residual():
    # A wheel on five vertices is planar and 3-connected. The observer receives
    # energies in a dense, invertibly transformed four-bit coordinate system.
    generating_graph = wheel_graph(5)
    edges = list(generating_graph.edges)
    chart_rows = [0b1110, 0b1101, 0b1011, 0b0111]
    assert rank(chart_rows) == 4

    def raw_form(u, v):
        # Delete graph vertex 4, the unobservable global-spin gauge.
        return (chart_rows[u] if u < 4 else 0) ^ (chart_rows[v] if v < 4 else 0)

    support = [raw_form(u, v) for u, v in edges]
    coefficients = [0.22 + 0.03 * j for j in range(len(edges))]
    exact_energy = np.array([sum(c * (-1) ** parity(s & x)
                                 for s, c in zip(support, coefficients))
                             for x in range(16)])
    eta = 0.0002
    observed = exact_energy + eta * np.cos(np.arange(16) * math.sqrt(2.0))
    fourier = np.array([np.mean([observed[x] * (-1) ** parity(s & x)
                                for x in range(16)]) for s in range(16)])
    recovered = [s for s in range(1, 16) if abs(fourier[s]) > 0.1]
    assert set(recovered) == set(support)
    reconstructed = np.array([sum(fourier[s] * (-1) ** parity(s & x)
                                   for s in recovered) + fourier[0]
                              for x in range(16)])
    learned_graph, stars = recover_three_connected_graph(recovered, 4)
    planar, _ = small_planar_embedding(learned_graph)
    assert planar
    weights = {}
    for (u, v), data in learned_graph.edge_data.items():
        s = recovered[data['label']]
        weights[frozenset((u, v))] = (math.exp(-fourier[s]), math.exp(fourier[s]))
    z_kw = kw_partition(learned_graph, weights) / 2.0 * math.exp(-fourier[0])
    z_direct = float(np.exp(-reconstructed).sum())
    assert abs(z_kw / z_direct - 1) < 1e-11

    extra_edges = [e for e in complete_graph(5).edges if not generating_graph.has_edge(*e)]
    extra_forms = [raw_form(*e) for e in extra_edges]
    all_forms = recovered + extra_forms
    nonplanar_graph, _ = recover_three_connected_graph(all_forms, 4)
    assert not small_planar_embedding(nonplanar_graph)[0]
    # Two weak nonplanar factors. Exact rational rejection probabilities exist.
    residual_weights = np.array([np.prod([1.2 if parity(s & x) else 1.0
                                          for s in extra_forms]) for x in range(16)])
    reference = np.exp(-reconstructed)
    reference /= reference.sum()
    target = reference * residual_weights
    ratio = float(target.sum())
    target /= target.sum()
    kappa = 1.2 ** len(extra_forms)
    mean_acceptance = ratio / kappa
    assert mean_acceptance >= 1 / kappa - 1e-12
    rng = np.random.default_rng(2046)
    count = np.zeros(16, dtype=int)
    proposals = 0
    accepted = 20000
    while int(count.sum()) < accepted:
        x = int(rng.choice(16, p=reference))
        proposals += 1
        if rng.random() * kappa <= residual_weights[x]:
            count[x] += 1
    empirical_tv = float(np.abs(count / accepted - target).sum() / 2)
    return {
        'raw_dimension': 4,
        'configuration_energy_queries': 16,
        'bounded_measurement_error': eta,
        'recovered_terms': len(recovered),
        'uniform_energy_reconstruction_error': float(np.max(np.abs(reconstructed-exact_energy))),
        'learned_graph_vertices': learned_graph.number_of_nodes(),
        'learned_graph_edges': learned_graph.number_of_edges(),
        'hidden_planarity_acquired': planar,
        'generic_extra_terms_make_graph_nonplanar': True,
        'kw_relative_partition_error': float(abs(z_kw / z_direct - 1)),
        'residual_kappa_bound': kappa,
        'exact_expected_proposals_per_acceptance': 1 / mean_acceptance,
        'observed_proposals_per_acceptance': proposals / accepted,
        'accepted_samples': accepted,
        'empirical_total_variation': empirical_tv,
        'scope': 'Tiny enumerative acquisition/recognition and floating Kac-Ward mechanism check; not a production-cost claim.'
    }


def soft_evidence_reduction():
    graph = complete_graph(4)
    edges = list(graph.edges)
    n, m = graph.number_of_nodes(), graph.number_of_edges()
    totals = [0] * (1 << n)
    base_total = 0
    for x in range(1 << n):
        for z in range(1 << m):
            base_weight = 1
            likelihood_numerator = 1
            for j, (u, v) in enumerate(edges):
                s = ((x >> u) ^ (x >> v)) & 1
                ze = (z >> j) & 1
                ye = ze ^ s
                base_weight *= 2 if ye == 0 else 1
                likelihood_numerator *= 1 if ze == 0 else 2
            base_total += base_weight
            totals[x] += base_weight * likelihood_numerator
    effective = [np.prod([4 if (((x >> u) ^ (x >> v)) & 1) == 0 else 5
                           for u, v in edges], dtype=object) for x in range(1 << n)]
    assert totals == effective
    assert base_total == 2 ** n * 3 ** m
    observation_probability = sum(totals) / (2 ** n * 9 ** m)
    return {
        'vertices': n,
        'edges': m,
        'joint_states_enumerated': 2 ** (n+m),
        'base_partition': base_total,
        'base_partition_formula': 2 ** n * 3 ** m,
        'posterior_integer_partition': int(sum(totals)),
        'observation_probability': observation_probability,
        'all_spin_marginal_weights_match_4_equal_5_different': True,
        'effective_antiferromagnetic_tanh_magnitude': 1/9,
        'degree_11_tree_nonuniqueness_product': 10/9,
        'scope': 'Algebraic reduction check, not a computational-hardness experiment.'
    }


def uniform_envelope():
    # Sharpness of the total-variation envelope under arbitrary likelihood.
    t = 0.4
    small, large = math.exp(-t), math.exp(t)
    base = np.array([math.sqrt(large), math.sqrt(small)])
    base /= base.sum()
    tilted = base * np.array([small, large])
    tilted /= tilted.sum()
    tv = float(np.abs(base - tilted).sum() / 2)
    bound = math.tanh(t/2)
    assert abs(tv-bound) < 1e-14
    # Multiplying a likelihood by an arbitrarily small scalar leaves the
    # conditional model and its perturbation envelope unchanged.
    scaled = 1e-200 * base
    scaled /= scaled.sum()
    assert np.max(np.abs(scaled-base)) < 1e-14
    return {'log_weight_error_radius': t, 'total_variation': tv,
            'sharp_tanh_half_radius': bound,
            'rare_evidence_scale': 1e-200,
            'scope': 'Analytic extremizer and invariance check.'}


def main():
    result = {'soft_evidence_reduction': soft_evidence_reduction(),
              'hidden_planar_and_residual': hidden_planar_and_residual(),
              'uniform_envelope': uniform_envelope()}
    destination = Path(__file__).with_name('check_results.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
