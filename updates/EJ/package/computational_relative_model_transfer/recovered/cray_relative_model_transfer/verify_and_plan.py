#!/usr/bin/env python3
"""Exact cutoff planner and finite checks for relative Gaussian crossing transfer.

This does NOT implement CRAY's convex integration / conditioned crossing sampler.
The planner assumes certified geometric spectral tails and valid geometry/energy
inputs, as specified in RESULTS.md. Numerical diagnostics are labelled separately.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import random
import math


def ceil_log2(x: F) -> int:
    """Exact ceil(log2(x)); no floating conversion, even for huge inputs."""
    if x <= 0:
        raise ValueError('x must be positive')
    k = x.numerator.bit_length() - x.denominator.bit_length()
    p = F(2**k) if k >= 0 else F(1, 2**(-k))
    return k if x <= p else k + 1


def surprisal_bound(dim: int, center_mean_l1: F, radius: F,
                    covariance_lower: F, covariance_upper: F) -> F:
    """Rational F0 with P(X_D(0) in K) >= exp(-F0), for every cutoff D."""
    if dim < 1 or radius <= 0 or covariance_lower <= 0:
        raise ValueError('invalid geometry / lower covariance bound')
    if covariance_upper < covariance_lower or center_mean_l1 < 0:
        raise ValueError('invalid covariance / mean bound')
    m = center_mean_l1 + dim * radius
    return 1 + m*m/(2*covariance_lower) + dim*(2 + covariance_upper + 1/radius)


def plan_cutoff(dim: int, amplitude: F, radius: F, shift_energy: F,
                f0: F, epsilon: F, max_degree: int = 100000) -> dict:
    """Return exact finite truncation certificate, with no representation of exp(-F0).

    Spectral contract: independent phase-invariant Gaussian blocks, each
    coordinate variance <= amplitude**2 * 4**(-j), all j>=1.
    Geometry: x_star + [-radius,radius]^dim is contained in closure(K),
    and x_star is strictly interior. shift_energy=(x_star-mu)' S0^-1(x_star-mu).
    Input f0 must certify p_D >= exp(-f0) uniformly in D.
    """
    if dim < 1 or amplitude <= 0 or radius <= 0 or shift_energy < 0:
        raise ValueError('invalid model parameters')
    if f0 < 1 or not F(0) < epsilon <= F(1,4):
        raise ValueError('require f0>=1 and epsilon in (0,1/4]')
    tail_log = f0 + ceil_log2(F(256*dim)/epsilon) + 1
    four_power = 4
    for degree in range(1, max_degree+1):
        n = dim*(2*degree+1)
        theta = epsilon/(64*(1+n+shift_energy))
        eta = radius*theta
        tail_radius_squared = 36*amplitude*amplitude*tail_log/four_power
        if tail_radius_squared <= eta*eta:
            beta_upper = 2*n*theta + theta*shift_energy/2
            assert beta_upper <= epsilon/32
            return {
                'degree': degree, 'coefficient_dimension': n,
                'theta': theta, 'uniform_tolerance': eta,
                'tail_radius_squared_upper': tail_radius_squared,
                'tail_log_upper': tail_log, 'beta_upper': beta_upper,
                'tail_failure_over_pD_upper': epsilon/64,
                'relative_probability_error_upper': 5*epsilon/64,
                'event_conditional_tv_upper': 7*epsilon/(64-3*epsilon),
                'f0': f0,
            }
        four_power *= 4
    raise RuntimeError('max_degree reached; increase the explicit cap')


def frac_json(x):
    if isinstance(x, F):
        return f'{x.numerator}/{x.denominator}'
    if isinstance(x, dict):
        return {str(k): frac_json(v) for k,v in x.items()}
    if isinstance(x, list):
        return [frac_json(v) for v in x]
    return x


def run_checks() -> dict:
    checks = {}
    count = 0
    # Exact completed-square identity underlying the sharp contraction factor.
    for theta in [F(1,100),F(1,7),F(1,3),F(1,2),F(3,4)]:
        c = 1-theta
        for h in map(F,[-10,-2,-1,0,1,3,17]):
            for z in [F(-13,4),F(-1),F(0),F(1,3),F(9,2),F(100)]:
                lhs = ((1-c*c)*z*z-2*c*theta*h*z-theta*theta*h*h)/2
                lower = -theta*h*h/(2*(2-theta))
                rhs = theta*(2-theta)*(z-c*h/(2-theta))**2/2
                assert lhs-lower == rhs and rhs >= 0
                count += 1
    checks['completed_square_exact_assertions'] = count

    rng=random.Random(73041)
    geometry_count=0
    for dim in range(1,6):
        for trial in range(80):
            center=[F(rng.randrange(-9,10),3) for _ in range(dim)]
            radius=F(rng.randrange(1,8),5)
            theta=F(rng.randrange(1,9),20)
            eta=theta*radius
            rows=[]
            for _ in range(5):
                a=[F(rng.randrange(-4,5)) for _ in range(dim)]
                if not any(a): a[0]=F(1)
                norm=sum(abs(v) for v in a)
                # Slack is at least radius*norm; the center is strictly interior.
                b=sum(ai*xi for ai,xi in zip(a,center))-radius*norm-F(rng.randrange(0,5),7)
                rows.append((a,b,norm))
            for _ in range(10):
                x=[ci+F(rng.randrange(-20,21),10)*radius for ci in center]
                y=[(1-theta)*xi+theta*ci for xi,ci in zip(x,center)]
                margins=[sum(ai*xi for ai,xi in zip(a,x))-b for a,b,norm in rows]
                new=[sum(ai*yi for ai,yi in zip(a,y))-b for a,b,norm in rows]
                if all(m > -eta*norm for m,(_,_,norm) in zip(margins,rows)):
                    assert all(v>0 for v in new)
                    geometry_count+=1
                if all(m>0 for m in margins):
                    assert all(v>eta*norm for v,(_,_,norm) in zip(new,rows))
                    geometry_count+=1
    checks['polyhedral_containment_exact_assertions']=geometry_count

    plans=[]
    planner_assertions=0
    for bits in [0,5,10,25,50,100,200,1000]:
        u=F(2**bits)
        dim=1
        radius=u  # K=(u,infty), center=2u
        f0=surprisal_bound(dim,2*u,radius,F(1),F(4,3))
        p=plan_cutoff(dim,F(1),radius,4*u*u,f0,F(1,20))
        assert p['tail_radius_squared_upper']<=p['uniform_tolerance']**2
        assert p['relative_probability_error_upper']<F(1,160)
        assert p['event_conditional_tv_upper']<F(1,160)
        planner_assertions += 3
        # Store compact summaries, not enormous probability denominators.
        variance_N=u**4/(288*F(1,20)**2)
        plans.append({'threshold_binary_exponent':bits,
                      'degree':p['degree'],
                      'coefficient_dimension':p['coefficient_dimension'],
                      'f0_bit_length':max(f0.numerator.bit_length(),f0.denominator.bit_length()),
                      'tolerance_binary_exponent_ceiling':ceil_log2(1/p['uniform_tolerance']),
                      'variance_data_lower_bound_log2_ceiling':(ceil_log2(variance_N) if u>=2 else None)})
    for dim in [2,3,8,16]:
        f0=surprisal_bound(dim,F(10*dim),F(1,7),F(1,3),F(3))
        p=plan_cutoff(dim,F(5),F(1,7),F(300*dim),f0,F(1,100))
        assert p['tail_radius_squared_upper']<=p['uniform_tolerance']**2
        assert p['beta_upper']<=F(1,3200)
        planner_assertions+=2
    checks['planner_exact_assertions']=planner_assertions
    checks['adverse_threshold_scaling']=plans

    # Exact rational stable-filter realization of the infinite spectral source.
    import sympy as sp
    C=sp.Matrix([[2,-1],[0,3]])
    I=sp.eye(2)
    U=sp.Matrix([[1,0],[0,1]])
    filter_assertions=0
    for j in range(1,9):
        R=C.row_join(j*I).col_join((-j*I).row_join(C))
        cov=R.inv()*sp.diag(U,U)*R.inv().T/sp.Integer(4)**j
        S=cov[:2,:2]; T=cov[:2,2:]
        assert cov[2:,2:]==S and cov[2:,:2]==-T and T.T==-T
        filter_assertions+=1
        for order in range(1,5):
            assert cov[:order,:order].det()>0
            assert (sp.eye(4)/sp.Integer(4)**j-cov)[:order,:order].det()>0
            filter_assertions+=2
    checks['stable_filter_exact_assertions']=filter_assertions
    checks['total_exact_assertions']=count+geometry_count+planner_assertions+filter_assertions

    # Floating diagnostics only: exact scalar crossing formula evaluated in log domain.
    from scipy.special import log_ndtr
    import numpy as np
    diagnostics=[]
    for u in [2.,5.,10.,20.,100.,1000.]:
        sigma=2/u
        lp0=float(log_ndtr(-u))
        term=(math.log(sigma)-0.5*math.log1p(sigma*sigma)
              -u*u/(2*(1+sigma*sigma))
              +float(log_ndtr(u*sigma/math.sqrt(1+sigma*sigma))))
        lp=float(np.logaddexp(lp0,term))
        ratio=math.exp(lp-lp0)
        certified_lower=math.exp(1.5-2/(u*u))
        assert ratio >= certified_lower*(1-1e-10)
        diagnostics.append({'threshold':u,'omitted_variance':sigma*sigma,
                            'log_baseline_probability':lp0,
                            'actual_probability_ratio':ratio,
                            'analytic_ratio_lower_bound':certified_lower})
    checks['floating_diagnostics_not_interval_certified']=diagnostics
    checks['status']='All listed finite checks passed; general proof and prior compiler not independently verified.'
    return checks


if __name__=='__main__':
    results=run_checks()
    target=Path(__file__).with_name('verification_results.json')
    target.write_text(json.dumps(frac_json(results),indent=2)+'\n')
    print(json.dumps({'exact_assertions':results['total_exact_assertions'],
                      'cutoff_scaling':results['adverse_threshold_scaling'],
                      'floating_diagnostics':len(results['floating_diagnostics_not_interval_certified']),
                      'results':str(target)},indent=2))
