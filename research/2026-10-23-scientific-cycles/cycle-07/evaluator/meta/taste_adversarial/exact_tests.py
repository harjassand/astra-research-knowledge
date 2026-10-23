#!/usr/bin/env python3
"""Exact bounded semantic tests of proof-cost accounting and lemma utility.

Standard library only; no owner scientific sources imported or executed.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from heapq import heappop, heappush
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time


def expansion_case(m: int, shared_cost: int = 20) -> dict:
    """All legal frontier walks, compressed by identical frontier states.

    remaining Ai nodes are encoded in a bitmask. The shared lemma L may be
    reintroduced by another Ai after an earlier expansion. Primitive p is
    inert. Count costs beyond T's one source proof line.
    """
    @lru_cache(None)
    def costs(mask: int, has_l: bool, has_p: bool):
        if mask == 0 and not has_l:
            assert has_p
            return {0: 1}
        total = Counter()
        for i in range(m):
            if mask & (1 << i):
                for c, n in costs(mask ^ (1 << i), True, has_p).items():
                    total[c + 1] += n
        if has_l:
            for c, n in costs(mask, False, True).items():
                total[c + shared_cost] += n
        return dict(total)

    found = {c + 1: n for c, n in costs((1 << m) - 1, False, False).items()}
    expected = {1 + m + shared_cost * r for r in range(1, m + 1)}
    assert set(found) == expected
    unique_dag = 1 + m + shared_cost
    minimum = min(found)
    maximum = max(found)
    assert minimum == unique_dag
    assert maximum == 1 + m + m * shared_cost
    return {
        "m": m,
        "shared_lemma_cost": shared_cost,
        "same_target": "T",
        "same_final_premises": ["p"],
        "terminal_label_schedule_counts": {str(k): found[k] for k in sorted(found)},
        "total_legal_schedules": sum(found.values()),
        "minimum_label": minimum,
        "maximum_label": maximum,
        "memoized_dependency_DAG_cost": unique_dag,
        "minimum_schedule": [f"A{i}" for i in range(m)] + ["L"],
        "maximum_schedule": [x for i in range(m) for x in (f"A{i}", "L")],
        "dynamic_program_states": costs.cache_info().currsize,
    }


def shortest_dag(rules, initial, targets):
    """Exact minimum positive-cost rule applications with shared derived facts.

    Each rule = (tuple antecedents, consequent, positive integer cost).
    Any rule with an already-derived consequent can be omitted. Enumerating
    states therefore includes all relevant proof DAGs for these finite systems.
    """
    initial = frozenset(initial)
    targets = frozenset(targets)
    dist = {initial: 0}
    queue = [(0, tuple(sorted(initial)))]
    while queue:
        value, key = heappop(queue)
        state = frozenset(key)
        if dist[state] != value:
            continue
        if targets <= state:
            return value
        for antecedents, consequent, weight in rules:
            assert weight > 0
            if consequent in state or not set(antecedents) <= state:
                continue
            child = state | {consequent}
            cand = value + weight
            if cand < dist.get(child, float("inf")):
                dist[child] = cand
                heappush(queue, (cand, tuple(sorted(child))))
    raise ValueError("Unprovable target set")


def utility_case(kind):
    rules = [(('p',), 'A', 4), (('p',), 'B', 4), (('p',), 'T', 5)]
    if kind == "complementary":
        rules += [(('A', 'B'), 'T', 1)]
    elif kind == "substitutable":
        rules += [(('A',), 'T', 1), (('B',), 'T', 1)]
    else:
        raise ValueError(kind)
    values = {}
    for subset in [(), ('A',), ('B',), ('A', 'B')]:
        values['+'.join(subset) or 'empty'] = shortest_dag(rules, ('p', *subset), ('T',))
    base = values['empty']
    savings = {key: base - val for key, val in values.items()}
    lhs = savings['A'] + savings['B']
    rhs = savings['empty'] + savings['A+B']
    if kind == 'complementary':
        assert values == {'empty': 5, 'A': 5, 'B': 5, 'A+B': 1}
        assert lhs < rhs  # Violates submodularity.
    else:
        assert values == {'empty': 5, 'A': 1, 'B': 1, 'A+B': 1}
        assert lhs > rhs  # Violates supermodularity.
    return {'kind': kind, 'rules': rules, 'shortest_shared_DAG_cost': values,
            'savings': savings, 'submodularity_lhs': lhs, 'submodularity_rhs': rhs}


def acquisition_control(n):
    rules = [(('p',), 'A', 4), (('p',), 'B', 4)]
    for i in range(n):
        rules.extend([(('p',), f'T{i}', 5), (('A', 'B'), f'T{i}', 1)])
    targets = tuple(f'T{i}' for i in range(n))
    actual_optimal = shortest_dag(rules, ('p',), targets)
    acquired = shortest_dag(rules, ('p',), ('A','B'))
    continuation = shortest_dag(rules, ('p', 'A', 'B'), targets)
    proposed = acquired + continuation
    naive_repeated_direct = 5*n
    assert actual_optimal == min(5*n, 8+n)
    assert proposed == 8+n
    assert actual_optimal <= proposed
    return {'targets': n, 'optional_lemma_acquisition_cost': acquired,
            'continuation_given_both': continuation,
            'total_if_acquire_both_first': proposed,
            'strong_conventional_global_shared_DAG_cost': actual_optimal,
            'weak_repeated_direct_proof_cost': naive_repeated_direct,
            'advantage_over_strong_control': actual_optimal-proposed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('EXACT_RESULTS.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    results = {
        'scope': 'Exact synthetic semantic countermodels, not measurements of the paper models, mathlib, or Astra research outcomes.',
        'expansion': [expansion_case(m) for m in (2, 4, 8)],
        'utility': [utility_case('complementary'), utility_case('substitutable')],
        'acquisition_control': [acquisition_control(n) for n in (1, 2, 3, 5)],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True)+'\n')
    receipt = {'status': 'PASS', 'wall_seconds': time.perf_counter()-start,
               'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'cost_scope': 'Executed finite analysis only; authoring, reasoning and source review are unmetered.'}
    args.output.with_name('EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
