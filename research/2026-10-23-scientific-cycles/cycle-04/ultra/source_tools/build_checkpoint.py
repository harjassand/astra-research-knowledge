#!/usr/bin/env python3
"""Build the Cycle4 immutable source checkpoint; private delivery is separate."""
from pathlib import Path
import hashlib,json,shutil,time,zipfile

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/Cycle4'
OUT=ROOT/'outputs'
NAME='Astra_Amplification_Cycle4_ULTRA_20261022'
stage=OUT/NAME
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def identity(path):return {'filename':path.name,'bytes':path.stat().st_size,'sha256':sha(path)}
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def copy(source,dest):dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)

started=time.perf_counter()
assert not stage.exists() and not (OUT/(NAME+'.zip')).exists(),'refuse overwrite'
stage.mkdir(parents=True)
for name in ['PROOF.txt','OUTPUT_INTERFACE.txt','COMPARATOR.txt','CHECKPOINT.txt',
             'FAILURES_AND_DECISION.txt','ROOT_REVIEW.txt']:
    copy(WORK/'principal'/name,stage/name)
for name in ['replay.py','RESULT.json']:
    copy(WORK/'principal'/name,stage/'replay/principal'/name)
for folder in ['witness_audit','nonmax_cut','physical_structure','capital_interface']:
    for source in sorted((WORK/folder).rglob('*')):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix!='.pyc':
            copy(source,stage/'audits'/folder/source.relative_to(WORK/folder))
copy(WORK/'REPLAY_TEMPLATE.py',stage/'REPLAY.py')
copy(Path(__file__).resolve(),stage/'source_tools/build_checkpoint.py')
copy(Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0002/main_response/Astra_Cycle4_01_Sol_Ultra_20261022.txt'),
     stage/'contract/01_ULTRA_CURRENT_INSTRUCTION.txt')
copy(WORK/'INPUT_RECOVERY_RECEIPT.json',stage/'contract/INPUT_RECOVERY_RECEIPT.json')

prior=WORK/'collection/returns/ultra/Astra_Amplification_Cycle3_ULTRA_20261022.zip'
incoming=Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0002/main_response/Astra_Cycle4_Operator_Capital_20261022.zip')
r1=OUT/'Astra_B2_R1_OWNER_SOURCE_20261021.zip'
assert identity(prior)['sha256']=='0f6207f9d1393640d1863507d69e61526ae2f063c218309f3e3a9b5f41a2a0c4'
assert identity(incoming)['sha256']=='708fff2ae6883f34423815cda3993fd35d5a4df2f4a786de9aeea2a92eae0af7'
assert identity(r1)['sha256']=='8b813c9f267e3079225219fb2e857cd3e4c18451f82471e3c5ee72be73136676'
for p in [prior,incoming]:copy(p,stage/'sources'/p.name)
write(stage/'INPUT_IDENTITIES.json',{
 'predecessor':identity(prior),'incoming_capital':identity(incoming),
 'collection':{'filename':'Astra_Continuous_Cycle_0001_Six_Complete_Returns_20261022.zip','bytes':48905277,
 'sha256':'d2d1ce472cc0ec0dfe1f5d2da22bffad5b7c45ef13099576b5aa0f8248263d3f',
 'library_file_id':'libfile_f066e2d63800819197015c6ee998bdc3','backing_file_id':'file_00000000ec00820bbadfc380db71d3f8',
 'inclusion':'exact owned return embedded; unrelated owner returns not duplicated'},
 'incoming_private_identity':{'library_file_id':'libfile_ad1a73408d80819190f20d618d982fdc','backing_file_id':'file_00000000e86c820b80cebbedebfec3e3'},
 'original_R1':{**identity(r1),'preservation':'unchanged original archived recursively in predecessor source; direct accessible owner export rehashed at build'},
 'current_source_recovery':'actual locally attached exact files rehashed; no inference from historical paths',
 'recipient_reading_verification_acceptance':'UNKNOWN'})

results={key:json.loads((WORK/path).read_text()) for key,path in {
 'principal':'principal/RESULT.json','physical_structure':'physical_structure/RESULT.json',
 'nonmax_cut':'nonmax_cut/RESULT.json','support_gap':'witness_audit/GAP_REPLAY.json'}.items()}
write(stage/'COSTS.json',{
 'new_bounded_admission_cpu_seconds':{key:value['cpu_seconds'] for key,value in results.items()},
 'sum_recorded_admission_cpu_seconds':sum(value['cpu_seconds'] for value in results.values()),
 'principal_actual_matrix_peak_RSS_bytes':results['principal']['peak_RSS_bytes'],
 'scope':'saved admission runs only; fresh relocated replay separately receipted; timings not end-to-end discovery cost',
 'source_recovery_operations_cost':'not separately measured',
 'full_discovery_reasoning_coordination_cost':'UNKNOWN','external_reference_query_total':'UNKNOWN',
 'new_hardware_acquisition':False,'new_spending_authorized_or_performed':False,
 'historical_search_rerun':False,
 'statistical_cost_contract':'OUTPUT_INTERFACE.txt; every score or support trial consumes a fresh full rN-output preparation',
 'generic_block_measurement_circuit_cost':'UNKNOWN; may be exponential in q; known projectors/commutation do not imply efficient synthesis',
 'historical_novelty':'UNKNOWN','physical_performance':'NOT_ESTABLISHED',
 'incoming_capital_received_math_gain':'NOT_CLAIMED; exact receiving shortcut obstructed'})
write(stage/'CLAIMS.json',{
 'mission_status':'ACTIVE','integration_owner':'Max','scientific_owner':'ULTRA principal with attributed independent challenges',
 'internal_claims':[
  {'id':'C4-A','status':'INTERNALLY_PROVED_AND_AUDITED','claim':'entire nonnormal block-commutant critical witness with weighted complementary log-rank defect','source':'PROOF.txt sections1-4'},
  {'id':'C4-B','status':'INTERNALLY_PROVED_AND_AUDITED','claim':'robust finite-output leakage witness and exact destructive commuting LOCC effect with explicit sampling costs','source':'PROOF.txt section5; OUTPUT_INTERFACE.txt'},
  {'id':'C4-C','status':'CONDITIONAL_INTERNALLY_PROVED','claim':'bounded rank/vanishing leakage and global initialization error force constrained iid reuse rate m/(2delta)+O(1), stock matched','source':'PROOF.txt section6'},
  {'id':'C4-D','status':'INTERNALLY_PROVED_EXACT_REPLAY_PASS','claim':'fixed-rank noncommuting tests can almost accept a state orthogonal to the common support; gap conversion sharp','source':'audits/witness_audit/COMMUTANT_UPGRADE.txt'},
  {'id':'C4-E','status':'INTERNALLY_PROVED_AND_AUDITED','claim':'universal erasure-invariant qubit MASA classification through four physical sites','source':'audits/physical_structure/FOUR_QUBIT_PROOF.txt'},
  {'id':'C4-F','status':'SCOPED_RECEIVING_MAP_OBSTRUCTION','claim':'literal stationary-law/positive-diagonal transfer from incoming killed-norm capital fails','source':'audits/capital_interface/RECEIVING_MAP_OBSTRUCTION.txt'}],
 'unresolved':['unrestricted critical hierarchy','generic logarithmic formation gap','growing complementary ranks or non-block operators','>=5-site invariant qubit MASAs','generic efficient block measurement implementation','hidden-memory return accessibility'],
 'historical_novelty':'UNKNOWN','external_correctness_validation':'UNKNOWN','physical_advantage':'NOT_ESTABLISHED',
 'research_amplification_from_incoming_pro3':'NOT_CLAIMED','pro3_owner_acceptance':'PENDING as supplied',
 'protected_or_closed_scopes':['original R1 preserved','no additive-constant/noisy-output programme','thermal/TPV/desalination/molecular/GUIDE closed','hidden entropy/N33/N557/IQM protected','Morrey halted']})

files=[{'path':p.relative_to(stage).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(stage.rglob('*')) if p.is_file()]
write(stage/'MANIFEST.json',{'format':'Astra immutable source payload v1','self_excluded':True,'files':files})
archive=OUT/(NAME+'.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(stage.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(stage).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    count=len(z.namelist())
receipt={**identity(archive),'status':'PASS','archive':str(archive),'staging':str(stage),
         'zip_members':count,'manifest_payloads':len(files),'CRC':'PASS','build_wall_seconds':time.perf_counter()-started,
         'historical_source_archives_unchanged':True,'original_R1_direct_identity':identity(r1),
         'delivery_state':'NOT_YET_DELIVERED','recipient_reading_verification_acceptance':'UNKNOWN'}
write(OUT/'CYCLE4_ULTRA_BUILD_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
