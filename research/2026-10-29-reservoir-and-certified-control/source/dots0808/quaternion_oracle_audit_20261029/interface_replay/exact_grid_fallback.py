"""Complete finite rational-quaternion fallback, deliberately not a fast claim."""
from fractions import Fraction as F
import itertools,json,math,time
from pathlib import Path

def ceil_q(x):return (x.numerator+x.denominator-1)//x.denominator

def evaluate(coeff,q):return sum(c*math.prod(q[i]**e[i] for i in range(4)) for e,c in coeff.items() if c)

def grid_fallback(coeff,tolerance,max_points=None):
 coeff={tuple(e):F(c) for e,c in coeff.items()};tolerance=F(tolerance)
 if tolerance<=0:raise ValueError('positive tolerance required')
 L=4*sum(abs(c) for c in coeff.values());m=max(1,ceil_q(2*L/tolerance));count=(2*m+1)**3
 if max_points is not None and count>max_points:
  return dict(status='budget_exceeded_no_oracle_success',required_points=count,m=m,L=str(L),tolerance=str(tolerance))
 best=None;arg=None;start=time.time();visited=0
 for k in itertools.product(range(-m,m+1),repeat=3):
  rr=sum(x*x for x in k);den=m*m+rr;q=[F(m*m-rr,den)]+[F(2*m*x,den) for x in k]
  v=evaluate(coeff,q);visited+=1
  if best is None or v<best:best,arg=v,q
 lower=best-2*L/m
 assert visited==count and best-lower<=tolerance and sum(x*x for x in arg)==1
 return dict(status='complete_exact_grid_certificate',m=m,visited_points=visited,L=str(L),lower=str(lower),upper=str(best),quaternion=[str(x) for x in arg],gap=str(best-lower),seconds=time.time()-start)

if __name__=='__main__':
 # Full execution exercises exact coverage/cap contracts; accuracy is intentionally modest.
 f={(4,0,0,0):F(1)}
 result=dict(executed=grid_fallback(f,F(1),max_points=10000),forced_limit=grid_fallback(f,F(1,1000),max_points=10000),scope='Complete finite fallback, polynomial in coefficient magnitude and inverse tolerance, not polynomial in input bit length. Modest-grid execution is not evidence of fast fine-accuracy fallback.')
 print(json.dumps(result,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
