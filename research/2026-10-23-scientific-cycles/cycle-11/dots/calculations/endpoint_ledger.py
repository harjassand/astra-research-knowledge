"""Finite measured-endpoint accounting, not a kinetic simulation or plant model."""
import json, math, time, resource
from pathlib import Path
P=Path(__file__).resolve().parent

def ledger(rows,V,v):
 n=len(rows)-1
 assert V>n*v>=0
 N=[r[1] for r in rows]; A=[r[2] for r in rows]
 Vfinal=V-n*v
 # mM*mL = micromol. Count surviving liquid and removed analytical aliquots once.
 total_A=Vfinal*A[-1]+v*sum(A[:-1]); total_N=Vfinal*N[-1]+v*sum(N[:-1])
 new_A=total_A-V*A[0]; loss=V*N[0]-total_N
 no_sampling=V*(A[-1]-A[0])
 assert math.isclose(new_A,no_sampling-v*sum(A[-1]-a for a in A[:-1]),rel_tol=1e-13)
 # Upper allowance for additional uncounted original-N-independent nitrate
 # before the net product falls below 90% of original nitrite; not a measured error.
 margin90=new_A-.9*V*N[0]
 return {'aliquot_mL':v,'final_volume_mL':Vfinal,'net_nitrate_micromol':new_A,'remaining_liquid_nitrate_micromol_gross':Vfinal*A[-1],'sampled_nitrate_micromol_gross':v*sum(A[:-1]),'original_nitrite_micromol':V*N[0],'nitrite_loss_micromol':loss,'net_nitrate_per_initial_nitrite':new_A/(V*N[0]),'nitrate_per_nitrite_lost':new_A/loss,'nitrate_per_nominal_peroxide_dosed':new_A/(V*1),'nominal_peroxide_per_net_nitrate':V/new_A,'unaccounted_inorganic_N_micromol':loss-new_A,'extra_background_allowance_to_90pct_micromol':margin90,'overcount_from_ignoring_withdrawal_micromol':no_sampling-new_A}

def compute(inp):
 V=inp['volume_mL_nominal'];D=inp['peroxide_mM_nominal']*V
 out={'source_doi':inp['source_doi'],'basis':'Actual source means; mM interpretation and nominal volumes/dose. No certified overall uncertainty, plant SEC or nitrate/photon claim.','arms':{}}
 for name,arm in inp['arms'].items():
  r=arm['rows'];N0=r[0][1];A0=r[0][2];Nt=r[-1][1];At=r[-1][2]
  entries=[ledger(r,V,v) for v in inp['sampling_mL_scenarios']]
  for e in entries:
   e['nitrate_per_nominal_peroxide_dosed']=e['net_nitrate_micromol']/D
   e['nominal_peroxide_per_net_nitrate']=D/e['net_nitrate_micromol']
  # Endpoint point ratios remain meaningful regardless of common mM/microM header seam.
  out['arms'][name]={'endpoint_min':r[-1][0],'initial_nitrate_fraction_of_initial_nitrite':A0/N0,'conversion_concentration_ratio':(N0-Nt)/N0,'uncorrected_final_nitrate_per_initial_nitrite':At/N0,'net_nitrate_per_initial_nitrite_concentration_ratio':(At-A0)/N0,'net_nitrate_per_loss_concentration_ratio':(At-A0)/(N0-Nt),'sampling_scenarios':entries}
 # A chosen independent +/-1 source-SD box is a sensitivity rectangle, not confidence.
 r=inp['arms']['H2O2']['rows'];Vf=V-4
 coeff=[-V+1,1,1,1,Vf]
 A=[x[2] for x in r];sd=[x[5] for x in r]
 center=sum(a*c for a,c in zip(A,coeff));radius=sum(abs(c)*s for c,s in zip(coeff,sd))
 out['H2O2_one_SD_box_sensitivity_not_CI']={'product_center_micromol':center,'product_L1_radius_micromol':radius,'net_product_interval_micromol':[center-radius,center+radius],'per_nominal_dose_interval':[(center-radius)/D,(center+radius)/D],'scope':'Not confidence coverage; unknown covariance/calibration, nominal dose exact only for this sensitivity.'}
 # Algebraic necessary evidence, not assumption that molecular mechanism is elementary.
 out['stoichiometry']={'balanced_reaction':'NO2- + H2O2 -> NO3- + H2O','net_stoichiometric_peroxide_per_nitrate':1,'nominal_charge_equals_measured_consumption':False,'excess_peroxide_recovery_measured':False}
 return out

if __name__=='__main__':
 t=time.perf_counter();inp=json.loads((P/'inputs.json').read_text());out=compute(inp)
 (P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 (P/'execution_receipt.json').write_text(json.dumps({'wall_seconds':time.perf_counter()-t,'peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'total_research_cost':'unknown','operation':'finite endpoint and discrete sampling accounting; no fit or trajectory'},indent=2)+'\n')
 print(json.dumps(out['arms']['H2O2'],indent=2))
