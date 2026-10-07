"""Independent small parity and white-mass checks; no peer imports."""
import json
import time
from itertools import product
from pathlib import Path
import sympy as s
start=time.perf_counter();checks={}
def kron(xs):
    out=s.Matrix([[1]])
    for x in xs:out=s.kronecker_product(out,x)
    return out
def zero(M):return all(s.simplify(x)==0 for x in M)
cases=[(2,1,[0]),(2,2,[0,1]),(2,3,[0,2]),(3,2,[0,1]),(3,3,[0,1,2])]
for d,N,active in cases:
    A=s.zeros(d);A[0,0]=1/s.sqrt(2);A[1,1]=-1/s.sqrt(2)
    m=len(active);D=d**N
    base=s.eye(D)/D
    tensor=kron([A if i in active else s.eye(d) for i in range(N)])
    for sign in [-1,1]:
        state=s.zeros(D)
        for signs in product([-1,1],repeat=m):
            if s.prod(signs)!=sign:continue
            local=[]
            for i in range(N):
                local.append((s.eye(d)+signs[active.index(i)]*A)/d if i in active else s.eye(d)/d)
            state+=kron(local)/2**(m-1)
        checks[f'parity_vertex_d{d}_N{N}_m{m}_sign{sign}']=zero(state-base-sign*tensor/D)
    Bnu=kron([A if i in active else s.eye(d)/s.sqrt(d) for i in range(N)])
    checks[f'tensor_normalization_d{d}_N{N}_m{m}']=zero(tensor/D-d**(-s.Rational(N+m,2))*Bnu)

# Exact white component, with an explicit product-mixture remainder.
d,N=3,3
eta=s.Rational(1,12)
rho=s.diag(s.Rational(1,6),s.Rational(1,3),s.Rational(1,2))
white=d*eta
rhop=(rho-eta*s.eye(d))/(1-white)
full=kron([rho]*N)
remainder=s.zeros(d**N)
for choices in product([0,1],repeat=N):
    if not any(choices):continue
    prob=s.prod([1-white if x else white for x in choices])
    remainder+=prob*kron([rhop if x else s.eye(d)/d for x in choices])
checks['white_mass_expansion']=zero(full-white**N*s.eye(d**N)/d**N-remainder)
checks['white_remainder_trace']=s.trace(remainder)==1-white**N
checks['absorption_threshold']=white**N*s.Rational(d)**(-2*N)==(eta/d)**N

# Removing white mass need not preserve the cone of IID mixtures.
# This fully separable diagonal remainder has negative identical-observable
# covariance; every IID mixture would have a nonnegative variance.
rho=s.diag(s.Rational(3,4),s.Rational(1,4));eta=s.Rational(1,8);w=(2*eta)**2
tau=(s.kronecker_product(rho,rho)-w*s.eye(4)/4)/(1-w)
sz=s.diag(1,-1)
mean=s.trace(tau*s.kronecker_product(sz,s.eye(2)))
pair=s.trace(tau*s.kronecker_product(sz,sz))
checks['white_remainder_not_iid_covariance']=pair-mean**2==-s.Rational(4,225)
checks['white_remainder_is_diagonal_positive']=all(x>0 for x in tau.diagonal()) and zero(tau-s.diag(*tau.diagonal()))

a,q=s.symbols('a q',positive=True)
L=(a+s.sqrt(a*a+4*a*q))/2+1
checks['all_N_absorption_root_slack']=s.simplify(L*L-a*(L+q)-s.sqrt(a*a+4*a*q)-1)==0
out={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'num_checks':len(checks),
     'runtime_seconds':time.perf_counter()-start,'sympy_version':s.__version__,
     'scope':'Finite exact parity/tensor normalization, white-mass product expansion, explicit non-IID remainder and scalar absorption slack. Analytic all-N theorem, sampler, actual Gibbs decomposition acquisition and priority are separate.'}
Path(__file__).with_name('ball_absorption_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert all(checks.values())
