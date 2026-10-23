"""Exact conditional stoichiometry and declared physical reference scales."""
from fractions import Fraction as F
from pathlib import Path
import json,math,time,resource
p=Path(__file__).parent;start=time.perf_counter();d=json.loads((p/'dataset_result.json').read_text())
air=F(str(d['controls'][0]['value_at_2700s_linear_interpolation']))/1000
scav=F(str(d['controls'][1]['value_at_2700s_linear_interpolation']))/1000
n2=F(str(d['controls'][2]['value_at_2700s_linear_interpolation']))/1000
rows=[]
for label,y in [('air_2700s',air),('N2_2700s',n2),('KSCN_air_2700s',scav),('published_1M_A',F(843,1000)),('published_875mM_A',F(730,875))]:
 rows.append({'case':label,'reference_bound_yield':float(y),'electrons_per_initial_N_if_other_N_min_NO_2':float(max(F(0),3*y-1)),'electrons_per_initial_N_if_other_N_min_N2_0':float(max(F(0),5*y-3)),'electrons_per_initial_N_if_other_N_min_NH3_minus3':float(max(F(0),8*y-6)),'multiplicative_overstatement_to_erase_y_gt_3quarters':float(y/F(3,4)),'scope':'Conditional on retained tracer, source feed ratio, zero imported nitrate and valid relative response; no statistical confidence.'})
# Rayleigh net-charge inventory check, explicit reference assumptions, not an actual droplet charge measurement.
r=5e-6;gamma=.072;epsilon0=8.8541878128e-12;Faraday=96485.3321233100184
C=1000.;V=4*math.pi*r**3/3;N0=C*V;emin=max(0.,8*float(air)-6)
Qneed=Faraday*N0*emin;Qrayleigh=8*math.pi*math.sqrt(epsilon0*gamma*r**3)
# Reversible creation of clean isolated spherical interface only, no spray/trap/recovery/humidity work included.
Esurf_molN=3*gamma/(r*C)
# Actual published absorber rows, G fixed; numerical values transcribed from2024Table5.
G=.0355;R=8.31446261815324;T=293.;cmp=[]
for run,L,Pno,eta,S2,HNO3M in [(1,1.111e-4,66.5,.158,.98,0),(5,1.667e-4,398.5,.369,.932,0),(27,1.111e-4,416.8,.396,.909,1),(40,1.944e-4,53.6,.104,.589,1)]:
 removal=G*Pno/(R*T)*eta;H2O2_feed=L*1000*.2;acid_feed=L*1000*HNO3M
 cmp.append({'run':run,'new_gas_N_removed_mol_s_ideal_gas_descriptor':removal,'fresh_H2O2_feed_mol_s':H2O2_feed,'H2O2_feed_per_removed_N':H2O2_feed/removal,'conditional_stoichiometric_H2O2_per_nitrate_N':1.5-S2,'background_HNO3_N_feed_per_removed_N':acid_feed/removal,'scope':'Feed charge not reagent consumption; 1.5-S2 is a conditional peroxide-only oxidation equivalent, not measured uptake or an unconditional minimum with oxygen reaction. Gas removal is not species-resolved new nitrate inventory. Liquid reuse/reset must be explicit.'})
out={'conditioned_data_rows':rows,'same_time_reference_signal_ratios':{'air_over_N2':float(air/n2),'scavenger_air_over_air':float(scav/air)},'charge_storage_reference':{'radius_m':r,'surface_tension_assumed_N_m':gamma,'initial_nitrite_assumed_mol_m3':C,'N0_mol':N0,'minimum_electron_export_mol_per_initial_N_air2700':emin,'hypothetical_charge_if_all_stored_C':Qneed,'Rayleigh_limit_conducting_isolated_drop_C':Qrayleigh,'ratio_Q_needed_over_Rayleigh':Qneed/Qrayleigh,'surface_tension_needed_to_store_charge_N_m':Qneed**2/(64*math.pi**2*epsilon0*r**3),'scope':'Conditional stable conducting spherical droplet check. Rules against net charge storage as sole sink under assumptions, not external gas electron acceptors or a photochemical mechanism.'},'surface_creation_reference_J_per_mol_initial_N':Esurf_molN,'surface_energy_scope':'Only reversible interface creation at assumedgamma,r,C; not measured spray energy, not electricitySEC or an engineeringlowercost guarantee','ordinary_peroxide_reference_rows':cmp,'elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(p/'material_bounds.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
