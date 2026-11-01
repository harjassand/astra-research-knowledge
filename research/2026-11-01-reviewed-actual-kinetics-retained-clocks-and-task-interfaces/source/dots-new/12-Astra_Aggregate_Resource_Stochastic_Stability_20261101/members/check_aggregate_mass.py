"""Actual tail and core-low-cone checks plus separately labeled small-head lemmas.
No huge head/cutoff expansion and no full global-tail receiving is claimed.
"""
from fractions import Fraction as F
from itertools import product
import json,copy
import aggregate_mass as A
G=A.G
count=dict(synthetic_head_states=0,channel_jumps=0,forward_phase_signs=0,reverse_phase_bounds=0,free_resource_neutrality=0,head_birth_bounds=0,tail_birth_bounds=0,reverse_sum_bounds=0,death_join_bounds=0,actual_core_low_cone=0,actual_mass_tail_states=0,actual_high_inventory_negative=0,actual_combined_cone_negative=0,actual_outer_head_values=0,budget_refusals=0)
def coords(r,x):
 a=x[r['a']];f=sum(x[v]for v in r['free']);u=sum(x)-f;j=u+a;R=a+G.C.cover_weight(r['inventory'],x)
 return sum(x),a,f,u,j,R

def zval(r,p,h,x,budget=100000):
 N,a,f,u,j,R=coords(r,x);g=A.mass_g(p,h,j,budget);assert isinstance(g,F),(j,g)
 return g-1+p['mass']['rho']*F(a,(j+1)**2)

def gen(r,t,x,fn,channels=None):
 old=fn(x);out=F(0)
 for u,v,k in r['channels']if channels is None else channels:
  rate=k*G.C.B.falling(x,u)
  if rate:
   y=tuple(a-b+c for a,b,c in zip(x,u,v));out+=rate*(t**(sum(v)-sum(u))*fn(y)-old)
 return out

def hcore(r,p,x):
 N,a,f,u,j,R=coords(r,x);c=p['core'];return G.gv(p['core_profile'],R)+c['rho0']*F(a,(R+1)**2)-c['e']*F(a,N+1)

cases=[]
for s in (1,2):
 raw=A.fixture(s);r=A.recognize(raw);plan=A.tail_plan(r,F(2));head=A.geometric_head(plan,r);assert head['status']=='PENDING_FACTORED_MASS_GLUE'
 assert G.qualitative(raw)['status']=='UNKNOWN' # All target triangle, not the accepted one-hub parser.
 for K in (8,17):
  p=copy.deepcopy(plan);p['mass']['K']=K;h=A.geometric_head(p,r);rho=p['mass']['rho'];c=p['mass']['c'];t=p['t']
  Bhead=h['Q']**K;D2=9*h['C']*Bhead;Cdeath=9*r['mu']*h['C']*Bhead/t+4*rho*r['mu']
  rev=[row for row in r['internal']if row[0][r['a']]==0]
  for x in product(range(3),repeat=r['n']):
   N,a,f,u,j,R=coords(r,x);gv=lambda j:A.mass_g(p,h,j);f0=F(a,(j+1)**2)
   for src,dst,k in r['internal']:
    rate=k*G.C.B.falling(x,src)
    if not rate:continue
    y=tuple(xx-uu+vv for xx,uu,vv in zip(x,src,dst));_,ap,fp,up,jp,Rp=coords(r,y);f1=F(ap,(jp+1)**2)
    if src[r['a']]:assert f1<=f0;count['forward_phase_signs']+=1
    else:assert f1-f0<=F(2,(j+1)**2);count['reverse_phase_bounds']+=1
    if any(src[v]or dst[v]for v in r['free']):assert jp==j;count['free_resource_neutrality']+=1
    count['channel_jumps']+=1
   Q=sum(x[v]*x[w]for v,w in r['edges'])
   rv=gen(r,t,x,lambda x:zval(r,p,h,x),rev)
   assert rv<=-r['bmin']*c*Q/(2*(j+1)**2);count['reverse_sum_bounds']+=1
   birth=[row for row in r['channels']if sum(row[1])-sum(row[0])==1]
   bd=gen(r,t,x,lambda x:zval(r,p,h,x),birth)
   if j<K:assert bd<=-r['lam']/2;count['head_birth_bounds']+=1
   else:assert bd<=p['mass']['B']/F(j+1);count['tail_birth_bounds']+=1
   death=[row for row in r['channels']if sum(row[1])-sum(row[0])==-1]
   dd=gen(r,t,x,lambda x:zval(r,p,h,x),death)
   assert dd<=Cdeath*a/F((j+1)**2);count['death_join_bounds']+=1
   assert 0<=zval(r,p,h,x)<=(h['C']*Bhead+2*c+rho/2)/F(j+1)
   count['synthetic_head_states']+=1
 # Real acquired K and actual count states: profile values near the OUTER head
 # require only a small power, despite the enormous total head length.
 K=plan['mass']['K'];rho=plan['mass']['rho'];c=plan['mass']['c']
 for off in range(-12,5):
  j=K+off;g=A.mass_g(plan,head,j);assert isinstance(g,F)
  if j<K:assert g>=2*plan['t']*(A.mass_g(plan,head,j+2)+rho)
  assert g-A.mass_g(plan,head,j+1)>=c/F((j+1)**2)
  count['actual_outer_head_values']+=1
 assert A.mass_g(plan,head,0,100000)['status']=='UNKNOWN_POWER_VALUE_BUDGET';count['budget_refusals']+=1
 # The core LOW branch is tested with F/U unbounded independently of a gamma.
 for power in (1,3,20):
  U=max(10,plan['core']['U0'],10*K)**power
  for aa in (0,1,2,plan['core_profile']['K']):
   for bulk in r['rare']:
    x=[0]*r['n'];x[r['a']]=aa;x[bulk]=U-aa
    for fi in r['free']:x[fi]=U**3+17
    xx=tuple(x);N,a,f,u,j,R=coords(r,xx)
    assert u>=plan['core']['U0']and R<=plan['core']['delta']*u
    value=gen(r,plan['t'],xx,lambda x:hcore(r,plan,x))
    assert value<=-plan['core']['zeta0']*hcore(r,plan,xx),(s,aa,power,'corelow')
    count['actual_core_low_cone']+=1
 # Local rational-tail cone, explicitly distinct from the much narrower global
 # cone based on the unexpanded head. All neighboring J are >=K.
 ct=(r['a_sum']+r['krplus'])*8*c+4*rho*r['mu']+1
 dt=min(F(1,4),rho*r['kfree']/(4*ct))
 for U in (4*K,K*K):
  for aa in (0,1,2,U//3):
   for pattern in ('pure','balanced','pair'):
    x=[0]*r['n'];x[r['a']]=aa;left=U-aa
    if pattern=='pure':x[r['rare'][0]]=left
    elif pattern=='pair':x[r['rare'][0]]=left//2;x[r['rare'][1]]=left-left//2
    else:
     for v in r['rare']:x[v]=left//len(r['rare'])
     x[r['rare'][0]]+=left-sum(x[v]for v in r['rare'])
    for fi in r['free']:x[fi]=G.ceilq(4*F(U+1)/dt)
    xx=tuple(x);N,a,f,u,j,R=coords(r,xx);lz=gen(r,plan['t'],xx,lambda x:zval(r,plan,head,x));l0=gen(r,plan['t'],xx,lambda x:hcore(r,plan,x));Q=sum(x[v]*x[w]for v,w in r['edges'])
    bound=plan['mass']['B']/F(j+1)-r['bmin']*c*Q/(2*(j+1)**2)-rho*r['kfree']*a*f/(2*(j+1)**2)
    assert lz<=bound
    if R>plan['core']['delta']*u:assert lz<=-plan['mass']['cfree'];count['actual_high_inventory_negative']+=1
    assert l0+plan['mass']['eta']*lz<=-head['nu'];count['actual_combined_cone_negative']+=1
    count['actual_mass_tail_states']+=1
 cases.append(dict(free_species=s,raw_sha256=r['raw_sha256'],core_steps=plan['core_profile_steps'],actual_K=K,head=head,scope='Actual huge K retained; local tail and outer head values executed, global cutoff/inner head powers unexpanded'))
print(json.dumps(G.encode(dict(status='PASS_AUTHOR_COMPONENT_CHECKS',counts=count,cases=cases,synthetic_head_warning='K=8,17 heads validate channel lemmas only, not a complete Foster certificate',no_global_tail_test=True,no_huge_head_expansion=True,no_new_source_retrieval=True)),indent=2))
