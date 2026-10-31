#!/usr/bin/env python3
"""Reproduce in disposable copies; never modify frozen source or reports."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path


def run():
    package=Path(__file__).resolve().parent
    source=package/'science'/'robust_operator_reuse_20261031'
    files=[p for p in package.rglob('*') if p.is_file()]
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    reports=[]
    with tempfile.TemporaryDirectory(prefix='robust-reuse-reproduce-') as td:
        td=Path(td);shadow=td/'science';shutil.copytree(source,shadow);out=td/'outputs';out.mkdir()
        scripts=['test_reuse.py','algebra_witness.py','check_barrier.py','strong_comparison.py','independent_reuse_checks.py',
                 'finite_observation/check_replay.py','finite_observation/risk_frontier.py','finite_observation/composition_check.py',
                 'finite_observation/independent_checks.py','finite_observation/mixing_baseline.py']
        stdout={}
        for script in scripts:
            tic=time.perf_counter()
            proc=subprocess.run([sys.executable,'-B',str(shadow/script)],cwd=out,text=True,capture_output=True,
                                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            if proc.returncode:raise RuntimeError(f'{script} failed:\n{proc.stdout}\n{proc.stderr}')
            stdout[script]=proc.stdout
            reports.append({'script':script,'exit_code':proc.returncode,'seconds':time.perf_counter()-tic,
                            'stdout_sha256':hashlib.sha256(proc.stdout.encode()).hexdigest()})
        expected=[('exact_author',json.loads((out/'tests_results.json').read_text())['checks'],167),
                  ('exact_independent',json.loads((shadow/'independent_reuse_checks.json').read_text())['checks'],150),
                  ('finite_author',json.loads((out/'replay_checks.json').read_text())['checks'],501),
                  ('frontier_author',json.loads((out/'risk_frontier_results.json').read_text())['checks'],4124),
                  ('composition_author',json.loads((out/'composition_results.json').read_text())['checks'],35),
                  ('finite_independent',json.loads(stdout['finite_observation/independent_checks.py'])['checks'],415),
                  ('mixing_author',json.loads((out/'mixing_baseline_results.json').read_text())['checks'],240)]
        for name,got,want in expected:assert got==want,(name,got,want)
        mixing=json.loads((out/'mixing_baseline_results.json').read_text())
        assert mixing['constant_lengths']==list(range(16,31))
        assert mixing['long_word_batch']['new_vector_products']==0
        composition=json.loads((out/'composition_results.json').read_text())
        assert composition['replay_rank']==7 and composition['logical_iid_draws']==15778976
    for p,digest in before.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest,p
    return {'passed':True,'test_counts':{name:got for name,got,want in expected},'total_counted_checks':sum(got for name,got,want in expected),
            'frozen_files_unchanged':len(before),'commands':reports,
            'scope':'Packaging reproduction, not an additional independent review or physical data validation.'}


if __name__=='__main__':print(json.dumps(run(),indent=2))
