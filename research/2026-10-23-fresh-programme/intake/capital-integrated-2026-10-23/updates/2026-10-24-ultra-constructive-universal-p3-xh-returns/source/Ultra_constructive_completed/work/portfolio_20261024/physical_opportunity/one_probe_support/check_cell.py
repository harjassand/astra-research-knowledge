from fractions import Fraction as F
from math import sqrt


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


Hinv = ((F(2, 3), F(1, 3)), (F(1, 3), F(2, 3)))
a = (F(1), F(0))
b = (F(-1), F(1))
f = (F(0), F(1))  # rational bond-deletion fixture; snap ledger is below

Hinv_a = tuple(sum(Hinv[i][j] * a[j] for j in range(2)) for i in range(2))
assert Hinv_a == (F(2, 3), F(1, 3))
assert dot(a, Hinv_a) == F(2, 3)
assert dot(b, Hinv_a) == F(-1, 3)

q = sum(b[i] * Hinv[i][j] * b[j] for i in range(2) for j in range(2))
e = sum(b[i] * Hinv[i][j] * f[j] for i in range(2) for j in range(2))
delta_C = e * e / (1 - q)
assert q == F(2, 3)
assert e == F(1, 3)
assert delta_C == F(1, 3)
assert (1 - q) > 0
# The fixed load used in the snap ledger is 2*sqrt(3) times this exact
# rational direction, so e scales linearly and delta_C quadratically.
snap_load_scale = 2 * sqrt(3.0)
assert abs(e * snap_load_scale - 2 / sqrt(3.0)) < 1e-12
assert abs(float(delta_C) * snap_load_scale**2 - 4) < 1e-12

# Snap ledger, in normalized spring/length/energy units.
r3 = sqrt(3.0)
yi, yf = -1 / r3, 2 / r3
s = 2 / r3
c = 2 / 3

def phi(y):
    return 0.75 * (y * y - 1) ** 2 - s * y

def V(y):
    return 0.75 * (y * y - 1) ** 2 + (1 / 3) * y * y

def x1(y):
    return (2 * y + 2 * r3) / 3

def x2(y):
    return (y + 4 * r3) / 3

def e_threat(y):
    return x2(y) - x1(y)

dy = yf - yi
assert abs(dy - r3) < 1e-12
assert abs((e_threat(yf) - e_threat(yi)) + 1 / r3) < 1e-12
assert abs((x1(yf) - x1(yi)) - 2 / r3) < 1e-12
assert abs((phi(yf) - phi(yi)) + 9 / 4) < 1e-12

load_work = 2 * r3 * (x2(yf) - x2(yi))
host_energy_change = s * dy + (c / 2) * (yf * yf - yi * yi)
cell_energy_change = V(yf) - V(yi)
coupling_energy_change = -yf * x1(yf) + yi * x1(yi)
internal_change = host_energy_change + cell_energy_change + coupling_energy_change
assert abs(load_work - 2) < 1e-12
assert abs(host_energy_change - 7 / 3) < 1e-12
assert abs(cell_energy_change - 1 / 12) < 1e-12
assert abs(coupling_energy_change + 8 / 3) < 1e-12
assert abs(internal_change + 1 / 4) < 1e-12
assert abs(internal_change - load_work + 9 / 4) < 1e-12

print("PASS: exact compliance, negative cross-compliance, and bond deletion identities")
print("PASS: spinodal snap lowers threat extension by 1/sqrt(3)")
print("PASS: energy ledger closes; fixed-load potential change is -9/4")
