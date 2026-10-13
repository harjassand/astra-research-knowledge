"""Exact finite diagnostics for TASK_CERTIFICATES.md; no scientific libraries."""
from fractions import Fraction as F
import json
from pathlib import Path

def mat(rows): return [[F(x) for x in r] for r in rows]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a): return [[c*x for x in r] for r in a]
def transpose(a): return list(map(list,zip(*a)))
def mul(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def inv2(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    assert d
    return scale(1/d,[[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]])
def psd2(a):
    return a==transpose(a) and a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]>=a[0][1]**2
I=mat([[1,0],[0,1]])
def g(a,x): return mul(x,inv2(add(I,scale(a,x))))
def phi(v,x): return mul(mul(v,x),transpose(v))
def row_bound(a): return max(sum(abs(x) for x in r) for r in a)

def run():
    sharp=0
    for a in map(F,[1,2,3]):
        for e in [F(1,1000),F(1,10),F(1,2),F(2)]:
            eta=e-e/(1+a*e)
            assert eta==a*e*e/(1+a*e)
            assert a*e*e-a*eta*e-eta==0
            sharp+=1
    # A noncommuting exact fixed-point realization with a subunital rational V.
    v=scale(F(1,2),mat([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]))
    x=mat([[F(1,3),0],[0,F(1,4)]])
    f=mul(x,inv2(add(I,scale(-1,x))))
    p=add(f,scale(-1,phi(v,x)))
    assert psd2(p) and psd2(add(I,scale(-1,phi(v,I))))
    assert g(F(1),add(phi(v,x),p))==x
    assert mul(p,x)!=mul(x,p)
    matrix=0
    for den in [64,128,256,512,1024,2048]:
        for sign in [1,-1]:
            err=scale(F(sign,den),mat([[2,1],[1,-1]]))
            y=add(x,err)
            assert psd2(y)
            residual=add(y,scale(-1,g(F(1),add(phi(v,y),p))))
            eta=row_bound(residual)  # certified norm bound, not an equality claim
            # Find a rational e satisfying the exact sufficient residual condition.
            e=F(1,den)
            while eta>e*e/(1+e): e*=2
            assert psd2(add(scale(e,I),err)) and psd2(add(scale(e,I),scale(-1,err)))
            matrix+=1
    # Same certificate, two legal targets with opposite optimal actions.
    p=F(1,2); x=F(1,2)
    assert (x+p)/(1+x+p)==x
    losses=[]
    for target in [F(0),x]:
        assert target<=(target+p)/(1+target+p)
        losses.append([(u-2*target)**2 for u in [F(0),F(1)]])
    assert losses==[[F(0),F(1)],[F(1),F(0)]]
    for prob in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        assert max(prob,1-prob)>=F(1,2)
    # Scalar source iteration and exact bound; this checks a finite instance only.
    z=F(0)
    for k in range(1,65):
        z=(z+p)/(1+z+p)
        assert 0<=x-z<=F(1,k+1)
    # Strict task margin: Q0=1,Q1=-1, constants make u1 optimal at x=1/2.
    e=F(1,100); y=x-e
    ell0=y; ell1=F(1,2)-y
    assert ell0-ell1>2*e
    assert F(1,2)-x<x
    # A large common task component cancels in the exact pairwise difference.
    q0=mat([[1001,0],[0,1000]])
    q1=mat([[1000,0],[0,1001]])
    qdiff=add(q1,scale(-1,q0))
    assert qdiff==mat([[-1,0],[0,1]])
    assert sum(abs(qdiff[i][i]) for i in range(2))==2
    assert sum(abs(q0[i][i])+abs(q1[i][i]) for i in range(2))==4002
    return {"status":"PASS", "arithmetic":"stdlib fractions.Fraction",
            "sharp_scalar_residual_identities":sharp,
            "noncommuting_matrix_residual_certificates":matrix,
            "shared_certificate_opposite_decisions":2,
            "randomized_no_observation_policies_checked":5,
            "scalar_source_iterations":64,"strict_task_margin_fixtures":1,
            "exact_pairwise_task_cancellation_fixtures":1,
            "scope":"Finite exact internal diagnostics; analytic proofs remain unreviewed. No physical interface, universal proof or novelty validation."}

if __name__=="__main__":
    result=run()
    Path(__file__).with_name("task_certificate_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
