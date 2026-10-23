#!/usr/bin/env python3
"""Bounded exact implementation admission; no probability estimation."""
import importlib.util
import json
import sys
from pathlib import Path

source = Path(__file__).with_name('colored_search.py')
spec = importlib.util.spec_from_file_location('colored_search_audit_module', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
pattern = [True, False, False, True, True, False, True, False] * 4
records = []
for n in (1, 2, 3, 9):
    tree, flat = module.IntegerWeights(n), [1] * n
    for step, answer in enumerate(pattern, 1):
        total, cumulative = sum(flat), 0
        for h, weight in enumerate(flat):
            if 2 * (cumulative + weight) >= total:
                break
            cumulative += weight
        assert tree.median() == (h, weight, cumulative)
        for t in range(n):
            if t < h:
                flat[t] *= 2 if answer else 4
            elif t > h:
                flat[t] *= 4 if answer else 2
            else:
                flat[t] = (4 * weight - (total - 2 * cumulative) if answer else
                           4 * weight - (2 * (cumulative + weight) - total))
        tree.update(h, weight, cumulative, answer)
        def leaves(node):
            if node.hi - node.lo == 1:
                return [node.total]
            node.push()
            return leaves(node.left) + leaves(node.right)
        assert leaves(tree.root) == flat
        assert sum(flat) == n * 3**step
    records.append({'atoms': n, 'steps': len(pattern),
                    'final_total': sum(flat), 'PASS': True})
print(json.dumps({'scope': '128 fixed-path exact tree-vs-flat transitions only; '
                  'not a probabilistic/theorem test', 'cases': records,
                  'PASS': True}, indent=2))
