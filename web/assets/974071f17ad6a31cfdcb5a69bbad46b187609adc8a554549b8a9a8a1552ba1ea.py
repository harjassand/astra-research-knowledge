"""Owned exact fixtures; finite checks do not validate the all-N proof."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import json
import time
import sympy as S

start=time.perf_counter()
checks={}
mx,my,mz=S.symbols('mx my mz', real=True)
m=S.Matrix([mx,my,mz])
pauli=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.Matrix([[1,0],[0,-1]])]
rho=(S.eye(2)+sum((m[i]*pauli[i] for i in range(3)),S.zeros(2)))/2
axes=[S.Matrix([1,0,0]),S.Matrix([S.Rational(3,5),S.Rational(4,5),0]),S.Matrix([S.Rational(1,3),S.Rational(2,3),S.Rational(2,3)])]
def kron(items):
    result=S.Matrix([[1]])
    for x in items: result=S.kronecker_product(result,x)
    return result
def zero(M):
    return all(S.expand(x)==0 for x in M)
for n in [1,2,3]:
    kernel=kron([rho]*n)
    Js=[sum((kron([pauli[i]/2 if j==site else S.eye(2) for j in range(n)]) for site in range(n)),S.zeros(2**n)) for i in range(3)]
    for axisid,axis in enumerate(axes):
        operator=sum((axis[i]*Js[i] for i in range(3)),S.zeros(2**n))
        u=axis.dot(m)
        v=axis-u*m
        r=axis.cross(m)
        def bop(X): return n*u*X+sum((v[i]*X.diff(m[i]) for i in range(3)),S.zeros(2**n))
        def rop(X): return sum((r[i]*X.diff(m[i]) for i in range(3)),S.zeros(2**n))
        checks[f'filter_identity_N{n}_axis{axisid}']=zero(bop(kernel)-(operator*kernel+kernel*operator))
        checks[f'rotation_identity_N{n}_axis{axisid}']=zero(S.I*rop(kernel)-(operator*kernel-kernel*operator))
        checks[f'quadratic_sandwich_N{n}_axis{axisid}']=zero(bop(bop(kernel))-rop(rop(kernel))-2*(operator*operator*kernel+kernel*operator*operator))

d,N=S.symbols('d N', positive=True)
z=S.Matrix(S.symbols('z0:3'))
gamma=1-(N+1)*d/2
center=d*N*m/gamma
raw=-z.dot(z)/(4*d)+(N+1)*z.dot(z)/8+N*m.dot(z)/2
completed=-gamma*(z-center).dot(z-center)/(4*d)+d*N*N*m.dot(m)/(4*gamma)
checks['three_dimensional_gaussian_completion']=S.simplify(raw-completed)==0
j=S.symbols('j',nonnegative=True)
checks['heat_character_eigenvalue']=S.expand(((2*j+1)**2-1)/4-j*(j+1))==0
f=S.symbols('f',positive=True)
checks['young_field_bound']=S.expand(f*f/(4*d)+d*j*j-f*j-(S.sqrt(d)*j-f/(2*S.sqrt(d)))**2)==0

# Exact powers separate the old and new admitted growing regions:
# N=q^20,R=q^4,B=q^8; old ratios diverge as q^2 and q,
# new ratios vanish as q^-2 and q^-1. A very large mathematical N
# is handled only as exact integer/rational scalars, never as a quantum matrix.
q=10**6
R=q**4
n=q**20
bound=q**8
L=2*R-1
u=q**5
g=1-F((n+1)*(L+u),2*q**30)
aa=F((L+u)*q**10,4)/g
r02=F(1,32*R)
checks['growth_new_anisotropy_ratio_q_inverse2']=F(R*R,q**10)==F(1,q*q)
checks['growth_old_anisotropy_ratio_q2']=F(R**3,q**10)==q*q
checks['growth_new_field_ratio_q_inverse1']=F(bound*q**6,q**15)==F(1,q)
checks['growth_old_field_ratio_q1']=F(bound*R*R,q**15)==q
checks['threshold_gamma_positive']=g>0
checks['threshold_weighted_small_tail_using_a0_ge_r0']=aa<=F(n,384)*r02
checks['threshold_drift_using_sqrt2_le_3_over2']=F(L,2*q**10)+F(3,q**5)<=F(1,8)
checks['young_logweight_ratio_exact']=F(bound*bound,4*u)*F(R*R,n)==F(1,4*q)

# Exact rational demonstration delta=1/2-logcosh1>1/100:
# cosh1 upper Taylor remainder is bounded geometrically;
# exp(.49) exceeds it already at degree3.
cosh_partial=sum((F(1,factorial(2*k)) for k in range(6)),F(0))
cosh_upper=cosh_partial+F(1,factorial(12))/(1-F(1,13*14))
exp_lower=sum((F(49,100)**k/F(factorial(k)) for k in range(4)),F(0))
checks['delta_greater_than_1_over100_rational_certificate']=cosh_upper<exp_lower
checks['threshold_weighted_outer_tail_using_delta_gt_01']=aa<=F(n,800)
checks['threshold_N_delta_ge2_using_delta_gt_01']=n>=200
checks['threshold_seed_normalizer']=n>=R*R

out={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
     'num_checks':len(checks),'runtime_seconds':time.perf_counter()-start,
     'sympy_version':S.__version__,
     'growth_fixture':{'N':'q^20','R':'q^4','B':'q^8','q':q,'new_region':'ratios q^-2,q^-1','old_region':'ratios q^2,q'},
     'scope':'Exact small-N filter/rotation/sandwich identities, scalar Gaussian/character algebra and explicit growing-threshold fixtures only. All-N analytic tail/stochastic proof, implementation, entropy, novelty and hardware remain separately assessed.'}
Path(__file__).with_name('growing_diffusion_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values())
