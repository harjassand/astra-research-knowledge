#!/usr/bin/env python3
"""Check algebraic diagnostics for the Astra controlled-matter audit.

No material potential, experimental data, DFT calculation, or physical signal is
simulated. Dimensionless matrices/oscillators are mathematical test fixtures.
Requires Python >= 3.10, NumPy and SciPy.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rotation(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


def tensor_tests() -> dict:
    rng = np.random.default_rng(193)
    errors = []
    for k in range(6):
        for mirror in (False, True):
            for inversion in (-1, 1):
                O = rotation(k*np.pi/3)
                if mirror:
                    O = O @ np.diag([1., -1.])
                r1, r2 = rng.normal(size=2)
                R = np.array([[r1, r2], [r2, -r1]])
                P = rng.normal(size=2)
                R_new = O @ R @ O.T  # even under inversion
                P_new = inversion * O @ P
                predicted = inversion * O @ (R @ P)
                errors.append(float(np.linalg.norm(R_new @ P_new-predicted)))
    # In-plane E1 and E2 are inequivalent already under the 60-degree rotation.
    # Check that no nonzero 2x2 intertwiner exists: T E2 = E1 T.
    E1, E2 = rotation(np.pi/3), rotation(2*np.pi/3)
    columns=[]
    for k in range(4):
        T=np.zeros((2,2)); T.flat[k]=1
        columns.append((T@E2-E1@T).ravel())
    singular=np.linalg.svd(np.column_stack(columns), compute_uv=False)
    local_C3 = rotation(4*np.pi/3)
    local_singular = np.linalg.svd(local_C3-np.eye(2), compute_uv=False)
    require(float(min(local_singular))>1e-8, 'Unexpected invariant linear E2g scalar gradient under C3')
    require(max(errors)<1e-12, 'E2g tensor times E1u vector covariance failed')
    require(float(min(singular))>1e-8, 'Unexpected E2-to-E1 intertwiner')
    return {'group_cases':len(errors),'max_covariance_error':max(errors),
            'E2_to_E1_intertwiner_min_singular':float(min(singular)),
            'local_C3_E2g_invariant_gradient_min_singular':float(min(local_singular))}


def energy_model(s: float, Q: np.ndarray, eta: float, sigma: int,
                 B: float=1., K: float=2., d: float=.2) -> float:
    c=np.array([d*np.cos(np.pi*s), sigma*eta*np.sin(np.pi*s)**2])
    return float(B*np.sin(np.pi*s)**2 + .5*K*np.sum((Q-c)**2))


def hessian_fd(x: np.ndarray, f, step: float=1e-5) -> np.ndarray:
    n=len(x); H=np.zeros((n,n)); f0=f(x)
    for i in range(n):
        ei=np.zeros(n);ei[i]=step
        H[i,i]=(f(x+ei)-2*f0+f(x-ei))/step**2
        for j in range(i):
            ej=np.zeros(n);ej[j]=step
            H[i,j]=H[j,i]=(f(x+ei+ej)-f(x+ei-ej)-f(x-ei+ej)+f(x-ei-ej))/(4*step**2)
    return H


def identifiability_tests() -> dict:
    K=2.;B=1.;d=.2; out=[]
    for eta in (0., .15):
        max_path_error=0.;max_hessian_error=0.
        for sigma in (-1,1):
            for s in np.linspace(0,1,101):
                Q=np.array([d*np.cos(np.pi*s),sigma*eta*np.sin(np.pi*s)**2])
                max_path_error=max(max_path_error, abs(energy_model(s,Q,eta,sigma)-B*np.sin(np.pi*s)**2))
            for s in (0.,1.):
                x=np.array([s,d*np.cos(np.pi*s),0.])
                H=hessian_fd(x,lambda z:energy_model(float(z[0]),z[1:],eta,sigma))
                expected=np.diag([2*B*np.pi**2,K,K])
                max_hessian_error=max(max_hessian_error,float(np.max(np.abs(H-expected))))
        eps=1e-6
        def u(Q):
            return energy_model(1.,Q,eta,1)-energy_model(0.,Q,eta,1)
        def v(Q):
            return .5*(energy_model(.5,Q,eta,1)-energy_model(.5,Q,eta,-1))
        A=np.zeros((2,2))
        for j in range(2):
            e=np.zeros(2);e[j]=eps
            A[0,j]=(u(e)-u(-e))/(2*eps)
            A[1,j]=(v(e)-v(-e))/(2*eps)
        expected_A=np.diag([2*K*d,-K*eta])
        require(np.allclose(A,expected_A,atol=1e-9),'Energy response derivatives failed')
        require(max_hessian_error<1e-5,'Well Hessian changed unexpectedly')
        require(max_path_error<1e-12,'Relaxed barrier path changed')
        out.append({'eta_synthetic':eta, 'relaxed_barrier_synthetic':B,
                    'control_matrix':A.tolist(),'rank':int(np.linalg.matrix_rank(A,tol=1e-9)),
                    'max_hessian_error':max_hessian_error,'max_relaxed_path_error':max_path_error})
    return {'scope':'counterexample, not a material force field','cases':out}


def loop_area_tests() -> dict:
    out=[]
    A=0.7;B=0.4
    for g in (.15,.5):
        for w1 in (1.,2.,3.):
            for w2 in (1.,1.7,3.):
                def integrand(t):
                    # 1/2 (q1 dq2 - q2 dq1), common damping g.
                    return .5*A*B*np.exp(-2*g*t)*(w2*np.cos(w1*t)*np.cos(w2*t)+w1*np.sin(w1*t)*np.sin(w2*t))
                numeric=quad(integrand,0.,30/g,epsabs=1e-11,epsrel=1e-10,limit=1500)[0]
                expected=A*B/4*((w1+w2)*(2*g)/((2*g)**2+(w1-w2)**2)
                              +(w2-w1)*(2*g)/((2*g)**2+(w1+w2)**2))
                require(abs(numeric-expected)<1e-8,'Damped loop-area identity failed')
                out.append(abs(numeric-expected))
    return {'synthetic_cases':len(out),'max_quadrature_error':max(out)}


def retention_and_capture_tests() -> dict:
    # Dimensionless periodic PNP fixtures, not potassium material parameters.
    N=256;L=2*np.pi; x=np.arange(N)*L/N
    k=np.fft.fftfreq(N,d=L/N)*2*np.pi
    maxerr=0.
    for mode in (1,2,4,7):
        D=.3;rho=.8;t=.7
        c=np.cos(mode*x)
        spectral=np.fft.ifft(np.fft.fft(c)*np.exp(-(D*k*k+rho)*t)).real
        exact=c*np.exp(-(D*mode*mode+rho)*t)
        maxerr=max(maxerr,float(np.max(np.abs(spectral-exact))))
    require(maxerr<1e-12,'Linear PNP modal decay failed')
    # A spatially uniform current has zero divergence.
    uniform=np.ones(N)*3.7
    derivative=np.fft.ifft(1j*k*np.fft.fft(uniform)).real
    require(float(np.max(np.abs(derivative)))<1e-12,'Uniform-current continuity failed')
    # If all capture hazards share a scalar mobility factor, conditional sink
    # fractions are unchanged. Finite pulse duration changes only completion.
    h=2.;bad=3.;capture=[]
    for dose in (.1,1.,5.):
        total=1-np.exp(-(h+bad)*dose)
        healed=h/(h+bad)*total
        capture.append(float(healed/total))
    require(np.allclose(capture,.4),'Shared-mobility capture invariance failed')
    ell=10e-9;t_seconds=3600.;f=.9
    Dmax=-np.log(f)*ell**2/(4*np.pi**2*t_seconds)
    rmax=-np.log(f)/t_seconds
    return {'PNP_synthetic_modes':4,'max_spectral_error':maxerr,
            'capture_conditional_fractions':capture,
            'stipulated_10nm_one_hour_90pct_Dmax_m2_per_s':float(Dmax),
            'stipulated_one_hour_90pct_sigma_over_epsilon_max_per_s':float(rmax)}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('checks.json'))
    args=parser.parse_args()
    result={'status':'floating-point algebra checks only; no material validation',
            'symmetry':tensor_tests(),'nonidentifiability':identifiability_tests(),
            'damped_area':loop_area_tests(),'retention_capture':retention_and_capture_tests()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
