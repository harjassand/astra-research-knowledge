#!/usr/bin/env python3
"""Read/replay the universal sharp-negative proof and its cone interface.

Keeps the interval freeze byte-for-byte intact and writes only new local
snapshots/receipts. The author's verifier is not imported from discovery code.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent/'sharp_boundary_qc'
EXPECTED={
    'UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json':'f45149312e694f6080a179b77d322aceabf0d7c2a55ed60c5e102037e55f6ee7',
    'verify_universal.py':'61302f2f2f2c76d9b82a2bc561532a7c0219356b0b47f7f996a96ffeae13c046',
    'UNIVERSAL_REPORT.txt':'db2b42e895e4e01df8be72225e83600a040b6cff936d0df37a8d32a738a8e61b'
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    v1=json.loads((HERE/'FREEZE_v0001.json').read_text())
    for name,record in v1['files'].items():
        assert sha(HERE/name)==record['sha256'], name
    for name,digest in EXPECTED.items():
        assert sha(AUTHOR/name)==digest, name
    snapshot=HERE/'universal_verifier_snapshot.py'
    snapshot.write_bytes((AUTHOR/'verify_universal.py').read_bytes())
    assert sha(snapshot)==EXPECTED['verify_universal.py']
    subprocess.run([sys.executable,str(snapshot),str(AUTHOR/'UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json')],check=True)
    for name,digest in EXPECTED.items():
        assert sha(AUTHOR/name)==digest, name
    replay=json.loads((HERE/'UNIVERSAL_VERIFICATION.json').read_text())
    assert replay['status']=='PASS' and replay['positive_rational_pivots_whole_branch']==12

    # An explicit positive parametrization of the entire delta<0 two-LMI cone.
    r,lam,mu,nu=s.symbols('r lambda mu nu',real=True)
    al=lam*3*r/(8*(r+2))+nu
    be=lam*r*(r-1)/6
    ga=lam+mu
    de=lam*r
    P=s.Matrix([[6*be+de,de],[de,ga]])
    Q=s.Matrix([[8*al,de],[de,2*be+de]])
    vector=s.Matrix([r,1])
    vq=s.Matrix([3,r+2])
    assert all(s.cancel(v)==0 for v in P-lam*vector*vector.T-s.diag(0,mu))
    assert all(s.cancel(v)==0 for v in Q-lam*r/(3*(r+2))*vq*vq.T-s.diag(8*nu,0))
    assert s.cancel(P.det()-lam*mu*r*r)==0
    assert s.cancel(Q.det()-8*nu*lam*r*(r+2)/3)==0
    assert s.cancel((6*be+de)/de-r)==0
    assert s.cancel(de*de/(6*be+de)-lam)==0
    assert s.cancel(ga-de*de/(6*be+de)-mu)==0
    assert s.cancel(al-de*de/(8*(2*be+de))-nu)==0
    for name,record in v1['files'].items():
        assert sha(HERE/name)==record['sha256'], name

    receipt={
        'status':'EXACT_REPLAY_AND_INTERFACE_PASS',
        'universal_frozen_inputs':EXPECTED,
        'author_inputs_unchanged':True,'v0001_files_unchanged':True,
        'certificate_whole_branch_pivots':12,
        'cone_interface_exact_groups':8,
        'positive_parametrization':'F=lambda J_r+mu j^2+nu H, lambda>0,r<-2,mu,nu>=0',
        'consequence':'For delta<=0, QC iff ROC iff both P and Q are PSD.',
        'analytic_review':'For each fixed r<-2, the diffusion is strictly positive; closed polynomial primitive, rapid-decay Stokes, quartic heat decay, zero-time continuity, W1,4 density and periodic passage reconstruct as written.',
        'nonuniformity':'No bound uniform as r approaches -2 or -infinity is inferred.',
        'scope':'Local exact replay and analytic/cone review. External correctness, formal proof verification and priority remain unresolved.'
    }
    (HERE/'UNIVERSAL_INPUT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('EXACT_REPLAY_AND_INTERFACE_PASS: universal r<-2 certificate and full delta<0 cone completion')


if __name__=='__main__':
    main()
