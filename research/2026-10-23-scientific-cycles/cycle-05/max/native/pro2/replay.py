#!/usr/bin/env python3
"""Verify archive payload identities and independently replay only NEW evidence."""
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path.cwd()/'new_receiving_output')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    output=args.out.resolve()
    if output == root or output in (root/'results',root/'verification'):
        raise ValueError('Choose a separate receiving output directory')
    output.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for item in manifest['files']:
        p=root/item['path']
        raw=p.read_bytes()
        assert len(raw)==item['bytes'], item['path']
        assert hashlib.sha256(raw).hexdigest()==item['sha256'], item['path']
    hashed=time.perf_counter()-started
    target=output/'independent_coordinate_result.json'
    t=time.perf_counter()
    proc=subprocess.run([sys.executable,str(root/'verification'/'independent_coordinate_check.py'),
                         str(root/'results'/'coordinate_operations.json'),'--output',str(target)],
                        text=True,capture_output=True)
    elapsed=time.perf_counter()-t
    (output/'checker_stdout.txt').write_text(proc.stdout)
    (output/'checker_stderr.txt').write_text(proc.stderr)
    if proc.returncode:
        raise RuntimeError('Independent checker failed; see receiving logs')
    checked=json.loads(target.read_text())
    assert checked['status']=='PASS'
    receipt=dict(status='PASS',checked_payloads=len(manifest['files']),
                 payload_hash_wall_seconds=hashed,checker_subprocess_wall_seconds=elapsed,
                 total_wall_seconds=time.perf_counter()-started,
                 original_results_overwritten=False,old_scientific_campaigns_replayed=False,
                 scope='New concrete-data independent check and transport/source identity only. Not historical priority or full-class four-query resolution.')
    (output/'receiving_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
