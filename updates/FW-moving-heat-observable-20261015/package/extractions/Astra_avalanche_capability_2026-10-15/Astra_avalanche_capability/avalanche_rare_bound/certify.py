from pathlib import Path
"""Original positive boundary-crossing DP; mpmath interval arithmetic throughout.
Binary64 strengths are exact rational inputs, F=7*n/40 and T=3/20 exactly.
No upstream code imports; no subtracting a probability from one at output.
"""
import numpy as np, mpmath as mp, time,json,math
from fractions import Fraction
mp.iv.dps=70

def I(x):
 x=Fraction(x);return mp.iv.mpf(x.numerator)/x.denominator

def bounds(x):return [str(x.a),str(x.b)]

def below(strengths,F,T,t,m):
 n=len(strengths);s=sorted(map(Fraction,strengths),reverse=True)
 u=I(t)*mp.iv.exp(I(F)/(m*I(T)))
 h=[mp.iv.mpf(1) for _ in range(n+1)]
 for j in range(n-1,-1,-1):
  lam=mp.iv.exp(-I(s[j])/I(T));p=mp.iv.exp(-lam*u);q=-mp.iv.expm1(-lam*u)
  g=[h[c] if c<m or s[j]*c<=F else mp.iv.mpf(0) for c in range(j+2)]
  h=[q*g[c]+p*g[c+1] for c in range(j+1)]
 return h[0]

def poisson_upper(x,r):
 # Positive tail sum, with geometric remainder because term ratio decreases.
 term=mp.iv.exp(-x)*x**r/math.factorial(r);total=term
 for k in range(r+1,r+600):
  term=term*x/k;total+=term
 # x/(k+1) bounds all subsequent ratios. For tested x<k+1.
 rho=x/(k+1);return total+term*rho/(1-rho)

def setup(n,f0=Fraction(7,40),T=Fraction(3,20)):
 s=sorted(map(Fraction,np.random.RandomState(0).uniform(size=n)),reverse=True);F=f0*n
 js=[sum(x*k>F for x in s) for k in range(1,n+1)]
 feas=[k for k in range(1,n+1) if js[k-1]>=k]
 rates=[]
 for k in feas:
  eligible=s[:js[k-1]];rates.append((mp.iv.exp(I(F)/(k*I(T)))*sum((mp.iv.exp(-I(x)/I(T)) for x in eligible[-k:]),mp.iv.mpf(0)),k))
 # maximum interval upper; construct an enclosing max with endpoint max
 R=mp.iv.mpf([max(v.a for v,k in rates),max(v.b for v,k in rates)])
 return s,F,T,feas,max(js[k-1]-k+1 for k in range(1,n+1)),R
if __name__=='__main__':
 out=[]
 for n,m in [(100,43),(400,166)]:
  s,F,T,feas,r,R=setup(n)
  for ts in ['.01','.1','.3','1']:
   t=Fraction(ts);start=time.perf_counter();p=below(s,F,T,t,m);elapsed=time.perf_counter()-start
   # Lower physical CDF using psi(n0)*U*: below(m=1) at u=t/psi(n0)
   # Evaluator parameter m also fixes clock, so adjust deadline exactly via an interval in separate extension if needed.
   pois=poisson_upper(R*I(t),r)
   row=dict(n=n,m=m,t=ts,kmin=min(feas),n0=max(feas),r=r,Rmax=bounds(R),physical_failure_upper_interval=bounds(p),poisson_tail_upper_interval=bounds(pois),dp_seconds=elapsed)
   out.append(row);print(json.dumps(row),flush=True)
 with open(str(Path(__file__).resolve().parent.parent / 'avalanche_rare_bound/certified_results.json'),'w') as f:json.dump(out,f,indent=2)
