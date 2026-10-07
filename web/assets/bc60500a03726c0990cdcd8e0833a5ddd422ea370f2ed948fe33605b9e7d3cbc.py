#!/usr/bin/env python3
"""Bounded exact bookkeeping checks; no solver or asymptotic certification."""
from fractions import Fraction as Q
import json, time
from pathlib import Path
start = time.monotonic()

def zero(r,c): return [[Q(0) for _ in range(c)] for _ in range(r)]
def eye(d):
    a=zero(d,d)
    for i in range(d): a[i][i]=Q(1)
    return a
def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0)) for j in range(len(b[0]))] for i in range(len(a))]
def scale(a,s): return [[s*v for v in row] for row in a]
def add(a,b): return [[x+y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def tensor(a,b):
    return [[a[i//len(b)][j//len(b[0])]*b[i%len(b)][j%len(b[0])] for j in range(len(a[0])*len(b[0]))] for i in range(len(a)*len(b))]
def swap(d):
    a=zero(d*d,d*d)
    for i in range(d):
        for j in range(d): a[i*d+j][j*d+i]=Q(1)
    return a
def partial(a,d,which):
    r=zero(d,d)
    for i in range(d):
        for j in range(d):
            r[i][j]=sum((a[i*d+k][j*d+k] if which==2 else a[k*d+i][k*d+j] for k in range(d)),Q(0))
    return r

def cloner_checks(d):
    ident=eye(d); sw=swap(d)
    sym=scale(add(eye(d*d),sw),Q(1,2))
    assert mm(sym,sym)==sym
    lam=Q(d+2,2*(d+1))
    choi=zero(d**3,d**3)
    marginal_supertrace=Q(0)
    for i in range(d):
        for j in range(d):
            e=zero(d,d);e[i][j]=Q(1)
            b=scale(mm(mm(sym,tensor(e,ident)),sym),Q(2,d+1))
            expected=scale(e,lam)
            if i==j: expected=add(expected,scale(ident,Q(1,2*(d+1))))
            assert partial(b,d,1)==expected
            assert partial(b,d,2)==expected
            assert sum((b[k][k] for k in range(d*d)),Q(0))==(1 if i==j else 0)
            assert mm(mm(sw,b),sw)==b
            marginal_supertrace+=expected[i][j]
            for u in range(d*d):
                for v in range(d*d): choi[i*d*d+u][j*d*d+v]=b[u][v]
    # CP: exact Choi Gram equality from the explicit isometric Kraus columns.
    gram=zero(d**3,d**3)
    for k in range(d):
        col=[sym[u][i*d+k] for i in range(d) for u in range(d*d)]
        for a in range(d**3):
            for b in range(d**3): gram[a][b]+=Q(2,d+1)*col[a]*col[b]
    assert gram==choi
    assert marginal_supertrace==Q(d*(d+1),2)
    return {"d":d,"checks":"exact projector, both marginals, TP, swap symmetry, Choi Gram CP, supertrace","cloner_lambda":str(lam),"supertrace":str(marginal_supertrace)}

rows=[]
for d in [2,3,4,8,16,32,64,128,1024]:
    lam=Q(d+2,2*(d+1))
    cap=Q(d*(d+3),4)
    raw_cap=Q(d*d+1,2)
    tr=Q(d*(d+1),2)
    assert tr-cap==Q(d*(d-1),4)
    assert tr-raw_cap==Q(d-1,2)
    assert (cap-1)/Q(d*d-1)==Q(d+4,4*(d+1))
    kappa=Q(4*((d*d)//4),d*d)
    powers={str(m):str(kappa*max(Q(0),lam**m-Q(1,d+1))) for m in [1,2,4,8,16]}
    rows.append({"d":d,"lambda":str(lam),"corrected_supertrace_cap":str(cap),"cloner_supertrace":str(tr),"corrected_gap":str(tr-cap),"raw_supertrace_cap":str(raw_cap),"raw_gap":str(tr-raw_cap),"corrected_norm_distance_lower":str(kappa*(tr-cap)/Q(d*d-1)),"EB_power_distance_exact":powers})

# Scalar eigenvalue inequality used to exclude even the raw instrument class.
eigen_rows=[]
for d in range(2,9):
    samples=[[Q(1,d)]*d,[Q(1)]+[Q(0)]*(d-1)]
    # Rational square-root eigenvalues, normalized by their square sum.
    for seed in range(1,11):
        r=[Q(((seed*(j+1)+j*j)%11)+1) for j in range(d)]
        norm=sum((x*x for x in r),Q(0))
        # S=(sum sqrt(p))^2 and purity, both rational for these p.
        S=sum(r,Q(0))**2/norm
        purity=sum((x**4 for x in r),Q(0))/norm**2
        assert S+purity<=Q(d)+Q(1,d)
        eigen_rows.append({"d":d,"seed":seed,"S_plus_purity":str(S+purity),"bound":str(Q(d)+Q(1,d))})

out={"scope":"Exact finite formula/transcription checks; proof is in INITIAL.txt. No general EB lifting or counterexample certified.","dense_cloner_checks":[cloner_checks(d) for d in [2,3,4]],"parameter_rows":rows,"scalar_fixtures":len(eigen_rows),"elapsed_seconds":time.monotonic()-start}
Path(__file__).with_name('checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({"dense_dimensions":[2,3,4],"parameter_rows":len(rows),"scalar_fixtures":len(eigen_rows),"elapsed_seconds":out['elapsed_seconds'],"all_exact_checks_passed":True}))
