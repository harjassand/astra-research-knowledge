"""Independent exact checks of root model algebra. Not a substitute for proof."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'neutral_return_obstruction_root_20261101/STABLE_PATH_NETWORK_BOUNDED_PROFILE_OBSTRUCTION.md'
EXPECTED='0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);zero=z();one=z(A);two=z(A,A)
pairs=[(zero,one),(two,z(A,C)),(two,z(A,D)),(two,z(A,E)),(z(A,E),z(C,D)),(z(C,D),z(A,B))]
channels=[uv for u,v in pairs for uv in [(u,v),(v,u)]]
def rate(u,x):
 p=1
 for k,n in zip(u,x):
  for j in range(k):p*=max(0,n-j)
 return p
bad=[(u,v) for u,v in channels if u[A]>0 and u!=z(A,B)]
def driftA(x):return sum(rate(u,x)*(v[A]-u[A]) for u,v in channels)
def badrate(x):return sum(rate(u,x) for u,v in bad)
count=0
for m in [0,1,2,4,10]:
 for ell in [0,1,3,8]:
  N=2*(3*m+ell+3)
  den=N-3*m-ell-2
  for I in range(m+1):
   for a in range(I+2):
    for e in range(ell+1):
     c=d=1+I-a;b=N-I+a-e;x=(a,b,c,d,e)
     exact=1-a-3*a*(a-1)+a*(c+d)+2*c*d-a*b
     assert driftA(x)==exact
     assert badrate(x)==a+3*a*(a-1)+a*(c+d+2*e)
     assert driftA(x)<=1+2*(m+1)**2-den*a
     assert badrate(x)<=(3+5*m+2*ell)*a
     # Falling-factorial detailed balance against product Poisson(1), with
     # normalizing exponential removed; exact rational arithmetic.
     import math
     pi=lambda y:F(1,math.prod(math.factorial(n) for n in y))
     for u,v in channels:
      q=rate(u,x)
      if not q:continue
      y=tuple(xx+vv-uu for xx,uu,vv in zip(x,u,v))
      assert pi(x)*q==pi(y)*rate(v,y)
     count+=1
# Verify dominant invariants across each retained enabled jump, augmenting state
# with immigration counter I. These are state identities, not simulated paths.
dominant=[(zero,one),(z(A,B),z(C,D)),(z(C,D),z(A,B)),(z(C,D),z(A,E))]
invchecks=0
for I in range(5):
 for a in range(I+2):
  for e in range(5):
   x=(a,100-I+a-e,1+I-a,1+I-a,e)
   for u,v in dominant:
    if rate(u,x):
     y=tuple(xx+vv-uu for xx,uu,vv in zip(x,u,v));J=I+int(u==zero)
     assert y[C]+y[A]==y[D]+y[A]==1+J
     assert y[B]==100-J+y[A]-y[E]
     invchecks+=1
# The claimed polynomial constants are checked exactly on integer T (the proof
# treats all real T>=1 by ceiling inequalities).
for T in range(1,101):
 m=2*T;ell=2*T*(1+m)**2;N=88*T**3
 den=N-3*m-ell-2
 actual=F((3+5*m+2*ell)*(1+2*(m+1)**2)*T,den)
 assert actual<=F(5544*T**6,N)
# Verify the model is a connected tree on exactly the advertised six binary
# complexes: 2A, AB, AC, AD, AE, CD.
adj={}
for u,v in pairs[1:]:adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
seen={two};todo=[two]
while todo:
 for v in adj[todo.pop()]:
  if v not in seen:seen.add(v);todo.append(v)
assert len(seen)==6 and len(pairs[1:])==5
assert {z(A,i) for i in range(1,5)}<=seen
assert all(sum(u)==sum(v)==2 for u,v in pairs[1:])
assert z(C,D) not in adj[two]
result={'status':'PASS_INDEPENDENT_ALGEBRA_AND_MODEL_CHECKS_WITH_ANALYTIC_AUDIT',
 'source_sha256':EXPECTED,'exact_state_checks':count,'dominant_invariant_checks':invchecks,
 'polynomial_constant_checks':100,'source_unchanged':hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED}
(ROOT/'audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
