#!/usr/bin/env python3
"""Check the finite-window reflection witness for the reversible-output model.

The strict sign of the witness is enclosed with mpmath interval arithmetic.
The all-lag positivity statement is proved analytically in v2.txt; the scan
below is only a finite diagnostic for implementation errors.
"""

from math import ceil, exp, log, sqrt

import numpy as np
from mpmath import iv


iv.dps = 60

# Physical model: a=10, b=1/100 clockwise/counterclockwise rates on Z_10;
# L=1_{S=-} is an independent equilibrium telegraph with P(L=1)=1/10 and
# relaxation rate gamma=1/20.  The observed binary signal is 1-L(1-h).
a = iv.mpf(10)
b = iv.mpf(1) / 100
gamma = iv.mpf(1) / 20
r = iv.mpf(1) / 10
sqrt5 = iv.sqrt(5)
c1 = (1 + sqrt5) / 10
c3 = (1 - sqrt5) / 10
c5 = iv.mpf(1) / 10
alpha1 = (a + b) * (1 - (1 + sqrt5) / 4)
alpha3 = (a + b) * (1 - (1 - sqrt5) / 4)
alpha5 = 2 * (a + b)
omega1 = (a - b) * iv.sqrt(10 - 2 * sqrt5) / 4
omega3 = (a - b) * iv.sqrt(10 + 2 * sqrt5) / 4


def ch_iv(t):
    """Exact Fourier expression for Cov(h(X_0), h(X_t)), interval-evaluated."""
    return (
        2 * c1**2 * iv.exp(-alpha1 * t) * iv.cos(omega1 * t)
        + 2 * c3**2 * iv.exp(-alpha3 * t) * iv.cos(omega3 * t)
        + c5**2 * iv.exp(-alpha5 * t)
    )


def cy_iv(t):
    ch = ch_iv(t)
    cl = r * (1 - r) * iv.exp(-gamma * t)
    return r**2 * ch + cl * (iv.mpf(1) / 4 + ch)


# Six strictly positive sampling offsets s_i=i*d, d=3/25.  The weights sum
# to zero and have positive mass +1/2 and negative mass -1/2, so F has range 1.
d = iv.mpf(3) / 25
weights_num = [68, 248, 184, -5, -193, -302]
assert sum(weights_num) == 0
assert sum(x for x in weights_num if x > 0) == 500
assert -sum(x for x in weights_num if x < 0) == 500

q = iv.mpf(0)
for i, wi in enumerate(weights_num, start=1):
    for j, wj in enumerate(weights_num, start=1):
        q += iv.mpf(wi * wj) / 1_000_000 * cy_iv((i + j) * d)

delta = -q
T = 12 * d
linear_floor = 16 * delta / T
z = 4 * delta  # R=1 in the nonlinear midpoint bound.
root_z = iv.sqrt(z)
atanh_root_z = (iv.log(1 + root_z) - iv.log(1 - root_z)) / 2
nonlinear_floor = 4 * root_z * atanh_root_z / T

# Verify a convenient strict interval for the all-lag envelope cutoff.
t0 = iv.mpf(3) / 50
envelope_at_t0 = iv.exp(-alpha1 * t0) * (1 + iv.exp(gamma * t0) / 9)

# Build the 20-state row-generator and check the output-preserving reversal
# conjugacy J Q J = Q* (J is a proof symmetry, not a physical odd parity).
n_ring = 10
n_hidden = 2 * n_ring
Q = np.zeros((n_hidden, n_hidden), dtype=float)
pi = np.zeros(n_hidden, dtype=float)
obs = np.zeros(n_hidden, dtype=int)

def index(j, is_minus):
    return 2 * (j % n_ring) + int(is_minus)


for j in range(n_ring):
    h = int(j in (0, 1, 2, 8, 9))
    for is_minus in (0, 1):
        x = index(j, is_minus)
        pi[x] = (0.1 if is_minus else 0.9) / n_ring
        obs[x] = 1 - is_minus * (1 - h)
        Q[x, index(j + 1, is_minus)] += 10.0
        Q[x, index(j - 1, is_minus)] += 0.01
        if is_minus:
            Q[x, index(j, 0)] += 0.045
        else:
            Q[x, index(j, 1)] += 0.005
        Q[x, x] = -Q[x].sum()

Qstar = Q.T * pi[np.newaxis, :] / pi[:, np.newaxis]
perm = [index(-j, is_minus) for j in range(n_ring) for is_minus in (0, 1)]
JQJ = Q[np.ix_(perm, perm)]
adjoint_residual = float(np.max(np.abs(Qstar - JQJ)))
stationarity_residual = float(np.max(np.abs(pi @ Q)))

# Float spectral diagnostic for the reflected covariance matrix and all-lag
# covariance.  These checks do not replace the exact interval sign of q.
def ch_float(t):
    return (
        2 * float((1 + sqrt(5)) / 10) ** 2
        * exp(-float(alpha1.a) * t)
        * np.cos(float(omega1.a) * t)
        + 2 * float((1 - sqrt(5)) / 10) ** 2
        * exp(-float(alpha3.a) * t)
        * np.cos(float(omega3.a) * t)
        + 0.01 * exp(-20.02 * t)
    )


def cy_float(t):
    cl = 0.09 * exp(-0.05 * t)
    return 0.01 * ch_float(t) + cl * (0.25 + ch_float(t))


sample_times = [float(i * 3 / 25) for i in range(1, 7)]
H = np.array([[cy_float(s + t) for t in sample_times] for s in sample_times])
reflected_eigenvalues = np.linalg.eigvalsh(H)
scan_minimum, scan_time = min(
    (cy_float(t), t) for t in np.linspace(0.0, 100.0, 100_001)
)

# Hoeffding accounting: each block statistic F_- F_+ lies in [-1/4,1/4],
# a width-1/2 interval.  With confidence 1-alpha, epsilon_N is as below.
alpha_conf = 0.05
delta_estimate = 0.002348303028442996035313766063581556
N_for_positive_CI = ceil(log(2 / alpha_conf) / (8 * (delta_estimate / 2) ** 2))
N_for_half_gap = ceil(log(2 / alpha_conf) / (8 * (delta_estimate / 4) ** 2))

print(f"Cov(h0,ht) Fourier coefficients: c1={float(c1.a):.12g}, c3={float(c3.a):.12g}, c5=0.1")
print(f"alpha1={float(alpha1.a):.15g}, alpha3={float(alpha3.a):.15g}, alpha5=20.02")
print(f"omega1={float(omega1.a):.15g}, omega3={float(omega3.a):.15g}")
print(f"all-lag envelope F(0.06) interval={envelope_at_t0}")
print(f"reflected witness q interval={q}")
print(f"linear EPR floor={linear_floor} nats/time")
print(f"nonlinear EPR floor={nonlinear_floor} nats/time")
print(f"reflected covariance eigenvalues={reflected_eigenvalues}")
print(f"dense diagnostic min C_Y={scan_minimum:.12g} at t={scan_time:.6g}")
print(f"max |JQJ-Q*|={adjoint_residual:.3g}; max |pi Q|={stationarity_residual:.3g}")
print(f"ring EPR={(10-0.01)*log(1000):.12g} nats/time")
print(f"95% Hoeffding N for positive lower CI (design threshold)={N_for_positive_CI}")
print(f"95% Hoeffding N for at least half-gap lower CI={N_for_half_gap}")

assert float(q.b) < 0.0
assert float(envelope_at_t0.b) < 1.0
assert stationarity_residual < 1e-14
assert adjoint_residual < 1e-14
assert reflected_eigenvalues[0] < 0.0
assert scan_minimum > 0.0
assert 0.0 < float(nonlinear_floor.a) < (10 - 0.01) * log(1000)
