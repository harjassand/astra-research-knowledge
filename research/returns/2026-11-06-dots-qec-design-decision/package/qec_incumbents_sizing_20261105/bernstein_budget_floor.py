"""Independent arithmetic, no upstream source imported or executed."""
import math,json
from pathlib import Path
alpha=.001/3; target=1e-12
rows=[]
for J in [1,2,4]:
 c=math.log(8/alpha)
 n=c/-math.log1p(-target/J)
 rows.append(dict(mixture_components=J,minimum_shots_for_any_upper_at_most_target=math.ceil(n),best_possible_upper_after_1000000=min(1.,J*-math.expm1(-c/1e6)),best_possible_upper_after_100000000=min(1.,J*-math.expm1(-c/1e8))))
out=dict(familywise_alpha=.001,distances=3,per_design_alpha=alpha,target=target,scope='Lower bound for the pinned uniformized ScaLER controller only, not all importance sampling or its conditional-stratified alternative. Arithmetic assumes exact mathematics; numeric output rounded.',rows=rows)
Path(__file__).with_name('bernstein_budget_floor.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
