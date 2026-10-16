#!/usr/bin/env python3
"""Exact bounded-rate exit check on the original eight-site process."""
import argparse
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import verify_slab as v

def run(a):
    s=v.Slab(a.manifest)
    tail=json.loads(Path(a.tail_result).read_text())
    sha=hashlib.sha256(s.npz_path.read_bytes()).hexdigest()
    assert tail['npz_sha256']==sha
    assert tail['full_generator_support_nonconstant']==[38,62]
    assert s.a==0 and s.h==F('0.0001')
    maxdeg=max(sum(i in edge for edge in v.EDGES) for i in range(8))
    assert maxdeg==3
    assert all(v.birth(n+1)>=v.birth(n) and v.death(n+1)>=v.death(n) for n in range(38,62))
    lp=v.birth(62)+maxdeg*v.DIFF*62
    lm=v.death(62)+maxdeg*v.DIFF*62
    mup=lp*s.h; mum=lm*s.h
    assert 0<mup<14 and 0<mum<14
    def poisson_upper(mu): return mu**13/F(factorial(13))/(1-mu/14)
    exit_bound=8*(poisson_upper(mup)+poisson_upper(mum))
    qtail=F(tail['endpoint_tail_mass']['lower']['exact'])
    qoverflow=F(tail['endpoint_overflow']['lower']['exact'])
    outside_mass=qtail+qoverflow
    lower=max(F(0),outside_mass-exit_bound)
    result={
        'status':'PASS_EXACT_LOCALIZATION_STATE_ERROR_REJECTION',
        'candidate_sha256':sha,
        'initial_state':[50]*8,
        'localization_box':[38,62],
        'maximum_graph_degree':maxdeg,
        'up_intensity_upper_exact':str(lp),
        'down_intensity_upper_exact':str(lm),
        'up_poisson_mean':v.fraction_json(mup),
        'down_poisson_mean':v.fraction_json(mum),
        'h_exact':str(s.h),
        'minimum_directed_coordinate_jump_count_to_exit':13,
        'true_probability_outside_box_or_overflow_upper':v.fraction_json(exit_bound),
        'candidate_mass_outside_box_plus_overflow_lower':v.fraction_json(outside_mass),
        'actual_augmented_state_l1_error_lower':v.fraction_json(lower),
        'full_graph_and_absorption':'All ten edges included through the verified degree upper bound; target freezing or overflow absorption cannot precede localization-box exit.',
        'proof':'Before first exit, each coordinate up/down counting intensity is bounded by its listed constant. Bounded-intensity counting processes are dominated by a Poisson process with that rate, without any independence across coordinates. An exit requires at least 13 jumps in one signed coordinate direction. Union bound over eight coordinates and two signs, then e^(-mu)<=1 and geometric tail ratio mu/14 bound.',
        'success_coordinate_error_lower_claimed':False,
        'all_decisive_arithmetic':'Exact rational; displayed approximations are descriptive only',
        'new_simulation_or_fit':False,
    }
    Path(a.output).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest');p.add_argument('--tail-result',required=True);p.add_argument('--output',required=True);run(p.parse_args())
