"""Bind executed controls and received source bytes; not a science audit."""
import ast,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/mechanism_selection_20261101'
OUT=ROOT/'outputs/mechanism_selection_20261101'
SRC=WORK/'sources'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sources=[]
    for packet,index,filename in (
        ('N1421.json',0,'pure_fast_whole_review.md'),
        ('N1421.json',1,'catalytic_fast_whole_review.md'),
        ('N1601.json',0,'latest_cover_acquisition_theorem.md'),
        ('N1601.json',7,'latest_arm_backbone_whole_review.md')):
        p=json.loads((SRC/packet).read_text());e=p['evidence'][index]
        actual=sha(SRC/filename);assert actual==e['sha256']
        sources.append({'file':str((SRC/filename).relative_to(ROOT)),
                        'governing_path':e['path'],'sha256':actual})
    for packet,tail,filename in (
        ('N1454.json','FULL_NONBALANCED_DORMANT_CLOSURE_CANDIDATE.md','full_dormant_source.md'),
        ('N1454.json','PARAMETRIC_INTERFACE_TRANSFER_CANDIDATE.md','parametric_transfer_source.md'),
        ('N1469.json','SOUND_TRACE_POOL_ACQUISITION.md','raw_sound_acquisition.md'),
        ('N1485.json','RAW_RANK_SPLIT_AND_TRANSFER.md','raw_rank_split.md')):
        p=json.loads((SRC/packet).read_text())
        e=next(x for x in p['evidence'] if x['path'].endswith('/'+tail))
        actual=sha(SRC/filename);assert actual==e['sha256']
        sources.append({'file':str((SRC/filename).relative_to(ROOT)),
                        'governing_path':e['path'],'sha256':actual})
    bindings=[]
    standard=('killed_pool_controls','residual_exit_controls','cooperative_pool_controls',
              'cooperative_exit_controls','cooperative_scope_controls',
              'cooperative_higher_order_pool_controls','cooperative_higher_order_exit_controls',
              'cooperative_higher_order_scope_controls')
    for name in standard:
        p=json.loads((OUT/(name+'.json')).read_text());actual=sha(WORK/(name+'.py'))
        assert p['script_sha256']==actual and p['status'].startswith('PASS')
        bindings.append({'result':name+'.json','source':name+'.py','sha256':actual,'status':p['status']})
    p=json.loads((OUT/'exact_stabilizer_controls.json').read_text())
    for field,name in (('source_sha256','exact_stabilizer.py'),('control_sha256','exact_stabilizer_controls.py')):
        assert p[field]==sha(WORK/name)
        bindings.append({'result':'exact_stabilizer_controls.json','source':name,'sha256':p[field]})
    assert p['independent_dense_Paulis_checked']==6312
    assert p['displayed_heuristic_counterexample']['displayed_Algorithm6']['dimension']==0
    assert p['larger_tensor_controls'][-1]['stabilizer_dimension']==63
    assert p['rare_support_case']['parity_contractions_for_extraction']==5
    p=json.loads((OUT/'cooperative_higher_order_scope_controls.json').read_text())
    assert p['import_sha256']==sha(WORK/'cooperative_scope_controls.py')
    failed=json.loads((OUT/'cooperative_exit_float_failure.json').read_text())
    assert failed['status'].startswith('FAILED')
    assert failed['script_sha256']==sha(WORK/'cooperative_exit_float_only_failed.py')
    head=json.loads((SRC/'head_scope_refresh.json').read_text())
    assert all(x['byte_identical'] for x in head['retained_packet_checks'])
    a=json.loads((SRC/'search_manifest.json').read_text())
    b=json.loads((SRC/'search_manifest_head.json').read_text())
    for row in head['retained_packet_checks']:
        key='knowledge/current/packets/'+row['packet']+'.json'
        assert a['outputs'][key]==b['outputs'][key]
    exit_rows=[]
    for name in ('cooperative_exit_controls','cooperative_higher_order_exit_controls'):
        p=json.loads((OUT/(name+'.json')).read_text());exit_rows+=p['rows']
        for row in p['rows']:
            assert max(row['certified_all_input_absolute_solution_errors'])<1e-45
            assert row['dormant_low_entrance_up_probability']==1.
    assert len(exit_rows)==9
    local_rows=[]
    for name in ('cooperative_pool_controls','cooperative_higher_order_pool_controls'):
        local_rows+=json.loads((OUT/(name+'.json')).read_text())['rows']
    assert len(local_rows)==32 and max(x['N'] for x in local_rows)==4096
    assert all(x['m']==6 and x['minimum_A']==3 for x in local_rows[-8:])
    assert local_rows[-1]['max_time_to_occupation_ratio']>0.25
    for f in WORK.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
    artifacts={str(f.relative_to(ROOT)):sha(f) for f in sorted(OUT.glob('*'))
               if f.is_file() and f.name!='verification.json'}
    artifacts.update({str(f.relative_to(ROOT)):sha(f) for f in sorted(WORK.glob('*.py'))})
    result={'status':'PASS source integrity and executed implementation bindings',
            'received_exact_source_matches':sources,'executed_bindings':bindings,
            'source_refresh':head,'local_killed_CME_systems':len(local_rows),
            'full_CME_interval_validated_systems':len(exit_rows),
            'full_CME_state_rows':sum(x['states'] for x in exit_rows),
            'largest_full_CME_system':max(x['states'] for x in exit_rows),
            'independent_dense_Pauli_checks':6312,
            'expected_failed_float_attempt_retained':True,
            'science':{'derivation_and_self_review':'COMPLETE_SOLO_AT_STATED_CONTRACT',
                       'independent_mathematical_review':'NOT_PERFORMED',
                       'new_Astra_scientific_acceptance':'NOT_CLAIMED',
                       'historical_novelty':'UNKNOWN','practical_advantage':'NOT_ACHIEVED',
                       'general_weakly_reversible_recurrence':'NOT_ACHIEVED','mission':'NOT_ACHIEVED'},
            'scope':'Integrity/finite implementation verification only; does not validate an infinite theorem, historical novelty or physical performance.',
            'artifacts':artifacts}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','local_killed_CME_systems','full_CME_interval_validated_systems',
                      'full_CME_state_rows','largest_full_CME_system','independent_dense_Pauli_checks','science')},indent=2))


if __name__=='__main__':main()
