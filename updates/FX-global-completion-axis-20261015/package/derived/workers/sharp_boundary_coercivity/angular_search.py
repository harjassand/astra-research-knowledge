"""Critical-degree homogeneous compatible gradient search (exploratory).

phi(rho,theta)=rho**(1/2) h(theta).  A logarithmically long annulus makes
both energy and fourth norm proportional to its length in log rho.  Smooth
inner/outer cutoffs have bounded cost.  A zero angular energy would therefore
be a potential noncoercive sequence, but positive finite-search values prove
no continuum lower bound.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize

ap=argparse.ArgumentParser()
ap.add_argument('--r',type=float,default=-2.5)
ap.add_argument('--k',type=int,default=8)
ap.add_argument('--restarts',type=int,default=3)
ap.add_argument('--maxiter',type=int,default=1000)
args=ap.parse_args()
r=args.r
a,b,c,d=sp.symbols('a b c d'); xx=(a,b,c,d)
F=3*r/(8*(r+2))*((a-d)**2+(b+c)**2)**2+r*(r-1)*(a*a+c*c)**2/6+(a*d-b*c)**2+r*(a*a+c*c)*(a*d-b*c)
ff=sp.lambdify(xx,F,'numpy',cse=True)
gg=[sp.lambdify(xx,sp.diff(F,t),'numpy',cse=True) for t in xx]
N=4*(args.k+1)+1
theta=2*np.pi*np.arange(N)/N; cs=np.cos(theta);sn=np.sin(theta)
basis=[];labels=[]
for n in range(args.k+1):
    for trig in range(1 if n==0 else 2):
        val=np.cos(n*theta) if trig==0 else np.sin(n*theta)
        dv=-n*np.sin(n*theta) if trig==0 else n*np.cos(n*theta)
        for target in range(2):
            arr=np.zeros((N,4))
            arr[:,2*target]=.5*val*cs-dv*sn
            arr[:,2*target+1]=.5*val*sn+dv*cs
            basis.append(arr);labels.append((n,trig,target))
basis=np.array(basis)
def fun(co,details=False):
    A=np.einsum('k,knc->nc',co,basis)
    A2=(A*A).sum(axis=1);den=np.mean(A2*A2)
    E=np.mean(ff(*A.T)); val=E/den
    DF=np.array([g(*A.T)+np.zeros(N) for g in gg]).T
    jac=np.einsum('knc,nc->k',basis,DF-val*4*A2[:,None]*A)/N/den
    return ({'ratio':float(val),'energy':float(E),'fourth_norm':float(den),
             'gradient_norm':float(np.linalg.norm(jac))} if details else (val,jac))
rng=np.random.default_rng(20261015)
rec={'scope':'Numerical critical homogeneous angular search; no global proof',
     'r':r,'K':args.k,'grid':N,'labels':labels,'runs':[]}
best=None;start=time.monotonic()
for seed in range(args.restarts):
    co=rng.normal(size=len(basis)) if seed else np.array([
        1. if (n,trig,t) in [(1,0,0),(1,1,1)] else 0.
        for n,trig,t in labels])+rng.normal(size=len(basis))*.01
    opt=minimize(fun,co,jac=True,method='L-BFGS-B',
                 options={'maxiter':args.maxiter,'ftol':1e-14,'gtol':1e-9,
                          'maxls':40})
    item=dict(fun(opt.x,True),seed=seed,iterations=int(opt.nit),
              success=bool(opt.success),message=str(opt.message))
    print(json.dumps(item),flush=True);rec['runs'].append(item)
    if best is None or item['ratio']<best['ratio']:
        best=dict(item,coefficients=opt.x.tolist())
rec['best']=best;rec['elapsed_seconds']=time.monotonic()-start
out=Path(__file__).with_name(f'angular_r{r:g}_k{args.k}.json')
out.write_text(json.dumps(rec,indent=2)+'\n');print('saved',out,flush=True)
