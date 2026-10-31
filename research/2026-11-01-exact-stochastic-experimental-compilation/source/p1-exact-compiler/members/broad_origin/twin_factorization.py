"""Learn a hidden symplectic product of ternary sets from finite samples.

Research diagnostic, not a quantum-device experiment. The samples are the Bell
law of paired Haar-random product qubits under a common unknown Clifford.
No full Hilbert-space arrays are built. All arithmetic is exact over F_2.
"""
import json
import math
import time
from itertools import combinations
import numpy as np


def mm(a, b):
    return (a @ b) & 1


def rref(a):
    a = a.copy().astype(np.uint8)
    row, pivots = 0, []
    for col in range(a.shape[1]):
        choices = np.flatnonzero(a[row:, col])
        if not len(choices):
            continue
        p = row + int(choices[0])
        a[[row, p]] = a[[p, row]]
        targets = np.flatnonzero(a[:, col])
        targets = targets[targets != row]
        a[targets] ^= a[row]
        pivots.append(col)
        row += 1
        if row == a.shape[0]:
            break
    return a, pivots


def nullspace(a):
    r, pivots = rref(a)
    free = [j for j in range(a.shape[1]) if j not in pivots]
    out = np.zeros((a.shape[1], len(free)), dtype=np.uint8)
    for k, j in enumerate(free):
        out[j, k] = 1
        for i, p in enumerate(pivots):
            out[p, k] = r[i, j]
    return out


def colbasis(a):
    _, p = rref(a)
    return a[:, p]


def rank(a):
    return len(rref(a)[1])


def symplectic_form(n):
    j = np.zeros((2*n, 2*n), dtype=np.uint8)
    for i in range(n):
        j[2*i, 2*i+1] = j[2*i+1, 2*i] = 1
    return j


def random_symplectic(n, rng):
    d = 2*n
    j, s = symplectic_form(n), np.eye(d, dtype=np.uint8)
    for _ in range(8*n*n):
        v = rng.integers(0, 2, d, dtype=np.uint8)
        transvection = np.eye(d, dtype=np.uint8) ^ np.outer(v, mm(v, j))
        s = mm(transvection, s)
    assert np.array_equal(mm(mm(s.T, j), s), j)
    return s


def decoder_transvections(s):
    """Emit an executable Clifford decoder as <=4n Pauli pi/4 rotations.

    A transvection v maps x to x + [v,x]v. Its physical Clifford is a
    pi/4 rotation about Pauli(v), realizable with O(n) elementary Clifford
    gates. Untracked Pauli phases change only within-factor frames.
    """
    d = s.shape[0]
    j = symplectic_form(d//2)
    current = s.copy()
    program = []

    def pairing(a,b):
        return int(mm(mm(a,j),b))

    def apply(v):
        nonlocal current
        t = np.eye(d,dtype=np.uint8) ^ np.outer(v,mm(v,j))
        current = mm(t,current)
        program.append(v.copy())

    for k in range(d//2):
        e, f = np.eye(d,dtype=np.uint8)[:,2*k:2*k+2].T
        a = current[:,2*k].copy()
        if not np.array_equal(a,e):
            if pairing(a,e):
                apply(a^e)
            else:
                candidates = [np.eye(d,dtype=np.uint8)[:,i] for i in range(2*k,d)]
                candidates += [x^y for x,y in combinations(candidates,2)]
                w = next(x for x in candidates if pairing(a,x) and pairing(e,x))
                apply(a^w)
                apply(w^e)
        b = current[:,2*k+1].copy()
        if not np.array_equal(b,f):
            if pairing(b,f):
                apply(b^f)
            else:
                w = e^f
                apply(b^w)
                apply(w^f)
    assert np.array_equal(current,np.eye(d,dtype=np.uint8))
    assert len(program)<=2*d
    return program


def sample_source(s, a, m, rng, corrupt=0.0):
    n = len(a)//2
    symbols = rng.integers(0, 3, (m, n))
    x = np.zeros((m, 2*n), dtype=np.uint8)
    x[:, 0::2] = symbols == 1
    x[:, 1::2] = symbols == 2
    y = mm(x, s.T) ^ a
    bad = rng.random(m) < corrupt
    y[bad] = rng.integers(0, 2, (bad.sum(), 2*n), dtype=np.uint8)
    return y, int(bad.sum())


def learn(y):
    m, d = y.shape
    n = d//2
    pairs = list(combinations(range(d), 2))
    features = np.column_stack([np.ones(m, dtype=np.uint8), y] +
                               [y[:, i] & y[:, k] for i, k in pairs])
    kernel = nullspace(features)
    if kernel.shape[1] != n:
        return None, {"kernel_dimension": kernel.shape[1], "reason": "wrong dimension"}
    j = symplectic_form(n)
    operators = []
    for z in kernel.T:
        polar = np.zeros((d, d), dtype=np.uint8)
        for value, (i, k) in zip(z[1+d:], pairs):
            polar[i, k] = polar[k, i] = value
        t = mm(j, polar)
        if not np.array_equal(mm(t, t), t):
            return None, {"kernel_dimension": n, "reason": "non-idempotent polar operator"}
        operators.append(t)
    for a in operators:
        for b in operators:
            if not np.array_equal(mm(a, b), mm(b, a)):
                return None, {"kernel_dimension": n, "reason": "noncommuting polar operators"}
    blocks = [np.eye(d, dtype=np.uint8)]
    for t in operators:
        refined = []
        for w in blocks:
            tw = mm(t, w)
            w0, w1 = mm(w, nullspace(tw)), colbasis(tw)
            if w0.shape[1]: refined.append(w0)
            if w1.shape[1]: refined.append(w1)
        blocks = refined
    if len(blocks) != n or any(w.shape[1] != 2 for w in blocks):
        return None, {"kernel_dimension": n, "reason": "wrong joint eigenspaces"}
    learned_s = np.column_stack(blocks)
    if not np.array_equal(mm(mm(learned_s.T, j), learned_s), j):
        return None, {"kernel_dimension": n, "reason": "not symplectic"}
    return blocks, {"kernel_dimension": n, "reason": "recovered"}


def run(n, seed, corruption=0.0, delta=0.01):
    rng = np.random.default_rng(seed)
    s = random_symplectic(n, rng)
    a = rng.integers(0, 2, 2*n, dtype=np.uint8)
    m = math.ceil(9*((2*n*n+1)*math.log(2)+math.log(1/delta)))
    y, faults = sample_source(s, a, m, rng, corruption)
    start = time.perf_counter()
    blocks, info = learn(y)
    elapsed = time.perf_counter()-start
    correct = blocks is not None and all(any(
        rank(np.column_stack([w, s[:, 2*i:2*i+2]])) == 2
        for i in range(n)) for w in blocks)
    program = decoder_transvections(np.column_stack(blocks)) if blocks is not None else []
    return {"n":n,"seed":seed,"samples":m,"pair_preparations":2*m,
            "corruption_probability":corruption,"faults":faults,
            "correct_factorization":correct,"decoder_pauli_rotations":len(program),
            "seconds":elapsed,**info}


if __name__ == "__main__":
    results = [run(n, seed) for n in (2,4,8,12) for seed in (7,19,31)]
    results += [run(8, seed, 0.02) for seed in (7,19,31)]
    print(json.dumps(results, indent=2))
