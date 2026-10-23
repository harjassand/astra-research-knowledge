#!/usr/bin/env python3
"""Finite-bit interval compiler, exploratory extension of the frozen experiment.

The original research.py and original results are intentionally unmodified.
On the translationally invariant ring, one forward impulse bounds all sites.
No trajectory, target normalizer, training sample, or rare event is queried
during compilation. Costs include the O(T*d*d) dot products below.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
from scipy.special import logsumexp
import research as base

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'/'secant_extension'


def acquire_secant(cfg):
    start=time.perf_counter()
    cfg.validate()
    S=base.SCALE
    r,k,s=map(Fraction,(cfg.rho,cfg.kappa,cfg.sigma))
    impulse=2*s*S
    if impulse.denominator!=1:
        raise ValueError('This implementation requires a dyadic initial impulse')
    vlo=[int(impulse)]+[0]*(cfg.d-1)
    vhi=vlo.copy()
    bf=cfg.b_fraction()
    bd=math.lcm(*(b.denominator for b in bf))
    bn=[b.numerator*(bd//b.denominator) for b in bf]
    lower=[[0]*cfg.d for _ in range(cfg.T)]
    upper=[[0]*cfg.d for _ in range(cfg.T)]
    cumulative_lo=[0]*cfg.d
    cumulative_hi=[0]*cfg.d
    dl=r.denominator*4*k.denominator*S*S
    du=r.denominator*k.denominator*S*S
    for age in range(cfg.T):
        # Shift the site-zero impulse to source j before taking b dot delta.
        for j in range(cfg.d):
            al=sum(bn[a]*vlo[(a-j)%cfg.d] for a in range(cfg.d))
            ah=sum(bn[a]*vhi[(a-j)%cfg.d] for a in range(cfg.d))
            cumulative_lo[j]+=al//bd
            cumulative_hi[j]+=base.ceil_div(ah,bd)
        lower[cfg.T-1-age]=cumulative_lo.copy()
        upper[cfg.T-1-age]=cumulative_hi.copy()
        zlo=[(2*vlo[j]+vlo[(j-1)%cfg.d]+vlo[(j+1)%cfg.d])//4 for j in range(cfg.d)]
        zhi=[base.ceil_div(2*vhi[j]+vhi[(j-1)%cfg.d]+vhi[(j+1)%cfg.d],4) for j in range(cfg.d)]
        assert all(0<=z<=2*S for z in zlo+zhi)
        newlo=[]; newhi=[]
        for j in range(cfg.d):
            z=zlo[j]
            nlo=r.numerator*vlo[j]*(4*k.denominator*S*S)+k.numerator*z*z*z*r.denominator
            newlo.append(nlo//dl)
            z=zhi[j]
            poly=z*z*z-3*z*z*S+3*z*S*S
            nhi=r.numerator*vhi[j]*(k.denominator*S*S)+k.numerator*poly*r.denominator
            newhi.append(min(2*S,base.ceil_div(nhi,du)))
        vlo,vhi=newlo,newhi
    return lower,upper,time.perf_counter()-start


def check():
    start=time.perf_counter()
    scalar_checks=0
    for aint in range(-32,33):
        for bint in range(-32,aint+1):
            a=Fraction(aint,32); b=Fraction(bint,32); z=a-b
            val=a**3-b**3
            assert z**3/4<=val<=3*z-3*z*z+z**3
            scalar_checks+=1
    cfg=base.Config('secant_exhaustive',2,8)
    m=cfg.d*cfg.T
    ids=np.arange(1<<m,dtype=np.uint64)
    bits=((ids[:,None]>>np.arange(m,dtype=np.uint64))&1).astype(bool).reshape(-1,cfg.T,cfg.d)
    x=np.zeros((len(ids),cfg.d)); score=np.zeros(len(ids)); lp=np.zeros(len(ids))
    r,k,s=map(lambda v:float(Fraction(v)),(cfg.rho,cfg.kappa,cfg.sigma))
    for t in range(cfg.T):
        z=base.neighbor(x); x=r*x+k*z*z*z+s*(2*bits[:,t].astype(float)-1)
        score+=np.sum(x*cfg.b,axis=1)
        lp+=np.sum(np.where(bits[:,t],np.log(cfg.p),np.log1p(-cfg.p)),axis=1)
    lo,hi,secs=acquire_secant(cfg)
    oldlo,oldhi,_=base.acquire_intervals(cfg)
    qs,endpoints,logs,width,certsecs=base.certified_proposals(cfg,lo,hi)
    logz=float(logsumexp(score+lp))
    results={}
    for name,qnum in qs.items():
        q=qnum/base.QSCALE
        lq=np.sum(np.where(bits,np.log(q),np.log1p(-q)),axis=(1,2))
        R=float(np.exp(logsumexp(2*(score+lp)-lq)-2*logz))
        results[name]={'enumerated_R_binary64':R,'bound_R':math.exp(float(logs[name]))}
        assert R<=math.exp(float(logs[name]))+1e-10
    violations=0; min_slack=math.inf
    for i in range(m):
        zero=(ids&(1<<i))==0
        dif=score[ids[zero]|np.uint64(1<<i)]-score[zero]
        t,j=divmod(i,cfg.d)
        ell=float(Fraction(lo[t][j],base.SCALE)); up=float(Fraction(hi[t][j],base.SCALE))
        violations+=int(np.sum((dif<ell-1e-12)|(dif>up+1e-12)))
        min_slack=min(min_slack,float(np.min(np.minimum(dif-ell,up-dif))))
    assert violations==0
    # Per-step rounding may shift a theoretical inclusion by a few grid units.
    lower_gap=min(lo[t][j]-oldlo[t][j] for t in range(cfg.T) for j in range(cfg.d))
    upper_gap=min(oldhi[t][j]-hi[t][j] for t in range(cfg.T) for j in range(cfg.d))
    assert lower_gap>=-10*cfg.T and upper_gap>=-10*cfg.T
    return {'scalar_fraction_checks':scalar_checks,'paths_enumerated':len(ids),
            'bit_flip_checks':m*(len(ids)//2),'violations':violations,
            'minimum_enumerated_slack_float':min_slack,
            'risk_checks':results,'elapsed_seconds':time.perf_counter()-start,
            'minimum_lower_inclusion_gap_grid':lower_gap,'minimum_upper_inclusion_gap_grid':upper_gap,
            'kind':'exact scalar checks; binary64 exhaustive path checks; mathematical proof separate'}


def run_case(cfg,simulate):
    out=OUT/cfg.name; out.mkdir(parents=True,exist_ok=True)
    lo,hi,acq=acquire_secant(cfg)
    qs,endpoints,logs,width,cert=base.certified_proposals(cfg,lo,hi)
    original=json.loads((ROOT/'results'/cfg.name/'results.json').read_text())
    original_q=np.load(ROOT/'results'/cfg.name/'proposals.npz')
    certify_original_start=time.perf_counter()
    linear_on_new=base.certificate_for_q(cfg,endpoints,original_q['linear_tilt'])
    certify_original_seconds=time.perf_counter()-certify_original_start
    oldlogK=float(original['logK_decimal']['probability_midpoint_minimax'])
    logK=float(logs['probability_midpoint_minimax'])
    required=max(1024,math.ceil(math.expm1(logK)/(.05**3)))
    n=min(32768,((required+255)//256)*256)
    result={'config':asdict(cfg),'acquisition_seconds':acq,'certificate_seconds':cert,
            'additional_linear_certificate_seconds':certify_original_seconds,
            'original_linear_tilt_new_certificate_logK':linear_on_new,
            'new_logK_decimal':logs,'old_minimax_logK':oldlogK,'new_minimax_logK':logK,
            'old_paths':original['paths_per_method'],'new_paths':n,
            'new_required_paths_before_cap':required,'width_only_log_bound':width,
            'certificate_variance_bound_ratio':math.expm1(logK)/math.expm1(oldlogK),
            'methods':{},'interpretation':'exploratory response to exposed original cases; no new blind confirmation'}
    (out/'intervals.json').write_text(json.dumps({'scale_bits':base.GRID_BITS,'lower_numerators':lo,'upper_numerators':hi}))
    np.savez_compressed(out/'proposals.npz',**qs)
    if simulate:
        for name,seed in [('probability_midpoint_minimax',20261023073701),('log_midpoint_tilt',20261023073702)]:
            print('simulating secant '+cfg.name+' '+name+' n='+str(n),flush=True)
            score,receipt=base.sample_paths(cfg,qs[name],n,seed)
            np.save(out/(name+'_logweights.npy'),score)
            stats=base.statistics(score,cfg,logs[name],receipt['uniform_log_weight_error_allowance'])
            stats.update(receipt)
            stats['end_to_end_seconds']=acq+cert+receipt['setup_seconds']+receipt['sampling_seconds']+stats['aggregation_seconds']
            stats['variance_times_sampling_cost_per_path']=stats['empirical_relative_variance']*receipt['sampling_seconds']/n
            result['methods'][name]=stats
        result['empirical_minimax_variance_ratio_to_original_linear']=result['methods']['probability_midpoint_minimax']['empirical_relative_variance']/original['methods']['linear_tilt']['empirical_relative_variance']
    result['criteria']={'certificate_trajectory_reduction_at_least_20percent':n<=.8*original['paths_per_method'],
                        'logK_strictly_improved':logK<oldlogK,
                        'within_path_cap':required<=32768}
    (out/'results.json').write_text(json.dumps(result,indent=2))
    print(cfg.name+': '+json.dumps({k:result[k] for k in ['old_minimax_logK','new_minimax_logK','old_paths','new_paths','criteria']}),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); parser.add_argument('--run',action='store_true')
    args=parser.parse_args(); OUT.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    if args.check:
        res=check(); (OUT/'check.json').write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2),flush=True)
    if args.run:
        freeze=json.loads((ROOT/'CONFIRMATION.json').read_text())
        for item in freeze['cases']:
            run_case(base.Config(**item),item['name']=='main_confirmation')
    receipt={'elapsed_seconds':time.perf_counter()-start,'python':platform.python_version(),'numpy':np.__version__,
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'base_source_sha256':hashlib.sha256((ROOT/'research.py').read_bytes()).hexdigest(),
             'freeze_sha256':hashlib.sha256((ROOT/'SECANT_EXTENSION.json').read_bytes()).hexdigest(),
             'arguments':vars(args),'workers':'root process only; native proof auditor separate and unmetered'}
    (OUT/('receipt_'+('run' if args.run else 'check')+'.json')).write_text(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
