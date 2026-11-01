from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import sys,json,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'replay/matched_energy_clock_constructor_20261101'));import positive_integrals as p;import acquire_derivative as ac
checks=0;cats={};start=time.perf_counter()
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 try:fn()
 except p.Unknown:ok(True,k)
 else:raise AssertionError('false budget admission '+k)
# Instrument only the copied module in memory, preserving exact source bytes.
exp_calls=[];orig=p.Intervals.expminus

def traced(self,x):
 before=self.operations;terms=self.exp_terms;r=orig(self,x);s=max(0,x.numerator.bit_length()-x.denominator.bit_length()+2);z=x/F(1<<s)
 while z>F(1,2):z/=2;s+=1
 expected=4*(self.exp_terms-terms)+1+2*s if x else 0
 ok(self.operations-before==expected,'every actual positive-price exp call product ledger')
 exp_calls.append({'argument':str(x),'operations':self.operations-before});return r
p.Intervals.expminus=traced
args=dict(alpha=4,beta=F(2,3),kappa=F(1),H=F(100),dmin=F(1,7),Nt=4,Ny=4,L=F(0),T=F(8),precision_bits=256)
obj=p.Price(**args);out=obj.run();p.Intervals.expminus=orig
Nt=Ny=4;a=4;ts=[F(0),F(2),F(4),F(6),F(8)];valid=sum(sum(F(t/4)>max(F(4*k-1,2),0)for k in range(4))for t in ts if t)
analytic=5*valid+2*sum(t>0 for t in ts)
base=(6*Ny+1)+(Nt+1)*(18*Ny+5)+Nt*(12*Ny+14)+8+2*(Nt+1)*(a-1)+16*a+analytic
ok(out['work']['fixed_operations']==base+sum(x['operations']for x in exp_calls),'full initial rows cells tails sum independent operation formula')
ok(out['work']['interval_additions']==5*Ny*(Nt+1)+(Nt+1)*(a-1)+8*a,'all named interval-addition calls')
ok(out['work']['interval_divisions']==Nt*(Ny+1),'all cell and frozen-price divisions')
ok(out['work']['gamma_survival_calls']==Nt+9,'all Gamma window and BOTH-tail calls')
ok(out['work']['root_calls']==2+sum(t>0 for t in ts)+Nt,'Machin coarea analytic and t32 root calls')
ok(out['work']['rational_power_calls']==valid+2,'analytic positive moment powers and both tilted shapes')
ok(out['work']['tensor_nodes']==(Nt+1)*(Ny+1),'tensor nodes exactly include initial row')
used=out['work']['fixed_operations'];z=p.Price(**args,max_operations=used).run();ok(z['P_total_upper']==out['P_total_upper'],'exact complete primitive product budget admits')
no(lambda:p.Price(**args,max_operations=used-1).run(),'one below COMPLETE product budget refuses including tails')
raw=p.old.fixture(16);canonical,info,_,_,_=ac.acquire(raw);ok(info['aggregation_and_derivative_rational_operations']==4*16+6*15,'all raw coefficient and derivative arithmetic count')

# Standalone tight exact references for the entire small-grid priced upper.
P=768;S=1<<P

def ex(x):
 r=x;s=0
 while r>F(1,2):r/=2;s+=1
 lo=hi=S;termlo=termhi=S
 for j in range(1,161):
  den=r.denominator*j;termlo=termlo*r.numerator//den;termhi=(termhi*r.numerator+den-1)//den
  if j%2:lo-=termhi;hi-=termlo
  else:lo+=termlo;hi+=termhi
  if j==159:lower=max(0,lo)
 upper=hi
 for _ in range(s):lower=lower*lower//S;upper=(upper*upper+S-1)//S
 return F(lower,S),F(upper,S)

def gamma(n,x):
 l,h=ex(x);v=t=F(1)
 for j in range(1,n):t*=x/j;v+=t
 return max(F(0),l*v),min(F(1),h*v)

def root(q):return F(isqrt((q.numerator<<(2*P))//q.denominator)+1,S)
N=128;mom={}
for y in [F(0),F(1,8),F(1,4),F(3,8),F(1,2)]:
 arr=[]
 for n in range(N+2):
  val=F(0);coef=F(1)
  for j in range(n+1):
   if j:coef*=F(n-j+1,j)*(-y*y/2)
   val+=coef/F(2*n+2*j+1)
  arr.append((2*y*y)**n*y*val)
 mom[y]=arr

def integrals(t,y):
 arr=mom[y];coef=F(1);j=arr[0];g=arr[1]
 for n in range(1,N+1):
  coef*=-t/F(2*n);j+=coef*arr[n];g+=coef*arr[n+1]
  if n==N-1:jl=j;gl=g
 return (max(F(0),jl),j),(max(F(0),gl),g)

rows=[]
for t in ts:
 J,G=integrals(t,F(1,2));parts=[]
 for y in mom:
  A,Ap=integrals(t,y)
  if y==F(1,2):B=Bp=(F(0),F(0))
  else:B=(max(F(0),J[0]-A[1]),max(F(0),J[1]-A[0]));Bp=(max(F(0),G[0]-Ap[1]),max(F(0),G[1]-Ap[0]))
  parts.append((A,Ap,B,Bp))
 rows.append((J,parts))
pf=pz=F(0);K=root(F(175,3))/(F(4)+F(1,2))
for i,t in enumerate(ts[1:]):
 W=max(F(0),gamma(4,ts[i])[1]-gamma(4,t)[0]);J=rows[i+1][0][0];pf+=W/(2*J);inner=F(0)
 for j in range(4):
  A0hi=rows[i][1][j+1][0][1];BphiHi=rows[i][1][j][3][1];AphiLo=rows[i][1][j][1][0];B0Lo=rows[i][1][j+1][2][0];D=max(F(0),A0hi*BphiHi-AphiLo*B0Lo)
  y=F(j+1,8);f=ex(t*(2*y*y-y**4)/2)[0];inner+=D*D/(4*J**4*f)
 pz+=K*W*t*root(t)*F(1,4)*inner
pf_tail=2*(1-gamma(4,F(0))[0]+4*(1-gamma(5,F(0))[0])+gamma(4,F(8))[1]+4*gamma(5,F(8))[1]);rho=F(25,32);osc=F(7,16)
pz_tail=K*osc**2/F(32)*(F(4)/rho**5*(1-gamma(5,F(0))[0]+gamma(5,rho*8)[1])+F(20)/rho**6*(1-gamma(6,F(0))[0]+gamma(6,rho*8)[1]))
ok(out['P_frozen_upper']>=pf+pf_tail,'whole frozen-cell price dominates independent exact tighter sum plus tails')
ok(out['P_transverse_upper']>=pz+pz_tail,'whole transverse price K t32 factor2 full cells plus tilted tails')
ok(out['P_frozen_tail_upper']>=pf_tail and out['P_transverse_tail_upper']>=pz_tail,'separately reported tail prices contain independent references')
report={'status':'PASS','checks':checks,'categories':cats,'work':out['work'],'full_price_reference':{'P_frozen_up':str(pf+pf_tail),'P_transverse_up':str(pz+pz_tail)},'seconds':time.perf_counter()-start};(H/'assembly_cost_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='full_price_reference'},indent=2))
