"""Exact full-quartic face forced by the inherited acoustic zeros.

No producer imports. It constructs every homogeneous quartic in four entries,
then enforces the full PSD-kernel equations over the exact acoustic root field
and all left rotations (using an unnormalized rational parametrization).
"""
from pathlib import Path
import json
import sympy as S

HERE=Path(__file__).resolve().parent
a,b,c,d,t,s=S.symbols('a b c d t s',real=True)
A=(a,b,c,d)
tau=S.Rational(1,30)
B=1-3*tau*tau
H=1+3*tau*tau
mod=S.Poly(B**2*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t).monic()
K=S.Matrix([
    -B*(tau*(1-t*t)+H*t*t)*(1+t*t),
    B*t*(H-tau*(1-t*t))*(1+t*t),
    B**2*t*(1-t*t)-tau*H*t*(1+t*t)**2,
    B**2*t*t*(1-t*t)+tau*H*(1+t*t)**2,
]).applyfunc(lambda x:S.rem(x,mod.as_expr(),t))
all_coefficients=[co for x in K for co in S.Poly(x,t).all_coeffs()]
scale=S.ilcm(*(co.q for co in all_coefficients))
K=K.applyfunc(lambda x:S.expand(scale*x))
common=S.igcd(*(int(co) for x in K for co in S.Poly(x,t).all_coeffs()))
K=K.applyfunc(lambda x:x/common)
# O_s=[[1,-s],[s,1]], equal to a proper rotation times sqrt(1+s^2).
Rrot=(S.Integer(1),t,s,s*t)
Krot=S.Matrix([K[0]-s*K[2],K[1]-s*K[3],s*K[0]+K[2],s*K[1]+K[3]])
exponents=[(i,j,k,4-i-j-k) for i in range(5) for j in range(5-i) for k in range(5-i-j)]
monomials=[S.prod(x**e for x,e in zip(A,ee)) for ee in exponents]
row_keys=[(i,u,v) for i in range(4) for u in range(4) for v in range(4)]
columns=[]
exposing=[]
for monomial in monomials:
    hh=S.hessian(monomial,A).subs(dict(zip(A,Rrot)),simultaneous=True)
    vec=hh*Krot
    pol=[S.Poly(S.rem(S.expand(x),mod.as_expr(),t),s,t) for x in vec]
    columns.append(S.Matrix([pol[i].coeff_monomial(s**u*t**v) for i,u,v in row_keys]))
    scalar=S.Poly(S.expand((Krot.T*vec)[0]),s)
    averaged=(3*scalar.nth(0)+scalar.nth(2)+3*scalar.nth(4))/8
    rem=S.Poly(S.rem(averaged,mod.as_expr(),t),t)
    exposing.append(S.factor(4*rem.nth(0)-2*mod.nth(2)*rem.nth(2)))
E=S.Matrix.hstack(*columns)
rr,pivots=E.rref()
N=E.nullspace()
print('equations',E.shape,'rank',len(pivots),'nullity',len(N),flush=True)
T=sum(x*x for x in A)
q=a*d-b*c
X=a*a+c*c-b*b-d*d
F=S.Poly(S.expand(T*T+4*(S.Rational(1084,301)-1)*q*q+4*S.Rational(299,301)*q*X),A)
fv=S.Matrix([F.coeff_monomial(mon) for mon in monomials])
assert E*fv==S.zeros(E.rows,1)
assert sum(x*y for x,y in zip(exposing,fv))==0
den=S.ilcm(*(co.q for co in exposing))
exposing=[int(den*co) for co in exposing]
gcd=S.igcd(*exposing)
assert all(co % gcd == 0 for co in exposing)
exposing=[co//gcd for co in exposing]
assert sum(x*y for x,y in zip(exposing,fv))==0
row_pivots=list(E.T.rref()[1])
minor=E.extract(row_pivots,list(range(34)))
minor_det=minor.det(method='domain-ge')
assert minor_det!=0
basis=[S.Poly(S.expand(sum(v*mon for v,mon in zip(col,monomials))),A) for col in N]
out={'tau':str(tau),'beta':'299/301','r':'1084/301',
     'acoustic_polynomial':str(mod.as_expr()),
     'constraint_rows':E.rows,'constraint_columns':E.cols,
     'exact_rank':len(pivots),'nullity':len(N),
     'monomial_exponents':exponents,'pivot_columns':list(pivots),
     'face_span_basis':[str(S.factor(pp.as_expr())) for pp in basis],
     'primitive_acoustic_kernel':[str(x) for x in K],
     'positive_exposing_functional_coefficients':exposing,
     'exposing_functional_scale':str(S.Rational(den,gcd)),
     'nonzero_minor_rows':row_pivots,
     'nonzero_minor_columns':list(range(34)),
     'nonzero_minor_determinant':str(minor_det),
     'inherited_polynomial_satisfies_constraints':True}
(HERE/'acoustic_face_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ('exact_rank','nullity','inherited_polynomial_satisfies_constraints','exposing_functional_scale')},indent=2),flush=True)
