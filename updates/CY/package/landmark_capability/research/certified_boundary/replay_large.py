"""Replay the wide-rate 32-coordinate interval experiment, without enumeration."""
from fractions import Fraction as F
from pathlib import Path
import json
from solver import certified_boundary_resolvent

n = 32
result = certified_boundary_resolvent(
    [F(1, 2)] * n,
    [F(1, 1 << i) for i in range(n)],
    [F(i + 1, i + 3) for i in range(n)],
    [0, (1 << n) - 1], F(1, 1 << n), delta_bits=140, output_bits=48)
Path(__file__).with_name('wide_rate_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
h = result['hitting_laplace_transform']
assert h['lower'] == '112090338961471/281474976710656'
assert h['upper'] == '112090338961472/281474976710656'
print(json.dumps({'status':result['status'], 'seconds':result['elapsed_seconds'],
                  'nodes':result['quadrature']['positive_log_nodes'],
                  'lower':h['lower'], 'upper':h['upper']}, indent=2))
