"""Verify saved receipts only; no physics simulation or source writes."""
from pathlib import Path
import ast
import hashlib
import json
import platform

ROOT=Path(__file__).resolve().parent
SOURCE=Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')


def read(name):return json.loads((ROOT/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    checks=[]
    for p in ROOT.glob('*.py'):ast.parse(p.read_text());checks.append({'syntax':p.name,'passed':True})
    b=read('BINNED_RESULTS.json');bc=read('BINNED_CHECK_RESULTS.json')
    differences={}
    for control in bc['cases']:
        old=next(x for x in b['cases'] if x['parts']==control['parts'])
        differences[str(control['parts'])]=abs(old['metrics']['accepted_Choi_infidelity']-control['metrics']['accepted_Choi_infidelity'])
    assert max(differences.values())<1e-7
    for control in b['no_q_transition_detector_controls']:
        assert .019<1-control['metrics']['acceptance_mixed_code']<.021
    checks.append({'binned_cutoff_frequency_convergence':differences,'passed':True})
    alt=read('ALTERNATIVE_CONTROL_RESULTS.json')
    assert alt['EF_shelving_alternative']['independent_EF_matrix_checks']==27
    assert alt['EF_shelving_alternative']['max_EF_formula_matrix_error']<1e-12
    checks.append({'EF_float_matrix_identity_cases':27,'maximum_error':alt['EF_shelving_alternative']['max_EF_formula_matrix_error'],'passed':True})
    best=read('PAIR_MODULATED_SMOOTH_CHECK_RESULTS.json')
    case=best['result']['count_threshold_cases'][0]
    ac=next(x for x in alt['ancilla_comparator'] if x['cycle_us']==3.8)
    assert case['accepted_Choi_infidelity']>ac['metrics']['accepted_Choi_infidelity']
    assert case['accepted_Choi_infidelity']>=case['accepted_terminal_outside_GF_mass']/case['code_acceptance']
    assert min(best['result']['represented_unconditional_traces_g_f_e'])>.9999
    assert max(best['result']['unconditional_cutoff_population_g_f_e'])<1e-6
    prev=read('PAIR_MODULATED_SATURATED_CHECK_RESULTS.json')['result']['count_threshold_cases'][0]
    checks.append({'best_completed_pair_error':case['accepted_Choi_infidelity'],
                   'same_duration_ancilla_error':ac['metrics']['accepted_Choi_infidelity'],
                   'failure_margin_percentage_points':100*(case['accepted_Choi_infidelity']-ac['metrics']['accepted_Choi_infidelity']),
                   'previous_grid_and_envelope_change_percentage_points':100*abs(case['accepted_Choi_infidelity']-prev['accepted_Choi_infidelity']),
                   'passed_receipt_consistency':True,'numerical_convergence_certified':False})
    claims=read('CLAIMS.json')
    for claim in claims['claims']:
        for rel in claim['evidence']:
            if rel!='SOURCE_MANIFEST.json':assert (ROOT/rel).is_file(),(claim['id'],rel)
    assert claims['mission_achieved'] is False
    checks.append({'claim_evidence_links':True,'mission_completion_claim':False})
    source_files=['outputs/ASTRA_GENESIS_HANDOFF.txt','outputs/STRONGEST_VERIFIED_RESULT.txt',
                  'work/phase5/quantum_operation/HANDOFF.txt','work/phase6/floquet_readout_audit/HANDOFF.txt',
                  'work/phase5/quantum_operation/floquet_record_instrument.py',
                  'work/phase5/quantum_operation/floquet_erasure_readout.py',
                  'work/phase5/quantum_operation/echoed_curvature_readout.py',
                  'work/phase5/quantum_operation/floquet_bias_and_ramp.py',
                  'work/phase5/quantum_operation/floquet_record_300_noecho.json',
                  'work/root/cascade_echo.py','work/root/quantum_probe_controls.py',
                  'work/sources/astra/AGENTS.md']
    source_hash={f:sha(SOURCE/f) for f in source_files}
    for name,h in b['source_hashes'].items():
        assert source_hash['work/phase5/quantum_operation/'+name]==h
    checks.append({'inherited_source_hashes_match_execution_receipt':True})
    independent_files=['../luna03_quantum_record/RESULT.txt',
                       '../luna03_quantum_record/NUMERICAL_RESULTS.json',
                       '../luna03_quantum_record/terminal_change_point_bound.py',
                       '../luna03_quantum_record/pair_mechanism_audit/RESULT.txt',
                       '../luna03_quantum_record/pair_mechanism_audit/SPLIT_FREQUENCY_CONTROL_RESULTS.json',
                       '../luna03_quantum_record/pair_mechanism_audit/split_frequency_control.py',
                       '../luna03_quantum_record/pair_mechanism_audit/SOURCES_AND_HASHES.txt']
    manifest={'date':'2026-10-13','source_root':str(SOURCE),
              'verified_astra_checkout_head':'d47777a817e273668b6af3f0548cd02af92c6bc5',
              'source_sha256':source_hash,
              'independent_evidence_sha256':{f:sha(ROOT/f) for f in independent_files},
              'current_artifact_sha256':{p.name:sha(p) for p in sorted(ROOT.iterdir()) if p.is_file() and p.name not in ['SOURCE_MANIFEST.json','CHECKS.json','VERIFY_RUN.log']},
              'primary_sources_retrieved_live':['https://arxiv.org/html/2604.08672v1',
                   'https://arxiv.org/html/2607.27123v1','https://arxiv.org/html/2601.11086v1',
                   'https://arxiv.org/abs/1206.1296','https://arxiv.org/abs/2208.05879'],
              'receipt_scope':'Current artifact hashes and inherited execution source hashes. Historical pair replay compatibility is described in REPLAY.txt; no source file was edited.',
              'verifier_python':platform.python_version()}
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    assert (ROOT/'SOURCE_MANIFEST.json').is_file()
    receipt={'status':'SAVED_RECEIPTS_CONSISTENT_NOT_PHYSICS_VALIDATION','checks':checks}
    (ROOT/'CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
