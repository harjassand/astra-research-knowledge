"""A source-anchored alternative, not an optimized fit or certified phase assessment.
Uses absolute G-H_elements(298) to cancel elemental reference conventions.
"""
from decimal import Decimal as D
from pathlib import Path
import json,math
T=D(1000)
# JANAF: Hf298[kJ/mol], -(G-H298)/T[J/mol/K].
janaf={'hematite':(D('-825.503'),D('152.360')),'carbonate_liquid':(D('-1216.038'),D('155.301')),'CO2':(D('-393.522'),D('235.901'))}
g={k:h-T*f/1000 for k,(h,f) in janaf.items()}
# Rakshit Table6 alpha-LiFeO2: Hf298 -719; S29875.8; H1000-H29878095J; S1000205.1.
H0=D(-719);S0=D('75.8');dh=D('78.095');S=D('205.1')
thermal=dh-T*(S-S0)/1000
G_table=H0-T*S0/1000+thermal
# Wang/Navrotsky calorimetry, alpha phase Hf298; measured S298 tabulated with it.
Hcal=D('-749.8');Scal=D('75.3')
G_cal=Hcal-T*Scal/1000+thermal
assert G_cal-G_table==(Hcal-H0)-T*(Scal-S0)/1000
r=[]
R=8.31446261815324
silicate=22.8+R*1000*math.log(1.01325)/1000
for name,F in [('Rakshit_Table6_shared_element_reference',G_table),('calorimetry_anchored_same_thermal_increment',G_cal)]:
 net=2*F+g['CO2']-g['hematite']-g['carbonate_liquid']
 r.append(dict(model=name,ferrite_Gstar_kJ_mol=str(F),ferrite_formation_reaction_G_kJ_mol=str(net),exchange_forward_G_kJ_mol=float(net)+silicate,ferrite_upper_CO2_bar=math.exp(-float(net)*1000/R/1000),silicate_lower_CO2_bar=math.exp(silicate*1000/R/1000)))
out=dict(T_K=1000,Gstar_JANAF_kJ_mol={k:str(v) for k,v in g.items()},thermal_increment_kJ_mol=str(thermal),models=r,anchor_shift_per_formula_kJ_mol=str(G_cal-G_table),anchor_box_halfwidth_per_formula_kJ_mol=2.6,thermal_shape_uncertainty='UNKNOWN; Table6 extrapolates measured Cp past861K; source rows indexed but full PDF not downloaded',status='SOURCE_ANCHORED_CONDITIONAL_COUNTERMODEL_TO_ROBUST_PRESSURE_EXCLUSION_NOT_VALIDATED_MELT_WINDOW')
Path(__file__).with_name('calorimetric_cycle_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
