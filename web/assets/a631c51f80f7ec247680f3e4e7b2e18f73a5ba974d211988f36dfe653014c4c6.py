"""Floating search only: inward symmetric linear drift vs reversible vertex flows."""
import json
import numpy as np
from scipy.optimize import linprog

def investigate(n, samples=1000, seed=901):
    rng=np.random.default_rng(seed+n)
    points=np.sqrt(2)*np.array([[np.cos(2*np.pi*i/n),np.sin(2*np.pi*i/n)] for i in range(n)])
    normals=np.array([[np.cos(2*np.pi*(i+.5)/n),np.sin(2*np.pi*(i+.5)/n)] for i in range(n)])
    edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    columns=[]
    for i,j in edges:
        col=np.zeros((n,2)); col[i]=points[i]-points[j]; col[j]=points[j]-points[i]; columns.append(col.ravel())
    matrix=np.array(columns).T
    count=0
    for _ in range(samples):
        angle=rng.uniform(0,np.pi); ratio=rng.uniform(0,1)
        v=np.array([np.cos(angle),np.sin(angle)])
        drift=np.eye(2)-(1-ratio)*np.outer(v,v)
        tests=np.array([normals[i]@drift@points[j] for i in range(n) for j in [i,(i+1)%n]])
        if tests.min()<-1e-10: continue
        count+=1
        rhs=(points@drift.T/n).ravel()
        result=linprog(np.ones(len(edges)),A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs')
        if not result.success:
            # Homogeneous Farkas separator with fixed bounded dual variables.
            dual=linprog(rhs,A_ub=-matrix.T,b_ub=np.zeros(len(edges)),bounds=[(-1,1)]*(2*n),method='highs')
            return dict(n=n,feasible_inward_count=count,drift=drift.tolist(),minimum_inward=float(tests.min()),status=result.message,dual=dual.x.tolist() if dual.success else None,dual_pairing=float(dual.fun) if dual.success else None)
    return dict(n=n,feasible_inward_count=count,counterexample=None)

if __name__=='__main__':
    out=[investigate(n,10000) for n in [5,6,7,8,9,10,12,16]]
    print(json.dumps(out,indent=2))
