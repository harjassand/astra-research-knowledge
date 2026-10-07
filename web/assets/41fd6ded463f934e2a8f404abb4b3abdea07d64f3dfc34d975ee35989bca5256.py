"""Numerical diagnostics for the bounded-likelihood Petz correction lemma.

These fixtures do not prove the lemma or the remaining EB implication.
"""
from pathlib import Path
import json
import numpy as np

SEED = 707173
rng = np.random.default_rng(SEED)

def herm(a):
    return (a + a.conj().T) / 2

def power(a, exponent, cutoff=1e-13):
    vals, vecs = np.linalg.eigh(herm(a))
    out = np.zeros_like(vals)
    good = vals > cutoff * max(1.0, float(np.max(vals)))
    out[good] = vals[good] ** exponent
    return (vecs * out) @ vecs.conj().T

def trnorm(a):
    return float(np.sum(np.linalg.svd(a, compute_uv=False)))

def random_unitary(n):
    z = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    q, r = np.linalg.qr(z)
    return q @ np.diag(np.diag(r) / np.abs(np.diag(r)))

def density(n, spread):
    weights = np.exp(rng.uniform(-spread, 0, n))
    weights /= np.sum(weights)
    u = random_unitary(n)
    return (u * weights) @ u.conj().T

def likelihood_state(sigma, theta):
    n = sigma.shape[0]
    z = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    h = herm(z)
    h -= np.trace(sigma @ h).real * np.eye(n)
    h *= theta / max(np.linalg.norm(h,2), 1e-14)
    root = power(sigma,.5)
    rho = root @ (np.eye(n) + h) @ root
    return herm(rho), h

def channel_from_isometry(n, out, anc):
    z = rng.normal(size=(out*anc,n)) + 1j*rng.normal(size=(out*anc,n))
    v, _ = np.linalg.qr(z)
    v = v[:,:n].reshape(out,anc,n)
    return [v[:,j,:] for j in range(anc)]

def apply(kraus, x):
    return sum((k @ x @ k.conj().T for k in kraus), np.zeros((kraus[0].shape[0],)*2,complex))

def adjoint(kraus,x):
    return sum((k.conj().T @ x @ k for k in kraus), np.zeros((kraus[0].shape[1],)*2,complex))

def superop(fn,n):
    cols = []
    for j in range(n):
        for i in range(n):
            e = np.zeros((n,n),complex)
            e[i,j] = 1
            cols.append(fn(e).reshape(-1,order='F'))
    return np.column_stack(cols)

def q(sigma,x):
    y = power(sigma,-.25) @ x @ power(sigma,-.25)
    return float(np.trace(y.conj().T @ y).real)

records=[]
max_residuals = dict(tp=0., reference_fixed=0., kms_hermiticity=0.,
                     kms_negative_eigenvalue=0., kms_eigenvalue_excess=0.,
                     petz_q_identity=0., loss_upper_violation=0.,
                     recovery_trace_violation=0., recovery_q_violation=0.)
for n in range(2,7):
    for fixture in range(80):
        sigma = density(n, (fixture % 5)*3.0)
        theta = [.1,.5,.9][fixture%3]
        rho,h = likelihood_state(sigma,theta)
        # Near-identity, generic, and singular-output channels are all included.
        if fixture % 10 == 0:
            out=1
            kraus=[np.eye(n)[j:j+1] for j in range(n)]
            kind='singular_support_compression'
        else:
            out=n
            ks=channel_from_isometry(n,out,1+fixture%4)
            if fixture % 2:
                mix=10.**(-1-fixture%7)
                kraus=[np.sqrt(1-mix)*np.eye(n)]+[np.sqrt(mix)*k for k in ks]
                kind='near_identity'
            else:
                kraus=ks
                kind='generic'
        tau=herm(apply(kraus,sigma))
        trho=herm(apply(kraus,rho))
        rs=power(sigma,.5)
        it=power(tau,-.5)
        def recover(x):
            return rs @ adjoint(kraus,it @ x @ it) @ rs
        def s(x):
            return recover(apply(kraus,x))
        srho=herm(s(rho))
        # In compression fixtures compare density on the original full output space
        # by embedding its sole output basis vector into that space.
        embedded_tau=tau if out==n else np.pad(tau,((0,n-out),(0,n-out)))
        embedded_trho=trho if out==n else np.pad(trho,((0,n-out),(0,n-out)))
        dr=trnorm(embedded_trho-rho)
        ds=trnorm(embedded_tau-sigma)
        loss=max(0.,q(sigma,rho)-q(tau,trho))
        upper=2*theta*(dr+ds)+6*theta**2*np.sqrt(ds)
        q_rec=q(sigma,srho-rho)
        trace_rec=trnorm(srho-rho)
        # All reference inverses are explicit; no condition-number-free floating
        # point claim is made at spectra below the documented cutoff.
        gs=power(sigma,.25)
        igs=power(sigma,-.25)
        kms=superop(lambda x: igs @ s(gs @ x @ gs) @ igs,n)
        kms_eigs=np.linalg.eigvalsh(herm(kms))
        vals={
            'tp': abs(np.trace(srho).real-1),
            'reference_fixed':trnorm(s(sigma)-sigma),
            'kms_hermiticity':float(np.linalg.norm(kms-kms.conj().T,2)),
            'kms_negative_eigenvalue':max(0.,-float(np.min(kms_eigs))),
            'kms_eigenvalue_excess':max(0.,float(np.max(kms_eigs))-1),
            'petz_q_identity':abs(np.trace((power(sigma,-.25)@rho@power(sigma,-.25)).conj().T @
                (power(sigma,-.25)@srho@power(sigma,-.25))).real-q(tau,trho)),
            'loss_upper_violation':max(0.,loss-upper),
            'recovery_trace_violation':max(0.,trace_rec-np.sqrt(loss)),
            'recovery_q_violation':max(0.,q_rec-loss),
        }
        for key,value in vals.items():
            max_residuals[key]=max(max_residuals[key],value)
        records.append(dict(n=n,fixture=fixture,kind=kind,theta=theta,
                            sigma_min_eigenvalue=float(np.min(np.linalg.eigvalsh(sigma))),
                            dr=dr,ds=ds,q_loss=loss,loss_upper=upper,
                            recovery_trace=trace_rec,recovery_q=q_rec))

# Exact reference-preserving tracial channels, to test the sharper ds=0 loss.
exact_max=0.
for n in range(2,8):
    sigma=np.eye(n)/n
    for fixture in range(50):
        theta=[.1,.5,.9][fixture%3]
        rho,h=likelihood_state(sigma,theta)
        us=[random_unitary(n) for _ in range(3)]
        probs=rng.dirichlet(np.ones(3))
        ks=[np.sqrt(p)*u for p,u in zip(probs,us)]
        trho=apply(ks,rho)
        loss=q(sigma,rho)-q(sigma,trho)
        exact_max=max(exact_max,loss-2*theta*trnorm(trho-rho))

# An exactly broadcastable classical family falsifies uniform replacement by
# the ultimate fixed-point channel: slow mixing is not a quantum obstruction.
a=.5
slow=[]
for delta in [1e-1,1e-2,1e-4,1e-6]:
    slow.append(dict(delta=delta,theta=a,
                     broadcast_error=a*delta,
                     ergodic_projection_error=a/2,
                     available_eb_error=0.0,
                     spectral_gap=2*delta))

result=dict(seed=SEED,fixture_count=len(records),exact_reference_fixture_count=300,
            max_residuals=max_residuals,exact_reference_loss_violation=max(0.,exact_max),
            tolerance=2e-7,all_checks_pass=all(v<2e-7 for v in max_residuals.values())
            and exact_max<2e-7,
            slow_classical_obstruction=slow,
            limitations=['No optimization for EB or broadcasting was solved.',
                        'No growing-family theorem follows from these fixtures.',
                        'Singular outputs were tested by compression; full-space TP recovery uses the explicit complementary-support replacement in the report.'],
            fixtures=records)
dest=Path(__file__).with_suffix('.json')
dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))
