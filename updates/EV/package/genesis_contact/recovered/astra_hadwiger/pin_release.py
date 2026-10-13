"""Exact matching pin-release operation and exhaustive small-state checks.

This is a matching resampling-oracle construction, not a new general local lemma.
It maps a uniform matching conditioned to contain specified disjoint edges back
into a uniform unconditioned matching. It can create new matching edges only
incident to the original pin support. No convergence is asserted outside an
applicable algorithmic local-lemma theorem.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from pathlib import Path
import json
from finite_checks import matchings

Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def canonical(matching):
    return tuple(sorted(tuple(sorted(e)) for e in matching))


def release(matching: Matching, pins: Matching, choices: tuple[int, ...]) -> Matching:
    if len(pins) != len(choices):
        raise ValueError('Supply one choice per pinned edge.')
    m = dict()
    for a,b in matching:
        if a in m or b in m or a == b:
            raise ValueError('Input edges must be a matching without loops.')
        m[a], m[b] = b,a
    if any(m.get(a) != b for a,b in pins):
        raise ValueError('All pins must occur in the input matching.')
    support = [v for edge in pins for v in edge]
    if len(set(support)) != len(support):
        raise ValueError('Pins must be pairwise vertex-disjoint.')
    for i, ((a,b), x) in enumerate(zip(pins, choices)):
        frozen = {v for e in pins[i+1:] for v in e}
        if x not in m or x == a or x in frozen:
            raise ValueError('Choice is outside the current free vertex set.')
        if x == b:
            continue
        y = m[x]
        assert m[a] == b and y not in frozen
        m[a],m[x],m[b],m[y] = x,a,y,b
    return canonical((a,b) for a,b in m.items() if a < b)


def exhaustive_check(n: int, pins: Matching):
    all_matchings = [canonical(m) for m in matchings(tuple(range(n)))]
    conditional = [m for m in all_matchings if set(canonical(pins)) <= set(m)]
    choices = []
    for i,(a,b) in enumerate(pins):
        frozen = {v for e in pins[i+1:] for v in e}
        choices.append([x for x in range(n) if x != a and x not in frozen])
    counts = Counter()
    support = {v for e in pins for v in e}
    for m in conditional:
        for decision in product(*choices):
            result = release(m, pins, decision)
            counts[result] += 1
            for edge in set(result) - set(m):
                assert set(edge) & support, 'Locality failed'
    assert set(counts) == set(all_matchings)
    assert set(counts.values()) == {1}, 'Exact uniform bijection failed'
    return dict(n=n, pins=pins, conditional_states=len(conditional),
                choice_set_sizes=[len(c) for c in choices],
                output_states=len(counts), preimages_per_output=1,
                locality_verified=True)

if __name__ == '__main__':
    results = [exhaustive_check(n, tuple((2*j,2*j+1) for j in range(k)))
               for n in (4,6,8,10) for k in range(1,min(n//2,3)+1)]
    path = Path(__file__).with_name('pin_release_checks.json')
    path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results[-3:], indent=2))
