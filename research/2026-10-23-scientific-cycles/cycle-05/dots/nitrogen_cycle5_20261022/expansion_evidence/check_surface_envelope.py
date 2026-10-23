"""Necessary gross-surface envelope only, not a conjugate heat-transfer solution.
Uses SI Table S.3 h(T), epsilon, ambient, and main-text collector dimensions.
No new trajectory. No assertion that collector is isothermal or well coupled to divider.
"""
from pathlib import Path
import math,json
P=Path(__file__).resolve().parent
D=0.0252; L=0.295; A=math.pi*D*L
sigma=5.670374419e-8; eps=.8; Ta=293.15
power=158.91333333333333
rows=[]
for T,h in [(400,15.61),(500,18.56),(600,20.61),(700,22.24),(800,23.61),(900,24.8),(1000,25.86)]:
 rad=eps*sigma*(T**4-Ta**4);conv=h*(T-Ta);flux=rad+conv
 rows.append(dict(surface_cap_K=T,h_Wm2K=h,radiative_flux_Wm2=rad,convective_flux_Wm2=conv,uniform_cylinder_lateral_capacity_W=A*flux,necessary_area_for_all_discharge_heat_m2=power/flux))
out=dict(collector_outer_diameter_m=D,collector_length_m=L,collector_lateral_area_m2=A,nozzle_outer_diameter_m=.0189,nozzle_total_length_m=.0295,nozzle_bore_m=.015,drawn_cavity_length_m=.0215,back_wall_m=.008,divider_dimensions_m=[.001,.002,.015],six_hole_total_area_m2=6*math.pi*.0008**2/4,epsilon=eps,ambient_K=Ta,discharge_power_reference_W=power,envelope=rows,ballast_conditional=dict(R_ohm=25000,reported_current_A=.135,minimum_power_if_current_is_mean_series_current_W=25000*.135**2),limitations=['Collector lateral area is known, but other exposed reactor surfaces are omitted.','At a prescribed uniform cap, monotonic h(T) and radiation give upper rejection capacity for this area only.','Nozzle is internal: this is NOT its direct-to-room radiating area.','All 159 W treated as heat is a conservative gross-load stress test, not sufficient admission; real total retained chemical energy reduces it.','The inequalities do NOT establish transport from tiny arc attachment through divider/back wall to collector.','Nonuniform temperature reduces actual rejection below this envelope.','Unknown local contact/arc heat flux and measured partial melting prevent material admission.','No modeled integrated heat export or maximum steel temperature was found in main paper/SI.'])
(P/'surface_envelope.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
