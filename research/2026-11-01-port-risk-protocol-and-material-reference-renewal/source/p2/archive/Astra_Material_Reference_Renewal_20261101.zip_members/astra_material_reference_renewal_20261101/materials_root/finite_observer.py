"""A complete finite reciprocal observation experiment.

Two held-polarity phases. Each phase starts at an unknown observed mechanical
state within the calibrated linear range; no equilibrium preparation or
noiseless position readout is supplied. Initial-state elimination is exact at
the stated response. Response calibration error times transient amplitude is
an additional bias, not included in the conditional Gaussian covariance.
Force polarity reversal is a real mechanical operation and its time/work remain
part of the apparatus contract.  It is not multiplication of one digital record.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import solve_banded

HERE=Path(__file__).resolve().parent
OUT=HERE/'results';OUT.mkdir(exist_ok=True)


def innovation_precision_ones(intervals, spacing, tau, meter_sd, readout_sd):
    rho=math.exp(-spacing/tau)
    process=meter_sd**2*(1-rho*rho)
    d=process+readout_sd**2*(1+rho*rho)
    off=-rho*readout_sd**2
    band=np.zeros((3,intervals));band[1]=d
    band[0,1:]=off;band[2,:-1]=off
    v=solve_banded((1,1),band,np.ones(intervals))
    return rho, v, float(np.sum(v)), band


def variance(intervals, spacing, tau, meter_sd, readout_sd):
    rho,v,weight,_=innovation_precision_ones(intervals,spacing,tau,meter_sd,readout_sd)
    return 1/(2*(1-rho)**2*weight)


def estimate(positive, negative, spacing, tau, meter_sd, readout_sd):
    n=len(positive)-1
    assert len(negative)==n+1
    rho,w,weight,_=innovation_precision_ones(n,spacing,tau,meter_sd,readout_sd)
    zp=positive[1:]-rho*positive[:-1]
    zn=negative[1:]-rho*negative[:-1]
    mp=float(w@zp)/((1-rho)*weight)
    mn=float(w@zn)/((1-rho)*weight)
    return (mp-mn)/2,(mp+mn)/2,variance(n,spacing,tau,meter_sd,readout_sd)


def observe_phase(mean,initial,offset,n,spacing,tau,meter_sd,readout_sd,rng):
    rho=math.exp(-spacing/tau)
    x=float(initial)
    y=[x+offset+rng.normal(0,readout_sd)]
    for _ in range(n):
        x=rho*x+(1-rho)*mean+rng.normal(0,meter_sd*math.sqrt(1-rho*rho))
        y.append(x+offset+rng.normal(0,readout_sd))
    return np.array(y)


def validate():
    rng=np.random.default_rng(98354)
    n,spacing,tau=16,.0005,.001
    sigma,sigma_r=1e-9,.2e-9
    true_mean,offset=2e-9,8e-9
    samples=8000;fitted=[]
    for _ in range(samples):
        # Deliberately far from equilibrium. Initial states not passed to estimator.
        pos=observe_phase(true_mean,10e-9,offset,n,spacing,tau,sigma,sigma_r,rng)
        neg=observe_phase(-true_mean,-7e-9,offset,n,spacing,tau,sigma,sigma_r,rng)
        a,b,v=estimate(pos,neg,spacing,tau,sigma,sigma_r)
        fitted.append((a,b))
    fitted=np.array(fitted)
    predicted=variance(n,spacing,tau,sigma,sigma_r)
    empirical=float(np.var(fitted[:,0],ddof=1))
    ratio=empirical/predicted
    assert abs(ratio-1)<.06
    assert abs(float(np.mean(fitted[:,0]))-true_mean)<4*math.sqrt(predicted/samples)
    no_readout=variance(n,spacing,tau,sigma,0.)
    formula=sigma**2/(2*n*math.tanh(spacing/(2*tau)))
    assert abs(no_readout/formula-1)<1e-12
    return dict(physical_mean_m=true_mean,unknown_offset_m=offset,
        initial_states_m=[10e-9,-7e-9],intervals_per_phase=n,
        readouts_total=2*(n+1),spacing_s=spacing,correlation_time_s=tau,
        total_observation_s=2*n*spacing,
        meter_equilibrium_sd_m=sigma,readout_sd_m=sigma_r,
        predicted_estimator_sd_m=math.sqrt(predicted),
        monte_carlo_estimator_sd_m=math.sqrt(empirical),
        monte_carlo_mean_m=float(np.mean(fitted[:,0])),
        monte_carlo_offset_mean_m=float(np.mean(fitted[:,1])),
        empirical_variance_over_prediction=ratio,monte_carlo_runs=samples,
        missing_apparatus_times=['polarity reversal','any actual input calibration','force routing or clutches'],
        caveat='Conditional on calibrated meter response/noise covariance, unknown initial state within its linear/amplitude range, and real stable-sign holds; offset constant across two phases. Response calibration uncertainty, write error and correlated drift require additional budgets. No fabricated device.')


if __name__=='__main__':
    result=validate()
    (OUT/'finite_observer_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
