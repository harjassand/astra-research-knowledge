"""Bounded thermal air-to-NOx quench/recuperation screen, not a plasma reactor model.
Standard Cantera air.yaml thermochemistry/kinetics; optional literature Zeldovich
rate replacement only. Prescribed cooling is a required actuator, not free hardware.
All energy quantities per kg fresh air, then divide retained mol NO+NO2 per kg.
"""
import os,time,json,hashlib,resource,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import cantera as ct
ROOT=Path(__file__).resolve().parent
T0=300.;P=ct.one_atm

def gas_model(variant='gri'):
 g=ct.Solution(str(ROOT/'sources/air.yaml'))
 if variant=='zeldovich2026':
  species=g.species();reactions=g.reactions()
  reactions[1]=ct.Reaction(equation='N2 + O <=> NO + N',rate=ct.ArrheniusRate(3e-16*ct.avogadro,0,38000*ct.gas_constant))
  reactions[2]=ct.Reaction(equation='N + O2 <=> NO + O',rate=ct.ArrheniusRate(9.7e-21*ct.avogadro,1.01,3120*ct.gas_constant))
  g=ct.Solution(thermo='ideal-gas',kinetics='gas',species=species,reactions=reactions)
 return g

def cool(g,Y,Ta,Tb,beta,rtol=2e-8):
 duration=(Ta-Tb)/beta;W=g.molecular_weights
 def rhs(t,y):
  g.TPY=max(Tb,Ta-beta*t),P,y
  return g.net_production_rates*W/g.density
 sol=solve_ivp(rhs,(0,duration),Y,method='BDF',rtol=rtol,atol=1e-13,max_step=duration/30)
 if not sol.success:raise RuntimeError(sol.message)
 y=sol.y[:,-1];g.TPY=Tb,P,y
 return y,{'steps':len(sol.t),'nfev':sol.nfev,'min_Y':float(sol.y.min()),'mass_drift':float(np.max(abs(sol.y.sum(0)-1)))}

def evaluate(g,Th,Tq,bq,br,pinch=50,rtol=2e-8):
 g.TPX=T0,P,{'N2':.79,'O2':.21};feedY=g.Y.copy();hfeed=g.enthalpy_mass
 g.TP=Th,P;g.equilibrate('TP');hotY=g.Y.copy();hhot=g.enthalpy_mass
 mol=lambda Y:1000*sum(Y[g.species_index(s)]/g.molecular_weights[g.species_index(s)] for s in ['NO','NO2'])
 hotmol=mol(hotY)
 yq,dq=cool(g,hotY,Th,Tq,bq,rtol);hq=g.enthalpy_mass
 yf,dr=cool(g,yq,Tq,T0,br,rtol);hf=g.enthalpy_mass;nmol=mol(yf)
 g.TPY=max(T0,Tq-pinch),P,feedY;feedcapacity=g.enthalpy_mass-hfeed
 potential=max(0,min(hq-hf,feedcapacity));net=hhot-hfeed-potential
 g.TPY=T0,P,yf
 return {'Th_K':Th,'Tq_K':Tq,'quench_K_s':bq,'recuperation_cooling_K_s':br,'pinch_K':pinch,'retained_mol_NOx_kg':nmol,'hot_mol_NOx_kg':hotmol,'survival':nmol/hotmol,'outlet_X_NOx':float(g['NO'].X[0]+g['NO2'].X[0]),'outlet_N2O_mol_kg':float(1000*g['N2O'].Y[0]/g['N2O'].molecular_weights[0]),'gross_J_kg':hhot-hfeed,'discarded_quench_J_kg':hhot-hq,'recuperation_hot_J_kg':hq-hf,'feed_preheat_cap_J_kg':feedcapacity,'credited_recovery_upper_bound_J_kg':potential,'favorable_net_MJ_mol':net/nmol/1e6,'no_recovery_MJ_mol':(hhot-hfeed)/nmol/1e6,'cold_product_enthalpy_increase_J_kg':hf-hfeed,'first_law_residual_J_kg':(hhot-hfeed)-(hhot-hq)-(hq-hf)-(hf-hfeed),'quench_diagnostics':dq,'recuperator_diagnostics':dr}

def main():
 start=time.monotonic();rows=[]
 for variant in ['gri','zeldovich2026']:
  g=gas_model(variant)
  for tq in [1400.,1800.,2100.,2400.]:
   for br in [1e3,1e4,1e5,1e6,1e7]:
    r=evaluate(g,3100.,tq,1e8,br);r['variant']=variant;rows.append(r)
 result={'scope':'favorable prescribed-temperature screen, no hardware/heat-transfer feasibility, thermal chemical model not nonthermal plasma','rows':rows,'elapsed_s':time.monotonic()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cantera':ct.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'air_sha256':hashlib.sha256((ROOT/'sources/air.yaml').read_bytes()).hexdigest()}
 (ROOT/'results/screen.json').write_text(json.dumps(result,indent=2)+'\n')
 for r in rows:print(r['variant'],r['Tq_K'],r['recuperation_cooling_K_s'],round(r['survival'],5),round(r['favorable_net_MJ_mol'],5),flush=True)
 print('wall',result['elapsed_s'])
if __name__=='__main__':main()
