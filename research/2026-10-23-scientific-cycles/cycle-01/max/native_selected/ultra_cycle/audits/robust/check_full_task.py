#!/usr/bin/env python3
"""Bounded independent formula checks; analytic proof is in RESULT.txt."""
import json
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path
import numpy as np

started = time.perf_counter()
cpu_started = time.process_time()
rng = np.random.default_rng(2026102104)
weights = [(1.0, 1.0), (0.0, 1.0), (1.7, 0.2), (0.3, 1.4)]
records = []
max_excess = -float("inf")
max_sharp_residual = 0.0
max_purity_violation = -float("inf")
max_rank_one_joint_violation = -float("inf")

def ptr(x, q, a):
    z = x.reshape(q, q, q, q)
    return np.einsum("abad->bd", z) if a == 1 else np.einsum("abcb->ac", z)

def scores(x, q):
    return [float(np.linalg.norm(ptr(x, q, a), "fro")**2 / q) for a in (1, 2)]

for q in (2, 3, 4):
    n = q*q
    for m in range(1, q+1):
        for sample in range(25):
            lam = rng.dirichlet(np.ones(m))
            ra = (rng.normal(size=(n,m)) + 1j*rng.normal(size=(n,m)))
            rb = (rng.normal(size=(n,m)) + 1j*rng.normal(size=(n,m)))
            ua = np.linalg.qr(ra, mode="reduced")[0]
            ub = np.linalg.qr(rb, mode="reduced")[0]
            x = (ua*np.sqrt(lam)) @ ub.conj().T
            p1, p2 = scores(x,q)
            renyi = float(np.sqrt(lam).sum()**2)
            for a,b in weights:
                excess = q*(a*p1+b*p2) - (max(a,b)*renyi+min(a,b))
                max_excess = max(max_excess, excess)
                assert excess < 2e-11
            # Positive sharpness representatives: all Schmidt spectrum on
            # either one complete task, the other coefficient |0><0|.
            diag = np.diag(np.r_[np.sqrt(lam), np.zeros(q-m)])
            zero = np.zeros((q,q)); zero[0,0]=1
            sharp = [np.kron(diag,zero), np.kron(zero,diag)]
            for a,b in weights:
                best = max(q*(a*scores(y,q)[0]+b*scores(y,q)[1]) for y in sharp)
                res = abs(best-(max(a,b)*renyi+min(a,b)))
                max_sharp_residual=max(max_sharp_residual,res)
                assert res < 2e-11
            # Auxiliary positive matrix and explicit two-copy purity identity.
            sigma=(ua*np.sqrt(lam)) @ ua.conj().T / np.sqrt(lam).sum()
            pur=lambda z: float(np.trace(z@z).real)
            purity_excess=pur(ptr(sigma,q,1))+pur(ptr(sigma,q,2))-1-pur(sigma)
            max_purity_violation=max(max_purity_violation,purity_excess)
            assert purity_excess<2e-11
            if m==1:
                joint=float(abs(np.trace(x))**2/q**2)
                joint_excess=q*(p1+p2)-q*q*joint-1
                max_rank_one_joint_violation=max(max_rank_one_joint_violation,joint_excess)
                assert joint_excess<2e-11
            records.append({"q":q,"rank":m,"sample":sample,"p1":p1,"p2":p2})

relaxation=[]
rectangle_count=0
for d,k in [(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(4,1),(4,2)]:
    t=d**k-1
    ell=t-k
    old={ (j,t-j):Fraction(1,t+1) for j in range(t+1) }
    new=dict(old)
    for oldpt,newpt in [((t,0),(t-1,0)),((0,t),(0,t-1))]:
        mass=new.pop(oldpt)
        new[newpt]=new.get(newpt,Fraction(0))+mass
    assert sum(new.values())==1
    for i in range(t+1):
        for j in range(t+1):
            tail=sum((w for (a,b),w in new.items() if a>=i and b>=j),Fraction(0))
            oldtail=Fraction(max(t-i-j+1,0),t+1)
            env=Fraction(1) if i+j<=ell else Fraction(1,d**(i+j-ell))
            assert tail<=oldtail<=env
            rectangle_count+=1
    tv=sum((abs(old.get(z,0)-new.get(z,0)) for z in set(old)|set(new)),Fraction(0))/2
    mean=sum((Fraction(a+b)*w for (a,b),w in new.items()),Fraction(0))
    assert tv==Fraction(2,t+1)
    assert mean==t-Fraction(2,t+1)
    assert all(not(a==t or b==t) for a,b in new)
    relaxation.append({"D":d,"k":k,"T":t,"L":ell,"TV":str(tv),"mean_sum":str(mean),"gap_in_logD":str(mean-ell)})

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes=int(rss if sys.platform=="darwin" else 1024*rss)
result={
    "status":"PASS_FINITE_FORMULA_CHECKS_ONLY",
    "python":sys.version.split()[0],"numpy":np.__version__,
    "random_pure_cases":len(records),"weights_per_case":len(weights),
    "max_random_bound_excess":max_excess,
    "max_sharpness_residual":max_sharp_residual,
    "max_purity_subadditivity_excess":max_purity_violation,
    "max_rank_one_joint_violation":max_rank_one_joint_violation,
    "exact_relaxation_rectangles":rectangle_count,
    "relaxation_cases":relaxation,
    "wall_seconds":time.perf_counter()-started,
    "cpu_seconds":time.process_time()-cpu_started,
    "max_rss_bytes":rss_bytes,
    "limitations":"No global optimization, physical realization of scalar data, EF additivity, asymptotic EC, or efficiency claim."
}
out=Path(__file__).resolve().parent/"FINITE_CHECKS.json"
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
