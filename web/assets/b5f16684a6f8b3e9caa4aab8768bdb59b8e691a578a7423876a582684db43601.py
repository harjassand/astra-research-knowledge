#!/usr/bin/env python3
"""Independent exact record-level checks; no sampler or peer imports."""
from fractions import Fraction as F
from pathlib import Path
import json, time
HERE=Path(__file__).resolve().parent
def rotation(v,g):
    x,y,z=v
    if g=='H': return z,-y,x
    if g=='S': return -y,x,z
    if g=='X': return x,-y,-z
    raise AssertionError(g)
def check(name):
    d=json.loads((HERE/'evidence'/name).read_text()); N=d['parameter_contract']['N']
    r2=F(d['parameter_contract']['r0_squared']); errors=d['numerical_error_certificate']
    assert F(d['total_numerical_error_with_local_output_upper'])<=F(errors['requested_numerical_epsilon'])
    assert not any(isinstance(x,float) for x in errors.values())
    for m in d['states']: assert sum(F(x)**2 for x in m)<=r2
    o=d['local_output']; local=list(map(F,o['dyadic_local_Bloch'])); D=o['common_denominator']
    weights=o['Pauli_axis_integer_weights']; assert sum(weights)==D and all(n>=0 for n in weights)
    assert sum(map(abs,local))<1
    for i in range(3): assert F(weights[i],D)==abs(local[i])
    gate_total=0
    for t in o['gate_transcript']:
        v=(0,0,1)
        for g in t['gates_in_application_order']: v=rotation(v,g); gate_total+=1
        label=t['branch']
        if label.startswith('I/2'): assert v in [(0,0,1),(0,0,-1)]
        else:
            expected=[0,0,0]; expected['XYZ'.index(label[0])]=1 if label[-1]=='+' else -1
            assert tuple(expected)==v
    assert gate_total==o['local_ideal_gate_count_executed']
    assert len(o['gate_transcript'])==o['sites_transcript_executed']
    assert o['complete_N_site_transcript']==(o['sites_transcript_executed']==N)
    bitlog=d.get('random_prefix_transcript')
    if bitlog is not None:
        assert all(0<=x['integer']<(1<<x['bits']) for x in bitlog)
        assert sum(x['bits'] for x in bitlog)==d['costs']['random_bits_used']
    return {'name':name,'N':N,'states_checked':len(d['states']),
        'gate_words_checked':len(o['gate_transcript']),'exact_gates_checked':gate_total,
        'complete_output_description':o['complete_N_site_transcript'],
        'random_prefix_ledger_checked':bitlog is not None,
        'numerical_error_upper_rational':d['total_numerical_error_with_local_output_upper']}
def main():
    start=time.perf_counter()
    cases=[check(n) for n in ['N4096_replay.json','N4096_nondiagonal_replay.json','N4096_OS_sample.json','N2p48_replay.json']]
    budgets=[]
    for name in ['N2p48_public_budget.json','N2p48_error_point1_budget.json']:
        b=json.loads((HERE/'evidence'/name).read_text())
        bound=F(b['combined_averaged_Gibbs_trace_error_upper_compact'])
        assert b['cone']['certifies_cone_error_at_most_2_to_minus99']
        assert F(b['cone']['trace_error_upper'])==F(1,1<<99)
        assert bound<1
        if 'point1' in name: assert bound<F(1,10)
        budgets.append({'name':name,'rational_scientific_bound':str(bound)})
    result={'status':'PASS_EXACT_RECORD_CHECKS','scope':'Own independent JSON/Fraction/Clifford reconstruction; not an all-N proof, independent code audit or Monte Carlo error check',
        'cases':cases,'public_budgets':budgets,'wall_seconds':time.perf_counter()-start}
    (HERE/'evidence/record_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'all_gate_words_checked':sum(x['gate_words_checked'] for x in cases),'wall_seconds':result['wall_seconds']}))
if __name__=='__main__': main()
