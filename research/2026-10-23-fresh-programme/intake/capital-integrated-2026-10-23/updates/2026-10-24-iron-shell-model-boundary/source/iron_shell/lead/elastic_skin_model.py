#!/usr/bin/env python3
"""Exact elastic screens for an oxidized skin; no acquired material parameters.

Three concentric isotropic regions: untransformed oxide core, metallic shell,
and an outer oxidized skin with stress-free isotropic linear eigenstrain e.
Small strain, perfect bonding, spherical symmetry, no plasticity/creep/cracks.
The illustrative moduli are arbitrary GPa inputs, NOT measured Fe/FeO data.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def solve_linear(matrix, rhs):
    rows = [list(map(F, row)) + [F(b)] for row, b in zip(matrix, rhs)]
    n = len(rows)
    for c in range(n):
        pivot = next(r for r in range(c, n) if rows[r][c])
        rows[c], rows[pivot] = rows[pivot], rows[c]
        v = rows[c][c]
        rows[c] = [x / v for x in rows[c]]
        for r in range(n):
            if r != c:
                v = rows[r][c]
                rows[r] = [x - v*y for x, y in zip(rows[r], rows[c])]
    return [row[-1] for row in rows]


def three_layer(a, b, c, K0, K1, G1, K2, G2, e):
    """Return A0,A1,B1,A2,B2 in u=A*r+B/r^2 (B0=0)."""
    a, b, c, K0, K1, G1, K2, G2, e = map(
        F, (a, b, c, K0, K1, G1, K2, G2, e))
    assert 0 < a < b < c and min(K0,K1,G1,K2,G2) > 0
    matrix = [
        [a, -a, -1/a**2, 0, 0],
        [3*K0, -3*K1, 4*G1/a**3, 0, 0],
        [0, b, 1/b**2, -b, -1/b**2],
        [0, 3*K1, -4*G1/b**3, -3*K2, 4*G2/b**3],
        [0, 0, 0, 3*K2, -4*G2/c**3],
    ]
    rhs = [0, 0, 0, -3*K2*e, 3*K2*e]
    result = solve_linear(matrix, rhs)
    assert all(sum(v*x for v,x in zip(row,result)) == r
               for row,r in zip(matrix,rhs))
    return result


def stresses(A, B, K, G, eigenstrain, r):
    A, B, K, G, eigenstrain, r = map(F, (A,B,K,G,eigenstrain,r))
    hydro = 3*K*(A-eigenstrain)
    radial = hydro-4*G*B/r**3
    hoop = hydro+2*G*B/r**3
    return {"radial_GPa":radial, "hoop_GPa":hoop,
            "mean_GPa":hydro, "von_Mises_GPa":abs(radial-hoop)}


def main():
    a,b,c,e = F(7,10),F(19,20),F(1),F(1,10000)
    K,G = F(100),F(40)
    same = three_layer(a,b,c,K,K,G,K,G,e)
    A0,A1,B1,A2,B2 = same
    skin_fraction = 1-(b/c)**3
    closed = 12*K*G/(3*K+4*G)*e*skin_fraction
    # Physically distinct check: equal moduli reduce exactly to a two-layer
    # sphere with a uniformly hydrostatic tensile interior, regardless of a.
    assert B1 == 0 and A0 == A1 and 3*K*A0 == closed
    assert stresses(A1,B1,K,G,0,a)["von_Mises_GPa"] == 0
    assert stresses(A2,B2,K,G,e,c)["radial_GPa"] == 0
    assert stresses(A2,B2,K,G,e,c)["hoop_GPa"] < 0
    zero = three_layer(a,b,c,K,K,G,K,G,0)
    assert all(x == 0 for x in zero)

    # Different elastic moduli produce a deviatoric component in the Fe-shell
    # region. These inputs are a geometric countercheck, not actual Fe/FeO.
    K0,K1,G1,K2,G2 = F(150),F(100),F(40),F(150),F(60)
    contrast = three_layer(a,b,c,K0,K1,G1,K2,G2,e)
    q0,q1,qB1,q2,qB2 = contrast
    assert qB1 != 0
    eps = F(1,100000)
    # Check continuity of radial traction, not just algebraic residuals.
    assert 3*K0*q0 == stresses(q1,qB1,K1,G1,0,a)["radial_GPa"]
    assert stresses(q1,qB1,K1,G1,0,b)["radial_GPa"] == \
        stresses(q2,qB2,K2,G2,e,b)["radial_GPa"]
    assert stresses(q2,qB2,K2,G2,e,c)["radial_GPa"] == 0

    # A purely geometric planar-pore counterexample to 'expansion opens paths'.
    # beta and xi are arbitrary: x radius drops and conductance falls, despite
    # positive transformation volume. No material growth law is asserted.
    beta, r0, xi = F(17,10), F(1), F(1,2)
    r = r0-(beta-1)*xi
    assert 0 < r < r0
    conductance_ratios = {"molecular_diffusion_r2": (r/r0)**2,
                          "Knudsen_r3": (r/r0)**3,
                          "viscous_tube_r4": (r/r0)**4}
    assert all(0 < v < 1 for v in conductance_ratios.values())

    output = {
        "scope": "Exact small-strain model checks; no physical fracture, rate or advantage prediction",
        "assumed_geometry": {"oxide_core_radius":a,"metal_outer_radius":b,
                             "outer_skin_radius":c,"eigenstrain":e},
        "assumed_moduli_units": "GPa, illustrative only",
        "same_moduli": {"K":K,"G":G,"coefficients":same,
                         "core_stress_GPa":closed,
                         "metal_inner":stresses(A1,B1,K,G,0,a),
                         "skin_outer":stresses(A2,B2,K,G,e,c)},
        "contrast_moduli": {"K0":K0,"K1":K1,"G1":G1,"K2":K2,"G2":G2,
                            "coefficients":contrast,
                            "metal_inner":stresses(q1,qB1,K1,G1,0,a),
                            "metal_outer":stresses(q1,qB1,K1,G1,0,b)},
        "assumed_planar_throat": {"beta":beta,"r_initial":r0,
                                  "Fe_consumption_depth":xi,"r_after":r,
                                  "conductance_ratios":conductance_ratios},
        "limits": ["Perfect bonding and spherical symmetry are assumptions",
                   "Full Pilling-Bedworth strain is not a small elastic strain",
                   "Hydrostatic stress is distinct from von Mises stress",
                   "Yield, creep, delamination, fracture and topology require measured laws",
                   "Pressure-only elastic excursions return to baseline without structural memory"],
    }
    def encode(value):
        if isinstance(value,F):
            return {"exact":str(value),"float":float(value)}
        raise TypeError(type(value).__name__)
    Path(__file__).with_name("elastic_skin_results.json").write_text(
        json.dumps(output,indent=2,default=encode)+"\n")
    print("PASS: interface tractions, free surface, zero-growth null, two-layer closed form")
    print(f"Same-modulus metal: mean={float(closed)*1000:.6g} MPa; von Mises=0")
    print("Contrast-modulus metal at inner radius:",
          {k:float(v) for k,v in stresses(q1,qB1,K1,G1,0,a).items()})
    print("Planar throat conductance ratios:",{k:float(v) for k,v in conductance_ratios.items()})
    print("No measured material response or persistent transport improvement is inferred")


if __name__ == "__main__":
    main()
