#!/usr/bin/env python3
"""Exact N=4 transcription checks for the independent representation proof.

Writes only alongside this script. No bath simulation or asymptotic test.
"""
import itertools
import json
import math
import pathlib
import time
import sympy as s

ROOT = pathlib.Path(__file__).resolve().parent
t0 = time.monotonic()
N = 4
D = 2**N
I = s.eye(D)
Jminus = s.zeros(D)
Jz = s.zeros(D)
bits = list(itertools.product(range(2), repeat=N))
index = {a: i for i, a in enumerate(bits)}
for a, i in index.items():
    Jz[i, i] = s.Rational(sum(a)-N//2)
    for k in range(N):
        if a[k]:
            v = list(a)
            v[k] = 0
            Jminus[index[tuple(v)], i] += 1
Jplus = Jminus.T
J2 = Jz**2 + (Jplus*Jminus + Jminus*Jplus)/2
P = {
    2: J2*(J2-2*I)/24,
    1: -J2*(J2-6*I)/8,
    0: (J2-6*I)*(J2-2*I)/12,
}
perms = list(itertools.permutations(range(N)))
maps = [[index[tuple(a[p[k]] for k in range(N))] for a in bits] for p in perms]

def twirl(a):
    out = s.zeros(D)
    for perm in maps:
        for i in range(D):
            for k in range(D):
                if a[i, k]:
                    out[perm[i], perm[k]] += a[i, k]/math.factorial(N)
    return out.applyfunc(s.simplify)

def canonical(b, r):
    K = N-2*b
    v = s.zeros(D, 1)
    for a, i in index.items():
        sign = 1
        valid = sum(a[2*b:]) == r
        for k in range(b):
            p = a[2*k:2*k+2]
            if p == (0, 1):
                pass
            elif p == (1, 0):
                sign *= -1
            else:
                valid = False
        if valid:
            v[i] = sign
    norm = 2**b*math.comb(K, r)
    assert (v.T*v)[0] == norm
    return v, norm

def block(b, q):
    K, j = N-2*b, N//2-b
    db = math.comb(N, b)-(math.comb(N, b-1) if b else 0)
    Z = sum(q**r for r in range(K+1))
    seed = s.zeros(D)
    for r in range(K+1):
        v, norm = canonical(b, r)
        seed += q**r*(v*v.T)/norm/Z
    diag = s.diag(*[int(sum(a)-N//2+j == 0) if q == 0 else q**int(sum(a)-N//2+j) for a in bits])
    target = P[j]*diag/(db*Z)
    actual = twirl(seed)
    assert actual == target
    assert s.trace(actual) == 1
    assert P[j]*actual == actual
    return actual

checks = []
for b in range(3):
    K, j = N-2*b, N//2-b
    db = math.comb(N, b)-(math.comb(N, b-1) if b else 0)
    assert s.trace(P[j]) == (K+1)*db
    assert P[j]**2 == P[j]
    for r in range(K+1):
        v, norm = canonical(b, r)
        assert J2*v == j*(j+1)*v
        assert Jz*v == (r-j)*v
        if r:
            prev, prevnorm = canonical(b, r-1)
            assert Jminus*v == (K-r+1)*prev
    for q in [s.Rational(0), s.Rational(1, 3), s.Rational(1)]:
        rho = block(b, q)
        if q == 1:
            L = Jminus*rho*Jplus-(Jplus*Jminus*rho+rho*Jplus*Jminus)/2
            L += Jplus*rho*Jminus-(Jminus*Jplus*rho+rho*Jminus*Jplus)/2
        else:
            nu = q/(1-q)
            L = (nu+1)*(Jminus*rho*Jplus-(Jplus*Jminus*rho+rho*Jplus*Jminus)/2)
            L += nu*(Jplus*rho*Jminus-(Jminus*Jplus*rho+rho*Jminus*Jplus)/2)
        assert L == s.zeros(D)
        checks.append({"b": b, "j": j, "K": K, "multiplicity": db, "rank_isotypic": int(s.trace(P[j])), "q": str(q), "twirl_and_stationarity": "PASS"})
    if K:
        v0, n0 = canonical(b, 0)
        v1, n1 = canonical(b, 1)
        offdiag = twirl(v0*v1.T/s.sqrt(n0*n1))
        ground_diag = s.diag(*[int(sum(a)==b) for a in bits])
        target = P[j]*ground_diag*Jminus/(db*s.sqrt(K))
        assert offdiag == target
        checks.append({"b": b, "spin_coherence_0_1": "PASS"})

assert sum(P.values(), s.zeros(D)) == I
mixed = sum((s.Rational(int(s.trace(P[N//2-b])), D)*block(b, s.Rational(1)) for b in range(3)), s.zeros(D))
assert mixed == I/D
dark = sum((s.Rational(int(s.trace(P[N//2-b])), D)*block(b, s.Rational(0)) for b in range(3)), s.zeros(D))
E = Jz+N*I/2
beta = s.trace(dark*E)
emission = s.trace(dark*Jplus*Jminus)
assert beta == s.Rational(13, 16)
assert emission == 0
assert emission < beta**2/N

haar = []
for K in range(5):
    for r in range(K+1):
        beta_integral = s.Rational(math.factorial(r)*math.factorial(K-r), math.factorial(K+1))
        assert (K+1)*math.comb(K, r)*beta_integral == 1
        haar.append([K, r])

# Global-unitary invariance alone does not imply the two-producible upper bound.
# This four-qubit singlet is pure and entangled across every bipartition.
gme = s.zeros(D, 1)
for word, coefficient in {"0011": 2, "0101": 1, "0110": -3, "1001": -3, "1010": 1, "1100": 2}.items():
    gme[index[tuple(map(int, word))]] = coefficient
assert (gme.T*gme)[0] == 28
assert J2*gme == s.zeros(D, 1)
assert Jminus*gme == s.zeros(D, 1)
schmidt_ranks = []
for size in [1, 2]:
    for left in itertools.combinations(range(N), size):
        if size == 2 and 0 not in left:
            continue
        right = tuple(i for i in range(N) if i not in left)
        mat = s.zeros(2**size, 2**(N-size))
        for a, i in index.items():
            li = sum(a[v]*2**(size-1-k) for k, v in enumerate(left))
            ri = sum(a[v]*2**(N-size-1-k) for k, v in enumerate(right))
            mat[li, ri] = gme[i]
        rank = mat.rank()
        assert rank == (2 if size == 1 else 4)
        schmidt_ranks.append({"cut": list(left), "rank": rank})
assert twirl(gme*gme.T/28) != gme*gme.T/28

result = {
    "scope": "Exact N=4 matrices; finite transcription evidence, not the general proof",
    "thermal_q_tests": ["0", "1/3", "1 (formal infinite-temperature endpoint)"],
    "block_checks": checks,
    "haar_beta_coefficients": len(haar),
    "maximally_mixed_q1_recovery": "PASS",
    "maximally_mixed_q0_nonsep_witness": {"E": str(beta), "R": str(emission), "SEP_lower_R": str(beta**2/N)},
    "non_PI_pure_dark_GME_counterexample": {"norm_squared": 28, "schmidt_ranks": schmidt_ranks, "status": "PASS"},
    "seconds": time.monotonic()-t0,
    "status": "PASS",
}
(ROOT/"qubit_stationary_check.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "seconds": result["seconds"], "block_checks": len(checks), "haar_coefficients": len(haar)}))
