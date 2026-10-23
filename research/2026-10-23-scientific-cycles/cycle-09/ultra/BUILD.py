#!/usr/bin/env python3
"""Producer-layout assembly of complete actual source and immutable predecessor."""
from pathlib import Path
import hashlib,json,shutil,zipfile

BASE=Path(__file__).resolve().parents[2];W=BASE/'work/Cycle9'
NAME='Astra_Amplification_Cycle9_ULTRA_20261022';OUT=BASE/'outputs'/NAME
PH='a91d763e1526ffb934e5cfeb996c9bcb04bbdc624e2e4a93d175a51dfcad8bf2'
PREV='ab46aeb4e46806a47edc8e2d791646a5f2015f65e6379aa5d06d55eb1187ea9d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(src,dst):
 p=OUT/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)
def write(name,data):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(data,indent=2)+'\n' if isinstance(data,(dict,list)) else data)

assert sha(W/'root/PROOF.txt')==PH
prev=BASE/'outputs/Astra_Amplification_Cycle8_ULTRA_20261022.zip';assert sha(prev)==PREV
if OUT.exists() or OUT.with_suffix('.zip').exists():raise SystemExit('Refuse to replace frozen release')
OUT.mkdir(parents=True)
for name in ['PROOF.txt','OUTPUT_INTERFACE.txt','COMPARATOR.txt','CAPITAL_AND_CHANGE.txt',
             'FAILURES_AND_DECISION.txt','DATED_STATUS_UPDATES.txt','REFERENCES.txt']:
 copy(W/'root'/name,name)
for name in ['replay.py','RESULT.json','TIMING.json']:
 copy(W/'root'/name,'calculations/principal/'+name)
for name in ['UNRELEASED_DRAFT_BEFORE_SCOPE_CLARIFICATIONS.txt','SCOPE_CORRECTION_RECEIPT.json']:
 copy(W/'root'/name,'provenance/'+name)
for role in ['loss_converse','collective','receiver_challenge','projection_audit']:
 prefix='audits/projection' if role=='projection_audit' else 'studies/'+role
 for p in (W/role).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:
   copy(p,prefix+'/'+str(p.relative_to(W/role)))
copy(prev,'sources/'+prev.name)
for name in ['START_HERE.txt','SOURCE_BINDINGS.json','SOURCE_INTAKE.json','OWNER_AND_R1_PRESERVATION.json']:
 copy(W/'intake'/name,'contract/'+name)
copy(W/'intake/evidence/CYCLE8_CURRENT_PROOF_CORRECTION.txt',
     'contract/CYCLE8_CURRENT_PROOF_CORRECTION.txt')
common_dir=Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0007/main_response')
for name in ['Astra_Cycle9_ULTRA_Continuation_20261022.txt','Astra_Cycle9_Private_Source_Receipt_20261022.json']:
 copy(common_dir/name,'contract/'+name)
copy(W/'REPLAY.py','REPLAY.py');copy(Path(__file__),'BUILD.py')

audits=['studies/loss_converse/FINAL_ROOT_AUDIT.txt',
        'studies/collective/FINAL_ROOT_AUDIT.txt',
        'studies/receiver_challenge/FINAL_ROOT_AUDIT.txt',
        'audits/projection/FINAL_ROOT_AUDIT.txt']
for a in audits:assert PH in (OUT/a).read_text(),a
write('README.txt','''ASTRA CYCLE9 ULTRA — UNIVERSAL LOSS / ERROR / RESOURCE BOUNDARY

Main result, complete proof: PROOF.txt. Governing source/interface and strongest
ordinary comparison: OUTPUT_INTERFACE.txt and COMPARATOR.txt. Actual capital
receiving step: CAPITAL_AND_CHANGE.txt. Failures and one next decision:
FAILURES_AND_DECISION.txt. Read DATED_STATUS_UPDATES.txt before interpreting
earlier bounded-source open-status language. Only the top-level current proof
is the integrated governing theorem.

For the ACTUAL product-nu-tail queue, zero added entanglement/access and one
GLOBAL error epsilon<=1/8, the optimal pointwise per-queue Bell loss satisfies
 w_*+1=Theta_D(min{L,1+lnL+ln(r/epsilon)}).
The lower permits arbitrary collective SEP for logL and even arbitrary global
channels for log(r/epsilon); the actual preserved Cycle8 receiver supplies
the upper. At fixed L, any fixed w<L-1 forces global error to1 as r grows.
A single-queue full loss-CDF/mean theorem and explicit access/aid/expected-lnM
resource laws are included. No hidden clock readout, favorable source or
postselection is supplied. All old memory, retained records and bad branches
remain in the joint error.

An explicit PAID Bell-ancilla difference receiver keeps the original source
loss independent of L at fixed epsilon, with logarithmic added Bell supply
and a fully priced seed/control. It is a comparator, not a zero-aid exception.
Known nonlocal parity/search/score machinery is credited in REFERENCES.txt.

Portable replay, standard library Python3.10+:
  python3 REPLAY.py --output /absolute/path/cycle9_replay.json
It verifies all payload identities and the four actual-source audit bindings,
then runs ONLY six NEW bounded admissions in a disposable relocated copy.
It does NOT execute any predecessor scientific suite, hardware, paid compute,
or retired programme. Exact rational/count/decimal outputs compare exactly;
finite floating admissions use1e-11 tolerance and timings are excluded.

sources/Astra_Amplification_Cycle8_ULTRA_20261022.zip is the FULL unchanged native
predecessor, preserving its complete chain and actual R1 proof/reservoir/replay.
Extracted predecessor bytes are exact despite outer lossless ZIP compression.
contract/ records actual common-source verification and owner/R1 preservation.
No missing original research ZIP or user file administration is needed.

Internal proofs/source-bound audits and bounded checks establish their stated
scope. Historical novelty, external correctness certification, physical
usefulness and recipient reading/acceptance/integration remain UNKNOWN.
No ordinary consumable-entanglement formation advantage or recursive
intelligence amplification is claimed. Original source supply remains charged.

Decision: retire unchanged fixed-L uniform-r pointwise profile search. Next
question is a declared pooled/encoded output interface with an actual joint-
memory decoupling/rate theorem and equally informed ordinary comparator.
That remaining question is OPEN. All protected and parked programmes stay shut.

BUILD.py is the actual producer-layout assembly record, not a portable host
installer. REPLAY.py is the supported portable receiving command. External
receipts bind the frozen ZIP size/hash/private file and binary roundtrip;
they are outside this archive to avoid self-reference. Hashes establish byte
identity, not proof acceptance. No background monitor is promised.
''')

root_result=json.loads((W/'root/RESULT.json').read_text())
write('CLAIMS.json',{
 'internal_proof':'COMPLETE_AT_STATED_PROFILE_SOURCE_RESOURCE_CONTRACT',
 'governing_proof_sha256':PH,'actual_queue':'UNMODIFIED_PHI_PREFIX_PRODUCT_NU_TAIL',
 'one_global_halftrace_error':True,'complete_memory_and_transcript_correlations':True,
 'zero_aid_pointwise_loss_order':'Theta_D(min{L,1+lnL+ln(r/epsilon)}) for w_*+1, epsilon<=1/8',
 'finite_r_CP_law':'epsilon>=r c/(1+r c)*(1-D^{-(d-w)})*(1-d/L), c=D^-2d',
 'collective_SEP_volume_law':'PROOF(13)',
 'fixed_L_nontrivial_uniform_r_profile':'IMPOSSIBLE; global error tends to1',
 'single_queue_CDF_mean_loss':'PROOF(9),(12)',
 'access_and_separable_domination_factor':'PROOF(17)',
 'expected_preselected_log_rank':'PROOF(18); no E M finiteness assumed',
 'paid_receiver':'EXPLICIT; full additional Bell/seed/control costs charged',
 'ordinary_stock_advantage':'NOT_ESTABLISHED','historical_novelty':'UNKNOWN',
 'external_correctness_certification':'UNKNOWN','physical_usefulness':'UNKNOWN',
 'recursive_amplification':'NOT_ESTABLISHED','pooled_encoded_joint_rate_question':'OPEN',
 'actual_principal_audits':audits})
write('COSTS.json',{
 'mathematical_resource_contract':'PROOF sections1,5,7; OUTPUT_INTERFACE.txt',
 'large_parameter_formula_table':root_result['matched_formula_table'],
 'observed_new_admissions':{
  'root_initial':{'wall_seconds':0.030222458066418767,'cpu_seconds':0.029705},
  'root_after_new_threshold_obligation':json.loads((W/'root/TIMING.json').read_text()),
  'loss_CDF':{k:v for k,v in json.loads((W/'loss_converse/EXACT_REPLAY_RESULTS.json').read_text()).items() if k in ['wall_seconds','cpu_seconds','status']},
  'collective_posterior_wall_seconds':json.loads((W/'collective/REPLAY_RESULT.json').read_text())['runtime_seconds'],
  'nested_parity_challenge_wall_seconds':json.loads((W/'receiver_challenge/RESULT.json').read_text())['wall_seconds'],
  'new_aided_primitive_wall_seconds':json.loads((W/'receiver_challenge/AIDED_PRIMITIVE_RESULT.json').read_text())['wall_seconds']},
 'scope':'Observed subset, not total discovery cost. Final relocated replay measured in external receipt.',
 'prior_scientific_suites_rerun':0,'hardware_calls':0,'paid_compute':0,
 'spending_outreach_public_disclosure':0,'total_discovery_inference_cost':'UNKNOWN',
 'source_preparation_time_energy_thermodynamic_reset_cost':'UNKNOWN'})
write('ROOT_REVIEW.json',{
 'status':'PASS_AT_INTERNAL_SCOPED_CHECKPOINT','principal_proof_sha256':PH,
 'actual_principal_audits':[{ 'path':a,'bytes':(OUT/a).stat().st_size,'sha256':sha(OUT/a)} for a in audits],
 'source_clock_fibre_clarification':'Applied before final hash binding; fixed labels restored in full error.',
 'root_constructions':['orthogonal-neighbor finite-r CPTP law','collective SEP weighted-volume law','expected-log-rank convex-secant resource law','paid difference-query receiving comparison'],
 'bounded_distinct_help':['sharp single-queue loss-CDF and access extension','posterior strong converse and mean-only boundary','quantum primitive/freshness/erasure challenge','independent analytic audits'],
 'finite_admissions':'Necessary sublemma/normalization checks only; all-parameter proofs are analytic.',
 'external_acceptance_novelty_physical_usefulness':'UNKNOWN'})
write('CHECKPOINT.txt','''SUBSTANTIVE CYCLE9 CHECKPOINT

The selected universal pointwise loss/error boundary has a complete matched-
order theorem, with explicit resource extensions and a fixed-L strong converse.
It no longer remains merely an upper-construction conjecture. The actual
operation/source, full proofs, new-only replay, failures and source-bound
independent audits are provided.

The broader scientific mission continues at the OPEN pooled/encoded output
interface and joint-memory rate/decoupling question. No result on that changed
interface, formation advantage, historical novelty or physical usefulness is
claimed. Protected/retired science is not resumed. Delivery is not evidence
of another owner's reading, scientific acceptance or integration.
''')
assert sha(OUT/'PROOF.txt')==PH
payload=[{'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)}
         for p in sorted(OUT.rglob('*')) if p.is_file()]
write('MANIFEST.json',{'archive_filename':NAME+'.zip','principal_proof_sha256':PH,
                       'actual_principal_audits':audits,'payloads':payload,
                       'self_authenticating':False})
archive=OUT.with_suffix('.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(str(p.relative_to(OUT)),(2026,10,22,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes(),compresslevel=9)
with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('sources/'+prev.name)).hexdigest()==PREV
receipt={'status':'BUILT','archive':str(archive),'bytes':archive.stat().st_size,
         'sha256':sha(archive),'payloads':len(payload),'principal_proof_sha256':PH,
         'exact_predecessor_preserved':True,
         'over_native_Page_10MiB_upload_limit':archive.stat().st_size>10*1024*1024,
         'outer_compression':'lossless DEFLATE; extracted predecessor bytes unchanged'}
(BASE/'outputs/CYCLE9_ULTRA_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
