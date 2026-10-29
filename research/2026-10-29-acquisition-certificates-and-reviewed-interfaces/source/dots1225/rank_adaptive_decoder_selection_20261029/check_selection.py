from fractions import Fraction as F
from math import comb
import json
from pathlib import Path

def ceilq(x):return -(-x.numerator//x.denominator)
def log2upper_inverse(delta):
 b=0
 while F(1,2**b)>delta:b+=1
 return b

def cdf_exact(n,p,t):
 a,b=p.numerator,p.denominator;den=b**n
 if a==0:return F(int(t>=0))
 term=(b-a)**n;total=term
 for i in range(t):
  term=term*(n-i)*a//((i+1)*(b-a));total+=term
 return F(total,den)
rows=[]
for alpha in [F(1,4),F(1,8),F(1,16)]:
 for delta in [F(1,8),F(1,32)]:
  for stage in [0,1,3]:
   dj=delta/F(2**(stage+1));b=log2upper_inverse(dj);m=ceilq(32*b/alpha);t=(3*alpha*m/4).__floor__()
   falsepass=cdf_exact(m,alpha,t);reject=1-cdf_exact(m,alpha/4,t)
   assert falsepass<=dj and reject<=dj**8
   rows.append(dict(alpha=str(alpha),delta=str(delta),stage=stage,b=b,tests=m,max_accepted_failures=t,false_accept_at_boundary=float(falsepass),false_accept_bound=str(dj),good_rejection=float(reject),good_rejection_bound=str(dj**8)))
# Cost-tail ratio: rank growth2^p perstage is dominated by rejection product.
tails=[]
for p in [4,8,16]:
 for jstar in [0,3,8]:
  reach=F(1);terms=[]
  for s in range(30):
   j=jstar+s;terms.append(reach*2**(p*j)*(j+1));reach*=F(1,2**(j+4))**8
  ratio=F(2**p)*F(31+jstar,30+jstar)*F(1,2**(29+jstar+4))**8
  assert ratio<1
  tails.append(dict(query_rank_exponent=p,first_good_stage=jstar,partial_expected_work=float(sum(terms)),next_ratio_upper=float(ratio)))
out=dict(exact_binomial_cases=rows,cost_tail_checks=tails,scope='Exact rational statistical/controller checks; candidate physical decoder is a separately reviewed dependency')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print('passed',len(rows),'exact binomial cases and',len(tails),'tail checks')
