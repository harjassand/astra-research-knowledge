"""Finite sine-Galerkin checks of the EB obstruction's exact algebra.
NumPy only. These do not certify continuum fidelity or the infinite limit.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/eb_checks.py
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

TOL = 3e-9
J = 1.


def model(K):
    basis = list(itertools.combinations_with_replacement(range(1,K+1),2))
    # Products of four sines have Fourier frequencies <=4K; midpoint
    # quadrature with 8K+1 nodes integrates them exactly to roundoff.
    Q = 8*K+1
    x = (np.arange(Q)+0.5)/Q
    phi = np.sqrt(2)*np.sin(np.pi*np.outer(np.arange(1,K+1),x))
    diag = np.array([phi[k-1]*phi[l-1]*(1 if k==l else np.sqrt(2))
                     for k,l in basis])
    contact = 2*diag @ diag.T/Q
    energy = np.array([2*J*np.pi**2*(k*k+l*l) for k,l in basis])
    return basis,energy,contact


def sqrt_positive(a):
    w,v = np.linalg.eigh((a+a.T.conj())/2)
    return (v*np.sqrt(np.maximum(w,0)))@v.T.conj()


identity_errors, c_bound_ratios, band_ratios, margins = [],[],[],[]
for M in range(1, 7):
    basis,e,b = model(4*M)
    s = 4*J*np.pi**2*M*M
    r = 1/(s+e)
    R0 = np.diag(r)
    half = np.diag(np.sqrt(r))
    C = half @ b @ half
    c = 4/math.sqrt(2*J*s)
    c_bound_ratios.append(float(np.linalg.eigvalsh(C)[-1]/c))
    assert c_bound_ratios[-1] <= 1+TOL
    u = np.array([1/math.sqrt(M) if k==l and M+1<=k<=2*M else 0
                  for k,l in basis])
    v = np.array([1/math.sqrt(M) if k==l and 3*M+1<=k<=4*M else 0
                  for k,l in basis])
    leading = half @ (R0@C-C@R0) @ half
    witness = float(u @ leading @ v)
    lower = 1/(27200*J**3*np.pi**6*M**5)
    band_ratios.append(witness/lower)
    assert witness >= lower-TOL
    for a,bval in ((1e-6,2e-6),(0.1,0.7),(1.,3.)):
        Ra = np.linalg.inv(np.diag(e+s)+a*b)
        Rb = np.linalg.inv(np.diag(e+s)+bval*b)
        Q = np.linalg.inv(np.eye(len(e))+a*C) @ np.linalg.inv(np.eye(len(e))+bval*C)
        lhs = Ra@Rb-Rb@Ra
        rhs = (a-bval)*half@Q@(R0@C-C@R0)@Q@half
        identity_errors.append(float(np.linalg.norm(lhs-rhs,2)))
        err = float(np.linalg.norm(lhs/(a-bval)-leading,2))
        bound = 4*(a+bval)*c*c/s**2
        margins.append(bound-err)
        assert identity_errors[-1] <= TOL
        assert err <= bound+TOL

# Check full finite-Galerkin density affinity/fidelity and EB commutator
# comparison; vacuum plus the complete retained m=2 sector is used here.
# This is a small diagnostic experiment, not the true full-Fock family.
density_cases = []
log_commutator_ratios = []
shift_error_ratios = []
for K in (3,5,8):
    basis,e,b = model(K)
    for tau in (0.001,0.01,0.1):
        rhos=[]
        for coupling in (0.3,0.9):
            ev,vec=np.linalg.eigh(np.diag(e)+coupling*b)
            w=np.exp(-tau*ev)
            block=(vec*w)@vec.T
            rho=np.zeros((len(e)+1,)*2)
            rho[0,0]=1
            rho[1:,1:]=block
            rho/=np.trace(rho)
            rhos.append(rho)
        rho,sigma=rhos
        product=sqrt_positive(rho)@sqrt_positive(sigma)
        affinity=float(np.trace(product).real)
        fidelity=float(np.linalg.svd(product,compute_uv=False).sum())
        comm=float(np.linalg.svd(rho@sigma-sigma@rho,compute_uv=False).sum())
        assert fidelity-affinity >= comm*comm/128-TOL
        assert fidelity-affinity > 0
        density_cases.append({"K":K,"tau":tau,"fidelity_minus_affinity":fidelity-affinity,
                              "commutator_trace_norm":comm})
        # The log transfer is a dimension-independent bounded-operator
        # identity. Here test it at ordinary representable shifts, rather
        # than evaluating the theorem's exponentially tiny delta.
        s=3/tau
        delta=0.05
        gamma=1/(s-math.log(delta)/tau)
        logs, shifted, unshifted=[],[],[]
        for a in rhos:
            w,vec=np.linalg.eigh(a)
            wx=np.maximum(w,0)+delta
            logs.append((vec*np.log(wx))@vec.T)
            shifted.append((vec/(s-np.log(wx)/tau))@vec.T)
            pr=np.array([0. if v<=0 else 1/(s-math.log(v)/tau) for v in w])
            unshifted.append((vec*pr)@vec.T)
        logcomm=float(np.linalg.svd(logs[0]@logs[1]-logs[1]@logs[0],compute_uv=False).sum())
        log_commutator_ratios.append(logcomm/(comm/delta**2))
        assert logcomm <= comm/delta**2+TOL
        for pshift,praw in zip(shifted,unshifted):
            shift_error_ratios.append(float(np.linalg.norm(pshift-praw,2))/gamma)
            assert np.linalg.norm(pshift-praw,2) <= gamma+TOL
        s0=s-math.log(1+delta)/tau
        rc=float(np.linalg.svd(shifted[0]@shifted[1]-shifted[1]@shifted[0],compute_uv=False).sum())
        assert rc <= comm/(tau**2*s0**4*delta**2)+TOL

scalar_shift_ratios=[]
for tau in (0.01,0.3,2.):
    s=3/tau
    for delta in (0.001,0.05,0.3):
        psi=lambda t:0. if t==0 else 1/(s-math.log(t)/tau)
        gamma=psi(delta)
        ratios=[(psi(float(t)+delta)-psi(float(t)))/gamma for t in np.linspace(0,1,301)]
        scalar_shift_ratios.append(max(ratios))
        assert min(ratios) >= -TOL
        assert max(ratios) <= 1+TOL

out={"status":"FINITE-EVIDENCE","all_checks_passed":True,
     "resolvent_identity_cases":len(identity_errors),
     "max_resolvent_identity_error":max(identity_errors),
     "max_normalized_contact_bound_ratio":max(c_bound_ratios),
     "min_free_band_witness_over_lower":min(band_ratios),
     "min_resolvent_dressing_margin":min(margins),
     "finite_density_cases":density_cases,
     "max_log_commutator_over_bound":max(log_commutator_ratios),
     "max_matrix_shift_error_over_bound":max(shift_error_ratios),
     "max_scalar_shift_error_over_bound":max(scalar_shift_ratios),
     "limitation":"Galerkin/finite scalar algebra only; no certified continuum fidelity, thermal truncation or practical EB margin."}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
