"""Selected fresh-process replay with explicit measurement boundaries."""
import sys,json,time,subprocess,resource,platform,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
commands=[
 ['compiler.py','NONDEGRADED_INPUT.json','NONDEGRADED_COMPILED.json'],
 ['compiler.py','sources/H03_INPUT.json','H03_COMPILED.json'],
 ['verify_certificate.py','NONDEGRADED_COMPILED.json'],
 ['verify_certificate.py','H03_COMPILED.json'],
 ['verify_entropy_separation.py'],
 ['check_construction.py']]
records=[]
for args in commands:
    start=time.perf_counter();prior=resource.getrusage(resource.RUSAGE_CHILDREN)
    p=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
    used=resource.getrusage(resource.RUSAGE_CHILDREN)
    row={'command':[sys.executable,*args],'exit_code':p.returncode,
         'fresh_process_wall_s':time.perf_counter()-start,
         'child_user_cpu_s':used.ru_utime-prior.ru_utime,
         'child_system_cpu_s':used.ru_stime-prior.ru_stime,
         'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),
         'stderr':p.stderr}
    records.append(row)
    if p.returncode:
        print(p.stdout,p.stderr);raise RuntimeError('selected replay failed')
# Verify the accepted prior's actual byte provenance separately from science.
manifest=json.loads((root/'sources'/'SOURCE_MANIFEST.json').read_text())
for source in manifest:
    got=hashlib.sha256((root/'sources'/source['local']).read_bytes()).hexdigest()
    if got!=source['sha256']:raise RuntimeError('source bytes changed')
review=json.loads((root/'INDEPENDENT_REVIEW_SCOPE.json').read_text())
if hashlib.sha256((root/review['proof_file']).read_bytes()).hexdigest()!=review['proof_sha256']:
    raise RuntimeError('reviewed proof changed')
answer={'python':platform.python_version(),'selected_replays':records,
        'selected_total_fresh_process_wall_s':sum(v['fresh_process_wall_s'] for v in records),
        'selected_total_child_cpu_s':sum(v['child_user_cpu_s']+v['child_system_cpu_s'] for v in records),
        'accepted_prior_source_hashes_verified':True,'reviewed_proof_hash_verified':True,
        'measurement_scope':'Final selected processes only, including startup/import/input/checking/output serialization. Ordinary warm OS caches. Excludes research, source acquisition, failed work, prior package setup, physical calibration and real execution of a detector/controller.',
        'excluded_total_research_or_failed_cost':'UNKNOWN; see FAILED_RUNS.md',
        'strong_ordinary_advantage':'NOT_ESTABLISHED'}
(root/'FINAL_REPLAY.json').write_text(json.dumps(answer,indent=2)+'\n')
print(json.dumps({k:v for k,v in answer.items() if k!='selected_replays'},indent=2))
