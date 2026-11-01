"""Independent trusted exact receiver for the frozen cover-seed construction.
Imports no constructor or earlier stability implementation. Generic raw-validation
scaffolding is ordinary reused design. Qualitative parsing never enumerates covers;
quantitative covers are generated as complements of maximal independent sets.
"""
from fractions import Fraction as Q
from itertools import combinations
import hashlib,json,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
FAMILY='dominating-cover-seed-three-energy-v1'
class Outside(ValueError):pass

def rational(v):
 if type(v) not in (int,Q):raise TypeError('exact int/Fraction required')
 return Q(v)
def wire(v):
 if type(v) is Q:return str(v)
 if isinstance(v,dict):return {str(k):wire(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [wire(x) for x in v]
 return v
def canonical(v):return json.dumps(wire(v),sort_keys=True,separators=(',',':'))
def digest(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
def ceiling(v):return (v.numerator+v.denominator-1)//v.denominator
def maxbits(v):
 if type(v) is Q:return max(abs(v.numerator).bit_length(),v.denominator.bit_length())
 if type(v) is int:return abs(v).bit_length()
 if isinstance(v,dict):return max([0]+[maxbits(x) for x in v.values()])
 if isinstance(v,(list,tuple)):return max([0]+[maxbits(x) for x in v])
 return 0

def parse(raw):
 if type(raw) not in (list,tuple) or not raw:raise ValueError('nonempty raw list')
 n=None;table={};coords=0
 for row in raw:
  if type(row) not in (list,tuple) or len(row)!=3:raise ValueError('reaction triple')
  u,v,k=row
  if type(u) not in (list,tuple) or type(v) not in (list,tuple):raise TypeError('complex vectors')
  if n is None:n=len(u)
  if n<3 or len(u)!=n or len(v)!=n:raise ValueError('fixed dimension n>=3')
  for x in list(u)+list(v):
   coords+=1
   if type(x) is not int or x<0:raise ValueError('nonnegative exact integer counts')
  k=rational(k)
  if k<=0:raise ValueError('strictly positive rate')
  u,v=tuple(u),tuple(v)
  if u!=v:table[u,v]=table.get((u,v),Q(0))+k
 channels=tuple((u,v,k) for (u,v),k in sorted(table.items()));zero=(0,)*n
 noncon=[(u,v) for u,v,k in channels if sum(u)!=sum(v)];ports=[]
 for a in range(n):
  one=tuple(int(i==a) for i in range(n))
  if len(noncon)==2 and set(noncon)=={(zero,one),(one,zero)}:ports.append(a)
 if len(ports)!=1:raise Outside('requires one exact reversible port')
 a=ports[0];one=tuple(int(i==a) for i in range(n));two=tuple(2*int(i==a) for i in range(n))
 internal=tuple(row for row in channels if sum(row[0])==sum(row[1]));hubs={}
 for u,v,k in internal:
  for z in (u,v):
   if sum(z)!=2:raise Outside('only binary nonnull internals')
   occupied=tuple(i for i,x in enumerate(z) if x)
   if not z[a]:
    if len(occupied)!=2 or any(z[i]!=1 for i in occupied):raise Outside('hub must be square-free satellite pair')
    hubs[z]=occupied
   elif z==two:pass
   elif z[a]==1:
    rest=[i for i in occupied if i!=a]
    if len(rest)!=1 or z[rest[0]]!=1:raise Outside('active complex must be A+X')
   else:raise Outside('unrecognized active complex')
 if not hubs:raise Outside('at least one hub required')
 for u,v,k in internal:
  if (u in hubs)==(v in hubs):raise Outside('only hub/active edges')
  if (v,u) not in table:raise Outside('every included edge must be reversible')
 vs=tuple(i for i in range(n) if i!=a);edges=tuple(sorted(hubs.values()));adj={i:set() for i in vs}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 tests=0
 # Induced adjacency test, independent of all vertex-cover enumeration.
 for size in (4,5):
  for sub in combinations(vs,size):
   tests+=1;induced=[(u,v) for u,v in combinations(sub,2) if v in adj[u]]
   if len(induced)!=3:continue
   deg={i:sum(i in e for e in induced) for i in sub}
   if sum(v==0 for v in deg.values())!=1:continue
   nonzero=sorted(v for v in deg.values() if v)
   if (size==4 and nonzero==[2,2,2]) or (size==5 and nonzero==[1,1,2,2]):raise Outside('forbidden cover-domination pattern on '+str(sub))
 kx={i:Q(0) for i in vs};rows=[]
 for h,edge in sorted(hubs.items()):
  if (two,h) not in table or (h,two) not in table:raise Outside('every hub needs 2A amplification pair')
  arms=[]
  for x in vs:
   arm=tuple(int(i==a)+int(i==x) for i in range(n))
   if (arm,h) in table:
    kx[x]+=table[arm,h];arms.append((x,table[arm,h],table[h,arm]))
  rows.append(dict(complex=h,edge=edge,to_hub=table[two,h],to_two_a=table[h,two],reverse_sum=table[h,two]+sum((k for _,_,k in arms),Q(0)),arms=tuple(arms)))
 if min(kx.values())<=0:raise Outside('each satellite needs a forward/reverse arm')
 aa=sum((z['to_hub'] for z in rows),Q(0))
 return dict(n=n,a=a,lam=table[zero,one],mu=table[one,zero],channels=channels,internal=internal,satellites=vs,edges=edges,hubs=tuple(rows),kX=tuple(sorted(kx.items())),kminus=min(kx.values()),kplus=max(kx.values()),a_sum=aa,bmin=min(h['to_two_a'] for h in rows),smax=max(h['reverse_sum'] for h in rows),b0=min(h['reverse_sum']+h['to_two_a'] for h in rows),F0=2*aa+max(kx.values()),S=sum((k for u,v,k in internal),Q(0)),raw_sha256=digest(channels),work=dict(input_rows=len(raw),normalized_channels=len(channels),raw_coordinate_checks=coords,internal_complex_checks=2*len(internal),reverse_edge_tests=len(internal),forbidden_pattern_tests=tests,amplification_edge_tests=2*len(hubs),arm_incidence_tests=len(hubs)*len(vs)))

def minimal_covers(rec):
 vs=rec['satellites'];edges=rec['edges'];adj={v:set() for v in vs}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 found=[];full=(1<<len(vs))-1
 for mask in range(1<<len(vs)):
  independent={vs[i] for i in range(len(vs)) if mask>>i&1}
  if any(u in independent and v in independent for u,v in edges):continue
  if any(not (adj[v]&independent) for v in vs if v not in independent):continue
  found.append((full^mask,tuple(v for v in vs if v not in independent)))
 return tuple(v for mask,v in sorted(found))

def qual(rec):
 work=dict(rec['work']);work.update(cover_masks_enumerated=0,profile_steps=0,states_enumerated=0,stationary_fiber_laws=0)
 return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',role=dict(dimension=rec['n'],open_coordinate=rec['a'],immigration=rec['lam'],death=rec['mu']),inventory='A+minimum weighted structural vertex-cover count; no supplied cover oracle',graph=dict(vertices=rec['satellites'],edges=rec['edges'],excluded_induced_patterns=['triangle plus isolate','P4 plus isolate']),work=work)
def qualitative(raw):
 try:return qual(parse(raw))
 except Outside as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def numerical(raw,t,max_profile_steps=100000,max_cover_masks=1048576):
 t=rational(t)
 if t<=1:raise ValueError('t>1 required')
 if any(type(v) is not int or v<0 for v in (max_profile_steps,max_cover_masks)):raise ValueError('nonnegative exact integer budget')
 try:r=parse(raw)
 except Outside as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
 lam,mu=r['lam'],r['mu'];E=len(r['edges']);m=len(r['satellites'])
 Kf=r['a_sum']+m*r['kplus'];beta=r['bmin']/(16*E);L=lam*(t-1);eps0=min(Q(1),(lam+beta)/2)
 c=4*(L+eps0)/beta;K=max(2,ceiling(2*c));D=mu*(1-1/t)
 eps=min(Q(1,4),D/(4*(r['F0']+D)),eps0/(4*mu));J=max(K+1,2,ceiling(4*c*(mu+Kf+beta)/D));steps=K+J-2;masks=1<<m
 if steps>max_profile_steps or masks>max_cover_masks:
  return dict(status='UNKNOWN_NUMERICAL_BUDGET',family=FAMILY,qualitative=qual(r),required_profile_steps=steps,required_cover_masks=masks,max_profile_steps=max_profile_steps,max_cover_masks=max_cover_masks,scope='qualitative stability CERTIFIED; requested explicit quantitative construction not acquired')
 head=[None]*(K+1);head[K]=1+c/K
 for k in reversed(range(1,K)):
  den=lam+beta*k*k-eps0;assert den>0
  head[k]=head[k+1]*(lam*t+beta*k*k)/den
 head[0]=2*t*head[1]
 def g(k):return head[k] if k<=K else 1+c/k
 def d(k):return g(k)-g(k+1)
 dstar=min([c]+[(k+1)**2*d(k) for k in range(1,K)]);G=max([Q(3)]+[d(k-1)/d(k) for k in range(1,K+1)])
 best=Q(0)
 for k in range(1,J):
  val=mu*(g(k-1)/t-g(k))+Kf*k*d(k-1)+2*beta*k*d(k)+eps*(r['F0']+D)
  best=max(best,4*(k+1)**2*max(val,0)/r['kminus'])
 q=1+best;delta=min(Q(1,2*r['n']),Q(1,2*E),r['bmin']/(8*E*r['smax']*G))
 Ccore=12*lam*t+12*mu;Ce=11*Kf+Ccore;Cint=2*L+2*mu+(2*c+11)*r['S']/delta**2+Ccore
 kap=min(D*delta/4,eps*r['b0']*delta**2/(32*E));Nstar=ceiling(max(Q(1),q,Q(K)/delta,88*q*r['smax']/(r['bmin']*dstar),4*q*Ce/eps0,(Cint+1)/kap))
 zeta=min(eps0,lam)/4;H=head[0]+q/4;cf=(zeta+lam+mu*Nstar+r['S']*Nstar**2)*H
 cv=minimal_covers(r)
 co=dict(Kf=Kf,beta=beta,L=L,epsilon0=eps0,c=c,K=K,D=D,epsilon=eps,J=J,dstar=dstar,G=G,q=q,delta=delta,Ccore=Ccore,Ce=Ce,Cint=Cint,kappa=kap,Nstar=Nstar,zeta=zeta,H=H)
 out=dict(status='CERTIFIED_NUMERICAL',family=FAMILY,raw_sha256=r['raw_sha256'],t=t,qualitative=qual(r),covers=cv,constants=co,profile_head=tuple(head[:K]),Foster=dict(coefficient=cf,base=t,exponent=Nstar+1),stationary_moment=dict(coefficient=2*cf/zeta,base=t,exponent=Nstar+1),work=dict(profile_steps=steps,cover_masks_enumerated=masks,retained_covers=len(cv),states_enumerated=0,expanded_Foster_powers=0,stationary_fiber_laws=0),cost_scope='Budgets cap only the stated profile-loop and cover-mask counts, not rational bit cost or wall time. Powers stay factored. No polynomial-bit quantitative acquisition claim.')
 out['work']['retained_scalar_bits']=maxbits(out);return out

def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_numerical(raw,t,receipt,**budgets):return canonical(numerical(raw,t,**budgets))==canonical(receipt)
