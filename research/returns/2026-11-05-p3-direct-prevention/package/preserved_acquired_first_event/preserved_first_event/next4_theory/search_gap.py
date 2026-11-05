import numpy as np
import cvxpy as cp
from itertools import combinations

def solve(a,b,x0,H=3,L=1.,consistent=True,objtype='linear',target=0.):
    n=1+H
    G=cp.Variable((n,n),symmetric=True)
    e=np.eye(n)
    def v(x): return float(x)*e[0]
    xx=[v(x0)]+[e[t] for t in range(1,H+1)]
    vertices=[(v(x),v(y)) for x,y in zip(a,b)]+list(zip(xx[:-1],xx[1:]))
    def Q(v): return np.outer(v,v)
    constraints=[G >>0,G[0,0]==1]
    matrices=[]
    for i,j in combinations(range(len(vertices)),2):
        if not consistent and min(i,j)>=len(a): continue
        x,y=vertices[i]; z,w=vertices[j]
        A=Q(y-w)-L*L*Q(x-z)
        constraints.append(cp.sum(cp.multiply(A,G))<=0)
        matrices.append((i,j,A))
    beta=abs(b[0]);R=abs(x0);cap=1.
    for t in range(H):
        R=beta+L*(R+abs(a[0]));cap+=R*R
    constraints.append(cp.trace(G)<=cap+1)
    if objtype=='linear': c=e[0]; C=(np.outer(c,e[-1])+np.outer(e[-1],c))/2
    else: C=Q(e[-1]-v(target))
    problem=cp.Problem(cp.Maximize(cp.sum(cp.multiply(C,G))),constraints)
    try: problem.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8,max_iter=300)
    except Exception: return None
    return problem.value,G.value,problem.status,[(i,j,float(c.dual_value)) for (i,j,A),c in zip(matrices,constraints[2:-1])]

if __name__=='__main__':
    rng=np.random.default_rng(146)
    best=[]
    for trial in range(120):
        count=rng.integers(2,5)
        a=np.arange(count,dtype=float)
        b=np.r_[rng.choice([-1.,0.,1.]),np.zeros(count-1)]
        b[1:]=b[0]+np.cumsum(rng.choice([-1.,-.5,0.,.5,1.],count-1))
        x0=rng.choice(np.arange(-1,5,.5))
        H=int(rng.choice([2,3,4]))
        full=solve(a,b,x0,H,consistent=True)
        relaxed=solve(a,b,x0,H,consistent=False)
        if full and relaxed and relaxed[0]-full[0]>.01:
            best.append((relaxed[0]-full[0],trial,a.tolist(),b.tolist(),x0,H,full[0],relaxed[0]))
    for row in sorted(best,reverse=True)[:20]: print(row)
