#!/usr/bin/env python3
"""Reacquire an existing raw Boolean fixture and acquire the pair terminal.

The moment oracle is populated by an explicitly enumerated small-field
reference.  This validates the complete interface, not a generic
Lauder--Wan implementation.
"""
from acquired_pair_terminal import *
from acquired_contact_counter import compile_contact
import json


def run():
    root=Path(__file__).resolve().parents[1]
    source_path=root/'work_chain_root/contact_field_36_input.json'
    reference_path=root/'work_chain_root/contact_field_results.json'
    source=json.loads(source_path.read_text())
    reference=json.loads(reference_path.read_text())['raw_field_case']
    records=[]
    def terminal(h,b,H):
        certificate=acquire_pair_template(h,H)
        value,validation=enumerated_terminal(certificate)
        moments=validation['exact_joint_moments']
        calls=[]
        def checked_moment_backend(h1,gamma,tau,i,j):
            assert (h1,gamma,tau)==(h,certificate['gamma'],certificate['radial_cubic'])
            calls.append([i,j])
            return moments[i][j]
        eight_result,eight_counts=moment_terminal_eight(certificate,checked_moment_backend)
        assert eight_result==value
        assert eight_counts==validation['eight_state_multiplicities']
        assert calls==[list(index) for index in EIGHT_MOMENT_INDICES if any(index)]
        records.append(dict(acquired_template=certificate,terminal_validation=validation,
            fixed_variable_moment_backend='test-only replay of explicitly enumerated moments',
            point_count_moment_calls=calls,zeroth_moment_method='exact binary Gaussian',
            production_reconstruction='eight states'))
        return eight_result
    result=compile_contact(source['polynomial'],source['n'],field_terminal=terminal)
    assert result['signed_count']==reference['reference']
    assert result['zero_count']==reference['zero_count']
    assert len(records)==1 and records[0]['acquired_template']['field_elements_enumerated_during_acquisition']==0
    result.update(raw_source=str(source_path),independent_reference=reference['reference'],
        terminal_template_records=records,
        general_fixed_variable_point_count_backend_implemented=False,
        practical_speed_claim=False)
    Path(__file__).with_name('raw_pair_terminal_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(original_binary_variables=result['original_variables'],
        field_degree=result['field_degree'],module_rank=result['module_dimension'],
        signed_count=result['signed_count'],zero_count=result['zero_count'],
        centroid_dimension=result['centroid_dimension'],
        field_values_enumerated_during_template_acquisition=0,
        field_values_enumerated_for_test_moments=records[0]['terminal_validation']['field_elements_enumerated'])))


if __name__=='__main__':run()
