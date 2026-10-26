"""Strong ordinary comparator over arbitrary piecewise resistance curves.

The ratio-constrained, mean-normalized formulation is a convex QP.
The optimizer receives no analytic threshold location.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import minimize,LinearConstraint
from switch_stress import frontier

OUT=Path(__file__).resolve().parent


def gram(grid):
    n=len(grid)
    ends=np.r_[grid[1:],np.inf]
    delta=ends-grid
    b=np.exp(-grid)-np.exp(-ends)
    m=np.zeros((n,n))
    for i in range(n):
        if np.isfinite(delta[i]):
            d=delta[i]
            m[i,i]=2*np.exp(-grid[i])*(-np.expm1(-d)-d*np.exp(-d))
        else:m[i,i]=2*np.exp(-grid[i])
        for j in range(i+1,n):
            m[i,j]=m[j,i]=delta[i]*b[j]
    return m,b


def one_qp(k,grid,previous=None):
    m,b=gram(grid);n=len(b)
    # x(s)=a(s)/mean; l<=x_i<=K*l encodes the resource contrast.
    lo=np.zeros((n,n+1));lo[:,:n]=np.eye(n);lo[:,-1]=-1
    hi=np.zeros((n,n+1));hi[:,:n]=-np.eye(n);hi[:,-1]=k
    c=np.vstack((lo,hi))
    eq=np.r_[b,0.][None,:]
    cons=[LinearConstraint(c,0,np.inf),LinearConstraint(eq,[1.],[1.])]
    def fun(q):return float(np.sum(q[:-1,None]*m*q[None,:-1]))
    def jac(q):return np.r_[2*np.sum(m*q[None,:-1],axis=1),0.]
    if previous is None:
        init=np.r_[np.ones(n),1/k]
    else:
        old_grid=np.asarray(previous['grid'])
        old_x=np.asarray(previous['normalized_resistance'])
        jj=np.searchsorted(old_grid,grid,side='right')-1
        init=np.r_[old_x[jj],previous['contrast_lower']]
        init/=np.sum(b*init[:-1])
    res=minimize(fun,init,jac=jac,method='SLSQP',constraints=cons,
                 bounds=[(0,None)]*(n+1),
                 options={'ftol':5e-13,'maxiter':1200})
    x=res.x[:-1]
    return dict(cv2=float(res.fun-1),success=bool(res.success),message=res.message,
                iterations=int(res.nit),mean_residual=float(np.sum(b*x)-1),
                inequality_min=float(min(np.min(x-res.x[-1]),np.min(k*res.x[-1]-x))),grid=grid.tolist(),
                normalized_resistance=x.tolist(),contrast_lower=float(res.x[-1]))


if __name__=='__main__':
    t=time.perf_counter();rows=[]
    for k in [7.,111.,1000.]:
        grid=np.r_[0.,np.geomspace(1e-5,10.,64)]
        history=[]
        for iteration in range(4):
            r=one_qp(k,grid,previous=history[-1] if history else None)
            history.append(r)
            x=np.asarray(r['normalized_resistance'])
            # Refine around the strongest transitions found by this optimizer.
            jumps=np.abs(np.diff(np.log(np.maximum(x,1e-20))))
            chosen=np.argsort(jumps)[-4:]
            additions=[]
            for j in chosen:
                if j>0:additions.append((grid[j-1]+grid[j])/2)
                additions.append((grid[j]+grid[j+1])/2)
                if j+2<len(grid):additions.append((grid[j+1]+grid[j+2])/2)
            grid=np.unique(np.r_[grid,additions])
        rows.append(dict(k=k,ideal_lower_cv2=frontier(k)[0],history=history))
    result=dict(scope='Convex finite-bin same-information ordinary comparison, no physical measurements.',
                results=rows,wall_seconds=time.perf_counter()-t)
    (OUT/'ordinary_curve_qp_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps([dict(k=r['k'],ideal=r['ideal_lower_cv2'],
                            best=r['history'][-1]['cv2'],
                            success=r['history'][-1]['success'],
                            residual=r['history'][-1]['mean_residual'],
                            min_constraint=r['history'][-1]['inequality_min']) for r in rows],indent=2))
