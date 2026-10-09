#!/usr/bin/env python3
"""Authorized post-freeze reconstruction; no classification addendum read."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
import sympy as s

Q = s.Rational
workspace = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
sources = [workspace / 'work/agents/variance_monogamy_sol/cycle06_kms_entropy/BASELINE_STRONG_C4.txt',
           workspace / 'work/agents/root_cycle06/KMS_C4_FIXED_STATE_CERTIFICATE.txt',
           workspace / 'work/agents/root_cycle06/replay_kms_c4_root.py']
source_hashes = {str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sources}
copy = out / 'authorized_root_replay_audit_copy.py'
copy.write_bytes(sources[2].read_bytes())
started = time.perf_counter()
completed = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True, check=True)
wall = time.perf_counter() - started
interval = json.loads(completed.stdout)
assert all(x['negative_upper_bound_verified'] for x in interval['fixed_states'])

sigma = s.diag(1, 16) / 17
sqrt_sigma = s.diag(1, 4) / s.sqrt(17)
P = [s.Matrix([[9, 12], [12, 16]]) / 25, s.Matrix([[16, -12], [-12, 9]]) / 25]
pi = [s.Matrix([[9, 48], [48, 256]]) / 265, s.Matrix([[1, -3], [-3, 9]]) / 10]
probabilities = [Q(53, 85), Q(32, 85)]
assert P[0] + P[1] == s.eye(2)
for p, z, probability in zip(P, pi, probabilities):
    assert p * p == p and z * z == z and s.trace(z) == 1
    assert s.trace(sigma * p) == probability
    assert s.simplify(sqrt_sigma * p * sqrt_sigma - probability * z) == s.zeros(2)
assert probabilities[0] * pi[0] + probabilities[1] * pi[1] == sigma


def phi(a):
    return sum((z * s.trace(p * a) for p, z in zip(P, pi)), s.zeros(2))


def H(a):
    return sum((p * s.trace(z * a) for p, z in zip(P, pi)), s.zeros(2))


diagonal = s.diag(1, 2)


def T(a):
    return diagonal.inv() * phi(diagonal * a * diagonal) * diagonal.inv()


units = []
for i in range(2):
    for j in range(2):
        e = s.zeros(2)
        e[i, j] = 1
        units.append(e)
        assert s.simplify(sqrt_sigma * H(e) * sqrt_sigma
                          - phi(sqrt_sigma * e * sqrt_sigma)) == s.zeros(2)
matrix = s.Matrix([[s.trace(u.T * T(v)) for v in units] for u in units])
expected = s.Matrix([[Q(101, 1325), -Q(84, 1325), -Q(84, 1325), Q(306, 1325)],
                     [-Q(84, 1325), Q(306, 1325), Q(306, 1325), Q(21, 1325)],
                     [-Q(84, 1325), Q(306, 1325), Q(306, 1325), Q(21, 1325)],
                     [Q(306, 1325), Q(21, 1325), Q(21, 1325), Q(2497, 2650)]])
assert matrix == expected and matrix == matrix.T
assert matrix.eigenvals() == {1: 1, Q(1273, 2650): 1, 0: 2}
direction = s.Matrix([[-4, 1], [1, 4]]) / 17
log_derivative = s.Matrix([[-4, Q(4, 15) * s.log(2)],
                           [Q(4, 15) * s.log(2), Q(1, 4)]])
root_derivative = s.Matrix([[-2, Q(1, 5)], [Q(1, 5), Q(1, 2)]]) / s.sqrt(17)
J2 = s.expand(s.trace((direction - phi(direction)) * log_derivative))
E2 = s.simplify(s.trace(root_derivative * (root_derivative - T(root_derivative))))
assert J2 == Q(2559, 2650) - Q(8, 337875) * s.log(2)
assert E2 == Q(1088273, 4505000)
assert s.expand(J2 - 4 * E2) == -Q(349, 563125) - Q(8, 337875) * s.log(2)

result = {
    'status': 'PASS_INTERNAL_CROSS_AUDIT',
    'sources': source_hashes,
    'independent_sympy_reconstruction': 'channel/posterior/KMS/full T spectrum/Hessian all exact',
    'root_interval_replay_exit': completed.returncode,
    'root_interval_replay_wall_seconds': wall,
    'fixed_states_certified': len(interval['fixed_states']),
    'writes': 'owned audit copy and its JSON only; source files untouched',
    'classification_addendum_read': False,
    'prior_inline_metadata_attempt': 'All algebra and interval checks passed, then metadata assembly raised AttributeError from a reused variable. This saved-script invocation repairs metadata, not mathematics.'
}
(out / 'EXPOSURE_AUDIT_METADATA.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
