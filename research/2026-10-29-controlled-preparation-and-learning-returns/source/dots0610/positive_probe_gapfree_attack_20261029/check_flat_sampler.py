from fractions import Fraction as F
from pathlib import Path
import json
p=Path(__file__).parent
# x=0/1 each1/2; conditional arms uniform over2 vs3 actions.
# One-attempt hierarchicalcap: binary rejection for D2 always succeeds, D3 only3/4.
a=[F(1,2),F(1,2)*F(3,4)];hier=[v/sum(a) for v in a];assert hier==[F(4,7),F(3,7)]
weights=[3,3,2,2,2];D=sum(weights);b=(D-1).bit_length();accept=F(D,1<<b)
rows=[]
for R in [1,2,4,8]:
 abort=(1-accept)**R;out=[F(w,D)*(1-abort) for w in weights];norm=sum(out);cond=[v/norm for v in out];assert cond==[F(w,D) for w in weights]
 assert sum(cond[:2])==sum(cond[2:])==F(1,2)
 rows.append({'cap':R,'abort_exact':str(abort),'conditional_joint_probabilities':list(map(str,cond)),'conditional_x_probabilities':['1/2','1/2']})
out={'exact_hierarchical_cap_bias_x':list(map(str,hier)),'flat_joint_sampler_cases':rows,'scope':'Exact finite cap demonstration. Whole-history conditioning is not asserted unchanged; global guarantee uses an additive abort coupling.'};(p/'flat_sampler_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
