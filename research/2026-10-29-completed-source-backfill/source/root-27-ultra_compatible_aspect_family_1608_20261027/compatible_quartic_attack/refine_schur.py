"""P1-compatible prolongation and Schur-ratio descent on refined meshes."""
import json,time,numpy as np
from scipy.optimize import minimize
from compatible_core import ROOT
from search_fem import FEMProblem
from search_schur_ratio import objective

def prolong(nodes):
 a=np.array(nodes);n=a.shape[0];out=np.empty((2*n,2*n,2))
 for i in range(2*n):
  for j in range(2*n):
    I=i//2;J=j//2;x=(i%2)/2;y=(j%2)/2
    v0=a[I,J];v1=a[(I+1)%n,J];v2=a[(I+1)%n,(J+1)%n];v3=a[I,(J+1)%n]
    out[i,j]=(1-x)*v0+(x-y)*v1+y*v2 if y<=x else(1-y)*v0+x*v2+(y-x)*v3
 return out

def run():
 source=json.loads((ROOT/'data/schur_ratio_search.json').read_text())
 current=min((r for r in source['runs']if r['kind']=='fem'),key=lambda r:r['Delta_over_c'])
 out={'status':'COMPATIBLE_REFINEMENT_NUMERICAL_NO_JENSEN_VIOLATION_CERTIFIED','initial':current,'levels':[]};rng=np.random.default_rng(1927)
 for n in [32,64,128]:
    p=FEMProblem(n,False);seed=prolong(current['normalized_nodes']).ravel()
    inherited=objective(p,seed)[0];assert abs(inherited-current['Delta_over_c'])<1e-10
    runs=[]
    for k in range(3 if n<128 else 2):
      x=seed if k==0 else seed+.015*np.linalg.norm(seed)/np.sqrt(len(seed))*rng.normal(size=len(seed))
      start=time.monotonic();opt=minimize(lambda z:objective(p,z),x,jac=True,method='L-BFGS-B',options=dict(maxiter=3000,ftol=1e-14,gtol=2e-10,maxls=50,maxcor=30))
      rec=p.evaluate(opt.x,True);rec.update(Delta_over_c=float(objective(p,opt.x)[0]),start=k,iterations=int(opt.nit),seconds=time.monotonic()-start)
      runs.append(rec);print(n,k,rec['Delta_over_c'],rec['objective_scaled'],rec['gradient_norm'],rec['seconds'],flush=True)
    current=min(runs,key=lambda r:r['Delta_over_c']);out['levels'].append({'n':n,'prolonged_ratio':inherited,'runs':runs,'best_start':current['start']})
    (ROOT/'data/schur_refinement.json').write_text(json.dumps(out,indent=2))
 return out
if __name__=='__main__':run()
