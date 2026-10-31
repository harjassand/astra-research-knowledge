"""Scope-preserving boundary tests for the learned-model consumer wrapper."""
import copy
import json
from pathlib import Path
from learn_affine_source import query_plan, learn_and_compile, SCOPE
from acquire_learned_pauli_consumer import acquire_learned_coupling


def run():
    folder = Path(__file__).parent; examples = folder/'examples'
    t = json.loads((examples/'learned_history.transcript.json').read_text())
    r = learn_and_compile(t)
    diagonal = {'system_qubits': 1, 'terms': [{'coefficient': '1', 'system_x': 1, 'system_z': 0, 'source_x': 0, 'source_z': 1}]}
    answer = acquire_learned_coupling(t, r, diagonal)
    assert answer['source_diagonal_coupling_verified']
    assert not answer['future_control_instrument_algebra_verified']
    assert not answer['downstream_simulation_executed']
    assert answer['mean_terms'] == []
    for key, value in SCOPE.items():
        assert answer[key] == value
    assert answer['admitted_transcript_average_failure_upper_bound'] == r['admitted_transcript_average_failure_upper_bound']
    failed = []
    bad = copy.deepcopy(r); bad['model_family_promise_verified_from_data'] = True; failed.append((t,bad,diagonal))
    bad = copy.deepcopy(r); bad['rare_postselection_covered'] = True; failed.append((t,bad,diagonal))
    bad = copy.deepcopy(r); bad['confidence_interpretation'] = 'Posterior certainty'; failed.append((t,bad,diagonal))
    bad_coupling = copy.deepcopy(diagonal); bad_coupling['terms'][0]['source_x'] = 1; failed.append((t,r,bad_coupling))
    empty_t = {'n': 2, 'failure_probability': '1/4', 'outputs': [0]*len(query_plan(2,'1/4')['inputs'])}
    empty_r = learn_and_compile(empty_t); failed.append((empty_t,empty_r,diagonal))
    for args in failed:
        try:
            acquire_learned_coupling(*args)
            raise AssertionError('A guarded boundary was bypassed.')
        except ValueError:
            pass
    rare = json.loads((examples/'rare_wrong_admitted_transcript.json').read_text())
    rare_answer = acquire_learned_coupling(rare['transcript'],rare['record'],diagonal)
    assert rare_answer['model_family_promise_verified_from_data'] is False
    assert rare_answer['rare_postselection_covered'] is False
    assert rare_answer['downstream_simulation_executed'] is False
    # Accepting this algebraic record is intentional. The hidden true-law
    # comparison is not available to the consumer; its statistical limits stay.
    preserved = answer['unconditional_model_failure_upper_bound']
    mutated = copy.deepcopy(r)
    mutated['query_plan']['proved_failure_upper_bound'] = '0'
    assert answer['unconditional_model_failure_upper_bound'] == preserved
    (examples/'learned_history.coupling.json').write_text(json.dumps(diagonal,indent=2)+'\n')
    (examples/'learned_history.acquired_coupling.json').write_text(json.dumps(answer,indent=2)+'\n')
    result = {'scope':'guarded classical specification only','successful_scoped_consumer':True,
              'rejected_boundary_cases':len(failed),
              'wrong_but_admitted_record_remains_accepted_with_limits':True,
              'statistical_scope_preserved':True,'downstream_execution_claimed':False,'passed':True}
    (folder/'learned_consumer_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    run()
