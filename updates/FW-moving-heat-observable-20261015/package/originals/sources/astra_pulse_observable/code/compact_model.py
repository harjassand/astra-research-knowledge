"""Observable-weighted positive-RC closure, including ideal capacitive endpoint.
Input units: Hz, mOhm; response: mOhm. Inductance coefficient unrestricted.
The grid optimizer is exploratory until its continuum dual is checked.
"""
from pathlib import Path
import numpy as np
from scipy.optimize import linprog, nnls
BASE=Path(__file__).resolve().parents[1]
F0=.01; F1=1.; R1=F1/F0; CINF=1.-1./R1**2

def features(s, f):
 s=np.asarray(s,float); q=1.-s; r=np.asarray(f,float)[:,None]/F0
 d1=q*q+s*s; dH=q*q+(R1*s)**2; B=q**3+s*s*(R1**2-s)
 dr=q*q+(r*s)**2
 fac=d1*dH/(dr*B)
 return fac*(q-1j*r*s)

def target(s,t):
 s=np.asarray(s,float); q=1.-s
 d1=q*q+s*s; dH=q*q+(R1*s)**2; B=q**3+s*s*(R1**2-s)
 a=2*np.pi*F0*t
 out=np.empty_like(s); left=s<=.5; right=~left
 with np.errstate(divide='ignore',invalid='ignore'):
  u=a*q[left]/s[left]; out[left]=-np.expm1(-u)*d1[left]*dH[left]/(q[left]*B[left])
  u=a*q[right]/s[right]; exprel=np.ones_like(u); z=u!=0; exprel[z]=-np.expm1(-u[z])/u[z]
  out[right]=a*d1[right]*dH[right]/(s[right]*B[right])*exprel
 return out

def make_problem(fmax=1000.,n=1000,eps=.1):
 d=np.loadtxt(BASE/'data/cell_001_eis.csv',delimiter=',',skiprows=1)
 d=d[d[:,0]<=fmax]; f,zr,zi=d.T; y=np.r_[zr,zi]*1000
 x=np.geomspace(1e-10,1e10,n); s=np.r_[0.,x/(1+x),1.]
 F=features(s,f); A=np.vstack([F.real,F.imag])
 # Choose the coefficient in mOhm per unit normalized frequency, unrestricted.
 lcol=np.r_[np.zeros(len(f)),f/f.max()]
 A=np.column_stack([A,lcol]); ncoef=A.shape[1]
 bounds=[(0,None)]*(ncoef-1)+[(None,None)]
 phi=np.zeros(len(y)); i0=np.argmin(abs(f-F0)); i1=np.argmin(abs(f-F1))
 assert f[i0]==F0 and f[i1]==F1
 phi[i0]=1.; phi[len(f)+i0]=-1.; phi[len(f)+i1]=F0/F1
 assert np.max(abs(phi@A-np.r_[np.ones(ncoef-1),0.]))<1e-12
 return s,f,A,y,bounds,phi

def solve(t,fmax=1000,n=1000,eps=.1):
 s,f,A,y,bounds,phi=make_problem(fmax,n,eps); q=np.r_[target(s,t),0.]
 opts={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9}
 rr=[]
 for sign in [1,-1]:
  r=linprog(sign*q,A_ub=np.r_[A,-A],b_ub=np.r_[y+eps,-y+eps],bounds=bounds,method='highs-ds',options=opts)
  if not r.success: raise RuntimeError(r.message)
  m=len(y); v=sign*(r.ineqlin.marginals[:m]-r.ineqlin.marginals[m:])
  rr.append({'lp_objective_mohm':float(sign*r.fun),'weights':v.tolist(),'primal':r.x.tolist(),'max_residual_mohm':float(np.max(abs(A@r.x-y))),'nonzero_modes':int(np.count_nonzero(r.x[:-1]>1e-9))})
 # NNLS with signed inductance implemented through positive and negative columns.
 nnA=np.column_stack([A,-A[:,-1]])
 xb,res=nnls(nnA,y,maxiter=30000); pred=q@xb[:-1]
 return {'time_s':t,'fmax_hz':fmax,'n_nodes':len(s),'eps_mohm':eps,'frequencies':f.tolist(),'lower':rr[0],'upper':rr[1], 'mass_upper_mohm':float(phi@y+eps*np.sum(abs(phi))),'baseline_prediction_mohm':float(pred),'baseline_max_residual_mohm':float(np.max(abs(nnA@xb-y))), 'nodes':s.tolist()}
if __name__=='__main__':
 import time,json
 t0=time.perf_counter(); runs=[]
 for n in [600,1600]:
  for t in [10.,1000.]:
   r=solve(t,n=n); runs.append(r)
   print(n,t,r['lower']['lp_objective_mohm'],r['upper']['lp_objective_mohm'],r['baseline_prediction_mohm'], flush=True)
 (BASE/'results/compact_lp.json').write_text(json.dumps(runs,indent=2))
 print('elapsed_seconds',time.perf_counter()-t0)
