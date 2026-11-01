"""Bind the actual source, scripts, reports and their scoped self-checks."""
import json,hashlib,platform,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];WORK=ROOT/'work/coherent_inference_20261101';OUT=ROOT/'outputs/coherent_inference_20261101'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    names=('opening_controls','collective_model','phase_spin_receiver','warm_controller_receiver',
           'warm_gain_controls','encoded_readout_controls','thermal_readout_controls',
           'parallel_readout_controls','interval_controls','matched_controls','lambda_read_controls')
    bound=[];records={}
    for name in names:
        p=WORK/(name+'.py');q=OUT/(name+'.json');d=json.loads(q.read_text())
        assert d['script_sha256']==sha(p),(name,'stale output binding')
        records[name]=d
        bound.append({'script':str(p.relative_to(ROOT)),'sha256':sha(p),
                      'output':str(q.relative_to(ROOT)),'output_sha256':sha(q),'status':d.get('status','not specified')})
    core=('warm_gain_controls','encoded_readout_controls','thermal_readout_controls',
          'parallel_readout_controls','interval_controls','matched_controls','lambda_read_controls')
    assert all(records[n]['status'].startswith('PASS') for n in core)
    encoded=records['encoded_readout_controls'];thermal=records['thermal_readout_controls']
    assert encoded['enumerated_physical_Kraus_histories']==34992
    assert encoded['accepted_wrong_logical_label_Choi_block_norm']==0
    assert encoded['full_source_logical_Choi_trace_preservation_residual']<2e-11
    assert thermal['logical_input_offdiagonal_source_channel_norm']<2e-11
    assert thermal['full_source_Choi_TP_residual']<2e-11
    assert records['matched_controls']['minimum_concatenation_level_for_total_error_below_1e_8']=={'sharp':4,'ordinary':4}
    sources=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((WORK/'sources').glob('*.pdf'))]
    reports=[]
    for name in ('RESULT.txt','PROOF.txt','OPTICAL_FINDINGS.txt','SOURCES_AND_COMPARISON.txt','REPRODUCE.txt'):
        p=OUT/name;assert p.is_file();reports.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
    old=[]
    for name in ('external_openings_20261101/OPENING.txt','external_openings_20261101/CONSTRUCTION.txt',
                 'external_openings_20261101/failed_transfers.json','external_openings_20261101/verification.json',
                 'latched_gate_20261101/RESULT.txt','latched_gate_20261101/THEOREM.txt'):
        p=ROOT/'outputs'/name
        if p.exists():old.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
    assert len(old)>=4
    first=ROOT/'outputs/external_openings_20261101'
    first_record=json.loads((first/'verification.json').read_text())
    for filename,digest in first_record['original_source_sha256'].items():
        assert sha(ROOT/'work/external_openings_20261101/sources'/filename)==digest,filename
    for filename,script in first_record['script_output_bindings'].items():
        old_output=json.loads((first/filename).read_text())
        assert old_output['script_sha256']==sha(ROOT/'work/external_openings_20261101'/script),script
    coord=Path('producer-workspace/astra-zenodo-opening-20261101')
    comparator=[]
    for name in ('GAUSSIAN_COMPARATOR_AT_STAGE1_POINT.txt','TREE_PRECISION_OBSERVATION.txt'):
        p=coord/name;assert p.is_file();comparator.append({'path':str(p),'sha256':sha(p)})
    result={'status':'PASS script/output bindings and scoped executable controls',
       'scientific_status':{'civilisation_capability':'NOT_ACHIEVED','historical_novelty':'UNKNOWN',
          'independent_audit':'NOT_PERFORMED','hardware_operating_region':'NOT_QUALIFIED',
          'new_sharp_read_bound_vs_matched_ordinary':'same selected encoding level; no demonstrated capability advantage'},
       'python':sys.version,'platform':platform.platform(),'bound_outputs':bound,'source_pdfs':sources,
       'reports':reports,'preserved_earlier_artifacts_present':old,'coordinator_comparators':comparator,
       'preserved_first_stage_binding_checks':{'original_sources':len(first_record['original_source_sha256']),
                                             'script_output_bindings':len(first_record['script_output_bindings'])},
       'scope':'hashes bind artifacts only; they do not establish scientific correctness, novelty, acceptance or measured hardware performance',
       'verification_script_sha256':sha(Path(__file__))}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'bound_outputs':len(bound),'core_scientific_self_checks':len(core),
                      'source_pdfs':len(sources),'reports':len(reports),'scientific_status':result['scientific_status']},indent=2))
if __name__=='__main__':main()
