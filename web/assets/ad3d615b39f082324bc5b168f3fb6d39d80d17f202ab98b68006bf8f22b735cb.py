"""Exact finite-data distance-envelope feasibility for nondecreasing DE density.

This computes numerical feasible fits, not certified global minima or p-values.
It treats the published compressed BAO quantities as point measurements.
Flat FLRW; conserved dust; positive nondecreasing separately conserved DE;
radiation is optional and is parametrized in the same scaled h^2 units.
"""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parent
raw=np.loadtxt(ROOT/'data/desi_gaussian_bao_ALL_GCcomb_mean.txt',dtype=str)
z=raw[:,0].astype(float);d=raw[:,1].astype(float);kind=raw[:,2]
C=np.loadtxt(ROOT/'data/desi_gaussian_bao_ALL_GCcomb_cov.txt');W=np.linalg.inv(C)
zn=np.unique(z);n=len(zn);left=np.r_[0,zn[:-1]]
ix=np.searchsorted(zn,z)
xg,wg=leggauss(48)
xmid=(zn+left)/2;xhalf=(zn-left)/2
zg=xmid[:,None]+xhalf[:,None]*xg
wg=xhalf[:,None]*wg

def unpack(p):
    return p[0],p[1:1+n],p[1+n:1+2*n]

def predict(p,radiation=0.):
    alpha,b,dm=unpack(p)
    dh=np.sqrt(1000/(alpha*(1+zn)**3+radiation*(1+zn)**4+b))
    dv=np.cbrt(zn*dm**2*dh)
    arr={'DH_over_rs':dh,'DM_over_rs':dm,'DV_over_rs':dv}
    return np.array([arr[k][j] for k,j in zip(kind,ix)])

def cost(p,radiation=0.):
    r=predict(p,radiation)-d
    return float(r@W@r)

def constraint(p,radiation=0.):
    alpha,b,dm=unpack(p)
    bb=np.r_[0.,b[:-1]]
    known=alpha*(1+zg)**3+radiation*(1+zg)**4
    lo=np.sum(wg*np.sqrt(1000/(known+b[:,None])),axis=1)
    hi=np.sum(wg*np.sqrt(1000/(known+bb[:,None])),axis=1)
    diff=np.diff(np.r_[0,dm])
    return np.r_[np.diff(b), diff-lo,hi-diff]

def fit(alpha=None,radiation=0.,starts=4,seed=328):
    base=np.load(ROOT/'results/baseline.npz'); om,t=base['lcdm_parameters']
    alpha0=om/t**2*1000 if alpha is None else alpha
    b0=np.ones(n)*(1-om)/t**2*1000
    from scipy.integrate import quad
    mm=np.array([quad(lambda x:np.sqrt(1000/(alpha0*(1+x)**3+radiation*(1+x)**4+b0[0])),0,zz)[0] for zz in zn])
    p0=np.r_[alpha0,b0,mm]
    bounds=[(.0001,.6) if alpha is None else (alpha,alpha)]+[(1e-7,30)]*n+[(.01,80)]*n
    rng=np.random.default_rng(seed);allres=[]
    for i in range(starts):
        pp=p0.copy()
        if i:
            pp[1:1+n]=np.sort(b0*rng.uniform(.6,1.4,n))
        rr=minimize(lambda x:cost(x,radiation),pp,method='SLSQP',bounds=bounds,
            constraints=[{'type':'ineq','fun':lambda x:constraint(x,radiation)}],
            options={'maxiter':2000,'ftol':1e-10,'disp':False})
        allres.append(rr)
    feasible=[r for r in allres if np.min(constraint(r.x,radiation))>=-2e-7]
    if not feasible: raise RuntimeError([(r.fun,r.message,np.min(constraint(r.x,radiation))) for r in allres])
    best=min(feasible,key=lambda r:r.fun)
    return {'alpha':float(best.x[0]),'chi2':float(best.fun),'parameters':best.x.tolist(),
        'min_constraint':float(np.min(constraint(best.x,radiation))),'success':bool(best.success),
        'message':str(best.message),'prediction':predict(best.x,radiation).tolist(),
        'runs':[{'chi2':float(r.fun),'success':bool(r.success),'min_constraint':float(np.min(constraint(r.x,radiation)))} for r in allres]}
if __name__=='__main__':
    out=[]
    for a in [None,.30,.32,.34,.345,.35,.36,.38]:
        r=fit(alpha=a);out.append(r)
        print('alpha',a,'best',r['alpha'], 'chi2',r['chi2'],'feas',r['min_constraint'], 'success',r['success'],flush=True)
        print('b=',r['parameters'][1:1+n],flush=True)
    (ROOT/'results/envelope_fits.json').write_text(json.dumps(out,indent=2))
