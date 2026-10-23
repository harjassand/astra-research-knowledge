#!/usr/bin/env python3
"""Separately frozen test of the finite-bit compiler at derivative criticality."""
from __future__ import annotations
from dataclasses import dataclass,asdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
import research as base
from secant_extension import acquire_secant

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'/'critical_confirmation'


@dataclass(frozen=True)
class CriticalConfig(base.Config):
    def validate(self):
        r,k,s=map(Fraction,(self.rho,self.kappa,self.sigma))
        assert r>=0 and k>=0 and s>=0 and r+k+s<=1
        assert r+3*k==1


def critical_roundoff_allowance(cfg,yes,no,coefficient_error):
    u=2.0**-53
    bsum=float(np.sum(cfg.b)); maxlr=float(np.max(np.maximum(np.abs(yes),np.abs(no))))
    # eta=64u local state error; at lambda=1 sum_t e_t <= eta T(T+1)/2.
    state_score=64*u*bsum*cfg.T*(cfg.T+1)/2
    dots=cfg.T*(8*cfg.d*u/(1-8*cfg.d*u))*(bsum+cfg.d*maxlr)
    sums=(8*cfg.T*u/(1-8*cfg.T*u))*cfg.T*(bsum+cfg.d*maxlr)
    return state_score+dots+sums+coefficient_error+1e-12


def sample(cfg,qnums,n,seed):
    setup=time.perf_counter()
    yes,no,coeff_err,coeff_seconds=base.exact_log_coefficients(cfg,qnums)
    tau=critical_roundoff_allowance(cfg,yes,no,coeff_err)
    setup_seconds=time.perf_counter()-setup
    start=time.perf_counter()
    rng=np.random.Generator(np.random.PCG64(seed))
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    scores=np.empty(n); max_abs_state=0.
    for first in range(0,n,1024):
        m=min(1024,n-first)
        x=np.zeros((m,cfg.d)); score=np.zeros(m)
        for t in range(cfg.T):
            bits=rng.integers(0,base.QSCALE,size=(m,cfg.d),dtype=np.uint64)<qnums[t]
            z=base.neighbor(x)
            x=r*x+k*z*z*z+s*(2*bits.astype(float)-1)
            np.clip(x,-1,1,out=x)
            score+=np.sum(x*cfg.b+np.where(bits,yes[t],no[t]),axis=1)
        max_abs_state=max(max_abs_state,float(np.max(np.abs(x))))
        scores[first:first+m]=score
    return scores,{'setup_seconds':setup_seconds,'log_coefficient_seconds':coeff_seconds,
                   'sampling_seconds':time.perf_counter()-start,
                   'uniform_log_weight_error_allowance':tau,
                   'state_error_rule':'local eta=64*2^-53; e_t<=t*eta, clipped cube',
                   'paths':n,'state_coordinate_updates':n*cfg.T*cfg.d,
                   'max_abs_final_state_observed':max_abs_state,'seed':seed,'rng':'numpy.PCG64'}


def run_case(cfg,simulate):
    out=OUT/cfg.name; out.mkdir(parents=True,exist_ok=True)
    oldlo,oldhi,oldacq=base.acquire_intervals(cfg)
    oldqs,oldend,oldlogs,oldwidth,oldcert=base.certified_proposals(cfg,oldlo,oldhi)
    lo,hi,acq=acquire_secant(cfg)
    qs,endpoints,logs,width,cert=base.certified_proposals(cfg,lo,hi)
    extra_start=time.perf_counter()
    linear_logK=base.certificate_for_q(cfg,endpoints,oldqs['linear_tilt'])
    extra=time.perf_counter()-extra_start
    logK=float(logs['probability_midpoint_minimax'])
    oldlogK=float(oldlogs['probability_midpoint_minimax'])
    required=max(1024,math.ceil(math.expm1(logK)/(.05**3)))
    n=min(32768,((required+255)//256)*256)
    # A completely independent coarse harmonic envelope for the first impulse.
    harmonic=2*sum(1/(i+2) for i in range(cfg.T))
    result={'config':asdict(cfg),'dimension_of_independent_innovations':cfg.d*cfg.T,
            'derivative_acquisition_seconds':oldacq,'derivative_certificate_seconds':oldcert,
            'secant_acquisition_seconds':acq,'secant_certificate_seconds':cert,
            'additional_linear_certificate_seconds':extra,
            'derivative_logK_decimal':oldlogs,'secant_logK_decimal':logs,
            'linear_tilt_secant_certificate_logK':linear_logK,
            'derivative_width_budget':oldwidth,'secant_width_budget':width,
            'derivative_minimax_logK':oldlogK,'secant_minimax_logK':logK,
            'required_paths_before_cap':required,'paths_per_method':n,
            'coarse_harmonic_first_bit_upper':float(sum(cfg.b_fraction()))*harmonic,
            'acquired_first_bit_upper':float(Fraction(hi[0][0],base.SCALE)),
            'methods':{}}
    for tag,l,h in [('derivative',oldlo,oldhi),('secant',lo,hi)]:
        (out/(tag+'_intervals.json')).write_text(json.dumps({'scale_bits':base.GRID_BITS,'lower_numerators':l,'upper_numerators':h}))
    qs['original_linear_tilt']=oldqs['linear_tilt']; logs['original_linear_tilt']=linear_logK
    np.savez_compressed(out/'proposals.npz',**qs)
    if simulate:
        for j,name in enumerate(['probability_midpoint_minimax','log_midpoint_tilt','original_linear_tilt']):
            print(f'{cfg.name} {name} n={n}',flush=True)
            score,receipt=sample(cfg,qs[name],n,20261023080100+j)
            np.save(out/(name+'_logweights.npy'),score)
            stats=base.statistics(score,cfg,logs[name],receipt['uniform_log_weight_error_allowance'])
            stats.update(receipt)
            stats['end_to_end_seconds']=acq+cert+receipt['setup_seconds']+receipt['sampling_seconds']+stats['aggregation_seconds']
            if name=='original_linear_tilt':
                stats['end_to_end_seconds']+=oldacq+extra
            stats['variance_times_sampling_cost_per_path']=stats['empirical_relative_variance']*receipt['sampling_seconds']/n
            result['methods'][name]=stats
    result['criteria']={'derivative_K_over_100':oldlogK>math.log(100),
                        'secant_K_at_most_5':logK<=math.log(5),
                        'five_percent_95pct_within_cap':required<=32768}
    (out/'results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ['config','derivative_minimax_logK','secant_minimax_logK','required_paths_before_cap','criteria']}),flush=True)


def main():
    start=time.perf_counter(); OUT.mkdir(parents=True,exist_ok=True)
    freeze=json.loads((ROOT/'CRITICAL_CONFIRMATION.json').read_text())
    for item in freeze['cases']:
        run_case(CriticalConfig(**item),item['name']==freeze['primary_case'])
    receipt={'elapsed_seconds':time.perf_counter()-start,'python':platform.python_version(),'numpy':np.__version__,
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'base_source_sha256':hashlib.sha256((ROOT/'research.py').read_bytes()).hexdigest(),
             'secant_source_sha256':hashlib.sha256((ROOT/'secant_extension.py').read_bytes()).hexdigest(),
             'freeze_sha256':hashlib.sha256((ROOT/'CRITICAL_CONFIRMATION.json').read_bytes()).hexdigest(),
             'workers':'root process only; existing native proof auditor separate and unmetered'}
    (OUT/'run_receipt.json').write_text(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
