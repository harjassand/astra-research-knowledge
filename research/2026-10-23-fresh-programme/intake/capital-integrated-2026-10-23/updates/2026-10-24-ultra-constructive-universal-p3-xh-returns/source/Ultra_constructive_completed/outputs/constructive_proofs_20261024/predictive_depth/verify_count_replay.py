#!/usr/bin/env python3
"""Replay learned objects with every plant/private-model import forbidden."""
import builtins
import json
import math
from pathlib import Path
import numpy as np

original_import = builtins.__import__
def no_plant_import(name,*args,**kwargs):
    if 'quantum_shot_plant' in name:
        raise AssertionError('Private plant import is forbidden in count replay')
    return original_import(name,*args,**kwargs)
builtins.__import__ = no_plant_import

from finite_predictive_learner import learn,compile_pattern_controller,predict_controller,serializable
from direct_macro_learner import learn_macro

ROOT = Path(__file__).resolve().parent


def main():
    data = json.loads((ROOT/'calibration_counts.json').read_text())
    model = learn(data)
    saved = json.loads((ROOT/'learned_predictive_model.json').read_text())
    assert serializable(model) == saved
    compiled = compile_pattern_controller(model,.15)
    p = predict_controller(model,compiled)
    report = json.loads((ROOT/'COUNT_ACQUISITION_RESULTS.json').read_text())
    assert p == report['controller']['learned']
    assert compiled['causal_row_error'] < 1e-12
    assert compiled['continuation_spectral_radius'] < 1
    assert model['certificate']['rank_4_certified_given_architecture_bound']
    assert model['certificate']['inverse_neumann_product'] < 1
    # Do not silently promote these examples to a uniform-policy certificate.
    assert model['certificate']['primitive_instrument_quotient_error_upper_bound'] > .15/.85
    macro_data = json.loads((ROOT/'direct_macro_counts.json').read_text())
    macro = learn_macro(macro_data)
    saved_macro = json.loads((ROOT/'direct_macro_model.json').read_text())
    assert np.array_equal(macro['H'],saved_macro['H'])
    for branch in ['success','abort']:
        assert np.array_equal(macro['ops'][branch],saved_macro['ops'][branch])
    mr = json.loads((ROOT/'DIRECT_MACRO_RESULTS.json').read_text())
    assert macro['certificate'] == mr['confidence_certificate']
    assert macro['certificate']['joint_terminal_instrument_quotient_error_upper_bound'] > 1
    assert all(sum(s['counts'].values()) == s['shots'] for s in macro_data['macro'])
    macro_calls = sum(s['sampled_macro_native_calls']+s['shots']*(len(s['preparation'])+1)
                      for s in macro_data['macro'])
    assert macro_calls == mr['extra_acquisition_cost']['represented_primitive_interventions']
    # A previously collected held-out memory witness: histories differ, but
    # BOTH next interventions prepare the same visible |+> and measure Y.
    w = report['reset_word_heldout'][0]
    n = w['shots_each']
    difference = (w['history0_test1']-w['history1_test1'])/n
    half_width = 2*math.sqrt(math.log(4/.01)/(2*n))
    assert difference-half_width > 0
    output = {'status':'PASS','private_plant_import_forbidden':True,
              'pilot_model_exactly_replayed':True,'direct_macro_exactly_replayed':True,
              'macro_integer_cost_replayed':macro_calls,
              'uniform_policy_certificate':'VACUOUS_AT_RECORDED_SHOTS',
              'all_input_macro_certificate':'VACUOUS_AT_RECORDED_SHOTS',
              'heldout_memory_witness':{'history_actions':[0,3],'common_next_action':2,
                 'shots_each':n,'empirical_future_probability_difference':difference,
                 'confidence_failure_probability':.01,
                 'difference_interval':[difference-half_width,difference+half_width],
                 'scope':'History dependence survives the same visible-system causal break; no irreducibly quantum-memory advantage certified.'}}
    (ROOT/'COUNT_REPLAY_CHECKS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
