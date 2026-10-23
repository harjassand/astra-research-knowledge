"""Finite constant-temperature heater and uncredited cold tail diagnostics.
Not a coupled finite-heater bed cycle: checks the favorable equilibrium boundary.
"""
import sys,json,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'nitrogen_quench_recovery_20261021'))
from paper_model import gas_model
P=101325.;T=2700.;G=1.
t0=time.monotonic();g=gas_model();ns=g.n_species;idx=[g.species_index(s) for s in ['O2','N','O','NO','NO2']];ni=g.species_index('N2');W=g.molecular_weights
z=np.load(ROOT/'radiating_2700_checkpoint.npz');a=z['y'];x=z['x']
def full(v):
 y=np.zeros(ns);y[idx]=v;y[ni]=1-sum(v);return y
Yin=full(a[6:11,0]);g.TPY=a[11,0]*1000,P,Yin;hin=g.enthalpy_mass
g.TPY=T,P,Yin;g.equilibrate('TP');Yeq=g.Y.copy();heq=g.enthalpy_mass
noidx=[g.species_index(s) for s in ['NO','NO2']]
def no(y):return float(np.sum(1000*y[noidx]/W[noidx]))
def rhs(t,y):
 g.TPY=T,P,y;return g.net_production_rates*W/g.density
sol=solve_ivp(rhs,[0,10],Yin,method='BDF',rtol=1e-9,atol=1e-14,dense_output=True)
times=np.r_[0,np.geomspace(1e-8,10,600)];ys=sol.sol(times);target=no(Yeq);nv=np.array([no(y) for y in ys.T]);ii=np.where(nv>=.99*target)[0];j=int(ii[0]) if len(ii) else None
# Integrate constant-T PFR specific volume to physical volume/mass flow.
vol=[]
for y in ys.T:g.TPY=T,P,y;vol.append(1/g.density)
V=np.r_[0,np.cumsum(np.diff(times)*(np.array(vol)[1:]+np.array(vol)[:-1])/2)]
# Tail, imposed 10000 K/s, no recovery credit; six-species kinetic continuation.
Tout=a[5,-1]*1000;Yout=full(a[:5,-1]);g.TPY=Tout,P,Yout;hout=g.enthalpy_mass
rate=1e4
c=solve_ivp(lambda t,y: tail_rhs(t,y),[0,1],Yout) if False else None
def tail_rhs(t,y):
 g.TPY=max(300,Tout-rate*t),P,y;return g.net_production_rates*W/g.density
c=solve_ivp(tail_rhs,[0,(Tout-300)/rate],Yout,method='BDF',rtol=1e-9,atol=1e-14)
g.TPY=300,P,c.y[:,-1];hf=g.enthalpy_mass;nf=no(c.y[:,-1]);heat=(heq-hin)/nf/1e6
r={'heater_success':sol.success,'heater_message':sol.message,'target_eq_NOx_mol_kg':target,'initial_preheated_NOx_mol_kg':no(Yin),'time_to_99_percent_eq_sampled_s':None if j is None else float(times[j]),'heater_volume_per_kg_s_m3':None if j is None else float(V[j]),'heater_final_NOx_mol_kg':float(nv[-1]),'heater_max_mass_drift':float(np.max(abs(ys.sum(axis=0)-1))),'heater_minY':float(ys.min()),'tail_success':c.success,'tail_initial_T_K':float(Tout),'tail_duration_s':float((Tout-300)/rate),'tail_in_NOx_mol_kg':no(Yout),'tail_out_NOx_mol_kg':nf,'tail_uncredited_heat_J_kg':float(hout-hf),'gas_heat_MJ_mol_300K_NOx':heat,'scope':__doc__,'wall_s':time.monotonic()-t0,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
np.savez_compressed(ROOT/'heater_and_tail_arrays.npz',times=times,Y=ys,NOx=nv,V=V,tail_t=c.t,tail_Y=c.y)
(ROOT/'heater_and_tail_result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
