from fractions import Fraction as R
from collections import defaultdict
from decimal import Decimal,localcontext
from pathlib import Path
import json,hashlib,time
start=time.time()
source=Path(__file__).resolve().with_name('overwritten_product_exact_dual.json')
raw=source.read_bytes();p=json.loads(raw)
# Construct the physical graph geometrically, independent of producer edge lists.
xy=[(column,row) for column in range(4) for row in range(2)]
edges=[(i,j) for i in range(8) for j in range(8) if abs(xy[i][0]-xy[j][0])+abs(xy[i][1]-xy[j][1])==1]
deg=[sum(i==u for u,v in edges) for i in range(8)]
type_of=[d-2 for d in deg]
assert len(edges)==20 and type_of==[0,0,1,1,1,1,0,0]
B=lambda n:R('2.676')*n*(n-1)+R('108.102')
A=lambda n:R('.040')*n*(n-1)*(n-2)+R('37.881')*n
D=R('8.2207');coeff=[R(0)]*326;coeff[50]=coeff[163+50]=4
mass=R(0);kill=R(0);target_entrance_rows=0;overflow_rows=0;seen=set()
perms=[[2*(3-c if fc else c)+(1-r if fr else r) for c,r in xy] for fc in (False,True) for fr in (False,True)]
for perm in perms:assert {(perm[i],perm[j]) for i,j in edges}==set(edges)
full=[R(0)]*(8*163)
for i in range(8):full[i*163+50]=1
for item in p['weights']:
 x=tuple(item['state']);w=R(item['weight'])
 assert len(x)==8 and all(type(n)==int and 0<=n<=162 for n in x)
 assert max(x)>15 and w>0 and x not in seen;seen.add(x)
 mass+=w;row=defaultdict(R);fullrow=defaultdict(R);rowkill=R(0);target=False
 def add(y,rate):
  global rowkill,target
  if not rate:return
  if max(y)>162:
   assert max(y)==163
   rowkill+=rate
   return # killed transition has constant -rate, derivative zero
  if max(y)<=15:
   target=True
   for i in range(8):
    row[type_of[i]*163+x[i]]-=rate
    fullrow[i*163+x[i]]-=rate
   return # fixed target payoff one has zero destination log derivative
  for i in range(8):
   row[type_of[i]*163+y[i]]+=rate
   row[type_of[i]*163+x[i]]-=rate
   fullrow[i*163+y[i]]+=rate
   fullrow[i*163+x[i]]-=rate
 for i in range(8):
  y=list(x);y[i]+=1;add(y,B(x[i]))
  if x[i]:y=list(x);y[i]-=1;add(y,A(x[i]))
 for i,j in edges:
  if x[i]:y=list(x);y[i]-=1;y[j]+=1;add(y,D*x[i])
 for k,v in row.items():coeff[k]+=w*v
 for perm in perms:
  for k,v in fullrow.items():
   i,n=divmod(k,163);full[perm[i]*163+n]+=w*v/4
 kill+=w*rowkill
 target_entrance_rows+=target;overflow_rows+=rowkill>0
expected=[R(0)]*326;
assert coeff==expected
expectedfull=[R(0)]*(8*163)

assert full==expectedfull
assert 0<mass<1 and 0<kill<R(3,10**22)
assert mass==R(p['total_weight']) and kill==R(p['kill_charge'])
with localcontext() as c:
 c.prec=45
 dec=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
 out={'source_sha256':hashlib.sha256(raw).hexdigest(),'positive_distinct_actual_state_weights':len(seen),'all_states_transient':True,'all_326_coordinate_identities_exact':True,'all_1304_site_specific_identities_after_four_exact_graph_automorphisms':True,'surviving_coordinates':{},'total_weight_descriptive':dec(mass),'total_weight_strictly_below_one':True,'overflow_charge_descriptive':dec(kill),'overflow_charge_strictly_below':'3/10^22','rows_with_overflow':overflow_rows,'rows_with_target_entrance':target_entrance_rows,'certified_log_envelope_lower':'-3/10^22','certified_envelope_floor':'1-3/10^22 (strict)','elapsed_seconds_descriptive':time.time()-start}
print(json.dumps(out,indent=2))
