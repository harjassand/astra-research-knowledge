"""Independent audit of complex Hermitian cases and a finite-precision counterexample.
Does not edit the implementation under audit.
"""
import sys
import json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'robust_computation'))
from demand_solver import AcquiredSolver,hermitian


def run(directed):
    rng=np.random.default_rng(191+directed)
    n,k,rank=11,3,2
    mu,upper,eta,tau,zeta=.7,2.4,.002,.035,.001
    alpha=np.array([1.,1.1,.9])
    U=np.linalg.qr(rng.normal(size=(n,rank))+1j*rng.normal(size=(n,rank)))[0]
    C=[]
    A=[]
    for j in range(k):
        R=np.linalg.qr(rng.normal(size=(rank,rank))+1j*rng.normal(size=(rank,rank)))[0]
        core=R@np.diag([.25+.1*j,.6+.1*j])@R.conj().T
        c=alpha[j]*np.eye(n)+U@core@U.conj().T
        F=hermitian(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
        F*=zeta/np.linalg.norm(F,2)
        C.append(c);A.append(c+F)
    C=np.array(C);A=np.array(A)
    calls=0
    def action(j,v):
        nonlocal calls
        calls+=1
        # Both a changing orthogonal error and impossible imaginary parallel
        # error. The latter exercises the Hermitian noise projection.
        w=rng.normal(size=n)+1j*rng.normal(size=n)
        w/=np.linalg.norm(w)
        e=.8*w+.6j*v/np.linalg.norm(v)
        e*=eta*np.linalg.norm(v)/np.linalg.norm(e)
        return A[j]@v+e
    observations=[]
    def audit(model):
        B=np.array([alpha[j]*np.eye(n)+model.q@model.d[j]@model.q.conj().T for j in range(k)])
        eigs=np.linalg.eigvalsh(B)
        observations.append((float(eigs.min()),float(eigs.max()),float(np.linalg.norm(model.q.conj().T@model.q-np.eye(model.rank)))))
        return float(np.sum(np.abs(B-C)**2))
    solver=AcquiredSolver(n,alpha,mu,upper,eta,tau,action,directed=directed,audit=audit)
    max_certificate_slack=-float('inf')
    for t in range(30):
        theta=rng.dirichlet(np.ones(k))
        b=rng.normal(size=n)+1j*rng.normal(size=n)
        if solver.rank and t%3==0:
            b+=solver.q@rng.normal(size=solver.rank)
        x,c=solver.solve(theta,b)
        truth=np.linalg.solve(np.einsum('j,jab->ab',theta,A),b)
        error=float(np.linalg.norm(x-truth)/np.linalg.norm(truth))
        max_certificate_slack=max(max_certificate_slack,error-c['certificate'])
    min_progress=float('inf')
    for e in solver.events:
        a=e['residual_norm']
        lower=(a-eta)*(a-eta-2*zeta)/e['coefficient_norm_squared']
        actual=e['potential_before']-e['potential_after']
        min_progress=min(min_progress,actual-lower)
    return dict(directed=directed,n=n,k=k,complex_Hermitian=True,updates=solver.count.updates,
                retained_dimension=solver.rank,source_calls=calls,counted_source_calls=solver.count.source_actions,
                maximum_error_minus_reported_certificate=max_certificate_slack,
                minimum_progress_minus_theorem_lower_bound=min_progress,
                minimum_model_eigenvalue=min(t[0] for t in observations),
                maximum_model_eigenvalue=max(t[1] for t in observations),
                maximum_basis_orthogonality_error=max(t[2] for t in observations))


def guard_band_counterexample():
    # An outward norm enclosure can reject a mathematically acceptable iterate.
    # The exact observed residual is zero, but its allowed numerical upper bound
    # is larger than tau. Rejection alone cannot justify a tau-sized correction.
    tau=.06
    exact_requested_residual=0.
    upper=.061
    return dict(tau=tau,exact_requested_residual=exact_requested_residual,
                outward_upper_bound=upper,rejected_by_upper_test=upper>tau,
                claimed_large_defect=exact_requested_residual>tau,
                necessary_fix='Bound enclosure width omega and subtract it from the failed-check threshold, or use a guard band/refinement rule.')


def cap_checks():
    calls=0
    def action(j,v):
        nonlocal calls
        calls+=1
        return (2+j)*v
    solver=AcquiredSolver(1,[1.,1.],1.,3.,0.,.1,action,directed=2)
    zero,_=solver.solve([1.,0.],[0.],max_updates=0)
    assert calls==0 and not np.linalg.norm(zero)
    try:
        solver.solve([1.,0.],[1.],max_updates=0)
        raise AssertionError('Zero cap should reject a needed update.')
    except RuntimeError:
        pass
    assert solver.count.updates==0 and solver.count.directed_experiments==0
    first,_=solver.solve([1.,0.],[1.],max_updates=1)
    assert solver.count.updates==1 and abs(first[0]-.5)<1e-12
    again,_=solver.solve([1.,0.],[2.],max_updates=1)
    assert solver.count.updates==1 and abs(again[0]-1.)<1e-12
    try:
        solver.solve([0.,1.],[1.],max_updates=1)
        raise AssertionError('Lifetime cap should include previous requests.')
    except RuntimeError:
        pass
    assert solver.count.updates==1
    final,_=solver.solve([0.,1.],[1.])
    assert solver.count.updates==2 and abs(final[0]-1/3)<1e-12
    for invalid in (-1,1.5):
        try:
            solver.solve([1.,0.],[1.],max_updates=invalid)
            raise AssertionError('Invalid cap accepted.')
        except ValueError:
            pass
    return dict(default_uncapped=True,explicit_zero_cap_preserves_model=True,
                zero_rhs_needs_no_action=True,accepted_answer_at_cap_allowed=True,
                lifetime_cap_includes_prior_requests=True,invalid_caps_rejected=True)


results=dict(complex_runs=[run(0),run(2)],finite_precision_guard_band=guard_band_counterexample(),
             cap_checks=cap_checks())
Path(__file__).with_name('central_audit_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
