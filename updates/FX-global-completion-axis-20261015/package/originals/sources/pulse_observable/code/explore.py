from pathlib import Path
import numpy as np, time, json
from scipy.optimize import linprog, nnls
BASE=Path(__file__).resolve().parents[1]
d=np.loadtxt(BASE/'data/cell_001_eis.csv',delimiter=',',skiprows=1)
# All impedances and finite-time response per amp are measured in mOhm.
f,zr,zi=d.T; omega=2*np.pi*f
tau=np.geomspace(1e-9,1e10,800); w0=2*np.pi*.01; x=w0*tau
w=(1+x)/(1+x*x)
F=1/(1+1j*omega[:,None]*tau[None,:])/w[None,:]
# Ohmic, positive RC modes, ideal capacitor, and inductance (uH).
Ac=np.column_stack([np.ones(len(f)),F,w0/(1j*omega),1j*omega*1e-3])
A=np.vstack([Ac.real,Ac.imag]); b=np.r_[zr,zi]*1000
opts={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9}
records=[]
for fmax in [1e4,1e3,100]:
 mask=f<=fmax; sel=np.r_[mask,mask]; Am=A[sel]; bm=b[sel]
 t0=time.perf_counter()
 Ap=np.vstack([np.column_stack([Am,-np.ones(len(bm))]),np.column_stack([-Am,-np.ones(len(bm))])])
 rp=linprog(np.r_[np.zeros(A.shape[1]),1.],A_ub=Ap,b_ub=np.r_[bm,-bm],bounds=(0,None),method='highs',options=opts)
 assert rp.success, rp.message
 delta_min=rp.x[-1]
 print('fmax',fmax,'delta_min_mohm',delta_min,'n',sum(mask),flush=True)
 rb,residual=nnls(Am,bm,maxiter=10000)
 base={'fmax':fmax,'samples':int(sum(mask)),'delta_min_mohm':float(delta_min),'nnls_maxerr_mohm':float(np.max(abs(Am@rb-bm))),'nnls_l2err_mohm':float(residual)}
 for eps in [.02,.05,.1,.2,.5,1.]:
  if eps<delta_min-1e-7: continue
  for t in [1.,10.,100.,1000.,1e5]:
   q=np.r_[1.,-np.expm1(-t/tau)/w,t*w0,0.]
   lo=linprog(q,A_ub=np.r_[Am,-Am],b_ub=np.r_[bm+eps,-bm+eps],bounds=(0,None),method='highs',options=opts)
   hi=linprog(-q,A_ub=np.r_[Am,-Am],b_ub=np.r_[bm+eps,-bm+eps],bounds=(0,None),method='highs',options=opts)
   rr=base|{'eps_mohm':eps,'t_s':t,'min_mohm':float(lo.fun) if lo.success else None,'max_mohm':float(-hi.fun) if hi.success else None,'baseline_mohm':float(q@rb)}
   records.append(rr)
   if t in [10,1000]: print(rr,flush=True)
 print('elapsed',time.perf_counter()-t0,flush=True)
(BASE/'results/exploratory_grid_results.json').write_text(json.dumps(records,indent=2))
