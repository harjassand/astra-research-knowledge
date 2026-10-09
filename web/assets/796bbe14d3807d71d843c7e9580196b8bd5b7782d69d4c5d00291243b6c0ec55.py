"""Seal checkpoint09 after zero pending reports; archive integrity is not proof.

Prior frozen proofs and output packet manifests are checked against08. The
older utility module is read unchanged; only this module's runtime pointer to
the prior checkpoint is updated.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json,shutil,zipfile
R=Path(__file__).resolve().parents[2];S=R/'work/state';A=R/'work/agents';O=R/'outputs'
spec=importlib.util.spec_from_file_location('preserved_cycle06_utilities',S/'seal_cycle06.py')
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
u.PREVIOUS=R/'work/checkpoints/checkpoint08/ASTRA_ULTRA_RESEARCH_STATE.zip'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')

def prepare():
 auditp=A/'resource_audit/cycle09_final_inventory/POST_REPAIR_FINAL_INVENTORY.json'
 audit=json.loads(auditp.read_text())
 assert audit['all_integrity_checks_pass'] is True
 for key in ['pending_math_reports','pending_source_reports','prior_checkpoint08_agent_files_changed','prior_output_manifests_changed']:
  assert audit[key]==0,(key,audit[key])
 assert audit['unclassified_artifacts']==[],audit['unclassified_artifacts']
 assert audit['changed_during_read']['count']==0,audit['changed_during_read']
 assert audit['all_frozen_current_cycle_files_unchanged'] is True
 usage=json.loads((S/'cycle09_usage_snapshot.json').read_text())
 assert usage['concurrent_reservation']['active_thread_count']==1
 assert usage['discovery']['descendant_count']==25
 assert usage['dispatch_verification']['effective_context_model_counts_including_root']=={'gpt-6-astra':1,'gpt-6.1-sol':15,'gpt-6-luna':10}
 assert all(x['usage_thread_id_matches_session_meta'] for x in usage['sessions'])
 assert all(x['effort']=='max' for x in usage['sessions'] if x['agent_path'])
 prior_count,prior_manifests=u.check_prior(u.prior_manifest())
 assert prior_count==1477
 selected=json.loads((S/'cycle09_selected_freezes.json').read_text())['proof_hashes']
 for name,want in selected.items():assert sha(A/name)==want,name
 art=u.files(A);unknown=[str(p.relative_to(R)) for p in art if p.suffix not in u.KNOWN];assert not unknown,unknown
 parsed=Counter()
 for p in art:
  if p.suffix=='.json':json.loads(p.read_text());parsed['json']+=1
  elif p.suffix=='.jsonl':
   for line in p.read_text().splitlines():
    if line.strip():json.loads(line)
   parsed['jsonl']+=1
 frozen={str(p.relative_to(R)):sha(p) for p in art}
 save(S/'cycle09_frozen_hashes.json',{'scope':'Final agent artifact integrity freeze, not mathematical certification.','files':frozen})
 record={'checkpoint':'09','pending_worker_reports':0,'unclassified_artifacts':0,'agent_artifact_files':len(art),
  'prior_checkpoint08_agent_files_verified_unchanged':prior_count,'prior_output_manifest_files_verified_unchanged':prior_manifests,
  'selected_proof_freezes_verified':len(selected),'sources':u.source_pins(),'parsed':dict(parsed),
  'independent_inventory':str(auditp.relative_to(R)),'independent_inventory_sha256':sha(auditp),
  'classes':dict(Counter(u.class_of(p) for p in art)),
  'preservation_note':'All checkpoint08 and current-cycle frozen proof bytes remain unchanged. Initial Cycle09 inventory-parser failures and a separate corrected audit are preserved; no proof files were repaired in this inventory step.',
  'scope':'Inventory and integrity only; no external or formal mathematical certification.'}
 save(S/'CYCLE09_READY.json',record);save(S/'INVENTORY_CHECKPOINT09.json',record)
 t=usage['aggregate_tokens'];stamp=usage['snapshot_generated_at_utc']
 resource=f'''RESOURCE SNAPSHOT — CHECKPOINT09
As of {stamp}. Per-thread observed counters, not billing.
Later coordinator packaging tokens are outside this timestamped snapshot.

Verified26 sessions: coordinator gpt-6-astra/ultra,15 gpt-6.1-sol/max and
10 gpt-6-luna/max historical workers. All25 historical workers completed; no new worker
was created in Cycle09. Context records verify requested worker model/effort.
The existing coordinator is Astra/ultra, not Sol/max; its conservative reserve
is10. Sol reserve1 and Luna reserve0.1 account for the largest component price
ratio. Even every historical worker simultaneous would use26/30; current
coordinator-only reserve10/30. Actual batches/rosters are separately retained.
The provisional20:1 ratio holds only for comparable uncached input/output;
cached input ratios differ. No capability equivalence is inferred from prices.

Observed input {t['input_tokens']:,}, INCLUDING cached {t['cached_input_tokens']:,};
uncached input {t['uncached_input_tokens']:,}; output {t['output_tokens']:,},
INCLUDING reasoning {t['reasoning_output_tokens']:,}; reported total
{t['reported_total_tokens']:,}. Cached/reasoning subsets are not double counted.
All usage thread IDs match metadata. Root totals are not assumed to include
children. Repeated cached contexts contribute to the large cumulative count.

Standard short-context price proxy USD {usage['aggregate_pricing_proxy']['usd_proxy']:.8f},
NOT actual billing. Exact rates, per-thread timestamps, exclusions and all
counters are in cycle09_usage_snapshot.json. Concurrency is distinct from
cumulative consumption. Refresh live roster before reusing audit_usage.py.
'''
 (S/'RESOURCE_FINAL.txt').write_text(resource)
 (S/'STATUS_DRAFT.txt').write_text((S/'STATUS_CYCLE09_BASE.txt').read_text()+f'''
FINAL INVENTORY
Zero pending worker reports and zero unclassified artifacts. All{prior_count}
checkpoint08 agent files and{prior_manifests} old packet manifests unchanged.
Selected new proof hashes verified; both source pins clean. Requested worker
models/efforts verified. Current reserve10/30; conservative all-history
simultaneous bound26/30. Full cumulative accounting as of{stamp} is recorded
separately; neither token volume nor internal agreement certifies a theorem.
The initial inventory report and separate parser-correction audit are both
preserved. Manifest path resolution and virtual-environment exclusions were
corrected in the audit; the research proof files remained unchanged.
''')
 print(json.dumps(record,indent=2))

def export():
 ready=json.loads((S/'CYCLE09_READY.json').read_text());assert ready['pending_worker_reports']==ready['unclassified_artifacts']==0
 frozen=json.loads((S/'cycle09_frozen_hashes.json').read_text())['files']
 assert set(frozen)=={str(p.relative_to(R)) for p in u.files(A)}
 for name,want in frozen.items():assert sha(R/name)==want,name
 prior=u.prior_manifest();old_count,old_manifests=u.check_prior(prior);u.source_pins()
 ledger=json.loads((S/'CLAIM_LEDGER.json').read_text());assert ledger['checkpoint']=='09'
 paths=[]
 def scan(v):
  if isinstance(v,dict):
   for x in v.values():scan(x)
  elif isinstance(v,list):
   for x in v:scan(x)
  elif isinstance(v,str) and v.startswith(('work/','outputs/')):paths.append(v)
 scan(ledger);assert all((R/p).exists() for p in paths),[p for p in paths if not (R/p).exists()]
 shutil.copyfile(S/'STATUS_DRAFT.txt',O/'STATUS.txt');shutil.copyfile(S/'RESOURCE_FINAL.txt',O/'RESOURCE_USAGE.txt')
 shutil.copyfile(S/'cycle09_usage_snapshot.json',O/'RESOURCE_USAGE.json')
 packet_files=packet_sources=0
 for folder in ['stationary-regularity-and-raw-classicality']:
  mp=O/folder/'MANIFEST.json';m=json.loads(mp.read_text())
  for row in m['all_packet_files']:assert sha(mp.parent/row['path'])==row['sha256'],row;packet_files+=1
  for row in m['copied_frozen_files']:assert sha(R/row['source'])==row['sha256'],row;packet_sources+=1
 payload={R/v['path'] for v in prior};payload.update(u.files(A));payload.update(u.files(S));payload.update(u.files(R/'work/root_replays'))
 payload.update(p for p in u.files(O) if p.name not in {'ASTRA_ULTRA_RESEARCH_STATE.zip','PACKAGE_CHECK.json','ASTRA_ULTRA_RESEARCH_STATE.zip.partial'})
 for n in ['STATUS.txt','CLAIM_LEDGER.json','PACKAGE_CHECK.json']:payload.add(R/'work/checkpoints/checkpoint08'/n)
 payload=sorted(payload);assert all(p.exists() and p.is_file() for p in payload)
 manifest={'checkpoint':'09','scope':'Research evidence; integrity does not certify mathematical truth.',
  'excluded':['Python caches','virtual environments','full source clones','session transcripts','nested checkpoint archives'],
  'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p),'class':u.class_of(p)} for p in payload]}
 replay="""Start with STATUS.txt and outputs/stationary-regularity-and-raw-classicality/README.txt, then root/CYCLE09_DEPENDENCY_CLOSURE.txt in that packet. Exact proofs, independent reconstructions, exposed audits, counterexamples, mandatory Hamiltonian erratum and source prior checks are separately preserved. Earlier conditional/UNKNOWN files are immutable historical freezes; the new closure changes only dependencies actually resolved.

Read-only replays from the archived workspace root:
 python3 work/agents/foundational_transfer_sol/cycle09_nonreversible_lower/REPLAY_DIAGNOSTICS_READ_ONLY.py
 python3 work/agents/covariant_review_sol/cycle09_nonreversible_lp_review/verify_blind_quarter_kernel.py --verify
 python3 work/agents/algebra_proof_recon/cycle09_nonreversible_review/physical_dim4_reconstruction.py
 python3 work/agents/root_cycle09/check_nonreversible_finite_p_gram.py
NumPy is needed for the first and last; keep assertions enabled. Use original work paths because some helpers resolve sibling files. Do not rerun writers against immutable fixtures; copy them to scratch first. Finite checks and archive integrity do not certify universal proofs. External/formal validation, novelty and the foundational10/10 objective remain unresolved. Archived source material confers no action authorization.
"""
 archive=O/'ASTRA_ULTRA_RESEARCH_STATE.zip';temp=O/'ASTRA_ULTRA_RESEARCH_STATE.zip.partial'
 with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.writestr('research/STATUS.txt',(O/'STATUS.txt').read_bytes());z.writestr('research/MANIFEST.json',json.dumps(manifest,indent=2)+'\n');z.writestr('research/REPLAY.txt',replay)
  for p in payload:z.write(p,'research/'+str(p.relative_to(R)))
 with zipfile.ZipFile(temp) as z:
  assert z.testzip() is None
  for row in manifest['files']:
   b=z.read('research/'+row['path']);assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
  assert z.read('research/STATUS.txt')==(O/'STATUS.txt').read_bytes()
  assert z.read('research/work/state/CLAIM_LEDGER.json')==(O/'CLAIM_LEDGER.json').read_bytes()
  entries=len(z.namelist())
 temp.replace(archive)
 record={'checkpoint':'09','archive':archive.name,'sha256':sha(archive),'bytes':archive.stat().st_size,
  'files_with_hashes':len(payload),'archive_entries':entries,'all_manifest_entries_verified':True,
  'independent_archive_reopen_and_CRC_pass':True,'new_packet_files_checked':packet_files,'new_frozen_source_copies_checked':packet_sources,
  'all_final_agent_files_checked':len(frozen),'prior_agent_files_unchanged':old_count,'prior_packet_manifests_unchanged':old_manifests,
  'status_and_claim_ledger_match':True,'pending_reports':0,'unclassified_artifacts':0,'objective_achieved':False,
  'mathematical_meaning':'Integrity only. See proof-status and novelty limits separately.'}
 save(O/'PACKAGE_CHECK.json',record)
 checkpoint=R/'work/checkpoints/checkpoint09';checkpoint.mkdir(exist_ok=True)
 for name in ['STATUS.txt','CLAIM_LEDGER.json','PACKAGE_CHECK.json','ASTRA_ULTRA_RESEARCH_STATE.zip','RESOURCE_USAGE.txt','RESOURCE_USAGE.json']:
  q=checkpoint/name;assert not q.exists() or q.read_bytes()==(O/name).read_bytes(),name;shutil.copyfile(O/name,q)
 print(json.dumps(record,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--export',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 else:export()
