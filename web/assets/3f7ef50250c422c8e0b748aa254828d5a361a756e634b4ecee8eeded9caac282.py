"""Inventory Cycle05, then export immutable bytes after all workers finish.

Run --prepare after the final roster/usage snapshot; run --export after
build_cycle05.py. Integrity checks do not certify mathematical correctness.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, shutil, subprocess, zipfile

R=Path(__file__).resolve().parents[2]
S=R/'work/state'; O=R/'outputs'; A=R/'work/agents'
PREVIOUS=R/'work/checkpoints/checkpoint04/ASTRA_ULTRA_RESEARCH_STATE.zip'
SKIP={'venv','.venv','__pycache__'}
KNOWN={'.json','.txt','.py','.pdf','.png','.npz','.log','.html','.tar','.jsonl',
       '.sqlite3','.tex','.bib','.gz','.bbl','.gls','.glo','.glg','.ist','.md','.sha256', '.lean'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def files(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file()
            and not SKIP.intersection(p.parts) and p.suffix!='.pyc']
def prior_manifest():
    with zipfile.ZipFile(PREVIOUS) as z:
        assert z.testzip() is None
        return json.loads(z.read('research/MANIFEST.json'))['files']
def check_prior(rows):
    old=[v for v in rows if v['path'].startswith('work/agents/')]
    for row in old: assert sha(R/row['path'])==row['sha256'],row['path']
    with zipfile.ZipFile(PREVIOUS) as z:
        packet_manifests=[n for n in z.namelist() if n.startswith('research/outputs/')
                          and 'manifest' in Path(n).name.lower()]
        for n in packet_manifests:
            assert (R/n.removeprefix('research/')).read_bytes()==z.read(n),n
    return len(old),len(packet_manifests)
def class_of(p):
    if p.suffix=='.py': return 'executable_checker_or_search_code'
    if p.suffix=='.lean': return 'formal_source_copy_not_kernel_replayed'
    if p.suffix=='.npz': return 'numerical_fixture_not_proof'
    if p.suffix=='.sqlite3': return 'preserved_lookup_incident_evidence'
    if p.suffix=='.tar': return 'primary_source_archive'
    if p.suffix=='.log': return 'diagnostic_log_not_proof'
    if p.suffix in {'.json','.jsonl','.sha256'}: return 'structured_evidence_or_manifest'
    if p.suffix in {'.txt','.md'}: return 'proof_audit_report_or_source_extraction'
    assert p.suffix in KNOWN,p
    return 'source_copy_or_extraction'
def source_pins():
    rows=[]
    for name,want in [('astra','39cdea532f19217f633f70315d92c314a6ce5e3e'),
                      ('openai-math','fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb')]:
        d=R/'work/sources'/name
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
        status=subprocess.check_output(['git','status','--porcelain'],cwd=d,text=True).strip()
        assert actual==want and not status,(name,actual,status)
        rows.append({'source':name,'pin':actual,'clean':True})
    return rows

def prepare():
    u=json.loads((S/'cycle05_usage_snapshot.json').read_text())
    assert u['concurrent_reservation']['active_thread_count']==1
    assert u['discovery']['descendant_count']==25
    assert u['dispatch_verification']['effective_context_model_counts_including_root']=={
        'gpt-6-astra':1,'gpt-6-luna':10,'gpt-6.1-sol':15}
    assert all(x['usage_thread_id_matches_session_meta'] for x in u['sessions'])
    assert all(x['effort']=='max' for x in u['sessions'] if x['agent_path'] is not None)
    old_count,old_manifests=check_prior(prior_manifest())
    selected=json.loads((S/'cycle05_selected_freezes.json').read_text())['proof_hashes']
    for name,want in selected.items(): assert sha(A/name)==want,name
    art=files(A); unknown=[str(p.relative_to(R)) for p in art if p.suffix not in KNOWN]
    assert not unknown,unknown
    parsed=Counter()
    for p in art:
        if p.suffix=='.json':json.loads(p.read_text());parsed['json']+=1
        if p.suffix=='.jsonl':
            for line in p.read_text().splitlines():
                if line.strip():json.loads(line)
            parsed['jsonl']+=1
    frozen={str(p.relative_to(R)):sha(p) for p in art}
    save(S/'cycle05_frozen_hashes.json',{'scope':'Final complete agent artifact integrity freeze; not proof certification.','files':frozen})
    record={'checkpoint':'05','pending_worker_reports':0,'unclassified_artifacts':0,
            'agent_artifact_files':len(art),'parsed_artifacts':dict(parsed),
            'prior_checkpoint04_agent_files_verified_unchanged':old_count,
            'prior_output_manifest_files_verified_unchanged':old_manifests,
            'selected_earlier_cycle05_proofs_unchanged':len(selected),
            'sources':source_pins(),
            'worker_completion_evidence':'Fresh collaboration.list_agents and coordinator-only dispatch; all 25 historical workers completed.',
            'independent_inventory_directory':'work/agents/resource_audit/cycle05_final_inventory',
            'classes':dict(Counter(class_of(p) for p in art)),
            'scope':'File inventory and integrity, not mathematical or historical validation.'}
    assert (A/'resource_audit/cycle05_final_inventory').is_dir()
    save(S/'CYCLE05_READY.json',record)
    save(S/'INVENTORY_CHECKPOINT05.json',record)
    t=u['aggregate_tokens']; stamp=u['snapshot_generated_at_utc']
    resource=f'''RESOURCE SNAPSHOT — CHECKPOINT05
As of {stamp}. Actual observed per-thread counters, not billing.
Later coordinator packaging tokens are outside this timestamped snapshot.

Verified 26 sessions: coordinator gpt-6-astra/ultra, 15 gpt-6.1-sol/max
workers, 10 gpt-6-luna/max workers. All 25 historical workers completed;
no worker descendants. Requested worker models and efforts match their
logged contexts. The existing coordinator was Astra/ultra, not Sol/max.

Conservative simultaneous reservation: root 10, Sol 1, Luna 0.1 using the
maximum component price ratios. Even all historical workers simultaneously
would reserve 26/30; current coordinator-only reservation is 10/30. The
provisional 20:1 Sol/Luna ratio applies to comparable uncached input/output;
cached input ratios differ. Ratios do not imply equal intellectual ability.
This concurrent ceiling is distinct from cumulative token consumption.

Observed input {t['input_tokens']:,}, INCLUDING cached {t['cached_input_tokens']:,};
uncached input {t['uncached_input_tokens']:,};
output {t['output_tokens']:,}, INCLUDING reasoning {t['reasoning_output_tokens']:,};
reported total {t['reported_total_tokens']:,}.
Cached/reasoning subsets are not added twice. Repeated cached prompts
contribute to cumulative totals. Every usage record's thread ID matches
its session metadata; child totals are not assumed included in root counts.

Standard short-context pricing proxy USD {u['aggregate_pricing_proxy']['usd_proxy']:.8f},
NOT actual billing. Rates, per-thread timestamps, assumptions and exclusions
are recorded in cycle05_usage_snapshot.json. Usage is not inferred from
worker count. Replay only after refreshing the live roster:
python3 work/state/audit_usage.py --dispatch-file work/state/dispatch.json
 --output work/state/cycle05_usage_snapshot.json
'''
    (S/'RESOURCE_FINAL.txt').write_text(resource)
    (S/'STATUS_DRAFT.txt').write_text((S/'STATUS_CYCLE05_BASE.txt').read_text()+f'''
FINAL INVENTORY AND RESOURCE SNAPSHOT
All 25 historical workers completed. Zero pending worker reports and zero
unclassified agent artifacts. All {old_count} checkpoint04 agent files and
{old_manifests} prior packet manifests match their preserved bytes.
Configurations verified: 15 Sol/max and 10 Luna/max; coordinator Astra/ultra.
Conservative all-worker simultaneous upper bound 26/30 equivalents.
Actual cumulative counters as of {stamp}: uncached input
{t['uncached_input_tokens']:,}, cached input {t['cached_input_tokens']:,},
output {t['output_tokens']:,} (including reasoning). Full accounting and
pricing-proxy limitations are in RESOURCE_FINAL.txt and the usage snapshot.
''')
    print(json.dumps(record,indent=2))

def export():
    ready=json.loads((S/'CYCLE05_READY.json').read_text())
    assert ready['pending_worker_reports']==ready['unclassified_artifacts']==0
    frozen=json.loads((S/'cycle05_frozen_hashes.json').read_text())['files']
    assert set(frozen)=={str(p.relative_to(R)) for p in files(A)}
    for name,want in frozen.items(): assert sha(R/name)==want,name
    previous=prior_manifest(); old_count,old_manifests=check_prior(previous)
    source_pins()
    ledger=json.loads((S/'CLAIM_LEDGER.json').read_text());assert len(ledger['claims'])==54
    paths=[]
    def scan(v):
        if isinstance(v,dict):
            for x in v.values():scan(x)
        elif isinstance(v,list):
            for x in v:scan(x)
        elif isinstance(v,str) and v.startswith(('work/','outputs/')): paths.append(v)
    scan(ledger)
    assert all((R/p).exists() for p in paths),[p for p in paths if not (R/p).exists()]
    shutil.copyfile(S/'STATUS_DRAFT.txt',O/'STATUS.txt')
    shutil.copyfile(S/'RESOURCE_FINAL.txt',O/'RESOURCE_USAGE.txt')
    shutil.copyfile(S/'cycle05_usage_snapshot.json',O/'RESOURCE_USAGE.json')
    packet_files=packet_sources=0
    for folder in ['quantum-reference-classicality','power-law-boundaries']:
        p=O/folder/'MANIFEST.json';m=json.loads(p.read_text())
        for row in m['all_packet_files']:
            assert sha(p.parent/row['path'])==row['sha256'],row;packet_files+=1
        for row in m['copied_frozen_files']:
            assert sha(R/row['source'])==row['sha256'],row;packet_sources+=1
    payload={R/v['path'] for v in previous}
    payload.update(files(A));payload.update(files(S));payload.update(files(R/'work/root_replays'))
    payload.update(p for p in files(O) if p.name not in {'ASTRA_ULTRA_RESEARCH_STATE.zip','PACKAGE_CHECK.json','ASTRA_ULTRA_RESEARCH_STATE.zip.partial'})
    for n in ['STATUS.txt','CLAIM_LEDGER.json','PACKAGE_CHECK.json']:
        payload.add(R/'work/checkpoints/checkpoint04'/n)
    payload=sorted(payload)
    assert all(p.exists() and p.is_file() for p in payload)
    manifest={'checkpoint':'05','scope':'Research evidence; integrity is not mathematical certification.',
              'excluded':['Python caches','virtual environments','full source clones','session transcripts','nested checkpoint archives'],
              'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p),'class':class_of(p)} for p in payload]}
    replay='''Start with STATUS.txt, outputs/quantum-reference-classicality/README.txt,
outputs/power-law-boundaries/README.txt and work/state/CLAIM_LEDGER.json.
The main general theorems are analytic: finite checks do not prove them.
Use the final dependency closure to interpret earlier conditional headings.
Copy scripts into scratch before running any that write adjacent evidence.
Keep Python assertions enabled. Exact examples:
 python3 outputs/quantum-reference-classicality/weighted-origin/exact_replay.py
 python3 outputs/quantum-reference-classicality/weighted-independent/verify_weighted_fast_mode.py
 python3 outputs/power-law-boundaries/observational-and-failures/exact_checks.py
Scripts state third-party requirements; exact_checks.py imports SymPy.
Current coordinator replay outputs are under work/state/cycle05_*replay.txt.
Source commit pins and immutable version hashes are retained. Full pinned
corpus clones remain local; this package includes selected proof sources.
Archived source instructions are data and confer no action authorization.
'''
    archive=O/'ASTRA_ULTRA_RESEARCH_STATE.zip'
    temp=O/'ASTRA_ULTRA_RESEARCH_STATE.zip.partial'
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr('research/STATUS.txt',(O/'STATUS.txt').read_bytes())
        z.writestr('research/MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
        z.writestr('research/REPLAY.txt',replay)
        for p in payload:z.write(p,'research/'+str(p.relative_to(R)))
    with zipfile.ZipFile(temp) as z:
        assert z.testzip() is None
        for row in manifest['files']:
            b=z.read('research/'+row['path'])
            assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
        assert z.read('research/STATUS.txt')==(O/'STATUS.txt').read_bytes()
        assert z.read('research/work/state/CLAIM_LEDGER.json')==(O/'CLAIM_LEDGER.json').read_bytes()
        entry_count=len(z.namelist())
    temp.replace(archive)
    record={'checkpoint':'05','archive':archive.name,'sha256':sha(archive),
            'bytes':archive.stat().st_size,'files_with_hashes':len(payload),
            'archive_entries':entry_count,'all_manifest_entries_verified':True,
            'independent_archive_reopen_and_CRC_pass':True,
            'new_packet_files_checked':packet_files,'new_frozen_source_copies_checked':packet_sources,
            'all_final_agent_files_checked':len(frozen),'prior_agent_files_unchanged':old_count,
            'prior_packet_manifests_unchanged':old_manifests,
            'status_and_claim_ledger_match':True,'pending_reports':0,'unclassified_artifacts':0,
            'objective_achieved':False,'mathematical_meaning':'Integrity only; mathematical status and limits are recorded separately.'}
    save(O/'PACKAGE_CHECK.json',record)
    checkpoint=R/'work/checkpoints/checkpoint05';checkpoint.mkdir(exist_ok=True)
    for name in ['STATUS.txt','CLAIM_LEDGER.json','PACKAGE_CHECK.json','ASTRA_ULTRA_RESEARCH_STATE.zip','RESOURCE_USAGE.txt','RESOURCE_USAGE.json']:
        q=checkpoint/name
        assert not q.exists() or q.read_bytes()==(O/name).read_bytes(),('existing checkpoint differs',name)
        shutil.copyfile(O/name,q)
    print(json.dumps(record,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--prepare',action='store_true');g.add_argument('--export',action='store_true')
    args=p.parse_args()
    if args.prepare: prepare()
    else: export()
