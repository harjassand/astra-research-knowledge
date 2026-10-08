#!/usr/bin/env python3
"""Exact rational audit of the source-derived no-growth yeast glycolysis tube.

This is an auditable calculation, not a biological validation. The only
non-rational outputs are the source Hill-law evaluation and growth-rate check.
"""
from fractions import Fraction as Q
from math import log, sqrt

# Source parameters (Janulevicius & van Doorn, PLOS Comp Biol 2021 Table 1 /
# plos_2021_S1_Model.cellml). Rates are mM/min, concentrations mM.
VMU = Q(10)
KMG = Q(1, 10)
KMATP = Q(1, 10)
KIATP = Q(3)
ATOT = Q(5)
VML = Q(10)
KMF = Q(1)
KMADP = Q(1, 10)
KMP = Q(2)
KATP = Q(10)
PV_MAX = Q(10)
KVAC = Q(250)
M = 4
KP = Q(2, 5)  # proposed intervention floor: 0.4 /min
EPS = Q(9, 50) # total effective flux error: 0.18 mM/min

FLO, FHI = Q(9, 5), Q(11, 5)
ALO, AHI = Q(3, 10), Q(3, 2)
PLO, SUMHI = Q(1), Q(14)


def vlo(F, A, P):
    D = ATOT - A
    return VML * F * D * P / ((KMF + F) * (KMADP + D) * (KMP + P))


def c_u(A):
    return VMU * A / (KMATP + A * (1 + A / KIATP))


def p_vac(F, A, P, kvac=KVAC):
    ptot = P + 2 * F + A
    return PV_MAX / (1 + (ptot / kvac) ** M)


def frac(x):
    return f"{x.numerator}/{x.denominator} = {float(x):.12g}"

# Source model on the no-growth face (growth dilution set to zero):
# Fdot = vu-vlo; Adot=-2vu+4vlo-10A; Pdot=-2vlo+10A+kp(Pvac-P).
# Controller defines actual vu=vlo-(F-2)+e, where |e|<=0.18.
# The six facets are the two F faces, two A faces, P=1, and A+P=14.

# F faces: bounds are exact.
flo_min = (Q(1, 5) - EPS)  # 2-F+e at F=1.8, e=-.18
fhi_max = (-Q(1, 5) + EPS) # 2-F+e at F=2.2, e=+.18

# At A=.3, vlo is minimized at F=1.8,P=1; e=+.18 minimizes Adot.
lo_a = vlo(FLO, ALO, PLO)
adot_lo_min = 2 * lo_a + 2 * (FLO - 2) - 2 * EPS - KATP * ALO
# At A=1.5, vlo is maximized at F=2.2,P=14-A=12.5; e=-.18 maximizes Adot.
hi_a = vlo(FHI, AHI, SUMHI - AHI)
adot_hi_max = 2 * hi_a + 2 * (FHI - 2) + 2 * EPS - KATP * AHI

# At P=1, 2*vlo-10*A is largest at F=2.2,A=.3. Given Pv>=9.5,
# kp>=.4 and Pv-1>0, this gives a uniform inward margin.
lo_p = vlo(FHI, ALO, PLO)
pdot_lo_min = -2 * lo_p + KATP * ALO + KP * (Q(19, 2) - PLO)

# At A+P=14, P>=12.5, Pv<=10, F<=2.2, e>=-.18.
sumdot_hi = 2 * (FHI - 2) + 2 * EPS + KP * (PV_MAX - (SUMHI - AHI))

# Vacuolar Pi on whole tube: P+ A <=14, F<=2.2 implies Ptot<=18.4.
ptot_max = SUMHI + 2 * FHI
pv_min = float(PV_MAX / (1 + (float(ptot_max) / float(KVAC)) ** M))
kvac_min_for_pv95 = float(ptot_max) / ((float(PV_MAX / Q(19, 2)) - 1) ** (1 / M))

# Exact, conservative glucose inversion feasibility. The lower-glycolysis
# flux is separable/monotone in F, A and P. Across the tube:
# vlo_min at (F=1.8,A=1.5,P=1); vlo_max at (2.2,.3,13.7).
vl_min = vlo(FLO, AHI, PLO)
vl_max = vlo(FHI, ALO, SUMHI - ALO)
u_req_lower = vl_min - Q(1, 5) - EPS
u_req_upper = vl_max + Q(1, 5) + EPS
# c_u(A) has its minimum over [.3,1.5] at A=1.5 (endpoints suffice;
# derivative changes sign once at sqrt(0.3)).
cu_min = c_u(AHI)
cu_gap = cu_min - u_req_upper
# Exact inverse for external glucose concentration G:
# G = Km_glc * u / (c_u(A)-u).
# The preceding interval proves 0<u<c_u(A) uniformly.
glucose_conservative_upper = KMG * u_req_upper / cu_gap

# Fixed-glucose contradiction for inwardness of both F faces.
# At the lower-F facet choose A=.3,P=13.7; at upper-F choose A=1.5,P=1.
low_face_flux = vlo(FLO, ALO, SUMHI - ALO)
up_face_flux = vlo(FHI, AHI, PLO)
ratio_hiA_to_loA = c_u(AHI) / c_u(ALO)
fixed_glucose_lower_bound_at_hiA = ratio_hiA_to_loA * low_face_flux

# Published failed-start initial condition: 2014 Fig. 4 varies only Pi 10.4->9.4;
# FBP and ATP are the same as the later source defaults F=2,A=1.
F0, A0, P0 = Q(2), Q(1), Q(47, 5)
lo_fail = vlo(F0, A0, P0)
cu_fail = c_u(A0)
u_fail = lo_fail  # zero tracking error at F=2
G_fail = KMG * u_fail / (cu_fail - u_fail)

# Optional extension to the full PLOS growth term. At F=1.8, worst-case e=-.18,
# Fdot=0.2-.18-F*g, so g<=1/90 /min suffices for that face.
growth_limit = Q(1, 90)
# Source growth at A<=1.5, with reference expression cost 5 and no other
# maintenance, is about ln(2)/(90*(12.7-5))* (10*1.5-5).
source_g_max = log(2) / (90 * (12.7 - 5)) * (10 * 1.5 - 5)
source_growth_F_margin = float(Q(1, 50)) - float(FLO) * source_g_max
# The upper-sum facet is the load-bearing face for kp. At the worst vertex,
# F=2.2, A=1.5, P=12.5, e=-.18 and Pv<=10, giving .76-2.5*kp.
kp_threshold_from_sum = Q(76, 100) / Q(5, 2)
kp03_sumdot_upper = Q(19, 25) + Q(3, 10) * (PV_MAX - (SUMHI - AHI))

rows = [
    ("F=1.8: min Fdot", flo_min),
    ("F=2.2: max Fdot", fhi_max),
    ("A=.3: min Adot", adot_lo_min),
    ("A=1.5: max Adot", adot_hi_max),
    ("P=1: min Pdot, kp=.4 and Pv=9.5", pdot_lo_min),
    ("A+P=14: max (A+P)dot, kp=.4 and Pv=10", sumdot_hi),
]
for label, value in rows:
    print(f"{label}: {frac(value)}")
print(f"max Ptot on tube: {frac(ptot_max)} mM")
print(f"source Pv lower bound on whole tube (Kvac=250): {pv_min:.12g} mM")
print(f"Kvac threshold for Pv>=9.5 on whole tube: {kvac_min_for_pv95:.12g} mM")
pv_needed_for_pi_facet = 1 + (2 * lo_p - KATP * ALO) / KP
kvac_min_for_pi_facet = float(ptot_max) / ((float(PV_MAX / pv_needed_for_pi_facet) - 1) ** (1 / M))
print(f"Pi=1 facet needs only Pv>={frac(pv_needed_for_pi_facet)} mM for kp=.4; corresponding conservative Kvac threshold: {kvac_min_for_pi_facet:.12g} mM")
print(f"vlo range: [{frac(vl_min)}, {frac(vl_max)}] mM/min")
print(f"conservative vup command range: [{frac(u_req_lower)}, {frac(u_req_upper)}] mM/min")
print(f"minimum upper-flux saturation c_u(A): {frac(cu_min)} mM/min")
print(f"uniform saturation gap: {frac(cu_gap)} mM/min")
print(f"conservative external glucose upper bound from separate extrema: {float(glucose_conservative_upper):.12g} mM")
print(f"fixed-GLC contradiction: lower-F face requires vup(A=.3)>={frac(low_face_flux)}; then at A=1.5 vup>={float(fixed_glucose_lower_bound_at_hiA):.12g}, but upper-F face permits only <={frac(up_face_flux)}")
print(f"published failure state (F,A,P)=(2,1,9.4): vlo={frac(lo_fail)}, c_u={frac(cu_fail)}, G(e=0)={float(G_fail):.12g} mM")
print(f"growth bound for F lower face: g<={frac(growth_limit)} /min")
print(f"source-param g_max at A=1.5 (approx): {source_g_max:.12g} /min")
print(f"source-param F lower-face margin with g_max and |e|=.18: {source_growth_F_margin:.12g} mM/min")
print(f"kp threshold from A+P face with |e|=.18 and Pv<=10: {float(kp_threshold_from_sum):.12g} /min")
print(f"reference kp=.3 A+P-face outward upper bound (Pv<=10): {frac(kp03_sumdot_upper)} mM/min")

assert flo_min > 0 and fhi_max < 0
assert adot_lo_min > 0 and adot_hi_max < 0
assert pdot_lo_min > 0 and sumdot_hi < 0
assert u_req_lower > 0 and cu_gap > 0
assert fixed_glucose_lower_bound_at_hiA > up_face_flux
assert source_growth_F_margin > 0
