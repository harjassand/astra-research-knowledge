"""NEW post-replacement exact tests; not the lost historical test bytes."""
from fractions import Fraction as F
from itertools import product,combinations
from copy import deepcopy
import json
import arm_backbone as B
A,G=B.A,B.G
counts={}
def hit(k):counts[k]=counts.get(k,0)+1

def fixture(edges,nrare,nfree,aux):
 n=1+nrare+nfree;z=lambda *ix:tuple(ix.count(i)for i in range(n));hs=[z(*e)for e in edges];raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for e in edges+aux:h=z(*e);raw.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
 for x in range(1,n):h=hs[(x-1)%len(hs)];raw.extend([(z(0,x),h,F(1)),(h,z(0,x),F(1))])
 return raw

def coords(r,x):
 a=x[r['a']];f=sum(x[v]for v in r['free']);u=sum(x)-f;j=u+a
 # Independent test-only cover enumeration; production uses acquired circuit.
 vs=r['rare'];vals=[]
 for mask in range(1<<len(vs)):
  co={v for i,v in enumerate(vs)if mask>>i&1}
  if all(v in co or w in co for v,w in r['edges']):vals.append(sum(x[v]for v in co))
 tau=min(vals);assert tau==G.C.cover_weight(r['inventory'],x)
 return sum(x),a,f,u,j,a+tau

def enabled(r,x):
 for src,dst,k in r['channels']:
  rate=k
  for xx,ss in zip(x,src):
   for v in range(ss):rate*=xx-v
  if rate:yield src,dst,rate,tuple(xx-ss+dd for xx,ss,dd in zip(x,src,dst))

def generator(r,t,x,fn,which=lambda u,v:True):
 val=fn(x);return sum((rate*(t**(sum(v)-sum(u))*fn(y)-val)for u,v,rate,y in enabled(r,x)if which(u,v)),F(0))

def core(r,c,x):
 N,a,f,u,j,R=coords(r,x);co=c['plan']['core'];return G.gv(c['plan']['core_profile'],R)+co['rho0']*F(a,(R+1)**2)-co['e']*F(a,N+1)

def mass(r,p,h,x):
 N,a,f,u,j,R=coords(r,x);return A.mass_g(p,h,j)-1+p['mass']['rho']*F(a,(j+1)**2)

raws=[B.fixture(),fixture([(1,2),(2,3),(3,4)],4,2,[(1,3),(1,5),(5,6)]),fixture([(1,2),(2,3),(3,4)],4,0,[(1,3)])]
rows=[]
for raw in raws:
 r=B.recognize(raw);c=B.construct(raw,2);p=c['plan'];co=p['core'];aux={h['complex']:h for h in r['auxiliary']}
 for x in product(range(3),repeat=r['n']):
  N,a,f,u,j,R=coords(r,x);assert generator(r,F(2),x,lambda y:core(r,c,y))<=co['C0'];hit('new_global_core_states')
  for src,dst,rate,y in enabled(r,x):
   if src not in aux and dst not in aux:continue
   NN,aa,ff,uu,jj,RR=coords(r,y)
   phaseR=F(aa,(RR+1)**2)-F(a,(R+1)**2);phaseJ=F(aa,(jj+1)**2)-F(a,(j+1)**2)
   if dst in aux:
    v=sum(dst[z]for z in r['free']);assert aa==a-2 and ff==f+v and uu==u-v and jj==j-2-v and -2<=RR-R<=0
    assert abs(phaseR)<=F(20,(R+1)**2)and abs(phaseJ)<=F(40,(j+1)**2);hit('new_forward_detour_jumps')
   else:
    v=sum(src[z]for z in r['free']);assert 0<=RR-R<=2 and jj==j+2+v
    assert phaseR<=F(2,(R+1)**2)and phaseJ<=F(2,(j+1)**2);hit('new_reverse_detour_jumps')
    if RR==R:
     prodcount=1
     for k in aux[src]['edge']:prodcount*=x[k]
     assert prodcount<=R*R;hit('new_neutral_reverse_controls')
 if r['free']:
  K=c['mass_head']['K'];U=max(4*K,2*co['U0'])
  for bulk in r['rare']:
   for aa in (0,1):
    x=[0]*r['n'];x[r['a']]=aa;x[bulk]=U-aa;x[r['free'][0]]=U**3;x=tuple(x)
    assert coords(r,x)[-1]<=co['delta']*U
    assert generator(r,F(2),x,lambda y:core(r,c,y))<=-co['zeta0']*core(r,c,x);hit('new_actual_low_core_states')
  NN=B.core_head(r,p,F(1,2))+10
  for aa in (0,1,NN//3):
   x=[0]*r['n'];x[r['a']]=aa
   for j0,v in enumerate(r['rare']):x[v]=(NN-aa)//len(r['rare'])+(j0<(NN-aa)%len(r['rare']))
   x[r['free'][0]]=NN;x=tuple(x)
   assert generator(r,F(2),x,lambda y:core(r,c,y))<=-co['zeta0']*core(r,c,x);hit('new_actual_partial_core_states')
  # Synthetic K=8 checks algebra only, never claims full global Foster.
  pp=deepcopy(p);pp['mass']['K']=8;hh=B.geometric_head(pp,r);rho=pp['mass']['rho'];Cb=hh['C']*hh['Q']**8
  cf=(r['a_sum']+r['krplus'])*9*Cb+r['aD']*(25*Cb+40*rho)
  for x in product(range(3),repeat=r['n']):
   N,a,f,u,j,R=coords(r,x);Q=sum(x[v]*x[w]for v,w in r['edges'])
   val=generator(r,F(2),x,lambda y:mass(r,pp,hh,y),lambda src,dst:sum(src)==sum(dst))
   upper=cf*F(a*u,(j+1)**2)-r['bmin']*Q/F(2*(j+1)**2)-rho*r['kfree']*F(a*f,(j+1)**2)
   assert val<=upper;hit('new_synthetic_mass_internal_bounds')
  for j in range(25):
   assert (j+1)**2*(A.mass_g(pp,hh,max(0,j-4))-A.mass_g(pp,hh,j))<=25*Cb;hit('new_four_step_profile_checks')
  # Actual huge-K LOCAL rational tail, not the nested global free cone.
  rho=p['mass']['rho'];local=min(F(1,4),rho*r['kfree']/(4*((r['a_sum']+r['krplus'])*8+r['aD']*(32+40*rho)+4*rho*r['mu']+1)))
  for aa in (0,1,2,U//3):
   for distributed in (False,True):
    x=[0]*r['n'];x[r['a']]=aa
    if distributed:
     for j0,v in enumerate(r['rare']):x[v]=(U-aa)//len(r['rare'])+(j0<(U-aa)%len(r['rare']))
    else:x[r['rare'][0]]=U-aa
    x[r['free'][0]]=G.ceilq(4*F(U+1)/local);x=tuple(x)
    assert coords(r,x)[4]>=K+4
    val=generator(r,F(2),x,lambda y:core(r,c,y)+p['mass']['eta']*mass(r,p,c['mass_head'],y))
    assert val<=-c['mass_head']['nu'];hit('new_actual_K_local_joins')
 else:
  NN=c['head']+10
  for aa in(0,1,NN//3):
   x=[0]*r['n'];x[r['a']]=aa
   for j0,v in enumerate(r['rare']):x[v]=(NN-aa)//len(r['rare'])+(j0<(NN-aa)%len(r['rare']))
   x=tuple(x);assert generator(r,F(2),x,lambda y:core(r,c,y))<=-co['zeta0']*core(r,c,x);hit('new_core_only_tail_states')
 rows.append(dict(raw_sha256=r['raw_sha256'],free=r['free'],core_steps=p['core_profile_steps']))
# Direct dyadic positive-cross bounds for every possible free-endpoint count.
for U in range(2,17):
 for aa in range(2,U+1):
  for ff in range(0,300,3):
   for v in(0,1,2):
    for width in(1,3,8):
     phi=lambda f,u:max(F(0),min(F(1),(G.dyadic(f+1)-G.dyadic(u+1)-4)/width))
     jump=phi(ff+v,U-v)-phi(ff,U)
     assert jump>=0
     if jump:
      assert ff+1>=U and jump<=F(16,width*U)
      assert U+aa-1-v>=F(U,2);hit('new_positive_cutoff_increments')
     assert phi(ff,U)-phi(ff+v,U-v)<=0;hit('new_cutoff_checks')
print(json.dumps(dict(status='PASS_NEW_RECOVERY_COMPONENT_PREFLIGHT',counts=counts,cases=rows,scope='New post-replacement tests. Exact finite checks support code/algebra, not all-state proof. Synthetic and actual-local cones remain distinct from unexpanded global head.'),indent=2))
