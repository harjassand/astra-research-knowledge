#!/usr/bin/env python3
"""Offline relocated replay of new metadata analysis only, preserving source."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile, time
ROOT=Path(__file__).resolve().parent
start=time.perf_counter()
source=ROOT/'external_self_improvement'
expected={n:json.loads((source/n).read_text()) for n in
          ('ROOT_LINEAGE_RESULTS.json','ROOT_SENSITIVITY_RESULTS.json')}
with tempfile.TemporaryDirectory(prefix='astra_cycle6_replay_') as scratch:
    target=Path(scratch)/'external_self_improvement';shutil.copytree(source,target)
    executed=[]
    for relative in ('analyze_lineages.py','analyze_sensitivity.py',
                     'verify_baseline_workspace.py','independent_review/check_common10.py'):
        result=subprocess.run([sys.executable,str(target/relative)],cwd=scratch,
                              text=True,capture_output=True,timeout=60)
        assert result.returncode==0, (relative,result.stdout[-2000:],result.stderr[-2000:])
        executed.append(relative)
    for name,value in expected.items():
        actual=json.loads((target/name).read_text())
        assert actual==value, ('Deterministic result mismatch',name)
    baseline=json.loads((target/'baseline_workspace_evidence/VERIFICATION.json').read_text())
    assert baseline['status']=='PASS'
print(json.dumps({'status':'PASS','calculations':executed,
                  'deterministic_result_files_equal':list(expected),
                  'baseline_observed_commands':baseline['child_pre_edit_observed_commands'],
                  'elapsed_seconds':time.perf_counter()-start,
                  'scope':'Historical metadata arithmetic and trace parsing; no model or owner science execution.'},indent=2))
