"""Read-only acceptance gate and separately metered downstream/cold-feed diagnostics.
Does not repair or silently promote failed counterflow shooting rows.
"""
import json,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from quench_screen import gas_model,cool,P,T0
ROOT=Path(__file__).resolve().parent
# Counterflow source did not persist outlet Y. Independent saved NOx score remains
# exchanger-only. Diagnostics here explicitly bound cold-feed chemistry; full
# downstream composition must come from a subsequently saved converged state.
def main():
 t=time.monotonic();raw=json.loads((ROOT/'results/counterflow.json').read_text());out=[]
 for row in raw['rows']:
  if 'profile' not in row:out.append({'Tq_K':row['Tq_K'],'length_m':row['length_m'],'accepted':False,'reason':'solver failure'});continue
  good=abs(row['cold_inlet_residual_K'])<1e-3 and abs(row['heat_balance_residual_J_kg'])<1e-6*row['gross_J_kg'] and row['min_Y']>-1e-10 and row['mass_drift']<1e-8
  r={'Tq_K':row['Tq_K'],'length_m':row['length_m'],'accepted':bool(good),'boundary_error_K':row['cold_inlet_residual_K'],'energy_error_J_kg':row['heat_balance_residual_J_kg'],'claim_scope':'converged exchanger only; not yet300K delivered endpoint'}
  if good:
   g=gas_model();g.TPX=300,P,{'N2':.79,'O2':.21};feedY=g.Y.copy();x=np.array(row['profile']['x_m']);tc=np.array(row['profile']['Tc_K']);G=row['mass_flux_kg_m2_s'];L=row['length_m']
   def rhs(s,Y):
    T=np.interp(L-s,x,tc);g.TPY=T,P,Y;return g.net_production_rates*g.molecular_weights/G
   sol=solve_ivp(rhs,[0,L],feedY,method='BDF',rtol=1e-8,atol=1e-14,max_step=L/100);assert sol.success;g.TPY=tc[0],P,sol.y[:,-1];hreact=g.enthalpy_mass;mol=sum(1000*g[s].Y[0]/g[s].molecular_weights[0] for s in ['NO','NO2']);g.TPY=tc[0],P,feedY;dh=hreact-g.enthalpy_mass
   r['cold_prescribed_path_diagnostic']={'NOx_mol_kg':mol,'enthalpy_change_vs_frozen_J_kg':dh,'fraction_of_reported_hot_NOx':mol/row['retained_mol_NOx_kg'],'not_coupled_correction':True}
   r['maximum_stream_temperature_K']=max(max(row['profile']['Th_K']),max(row['profile']['Tc_K']))
  out.append(r)
 result={'rows':out,'wall_s':time.monotonic()-t,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'status':'VALIDITY_GATE_NOT_NEW_DEVICE_CLAIM'};(ROOT/'results/acceptance_gate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
