"""Owned exact checks for the analytic contour/Legendre audit.
These finite checks supplement, and never replace, its all-N proof.
No peer implementation is imported.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import json, hashlib, datetime
ROOT=Path(__file__).parent

def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c

def scale(a,s):return [s*x for x in a]
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def bern(N,k):
    return [Q(0)]*k+[Q(comb(N,k)*(-1)**j*comb(N-k,j)) for j in range(N-k+1)]

def legendre_shifted(N):
    a=[[Q(1)]]
    if N:a.append([Q(-1),Q(2)])
    for l in range(1,N):
        a.append(add(scale(mul([Q(-1),Q(2)],a[-1]),Q(2*l+1,l+1)),scale(a[-2],Q(-l,l+1))))
    return a

def elevated(l,N,k):
    return sum((Q((-1)**(l-j)*comb(l,j)**2*comb(N-l,k-j),comb(N,k)) for j in range(l+1) if 0<=k-j<=N-l),Q(0))

def integral(a):return sum((x/Q(i+1) for i,x in enumerate(a)),Q(0))

checks={
 'phase_cubic_256_over_7935_le_1_over_30':Q(256,7935)<=Q(1,30),
 'phase_denominator_power_bound':Q(15,23)**4>Q(2,15),
 'phase_loss_less_1_over_64':Q(2,64*15)/(Q(15,23)**4)<Q(1,64),
 'exp4_partial_sum_gt32':sum((Q(4**j,factorial(j)) for j in range(5)),Q(0))>32,
 'exp7_over3_partial_sum_gt8':sum(((Q(7,3)**j)/factorial(j) for j in range(4)),Q(0))>8,
 'vertical_exponent_56_over23_gt7_over3':Q(56,23)>Q(7,3),
 'ratio_40_over81_lt_half':Q(40,81)<Q(1,2),
 'ratio_derivative_uniform_upper_negative':Q(1,4)+1-Q(35,16)<0,
 'positive_margin_41_over81_gt_half':1-Q(40,81)>Q(1,2)
}
assert all(checks.values())
expansions=0;duality=0;orthogonal=0
for N in range(17):
    R=legendre_shifted(N)
    B=[bern(N,k) for k in range(N+1)]
    C=[[elevated(l,N,k) for k in range(N+1)] for l in range(N+1)]
    for l in range(N+1):
        s=[Q(0)]*(N+1)
        for k in range(N+1):s=add(s,scale(B[k],C[l][k]))
        rr=R[l]+[Q(0)]*(N-l)
        assert s==rr
        assert max(map(abs,C[l]))<=2**l
        expansions+=1
        for j in range(l+1):
            assert integral(mul(R[l],R[j]))==(Q(1,2*l+1) if j==l else 0)
            orthogonal+=1
    D=[Q((-1)**k*(k+1),(N+3)**2) for k in range(N+1)]
    E=[sum((C[l][k]*D[k] for k in range(N+1)),Q(0)) for l in range(N+1)]
    PC=[Q(0)]*(N+1)
    for l in range(N+1):PC=add(PC,scale(R[l],(2*l+1)*E[l]))
    for k in range(N+1):
        assert integral(mul(B[k],PC))==D[k]
        duality+=1
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'scope':'exact rational constant checks and finite Bernstein/Legendre algebra; analytic proof supplies all-N quantifiers',
     'all_passed':True,'constant_checks':checks,
     'degrees':list(range(17)),'exact_elevated_expansions':expansions,
     'exact_orthogonality_pairs':orthogonal,'exact_population_duality_checks':duality,
     'peer_code_imports':False}
(ROOT/'exact_audit_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
