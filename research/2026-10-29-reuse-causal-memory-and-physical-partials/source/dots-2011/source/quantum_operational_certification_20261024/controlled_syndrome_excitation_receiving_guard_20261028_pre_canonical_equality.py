#!/usr/bin/env python3
"""Receiving-only symbolic scope guard and preserved wrong-frame counterexample.

No source outcomes, random draws, production tomography or decoder synthesis.
The pre-existing independent physical-channel check is replayed in a temporary
directory so that all author and earlier independent files remain untouched.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import sympy as s

ROOT = Path(__file__).resolve().parent
ES = [0, 4, 2, 1]
p, t = s.symbols('p t', real=True)
w = [p**f.bit_count() * (1-p)**(3-f.bit_count()) for f in range(8)]
ai = [s.expand(sum(w[e ^ g] for e in ES)/4) for g in ES]
ax = [s.expand(sum(w[e ^ g ^ 7] for e in ES)/4) for g in ES]
hz = [s.factor(a-b) for a,b in zip(ai,ax)]
assert all(s.expand(a+b-s.Rational(1,4)) == 0 for a,b in zip(ai,ax))
hz_t = [s.factor(v.subs(p,(1-t)/2)) for v in hz]
assert hz_t == [t*(3-t*t)/8] + [t*(1+t*t)/8]*3
# Explicit nonnegative factorization on t in [0,1], not an inference from samples.
assert s.expand(hz_t[0]-hz_t[1]) == t*(1-t*t)/4
assert s.expand(sum(ax)-(3*p-3*p*p+2*p**3)/2) == 0

# Native deterministic X1 is an exactly correctable isometric channel.  However,
# adding the uniform injection does NOT preserve nonnegative H_Z in this world.
det_w = [int(f == 4) for f in range(8)]
det_ai = [s.Rational(sum(det_w[e ^ g] for e in ES),4) for g in ES]
det_ax = [s.Rational(sum(det_w[e ^ g ^ 7] for e in ES),4) for g in ES]
det_hz = [a-b for a,b in zip(det_ai,det_ax)]
assert det_hz == [s.Rational(1,4),s.Rational(1,4),-s.Rational(1,4),-s.Rational(1,4)]
X = s.Matrix([[0,1],[1,0]])
Z = s.diag(1,-1)
U = s.zeros(8)
for l in range(2):
    for g,e in enumerate(ES):
        U[(7*l)^e,4*l+g] = 1
F = s.zeros(8)
for l in range(2):
    for g in range(4):
        F[4*(l ^ int(g >= 2))+g,4*l+g] = 1
U_wrong = U*F
BX = U*s.kronecker_product(X,s.eye(4))*U.H
BZ_wrong = U*s.kronecker_product(Z,s.diag(1,1,-1,-1))*U.H
assert U_wrong*s.kronecker_product(X,s.eye(4))*U_wrong.H == BX
assert U_wrong*s.kronecker_product(Z,s.eye(4))*U_wrong.H == BZ_wrong
assert BX*BZ_wrong+BZ_wrong*BX == s.zeros(8)
matrix_units_checked = 0
for g in [1,2]:
    G = s.zeros(4); G[g,g] = 1
    for a in range(2):
        for b in range(2):
            E=s.zeros(2); E[a,b]=1
            physical=U*s.kronecker_product(E,G)*U.H
            mid=U_wrong.H*physical*U_wrong
            decoded=s.Matrix(2,2,lambda i,j:sum(mid[4*i+h,4*j+h] for h in range(4)))
            expected=E if g==1 else X*E*X
            assert decoded==expected
            matrix_units_checked += 1

dependencies = [
    'ordinary_controlled_syndrome_excitation_witness_20261028.json',
    'ordinary_margin_free_local_gap_acquisition_main_receipt_20261028.json',
    'ordinary_margin_free_local_gap_acquisition_statistics_receipt_20261028.json',
    'ordinary_acquired_patch_excitation_frozen_recovery_main_receipt_20261028.json',
]
bindings={}
for filename in dependencies:
    data=json.loads((ROOT/filename).read_text())
    for name,digest in data['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,(filename,name)
    bindings[filename]=len(data['sha256'])

script='controlled_syndrome_excitation_independent_check_20261028.py'
before={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        for name in [script,script.replace('.py','.json')]}
with tempfile.TemporaryDirectory(prefix='injection_receiving_') as tmp:
    target=Path(tmp)/script
    shutil.copyfile(ROOT/script,target)
    replay=subprocess.run([sys.executable,str(target)],capture_output=True,text=True,check=True)
    assert target.with_suffix('.json').read_bytes()==(ROOT/script.replace('.py','.json')).read_bytes()
for name,digest in before.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest

out={
    'status':'PASS_SYMBOLIC_INTERVAL_SCOPE_GUARD_AND_WRONG_FRAME_COUNTEREXAMPLE',
    'source_draws':0,'rng_draws':0,
    'symbolic_parameter_interval':'p in [0,1/2], equivalently t in [0,1]',
    'symbolic_signed_blocks':[str(v) for v in hz_t],
    'deterministic_X1_injected_HZ':[str(v) for v in det_hz],
    'counterexample_native_X1_loss':'0',
    'counterexample_later_X2_wrong_decoder_loss':'1',
    'counterexample_coherent_matrix_units':matrix_units_checked,
    'prior_independent_replay':'byte-identical JSON from temporary-directory replay',
    'dependency_direct_bindings_reverified':bindings,
    'dependency_direct_bindings_reverified_total':sum(bindings.values()),
    'author_or_prior_independent_files_modified':False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
