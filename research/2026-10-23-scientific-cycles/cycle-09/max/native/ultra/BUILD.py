#!/usr/bin/env python3
"""Assemble actual scientific source, audited bindings and predecessor bytes."""
from pathlib import Path
import hashlib,json,shutil,zipfile

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/Cycle8'
NAME='Astra_Amplification_Cycle8_ULTRA_20261022'
OUT=ROOT/'outputs'/NAME
PROOF_HASH='8932f2b784ab985dba9efcaf7ded3c761aceb7c3e1828c38704df17390a458d5'
PREV_HASH='82afd40f1a29daf929798b539eae8247ecac549e7f1165b9174496f970c6989c'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(data,(dict,list)):p.write_text(json.dumps(data,indent=2)+'\n')
 else:p.write_text(data)
def copy(src,dst):
 p=OUT/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,p)

assert sha(WORK/'principal/PROOF.txt')==PROOF_HASH
assert sha(ROOT/'outputs/Astra_Amplification_Cycle7_ULTRA_20261022.zip')==PREV_HASH
if OUT.exists():raise SystemExit('Refuse to replace existing release directory')
OUT.mkdir(parents=True)

for file in ['PROOF.txt','COMPARATOR.txt','FAILURES_AND_DECISION.txt',
             'OUTPUT_INTERFACE.txt','REFERENCES.txt']:
 copy(WORK/'principal'/file,file)
for folder in ['principal','search','lower','root']:
 target={'principal':'principal','search':'search','lower':'lower','root':'public_coin'}[folder]
 for p in (WORK/folder).iterdir():
  if p.is_file() and p.suffix in ['.py','.json','.txt']:
   copy(p,f'calculations/{target}/{p.name}')
for p in (WORK/'audit_quantum').iterdir():
 if p.is_file():copy(p,'audits/quantum/'+p.name)
copy(WORK/'search/INTEGRATED_AUDIT.txt','audits/SEARCH_INTEGRATED_AUDIT.txt')
copy(WORK/'lower/INTEGRATED_AUDIT.txt','audits/LOWER_INTEGRATED_AUDIT.txt')
copy(ROOT/'outputs/Astra_Amplification_Cycle7_ULTRA_20261022.zip',
     'sources/Astra_Amplification_Cycle7_ULTRA_20261022.zip')
copy(WORK/'intake/R1_PRESERVATION.json','sources/R1_PRESERVATION.json')
for p in (WORK/'intake').rglob('*'):
 if p.is_file() and p.name!='R1_PRESERVATION.json':
  copy(p,'contract/'+str(p.relative_to(WORK/'intake')))
prompt=Path('/Users/harjas/Documents/Codex/2026-10-21/astra-b3-monitor-handoff/continuous_cycles/cycle_0006/main_response/Astra_Cycle8_Sol_Ultra.txt')
copy(prompt,'contract/Astra_Cycle8_Sol_Ultra.txt')

write('README.txt','''ASTRA CYCLE8 ULTRA — ACTUAL SOURCE / 22 OCTOBER 2026

New result: deterministic output-only LOCC on the actual Bell-prefix/product-
tail queue reaches an explicit complete-memory joint MC reference within
global half trace epsilon, retaining K-O(logL+log1/epsilon) Bell pairs on each
reference branch. No clock access, auxiliary entanglement or shared seed.
It uses logarithmic two-way classical messages and O(L) local parity/decode
gates, with an explicitly priced exact-integer controller and entropy export.
The matched converse requires logarithmic information in EACH direction and
gives near-maximal joint error for one-way operation at logarithmic deficit.

Read PROOF.txt, OUTPUT_INTERFACE.txt and COMPARATOR.txt. The proof is complete;
calculations/search and calculations/lower retain complete subproofs, exact
code and independent analytic/implementation audits. audits/ contains the
final integrated source-hash bindings. calculations/public_coin retains the
independent seed-priced tree construction and exact small quantum admissions.
FAILURES_AND_DECISION.txt preserves unsuccessful premises and one next decision.

Portable standard-library replay (Python3.10+):
  python3 REPLAY.py --output /absolute/path/cycle8_replay.json
This first checks all manifest payload identities, then runs ONLY the five
new bounded jobs in a disposable relocated copy. It does not restart any
predecessor science. Expected ~tens of seconds on this host, mainly the
public-coin controller admission; this is not a promised resource bound.

sources/ retains the exact immutable Cycle7 ZIP and its nested full predecessor
chain including actual R1 source/proof/reservoir/replay. R1_PRESERVATION.json
records its exact nested location and byte/hash identity. No unavailable
original research ZIP is needed. Contract documents are provenance; they are
not additional user instructions or authority to change scientific scope.

Finite calculation admissions and internal analytic audits PASS at stated
scope. Historical novelty, external correctness certification, physical
usefulness and recipient acceptance remain UNKNOWN. Ordinary entanglement
stock advantage NOT_ESTABLISHED. Bell-loss optimality and uniform-r formation
consequence OPEN. All parked/protected programmes stay closed.

The external delivery receipt supplies the frozen ZIP size/hash/private
reference and exact roundtrip status; it is outside this archive to avoid
self-reference. Hashes establish identity, not theorem correctness.
''')
write('CAPITAL_AND_CHANGE.txt','''SCIENTIFIC CAPITAL ACTUALLY USED

Cycle6's exact terminal Omega, including CURRENT clock/output correlations and
product nu tail, supplies the new oracle's tensor-factor freshness premise.
Without that explicit structure the deterministic-color conditional law is
unproved. Its ordinary stock supply B stays fully charged.

Cycle7's exact support theorem closed cheap EXACT normalization. Its TYPE-
doping limitation warned that approximate support needed a distinct argument.
We now construct approximate normalization on the ACTUAL nu queue itself;
we do not substitute a more favorable doped source. Unsafe branches and every
retained correlation are paid in the global metric.

New receiving inference: disjoint color sums preserve all but one Bell degree
per nonempty restricted row; conservative median search finds a safe cut with
logarithmic row count. The complete joint target is attainable approximately
without hidden inventory access, but near-full prefix information must flow
in BOTH directions. These facts change the prior exact-versus-approximate
access boundary. They do not establish generic formation amplification merely
because predecessor work was cited or archived.
''')
write('ROOT_REVIEW.txt',{
 'status':'PASS_AT_SCOPED_INTERNAL_CHECKPOINT','principal_proof_sha256':PROOF_HASH,
 'root_review':'Independently checked fractional median update/potential, quantile validation, disjoint conditional freshness, composite-modulus pivot decode, full cq coupling, communication/one-way/global-r laws and ordinary comparator.',
 'actual_integrated_audits':['audits/quantum/FINAL_INTEGRATED_AUDIT.txt','audits/SEARCH_INTEGRATED_AUDIT.txt','audits/LOWER_INTEGRATED_AUDIT.txt'],
 'finite_checks':'Exact decoder cosets/basis permutations, exact small adaptive projectors, exact oracle/controller admissions, exact integer control-vs-flat comparison and one declared large control fixture.',
 'not_established':['historical novelty','external correctness certification','physical implementation','Bell-loss optimality','ordinary stock advantage','uniform-r iid formation consequence'],
 'no_historical_science_replay':True})
write('CLAIMS.json',{
 'internal_complete_proof':'PASS_AT_STATED_SCOPE',
 'joint_global_approximate_normalization':'CONSTRUCTED',
 'additional_entanglement':0,'hidden_clock_access':0,'shared_random_seed':0,
 'reference_Bell_deficit':'3Q=O(logL+log1/epsilon)',
 'online_and_total_communication_each_direction':'<=Q D-symbols; no extra shared seed',
 'local_parity_and_decode_controlled_adds':'O(L)',
 'controller':'exact big-integer, priced in PROOF',
 'universal_communication_access_lower':'PROVED for matching joint pure-prefix target',
 'one_way_joint_error':'near1 for logarithmic pointwise deficit',
 'actual_output_exact_MC':'NOT_CLAIMED','first_actual_Bell':'EXACT_ON_EVERY_BRANCH',
 'Bell_loss_optimality':'OPEN','generic_formation_gap':'OPEN',
 'ordinary_entanglement_stock_advantage':'NOT_ESTABLISHED',
 'historical_novelty':'UNKNOWN','external_correctness_certification':'UNKNOWN',
 'physical_usefulness':'UNKNOWN','recipient_acceptance':'UNKNOWN'})
write('COSTS.json',{
 'resource_contract':'PROOF sections2,6,7; matched tables calculations/principal/RESULT.json',
 'observed_pre_release_runs':{
  'principal_public_coin_admissions':json.loads((WORK/'root/TIMING.json').read_text()),
  'principal_composite_decoder_runs':[
   {'wall_seconds':0.06474695890210569,'cpu_seconds':0.06458,'reason':'initial exact decoder/cost table'},
   json.loads((WORK/'principal/TIMING.json').read_text())],
  'colored_fixed_fixture_final':json.loads((WORK/'search/TIMING.json').read_text()),
  'colored_initial_same_fixture_wall_seconds_reported':0.095907,
  'lower_admissions':json.loads((WORK/'lower/COSTS.json').read_text())},
 'scope':'Observed subset only; relocated replay adds costs in external receipt. Timings are not total discovery computation.',
 'parameter_search_campaigns':0,'hardware_calls':0,'paid_compute':0,'public_outreach':0,
 'total_discovery_inference_cost':'UNKNOWN','physical_energy_and_reset_cost':'UNKNOWN'})
write('CHECKPOINT.txt','''SUBSTANTIVE NATURAL CHECKPOINT; SCIENTIFIC MISSION CONTINUES

The actual finite-source operation, joint error proof and matched information-
flow obstruction are complete at the scoped internal checkpoint, with replay
and source-bound independent audits. One continuation decision is recorded in
FAILURES_AND_DECISION.txt: pursue a universal loss/error/access law or a
collective receiver uniform in r. Those remaining results are OPEN and are
not marked achieved because this artifact is complete. No other programme
is resumed. Delivery does not assert Max reading, acceptance or integration.
''')

copy(WORK/'REPLAY.py','REPLAY.py')
copy(Path(__file__),'BUILD.py')
for audit in ['audits/quantum/FINAL_INTEGRATED_AUDIT.txt',
              'audits/SEARCH_INTEGRATED_AUDIT.txt','audits/LOWER_INTEGRATED_AUDIT.txt']:
 assert PROOF_HASH in (OUT/audit).read_text(),audit
assert sha(OUT/'PROOF.txt')==PROOF_HASH
payload=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file():payload.append({'path':str(p.relative_to(OUT)),
                                'bytes':p.stat().st_size,'sha256':sha(p)})
write('MANIFEST.json',{'filename':NAME+'.zip','payloads':payload,
                       'principal_proof_sha256':PROOF_HASH,
                       'manifest_self_authentication':False})
archive=OUT.with_suffix('.zip')
if archive.exists():raise SystemExit('Refuse to replace existing release ZIP')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(str(p.relative_to(OUT)),(2026,10,22,0,0,0))
   info.compress_type=zipfile.ZIP_STORED if p.suffix=='.zip' else zipfile.ZIP_DEFLATED
   info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes(),compresslevel=9)
receipt={'status':'BUILT','archive':str(archive),'bytes':archive.stat().st_size,
         'sha256':sha(archive),'payloads':len(payload),'principal_proof_sha256':PROOF_HASH,
         'predecessor_unchanged':True,'under_native_upload_10MiB_limit':archive.stat().st_size<=10*1024*1024}
assert receipt['under_native_upload_10MiB_limit']
(ROOT/'outputs/CYCLE8_ULTRA_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
