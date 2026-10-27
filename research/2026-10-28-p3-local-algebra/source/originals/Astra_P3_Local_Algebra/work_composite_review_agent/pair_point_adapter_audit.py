#!/usr/bin/env python3
"""Actual small-field hypersurface counts and raw-wrapper callback replay.

Every small hypersurface is exhaustively evaluated, including its AS
coordinate. The raw36 callback replays counts derived from an explicit
16-element Gaussian-fiber scan; it is NOT a Lauder--Wan implementation.
"""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_chain_root','work_stationary_prior_agent'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_pair_counter import moment_hypersurface,compile_pair_family
from acquired_pair_terminal import acquire_pair_template,enumerated_terminal,EIGHT_MOMENT_INDICES
from field_descent import gf_mul,gf_trace


def arithmetic(h):
    d=h.bit_length()-1;q=1<<d
    multiplication=np.array([[gf_mul(a,b,h) for b in range(q)] for a in range(q)],dtype=np.uint8)
    trace=np.array([gf_trace(a,h) for a in range(q)],dtype=np.uint8)
    return d,q,multiplication,trace


def coordinates(q,d,variables):
    packed=np.arange(q**variables,dtype=np.uint32)
    return [((packed>>(d*i))&(q-1)).astype(np.uint8) for i in range(variables)]


def actual_hypersurface_count(h,variables,P):
    """Evaluate the supplied ordinary polynomial at every point, including w."""
    d,q,mul,trace=arithmetic(h);xs=coordinates(q,d,variables)
    value=np.zeros(q**variables,dtype=np.uint8)
    for exponent,coefficient in P.items():
        term=np.full(q**variables,coefficient,dtype=np.uint8)
        for index,power in enumerate(exponent):
            for _ in range(power):term=mul[term,xs[index]]
        value^=term
    return int(np.count_nonzero(value==0))


def independently_expanded_moment(h,gamma,tau,positive,negative):
    """Separate direct pair-phase formula, without the hypersurface builder."""
    d,q,mul,trace=arithmetic(h);pairs=positive+negative
    xs=coordinates(q,d,2*pairs+1);z=xs[0]
    phase=mul[tau,mul[z,mul[z,z]]]
    for pair in range(pairs):
        x,y=xs[2*pair+1],xs[2*pair+2]
        x2,y2=mul[x,x],mul[y,y]
        value=mul[x2,x]^mul[x,y2]^mul[y2,y]^mul[z,mul[x,y]]
        if pair>=positive:value^=mul[z,x2^y2]
        phase^=mul[gamma,value]
    ones=int(np.sum(trace[phase],dtype=np.uint64))
    return q**(2*pairs+1)-2*ones


def small_hypersurfaces():
    cases=[]
    for h in (3,7):
        d,q,_,_=arithmetic(h)
        for gamma in range(1,q):
            for tau in range(q):
                for i,j in EIGHT_MOMENT_INDICES:
                    reduction=moment_hypersurface(h,gamma,tau,i,j)
                    variables=reduction['variables']
                    P={tuple(row['exponents']):row['coefficient'] for row in reduction['polynomial']}
                    assert variables==2*(i+j)+2<=8
                    assert reduction['subtract_field_power']==variables-1
                    assert all(len(a)==variables and sum(a)<=3 for a in P)
                    w=[0]*variables;w[-1]=1;assert P[tuple(w)]==1
                    w[-1]=2;assert P[tuple(w)]==1
                    actual=actual_hypersurface_count(h,variables,P)
                    moment=independently_expanded_moment(h,gamma,tau,i,j)
                    assert actual-q**(variables-1)==moment,(h,gamma,tau,i,j,actual,moment)
                    cases.append(dict(d=d,gamma=gamma,tau=tau,moment_indices=[i,j],
                        variables=variables,hypersurface_count=actual,
                        subtract=q**(variables-1),independent_character_moment=moment,
                        actual_hypersurface_assignments=q**variables,
                        expanded_character_assignments=q**(variables-1)))
    return cases


def polynomial_key(h,variables,P):
    return h,variables,tuple(sorted(P.items()))


def raw_wrapper_replay():
    source_path=ROOT/'work_chain_root/contact_field_36_input.json'
    source=json.loads(source_path.read_text())
    reference=json.loads((ROOT/'work_chain_root/contact_field_results.json').read_text())['raw_field_case']
    field_h=reference['field_modulus'];d=reference['field_degree'];q=1<<d
    H={tuple(row['exponents']):row['coefficient'] for row in reference['homogeneous_cubic']}
    template=acquire_pair_template(field_h,H)
    field_sum,scan=enumerated_terminal(template)
    lookup={};expected_indices=[index for index in EIGHT_MOMENT_INDICES if any(index)]
    for i,j in expected_indices:
        reduction=moment_hypersurface(field_h,template['gamma'],template['radial_cubic'],i,j)
        P={tuple(row['exponents']):row['coefficient'] for row in reduction['polynomial']}
        number=q**reduction['subtract_field_power']+scan['exact_joint_moments'][i][j]
        lookup[polynomial_key(field_h,reduction['variables'],P)]=(i,j,number)
    assert len(lookup)==7
    actual_calls=[]
    def explicitly_replayed_point_counter(h,variables,P):
        key=polynomial_key(h,variables,P)
        assert key in lookup,'wrapper changed a manufactured coefficient or field parameter'
        i,j,number=lookup[key]
        actual_calls.append(dict(moment_indices=[i,j],variables=variables,returned_cardinality=number,
            backend='test-only replay prepared by an explicit 16-element field scan'))
        return number
    result=compile_pair_family(source['polynomial'],source['n'],
        point_counter=explicitly_replayed_point_counter,field_bit_budget=0)
    assert result['signed_count']==reference['reference']
    assert result['zero_count']==reference['zero_count']
    assert [tuple(row['moment_indices']) for row in actual_calls]==expected_indices
    assert len(result['terminal_evidence'])==1
    evidence=result['terminal_evidence'][0]
    assert evidence['supplied_point_counter_executed'] is True
    assert evidence['field_elements_enumerated_by_wrapper']==0
    assert evidence['supplied_backend_internal_work_reported'] is False
    assert 'field_elements_enumerated' not in evidence
    assert [tuple(row['moment_indices']) for row in evidence['point_count_calls']]==expected_indices
    assert max(row['variables'] for row in evidence['point_count_calls'])==8
    acquired_template=result['acquired_pair_template']
    for key,value in template.items():
        if key=='normalized_polynomial':
            expected_poly={tuple(row['exponents']):row['coefficient'] for row in value}
            actual_poly={tuple(row['exponents']):row['coefficient'] for row in acquired_template[key]}
            assert actual_poly==expected_poly
        else:assert acquired_template[key]==value,(key,acquired_template[key],value)
    result.update(audit_method='transparent callback replay, not Lauder--Wan execution',
        callback_calls=actual_calls,reference_field_sum=field_sum,
        callback_preparation_field_values_explicitly_enumerated=scan['field_elements_enumerated'],
        generic_point_count_engine_implemented=False,
        generic_polynomial_point_count_execution=False,practical_speed_claim=False,
        wrapper_enumeration_metadata_scope='zero is reported only for the wrapper; opaque callback work is not claimed',
        callback_scope_fields_explicitly_verified=True)
    return result


if __name__=='__main__':
    small=small_hypersurfaces();raw=raw_wrapper_replay()
    result=dict(status='all exact assertions passed',hypersurface_cases=small,raw_wrapper_replay=raw,
        actual_hypersurface_assignments=sum(row['actual_hypersurface_assignments'] for row in small),
        independent_expanded_character_assignments=sum(row['expanded_character_assignments'] for row in small),
        generic_point_count_engine_implemented=False)
    Path(__file__).with_name('pair_point_adapter_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],hypersurface_cases=len(small),
        actual_hypersurface_assignments=result['actual_hypersurface_assignments'],
        independent_character_assignments=result['independent_expanded_character_assignments'],
        raw_original_variables=raw['original_variables'],raw_signed_count=raw['signed_count'],
        raw_zero_count=raw['zero_count'],point_counter_calls=len(raw['callback_calls']),
        callback_preparation_field_values_explicitly_enumerated=raw['callback_preparation_field_values_explicitly_enumerated'],
        generic_point_count_engine_implemented=False)))
