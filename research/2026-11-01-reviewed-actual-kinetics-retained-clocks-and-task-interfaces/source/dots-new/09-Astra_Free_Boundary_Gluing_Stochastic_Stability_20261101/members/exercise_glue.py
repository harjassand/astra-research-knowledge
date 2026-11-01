from fractions import Fraction as F
from itertools import product
import copy,json,random
import free_port_glue as G
COUNT=dict(states=0,jumps=0,free_cone_checks=0,core_partial_tail_checks=0,full_negative_checks=0,cross_checks=0,synthetic_cutoff_checks=0,head_reader_checks=0)
CASES=[]
def partial_head(rec,cc,gamma):
 co=cc['constants'];p=cc['core_profile'];du=co['delta_unit']*gamma
 cint=2*co['L']+2*rec['mu']+(2*p['c']+11*co['rho0'])*rec['S']/du**2+co['rho0']*(11*rec['lam']*cc['t']+co['CA'])
 kap=min(co['D']*du/4,co['e']*rec['b0']*du**2/(32*len(rec['edges'])))
 return G.ceilq(max(F(1),F(p['K'])/du,4*co['CA']/(rec['krminus']*gamma),4*co['Qhead']/(co['rho0']*rec['krminus']*gamma),(cint+1)/kap))
def check_state(rec,cc,x,gamma=None):
 co=cc['constants'];N,A,f,U,R,P=G.coordinates(rec,cc,x);h0,Z,phi=G.pieces(rec,cc,x);L0,LZ,cross,whole=G.scaled_pieces(rec,cc,x)
 assert P<=R<=U and 0<=phi<=1 and F(3,4)<=h0<=co['H0'] and 0<=Z<=co['CZ']/F(P+1)
 assert L0<=co['C0'],('global ceiling',x,L0,co['C0'])
 assert cross<=co['Ccross']/co['Jcut'],('cross',x,cross,co['Ccross']/co['Jcut'])
 assert G.hvalue(rec,cc,x)==h0+co['eta']*phi*Z
 if phi:assert U+1<=co['deltaF']*f
 if U+1<=co['deltaF']*f:
  assert LZ<=-co['cfree'],('free cone',x,LZ,-co['cfree']);COUNT['free_cone_checks']+=1
 if gamma is not None:
  assert U>=gamma*N and N>=partial_head(rec,cc,gamma)
  assert L0<=-co['zeta0']*h0,('partial',gamma,x,L0,-co['zeta0']*h0)
  assert whole<=-co['zeta0']/2,('whole on tested partial region',gamma,x,whole)
  COUNT['core_partial_tail_checks']+=1;COUNT['full_negative_checks']+=1
 for u,v,k in rec['internal']:
  rate=k*G.C.B.falling(x,u)
  if not rate:continue
  y=tuple(a-b+c for a,b,c in zip(x,u,v));Np,Ap,fp,Up,Rp,Pp=G.coordinates(rec,cc,y)
  assert Np==N and abs(Rp-R)<=1 and abs(Pp-P)<=2
  fP=F(A,(P+1)**2);fPP=F(Ap,(Pp+1)**2)
  if u[rec['a']]==0:
   assert Pp>=P
   if v[rec['a']]==2:assert Pp>=P+1
   assert fPP-fP<=F(2,(P+1)**2)
  else:
   assert Pp<=P
   assert abs(fPP-fP)<=F(20,(P+1)**2)
  if u[rec['f']]or v[rec['f']]:assert Pp==P
  COUNT['jumps']+=1
 COUNT['states']+=1;COUNT['cross_checks']+=1

def run(raw,t,name):
 rec=G.recognize(raw);cc=G.construct(raw,t);assert cc['status']=='CERTIFIED_SYMBOLIC_FOSTER';co=cc['constants'];n=rec['n'];a=rec['a'];f=rec['f'];rare=rec['rare'];b,c=rec['h0']
 for xx in product(range(3),repeat=n):check_state(rec,cc,xx)
 # Actual free-cone checks, with all extinction and two-step protected-mass layers.
 for A in (0,1,2,3,cc['free_profile']['K'],10**10):
  for rarevec in ([0]*len(rare),[1]*len(rare),[2,0]+[3]*(len(rare)-2),[0,2]+[1]*(len(rare)-2),[10**12]+[1]*(len(rare)-1)):
   x=[0]*n;x[a]=A
   for v,z in zip(rare,rarevec):x[v]=z
   U=sum(x);x[f]=G.ceilq(F(4*(U+1))/co['deltaF']);check_state(rec,cc,tuple(x))
 # The same core h0 is tested at three acquired gamma thresholds, not at the unexpanded global head.
 for gamma in (F(1,2),F(1,64),F(1,1<<40)):
  cutoff=partial_head(rec,cc,gamma);U=2*G.ceilq(gamma*cutoff)+100
  fcount=int(F(U)*(1-gamma)/gamma)
  for A in (0,1,2,cc['core_profile']['K'],U//3):
   for bulk in rare:
    x=[0]*n;x[a]=A;x[f]=fcount;left=U-A
    for v in rare:
     if v!=bulk:x[v]=min(left,1);left-=x[v]
    x[bulk]=left;check_state(rec,cc,tuple(x),gamma)
   x=[0]*n;x[a]=A;x[f]=fcount;left=U-A
   for v in rare:x[v]=left//len(rare)
   x[rare[0]]+=left-sum(x[v]for v in rare);check_state(rec,cc,tuple(x),gamma)
 # Generic cutoff error bound at short synthetic widths, including phi=0 and1 joins.
 # These are NOT claimed complete Foster certificates (their J need not meet the gluing condition).
 for J in (1,2,7):
  synth=copy.deepcopy(cc);synth['constants']['Jcut']=J
  for U in (0,1,2,4,11,100):
   for A in range(min(2,U)+1):
    for k in (co['L0']-1,co['L0'],co['L0']+J,co['L0']+J+1):
     x=[0]*n;x[a]=A
     left=U-A;x[b]=left//2;x[c]=left-left//2
     for off in (-1,0,1):
      x[f]=max(0,((U+1)<<k)+off-1)
      h0,Z,phi=G.pieces(rec,synth,tuple(x));_,LZ,cross,_=G.scaled_pieces(rec,synth,tuple(x))
      assert cross<=co['Ccross']/J
      if phi:assert U+1<=co['deltaF']*x[f] and LZ<=-co['cfree']
      COUNT['synthetic_cutoff_checks']+=1
 assert not G.outside_head(cc,10**1000)
 refusal=G.expand_head(cc,100000);assert refusal['status']=='UNKNOWN_POWER_EXPANSION_BUDGET'
 CASES.append(dict(name=name,n=n,t=t,roles=cc['qualitative']['roles'],work=cc['work'],L0=co['L0'],Jcut=co['Jcut'],head_power_bits=cc['symbolic_head']['exponent']+1,head_expansion=refusal,certificate_sha256=G.digest(cc)))
 return rec,cc
rec,cert=run(G.fixture(),F(2),'triangle_plus_unique_arm_free_F')
base=G.C.B.fixture();raw=[(tuple(u)+(0,),tuple(v)+(0,),k)for u,v,k in base]
n=6;z=lambda *ix:tuple(ix.count(i)for i in range(n));raw.extend([(z(0,5),z(1,2),F(1)),(z(1,2),z(0,5),F(1))])
run(raw,F(3,2),'nonCB_P4_plus_unique_arm_free_F')
# Exact symbolic-head threshold algorithm, tested separately from any stability claim.
for exponent in range(13):
 for aa,bb,dd in [(F(1),F(1,3),F(1,7)),(F(7,2),F(2),F(9,5))]:
  artificial={'symbolic_head':dict(exponent=exponent,coefficients=(aa,bb,dd))}
  U=2*((1<<exponent)+1);exact=G.ceilq(aa*U+bb*U**2+dd*U**4+1)
  assert G.expand_head(artificial,exponent+1)==exact
  for N in (0,1,(1<<exponent),exact-1,exact,exact+1,2*exact):
   assert G.outside_head(artificial,N)==(N>=exact);COUNT['head_reader_checks']+=1
# Structural frontier and paid refusals remain exact.
raw=G.fixture();assert G.C.B.qualitative(raw)['status']=='UNKNOWN'
extra=raw+[((1,0,0,0,1),(0,1,0,1,0),F(1)),((0,1,0,1,0),(1,0,0,0,1),F(1))]
assert G.qualitative(extra)['status']=='UNKNOWN'
assert G.construct(raw,F(2),max_profile_steps=0)['status']=='UNKNOWN_PROFILE_BUDGET'
print(json.dumps(G.encode(dict(status='PASS_AUTHOR_COMPONENT_CHECKS',scope='Candidate only; actual global symbolic-head expansion and phi=1 global-tail states not executed',counts=COUNT,cases=CASES,no_simulation=True,no_expanded_global_head=True,no_Foster_power_expansion=True)),indent=2))
