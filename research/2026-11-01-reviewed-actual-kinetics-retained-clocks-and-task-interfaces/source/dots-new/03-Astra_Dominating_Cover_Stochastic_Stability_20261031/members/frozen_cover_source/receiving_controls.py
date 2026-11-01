from fractions import Fraction as F
from itertools import permutations
import copy,json
import cover_seed as C
raw=C.fixture();qual=C.qualitative(raw)
counts=dict(qualitative_mutations=0,numerical_field_mutations=0,coordinate_permutations=0,numerical_permutations=0,domain_refusals=0,structural_unknowns=0,normalization_controls=0,budget_controls=0)
for key in qual:
 bad=copy.deepcopy(qual)
 if isinstance(bad[key],dict):bad[key]['forged']=True
 else:bad[key]=None
 assert not C.receive_qualitative(raw,bad);counts['qualitative_mutations']+=1
base=C.numerical(raw,F(2));pfields=['t','raw_sha256','covers','profile_head','Foster','stationary_moment','work','cost_scope','status','family','qualitative']
for key in pfields:
 bad=copy.deepcopy(base)
 if isinstance(bad[key],dict):bad[key]['forged']=True
 else:bad[key]=None
 assert not C.receive_numerical(raw,F(2),bad);counts['numerical_field_mutations']+=1
for j,perm in enumerate(permutations(range(5))):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw]
 got=C.qualitative(rr);assert got['status']=='CERTIFIED_QUALITATIVE'and got['role']['open_coordinate']==perm.index(0)
 assert C.receive_qualitative(rr,got);counts['coordinate_permutations']+=1
 if j in (0,23,73,119):
  cc=C.numerical(rr,F(2));rc=C.recognize(rr)
  assert cc['constants']==base['constants']
  for x in [(0,1,1,0,10**30),(0,10**30,1,1,10**30),(1,0,0,0,10**30)]:
   y=tuple(x[i]for i in perm)
   assert C.scaled_drift(rc,cc,y)==C.scaled_drift(C.recognize(raw),base,x)
  counts['numerical_permutations']+=1

def refuses(fn):
 try:fn()
 except (TypeError,ValueError):counts['domain_refusals']+=1
 else:raise AssertionError('missing domain refusal')
for bad in (None,{},iter(raw),[],[(raw[0][0],raw[0][1])]):refuses(lambda bad=bad:C.qualitative(bad))
for value in (True,1.0,'1',F(1),-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];u=list(u);u[2]=value;rr[0]=(u,v,k);refuses(lambda rr=rr:C.qualitative(rr))
for value in (True,1.0,'1',0,-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,value);refuses(lambda rr=rr:C.qualitative(rr))
for value in (True,0.0,-1,None):
 refuses(lambda value=value:C.numerical(raw,F(2),max_profile_steps=value))
 refuses(lambda value=value:C.numerical(raw,F(2),max_cover_masks=value))
for field in ('max_profile_steps','max_cover_masks'):
 got=C.numerical(raw,F(2),**{field:0});assert got['status']=='UNKNOWN_NUMERICAL_BUDGET'and got['qualitative']==qual;counts['budget_controls']+=1
# Near-one request or tiny death can require enormous explicit loops; qualitative stays acquired.
rr=copy.deepcopy(raw)
for j,(u,v,k)in enumerate(rr):
 if sum(v)==0:rr[j]=(u,v,F(1,10**100))
got=C.numerical(rr,F(2),max_profile_steps=1000);assert got['status']=='UNKNOWN_NUMERICAL_BUDGET'and got['qualitative']['status']=='CERTIFIED_QUALITATIVE';counts['budget_controls']+=1
# Duplicate/null normalization is exact after validating every row.
u,v,k=raw[2];rr=raw[:2]+[(u,v,k/3),(u,v,2*k/3)]+raw[3:]+[((1,0,0,0,0),(1,0,0,0,0),F(7))]
assert C.recognize(rr)['raw_sha256']==C.recognize(raw)['raw_sha256']
assert C.numerical(rr,F(2))['constants']==base['constants'];counts['normalization_controls']+=1
# Reversibility, port, arm, and binary-architecture failures are UNKNOWN, not instability.
aa=(2,0,0,0,0);bc=(0,1,1,0,0);ab=(1,1,0,0,0)
neg=[raw[:-1],[r for r in raw if (r[0],r[1])not in [(aa,bc),(bc,aa)]],[r for r in raw if r[0]!=ab and r[1]!=ab],raw+[(aa,ab,1),(ab,aa,1)],raw+[((0,0,0,0,0),(0,1,0,0,0),1),((0,1,0,0,0),(0,0,0,0,0),1)],raw+[((3,0,0,0,0),(0,3,0,0,0),1),((0,3,0,0,0),(3,0,0,0,0),1)]]
for rr in neg:
 got=C.qualitative(rr);assert got['status']=='UNKNOWN'and got['stability']=='UNKNOWN';counts['structural_unknowns']+=1
print(json.dumps(dict(status='PASS',counts=counts,receiving_status='same-implementation author self-checks, not independent receiving',no_simulation=True),indent=2))
