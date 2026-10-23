#!/usr/bin/env python3
"""Independent diagnostics for the residual completion; proof is in the note.

Exact rational sharpness identities are checked first. Floating experiments
test implementation/algebra only and do not certify the theorem.
"""
from fractions import Fraction as F
import json
import pathlib
import resource
import time
import numpy as np


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    wall = time.perf_counter()
    cpu = time.process_time()
    exact = []
    # At z/r=1, the optimal 2x2 matrix has a=r/3, b^2=8r^2/9.
    # Its larger eigenvalue is 5r/3; no irrational b is needed to
    # check the characteristic identity or the first-column norm.
    for r in (F(1), F(3, 7), F(17, 5)):
        z, a, b2, lam = r, r / 3, 8 * r * r / 9, 5 * r / 3
        require(a*a+b2 == r*r, 'sharpness residual identity')
        require((lam-a)*(lam-z)-b2 == 0, 'sharpness characteristic identity')
        require(lam >= a and lam >= z, 'sharpness top eigenvalue')
        exact.append({'r':str(r), 'z':str(z), 'a':str(a),
                      'b_squared':str(b2), 'lambda':str(lam)})
    # Degenerate limits: no first-column error -> e=z; zero diagonal
    # error has sharp e^2=4r^2/3 with a^2=r^2/3,b^2=2r^2/3.
    require(F(1,3)+F(2,3)==1, 'z=0 residual identity')
    require(F(4,3)-F(2,3)-F(2,3)==0, 'z=0 characteristic identity')

    rng = np.random.default_rng(20261021)
    max_budget_excess = -float('inf')
    max_relation_residual = 0.0
    max_moment_error = 0.0
    max_probe_excess = -float('inf')
    max_exact_budget_excess = -float('inf')
    max_frobenius_excess = -float('inf')
    cases = 0
    for n in range(2, 17):
        for k in sorted({1, min(2,n), min(4,n), min(6,n), n}):
            for _ in range(6):
                H = rng.normal(size=(n,n))
                A = (H+H.T)/2
                A *= 0.3/max(1e-30,np.linalg.norm(A,2))
                M = np.linalg.norm(A,2)
                Q0, _ = np.linalg.qr(rng.normal(size=(n,k)), mode='reduced')
                W = rng.normal(size=(k,k))
                V = Q0 @ (np.eye(k)+0.002*W/max(1,np.linalg.norm(W,2)))
                a = rng.normal(size=k)*0.15
                b = rng.uniform(0.025,0.1,size=max(0,k-1))
                J = np.diag(a)+np.diag(b,1)+np.diag(b,-1)
                K = np.linalg.norm(J,2)
                G = V.T@V
                vals,U = np.linalg.eigh(G)
                Q = V @ ((U/np.sqrt(vals))@U.T)
                gamma = np.linalg.norm(G-np.eye(k),'fro')
                require(gamma<1, 'Gram admission')
                d = gamma/(1+np.sqrt(1-gamma))
                P = np.eye(k); P[-1,-1]=0
                r0 = np.linalg.norm((A@V-V@J)@P,'fro')
                xi = abs(J[-1,-1]-V[:,-1]@A@V[:,-1])
                r = 0.0 if k==1 else r0+(M+K)*d
                z = xi+M*d*(1+np.sqrt(1+gamma))
                budget = (z+2*np.sqrt(z*z+3*r*r))/3
                D = J-Q.T@A@Q
                R = (np.eye(n)-Q@Q.T)@A@Q@P
                E = Q@D@Q.T-R@Q.T-Q@R.T
                B = A+E
                rv = (np.eye(n)-Q@Q.T)@A@Q[:,-1]
                relation = B@Q-Q@J-np.outer(rv,np.eye(k)[-1])
                actual = np.linalg.norm(E,2)
                max_budget_excess=max(max_budget_excess,actual-budget)
                max_relation_residual=max(max_relation_residual,np.linalg.norm(relation,'fro'))
                rex = np.linalg.norm((A@Q-Q@J)@P,'fro')
                zex = abs(D[-1,-1])
                budget_exact = (zex+2*np.sqrt(zex*zex+3*rex*rex))/3
                max_exact_budget_excess=max(max_exact_budget_excess,actual-budget_exact)
                max_frobenius_excess=max(max_frobenius_excess,
                    np.linalg.norm(E,'fro')**2-(2*rex*rex+zex*zex))
                # Bound coefficients used in the analytic argument.
                require(np.linalg.norm(Q-V,'fro')<=d+1e-12, 'polar perturbation')
                require(np.linalg.norm((A@Q-Q@J)@P,'fro')<=r+1e-12, 'first residual')
                require(abs(D[-1,-1])<=z+1e-12, 'last diagonal')
                require(actual<=budget+1e-11, 'operator completion budget')
                require(np.linalg.norm(relation,'fro')<1e-11,'exact recurrence diagnostic')
                # Moment tests use bounded-degree examples to avoid power
                # conditioning obscuring the algebraic identity.
                if k<=6:
                    w=Q[:,0].copy(); y=np.eye(k)[:,0].copy()
                    for ell in range(2*k):
                        err=abs(Q[:,0]@w-y[0])
                        max_moment_error=max(max_moment_error,err)
                        require(err<2e-10,'moment identity diagnostic')
                        w=B@w; y=J@y
                u=V[:,0]/np.linalg.norm(V[:,0])
                H=rng.normal(size=(n,n)); ev,Z=np.linalg.eigh((H+H.T)/2)
                Pi=Z[:,:n//2]@Z[:,:n//2].T
                pdiff=abs(u@Pi@u-Q[:,0]@Pi@Q[:,0])
                pbound=np.linalg.norm(u-V[:,0])+d
                max_probe_excess=max(max_probe_excess,pdiff-pbound)
                cases+=1

    receipt={
        'status':'PASS',
        'exact_rational_sharpness_cases':exact,
        'floating_cases':cases,
        'max_operator_norm_minus_reported_budget':max_budget_excess,
        'max_operator_norm_minus_exact_rz_budget':max_exact_budget_excess,
        'max_frobenius_squared_minus_exact_bound':max_frobenius_excess,
        'max_recurrence_residual_frobenius':max_relation_residual,
        'max_moment_identity_absolute_error':max_moment_error,
        'max_probe_discrepancy_minus_bound':max_probe_excess,
        'wall_seconds':time.perf_counter()-wall,
        'cpu_seconds':time.process_time()-cpu,
        'peak_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1024 if __import__('sys').platform.startswith('linux') else 1),
        'rss_units':'native field is Linux KiB or macOS bytes; peak_rss_bytes is normalized',
        'platform':__import__('sys').platform,
        'scope':'Exact sharpness identities plus floating algebra diagnostics; analytic note supplies the theorem.'
    }
    out=pathlib.Path(__file__).resolve().parents[1]/'results'/'residual_construction_checks.json'
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
