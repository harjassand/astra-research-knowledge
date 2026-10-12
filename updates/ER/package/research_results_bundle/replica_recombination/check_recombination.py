#!/usr/bin/env python3
"""Exact audit of sitewise three-replica binary-spin recombination.
No Monte Carlo, external data, network calls, or third-party dependencies.
Run: python3 check_recombination.py [output_json]
"""
from itertools import product
from math import exp, log, comb
import json, random, sys


def energy(replicas, edges, fields):
    return -sum(J * sum(row[i] * row[j] for row in replicas)
                for i, j, J in edges) - sum(h * sum(row[i] for row in replicas)
                                          for i, h in enumerate(fields))


def decompose(replicas, edges, fields):
    n = len(replicas[0])
    mixed = [i for i in range(n) if abs(sum(row[i] for row in replicas)) == 1]
    mixed_set = set(mixed)
    s = [1 if sum(row[i] for row in replicas) > 0 else -1 for i in range(n)]
    # Energy constant: unary fields, all edges touching a unanimous vertex,
    # and +J*s_i*s_j for mixed-mixed edges.
    const = -sum(h * sum(row[i] for row in replicas) for i,h in enumerate(fields))
    effective_edges = []
    for i,j,J in edges:
        if i in mixed_set and j in mixed_set:
            const += J*s[i]*s[j]
            effective_edges.append((i,j,4*J*s[i]*s[j]))
        else:
            const -= J*sum(row[i]*row[j] for row in replicas)
    return mixed, s, const, effective_edges


def exact_check(seed=20261012):
    rng = random.Random(seed)
    n = 8
    # A 2x4 lattice, signed integer edge weights and local fields.
    edges = [(i, i+1, rng.choice([-2,-1,1,2])) for i in range(7) if i != 3]
    edges += [(i, i+4, rng.choice([-2,-1,1,2])) for i in range(4)]
    fields = [rng.choice([-1,0,1]) for _ in range(n)]
    replicas = [[rng.choice([-1,1]) for _ in range(n)] for _ in range(3)]
    mixed, s, const, effective_edges = decompose(replicas, edges, fields)
    direct, reduced, preserve = [], [], True
    for colors in product(range(3), repeat=len(mixed)):
        c = dict(zip(mixed, colors))
        out = [row[:] for row in replicas]
        for i in mixed:
            for a in range(3):
                out[a][i] = s[i] * (1-2*(a == c[i]))
        preserve &= all(sorted(row[i] for row in out) == sorted(row[i] for row in replicas)
                        for i in range(n))
        direct.append(energy(out, edges, fields))
        reduced.append(const - sum(K*(c[i]==c[j]) for i,j,K in effective_edges))
    beta = .73
    e0 = min(direct)
    w1 = [exp(-beta*(e-e0)) for e in direct]
    w2 = [exp(-beta*(e-e0)) for e in reduced]
    z1,z2 = sum(w1),sum(w2)
    p1,p2 = [v/z1 for v in w1],[v/z2 for v in w2]
    return {
        'seed':seed, 'n_vertices':n, 'n_edges':len(edges), 'mixed_vertices':mixed,
        'enumerated_unique_recombinations':len(direct), 'replicas':replicas,
        'edges':edges, 'fields':fields, 'energy_constant':const,
        'max_absolute_energy_identity_error':max(abs(a-b) for a,b in zip(direct,reduced)),
        'max_absolute_probability_error':max(abs(a-b) for a,b in zip(p1,p2)),
        'sitewise_multisets_preserved':preserve,
    }


def antiferromagnetic_coloring_check(n, pairs):
    # At every vertex the multiset is {+1,+1,-1}; all J=-1.
    # E_total = -|E| + 4*(number of monochromatic edges).
    edges=[(i,j,-1) for i,j in pairs]
    initial=[[1]*n,[1]*n,[-1]*n]
    values=[]
    for colors in product(range(3), repeat=n):
        out=[[1-2*(a==colors[i]) for i in range(n)] for a in range(3)]
        mono=sum(colors[i]==colors[j] for i,j in pairs)
        E=energy(out,edges,[0]*n)
        assert E == -len(pairs)+4*mono
        values.append((E,mono))
    Emin=min(E for E,_ in values)
    return {'n_vertices':n,'n_edges':len(pairs),'number_assignments':len(values),
            'minimum_total_energy':Emin,'minimum_monochromatic_edges':min(m for _,m in values),
            'number_ground_assignments':sum(E==Emin for E,_ in values),
            'proper_three_colorable':Emin==-len(pairs)}


def outputs():
    result={
      'identity_test': exact_check(),
      'coloring_examples': {
        'triangle': antiferromagnetic_coloring_check(3,[(0,1),(1,2),(0,2)]),
        'K4': antiferromagnetic_coloring_check(4,[(i,j) for i in range(4) for j in range(i+1,4)]),
      },
      'independent_unbiased_replica_site_statistics': [
        {'replicas':m,'mixed_site_probability':1-2**(1-m),
         'largest_site_assignment_alphabet':comb(m,m//2)} for m in range(2,11)],
      'synchronized_replicas': {
        'n_vertices':1000000,'unique_recombinations':1,
        'reason':'Every site has a unanimous multiset; permutations change no spin.'},
      'conclusion':'Identity verified; no demonstrated scaling breakthrough. Conditional recombination retains a frustrated Potts problem.'
    }
    return result

if __name__=='__main__':
    text=json.dumps(outputs(),indent=2)
    print(text)
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as f: f.write(text+'\n')
