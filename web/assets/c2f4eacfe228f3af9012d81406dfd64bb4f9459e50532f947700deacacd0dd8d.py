from pathlib import Path
from collections import Counter
import hashlib, json, subprocess

R=Path(__file__).resolve().parents[2]
S=R/'work/state'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
usage=json.loads((S/'cycle03_usage_snapshot.json').read_text())
t=usage['aggregate_tokens']; timestamp=usage['snapshot_generated_at_utc']
assert usage['concurrent_reservation']['active_thread_count']==1
assert usage['discovery']['descendant_count']==25
assert usage['dispatch_verification']['effective_context_model_counts_including_root']=={'gpt-6-astra':1,'gpt-6-luna':10,'gpt-6.1-sol':15}
assert all(x['usage_thread_id_matches_session_meta'] for x in usage['sessions'])
(S/'RESOURCE_FINAL.txt').write_text(f'''FINAL RESOURCE SNAPSHOT, CHECKPOINT03
As of {timestamp}. Counters are cumulative per-thread observed usage,
not actual billing. Later coordinator packaging tokens are outside this
snapshot; the timestamp is not an end-of-account invoice.

Verified 26 sessions: coordinator gpt-6-astra/ultra; 15 workers gpt-6.1-sol/max;
10 workers gpt-6-luna/max. All requested worker configurations match logged
turn contexts. All 25 workers completed; only coordinator active at snapshot.
No descendants of workers. All historical workers simultaneously would
reserve 26/30 Sol-max price equivalents using maximum component ratios
Astra 10, Sol 1, Luna 0.1. Current reservation is 10/30. Thus concurrency
remained below 30 even under this conservative historical upper bound.
Concurrent capacity is separate from cumulative token use.

Observed token totals:
 input {t['input_tokens']:,}, including cached {t['cached_input_tokens']:,};
 uncached input {t['uncached_input_tokens']:,};
 output {t['output_tokens']:,}, including reasoning {t['reasoning_output_tokens']:,};
 reported total {t['reported_total_tokens']:,}.
Reasoning is included in output, and cached tokens are included in input;
neither is added twice. Repeated cached prompts contribute to cumulative
counts. Each usage record belongs to its own metadata thread ID; parent
records are not assumed to include child cumulative counters.

Standard short-context pricing proxy USD {usage['aggregate_pricing_proxy']['usd_proxy']:.8f}, NOT actual billing
or an imposed budget. Rates and exclusions are in the JSON. The 20:1
Luna/Sol ratio applies to comparable uncached input/output consumption;
cached-input ratio differs. No equal-capability inference is made.

Machine-readable per-session evidence: cycle03_usage_snapshot.json.
Replay: python3 work/state/audit_usage.py --dispatch-file work/state/dispatch.json
        --output work/state/cycle03_usage_snapshot.json
Refresh the active roster first if work resumes. The script reads only
descendant metadata/usage and emits no message or prompt contents.
''')
p=S/'STATUS_DRAFT.txt';s=p.read_text()
s+='\nRESOURCE SNAPSHOT\nAll 25 workers completed: 15 verified Sol/max and 10 Luna/max. The coordinator is Astra/ultra and is counted at a conservative 10 Sol equivalents. Even the upper bound with every historical worker active simultaneously is 26/30; the final coordinator-only reservation is 10/30. The final cumulative usage snapshot is '+timestamp+'; exact counters and the non-billing pricing proxy are in RESOURCE_FINAL.txt and cycle03_usage_snapshot.json.\n'
p.write_text(s)

for folder in ['universal-broadcasting-proof','bounded-capacity-classicality']:
 p=R/'outputs'/folder/'MANIFEST.json';d=json.loads(p.read_text())
 for row in d.get('copied_frozen_files',d.get('files',[])):
  assert digest(p.parent/row['path'])==row['sha256'],row['path']
  assert digest(R/row['source'])==row['sha256'],row['source']
 d['all_packet_files']=[{'path':str(f.relative_to(p.parent)),'bytes':f.stat().st_size,'sha256':digest(f)} for f in sorted(p.parent.rglob('*')) if f.is_file() and f!=p and '__pycache__' not in f.parts]
 d['manifest_scope']='Integrity only. Excludes this manifest itself; frozen copy provenance and all packet artifacts verified separately from proof status.'
 save(p,d)

files=[p for p in sorted((R/'work/agents').rglob('*')) if p.is_file() and not {'venv','.venv','__pycache__'}.intersection(p.parts) and p.suffix!='.pyc']
known={'.json','.txt','.py','.pdf','.png','.npz','.log','.html','.tar','.jsonl','.sqlite3','.tex','.bib','.gz','.bbl','.gls','.glo','.glg','.ist'}
unclassified=[str(p.relative_to(R)) for p in files if p.suffix not in known]
assert not unclassified,unclassified
json_count=jsonl_count=0
for p in files:
 if p.suffix=='.json': json.loads(p.read_text());json_count+=1
 if p.suffix=='.jsonl':
  for line in p.read_text().splitlines():
   if line.strip(): json.loads(line)
  jsonl_count+=1
ledger=json.loads((S/'CLAIM_LEDGER.json').read_text())
paths=[]
def scan(v):
 if isinstance(v,dict):
  for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
 elif isinstance(v,str) and v.startswith(('work/','outputs/')): paths.append(v)
scan(ledger)
missing=[p for p in paths if not (R/p).exists()]
assert not missing,missing
frozen=json.loads((S/'cycle03_frozen_hashes.json').read_text())['files']
for p,h in frozen.items():assert digest(R/p)==h,p
sources=[]
for name,expected in [('astra','39cdea532f19217f633f70315d92c314a6ce5e3e'),('openai-math','fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb')]:
 cwd=R/'work/sources'/name
 pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=cwd,text=True).strip()
 status=subprocess.check_output(['git','status','--porcelain'],cwd=cwd,text=True).strip()
 assert pin==expected and not status,(name,pin,status)
 sources.append({'source':name,'pin':pin,'clean':True})
record={'checkpoint':'03','pending_worker_reports':0,'unclassified_artifact_files':0,'claim_count':len(ledger['claims']),'missing_claim_paths':missing,'agent_artifact_files':len(files),'parsed_json_artifacts':json_count,'parsed_jsonl_artifacts':jsonl_count,'extensions':dict(sorted(Counter(p.suffix for p in files).items())),'selected_frozen_proof_hashes_checked':frozen,'sources':sources,'worker_completion_evidence':'Fresh collaboration.list_agents: all 25 workers completed; dispatch.json records coordinator-only active roster.','replay_evidence':'cycle03_*replay_stdout.txt and cycle03_tree_audit_stdout.txt; all seven independent root diagnostic groups and both portable checks passed. These are scoped finite checks, not formal proofs.','scope':'Inventory and integrity audit only; exact mathematical proof statuses are in CLAIM_LEDGER.json.','sqlite_artifact':'One zero-byte accidental lookup preserved in worker scratch, classified incident evidence; original removed and source tree clean.'}
save(S/'INVENTORY_CHECKPOINT03.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in ['selected_frozen_proof_hashes_checked','extensions']},indent=2))
