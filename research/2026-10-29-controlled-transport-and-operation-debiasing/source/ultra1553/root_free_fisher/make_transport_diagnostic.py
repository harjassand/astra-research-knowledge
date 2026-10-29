"""Use the SAME saved tall-reference release to test a zero-factor rejection.

This is a classical centered witness checking the dual transport, not a new
source, quantum separation, optimization or experimental result.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
producer = root.parent/'c_general_design'
source_bytes = (producer/'SOURCE.json').read_bytes()
certificate_bytes = (producer/'CERTIFICATE.json').read_bytes()
source = json.loads(source_bytes)
certificate = json.loads(certificate_bytes)
L = [[F(x) for x in row] for row in source['L']]
K = [[F(x) for x in row] for row in certificate['K']]
assert all(len(row) == 2 for row in L+K)
m = len(K)
mean = [sum(row)/2 for row in K]
delta = [row[0]-row[1] for row in K]
fisher = sum(d*d/p for d, p in zip(delta, mean))
assert fisher > 0
v = [-d/p for d, p in zip(delta, mean)]+[F(1)]
outer = [[a*b for b in v] for a in v]
zero = [[F(0)]*(m+1) for _ in range(m+1)]
def enc(matrix):
    return [[[str(x), '0'] for x in row] for row in matrix]
result = {
    'scope': 'mechanical dual-transport diagnostic on same stored L,K; c=0',
    'original_source_sha256': hashlib.sha256(source_bytes).hexdigest(),
    'original_certificate_sha256': hashlib.sha256(certificate_bytes).hexdigest(),
    'L': [[str(x) for x in row] for row in L],
    'K': [[str(x) for x in row] for row in K], 'c': '0',
    'epsilon': str(fisher/4), 'Y0': enc(outer), 'Y_Q': [enc(zero)],
    'Y_U_real': [enc(outer)], 'Y_U_imag': [enc(zero)],
}
(root/'TRANSPORT_DIAGNOSTIC.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': 'PROPOSED_SAME_RELEASE_ZERO_FACTOR_TRANSPORT',
                  'new_model_or_solver_runs': 0, 'actual_factor_test': '0'}))
