#!/usr/bin/env python3
"""Bounded stdlib checks accompanying the written incidence/link proof.

This does not enumerate or acquire the astronomical N06 incidence instance.
Run: python exact_checks.py --output results.json
"""
from collections import defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
import argparse
import json
import time


def exact_parameters():
    exponent = 521
    assert all(exponent % d for d in range(2, isqrt(exponent) + 1))
    q = (1 << exponent) - 1
    residue, residues = 4, []
    for _ in range(exponent - 2):
        residue = (residue * residue - 2) % q
        residues.append(residue)
    assert residue == 0
    h, cden, r = 20, 100**20, 10**42
    m, size_s = q**h, q // 100
    M0 = size_s**h
    J = (m - 1) // (q - 1)
    checks = {
        'q_gt_r': q > r,
        'q_ge_4000': q >= 4000,
        'cm_ge_4': m >= 4*cden,
        'M0_ge_cm_over_2': 2*M0*cden >= m,
        'M0_minus_1_ge_cm_over_4': 4*(M0-1)*cden >= m,
        'J_le_2_q19': J <= 2*q**19,
        'mean_min_ge_cq_over_8': 8*cden*(M0-1) >= q*J,
        'cq_over_8_ge_8r2': q >= 64*r*r*cden,
        'six_q14_le_m_over_4r': 24*r <= q**6,
        'six_q13_le_cm_over_4': 24*cden <= q**7,
        'interpolation_degree_lt_q_minus_1': 2*h*(size_s-1) < q-1,
        'c_times_r_equals_100': r == 100*cden,
    }
    # B <= m/(4r), C <= q^13; this also implies the source's looser C gate.
    p_reject = Fraction(128*r*cden+5, q)
    checks['rejection_lt_half'] = p_reject < Fraction(1, 2)
    checks['rejection_lt_2e_minus_73'] = p_reject < Fraction(2, 10**73)
    checks['C_q13_gate_implies_source_gate'] = 24*r*q*q**13 <= m
    delta_coefficient = Fraction(r,16*cden)-2-Fraction(1,2)
    checks['Delta_ge_15m_over_4'] = delta_coefficient == Fraction(15,4)
    assert all(checks.values()), checks
    return {
        'checks': checks,
        'q': str(q), 'q_bits': q.bit_length(), 'r': str(r), 'h': h,
        'c': '1/'+str(cden),
        'lucas_lehmer': {
            'prime_exponent_trial_division': True, 'iterations': exponent-2,
            'final_residue': residue,
            'hex_residues_newline_sha256': sha256(('\n'.join(format(s,'x') for s in residues)+'\n').encode()).hexdigest(),
        },
        'rejection_bound_exact': [str(p_reject.numerator), str(p_reject.denominator)],
        'rejection_bound_decimal_approximation': format(float(p_reject), '.12e'),
        'decimal_digit_counts': {
            name: len(str(n)) for name,n in {
                'q': q, 'm':m, 'M0':M0, 'initial_incidences':M0*(q-1),
                'x_edge_upper':M0*r*r, 'triangle_upper':M0*(q-1)*r*r,
            }.items()
        },
        'instance_materialized': False,
    }


def cartesian_checks():
    cases = 0
    for r in range(2, 41):
        # Check every residue at the lower endpoint and much farther away.
        for d in range(4*r*r, 4*r*r+10*r*r+1):
            t = r+d%r
            s = (d-(r+1)*t)//r
            assert d == r*s+(r+1)*t
            assert r <= t <= 2*r-1 and s >= r
            cases += 1
    return {'integer_cases':cases, 'all_passed':True,
            'general_proof_in':'PROOF.md, Cartesian partitions'}


def graph_add(graph, a, b):
    assert a != b and b not in graph[a]
    graph[a].add(b)
    graph[b].add(a)


def distances(graph, start):
    dist = {start:0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u]+1
                queue.append(v)
    return dist


def girth(graph):
    best = None
    for start in graph:
        dist, parent = {start:0}, {start:None}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v], parent[v] = dist[u]+1, u
                    queue.append(v)
                elif parent[u] != v and parent[v] != u:
                    n = dist[u]+dist[v]+1
                    best = n if best is None else min(best,n)
    return best


def link_fixture():
    # A 14-cycle with label leaves added so each of its seven point degrees is 16.
    # This fixture checks wiring only, and is not an affine-line/rank witness.
    r = 2
    inc = defaultdict(set)
    point_labels = {}
    for z in range(7):
        labels = [z, (z-1)%7] + list(range(7+14*z, 7+14*(z+1)))
        # One cyclic shift gives a genuine length-14 path between distinct
        # same-label x germs in the V link (its full lift closes after 28).
        if z == 0:
            labels[1],labels[5] = labels[5],labels[1]
        point_labels[z] = labels
        for i in labels:
            graph_add(inc, ('p',z), ('i',i))
    assert girth(inc) == 14
    graphs = {name:defaultdict(set) for name in ['O','V','W']}
    projection = {name:{} for name in ['V','W']}
    triangles = 0
    for z, labels in point_labels.items():
        d = len(labels)
        t = r+d%r
        s = (d-(r+1)*t)//r
        pieces = [(r,s,labels[:r*s]), (r+1,t,labels[r*s:])]
        for part,(sb,tb,block) in enumerate(pieces):
            b = (z,part)
            assert len(block) == sb*tb and sb >= r and tb >= r
            for i,(alpha,beta) in zip(block, product(range(sb),range(tb))):
                for u,v in product(range(r),repeat=2):
                    x = ('x',i,u,v)
                    L = ('L',b,u,(alpha+v)%sb)
                    R = ('R',b,v,(beta+u)%tb)
                    graph_add(graphs['O'],L,R)
                    graph_add(graphs['V'],x,L)
                    graph_add(graphs['W'],x,R)
                    projection['V'][x] = projection['W'][x] = ('i',i)
                    projection['V'][L] = projection['W'][R] = ('p',z)
                    triangles += 1
    reports = {}
    for name,graph in graphs.items():
        g = girth(graph)
        assert g is None or g >= (4 if name == 'O' else 14)
        reports[name] = {'vertices':len(graph), 'edges':sum(map(len,graph.values()))//2, 'girth':g}
        if name != 'O':
            proj = projection[name]
            for vertex,neighbors in graph.items():
                images = [proj[v] for v in neighbors]
                assert len(images) == len(set(images))
                assert all(p in inc[proj[vertex]] for p in images)
            finite_turn_distances = []
            xvertices = [v for v in graph if v[0] == 'x']
            for a in xvertices:
                dist = distances(graph,a)
                for b in xvertices:
                    if a != b and a[1] == b[1] and b in dist:
                        finite_turn_distances.append(dist[b])
                        assert dist[b] >= 14
            reports[name]['minimum_finite_same_label_distance'] = min(finite_turn_distances,default=None)
            reports[name]['locally_injective'] = True
    assert reports['V']['minimum_finite_same_label_distance'] == 14
    # Negative control: with s_b < r two different v values collide at an L germ.
    bad_r,bad_s,alpha,j = 3,2,0,0
    collision = [v for v in range(bad_r) if (alpha+v)%bad_s == j]
    assert collision == [0,2]
    return {'incidence_girth':14, 'point_degrees':16, 'triangles':triangles,
            'links':reports,
            'negative_control_s_b_below_r':{'s_b':bad_s,'r':bad_r,'colliding_v':collision},
            'not_a_large_admissible_incidence_instance':True}


def interpolation_fixture():
    # Deliberately coincident geometric lines: horizontal lines through marks.
    q,h,S = 7,2,[0,1]
    marks = list(product(S, repeat=h))
    points = list(product(range(q),repeat=h))
    N = len(marks)
    def f(mark,z):
        value = 1
        for a,x in zip(mark,z):
            for b in S:
                if b != a:
                    value = value*(x-b)*pow((a-b)%q,-1,q)%q
        return value
    H = {}
    for z in points:
        fs = [f(mark,z) for mark in marks]
        H[z] = [[a*b%q for b in fs] for a in fs]
    def matrix_sum(xs):
        return [[sum(H[z][a][b] for z in xs)%q for b in range(N)] for a in range(N)]
    wrong_omit_all_marks,wrong_delete_exception = 0,0
    for i,a in enumerate(marks):
        line = [(x,a[1]) for x in range(q)]
        target = [[(-int(j==i and k==i))%q for k in range(N)] for j in range(N)]
        assert matrix_sum(line) == [[0]*N for _ in range(N)]
        assert matrix_sum([z for z in line if z != a]) == target
        wrong_omit_all_marks += matrix_sum([z for z in line if z not in marks]) != target
        wrong_delete_exception += matrix_sum([z for z in line if z != a and z != (2,a[1])]) != target
    assert wrong_omit_all_marks == N and wrong_delete_exception == N
    return {'q':q,'h':h,'marks':N,'product_degree':2*h*(len(S)-1),
            'coincident_geometric_lines':True,'punctured_identities_passed':N,
            'negative_control_omit_all_marks_failures':wrong_omit_all_marks,
            'negative_control_delete_exceptional_incidence_failures':wrong_delete_exception}


def cycle_independence_fixture():
    # Exact binomial marginals even when differently marked labels select one line.
    q = 3
    marks = list(product(range(2),repeat=2))
    points = list(product(range(q),repeat=2))
    directions = [(1,a) for a in range(q)]+[(0,1)]
    J = len(directions)
    histograms = {z:defaultdict(int) for z in points}
    coincidence_outcomes = 0
    outcome_count = 0
    for choices in product(directions,repeat=len(marks)):
        lines = [frozenset(((a[0]+t*d[0])%q,(a[1]+t*d[1])%q) for t in range(q))
                 for a,d in zip(marks,choices)]
        coincidence_outcomes += len(set(lines)) < len(lines)
        for z in points:
            degree = sum(z in line and z != a for a,line in zip(marks,lines))
            histograms[z][degree] += 1
        outcome_count += 1
    from math import comb
    for z,hist in histograms.items():
        n = len(marks)-int(z in marks)
        for k in range(n+1):
            want = Fraction(comb(n,k)*(J-1)**(n-k), J**n)
            assert Fraction(hist[k],outcome_count) == want
    assert coincidence_outcomes > 0
    return {'q':q,'directions':J,'marks':len(marks),'outcomes':outcome_count,
            'coincident_line_outcomes':coincidence_outcomes,'binomial_marginals_checked':len(points)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    results = {
        'status':'scoped_exact_arithmetic_and_transcription_checks_passed',
        'parameters':exact_parameters(),
        'cartesian':cartesian_checks(),
        'links':link_fixture(),
        'interpolation':interpolation_fixture(),
        'independence':cycle_independence_fixture(),
    }
    results['elapsed_seconds'] = time.perf_counter()-start
    args.output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
