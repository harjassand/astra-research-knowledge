"""Package the research return and verify artifacts, not mathematical truth."""
from pathlib import Path
import hashlib,json,shutil,zipfile,re,datetime,sys
from urllib.parse import unquote

root=Path(__file__).resolve().parents[1]
out=root.parents[1]/'outputs'
record=out/'COLLECTIVE_INFORMATION_RESEARCH_RECORD'
dossier=out/'COLLECTIVE_INFORMATION_RESEARCH_DOSSIER.md'
ledger=out/'COLLECTIVE_INFORMATION_THEOREM_LEDGER.json'
archive=out/'COLLECTIVE_INFORMATION_RESEARCH_RECORD.zip'
report=out/'COLLECTIVE_INFORMATION_VALIDATION.json'
EXPECTED='756625ddb72122bc77aaa3f91d99ab109a0193cfda4ada062c8ab75dcde1fa14'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')

assert sha(root/'principal/CONSOLIDATED_DOSSIER.md')==EXPECTED
for role in ('auditor','machinery'):
    f=root/role/'FINAL_ASSEMBLED_REVIEW.md'
    assert f.exists() and EXPECTED in f.read_text(),str(f)
if '--refresh-owned' in sys.argv:
    previous=json.loads(report.read_text())
    for a in previous['artifacts']:
        assert sha(out/a['name'])==a['sha256'],'External change to '+a['name']
    pm=json.loads((record/'FILE_MANIFEST.json').read_text())['files']
    assert {str(p.relative_to(record)) for p in record.rglob('*') if p.is_file()}=={x['path'] for x in pm}|{'FILE_MANIFEST.json'}
    assert all(sha(record/x['path'])==x['sha256'] for x in pm)
else:
    for p in (record,dossier,ledger,archive,report):
        if p.exists():raise RuntimeError('Existing deliverable: '+str(p))
record.mkdir(parents=True,exist_ok=True)
ignored={'.git','.venv','__pycache__','.DS_Store'}
copied=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if not p.is_file() or any(s in ignored for s in rel.parts) or p.suffix=='.pyc':continue
    dest=record/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    assert sha(p)==sha(dest)
    copied.append(dict(path=str(rel),bytes=dest.stat().st_size,sha256=sha(dest)))
dump(record/'FILE_MANIFEST.json',{'scope':'All copied supporting files; this manifest excludes itself.','files':copied})
shutil.copy2(root/'principal/CONSOLIDATED_DOSSIER.md',dossier)
shutil.copy2(root/'COLLECTIVE_INFORMATION_THEOREM_LEDGER.json',ledger)
checks={'final_dossier_matches_reviewed_hash':sha(dossier)==EXPECTED}
claims=json.loads(ledger.read_text());ids=[c['id'] for c in claims['claims']]
checks['unique_ledger_ids']=len(ids)==len(set(ids))
checks['broad_goal_not_achieved']=claims['broad_objective']=='NOT_ACHIEVED_OPEN'
checks['no_physical_experiments']=claims['physical_experiments']==0
proofs=[]
for c in claims['claims']:
    p=record/c['proof'];proofs.append({'id':c['id'],'ok':p.is_file() and sha(p)==c['proof_sha256']})
checks['all_ledger_proofs_match']=all(x['ok'] for x in proofs)
initial=json.loads((record/'sources/INITIAL_REPORT_PINS.json').read_text())['reports']
checks['immutable_initials_match']=all(sha(record/x['path'])==x['sha256'] and (record/x['path']).stat().st_size==x['bytes'] for x in initial)
rr=json.loads((record/'verification-rerun/RERUN_REPORT.json').read_text());runs=[]
for x in rr['results']:
    p=record/'verification-rerun'/x['script'];l=record/'verification-rerun'/x['log']
    runs.append(x['exit_code']==0 and sha(p)==x['sha256'] and sha(l)==x['log_sha256'])
checks['eleven_finite_reruns_match']=len(runs)==11 and all(runs) and rr['all_pass']
json_errors=[];json_count=0
for p in record.rglob('*.json'):
    try:json.loads(p.read_text());json_count+=1
    except Exception as e:json_errors.append({'path':str(p.relative_to(record)),'error':str(e)})
checks['supporting_json_parses']=not json_errors
link_results=[]
for p in (dossier,record/'INDEX.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        target=target.strip().split(' "',1)[0].strip('<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
        file=unquote(target.split('#',1)[0])
        link_results.append({'document':str(p.relative_to(out)),'target':target,'exists':(p.parent/file).exists()})
checks['user_facing_local_links_resolve']=all(x['exists'] for x in link_results)
members=[dossier,ledger]+[p for p in sorted(record.rglob('*')) if p.is_file()]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in members:z.write(p,str(p.relative_to(out)))
with zipfile.ZipFile(archive) as z:
    checks['zip_crc_pass']=z.testzip() is None
    checks['zip_members_exact']=set(z.namelist())=={str(p.relative_to(out)) for p in members}
    checks['zip_member_hashes_match']=all(hashlib.sha256(z.read(str(p.relative_to(out)))).hexdigest()==sha(p) for p in members)
checks['copied_source_bytes_match']=all(sha(record/x['path'])==x['sha256'] for x in copied)
payload={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'scope':'Artifact/record verification only; not a mathematical theorem verifier, experiment or priority proof.',
         'all_checks_pass':all(checks.values()),'checks':checks,'theorem_entries':len(ids),
         'copied_supporting_files':len(copied),'supporting_json_files':json_count,'json_errors':json_errors,
         'ledger_proof_checks':proofs,'local_link_checks':link_results,
         'artifacts':[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in (dossier,ledger,archive)],
         'archive_members':len(members),'archive_contains':'Dossier, ledger and record. External validation is excluded to avoid a circular archive hash.'}
dump(report,payload)
print(json.dumps({k:payload[k] for k in ('all_checks_pass','checks','theorem_entries','copied_supporting_files','archive_members','artifacts')},indent=2))
if not payload['all_checks_pass']:sys.exit(1)
