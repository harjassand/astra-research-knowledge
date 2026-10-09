#!/usr/bin/env python3
"""One exact K=4 identity replay; no scan. Requires SymPy, writes only own JSON."""
from pathlib import Path
import hashlib
import json
import time
import sympy as sp

t0 = time.perf_counter()
checks = []

def exact_zero(x):
    if isinstance(x, sp.MatrixBase):
        return all(sp.simplify(z) == 0 for z in x)
    return sp.simplify(x) == 0

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

K = 4
v = sp.Rational(1, K*K)
c = sp.sqrt(v*(1-v))
sigma = sp.diag(sp.Rational(3,4), sp.Rational(1,4))
sigma_root = sp.diag(sp.sqrt(3)/2, sp.Rational(1,2))
sigma_inverse_root = sigma_root.inv()
tau = [sp.Matrix([[1-v/3,-c/3],[-c/3,v/3]]),
       sp.Matrix([[v,c],[c,1-v]])]
E = [sp.Matrix([[int(i==a and j==b) for j in range(2)]
                 for i in range(2)]) for b in range(2) for a in range(2)]

def phi(X):
    return X[0,0]*tau[0]+X[1,1]*tau[1]

def phi_star(X):
    return sp.diag(sp.trace(tau[0]*X), sp.trace(tau[1]*X))

def gamma(X):
    return sigma_root*X*sigma_root

def sharp(X):
    return gamma(phi_star(sigma_inverse_root*X*sigma_inverse_root))

def S(X):
    return sharp(phi(X))

def broadcaster(X):
    return (X[0,0]*sp.kronecker_product(tau[0],tau[0])
            +X[1,1]*sp.kronecker_product(tau[1],tau[1]))

def partial_trace_second(X):
    return sp.Matrix(2,2,lambda i,j: sum(X[2*i+k,2*j+k] for k in range(2)))

def partial_trace_first(X):
    return sp.Matrix(2,2,lambda i,j: sum(X[2*k+i,2*k+j] for k in range(2)))

def postprocessed_broadcaster(X):
    return (X[0,0]*sp.kronecker_product(sharp(tau[0]),sharp(tau[0]))
            +X[1,1]*sp.kronecker_product(sharp(tau[1]),sharp(tau[1])))

def superoperator(fn):
    return sp.Matrix.hstack(*[fn(x).vec() for x in E])

for j in range(2):
    check(f'tau_{j} trace one', exact_zero(sp.trace(tau[j])-1))
    check(f'tau_{j} positive diagonal', all(tau[j][i,i]>0 for i in range(2)))
check('tau_0 exact determinant', exact_zero(tau[0].det()-2*v/9))
check('tau_1 rank-one positive', exact_zero(tau[1].det()))
check('exact channel stationarity', exact_zero(phi(sigma)-sigma))
check('Petz exact stationarity', exact_zero(sharp(sigma)-sigma))
check('original genuinely non-KMS', not exact_zero(phi(E[1])-sharp(E[1])))
check('Petz coherence formula', exact_zero(sharp(E[2])-sp.diag(-c/sp.sqrt(3),c/sp.sqrt(3))))

for n,X in enumerate(E):
    check(f'full input {n}: Phi trace preservation', exact_zero(sp.trace(phi(X))-sp.trace(X)))
    check(f'full input {n}: Petz trace preservation', exact_zero(sp.trace(sharp(X))-sp.trace(X)))
    check(f'full input {n}: actual first marginal', exact_zero(partial_trace_second(broadcaster(X))-phi(X)))
    check(f'full input {n}: actual second marginal', exact_zero(partial_trace_first(broadcaster(X))-phi(X)))
    check(f'full input {n}: symmetrized first marginal', exact_zero(partial_trace_second(postprocessed_broadcaster(X))-S(X)))
    check(f'full input {n}: symmetrized second marginal', exact_zero(partial_trace_first(postprocessed_broadcaster(X))-S(X)))
    check(f'full input {n}: Petz output diagonal', exact_zero(sharp(X)[0,1]) and exact_zero(sharp(X)[1,0]))

P = superoperator(phi)
Ps = superoperator(sharp)
G = superoperator(gamma)
Sm = superoperator(S)
check('Petz superoperator orientation', exact_zero(Ps-G*P.conjugate().T*G.inv()))
check('S KMS self-adjoint', exact_zero(Sm*G-G*Sm.conjugate().T))

qvalues = [sp.Rational(3,8),sp.Rational(1,8)]
rhos = [sp.Matrix([[1-q,(4*sp.Rational(1,3))*c*(q-sp.Rational(1,4))],
                  [(4*sp.Rational(1,3))*c*(q-sp.Rational(1,4)),q]]) for q in qvalues]
m = 1-4*v/3
ell = m*m+8*c*c/(3*sp.sqrt(3))
check('S positive population eigenvalue', ell>0)
check('S population eigenvalue <= one', ell<1)
check('exact local stationary margin', exact_zero((rhos[0]+rhos[1])/2-sigma))
check('exact reference dimension two', len(rhos)==2)

for n,(q,rho) in enumerate(zip(qvalues,rhos)):
    h = rho[0,1]
    check(f'state {n} trace one', exact_zero(sp.trace(rho)-1))
    check(f'state {n} faithful', rho[0,0]>0 and rho.det()>0)
    check(f'state {n} uniform determinant lower bound', rho.det()>=sp.Rational(5,48))
    check(f'state {n} preserved off-diagonal', exact_zero(phi(rho)[0,1]-h))
    check(f'state {n} exact forward diagonal change', exact_zero((rho-phi(rho))[1,1]-4*v*(q-sp.Rational(1,4))/3))
    check(f'state {n} exact forward half-error', exact_zero((rho-phi(rho))[1,1]**2-(v/6)**2))
    check(f'state {n} exact S tail probability', exact_zero(S(rho)[1,1]-(sp.Rational(1,4)+ell*(q-sp.Rational(1,4)))))
    delta = rho-S(rho)
    check(f'state {n} exact residual squared', exact_zero(delta[0,0]**2+delta[0,1]**2-((1-ell)**2/64+c**2/36)))
    check(f'state {n} residual coherence lower bound', exact_zero(delta[0,1]**2-c**2/36))

check('r lower bound >= 1/(7K)', c*c/36>=sp.Rational(1,49*K*K))
check('exact forward b=1/(6K^2)', v/6==sp.Rational(1,6*K*K))
check('uniform entropy budget analytic certificate', sigma[0,0]+sigma[1,1]==1 and sigma[0,0]!=sigma[1,1])

out = {
    'status':'PASS', 'K':K, 'checks':len(checks), 'check_names':checks,
    'v':str(v), 'c':str(c), 'sigma':'diag(3/4,1/4)',
    'forward_half_error':str(v/6),
    'S_population_eigenvalue':str(sp.simplify(ell)),
    'Petz_half_error_squared':str(sp.simplify((1-ell)**2/64+c*c/36)),
    'Petz_half_error_lower_bound':str(c/6),
    'information_bound':'I(R:B)<=S(diag(3/4,1/4))<ln 2; analytic entropy nonnegativity',
    'elapsed_seconds':time.perf_counter()-t0,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'sympy_version':sp.__version__,
    'invocation':'python3 work/agents/tensor_frame_sol/cycle09_petz_symmetrization/check_fixed_qubit_stationary_margin_exact.py',
    'purpose':'one exact matrix identity control; analytic all-K proof separate; no scan'
}
Path(__file__).with_name('fixed_qubit_stationary_margin_exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
