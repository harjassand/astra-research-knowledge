"""Necessary scale-separation screen, not a finite-cycle solution or error bound.
Gas-inventory budget counts all bed gas as sacrificial at each reversal.
Frozen-profile thermal ripple neglects nonlinear evolution and intragrain gradients.
"""
import sys,json,time,resource
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'vector_kernel'));from kernel import Kernel
K=Kernel();m=json.loads((R/'vector_kernel/manifest.json').read_text());sp=list(K.species_names) if hasattr(K,'species_names') else ['N2','O2','N','O','NO','NO2']
# Use native mechanism ordering rather than assuming ordering.
sys.path.insert(0,str(R.parent/'nitrogen_quench_recovery_20261021'));from paper_model import gas_model
g=gas_model();idx=[g.species_index(s) for s in ['O2','N','O','NO','NO2']];ni=g.species_index('N2');G=1.;dp=.009525;por=.4
start=time.monotonic();out=[]
for name in ['radiating_2700','radfactor_0.2_2700','radfactor_0.05_2700']:
 z=np.load(R/(name+'_checkpoint.npz'));x=z['x'];y=z['y'];Ts=y[12]*1000
 def state(a,T):
  Y=np.zeros((6,a.shape[1]));Y[idx]=a;Y[ni]=1-a.sum(0);return K.evaluate(T,Y)
 h=state(y[:5],1000*y[5]);c=state(y[6:11],1000*y[11])
 def U(r):
  Re=G*dp/r['viscosity'];Pr=r['cp']*r['viscosity']/r['conductivity'];return (2+1.1*Re**.6*Pr**(1/3))*r['conductivity']/dp*6*(1-por)/dp
 Sh=U(h)*(1000*y[5]-Ts);Sc=U(c)*(1000*y[11]-Ts)
 # Mean source exactly cancelled by steady axial conduction. Phase residual is +/- (Sh-Sc)/2.
 imbalance=.5*(Sh-Sc);maxrate=float(max(abs(imbalance)))
 holdup=float(np.trapezoid(por*(h['rho']+c['rho']),x)/G)
 margin=float(2500-Ts.max());tau_min=holdup/.02
 # Centered sawtooth frozen-profile peak deviation = tau*maxrate/(2 Cvol).
 cv_req=tau_min*maxrate/(2*margin) if margin>0 else None
 # Bulk grain capacity would be rho_s*cp_s = Cvol/(1-por).
 out.append({'case':name,'max_Ts_K':float(Ts.max()),'margin_K':margin,'combined_gas_holdup_s':holdup,'minimum_blow_s_for_2percent_sacrificial_inventory':tau_min,'frozen_profile_max_phase_imbalance_W_m3':maxrate,'required_bulk_solid_rho_cp_J_m3_K_for_overlap':None if cv_req is None else cv_req/(1-por),'assumptions':['Not a proof that purge costs exactly this amount: deliberately counts all residual gas as lost in mass budget.','Centered frozen-source ripple formula is a scale screen only, not guaranteed nonlinear temperature bound.','Actual cyclic reset, surface chemistry, wall leakage, gas acceleration and intragrain temperatures remain unresolved.']})
r={'scope':__doc__,'cases':out,'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(R/'finite_period_window.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
