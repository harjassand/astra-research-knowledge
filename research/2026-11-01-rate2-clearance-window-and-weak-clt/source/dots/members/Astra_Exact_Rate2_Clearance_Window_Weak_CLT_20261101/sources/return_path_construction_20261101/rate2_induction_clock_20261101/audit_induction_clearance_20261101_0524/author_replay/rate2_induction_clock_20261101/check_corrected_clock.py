"""Exact identities and polynomial envelopes; not an independent theorem review."""
import sympy as s
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
a,b,c,d,e,w=s.symbols('a b c d e w');x=(a,b,c,d,e)
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);two=z(A,A)
raw=[(z(),z(A),1),(z(A,B),z(C,D),1),(z(C,D),z(A,B),1),(z(C,D),z(A,E),2),(z(A,E),z(C,D),1),(z(A,E),two,1)]
def rate(u,x):
 p=1
 for n,j in zip(x,u):
  for k in range(j):p*=n-k
 return p
def jump(x,u,v):return tuple(a+b-c for a,c,b in zip(x,u,v))
ff=lambda x:x[A]+(x[C]+x[D])/s.Integer(2)-s.Rational(3,4)*w*x[E]**2+w*x[A]*x[E]
lf=s.expand(sum(k*rate(u,x)*(ff(jump(x,u,v))-ff(x)) for u,v,k in raw))
want=1+w*e+w*c*d/2+2*w*a*c*d+a*e*(1+w*(3*e-2*a-s.Rational(3,2)-b))
assert s.expand(lf-want)==0
la=s.expand(sum(k*rate(u,x)*(jump(x,u,v)[A]-a) for u,v,k in raw))
assert s.expand(la-(1+3*c*d-a*b))==0
# Exact retained invariants, allowing count-counter marks.
checks=0
for xx in product(range(4),repeat=5):
 for u,v,k in raw:
  if rate(u,xx)<=0:continue
  yy=jump(xx,u,v);di=int(u==z());dr=int(u==z(A,E) and v==two)
  assert (yy[A]+yy[C])-(xx[A]+xx[C])==di+dr
  assert (yy[A]+yy[D])-(xx[A]+xx[D])==di+dr
  assert yy[B]-xx[B]==-di-2*dr+(yy[A]-xx[A])-(yy[E]-xx[E])
  checks+=1
p,q=s.symbols('p q');H=p+q+1
positive_polynomials={
'drift':100*H**4-q-p**2/2-16*p**4-40*H*p**2*q,
'bracket':64*H**5-4-32*p**2*q-7*H**2*p**2-8*H**2*p**2*q,
'up_count':12*H**3-1-3*p**2-8*p**2*q}
for name,poly in positive_polynomials.items():assert all(cc>=0 for _,cc in s.Poly(s.expand(poly),p,q).terms()),name
assert 16384*3+8+800*3+4608*3+1152*3+48*3<10**5
assert Q(4,3)*(1-Q(4,32))>=1
assert Q(4,3)*(1+Q(2,32))<=Q(13,10)**2
# AE phase bound and fast-A bounds from normalized conditions.
assert Q(48,64)+Q(16,64)<=1
assert Q(1,4)+Q(1,4)==Q(1,2)
assert Q(2,3)*(Q(1,2))**3==Q(1,12)
result={'status':'PASS_AUTHOR_EXACT_IDENTITIES_AND_POLYNOMIAL_ENVELOPES_NOT_INDEPENDENT_REVIEW','retained_channels':6,'global_polynomial_identities':2,'retained_invariant_jump_checks':checks,'coefficientwise_nonnegative_envelopes':list(positive_polynomials),'proof_sha256':hashlib.sha256((root/'FINITE_LEVEL_CORRECTED_CLOCK.md').read_bytes()).hexdigest(),'retained_LF':str(lf)}
(root/'CLOCK_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
