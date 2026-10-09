#!/usr/bin/env python3
"""Finite numerical diagnostics for the accompanying analytical research note.

These tests do not prove the universal statements, optimize a broadcaster,
construct the smoothing minimizer, or certify historical novelty.
Run: python verify.py [--output diagnostics.json]
Requires Python 3.10+, NumPy and SciPy. No network access is used.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import qr

SEED = 20261009
TOL = 2e-7
rng = np.random.default_rng(SEED)
stats: dict[str, float] = {}
counts: dict[str, int] = {}


def herm(a: np.ndarray) -> np.ndarray:
    return (a + a.conj().T) / 2


def power(a: np.ndarray, exponent: float, support: bool = False) -> np.ndarray:
    w, v = np.linalg.eigh(herm(a))
    if w.min() < -1e-8:
        raise ValueError(f"Matrix is not positive: minimum eigenvalue {w.min()}")
    w = np.maximum(w, 0)
    if exponent < 0:
        threshold = max(float(w.max()), 1.) * 1e-12
        if not support and np.any(w <= threshold):
            raise ValueError("Inverse requested for a singular matrix")
        z = np.zeros_like(w)
        np.power(w, exponent, out=z, where=w > threshold)
    else:
        z = w ** exponent
    return (v * z) @ v.conj().T


def trace_norm(a: np.ndarray) -> float:
    return float(np.linalg.svd(a, compute_uv=False).sum())


def hs(a: np.ndarray) -> float:
    return float(np.linalg.norm(a, 'fro'))


def unitary(d: int) -> np.ndarray:
    z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    q, _ = qr(z)
    return q


def state(d: int, spread: float = 5.) -> np.ndarray:
    u = unitary(d)
    ev = np.exp(np.linspace(-spread, 0, d))
    ev /= ev.sum()
    return herm((u * ev) @ u.conj().T)


def root_fidelity(a: np.ndarray, b: np.ndarray) -> float:
    return trace_norm(power(a,.5) @ power(b,.5))


def Q(reference: np.ndarray, x: np.ndarray) -> float:
    inv = power(reference, -.25, support=True)
    return hs(inv @ x @ inv) ** 2


def record(name: str, residual: float, scale: float = 1.) -> None:
    value = abs(float(residual)) / max(1., abs(scale))
    stats[name] = max(stats.get(name, 0.), value)
    counts[name] = counts.get(name, 0) + 1
    if not np.isfinite(value) or value > TOL:
        raise AssertionError(f"{name}: normalized residual {value:.9g} > {TOL}")


def leq(name: str, lhs: float, rhs: float) -> None:
    record(name, max(0., lhs-rhs), max(abs(lhs),abs(rhs)))


def channel(d: int, singular: bool = False):
    """Random CPTP endomorphism, optionally with a proper output support."""
    r = max(1,d-1) if singular else d
    rank = d + 1
    g = rng.normal(size=(rank*r,d)) + 1j*rng.normal(size=(rank*r,d))
    v, _ = qr(g, mode='economic')
    ks = []
    for k in range(rank):
        a = np.zeros((d,d),complex)
        a[:r,:] = v[k*r:(k+1)*r,:]
        ks.append(a)
    if not singular:
        mixture = float(rng.uniform(.02,.8))
        ks = [math.sqrt(mixture)*a for a in ks]
        ks.append(math.sqrt(1-mixture)*np.eye(d))
    def forward(x):
        return herm(sum((k @ x @ k.conj().T for k in ks), np.zeros_like(x)))
    def adjoint(x):
        return herm(sum((k.conj().T @ x @ k for k in ks), np.zeros_like(x)))
    return forward, adjoint


def finite_flags(sig: np.ndarray, t: float):
    """Exact interval decomposition of the random shifted logarithmic bins."""
    ev, u = np.linalg.eigh(sig)
    sv = np.sqrt(ev)
    lv = np.log(sv)
    points = np.r_[0., np.mod(lv,t), t]
    points.sort()
    intervals = []
    for lo, hi in zip(points[:-1],points[1:]):
        if hi-lo <= 1e-13:
            continue
        shift = (lo+hi)/2
        labels = np.floor((lv-shift)/t).astype(int)
        flat = np.exp(shift+labels*t)
        flat /= np.linalg.norm(flat)
        sp = herm((u*(flat**2))@u.conj().T)
        af = np.exp(-t)*flat/sv
        a = herm((u*af)@u.conj().T)
        mask = labels[:,None] == labels[None,:]
        def pinch(z, mask=mask, u=u):
            return herm(u @ ((u.conj().T@z@u)*mask) @ u.conj().T)
        def filt(z, a=a, sp=sp, pinch=pinch):
            remainder = np.trace((np.eye(len(a))-a@a)@z).real
            return herm(a@pinch(z)@a + remainder*sp)
        intervals.append(((hi-lo)/t,sp,a,pinch,filt))
    return intervals


def test_matrix_lemmas(n: int = 180):
    for iteration in range(n):
        d = 2 + iteration%6
        sig = state(d, spread=float(rng.uniform(0,12)))
        ss = power(sig,.5)
        h = herm(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
        h -= np.trace(sig@h).real*np.eye(d)
        h *= .5 / max(abs(np.linalg.eigvalsh(h)))
        rho = herm(ss@(np.eye(d)+h)@ss)
        kappa = math.sqrt(1.5)
        x = power(sig,-.5) @ power(ss@rho@ss,.5) @ power(sig,-.5)
        x = herm(x)
        record('canonical_state_identity',hs(x@sig@x-rho))
        leq('canonical_likelihood_bound',float(np.linalg.eigvalsh(x).max()),kappa)
        delta = max(0.,root_fidelity(sig,rho)-np.trace(ss@power(rho,.5)).real)
        xi = hs(x@ss-ss@x)
        leq('canonical_commutator_bound',xi,2*math.sqrt(2*kappa*delta))
        t = float(rng.uniform(.05,1.))
        flags = finite_flags(sig,t)
        record('flag_probability_sum',sum(f[0] for f in flags)-1)
        averaged_pinching_sq = 0.
        averaged_error = 0.
        for prob, sp, a, pinch, filt in flags:
            output = filt(rho)
            record('filter_trace_preservation',np.trace(output).real-1)
            record('filter_exact_reference',hs(filt(sig)-sp))
            leq('filter_output_positivity',-np.linalg.eigvalsh(output).min(),0)
            leq('filter_lower_sandwich',-np.linalg.eigvalsh(output-.5*sp).min(),0)
            leq('filter_upper_sandwich',-np.linalg.eigvalsh(1.5*sp-output).min(),0)
            record('filter_reference_centrality',hs(output@sp-sp@output))
            leq('filter_modification_cost',trace_norm(output-pinch(rho)),8*t)
            averaged_pinching_sq += prob*hs((x-pinch(x))@ss)**2
            averaged_error += prob*trace_norm(output-rho)
        leq('random_pinching_bound',averaged_pinching_sq,3*kappa*xi/t)
        leq('flagged_decoder_error',averaged_error,4*math.sqrt(3*kappa*xi/t)+8*t)

        U, adj = channel(d,singular=(iteration%11==0))
        nu, urho = U(sig), U(rho)
        invnu = power(nu,-.5,support=True)
        corrected = herm(ss@adj(invnu@urho@invnu)@ss)
        dr, ds = trace_norm(urho-rho), trace_norm(nu-sig)
        loss = Q(sig,rho)-Q(nu,urho)
        leq('Q_data_processing',Q(nu,urho),Q(sig,rho))
        leq('Petz_Q_recovery',Q(sig,rho-corrected),loss)
        leq('Petz_trace_recovery',trace_norm(rho-corrected)**2,loss)
        leq('sandwich_Q_loss_continuity',loss,dr+ds+1.5*math.sqrt(ds))
        record('Petz_reference_recovery',hs(ss@adj(invnu@nu@invnu)@ss-sig))

        # Test the transport inequalities used by the strongly convex smoother.
        # This is NOT a numerical solution of that minimization problem.
        M = float(rng.uniform(2,60))
        z = state(d,spread=float(rng.uniform(0,7)))
        amat = M*z/np.linalg.eigvalsh(z).max()
        tau = herm(ss@amat@ss)
        if np.trace(tau).real > 1:
            amat /= np.trace(tau).real
            tau = herm(ss@amat@ss)
        ns = power(nu,.5)
        tau_prime = herm(ns@amat@ns)
        clipped = tau_prime/max(1.,np.trace(tau_prime).real)
        leq('smoothing_transport_trace',trace_norm(clipped-tau),2*M*math.sqrt(ds)+M*ds)
        leq('smoothing_transport_Q',Q(nu,clipped)-Q(sig,tau),2*M*M*math.sqrt(ds))
        fidloss = root_fidelity(rho,tau)-root_fidelity(urho,clipped)
        leq('smoothing_transport_fidelity',fidloss,math.sqrt(dr)+math.sqrt(M*ds)+M*ds/2)
    return n


def traceless_basis(d: int) -> np.ndarray:
    out=[]
    for i in range(d):
        for j in range(i+1,d):
            a=np.zeros((d,d),complex); a[i,j]=a[j,i]=math.sqrt(d/2)
            out.append(a)
            a=np.zeros((d,d),complex); a[i,j]=-1j*math.sqrt(d/2); a[j,i]=1j*math.sqrt(d/2)
            out.append(a)
    for k in range(1,d):
        a=np.zeros((d,d),complex)
        a[range(k),range(k)]=1
        a[k,k]=-k
        out.append(a*math.sqrt(d/(k*(k+1))))
    return np.array(out)


def test_tree(mixed_sign: bool):
    d=3
    basis=traceless_basis(d)
    P=np.array([np.diag(np.eye(d)[i]).astype(complex) for i in range(d)])
    if mixed_sign:
        permutation=np.array([[0,1,0],[1,0,0],[0,0,1]],float)
        trans=.9*permutation+.1*np.ones((d,d))/d
        inputs=P
        output_states=np.array([np.diag(trans[:,i]).astype(complex) for i in range(d)])
        weights=np.ones(d)
    else:
        u=unitary(d)
        P2=np.array([np.outer(u[:,i],u[:,i].conj()) for i in range(d)])
        inputs=np.concatenate((P,P2))
        output_states=inputs.copy()
        weights=np.r_[np.full(d,.96),np.full(d,.04)]
    def phi(a):
        coefficients=np.einsum('kij,ji->k',inputs,a).real
        return np.einsum('k,k,kij->ij',weights,coefficients,output_states)
    mat=np.array([[np.trace(a@phi(b)).real/d for b in basis] for a in basis])
    ev,vec=np.linalg.eigh(mat)
    select=np.abs(ev)>1/math.sqrt(2)
    lambdas=ev[select]
    modes=np.einsum('ji,jab->iab',vec[:,select],basis)
    m=len(modes)
    E=[]; z=[]
    for i,a in enumerate(modes):
        val,v=np.linalg.eigh(a)
        for j in range(d):
            E.append(np.outer(v[:,j],v[:,j].conj())/m)
            row=np.zeros(m);row[i]=m*val[j];z.append(row)
    E=np.array(E); z=np.array(z)
    # Joint reference state = sum_k weights_k tau(input_k) out_k tensor out_k.
    means=np.einsum('kab,iba->ki',output_states,modes).real
    pref=weights*np.trace(inputs,axis1=1,axis2=2).real/d
    corr=np.einsum('k,ki,kj->ij',pref,means,means)
    leq('tree_cross_covariance_upper',np.linalg.eigvalsh(corr-np.eye(m)).max(),0)
    Cprev=None; records=[]
    for depth in range(3):
        probs=np.trace(E,axis1=1,axis2=2).real/d
        C=np.einsum('y,yi,yj->ij',probs,z,z)
        unbiased=np.einsum('yi,yab->iab',z,E)
        record('tree_unbiasedness',hs((unbiased-modes).reshape(m*d,d)))
        record('tree_POVM_normalization',hs(E.sum(axis=0)-np.eye(d)))
        leq('tree_POVM_positivity',-np.linalg.eigvalsh(E).min(),0)
        if Cprev is not None:
            expected=(Cprev+corr)/(2*lambdas[:,None]*lambdas[None,:])
            record('tree_covariance_recursion',hs(C-expected),hs(expected))
        # Regression as a full-space quadratic form, not only a compression.
        moment=np.einsum('yab,jba->yj',E,basis).real/d
        matrix=np.einsum('yi,yj,y->ij',moment,moment,1/probs)
        coords=np.array([[np.trace(a@b).real/d for b in modes] for a in basis])
        lower=coords@np.linalg.inv(C)@coords.T
        leq('tree_full_space_regression',-np.linalg.eigvalsh(herm(matrix-lower)).min(),0)
        records.append({'depth':depth,'outcomes':len(E),'min_C_eigenvalue':float(np.linalg.eigvalsh(C).min())})
        if depth<2:
            moments=np.einsum('kab,yba->ky',output_states,E).real
            E=np.einsum('k,ky,kz,kab->yzab',weights,moments,moments,inputs).reshape(-1,d,d)
            z=((z[:,None,:]+z[None,:,:])/(2*lambdas)).reshape(-1,m)
            Cprev=C
    commutator_norm = hs(modes[0]@modes[1]-modes[1]@modes[0]) if m >= 2 else 0.
    if not mixed_sign:
        assert commutator_norm > 1e-6, 'The designated noncommuting fixture became commuting.'
    return {'mixed_sign':mixed_sign,'selected_eigenvalues':lambdas.tolist(),'selected_mode_commutator_HS_norm':commutator_norm,'depths':records}


def scalar_checks():
    vals={
        'sandwich_scaling_20_times_5_power':20*5**(1/192),
        'smoothing_s_coefficient_upper':1.5+(1+math.sqrt(2))*2**.25/2+(1+math.sqrt(2))/4+math.sqrt(2)/2,
        'logarithmic_coefficient_4sqrt1536_plus1':4*math.sqrt(1536)+1,
        'exponential_tail_ratio_at_threshold':336*math.sqrt(24576)/65536,
        'pair_q_coefficient':2/(math.e*math.log(2))+1+math.sqrt(math.log(2)/2),
    }
    assert vals['sandwich_scaling_20_times_5_power']<21
    assert vals['smoothing_s_coefficient_upper']<5
    assert vals['logarithmic_coefficient_4sqrt1536_plus1']<200
    assert vals['exponential_tail_ratio_at_threshold']<1
    assert vals['pair_q_coefficient']<3
    return vals


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('diagnostics.json'))
    args=parser.parse_args()
    fixtures=test_matrix_lemmas()
    trees=[test_tree(False),test_tree(True)]
    result={
        'status':'PASS',
        'seed':SEED,
        'relative_absolute_tolerance':TOL,
        'matrix_fixtures':fixtures,
        'dimensions':[2,3,4,5,6,7],
        'includes_singular_output_reference':True,
        'max_normalized_residuals':stats,
        'checks_per_identity':counts,
        'total_checks':sum(counts.values()),
        'tree_fixtures':trees,
        'scalar_constants':scalar_checks(),
        'limitations':[
            'Finite floating-point diagnostics, not a universal proof or interval certificate.',
            'The smoothing minimizer was not numerically optimized.',
            'No historical-priority certification, external expert review, or proof-assistant run.',
            'These checks are newly written; inaccessible archived scripts were not replayed.'
        ]
    }
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'matrix_fixtures':fixtures,'total_checks':result['total_checks'],'max_normalized_residual':max(stats.values()),'output':str(args.output)},indent=2))

if __name__=='__main__':
    main()
