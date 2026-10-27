"""Selected fresh NONPHYSICAL software replay; no physical/IID acquisition."""
from pathlib import Path
import hashlib,json,platform,resource,subprocess,sys,time
R=Path(__file__).resolve().parent
source_sha=hashlib.sha256((R/'photon_certificate.py').read_bytes()).hexdigest()
review=json.loads((R/'REVIEW_BINDING.json').read_text());assert source_sha==review['final_reader_sha256']
# Explicitly invalid NONPHYSICAL stream, not a qualified/generated experiment.
base=(R/'NONPHYSICAL_TINY.jsonl').read_bytes();extra=b'{"kind":"block","index":2,"bright_a":[],"bright_b":[],"dark":[]}\n'
(R/'NONPHYSICAL_INVALID_EXTRA.jsonl').write_bytes(base+extra)
commands=[(['photon_certificate.py','NONPHYSICAL_TINY.jsonl','-o','NONPHYSICAL_TINY_RESULT.json'],0),
          (['photon_certificate.py','NONPHYSICAL_INVALID_EXTRA.jsonl','-o','NONPHYSICAL_INVALID_RESULT.json'],2),
          (['-m','unittest','-v','test_reader.py'],0)]
receipts=[]
for args,expected in commands:
 before=resource.getrusage(resource.RUSAGE_CHILDREN);started=time.perf_counter()
 p=subprocess.run([sys.executable,*args],cwd=R,capture_output=True)
 after=resource.getrusage(resource.RUSAGE_CHILDREN)
 receipt={'command':[sys.executable,*args],'expected_exit':expected,'actual_exit':p.returncode,
          'wall_seconds':time.perf_counter()-started,'user_cpu_seconds':after.ru_utime-before.ru_utime,
          'system_cpu_seconds':after.ru_stime-before.ru_stime,
          'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
 receipts.append(receipt)
 if args[0]=='-m':(R/'SOFTWARE_TEST_LOG.txt').write_bytes(p.stdout+p.stderr)
 if p.returncode!=expected:raise RuntimeError(p.stderr.decode(errors='replace'))
tiny=json.loads((R/'NONPHYSICAL_TINY_RESULT.json').read_text());invalid=json.loads((R/'NONPHYSICAL_INVALID_RESULT.json').read_text());positive=json.loads((R/'NONPHYSICAL_POSITIVE_SOFTWARE_RESULT.json').read_text())
assert tiny['status']=='UNKNOWN' and invalid['status']=='INVALID_INPUT'
assert positive['status']=='CONDITIONAL_LOWER_BOUND' and not positive['physical_experiment_acquired_or_qualified']
assert all(d['data_kind']=='NONPHYSICAL_SOFTWARE_TEST' for d in (tiny,positive))
summary={'scope':'SELECTED_NONPHYSICAL_SOFTWARE_REPLAY_ONLY','reader_sha256':source_sha,'python':platform.python_version(),
 'fresh_processes':receipts,'total_selected_wall_seconds':sum(v['wall_seconds'] for v in receipts),
 'total_selected_child_cpu_seconds':sum(v['user_cpu_seconds']+v['system_cpu_seconds'] for v in receipts),
 'worker_tests':13,'all_selected_checks_passed':True,'independent_code_review_completed':True,
 'tiny_fixture':{'blocks':2,'clipped':tiny['blocks']['clipped_whole'],'coded_photons':sum(sum(v) for v in tiny['photon_counts_by_record_and_channel'].values()),'input_bytes':tiny['received_bytes']},
 'positive_software_fixture':{'blocks':4096,'coded_photons':sum(sum(v) for v in positive['photon_counts_by_record_and_channel'].values()),'input_bytes':positive['received_bytes'],'is_claimed_IID_or_physical':False},
 'measurement_boundary':'Selected startup/import/parsing/exact arithmetic/validation/serialization and tests, with ordinary warm OS caches. Excludes research, source review, interim debugging, external calibration/qualification and all physical acquisition.',
 'total_research_and_failed_work_time':'UNKNOWN/not comprehensively instrumented',
 'physical_source_or_experiment_acquired':False,'statistical_or_solver_advantage_claimed':False}
(R/'SOFTWARE_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='fresh_processes'},indent=2))
