"""Reproducible diagnostics for the strain-history estimates.

These floating-point tests are not a formal verification of the theorems.
The optional symbolic calculation proves an exact identity in one example,
not the PDE theorem.  Requires Python 3.10+, NumPy, SciPy, and SymPy.
Run: python verify.py
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from scipy.integrate import quad
from scipy.linalg import expm, expm_frechet
import scipy
import sympy as sp

Array = NDArray[np.float64]
SEED = 20261012


def comm(a: Array, b: Array) -> Array:
    return a @ b - b @ a


def sym(a: Array) -> Array:
    return (a + a.T) / 2


def op(a: Array) -> float:
    return float(np.linalg.norm(a, 2))


def width(b: Array) -> float:
    eig = np.linalg.eigvalsh(b)
    return float(eig[-1] - eig[0])


def cfun(r: float) -> float:
    """(r cosh(r)-sinh(r))/r^3, evaluated stably near zero."""
    if r < 1e-3:
        return 1/3 + r*r/30 + r**4/840 + r**6/45360
    return (r*math.cosh(r) - math.sinh(r)) / r**3


def afun(r: float) -> float:
    return float(np.expm1(r)/r) if r > 1e-7 else 1+r/2+r*r/6+r**3/24


def hfun(r: float) -> float:
    """2 integral_0^1 s exp(rs) ds."""
    if r < 1e-3:
        return 1 + 2*r/3 + r*r/4 + r**3/15 + r**4/72
    return 2*((r-1)*math.exp(r)+1)/r**2


def second_exp(b: Array, c: Array) -> Array:
    """D^2 exp_B[C,C] via an upper-triangular block exponential."""
    n = b.shape[0]
    block = np.zeros((3*n, 3*n))
    for j in range(3):
        block[j*n:(j+1)*n, j*n:(j+1)*n] = b
    block[:n, n:2*n] = c
    block[n:2*n, 2*n:3*n] = c
    return 2*expm(block)[:n, 2*n:3*n]


def random_symmetric(rng: np.random.Generator, n: int, scale: float=1) -> Array:
    b = sym(rng.normal(size=(n, n)))
    b -= np.trace(b)/n*np.eye(n)
    return scale*b/max(op(b), 1e-15)


def run() -> dict:
    rng = np.random.default_rng(SEED)
    result = {
        'seed': SEED,
        'versions': {'numpy': np.__version__, 'scipy': scipy.__version__, 'sympy': sp.__version__},
        'status': 'diagnostics only; not independent review or formal proof',
    }
    max_identity_relerr = 0.
    max_local_ratio = 0.
    max_gamma_ratio = 0.
    max_theta_ratio = 0.
    min_parabolic_slack = math.inf
    min_energy_slack = math.inf
    ntests = 0
    for n in [2, 3, 5, 8]:
        for _ in range(30):
            b = random_symmetric(rng, n, float(rng.uniform(.001, 1.5)))
            s = random_symmetric(rng, n)
            r = width(b)
            em = expm(-b)
            base = em@s@expm(b)-em@expm_frechet(b, s, compute_expm=False)
            d, q = np.linalg.eigh(b)
            st = q.T@s@q
            gaps = d[:, None]-d[None, :]
            f = np.empty_like(gaps)
            small = np.abs(gaps)<1e-5
            f[small] = gaps[small]**2/3+gaps[small]**4/30
            f[~small] = np.cosh(gaps[~small])-np.sinh(gaps[~small])/gaps[~small]
            exact = q@(f*st)@q.T
            err = op(sym(base)-exact)/max(1., op(base))
            max_identity_relerr = max(max_identity_relerr, err)
            dd = op(comm(b, comm(b, s)))
            denom = cfun(r)*dd
            if denom > 1e-14:
                max_local_ratio = max(max_local_ratio, op(sym(base))/denom)
            # Check both pointwise parabolic inequalities on arbitrary first jets.
            y = rng.normal(size=n)
            nu = float(rng.uniform(.01, 1.))
            grads = [rng.normal(size=n) for _ in range(3)]
            cs = [random_symmetric(rng, n, float(rng.uniform(.1, 1.))) for _ in range(3)]
            gammas = [em@expm_frechet(b, c, compute_expm=False) for c in cs]
            thetas = [em@second_exp(b, c) for c in cs]
            for c, gamma, theta in zip(cs, gammas, thetas):
                max_gamma_ratio = max(max_gamma_ratio, op(gamma)/(afun(r)*op(c)))
                max_theta_ratio = max(max_theta_ratio, op(theta)/(hfun(r)*op(c)**2))
            lhs = 2*y@(base+nu*sum(thetas, np.zeros_like(b)))@y
            lhs += sum(4*nu*y@g@z-2*nu*z@z for g,z in zip(gammas, grads))
            gnorm = sum(op(c)**2 for c in cs)
            pot = cfun(r)*dd+nu*(hfun(r)+afun(r)**2)*gnorm
            pot_energy = cfun(r)*dd+nu*(hfun(r)+2*afun(r)**2)*gnorm
            rhs = 2*pot*(y@y)
            rhs_energy = 2*pot_energy*(y@y)
            norm = max(1., abs(lhs), rhs, rhs_energy)
            min_parabolic_slack = min(min_parabolic_slack, (rhs-lhs)/norm)
            energy_lhs = lhs+nu*sum(z@z for z in grads)
            min_energy_slack = min(min_energy_slack, (rhs_energy-energy_lhs)/norm)
            ntests += 1
    assert max_identity_relerr < 1e-10
    assert max_local_ratio < 1+1e-10
    assert max_gamma_ratio < 1+1e-10
    assert max_theta_ratio < 1+1e-10
    assert min_parabolic_slack > -1e-10
    assert min_energy_slack > -1e-10
    result['local_matrix_and_parabolic_tests'] = {
        'cases': ntests, 'matrix_dimensions': [2,3,5,8],
        'max_relative_identity_error': max_identity_relerr,
        'max_double_commutator_bound_ratio': max_local_ratio,
        'max_first_derivative_bound_ratio': max_gamma_ratio,
        'max_second_derivative_bound_ratio': max_theta_ratio,
        'min_scaled_maximum_principle_slack': min_parabolic_slack,
        'min_scaled_energy_inequality_slack': min_energy_slack,
    }
    # Equality in the pointwise commutator coefficient, with 2x2 matrices.
    A = np.diag([1., -1.])
    Z = np.array([[0.,1.],[1.,0.]])
    sharp = []
    for r in [.001,.01,.1,1.,3.]:
        b = r*A/2
        R = expm(-b)@Z@expm(b)-expm(-b)@expm_frechet(b,Z,compute_expm=False)
        ratio = op(sym(R))/(cfun(r)*op(comm(b,comm(b,Z))))
        assert abs(ratio-1) < 2e-8
        sharp.append({'width': r, 'attained_ratio': ratio})
    result['sharp_local_coefficient'] = sharp
    # Exact counterexample and numerical integrated growth certificate.
    word = [A,A,Z,-A,-Z,-A,Z,A,-Z,-A]
    pulse_results = []
    for eps in [.01,.03,.1,.2,.5]:
        U = np.eye(2)
        B = np.zeros((2,2))
        clock = 0.
        action = 0.
        maxb = 0.
        for X in reversed(word):
            S = eps*X
            def df(t: float) -> float:
                Bt = B+t*S
                return op(comm(Bt,comm(Bt,S)))
            action += quad(df, 0, 1, epsabs=1e-12)[0]
            clock += quad(lambda t:cfun(width(B+t*S))*df(t),0,1,epsabs=1e-12)[0]
            B += S
            U = expm(S)@U
            maxb = max(maxb,op(B))
        exact_logrho = 2*np.arcsinh(2*np.sinh(eps)**3*np.cosh(eps))
        actual_logrho = np.log(max(np.abs(np.linalg.eigvals(U))))
        lognorm = np.log(op(U))
        assert np.allclose(B,0,atol=1e-14)
        assert abs(np.linalg.det(U)-1) < 1e-10
        assert abs(actual_logrho-exact_logrho) < 1e-10
        assert lognorm <= clock+1e-10
        pulse_results.append({
            'epsilon':eps,'primitive_sup':maxb,'double_commutator_action':action,
            'growth_clock':clock,'log_operator_norm':float(lognorm),
            'log_spectral_radius':float(actual_logrho),
            'exact_log_spectral_radius':float(exact_logrho),
            'log_spectral_radius_over_epsilon_cubed':float(actual_logrho/eps**3),
        })
    result['ten_pulse_counterexample'] = pulse_results
    # Finite-time tensor comparison for nonzero final primitives.
    max_tensor_ratio = 0.
    trajectory_cases = 0
    for n in [2,3,5]:
        for _ in range(12):
            U = np.eye(n)
            B = np.zeros((n,n))
            clock = 0.
            for _step in range(8):
                S = random_symmetric(rng,n,float(rng.uniform(.05,.3)))
                dt = float(rng.uniform(.1,.5))
                def clock_integrand(t: float) -> float:
                    Bt = B+t*S
                    return cfun(width(Bt))*op(comm(Bt,comm(Bt,S)))
                clock += quad(clock_integrand,0,dt,epsabs=1e-11)[0]
                B += dt*S
                U = expm(dt*S)@U
            V = expm(-B)@U
            logsv = np.log(np.linalg.svd(V,compute_uv=False))
            deviation = float(np.max(np.abs(logsv)))
            assert deviation <= clock+1e-9
            max_tensor_ratio = max(max_tensor_ratio,deviation/max(clock,1e-15))
            trajectory_cases += 1
    result['nonzero_primitive_tensor_comparison'] = {
        'cases':trajectory_cases,
        'max_abs_log_singular_value_over_growth_clock':max_tensor_ratio,
    }
    # Symbolic, exact rational identity q=exp(epsilon).
    q = sp.symbols('q', positive=True)
    EA = sp.diag(q,1/q)
    EZ = sp.Matrix([[(q+1/q)/2,(q-1/q)/2],[(q-1/q)/2,(q+1/q)/2]])
    C = EA*EZ*EA.inv()*EZ.inv()
    D = sp.simplify(EA*C*EA.inv()*C.inv())
    trace_minus_two = sp.factor(sp.trace(D)-2)
    target = (q-1)**6*(q+1)**6*(q*q+1)**2/(16*q**8)
    assert sp.simplify(trace_minus_two-target)==0
    assert sp.simplify(D.det()-1)==0
    result['symbolic_counterexample'] = {'determinant':'1','trace_minus_2':str(trace_minus_two)}
    result['all_checks_passed'] = True
    return result


if __name__ == '__main__':
    payload = run()
    destination = Path(__file__).with_name('verification_results.json')
    destination.write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2))
