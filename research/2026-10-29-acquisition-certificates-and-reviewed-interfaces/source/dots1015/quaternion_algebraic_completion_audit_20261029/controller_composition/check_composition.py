from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
p=F(1,3);L0=720;d=35;rows=[]
for k in [0,1,4,16,64,256]:
 T=2**k;R=F(1);opt2=F(L0**2*T,d)/p
 while R*R<opt2:R*=2
 assert R*R>=opt2 and R*R<4*opt2
 M=1
 while M<4*d*T*T:M*=2
 eps=R/(4*T*T);total=eps+d*R/M
 assert total<=R/(2*T*T)
 exact=F(d,4)*R+F(T*L0**2,4)/(R*p)
 assert exact*exact<=L0**2*d*T/p
 # Maximal sign-aligned accumulated coefficient plus largest midpoint.
 w=F(T*L0)/p+R*F(M-1,M);quartic=w/2
 rows.append({'log2T':k,'R_bits':max(R.numerator.bit_length(),R.denominator.bit_length()),'midpoint_bank_bits':M.bit_length(),'query_coefficient_bits':max(quartic.numerator.bit_length(),quartic.denominator.bit_length()),'tolerance_bits':max(eps.numerator.bit_length(),eps.denominator.bit_length()),'exact_smoothing_bound_dominated':True})
# Every epsilon-optimal returned action, hence every randomized selection of them,
# satisfies the coordinate finite-difference squeeze pointwise.
K=[(F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1),F(1)),(F(1,3),F(2,3))]
def phi(w):return min(sum(a*b for a,b in zip(w,x)) for x in K)
checks=0;multiple=0
for nums in product(range(-3,4),repeat=2):
 w=[F(a,5) for a in nums];eps=F(1,4);h=F(2,5);near=[x for x in K if sum(a*b for a,b in zip(w,x))<=phi(w)+eps]
 multiple+=len(near)>1
 for x in near:
  for i in range(2):
   plus=w.copy();minus=w.copy();plus[i]+=h;minus[i]-=h
   assert (phi(plus)-phi(w)-eps)/h<=x[i]<=(phi(w)-phi(minus)+eps)/h
   checks+=1
out={'scope':'Exact parameter scaling and pointwise approximate-action checks; universal resultant template is neither implemented nor benchmarked.','fixed_p':str(p),'scaling_cases':rows,'pointwise_approx_action_checks':checks,'queries_with_multiple_allowed_actions':multiple}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
