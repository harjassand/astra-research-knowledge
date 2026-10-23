#!/usr/bin/env python3
"""Exact new diagnostics, independent of the analytic counting proof.

Walk maxima are built by dynamic programming on (position,maximum), then
compared with the closed susceptibility. A three-qubit permutation directly
checks the omitted-correlation witness. Neither bounded check proves all k.
Standard library only; no physical bath cutoff or stationarity simulation.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json, platform, resource, time


def maxima(max_n):
    state = {(0,0): F(1)}
    result = []
    for n in range(max_n+1):
        marginal = defaultdict(F)
        for (position,highest),mass in state.items():
            marginal[highest] += mass
        result.append(dict(marginal))
        nxt = defaultdict(F)
        for (position,highest),mass in state.items():
            for step in (-1,1):
                p = position+step
                nxt[p,max(highest,p)] += mass/2
        state = nxt
    return result


def contract(order, rho):
    # U maps (input x,bath a,b) to (output a,bath x,b) or (a,b,x).
    # M_uv = sum rho[bin,bout] U[u,bout;v,bin], preserving complex convention.
    matrix = [[F(0) for _ in range(2)] for _ in range(2)]
    for x,a,b in product(range(2),repeat=3):
        y,c,d = (a,x,b) if order == 'A' else (a,b,x)
        matrix[y][x] += rho[2*a+b][2*c+d]
    return matrix


def run(max_k=16):
    start = time.perf_counter()
    distributions = maxima(max_k-2)
    observations=[]
    for k in range(2,max_k+1):
        pair_sum=F(0)
        for i in range(k-1):
            for r in range(k-i-1):
                gt=eq=F(0)
                for h,p in distributions[i].items():
                    for d,q in distributions[r].items():
                        if h>d:gt+=p*q
                        if h==d:eq+=p*q
                pair_sum+=(gt+eq/4)/2
        collision=sum(F((k-1-2*m)*comb(2*m,m),4**m)
                      for m in range((k-2)//2+1))
        formula=F(k*(k-1),8)-collision/8
        n=(k-2)//2
        closed=F((2*n+1)*comb(2*n,n),4**n)*(F(k-1)-F(2*n,3))
        assert collision == closed
        assert pair_sum == formula
        assert formula >= F(k*k,32)
        observations.append({'k':k,'exact_v':str(formula),
                             'independent_walk_DP_matches':True})

    uniform=[[F(int(i==j),4) for j in range(4)] for i in range(4)]
    sym=[[F(int(i==j)+int((i//2,i%2)==(j%2,j//2)),6)
          for j in range(4)] for i in range(4)]
    witness={}
    for name,rho in [('independent_uniform',uniform),('symmetric_correlated',sym)]:
        a,b=contract('A',rho),contract('B',rho)
        delta=[[a[i][j]-b[i][j] for j in range(2)] for i in range(2)]
        square=sum(t*t for row in delta for t in row)/2
        expected=F(1,16) if name=='independent_uniform' else F(0)
        assert square==expected
        reduced=[[sum(rho[2*i+t][2*j+t] for t in range(2))
                  for j in range(2)] for i in range(2)]
        assert reduced==[[F(1,2),F(0)],[F(0),F(1,2)]]
        witness[name]={'A':[[str(t) for t in row] for row in a],
                       'B':[[str(t) for t in row] for row in b],
                       'normalized_square_difference':str(square),
                       'one_site_marginal':'I/2'}
    return {'scope':'Bounded exact DP and omitted-correlation replay, not all-length proof',
            'maximum_k':max_k,'walk_checks':observations,
            'omitted_correlation_witness_charge':'001','endpoints':[0,2],
            'witness':witness,'wall_seconds':time.perf_counter()-start,
            'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':platform.python_version(),
            'total_discovery_inference_review_cost':'unknown'}


if __name__=='__main__':
    result=run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
