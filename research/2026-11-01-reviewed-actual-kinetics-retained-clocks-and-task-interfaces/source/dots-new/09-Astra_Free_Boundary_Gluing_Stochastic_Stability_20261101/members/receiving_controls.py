from fractions import Fraction as F
from itertools import permutations
import copy,json
import free_port_glue as G
raw=G.fixture();rec=G.recognize(raw);cert=G.construct(raw,F(2));qual=G.qualitative(raw)
counts=dict(qualitative_mutations=0,symbolic_mutations=0,coordinate_permutations=0,numerical_permutations=0,domain_refusals=0,structural_unknowns=0,budget_controls=0,normalization_controls=0,bit_guard_controls=0)
for key in qual:
 bad=copy.deepcopy(qual);bad[key]=None
 assert not G.receive_qualitative(raw,bad);counts['qualitative_mutations']+=1
for key in cert['constants']:
 bad=copy.deepcopy(cert);bad['constants'][key]+=1
 assert not G.receive_symbolic(raw,F(2),bad);counts['symbolic_mutations']+=1
for key in ['t','family','status','raw_sha256','qualitative','core_profile','free_profile','symbolic_head','Foster','work','cost_scope']:
 bad=copy.deepcopy(cert);bad[key]=None
 assert not G.receive_symbolic(raw,F(2),bad);counts['symbolic_mutations']+=1
for j,perm in enumerate(permutations(range(5))):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw];qq=G.qualitative(rr)
 assert qq['status']=='CERTIFIED_QUALITATIVE'and qq['roles']['open_coordinate']==perm.index(0)and qq['roles']['free_coordinate']==perm.index(4)
 counts['coordinate_permutations']+=1
 if j in (0,37,83,119):
  cc=G.construct(rr,F(2));rc=G.recognize(rr)
  assert cc['constants']==cert['constants']and cc['symbolic_head']==cert['symbolic_head']
  for x in [(0,1,1,1,10**30),(1,0,1,0,10**30),(2,0,0,0,10**30),(0,10**30,1,1,10**30)]:
   y=tuple(x[i]for i in perm)
   assert G.scaled_pieces(rc,cc,y)==G.scaled_pieces(rec,cert,x)
  counts['numerical_permutations']+=1

def refuse(fn):
 try:fn()
 except(TypeError,ValueError):counts['domain_refusals']+=1
 else:raise AssertionError('missing domain refusal')
for bad in (True,2.0,'2',F(1),0,-1,None):refuse(lambda bad=bad:G.construct(raw,bad))
for bad in (True,1.0,-1,None):
 refuse(lambda bad=bad:G.construct(raw,F(2),max_profile_steps=bad));refuse(lambda bad=bad:G.expand_head(cert,bad))
for bad in (True,1.0,'1',F(1),-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];u=list(u);u[2]=bad;rr[0]=(u,v,k);refuse(lambda rr=rr:G.qualitative(rr))
for bad in (True,1.0,'1',0,-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,bad);refuse(lambda rr=rr:G.qualitative(rr))
for bad in (True,1.0,'1',-1,None):refuse(lambda bad=bad:G.outside_head(cert,bad))
for bad in (True,1.0,F(1),0,-1,None):refuse(lambda bad=bad:G.dyadic(bad))
for bad in (True,1.0,0,-1,None):refuse(lambda bad=bad:G.ceil_log2(bad))
for bad in (None,{},iter(raw),[],[(raw[0][0],raw[0][1])]):refuse(lambda bad=bad:G.qualitative(bad))
assert G.construct(raw,F(2),max_profile_steps=0)['status']=='UNKNOWN_PROFILE_BUDGET';counts['budget_controls']+=1
assert G.expand_head(cert,100000)['status']=='UNKNOWN_POWER_EXPANSION_BUDGET';counts['budget_controls']+=1
rr=copy.deepcopy(raw)
for j,(u,v,k)in enumerate(rr):
 if sum(v)==0:rr[j]=(u,v,F(1,10**100))
cc=G.construct(rr,F(2),max_profile_steps=10);assert cc['status']=='UNKNOWN_PROFILE_BUDGET'and cc['qualitative']['status']=='CERTIFIED_QUALITATIVE';counts['budget_controls']+=1
# Guard uses supplied binary input size; it never expands an astronomical power merely to reject.
artificial={'symbolic_head':dict(exponent=10**100,coefficients=(F(1),F(1),F(1)))}
assert not G.outside_head(artificial,10**1000)
assert G.expand_head(artificial,100000)['required_power_bits']==10**100+1;counts['bit_guard_controls']+=2
# A power-bit cap is not falsely a cap on the total expanded head output.
small={'symbolic_head':dict(exponent=12,coefficients=(F(1),F(1),F(1)))}
assert G.expand_head(small,13).bit_length()>13;counts['bit_guard_controls']+=1
u,v,k=raw[2];rr=raw[:2]+[(u,v,k/3),(u,v,2*k/3)]+raw[3:]+[((1,0,0,0,0),(1,0,0,0,0),F(7))]
assert G.recognize(rr)['raw_sha256']==rec['raw_sha256']and G.construct(rr,F(2))['constants']==cert['constants'];counts['normalization_controls']+=1
# Well-typed structural UNKNOWN controls. Reversible all-unit cases below are ordinary wins; the missing-reverse case is only UNKNOWN.
z=lambda *ix:tuple(ix.count(i)for i in range(5))
negatives=[raw[:-1],raw+[(z(0,4),z(1,3),F(1)),(z(1,3),z(0,4),F(1))],raw+[(z(0,0),z(1,4),F(1)),(z(1,4),z(0,0),F(1))]]
for rr in negatives:
 q=G.qualitative(rr);assert q['status']=='UNKNOWN'and q['stability']=='UNKNOWN';counts['structural_unknowns']+=1
core=G.C.B.fixture();assert G.qualitative(core)['status']=='UNKNOWN';counts['structural_unknowns']+=1
# Two free ports over a triangle leave a forbidden pattern in either prospective core.
rr=[(tuple(u)+(0,),tuple(v)+(0,),F(1))for u,v,k in raw];zz=lambda *ix:tuple(ix.count(i)for i in range(6));rr.extend([(zz(0,5),zz(1,2),F(1)),(zz(1,2),zz(0,5),F(1))])
assert G.qualitative(rr)['status']=='UNKNOWN';counts['structural_unknowns']+=1
# Explicitly verify the intended ordinary reversible all-unit controls, not the missing-edge case.
for rr in [negatives[1],negatives[2],rr]:
 unit=[(u,v,F(1))for u,v,k in rr];pairs={(u,v)for u,v,k in unit}
 assert all((v,u)in pairs for u,v in pairs)and G.qualitative(unit)['status']=='UNKNOWN'
print(json.dumps(dict(status='PASS_AUTHOR_RECEIVING' ,counts=counts,scope='Same-implementation self-checks, not independent receiving; symbolic head not expanded',all_unit_unknowns_are_not_instability_claims=True),indent=2))
