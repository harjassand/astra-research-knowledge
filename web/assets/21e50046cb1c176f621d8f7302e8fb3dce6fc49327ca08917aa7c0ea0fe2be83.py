#!/usr/bin/env python3
"""Analytic checks for the finite-time reset channel and its LDB boundary.

This checks the effective two-state alarm-reset CTMC and demonstrates the
affinity required when it is paired with the stipulated background rates.
It does not model the sensor/controller gate or claim an ATP cost for it.
"""

from __future__ import annotations

import math
from fractions import Fraction
import importlib.util
from pathlib import Path


TAU = 1.0
DELTA = 0.2  # G -> B transition probability during an alarm reset
RHO = 0.6    # B -> G transition probability during an alarm reset
A = 0.005    # background G -> B rate
B = 0.02     # background B -> G rate

K = -math.log(1.0 - DELTA - RHO) / TAU
K_GB = DELTA * K / (DELTA + RHO)
K_BG = RHO * K / (DELTA + RHO)
P_GB = (K_GB / K) * (1.0 - math.exp(-K * TAU))
P_BG = (K_BG / K) * (1.0 - math.exp(-K * TAU))

assert math.isclose(P_GB, DELTA, rel_tol=0.0, abs_tol=1e-15)
assert math.isclose(P_BG, RHO, rel_tol=0.0, abs_tol=1e-15)
assert K_GB > 0 and K_BG > 0

# LDB convention for G + ATP <-> B + ADP + Pi:
# ln(k_GB/k_BG) = beta*(Delta_mu_ATP - (E_B-E_G)).
# The equilibrium background channel implies E_B-E_G = kT*ln(b/a).
gap_over_kT = math.log(B / A)
mu_over_kT = math.log(K_GB / K_BG) + gap_over_kT
assert math.isclose(mu_over_kT, math.log(4.0 / 3.0), abs_tol=1e-15)

# If instead B -> G were designated ATP hydrolysis, its implied affinity is
# ln(k_BG/k_GB) - (E_B-E_G), which is ln(3/4) < 0.
opposite_mu_over_kT = math.log(K_BG / K_GB) - gap_over_kT
assert math.isclose(opposite_mu_over_kT, math.log(3.0 / 4.0), abs_tol=1e-15)

# Exact stationary flux check for the candidate policy. For the chosen
# G->B-hydrolysis orientation, net hydrolysis is delta*alarms_starting_G minus
# rho*alarms_starting_B = reverse_G_to_B - successful_B_to_G.
source = Path(__file__).with_name("exact_check.py")
spec = importlib.util.spec_from_file_location("n27_exact", source)
assert spec is not None and spec.loader is not None
exact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact)
candidate = tuple(int(2 * mem + z in (7, 11, 13))
                  for mem in range(exact.NM) for z in (0, 1))
rewards = exact.evaluate(candidate)
net_hydrolysis = rewards["reset_reverse"] - rewards["reset_success"]
assert net_hydrolysis < 0

print(f"K={K:.15g}; k_GB={K_GB:.15g}; k_BG={K_BG:.15g}; tau={TAU}")
print(f"finite-time reset map: P(G->B)={P_GB:.15g}; P(B->G)={P_BG:.15g}")
print(f"background gap (E_B-E_G)/kT={gap_over_kT:.15g}")
print(f"LDB ATP affinity for G->B hydrolysis, Delta_mu/kT={mu_over_kT:.15g} (ln(4/3))")
print(f"opposite B->G hydrolysis affinity/kT={opposite_mu_over_kT:.15g} (ln(3/4))")
print(f"candidate net ATP hydrolysis/site={float(net_hydrolysis):.15g}")
print(f"candidate exact net-flux fraction={net_hydrolysis.numerator}/{net_hydrolysis.denominator}")
print("PASS: finite-time map embeds with positive rates; local reset-edge LDB is consistent at the stated affinity.")
print("LIMIT: action gate, cue sensor/reuse, memory overwrite, clock, and total fuel/work are not closed by this check.")
