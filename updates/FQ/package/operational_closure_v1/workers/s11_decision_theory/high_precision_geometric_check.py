"""Independent matrix-exponential check for the geometric path audit.

Requires mpmath. This is numerical cross-validation, not the proof.
"""

import mpmath as mp


mp.mp.dps = 60
q = mp.mpf(1) / 20
s = 1 + q
t = mp.mpf(3) / 10
pi = mp.mpf(1) / 3
Q = mp.matrix([[-s, 1, q], [q, -s, 1], [1, q, -s]])
G = mp.matrix([
    [-s, mp.sqrt(q), mp.sqrt(q)],
    [mp.sqrt(q), -s, mp.sqrt(q)],
    [mp.sqrt(q), mp.sqrt(q), -s],
])
B = mp.matrix([0, 1, 1])
P = mp.expm(t * Q)
a = mp.fsum(pi * P[i, j] for i in (1, 2) for j in (1, 2)) / (mp.mpf(2) / 3)
f = B - mp.matrix([a, a, a])
v = mp.expm(t * G) * f
e_nu_w = pi * (v[1] ** 2 + v[2] ** 2)
e_q_w = mp.fsum(
    pi * P[j, i] * P[i, k] * (B[j] - a) * (B[k] - a)
    for i in (1, 2) for j in range(3) for k in range(3)
)
affinity = mp.exp(-2 * t * (s - 2 * mp.sqrt(q)))
print("a", mp.nstr(a, 50))
print("E_Q W", mp.nstr(e_q_w, 50))
print("E_nu W", mp.nstr(e_nu_w, 50))
print("affinity", mp.nstr(affinity, 50))
print("lost mass times score minimum", mp.nstr(a * (1 - a) * (1 - affinity), 50))
assert e_q_w < 0 < e_nu_w
assert -e_q_w < a * (1 - a) * (1 - affinity)
