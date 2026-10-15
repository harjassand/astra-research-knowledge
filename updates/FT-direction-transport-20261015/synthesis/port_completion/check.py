#!/usr/bin/env python3
"""Task-restricted adjoint validation: exact algebra and synthetic checks.

No physical data, experimental noise calibration or novelty certification.
Imports the supplied implementation without executing its source-writing main.
Writes only beside this file.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.stats import chi2

HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'sources/closure/closure_experiment.py'
spec=importlib.util.spec_from_file_location('incoming_port',SRC)
inc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(inc)
RNG=np.random.default_rng(202610153)


def scalar(v): return float(np.asarray(v).squeeze())


def main():
    results={'scope':'Internal exact/synthetic checks only; no laboratory observations',
             'seed':202610153}
    # Reconstruct the source's exact missing-support pair with rational algebra.
    I=sp.eye(5); b,c=I[:,0],I[:,1]; P=I[:,[2,4]]; v=I[:,0]-I[:,3]
    source=[]
    for sign in [-1,1]:
        A=I+sign*I[:,1]*I[:,3].T
        M=A.inv()*sp.Matrix.hstack(b,P,c)
        lam=A.T.inv()*c
        grad=-(v.T*A.inv()*b)[0]*(v.T*lam)[0]
        p=sp.symbols('p',nonnegative=True)
        J=sp.factor((c.T*(A+p*v*v.T).inv()*b)[0])
        assert grad==-sign
        assert J==-sign*p/(1+2*p)
        source.append({'sign':sign,'response':str(M),'gradient':str(grad),'finite_action':str(J)})
    assert source[0]['response']==source[1]['response']
    results['source_counterexample_exact']=source

    # Bounded stable rank-two obstruction, independent of large conditioning.
    n=9; eye=sp.eye(n); cc=eye[:,0]; dd=eye[:,8]
    U=eye[:,:6]; amplitude=sp.Rational(1,2)
    hard=[]
    for sign in [-1,1]:
        A=eye+sign*amplitude*cc*dd.T
        assert A.inv()==eye-sign*amplitude*cc*dd.T
        assert A.inv()*U==U
        assert (A-A.T).rank()==2
        target=(cc.T*A.inv()*dd)[0]
        assert target==-sign*amplitude
        hard.append({'sign':sign,'target_response':str(target),
                     'skew_rank':2,'minimum_symmetric_eigenvalue':'3/4',
                     'inverse_formula_verified':True})
    results['stable_rank_two_hidden_direction']={'state_dimension':n,
        'queried_source_dimension':6,'records':hard,'entire_measured_columns_identical':True}

    # Port completion and hidden-defect target identity for arbitrary accretive A.
    max_port_error=max_defect_identity_error=0.
    max_energy_violation=-float('inf')
    max_robust_violation=-float('inf')
    for _ in range(48):
        n,k=9,2
        X=RNG.normal(size=(n,n))
        R=X@X.T+np.eye(n)
        ports=np.arange(k)
        Pn=np.eye(n)[:,ports]
        Z=RNG.normal(size=(k,k)); K=Z-Z.T
        A0=R+Pn@K@Pn.T
        c0=RNG.normal(size=n)
        Y0=np.linalg.solve(A0,Pn); z0=np.linalg.solve(A0,c0)
        estimate,_=inc.port_complete(Pn.T@Y0,Y0,z0,ports)
        max_port_error=max(max_port_error,np.linalg.norm(estimate-np.linalg.solve(A0.T,c0)))
        W=RNG.normal(size=(n,n)); hidden=.15*(W-W.T)
        A=A0+hidden
        Y=np.linalg.solve(A,Pn); z=np.linalg.solve(A,c0)
        H=Pn.T@Y
        estimate,D=inc.port_complete(H,Y,z,ports)
        surrogate=A+Pn@D@Pn.T
        E=A.T-surrogate
        truth=np.linalg.solve(A.T,c0)
        f=RNG.normal(size=n)
        yf=np.linalg.solve(A,f)
        lhs=float(f@(truth-estimate)); rhs=float(-yf@E@estimate)
        max_defect_identity_error=max(max_defect_identity_error,abs(lhs-rhs))
        m=float(np.linalg.eigvalsh(R).min())
        tau=float(np.linalg.norm(E@estimate))
        robust=np.linalg.norm(f)*tau/m
        max_robust_violation=max(max_robust_violation,abs(lhs)-robust)
        h=A@estimate
        max_energy_violation=max(max_energy_violation,np.linalg.norm(estimate)**2-float(h@estimate)/m)
    assert max_port_error<2e-12 and max_defect_identity_error<2e-12
    assert max_robust_violation<1e-10 and max_energy_violation<1e-10
    results['port_and_defect_checks']={'instances':48,'maximum_exact_port_error':max_port_error,
        'maximum_hidden_defect_identity_error':max_defect_identity_error,
        'largest_robust_bound_violation':max_robust_violation,
        'largest_source_work_norm_bound_violation':max_energy_violation}

    # Physical-form audit on a plant with hidden skew and fixed candidate.
    r=32; n=r+1; c0=np.eye(n)[:,0]; Q=np.eye(n)[:,1:]
    h=.4*Q[:,0]
    d=RNG.normal(size=r); d/=np.linalg.norm(d)
    M=np.eye(n)+np.outer(c0,h)+np.outer(h,c0)+.04*np.outer(c0,Q@d)
    A=np.linalg.inv(M)
    assert np.linalg.eigvalsh((A+A.T)/2).min()>.2
    estimate=M@c0
    truth=M.T@c0
    g=Q.T@(estimate-truth)
    q=16; delta=.05; amp=1.
    Xi=RNG.normal(size=(q,r))
    L=np.maximum(1.,np.linalg.norm(Xi,axis=1)/amp)
    sources=Q@((Xi/L[:,None]).T)
    observations=c0@np.linalg.solve(A,sources)
    predicted=estimate@sources
    defects=L*(predicted-observations)
    assert np.max(np.abs(defects-Xi@g))<1e-12
    # Acquired deterministic per-profile scalar error bound, chosen here.
    eps=1e-4
    scalar_noise=-eps*np.sign(defects)
    observed_defects=defects+L*scalar_noise
    reconstructed_noise_bound=eps*np.linalg.norm(L)
    lower=float(chi2.ppf(delta,q))
    upper=(np.linalg.norm(observed_defects)+reconstructed_noise_bound)/np.sqrt(lower)
    selected_force=Q[:,0]
    center=float(estimate@selected_force)
    actual=float(truth@selected_force)
    margin=center-upper*np.linalg.norm(selected_force)
    assert margin>0 and actual>0
    assert abs(actual-center)<=upper+1e-12
    results['amplitude_capped_task_audit']={'task_rank':r,'audit_profiles':q,
        'failure_probability':delta,'true_task_residual_norm':float(np.linalg.norm(g)),
        'certified_upper_in_this_draw':float(upper),
        'per_profile_assumed_error_bound':eps,'reconstructed_noise_bound':float(reconstructed_noise_bound),
        'source_norm_cap':amp,'total_squared_source_amplitude':float(np.linalg.norm(sources)**2),
        'unscaled_total_squared_source_amplitude':float(np.linalg.norm(Xi)**2),
        'candidate_direction_predicted_gain':center,'actual_gain':actual,
        'lower_first_order_gain_in_this_draw':float(margin),
        'warning':'Synthetic assumed errors; one direct chosen-direction tangent probe is a cheaper comparator for this single decision.'}

    # The confidence proof is exact chi-square; finite trials only check code.
    trials=6000; q=8; r=32; delta=.05
    fixed=RNG.normal(size=r); fixed/=np.linalg.norm(fixed)
    sketches=RNG.normal(size=(trials,q,r))@fixed
    bounds=np.linalg.norm(sketches,axis=1)/np.sqrt(chi2.ppf(delta,q))
    coverage=float(np.mean(bounds>=1.))
    assert .92<coverage<.98
    results['finite_coverage_diagnostic']={'trials':trials,'q':q,'task_rank':r,
        'theoretical_coverage':1-delta,'observed_coverage':coverage,
        'scope':'Synthetic diagnostic, not empirical calibration of noise/plant independence.'}

    # Amplitude normalization exposes the dimension-dependent precision floor.
    floors=[]
    q=16; delta=.05; sigma=.001
    for rank in [4,16,64,256]:
        xi=RNG.normal(size=(q,rank))
        scaling=np.maximum(1.,np.linalg.norm(xi,axis=1))
        floor=sigma*np.linalg.norm(scaling)/np.sqrt(chi2.ppf(delta,q))
        floors.append({'task_rank':rank,'audit_profiles':q,
            'squared_reconstruction_scaling':float(scaling@scaling),
            'noise_term_in_norm_upper_bound':float(floor),
            'noise_term_divided_by_sigma_sqrt_rank':float(floor/(sigma*np.sqrt(rank)))})
    assert floors[-1]['noise_term_in_norm_upper_bound']>floors[0]['noise_term_in_norm_upper_bound']
    results['precision_cost_frontier']={'assumed_per_profile_error':sigma,'records':floors,
        'scope':'Fixed capped injection amplitude; repeat/precision cost cannot be omitted.'}

    # Sharp projected-ball decision interval, independently of random audit.
    eta=.5; known=np.array([.1,-.15,.05]); remaining=np.sqrt(eta**2-known@known)
    candidate=RNG.normal(size=12)
    radius=np.linalg.norm(candidate[3:])*remaining
    extreme=remaining*candidate[3:]/np.linalg.norm(candidate[3:])
    vplus=np.r_[known,extreme]; vminus=np.r_[known,-extreme]
    assert abs(np.linalg.norm(vplus)-eta)<1e-12
    assert abs(candidate@vplus-candidate@vminus-2*radius)<1e-12
    results['projected_ball_interval']={'known_projection':known.tolist(),'prior_norm_bound':eta,
        'remaining_radius':float(remaining),'candidate_half_width':float(radius),
        'attained_width':float(candidate@vplus-candidate@vminus)}
    results['all_assertions_passed']=True
    (HERE/'check_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
