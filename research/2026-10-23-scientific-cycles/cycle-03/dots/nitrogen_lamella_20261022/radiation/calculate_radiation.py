"""Reproduce a conservative NO catalogue envelope and published Planck-mean estimates.
Only Python stdlib is required. No transition list, external package, or remote action.
Run in this directory. The NO lifetime assignments are NOT used state-by-state.
"""
import gzip, json, math
from pathlib import Path
P = Path(__file__).resolve().parent
h, c, kb, NA = 6.62607015e-34, 299792458., 1.380649e-23, 6.02214076e23
R, sig, atm = NA*kb, 5.670374419e-8, 101325.
T, inventory, heat = 1700., 1.01*1.9050984107423, 53995.
rows=[]
for line in gzip.open(P/'s_14n16o.dat.gz','rt'):
    t=line.split()
    rows.append((int(t[0]),float(t[1]),int(t[2]),math.inf if t[4]=='---' else float(t[4])))
# Publication and its Fig. 11 establish tau is seconds; CDS ReadMe says s^-1 in error.
weights=[g*math.exp(-h*c*100*E/(kb*T)) for _,E,g,_ in rows]
Z=sum(weights)
U=NA*sum(w*h*c*100*E for w,(_,E,_,_) in zip(weights,rows))/Z
Amax=max(1/tau for _,_,_,tau in rows)
# Amax is a global cap, hence does not depend on possibly mispaired tau/E entries.
bound=Amax*U
coefs={
 'NO':[.065741836,-2.1198447,-1.1067288,.40888497,-.084908367,.0069002025],
 'NO2':[2.5761129,-2.5457045,-1.1422229,-.53698484,.26572755,-.034491369]
}
fit={}
for s,cc in coefs.items():
    kP=math.exp(sum(ci*math.log(T/1000.)**i for i,ci in enumerate(cc)))
    fit[s]={'kP_m_inv_atm_inv':kP,'power_W_per_mol':4*sig*T**4*kP*R*T/atm}
    fit[s]['J_per_kg_at_50us']=fit[s]['power_W_per_mol']*inventory*50e-6
    fit[s]['J_per_kg_at_110us']=fit[s]['power_W_per_mol']*inventory*110e-6
    fit[s]['J_per_kg_at_1ms']=fit[s]['power_W_per_mol']*inventory*1e-3
    fit[s]['constant_1700K_heat_to_power_time_s']=heat/(fit[s]['power_W_per_mol']*inventory)
required=heat/(inventory*110e-6)
res={
 'conditions':{'T_K':T,'NOx_mol_per_kg_fresh':inventory,'required_heat_J_per_kg_fresh':heat,
 'timing_scope':'110 microseconds is a specified rapid-export challenge, NOT an established complete-reset deadline. The transient all-gas-below-1700 K window still has O=0.345 to 0.226 mol/kg, unlike the O<=0.003 mol/kg final certificate. Downstream heat transfer may continue within the original 0.14 s cooler.'},
 'NO_catalogue':{'states':len(rows),'Z':Z,'U_J_per_mol':U,'Amax_per_s':Amax,'minimum_tau_s':1/Amax,
 'conditional_power_envelope_W_per_mol':bound,'envelope_J_per_kg_at_50us':bound*inventory*50e-6,
 'envelope_J_per_kg_at_110us':bound*inventory*110e-6,
 'envelope_J_per_kg_at_1ms':bound*inventory*1e-3,
 'conditional_NO_only_minimum_time_s':heat/(bound*inventory),
 'warning':'Finite represented model only. Archived tau/state assignments are inconsistent with the published plot. No state-by-state power sum is used.'},
 'Planck_fit_estimates':fit,
 'threshold_if_all_NOx_emits':{'scope':'Specified 110 microsecond rapid-export challenge only; not a complete-reset deadline.',
 'required_W_per_mol':required,'required_Planck_coefficient_m_inv_atm_inv':required/(4*sig*T**4*R*T/atm),
 'ratio_to_NO_fit':required/fit['NO']['power_W_per_mol'],'ratio_to_NO2_extrapolation':required/fit['NO2']['power_W_per_mol']},
 'scope_warning':'NO2 fit at 1700 K extrapolates a source list whose own authors advise caution near 1000 K. It is not an upper bound. N2/O2/atomic/electronic/continuum paths are not bounded.'
}
(P/'radiation_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
