#!/usr/bin/env python3
"""Illustrative RAW-SAMPLE validation, not an experimental/biological benchmark.

Both protocols use the same number of independently simulated stationary
snapshots. For the tested skew-symmetric A, the mean protocol has no larger
expected added stationary second moment, including the noise baseline samples.
Stationarity and calibrated controls are supplied by this mathematical
simulator, NOT acquired from data. Timing is not a claimed application speedup.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from research_gate import (random_binary_code, stationary_covariance,
                           decode_covariance_differences)


def sample_second_moment(cov, count, rng, chunk=8192):
    chol=np.linalg.cholesky(cov)
    moment=np.zeros_like(cov)
    for start in range(0,count,chunk):
        x=rng.normal(size=(min(chunk,count-start),len(cov)))@chol.T
        moment += x.T@x
    # The zero mean is part of the model, not estimated/assumed from these data.
    return moment/count


def mean_regression(a, gamma, count, fraction, rng, chunk=8192):
    n=len(a)
    transfer=gamma*np.sqrt(fraction)*np.linalg.inv(gamma*np.eye(n)-a)
    zz=np.zeros((n,n)); xz=np.zeros((n,n))
    for start in range(0,count,chunk):
        size=min(chunk,count-start)
        z=rng.normal(size=(size,n))
        # Background stationary covariance is I for a skew-symmetric A.
        x=z@transfer.T+rng.normal(size=(size,n))
        zz+=z.T@z; xz+=x.T@z
    fitted=np.linalg.solve(zz.T,xz.T).T
    estimate=gamma*np.eye(n)-gamma*np.sqrt(fraction)*np.linalg.inv(fitted)
    return estimate,float(np.sum(transfer**2))


def main(output):
    rng=np.random.default_rng(2026100923)
    n=4; gamma=9.
    raw=rng.normal(size=(n,n))
    a=(raw-raw.T)/2
    a/=np.linalg.norm(a,2)
    code,delta=random_binary_code(n,rng)
    ds=[np.diag(1+sign*row) for row in code for sign in [-1.,1.]]
    conditions=len(ds)+1
    b=a-gamma*np.eye(n)
    cov0=stationary_covariance(b,2*gamma*np.eye(n))
    covs=[stationary_covariance(b,2*gamma*(np.eye(n)+d)) for d in ds]
    fraction=len(ds)/conditions
    noise_budget=float(sum(np.trace(c-cov0) for c in covs)/conditions)
    records=[]
    for per_condition in [2000,20000]:
        total=conditions*per_condition
        trials=[]
        for trial in range(6):
            base=sample_second_moment(cov0,per_condition,rng)
            differences=[sample_second_moment(c,per_condition,rng)-base for c in covs]
            estimate,diagnostics=decode_covariance_differences(differences,ds,gamma)
            mean_estimate,mean_budget=mean_regression(a,gamma,total,fraction,rng)
            assert mean_budget <= noise_budget+1e-10
            trials.append({'noise_full_frobenius_error':float(np.linalg.norm(estimate-a)),
                'mean_full_frobenius_error':float(np.linalg.norm(mean_estimate-a)),
                'noise_skew_projected_error':float(np.linalg.norm((estimate-estimate.T)/2-a)),
                'mean_skew_projected_error':float(np.linalg.norm((mean_estimate-mean_estimate.T)/2-a))})
        summary={key:float(np.sqrt(np.mean([t[key]**2 for t in trials]))) for key in trials[0]}
        records.append({'snapshots_per_noise_condition':per_condition,
                'total_snapshots_each_protocol':total,'independent_trials':6,
                'root_mean_squared_frobenius_errors':summary,'trials':trials,
                'noise_average_added_stationary_second_moment':noise_budget,
                'mean_average_added_stationary_second_moment':mean_budget})
    result={'status':'SIMULATED_ACQUISITION_CHECK_ONLY; NOT_A_REAL_WORLD_BENCHMARK',
        'n':n,'gamma':gamma,'A_spectral_norm':float(np.linalg.norm(a,2)),
        'A':a.tolist(),'noise_conditions_including_baseline':conditions,
        'code_relative_distance':delta,'records':records,
        'limitations':['Stationary Gaussian samples generated from supplied true drift by the TEST HARNESS only',
          'Decoders do not receive the true drift or exact covariances',
          'No temporal independence/settling is acquired from observations',
          'Known mean labels and fresh controllable inputs required for mean protocol',
          'Equal replica count and bounded stationary second moment, not equal laboratory switching/calibration/energy cost',
          'Noise least squares is not asserted statistically optimal; analytic Fisher comparison is separate',
          'Synthetic small linear model; no molecular/cellular/device data']}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    for r in records:
        print({k:v for k,v in r.items() if k!='trials'})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('raw_snapshot_results.json'))
    main(parser.parse_args().output)
