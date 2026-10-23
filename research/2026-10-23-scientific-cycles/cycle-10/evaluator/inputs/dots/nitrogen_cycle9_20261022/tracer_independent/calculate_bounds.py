"""Deterministic stoichiometric fixtures; no data fitting or statistical intervals."""
import csv,json
from pathlib import Path
P=Path(__file__).parent
fixtures=[('1000mM_5um',.843),('875mM_rounded',.834),('750mM_rounded',.357),('625mM_rounded',.283),('500mM_5um',.29),('500mM_3p5um_361_over_500',361/500),('500mM_3p5um_printed',.56)]
rows=[]
for label,y in fixtures:
 r=dict(label=label,apparent_y=y,disjoint_route_direct_nitrate_min=max(0,(3*y-1)/2),extra_nitrate_above_one_pass_NO_disprop=max(0,y-1/3),net_N_electron_export_min=max(0,8*y-6),net_unretained_N_max=1-y)
 for name,T in [('NO_disprop',1/3),('all_N_disprop',.75)]:
  r[name+'_excluded_nominal']=y>T
  r[name+'_K_boundary']=T/y
  r[name+'_apparent_over_true_boundary']=y/T
  r[name+'_background_boundary']=max(0,y-T)
  r[name+'_tracer_loss_boundary']=max(0,1-T/y)
 rows.append(r)
with (P/'bounds.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'bounds.json').write_text(json.dumps(rows,indent=2)+'\n')
assert abs(rows[0]['disjoint_route_direct_nitrate_min']-.7645)<1e-12
assert abs(rows[0]['net_N_electron_export_min']-.744)<1e-12
print(json.dumps(rows,indent=2))
