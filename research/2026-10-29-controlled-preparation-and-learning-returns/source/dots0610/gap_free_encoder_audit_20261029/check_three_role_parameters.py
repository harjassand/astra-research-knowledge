from fractions import Fraction as F
from math import comb,isqrt,log,sqrt,exp
from pathlib import Path
import json

def ceilroot(n,k):
 lo,hi=0,1
 while hi**k<n:hi*=2
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**k<n:lo=mid
  else:hi=mid
 return hi
rows=[]
for h in [5,10,20,40,80,120,160,256]:
 B=2**h;n=4*h;T=9*B;t=B//8;b=B//32
 C=F(n+2,n-1);p=F(1,3);s=F(2,3)/(C+1);a=F(2,3)*C/(C+1)
 assert p+a+s==1 and C*s/a==1 and s*T>=2*B
 d=comb(n,n//2)//(n//2+1);alpha=F(2**n,d)
 m=5*ceilroot(T,4);M=(2*m+1)**3;l=(M-1).bit_length()
 # k=ceil sqrt(3T/l) with exact integer comparisons.
 k=isqrt((3*T)//l)
 while k*k*l<3*T:k+=1
 eta=F(1,6+k);assert eta<=p/2
 # Exact conservative regret uses eps<=5/m and log M<=l, no floating decisions.
 LT=F(225*T,2*m*m)+45*(F(l,1)/eta+eta*T/p)
 abort=a*alpha*(n-1)*LT/(b+1)
 soundexp=F((t-b+1)**2,2*(t+b+1));assert soundexp>=F(3*B,128)
 assert F(h*B,2*n*T)==F(1,72)
 rows.append({'h':h,'n':n,'T':str(T),'net_m':str(m),'M':str(M),'eta':str(eta),'regret_bound_float':float(LT),'failure_abort_bound_float':float(abort),'source_exposure_rate':'1/72','soundness_exponent_lower':str(F(3*B,128))})
assert rows[-1]['failure_abort_bound_float']<1e-20
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'Exact rational conservative parameters instantiate v2 learner and v3 roles; floats only for display. This is not a run with the huge net/outer code.','rows':rows},indent=2))
print(json.dumps([{'h':x['h'],'abort_bound':x['failure_abort_bound_float']} for x in rows]))
