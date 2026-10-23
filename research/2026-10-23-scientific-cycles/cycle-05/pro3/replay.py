#!/usr/bin/env python3
"""Verify this source return and replay only its new exact diagnostic."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    started=time.perf_counter()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for item in manifest['files']:
        p=root/item['path']
        assert p.is_file(),item['path']
        assert p.stat().st_size==item['bytes'],item['path']
        assert digest(p)==item['sha256'],item['path']
    with tempfile.TemporaryDirectory(prefix='astra_cycle5_replay_') as tmp:
        out=Path(tmp)
        run=subprocess.run([sys.executable,str(root/'code/absorbed_checks.py'),
            '--output',str(out/'results.json'),'--inputs',str(out/'inputs.json'),
            '--resources',str(out/'resources.json')],check=True,capture_output=True,text=True)
        assert (out/'results.json').read_bytes()==(root/'evidence/ABSORBED_CHECKS.json').read_bytes()
        assert (out/'inputs.json').read_bytes()==(root/'evidence/EXACT_INPUTS.json').read_bytes()
        receipt={'status':'all manifest payloads verified; deterministic replay byte-identical',
                 'manifest_payloads':len(manifest['files']),
                 'results_sha256':digest(out/'results.json'),
                 'inputs_sha256':digest(out/'inputs.json'),
                 'replay_body':json.loads((out/'resources.json').read_text()),
                 'subprocess_stdout':run.stdout.strip(),
                 'replay_wall_seconds':time.perf_counter()-started,
                 'historical_campaigns_replayed':False,
                 'discovery_cost':'not measured by this replay; unknown'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))


if __name__=='__main__':
    main()
