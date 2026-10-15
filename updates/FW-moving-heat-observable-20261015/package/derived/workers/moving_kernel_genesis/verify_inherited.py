#!/usr/bin/env python3
"""Read-only reconstruction of the inherited exact inputs.

Writes receipts only in this worker directory.  The portable verifiers are
imported and called as functions, so their source-directory output paths are
never used.  Exact checks do not certify the analytic implication or priority.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import sympy as s

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
SOURCE = RESEARCH / 'sources/astra_compatible_heat_result'
WORKTREE = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-moving-heat-observable-20261015')
PIN = '33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    head = subprocess.check_output(['git', '-C', str(WORKTREE), 'rev-parse', 'HEAD'], text=True).strip()
    assert head == PIN
    original = WORKTREE / 'updates/FT-direction-transport-20261015/synthesis/nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json'
    incoming = SOURCE / 'MOVING_ACOUSTIC_CERTIFICATE.json'
    before = {str(path): sha(path) for path in [original, incoming]}
    rec = module('moving_genesis_reconstruct', SOURCE / 'reconstruct.py')
    data = json.loads(original.read_text())
    matrix = lambda value: s.Matrix([[s.Rational(v) for v in row] for row in value])
    assert rec.C == matrix(data['basis'])
    assert rec.S == matrix(data['reduced_gram'])
    assert rec.Q == matrix(data['gram'])
    assert rec.W == matrix(data['omega_coefficients'])
    assert [rec.D1, rec.D2] == [s.Rational(data['diffusion'][i][i]) for i in range(2)]
    old_receipt = rec.verify()
    check = module('moving_genesis_portable_check', SOURCE / 'verify_moving_acoustic.py')
    moving_receipt = check.verify(incoming)
    assert before == {str(path): sha(path) for path in [original, incoming]}
    assert subprocess.check_output(['git', '-C', str(WORKTREE), 'rev-parse', 'HEAD'], text=True).strip() == PIN
    receipt = {
        'status': 'EXACT_PASS', 'pinned_head': head,
        'sympy_version': s.__version__, 'input_sha256': before,
        'actual_N850_matrices_equal_incoming_reconstruction': True,
        'source_files_unchanged': True,
        'N850_reconstruction': old_receipt,
        'moving_family': moving_receipt,
        'scope': 'Exact arithmetic and input reconstruction; analytic proof and novelty are separate.'
    }
    (HERE / 'INHERITED_EXACT_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('EXACT_PASS: actual pinned N850 matrices, heat identity, moving interval certificate')


if __name__ == '__main__':
    main()
