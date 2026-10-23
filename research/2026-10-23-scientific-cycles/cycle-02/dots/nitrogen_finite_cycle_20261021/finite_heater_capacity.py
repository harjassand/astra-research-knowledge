"""Fixed-temperature ideal PFR capacity diagnostic at matched heater volume/flow.
Not a universal reactor upper bound, cycle, measured heater, or energy SEC.
Tests whether lowering temperature alone preserves the current heater capacity.
"""
import sys,json,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'thermo_helper'));from helper import ThermoKernel
from validate import native_corrected
K=ThermoKernel();g=native_corrected(K);W=g.molecular_weights;noids=[g.species_index('NO'),g.species_index('NO2')]
g.TPX=300,101325,{'N2':.79,'O2':.21};fresh=g.Y.copy()
z=np.load(R.parent/'nitrogen_regenerator_20261021/radiating_2700_checkpoint.npz');pre=np.r_[1-z['y'][6:11,0].sum(),z['y'][6:11,0]]
def NO(y):return float(sum(1000*y[noids]/W[noids]))
start=time.monotonic();rows=[]
for T in [2100.,2300.,2500.,2700.]:
 for name,yin in [('fresh_air',fresh),('saved2700case_preheated_composition',pre)]:
  g.TPY=T,101325,yin;g.equilibrate('TP');eq=NO(g.Y)
  def rhs(v,Y):
   g.TPY=T,101325,Y;return g.net_production_rates*W
  sol=solve_ivp(rhs,[0,.1],yin,method='BDF',rtol=1e-10,atol=1e-18)
  y=sol.y[:,-1];g.TPY=T,101325,y;actual=NO(y)
  row={'T_K':T,'initial_composition':name,'volume_over_massflow_m3_s_kg':.1,'success':sol.success,'NOx_mol_kg':actual,'equilibrium_NOx_mol_kg':eq,'fraction_eq':actual/eq,'out_density_kg_m3':g.density,'density_based_holdup_time_s':.1*g.density,'min_Y':float(sol.y.min()),'max_mass_drift':float(max(abs(sol.y.sum(0)-1))),'steps':len(sol.t)-1};rows.append(row);print(json.dumps(row),flush=True)
result={'scope':__doc__,'rows':rows,'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'caveats':['Temperature is imposed everywhere without heater efficiency, wall loss or temperature gradients.','PFR ordering is not proved optimal among all RTDs for this multistep chemistry.','Saved preheated composition is a sensitivity seed, not a self-consistent lower-temperature regenerator solution.','Equilibrium species composition computed from same continuous-NASA model; rates extrapolation and source model caveats remain.']};(R/'finite_heater_capacity.json').write_text(json.dumps(result,indent=2)+'\n')
