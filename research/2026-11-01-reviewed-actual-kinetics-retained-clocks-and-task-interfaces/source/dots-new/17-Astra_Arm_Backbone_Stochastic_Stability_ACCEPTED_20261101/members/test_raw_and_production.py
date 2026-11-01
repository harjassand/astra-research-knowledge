"""NEW recovery raw/cost/production preflight; exact independent test oracles."""
from fractions import Fraction as F
from itertools import combinations,permutations
import json
import arm_backbone as B
A,G=B.A,B.G
counts={}
def hit(k):counts[k]=counts.get(k,0)+1

def forbidden(es,vs):
 e={frozenset(z)for z in es}
 for size,ds in[(4,[0,2,2,2]),(5,[0,1,1,2,2])]:
  for sub in combinations(vs,size):
   if sorted(sum(frozenset((v,w))in e for w in sub if w!=v)for v in sub)==ds:return True
 return False

def raw_of(m,armed,aux):
 n=m+1;z=lambda *ix:tuple(ix.count(i)for i in range(n));hs=[z(*e)for e in armed];raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for e in armed+aux:h=z(*e);raw.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
 for x,i in sorted({(1,i)for i in range(len(hs))}|{(x,0)for x in range(1,n)}):raw.extend([(z(0,x),hs[i],F(1)),(hs[i],z(0,x),F(1))])
 return raw
for m in range(2,6):
 es=list(combinations(range(1,m+1),2))
 for mask in range(1,1<<len(es)):
  armed=[e for i,e in enumerate(es)if mask>>i&1];unused=[e for e in es if e not in armed]
  for aux in {(),tuple(unused),tuple(unused[::2])}:
   raw=raw_of(m,armed,list(aux));incident={v for e in armed for v in e};bad=forbidden(armed,sorted(incident));q=B.qualitative(raw)
   assert(q['status']=='UNKNOWN')==bad;hit('raw_cases');hit('unknown'if bad else'accepted')
   if not bad:
    r=B.recognize(raw);assert set(r['edges'])==set(armed)and set(h['edge']for h in r['auxiliary'])==set(aux)
    assert set(r['free'])==set(range(1,m+1))-incident
armed=[(1,2),(2,3),(3,4),(5,6)];aux=[e for e in combinations(range(1,7),2)if e not in armed]
assert forbidden(armed,range(1,7))and B.qualitative(raw_of(6,armed,aux))['status']=='UNKNOWN';hit('P4_separate_edge_control')
armed=[(1,2),(1,3),(2,3),(4,5)];aux=[e for e in combinations(range(1,6),2)if e not in armed];raw=raw_of(5,armed,aux)
assert B.qualitative(raw)['status']=='UNKNOWN'and G.C.B.qualitative(raw)['status']=='CERTIFIED_QUALITATIVE';hit('ordinary_previous_route_win')
# Unit rates have pairwise detailed balance at all-ones: no UNKNOWN instability.
assert all(k==1 for u,v,k in raw);hit('unit_rate_detailed_balance_control')
raw=B.fixture();r=B.recognize(raw);c=B.construct(raw,2);n=r['n']
for perm in list(permutations(range(n)))[:120]:
 rr=[(tuple(u[j]for j in perm),tuple(v[j]for j in perm),k)for u,v,k in raw];qq=B.recognize(rr);inv={old:new for new,old in enumerate(perm)}
 assert qq['a']==inv[r['a']]and set(qq['free'])=={inv[x]for x in r['free']};hit('coordinate_permutations')
split=[]
for u,v,k in reversed(raw):split.extend([(u,v,k/3),(u,v,2*k/3)])
assert B.recognize(split)['raw_sha256']==r['raw_sha256'];hit('duplicate_normalization')
required=c['plan']['core_profile_steps'];assert B.construct(raw,2,required-1)['status']=='UNKNOWN_CORE_PROFILE_BUDGET';assert G.canonical(B.construct(raw,2,required))==G.canonical(c);hit('exact_loop_boundary')
for t,scale in[(F(1001,1000),1000),(F(3,2),7),(F(2),F(1,1000000))]:
 rr=[(u,v,k*(scale if sum(u)==2 and u[r['a']]==0 else 1))for u,v,k in raw]
 cc=B.construct(rr,t,0);assert cc['status']=='UNKNOWN_CORE_PROFILE_BUDGET'and cc['qualitative']['status']!='UNKNOWN';hit('budget_refusal_retains_qualitative')
for t in(True,1.2,'2',None,0,1):
 try:B.construct(raw,t)
 except(ValueError,TypeError):hit('invalid_requested_t')
 else:raise AssertionError('invalid t')
# Actual 27-species/133-detour production receipt with exhaustive helpers disabled.
m=24;n=m+3;v=lambda *ix:tuple(ix.count(i)for i in range(n));free=tuple(range(3,n))
edges={tuple(sorted((free[i],free[(i+1)%m])))for i in range(m)}|{(free[i],free[j])for i in range(m)for j in range(i+1,m)if(31*i+17*j)%7<3}|{(3,4),(4,5),(3,5)}
H=v(1,2);raw=[(v(),v(0),F(1)),(v(0),v(),F(1)),(v(0,0),H,F(1)),(H,v(0,0),F(1))]
for x in range(1,n):raw.extend([(v(0,x),H,F(1)),(H,v(0,x),F(2 if x==2 else 1))])
for i,j in sorted(edges):raw.extend([(v(0,0),v(i,j),F(1,len(edges))),(v(i,j),v(0,0),F(1,len(edges)))])
assert G.C.B.qualitative(raw)['status']=='UNKNOWN'and A.qualitative(raw)['status']=='UNKNOWN'
def fail(*a,**k):raise AssertionError('production called exhaustive helper')
saved=[(G.C.B,'covers',G.C.B.covers),(G.C.B,'numerical',G.C.B.numerical),(G.C,'numerical',G.C.numerical)]
for mod,key,old in saved:setattr(mod,key,fail)
pc=B.construct(raw,2);assert B.receive_symbolic(raw,2,json.loads(G.canonical(pc)))
for mod,key,old in saved:setattr(mod,key,old)
pr=B.recognize(raw);assert pr['free']==free and len(pr['edges'])==1 and len(pr['auxiliary'])==133 and pr['aD']==pr['BD']==1
assert len(G.canonical(pc).encode())==150663 and G.digest(pc)=='181979210f47b93a7d8b8e21a2b726ae0f5161360ae2a5b8397901df61619442'
production=dict(species=n,free_species=m,armed_hubs=1,auxiliary_hubs=133,channels=len(raw),core_steps=pc['plan']['core_profile_steps'],work=pc['work'],canonical_bytes=150663,canonical_sha256=G.digest(pc),full_graph_cover_masks=0,ordinary_nonCB='a²=bc, ab=bc, ac=2bc => b=a,c=2a => bc=2a² != a²')
print(json.dumps(G.encode(dict(status='PASS_NEW_RECOVERY_RAW_AND_PRODUCTION',counts=counts,production=production,scope='New test bytes. Same-author receiving only; old successful source is not inferred from matching receipts. No global powers expanded or instability conclusion.')),indent=2))
