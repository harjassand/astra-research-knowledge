#!/usr/bin/env python3
"""Finite stress check of analytic two-mode and monotone-effect theorems.
Not a proof; proofs are in PROOF_AND_SCOPE.md.
"""
import json
import numpy as np
rng=np.random.default_rng(5489)
two_mode_cases=0
for _ in range(300_000):
    pf,ps=sorted(rng.uniform(.001,.999,size=2),reverse=True)
    w=float(rng.uniform(.001,.999))
    aa=rng.uniform(size=2);bb=rng.uniform(size=2)
    d0=w*(aa[0]-bb[0])+(1-w)*(aa[1]-bb[1])
    d1=w*pf*(aa[0]-bb[0])+(1-w)*ps*(aa[1]-bb[1])
    if d0<0<d1:
        two_mode_cases+=1
        for k in (1,2,3,8,21,74,199):
            d=w*(aa[0]-bb[0])+(1-w)*(ps/pf)**k*(aa[1]-bb[1])
            assert d>0, (d0,d1,k,d)

monotone_cases=0
for _ in range(150_000):
    p=np.sort(rng.uniform(.02,.999,size=7))
    w=rng.dirichlet(np.ones(7))
    # monotone signed difference within [-.4,.4]
    diff=np.sort(rng.uniform(-.4,.4,size=7))
    d1=float(np.sum(w*p*diff))
    if d1>0:
        monotone_cases+=1
        for k in (1,2,3,8,21,74,199):
            assert float(np.dot(w, (p/p[-1])**k*diff))>= -1e-14

r={'random_seed':5489,'two_mode_total_draws':300000,'two_mode_sign_cases_tested':two_mode_cases,'monotone_effect_total_draws':150000,'monotone_effect_sign_cases_tested':monotone_cases,'horizons':[1,2,3,8,21,74,199],
'violations':0,'status':'Finite numerical diagnostics only, not proofs.'}
with open('producer-workspace/theorem_stress_results.json','w') as f:json.dump(r,f,indent=2)
print(r)
