#!/usr/bin/env python3
"""Independent exact audit of heterogeneous rank-budget acquisition."""
from itertools import combinations, product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_orbit_root'))
import orbit_phase_compiler as oc
import heterogeneous_orbit_compiler as hc
from orbit_rounding_audit import direct_projection, input_optimum


def hidden_model(sizes, profile, errors, rng):
    n = sum(sizes)
    starts = hc.offsets(sizes)
    groups = {d: list(oc.general_linear(d)) for d in set(sizes)}
    type_starts = {}
    rank_budget = 0
    for d, count in sorted(profile.items()):
        for t in range(count):
            type_starts[d,t] = rank_budget
            rank_budget += d
    types = [None] * len(sizes)
    for d in sorted(profile):
        ids = [a for a, size in enumerate(sizes) if size == d]
        labels = [a % profile[d] for a in range(len(ids))]
        rng.shuffle(labels)
        for a, label in zip(ids, labels):
            types[a] = (d,label)
    scalar_types = [type_starts[types[a]]+u for a, d in enumerate(sizes) for u in range(d)]
    K = [0] * rank_budget
    for i in range(rank_budget):
        for j in range(i, rank_budget):
            if rng.randrange(2):
                K[i] |= 1 << j
                K[j] |= 1 << i
    D = [sum(((K[scalar_types[i]] >> scalar_types[j]) & 1) << j for j in range(n))
         for i in range(n)]
    S = [0] * n
    pairs = list(combinations(range(len(sizes)), 2))
    rng.shuffle(pairs)
    for a, z in pairs[:errors]:
        noise = [rng.randrange(1 << sizes[z]) for _ in range(sizes[a])]
        if not any(noise):
            noise[0] = 1
        for u, row in enumerate(noise):
            for v in range(sizes[z]):
                if row >> v & 1:
                    S[starts[a]+u] ^= 1 << (starts[z]+v)
                    S[starts[z]+v] ^= 1 << (starts[a]+u)
    B = [x ^ y for x, y in zip(D, S)]
    for a, d in enumerate(sizes):
        for i in range(starts[a], starts[a+1]):
            B[i] &= ~(((1 << d)-1) << starts[a])
        for u in range(d):
            for v in range(u+1, d):
                if rng.randrange(2):
                    B[starts[a]+u] ^= 1 << (starts[a]+v)
                    B[starts[a]+v] ^= 1 << (starts[a]+u)
    G = [row << starts[a] for a, d in enumerate(sizes) for row in rng.choice(groups[d])]
    raw, ideal = oc.congruence(B, G), oc.congruence(D, G)
    E = sum(oc.rank([(S[i] >> starts[z]) & ((1 << sizes[z])-1)
                    for i in range(starts[a], starts[a+1])])
            for a in range(len(sizes)) for z in range(a+1, len(sizes)))
    T = sum(hc.distance(raw[starts[a]:starts[a+1]], ideal[starts[a]:starts[a+1]], sizes, starts)
            for a in range(len(sizes)))
    assert T <= 2*E+n
    return raw, rank_budget, E, T, groups


def audit_budget(rng):
    fixtures = []
    exact_budget_checks = 0
    for sizes, profile in [([1,2,1,2], {1:1,2:1}),
                           ([1,2,3,1,2,3], {1:1,2:1,3:1}),
                           ([2,3,2,3,2], {2:2,3:1}),
                           ([3,1,3,2,1,2], {1:1,2:1,3:2})]:
        for errors in (0, 2, 5):
            B, budget, E, T, groups = hidden_model(sizes, profile, errors, rng)
            got = hc.acquire_budget(B, sizes, budget)
            choices = list(got['profile_costs'].items())
            possibilities = [(0,0)]
            for d, options in choices:
                possibilities = [(r+int(d)*int(c), v+cost) for r,v in possibilities
                                 for c,cost in options.items()]
            expected = min(v for r,v in possibilities if r <= budget)
            assert got['objective'] == expected <= 10*T
            assert got['rank_budget'] <= budget
            assert got['residual_edges'] <= 15*max(sizes)**2*(2*E+len(B))
            labels = [None] * len(B)
            for label, cls in enumerate(got['scalar_classes']):
                for i in cls:
                    labels[i] = label
            assert direct_projection(got['transformed_matrix'], labels) == got['low_rank_matrix']
            # Compare against exact optimal observed medoids, not local-search witnesses.
            starts = hc.offsets(sizes)
            exact_profiles = [(0,0)]
            for d in sorted(set(sizes)):
                ids = [a for a, size in enumerate(sizes) if size == d]
                distances = [[hc.orbit(B[starts[a]:starts[a+1]], B[starts[z]:starts[z+1]],
                                      sizes, starts, groups[d])[0] for z in ids] for a in ids]
                optima = [(d*c, input_optimum(distances, c)) for c in range(1,len(ids)+1)]
                exact_profiles = [(r+s,v+w) for r,v in exact_profiles for s,w in optima]
            true_optimum = min(v for r,v in exact_profiles if r <= budget)
            assert got['objective'] <= 5*true_optimum <= 10*T
            fixtures.append(dict(sizes=sizes, hidden_profile=profile, budget=budget,
                                 error_rank=E, hidden_row_cost=T, dp_cost=got['objective'],
                                 exact_data_profile_optimum=true_optimum,
                                 acquired_profile=got['acquired_profile'], rank=got['low_rank'],
                                 residual_edges=got['residual_edges']))
            exact_budget_checks += 1
    # All budgets for one instance verify at-most semantics and inaccessible states.
    sizes = [1,2,1,2,3]
    B, _, _, _, _ = hidden_model(sizes, {1:1,2:1,3:1}, 4, rng)
    previous = None
    budget_costs = []
    for budget in range(sum(set(sizes)), sum(sizes)+1):
        got = hc.acquire_budget(B, sizes, budget)
        if previous is not None:
            assert got['objective'] <= previous
        previous = got['objective']
        budget_costs.append([budget, got['objective'], got['selected_profile_weight']])
    assert previous == 0
    return dict(fixtures=fixtures, exact_budget_checks=exact_budget_checks, all_budget_costs=budget_costs)


def audit_raw(rng):
    indecomposable5 = {7, 1 | (1 << 3) | (1 << 4)}
    indecomposable6 = {(1 << 0) | (1 << 1) | (1 << 5),
                      (1 << 0) | (1 << 2) | (1 << 4),
                      (1 << 1) | (1 << 2) | (1 << 3)}
    fixtures = []
    pointwise = 0
    for sizes, blocks, budget in (([5,3,3], [indecomposable5,{7},{7}], 8),
                                   ([3,6,3], [{7},indecomposable6,{7}], 9)):
        starts = hc.offsets(sizes)
        n = sum(sizes)
        p = {term << starts[a] for a, block in enumerate(blocks) for term in block}
        for i,j in combinations(range(n),2):
            if rng.randrange(2):
                p.symmetric_difference_update({(1 << i) | (1 << j)})
        p.symmetric_difference_update({0, 1, 1 << (n-1)})
        raw = oc.substitute(p, n, oc.random_invertible(n,rng), rng.randrange(1 << n))
        got = hc.acquire_raw(raw, n, budget)
        assert sorted(got['block_sizes']) == sorted(sizes)
        final = set(got['final_polynomial'])
        for y in range(1 << n):
            assert oc.phase(raw, oc.apply(got['full_coordinate_columns'], y)) == oc.phase(final,y)
            pointwise += 1
        actual = oc.truth_sum(raw,n)
        reconstructed, _ = oc.exact_reconstruct(got)
        assert actual == reconstructed == oc.truth_sum(p,n)
        fixtures.append(dict(n=n, blocks=got['block_sizes'], acquired_profile=got['acquired_profile'],
                             rank=got['low_rank'], residual_edges=got['residual_edges'], exact_sum=actual))
    return dict(fixtures=fixtures, pointwise_checks=pointwise, exact_reconstructions=len(fixtures))


def audit_rejections():
    calls = [lambda: hc.acquire_budget([],[],0),
             lambda: hc.acquire_budget([0],[0,1],1),
             lambda: hc.acquire_budget([0,0],[1],1),
             lambda: hc.acquire_budget([4,0],[1,1],1),
             lambda: hc.acquire_budget([-1,0],[1,1],1),
             lambda: hc.acquire_budget([1,0],[1,1],1),
             lambda: hc.acquire_budget([2,0],[1,1],1),
             lambda: hc.acquire_budget([0,0],[1,1],0),
             lambda: hc.acquire_budget([0,0],[1,1],3),
             lambda: hc.acquire_raw({-1},3,3),
             lambda: hc.acquire_raw({0},0,0),
             lambda: hc.acquire_raw({15},4,4),
             lambda: hc.acquire_raw({8},3,3),
             lambda: hc.acquire_raw({1},3,3)]
    for call in calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError('Expected malformed input rejection')
    return len(calls)


def main():
    rng = random.Random(2026102712)
    out = dict(budget=audit_budget(rng), raw=audit_raw(rng), malformed_rejections=audit_rejections(),
               status='All exact heterogeneous assertions passed; exhaustive finite count backend only.')
    Path(__file__).with_name('heterogeneous_orbit_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
