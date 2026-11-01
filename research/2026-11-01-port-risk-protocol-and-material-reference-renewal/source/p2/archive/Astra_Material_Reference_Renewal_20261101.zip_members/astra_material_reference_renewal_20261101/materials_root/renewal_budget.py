"""Precision versus exposure in repeated finite-noise reference renewal.

The bound covers all completed renewal rounds, not just the terminal sample.
This is an architecture-specific sufficient feasibility calculation; no universal
lower bound or hardware advantage is asserted.
"""
import json
import math
import os
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm
from finite_observer import variance as finite_observer_variance

HERE=Path(__file__).resolve().parent
OUT=HERE/'results';OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def factor(z):
    return 1-z/3+z*z/12 if z<1e-4 else 2*(z+math.expm1(-z))/z**2


def cyclic_mean_variance(rounds):
    n=rounds
    return 4*n/3-4/9+(-1/8)**(n-1)/27-(1/64)**(n-1)/432


def cyclic_mean_bias(rounds):
    return 2*rounds-4/9+(-1/8)**(rounds-1)/36


def proof_check():
    A=np.array([[0,.5,.5],[0,.25,.75],[0,.375,.625]])
    B=np.array([[1,0,0],[.5,1,0],[.75,.5,1]])
    v=np.ones(3)/3;w=np.array([0,1/3,2/3]);q=v-w
    cov=np.zeros((3,3));bias=np.zeros(3);err=0.;max_disagreement_var=0.
    for n in range(1,1001):
        cov=A@cov@A.T+B@B.T
        bias=A@bias+B@np.ones(3)
        err=max(err,abs(v@cov@v-cyclic_mean_variance(n)),
                abs(v@bias-cyclic_mean_bias(n)))
        max_disagreement_var=max(max_disagreement_var,float(q@cov@q))
    assert err<1e-8
    assert max_disagreement_var<=4/27+1e-10
    return dict(maximum_closed_form_residual=err,
                maximum_disagreement_variance_coefficient=max_disagreement_var,
                bound_disagreement_variance_coefficient=4/27)


def required_window(allowed_sd, snapshot_sd, correlation_time, readout_sd, spacing):
    # Optimal GLS for the ACTUAL finite two-polarity experiment, including
    # arbitrary initial states, an unknown offset, and noisy endpoint readings.
    def enough(n):
        return finite_observer_variance(n,spacing,correlation_time,snapshot_sd,readout_sd)<=allowed_sd**2
    hi=1
    while not enough(hi):hi*=2
    lo=0
    while hi-lo>1:
        mid=(hi+lo)//2
        if enough(mid):hi=mid
        else:lo=mid
    return 2*hi*spacing, 2*(hi+1)


def budget():
    # Declared normalized design example; not sensor performance data.
    sigma0=1e-9;tau=.001;precision=10e-9;lam=1e-5
    read_sd=.2*sigma0;spacing=.001
    overhead=.006
    delta_R=.0025;delta_D=.0025;delta_overlap=.01
    rows=[]
    for M in [1,10,100,300,500,700,1000,3000,10000]:
        zR=norm.isf(delta_R/4)
        zD=norm.isf(delta_D/(2*M))
        L=math.sqrt(4*M/3)*zR+math.sqrt(4/27)*zD
        allowed=precision/L
        lo,reads=required_window(allowed,sigma0,tau,read_sd,spacing)
        hi=-math.log1p(-delta_overlap)/(6*M*lam)-overhead
        # Ordinary coded-reference comparator: independent replacement errors
        # about a retained true setpoint and a working dimensional standard.
        zc=norm.isf((delta_R+delta_D)/(2*M))
        allowed_code=precision*math.sqrt(3)/zc
        tcode,code_reads=required_window(allowed_code,sigma0,tau,read_sd,spacing)
        # Even an ideal continuously read OU meter with no readout error has
        # conditional Fisher information T/(2 sigma0^2 tau). Combined with the
        # exact terminal variance, this yields a NECESSARY observation time in
        # this model; it is not merely failure of a sufficient union bound.
        zterm=norm.isf((delta_R+delta_D)/2)
        necessary=2*sigma0**2*tau*cyclic_mean_variance(M)*zterm**2/precision**2
        rows.append(dict(rounds=M,comparison_copy_sd_limit_m=allowed,
                         comparison_minimum_observation_s=lo,
                         maximum_observation_s_from_overlap=hi,
                         comparison_sufficient_certificate_feasible=bool(0<=lo<=hi),
                         comparison_finite_readouts=reads,
                         optimistic_necessary_observation_s=necessary,
                         excluded_even_by_terminal_precision=bool(necessary>hi),
                         coded_reference_minimum_observation_s=tcode,
                         coded_reference_finite_readouts=code_reads,
                         coded_model_feasible=bool(0<=tcode<=hi),
                         ideal_zero_bias_error_budget_m=precision,
                         per_copy_systematic_bias_m_using_half_precision_budget=precision/(4*M)))
    return dict(meter_equilibrium_copy_error_sd_m=sigma0,correlation_time_s=tau,
                independent_readout_noise_sd_m=read_sd,readout_spacing_s=spacing,
                geometric_precision_m=precision,remaining_member_fault_rate_per_s=lam,
                per_renewal_nonobservation_overhead_s=overhead,
                error_budgets=dict(martingale=delta_R,disagreement=delta_D,overlap=delta_overlap),
                scope='All completed cycle boundaries. Observer-limited, zero-bias example: independent Gaussian copy errors from optimal finite reciprocal GLS. Actual total copy error must also include actuation/write error and calibration uncertainty, with correlations if present. Constant independent hazard during renewal under a no-reference-fault contract. The separate half-precision bias allowance requires recomputing noise time with the remaining half precision. Between-round geometry, rupture, probe error and standard/code faults need separate budgets. Coded comparator needs retained correct information and calibrated dimensional access; their hardware costs are not priced by these equations.',
                rows=rows)


def figure(data):
    rr=data['rows'];m=np.array([r['rounds'] for r in rr])
    low=np.array([r['comparison_minimum_observation_s'] for r in rr])
    high=np.array([r['maximum_observation_s_from_overlap'] for r in rr])
    fig,ax=plt.subplots(figsize=(8.3,4.8),layout='constrained')
    necessary=np.array([r['optimistic_necessary_observation_s'] for r in rr])
    ax.loglog(m,np.maximum(low,1e-5),'o-',label='Sufficient finite GLS observation')
    ax.loglog(m,necessary,'--',label='Optimistic necessary observation')
    ax.loglog(m,high,'s-',label='Maximum observation from survivor exposure')
    ax.fill_between(m,np.maximum(low,1e-5),high,where=high>=np.maximum(low,1e-5),
                    alpha=.16,color='green',label='Allowed window in this model')
    ax.set(xlabel='Complete three-member renewal rounds',ylabel='Observation time per renewal (s)',
           title='Reference renewal: precision versus survivor exposure (declared model)')
    ax.legend(fontsize=8);ax.spines[['top','right']].set_visible(False)
    fig.savefig(OUT/'renewal_budget.png',dpi=180);plt.close(fig)


if __name__=='__main__':
    data=budget();data['closed_form_checks']=proof_check()
    (OUT/'renewal_budget_results.json').write_text(json.dumps(data,indent=2)+'\n')
    figure(data)
    print(json.dumps(data,indent=2))
