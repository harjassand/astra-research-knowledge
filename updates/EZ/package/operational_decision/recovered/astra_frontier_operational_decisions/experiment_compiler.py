"""Construct the nuisance-insensitive probe from the known interaction templates.
No fitted response derivative or precomputed sensor state is an input.
The output is a mathematical operation specification, not a hardware execution.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from finite_certificates import occ,fstr
from decision_certificate import pi_bounds

def labels(a):
    n=[occ(a,i) for i in range(4)]
    return (n[0]*(n[1]+n[2]),n[3]*(n[1]+n[2]),n[1]*n[2],n[0]*n[3])

def compile_probe(folder='results'):
    candidates=[]
    for a in range(16):
        if occ(a,1)==1 and occ(a,3)==0:
            b=a^4^1
            candidates.append({'state_a':format(a,'04b'),'state_b':format(b,'04b'),
                               'label_a':labels(a),'label_b':labels(b),
                               'difference':tuple(x-y for x,y in zip(labels(a),labels(b)))})
    admitted=[r for r in candidates if not any(r['difference'])]
    assert len(admitted)==1 and admitted[0]['state_a']=='0100' and admitted[0]['state_b']=='0001'
    # Known complex hopping on the spanning tree + onsite phase control implements
    # any 4x4 one-excitation unitary: six Givens rotations, each routed using <=5
    # adjacent rotations, plus four phases. <=20*pi/Gamma is a safe duration.
    pi_lo,pi_hi=pi_bounds();Gamma=4096
    time_hi=20*pi_hi/Gamma
    noise_tv=F(1,100)*time_hi
    tcmd=(pi_lo/4-F(1,2**17)); tcmd=F(tcmd.numerator*2**32//tcmd.denominator,2**32)
    jitter=F(1,2**18)
    assert tcmd+jitter<pi_lo/4
    timing_error=pi_hi/4-tcmd+jitter
    timing_tv=F(101,100)*timing_error
    available_other=F(1,2000)-noise_tv-timing_tv
    assert available_other>F(3,10000)
    out={'candidate_pairs':candidates,'admitted_probe_subspaces':admitted,
         'isolated_link':[1,3],'initial_state':'0100','unknown_link_exposure':'pi/4',
         'known_readout_isometry':'row_a = sqrt(2/3) <v_a|, (n_a.sigma)|v_a>=-|v_a>; three rows, two columns',
         'readout_realization':'complete to a 4x4 number-conserving unitary using empty sites; known complex hopping on 1-0-2-3 tree and site phases; switch the unknown 1-3 link off',
         'sufficient_known_readout_amplitude':Gamma,
         'conservative_readout_duration_upper':fstr(time_hi),
         'downward_rounded_probe_command':fstr(tcmd),'allowed_probe_timing_jitter':fstr(jitter),
         'probe_state_TV_timing_allowance':fstr(timing_tv),
         'actual_unknown_link_exposure_cap':'pi/4; follows from the command and jitter guard',
         'dephasing_TV_during_readout_upper':fstr(noise_tv),
         'remaining_aggregate_preparation_switching_timing_calibration_TV_allowance':fstr(available_other),
         'scope':'sufficient finite control-bandwidth requirement only; not an implemented pulse train or validated experimental device; preparation/reset/readout times remain physical resources'}
    Path(folder,'experiment_construction.json').write_text(json.dumps(out,indent=2))
    return out
if __name__=='__main__':print(json.dumps(compile_probe(),indent=2))
