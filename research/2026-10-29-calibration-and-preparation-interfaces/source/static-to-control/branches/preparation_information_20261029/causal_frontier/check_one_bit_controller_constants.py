"""Exact constants for the one-retained-bit controller boundary.

This checks arithmetic consequences of the ordinary proofs, not trajectory
acquisition, execution of a controller, or a whole-theorem formal proof.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math


def main():
    # a=A=gamma=tau=T0=B=eta=1; reporter duration h=log(2).
    delta_mean=F(1,2)
    source_second=F(6)
    gibbs_second=F(6)
    total_second=source_second+gibbs_second
    score_clip=total_second/(2*delta_mean)
    bit_gap=delta_mean**2/(2*total_second)
    assert score_clip==12 and bit_gap==F(1,96)
    clipped_mean_gap=delta_mean-total_second/(4*score_clip)
    assert clipped_mean_gap/(2*score_clip)==bit_gap

    # beta=erf(1/4). 2/sqrt(pi)>1 and exp(-t^2)>=1-t^2 give
    # beta > integral_0^(1/4) (1-t^2)dt =47/192.
    quarter=F(1,4)
    beta_lower=quarter-quarter**3/3
    assert beta_lower==F(47,192)
    output_gap=beta_lower*bit_gap
    assert output_gap==F(47,18432)

    bins=512
    finite_dither_gap=bit_gap-F(2,bins)
    assert bins>=4/bit_gap
    assert finite_dither_gap>=bit_gap/2
    free_bit_gap=beta_lower/6
    free_output_gap=beta_lower*free_bit_gap

    result={
        'status':'PASS',
        'scope':'Exact rational arithmetic for proved constants; no trajectory simulation, physical record, controller execution, or whole-theorem formal verification',
        'parameters':{'a':1,'A':1,'gamma':1,'tau':1,'T0':1,'B':1,'eta':1,'reporter_duration':'log(2)'},
        'score':{'mean_gap':str(delta_mean),'sum_second_moment_bound':str(total_second),'clip_halfwidth':str(score_clip)},
        'all_candidate_bit_gap':str(bit_gap),
        'reporter_gain':'erf(1/4)',
        'reporter_gain_rational_lower_bound':str(beta_lower),
        'all_candidate_output_gap_rational_lower_bound':str(output_gap),
        'optional_finite_threshold_bins':bins,
        'finite_threshold_bit_gap_lower_bound':str(finite_dither_gap),
        'finite_threshold_output_gap_lower_bound':str(beta_lower*finite_dither_gap),
        'explicit_free_sign_score_bit_gap_lower_bound':str(free_bit_gap),
        'explicit_free_sign_score_output_gap_lower_bound':str(free_output_gap),
        'reporter_work':'log(2)-1/2',
        'reporter_energy_increase':'1/8',
        'reporter_heat':'log(2)-5/8',
        'floating_displays_only':{'reporter_gain':math.erf(.25),
            'candidate_before_controller_proved_gap_using_exact_gain':math.erf(.25)/96,
            'free_explicit_test_proved_gap_using_exact_gain':math.erf(.25)**2/6,
            'reporter_work':math.log(2)-.5,'reporter_heat':math.log(2)-.625},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('ONE_BIT_CONTROLLER_CONSTANT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
