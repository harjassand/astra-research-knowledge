"""Independent circuit receiver. No candidate imports; no cover enumeration.
Shares this audit's separately written exact raw parser/encoding only.
"""
from fractions import Fraction as Q
from collections import deque
import independent_cover_receiver as S
FAMILY='dominating-cover-polynomial-inventory-circuit-v1'

def compile_inventory(rec):
 vs=rec['satellites'];adj={v:set() for v in vs}
 for u,v in rec['edges']:adj[u].add(v);adj[v].add(u)
 rows=[];neighbor_tests=pair_tests=0
 for anchor in vs:
  anti=tuple(v for v in vs if v!=anchor and v not in adj[anchor]);unseen=set(anti);isolates=[];blocks=[]
  neighbor_tests+=len(anti)**2
  while unseen:
   seed=min(unseen);queue=deque([seed]);color={seed:0};unseen.remove(seed)
   while queue:
    v=queue.popleft()
    for w in sorted(adj[v]&set(anti)):
     if w in color:assert color[w]!=color[v]
     else:color[w]=1-color[v];unseen.remove(w);queue.append(w)
   if len(color)==1:isolates.append(seed)
   else:
    left=tuple(sorted(v for v in color if color[v]==0));right=tuple(sorted(v for v in color if color[v]==1))
    assert all(v in adj[u] for u in left for v in right);pair_tests+=len(left)*len(right);blocks.append((left,right))
  rows.append(dict(anchor=anchor,isolates=tuple(isolates),bicliques=tuple(blocks)))
 return dict(vertices=vs,edges=rec['edges'],anchors=tuple(rows),work=dict(anchors=len(vs),anti_neighborhood_tests=len(vs)**2,component_neighbor_tests=neighbor_tests,biclique_pair_tests=pair_tests),formula='tau=sum satellite counts-max_anchor(anchor count+isolated counts+sum max(biclique shore totals))')

def independent_weight(circuit,x):
 scores=[]
 for row in circuit['anchors']:
  total=x[row['anchor']]+sum(x[v] for v in row['isolates'])
  for left,right in row['bicliques']:total+=max(sum(x[v] for v in left),sum(x[v] for v in right))
  scores.append(total)
 return max(scores)
def cover_weight(circuit,x):return sum(x[v] for v in circuit['vertices'])-independent_weight(circuit,x)
def optimal_minimal_cover(circuit,x):
 candidates=[]
 for row in circuit['anchors']:
  chosen=set(row['isolates'])|{row['anchor']}
  for left,right in row['bicliques']:
   chosen.update(max((left,right),key=lambda shore:sum(x[v] for v in shore)))
  candidates.append(chosen)
 chosen=max(candidates,key=lambda vertices:sum(x[v] for v in vertices));adj={v:set() for v in circuit['vertices']}
 for u,v in circuit['edges']:adj[u].add(v);adj[v].add(u)
 for v in circuit['vertices']:
  if v not in chosen and chosen.isdisjoint(adj[v]):assert x[v]==0;chosen.add(v)
 return tuple(v for v in circuit['vertices'] if v not in chosen)
def bad_active_edges(circuit,x):
 optimum=independent_weight(circuit,x);answer=[]
 for u,v in circuit['edges']:
  if x[u]>0 and x[v]>0:
   changed={w:(0 if w in (u,v) else x[w]) for w in circuit['vertices']}
   if independent_weight(circuit,changed)==optimum:answer.append((u,v))
 return tuple(answer)

def qual(rec):
 old=S.qual(rec)
 return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],conclusion=old['conclusion'],role=old['role'],graph=old['graph'],inventory=compile_inventory(rec),work=dict(raw=rec['work'],cover_masks_enumerated=0,profile_steps=0,states_enumerated=0,stationary_fiber_laws=0),cost_scope='Raw forbidden-pattern scans and polynomial-size anti-neighborhood max-plus circuit; explicit profile not materialized')
def qualitative(raw):
 try:return qual(S.parse(raw))
 except S.Outside as e:return dict(status='UNKNOWN',family=FAMILY,reason=str(e),stability='UNKNOWN')

def numerical(raw,t,max_profile_steps=100000):
 t=S.rational(t)
 if t<=1:raise ValueError('t>1 required')
 if type(max_profile_steps) is not int or max_profile_steps<0:raise ValueError('nonnegative exact integer budget')
 try:r=S.parse(raw)
 except S.Outside as e:return dict(status='UNKNOWN',family=FAMILY,reason=str(e),stability='UNKNOWN')
 lam,mu=r['lam'],r['mu'];E=len(r['edges']);m=len(r['satellites'])
 Kf=r['a_sum']+m*r['kplus'];beta=r['bmin']/(16*E);L=lam*(t-1);eps0=min(Q(1),(lam+beta)/2)
 c=4*(L+eps0)/beta;K=max(2,S.ceiling(2*c));D=mu*(1-1/t)
 eps=min(Q(1,4),D/(4*(r['F0']+D)),eps0/(4*mu));J=max(K+1,2,S.ceiling(4*c*(mu+Kf+beta)/D));steps=K+J-2
 if steps>max_profile_steps:return dict(status='UNKNOWN_NUMERICAL_BUDGET',family=FAMILY,qualitative=qual(r),required_profile_steps=steps,max_profile_steps=max_profile_steps,scope='qualitative stability CERTIFIED; requested explicit quantitative construction not acquired')
 head=[None]*(K+1);head[K]=1+c/K
 for k in reversed(range(1,K)):head[k]=head[k+1]*(lam*t+beta*k*k)/(lam+beta*k*k-eps0)
 head[0]=2*t*head[1]
 def g(k):return head[k] if k<=K else 1+c/k
 def d(k):return g(k)-g(k+1)
 dstar=min([c]+[(k+1)**2*d(k) for k in range(1,K)]);G=max([Q(3)]+[d(k-1)/d(k) for k in range(1,K+1)])
 best=Q(0)
 for k in range(1,J):
  val=mu*(g(k-1)/t-g(k))+Kf*k*d(k-1)+2*beta*k*d(k)+eps*(r['F0']+D)
  best=max(best,4*(k+1)**2*max(val,0)/r['kminus'])
 q=1+best;delta=min(Q(1,2*r['n']),Q(1,2*E),r['bmin']/(8*E*r['smax']*G));Ccore=12*lam*t+12*mu;Ce=11*Kf+Ccore
 Cint=2*L+2*mu+(2*c+11)*r['S']/delta**2+Ccore;kap=min(D*delta/4,eps*r['b0']*delta**2/(32*E))
 Nstar=S.ceiling(max(Q(1),q,Q(K)/delta,88*q*r['smax']/(r['bmin']*dstar),4*q*Ce/eps0,(Cint+1)/kap))
 zeta=min(eps0,lam)/4;H=head[0]+q/4;cf=(zeta+lam+mu*Nstar+r['S']*Nstar**2)*H
 co=dict(Kf=Kf,beta=beta,L=L,epsilon0=eps0,c=c,K=K,D=D,epsilon=eps,J=J,dstar=dstar,G=G,q=q,delta=delta,Ccore=Ccore,Ce=Ce,Cint=Cint,kappa=kap,Nstar=Nstar,zeta=zeta,H=H)
 out=dict(status='CERTIFIED_NUMERICAL',family=FAMILY,raw_sha256=r['raw_sha256'],t=t,qualitative=qual(r),inventory=compile_inventory(r),constants=co,profile_head=tuple(head[:K]),Foster=dict(coefficient=cf,base=t,exponent=Nstar+1),stationary_moment=dict(coefficient=2*cf/zeta,base=t,exponent=Nstar+1),work=dict(profile_steps=steps,cover_masks_enumerated=0,states_enumerated=0,expanded_Foster_powers=0,stationary_fiber_laws=0),cost_scope='Polynomial inventory-circuit acquisition/evaluation after raw scans; profile-loop budget is not rational bit or wall-time cap. Powers stay factored. No polynomial-bit complete quantitative acquisition claim.')
 out['work']['retained_scalar_bits']=S.maxbits(out);return out

def receive_qualitative(raw,receipt):return S.canonical(qualitative(raw))==S.canonical(receipt)
def receive_numerical(raw,t,receipt,**budgets):return S.canonical(numerical(raw,t,**budgets))==S.canonical(receipt)
def scaled_drift(rec,cert,x):
 co=cert['constants'];t=cert['t'];a=rec['a']
 def h(z):
  N=sum(z);A=z[a];r=A+cover_weight(cert['inventory'],z);g=cert['profile_head'][r] if r<co['K'] else 1+co['c']/r
  return g+co['q']*Q(A,(N+1)*(r+1)**2)-co['epsilon']*Q(A,N+1)
 old=h(x);ans=Q(0)
 for u,v,k in rec['channels']:
  for xx,uu in zip(x,u):
   if xx<uu:k=Q(0);break
   for j in range(uu):k*=xx-j
  if k:
   y=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));ans+=k*(t**(sum(v)-sum(u))*h(y)-old)
 return ans
