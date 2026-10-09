"""Numerically check the midpoint Pinsker and copositive witness bounds."""
from math import atan, cos, exp, log, pi, sqrt

# Three-state binary ring: parent midpoint bound for a negative autocovariance.
a, b = 10.0, 1.0
s, d = a + b, a - b
alpha, omega = 1.5 * s, sqrt(3.0) * d / 2.0
phase = pi - atan(alpha / omega)
t = phase / omega
cov = (2.0 / 9.0) * exp(-alpha * t) * cos(omega * t)
ring_epr = d * log(a / b)
scalar_floor = 16.0 * (-cov) / t

# C5 reflection table and finite M-stage biased-ring realization.
c5 = 11.0 / 20.0
phi = (1.0 + sqrt(5.0)) / 2.0
normalizer = 5.0 * (1.0 + 2.0 * c5)
M, eps = 50000, 1.0e-4
eta = sqrt(M + 2.0) / M + eps
min_eig = (1.0 - phi * c5) / normalizer
horn_margin = (2.0 * c5 - 1.0) / (1.0 + 2.0 * c5)
retained_psd_margin = min_eig - 2.0 * eta
retained_horn_margin = horn_margin - 2.0 * eta
c5_floor = 4.0 * retained_horn_margin  # word-pair window duration T=1
c5_epr = M * log(M + 1.0)

print(f"binary ring covariance C(t)={cov:.12g}, t={t:.12g}")
print(f"midpoint Pinsker floor 16(-C)/t={scalar_floor:.12g} nats/time")
print(f"ring EPR={ring_epr:.12g} nats/time")
print(f"C5 TV error eta={eta:.12g}; retained PSD margin={retained_psd_margin:.12g}")
print(f"retained negative Horn pairing margin={retained_horn_margin:.12g}")
print(f"C5 linear copositive-witness floor={c5_floor:.12g} nats/time")
print(f"C5 realized hidden EPR={c5_epr:.12g} nats/time")

assert cov < 0.0
assert 0.0 < scalar_floor < ring_epr
assert retained_psd_margin > 0.0
assert retained_horn_margin > 0.0
assert 0.0 < c5_floor < c5_epr
