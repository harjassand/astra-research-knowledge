"""Exact rational certificate: no optimizer or floating point is used in this replay."""
import json
from pathlib import Path
import sympy as S
s,x,y,z=S.symbols('s x y z');ds=[s+x,s+y,s+z]
A=S.prod(ds)+6*sum(ds[i]*ds[j] for i,j in [(0,1),(0,2),(1,2)])
Q=S.prod(ds[i]*ds[j]+3*(ds[i]+ds[j]) for i,j in [(0,1),(0,2),(1,2)])
H=S.Poly(S.expand(Q**2-A*S.prod(d+2 for d in ds)**3),s)
assert H.degree()==10
for j in range(7,11):assert all(c>=0 for c in S.Poly(H.coeff_monomial(s**j),x,y,z).coeffs())
assert H.coeff_monomial(s**10)==72
cert=json.loads(Path(__file__).with_suffix('.json').read_text());E=x+y+z;E2=x*y+x*z+y*z;E3=x*y*z
for j in range(6,0,-1):
 if j>=4:nb=[1,E];db=[]
 elif j>=2:nb=[1,E,E**2,E2];db=[E]
 else:nb=[1,E,E**2,E2,E**3,E*E2,E3];db=[E,E**2,E2]
 nv=list(map(S.Rational,cert[str(j)]['num']));dv=list(map(S.Rational,cert[str(j)]['den_extra']))
 assert all(v>=0 for v in nv+dv)
 N=sum(v*m for v,m in zip(nv,nb));D=1+sum(v*m for v,m in zip(dv,db))
 rem=S.Poly(S.expand(N*H.coeff_monomial(s**j)-D*H.coeff_monomial(s**(j-1))),x,y,z)
 assert all(c>=0 for c in rem.coeffs())
 print(dict(j=j,nonnegative_remainder_monomials=len(rem.terms()),minimum_coefficient=str(min(rem.coeffs()))))
print('PASS: exact descending-coefficient implication and at-most-one-positive-root certificate')
