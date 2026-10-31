#!/usr/bin/env python3
"""Finite structural regression; none of these finite checks replace the proof."""
from itertools import combinations
import json
from exact_terminal_gap import compile_cones, verify_certificate, cycle

C=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
counts={'binary_single_linkage_subsets':0,'exact_bases_total':0}
for size in range(2,len(C)+1):
    for subset in combinations(C,size):
        raw=cycle(list(subset));cert=compile_cones(raw)
        assert cert['accepted'],subset
        assert verify_certificate(raw,cert),subset
        counts['binary_single_linkage_subsets']+=1
        counts['exact_bases_total']+=cert['exact_basis_candidates_tested']
# The two-linkage obstruction remains a genuine rejection under graph reorderings.
raw=[((0,0),(1,0)),((1,0),(0,0)),((2,0),(1,1)),((1,1),(2,0))]
for reordered in [raw,raw[::-1],[(s[::-1],t[::-1]) for s,t in raw]]:
    assert not compile_cones(reordered)['accepted']
counts['reordered_obstruction_rejections']=3
counts['finite_checks_not_general_proof']=True
print(json.dumps(counts,indent=2))
