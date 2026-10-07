"""Small exact diagnostics for compiler building blocks, not the theorem."""
from fractions import Fraction as F
from pathlib import Path
import json
from compiler_primitives import (ceil_log2, determinant, is_psd,
                                 physical_round, survival_bracket,
                                 compiler_parameters)
count = 0
for num in range(1, 41):
    for den in range(1, 31):
        x = F(num, den)
        k = ceil_log2(x)
        p = F(1 << k) if k >= 0 else F(1, 1 << -k)
        assert p/2 < x <= p
        count += 1
# Squared Gram matrices and several indefinite/semidefinite boundaries.
fixtures = [([[0,0],[0,1]], True), ([[0,1],[1,1]],False),
            ([[1,2],[2,4]], True), ([[1,2],[2,3]],False),
            ([[-1,0],[0,2]], False)]
for a, expected in fixtures:
    assert is_psd(a) == expected
    count += 1
assert determinant([[0,2],[3,4]]) == -6; count += 1
assert determinant([[1,2],[2,4]]) == 0; count += 1
assert determinant([[2,1,0],[1,3,1],[0,1,4]]) == 18; count += 1
# One-mode pure squeezing r=log2 with eta=1/16: K diagonal rational.
k = [[F(3,32),F(0)],[F(0),F(-3,128)]]
for bits in (12,24,48,96):
    rounded = physical_round(k, bits)
    diff = [[rounded[i][j]-k[i][j] for j in range(2)] for i in range(2)]
    upper = [[F(4,1 << bits)*int(i==j)-diff[i][j] for j in range(2)] for i in range(2)]
    assert is_psd(diff) and is_psd(upper); count += 2
    for v in (F(0), F(1,7), F(1,2), F(7,8), F(1)):
        lo, hi = survival_bracket(k,v,bits)
        a = [[F(i==j)+(1-v)*k[i][j] for j in range(2)] for i in range(2)]
        det = determinant(a)
        assert lo*lo*det <= 1 <= hi*hi*det
        assert hi-lo == F(1,1 << bits)
        count += 2
# Non-diagonal physical-noise rounding: verify exact PSD order in dimension 4.
a = [[F(i+j+1, (i+1)*(j+1)+7) for j in range(4)] for i in range(4)]
for bits in (12,24,48,96):
    out = physical_round(a,bits)
    diff = [[out[i][j]-a[i][j] for j in range(4)] for i in range(4)]
    upper = [[F(8,1 << bits)*int(i==j)-diff[i][j] for j in range(4)] for i in range(4)]
    assert is_psd(diff) and is_psd(upper)
    count += 2
params=compiler_parameters(2,F(1,10),F(1,4))
assert params['count_cap']==440 and params['precision_bits']>10000
count += 1
out={"status":"PASS", "exact_assertions":count,
     "tested_precisions":[12,24,48,96], "example_schedule":params,
     "scope":"Exact primitive diagnostics only. No full high-precision sampler run, statistical TV validation, external review, or formal verification."}
path=Path(__file__).with_name('compiler_primitive_results.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
