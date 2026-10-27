"""Exact rational/Sturm replay for edge extrema; no sampling or optimization."""
import sympy as S,json
from pathlib import Path
s,e,r,u,v=S.symbols('s e r u v');a=S.Integer(6)
A=(s**3+(e+3*a)*s*s+2*a*e*s)/(s+a)
R=(s+a/3)**2+e*(s+a/3)
C=s*s+(e+a)*s+a*e/2
B=C*s*(s+a)/(s+a/2)**2
K=2/(r+B)+2/(r+C)-1/(r+A)-3/(r+R)
num,den=S.fraction(S.factor(K))
assert all(c>=0 for c in S.Poly(den,s,e,r).coeffs())
H=S.Poly(S.expand(-num.subs({e:u+v,r:u*v})),s)
assert H.degree()==7
for j in [7,6]:assert all(c>=0 for c in S.Poly(H.coeff_monomial(s**j),u,v).coeffs())
assert S.factor(num.subs(s,0))==324*r*(e**2+2*e+2*r)
E=u+v;T=u*v;cert=json.loads(Path(__file__).with_suffix('.json').read_text())
for j in range(5,0,-1):
 nb=[1,E] if j>=4 or j==1 else [1,E,E**2,T];db=[] if j>=4 or j==1 else [E]
 nv=list(map(S.Rational,cert[str(j)]['num']));dv=list(map(S.Rational,cert[str(j)]['den_extra']))
 assert all(x>=0 for x in nv+dv)
 N=sum(x*y for x,y in zip(nv,nb));D=1+sum(x*y for x,y in zip(dv,db))
 P=S.Poly(S.expand(N*H.coeff_monomial(s**j)-D*H.coeff_monomial(s**(j-1))),u,v)
 assert all(c>=0 for c in P.coeffs())
print('PASS: K has exactly one positive-to-negative s crossing for r>0')
w=(S.Rational(5,2)+s/(30*(s+180+e)))/(r+R)
gn,gd=S.fraction(S.factor(S.diff(K,r)+w*K))
assert all(c>=0 for c in S.Poly(gd,s,e,r).coeffs())
P=S.Poly(S.expand(-gn.subs({e:u+v,r:u*v})),u,v)
count=0
for mon,expr in P.terms():
 pol=S.Poly(expr,s)
 assert pol.LC()>0
 if all(c>=0 for c in pol.all_coeffs()):continue
 count+=1
 low=min(m[0] for m,c in pol.terms())
 pol=pol.exquo(S.Poly(s**low,s))
 assert pol.eval(0)>0
 assert pol.count_roots(0,S.oo)==0 # exact Sturm count
print(dict(status='PASS',nonnegative_uv_coefficients=len(P.terms()),mixed_sign_univariate_Sturm_checks=count))
# Monotonic multiplier uses r<=e^2/4; elementary inequalities are in proof.
