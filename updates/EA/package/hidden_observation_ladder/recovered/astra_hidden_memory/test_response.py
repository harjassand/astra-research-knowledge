"""Independent state-space symmetry and numerical-response checks.
Exact integer assertions are separated from floating-point diagnostics.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, expm_frechet
from test_lift import setup, dense, state_permutation


def tilt(Q, f, h):
    out = Q * np.exp(h * (f[None,:] - f[:,None])/2)
    np.fill_diagonal(out, 0.)
    np.fill_diagonal(out, -out.sum(axis=1))
    return out


def run():
    exact=0; numerical=[]
    for r in range(1,9):
        num,den,araw,f=dense(r); n=len(f)
        perm=state_permutation(r)
        assert np.array_equal(perm[perm],np.arange(n)); exact+=1
        assert np.array_equal(f[perm],f); exact+=1
        assert np.array_equal(num[np.ix_(perm,perm)],num.T); exact+=1
        assert np.sum((araw-araw.T)**2)==4*r*n*n; exact+=1
        # The mean of every polynomial generator perturbation of order <2r
        # vanishes even with arbitrarily many observation multiplications:
        # minimum number of A-edges in a 0-to-0 walk using >=1 A-edge.
        d,ff,c,edges,theta=setup(r)
        import heapq
        start=(0,False); dist={start:0}; heap=[(0,*start)]
        while heap:
            cost,a,used=heapq.heappop(heap)
            if dist[(a,used)] != cost: continue
            nxt=[(a^ff,used,0)]
            if a in edges: nxt.append((edges[a],True,1))
            for b,u,w in nxt:
                if cost+w < dist.get((b,u),10**9):
                    dist[(b,u)]=cost+w; heapq.heappush(heap,(cost+w,b,u))
        assert dist[(0,True)]==2*r; exact+=1
        Q=num/den; pi=np.ones(n)/n; eps=1/(16*r)
        V=Q*(f[None,:]-f[:,None])/2
        np.fill_diagonal(V,0.); np.fill_diagonal(V,-V.sum(axis=1))
        E,dE=expm_frechet(Q,V)
        susceptibility=float(pi@dE@f)
        predicted=1-np.exp(-1)-eps**2/2*(1-2/np.e)
        assert abs(susceptibility-predicted)<3e-12
        h=eps/100
        plus=float(pi@expm(tilt(Q,f,h))@f)
        minus=float(pi@expm(tilt(Q,f,-h))@f)
        slope=(plus-minus)/(2*h)
        baseline=np.tanh(h)*(1-np.exp(-np.cosh(h)))/h
        gap=baseline-slope
        assert gap>eps**2/10
        assert abs(float(pi@(f*(E@f)))-1/np.e)<3e-12
        numerical.append({'r':r,'states':n,'susceptibility':susceptibility,
                          'formula_error':susceptibility-predicted,
                          'finite_field':h,'finite_field_gap':gap,
                          'proved_gap_lower_bound':eps**2/10})
    out={'exact_integer_assertions':exact,'numerical_diagnostics':numerical,
         'status':'Finite falsification tests; numerical exponentials are not interval-certified.'}
    with open(Path(__file__).resolve().parent/'response_results.json','w') as f:
        json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))

if __name__=='__main__': run()
