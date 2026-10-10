#!/usr/bin/env python3
"""Exact one-state passive interpolation example and robust rank certificate."""

from fractions import Fraction as F
import numpy as np


nodes = [1, 2, 3, 4]
values = [F(3, 2), F(4, 3), F(5, 4), F(6, 5)]
eps = F(1, 100)  # 0.01 normalized-impedance radius on each specified sample
mu = nodes[:2]
lam = nodes[2:]
y_mu = values[:2]
y_lam = values[2:]

# Exact Loewner matrix at the interval centers.
Lq = [[(y_mu[i] - y_lam[j]) / F(mu[i] - lam[j]) for j in range(2)] for i in range(2)]
det = Lq[0][0] * Lq[1][1] - Lq[0][1] * Lq[1][0]
L = np.array([[float(x) for x in row] for row in Lq])
sv = np.linalg.svd(L, compute_uv=False)

# Each entry error is bounded by (eps_left+eps_right)/|mu-lambda|.
entry_error_bounds = [[2 * eps / abs(mu[i] - lam[j]) for j in range(2)] for i in range(2)]
delta_sq = sum(x * x for row in entry_error_bounds for x in row)
delta = float(delta_sq) ** 0.5
entry_lower_bound = abs(Lq[0][0])  # ||L0||_2 >= |e_1^T L0 e_1|

# Recover a degree <=1 real rational H(s)=(d*s+q)/(s+a) from centers.
# For every sample: y_i*a - d*s_i - q = -y_i*s_i.
def solve_fraction_system(matrix, rhs):
    """Gauss-Jordan elimination over exact rationals."""
    aug = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    n = len(aug)
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row != col:
                scale = aug[row][col]
                aug[row] = [aug[row][k] - scale * aug[col][k] for k in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


M = [[values[i], F(-nodes[i]), F(-1)] for i in range(3)]
b = [-values[i] * nodes[i] for i in range(3)]
a, d, q = solve_fraction_system(M, b)
r = q - d * a
predicted = [F(d * s + q, s + a) for s in nodes]
residuals = [predicted[i] - values[i] for i in range(4)]

# A different, arbitrarily higher-order strict PR impedance can share all four
# exact samples. For q_extra=1, r(s)=prod(s-i)/prod(s+a_k) with a_k=11,...,15.
# It vanishes at every sample; |r(s)|<=1/15 on Re(s)>=0, so H+r remains PR.
q_extra = 1
extra_denoms = list(range(11, 15 + q_extra))
def hidden_term(s):
    num = F(1)
    den = F(1)
    for i in nodes:
        num *= s - i
    for aa in extra_denoms:
        den *= s + aa
    return num / den
hidden_at_samples = [hidden_term(F(s)) for s in nodes]
hidden_bound = F(1, extra_denoms[-1])

# Positive-real one-pole form d + r/(s+a): d>=0, r>=0, a>0.
assert det == 0
assert entry_lower_bound * entry_lower_bound > delta_sq  # exact proof that every compatible L is nonzero
assert (a, d, q, r) == (F(1), F(1), F(2), F(1))
assert all(x == 0 for x in residuals)
assert d >= 0 and r >= 0 and a > 0
assert max(values) - min(values) > 2 * eps  # no constant can fit all intervals
assert hidden_at_samples == [F(0)] * 4
assert hidden_bound <= F(1, 15)

print(f"Loewner matrix exact: {Lq}")
print(f"Loewner determinant exact: {det}")
print(f"center singular values (diagnostic only): {sv.tolist()}")
print(f"exact squared Frobenius uncertainty bound: delta^2={delta_sq}")
print(f"exact robust state lower bound: ||L0||_2 >= |L0[0,0]|={entry_lower_bound}; its square exceeds delta^2, hence every compatible L has rank >=1")
print(f"recovered H(s)=(d*s+q)/(s+a): d={d}, q={q}, a={a}")
print(f"residue r=q-d*a={r}; PR signs d>=0, r>=0, a>0 hold")
print(f"exact interpolation residuals: {residuals}")
print("normalized passive compile: series R=1 plus (parallel R=1 || C=1), matching z(x)=1+1/(x+1)")
print("physical scale R0=1 kOhm, tau=1 ms: Rs=Rp=1 kOhm and C=tau/R0=1 uF")
print(f"tolerance: +/-{float(eps):.3g} normalized impedance per sample; 0-state lower bound also follows from endpoint spread")
print(f"non-uniqueness falsifier: H(s)+r(s), r(s)=prod_(i=1)^4(s-i)/prod_(a={extra_denoms[0]}^{extra_denoms[-1]})(s+a)")
print(f"alternate model has {1 + len(extra_denoms)} poles/states, the same four samples, and |r(s)|<={hidden_bound} on Re(s)>=0, so it remains strictly PR")
