"""Second operation: choose a target-specific measurement interface, not a DRT.
Six-frequency linear estimators use the kernel and a declared 62.5 mOhm design
scale selected during cell-001 exploration. This is not a blinded prospective
design, nor globally optimal experimental design. The continuum guarantees do
not depend on that scale being correct for a future cell.
"""
import json,time,numpy as np
from scipy.optimize import linprog
from compact_model import BASE,features,target,make_problem
sets={
 'slow':[.01,.03325,.1105,.3675,1.222,4.062],
 'medium':[.1105,.3675,1.222,4.062,13.5,44.89],
 'fast':[1.,3.325,11.05,36.75,122.2,406.2]
}
x=np.geomspace(1e-12,1e12,3000); s=np.r_[0,x/(1+x),1.]
T=10.; eps=.1; nominal_q_scale=62.5
_,allf,_,y,_,_=make_problem()
records=[]
for name,flist in sets.items():
 start=time.perf_counter(); f=np.array(flist); m=len(f)
 z=features(s,f); h=target(s,T)
 K=np.column_stack([z.real.T,z.imag.T])/h[:,None]
 C=np.column_stack([K,-K]); n=2*m
 A=np.r_[np.column_stack([C,-np.ones(len(s))]),np.column_stack([-C,-np.ones(len(s))])]
 rhs=np.r_[np.ones(len(s)),-np.ones(len(s))]
 ell=np.r_[np.zeros(m),f/f.max()]; E=np.r_[ell,-ell,0.][None,:]
 obj=np.r_[np.full(2*n,eps/nominal_q_scale),1.]
 res=linprog(obj,A_ub=A,b_ub=rhs,A_eq=E,b_eq=[0.],bounds=(0,None),method='highs')
 assert res.success,res.message
 v=res.x[:n]-res.x[n:2*n]; eta=res.x[-1]
 indices=[int(np.argmin(abs(allf-fj))) for fj in f]
 assert all(allf[j]==fj for j,fj in zip(indices,f))
 small_y=np.r_[y[indices],y[len(allf)+np.array(indices)]]
 pred=v@small_y; noise=eps*sum(abs(v)); eta_guard=eta+1e-3
 lo=(pred-noise)/(1+eta_guard); hi=(pred+noise)/(1-eta_guard) if eta_guard<1 else None
 rec={'name':name,'time_s':T,'frequencies_hz':flist,'eta_grid':float(eta),'eta_guard':float(eta_guard),'noise_l1_gain':float(sum(abs(v))),'noise_error_mohm':float(noise),'estimate_mohm':float(pred),'provisional_interval_mohm':[float(lo),float(hi) if hi else None], 'one_period_each_seconds':float(np.sum(1/f)),'elapsed_seconds':time.perf_counter()-start,'weights':v.tolist(), 'design_scale_mohm':nominal_q_scale}
 # Full-length zero-padded representation for reusing the independent dual checker.
 padded=np.zeros(2*len(allf)); padded[indices]=v[:m]; padded[len(allf)+np.array(indices)]=v[m:]
 rec['certificate_input']={'time_s':T,'fmax_hz':1000.,'eps_mohm':eps,'frequencies':allf.tolist(),'lower':{'weights':(padded/(1+eta_guard)).tolist()},'upper':{'weights':(padded/(1-eta_guard)).tolist()}}
 records.append(rec)
 print({k:v for k,v in rec.items() if k not in ['weights','certificate_input']},flush=True)
(BASE/'results/probe_protocols.json').write_text(json.dumps(records,indent=2))
