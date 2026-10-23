#!/usr/bin/env python3
"""Verify this checkpoint and replay only its new, bounded finite checks."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=(args.output_dir or Path(tempfile.mkdtemp(prefix='astra_pro3_cycle4_'))).resolve()
    out.mkdir(parents=True,exist_ok=True)
    if out==root or root in out.parents:
        raise ValueError('Replay output must be outside the preserved source tree')
    t=time.perf_counter()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for f in manifest['files']:
        p=root/f['path']; data=p.read_bytes()
        assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],f['path']
    subprocess.run([sys.executable,str(root/'code/branching_checks.py'),
                    '--reserve','80','--output',str(out/'branching_80.json'),
                    '--exact-inputs',str(out/'exact_tree_inputs.json'),
                    '--resources',str(out/'branching_80_resources.json')],check=True)
    for name in ('branching_80.json','exact_tree_inputs.json'):
        assert (out/name).read_bytes()==(root/'evidence'/name).read_bytes(),name
    subprocess.run([sys.executable,str(root/'reviews/tree_lumping_exact_check.py'),
                    '--output',str(out/'tree_lumping_exact_check.json')],check=True)
    old=json.loads((root/'reviews/tree_lumping_exact_check.json').read_text())
    new=json.loads((out/'tree_lumping_exact_check.json').read_text())
    for x in (old,new):
        x.pop('wall_seconds',None);x.pop('cpu_seconds',None)
    assert old==new
    receipt=dict(status='passed',manifest_payloads=len(manifest['files']),
                 principal_result='byte-identical',exact_inputs='byte-identical',
                 independent_exact_check='identical excluding measured time',
                 historical_campaigns_replayed=0,
                 wall_seconds=time.perf_counter()-t,output_dir=str(out),
                 source_root=str(root),
                 limitation='Finite replay checks integrity and implementation, not the theorem')
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
