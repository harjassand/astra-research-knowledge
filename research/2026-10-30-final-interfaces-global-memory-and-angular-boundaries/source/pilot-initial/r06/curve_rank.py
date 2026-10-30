"""Exact all-parameter rank proof, using a symbolic determinant and finite fields.

The main determinant is an exact rational-function identity, not a sample
interpolation. For an irreducible factor with real roots in (0,1/3), a
finite-field rank witness rules out its dividing every 34-minor. Thus the
rank cannot fall at any of that factor's characteristic-zero roots.
"""
from pathlib import Path
import json,time
import sympy as S

HERE=Path(__file__).resolve().parent;start=time.time()
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
global_den=S.factor(S.lcm_list([S.denom(x) for x in E]))
EP=[[S.Poly(S.cancel(global_den*E[i,j]),u) for j in range(E.cols)] for i in range(E.rows)]
assert all(co.is_Integer for row in EP for pp in row for co in pp.all_coeffs())
assert global_den==u*(3*u*u-3*u+1)

def rank_mod(matrix,p):
    aa=[[int(x)%p for x in row] for row in matrix]
    original_rows=list(range(len(aa)));pivrows=[];pivcols=[];rr=0
    for j in range(len(aa[0])):
        ii=next((i for i in range(rr,len(aa)) if aa[i][j]),None)
        if ii is None:continue
        aa[ii],aa[rr]=aa[rr],aa[ii]
        original_rows[ii],original_rows[rr]=original_rows[rr],original_rows[ii]
        pivrows.append(original_rows[rr]);pivcols.append(j)
        inv=pow(aa[rr][j],-1,p)
        aa[rr]=[(x*inv)%p for x in aa[rr]]
        for i in range(rr+1,len(aa)):
            if aa[i][j]:
                co=aa[i][j];aa[i]=[(x-co*y)%p for x,y in zip(aa[i],aa[rr])]
        rr+=1
        if rr==len(aa):break
    return rr,pivrows,pivcols

def evaluate_mod(poly,root,p):
    ans=0
    for co in poly.all_coeffs():ans=(ans*root+int(co))%p
    return ans

generic=json.loads((HERE/'generic_face_result.json').read_text())
det=S.sympify(generic['polynomial_minor_determinant'],locals={'u':u})
factors=S.factor_list(det,u)[1]
proof=[]
for factor,multiplicity in factors:
    pp=S.Poly(factor,u)
    assert pp.is_irreducible
    assert S.gcd_list(pp.all_coeffs())==1
    count=pp.count_roots(S.Rational(0),S.Rational(1,3))
    if pp.eval(0)==0 or pp.eval(S.Rational(1,3))==0:count=0
    item={'irreducible_factor':str(factor),'multiplicity':int(multiplicity),'real_roots_inside':int(count)}
    if count:
        witness=None
        for prime in S.primerange(101,1000):
            for root in range(prime):
                if evaluate_mod(pp,root,prime):continue
                if evaluate_mod(S.Poly(global_den,u),root,prime)==0:continue
                mm=[[evaluate_mod(EP[i][j],root,prime) for j in range(E.cols)] for i in range(E.rows)]
                rank,ii,jj=rank_mod(mm,prime)
                if rank==34:
                    witness={'prime':prime,'root_mod_prime':root,'rank_mod_prime':rank,
                             'independent_rows':ii,'independent_columns':jj}
                    break
            if witness:break
        if witness is None:
            raise AssertionError('No rank-34 arithmetic witness found for '+str(factor))
        item['factor_does_not_divide_all_34_minors']=witness
    proof.append(item)
    print(item,flush=True)

# Exact generic seed-kernel identity proves rank <=34 at EVERY parameter,
# including roots of the selected minor, because the coefficient of a^4 is 1.
T=sum(x*x for x in A);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=S.Poly(S.expand(T*T+4*((4-12*u/H)-1)*q*q+4*(B/H)*q*X),A)
fv=S.Matrix([F.coeff_monomial(mon) for mon in monomials])
assert all(S.cancel(x)==0 for x in E*fv)
z=S.symbols('z',real=True);beta=B/H;r=4-12*u/H
zstar=(r-1)/(3*beta*beta)
schur_det=(1-beta*beta*z)*(2*r-1-4*beta*beta+beta*beta*z)-4*beta**4*z*(1-z)
assert S.cancel(schur_det-3*beta**4*(z-zstar)**2)==0
assert S.expand(B*B-(1-4*u+3*u*u)*H-4*u*(3*u*u-3*u+1))==0
from sympy.polys.matrices import DomainMatrix
scaledF=S.expand(H*T*T+4*(3*H-12*u)*q*q+4*B*q*X)
HR=S.hessian(scaledF,A).subs({a:1,b:t,c:0,d:0})
detHR=DomainMatrix.from_Matrix(HR).convert_to(S.QQ.poly_ring(u,t)).det().as_expr()
rawmod=B*B*(1-t*t)**2-(1-4*u+3*u*u)*H*(1+t*t)**2
assert S.expand(detHR-2304*rawmod**2)==0

out={'interval':'0 < u < 1/3','global_matrix_denominator':str(global_den),
     'kernel_clear_denominator':str(den),
     'exact_generic_kernel_identity':True,
     'exact_rank_one_convexity_schur_square_identity':True,
     'exact_acoustic_hessian_determinant_identity':True,
     'selected_minor_identity_source':'generic_face_result.json',
     'all_irreducible_factors':proof,
     'conclusion':'Rank is exactly 34 throughout 0<u<1/3. Every upper-curved-boundary quartic is an exposed ray of the full homogeneous quartic rank-one-convex cone.',
     'seconds':time.time()-start}
(HERE/'curve_rank_result.json').write_text(json.dumps(out,indent=2)+'\n')
print('all-curve rank proof complete',time.time()-start,flush=True)
