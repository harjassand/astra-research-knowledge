from itertools import permutations
from fractions import Fraction as F
from copy import deepcopy
import json
import aggregate_mass as A
G=A.G
counts=dict(qualitative_permutations=0,symbolic_permutations=0,normalizations=0,structural_unknowns=0,domain_refusals=0,budget_controls=0,production_no_exhaustive=0,extreme_tail_plans=0)
raw=A.fixture();base=A.qualitative(raw);cert=A.construct(raw,2)
for perm in permutations(range(5)):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw]
 q=A.qualitative(rr);assert q['status']==base['status'];assert q['open_coordinate']==perm.index(0)and q['free_coordinates']==(perm.index(4),);counts['qualitative_permutations']+=1
for perm in ((4,3,2,1,0),(1,2,3,4,0),(0,2,1,4,3)):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw];c=A.construct(rr,2)
 assert c['plan']==cert['plan']and c['mass_head']==cert['mass_head'];counts['symbolic_permutations']+=1
u,v,k=raw[3];rr=raw[:3]+[(u,v,k/3),(u,v,2*k/3)]+raw[4:]+[(u,u,F(17))]
assert G.canonical(A.construct(rr,2))==G.canonical(cert);counts['normalizations']+=1
# No isolated coordinate, no reversible pair, and unrecognized residual graph.
neg=[[(tuple(u[:4]),tuple(v[:4]),k)for u,v,k in raw if not(u[4]or v[4])],raw[:-1]]
n=7;z=lambda *ix:tuple(ix.count(i)for i in range(n));hubs=[z(1,2),z(1,3),z(2,3),z(4,5)]
rr=[(z(),z(0),F(1)),(z(0),z(),F(1))]
for h in hubs:rr.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
for x in range(1,n):rr.extend([(z(0,x),hubs[0],F(1)),(hubs[0],z(0,x),F(1))])
neg.append(rr)
for rr in neg:
 assert A.qualitative(rr)['status']=='UNKNOWN';counts['structural_unknowns']+=1
# Third negative is ordinary detailed balance at the all-ones point, not instability.
assert all(k==1 for u,v,k in neg[-1])and all(any(v==p and u==q for p,q,l in neg[-1])for u,v,k in neg[-1])
for budget in (0,cert['plan']['core_profile_steps']-1):
 cc=A.construct(raw,2,budget);assert cc['status']=='UNKNOWN_CORE_PROFILE_BUDGET'and cc['qualitative']==base;counts['budget_controls']+=1
assert G.canonical(A.construct(raw,2,cert['plan']['core_profile_steps']))==G.canonical(cert);counts['budget_controls']+=1
def reject(fn):
 try:fn()
 except(ValueError,TypeError):counts['domain_refusals']+=1
 else:raise AssertionError('expected invalid-domain rejection')
for bad in (True,2.0,'2',1,0,-1,None):reject(lambda bad=bad:A.construct(raw,bad))
for bad in (True,1.0,'1',-1,None):reject(lambda bad=bad:A.construct(raw,2,bad))
for bad in (True,1.0,'1',0,-1,None):
 rr=deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,bad);reject(lambda rr=rr:A.qualitative(rr))
for bad in (True,1.0,'1',F(1),-1,None):
 rr=deepcopy(raw);u,v,k=rr[0];u=list(u);u[1]=bad;rr[0]=(u,v,k);reject(lambda rr=rr:A.qualitative(rr))
# The production finder and symbolic plan do not call exhaustive covers or old numerical finders.
def forbidden(*a,**k):raise AssertionError('unpaid exhaustive path')
saved=[(G.C.B,'covers',G.C.B.covers),(G.C.B,'numerical',G.C.B.numerical),(G.C,'numerical',G.C.numerical)]
for module,name,fn in saved:setattr(module,name,forbidden)
assert G.canonical(A.construct(raw,2))==G.canonical(cert);counts['production_no_exhaustive']+=1
for module,name,fn in saved:setattr(module,name,fn)
# Joint arbitrary ratios are acquired or honestly refused by the explicit core-loop cap.
extremes=[]
for t,scale in ((F(1001,1000),F(1000)),(F(3,2),F(7)),(F(17,2),F(1,1000))):
 rr=[]
 for i,(u,v,k)in enumerate(A.fixture(2)):
  kk=k*(scale if i%3==0 else 1/scale if i%3==1 else 1);rr.append((u,v,kk))
 cc=A.construct(rr,t,max_core_steps=100000)
 assert cc['status']in('UNKNOWN_CORE_PROFILE_BUDGET','SYMBOLIC_FOSTER_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW')
 extremes.append(dict(t=t,scale=scale,status=cc['status'],required_core_steps=cc.get('required_core_steps'),actual_K=cc.get('mass_head',{}).get('K')));counts['extreme_tail_plans']+=1
print(json.dumps(G.encode(dict(status='PASS_AUTHOR_STRUCTURAL_AND_DOMAIN_CONTROLS',counts=counts,extremes=extremes,full_canonical_main_bytes=len(G.canonical(cert).encode()),main_canonical_sha256=G.digest(cert),largest_retained_scalar_bits=cert['work']['largest_retained_scalar_bits'],new_mass_head_powers_expanded=0,scope='Same-author controls, not independent semantic receiving or whole proof acceptance')),indent=2))
