from fractions import Fraction as F
from math import isclose, log


def metrics(u, ubar, v, vbar):
    total = u + ubar + v + vbar
    p_a = (ubar + vbar) / total
    p_b = (u + v) / total
    productive_current = (u * vbar - v * ubar) / total
    cycle_affinity = log(float(u * vbar / (v * ubar)))
    return total, p_a, p_b, productive_current, cycle_affinity


# Two distinct splits of the same aggregate A<->B generator at [S]=[P]=1.
model_1 = (F(1), F(1, 2), F(1), F(3, 2))
model_2 = (F(6, 5), F(7, 10), F(4, 5), F(13, 10))

for model in (model_1, model_2):
    u, ubar, v, vbar = model
    assert u + v == 2
    assert ubar + vbar == 2

m1 = metrics(*model_1)
m2 = metrics(*model_2)
assert m1[:4] == m2[:4] == (F(4), F(1, 2), F(1, 2), F(1, 4))
assert F(model_1[0] * model_1[3], model_1[2] * model_1[1]) == 3
assert F(model_2[0] * model_2[3], model_2[2] * model_2[1]) == F(39, 14)
assert not isclose(m1[4], m2[4], rel_tol=0, abs_tol=1e-12)

# Mass-action intervention [S] -> 4[S] multiplies only channel-1 forward rate.
def flux_after_substrate_scale(model, scale):
    u, ubar, v, vbar = model
    return (scale * u * vbar - v * ubar) / (scale * u + ubar + v + vbar)

j1 = flux_after_substrate_scale(model_1, 4)
j2 = flux_after_substrate_scale(model_2, 4)
assert j1 == F(11, 14)
assert j2 == F(71, 95)
assert j1 - j2 == F(51, 1330)

# The entropy production for the cycle is nonnegative and differs across models.
sigma1_over_kb = F(1, 4) * m1[4]
sigma2_over_kb = F(1, 4) * m2[4]
assert sigma1_over_kb > 0 and sigma2_over_kb > 0
assert sigma1_over_kb != sigma2_over_kb

print("PASS: identical aggregate rates, occupancy, and baseline product flux")
print(f"cycle affinities: ln(3)={m1[4]:.12f}; ln(39/14)={m2[4]:.12f}")
print(f"sigma/kB: {sigma1_over_kb:.12f}; {sigma2_over_kb:.12f}")
print(f"flux at [S] x4: 11/14={float(j1):.12f}; 71/95={float(j2):.12f}")
print(f"dose-response gap: 51/1330={float(j1-j2):.12f}")
