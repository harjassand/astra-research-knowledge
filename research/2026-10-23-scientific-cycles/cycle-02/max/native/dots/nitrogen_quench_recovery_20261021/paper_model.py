"""Six-species seven-reaction thermal variant from Albrechts2026 Table1.
R6 Lindemann data Baulch2005 (200–2200K recommended); extrapolation above2200
is explicit. All reverses enforce common NASA thermochemistry, unlike paper's
separately fitted R6 equilibrium. Not exact CFD reproduction, no plasma states.
"""
from pathlib import Path
import numpy as np
import cantera as ct
ROOT=Path(__file__).resolve().parent

def gas_model(variant='paper7'):
 ref=ct.Solution(str(ROOT/'sources/air.yaml'));species=[ref.species(n) for n in ['N2','O2','N','O','NO','NO2']];A=ct.avogadro;R=ct.gas_constant
 r=[]
 def custom(eq,fun,eff=None):
  q=ct.Reaction(equation=eq,rate=ct.CustomRate(fun))
  if eff:q.third_body.efficiencies=eff
  r.append(q)
 custom('N2 + M <=> 2 N + M',lambda T:5e-14*A*np.exp(-113200/T)*(-np.expm1(-3354/T)),{'N':2.2,'O':2.2})
 custom('O2 + M <=> 2 O + M',lambda T:3.7e-14*A*np.exp(-59380/T)*(-np.expm1(-2238/T)),{'N':3.5,'O':3.5,'N2':.25})
 r.append(ct.Reaction(equation='N2 + O <=> NO + N',rate=ct.ArrheniusRate(3e-16*A,0,38000*R)))
 r.append(ct.Reaction(equation='O2 + N <=> NO + O',rate=ct.ArrheniusRate(9.7e-21*A,1.01,3120*R)))
 custom('NO + M <=> N + O + M',lambda T:2.4e-15*A*np.exp(-74700/T))
 lr=ct.LindemannRate(low=ct.ArrheniusRate(9.2e-40*A*A,-1.6,0),high=ct.ArrheniusRate(4.9e-16*A,-.4,0))
 r.append(ct.Reaction(equation='NO + O (+M) <=> NO2 (+M)',rate=lr))
 r.append(ct.Reaction(equation='NO2 + O <=> NO + O2',rate=ct.ArrheniusRate(5.5e-18*A,0,-188*R)))
 return ct.Solution(thermo='ideal-gas',kinetics='gas',transport_model='mixture-averaged',species=species,reactions=r)
if __name__=='__main__':
 import json,time,resource
 import counterflow as cf
 t=time.monotonic();cf.gas_model=gas_model;rows=[]
 for Tq,L in [(1800.,.02),(2100.,.02),(2400.,.02)]:
  try:
   row=cf.run(Tq=Tq,L=L,variant='paper7');row['accepted_boundary']=abs(row['cold_inlet_residual_K'])<1e-3 and abs(row['heat_balance_residual_J_kg'])<1e-6*row['gross_J_kg'];rows.append(row);print(Tq,row['net_gas_heat_MJ_mol'],row['recuperator_survival'],row['accepted_boundary'],flush=True)
  except Exception as e:rows.append({'Tq':Tq,'error':repr(e),'status':'NUMERICAL_FAILURE'})
 result={'rows':rows,'wall_s':time.monotonic()-t,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':__doc__};(ROOT/'results/paper_model_sensitivity.json').write_text(json.dumps(result,indent=2)+'\n')
