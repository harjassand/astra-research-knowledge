from fractions import Fraction as F
from itertools import product
from copy import deepcopy
from pathlib import Path
import sys,os,json
import independent_backbone as I
from fixtures import raw_graph,state
sys.path.insert(0,os.environ.get('BACKBONE_SOURCE_DIR','producer-workspace/stochastic_arm_backbone_recovery_20261101'));import arm_backbone as A
counts={};hit=lambda k,n=1:counts.__setitem__(k,counts.get(k,0)+n)
raws=[A.fixture(),raw_graph(6,[(1,2),(2,3),(3,4)],[(1,3),(1,5),(5,6)],True,True),raw_graph(4,[(1,2),(2,3),(3,4)],[(1,3)],False,True)];reports=[]
for index,raw in enumerate(raws):
 r=I.parse(raw);c=I.construct(raw,2,300000);assert I.canonical(c)==I.canonical(A.construct(raw,2,300000));p=c['plan'];co=p['core'];hit('complete_receipts')
 assert I.canonical(I.dag(raw,c))==I.canonical(A.certificate_expressions(raw,c));hit('complete_DAGs')
 vs=r['rare'];covers=[{v for i,v in enumerate(vs)if mask>>i&1}for mask in range(1<<len(vs))if all((mask>>vs.index(u)&1)or(mask>>vs.index(v)&1)for u,v in r['edges'])]
 for x in product(range(3),repeat=r['n']):
  N,a,f,u,j,R=I.coords(r,x);tau=min(sum(x[v]for v in cc)for cc in covers);assert R==a+tau
  assert F(3,4)<=I.core(r,c,x)<=co['H0'];assert I.drift(r,c,x,lambda y:I.core(r,c,y))<=co['C0'];hit('global_core_ceiling_states')
  for h in r['auxiliary']:
   v,w=h['edge'];b=int(v in r['free'])+int(w in r['free'])
   if a>=2:
    y=list(x);y[r['a']]-=2;y[v]+=1;y[w]+=1;_,ap,fp,up,jp,Rp=I.coords(r,y)
    assert -2<=Rp-R<=0 and jp==j-2-b and fp==f+b and up==u-b
    assert abs(F(ap,(Rp+1)**2)-F(a,(R+1)**2))<=F(20,(R+1)**2)
    assert abs(F(ap,(jp+1)**2)-F(a,(j+1)**2))<=F(40,(j+1)**2);hit('forward_detour_jumps')
   if x[v]and x[w]:
    y=list(x);y[r['a']]+=2;y[v]-=1;y[w]-=1;_,ap,fp,up,jp,Rp=I.coords(r,y)
    assert 0<=Rp-R<=2 and jp==j+2+b
    assert F(ap,(Rp+1)**2)-F(a,(R+1)**2)<=F(2,(R+1)**2)and F(ap,(jp+1)**2)-F(a,(j+1)**2)<=F(2,(j+1)**2)
    if Rp==R:assert b==0 and x[v]*x[w]<=R**2 and any({v,w}<=cc and sum(x[z]for z in cc)==tau for cc in covers);hit('neutral_reverse_witnesses')
    if R==0:assert Rp==2 and I.core(r,c,y)<I.core(r,c,x);hit('latent_R0_reverse_states')
    hit('reverse_detour_jumps')
 for gamma in ((F(1),F(1,8),F(1,2**25))if r['free']else(F(1),)):
  nstar=I.core_head(r,p,gamma);U=2*I.ceil(gamma*nstar)+100
  for a in (0,1,2,p['core_profile']['K'],U//3):
   for balanced in (False,True):
    x=state(r,U,a,balanced,int(U*(1-gamma)/gamma));N,_,_,u,_,_=I.coords(r,x);assert u>=gamma*N and N>=nstar
    assert I.drift(r,c,x,lambda y:I.core(r,c,y))<=-co['zeta0']*I.core(r,c,x);hit('partial_core_tail_states')
 if not r['free']:
  for N in (0,c['head']-1,c['head'],c['head']+1):assert I.outside(c,N)==A.outside_head(c,N)==(N>=c['head']);hit('core_only_head_comparisons')
  reports.append(dict(status=c['status'],receipt=I.digest(c),steps=p['core_profile_steps']));continue
 m=p['mass'];K=m['K'];rho=m['rho'];hd=c['mass_head']
 for j in range(K-8,K+6):
  g=I.I.evaluate(I.I.mass_g(c,j));gp=I.I.evaluate(I.I.mass_g(c,j+1));assert g-gp>=F(1,(j+1)**2)
  if j<K:assert g>=2*c['t']*(I.I.evaluate(I.I.mass_g(c,j+2))+rho)
  hit('actual_head_join_values')
 for U in (max(co['U0'],4*K),K*K):
  for a in (0,1,2,p['core_profile']['K']):
   x=state(r,U,a,False,U**3);assert I.coords(r,x)[-1]<=co['delta']*U
   assert I.drift(r,c,x,lambda y:I.core(r,c,y))<=-co['zeta0']*I.core(r,c,x);hit('actual_low_core_states')
 dt=min(F(1,4),rho*r['kfree']/(4*((r['a_sum']+r['krplus'])*8+r['aD']*(32+40*rho)+4*rho*r['mu']+1)))
 for U in (4*K,K*K):
  for a in (0,1,2,U//3):
   for b in (False,True):
    for fb in (False,True):
     x=state(r,U,a,b,I.ceil(4*F(U+1)/dt),fb)
     assert I.drift(r,c,x,lambda y:I.core(r,c,y)+m['eta']*I.mass(r,c,y))<=-hd['nu'];hit('actual_K_local_joins')
 for KS in (8,17):
  s=deepcopy(c);s['plan']['mass']['K']=KS;s['mass_head']=I.head(s['plan'],r);h=s['mass_head'];bh=h['Q']**KS;CZ=h['C']*bh+2+rho/2;d2=9*h['C']*bh;d4=25*h['C']*bh;CF=(r['a_sum']+r['krplus'])*d2+r['aD']*(d4+40*rho);CD=9*r['mu']*h['C']*bh/s['t']+4*rho*r['mu']
  for j in range(KS+35):assert (j+1)**2*(I.I.evaluate(I.I.mass_g(s,max(0,j-4)))-I.I.evaluate(I.I.mass_g(s,j)))<=d4;hit('synthetic_four_step_points')
  for x in product(range(3),repeat=r['n']):
   N,a,f,u,j,R=I.coords(r,x);QB=sum(x[v]*x[w]for v,w in r['edges']);birth=-r['lam']/2 if j<KS else m['B']/F(j+1)
   bound=birth-r['bmin']*QB/F(2*(j+1)**2)-rho*r['kfree']*a*f/F((j+1)**2)+(CF*a*u+CD*a)/F((j+1)**2)
   assert I.drift(r,s,x,lambda y:I.mass(r,s,y))<=bound;hit('synthetic_complete_mass_generator_states')
  for width in (1,3):
   def phi(x):
    _,_,f,u,_,_=I.coords(r,x);return max(F(0),min(F(1),(I.P.dyadic(f+1)-I.P.dyadic(u+1)-4)/width))
   for U in (0,1,2,3,8,17):
    for a in sorted({0,min(1,U),min(2,U),U}):
     for bal in (False,True):
      for shift in (3,4,4+width,5+width):
       for off in (-1,0,1):
        x=state(r,U,a,bal,max(0,((U+1)<<shift)+off-1));ph=phi(x);cross=F(0)
        for src,dst,rate,y in I.P.enabled(r,x):
         dp=phi(y)-ph;z=I.mass(r,s,y);cross+=rate*s['t']**(sum(dst)-sum(src))*z*dp
         if dp<=0:continue
         hit('positive_cutoff_jumps');hit('zero_crossings',int(ph==0));hit('one_crossings',int(ph<1 and phi(y)==1))
         if sum(dst)==sum(src)-1:assert I.coords(r,y)[4]+1>=U and z<=CZ/F(U);hit('last_copy_deaths',int(a==1))
         elif src[r['a']]==2 and dst in {h['complex']for h in r['auxiliary']}:
          assert dp<=F(16,width*U)and z<=2*CZ/F(U);hit('positive_forward_detour_cutoff')
        assert cross<=4*CZ*(r['ell']*len(r['edges'])+r['mu']+8*r['aD'])/width
        direct=I.drift(r,s,x,lambda y:I.core(r,s,y)+m['eta']*phi(y)*I.mass(r,s,y));split=I.drift(r,s,x,lambda y:I.core(r,s,y))+m['eta']*(ph*I.drift(r,s,x,lambda y:I.mass(r,s,y))+cross)
        assert direct==split;hit('synthetic_cutoff_product_states')
 reports.append(dict(status=c['status'],receipt=I.digest(c),steps=p['core_profile_steps'],K=K));print('PASS fixture',index,flush=True)
res=dict(status='PASS_FRESH_INDEPENDENT_COMPONENTS',counts=counts,cases=reports,scope='New independent tests, not lost historical bytes. Actual-K local cones and synthetic heads/widths are explicitly not the unexpanded global region.')
Path(__file__).with_name('COMPONENT_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(counts),flush=True)
