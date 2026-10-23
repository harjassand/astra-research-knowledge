"""Exact linear Schumann-model periodic thermal gate, not a reacting device result.
Finite gas/solid conductance; negligible gas inventory, axial conduction/loss,
constant gas cp, equal hot/cold mass-flow and duration. Solid state reset exactly.
Mesh convergence essential: few isothermal lumps can fake an advantage.
"""
import json,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import expm,solve
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent

def phase(N,NTU,direction,b,axial=0.):
 a=np.exp(-NTU/N);B=np.zeros((N,N));f=np.zeros(N)
 # Dimensionless time = m_dot cp_g t / C_s_total.
 for i in range(N):
  B[i,i]=-N*(1-a)
  for j in range(i):B[i,j]=N*(1-a)**2*a**(i-1-j)
  f[i]=N*(1-a)*a**i
 if direction=='cold':B=B[::-1,::-1];f=np.zeros(N)
 if axial:
  lap=np.diag(np.r_[-1.,np.full(N-2,-2.),-1.])+np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)
  B+=axial*N*N*lap
 # affine map and exact integral of gas outlet temperature over a blow
 E=np.zeros((N+2,N+2));E[:N,:N]=B;E[:N,N]=f
 weights=(1-a)*a**np.arange(N-1,-1,-1)
 E[-1,:N]=weights if direction=='hot' else weights[::-1]
 E[-1,N]=a**N if direction=='hot' else 0
 M=expm(E*b)
 return M,E

def run(N,NTU,b,trace=False,axial=0.):
 H,Eh=phase(N,NTU,'hot',b,axial);C,Ec=phase(N,NTU,'cold',b,axial)
 A=C[:N,:N]@H[:N,:N];bias=C[:N,:N]@H[:N,N]+C[:N,N]
 x0=solve(np.eye(N)-A,bias);x1=H[:N,:N]@x0+H[:N,N];x2=C[:N,:N]@x1+C[:N,N]
 hotavg=(H[-1,:N]@x0+H[-1,N])/b;coldavg=(C[-1,:N]@x1+C[-1,N])/b
 # Stored temperature extrema may be interior; sample then tighten independently.
 states=[]
 for E,x in [(Eh,x0),(Ec,x1)]:
  for s in np.linspace(0,b,9):states.append((expm(E*s)@np.r_[x,1.,0.])[:N])
 maximum=float(np.max(states));minimum=float(np.min(states));out={'axial':axial,'N':N,'NTU':NTU,'blow_ratio':b,'effectiveness':float(coldavg),'hot_out_mean_theta':float(hotavg),'maximum_solid_theta_sampled':maximum,'minimum_solid_theta_sampled':minimum,'periodic_reset_max':float(abs(x2-x0).max()),'energy_balance_residual':float(1-hotavg-coldavg)}
 if trace:out['start_profile']=x0.tolist();out['after_hot_profile']=x1.tolist()
 return out
if __name__=='__main__':
 t=time.monotonic();rows=[]
 for N in [10,40,100]:
  for b in [.001,.03,.3]:
   # Finite cycle point at continuum hot-face limit NTU chosen for epsilon~.57.
   for ntu in [1.,2.,4.,8.]:
    r=run(N,ntu,b,True);rows.append(r);print(N,b,ntu,r['effectiveness'],300+2800*r['maximum_solid_theta_sampled'],flush=True)
 result={'scope':__doc__,'hot_K':3100,'cold_K':300,'solid_limit_K':2500,'rows':rows,'wall_s':time.monotonic()-t,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(ROOT/'thermal_gate.json').write_text(json.dumps(result,indent=2)+'\n')
