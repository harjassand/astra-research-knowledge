#!/usr/bin/env python3
"""Direct symbolic reconstruction for the FY source mathematical audit.

Reads no producer verifier, certificate JSON, discovery script, or other worker
result. All polynomial inputs are defined below. Universal cone closure,
contact completeness, sign arguments and the LMI obstruction are in PROOFS.md.
"""
from pathlib import Path
import hashlib
import json
import platform
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
checks = []

def zero(name, expression):
    entries = list(expression) if isinstance(expression, S.MatrixBase) else [expression]
    residuals = [S.factor(e) for e in entries]
    assert all(e == 0 for e in residuals), (name, residuals)
    checks.append(name)

def fact(name, condition):
    assert condition, name
    checks.append(name)

a, b, c, d, n, m, r, t, k, lam = S.symbols('a b c d n m r t k lambda', real=True)
al, be, ga, de = S.symbols('alpha beta gamma delta', real=True)
x = S.Matrix([a, b, c, d])
u, v, w, j = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
H = ((a-d)**2+(b+c)**2)**2
zero('invariant relation', u*v-w*w-j*j)
zero('distortion identity', H-(u+v-2*j)**2)
basis = [u*u, v*v, u*v, w*w, u*w, v*w, j*u, j*v, j*w]
polys = [S.Poly(z, *x) for z in basis]
monomials = sorted({e for p in polys for e in p.monoms()})
fact('nine displayed invariant quartics are independent',
     S.Matrix([[p.coeff_monomial(e) for p in polys] for e in monomials]).rank() == 9)

coeff = S.symbols('p0:9', real=True)
general = sum(p*z for p, z in zip(coeff, basis))
eta1, eta2, xi1, xi2 = S.symbols('eta1 eta2 xi1 xi2', real=True)
rankone = S.Matrix([eta1*xi1, eta1*xi2, eta2*xi1, eta2*xi2])
LH = (rankone.T*S.hessian(general, x)*rankone)[0]
contact = {a:1, b:0, c:0, d:1, eta1:1, eta2:0, xi1:0, xi2:1}
equations = [LH.subs(contact)] + [S.diff(LH,z).subs(contact)
              for z in [*x, eta1, eta2, xi1, xi2]]
constraint_matrix, _ = S.linear_eq_to_matrix(equations, coeff)
fact('first acoustic contact and derivatives impose exactly five equations',
     constraint_matrix.rank() == 5)
expected = (coeff[0], -coeff[7]/4, -coeff[3]-coeff[7]/2,
            coeff[3], 0, 0, coeff[6], coeff[7], 0)
fact('first contact linear solution has four free coefficients',
     S.linsolve(equations, coeff) == S.FiniteSet(expected))
face_map = dict(zip(coeff, [al+be, al, 6*al+ga, -4*al-ga, 0, 0,
                           -4*al+de, -4*al, 0]))
F = al*H+be*u*u+ga*j*j+de*u*j
zero('four-coefficient contact span parametrization', general.subs(face_map)-F)
direction = S.Matrix([n, m, 0, 0])
acoustic_half = S.expand((direction.T*S.hessian(F,x)*direction)[0]/2)
acoustic_matrix = (S.hessian(acoustic_half,x)/2).applyfunc(S.factor)
zero('derived acoustic matrix reconstructs the polynomial',
     acoustic_half-(x.T*acoustic_matrix*x)[0])

P = S.Matrix([[6*be+de,de],[de,ga]])
Q = S.Matrix([[8*al,de],[de,2*be+de]])
zero('first necessary LMI tangent identity',
     acoustic_half.subs({a:1,b:-k*t,c:k*t,d:1,n:t,m:1})
     -t*t*(6*be+de+2*de*(1-k)+ga*(1-k)**2)-t**4*k*k*(2*be+de))
X,Y = S.symbols('X Y', real=True)
zero('second necessary LMI direct acoustic slice',
     acoustic_half.subs({a:0,b:X-Y,c:Y,d:0,n:1,m:0})
     -(S.Matrix([[X/2,-Y]])*Q*S.Matrix([X/2,-Y]))[0])
zero('determinant of the bc acoustic block in the supplied normalization',
     (2*acoustic_matrix.subs({n:1,m:0})).extract([1,2],[1,2]).det()
     -(8*al*(2*be+de)-de*de))

sharp = {al:3*r/(8*(r+2)), be:r*(r-1)/6, ga:1, de:r}
J = S.factor(F.subs(sharp))
M = acoustic_matrix.subs(sharp).applyfunc(S.factor)
minor_formulas = [
    r*((2*r+1)**2*n*n+3*m*m)/(4*(r+2)),
    3*r*r*(((2*r+1)*n*n-3*m*m)**2+12*r*(r+2)*n*n*m*m)/(16*(r+2)**2),
    3*m*m*r*r*(((r+1)*(2*r+1)*n*n-3*m*m)**2
        +3*r*(5*r+4)*n*n*m*m)/(16*(r+2)**2),
    9*r**4*n**4*m**4/16,
]
for order, formula in enumerate(minor_formulas,1):
    zero(f'half-acoustic leading minor of order {order}',
         M[:order,:order].det(method='domain-ge')-formula)
zero('full acoustic determinant fixes the factor sixteen convention',
     (2*M).det(method='domain-ge')-9*r**4*n**4*m**4)

Id = S.Matrix([1,0,0,1])
Ar = S.Matrix([0,(2*r+1)/3,1,0])
M_n0, M_m0 = M.subs({n:0,m:1}), M.subs({n:1,m:0})
zero('n=0 acoustic null vector', M_n0*Id)
zero('m=0 acoustic null vector', M_m0*Ar)
zero('n=0 ad block is a nonnegative square',
     M_n0.extract([0,3],[0,3])-3*r*S.Matrix([[1,-1],[-1,1]])/(4*(r+2)))
zero('n=0 bc block determinant is strictly positive on both branches',
     M_n0.extract([1,2],[1,2]).det()-9*r/(4*(r+2)))
zero('m=0 bc block is a nonnegative square',
     M_m0.extract([1,2],[1,2])
     -r*S.Matrix([3,-2*r-1])*S.Matrix([[3,-2*r-1]])/(12*(r+2)))
zero('m=0 ad block determinant is strictly positive on both branches',
     M_m0.extract([0,3],[0,3]).det()-r*(2*r+1)**2/(4*(r+2)))
zero('second contact determinant',
     S.Matrix([[Ar[0],Ar[1]],[Ar[2],Ar[3]]]).det()+(2*r+1)/3)

positive = S.symbols('positive', positive=True)
for branch in [positive,-2-positive]:
    for value in [r/(r+2),r*(r+2),r*(5*r+4),(2*r+1)**2]:
        fact(f'exact sign on branch r={branch}: {value}',
             S.factor(value.subs(r,branch)).is_positive is True)

ell_r = 2*acoustic_half.subs({a:0,b:(2*r+1)/3,c:1,d:0,n:1,m:0})
z = S.Matrix([r+2,-3])
zero('second contact equals second LMI kernel functional',
     ell_r-S.Rational(2,9)*(z.T*Q*z)[0])
kernel_solution = S.solve(list(Q*z), [al,be],dict=True)[0]
zero('second contact imposes exact alpha constraint',
     kernel_solution[al]-3*de/(8*(r+2)))
zero('second contact imposes exact beta constraint',
     kernel_solution[be]-de*(r-1)/6)
scale, remainder = S.symbols('scale remainder', real=True)
exposed_map = {al:scale*sharp[al],be:scale*sharp[be],ga:scale+remainder,de:scale*r}
zero('two-contact exposed-face decomposition',
     F.subs(exposed_map)-scale*J-remainder*j*j)
zero('first LMI determinant on the two-contact face',
     P.subs(exposed_map).det()-scale*remainder*r*r)
zero('determinant square acoustic evaluation',
     (direction.T*S.hessian(j*j,x)*direction)[0]-2*(d*n-c*m)**2)
zero('determinant square vanishes at the first contact',
     (d*n-c*m).subs({a:1,b:0,c:0,d:1,n:0,m:1}))
zero('determinant square vanishes at the second contact',
     (d*n-c*m).subs({a:0,b:(2*r+1)/3,c:1,d:0,n:1,m:0}))

# Unrestricted polyconvex supporting-plane necessary condition.
I_values = {a:1,b:0,c:0,d:1}
HF_I = S.hessian(F,x).subs({be:r*(r-1)/6,ga:1,de:r}).subs(I_values)
Hdet_I = S.hessian(j,x).subs(I_values)
zero('contact forces determinant support multiplier independently of alpha',
     (HF_I-lam*Hdet_I)[1,2]-(lam-r-2))
zero('forced support Hessian null direction independently of alpha',
     (HF_I-(r+2)*Hdet_I)*S.Matrix([1,0,0,-r-1]))
curved = F.subs({be:r*(r-1)/6,ga:1,de:r})
grad_I = S.Matrix([S.diff(curved,z).subs(I_values) for z in x])
gap = curved-curved.subs(I_values)-(grad_I.T*(x-Id))[0]-(r+2)*(j-1-(a+d-2))
zero('all-finite-alpha polyconvex support residual',
     gap.subs({a:1+t,b:0,c:0,d:1-(r+1)*t})
     +r*(r+2)*t**3/3-(al*(r+2)**4+(r+2)*(r+3)/6)*t**4)

# Lift blocks reconstructed by direct differentiation, without reading arrays.
M11 = S.hessian(S.diff(general,a,2),x)/2
M12 = S.hessian(S.diff(general,a,b),x)/2
M22 = S.hessian(S.diff(general,b,2),x)/2
zero('full nine-coefficient acoustic lift polynomial',
     LH.subs({eta1:1,eta2:0,xi1:n,xi2:m})
     -(x.T*(n*n*M11+2*n*m*M12+m*m*M22)*x)[0])
skew_symbols = S.symbols('k0:6',real=True)
K = S.zeros(4)
idx = 0
for i in range(4):
    for kidx in range(i+1,4):
        K[i,kidx],K[kidx,i] = skew_symbols[idx],-skew_symbols[idx]
        idx += 1
lift = M11.row_join(M12+K).col_join((M12-K).row_join(M22))
nx_mx = (n*x).col_join(m*x)
zero('six skew variables vanish on acoustic vectors',
     (nx_mx.T*lift*nx_mx)[0]-LH.subs({eta1:1,eta2:0,xi1:n,xi2:m}))

report = {
    'schema':'astra-fy-independent-symbolic-audit-v1',
    'status':'EXACT_IDENTITIES_PASS', 'check_count':len(checks), 'checks':checks,
    'python':sys.version, 'sympy':S.__version__, 'platform':platform.platform(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'full_acoustic_normalization':'D2J=x^T(2M)x; det(2M)=9r^4n^4m^4',
    'not_established_by_this_script':[
        'analytic dual-cone closure or LMI exposed-face theorem',
        'quasiconvexity or all-background heat certificate',
        'historical originality or external mathematical review',
        'replay of the absent supplied ZIP or its producer verifier'],
    'derived_matrices':{
        'half_acoustic_J':str(M),'n_zero':str(M_n0),'m_zero':str(M_m0),
        'nine_coefficient_M11':str(M11),'nine_coefficient_M12':str(M12),
        'nine_coefficient_M22':str(M22)}
}
(HERE/'EXACT_ALGEBRA_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='derived_matrices'},indent=2))
