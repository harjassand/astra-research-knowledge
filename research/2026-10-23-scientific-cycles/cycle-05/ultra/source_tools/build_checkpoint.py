#!/usr/bin/env python3
"""Producer assembly record. Portable scientific entry point is REPLAY.py."""
from pathlib import Path
import hashlib,json,shutil,time,zipfile

ROOT=Path(__file__).resolve().parents[2];W=ROOT/'work/Cycle5';OUT=ROOT/'outputs'
NAME='Astra_Amplification_Cycle5_ULTRA_20261022';stage=OUT/NAME
main=Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0003/main_response')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(p):return {'filename':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def cp(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)

t=time.perf_counter();assert not stage.exists() and not (OUT/(NAME+'.zip')).exists(),'refuse overwrite'
stage.mkdir(parents=True)
for name in ['CHECKPOINT.txt','PROOF.txt','OUTPUT_INTERFACE.txt','COMPARATOR.txt','FAILURES_AND_DECISION.txt','ROOT_REVIEW.txt','CORRECTIONS.txt']:
    cp(W/name,stage/name)
for name in ['replay.py','INPUTS.json','RESULT.json']:cp(W/name,stage/'calculations/universal'/name)
for folder,dest in [('label_audit','label'),('known_boundary','known_boundary'),('sparse_support','sparse_support')]:
    for p in sorted((W/folder).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':cp(p,stage/'audits'/dest/p.relative_to(W/folder))
for p in sorted((W/'contract').rglob('*')):
    if p.is_file():cp(p,stage/'contract'/p.relative_to(W/'contract'))
cp(main/'Astra_Cycle5_01_Sol_Ultra_20261022.txt',stage/'contract/01_ULTRA_CURRENT_INSTRUCTION.txt')
cp(main/'Astra_Cycle5_Private_Source_Receipt_20261022.json',stage/'contract/COMMON_PRIVATE_SOURCE_RECEIPT.json')
cp(W/'INPUT_RECOVERY_RECEIPT.json',stage/'contract/INPUT_RECOVERY_RECEIPT.json')
cp(W/'REPLAY_TEMPLATE.py',stage/'REPLAY.py');cp(Path(__file__).resolve(),stage/'source_tools/build_checkpoint.py')
prior=OUT/'Astra_Amplification_Cycle4_ULTRA_20261022.zip'
assert prior.stat().st_size==9965729 and sha(prior)=='39f46bc6baf0757f556faf1581f73a24e5dbfb8ee7fc2fa395820a033f0147f9'
cp(prior,stage/'sources'/prior.name)
write(stage/'INPUT_IDENTITIES.json',{
 'actual_unchanged_owner_source':ident(prior),
 'original_collection':{'filename':'Astra_Continuous_Cycle_0002_Six_Complete_Returns_20261022.zip','bytes':52206289,
 'sha256':'e98bf6a762ff302b2a4b38668a22f0f83e6a3748b83c3b3b26228a33373aeb76',
 'library_file_id':'libfile_624889c27cdc8191b844ccdc0e6b7ffb','backing_file_id':'file_0000000040f8820b9134213ae34e509f',
 'verification':'current locally attached bytes and CRC checked; actual owner member independently byte-matched'},
 'current_evaluator_packet':ident(main/'Astra_Scientific_Amplification_Cycle5_20261022.zip'),
 'information_experiment':{**ident(main/'Astra_Cycle5_Information_Experiment_20261022.zip'),'use':'settled provenance only; not executed or used to claim process superiority'},
 'current_instruction':ident(main/'Astra_Cycle5_01_Sol_Ultra_20261022.txt'),
 'Pro3_acceptance':'native owner source acceptance read and source-bound under contract; no mathematical transfer claimed',
 'original_R1':{'filename':'Astra_B2_R1_OWNER_SOURCE_20261021.zip','bytes':3663087,'sha256':'8b813c9f267e3079225219fb2e857cd3e4c18451f82471e3c5ee72be73136676','preservation':'unchanged recursively inside embedded Cycle4 source'},
 'newer_owner_local_progress':'none superseding source at intake; Cycle5 continuation separate',
 'strategy_owner':'evaluator','integration_owner':'Max','scientific_owner':'ULTRA principal'})
u=json.loads((W/'RESULT.json').read_text());g=json.loads((W/'sparse_support/RESULT.json').read_text())
write(stage/'COSTS.json',{
 'principal_fixed_admission':{k:u[k] for k in ['cpu_seconds','wall_seconds','peak_RSS_bytes','scope']},
 'graph_fixed_admission':{k:g[k] for k in ['process_cpu_seconds','wall_seconds','peak_rss_bytes','scope']},
 'sum_stored_body_CPU_seconds':u['cpu_seconds']+g['process_cpu_seconds'],
 'timing_scope':'successful stored bounded admission bodies only; module imports/source recovery/failed receipt emission/reasoning not fully charged; relocated replay separately receipted',
 'principal_cases':8,'graph_cases':10,'graph_stock_cases':19,
 'optimization_or_search_jobs':0,'historical_scientific_replay_jobs':0,'evaluator_comparisons_rerun':0,
 'failed_graph_receipt_emission':'preserved, runtime UNKNOWN',
 'full_discovery_coordination_learning_calibration_cost':'UNKNOWN',
 'primary_reference_queries':'not fully counted; known-method source checks retained',
 'hardware_spending_paid_credits_or_public_hosting':False,
 'statistical_copy_cost':'n_O+n_R fresh full rN-output preparations plus training; OUTPUT_INTERFACE.txt',
 'known_effect_accuracy':'not experimentally acquired; operator-norm error terms explicit',
 'generic_dense_POVM_or_reference_circuit_efficiency':'NOT_ESTABLISHED; may be exponential',
 'optimized_quantum_penalty_cost':'known E_F convex roof; not assumed efficiently computable',
 'historical_novelty':'UNKNOWN','physical_usefulness':'NOT_ESTABLISHED'})
write(stage/'CLAIMS.json',{
 'mission':'ACTIVE_AT_CHECKPOINT','strategy_owner':'evaluator','integration_owner':'Max',
 'claims':[
 {'id':'C5-Q','internal_status':'PROVED_AND_INDEPENDENTLY_AUDITED','claim':'universal finite-output EF hierarchy witness with complementary quantum-readout entropy penalty; arbitrary mixed states, no support/gap/normality premise','source':'PROOF.txt sections1-2'},
 {'id':'C5-P','internal_status':'PROVED_AND_INDEPENDENTLY_AUDITED','claim':'arbitrary different POVM weighted-rank/conditional-label relaxation and universal fixed-prediction linear witnesses','source':'PROOF.txt sections3-4; OUTPUT_INTERFACE.txt'},
 {'id':'C5-F','internal_status':'CONDITIONAL_PROVED','claim':'matched finite supplied-entanglement/return/global-initialization/prediction-cost law and enlarged bounded-uncertainty O1-gap iid class','source':'PROOF.txt section6'},
 {'id':'C5-G','internal_status':'PROVED_AND_INDEPENDENTLY_AUDITED','claim':'degree-two graph support versus exponentially growing exact commutant closure ranks; actual stock receives bounded prefix-score loss','source':'audits/sparse_support/PROOF.txt'},
 {'id':'C5-L','internal_status':'PROVED_CLASSICAL_OBSERVATION_LIMIT','claim':'small mismatch alone cannot bound growing-alphabet conditional Shannon entropy; actual product-state sharpness and finite-sample obstruction','source':'audits/known_boundary/KNOWN_BOUNDARY.txt'},
 {'id':'C5-KW','internal_status':'KNOWN_IDENTITY_CORRECTLY_RECEIVED','claim':'optimized penalty is Koashi-Winter EF convex roof; logarithmic savings require growing every-readout average uncertainty','source':'audits/known_boundary/KOASHI_WINTER_BOUNDARY.txt'}],
 'unresolved':['unrestricted critical hierarchy','generic logarithmic formation gap','whether actual causal exact-output/return structure bounds optimized uncertainty','admitted reservoir with growing irreducible uncertainty and genuine saving','generic efficient measurement/optimization','hidden-memory return accessibility'],
 'historical_novelty':'UNKNOWN','external_acceptance':'UNKNOWN','physical_advantage':'NOT_ESTABLISHED',
 'Pro3_native_incoming_proof_acceptance':'ACCEPTED and used by its owner; provenance verified; no Ultra transfer gain',
 'causal_research_amplification':'NOT_CLAIMED',
 'protected_closed_scopes_preserved':True})
files=[{'path':p.relative_to(stage).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(stage.rglob('*')) if p.is_file()]
write(stage/'MANIFEST.json',{'format':'Astra source-complete immutable checkpoint v1','self_excluded':True,'files':files})
archive=OUT/(NAME+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(stage.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(stage).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None;members=len(z.namelist())
receipt={**ident(archive),'status':'PASS','archive':str(archive),'staging':str(stage),'zip_members':members,
 'manifest_payloads':len(files),'CRC':'PASS','build_wall_seconds':time.perf_counter()-t,
 'unchanged_owner_source':ident(prior),'delivery_state':'NOT_YET_DELIVERED','recipient_reading_verification_scientific_acceptance':'UNKNOWN'}
write(OUT/'CYCLE5_ULTRA_BUILD_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
