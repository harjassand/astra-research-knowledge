"""Value-only affine cloud channel and a separate joint Gaussian verifier.

The runtime receives a callable g, X, L,tau,S,epsilon. It never receives A,
theta, a derivative, or a mean. Tests use numpy from the primary runtime.
"""
import csv
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


class CountingOracle:
    def __init__(self, matrix, offset):
        self._matrix = matrix
        self._offset = offset
        self.calls = 0

    def __call__(self, value):
        self.calls += 1
        return self._matrix @ value + self._offset


def finite_order(dimension, q, epsilon):
    assert 0 < q < 1 and 0 < epsilon <= 0.5
    n = 0
    while q ** (2*n+2)/(1-q*q) > epsilon/(3*math.sqrt(dimension)):
        n += 1
    return n


def acquired_cloud(g, x, lipschitz, tau, noise, epsilon, w):
    dimension = len(x)
    q = tau*lipschitz/noise
    n = finite_order(dimension, q, epsilon)
    c = g(np.zeros(dimension))
    gx = g(x)
    power = np.array(w, copy=True)
    p_sum = np.array(w, copy=True)
    c_sum = np.zeros(dimension)
    b_coefficient = p_coefficient = 1.0
    for j in range(1, 2*n+2):
        power = (g(power)-c)/lipschitz
        if j % 2:
            c_sum += b_coefficient*power
        else:
            k = j//2
            b_coefficient *= (2*k-1)/(2*k)*q*q
            p_coefficient *= (k-1.5)/k*q*q
            p_sum += p_coefficient*power
    retained = x-(tau*tau*lipschitz/noise)*c_sum
    child = gx+noise*p_sum
    return retained, child, n


def scalar_polynomials(lambdas, n):
    p = np.ones_like(lambdas)
    b = np.ones_like(lambdas)
    pterm = np.ones_like(lambdas)
    bterm = np.ones_like(lambdas)
    for k in range(1, n+1):
        pterm *= (k-1.5)/k*lambdas*lambdas
        bterm *= (2*k-1)/(2*k)*lambdas*lambdas
        p += pterm
        b += bterm
    return p,b


def verify_joint_gaussian(lambdas, n):
    p,b = scalar_polynomials(lambdas,n)
    total_kl = 0.0
    max_covariance_error = 0.0
    for lam, pi, bi in zip(lambdas,p,b):
        actual_map = np.array([[1.,-lam*bi],[lam,pi]])
        whitening = np.diag([math.sqrt(1-lam*lam),1.])
        relative = whitening @ actual_map @ actual_map.T @ whitening
        delta = np.linalg.eigvalsh(relative)-1
        assert np.min(delta)>-1
        total_kl += .5*np.sum(np.maximum(0.,delta-np.log1p(delta)))
        max_covariance_error=max(max_covariance_error,float(np.linalg.norm(relative-np.eye(2),2)))
    return total_kl, math.sqrt(total_kl/2), max_covariance_error


def main():
    rng = np.random.default_rng(20261027)
    records=[]
    lines=[]
    total_calls=0
    for dimension in (5,17,64,129):
        orthogonal,_=np.linalg.qr(rng.normal(size=(dimension,dimension)))
        eigenvalues=np.linspace(-1,1,dimension)
        matrix=(orthogonal*eigenvalues)@orthogonal.T
        offset=rng.normal(size=dimension)
        theta=rng.normal(size=dimension)
        for q in (.2,.6,.9):
            tau=lipschitz=1.
            noise=1/q
            epsilon=.001
            z=rng.normal(size=dimension)
            w=rng.normal(size=dimension)
            x=theta+tau*z
            oracle=CountingOracle(matrix,offset)
            retained,child,n=acquired_cloud(oracle,x,lipschitz,tau,noise,epsilon,w)
            assert oracle.calls==2*n+3
            total_calls+=oracle.calls
            lambdas=eigenvalues*q
            p,b=scalar_polynomials(lambdas,n)
            exact_runtime_retained=x-tau*(orthogonal*(lambdas*b))@(orthogonal.T@w)
            exact_runtime_child=matrix@x+offset+noise*(orthogonal*p)@(orthogonal.T@w)
            discrepancy=max(np.max(np.abs(retained-exact_runtime_retained)),
                            np.max(np.abs(child-exact_runtime_child)))
            assert discrepancy<1e-10
            kl,pinsker,covariance_error=verify_joint_gaussian(lambdas,n)
            proof_bound=3*math.sqrt(dimension)*q**(2*n+2)/(1-q*q)
            assert proof_bound<=epsilon*(1+1e-12)
            assert pinsker<=proof_bound*(1+1e-8)
            records.append([dimension,q,n,oracle.calls,proof_bound,kl,pinsker,covariance_error,discrepancy])
            lines.append(f"d={dimension}, q={q}: n={n}, values={oracle.calls}, theorem TV<={proof_bound:.8g}, exact Gaussian KL={kl:.8g}, Pinsker={pinsker:.8g}")
    # Every-execution query accounting includes all-zero seeds and input.
    dimension=7
    oracle=CountingOracle(np.eye(dimension),np.zeros(dimension))
    retained,child,n=acquired_cloud(oracle,np.zeros(dimension),1.,1.,2.,.001,np.zeros(dimension))
    assert oracle.calls==2*n+3 and np.all(np.isfinite(retained)) and np.all(np.isfinite(child))
    total_calls+=oracle.calls
    lines.append(f"Null-seed execution: {oracle.calls} values, finite output.")
    lines.append(f"Total synthetic value calls: {total_calls}.")
    lines.append("Runtime hides A and theta; verifier alone uses them. Floating matrices are consistency checks. The separate all-event Gaussian KL proof certifies the ideal-real law.")
    with (ROOT/'affine_cloud_checks.csv').open('w',newline='') as handle:
        writer=csv.writer(handle)
        writer.writerow(['dimension','q','polynomial_order','source_queries','proved_tv_upper','joint_gaussian_kl','gaussian_pinsker_upper','relative_covariance_op_error','runtime_formula_error'])
        writer.writerows(records)
    text='\n'.join(lines)+'\n'
    (ROOT/'AFFINE_CLOUD_CHECK_RESULTS.txt').write_text(text)
    print(text,end='')


if __name__=='__main__':
    main()
