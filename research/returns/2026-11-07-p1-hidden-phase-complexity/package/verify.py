"""Executed illustrations and exact rational certificate checks.

Floating Newton solves only propose coordinates. Every reported minimum error
bound is subsequently checked using exact rational arithmetic. The general
theorem, not these finite checks, proves the counts and all-input statements.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
from time import perf_counter
import json
import numpy as np
from exact_core import (coupling, graph_laplacian, partition_laplacian,
                        check_quotient, compile_phase, minimum_certificate,
                        cut_size, fixed_mean_bounds)


def jsonable(obj):
    if isinstance(obj, F):
        return {'numerator': str(obj.numerator), 'denominator': str(obj.denominator),
                'decimal': float(obj)}
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    return obj


def proposal(L, labels):
    n = len(labels)
    a = float(coupling(n))
    A = np.asarray(L, dtype=float)
    X = np.r_[0.0, labels].astype(float)
    for _ in range(18):
        z, x = X[0], X[1:]
        g = np.r_[2*z+z**3-a*x.sum(), x**3-x+A@x-a*z]
        if np.max(np.abs(g)) < 2e-15:
            break
        H = np.zeros((n+1,n+1))
        H[0,0] = 2+3*z*z
        H[0,1:] = H[1:,0] = -a
        H[1:,1:] = np.diag(3*x*x-1)+A
        X -= np.linalg.solve(H,g)
    assert np.max(np.abs(g)) < 1e-11
    den = 1 << 44
    return [F(int(round(float(v)*den)), den) for v in X]


def verify_constants():
    assert F(100,97)*(F(1,200)+F(1,50)) == F(5,194) < F(1,32)
    assert F(97,100)-F(1,10)-F(1,50) == F(17,20)
    assert F(3,100)*F(3,5) > F(1,100)  # Schur margin for H >= 7/5.
    assert F(49,50)-F(49,50)**3 > F(101,4000)
    assert F(7,10)*F(2,25)**2 > F(1,250)
    return True


def main():
    start = perf_counter()
    out = {'status': 'checks_in_progress', 'exact_constant_checks': verify_constants(),
           'scope': 'finite software execution; no physical experiment',
           'counts_proven_by': 'general contraction/inertia theorem in RESEARCH_REPORT.txt'}
    n = 12
    edges = [(i,j) for i in range(n) for j in range(i+1,n)
             if (i*7+j*11+i*j) % 7 <= 2]
    degrees = [sum(i == u or i == v for u,v in edges) for i in range(n)]
    scale = F(1,100*max(degrees))
    L = graph_laplacian(n,edges,scale)
    R = check_quotient(L)
    worst_error = F(0)
    worst_gap = F(0)
    examples = []
    for index, labels in enumerate(product((-1,1), repeat=n)):
        X = proposal(L,labels)
        cert = minimum_certificate(X,L,labels)
        assert cert['distance_bound'] < F(1,10**10)
        worst_error = max(worst_error,cert['distance_bound'])
        worst_gap = max(worst_gap,cert['energy_gap_bound'])
        if index in (0,1,37,1234,2047,4095):
            examples.append({'labels':labels,'X':X,'certificate':cert})
    out['weak_13_state_execution'] = {
        'hidden_n':n,'edges':edges,'edge_weight':scale,'row_quotient':R,
        'certified_minima':2**n,'theorem_total_critical_points':3**n,
        'theorem_morse_counts':[comb(n,j)*2**(n-j) for j in range(n+1)],
        'maximum_exact_distance_certificate':worst_error,
        'maximum_exact_energy_gap_certificate':worst_gap,'examples':examples}
    print('weak model: all 4096 minimum residual certificates passed',flush=True)

    partition_rows=[]
    for groups in ([12],[4,4,4],[2]*6,[1]*12):
        LP = partition_laplacian(groups)
        assert check_quotient(LP) == R
        k = len(groups)
        selected = [tuple(1 for _ in groups), tuple((-1)**i for i in range(k))]
        certs=[]
        for group_labels in selected:
            labels=tuple(s for m,s in zip(groups,group_labels) for _ in range(m))
            X=proposal(LP,labels)
            c=minimum_certificate(X,LP,labels)
            assert c['distance_bound'] < F(1,10**10)
            certs.append({'labels':group_labels,'distance_bound':c['distance_bound']})
        partition_rows.append({'groups':groups,'k':k,'minima':2**k,'critical_points':3**k,
                               'morse_counts':[comb(k,j)*2**(k-j) for j in range(k+1)],
                               'selected_minimum_certificates':certs})
    out['partition_family']=partition_rows

    reference=[]
    for labels in ((1,)*n, tuple((-1)**i for i in range(n)),
                   tuple((-1,0,1)[i%3] for i in range(n))):
        result=compile_phase(labels,F(1,10**10),L=L)
        reference.append({'kind':'weak','labels':labels,**result})
    result=compile_phase((-1,0,1),F(1,10**10),groups=(4,4,4),expand_physical=True)
    reference.append({'kind':'partition','groups':[4,4,4],'labels':[-1,0,1],**result})
    out['standard_library_rational_compiler_runs']=reference
    print('rational contraction compiler: four addressed phases passed',flush=True)

    # A nontrivial, fully explicit MaxCut -> minimum bisection instance.
    v=6
    original=[(0,1),(0,2),(0,5),(1,2),(1,3),(2,4),(3,4),(3,5),(4,5)]
    maxcut=max(cut_size(original,s) for s in product((-1,1),repeat=v))
    N=2*v
    original_set=set(original)
    complement=[(i,j) for i in range(N) for j in range(i+1,N)
                if (i,j) not in original_set]
    bis=10**9
    witness=None
    hist={}
    for plus in combinations(range(N),N//2):
        plus=set(plus)
        s=tuple(1 if i in plus else -1 for i in range(N))
        value=cut_size(complement,s)
        hist[value]=hist.get(value,0)+1
        if value < bis:
            bis=value; witness=s
    assert bis == v*v-maxcut
    bounds=fixed_mean_bounds(N,complement,bis)
    assert bounds['cut_recovery_margin'] > F(1,3)
    lam=bounds['lambda']
    assert check_quotient(graph_laplacian(N,complement,lam)) == R
    out['maxcut_to_phase_separation']={'original_graph_vertices':v,'original_edges':original,
        'maxcut':maxcut,'phase_graph_vertices':N,'phase_graph_edges':complement,
        'balanced_patterns_enumerated':comb(N,N//2),'minimum_bisection':bis,
        'bisection_witness':witness,'cut_histogram':hist,'energy_certificate':bounds}

    # Two indistinguishable graphs with very different fixed-mean tasks.
    empty=fixed_mean_bounds(n,[],0)
    complete_edges=list(combinations(range(n),2))
    complete=fixed_mean_bounds(n,complete_edges,n*n//4)
    out['indistinguishable_fixed_mean_pair']={'empty':empty,'complete':complete}
    out['elapsed_seconds']=perf_counter()-start
    out['status']='all_checks_passed'
    target=Path(__file__).with_name('EXECUTED_CERTIFICATES.json')
    target.write_text(json.dumps(jsonable(out),indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':out['status'],'certified_minima':2**n,
        'worst_distance_bound':float(worst_error),'worst_energy_gap':float(worst_gap),
        'maxcut':maxcut,'minimum_bisection':bis,'phase_energy_interval':
        [float(bounds['lower']),float(bounds['upper'])],
        'elapsed_seconds':out['elapsed_seconds']},indent=2))


if __name__ == '__main__':
    main()
