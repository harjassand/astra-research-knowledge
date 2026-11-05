#!/usr/bin/env python3
"""Exact finite ingredients of the one-logical-qubit comparator counterexample.

This is not a BDL matrix, decoder, memory, or obstruction for that family.
The direct-sum defect argument is proved in the accompanying selection brief.
"""
from collections import Counter
from pathlib import Path
import json


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def verify():
    rows = tuple(range(1, 8))
    syndromes = [tuple((r & x).bit_count() % 2 for r in rows)
                 for x in range(8)]
    relations = []
    for mask in range(1 << 7):
        xor = 0
        for j, row in enumerate(rows):
            if (mask >> j) & 1:
                xor ^= row
        if xor == 0:
            relations.append(mask)
    syndrome_weights = Counter(map(sum, syndromes))
    relation_weights = Counter(x.bit_count() for x in relations)
    assert syndrome_weights == {0: 1, 4: 7}
    assert relation_weights == {0: 1, 3: 7, 4: 7, 7: 1}
    assert len(set(syndromes)) == 8 and len(relations) == 16

    # A connected simple graph of incidence rank r has r+1 vertices.
    # Sum the maximal edge counts over every possible component-rank split.
    simple_bound = max(sum(r * (r + 1) // 2 for r in p)
                       for p in partitions(3))
    bipartite_bound = max(sum((r + 1) ** 2 // 4 for r in p)
                          for p in partitions(4))
    assert simple_bound == bipartite_bound == 6 < len(rows)

    xor_diagnostics = []
    for depth in range(1, 13):
        leaves = [0] * (1 << depth)
        leaves[0] = leaves[len(leaves) // 2] = 1
        levels = [leaves]
        while len(levels[-1]) > 1:
            x = levels[-1]
            levels.append([x[i] ^ x[i + 1] for i in range(0, len(x), 2)])
        assert levels[-1] == [0]
        assert sum(map(sum, levels)) == 2 * depth
        xor_diagnostics.append({'depth': depth, 'physical_defects': 2,
                                'nonzero_history_variables': 2 * depth})
    return {
        'status': 'all exact integer checks passed',
        'scope': 'synthetic counterexamples only; no conclusion about BDL regularity',
        'check_rows_as_binary_integers': rows,
        'syndrome_weight_enumerator': dict(sorted(syndrome_weights.items())),
        'relation_weight_enumerator': dict(sorted(relation_weights.items())),
        'maximum_simple_graph_edges_at_rank_3': simple_bound,
        'maximum_simple_bipartite_graph_edges_at_rank_4': bipartite_bound,
        'xor_history_failure_of_uniform_energy_coercivity': xor_diagnostics,
    }


if __name__ == '__main__':
    result = verify()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
