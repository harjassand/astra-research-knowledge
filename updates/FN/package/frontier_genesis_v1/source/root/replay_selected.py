"""Copy-first independent root replay of selected campaign computations.

Runs immutable copies in a fresh temporary directory. Hashes and timings certify
only the listed executions, not novelty, physical outcomes or omitted proofs.
"""
from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
WORKER = 'workers/f_sol_quantum_dual/'
COPIES = [
    WORKER+'aklt_r3_obstruction.py', WORKER+'aklt_n6_interval.py',
    WORKER+'aklt_compact_gram.py',
    'root/knabe_response_baseline.py',
    'workers/f_luna_dual_construction/aklt_virtual_current_identity.py',
]
JOBS = [
    (WORKER+'aklt_r3_obstruction.py', [], WORKER+'aklt_r3_obstruction.json'),
    (WORKER+'aklt_n6_interval.py', [], WORKER+'aklt_n6_certified_interval.json'),
    (WORKER+'aklt_compact_gram.py', ['6'], WORKER+'aklt_compact_gram_n6.json'),
    (WORKER+'aklt_compact_gram.py', ['12'], WORKER+'aklt_compact_gram_n12.json'),
    ('root/knabe_response_baseline.py', [], 'root/knabe_response_baseline.json'),
    ('workers/f_luna_dual_construction/aklt_virtual_current_identity.py', [], None),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stable(value):
    if isinstance(value, dict):
        return {k:stable(v) for k,v in value.items() if k not in {'wall_seconds'}}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value

def main():
    output_dir=ROOT/'root/replay_outputs'
    output_dir.mkdir(exist_ok=True)
    receipt={'schema':'astra.frontier-genesis.root-replay.v1',
        'scope':'independent execution of copied code; finite exact arithmetic only',
        'python':sys.version,'platform':platform.platform(),
        'source_hashes':{p:digest(ROOT/p) for p in COPIES},'runs':[]}
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',
             MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='astra-frontier-replay-') as folder:
        replay=Path(folder)
        for p in COPIES:
            dest=replay/p
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/p,dest)
        for i,(script,args,expected) in enumerate(JOBS):
            started=time.monotonic()
            run=subprocess.run([sys.executable,str(replay/script),*args],
                cwd=replay,env=env,capture_output=True,text=True,timeout=300)
            seconds=time.monotonic()-started
            log=output_dir/f'{i:02d}-{Path(script).stem}-{args[0] if args else "default"}.txt'
            log.write_text(run.stdout+'\nSTDERR\n'+run.stderr)
            item={'script':script,'arguments':args,'exit_code':run.returncode,
                'wall_seconds':seconds,'output':str(log.relative_to(ROOT)),
                'output_sha256':digest(log)}
            assert run.returncode==0,(script,run.stderr)
            if expected:
                actual=json.loads((replay/expected).read_text())
                supplied=json.loads((ROOT/expected).read_text())
                item['expected_artifact']=expected
                item['expected_sha256']=digest(ROOT/expected)
                item['matches_saved_json_excluding_wall_seconds']=stable(actual)==stable(supplied)
                assert item['matches_saved_json_excluding_wall_seconds'],script
            receipt['runs'].append(item)
            print(json.dumps(item),flush=True)
    receipt['all_selected_replays_passed']=True
    receipt['not_replayed']=['N20 older RREF-only receipt',
        'N7-9 explicit-sector rank receipts','physical studies and raw data acquisition',
        'all-N feasibility (no proof exists)','independent external mathematics review']
    (ROOT/'root/REPLAY_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':
    main()
