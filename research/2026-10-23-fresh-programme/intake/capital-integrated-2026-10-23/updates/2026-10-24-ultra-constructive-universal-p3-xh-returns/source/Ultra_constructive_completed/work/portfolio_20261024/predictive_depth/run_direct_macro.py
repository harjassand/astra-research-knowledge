#!/usr/bin/env python3
"""Ordinary-count selected macro acquisition; no huge-count certificate rescue."""
import json
import math
import time
from pathlib import Path
import numpy as np
from quantum_shot_plant import ShotPlant
from direct_macro_learner import learn_macro
from finite_predictive_learner import compile_pattern_controller

ROOT = Path(__file__).resolve().parent


def plain(x):
    if isinstance(x,np.ndarray):
        return x.tolist()
    if isinstance(x,(np.floating,np.integer)):
        return x.item()
    if isinstance(x,dict):
        return {k:plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [plain(v) for v in x]
    return x


def main(shots=200000):
    start = time.perf_counter()
    pilot = json.loads((ROOT/'calibration_counts.json').read_text())
    selected = json.loads((ROOT/'learned_predictive_model.json').read_text())
    ps,fs = selected['preparations'],selected['tests']
    future_actions = sorted(set(f[0][0] for f in fs if f))
    plant = ShotPlant(seed=7912026)
    data = {'status':'SYNTHETIC_COUNT_ONLY_SELECTED_MACRO',
            'preparations':ps,'tests':fs,'architecture_rank_upper_bound':4,
            'abort_probability':0.15,'maximum_calls':128,
            'pilot_calibration':pilot,'macro':[]}
    for p in ps:
        for a in future_actions:
            data['macro'].append(plant.macro_counts(p,shots,0.15,a,128))
    (ROOT/'direct_macro_counts.json').write_text(json.dumps(data,indent=2)+'\n')
    # The operation learner receives the serialized counts and selected legal
    # interface only, exactly as saved. It imports no plant/private truth.
    model = learn_macro(json.loads((ROOT/'direct_macro_counts.json').read_text()))
    x0 = model['x0']
    success = model['ops']['success']@x0
    twice = model['ops']['success']@success
    test_index = fs.index([[2,0]])
    pred = {'success_probability':float(success[0]),
            'success_joint_test1':float(success[0]-success[test_index]),
            'success_conditional_test1':float(1-success[test_index]/success[0]),
            'two_success_probability':float(twice[0]),
            'two_success_joint_test1':float(twice[0]-twice[test_index]),
            'two_success_conditional_test1':float(1-twice[test_index]/twice[0])}
    # Fixed-INPUT probability statements can have useful ordinary-count
    # intervals even when the reusable ALL-INPUT operator bound is vacuous.
    cell = next(s for s in data['macro'] if s['preparation'] == [] and s['future_action'] == 2)
    n = cell['shots']
    successes = cell['counts']['success,0']+cell['counts']['success,1']
    joint = cell['counts']['success,1']/n
    conditional = cell['counts']['success,1']/successes
    initial_cells = [s for s in data['macro'] if s['preparation'] == []]
    pooled_n = sum(s['shots'] for s in initial_cells)
    pooled_success = sum(s['counts']['success,0']+s['counts']['success,1'] for s in initial_cells)
    alpha,number_statements = 0.01,3
    width = lambda trials: math.sqrt(math.log(2*number_statements/alpha)/(2*trials))
    tail = 0.85**128
    p = pooled_success/pooled_n
    p_lower = max(1e-15,p-width(pooled_n)-tail)
    conditional_tail = 2*tail/p_lower
    local = {'confidence_failure_probability':alpha,
             'scope':'FIXED_INITIAL_INPUT_AND_FIXED_FUTURE_TEST_ONLY',
             'native_success_probability':p,
             'success_probability_interval':[max(0,p-width(pooled_n)-tail),min(1,p+width(pooled_n)+tail)],
             'success_joint_test1':joint,
             'joint_test1_interval':[max(0,joint-width(n)-tail),min(1,joint+width(n)+tail)],
             'success_conditional_test1':conditional,
             'conditional_test1_interval':[max(0,conditional-width(successes)-conditional_tail),
                                          min(1,conditional+width(successes)+conditional_tail)],
             'joint_trials':n,'successful_trials_for_conditional':successes,
             'pooled_trials_for_success_probability':pooled_n,
             'conditional_binomial_bound_conditioned_on_success_count':True,
             'cap_to_unbounded_systematic_tail_bound':tail}
    # Truth is used AFTER count learning, for evaluation alone.
    ptuples = [tuple(p) for p in ps]
    ftuples = [tuple(tuple(z) for z in f) for f in fs]
    def exact_cell(p,f,z=()):
        actions = p+tuple(a for a,o in z+f)
        outcomes = (None,)*len(p)+tuple(o for a,o in z+f)
        return plant.evaluator_joint_probability(actions,outcomes)
    he = np.array([[exact_cell(p,f) for p in ptuples] for f in ftuples])
    be = {}
    for a in range(4):
        for o in range(2):
            hez = np.array([[exact_cell(p,f,((a,o),)) for p in ptuples] for f in ftuples])
            be[a,o] = hez@np.linalg.inv(he)
    true = compile_pattern_controller({'B':be,'x0':he[:,ptuples.index(())]},0.15)
    errors = {branch:float(np.linalg.norm(model['ops'][branch]-true[branch],np.inf))
              for branch in ['success','abort']}
    exact_previous = json.loads((ROOT/'COUNT_ACQUISITION_RESULTS.json').read_text())['controller']['EVALUATOR_ONLY_exact']
    scalar_errors = {k:abs(v-exact_previous[k]) for k,v in pred.items()}
    output = {'status':'SYNTHETIC_SELECTED_OPERATION_ACQUIRED_FROM_COUNTS',
              'shots_per_setting':shots,'new_macro_settings':len(data['macro']),
              'confidence_certificate':model['certificate'],
              'count_only_predictions':pred,'fixed_input_confidence_intervals':local,
              'EVALUATION_ONLY_branch_matrix_errors_infinity':errors,
              'EVALUATION_ONLY_scalar_prediction_errors':scalar_errors,
              'extra_acquisition_cost':{'full_process_reset_episodes':plant.reset_episodes,
                                        'represented_primitive_interventions':plant.primitive_interventions},
              'pilot_acquisition_cost_already_paid':{'full_process_reset_episodes':12800000,
                                                      'represented_primitive_interventions':38400000},
              'wall_seconds':time.perf_counter()-start,
              'scope':['Counts only enter direct_macro_learner.py.',
                       'Exact private propagation only generates synthetic sample distribution or post-training evaluation.',
                       'Capped at 128 calls; truncation error to unbounded target included.',
                       'No laboratory, CP-gauge, all-input accuracy or incumbent advantage claim.',
                       'Conservative reusable operator certificate must be reported even when vacuous.']}
    (ROOT/'DIRECT_MACRO_RESULTS.json').write_text(json.dumps(plain(output),indent=2)+'\n')
    (ROOT/'direct_macro_model.json').write_text(json.dumps(plain(model),indent=2)+'\n')
    print(json.dumps(plain(output),indent=2))


if __name__ == '__main__':
    main()
