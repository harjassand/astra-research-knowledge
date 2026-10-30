import itertools,json,math
from pathlib import Path
rows=[120,102,85];C=[0]
for v in rows:C += [x^v for x in C]
V=[{c^(127 if z else 0):1/math.sqrt(8) for c in C} for z in (0,1)]
def action(v,supp,ps):
 o={}
 for w,a in v.items():
  for i,p in zip(supp,ps):
   bit=(w>>i)&1
   if p=='Y':a*=1j*(-1)**bit
   elif p=='Z':a*=(-1)**bit
   if p in ('X','Y'):w^=1<<i
  o[w]=a
 return o
def matrix(supp,ps):
 EV=[action(v,supp,ps) for v in V]
 return [[sum(a.conjugate()*EV[j].get(w,0) for w,a in V[i].items()) for j in range(2)] for i in range(2)]
mx=0;n=0
for t in range(3):
 for supp in itertools.combinations(range(7),t):
  for ps in itertools.product('XYZ',repeat=t):
   M=matrix(supp,ps);c=M[0][0]
   mx=max(mx,abs(M[0][1]),abs(M[1][0]),abs(M[1][1]-c));n+=1
boundary=0
for supp in itertools.combinations(range(7),3):
 for ps in itertools.product('XYZ',repeat=3):
  M=matrix(supp,ps);boundary=max(boundary,abs(M[0][1]),abs(M[1][0]),abs(M[1][1]-M[0][0]))
r={'operators_below_distance':n,'max_local_indistinguishability_residual':mx,'weight_equal_distance_non_scalar_witness':boundary,'scope':'Steane algebra check of strict erasure support margin, not polynomial-code gadget certification'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
