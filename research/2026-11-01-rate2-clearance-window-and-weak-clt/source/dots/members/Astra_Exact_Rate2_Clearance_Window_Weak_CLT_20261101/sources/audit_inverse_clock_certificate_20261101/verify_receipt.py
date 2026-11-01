#!/usr/bin/env python3
"""Verify independent receipt bindings and rerun its checks, without constructor imports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import independent_check as ic

ROOT=Path(__file__).resolve().parent
SNAP=ROOT/'frozen_scalar'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    bindings=json.loads((ROOT/'RECEIPT_BINDINGS.json').read_text())
    for item in bindings['files']:
        assert digest(ROOT/item['path'])==item['sha256'],item['path']
    manifest=json.loads((SNAP/'SCALAR_FREEZE.json').read_text())
    for item in manifest['files']:
        assert digest(SNAP/item['path'])==item['sha256'],item['path']
    addendum=json.loads((SNAP/'SUP_PRIMITIVE_ADDENDUM_FREEZE.json').read_text())
    assert digest(SNAP/addendum['file'])==addendum['sha256']
    results=[]
    for name in ('CERTIFICATE.json','CERTIFICATE_FINE.json'):
        results.append(ic.check(SNAP/name,SNAP/'validated_clock.py'))
    coarse=json.loads((SNAP/'CERTIFICATE.json').read_text())
    fine=json.loads((SNAP/'CERTIFICATE_FINE.json').read_text())
    assert ic.R(coarse['s_star_lower'])<=ic.R(fine['s_star_lower'])<=ic.R(fine['s_star_upper'])<=ic.R(coarse['s_star_upper'])
    test_run=subprocess.run([sys.executable,str(ROOT/'test_independent.py'),str(SNAP)],check=True,capture_output=True,text=True)
    tests=json.loads(test_run.stdout)
    print(json.dumps({'status':'PASS_INDEPENDENT_SCALAR_AND_DETERMINISTIC_COMPONENT_REVIEW',
      'receipt_bindings_sha256':digest(ROOT/'RECEIPT_BINDINGS.json'),'independent_tests':tests,
      'bound_files_verified':len(bindings['files']),'scalar_snapshot_files_verified':len(manifest['files']),
      'separate_addendum_hash_verified':True,'coarse_contains_fine':True,'replays':results,
      'stochastic_clearance_theorem_accepted':False},indent=2))

if __name__=='__main__':main()
