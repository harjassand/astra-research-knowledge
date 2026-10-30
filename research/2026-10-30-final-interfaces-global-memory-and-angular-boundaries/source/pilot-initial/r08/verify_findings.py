"""Replay the exact mathematical findings. Requires SymPy.

python3 verify_findings.py --full-minors

The full option recomputes both 34x34 polynomial determinants (minutes).
Without it, the stored determinants' common-root exclusion and all other
identities are checked, but those determinant identities are not replayed.
"""
from pathlib import Path
import argparse
import json
import time
import sympy as s
from sympy.polys.matrices import DomainMatrix

OUT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--full-minors',action='store_true')
args=parser.parse_args()
start=time.perf_counter()
a,b,c,d,t,x,y,tau=s.symbols('a b c d t x y tau')
av=(a,b,c,d)
powers=[(i,j,k,4-i-j-k) for i in range(5) for j in range(5-i)
        for k in range(5-i-j)]
monomials=[s.prod(z**e for z,e in zip(av,pw)) for pw in powers]
H=1+3*tau*tau;B=1-3*tau*tau
beta=B/H;r=4-12*tau/H;St=1+t*t;Xt=1-t*t
m=B*B*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2
AA=s.diag(3*St,St)
BB=beta*s.Matrix([[0,3*Xt],[-Xt,-4*t]])
DD=s.diag(St,(2*r-1)*St)
Schur=DD-BB.T*AA.inv()*BB
assert s.cancel(Schur[0,0]-4*(t*t+3*tau*tau)*(3*t*t*tau*tau+1)/(St*H*H))==0
assert s.cancel(Schur.det()-3*m*m/(St*St*H**4))==0
assert s.expand(B*B-(1-4*tau+3*tau*tau)*H-4*tau*(3*tau*tau-3*tau+1))==0
print('Exact rank-one-convex Schur factorization checked.',flush=True)

domain=s.QQ.frac_field(tau)
mp=s.Poly(m,t,domain=domain).monic()
K=s.Matrix([
    -B*(tau*(1-t*t)+H*t*t)*(1+t*t),
    B*t*(H-tau*(1-t*t))*(1+t*t),
    B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
    B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2,
]).applyfunc(lambda z:s.Poly(z,t,domain=domain).rem(mp).as_expr())
Ku=s.Matrix([x*K[0]-y*K[2],x*K[1]-y*K[3],
             y*K[0]+x*K[2],y*K[1]+x*K[3]])
R=dict(zip(av,(x,x*t,y,y*t)))
columns=[]
for mon in monomials:
    vector=s.hessian(mon,av).subs(R,simultaneous=True)*Ku
    column=[]
    for v in vector:
        poly=s.Poly(s.expand(v),x,y)
        for ix in range(4):
            rem=s.Poly(poly.coeff_monomial(x**ix*y**(3-ix)),t,domain=domain).rem(mp)
            column.extend(rem.nth(j) for j in range(4))
    columns.append(column)
L=s.Matrix.hstack(*[s.Matrix(v) for v in columns])
T=sum(z*z for z in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=s.Poly(s.expand(T*T+4*(r-1)*q*q+4*beta*q*X),*av)
O=s.Matrix([[1,-t],[t,1]])
O4=s.diag(O,O)
actual_hessian=s.hessian(F.as_expr(),av).subs({a:1,b:t,c:0,d:0})
candidate=AA.row_join(BB).col_join(BB.T.row_join(DD))
assert all(s.cancel(z)==0 for z in O4.T*actual_hessian*O4-4*St*candidate)
fv=s.Matrix([F.coeff_monomial(mon) for mon in monomials])
assert all(s.cancel(v)==0 for v in L*fv)
print('Full 64 by 35 matrix reconstructed; generic acoustic kernel checked.',flush=True)

for value in (s.Rational(1,6),s.Rational(1,30)):
    label=f'{value.p}_{value.q}'
    seed=json.loads((OUT/f'face_{label}.json').read_text())
    exact=L.subs(tau,value)
    assert exact==s.Matrix([[s.Rational(z) for z in row] for row in seed['constraint_matrix']])
    assert exact.rank()==34
    ee=json.loads((OUT/f'exposing_{label}.json').read_text())
    ell=s.Matrix([s.Integer(z) for z in ee['integer_exposing_functional']])
    scale=s.Rational(ee['scale_from_raw_sum'])
    assert scale>0
    point_mp=s.Poly(mp.as_expr().subs(tau,value),t)
    point_K=K.subs(tau,value)
    trace_t2=-2*point_mp.nth(2)
    rebuilt=[]
    for mon in monomials:
        result=0
        for xx,yy in ((1,0),(0,1),(1,1),(1,-1)):
            kk=s.Matrix([xx*point_K[0]-yy*point_K[2],xx*point_K[1]-yy*point_K[3],
                         yy*point_K[0]+xx*point_K[2],yy*point_K[1]+xx*point_K[3]])
            hh=s.hessian(mon,av).subs(dict(zip(av,(xx,xx*t,yy,yy*t))),simultaneous=True)
            rem=s.Poly(s.rem(s.expand((kk.T*hh*kk)[0]),point_mp.as_expr(),t),t)
            result+=4*rem.nth(0)+trace_t2*rem.nth(2)
        rebuilt.append(s.cancel(scale*result))
    assert s.Matrix(rebuilt)==ell
    assert (ell.T*fv.subs(tau,value))[0]==0
    print(f'Exact seed face and rational exposing functional checked at tau={value}.',flush=True)

def expr(raw):
    return s.sympify(raw,locals={'tau':tau})

def open_roots(poly):
    pp=s.Poly(poly,tau).sqf_part()
    return int(pp.count_roots(0,s.Rational(1,3)))-int(pp.eval(0)==0)-int(pp.eval(s.Rational(1,3))==0)

records=[json.loads((OUT/name).read_text()) for name in
         ('generic_face_result.json','generic_face_exception_result.json')]
determinants=[]
for index,record in enumerate(records):
    expected=s.Poly(expr(record['cleared_minor_determinant']),tau)
    determinants.append(expected)
    for denominator in record['row_denominators']:
        assert open_roots(expr(denominator))==0
    if args.full_minors:
        minor=L.extract(record['minor_rows'],record['minor_columns'])
        for i,denominator in enumerate(record['row_denominators']):
            den=expr(denominator)
            for j in range(minor.cols):
                minor[i,j]=s.cancel(minor[i,j]*den)
                assert s.denom(minor[i,j])==1
        actual=DomainMatrix.from_Matrix(minor).convert_to(s.QQ.poly_ring(tau)).det().as_expr()
        assert s.Poly(actual,tau)==expected
        print(f'Exact polynomial determinant {index+1}/2 recomputed.',flush=True)

gcd=s.gcd(*determinants).monic()
expected_gcd=tau**9*(3*tau*tau-1)**52*(3*tau*tau+1)**9*(3*tau*tau-3*tau+1)**9*(3*tau*tau-2*tau+1)**3
assert gcd==s.Poly(expected_gcd,tau).monic()
for factor,_ in s.factor_list(gcd.as_expr(),tau)[1]:
    assert open_roots(factor)==0
print('Two-minor common zeros and all denominator zeros excluded on 0<tau<1/3.',flush=True)

# Reconstruct the unrestricted infinitesimal stabilizer as a separate
# eight-variable linear system.
uv=s.symbols('u0:8')
U=s.Matrix(2,2,uv[:4]);V=s.Matrix(2,2,uv[4:]);A=s.Matrix([[a,b],[c,d]])
delta=U*A+A*V
HF=s.expand(H*T*T+4*(3*H-12*tau)*q*q+4*B*q*X)
co=s.Poly(s.expand(sum(s.diff(HF,z)*w for z,w in zip(av,list(delta)))),*av).coeffs()
stab=s.linear_eq_to_matrix(co,uv)[0]
sr=json.loads((OUT/'stabilizer_result.json').read_text())
assert s.factor(stab.extract(sr['minor_rows'],sr['minor_columns']).det())==expr(sr['minor_determinant'])
assert expr(sr['minor_determinant'])==16384*(3*tau*tau-1)**2*(3*tau*tau+1)**4
for vec in sr['basis']:
    assert stab*s.Matrix([s.Integer(v) for v in vec])==s.zeros(stab.rows,1)
print('Exact stabilizer dimension and invariant-pullback obstruction checked.',flush=True)
print(json.dumps({'full_polynomial_determinants_recomputed':args.full_minors,
    'rank_one_convexity_and_acoustic_constraints':True,
    'full_branch_exposed_extreme_ray_certificate':True,
    'seed_exposing_functionals':True,
    'invariant_pullback_obstruction':True,
    'seconds':time.perf_counter()-start},indent=2),flush=True)
