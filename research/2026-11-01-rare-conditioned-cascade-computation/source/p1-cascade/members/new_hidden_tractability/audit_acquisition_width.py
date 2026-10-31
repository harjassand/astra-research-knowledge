"""Independent finite audits of root-owned acquisition and width construction.

Acquisition is tested against adversarial cached log-oracle errors bounded by the
proved confidence radius. Dense monotone perturbations saturate the proposed
approximate-junta tolerance. This audits the deterministic learner on its good
event, not the probability of the statistical assay event.

Width is compared with every elimination order on all graphs with <=5 vertices,
plus random six/seven-vertex graphs. Root files are imported and not modified.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import random
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'new_cascade'))
from acquire_local_rates import learn_local_scopes
from acquire_width import acquire_order, graph_from_scopes, order_width


class BoundedErrorOracle:
    def __init__(self, n, degree, rho, truth, salt, error_mode):
        self.n, self.degree, self.rho = n, degree, rho
        self.a = rho/(64*max(1, degree))
        self.truth = truth
        self.salt = salt
        self.error_mode = error_mode
        self.cache = {}
        self.max_calls = n*(2**(degree+3)+8*max(1, degree)**2*(max(1, math.ceil(math.log2(max(2, n-1))))+1))

    def log_rate(self, v, mask):
        mask &= ~(1 << v)
        key = v, mask
        if key not in self.cache:
            if self.error_mode == 0:
                sign = 1 if mask.bit_count() % 2 else -1
            elif self.error_mode == 1:
                sign = -1 if mask.bit_count() % 2 else 1
            else:
                x = ((mask+1)*0x9E3779B1 ^ (v+1)*0x85EBCA77 ^ self.salt) & 0xffffffff
                x ^= x >> 16
                sign = 1 if x & 1 else -1
            self.cache[key] = self.truth(v, mask) + sign*self.a
        return self.cache[key]


def check_acquisition():
    rng = np.random.default_rng(905237)
    fixtures = 0
    contexts = 0
    max_error = 0.0
    max_cap_fraction = 0.0
    dense_examples = 0
    for n in [2, 3, 5, 8, 12]:
        for degree in range(min(3, n-1)+1):
            for kind in ['or', 'and', 'additive', 'mixed']:
                rho = 0.4
                latent = []
                tables = []
                dense_weights = []
                b = rho/(64*max(1, degree))
                for v in range(n):
                    candidates = [u for u in range(n) if u != v]
                    parents = tuple(sorted(rng.choice(candidates, size=degree, replace=False).tolist()))
                    latent.append(parents)
                    weights = rng.uniform(0.05, 1.0, n)
                    weights[v] = 0
                    weights *= 2*b/weights.sum()
                    dense_weights.append(weights)
                    values = []
                    for local in range(1 << degree):
                        count = local.bit_count()
                        if degree == 0:
                            value = 0.0
                        elif kind == 'or':
                            value = 0.9*rho*(count > 0)
                        elif kind == 'and':
                            value = 0.9*rho*(count == degree)
                        elif kind == 'additive':
                            value = 0.9*rho*count/degree
                        else:
                            value = 0.2*rho*count/degree + 0.7*rho*(count >= max(1, degree-1))
                        values.append(value)
                    tables.append(values)

                def truth(v, mask):
                    code = sum(((mask >> u) & 1) << j for j, u in enumerate(latent[v]))
                    perturbation = sum(dense_weights[v][u] for u in range(n) if mask >> u & 1) - b
                    return tables[v][code] + perturbation

                for mode in range(3):
                    oracle = BoundedErrorOracle(n, degree, rho, truth, int(rng.integers(2**30)), mode)
                    learned, witnesses = learn_local_scopes(oracle)
                    assert len(oracle.cache) <= oracle.max_calls
                    max_cap_fraction = max(max_cap_fraction, len(oracle.cache)/oracle.max_calls)
                    for v, item in enumerate(learned):
                        assert set(item['parents']) <= set(latent[v])
                        assert len(item['parents']) <= degree
                        for mask in range(1 << n):
                            if mask >> v & 1:
                                continue
                            local = sum(((mask >> u) & 1) << j for j, u in enumerate(item['parents']))
                            estimated = math.log(float(item['table'][local]))
                            error = truth(v, mask)-estimated
                            assert error >= -1e-12
                            assert error <= rho/2+4*oracle.a+1e-12
                            max_error = max(max_error, error)
                            contexts += 1
                    for witness in witnesses:
                        assert witness['parent'] in latent[witness['node']]
                        assert witness['positive_gap_lower_bound'] > 0
                    fixtures += 1
                    dense_examples += int(n-1 > degree)
    return {'fixtures': fixtures, 'original_contexts_exhaustively_checked': contexts,
            'rho': 0.4, 'maximum_actual_log_rate_error': max_error,
            'largest_fraction_of_assay_cap_used': max_cap_fraction,
            'dense_exact_dependency_fixtures': dense_examples,
            'bounded_error_modes': ['alternating parity', 'opposite parity', 'deterministic signed hash'],
            'latent_monotone_families': ['OR', 'AND', 'additive', 'mixed threshold'],
            'all_learned_scopes_subset_of_latent_scopes': True,
            'all_models_one_sided_and_uniformly_accurate': True,
            'scope': 'Deterministic acquisition on simultaneous confidence event; no statistical success-probability claim from these checks.'}


def check_width():
    tested = 0
    max_states = 0
    width_histogram = {}
    for n in range(1, 6):
        possible = list(itertools.combinations(range(n), 2))
        orders = list(itertools.permutations(range(n)))
        for code in range(1 << len(possible)):
            scopes = [possible[i] for i in range(len(possible)) if code >> i & 1]
            graph = graph_from_scopes(scopes, n)
            optimal = min(order_width(graph, order) for order in orders)
            order, found, counts = acquire_order(scopes, n)
            assert found == optimal
            assert sorted(order) == list(range(n))
            if found:
                try:
                    acquire_order(scopes, n, max_width=found-1)
                except ValueError:
                    pass
                else:
                    raise AssertionError('Width cap should have rejected this graph')
            max_states = max(max_states, max(item['states'] for item in counts))
            width_histogram[str(found)] = width_histogram.get(str(found), 0)+1
            tested += 1
    rng = random.Random(83051)
    larger = 0
    for n, repetitions in [(6, 24), (7, 12)]:
        possible = list(itertools.combinations(range(n), 2))
        for _ in range(repetitions):
            p = rng.uniform(0.1, 0.9)
            scopes = [edge for edge in possible if rng.random() < p]
            graph = graph_from_scopes(scopes, n)
            optimal = min(order_width(graph, order) for order in itertools.permutations(range(n)))
            _, found, counts = acquire_order(scopes, n)
            assert found == optimal
            max_states = max(max_states, max(item['states'] for item in counts))
            larger += 1
    return {'all_graphs_up_to_vertices': 5, 'exhaustive_graphs': tested,
            'additional_six_seven_vertex_graphs': larger,
            'all_compared_against_every_elimination_order': True,
            'all_returned_widths_optimal': True,
            'exhaustive_graph_width_histogram': width_histogram,
            'maximum_memoized_states_in_one_width_search': max_states}


def main():
    result = {'approximate_junta_acquisition': check_acquisition(),
              'complete_width_search': check_width()}
    Path(__file__).with_name('acquisition_width_audit_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
