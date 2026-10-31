#!/usr/bin/env python3
"""Independent raw, mathematical certificate, and acquisition-transcript receiver.
Does not call the candidate recognizer, derive, or search functions.
"""
from fractions import Fraction as F
from itertools import product,permutations
from math import prod,isqrt
import hashlib,json


def wire(x):return json.loads(json.dumps(x,default=lambda z:str(z) if type(z) is F else (_ for _ in ()).throw(TypeError(type(z)))))
def canonical(x):return json.dumps(wire(x),sort_keys=True,separators=(',',':'))
def bits(x):
 stack=[x];peak=0
 while stack:
  a=stack.pop()
  if type(a) is F:peak=max(peak,abs(a.numerator).bit_length(),a.denominator.bit_length())
  elif type(a) is int:peak=max(peak,abs(a).bit_length())
  elif isinstance(a,dict):stack.extend(a.values())
  elif isinstance(a,(tuple,list)):stack.extend(a)
 return peak
def rat(x):
 if type(x) not in (int,F):raise ValueError('exact rational required')
 return F(x)
def ceilq(x):return (x.numerator+x.denominator-1)//x.denominator
def ceilroot(x):
 k=isqrt(x.numerator//x.denominator)
 return k+int(k*k*x.denominator<x.numerator)

def recognize(raw):
 assert type(raw) in (list,tuple) and raw
 grouped={};n=None
 for row in raw:
  assert type(row) in (list,tuple) and len(row)==3
  u,v,k=row;assert type(u) in (list,tuple) and type(v) in (list,tuple)
  if n is None:n=len(u)
  assert n>=2 and len(u)==len(v)==n and all(type(x)is int and x>=0 for x in tuple(u)+tuple(v))
  k=rat(k);assert k>0;u=tuple(u);v=tuple(v)
  if u!=v:grouped[u,v]=grouped.get((u,v),F(0))+k
 channels=tuple((u,v,k) for (u,v),k in sorted(grouped.items()));zero=(0,)*n
 nc=[(u,v,k)for u,v,k in channels if sum(u)!=sum(v)];assert len(nc)==2
 births=[(u,v,k)for u,v,k in nc if u==zero and sum(v)==1];assert len(births)==1
 _,e,lam=births[0];a=e.index(1);assert (e,zero)in grouped;mu=grouped[e,zero]
 internal=[]
 for u,v,k in channels:
  if sum(u)!=sum(v):assert (u,v)in [(zero,e),(e,zero)];continue
  assert u[a]>=1 and v[a]>=1 and 2<=sum(u)<=3
  internal.append((tuple(x-int(i==a)for i,x in enumerate(u)),tuple(x-int(i==a)for i,x in enumerate(v)),k))
 adj={u:set() for u,v,k in channels}|{v:set() for u,v,k in channels}
 for u,v,k in channels:adj[u].add(v)
 reaches={}
 for start in adj:
  seen={start};front={start}
  while front:
   nxt=set().union(*(adj[v]for v in front))-seen;seen|=nxt;front=nxt
  reaches[start]=seen
 assert all(u in reaches[v]for u,v,k in channels)
 visits=sum(sum(len(adj[z])for z in reaches[v])for u,v,k in channels)
 return dict(n=n,a=a,satellites=tuple(j for j in range(n)if j!=a),lam=lam,mu=mu,channels=channels,internals=tuple(internal),raw_sha256=hashlib.sha256(canonical(channels).encode()).hexdigest(),input_rows=len(raw),graph_edge_visits=visits)

def derive(rec,t,weights):
 t=rat(t);assert t>1;ws=tuple(map(rat,weights));n=rec['n'];A=rec['a'];J=rec['satellites'];assert len(ws)==len(J) and all(0<=x<=1 for x in ws)
 v=[F(0)]*n;v[A]=1
 for j,w in zip(J,ws):v[j]=w
 jumps=[sum(a*(y-x)for a,x,y in zip(v,u,z))for u,z,k in rec['internals']];ell=1+max([F(0)]+[abs(x)for x in jumps]);co={}
 for (u,z,k),delta in zip(rec['internals'],jumps):co[u]=co.get(u,F(0))+k*(delta/ell if delta>=0 else ell*delta)
 pure=tuple(co.get(tuple(2*int(i==j)for i in range(n)),F(0))for j in J);reasons=[]
 if any(u<=0 for u in pure):reasons.append('nonpositive pure satellite effective coefficient')
 for j,k in [(j,k)for j in J for k in J if j<k]:
  if co.get(tuple(int(i==j)+int(i==k)for i in range(n)),F(0))<0:reasons.append('negative mixed satellite effective coefficient')
 base=dict(t=t,weights=ws,ell=ell,source_coefficients=tuple((u,co[u])for u in sorted(co)),pure=pure)
 if reasons:return dict(status='PROFILE_REJECTED',reasons=reasons,**base)
 K1=max([F(0)]+[-g for u,g in co.items()if sum(u)==1]);K2=max([F(0)]+[-g for u,g in co.items()if sum(u)==2 and u[A]>0]);K0=K1+K2;K=K0+sum((u+K0)**2/(2*u)for u in pure)
 D=rec['mu']*(1-1/t);c=min(F(1),D/(4*K));C=rec['lam']*(t-1)+3*rec['mu']+D;zeta=min(rec['lam']/4,D/4,F(1));S=sum(w*w/u for w,u in zip(ws,pure));strength=c/(4*(1+c)*S)if S else None
 other=dict(K1=K1,K2=K2,K=K,D=D,c=c,C=C,zeta=zeta,S=S,head_strength=strength)
 if S and strength<C+zeta:return dict(status='PROFILE_REJECTED',reasons=['finite-head compatibility failed'],**base,**other)
 Ac=max(2,ceilq(4*(C+zeta)/(3*D)));threshold=9*Ac*Ac/S if S else 2*(1+c)*(C+zeta)*Ac*Ac/c;cuts=tuple(max(1,ceilroot(threshold/u))for u in pure);count=(Ac-1)*prod(cuts);Nmax=Ac-1+sum(z-1 for z in cuts);h0=2*t*(1+c);prefactor=(C+zeta)*h0
 return dict(status='CERTIFIED_REQUESTED_T_MOMENT',raw_sha256=rec['raw_sha256'],dimension=n,open_coordinate=A,satellite_coordinates=J,**base,**other,A_cut=Ac,B_cuts=cuts,tail_threshold=threshold,exception_states_not_enumerated=count,N_max=Nmax,h0=h0,
 foster_constant_factored=dict(prefactor=prefactor,base=t,exponent=Nmax,expanded_numerator_bits_upper=prefactor.numerator.bit_length()+Nmax*t.numerator.bit_length(),expanded_denominator_bits_upper=prefactor.denominator.bit_length()+Nmax*t.denominator.bit_length()),guarantee='classwise positive recurrence and stationary t^N moment; not automatically all t')

def receive(raw,t,weights,cert):
 try:expected=derive(recognize(raw),t,weights)
 except (AssertionError,ValueError,TypeError,KeyError):return False
 return expected['status']=='CERTIFIED_REQUESTED_T_MOMENT' and type(cert)is dict and canonical(cert)==canonical(expected)

def match(rec):
 if rec['n']!=3 or len(rec['internals'])!=6:return None
 A=rec['a'];observed={(u,v):k for u,v,k in rec['internals']}
 for B,C in permutations(rec['satellites']):
  def vec(a,b,c):
   x=[0]*3;x[A]=a;x[B]=b;x[C]=c;return tuple(x)
  rB=vec(1,1,0);BC=vec(0,1,1);rC=vec(1,0,1);BB=vec(0,2,0);CC=vec(0,0,2)
  edges=[(rB,BC),(BC,rB),(rC,BB),(BB,rC),(BC,CC),(CC,BC)]
  if set(edges)==set(observed):return B,C,tuple(observed[e]for e in edges)
 return None

def structural(raw):
 rec=recognize(raw);found=match(rec)
 if found is None:return dict(status='UNKNOWN',reason='not the proved halving skeleton')
 B,C,rates=found
 return dict(status='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS',raw_sha256=rec['raw_sha256'],open_coordinate=rec['a'],mediator_coordinate=B,other_satellite_coordinate=C,dimension=rec['n'],guarantee='every closed communicating class positive recurrent; every stationary exp(theta*N) moment finite, theta>0',numerical_foster_constants_provided=False,profile_evaluations=0,recognition_input_rows=rec['input_rows'],recognition_graph_edge_visits=rec['graph_edge_visits'],candidate_orientations_upper_bound=2)

def receive_structural(raw,cert):
 try:r=structural(raw)
 except (AssertionError,ValueError,TypeError,KeyError):return False
 return r['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS' and type(cert)is dict and canonical(r)==canonical(cert)

def hard_audit(raw,t,bundle):
 rec=recognize(raw);found=match(rec);assert found is not None;B,C,rate=found;a1,b1,a2,b2,a3,b3=rate;t=rat(t);assert t>1
 eta0=min(F(1,4),b1/(4*a3));Kmax=2*max(a1,a2);umin=b2/4;umax=b2/2;v0=b3/2
 Kbar=eta0*(Kmax+(umax+Kmax)**2/(2*umin))+Kmax*Kmax/(2*v0)+Kmax*eta0+v0*eta0*eta0/2;D=rec['mu']*(1-1/t);CC=rec['lam']*(t-1)+3*rec['mu']+D;zeta=min(rec['lam']/4,D/4,F(1));c0=min(F(1),D/(4*Kbar));req=c0*umin/(8*(CC+zeta))
 bound=1;last=eta0
 while last>req:last/=2;bound+=1
 eta=eta0;peak=bits([rec,Kbar,c0,req,last]);trials=[];reported=bundle['acquisition'];ntests=reported['profiles'];assert type(ntests)is int and 1<=ntests<=bound
 for i in range(ntests):
  w=tuple(eta if j==B else F(0)for j in rec['satellites']);cert=derive(rec,t,w);assert cert.get('K',F(0))<=Kbar/eta
  assert cert['c']>=c0*eta and cert['head_strength']>=c0*umin/(8*eta)
  trials.append(dict(eta=eta,certificate_status=cert['status'],head_strength=cert.get('head_strength')));peak=max(peak,bits(cert))
  if i<ntests-1:assert cert['status']=='PROFILE_REJECTED' and eta>req
  eta/=2
 expected=dict(route='recognized mediated triangle halving',profiles=ntests,source_term_evaluations=ntests*len(rec['internals']),trials=trials,guaranteed_trials=bound,guarantee_bound_halvings=bound-1,eta0=eta0,eta_required_sufficient=req,Kbar=Kbar,c0=c0,retained_rational_peak_bits=peak,recognition_input_rows=rec['input_rows'],recognition_graph_edge_visits=rec['graph_edge_visits'],cap_scope='profile count only; does not cap termination-bound preprocessing or bit/memory cost',all_t_qualitative='proved termination for every rational t>1; hence every finite exponential stationary moment')
 assert canonical(reported)==canonical(expected)
 if bundle['status']=='CERTIFIED':assert cert['status']=='CERTIFIED_REQUESTED_T_MOMENT' and canonical(bundle['certificate'])==canonical(cert)
 else:assert bundle['status']=='UNKNOWN' and cert['status']=='PROFILE_REJECTED'
 if 'qualitative'in bundle:assert receive_structural(raw,bundle['qualitative'])
 return cert

def grid_audit(raw,t,bundle):
 rec=recognize(raw);target=bundle['acquisition']['profiles'];assert type(target)is int and target>=1;m=rec['n']-1;peak=bits(rec);count=0;q=1;last=None
 while count<target:
  for ks in product(range(q+1),repeat=m):
   if count==target:break
   cert=derive(rec,t,tuple(F(k,q)for k in ks));count+=1;peak=max(peak,bits(cert));last=cert
   if count<target:assert cert['status']=='PROFILE_REJECTED'
  if count<target:q+=1
 # UNKNOWN uses the enumeration cursor at which the next profile cap check fires.
 if bundle['status']=='UNKNOWN' and sum((r+1)**m for r in range(1,q+1))==target:q+=1
 ac=bundle['acquisition'];assert ac['route']=='rational grid' and ac['cap_scope']=='profile count only; not total bit/preprocessing/memory cost';assert ac['profiles']==count and ac['source_term_evaluations']==count*len(rec['internals']) and ac['last_denominator']==q and ac['retained_rational_peak_bits']==peak and ac['repeated_profiles_charged'] is True
 if bundle['status']=='CERTIFIED':assert last['status']=='CERTIFIED_REQUESTED_T_MOMENT' and canonical(last)==canonical(bundle['certificate']);assert ac['recognition_input_rows']==len(raw) and ac['recognition_graph_edge_visits']==rec['graph_edge_visits']
 else:assert bundle['status']=='UNKNOWN' and last['status']=='PROFILE_REJECTED'
 return last

def ff(x,u):
 if any(a<b for a,b in zip(x,u)):return 0
 return prod(prod(range(a-b+1,a+1))for a,b in zip(x,u))
def generator_checker(raw,t,weights,receipt):
 rec=recognize(raw);cert=derive(rec,t,weights);assert receive(raw,t,weights,receipt);A=rec['a'];J=rec['satellites'];w=tuple(map(F,weights));c=cert['c'];t=F(t)
 co={tuple(u):g for u,g in cert['source_coefficients']}
 def h(x):return cert['h0'] if not x[A] else 1+c/(x[A]+sum(a*x[j]for a,j in zip(w,J)))
 def check(x):
  assert len(x)==rec['n'] and all(type(z)is int and z>=0 for z in x);N=sum(x);hx=h(x);assert 1<=hx<=cert['h0'];out=lint=F(0)
  for u,v,k in rec['channels']:
   rate=k*ff(x,u)
   if not rate:continue
   y=tuple(z-a+b for z,a,b in zip(x,u,v));out+=rate*(t**(sum(v)-sum(u))*h(y)/hx-1)
   if sum(u)==sum(v):
    lint+=rate*(h(y)-hx);r=list(x);r[A]-=1;us=tuple(z-int(i==A)for i,z in enumerate(u));assert rate==x[A]*k*ff(r,us)
    R=x[A]+sum(a*x[j]for a,j in zip(w,J));Rp=y[A]+sum(a*y[j]for a,j in zip(w,J));assert R/cert['ell']<=Rp<=cert['ell']*R and Rp>=1
  if not x[A]:assert lint==0 and out<=-rec['lam']/2
  else:
   r=list(x);r[A]-=1;psi=sum(g*ff(r,u)for u,g in co.items());Q=sum(u*x[j]**2 for u,j in zip(cert['pure'],J));R=x[A]+sum(a*x[j]for a,j in zip(w,J));negative=c*x[A]*Q/(2*(1+c)*R*R)
   assert lint<=-c*x[A]*psi/R**2 and psi>=Q/2-cert['K']*x[A]**2
   assert lint/hx<=c*cert['K']*x[A]-negative
   assert out<=cert['C']-3*cert['D']*x[A]/4-negative
  outside=not x[A] or x[A]>=cert['A_cut'] or any(x[j]>=cut for j,cut in zip(J,cert['B_cuts']))
  if outside:assert out<=-cert['zeta']
  else:assert N<=cert['N_max'] and out<=cert['C']
  return out
 return rec,cert,check
