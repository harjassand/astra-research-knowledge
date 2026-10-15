import sys,json,time,itertools,random
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / 'avalanche_rare_bound'))
from certify import setup,I,below
from trigger_baseline import trigger_rates
mp.iv.dps=90;M=1<<384

def exact(t):
 sign,man,exponent,bc=t
 return (-1 if sign else 1)*Q(man)*Q(2)**exponent

def dyadic_p(s,F,T,t,m):
 u=I(t)*mp.iv.exp(I(F)/(m*I(T)));ps=[]
 for strength in s:
  p=mp.iv.exp(-mp.iv.exp(-I(strength)/I(T))*u);l,h=map(exact,p._mpi_)
  ps.append((int(l*M),-((-h*M).numerator//(-h*M).denominator)))
 return ps

def integer_dp(s,F,m,ps,upper):
 n=len(s);h=[M]*(n+1)
 for j in range(n-1,-1,-1):
  p=ps[j][0 if upper else 1];q=M-p;g=[h[c] if c<m or s[j]*c<=F else 0 for c in range(j+2)]
  h=[(q*g[c]+p*g[c+1]+(M-1 if upper else 0))//M for c in range(j+1)]
 return Q(h[0],M)

out=[]
for n,m in [(100,43),(400,166)]:
 s,F,T,feas,r,R=setup(n)
 for t in [Q(1,10)]:
  ps=dyadic_p(s,F,T,t,m);a=integer_dp(s,F,m,ps,False);b=integer_dp(s,F,m,ps,True);ref=below(s,F,T,t,m);rl,rh=map(exact,ref._mpi_)
  assert a<=rh and rl<=b
  mp.mp.dps=100
  def fmt(q):return mp.nstr(mp.mpf(q.numerator)/q.denominator,90)
  out.append(dict(n=n,m=m,t=str(t),integer_lower=fmt(a),integer_upper=fmt(b),width=fmt(b-a),upper_numerator=str(b.numerator),upper_denominator=str(b.denominator),overlaps_90_digit_interval=True))
# Exhaustively test feasibility constraints and hazard bounds over all thermal-deletion subsets.
random.seed(309);cases=0
for repeat in range(60):
 n=random.randrange(2,10);s=sorted([Q(random.randrange(1,21),20) for _ in range(n)],reverse=True);F=Q(random.randrange(1,n*4),10)
 js={k:sum(v*k>F for v in s) for k in range(1,n+1)};feas=[k for k in js if js[k]>=k]
 if not feas:continue
 n0=max(feas);r=max(js[k]-k+1 for k in js)
 for ell in range(r):
  klow=max(k for k in feas if js[k]-ell>=k)
  allowed=[k for k in feas if klow<=k<=n0-ell and js[k]-k<=ell]
  # Delete only initially active fibers; remaining initial inactive fibers cannot reappear.
  for deleted in itertools.combinations(range(n0),ell):
   alive=[j for j in range(n) if j not in deleted]
   k=max([0]+[c for c in range(1,n+1) if sum(s[j]*c>F for j in alive)>=c])
   assert k in allowed,(s,F,ell,k,allowed)
   survivors=[j for j in alive if s[j]*k>F]
   assert len(survivors)==k
   # Weakest k eligible strengths bound every increasing-in-weakness thermal sum.
   worst=s[js[k]-k:js[k]];actual=[s[j] for j in survivors]
   assert all(x>=y for x,y in zip(sorted(actual),sorted(worst)))
   cases+=1
res={'rare_integer_crosschecks':out,'exhaustive_trigger_constraint_cases':cases};Path(str(Path(__file__).resolve().parent.parent / 'avalanche_independent_audit/rare_result.json')).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
