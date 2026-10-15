#!/usr/bin/env python3
"""Root-authorized PR92 bounded suite and HNF audit, only in a complete external copy."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
REPO=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015')
PREFIX='updates/FT-foundational-capability-20261015/'
PIN='5eb2441c93011d4fefb819b6f751f33537427dc3'
OUT=Path(__file__).resolve().parent/'bounded_replay_v0001'
PYTHON=Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-direction-transport-v1/.venv/bin/python')
def need(v,msg):
 if not v:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def encoded(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def snapshot():
 names=set(git('ls-files','-z','--cached','--others','--exclude-standard').decode().split('\0'))
 return {name:sha(REPO/name) if (REPO/name).is_file() else None for name in sorted(names) if name and '__pycache__' not in Path(name).parts}
need(git('rev-parse','HEAD').decode().strip()==PIN,'PR92 head changed')
need(git('status','--porcelain')==b'','original audit checkout must stay clean')
need(not OUT.exists() and not OUT.is_relative_to(REPO),'new external replay output required')
before=snapshot();OUT.mkdir();(OUT/'ORIGINAL_INPUTS.json').write_bytes(encoded(before))
package=REPO/PREFIX/'package';copy=OUT/'package';shutil.copytree(package,copy,ignore=shutil.ignore_patterns('__pycache__'))
copy_initial={str(p.relative_to(copy)):sha(p) for p in sorted(copy.rglob('*')) if p.is_file()}
need(all(sha(package/name)==value for name,value in copy_initial.items()),'copy not byte-identical')
(OUT/'COPY_INITIAL_HASHES.json').write_bytes(encoded(copy_initial))
(OUT/'tmp').mkdir();env=dict(os.environ);env['TMPDIR']=str(OUT/'tmp');env['PYTHONDONTWRITEBYTECODE']='1'
runtime=json.loads(subprocess.check_output([str(PYTHON),'-B','-c','import json,sys,numpy,scipy,sympy;print(json.dumps(dict(python=sys.version,executable=sys.executable,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__)))'],text=True,env=env))
start=time.monotonic();command=[str(PYTHON),'-B',str(copy/'root/replay_selected.py')]
run=subprocess.run(command,cwd=copy/'root',capture_output=True,text=True,timeout=400,env=env)
(OUT/'suite.stdout.txt').write_text(run.stdout);(OUT/'suite.stderr.txt').write_text(run.stderr)
need(run.returncode==0,'copied eight-suite runner failed')
receipt=json.loads((copy/'root/REPLAY_RECEIPTS.json').read_text())
expected=['root/isotope_renewal.py','workers/physical_path/calculate.py','workers/scientific_operation/verify_operation.py','workers/foundational_math/verify_phase_clock.py','workers/foundational_math/verify_hidden_spectrum.py','workers/foundational_math/search_partial_injections.py','workers/abelian_sampler_audit/exact_audit.py','workers/capital_routes/n610_ring_benchmark.py']
need([x['script'] for x in receipt['results']]==expected and receipt['all_passed'],'suite selection/status changed')
for ref in receipt['results']:
 need(ref['status']=='PASS' and ref['exit_code']==0 and sha(package/ref['script'])==ref['sha256'],'source script/exit mismatch')
 for field in ['stdout','stderr']:need((copy/ref[field]).is_file(),'suite log missing')
calculation_copy=Path(receipt['disposable_copy']).resolve();need(calculation_copy.is_relative_to(OUT/'tmp'),'underlying calculation copy escaped authorized scratch')
hnf=calculation_copy/'workers/abelian_sampler_audit/hnf_audit.py';need(sha(hnf)==sha(package/'workers/abelian_sampler_audit/hnf_audit.py'),'HNF code differs')
hnfstart=time.monotonic();hcmd=[str(PYTHON),'-B',str(hnf)];hrun=subprocess.run(hcmd,cwd=hnf.parent,capture_output=True,text=True,timeout=180,env=env)
(OUT/'hnf.stdout.txt').write_text(hrun.stdout);(OUT/'hnf.stderr.txt').write_text(hrun.stderr)
need(hrun.returncode==0,'copied HNF audit failed')
hdata=json.loads((hnf.parent/'hnf_results.json').read_text());adata=json.loads((hnf.parent/'on_access_results.json').read_text())
need(hdata['membership_mismatches']==0 and hdata['uniform_pushforward_mismatches']==0,'HNF finite checks failed')
need(adata['duplicate_parent_query_fixed'] is True,'local-access accounting contract missing')
shutil.copyfile(hnf.parent/'hnf_results.json',OUT/'hnf_results.json');shutil.copyfile(hnf.parent/'on_access_results.json',OUT/'on_access_results.json')
after=snapshot();changed=[name for name in sorted(set(before)|set(after)) if before.get(name)!=after.get(name)]
need(not changed and git('status','--porcelain')==b'','original checkout changed during copy replay')
result={'schema':'astra.late-pr92.copy-only-replay.v1','status':'PASS','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_revision':'b7cada92d2eb304578be5ed974f1e44b10a89928','pr92_head':PIN,'runtime':runtime,'scope':'Authorized eight bounded synthetic/model/arithmetic scripts plus exact HNF/local-access audit in a complete external copy; no mathematical, physical, novelty, or practical-speed certification.','original_input_files':len(before),'original_inputs_unchanged':True,'changed_original_paths':changed,'original_hash_manifest':{'path':'ORIGINAL_INPUTS.json','sha256':sha(OUT/'ORIGINAL_INPUTS.json')},'whole_package_copy_items':len(copy_initial),'whole_package_copy_initial_hash_manifest':{'path':'COPY_INITIAL_HASHES.json','sha256':sha(OUT/'COPY_INITIAL_HASHES.json')},'original_runner_sha256':sha(package/'root/replay_selected.py'),'copied_runner_sha256':sha(copy/'root/replay_selected.py'),'suite_command':command,'suite_exit_code':run.returncode,'suite_reported_elapsed_wall_seconds':receipt['elapsed_wall_seconds'],'suite_results':receipt['results'],'suite_receipt_copy':{'path':str((copy/'root/REPLAY_RECEIPTS.json').relative_to(OUT)),'sha256':sha(copy/'root/REPLAY_RECEIPTS.json')},'hnf_command':hcmd,'hnf_exit_code':hrun.returncode,'hnf_elapsed_wall_seconds':time.monotonic()-hnfstart,'hnf_group_extension_cases':hdata['group_extension_cases'],'hnf_membership_comparisons':hdata['membership_comparisons'],'all_selected_checks':9,'total_elapsed_wall_seconds_including_after_hashes':time.monotonic()-start,'log_hashes':{name:sha(OUT/name) for name in ['suite.stdout.txt','suite.stderr.txt','hnf.stdout.txt','hnf.stderr.txt']},'source_mutation_warning':'Original runner writes its own logs/receipt; it was executed only after complete outside-checkout copying. Original runner and all package files retained byte-identical.'}
(OUT/'RECEIPT.json').write_bytes(encoded(result));print(json.dumps({k:v for k,v in result.items() if k not in ('suite_results','log_hashes')},indent=2))
