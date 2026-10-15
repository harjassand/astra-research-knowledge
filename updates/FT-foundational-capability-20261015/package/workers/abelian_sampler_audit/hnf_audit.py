"""Exhaustive tiny subgroup check of the worker's HNF adapter against closure."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().parent.parent / 'capital_routes/n610_ring_sampler.py'
spec = importlib.util.spec_from_file_location('audited_ring_sampler', SOURCE)
worker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = worker
spec.loader.exec_module(worker)


def plus(v, w, modulus):
    return tuple((a+b) % modulus for a, b in zip(v, w))


def closure_add(group, generator, modulus):
    return {plus(v, tuple(a*x % modulus for x in generator), modulus)
            for v in group for a in range(modulus)}


def run():
    rng = random.Random(1710610)
    queries = 0
    cases = 0
    for modulus, dimension in [(m, 2) for m in (4, 6, 8, 12)] + [(4, 3)]:
        all_vectors = tuple(product(range(modulus), repeat=dimension))
        for _ in range(8):
            h = worker.Subgroup(modulus, dimension)
            group = {(0,)*dimension}
            for _ in range(4):
                generator = tuple(rng.randrange(modulus) for _ in range(dimension))
                h.add_image(generator)
                group = closure_add(group, generator, modulus)
                for vector in all_vectors:
                    assert h.contains(vector) == (vector in group)
                    queries += 1
                pushed = Counter()
                for vector in all_vectors:
                    y = tuple(sum(int(h.B[i, j])*vector[j] for j in range(dimension)) % modulus
                              for i in range(dimension))
                    pushed[y] += 1
                assert set(pushed) == group
                assert len(set(pushed.values())) == 1
                cases += 1
    result = {'worker_source': str(SOURCE),
              'worker_source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'group_extension_cases': cases, 'membership_comparisons': queries,
              'membership_mismatches': 0, 'uniform_pushforward_mismatches': 0,
              'scope': 'tiny exact modular subgroup adapter checks, not sampler or complexity proof'}
    Path(__file__).with_name('hnf_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    access = Counter()
    n = 1_000_000

    def parents(site):
        access['parent_descriptor_calls'] += 1
        return ((site+1) % n,)

    def coefficients(site, layer):
        access['coefficient_descriptor_calls'] += 1
        return (2,)

    def residual(site):
        access['residual_descriptor_calls'] += 1
        return (1, 2)

    def forcing(site, layer, lower):
        access['forcing_calls'] += 1
        return 1 if layer == 0 else lower[0][0]**2+1

    model = worker.ModularModel(n, 2, 4, Fraction(1, 3), Fraction(1, 3),
                                parents, coefficients, forcing, residual)
    values, counters = worker.sample_coordinates(
        model, [(1234, 0, 1), (9999, 0, 0)], random.Random(5), diagnostics=True)
    assert access['parent_descriptor_calls'] == counters['parent_lookups']
    assert access['coefficient_descriptor_calls'] == counters['parent_lookups']
    assert access['forcing_calls'] == counters['forcing_calls']
    assert access['parent_descriptor_calls'] > 0
    assert access['parent_descriptor_calls'] < 50
    oracle_result = {'worker_source_sha256': result['worker_source_sha256'],
                     'n': n, 'model_representation': 'local callables; no N-sized arrays',
                     'targets': [[1234, 0, 1], [9999, 0, 0]], 'output': values,
                     'actual_descriptor_counts': dict(access), 'diagnostics': counters,
                     'duplicate_parent_query_fixed': True,
                     'scope': 'single instrumented local-access execution and source review; no scaling theorem from one run'}
    Path(__file__).with_name('on_access_results.json').write_text(json.dumps(oracle_result, indent=2)+'\n')
    print(json.dumps(oracle_result, indent=2))


if __name__ == '__main__':
    run()
