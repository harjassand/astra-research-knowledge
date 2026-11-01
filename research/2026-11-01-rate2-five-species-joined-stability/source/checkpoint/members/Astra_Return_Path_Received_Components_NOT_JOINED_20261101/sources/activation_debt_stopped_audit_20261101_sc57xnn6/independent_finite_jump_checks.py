"""Independent rational interval verification of literal twelve-channel generator.
No author program imported. Analytic proof, not finite tests, is controlling.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib,json,time
PTH=Path(__file__).resolve().parent
A0=F(1,100);q=2;eps=20

def vector(*indices):return tuple(indices.count(i)for i in range(5))
rows=[(vector(),vector(0),1,'birth'),(vector(0),vector(),1,'death')]
for i in [2,3,4]:rows.extend([(vector(0,0),vector(0,i),1,'forward_'+str(i)),(vector(0,i),vector(0,0),1,'reverse_'+str(i))])
rows.extend([(vector(0,4),vector(2,3),1,'AE_CD'),(vector(2,3),vector(0,4),2,'CD_AE'),(vector(2,3),vector(0,1),1,'CD_AB'),(vector(0,1),vector(2,3),1,'AB_CD')])

def coords(x):
 A,B,C,D,E=x;return A+C,A+D,F(B-A-99*E,100)
def cubic(c,d,t):return c*d*t+F(c+d,2)*t*t+t*t*t/3
@lru_cache(None)
def root(c,d,H):
 if H<=0:return F(0),F(0)
 lo=F(0);hi=F(1)
 while q*cubic(c,d,hi)<H:hi*=2
 for _ in range(128):
  mid=(lo+hi)/2;v=q*cubic(c,d,mid)
  if v==H:return mid,mid
  if v<H:lo=mid
  else:hi=mid
 return lo,hi
@lru_cache(None)
def exp_bound(x):
 if x<0:
  lo,hi=exp_bound(-x);return 1/hi,1/lo
 assert x<=2
 term=F(1);total=F(1)
 for k in range(1,41):term=term*x/k;total+=term
 nextterm=term*x/41
 remainder=nextterm/(1-x/42)
 return total,total+remainder

def transitions(x):
 for u,v,k,name in rows:
  rate=k
  for xi,ui in zip(x,u):
   if xi<ui:rate=0;break
   for j in range(ui):rate*=xi-j
  if rate:yield rate,tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v)),sum(v)-sum(u),name

def exact_phase(x):return 1+F(eps*x[0]*x[0],x[1]+1)
def generator_terms(x):
 old=coords(x);tl,th=root(*old);h=exact_phase(x);out=[]
 for rate,y,dN,name in transitions(x):
  new=coords(y);assert new[2]>0
  if new==old:lo=hi=F(1)
  else:
   yl,yh=root(*new);lo=exp_bound(yl-th)[0];hi=exp_bound(yh-tl)[1]
  ratio=exact_phase(y)/h;out.append((rate,lo*ratio,hi*ratio,dN,name))
 return tl,th,out

def ceil(x):return -(-x.numerator//x.denominator)

def main():
 start=time.monotonic();mu=F(1,198);nu=F(1,99);theta=16*mu/2+2*nu+9*F(101,100)*mu/8
 assert theta==F(10509,158400) and theta<F(1,15)
 endpoint=-F(4319,12500);phase=F(501,2640);slack=-(endpoint+phase)-F(3,20);assert slack>0
 assert F(35,3)*F(99,104)>10+F(3,20)
 assert F(3,200)<F(1,64)
 assert 1+6+F(6**2,2)>21
 assert 3000**2>200**3
 assert 7-F(3,20)*100==-8 and F(2,3)-F(1,2)==F(1,6)
 # Check all linear-coordinate ledger entries independently from stoichiometry.
 expected=[(1,1,-A0,1),(-1,-1,A0,-1),(0,-1,A0,0),(0,1,-A0,0),(-1,0,A0,0),(1,0,-A0,0),(-1,-1,2*A0-1,0),(1,1,1-2*A0,0),(0,0,F(1),0),(0,0,F(-1),0),(0,0,F(0),0),(0,0,F(0),0)]
 for (u,v,k,name),wanted in zip(rows,expected):
  cu,du,hu=coords(u);cv,dv,hv=coords(v);assert (cv-cu,dv-du,hv-hu,sum(v)-sum(u))==wanted
 identity_count=0
 for c in [0,1,10,10**9]:
  for d in [0,1,10,10**9]:
   for t in [F(2),F(5,2),F(3),F(100)]:
    assert cubic(c+1,d+1,t-1)==cubic(c,d,t)-cubic(c,d,F(1));identity_count+=1
 states=[]
 for target in [F(2),F(3),F(100)]:
  for A in [0,1,2,20]:
   for C,D in [(0,0),(0,1),(1,0),(1,1),(1,10**6),(10**6,1),(10**6,10**6),(10**9,0),(0,10**9)]:
    for E in [0,10**12]:
     H=q*cubic(A+C,A+D,target);B=A+99*E+ceil(100*H);states.append((A,B,C,D,E))
 states=list(dict.fromkeys(states));checks=0;zeroA=0;active=0;worst=None;counts={}
 for x in states:
  tl,th,terms=generator_terms(x);assert tl>=2
  A,B,C,D,E=x;c=A+C;d=A+D
  reserve=F(3,20)+10*A*A+th/4*(F(A*C)/(d+th+1)+F(A*D)/(c+th+1))
  for r in [F(1),F(1000001,1000000),F(101,100)]:
   lo=sum(rate*(r**dN*a-1)for rate,a,b,dN,name in terms)
   hi=sum(rate*(r**dN*b-1)for rate,a,b,dN,name in terms)
   assert lo<=hi and hi+reserve<=0,(x,r,'strengthened generator bound')
   if tl>=100:assert hi<=-F(1,2)
   margin=(-hi-reserve)*10**6;floor=margin.numerator//margin.denominator
   if worst is None or floor<worst['certified_margin_millionths']:worst={'state':list(x),'r':str(r),'certified_margin_millionths':floor,'root_lower_ge_two':tl>=2}
   checks+=1
  zeroA+=A==0;active+=A>0
  for rate,a,b,dN,name in terms:counts[name]=counts.get(name,0)+1
 result={'status':'PASS_INDEPENDENT_EXACT_RATIONAL_INTERVAL_FINITE_JUMP_CHECKS','inputs':{n:hashlib.sha256((PTH/n).read_bytes()).hexdigest()for n in ['FULL_GENERATOR_STOPPED_DRIFT.md','STRENGTHENED_CUTOFF_TWO.md','UNIFORM_PAID_CHARGING_COROLLARY_PENDING.md']},'author_code_imported':False,'state_count':len(states),'generator_checks':checks,'A_zero_states':zeroA,'A_positive_states':active,'ledger_rows':len(rows),'paid_charging_constant_checks':5,'polynomial_shift_identities':identity_count,'reaction_occurrences':counts,'theta_at_cutoff':str(theta),'A_zero_endpoint_phase_margin_over_3_20':str(slack),'root_bisection_steps':128,'exponential_taylor_degree':40,'r_equal_one_explicitly_checked':True,'worst_recorded_certified_margin':worst,'scope':'Finite supplements to the uniform analytic stopped-domain proof, no global theorem.'}
 (PTH/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'states':len(states),'generator_checks':checks,'elapsed_seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':main()
