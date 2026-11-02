#!/usr/bin/env python3
"""Reproduce final exact proof checks and replay frozen original source upper."""
from pathlib import Path
import subprocess,sys,zipfile,tempfile,hashlib,shutil
BASE=Path(__file__).resolve().parent
EXPECTED='a339c1e31c60c27b0dfb77c13c725e19f04f8486a847e24e5f84ee2fe67e5a21'
def run(file,args=(),cwd=BASE):
    print('RUN',file,' '.join(map(str,args)),flush=True)
    subprocess.run([sys.executable,str(file),*map(str,args)],cwd=cwd,check=True)
run('verify_physical_exact.py')
run('verify_replica_exact.py')
run('verify_gram_k5.py')
archive=BASE/'preserved_original_cluster_baseline.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED
with tempfile.TemporaryDirectory(prefix='astra_previous_source_') as p:
    with zipfile.ZipFile(archive) as z:
        selected=[f for f in z.namelist() if f.endswith('/check_trial_upper.py') or f.endswith('/upper_trial_L4.json')]
        assert len(selected)==2,selected
        z.extractall(p,members=selected)
    project=Path(p)/'astra_independent_quantum_20261102'
    run('check_trial_upper.py',['upper_trial_L4.json'],cwd=project)
print('ALL FINAL SCIENTIFIC REPLAYS PASS')
