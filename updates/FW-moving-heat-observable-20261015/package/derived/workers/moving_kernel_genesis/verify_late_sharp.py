#!/usr/bin/env python3
"""Replay the newly supplied frozen sharp certificate without editing its lane.

The author's exact verifier is copied byte-for-byte here and called on the
author's JSON. Its output receipt is consequently local to this directory.
This is an exact replay and a dependency receipt, not independent discovery.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent/'sharp_boundary_qc'
EXPECTED={
    'SHARP_ACOUSTIC_HEAT_CERTIFICATE.json':'2adcc075976981aab4533fbaf16830e2fd6a99b86e0aa16b7d0fd65226674863',
    'verify_sharp_certificate.py':'e6cee5ed72f5e2c4e11cf2a9d0338d861d1fdaafca6345910b8b5586f5b030bd'
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name,digest in EXPECTED.items():
        assert sha(AUTHOR/name)==digest, name
    snapshot=HERE/'sharp_verifier_snapshot.py'
    snapshot.write_bytes((AUTHOR/'verify_sharp_certificate.py').read_bytes())
    assert sha(snapshot)==EXPECTED['verify_sharp_certificate.py']
    subprocess.run([sys.executable,str(snapshot),str(AUTHOR/'SHARP_ACOUSTIC_HEAT_CERTIFICATE.json')],check=True)
    for name,digest in EXPECTED.items():
        assert sha(AUTHOR/name)==digest, name
    replay=json.loads((HERE/'SHARP_VERIFICATION.json').read_text())
    assert replay['status']=='PASS' and replay['positive_rational_pivots']==72
    receipt={
        'status':'EXACT_REPLAY_PASS','author_directory':str(AUTHOR),
        'frozen_inputs':EXPECTED,'author_report_sha256':sha(AUTHOR/'REPORT.txt'),
        'snapshot_byte_identical':True,'source_inputs_unchanged':True,
        'checked_interval':['-21/8','-5/2'],
        'author_analytic_heat_argument_read':True,
        'analytic_scope_review':'Heat relative energy, closed-form Stokes, Gaussian decay, strong W1,4 passage and periodic argument reconstruct as written.',
        'scope':'Exact replay plus this lane analytic reading; not independent external review or priority clearance.'
    }
    (HERE/'LATE_SHARP_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('EXACT_REPLAY_PASS: frozen sharp certificate; independent analytic reading recorded')


if __name__=='__main__':
    main()
