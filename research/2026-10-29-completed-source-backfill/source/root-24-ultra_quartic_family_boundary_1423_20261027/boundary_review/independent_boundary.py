"""Independent literal boundary identity in SymPy's algebraic number field.
Imports no author verifier, facial generator, numeric arrays or pickle.
"""
from pathlib import Path
from itertools import combinations_with_replacement as cw
from fractions import Fraction
import json,hashlib,time
import sympy as s
ROOT=Path(__file__).resolve().parent
K=s.QQ.algebraic_field(s.sqrt(42));root42=s.sqrt(42)
a=s.symbols('a0:4',real=True);x=s.symbols('x0:4',real=True);variables=a+x
def load_field(pair):return K.from_sympy(s.Rational(pair[0])+s.Rational(pair[1])*root42)
def expression(pair):return s.Rational(pair[0])+s.Rational(pair[1])*root42
def positive(v):
    values=v.to_list();values=[K.dom.zero]*(2-len(values))+values
    b,c=[Fraction(int(v.numerator),int(v.denominator)) for v in values]
    if b==0:return c>0
    if c==0:return b>0
    if b>0 and c>0:return True
    if b<0 and c<0:return False
    return c*c>42*b*b if c>0 else 42*b*b>c*c
def poly(p):return s.Poly(p,*variables,domain=K)
def invariants(y):
    aa,b,c,d=y;return aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
def energy(y,tau):
    u,v,w,q=invariants(y)
    return u*u+v*v+3*w*w+tau*q*q+4*q*(u-v)
def components(z):
    p=s.expand_complex(z).expand()
    return poly(s.re(p).expand()),poly(s.im(p).expand())
def ldl(A):
    n=len(A);L=[[K.one if i==j else K.zero for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        pivot=A[j][j]-sum((L[j][k]*L[j][k]*D[k] for k in range(j)),K.zero)
        assert positive(pivot),j;D.append(pivot)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),K.zero))/pivot
    assert all(A[i][j]==sum((L[i][k]*L[j][k]*D[k] for k in range(n)),K.zero) for i in range(n) for j in range(n))
    return D
def main():
    started=time.monotonic();path=ROOT.parent/'quartic_alternative/sector_boundary/EXACT_BOUNDARY_SUPPORT.json'
    raw=path.read_bytes();data=json.loads(raw);tau=89-12*root42
    assert expression(data['tau'])==tau
    alpha=expression(data['selector_alpha']);delta=expression(data['selector_delta'])
    u,v,w,q=invariants(a);qx=invariants(x)[3];f=energy(a,tau)
    target=poly(sum(t*t for t in x)*(energy(tuple(ai+xi for ai,xi in zip(a,x)),tau)-f-
       sum(s.diff(f,a[i])*x[i] for i in range(4))-(alpha*(u-v)+delta*q)*qx))
    ac=[a[0]+s.I*a[2],a[1]+s.I*a[3]];xc=[x[0]+s.I*x[2],x[1]+s.I*x[3]]
    spin1=[s.I**(i+j+k)*ac[i]*xc[j]*s.conjugate(xc[k]) for i in range(2) for j in range(2) for k in range(2)]
    spin1 += [s.I**(i+j+k)*s.conjugate(ac[i])*xc[j]*xc[k] for i in range(2) for j,k in cw(range(2),2)]
    spin1 += [s.I**(i+j+k)*xc[i]*xc[j]*s.conjugate(xc[k]) for i,j in cw(range(2),2) for k in range(2)]
    spin3=[s.I**(i+j+k)*ac[i]*xc[j]*xc[k] for i in range(2) for j,k in cw(range(2),2)]
    spin3 += [s.I**(i+j+k)*xc[i]*xc[j]*xc[k] for i,j,k in cw(range(2),3)]
    rebuilt=poly(0);total_pivots=0
    for b,features in enumerate([spin1,spin3]):
        split=[components(z) for z in features]
        V=[[load_field(p) for p in row] for row in data['basis_matrices'][b]]
        matrix=[[load_field(p) for p in row] for row in data['positive_blocks'][b]]
        n=len(matrix);assert n==[16,6][b] and len(V)==len(features)
        assert all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n))
        reduced=[]
        for j in range(n):
            reduced.append(tuple(sum((split[i][part].mul_ground(K.to_sympy(V[i][j])) for i in range(len(V))),poly(0)) for part in [0,1]))
        for i in range(n):
            for j in range(i,n):
                p=reduced[i][0]*reduced[j][0]+reduced[i][1]*reduced[j][1]
                rebuilt +=p.mul_ground(K.to_sympy(matrix[i][j])*(1 if i==j else 2))
        rho=K.from_sympy(s.Rational(1,200))
        pivots=ldl([[matrix[i][j]-(rho if i==j else K.zero) for j in range(n)] for i in range(n)])
        assert pivots==[load_field(p) for p in data['shifted_LDL_pivots'][b]]
        total_pivots+=n
    assert rebuilt==target
    assert s.simplify(delta-(162-21*root42-alpha*(-s.Rational(3,2)+root42/3)))==0
    # Independent exact witness for every parameter BELOW the boundary.
    pair_raw=(path.parent/'CRITICAL_PAIR.json').read_bytes();pair=json.loads(pair_raw)
    z=s.symbols('z',real=True);m=expression(pair['critical_m'])
    assert positive(K.from_sympy(m-s.Rational(5,2)))
    modulus=s.Poly(z**4-m*z*z+1,z,domain=K)
    critical=[sum(expression(c)*z**j for j,c in enumerate(row)) for row in pair['A_polynomial_coefficients']]
    curvature=s.diff(f,a[0],2)+2*z*s.diff(f,a[0],a[1])+z*z*s.diff(f,a[1],2)
    acoustic=s.hessian(curvature,a)/2
    for entry in acoustic*s.Matrix(critical):assert s.Poly(entry,z,domain=K).rem(modulus).is_zero
    g0=expression(pair['cofactor_pairing_g0']);g2=expression(pair['cofactor_pairing_g2'])
    cf=g0+g2*z*z
    assert s.Poly(critical[3]-z*critical[2]-cf,z,domain=K).rem(modulus).is_zero
    assert positive(-K.from_sympy(g2)) and positive(-K.from_sympy(g0+2*g2))
    q2=invariants(a)[3]**2
    detsquare_curvature=s.diff(q2,a[0],2)+2*z*s.diff(q2,a[0],a[1])+z*z*s.diff(q2,a[1],2)
    substituted=detsquare_curvature.subs(dict(zip(a,critical)),simultaneous=True)
    assert s.Poly(substituted-2*cf*cf,z,domain=K).rem(modulus).is_zero
    out={'status':'INDEPENDENT_ALGEBRAIC_BOUNDARY_LITERAL_IDENTITY_AND_POSITIVITY_PASS',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),
      'critical_pair_sha256':hashlib.sha256(pair_raw).hexdigest(),
      'field':'SymPy QQ(sqrt42), positive real embedding checked by rational squares',
      'positive_shifted_pivots':total_pivots,'complex_feature_blocks':[20,10],
      'positive_reduced_blocks':[16,6],'literal_polynomial_coefficients':len(target.terms()),
      'critical_pair_kernel':'EXACT_MOD_QUARTIC_FROM_LITERAL_HESSIAN',
      'cofactor_pairing_nonzero':'EXACT_REAL_FIELD_SIGNS_AND_Z_SQUARED_GT_2',
      'all_lower_tau':'CURVATURE_EQUALS_2_TIMES_TAU_MINUS_EDGE_TIMES_NONZERO_SQUARE',
      'seconds':time.monotonic()-started,
      'scope':'Global boundary PC support, PSD factors and fixed all-lower-parameter non-ROC witness independently checked. Together with the whole-read analytic finite-lift/addition/null-Lagrangian proof, accepts the exact ROC=PC=QC threshold on this line; no source-author code imported.'}
    (ROOT/'INDEPENDENT_BOUNDARY_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
