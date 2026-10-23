"""Bounded fixed-intertwiner graph sparsification from frozen V2.

This discovery script emits floating support candidates. The exact certificate
and component audit are separate; a solver success is not their substitute.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from fractions import Fraction as F

DIRECTORY=Path(__file__).resolve().parent
data=json.loads((DIRECTORY/'AUTONOMOUS_ESCAPE_RATIONAL_V2_CERTIFICATE.json').read_text())
n=data['n'];u=np.array([[float(F(x)) for x in row] for row in data['U']])
k=np.array([[float(F(x)) for x in row] for row in data['K']]);a=float(F(data['a']))
edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
aa=np.zeros((5*n-1,len(edges)))
for e,(i,j) in enumerate(edges):
    aa[4*i:4*i+4,e]=u[j]-u[i]
    if i<n-1:aa[4*n+i,e]+=1
    if j<n-1:aa[4*n+j,e]-=1
bb=np.r_[(u@(k-a*np.eye(4))).reshape(-1),np.zeros(n-1)]
records=[]
rng=np.random.default_rng(2026102381)
for attempt in range(12):
    objective=np.ones(len(edges)) if attempt==0 else np.exp(rng.normal(size=len(edges))*.5)
    out=linprog(objective,A_eq=aa,b_eq=bb,bounds=(0,None),method='highs',
                options={'primal_feasibility_tolerance':1e-10,
                         'dual_feasibility_tolerance':1e-10,'time_limit':20.})
    record={'attempt':attempt,'success':bool(out.success),'message':str(out.message)}
    if out.success:
        indices=np.flatnonzero(out.x>1e-9)
        _,rr,rowpivots=qr(aa[:,indices].T,mode='economic',pivoting=True)
        singular=np.linalg.svd(aa[:,indices],compute_uv=False)
        record.update({'objective':float(out.fun),'support_count':int(len(indices)),
                       'min_positive':float(np.min(out.x[indices])),
                       'max_residual':float(np.max(np.abs(aa@out.x-bb))),
                       'active_min_singular':float(singular[-1]),
                       'active_singular_tail':singular[-8:].tolist(),
                       'support':[list(edges[index]) for index in indices],
                       'values':out.x[indices].tolist(),
                       'independent_row_order':rowpivots.tolist()})
        (DIRECTORY/f'AUTONOMOUS_SPARSE_FLOAT_{attempt}.json').write_text(json.dumps(record,indent=2))
    records.append(record)
    print(json.dumps({k:v for k,v in record.items() if k not in ['support','values','independent_row_order']}),flush=True)
(DIRECTORY/'AUTONOMOUS_SPARSE_FLOAT_RESULTS.json').write_text(json.dumps(records,indent=2))
