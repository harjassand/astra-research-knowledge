"""Construct exact family and numerically optimize the charge-quotient cone.

Floating point SDP outputs are exploratory, not exact PSD certificates.
The Hadamard identity in CONSTRUCTION.md is the exact all-size argument.
"""
import itertools
import json
import time
from pathlib import Path

import cvxpy as cp
import numpy as np
from scipy.linalg import hadamard, null_space


def sector_states(m, k):
    ans = []
    for occ in itertools.combinations(range(m), k):
        a = np.zeros(m)
        a[list(occ)] = 1
        ans.append(a)
    return np.asarray(ans)


def optimize(U, projected, gauges):
    m = len(U)
    Q = null_space(np.ones((1, m))) if projected else np.eye(m)
    P = Q @ Q.T
    gamma = cp.Variable(nonneg=True)
    d = cp.Variable(m)
    s = cp.Variable(m) if gauges else np.zeros(m)
    v = cp.Variable(m) if gauges and projected else np.zeros(m)
    one = np.ones((m, 1))
    Up = U + cp.diag(s)
    if projected and gauges:
        Up = Up + one @ cp.reshape(v, (1, m), order='C') + cp.reshape(v, (m, 1), order='C') @ one.T
    block = cp.bmat([[gamma*np.eye(Q.shape[1])-Q.T@cp.diag(d)@Q, .5*Q.T@Up],
                     [.5*Up@Q, cp.diag(d)]])
    problem = cp.Problem(cp.Minimize(gamma), [d >= 1e-7, block >> 0])
    start = time.perf_counter()
    problem.solve(solver='CLARABEL', tol_gap_abs=1e-9, tol_feas=1e-9,
                  tol_gap_rel=1e-9, max_iter=200)
    seconds = time.perf_counter()-start
    Upv = np.asarray(Up.value)
    dv = np.asarray(d.value)
    S = gamma.value*P-np.diag(dv)-.25*Upv@np.diag(1/dv)@Upv
    margin = np.linalg.eigvalsh(Q.T@S@Q).min()
    return {'status':problem.status, 'gamma':float(gamma.value),
            'min_projected_margin':float(margin), 'd_min':float(dv.min()),
            'seconds':seconds, 'd':dv.tolist(), 'Uprime':Upv.tolist()}


def exact_family(m):
    W = hadamard(m).astype(float)/np.sqrt(m)
    P = np.eye(m)-np.ones((m,m))/m
    Up = P@W@P
    D = .5*np.eye(m)
    base = D+.5*Up@Up
    R = .5*P@W@(np.eye(m)-P)@W@P
    # Q-sector identity and finite-time channel-entry equality; no Monte Carlo.
    states = sector_states(m, min(2,m-1))
    h = .371
    # Charge gauge U' = U + 1v^T + v1^T. Compensate by g = k v.
    one = np.ones(m)
    v = -(W@one)/m + (one@W@one)/(2*m*m)*one
    k = min(2,m-1)
    g = k*v
    maxerr = 0.
    for a in states:
        for b in states:
            delta = a-b
            target = np.exp(-.5j*h*(a@W@a-b@W@b)-.5*h*delta@P@delta)
            represented = np.exp(-.5j*h*(a@Up@a-b@Up@b)+1j*h*g@delta
                                 -.5*h*delta@(base+R)@delta)
            maxerr = max(maxerr,abs(target-represented))
    # Distance from the space of additive pair coefficients: nonzero forbids
    # reduction to a single-particle potential within the k=2 sector.
    pairs = list(itertools.combinations(range(m),2))
    design = np.asarray([[float(i in pair) for i in range(m)] for pair in pairs])
    values = np.asarray([W[i,j] for i,j in pairs])
    coeff = np.linalg.lstsq(design,values,rcond=None)[0]
    irreducible = float(np.linalg.norm(design@coeff-values))
    return {'m':m, 'gamma':1., 'ordinary_edgewise_threshold':float((m-1)/np.sqrt(m)),
            'R_min_eigen':float(np.linalg.eigvalsh(R).min()),
            'projected_identity_error':float(np.linalg.norm(P@(base+R-P)@P)),
            'finite_step_channel_entry_max_error':float(maxerr),
            'all_k2_entries_checked':len(states)**2,
            'k2_pair_potential_residual':irreducible}


def fair_edgewise(m):
    """Give the pairwise incumbent the SAME fixed-charge gauge freedom."""
    W = hadamard(m).astype(float)/np.sqrt(m)
    pairs = list(itertools.combinations(range(m),2))
    v = cp.Variable(m)
    w = cp.Variable(len(pairs),nonneg=True)
    gamma = cp.Variable(nonneg=True)
    incidence = np.asarray([[float(i in pair) for pair in pairs] for i in range(m)])
    coeff = np.asarray([W[i,j] for i,j in pairs])
    shifted = coeff+incidence.T@v
    problem = cp.Problem(cp.Minimize(gamma),[shifted<=w,-shifted<=w,incidence@w<=gamma])
    start = time.perf_counter()
    problem.solve(solver='HIGHS')
    return {'m':m,'gauge_optimized_edgewise_threshold':float(gamma.value),
            'status':problem.status,'seconds':time.perf_counter()-start,
            'exact_all_gauges_dual_lower_bound':float((m*m-4*m+2)*(m-2)/(m*m*np.sqrt(m))),
            'new_global_sufficient_threshold':1.}


def general_sector_cone(U):
    """No inverse or positive-diagonal restriction; X can use charge gauges."""
    m = len(U)
    Q = null_space(np.ones((1,m)))
    P = Q@Q.T
    one = np.ones((m,1))
    gamma = cp.Variable(nonneg=True)
    d = cp.Variable(m)
    s = cp.Variable(m)
    vx = cp.Variable((m,1))
    vy = cp.Variable((m,1))
    vu = cp.Variable((m,1))
    X = cp.diag(d)+one@vx.T+vx@one.T
    Up = U+cp.diag(s)+one@vu.T+vu@one.T
    Y = gamma*P-X+one@vy.T+vy@one.T
    cov = cp.bmat([[X,-.5*Up],[-.5*Up,Y]])
    problem = cp.Problem(cp.Minimize(gamma),[cov >> 0])
    start = time.perf_counter()
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,
                  tol_feas=1e-9,max_iter=200)
    Xv=np.asarray(X.value); Yv=np.asarray(Y.value); Uv=np.asarray(Up.value)
    return {'gamma':float(gamma.value),'status':problem.status,
            'seconds':time.perf_counter()-start,
            'd_min':float(np.asarray(d.value).min()),
            'cov_min_eigen':float(np.linalg.eigvalsh(cov.value).min()),
            'projected_noise_error':float(np.linalg.norm(Q.T@(Xv+Yv-float(gamma.value)*P)@Q)),
            'X':Xv.tolist(),'Y':Yv.tolist(),'Uprime':Uv.tolist(),
            'l':(np.asarray(d.value)+2*2*np.asarray(vx.value).ravel()).tolist(),
            'g':(.5*np.asarray(s.value)+2*np.asarray(vu.value).ravel()).tolist(),
            'charge':2}


def spectral_cone(U):
    m=len(U)
    Q=null_space(np.ones((1,m)))
    s=cp.Variable(m)
    gamma=cp.Variable(nonneg=True)
    compressed=Q.T@(U+cp.diag(s))@Q
    problem=cp.Problem(cp.Minimize(gamma),[gamma*np.eye(m-1)-compressed >> 0,
                                            gamma*np.eye(m-1)+compressed >> 0])
    start=time.perf_counter()
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
    return {'gamma':float(gamma.value),'status':problem.status,
            'seconds':time.perf_counter()-start,'s':np.asarray(s.value).tolist(),
            'actual_compressed_spectral_radius':float(np.linalg.norm(compressed.value,2))}


def main():
    start = time.perf_counter()
    result = {'scope':'Restricted physical-noise Gaussian-trajectory cone; no novelty/runtime advantage claim',
              'exact_family':[exact_family(m) for m in (4,16)],
              'fair_edgewise_comparison':[fair_edgewise(m) for m in (4,16,64)],
              'optimization':[]}
    rng = np.random.default_rng(20261029)
    m = 8
    noise = rng.normal(size=(m,m)); noise = .5*(noise+noise.T)/np.sqrt(m)
    np.fill_diagonal(noise,0.)
    a = rng.normal(size=m)
    # Large charge gauge has exactly no interacting content within a fixed sector.
    U = noise + np.outer(np.ones(m),a)+np.outer(a,np.ones(m))
    for name,projected,gauges in [('full_raw',False,False),('full_diag',False,True),
                                  ('sector_raw',True,False),('sector_gauges',True,True)]:
        row = optimize(U,projected,gauges); row['case']=name
        result['optimization'].append(row)
    result['general_sector_cone']=[]
    result['spectral_cone']=[]
    for name,mat in [('random8',U),('hadamard4',hadamard(4)/2),('hadamard16',hadamard(16)/4)]:
        row=general_sector_cone(mat); row['case']=name
        result['general_sector_cone'].append(row)
        row=spectral_cone(mat); row['case']=name
        result['spectral_cone'].append(row)
    result['total_seconds']=time.perf_counter()-start
    out = Path(__file__).with_name('RESULT.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'optimization':[{k:v for k,v in r.items() if k not in ('d','Uprime')}
                                              for r in result['optimization']],
                     'general_sector_cone':[{k:v for k,v in r.items() if k not in ('X','Y','Uprime','l','g')}
                                            for r in result['general_sector_cone']]},indent=2))


if __name__ == '__main__':
    main()
