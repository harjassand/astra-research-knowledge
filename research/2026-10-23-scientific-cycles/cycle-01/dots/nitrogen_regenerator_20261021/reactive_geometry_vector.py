"""Conditional rapid-cycle reacting packed-bed geometry test.
Temperature-state collocation avoids inner enthalpy-inversion Newton failures.
Wakao gas films and stipulated opaque-black correlated-scattering Rosseland
transport are tied to the SAME particle diameter/porosity. This is NOT measured
finite-conductivity zirconia: lumped isothermal grains, insulated radiative ends,
no axial contact conduction, and rapid-cycle approximation remain explicit gates.
"""
import json,time,sys,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
import cantera as ct
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'nitrogen_quench_recovery_20261021'))
from paper_model import gas_model
sys.path.insert(0,str(ROOT/"vector_kernel"))
from kernel import Kernel
KERNEL=Kernel()
L=.1;G=1.;POR=.4;DP=.009525;P=ct.one_atm;HOT=3100.;SIGMA=5.670374419e-8
C2=1+1.5*(1-POR)-.75*(1-POR)**2;BETA=1.5*(1-POR)/DP*(2*C2-1);KR=16*SIGMA/(3*BETA)

def main():
 t=time.monotonic();h=gas_model();c=gas_model();c.TPX=300,P,{'N2':.79,'O2':.21};Yf=c.Y.copy();h0=c.enthalpy_mass;h.TPY=HOT,P,Yf;h.equilibrate('TP');Yh=h.Y.copy();hh=h.enthalpy_mass;idx=[h.species_index(s) for s in ['O2','N','O','NO','NO2']];ni=h.species_index('N2');W=h.molecular_weights
 def Y(z):
  y=np.zeros(6);y[idx]=z;y[ni]=1-sum(z);return y
 def uv(gas):
  Re=G*DP/gas.viscosity;Pr=gas.cp_mass*gas.viscosity/gas.thermal_conductivity;Nu=2+1.1*Re**.6*Pr**(1/3);return Nu*gas.thermal_conductivity/DP*6*(1-POR)/DP
 def bc(a,b):return np.r_[a[:5]-Yh[idx],a[5]-HOT/1000,b[6:11]-Yf[idx],b[11]-.3,a[13],b[13]]
 def rhs(zeta):
  def fun(x,y):
   out=np.empty_like(y)
   def ys(z):
    q=np.zeros((6,z.shape[1]));q[idx]=z;q[ni]=1-z.sum(axis=0);return q
   Th=np.clip(1000*y[5],200,3500);Tc=np.clip(1000*y[11],200,3500);Ts=np.maximum(200,1000*y[12])
   rh=KERNEL.evaluate(Th,ys(y[:5]));rc=KERNEL.evaluate(Tc,ys(y[6:11]))
   def u(r):
    Re=G*DP/r['viscosity'];Pr=r['cp']*r['viscosity']/r['conductivity']
    return (2+1.1*Re**.6*Pr**(1/3))*r['conductivity']/DP*6*(1-POR)/DP
   UH=(1-zeta)*96000+zeta*u(rh);UC=(1-zeta)*96000+zeta*u(rc);ks=(1-zeta)*12+zeta*KR*Ts**3
   dh=POR*rh['mass_production']/G;dc=-POR*rc['mass_production']/G
   out[:5]=dh[idx];out[5]=(-UH/G*(Th-Ts)-(rh['h_species']*dh).sum(axis=0))/rh['cp']/1000
   out[6:11]=dc[idx];out[11]=(UC/G*(Tc-Ts)-(rc['h_species']*dc).sum(axis=0))/rc['cp']/1000
   out[12]=-y[13]*1000/ks;out[13]=.5*(UH*(Th-Ts)+UC*(Tc-Ts))/1e6
   return out
  return fun
 old=np.load(ROOT/'reactive_continuation.npz');x=np.linspace(0,L,180);oldy=np.array([np.interp(x,old['x'],v) for v in old['y']]);y=oldy.copy()
 for j in range(len(x)):
  h.HPY=oldy[5,j]*1e6,P,Y(oldy[:5,j]);c.HPY=oldy[11,j]*1e6,P,Y(oldy[6:11,j]);y[5,j]=h.T/1000;y[11,j]=c.T/1000
 progress=[]
 for zeta in [0.,.25,.5,.75,1.]:
  st=time.monotonic();sol=solve_bvp(rhs(zeta),bc,x,y,tol=2e-4,max_nodes=6000)
  r={'geometry_homotopy':zeta,'success':sol.success,'message':sol.message,'nodes':len(sol.x),'rms_max':float(max(sol.rms_residuals)),'wall_s':time.monotonic()-st};progress.append(r);print(json.dumps(r),flush=True)
  (ROOT/'reactive_geometry_vector_progress.json').write_text(json.dumps(progress,indent=2)+'\n')
  if not sol.success:return
  x=sol.x;y=sol.y;np.savez_compressed(ROOT/'reactive_geometry_vector_checkpoint.npz',x=x,y=y,zeta=zeta)
 yy=sol.sol(np.linspace(0,L,801));NO=[];HC=[];HH=[]
 for j in range(yy.shape[1]):
  h.TPY=1000*yy[5,j],P,Y(yy[:5,j]);c.TPY=1000*yy[11,j],P,Y(yy[6:11,j]);NO.append(sum(1000*h[s].Y[0]/h[s].molecular_weights[0] for s in ['NO','NO2']));HH.append(h.enthalpy_mass);HC.append(c.enthalpy_mass)
 r={'scope':__doc__,'parameters':{'L_m':L,'G':G,'porosity':POR,'particle_diameter_m':DP,'radiation_beta_m_inv':BETA,'radiation_k_coefficient':KR},'peak_solid_K':float(max(1000*yy[12])),'cold_out_K':float(1000*yy[11,0]),'hot_out_K':float(1000*yy[5,-1]),'hot_survival':NO[-1]/NO[0],'retained_mol_NOx_kg':NO[-1],'gas_heat_MJ_mol_exchanger_out':float((hh-HC[0])/NO[-1]/1e6),'heat_balance_J_kg':float(hh-HH[-1]-HC[0]+h0),'max_boundary_residual':float(max(abs(bc(yy[:,0],yy[:,-1])))),'min_species':float(min(yy[:5].min(),yy[6:11].min())),'gas_T_range_K':[float(min(yy[5].min(),yy[11].min())*1000),float(max(yy[5].max(),yy[11].max())*1000)],'progress':progress,'wall_s':time.monotonic()-t,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(ROOT/'reactive_geometry_vector_result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
if __name__=='__main__':main()
