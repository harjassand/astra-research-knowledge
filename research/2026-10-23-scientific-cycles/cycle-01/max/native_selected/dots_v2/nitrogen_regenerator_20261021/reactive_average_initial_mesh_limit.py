"""Rapid-cycle averaged two-bed reacting model with passive axial solid conduction.
Conditional specified conductances, NOT a qualified zirconia device; no perfect
NO retention. Both gas streams react; hot/cold gas inventories are quasi-steady.
A full finite-period cycle and coupled property realization remain separate gates.
"""
import sys,time,json,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'nitrogen_quench_recovery_20261021'))
from paper_model import gas_model
import cantera as ct
L=.1;G=1.;POR=.4;UV=96000.;KS=12.;P=ct.one_atm

def main():
 start=time.monotonic();h=gas_model();c=gas_model();c.TPX=300,P,{'N2':.79,'O2':.21};Yfeed=c.Y.copy();hfeed=c.enthalpy_mass;h.TPY=3100,P,Yfeed;h.equilibrate('TP');Yhot=h.Y.copy();hhot=h.enthalpy_mass;W=h.molecular_weights;indices=[h.species_index(s) for s in ['O2','N','O','NO','NO2']];nit=h.species_index('N2');levels=[]
 def unpack(z):
  y=np.zeros(6);y[indices]=z;y[nit]=1-sum(z);return y
 def boundary(a,b):return np.r_[a[:5]-Yhot[indices],a[5]-hhot/1e6,b[6:11]-Yfeed[indices],b[11]-hfeed/1e6,a[13],b[13]]
 def system(alpha):
  def fun(x,y):
   out=np.empty_like(y)
   for j in range(len(x)):
    yh=unpack(y[:5,j]);yc=unpack(y[6:11,j]);h.HPY=y[5,j]*1e6,P,yh;c.HPY=y[11,j]*1e6,P,yc;Th=h.T;Tc=c.T;Ts=1000*y[12,j]
    out[:5,j]=alpha*POR*h.net_production_rates[indices]*W[indices]/G
    out[5,j]=-UV/G*(Th-Ts)/1e6
    out[6:11,j]=-alpha*POR*c.net_production_rates[indices]*W[indices]/G
    out[11,j]=UV/G*(Tc-Ts)/1e6
    out[12,j]=-y[13,j]*1000/KS
    out[13,j]=.5*UV*(Th+Tc-2*Ts)/1e6
   return out
  return fun
 x=np.linspace(0,L,60);y=np.zeros((14,len(x)));y[:5]=Yhot[indices,None];y[6:11]=Yfeed[indices,None]
 for j,xx in enumerate(x):
  th=3100-2000*xx/L;tc=2300-2000*xx/L;h.TPY=th,P,Yhot;c.TPY=tc,P,Yfeed;y[5,j]=h.enthalpy_mass/1e6;y[11,j]=c.enthalpy_mass/1e6;y[12,j]=(th+tc)/2000;y[13,j]=KS*2000/L/1e6
 for alpha in [0.,.01,.03,.1,.3,1.]:
  t=time.monotonic();sol=solve_bvp(system(alpha),boundary,x,y,tol=2e-5,max_nodes=2500,verbose=0)
  info={'alpha':alpha,'success':sol.success,'message':sol.message,'nodes':len(sol.x),'max_rms_residual':float(max(sol.rms_residuals)),'wall_s':time.monotonic()-t};levels.append(info);print(json.dumps(info),flush=True)
  if not sol.success:break
  x=sol.x;y=sol.y
 (ROOT/'reactive_average_progress.json').write_text(json.dumps({'levels':levels},indent=2)+'\n')
 if levels[-1]['alpha']!=1 or not sol.success:return
 xx=np.linspace(0,L,501);yy=sol.sol(xx);Th=[];Tc=[];nh=[];nc=[]
 for j in range(len(xx)):
  h.HPY=yy[5,j]*1e6,P,unpack(yy[:5,j]);c.HPY=yy[11,j]*1e6,P,unpack(yy[6:11,j]);Th.append(h.T);Tc.append(c.T);nh.append(sum(1000*h[s].Y[0]/h[s].molecular_weights[0] for s in ['NO','NO2']));nc.append(sum(1000*c[s].Y[0]/c[s].molecular_weights[0] for s in ['NO','NO2']))
 yieldNO=nh[-1];duty=hhot-yy[11,0]*1e6;hotloss=hhot-yy[5,-1]*1e6;coldgain=yy[11,0]*1e6-hfeed
 result={'scope':__doc__,'geometry':{'L_m':L,'G_kg_m2_s':G,'porosity':POR,'Uv_W_m3_K':UV,'k_eff_W_m_K':KS},'levels':levels,'net_heater_heat_MJ_mol_NOx_exchanger_out':float(duty/yieldNO/1e6),'retained_mol_NOx_kg':yieldNO,'hot_initial_mol_NOx_kg':nh[0],'hot_survival':yieldNO/nh[0],'cold_preheat_NOx_mol_kg':nc[0],'maximum_solid_K':float(max(yy[12]*1000)),'max_hot_K':max(Th),'cold_out_K':Tc[0],'hot_out_K':Th[-1],'heat_balance_J_kg':float(hotloss-coldgain),'boundary_residual_max':float(max(abs(boundary(yy[:,0],yy[:,-1])))),'min_independent_species_fraction':float(min(yy[:5].min(),yy[6:11].min())),'wall_s':time.monotonic()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'profile':{'x_m':xx.tolist(),'Th_K':Th,'Tc_K':Tc,'Ts_K':(1000*yy[12]).tolist(),'NOx_hot_mol_kg':nh,'NOx_cold_mol_kg':nc}}
 (ROOT/'reactive_average_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['profile','scope','levels']}),flush=True)
if __name__=='__main__':main()
