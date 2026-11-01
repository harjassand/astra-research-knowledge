"""Independent audit of root's Gaussian reference and quartic insertion.

The baseline generator is derived directly from spin-flip energy differences,
then quotiented by global spin reversal.  It does not call root.dense_generator.
This is floating-point verification, not a numerical interval certificate.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import expit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "root" / "gaussian_kinetics.py"
spec = importlib.util.spec_from_file_location("root_gaussian", ROOT)
root = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root)


def spin_quotient(J, attempts, epsilon=0.0):
    n = len(J)
    walls = [s for s in range(1 << n) if s.bit_count() % 2 == 0]
    index = {s: i for i, s in enumerate(walls)}
    Q = np.zeros((len(walls), len(walls)))
    E = np.empty(len(walls))
    for col, w in enumerate(walls):
        spins = np.ones(n, dtype=int)
        for j in range(1, n):
            spins[j] = spins[j-1] * (1 - 2*((w >> (j-1)) & 1))
        E[col] = -sum(J[j]*spins[j]*spins[(j+1) % n] for j in range(n))
        for j in range(n):
            left = (j-1) % n
            delta = 2*spins[j]*(J[left]*spins[left] + J[j]*spins[(j+1) % n])
            multiplier = 1 + epsilon*((w >> ((j+1) % n)) & 1)
            rate = attempts[left] * expit(-delta) * multiplier
            dest = w ^ (1 << left) ^ (1 << j)
            Q[index[dest], col] += rate
            Q[col, col] -= rate
    p = np.exp(-(E-E.min()))
    p /= p.sum()
    K = -(Q * np.sqrt(p)[None, :]) / np.sqrt(p)[:, None]
    return Q, K, p


def check_case(label, J, nu):
    m = root.model(J, nu)
    Q, K, p = spin_quotient(np.asarray(J), np.asarray(nu))
    vals, vecs = eigh(K)
    G = (vecs[:, 1:] / vals[1:]) @ vecs[:, 1:].T
    times = [0.0, 1e-4, .03, 1.0, 10.0, 50/m["gap"]]
    returns = []
    for t in times:
        expected = float(np.dot(vecs[0]**2, np.exp(-vals*t)))
        got = float(np.exp(root.log_return(m, t)))
        # The spectral stationary eigenvalue's numerical residual must not be
        # amplified into an alleged long-time discrepancy.
        excess = float(np.dot(vecs[0, 1:]**2, np.exp(-vals[1:]*t)))
        returns.append(dict(t=t, expected=expected, actual=got,
                            absolute_error=abs(expected-got),
                            excess_relative_error=abs(root.return_excess(m,t)/excess-1)
                            if excess > 1e-200 else None))
    _, K1, _ = spin_quotient(np.asarray(J), np.asarray(nu), 1.0)
    E = K1-K
    insertions = []
    for s, t in [(0., 0.), (.01, .2), (.7, .3), (2., 4.)]:
        expected = float((expm(-K*s) @ E @ expm(-K*t))[0, 0])
        actual = float(root.local_insertions(m, s, t))
        insertions.append(dict(s=s, t=t, expected=expected, actual=actual,
                               absolute_error=abs(expected-actual)))
    mean = root.mean_reference(m)
    mean_expected = G[0,0]/(p[0]*(1-p[0]))
    # Nonzero singular values of this chart expose its conditioning; total
    # target rarity alone does not measure numerical difficulty.
    singular = np.linalg.svd(m["U"], compute_uv=False)
    return dict(label=label,n=len(J),pi_target=float(p[0]),
                pi_relative_error=abs(np.exp(m["logpi"])/p[0]-1),
                normalization_log_error=m["normalization_error"],
                canonical_orthogonality_error=float(np.max(np.abs(
                    m["U"].T@m["U"]+m["V"].T@m["V"]-np.eye(len(J))))),
                canonical_pairing_error=float(np.max(np.abs(
                    m["U"].T@m["V"]+m["V"].T@m["U"]))),
                U_min_singular=float(singular[-1]),
                U_condition_number=float(singular[0]/singular[-1]),
                dense_symmetry_error=float(np.max(np.abs(K-K.T))),
                dense_stationarity_error=float(np.max(np.abs(Q@p))),
                gap_expected=float(vals[1]),gap_actual=m["gap"],
                gap_relative_error=abs(m["gap"]/vals[1]-1),
                returns=returns,insertions=insertions,
                mean_expected=float(mean_expected),mean_actual=mean["mean"],
                mean_relative_error=abs(mean["mean"]/mean_expected-1),
                first_coefficient_dense=float((G@E@G)[0,0]))


def fermion_contractions():
    """Check every Nambu entry, not just the summed physical insertion."""
    n = 4
    m = root.model(np.array([-.7, .3, -1.1, .2]), np.array([.6, 1.4, .8, 1.1]))
    size = 1 << n
    annihilators = []
    for j in range(n):
        op = np.zeros((size,size))
        for state in range(size):
            if (state >> j) & 1:
                sign = (-1)**((state & ((1 << j)-1)).bit_count())
                op[state ^ (1 << j), state] = sign
        annihilators.append(op)
    creators = [c.T for c in annihilators]
    H = np.eye(size)*sum(m["c"])
    for i in range(n):
        for j in range(n):
            H -= m["D"][i,j]*(creators[i]@annihilators[j])
            H -= .5*m["A"][i,j]*(creators[i]@creators[j]+annihilators[j]@annihilators[i])
    ops = annihilators+creators
    checks = []
    for s,t in [(0.,0.),(.03,.2),(.7,1.2),(4.,2.)]:
        left, right = expm(-H*s)[0], expm(-H*t)[:,0]
        norm = left@right
        exact = np.array([[left@a@b@right/norm for b in ops] for a in ops])
        got = root.gaussian_contractions(m,s,t)
        checks.append(dict(s=s,t=t,all_entry_absolute_error=float(np.max(np.abs(exact-got)))))
    return checks


def large_charts():
    out=[]
    for n in [32,64,128,256]:
        m=root.model(np.full(n,-.4))
        singular=np.linalg.svd(m["U"],compute_uv=False)
        out.append(dict(n=n,normalization_log_error=m["normalization_error"],
                        U_min_singular=float(singular[-1]),
                        U_condition_number=float(singular[0]/singular[-1]),
                        return_at_zero_absolute_error=abs(np.exp(root.log_return(m,0))-1),
                        long_time_log_error=abs(root.log_return(m,1e4)-m["logpi"])))
    return out


def first_correction_check():
    n=4
    m=root.model(np.full(n,-.4))
    _,K,p=spin_quotient(np.full(n,-.4),np.ones(n))
    _,K1,_=spin_quotient(np.full(n,-.4),np.ones(n),1.)
    vals,V=eigh(K)
    G=(V[:,1:]/vals[1:])@V[:,1:].T
    exact=float((G@(K1-K)@G)[0,0])
    checks=[]
    for u,v in [(32,8),(64,16)]:
        result=root.first_correction(m,u,v,tol=1e-8)
        result["relative_error"]=abs(result["coefficient"]/exact-1)
        checks.append(result)
    return dict(exact=exact,quadratures=checks)


if __name__=="__main__":
    cases=[("uniform_antiferromagnet",[-.4]*8,[1.]*8),
           ("rarer_antiferromagnet",[-1.5]*8,[1.]*8),
           ("mixed_sign_unequal_attempts",[-.7,.3,-1.1,.2,-.5,.8], [.6,1.4,.8,1.1,.7,1.3]),
           ("strong_mixed_sign",[-2.,1.3,-.2,-1.7,.4,1.1,0.,-.9], [.3,2.,.4,1.7,.5,1.2,.9,.7])]
    results=dict(scope="independent spin generator; floating point evidence only",
                 cases=[check_case(*case) for case in cases],
                 all_nambu_contractions=fermion_contractions(),
                 large_chart_checks=large_charts(),
                 first_correction=first_correction_check())
    target=HERE/"audit_gaussian_results.json"
    target.write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
