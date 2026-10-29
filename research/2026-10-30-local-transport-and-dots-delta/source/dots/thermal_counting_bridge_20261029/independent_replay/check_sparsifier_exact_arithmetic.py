from fractions import Fraction as F
from math import comb,ceil,log2
from pathlib import Path
import json
identity_cases=0
for q in range(1,21):
 for p in [F(0),F(1,7),F(1,3),F(1,2),F(6,7),F(1)]:
  probs=[F(comb(q,x))*p**x*(1-p)**(q-x) for x in range(q+1)]
  for D in range(q+2):
   lhs=sum((x*probs[x] for x in range(q+1) if x>D),F(0))
   rhs=q*p*sum((F(comb(q-1,x))*p**x*(1-p)**(q-1-x) for x in range(q) if x>=D),F(0))
   assert lhs==rhs
   identity_cases+=1
# Valid support/parameter family, deliberately rare sample sequences forcing trimming.
n=64;g=F(1);eps=F(1,2);L=F(n,2)
q=ceil(512*L*L/(eps*eps*n));lam=512*g*g/(eps*eps)+4*g/eps
D=ceil(9*lam)+ceil(log2(max(F(2),200*g/eps)))
forced=[]
for label,samples in [('both_endpoints_high',[(0,1,q)]),('high_and_retained',[(0,1,19200),(2,3,q-19200)]),('one_high_hub',[(0,1,12000),(0,2,12000),(3,4,q-24000)])]:
 degree=[0]*n
 for u,v,c in samples:degree[u]+=c;degree[v]+=c
 bad={v for v,x in enumerate(degree) if x>D}
 kept=[(u,v,c) for u,v,c in samples if u not in bad and v not in bad]
 deleted=sum(c for u,v,c in samples if u in bad or v in bad)
 upper=sum(degree[v] for v in bad)
 final=[0]*n
 for u,v,c in kept:final[u]+=c;final[v]+=c
 assert deleted<=upper and max(final)<=D
 forced.append({'case':label,'bad_vertices':sorted(bad),'deleted_occurrences':deleted,'bad_incidence_upper_bound':upper,'remaining_max_degree':max(final),'deleted_norm_budget':str(L*deleted/q)})
out={'exact_binomial_identity_cases':identity_cases,'forced_sample_parameters':{'n':n,'g':str(g),'epsilon':str(eps),'L':str(L),'q':q,'D':D},'forced_trimming_cases':forced,'scope':'Exact rational binomial identity and combinatorial trimming checks, including rare forced sample sequences under valid theoretical parameters; no statistical tail validation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
