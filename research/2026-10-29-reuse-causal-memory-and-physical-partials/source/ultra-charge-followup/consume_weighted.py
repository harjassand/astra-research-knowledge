"""Consume the weighted exact-charge spectral compiler on a two-charge model.

Float diagnostic of algebra/implementation, not a directed PSD certificate
or a physical-model qualification. The proof is in OPTIMAL_CONE.txt.
"""
import itertools
import json
import time
from pathlib import Path

import cvxpy as cp
import numpy as np
from scipy.linalg import null_space, orth


def main():
    start=time.perf_counter()
    rng=np.random.default_rng(29102026)
    m=8
    C=np.zeros((m,2)); C[:4,0]=1; C[4:,1]=1
    q=np.array([2.,2.])
    Q=null_space(C.T)
    P=Q@Q.T
    raw=rng.normal(size=(m,m))
    U=(raw+raw.T)/np.sqrt(m)
    np.fill_diagonal(U,0.)
    G0=np.diag([1.,.8,1.4,.9,1.1,1.5,.7,1.3])
    L=np.sqrt(G0); Li=np.diag(1/np.diag(L))
    s=cp.Variable(m); gamma=cp.Variable(nonneg=True)
    A=U+cp.diag(s)
    problem=cp.Problem(cp.Minimize(gamma),
                       [Q.T@(gamma*G0-A)@Q >> 0,Q.T@(gamma*G0+A)@Q >> 0])
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
    Av=U+np.diag(s.value)
    B=orth(L@Q); Pi=B@B.T
    Uprime=L@Pi@Li@Av@Li@Pi@L
    whitened=Li@Uprime@Li
    # Choose explicit measured slack; this is FLOATING POINT, not directed.
    realized_gamma=float(np.linalg.norm(whitened,2)+1e-4)
    Gamma=realized_gamma*G0
    X=Gamma/2; Y=Gamma/2; Z=-Uprime/2
    covariance=np.block([[X,Z],[Z,Y]])
    difference=Uprime-Av
    Gi=np.linalg.inv(C.T@C)
    V=difference@C@Gi-.5*C@Gi@C.T@difference@C@Gi
    gauge_reconstruction=C@V.T+V@C.T
    g=.5*np.asarray(s.value)+V@q
    l=np.diag(X)
    states=[]
    for a in itertools.combinations(range(4),2):
        for b in itertools.combinations(range(4,8),2):
            n=np.zeros(m); n[list(a)+list(b)]=1; states.append(n)
    h=.217
    max_channel_error=0.
    for a in states:
        for b in states:
            v=a+b; delta=a-b
            target=np.exp(-.5j*h*(a@U@a-b@U@b)-.5*h*delta@Gamma@delta)
            represented=np.exp(-.5j*h*(a@Uprime@a-b@Uprime@b)+1j*h*g@delta
                               +.5*h*v@X@v-h*l@v-.5*h*delta@Y@delta)
            max_channel_error=max(max_channel_error,abs(target-represented))
    result={'scope':'Nonuniform local dephasing, TWO exactly preserved charges; ideal Gaussian finite-step identity',
            'solver_status':problem.status,'gamma_opt_float':float(gamma.value),
            'gamma_used_float_with_slack':realized_gamma,
            'cov_min_eigen_float':float(np.linalg.eigvalsh(covariance).min()),
            'Q_restriction_error':float(np.linalg.norm(Q.T@(Uprime-Av)@Q)),
            'gauge_reconstruction_error':float(np.linalg.norm(difference-gauge_reconstruction)),
            'finite_step_channel_entry_max_error':float(max_channel_error),
            'occupation_states':len(states),'coherences_checked':len(states)**2,
            'seconds':time.perf_counter()-start,
            'U':U.tolist(),'C':C.tolist(),'q':q.tolist(),'G0':G0.tolist(),
            's':s.value.tolist(),'Uprime':Uprime.tolist(),'g':g.tolist()}
    Path(__file__).with_name('WEIGHTED_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('U','C','q','G0','s','Uprime','g')},indent=2))


if __name__=='__main__':
    main()
