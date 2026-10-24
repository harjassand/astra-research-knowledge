#!/usr/bin/env python3
"""Synthetic acquisition/evaluation driver; private truth never enters learner.

Produces count data, then passes ONLY that data to the learner. Exact private
evaluation, when used, is after training and separately labelled. Nothing here
is physical-device acquisition or a performance advantage experiment.
"""
import itertools
import json
import time
from pathlib import Path
import numpy as np

from quantum_shot_plant import ShotPlant
from finite_predictive_learner import (learn,compile_pattern_controller,
                                     predict_controller,search_reset_word,
                                     serializable)

ROOT = Path(__file__).resolve().parent


def plain(value):
    if isinstance(value,np.ndarray):
        return value.tolist()
    if isinstance(value,(np.integer,np.floating)):
        return value.item()
    if isinstance(value,dict):
        return {k:plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [plain(v) for v in value]
    return value


def main(shots=200000,heldout=100000):
    started = time.perf_counter()
    plant = ShotPlant(seed=146071)
    data = {'status':'SYNTHETIC_SHOT_DATA',
            'number_actions':plant.number_actions,
            'number_outcomes':plant.number_outcomes,
            'observable_rank_upper_bound':plant.observable_rank_upper_bound,
            'maximum_length':3,'shots_per_setting':shots,'settings':[]}
    for actions in itertools.product(range(4),repeat=3):
        data['settings'].append({'actions':list(actions),
                                 'counts':plant.episode_counts(actions,shots)})
    calibration_ledger = {'reset_episodes':plant.reset_episodes,
                          'primitive_interventions':plant.primitive_interventions}
    # This serialization is the actual boundary: no density matrix, Kraus
    # operator, exact expectation, U or eigenbasis is given to learn().
    data_path = ROOT/'calibration_counts.json'
    data_path.write_text(json.dumps(data,indent=2)+'\n')
    serialized_data = json.loads(data_path.read_text())
    model = learn(serialized_data,alpha=0.01)
    model_path = ROOT/'learned_predictive_model.json'
    model_path.write_text(json.dumps(serializable(model),indent=2)+'\n')
    delta = 0.15
    compiled = compile_pattern_controller(model,delta)
    predictions = predict_controller(model,compiled)
    before_heldout = plant.primitive_interventions
    heldout_single = plant.controller_experiment(heldout,delta)
    heldout_double = plant.repeated_controller_experiment(heldout,delta)
    reset = search_reset_word(model,maximum_length=4)
    reset_data = []
    for repeats in [0,1,2,4,8]:
        result = plant.reset_word_experiment(reset['word'],repeats,heldout)
        result['repetitions'] = repeats
        result['empirical_test1_difference'] = (result['history0_test1']-result['history1_test1'])/heldout
        reset_data.append(result)
    # Post-training independent evaluation using exact private probabilities.
    # Only this evaluation block invokes the private truth API.
    ps,fs = model['preparations'],model['tests']
    def exact_cell(p,f,z=()):
        actions = tuple(p)+tuple(a for a,o in z+f)
        outcomes = (None,)*len(p)+tuple(o for a,o in z+f)
        return plant.evaluator_joint_probability(actions,outcomes)
    he = np.array([[exact_cell(p,f) for p in ps] for f in fs])
    be = {}
    for a in range(4):
        for o in range(2):
            hz = np.array([[exact_cell(p,f,((a,o),)) for p in ps] for f in fs])
            be[a,o] = hz@np.linalg.inv(he)
    xe = np.array([exact_cell((),f) for f in fs])
    exact_model = {'B':be,'x0':xe}
    exact_compiled = compile_pattern_controller(exact_model,delta)
    exact_predictions = predict_controller(exact_model,exact_compiled)
    actual_errors = {key:abs(predictions[key]-exact_predictions[key]) for key in predictions}
    result = {'status':'SYNTHETIC_KNOWN_ARCHITECTURE_COUNTS_ONLY_LEARNING',
              'seed':146071,'calibration_ledger':calibration_ledger,
              'calibration_settings':64,'serialized_calibration_bytes':data_path.stat().st_size,
              'serialized_model_bytes':model_path.stat().st_size,
              'H_singular_values':np.linalg.svd(model['H'],compute_uv=False).tolist(),
              'H_exact_singular_values_EVALUATION_ONLY':np.linalg.svd(he,compute_uv=False).tolist(),
              'learned_basis_preparations':ps,'learned_basis_tests':fs,
              'confidence_certificate':model['certificate'],
              'controller':{'abort_probability':delta,'classical_states':2,
                            'learned':predictions,'EVALUATOR_ONLY_exact':exact_predictions,
                            'absolute_errors':actual_errors,
                            'continuation_spectral_radius':compiled['continuation_spectral_radius'],
                            'resolvent_2_condition_number':compiled['resolvent_2_condition_number'],
                            'causal_row_error':compiled['causal_row_error'],
                            'heldout_single':heldout_single,'heldout_reused_twice':heldout_double},
              'reset_word':reset,'reset_word_heldout':reset_data,
              'total_ledger':{'reset_episodes':plant.reset_episodes,
                              'primitive_interventions':plant.primitive_interventions,
                              'heldout_primitive_interventions':plant.primitive_interventions-before_heldout},
              'wall_seconds':time.perf_counter()-started,
              'scope':['Known hidden-qubit architecture; unknown parameters to learner.',
                       'Only four legal prepare/measure actions; no arbitrary quantum intervention claim.',
                       'Multinomial batching accelerates simulation, not the charged shot cost.',
                       'Exact private probabilities only used after count-only training for evaluation.',
                       'No physical acquisition, novelty or incumbent advantage established.']}
    (ROOT/'COUNT_ACQUISITION_RESULTS.json').write_text(json.dumps(plain(result),indent=2)+'\n')
    print(json.dumps(plain({'calibration':calibration_ledger,
                           'singular_values':result['H_singular_values'],
                           'certificate':model['certificate'],
                           'predictions':predictions,'errors':actual_errors,
                           'reset_word':reset,'total':result['total_ledger'],
                           'wall_seconds':result['wall_seconds']}),indent=2))


if __name__ == '__main__':
    main()
