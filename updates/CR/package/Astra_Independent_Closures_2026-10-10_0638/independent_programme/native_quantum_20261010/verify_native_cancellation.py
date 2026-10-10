#!/usr/bin/env python3
"""Small exact/native tests for a rejected quantum cancellation proposal.
CPU only. Run with OPENBLAS_NUM_THREADS=1. No external data required.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import itertools, math, json, platform
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh, expm
from scipy.special import logsumexp

P = {
    'I': np.eye(2, dtype=complex),
    'X': np.array([[0,1],[1,0]], dtype=complex),
    'Y': np.array([[0,-1j],[1j,0]], dtype=complex),
    'Z': np.diag([1,-1]).astype(complex),
}

def pmatrix(word):
    q=np.array([[1]],dtype=complex)
    for a in word:q=np.kron(q,P[a])
    return q

def anticomm(p,q):
    return sum(a!='I' and b!='I' and a!=b for a,b in zip(p,q))%2

def counts(total,length):
    if length==1:
        yield (total,);return
    for x in range(total+1):
        for t in counts(total-x,length-1):yield (x,)+t

def check_shuffle():
    strings=['XZI','ZIX','IYX','IZI']
    coeff=[1,-2,1,3]
    terms=[pmatrix(p) for p in strings]
    adj=[[anticomm(p,q) for q in strings] for p in strings]
    L=len(terms);dim=len(terms[0]);Id=np.eye(dim,dtype=complex)
    @lru_cache(None)
    def S(c):
        if not any(c):return 1
        ans=0
        for i in range(L):
            if c[i]:
                d=list(c);d[i]-=1
                sign=(-1)**sum(adj[i][j]*c[j] for j in range(i+1,L))
                ans+=sign*S(tuple(d))
        return ans
    H=sum(c*p for c,p in zip(coeff,terms))
    records=[]
    for m in range(10):
        aggregate=np.zeros_like(H);nonzero=0;allc=0;maxbits=0
        for c in counts(m,L):
            allc+=1;sc=S(c);maxbits=max(maxbits,abs(sc).bit_length())
            if sc:
                nonzero+=1
                canonical=Id.copy()
                for ci,Pi in zip(c,terms):
                    if ci%2:canonical=canonical@Pi
                aggregate+=sc*math.prod(h**ci for h,ci in zip(coeff,c))*canonical
        direct=np.linalg.matrix_power(H,m)
        err=float(np.max(abs(aggregate-direct)))
        assert err==0, (m,err)
        records.append(dict(order=m,multiplicity_vectors=allc,nonzero_shuffle=nonzero,max_shuffle_bits=maxbits,max_abs_error=err))
    # A d-leaf star: square-free ordering sum is d! sum_{k=0}^d (-1)^k.
    star=[]
    for d in range(1,8):
        signed=0
        for perm in itertools.permutations(range(d+1)):
            signed+=(-1)**perm.index(0)
        expected=math.factorial(d)*(1 if d%2==0 else 0)
        assert signed==expected
        star.append(dict(leaves=d,signed_sum=signed,expected=expected))
    return {'power_identity':records,'squarefree_stars':star,'cache_states':S.cache_info().currsize}

def gadget_terms(n,edges,eta=0.):
    N=n+2*len(edges);terms=[]
    def word(d):
        p=['I']*N
        for j,a in d.items():p[j]=a
        return ''.join(p)
    for e,(u,v) in enumerate(edges):
        for i,s in enumerate([1,-1]):
            a=n+2*e+i
            terms.extend([(1,word({a:'X'})),(s,word({a:'Z'})),(1,word({a:'Z',u:'Z'})),(-1,word({a:'Z',v:'Z'}))])
    if eta:
        for u in range(n):terms.append((-eta,word({u:'X'})))
    return N,terms

def graph_components(terms):
    adj=[set() for _ in terms]
    for i,(_,p) in enumerate(terms):
        for j in range(i):
            if anticomm(p,terms[j][1]):adj[i].add(j);adj[j].add(i)
    todo=set(range(len(terms)));components=[]
    while todo:
        stack=[todo.pop()];comp=set(stack)
        while stack:
            u=stack.pop()
            for v in adj[u]&todo:todo.remove(v);comp.add(v);stack.append(v)
        components.append(sorted(len(adj[u]) for u in comp))
    return components

def dense_H(n,edges,eta=0.):
    N,terms=gadget_terms(n,edges,eta)
    # Accumulate direct local matrices; no sector formula is used here.
    H=np.zeros((2**N,2**N),complex)
    for c,p in terms:H+=c*pmatrix(p)
    return H

def cut_histogram(n,edges):
    ids=np.arange(2**n,dtype=np.uint64);cuts=np.zeros(2**n,dtype=np.int16)
    for u,v in edges:cuts+=(((ids>>u)^(ids>>v))&1).astype(np.int16)
    return np.bincount(cuts,minlength=len(edges)+1)

def lc(x):return float(np.logaddexp(x,-x)-np.log(2.))

def reduced_logZ(n,edges,beta):
    hist=cut_histogram(n,edges)
    logr=lc(beta*math.sqrt(10))-lc(beta*math.sqrt(2))
    logw0=math.log(4)+2*lc(beta*math.sqrt(2))
    nz=np.flatnonzero(hist)
    logQ=float(logsumexp(np.log(hist[nz])+nz*logr))
    return len(edges)*logw0+logQ,logr,logw0,hist,logQ

def check_gadgets():
    small=[('one_edge',2,[(0,1)]),('path',3,[(0,1),(1,2)]),('triangle',3,[(0,1),(1,2),(0,2)])]
    records=[]
    for name,n,edges in small:
        N,terms=gadget_terms(n,edges)
        comps=graph_components(terms)
        assert len(comps)==2*len(edges) and all(c==[1,1,1,3] for c in comps)
        E=eigvalsh(dense_H(n,edges))
        hist=cut_histogram(n,edges);cmax=max(np.flatnonzero(hist))
        exactE0=-2*len(edges)*math.sqrt(2)-(math.sqrt(10)-math.sqrt(2))*cmax
        assert abs(E[0]-exactE0)<2e-11
        for beta in [.01,.7,2.,n+2.]:
            direct=float(logsumexp(-beta*E));formula,*_=reduced_logZ(n,edges,beta)
            err=abs(direct-formula);assert err<2e-11
            records.append(dict(graph=name,data_qubits=n,total_qubits=N,beta=beta,logZ_direct=direct,logZ_formula=formula,abs_error=err))
    # Perturbation is constructed directly from native Pauli coefficients.
    name,n,edges=small[-1];beta=n+2;eta=1/(100*n*beta)
    N,pert_terms=gadget_terms(n,edges,eta)
    assert len(graph_components(pert_terms))==1
    Ep=eigvalsh(dense_H(n,edges,eta));lp=float(logsumexp(-beta*Ep))
    l0,logr,logw0,hist,logQ=reduced_logZ(n,edges,beta)
    shift=abs(lp-l0);assert shift<=beta*n*eta+1e-12
    pert=dict(graph=name,total_qubits=N,beta=beta,eta=eta,logZ_shift=shift,norm_bound=beta*n*eta,frustration_components=1)
    return records,pert

def check_maxcut_recovery():
    # Deterministic named bounded-degree graphs. No random graph generator needed.
    graphs=[]
    graphs.append(('K4',4,[(i,j) for i in range(4) for j in range(i+1,4)]))
    graphs.append(('triangular_prism',6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]))
    graphs.append(('cube',8,[(i,i^(1<<j)) for i in range(8) for j in range(3) if i<(i^(1<<j))]))
    graphs.append(('petersen',10,[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(i+5,((i+2)%5)+5) for i in range(5)]))
    # Möbius ladders have degree three.
    for n in [12,16]:graphs.append((f'mobius_ladder_{n}',n,[(i,(i+1)%n) for i in range(n)]+[(i,i+n//2) for i in range(n//2)]))
    records=[]
    for name,n,edges in graphs:
        beta=n+2
        lz,logr,logw0,hist,logQ=reduced_logZ(n,edges,beta)
        maxcut=int(max(np.flatnonzero(hist)))
        recovered=[]
        for factor in [.75,1.,1.25]:
            for perturb in [-.01,0.,.01]:
                value=(logQ+math.log(factor)+perturb)/logr
                estimate=round(value);assert estimate==maxcut
                recovered.append(dict(relative_factor=factor,allowed_log_perturbation=perturb,pre_round=value,recovered=estimate))
        # Worst-case analytic interval, independent of enumerated graph.
        lo=-(math.log(4/3)+.01)/logr
        hi=(n*math.log(2)+math.log(1.25)+.01)/logr
        assert lo>-.5 and hi<.5
        records.append(dict(graph=name,n=n,m=len(edges),maxcut=maxcut,beta=beta,cut_histogram=hist.tolist(),logr=logr,universal_rounding_interval=[lo,hi],recovery_checks=recovered))
    return records

def check_other_mechanisms():
    # Reflection positivity does not imply a positive product-PSD mixture.
    H=sum(np.kron(P[a],P[a]) for a in ['X','Y','Z'])
    thermal=[]
    for beta in [.1,.3,1.]:
        rho=expm(-beta*H);rho=rho/np.trace(rho)
        pt=rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
        mineig=float(eigvalsh(pt)[0])
        predicted=(3-math.exp(4*beta))/(2*(math.exp(4*beta)+3))
        assert abs(mineig-predicted)<1e-12
        thermal.append(dict(beta=beta,partial_transpose_minimum=mineig,formula=predicted))
    # Exact resolvent expansion: (m+1-sum Z_j)^(-1) has all 2^m Z-monomials.
    fillin=[]
    for m in range(1,9):
        values=[Fraction(1,1+2*x.bit_count()) for x in range(2**m)]
        coeff=[]
        for subset in range(2**m):
            c=sum(((-1)**((x&subset).bit_count()))*values[x] for x in range(2**m))/2**m
            assert c>0
            coeff.append(c)
        fillin.append(dict(spectator_qubits=m,nonzero_pauli_coefficients=len(coeff),
            smallest_coefficient=str(min(coeff))))
    # Positive hopping around a 3-cycle is not gauge-equivalent to all negative hopping.
    triangle=[(0,1),(1,2),(2,0)]
    admissible=0
    for signs in itertools.product([-1,1],repeat=3):
        if all(signs[u]*signs[v]<0 for u,v in triangle):admissible+=1
    assert admissible==0
    return dict(reflection_product_positivity=thermal,resolvent_pauli_fillin=fillin,
        negative_triangle_diagonal_sign_gauges=admissible,
        warning='These tests reject proposed shortcuts; they are not hardness or novelty claims.')

def main():
    shuffle=check_shuffle();gadgets,pert=check_gadgets();recovery=check_maxcut_recovery()
    result={'status':'all checks passed; no efficient general simulator obtained',
            'python':platform.python_version(),'numpy':np.__version__,
            'shuffle':shuffle,'dense_gadget_checks':gadgets,'connected_perturbation':pert,'maxcut_recovery':recovery,'other_mechanisms':check_other_mechanisms()}
    out=Path(__file__).with_name('test_results.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'shuffle_orders':len(shuffle['power_identity']),
        'dense_trace_checks':len(gadgets),'max_dense_dimension':512,
        'max_dense_logZ_error':max(x['abs_error'] for x in gadgets),
        'maxcut_graphs':len(recovery),'perturbation':pert,'results':str(out)},indent=2))
if __name__=='__main__':main()
