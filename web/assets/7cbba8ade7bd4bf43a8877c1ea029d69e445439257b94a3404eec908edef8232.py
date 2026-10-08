"""Small new checks of the rank/K and gap-free basis refinements.
FINITE-EVIDENCE only. Rational column decisions; float eigen diagnostics.
Run once: OPENBLAS_NUM_THREADS=1 python3 .../refinements_checks.py
No continuum, large-n, external-validation or priority claim.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from pathlib import Path
import json
import numpy as np

RNG = np.random.default_rng(81012719)
TOL = 1e-8


def physical_and_cube(L, m, J=1.):
    xs = list(combinations(range(1, L), m))
    ys = [tuple(x[i]-i for i in range(m)) for x in xs]
    ix, iy = {x:i for i,x in enumerate(xs)}, {y:i for i,y in enumerate(ys)}
    a, n = len(xs), L-m
    T = np.zeros((a,a)); W = np.zeros(a); cube = np.eye(a)*4*J*L**2*m
    alpha = np.zeros(a)
    for i,(x,y) in enumerate(zip(xs,ys)):
        occ = set(x)
        T[i,i] = 2*J*L**2*((1 in occ)+(L-1 in occ))
        W[i] = sum(v+1 in occ for v in x)
        for v in x:
            for dest in (v-1,v+1):
                if 1<=dest<L and dest not in occ:
                    zz=tuple(sorted((occ-{v})|{dest}))
                    T[i,i]+=2*J*L**2; T[i,ix[zz]]-=2*J*L**2
        counts=Counter(y)
        alpha[i]=1/np.sqrt(np.prod([factorial(r) for r in counts.values()]))
        for v,r in counts.items():
            for dest in (v-1,v+1):
                if 1<=dest<=n:
                    zz=list(y); zz.remove(v); zz.append(dest); zz=tuple(sorted(zz))
                    cube[i,iy[zz]]-=2*J*L**2*np.sqrt(r*(counts[dest]+1))
    K=np.diag(alpha)
    return T,W,cube,K


def det(A):
    A=[list(row) for row in A]; n=len(A); answer=F(1)
    for k in range(n):
        p=next((j for j in range(k,n) if A[j][k]),None)
        if p is None: return F(0)
        if p!=k: A[k],A[p]=A[p],A[k];answer=-answer
        d=A[k][k];answer*=d
        for i in range(k+1,n):
            t=A[i][k]/d
            for j in range(k+1,n): A[i][j]-=t*A[k][j]
    return answer


def inverse(A):
    n=len(A)
    C=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        p=next(j for j in range(k,n) if C[j][k]);C[k],C[p]=C[p],C[k]
        pivot=C[k][k];C[k]=[x/pivot for x in C[k]]
        for i in range(n):
            if i!=k:
                t=C[i][k];C[i]=[x-t*y for x,y in zip(C[i],C[k])]
    return [row[n:] for row in C]


def gram(Q, selected):
    return [[sum((Q[k][i]*Q[k][j] for k in range(len(Q))),F(0))
             for j in selected] for i in selected]


kinetic_margins=[]; defect_margins=[]; equalities=[]; orbit_errors=[]
rank_checks=[]
for L in range(3,11):
    g=100.;R=g*L/4
    whole_rank=0
    for m in range(L):
        T,W,cube,K=physical_and_cube(L,m)
        a=len(W)
        kinetic_margins.append(float(np.linalg.eigvalsh(T-K@cube@K)[0]))
        defect_margins.append(float(np.min(W-(1-np.diag(K)**2))))
        xs=list(combinations(range(1,L),m))
        for j,x in enumerate(xs):
            counts=Counter(tuple(x[i]-i for i in range(m)))
            P=sum(r*(r-1)//2 for r in counts.values())
            t=np.prod([factorial(r) for r in counts.values()])
            orbit_errors.append(abs(P/t-P*np.diag(K)[j]**2))
        if m==2:
            equalities.append(float(np.linalg.norm(T-K@cube@K,2)))
            P=np.diag(W)
            equalities.append(float(np.linalg.norm(K@(2*L*P)@K-L*P,2)))
            mass=np.diag(np.diag(K)**-2)
            equalities.append(float(np.linalg.norm(mass-(np.eye(a)+P),2)))
        energies,vectors=np.linalg.eigh(T+g*L*np.diag(W))
        sel=energies<=2*R+1e-9;whole_rank+=int(sel.sum())
        if sel.any():
            U=vectors[:,sel];transfer=U.T@K@K@U
            assert np.linalg.eigvalsh(transfer)[0]>=.5-TOL
            assert np.linalg.eigvalsh(4*R*transfer-U.T@K@cube@K@U)[0]>=-TOL
    # Count all free-boson label occupations 8 sum k²<=4R via integer DP.
    emax=int(np.floor(4*R/8+1e-10))
    dp=[0]*(emax+1);dp[0]=1
    for k in range(1,int(np.sqrt(emax))+1):
        for e in range(k*k,emax+1): dp[e]+=dp[e-k*k]
    bound=sum(dp)
    assert whole_rank<=bound
    rank_checks.append({"L":L,"R":R,"finite_rank":whole_rank,
                        "free_Fock_count_upper":bound})

greedy_cases=[]
for a in (5,8,10):
    for d in (1,2,3,4):
        if d>=a:continue
        while True:
            C=[[F(int(RNG.integers(-3,4))) for _ in range(d)] for _ in range(a)]
            G=[[sum((C[k][i]*C[k][j] for k in range(a)),F(0)) for j in range(d)]
               for i in range(d)]
            if det(G):break
        Gi=inverse(G)
        P=[[sum((C[i][k]*Gi[k][l]*C[j][l] for k in range(d) for l in range(d)),F(0))
            for j in range(a)] for i in range(a)]
        H=1+3*d*(a-d);theta=F(factorial(d),(2*a)**d);nu=F(1,100)
        zeta=min(F(1,4),theta/(100*d*2**d),F(1,12*H),nu/(128*H**2))
        noise=[[F(int(RNG.integers(-1,2)),a) for j in range(a)] for i in range(a)]
        noise=[[((noise[i][j]+noise[j][i])/2) for j in range(a)] for i in range(a)]
        Q=[[P[i][j]+zeta*noise[i][j] for j in range(a)] for i in range(a)]
        selected=[];volume=F(1)
        for k in range(d):
            best=max((det(gram(Q,selected+[j])),j) for j in range(a) if j not in selected)
            residual=best[0]/volume
            assert residual>=F(d-k,2*a)
            selected.append(best[1]);volume=best[0]
        assert volume>=theta
        exchanges=0
        while True:
            changed=False
            for i in range(d):
                for j in range(a):
                    if j in selected:continue
                    candidate=selected[:];candidate[i]=j
                    v=det(gram(Q,candidate))
                    if v>2*volume:
                        selected=candidate;volume=v;exchanges+=1;changed=True;break
                if changed:break
            if not changed:break
        true_volume=det(gram(P,selected));ratios=[]
        for i in range(d):
            for j in range(a):
                if j in selected:continue
                candidate=selected[:];candidate[i]=j
                ratio=det(gram(P,candidate))/true_volume;ratios.append(ratio)
                assert ratio<=3
        true_gram=np.array(gram(P,selected),dtype=float)
        lower=float(np.linalg.eigvalsh(true_gram)[0])
        assert lower>=1/H-TOL
        greedy_cases.append({"a":a,"d":d,"exchanges":exchanges,
                             "min_true_Gram":lower,"public_lower":1/H,
                             "max_true_replacement_ratio":float(max(ratios)),
                             "exact_determinant_tests":True})

assert min(kinetic_margins)>-TOL
assert min(defect_margins)>-TOL
assert max(equalities)<TOL
assert max(orbit_errors)<TOL
out={"status":"FINITE-EVIDENCE: scoped small matrix refinements",
     "K_form_cases":len(kinetic_margins),"min_kinetic_margin":min(kinetic_margins),
     "min_defect_margin":min(defect_margins),"m2_identity_cases":len(equalities),
     "max_m2_identity_error":max(equalities),"max_contact_orbit_error":max(orbit_errors),
     "whole_rank_cases":rank_checks,"greedy_cases":greedy_cases,
     "checks_passed":True,
     "excludes":["Continuum proof validation","Large-n acquisition/circuit",
                 "Useful global localizer threshold","External validation","Novelty clearance"]}
Path(__file__).with_name("refinements_checks.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
