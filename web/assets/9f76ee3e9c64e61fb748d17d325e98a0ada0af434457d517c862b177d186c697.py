#!/usr/bin/env python3
"""Bounded numerical algebra check for c08_l03's 3D strain identities.

This checks finite-dimensional identities only. It does not test the normal
cocycle, Ruelle, ergodic decomposition, equality rigidity, or prior art.
"""
from math import atan2, cos, sin, sqrt
import random

rng = random.Random(20261007)

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A):
    return [list(row) for row in zip(*A)]

def frob2(A):
    return sum(x*x for row in A for x in row)

def close(a, b, tol=2e-10):
    return abs(a-b) <= tol * max(1.0, abs(a), abs(b))

# Relative to e=(1,0,0), every symmetric trace-zero S has block form
# [[q,b1,b2],[b1,B11,B12],[b2,B12,B22]], trace(B)=-q.
for _ in range(5000):
    q, b1, b2, a, c = [rng.uniform(-5.0, 5.0) for _ in range(5)]
    # B0 is trace-free [[a,c],[c,-a]], and B=B0-(q/2)I.
    B11, B22 = a-q/2, -a-q/2
    S = [[q,b1,b2],[b1,B11,c],[b2,c,B22]]
    s = sqrt(a*a+c*c)
    b2norm = b1*b1+b2*b2
    lhs, rhs = frob2(S), 2*s*s+1.5*q*q+2*b2norm
    assert close(lhs, rhs), (lhs, rhs)

    # Rotate the normal plane to diagonalize B0. The target diag(0,H,-H)
    # is a member of the orthogonal orbit; its squared residual must equal
    # 2(s-H)^2 + 3q^2/2 + 2|b|^2.
    H = rng.uniform(0.0, 5.0)
    theta = 0.5*atan2(c, a)
    R = [[cos(theta),-sin(theta)],[sin(theta),cos(theta)]]
    Q = [[1.0,0.0,0.0],[0.0,R[0][0],R[0][1]],[0.0,R[1][0],R[1][1]]]
    Sprime = matmul(transpose(Q), matmul(S,Q))
    residual = [[Sprime[i][j] - (0.0 if i == j == 0 else
                  H if i == j == 1 else -H if i == j == 2 else 0.0)
                 for j in range(3)] for i in range(3)]
    residual2 = frob2(residual)
    claimed2 = 2*(s-H)**2+1.5*q*q+2*b2norm
    assert close(residual2, claimed2), (residual2, claimed2)

# Verify the scalar rearrangement for a mixed U/Z sample. q and b vanish
# off U by convention; Z carries an independent |S|^2/2 term.
for _ in range(1000):
    n = 40
    U = [rng.random() > 0.25 for _ in range(n)]
    svals = [rng.uniform(0.0, 3.0) if U[i] else 0.0 for i in range(n)]
    qs = [rng.uniform(-2.0, 2.0) if U[i] else 0.0 for i in range(n)]
    bs2 = [rng.uniform(0.0, 2.0) if U[i] else 0.0 for i in range(n)]
    zS2 = [0.0 if U[i] else rng.uniform(0.0, 3.0) for i in range(n)]
    mean = lambda xs: sum(xs)/len(xs)
    Es, Es2 = mean(svals), mean([x*x for x in svals])
    H = rng.uniform(0.0, Es) if Es > 0 else 0.0
    work_density = (Es2 + .75*mean([q*q for q in qs]) + mean(bs2)
                    + .5*mean(zS2))
    Delta = work_density-H*H
    rhs = (Es2-Es*Es + 2*H*(Es-H) + (Es-H)**2
           + .75*mean([q*q for q in qs]) + mean(bs2) + .5*mean(zS2))
    assert close(Delta, rhs), (Delta, rhs)
    # The chosen-orbit bound is controlled by twice the exact deficit.
    local = mean([2*(svals[i]-H)**2 + 1.5*qs[i]**2 + 2*bs2[i]
                  if U[i] else 0.0 for i in range(n)])
    assert local <= 2*Delta + 2e-10*max(1.0,abs(Delta)), (local,2*Delta)

print("PASS: 5,000 block-strain/orbit identities and 1,000 mixed U/Z deficit/local-bound samples")
print("Scope: finite-dimensional algebra only; no analytic or dynamical proof is certified.")
