from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json

sectors=defaultdict(F);count=0
for b1 in range(3):
 for b2 in range(3-b1):
  for c1 in range(3-b1-b2):
   c2=2-b1-b2-c1
   energy=(b1-c1)**2+(b2-c2)**2
   assert energy%2==0
   sectors[b1+b2,c1+c2]+=F(1,4)*F(1,2)**(energy//2)
   count+=1
assert count==10 and sum(sectors.values())==F(5,4)
assert sectors[1,1]==F(3,4) and sectors[2,0]==sectors[0,2]==F(1,4)
r=F(1,2);eps=F(1,16);negative=r*r*(-2+12*eps+4*eps*eps)
assert negative<-r*r
result={'literal_model':'two-site U(nb-nc)^2-muN, betaU=ln2/2, beta*mu=-ln2',
 'fixed_total_N':2,'exact_occupation_count':count,
 'sector_partition':{str(k):str(v) for k,v in sectors.items()},
 'total_partition':'5/4','grand_field_weight_at_phase_center':str(1/(1+r*r)**2),
 'total_N2_field_weight_at_phase_center':str(-2*r*r),
 'balanced_11_field_weight_at_phase_center':'0',
 'phase_box_halfwidth':str(eps),'negative_weight_upper_in_box':str(negative),
 'scope':'Exact rational ensemble control; analytic Gaussian identity/open-box proof in COUNTEREXAMPLE.md. No generic positive-representation impossibility or computational advantage.'}
Path(__file__).with_name('EXACT_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
