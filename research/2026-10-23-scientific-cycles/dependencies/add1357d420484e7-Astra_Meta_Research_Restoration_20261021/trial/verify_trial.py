#!/usr/bin/env python3
"""Replay exact fixtures and frozen-input bindings; not an automated proof grader."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def mat(a):
    return [[F(x) for x in row] for row in a]

def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def rank(a):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        scale = a[r][j]
        a[r] = [x / scale for x in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r

prereg = json.loads((ROOT/"PREREGISTRATION.json").read_text())
for name, expected in prereg["inputs"].items():
    data = (ROOT/name).read_bytes()
    assert len(data) == expected["bytes"]
    assert hashlib.sha256(data).hexdigest() == expected["sha256"]
T = mat([[1,0],[1,0],[0,1]])
bad = mat([[1,-1,0]])
good = mat([[1,0,0],[0,0,1]])
A = mat([[1,1,0],[0,0,1]])
assert rank(mul(bad,T)) == 0
assert mul(good,T) == mat([[1,0],[0,1]])
H = A+good
AT = mul(A,T)
M = [h+d for h,d in zip(H,AT+mat([[0,0],[0,0]]))]
assert rank(H) == 3 and rank(M) == 4
B = mat([[0],[-2],[0]])
theta = mat([[1],[0]])
mix = [[b[0]+t[0]] for b,t in zip(B,mul(T,theta))]
assert mul(A,mix) == mat([[0],[0]])
assert mul(good,B) == mat([[0],[0]])
gain = lambda alpha: 2*alpha*F(1,8)-alpha*alpha
assert gain(F(1,2)) == -F(1,8)
assert gain(F(1,8)) == F(1,64)
c = mat([[3],[4]])
Q = mat([[F(16,25),-F(12,25)],[-F(12,25),F(9,25)]])
assert mul(Q,Q) == Q
assert mul(Q,c) == mat([[0],[0]])
assert Q[0][0]+Q[1][1] == 1
names = [f"{arm}_{stage}.txt" for arm in "abc"
         for stage in ("stage1","stage2_warm","stage2_fresh")]
outputs = []
for name in names:
    p = ROOT/"outputs"/name
    text = p.read_text()
    assert text.strip()
    # Whitespace words are only a format check, not token or computation cost.
    words = len(text.split())
    assert words <= 1200, (name,words)
    outputs.append({"file":name,"bytes":p.stat().st_size,"whitespace_words":words,
                    "sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
result = {
    "status":"PASS",
    "scope":"Frozen input hashes, exact fixture arithmetic, output presence and length. Human mathematical assessment is separate.",
    "rank_deficient_example":{"nuisance_rank":rank(H),"full_rank":rank(M),"theta_dimension":2},
    "outputs":outputs,
    "capital_bytes":{"full":21005,"seed":1901,"no_capital_instruction":108},
    "source_byte_reduction":1-1901/21005,
    "cost_limit":"No model-token, reasoning-time, seed-construction or end-to-end resource advantage was measured.",
}
print(json.dumps(result,indent=2))
