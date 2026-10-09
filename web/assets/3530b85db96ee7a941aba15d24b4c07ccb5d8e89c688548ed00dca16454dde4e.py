"""Floating search: symmetric inward drift need not have detailed-balance lift."""
import json
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog

def point_cloud(n,d,rng):
    raw=rng.normal(size=(n,d)); raw/=np.linalg.norm(raw,axis=1)[:,None]
    mean=raw.mean(axis=0)
    centered=raw-mean
    cov=centered.T@centered/n
    ev,u=np.linalg.eigh(cov)
    return centered@(u@np.diag(ev**-.5)@u.T)

def search(seed=801,clouds=50,samples=1000,d=2,n=5):
    rng=np.random.default_rng(seed)
    for cloud in range(clouds):
        points=point_cloud(n,d,rng)
        hull=ConvexHull(points)
        facets=hull.equations
        incident=[(k,i) for k,facet in enumerate(facets) for i in range(n) if abs(facet[:-1]@points[i]+facet[-1])<1e-8]
        edges=[(i,j) for i in range(n) for j in range(i+1,n)]
        cols=[]
        for i,j in edges:
            col=np.zeros((n,d)); col[i]=points[i]-points[j]; col[j]=points[j]-points[i]; cols.append(col.ravel())
        matrix=np.array(cols).T
        for _ in range(samples):
            raw=rng.normal(size=(d,d)); rotation=np.linalg.qr(raw)[0]
            eigen=rng.uniform(0,1,d); eigen[0]=1
            drift=rotation@np.diag(eigen)@rotation.T
            tests=np.array([facets[k,:-1]@drift@points[i] for k,i in incident])
            if tests.min()<-1e-9: continue
            rhs=(points@drift.T/n).ravel()
            result=linprog(np.ones(len(edges)),A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs')
            if not result.success:
                dual=linprog(rhs,A_ub=-matrix.T,b_ub=np.zeros(len(edges)),bounds=[(-1,1)]*(d*n),method='highs')
                directed=[(i,j) for i in range(n) for j in range(n) if i!=j]
                directed_cols=[]
                for i,j in directed:
                    col=np.zeros(n*d+n); col[i*d:(i+1)*d]=points[i]-points[j]; col[n*d+i]=1;col[n*d+j]=-1;directed_cols.append(col)
                direct=linprog(np.ones(len(directed)),A_eq=np.array(directed_cols).T,b_eq=np.r_[rhs,np.zeros(n)],bounds=(0,None),method='highs')
                return dict(seed=seed,cloud=cloud,d=d,n=n,points=points.tolist(),drift=drift.tolist(),min_inward=float(tests.min()),farkas_pairing=float(dual.fun),farkas_vectors=dual.x.reshape(n,d).tolist(),farkas_min_monotonicity=float(np.min(matrix.T@dual.x)),status=result.message,stationary_directed=direct.message,directed_flows=direct.x.tolist() if direct.success else None)
    return None

if __name__=='__main__':
    out=search()
    if out is None:out=search(seed=802,clouds=100,samples=1000,d=3,n=7)
    print(json.dumps(out,indent=2))
