#!/usr/bin/env python3
"""Copy-first bounded FK replays. Requires NumPy, SciPy, SymPy, mpmath.

Only copied evidence may be overwritten. Searches/scans, primary downloads,
large producer campaigns and laboratory experiments are not silently rerun.
Finite algebra/model checks do not certify analytic proofs, novelty or hardware.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
JOBS={
 'moving':[
  'FK-sources/moving/verify_adaptive_affine.py',
  'FK-affine-audit/adversarial_check.py',
  'FK-regression-geometry/verify_examples.py',
  'FK-quartic-global/exact_resonant_profile.py',
  'FK-tangent-compatibility/verify_exact_moving_metric.py'],
 'thermal':[
  'FK-sources/thermal/checks.py',
  'FK-anchor-audit/exact_finite_audit.py',
  'FK-anchor-scaling/geometry_checks.py',
  'FK-anchor-scaling-correlated-source-delta/correlated_source_checks.py',
  'FK-anchor-prior/reconstruction/anchor_fourier_check.py',
  'FK-response-bounds/corrected_equal_information_witness.py',
  'FK-transition-acquisition/check_transition_protocol.py',
  'FK-local-response/exact_patch_checks.py',
  'FK-modular-response/finite_case.py',
  'FK-root/verify_thermal_transition.py',
  'FK-anchor-audit/delta/checks/exact_delta_checks.py'],
 'physical':[
  'FK-sources/physical/checks.py',
  'FK-defect-experiment/derive_quantities.py',
  'FK-reaction-control/code/reaction_control.py',
  'FK-repair-observable/exact_checks.py',
  'FK-physical-pivot/derive_gate.py']
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group',choices=list(JOBS),required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    a=parser.parse_args();out=a.output_dir.resolve()
    if out.is_relative_to(ROOT) or (out.exists() and any(out.iterdir())):
        raise ValueError('Use a new or empty owned output directory outside the checkout')
    out.mkdir(parents=True,exist_ok=True)
    def hashes():
        count=0
        for mf in ['SOURCE_MANIFEST.json','DERIVED_MANIFEST.json']:
            for row in json.loads((HERE/mf).read_text())['files']:
                p=ROOT/row['path']
                if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
                    raise ValueError('Published input drift: '+row['path'])
                count+=1
        return count
    count=hashes()
    for group in ['moving','thermal','physical']:
        shutil.copytree(HERE/'package'/group,out/'work/FK-sources'/group)
    for d in sorted((HERE/'synthesis').iterdir()):
        if d.is_dir():
            shutil.copytree(d,out/'work'/('FK-'+d.name.replace('_','-')),ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    rows=[]
    for i,relative in enumerate(JOBS[a.group]):
        command=[sys.executable,'-B',str(out/'work'/relative)]
        start=time.monotonic()
        try:
            p=subprocess.run(command,cwd=out,env=env,capture_output=True,text=True,timeout=180)
            code,stdout,stderr=p.returncode,p.stdout,p.stderr
        except subprocess.TimeoutExpired as e:
            code=124;stdout=e.stdout or '';stderr=e.stderr or ''
            if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
            if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
            stderr+='\nBounded replay exceeded180seconds.'
        log=out/(str(i)+'-'+Path(relative).stem+'.log')
        log.write_text(stdout+'\nSTDERR:\n'+stderr)
        rows.append(dict(command=command,exit_code=code,seconds=time.monotonic()-start,log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        if code:break
    assert hashes()==count
    status='PASS' if len(rows)==len(JOBS[a.group]) and all(x['exit_code']==0 for x in rows) else 'FAIL'
    receipt=dict(status=status,group=a.group,python=platform.python_version(),executable=sys.executable,
        checks=rows,expected_steps=len(JOBS[a.group]),published_inputs_hash_unchanged=True,hashed_original_and_derived_files=count,
        scope='21 bounded source/exact/finite-model software steps across3groups. Corrected aligned Euclidean witness is replayed; original incorrect initialization retained but not certified. Exact scripts do not verify analytic proofs; no searches,novelty,hardware,scalability or totalcost certification. Wall seconds exclude aggregate inference.')
    (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status=status,group=a.group,steps=len(rows),expected_steps=len(JOBS[a.group]))),flush=True)
    return 0 if status=='PASS' else 1


if __name__=='__main__':
    sys.exit(main())
