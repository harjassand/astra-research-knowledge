"""Try to extend the exposed-ray calculation to the entire curved ROC arc.

All symbolic work is scientific derivation within this directory. The exact
finite-seed theorem is verified independently by verify_extreme.py.
"""
from pathlib import Path
import json,time
import sympy as S
from sympy.polys.matrices import DomainMatrix

start=time.time();HERE=Path(__file__).resolve().parent
a,b,c,d,t,s,u=S.symbols('a b c d t s u',real=True);A=(a,b,c,d)
B=1-3*u*u;H=1+3*u*u
mod=S.Poly(B**2*(1-t*t)**2-(1-4*u+3*u*u)*H*(1+t*t)**2,t).monic()
K=S.Matrix([-B*(u*(1-t*t)+H*t*t)*(1+t*t),
 B*t*(H-u*(1-t*t))*(1+t*t),
 B**2*t*(1-t*t)-u*H*t*(1+t*t)**2,
 B**2*t*t*(1-t*t)+u*H*(1+t*t)**2])
K=K.applyfunc(lambda x:S.cancel(S.rem(x,mod.as_expr(),t)))
den=S.factor(S.lcm_list([S.denom(co) for x in K for co in S.Poly(x,t).all_coeffs()]))
K=K.applyfunc(lambda x:S.Poly(x,t).mul_ground(den).as_expr().expand())
Rrot=(S.Integer(1),t,s,s*t)
Krot=S.Matrix([K[0]-s*K[2],K[1]-s*K[3],s*K[0]+K[2],s*K[1]+K[3]])
exponents=[(i,j,k,4-i-j-k) for i in range(5) for j in range(5-i) for k in range(5-i-j)]
monomials=[S.prod(x**e for x,e in zip(A,ee)) for ee in exponents]
row_keys=[(i,v,w) for i in range(4) for v in range(4) for w in range(4)]
columns=[]
for monomial in monomials:
    hh=S.hessian(monomial,A).subs(dict(zip(A,Rrot)),simultaneous=True)
    vec=hh*Krot
    pol=[S.Poly(S.rem(S.expand(x),mod.as_expr(),t),s,t) for x in vec]
    columns.append([S.factor(pol[i].coeff_monomial(s**v*t**w)) for i,v,w in row_keys])
E=S.Matrix.hstack(*(S.Matrix(col) for col in columns))
print('generic matrix built',time.time()-start,flush=True)
seed=json.loads((HERE/'acoustic_face_result.json').read_text())
rows=seed['nonzero_minor_rows'];cols=seed['nonzero_minor_columns']
M=E.extract(rows,cols)
# Clear one common denominator for each row, then compute a polynomial
# determinant over QQ[u], not numerical interpolation.
scales=[]
for i in range(M.rows):
    scale=S.factor(S.lcm_list([S.denom(x) for x in M.row(i)]))
    scales.append(scale)
    for j in range(M.cols):M[i,j]=S.cancel(M[i,j]*scale)
print('row denominators cleared',time.time()-start,flush=True)
DD=DomainMatrix.from_Matrix(M).convert_to(S.QQ.poly_ring(u)).det().as_expr()
det=S.factor(DD)
print('det factorized',det,'seconds',time.time()-start,flush=True)
out={'parameter':'u','minor_rows':rows,'minor_columns':cols,
     'kernel_clear_denominator':str(den),
     'row_denominators':[str(x) for x in scales],
     'polynomial_minor_determinant':str(det),
     'seconds':time.time()-start}
(HERE/'generic_face_result.json').write_text(json.dumps(out,indent=2)+'\n')
