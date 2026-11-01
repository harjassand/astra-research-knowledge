from pathlib import Path
from fractions import Fraction as F
from math import comb
from copy import deepcopy
import importlib.util,sys,json,random,time
H=Path(__file__).resolve().parent;S=H/'replay/matched_energy_clock_constructor_20261101';sys.path.insert(0,str(S));import positive_integrals as p;import acquire_derivative as ac
checks=0;cats={};refusals=[];rng=random.Random(11010201);start=time.perf_counter()
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 try:fn()
 except p.Unknown as e:refusals.append({'test':k,'reason':str(e)});ok(True,k)
 else:raise AssertionError('admitted '+k)

# Independent signed alternating Taylor arithmetic, never candidate expminus.
# The interval terms are integer-directed; odd sum255 below exp(-r), even256
# above, 0<=r<=1/2. Rounding at every signed sum and square remains outward.
RP=1536;RS=1<<RP;exp_calls=0

def ex(x):
 global exp_calls
 exp_calls+=1;x=F(x);s=0
 while x>F(1,2):x/=2;s+=1
 tl=th=RS;sl=sh=RS;lower=None
 for j in range(1,257):
  den=x.denominator*j;tl=tl*x.numerator//den;th=(th*x.numerator+den-1)//den
  if j%2:sl-=th;sh-=tl
  else:sl+=tl;sh+=th
  if j==255:lower=max(0,sl)
 upper=min(RS,sh)
 for _ in range(s):lower=lower*lower//RS;upper=(upper*upper+RS-1)//RS
 return F(lower,RS),F(upper,RS)

def gamma(n,x):
 lo,hi=ex(x);term=total=F(1)
 for k in range(1,n):term*=x/k;total+=term
 return max(F(0),lo*total),min(F(1),hi*total)

# Exact arithmetic on independently selected interval endpoints.
for rep in range(500):
 P=rng.choice([32,64,128]);fx=p.Intervals(P,1000000,10000,1024,1);a=F(rng.randrange(100),17);b=a+F(rng.randrange(100),19);c=F(rng.randrange(1,100),23);d=c+F(rng.randrange(100),29)
 ai=(fx.rat(a)[0],fx.rat(b)[1]);bi=(fx.rat(c)[0],fx.rat(d)[1]);lo,hi=fx.div(ai,bi)
 ok(F(lo,fx.S)<=a/d<=b/c<=F(hi,fx.S),'directed positive division all endpoints')
 n=rng.randrange(7);lo,hi=fx.power(ai,n);ok(F(lo,fx.S)<=a**n<=b**n<=F(hi,fx.S),'positive interval power all endpoints')
 lo,hi=fx.positive_sub(ai,bi);ok(F(lo,fx.S)<=max(0,a-d)<=max(0,b-c)<=F(hi,fx.S),'positive subtraction clips only downward lower')

# Price initialization, Machin lower sqrt(pi), analytic zero branch and full
# integer-Gamma mass references. Exact lower/upper pi use separate 48-term
# alternating arctan, not the candidate's32-term calculation.
def atan48(n):
 v=sum((F((-1)**j,(2*j+1)*n**(2*j+1))for j in range(48)),F(0));return v,v+F(1,97*n**97)
a0,a1=atan48(5);b0,b1=atan48(239);pi_lo,pi_hi=16*a0-4*b1,16*a1-4*b0
price=p.Price(128,F(1),F(1),F(4322048),F(1),Nt=4,Ny=4,L=F(0),T=F(400),precision_bits=512,max_operations=30000000)
ok(price.sqrt_pi_lower>0 and price.sqrt_pi_lower**2<pi_lo,'Machin sqrt(pi) is a rigorous lower')
ok(price.analytic_J_lower(F(0))==price.fx.S//2,'analytic J exact t0 branch')
ok(price.K**2*(F(128)+F(1,2))**2>=F(4322048,8),'full beta-H-dmin-vstar K root upward')
for n in [4,5,16,128,129,130]:
 for x in [F(0),F(1,100),F(1),F(32),F(128),F(400),F(1000)]:
  s0,s1=price.gamma_survival(n,x);r0,r1=gamma(n,x);ok(F(s0,price.fx.S)<=r0<=r1<=F(s1,price.fx.S),'finite Gamma survival independent exact-exp reference')
  c0,c1=price.gamma_cdf(n,x);ok(F(c0,price.fx.S)<=1-r1<=1-r0<=F(c1,price.fx.S),'Gamma CDF complement reversed endpoints')
for l,r in [(F(0),F(1)),(F(32),F(321,10)),(F(128),F(12801,100)),(F(399),F(400))]:
 ai=price.gamma_survival(128,l);bi=price.gamma_survival(128,r);w=price.fx.positive_sub(ai,bi);a,b=gamma(128,l);c,d=gamma(128,r)
 ok(F(w[0],price.fx.S)<=max(F(0),a-d)<=b-c<=F(w[1],price.fx.S),'Gamma cell mass no floating CDF subtraction')

# Independent exact spatial integrals. For psi(y)=2y²-y⁴, every moment
# int_0^b psi^n is obtained by finite binomial integration. Global alternating
# Taylor bounds for exp(-c psi) give certified J/Aphi intervals, even for
# non-small c psi; no quadrature or asymptotic remainder is assumed.
N=512;moments={};references=[]
for y in [F(0),F(1,8),F(1,4),F(3,8),F(1,2)]:
 arr=[]
 if not y:arr=[F(0)]*(N+2)
 else:
  yp=y;twop=F(1);ratio=-y*y/2
  for n in range(N+2):
   coeff=F(1);val=F(1,2*n+1)
   for j in range(1,n+1):coeff*=F(n-j+1,j)*ratio;val+=coeff/F(2*n+2*j+1)
   q=twop*yp*val;ok(q>=0,'exact positive spatial polynomial moment');arr.append(q);yp*=y*y;twop*=2
 moments[y]=arr

def integrals(t,y,kap=F(1)):
 c=t*kap/(1+kap);arr=moments[y];coef=F(1);J=arr[0];G=kap*arr[1]
 for n in range(1,N+1):
  coef*=-c/n;J+=coef*arr[n];G+=kap*coef*arr[n+1]
  if n==N-1:jl=J;gl=G
 return (max(F(0),jl),J),(max(F(0),gl),G)

for t in [F(0),F(1,100),F(1),F(8),F(32),F(128),F(400)]:
 fi=[]
 for phi in price.phi:
  l,h=ex(t*phi/price.vstar);fi.append((int(l*price.fx.S),-(-h.numerator*price.fx.S//h.denominator)))
 row=price.row(t,fi);Jref,Gref=integrals(t,F(1,2));ok(F(row['Jlo'],price.fx.S)<=Jref[0]<=Jref[1],'row combined J lower independently certified')
 ok(F(price.analytic_J_lower(t),price.fx.S)<=Jref[0],'positive K0=3 Taylor J lower not asymptotic equality')
 refs={}
 for j,y in enumerate([F(0),F(1,8),F(1,4),F(3,8),F(1,2)]):
  A,G=integrals(t,y);B=(max(F(0),Jref[0]-A[1]),max(F(0),Jref[1]-A[0]));BG=(max(F(0),Gref[0]-G[1]),max(F(0),Gref[1]-G[0]));B,BG=((F(0),F(0)),(F(0),F(0))) if y==F(1,2) else (B,BG);refs[j]=(A,G,B,BG)
  ok(F(row['A0hi'][j],price.fx.S)>=A[1],'positive prefix A0 upper trapezoid error')
  ok(F(row['AphiLo'][j],price.fx.S)<=G[0],'positive prefix Aphi lower trapezoid error')
  ok(F(row['B0lo'][j],price.fx.S)<=B[0],'independently summed B0 lower no rounded-prefix cancellation')
  ok(F(row['BphiHi'][j],price.fx.S)>=BG[1],f'independently summed Bphi upper t={t} j={j}')
 for j in range(4):
  one=price.fx.mul((row['A0hi'][j+1],)*2,(row['BphiHi'][j],)*2)[1];two=price.fx.mul((row['AphiLo'][j],)*2,(row['B0lo'][j+1],)*2)[0];D=F(max(0,one-two),price.fx.S)
  for k in [j,j+1]:
   A,G,B,BG=refs[k];actualhi=A[1]*BG[1]-G[0]*B[0];ok(D>=actualhi,'full positive-D cell ceiling at both edges')
 references.append({'t':str(t),'J_reference_lower':str(Jref[0]),'J_reference_upper':str(Jref[1]),'candidate_J_lower':str(F(row['Jlo'],price.fx.S))})

# Independent exact tail formula prices, all Gamma shapes and rate prefactors.
pf,pz=price.tails();L=price.L;T=price.T;a=price.alpha;rho=(1+F(9,16)*price.kappa)/price.vstar;osc=F(7,16)*price.kappa
low_mass=1-gamma(a,L)[0];low_moment=1-gamma(a+1,L)[0];upper_mass=gamma(a,T)[1];upper_moment=gamma(a+1,T)[1]
ok(F(pf,price.fx.S)>=2*(low_mass+a*low_moment+upper_mass+a*upper_moment),'both complete frozen lower/upper Gamma tails')
z=F(0)
for k,fac in [(1,F(a)),(2,F(a*(a+1)))]:z+=fac/rho**(a+k)*(1-gamma(a+k,rho*L)[0]+gamma(a+k,rho*T)[1])
ok(F(pz,price.fx.S)>=price.K*osc**2*z/32,'both complete transverse tilted-Gamma tails with prefactors')

# Exp recurrence and whole small finite grid runs include L=0 exactly.
runrows=[]
for alpha,kap,L,T in [(4,F(1),F(0),F(8)),(16,F(1,10),F(0),F(32)),(16,F(3),F(1),F(32))]:
 pr=p.Price(alpha,F(2,3),kap,F(100),F(1,7),Nt=8,Ny=8,L=L,T=T,precision_bits=256,max_operations=1000000);f=pr.f_seed
 for i in range(9):
  t=L+i*pr.ht
  for j in range(9):
   l,h=ex(t*pr.phi[j]/pr.vstar);ok(F(f[j][0],pr.fx.S)<=l<=h<=F(f[j][1],pr.fx.S),'seed/ratio repeated exponential enclosure at every small-grid node')
  if i<8:f=[pr.fx.mul(x,r)for x,r in zip(f,pr.f_ratio)]
 out=pr.run();ok(out['P_total_upper']==out['P_frozen_upper']+out['P_transverse_upper'] and out['P_total_upper']>0,'full small-grid complete positive price')
 ok(out['work']['tensor_nodes']==81 and out['work']['rows']==9,'actual tensor nodes and rows ledger')
 runrows.append({'alpha':alpha,'kappa':str(kap),'L':str(L),'T':str(T),'P_total_upper':str(out['P_total_upper']),'work':out['work']})

# Exact aggregation gets the full literal coefficients/mobility, including
# non-first-axis minima, zeros and duplicate aliases; no surrogate H oracle.
for rep in range(30):
 raw=p.old.fixture(16,diagonal=True);mu=[F(rng.randrange(1,30),rng.randrange(1,20))for _ in range(16)];raw['mobility_program']['entries']=[str(x)for x in mu]
 for rec in raw['energy_terms']:rec['coefficient']=str(F(rng.randrange(1,40),rng.randrange(1,20)))
 add=deepcopy(raw['energy_terms'][-1]);add['coefficient']='0';raw['energy_terms'].append(add);raw['energy_terms'].append(deepcopy(raw['energy_terms'][0]))
 canonical,info,Hcoef,dmin,alpha=ac.acquire(raw);coef=[F(0)]*16;pure=[F(0)]*16
 for rec in raw['energy_terms']:
  z=F(rec['coefficient']);support=[i for i,e in enumerate(rec['powers'])if e]
  if len(support)==1:i=support[0];pure[i]+=z;coef[i]+=12*mu[i]*z
  else:i,j=support;coef[j]+=2*mu[i]*z;coef[i]+=2*mu[j]*z
 ok([F(x)for x in info['actual_Hessian_trace_coefficients']]==coef and Hcoef==sum(x*x for x in coef),'full literal actual Hessian coefficients/H exactly aggregated')
 ok(dmin==min(pure) and F(info['actual_mobility_floor'])==min(mu) and alpha==4,'complete actual last-axis coercivity/mobility scan')
 ok(info['duplicate_terms_aggregated']==2 and info['zero_terms_read']==1 and info['literal_exponent_entries_read']==len(raw['energy_terms'])*16,'duplicates zeros exponent bytes remain paid')

# Primitive paid failures and constructor preallocation repair.
kwargs=dict(Nt=2,Ny=2,L=F(0),T=F(8),precision_bits=128)
for change in [dict(max_nodes=8),dict(max_operations=1),dict(max_integer_bits=255),dict(max_exp_terms=1),dict(max_rational_bits=1),dict(Nt=True),dict(Ny=2.0),dict(precision_bits=True),dict(L=F(-1)),dict(T=F(0))]:
 no(lambda change=change:p.Price(4,F(1),F(1),F(1),F(1),**{**kwargs,**change}),'finite primitive domain/work/bit UNKNOWN')
for key in ['beta','kappa','H','dmin']:
 args=dict(alpha=4,beta=F(1),kappa=F(1),H=F(1),dmin=F(1));args[key]=True;no(lambda args=args:p.Price(**args,**kwargs),'strict exact primitive scalar types')
old=p.Intervals;calls=[]
def forbidden(*args):calls.append(args);raise AssertionError('allocation before guard')
p.Intervals=forbidden
no(lambda:p.Price(4,F(1),F(1),F(1),F(1),Nt=1,Ny=1,precision_bits=10**9,max_integer_bits=1),'repaired enormous-precision request rejected before allocation')
ok(not calls,'no fixed-point constructor reached before bit guard');p.Intervals=old
(H/'independent_J_references.json').write_text(json.dumps(references,indent=2)+'\n');(H/'small_grid_runs.json').write_text(json.dumps(runrows,indent=2)+'\n')
report={'status':'PASS','checks':checks,'categories':cats,'refusals':refusals,'reference_exp_calls':exp_calls,'exact_spatial_moment_degree':N+1,'seconds':time.perf_counter()-start,'scope':'numerical primitive and coefficient acquisition only, not frozen whole consumer acceptance'};(H/'positive_exact_v3_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2))
