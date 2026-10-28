"""Restricted covariance-diversity search followed by unconstrained release.

The restriction is not WLOG. It avoids repeatedly landing on the known
rank<=2 compatible classes while looking for a genuinely coupled profile.
"""
import json,time,argparse
import numpy as np
import scipy.sparse as ss
from scipy.optimize import minimize
from compatible_core import FourierProblem,half_square,ROOT
from search_fem import FEMProblem

def penalized(problem,p,threshold,weight,info=False):
 obj,g=problem.evaluate(p);norm=np.linalg.norm(p);q=p/norm
 sparse=ss.issparse(problem.design)
 x=(problem.design@q).reshape(-1,4)if sparse else np.einsum('npi,p->ni',problem.design,q)
 C=x.T@x/problem.N;s=np.trace(C);t=np.trace(C@C);diversity=1-t/s**2
 d=max(0,threshold-diversity);v=4*x@(t*np.eye(4)/s**3-C/s**2)
 dgq=problem.design.T@v.reshape(-1)/problem.N if sparse else np.einsum('npi,ni->p',problem.design,v)/problem.N
 dg=(dgq-q*np.dot(q,dgq))/norm
 if info:return float(diversity),float(obj)
 return obj+weight*d*d,g-2*weight*d*dg

def run(kind='fourier',size=3,starts=6):
 problem=FourierProblem(half_square(size))if kind=='fourier'else FEMProblem(size,False)
 dim=4*problem.m if kind=='fourier'else 2*size*size;rng=np.random.default_rng(861+size)
 out={'status':'RESTRICTED_DIVERSITY_SEARCH_NOT_A_GLOBAL_REDUCTION','diversity':'1-tr(C²)/tr(C)²','runs':[]}
 path=ROOT/f'data/diverse_{kind}{size}.json'
 for threshold in [.55,.65,.72]:
  for k in range(starts):
    start=time.monotonic();p=rng.normal(size=dim)
    for weight in [10,100,1000]:
      opt=minimize(lambda z:penalized(problem,z,threshold,weight),p,jac=True,method='L-BFGS-B',options=dict(maxiter=1000,ftol=1e-13,gtol=2e-9,maxls=50,maxcor=20));p=opt.x
    retained=problem.evaluate(p,True);retained['diversity']=penalized(problem,p,threshold,0,True)[0]
    release=minimize(problem.evaluate,p,jac=True,method='L-BFGS-B',options=dict(maxiter=1500,ftol=1e-14,gtol=2e-10,maxls=50,maxcor=20))
    final=problem.evaluate(release.x,True);final['diversity']=penalized(problem,release.x,threshold,0,True)[0]
    r=dict(threshold=threshold,start=k,retained=retained,released=final,seconds=time.monotonic()-start)
    out['runs'].append(r);path.write_text(json.dumps(out,indent=2));print(kind,size,threshold,k,retained['objective_scaled'],retained['diversity'],final['objective_scaled'],r['seconds'],flush=True)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=['fourier','fem'],default='fourier');p.add_argument('--size',type=int,default=3);p.add_argument('--starts',type=int,default=6);a=p.parse_args();run(a.kind,a.size,a.starts)
