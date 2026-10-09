#!/usr/bin/env python3
"""Exact rational replay of the biased-trine counterexample certificate."""
from fractions import Fraction as Q

# Exact Bloch moments for p=(1/20,1/10,17/20), with sqrt(3) tracked separately.
# A pair (a,b) below denotes a + b*sqrt(3).
p = (Q(1, 20), Q(1, 10), Q(17, 20))
r = (Q(-17, 40), Q(0), Q(-3, 8))  # x, y coefficient, z; y means coeff*sqrt(3)
T = ((Q(23, 80), Q(3, 16)), (Q(3, 16), Q(57, 80)))  # off-diagonal coeffs multiply sqrt(3)

# b = Tr/A with A=9/10; x rational, y coefficient multiplies sqrt(3).
A = Q(9, 10)
bx = Q(-533, 1440)
by_coeff = Q(-37, 96)
assert bx == (T[0][0] * r[0] + 3 * T[0][1] * r[2]) / A
assert by_coeff == (T[1][0] * r[0] + T[1][1] * r[2]) / A

# M = D + (83/400)I; derive it from D=b b^T-T^2.
r2 = r[0]**2 + 3 * r[2]**2
A2_minus_r2 = A**2 - r2
assert r2 == Q(241, 400) and A2_minus_r2 == Q(83, 400)
a, c, d = T[0][0], T[0][1], T[1][1]  # Txy off-diagonal is c*sqrt(3)
M11 = bx**2 - (a**2 + 3*c**2) + A2_minus_r2
M22 = 3*by_coeff**2 - (d**2 + 3*c**2) + A2_minus_r2
M12_coeff = bx*by_coeff - c*(a+d)
Mdet = M11 * M22 - 3 * M12_coeff**2
bnorm2 = bx**2 + 3 * by_coeff**2
assert M11 == Q(324265, 2073600)
assert M22 == Q(3073, 76800)
assert M12_coeff == Q(-6199, 138240)
assert Mdet == Q(37267, 165888000)
assert bnorm2 == Q(302041, 518400)
assert M11 > 0 and Mdet > 0
assert bnorm2 < A**2

# Weighted doubled-ket Gram matrix invariants. For G=(3/4)diag(p)+(1/4)xx^T,
# tr(G^2)=(15/16)sum_i p_i^2+1/16 and det(G)=(27/32)prod_i p_i.
sum_p2 = sum(pi**2 for pi in p)
tr_G2 = Q(15, 16) * sum_p2 + Q(1, 16)
e2 = (1 - tr_G2) / 2
det_G = Q(27, 32) * p[0] * p[1] * p[2]
assert tr_G2 == Q(481, 640)
assert e2 == Q(159, 1280)
assert det_G == Q(459, 128000)

def f(t):
    return t**3 - t**2 + e2 * t - det_G

# Three rational sign-changing brackets isolate all roots of the cubic.
brackets = (
    (Q(43, 1000), Q(44, 1000), Q(-56097, 4000000000), Q(57743, 2000000000)),
    (Q(96, 1000), Q(97, 1000), Q(15597, 2000000000), Q(-132183, 4000000000)),
    (Q(860, 1000), Q(861, 1000), Q(-4829, 16000000), Q(1291149, 4000000000)),
)
for lo, hi, flo, fhi in brackets:
    assert f(lo) == flo and f(hi) == fhi and flo * fhi < 0

# rho_1 eigenvalue comparisons: sqrt(241)/20 lies between .776 and .778.
assert Q(776, 1000) ** 2 < Q(241, 400) < Q(778, 1000) ** 2

print(f"A={A}; b=( {bx}, {by_coeff}*sqrt(3) )")
print(f"M11={M11}; M22={M22}; M12={M12_coeff}*sqrt(3)")
print(f"det(M)={Mdet}; ||b||^2={bnorm2}; A^2={A**2}; PD_and_positive_majorant=PASS")
print(f"G characteristic polynomial: t^3 - t^2 + ({e2})*t - ({det_G})")
for lo, hi, flo, fhi in brackets:
    print(f"root bracket ({lo}, {hi}): f(lo)={flo}; f(hi)={fhi}; PASS")
print("rho1 eigenvalues: a_plus > 0.888, a_minus > 0.111; hence mu1<a_plus and mu2<a_minus")
print("spectral overlap = 1-mu3 > 0.956")
print("EB affine certificate: F_acc <= 1/2 + A/2 = 19/20 = 0.95")
print("strict counterexample: PASS")
