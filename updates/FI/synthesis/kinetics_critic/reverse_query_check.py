"""Independent Fraction reconstruction of all final reverse-clock queries."""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]/'FI-sources'/'kinetics'
def sqrtf(x):
    a=isqrt(x.numerator); b=isqrt(x.denominator)
    if a*a!=x.numerator or b*b!=x.denominator: raise ValueError('nonrational pair factor')
    return F(a,b)
def load(stem): return json.loads((ROOT/(stem+'.json')).read_text())
def loadtr(stem): return json.loads((ROOT/(stem+'_transcript.json')).read_text())
def reconstruct(tr):
    data={int(k):F(v) for k,v in tr['weights'].items()}; n=next(k for k in range(1,200) if 1+k+k*(k-1)//2==tr['energy_queries'])
    w0=data[0]; singles=[data[1<<i] for i in range(n)]; edges={}; fields=[]
    for i,j in combinations(range(n),2):
        t=sqrtf(data[(1<<i)|(1<<j)]*w0/(singles[i]*singles[j]))
        if t!=1: edges[i,j]=t
    for i in range(n):
        h=singles[i]/w0
        for (a,b),t in edges.items():
            if i in (a,b): h*=t
        fields.append(h)
    def ratio(i,x):
        r=fields[i]
        for (a,b),t in edges.items():
            if i==a:r*=t if (x>>b)&1 else 1/t
            elif i==b:r*=t if (x>>a)&1 else 1/t
        return r
    attempts={}; expected_prep={}; rates={}
    for key,raw0 in tr['reverse_rates'].items():
        i,x=map(int,key.split(':')); raw=F(raw0); r=ratio(i,x)
        dprob=max(F(1),r)/(1+r); a=raw/dprob
        expected_prep[key]=0 if r>=1 else 1
        assert int(tr['prepared_bit'][key])==expected_prep[key]
        # Re-evaluate the actual downhill edge from its selected less probable endpoint.
        src=x | (expected_prep[key]<<i); dst=src^(1<<i)
        def W(mask):
            z=F(1)
            for j,h in enumerate(fields):
                if (mask>>j)&1:z*=h
            for (j,k),t in edges.items():
                if ((mask>>j)&1)==((mask>>k)&1):z*=t
            return z
        actual_d=a*W(dst)/(W(src)+W(dst))
        assert actual_d==raw
        assert a/2<=raw<=a
        attempts[key]=a; rates[key]=raw
    # Möbius recovery, support, and exact evaluation over every context in each
    # recovered support (the only step needing an exponential truth table).
    by_i={}; max_support=0; min_attempt=None; max_attempt=F(0); all_recovered=True
    for i in range(n):
        others=[j for j in range(n) if j!=i]
        def query(S):return attempts[f'{i}:{sum(1<<j for j in S)}']
        c0=query(())
        linear={j:query((j,))-c0 for j in others}
        quad={(j,k):query((j,k))-query((j,))-query((k,))+c0 for j,k in combinations(others,2)}
        linear={j:v for j,v in linear.items() if v}
        quad={p:v for p,v in quad.items() if v}
        support=sorted(set(linear)|{j for pair in quad for j in pair})
        max_support=max(max_support,len(support))
        for z in range(1<<len(support)):
            y={j:(z>>p)&1 for p,j in enumerate(support)}
            a=c0+sum((v*y.get(j,0) for j,v in linear.items()),F(0))+sum((v*y.get(j,0)*y.get(k,0) for (j,k),v in quad.items()),F(0))
            assert a>0
            min_attempt=a if min_attempt is None else min(min_attempt,a)
            max_attempt=max(max_attempt,a)
        # Compare coefficients against every acquired context (empty/single/pair).
        for size in range(3):
            for S in combinations(others,size):
                pred=c0+sum((v for j,v in linear.items() if j in S),F(0))+sum((v for (j,k),v in quad.items() if j in S and k in S),F(0))
                assert pred==query(S)
        by_i[i]={'support_size':len(support),'nonzero_linear':len(linear),'nonzero_quadratic':len(quad),'support':support,'coefficients_positive_on_full_support':True}
    assert len(attempts)==n*(1+(n-1)+(n-1)*(n-2)//2)
    return {'n':n,'energy_queries':tr['energy_queries'],'reverse_queries':len(attempts),'edge_count':len(edges),'all_preparation_bits_match':True,'all_d_rates_recomputed_exactly':True,'all_rates_in_a_over2_to_a':True,'degree2_coefficients_recover_every_queried_context':all_recovered,'max_recovered_support':max_support,'all_acquired_support_tables_positive':True,'min_attempt_on_recovered_support_tables':str(min_attempt),'max_attempt_on_recovered_support_tables':str(max_attempt),'supports':by_i,'maximum_local_excitation_weight_ratio':tr['maximum_local_excitation_weight_ratio']}

A=loadtr('reverse_A');B=loadtr('reverse_B')
ra=reconstruct(A); rb=reconstruct(B)
assert A['weights']==B['weights']
zero_same=all(A['reverse_rates'][f'{i}:0']==B['reverse_rates'][f'{i}:0'] for i in range(18))
assert zero_same
loB=F(load('reverse_B')['lower']); hiA=F(load('reverse_A')['upper']); ratio=loB/hiA
assert ratio>F(154685,100000)
print(json.dumps({'A':ra,'B':rb,'same_energy_transcript':True,'all_zero_context_rates_equal':zero_same,'exact_certified_separation_lower':str(ratio),'separation_float':float(ratio)},indent=2))
