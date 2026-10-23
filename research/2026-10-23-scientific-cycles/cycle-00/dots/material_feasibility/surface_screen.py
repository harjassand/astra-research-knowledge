"""Algebraic loss screens on saved gas-model profiles, NOT a new reacting-flow simulation.
Measured geometric-area NO loss from AVCO 1974 is used as a borrowed-flux sensitivity,
not a validated upper bound for dry air/NO at 1 atm or a material property.
Nominal molecular weight is that of 79:21 molecular N2:O2; hot-stream species profiles
were not saved, so residence times and first-order coefficients are approximate.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
P=101325.;R=8.314462618;MW=.79*.0280134+.21*.031998
FLUX=7e-9*1e4 # mol/cm2/s -> mol/m2/s, AVCO measured high-T case II
rows=[]
for filename in ['counterflow.json','finite_quench.json']:
 path=ROOT/'results'/filename
 for row in json.loads(path.read_text())['rows']:
  if 'profile' not in row: continue
  if abs(row['cold_inlet_residual_K'])>=1e-3 or abs(row['heat_balance_residual_J_kg'])>=1e-6*row['gross_J_kg'] or row['mass_drift']>=1e-8 or row['min_Y']<=-1e-10: continue
  x=np.array(row['profile']['x_m']);T=np.array(row['profile']['Th_K'])
  D=row['D_m'];G=row['mass_flux_kg_m2_s'];L=row['length_m'];n=row['retained_mol_NOx_kg'];e=row['net_gas_heat_MJ_mol']
  area_per_massflow=4*L/(D*G)
  dn=FLUX*area_per_massflow;fraction=dn/n
  density=P*MW/R/T
  tau=float(np.trapezoid(density,x)/G)
  lossmax=max(0,1-e/1.5)
  firstorder_limit= -math.log(1-lossmax)/(4/D*tau) if lossmax else 0
  # fixed thermal duty / pure NO loss assumption, no recovery credit for destruction heat
  net_after=e/(1-fraction)
  out={'source':filename,'Tq_K':row['Tq_K'],'L_m':L,'front_quench_D_m':row.get('front_quench',{}).get('diameter_m'),'retained_NOx_mol_kg':n,'net_MJ_mol':e,
       'geometric_area_per_massflow_m2_s_kg':area_per_massflow,'borrowed_AVCO_j_mol_m2_s':FLUX,'borrowed_flux_loss_mol_kg':dn,
       'borrowed_flux_loss_fraction':fraction,'fixed_duty_net_after_borrowed_flux_MJ_mol':net_after,
       'maximum_loss_fraction_if_eta_capture_one_no_aux_fixed_duty':lossmax,'maximum_uniform_j_same_assumptions_mol_m2_s':n*lossmax/area_per_massflow,
       'nominal_diatic_MW_kg_mol':MW,'approx_hot_residence_s':tau,'maximum_uniform_effective_surface_velocity_same_assumptions_m_s':firstorder_limit}
  rows.append(out)
output={'warning':'NOT a coupled surface-chemistry result. Borrowed measured flux is not an extrapolatable upper bound. Effective mass-transfer velocity threshold combines intrinsic catalysis and diffusion; approximate residence uses fixed diatomic-air MW. No purchase, outreach or hardware work.',
 'sources_sha256':{f:hashlib.sha256((ROOT/'results'/f).read_bytes()).hexdigest() for f in ['counterflow.json','finite_quench.json']},'rows':rows}
(ROOT/'material_feasibility'/'surface_screen.json').write_text(json.dumps(output,indent=2)+'\n')
for r in rows:
 print(r['source'],r['Tq_K'],r['L_m'],r['front_quench_D_m'],'loss%',round(100*r['borrowed_flux_loss_fraction'],4),'tau_ms',round(1e3*r['approx_hot_residence_s'],3),'allowed_loss%',round(100*r['maximum_loss_fraction_if_eta_capture_one_no_aux_fixed_duty'],3),'kmax',round(r['maximum_uniform_effective_surface_velocity_same_assumptions_m_s'],6),'jmax',round(r['maximum_uniform_j_same_assumptions_mol_m2_s'],6),'energy_after',round(r['fixed_duty_net_after_borrowed_flux_MJ_mol'],6))
