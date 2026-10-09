"""Finalize inventory only after all reports and proof packets are complete."""
from pathlib import Path
from collections import Counter
import hashlib,json,subprocess,zipfile

R=Path(__file__).resolve().parents[2];S=R/'work/state'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
u=json.loads((S/'cycle04_usage_snapshot.json').read_text());t=u['aggregate_tokens']
assert u['concurrent_reservation']['active_thread_count']==1
assert u['discovery']['descendant_count']==25
assert u['dispatch_verification']['effective_context_model_counts_including_root']=={'gpt-6-astra':1,'gpt-6-luna':10,'gpt-6.1-sol':15}
assert all(x['usage_thread_id_matches_session_meta'] for x in u['sessions'])
assert all(x['effort']=='max' for x in u['sessions'] if x['agent_path'] is not None)
stamp=u['snapshot_generated_at_utc']
(S/'RESOURCE_FINAL.txt').write_text(f'''RESOURCE SNAPSHOT — CHECKPOINT04
As of {stamp}. Actual observed per-thread token counters, not actual billing.
Later coordinator packaging tokens are outside this timestamped snapshot.

Verified26 sessions: root gpt-6-astra/ultra,15 gpt-6.1-sol/max workers,
10 gpt-6-luna/max workers. All25 workers completed at the final roster
snapshot; no descendants of workers. The root configuration is the actual
existing coordinator model, not silently reported as Sol/max. All explicitly
dispatched worker models and maximum efforts match their logged contexts.

Conservative reservation: root10, Sol1, Luna0.1 using the maximum component
price ratio. Current coordinator-only reservation10/30. Even all historical
workers simultaneously would reserve26/30, so every adaptive batch fits.
The provisional20:1 ratio applies to comparable uncached input/output
consumption; cached ratios differ. Price ratio is not an ability assertion.
Concurrency capacity is not cumulative usage or an imposed spending budget.

Observed input {t['input_tokens']:,}, INCLUDING cached {t['cached_input_tokens']:,};
uncached input {t['uncached_input_tokens']:,};
output {t['output_tokens']:,}, INCLUDING reasoning {t['reasoning_output_tokens']:,};
reported total {t['reported_total_tokens']:,}.
Cached and reasoning components are not added twice. Repeated cached prompts
contribute to cumulative counts. Metadata confirms every usage record's
thread ID, so the coordinator is not assumed to include child totals.

Standard short-context pricing proxy USD {u['aggregate_pricing_proxy']['usd_proxy']:.8f},
NOT billing. Rates, exclusions, per-thread counters, timestamps and model
evidence are in cycle04_usage_snapshot.json. Replay after refreshing roster:
python3 work/state/audit_usage.py --dispatch-file work/state/dispatch.json
 --output work/state/cycle04_usage_snapshot.json
''')
p=S/'STATUS_DRAFT.txt';body=p.read_text().split('\nRESOURCE SNAPSHOT\n')[0]
body+=f'''\nRESOURCE SNAPSHOT
All25 historical workers completed. Configurations verified:15 Sol/max and
10 Luna/max; the coordinator is Astra/ultra. The conservative all-worker
simultaneous upper bound is26/30 Sol-max equivalents; final reservation10/30.
Actual cumulative counters as of {stamp} are preserved in RESOURCE_FINAL.txt
and cycle04_usage_snapshot.json. Pricing proxies are explicitly not billing.
'''
p.write_text(body)

files=[p for p in sorted((R/'work/agents').rglob('*')) if p.is_file() and not {'venv','.venv','__pycache__'}.intersection(p.parts) and p.suffix!='.pyc']
known={'.json','.txt','.py','.pdf','.png','.npz','.log','.html','.tar','.jsonl','.sqlite3','.tex','.bib','.gz','.bbl','.gls','.glo','.glg','.ist','.md'}
unclassified=[str(p.relative_to(R)) for p in files if p.suffix not in known]
assert not unclassified,unclassified
parsed=Counter()
for p in files:
 if p.suffix=='.json':json.loads(p.read_text());parsed['json']+=1
 if p.suffix=='.jsonl':
  for line in p.read_text().splitlines():
   if line.strip():json.loads(line)
  parsed['jsonl']+=1

with zipfile.ZipFile(R/'work/checkpoints/checkpoint03/ASTRA_ULTRA_RESEARCH_STATE.zip') as z:
 previous=json.loads(z.read('research/MANIFEST.json'))['files']
 old=[v for v in previous if v['path'].startswith('work/agents/')]
 for row in old:assert sha(R/row['path'])==row['sha256'],row['path']

packet_counts={}
for folder in ['universal-broadcasting-proof','bounded-capacity-classicality','effective-broadcasting-compiler','classicality-extensions','memory-obstructions']:
 p=R/'outputs'/folder/'MANIFEST.json';m=json.loads(p.read_text())
 for row in m.get('copied_frozen_files',m.get('files',[])):
  assert sha(p.parent/row['path'])==row['sha256'],row
  if 'source' in row:assert sha(R/row['source'])==row['sha256'],row
 for row in m.get('all_packet_files',[]):assert sha(p.parent/row['path'])==row['sha256'],row
 packet_counts[folder]=len(m.get('all_packet_files',[]))

ledger=json.loads((S/'CLAIM_LEDGER.json').read_text());assert len(ledger['claims'])==39
paths=[]
def scan(v):
 if isinstance(v,dict):
  for x in v.values():scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
 elif isinstance(v,str) and v.startswith(('work/','outputs/')):paths.append(v)
scan(ledger)
missing=[x for x in paths if not (R/x).exists()];assert not missing,missing

pins=[]
for name,want in [('astra','39cdea532f19217f633f70315d92c314a6ce5e3e'),('openai-math','fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb')]:
 cwd=R/'work/sources'/name
 actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=cwd,text=True).strip()
 status=subprocess.check_output(['git','status','--porcelain'],cwd=cwd,text=True).strip()
 assert actual==want and not status,(name,actual,status)
 pins.append({'source':name,'pin':actual,'clean':True})
frozen={str(p.relative_to(R)):sha(p) for p in files if any(part.startswith('cycle04') for part in p.parts) or 'root_cycle04' in p.parts}
save(S/'cycle04_frozen_hashes.json',{'scope':'Checkpoint04 artifact freeze; hashes prove integrity only. Prior633 agent files independently compared with checkpoint03 archive.','files':frozen})

record={'checkpoint':'04','pending_worker_reports':0,'unclassified_artifact_files':0,
 'claim_count':39,'missing_claim_paths':missing,'agent_artifact_files':len(files),
 'parsed_artifacts':dict(parsed),'extensions':dict(sorted(Counter(p.suffix for p in files).items())),
 'prior_checkpoint03_agent_files_verified_unchanged':len(old),'cycle04_frozen_artifact_count':len(frozen),
 'packet_file_counts':packet_counts,'sources':pins,
 'worker_completion_evidence':'Fresh collaboration.list_agents plus coordinator-only dispatch snapshot;25 workers completed.',
 'replay_scope':'cycle04_*replay_stdout.txt and copied scripts/results under work/root_replays/cycle04; exact finite checks plus explicitly marked numerical process probes, not formal proof.',
 'scope':'Inventory/integrity only. Mathematical and historical status remains as in claim ledger.'}
save(S/'INVENTORY_CHECKPOINT04.json',record)
print(json.dumps(record,indent=2))
