"""Declared common-wall recovery class, not universal quench or regeneration bound.
If ALL useful recovery to composition-preserving internally equilibrated fresh feed crosses one wall no hotter than
Tw and no heat pump/work transformation/nonthermal feed exists, fresh Tin<=Tw.
One kg fresh, same saved heater chemical history and output; zero pinch favorable.
"""
from pathlib import Path
import sys,json,time,resource
import numpy as np
D=Path(__file__).resolve().parent;ROOT=D.parents[1]
sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper'))
from helper import ThermoKernel
K=ThermoKernel();start=time.monotonic();Y=np.array([.79,.21,0,0,0,0])*K.W;Y/=Y.sum();R=K.R
src=np.load(ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz');reaction=float(src['heater_positive_reaction_J_kg']);Nhot=float(np.sum(src['hot_Y'][[4,5]]*1000/K.W[[4,5]]))
def h(t):return float(Y@(K.thermochemistry(np.array([t]))[1][:,0]*R*t/K.W))
rows=[]
for tw in [300.,500.,600.,800.,1000.,1200.,1400.,1700.]:
 duty=h(2700)-h(tw)+reaction
 rows.append({'wall_cap_K':tw,'minimum_heater_duty_J_kgfresh':duty,'perfect_retention_thermal_MJ_mol_floor':duty/Nhot/1e6,'additional_duty_relative_1700K_preheat_J_kgfresh':h(1700)-h(tw)})
r={'scope':__doc__,'rows':rows,'warning':'Separate staged high-temperature recovery can leave this class; do not apply this bound to a locally cold spot with upstream hotter recuperation. No actual material temperature inferred from source nozzle. The cited500/600K collector envelopes are not measured wall temperatures. No practical quench or whole-plant electrical energy is established.','elapsed_s':time.monotonic()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'heat_grade.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
