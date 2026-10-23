"""Bind a conditional moment witness to independently pinned owner inputs.

This complements verify.py; it does not prove the polynomial inequalities.
The two hashes are from the received immutable owner archive, not the witness.
Usage: python bind_to_owner.py OWNER_ROOT WITNESS_DIR PROBE_INDEX
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys
import time
import numpy as np

started = time.perf_counter()
owner, packet, probe = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
assert 0 <= probe < 8
pinned = {
    'results/krylov_certificates.json': 'f156f7fbfb7dcd4975331f8099a2604a77bebf6463a59f055d81ad230e85264c',
    'results/input_construction.json': '7cde80f10d7a13b8d35d3f5f2a2c9bbb30ed70be7aa57da3fedaa18aaa59f121',
}
for rel, digest in pinned.items():
    assert hashlib.sha256((owner / rel).read_bytes()).hexdigest() == digest, rel
case = json.loads((owner / 'results/krylov_certificates.json').read_text())['64'][probe]
original = json.loads((owner / 'results/input_construction.json').read_text())
received = json.loads((packet / 'input.json').read_text())
def f(z):
    return F(int(z['numerator']), int(z['denominator']))
for key in ['diagonal_int', 'offdiagonal_int']:
    assert list(map(int, received['jacobi'][key])) == list(map(int, case['jacobi'][key]))
assert int(received['jacobi']['denominator']) == int(case['jacobi']['denominator']) == 2**32
with np.load(owner / 'witnesses/lanczos.npz') as z:
    assert list(map(int, z['diagonal'][probe, :64])) == list(map(int, received['jacobi']['diagonal_int']))
    assert list(map(int, z['offdiagonal'][probe, :63])) == list(map(int, received['jacobi']['offdiagonal_int']))
assert received['source_sha256'] == pinned
assert f(received['M']) == f(original['M'])
assert f(received['tau']) == f(original['tau'])
assert f(received['operator_error']) == f(case['residual']['operator_error'])
assert f(received['S']) == f(original['M']) + f(original['tau']) + f(case['residual']['operator_error'])
x = F(12983, 536870912)
assert f(received['x']) == x
up = json.loads((packet / 'maximum_witness.json').read_text())
near = json.loads((packet / 'near_infimum_witness.json').read_text())
for w, y in [(up, x), (near, x + F(1, 2**60))]:
    assert f(w['prescribed_node']) == y
    assert f(w['nodes'][1]['lower']) == f(w['nodes'][1]['upper']) == y
    assert f(w['nodes'][64]['lower']) == f(w['nodes'][64]['upper']) == f(received['S'])
    assert all(-f(received['S']) <= f(n['lower']) <= f(n['upper']) <= f(received['S']) for n in w['nodes'])
summary = json.loads((packet / 'summary.json').read_text())
def enclosure(outer, lower, upper):
    assert F(outer['lower']) <= lower <= upper <= F(outer['upper'])
enclosure(summary['infimum_inclusive'], F(up['nodes'][0]['weight_lower']), F(up['nodes'][0]['weight_upper']))
assert summary['infimum_inclusive']['attained'] is False
enclosure(summary['maximum_inclusive'], F(up['cdf_at_x']['lower']), F(up['cdf_at_x']['upper']))
enclosure(summary['extremal_width'], F(up['nodes'][1]['weight_lower']), F(up['nodes'][1]['weight_upper']))
enclosure(summary['concrete_witness_gap'], F(up['cdf_at_x']['lower']) - F(near['cdf_at_x']['upper']), F(up['cdf_at_x']['upper']) - F(near['cdf_at_x']['lower']))
print(json.dumps({'PASS': True, 'probe_index': probe, 'source_hashes_independently_pinned': pinned,
 'all_Jacobi_coefficients_and_NPZ_checked': True, 'support_threshold_and_endpoint_identities_checked': True,
 'summary_outward_consistency_checked': True, 'wall_seconds': time.perf_counter() - started,
 'scope': 'Input and summary binding; run verify.py for exact atomic facts and read RESULT.txt for the global dual proof.'}, indent=2))
