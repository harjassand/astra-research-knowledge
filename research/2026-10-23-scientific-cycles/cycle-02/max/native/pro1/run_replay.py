#!/usr/bin/env python3
"""Replay only this checkpoint's two diagnostics and record observed resources."""
from pathlib import Path
import hashlib,json,platform,resource,subprocess,sys,time

root=Path(__file__).resolve().parent
out=root/'replay'
out.mkdir(exist_ok=True)
commands=[
    ('supplied_feedback_factorization',[sys.executable,str(root/'supplied_feedback/check_factorization.py')]),
    ('new_frontier_diagnostic',[sys.executable,str(root/'replay_frontier.py'),'--output',str(out/'replay_frontier.json')]),
]
records=[]
for name,cmd in commands:
    start=time.perf_counter()
    p=subprocess.run(cmd,capture_output=True,text=True,check=False)
    elapsed=time.perf_counter()-start
    (out/(name+'.txt')).write_text(p.stdout+p.stderr)
    records.append({'name':name,'command':cmd,'returncode':p.returncode,'wall_seconds':elapsed,
        'output_file':'replay/'+name+'.txt'})
    if p.returncode:
        raise SystemExit(p.stdout+p.stderr)
receipt={'status':'both_new_delta_diagnostics_passed','runs':records,
    'python':sys.version.split()[0],'machine':platform.machine(),
    'child_peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    'scope':'No old recurrence/tree-capacity replay. These diagnostics supplement the written proofs.',
    'unmetered':'Model inference, literature search energy, total scientific labor and monetary cost.',
    'source_hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (root/'replay_frontier.py',root/'supplied_feedback/check_factorization.py')}}
(root/'replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
