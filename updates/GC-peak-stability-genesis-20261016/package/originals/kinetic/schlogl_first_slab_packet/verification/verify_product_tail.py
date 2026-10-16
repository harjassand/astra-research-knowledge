#!/usr/bin/env python3
"""Exact full-operator tail functional for rank-one product enrichment.

Generalizes the uniform-tail rejection to the actual weighted-repair export.
No approximations, weighted residual estimates, or unknown support assumptions.
"""
import argparse
from fractions import Fraction as F
from math import prod, factorial
from pathlib import Path
import hashlib
import json
import resource
import time
import numpy as np
import verify_slab as v

def run(a):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(120,121))
    s=v.Slab(a.manifest)
    assert s.a==0 and s.anchored
    assert np.array_equal(s.initial,np.eye(len(s.basis),dtype=np.float64)[1])
    assert s.initial_overflow==0
    for g in s.basis[1]: assert g.shape==(1,163,1) and np.array_equal(g[0,:,0],np.eye(163)[50])
    weights=[None]*8
    for i,g in enumerate(s.basis[0]):
        assert g.shape==(1,163,1)
        weights[s.order[i]]=[F.from_float(float(x)) for x in g[0,:,0]]
    support=[]
    for cores in s.basis[1:]:
        for g in cores:
            nz=np.flatnonzero(np.any(g!=0,axis=(0,2)))
            if len(nz): support.extend([int(nz[0]),int(nz[-1])])
    lo,hi=min(support),max(support);L=lo-1;U=hi+1
    assert 17<L<=U<161
    total=[sum(w,F(0)) for w in weights]
    inside=[sum(w[L:U+1],F(0)) for w in weights]
    mean=[sum((n*z for n,z in enumerate(w)),F(0)) for w in weights]
    cap=[w[-1] for w in weights]
    exclude=lambda vals,inds:prod(vals[k] for k in range(8) if k not in inds)
    tailmass=prod(total)-prod(inside)
    overflowflux=sum((v.birth(162)*cap[i]*exclude(total,[i]) for i in range(8)),F(0))
    insidegenerator=F(0)
    for i,w in enumerate(weights):
        row=sum((v.birth(n-1)*w[n-1]+v.death(n+1)*w[n+1]-(v.birth(n)+v.death(n))*w[n] for n in range(L,U+1)),F(0))
        insidegenerator+=row*exclude(inside,[i])
    for i,j in v.EDGES:
        for src,dst in ((i,j),(j,i)):
            wa,wb=weights[src],weights[dst]
            incoming_a=sum(((n+1)*wa[n+1] for n in range(L,U+1)),F(0))
            incoming_b=sum((wb[n-1] for n in range(L,U+1)),F(0))
            outgoing_a=sum((n*wa[n] for n in range(L,U+1)),F(0))
            insidegenerator+=v.DIFF*(incoming_a*incoming_b-outgoing_a*inside[dst])*exclude(inside,[src,dst])
            overflowflux+=v.DIFF*mean[src]*cap[dst]*exclude(total,[src,dst])
    # H P_B is supported outside the distant cube and has zero total mass.
    # Thus its complement aggregate is zero, even for a nonuniform product.
    tailgenerator=-overflowflux-insidegenerator
    y=s.time_power[0]
    tailpoly=v.p_scale(y,tailmass)
    tailr=v.p_add(v.p_scale(v.p_derivative(tailpoly),1/s.h),v.p_scale(y,-tailgenerator))
    op=s.overflow_power()
    or_=v.p_add(v.p_scale(v.p_derivative(op),1/s.h),v.p_scale(y,-overflowflux))
    tail_lb=v.integrated_abs_lower(tailr,s.h,a.bins)
    overflow_lb=v.integrated_abs_lower(or_,s.h,a.bins)
    ep_tail=v.p_eval(tailpoly,F(1));ep_over=v.p_eval(op,F(1))
    ep_success=v.p_eval(v.p_scale(y,prod(sum(w[:16],F(0)) for w in weights)),F(1))
    # Localization proof, now using the actual verified support cube.
    maxdeg=max(sum(i in edge for edge in v.EDGES) for i in range(8))
    upsteps=U-50+1;downsteps=50-L+1
    mup=(v.birth(U)+maxdeg*v.DIFF*U)*s.h
    mum=(v.death(U)+maxdeg*v.DIFF*U)*s.h
    assert upsteps>0 and downsteps>0 and mup<upsteps+1 and mum<downsteps+1
    poisson=lambda mu,k:mu**k/F(factorial(k))/(1-mu/F(k+1))
    exitbound=8*(poisson(mup,upsteps)+poisson(mum,downsteps))
    outside=(ep_tail+ep_over)
    simple_state_lower=max(F(0),outside.lo-exitbound)
    result={
      'status':'REJECT_FULL_FORWARD_L1_BUDGET' if tail_lb+overflow_lb>F('1e-9') else 'INCONCLUSIVE',
      'candidate':str(s.npz_path),'candidate_sha256':hashlib.sha256(s.npz_path.read_bytes()).hexdigest(),
      'basis0_verified_rank1':True,'nonconstant_support':[lo,hi],'full_operator_support':[L,U],
      'physical_order':s.order,'first_basis_total_mass_exact':str(prod(total)),
      'first_basis_tail_mass_exact':str(tailmass),'first_basis_overflow_flux_exact':str(overflowflux),
      'first_basis_full_generator_tail_functional_exact':str(tailgenerator),
      'initial_l1_defect_exact':'0','join_l1_defect_exact':'0 (first slab)',
      'tail_integrated_residual_lower':v.fraction_json(tail_lb),
      'overflow_integrated_residual_lower':v.fraction_json(overflow_lb),
      'augmented_integrated_l1_residual_lower':v.fraction_json(tail_lb+overflow_lb),
      'endpoint_tail_mass':v.interval_json(ep_tail),'endpoint_overflow':v.interval_json(ep_over),
      'endpoint_success':v.interval_json(ep_success),
      'true_probability_outside_box_or_overflow_upper':v.fraction_json(exitbound),
      'actual_augmented_state_l1_error_lower':v.fraction_json(simple_state_lower),
      'all_decisive_arithmetic':'Exact rational for rank-one tail, full model operator, scalar sink, localization and polynomial calculations',
      'full_temporal_cross_terms':'All signed polynomial coefficients retained before exact integration; no time sampling or diagonal-only Gram',
      'success_coordinate_error_lower_claimed':False,
    }
    if a.total_mass:
        mass=v.p_eval(op,F(1))
        for j,cores in enumerate(s.basis):
            bj=s.contractor.functional(cores)
            mass=mass+bj*v.p_eval(s.time_power[j],F(1))
        err=(mass-v.RI.exact(1)).abs_upper()
        dual=max(F(0),2*(outside.lo-exitbound)-err)
        result.update({'endpoint_augmented_mass_interval':v.interval_json(mass),'mass_defect_absolute_upper':v.fraction_json(err),'actual_augmented_state_l1_error_lower_balanced_witness':v.fraction_json(dual),'mass_arithmetic':'80-digit directed Decimal contractions on exact saved dyadics, then exact rational interval endpoint evaluation','balanced_witness':'2*indicator(outside box or overflow)-1, infinity norm exactly one; no candidate positivity assumed'})
    result.update({'elapsed_seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'memory_limit_mib':512,'cpu_limit_seconds':120})
    Path(a.output).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:z for k,z in result.items() if not k.endswith('_exact')},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--output',required=True);p.add_argument('--bins',type=int,default=256);p.add_argument('--total-mass',action='store_true');run(p.parse_args())
