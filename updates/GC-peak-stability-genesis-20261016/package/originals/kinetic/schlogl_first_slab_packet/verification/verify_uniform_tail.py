#!/usr/bin/env python3
"""Exact separating-functional verifier for the exported uniform enrichment.

The actual export is checked for the claimed constant and compact support.
This is NOT a new approximation, smaller model, simulation, or fitted bound.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import resource
import time
import numpy as np
import verify_slab as v

def run(a):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    s=v.Slab(a.manifest)
    if s.a!=0 or not s.anchored: raise ValueError('Expected first anchored slab')
    # Prove constant spatial coefficient exactly from every saved binary64 entry.
    gamma=F(1)
    for g in s.basis[0]:
        if g.shape!=(1,163,1) or not np.all(g==g[0,0,0]): raise ValueError('Basis 0 is not exactly spatially constant')
        gamma*=F.from_float(float(g[0,0,0]))
    # Verify full grid initial state, not merely a sampled initial coordinate.
    if not np.array_equal(s.initial,np.eye(len(s.basis),dtype=np.float64)[1]): raise ValueError('Initial coefficients not exactly delta basis')
    for g in s.basis[1]:
        if g.shape!=(1,163,1) or not np.array_equal(g[0,:,0],np.eye(163,dtype=np.float64)[50]): raise ValueError('Initial basis is not exact delta')
    if s.initial_overflow!=0: raise ValueError('Initial overflow not zero')
    # Bounds of the actual saved support; all later full operator actions grow
    # this cube by at most 1 in each coordinate. Nothing is cropped here.
    support_lo=163; support_hi=-1
    for cores in s.basis[1:]:
        for g in cores:
            nz=np.flatnonzero(np.any(g!=0,axis=(0,2)))
            if len(nz): support_lo=min(support_lo,int(nz[0])); support_hi=max(support_hi,int(nz[-1]))
    L=support_lo-1; U=support_hi+1
    if not (17<L<=U<161): raise ValueError('Support not separated from target and cap')
    for cores in s.basis[1:]:
        for g in cores:
            if np.any(g[:,:support_lo,:]) or np.any(g[:,support_hi+1:,:]): raise ValueError('Support check failed')
    width=U-L+1
    volume=v.D**8-width**8
    countsum=sum(range(v.D))
    # Sum_x overflow_rate(x), for a spatially constant per-state coefficient.
    fluxsum=8*v.birth(162)*v.D**7+20*v.DIFF*countsum*v.D**6
    # On this interior cube, all neighbors are retained and outside the target.
    # Sum of reaction row sums telescopes; each edge contributes 2D per row.
    inside_h_sum=8*(v.birth(L-1)-v.birth(U)+v.death(U+1)-v.death(L))*width**7+20*v.DIFF*width**8
    # G=H(I-P_B). All H P_B columns conserve mass and have no rows inside
    # this distant cube; their aggregate on its complement is therefore zero.
    outside_g_sum=-fluxsum-inside_h_sum
    per_state=v.p_scale(s.time_power[0],gamma)
    tail_mass=v.p_scale(per_state,volume)
    tail_r=v.p_add(v.p_scale(v.p_derivative(tail_mass),1/s.h),v.p_scale(per_state,-outside_g_sum))
    overflow=s.overflow_power()
    overflow_r=v.p_add(v.p_scale(v.p_derivative(overflow),1/s.h),v.p_scale(per_state,-fluxsum))
    tail_lb=v.integrated_abs_lower(tail_r,s.h,a.bins)
    overflow_lb=v.integrated_abs_lower(overflow_r,s.h,a.bins)
    endpoint_overflow=v.p_eval(overflow,F(1))
    endpoint_tail=v.p_eval(tail_mass,F(1))
    endpoint_success=v.p_eval(v.p_scale(per_state,16**8),F(1))
    endpoint_negative_mass_lower=max(F(0),-endpoint_tail.hi)
    report={
        'status':'REJECT_FORWARD_L1_CERTIFICATE_FOR_FULL_1E9_BUDGET' if tail_lb+overflow_lb>F('1e-9') else 'INCONCLUSIVE',
        'manifest':str(Path(a.manifest)),
        'npz_sha256':hashlib.sha256(s.npz_path.read_bytes()).hexdigest(),
        'arithmetic':'Exact Fraction arithmetic on saved binary64 values; no floating contraction or polynomial evaluation',
        'full_model':'Eight sites, count 0 through 162, full open 2-by-4 graph, initial all 50, frozen all-low target, physical overflow sink',
        'export_verified_spatial_support_nonconstant':[support_lo,support_hi],
        'full_generator_support_nonconstant':[L,U],
        'tail_set':'Complement of full-generator support cube, in the complete 163^8 grid',
        'tail_cardinality_exact':str(volume),
        'uniform_per_state_basis_exact':str(gamma),
        'overflow_flux_sum_exact':str(fluxsum),
        'full_generator_uniform_tail_sum_exact':str(outside_g_sum),
        'initial_l1_defect_exact':'0',
        'join_l1_defect_exact':'0 (first slab)',
        'tail_aggregate_integrated_residual_lower':v.fraction_json(tail_lb),
        'overflow_integrated_residual_lower':v.fraction_json(overflow_lb),
        'augmented_integrated_l1_residual_lower':v.fraction_json(tail_lb+overflow_lb),
        'proportional_time_planning_share':'1e-13',
        'full_interior_error_budget':'1e-9',
        'endpoint_overflow':v.interval_json(endpoint_overflow),
        'endpoint_tail_mass':v.interval_json(endpoint_tail),
        'endpoint_success':v.interval_json(endpoint_success),
        'endpoint_actual_grid_l1_error_lower_from_negative_tail':v.fraction_json(endpoint_negative_mass_lower),
        'endpoint_success_error_lower_from_negative_success':v.fraction_json(max(F(0),-endpoint_success.hi)),
        'interpretation':'Residual lower bound rejects the full forward l1 certificate budget, not target accuracy. Negative tail mass independently lower-bounds actual grid l1 error by positivity of the exact Markov state. Negative success only proves its separately reported much smaller error floor.',
        'signed_temporal_cross_terms':'Every polynomial term is retained until exact integration; squared checks below contain all i,j terms.',
        'tail_integrated_square':v.interval_json(v.integrated_square(tail_r,s.h)),
        'overflow_integrated_square':v.interval_json(v.integrated_square(overflow_r,s.h)),
        'bins':a.bins,
        'elapsed_seconds':time.monotonic()-start,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'memory_limit_mib':512,
        'cpu_limit_seconds':120,
    }
    if a.physical_overflow_upper:
        cap=F(a.physical_overflow_upper)
        report['conditional_physical_overflow_upper']=str(cap)
        report['conditional_actual_augmented_l1_error_lower']=v.fraction_json(max(F(0),endpoint_overflow.lo-cap))
        report['conditional_warning']='Validity requires independently verified same-model overflow probability upper bound; argument alone does not verify that source.'
    Path(a.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:val for k,val in report.items() if k not in ('tail_integrated_square','overflow_integrated_square')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--output',required=True);p.add_argument('--bins',type=int,default=256);p.add_argument('--physical-overflow-upper')
    run(p.parse_args())
