"""Bounded discovery probe for the exact G soft-potential identity.

Grid outputs are exploratory. Coefficient formation and each selected grid
point ratio are rational; no continuum optimization claim is made.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import numpy as np


ROOT = Path(__file__).resolve().parent


def K(z):
    p, q, r = z
    return Q(1, 1944)*(8667*p**4+18792*p**3*r+576*p*p*q*q+16416*p*p*r*r
       +1440*p*q*q*r+6912*p*r**3+56*q**4+576*q*q*r*r+1152*r**4)


def jet(k):
    x, y = k
    return (-x*x, -x*y, -y*y)


def add(v, w, sign=1):
    return tuple(a+sign*b for a, b in zip(v, w))


def coeffs(k, ell):
    ks = (k, ell, tuple(a+b for a, b in zip(k, ell)))
    jets = [jet(t) for t in ks]
    alpha = [Q(5, 24)*z[0]**2 for z in jets]
    beta = [Q(3, 8)*K(z) for z in jets]
    pairs = [(0,1), (0,2), (1,2)]
    gamma = [(K(add(jets[i], jets[j]))+K(add(jets[i], jets[j], -1))
              -2*K(jets[i])-2*K(jets[j]))/8 for i,j in pairs]
    p = [z[0] for z in jets]
    q = [z[1] for z in jets]
    cubic = -Q(5, 36)*sum(q[i]*p[(i+1)%3]*p[(i+2)%3] for i in range(3))
    cubic -= Q(5, 27)*q[0]*q[1]*q[2]
    return ks, alpha, beta, gamma, cubic


def ratio(s, alpha, beta, gamma, cubic):
    quad = np.dot(alpha, s)
    quartic = np.dot(beta, s*s)+gamma[0]*s[0]*s[1]+gamma[1]*s[0]*s[2]+gamma[2]*s[1]*s[2]
    if quad <= 0 or quartic <= 0:
        return -np.inf
    return cubic*cubic*np.prod(s)/(4*quad*quartic)


# Distinct noncollinear pairs, with the sum as the third Fourier mode.
# This is a bounded triad family, not an exhaustive profile representation.
vectors = [(x,y) for x in (1,2,3) for y in range(-4,5)]
seen = set()
records = []
denominator = 60
integer_grid = np.array([(i,j,denominator-i-j) for i in range(1,denominator-1)
                        for j in range(1,denominator-i)])
simplex_grid = integer_grid/denominator
for k in vectors:
    for ell in vectors:
        if k[0]*ell[1] == k[1]*ell[0]:
            continue
        ks, alpha, beta, gamma, cubic = coeffs(k, ell)
        key = tuple(sorted(ks))
        if key in seen or cubic == 0:
            continue
        seen.add(key)
        af, bf, gf = [np.array([float(z) for z in t]) for t in (alpha,beta,gamma)]
        cf = float(cubic)
        quad = simplex_grid@af
        quartic = (simplex_grid*simplex_grid)@bf
        quartic += gf[0]*simplex_grid[:,0]*simplex_grid[:,1]
        quartic += gf[1]*simplex_grid[:,0]*simplex_grid[:,2]
        quartic += gf[2]*simplex_grid[:,1]*simplex_grid[:,2]
        values = cf*cf*np.prod(simplex_grid,axis=1)/(4*quad*quartic)
        idx = int(np.argmax(values))
        rational_s = [Q(int(i),denominator) for i in integer_grid[idx]]
        exact_quad = sum(a*s for a,s in zip(alpha,rational_s))
        exact_quartic = sum(b*s*s for b,s in zip(beta,rational_s))
        exact_quartic += gamma[0]*rational_s[0]*rational_s[1]
        exact_quartic += gamma[1]*rational_s[0]*rational_s[2]
        exact_quartic += gamma[2]*rational_s[1]*rational_s[2]
        exact_ratio = cubic*cubic*rational_s[0]*rational_s[1]*rational_s[2]/(4*exact_quad*exact_quartic)
        best = {"ratio":float(values[idx]), "s":[str(s) for s in rational_s],
                "selected_point_exact_ratio":str(exact_ratio),
                "minimum_observed_quartic":float(np.min(quartic))}
        records.append({"modes":ks, "quadratic_coefficients":[str(t) for t in alpha],
            "quartic_diagonal_coefficients":[str(t) for t in beta],
            "quartic_pair_coefficients":[str(t) for t in gamma], "cubic_coefficient":str(cubic),
            "best_numerical_ratio":best})

records.sort(key=lambda r: r["best_numerical_ratio"]["ratio"], reverse=True)
receipt = {"status":"EXPLORATORY_COMPLETED", "family":"three cosine modes k,ell,k+ell in soft potential",
  "criterion":"negative scaling possible when cubic^2/(4 quadratic quartic) > 1, with quartic>0",
  "pair_count":len(records), "simplex_denominator":denominator,
  "grid_points_per_pair":len(simplex_grid),
  "maximum_observed_ratio":records[0]["best_numerical_ratio"]["ratio"] if records else None,
  "negative_witness":"NONE_FOUND", "universal_conclusion":"NONE", "records":records}
(ROOT/"soft_triad_probe.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({k:v for k,v in receipt.items() if k != "records"}, indent=2))
print(json.dumps(records[:3], indent=2))
