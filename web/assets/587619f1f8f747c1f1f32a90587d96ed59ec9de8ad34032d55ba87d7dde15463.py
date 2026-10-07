#!/usr/bin/env python3
"""Run the finite diagnostics. Passing does not certify the research proofs."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work' if (ROOT / 'work').is_dir() else ROOT
SCRIPTS = [
    'frontier_algebra_checks.py', 'nonsofic_adversary_checks.py',
    'repetition_attack_check.py', 'frontier_physics/checks.py',
    'frontier_physics/exactification_checks.py',
    'pcp_bridge_checks.py', 'selective_tensor_checks.py',
    'unknown_field_checks.py', 'quantum_collision_checks/check_gaussian_periodic.py',
    'quantum_collision_checks/check_block_moments.py', 'frontier_tcs_checks.py',
    'frontier_geometry_checks.py', 'stability_rounding_counterexample.py',
    'acquisition_attack_check.py', 'frontier_analysis_check.py',
]

def run(name):
    source = WORK / name
    start = time.monotonic()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    result = subprocess.run([sys.executable, str(source)], cwd=WORK,
                            text=True, capture_output=True, env=env, timeout=900)
    record = dict(script=name, sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  returncode=result.returncode, seconds=round(time.monotonic()-start, 3),
                  stdout=result.stdout, stderr=result.stderr)
    print(f"{name}: {'PASS' if result.returncode == 0 else 'FAIL'}", flush=True)
    return record

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(run, SCRIPTS))
    obj = dict(scope='FINITE_DIAGNOSTICS_ONLY_NOT_PROOF_OR_EXTERNAL_VALIDATION',
               python=sys.version, passed=all(x['returncode']==0 for x in records),
               checks=records)
    (ROOT / 'replay_results.json').write_text(json.dumps(obj, indent=2)+'\n')
    sys.exit(0 if obj['passed'] else 1)
