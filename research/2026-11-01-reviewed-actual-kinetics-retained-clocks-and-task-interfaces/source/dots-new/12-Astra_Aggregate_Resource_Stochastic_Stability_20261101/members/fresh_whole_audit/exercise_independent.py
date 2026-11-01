from fractions import Fraction as F
from itertools import product,combinations,permutations
from copy import deepcopy
from pathlib import Path
import json,sys,random,time,os
import independent_aggregate_receiver as I
SRC=Path(os.environ.get('AGGREGATE_SOURCE_DIR','producer-workspace/stochastic_free_aggregate_mass_pending_20261031'));sys.path.insert(0,str(SRC));import aggregate_mass as A
OUT=Path(__file__).resolve().parent;counts={}
def hit(k,n=1):counts[k]=counts.get(k,0)+n
def fixture(edges,nrare,nfree=2,hetero=False):
 n=1+nrare+nfree;z=lambda *ix:tuple(ix.count(i)for i in range(n));hs=[z(*e)for e in edges];raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for h in hs:raw.extend(((z(0,0),h,F(1)),(h,z(0,0),F(1))))
 for x in range(1,nrare+1):
  h=hs[(x-1)%len(hs)];raw.extend(((z(0,x),h,F(1)),(h,z(0,x),F(2 if x==nrare else 1))))
 for f in range(nrare+1,n):
  targets=[h for k,h in enumerate(hs)if not hetero or (k+f)%3!=0]
  if not targets:targets=hs[:1]
  for k,h in enumerate(targets):raw.extend(((z(0,f),h,F((k+1 if hetero else 1))), (h,z(0,f),F((f-nrare if hetero else 1)))))
 return raw

def cover(r,x):
 vals=[]
 for mask in range(1<<len(r['rare'])):
  s={v for i,v in enumerate(r['rare'])if mask>>i&1}
  if all(u in s or v in s for u,v in r['edges']):vals.append(sum(x[v]for v in s))
 return min(vals)
def zval(r,c,x):
 N,a,f,u,j,R=I.coords(r,x);g=I.evaluate(I.mass_g(c,j));assert isinstance(g,F)
 return g-1+c['plan']['mass']['rho']*F(a,(j+1)**2)
def coreval(r,c,x):
 N,a,f,u,j,R=I.coords(r,x);co=c['plan']['core'];return I.P.g(c['plan']['core_profile'],R)+co['rho0']*F(a,(R+1)**2)-co['e']*F(a,N+1)
def generator(r,c,x,fn,selection=lambda u,v:True):
 old=fn(x);val=F(0)
 for u,v,rate,y in I.P.enabled(r,x):
  if selection(u,v):val+=rate*(c['t']**(sum(v)-sum(u))*fn(y)-old)
 return val

def make_state(r,u,a,pattern,f,distribution=0):
 x=[0]*r['n'];x[r['a']]=a;remaining=u-a
 if pattern==0:x[r['rare'][0]]=remaining
 else:
  vv=r['rare'][:min(pattern,len(r['rare']))]
  for i,v in enumerate(vv):x[v]=remaining//len(vv)+(i<remaining%len(vv))
 if distribution==0:x[r['free'][0]]=f
 else:
  for i,v in enumerate(r['free']):x[v]=f//len(r['free'])+(i<f%len(r['free']))
 return tuple(x)
raws=[A.fixture(),A.fixture(2),fixture(((1,2),(2,3),(3,4)),4,2,True),fixture(((1,2),(2,3),(3,4),(4,5),(1,5)),5,2,True),fixture(((1,2),(3,4)),4,2,True)]
reports=[]
for ix,raw in enumerate(raws):
 r=I.parse(raw);c=I.construct(raw,F(2));other=A.construct(raw,F(2));assert I.canonical(c)==I.canonical(other);hit('complete_receipt_matches')
 assert r['free']==A.recognize(raw)['free'];K=c['mass_head']['K'];p=c['plan'];co=p['core'];m=p['mass']
 # Actual huge-K boundary calculations (only low exponents are expanded).
 for j in range(K-8,K+5):
  g=I.evaluate(I.mass_g(c,j));g1=I.evaluate(I.mass_g(c,j+1));g2=I.evaluate(I.mass_g(c,j+2))
  assert g-g1>=F(1,(j+1)**2)
  if j<K:assert g>=2*c['t']*(g2+m['rho'])
  hit('actual_mass_join_values')
 assert I.evaluate(I.mass_g(c,0),1000)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET';hit('actual_power_refusals')
 assert I.outside_head(c,10**5000) is False;hit('nested_head_shortcuts')
 # Exact physical generator in low-cover cone, independently of free-to-core ratio.
 for power in (1,2):
  U=max(K*4,co['U0'])**power
  for a in (0,1,2,p['core_profile']['K']):
   for bulk in r['rare']:
    x=[0]*r['n'];x[r['a']]=a;x[bulk]=U-a;x[r['free'][-1]]=U**3+7;x=tuple(x)
    N,aa,f,u,j,R=I.coords(r,x);assert R<=co['delta']*u
    drift=generator(r,c,x,lambda y:coreval(r,c,y));assert drift<=-co['zeta0']*coreval(r,c,x);hit('actual_low_core_generator')
 # Local rational-tail cone: never mislabel as the actual global free cone.
 dt=min(F(1,4),m['rho']*r['kfree']/(4*((r['a_sum']+r['krplus'])*8+4*m['rho']*r['mu']+1)))
 for U in (4*K,K*K):
  for a in (0,1,2,U//3):
   for pattern in (0,2,len(r['rare'])):
    for distribution in (0,1):
     x=make_state(r,U,a,pattern,I.ceil(4*F(U+1)/dt),distribution);N,aa,f,u,j,R=I.coords(r,x)
     assert R==a+cover(r,x);hit('independent_cover_values')
     lz=generator(r,c,x,lambda y:zval(r,c,y));lc=generator(r,c,x,lambda y:coreval(r,c,y));Q=sum(x[v]*x[w]for v,w in r['edges'])
     bound=m['B']/F(j+1)-r['bmin']*Q/(2*(j+1)**2)-m['rho']*r['kfree']*a*f/(2*(j+1)**2)
     assert lz<=bound and lc+m['eta']*lz<=-c['mass_head']['nu'];hit('actual_tail_combined_states')
     if R>co['delta']*u:assert lz<=-m['cfree'];hit('actual_active_mass_cone')
 # Synthetic heads only test algebra, not their missing full K thresholds.
 for smallK in (8,17):
  cc=deepcopy(c);cc['plan']['mass']['K']=smallK;cc['mass_head']=I.head(cc['plan'],r);h=cc['mass_head'];rho=m['rho'];BH=h['Q']**smallK;CZ=h['C']*BH+2+rho/2;D2=9*h['C']*BH;Ddeath=9*r['mu']*h['C']*BH/cc['t']+4*rho*r['mu']
  for j in range(0,smallK+30):
   gg=I.evaluate(I.mass_g(cc,j));g1=I.evaluate(I.mass_g(cc,j+1));g2=I.evaluate(I.mass_g(cc,j+2));assert gg-g1>=F(1,(j+1)**2)
   if j<smallK:assert gg>=2*cc['t']*(g2+rho)
   assert (j+1)*(gg-1)+rho*F(j,2*(j+1))<=CZ
   if j:assert (j+1)**2*(I.evaluate(I.mass_g(cc,max(0,j-2)))-gg)<=D2
   if j>=2:assert r['mu']*(j+1)**2*max((I.evaluate(I.mass_g(cc,j-2))-1)/cc['t']-(gg-1),0)+4*rho*r['mu']<=Ddeath
   hit('synthetic_geometric_bound_points')
  for U in (0,1,2,3,7,8,9,16,17,18,30):
   for aa in sorted({0,min(1,U),min(2,U),U//2,U}):
    for pattern in (0,2,len(r['rare'])):
     x=make_state(r,U,aa,pattern,5,1);N,a,f,u,j,R=I.coords(r,x);oldf=F(a,(j+1)**2)
     for src,dst,rate,y in I.P.enabled(r,x):
      if sum(src)!=sum(dst):continue
      _,ap,fp,up,jp,Rp=I.coords(r,y);diff=F(ap,(jp+1)**2)-oldf
      if src[r['a']]:assert diff<=0;hit('forward_phase_sign')
      else:assert diff<=F(2,(j+1)**2);hit('reverse_phase_upper')
      if any(src[v]or dst[v]for v in r['free']):assert j==jp;hit('aggregate_resource_neutrality')
      hit('enabled_channel_checks')
     Q=sum(x[v]*x[w]for v,w in r['edges'])
     rev=generator(r,cc,x,lambda y:zval(r,cc,y),lambda u,v:sum(u)==sum(v)and u[r['a']]==0)
     birth=generator(r,cc,x,lambda y:zval(r,cc,y),lambda u,v:sum(v)==sum(u)+1)
     death=generator(r,cc,x,lambda y:zval(r,cc,y),lambda u,v:sum(v)==sum(u)-1)
     assert rev<=-r['bmin']*Q/F(2*(j+1)**2)
     assert birth<=(-r['lam']/2 if j<smallK else m['B']/F(j+1))
     assert death<=Ddeath*a/F((j+1)**2);hit('synthetic_physical_generator_states')
  # Cutoff crossings including last-copy J -> J-2, arbitrary free allocation.
  for width in (1,3):
   for U in (0,1,2,3,8,17,40):
    for a in sorted({0,min(1,U),min(2,U),U}):
     for pattern in (0,len(r['rare'])):
      for shift in (3,4,4+width,5+width):
       for off in (-1,0,1):
        x=make_state(r,U,a,pattern,max(0,((U+1)<<shift)+off-1),1)
        def phi(y):
         _,_,ff,uu,_,_=I.coords(r,y);return min(F(1),max(F(0),(I.P.dyadic(ff+1)-I.P.dyadic(uu+1)-4)/width))
        ph=phi(x);cross=F(0);direct=F(0);old=coreval(r,cc,x)+m['eta']*ph*zval(r,cc,x)
        for src,dst,rate,y in I.P.enabled(r,x):
         dif=phi(y)-ph;tilt=cc['t']**(sum(dst)-sum(src));zz=zval(r,cc,y);cross+=rate*tilt*zz*dif
         direct+=rate*(tilt*(coreval(r,cc,y)+m['eta']*phi(y)*zz)-old)
         if dif>0:
          hit('positive_cutoff_jumps');hit('zero_crossings',int(ph==0));hit('one_crossings',int(phi(y)==1 and ph<1))
          _,_,_,_,jp,_=I.coords(r,y)
          if sum(dst)==sum(src)-1:
           assert jp==U+a-2 and jp+1>=U and zz<=CZ/F(U);hit('last_copy_deaths',int(a==1))
        assert cross<=4*CZ*(r['ell']*len(r['edges'])+r['mu'])/width
        lc=generator(r,cc,x,lambda y:coreval(r,cc,y));lz=generator(r,cc,x,lambda y:zval(r,cc,y))
        assert direct==lc+m['eta']*(ph*lz+cross);hit('synthetic_cutoff_product_states')
 reports.append(dict(raw_sha256=r['raw_sha256'],free=len(r['free']),rare=len(r['rare']),edges=r['edges'],core_steps=p['core_profile_steps'],K=K,receipt_sha256=I.digest(c)))
 print('Completed fixture',ix,flush=True)

# Nested expression execution at small algebraic parameters, not complete certificates.
r=I.parse(raws[0]);c=I.construct(raws[0],2);s=deepcopy(c);s['mass_head'].update(K=2,Q=2,L0=0,Jcoef=1,outer_head_coefficients=(F(1),F(1),F(1)))
e=I.expressions(r,s);threshold=int(I.evaluate(e['Nstar'],1000))
for N in (0,1,threshold-1,threshold,threshold+1,2*threshold):assert I.outside_head(s,N)==(N>=threshold);hit('nested_threshold_exact_comparisons')
assert I.evaluate(e['Bhead'])==4 and I.evaluate(e['cutoff_exponent'])==5
for cap in (0,10,1000):assert I.evaluate(I.expressions(r,c)['Nstar'],cap)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET';hit('nested_expansion_refusals')
for N in (0,1,10**100,10**5000):assert not I.outside_head(c,N);hit('nested_head_shortcuts')
for x in ((0,0,0,0,10**100),(1,2,3,4,100),(0,0,0,0,0)):
 value=I.hvalue(r,c,x);assert isinstance(value,F);drift=I.evaluate(I.scaled_drift(r,c,x));assert isinstance(drift,F);hit('actual_zero_cutoff_pointwise_generator')
# Direct symbolic profile evaluation budget boundary agrees with author resource interface.
for j in (c['mass_head']['K']-5,c['mass_head']['K'],c['mass_head']['K']+1):assert I.evaluate(I.mass_g(c,j))==A.mass_g(c['plan'],c['mass_head'],j);hit('profile_receiver_values')
# Full JSON wire receiving and semantic mutations.
wire=json.loads(I.canonical(c));assert I.receive(raws[0],2,wire);hit('json_wire_receiving')
for key in ('K','Q','Jcoef','L0','delta_base','nu'):
 bad=deepcopy(wire);v=bad['mass_head'][key];bad['mass_head'][key]=str(F(v)+1)if isinstance(v,str)else v+1
 assert not I.receive(raws[0],2,bad);hit('receipt_mutations_rejected')
for key in ('core_backward_steps','expanded_outer_head'):
 bad=deepcopy(wire);bad['work'][key]+=1;assert not I.receive(raws[0],2,bad);hit('receipt_mutations_rejected')
# Normalization, coordinate permutation, honest budgets and non-membership.
for perm in ((4,3,2,1,0),(1,4,0,2,3),(0,2,1,3,4)):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raws[0]]
 assert I.canonical(I.construct(rr,2))==I.canonical(A.construct(rr,2));hit('coordinate_permutations')
steps=c['plan']['core_profile_steps']
for cap in (0,steps-1,steps):assert I.canonical(I.construct(raws[0],2,cap))==I.canonical(A.construct(raws[0],2,cap));hit('core_budget_boundaries')
# Constructor is independent even when every author production entry is disabled.
def forbidden(*a,**k):raise RuntimeError('author dependency called')
saved={k:getattr(A,k)for k in ('recognize','tail_plan','geometric_head','construct','qualitative')}
for k in saved:setattr(A,k,forbidden)
assert I.canonical(I.construct(raws[0],2))==I.canonical(c);hit('author_dependency_disabled')
for k,v in saved.items():setattr(A,k,v)
res=dict(status='PASS_INDEPENDENT_EXACT_COMPONENT_AND_NESTED_RECEIVING',counts=counts,fixtures=reports,main_canonical_bytes=len(I.canonical(c).encode()),main_canonical_sha256=I.digest(c),scope='Actual-K local tail/core checks and executable nested receiving; synthetic small heads/cutoff widths are explicitly NOT full certificates. No actual enormous global-tail state or stationary constant expanded.')
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(counts,sort_keys=True),flush=True)
