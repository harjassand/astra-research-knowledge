#!/usr/bin/env python3
"""Exact finite algebra and declared-parameter calculations; no device experiment."""
from fractions import Fraction as F
from pathlib import Path
import json
import math


def main():
    ring_cases = 0
    for p in (F(1, 10), F(33, 100), F(1)):
        for f in (F(1, 4), F(1, 2), F(17, 20), F(9, 10)):
            # Set b=1, a^2=f; stresses need only squared radii.
            aa = p * f / (1-f)
            bb = aa
            assert aa-bb == 0  # radial traction at outer edge
            assert aa-bb/f == -p  # traction at ceramic boundary
            assert aa+bb/f == p*(1+f)/(1-f)
            assert aa*(1-f) == p*f  # integrated in-plane stress balance
            e, nu = F(250), F(1, 4)
            for r_squared in (f, (1+f)/2, F(1)):
                er = ((1-nu)*aa-(1+nu)*bb/r_squared)/e
                et = ((1-nu)*aa+(1+nu)*bb/r_squared)/e
                assert e*(er+nu*et)/(1-nu*nu) == aa-bb/r_squared
                assert e*(et+nu*er)/(1-nu*nu) == aa+bb/r_squared
            ring_cases += 1

    series_cases = 0
    for c1 in (F(1), F(3), F(1, 1000000)):
        for c2 in (F(1), F(7)):
            cap = 1/(1/c1+1/c2)
            for t in (F(1, 10), F(1, 2), F(9, 10)):
                q = (t, 1-t)
                a = (c1*t, c2*(1-t))
                b = (1/(c1*t), 1/(c2*(1-t)))
                energy = c1*t*t+c2*(1-t)*(1-t)
                resistance = 1/c1+1/c2
                assert sum(q) == 1
                assert all(x*y == 1 for x,y in zip(a,b))
                assert sum(x*y for x,y in zip(q,a)) == energy
                assert sum(x*y for x,y in zip(q,b)) == resistance
                assert 1/resistance == cap <= energy
                # Berman-Konsowa is exact on the sole series path.
                assert 1/sum((1/c1, 1/c2)) == cap
                series_cases += 1

    parallel_cases = 0
    for c in ((F(1),F(1)), (F(1),F(1000000)), (F(1,1000),F(1))):
        for j1 in (F(1,100), F(1,2), F(99,100)):
            j = (j1,1-j1)
            a = tuple(x/y for x,y in zip(c,j))
            b = tuple(y/x for x,y in zip(c,j))
            energy = sum(c)
            resistance = sum(y*y/x for x,y in zip(c,j))
            assert sum(x*y for x,y in zip(j,a)) == energy
            assert sum(x*y for x,y in zip(j,b)) == resistance
            assert 1/resistance <= energy
            parallel_cases += 1
    missed_channel = {"conductances": [1,1000000], "flow": [1,0],
                      "true_capacity": 1000001, "sampled_apparent_upper": 1}
    assert missed_channel["sampled_apparent_upper"] < missed_channel["true_capacity"]

    p, ec, nc, er, nr, strength = .330,150.,.25,250.,.25,2.
    f = (strength-p)/(strength+p)
    rows = []
    for fraction in (f,.85):
        hoop = p*(1+fraction)/(1-fraction)
        interference = p*((1-nc)/ec+((1+fraction)/(1-fraction)+nr)/er)
        rows.append({"core_area_fraction":fraction,"peak_hoop_GPa":hoop,
                     "radial_interference_fraction":interference,
                     "hex_packed_active_fraction_upper":math.pi/(2*math.sqrt(3))*fraction})
    pf,ff,mc,mr,thickness = .330e9,.85,200e9,300e9,50e-6
    energy_density = ff*pf**2/mc+ff**2*pf**2/((1-ff)*mr)
    result = {"status":"FINITE_ALGEBRA_AND_ILLUSTRATIONS_ONLY",
              "exact_annular_elasticity_cases":ring_cases,
              "exact_cross_flux_series_cases":series_cases,
              "exact_cross_flux_parallel_cases":parallel_cases,
              "missed_channel_counterexample":missed_channel,
              "illustrative_material_parameters_GPa":
                  {"compression":p,"core_modulus":ec,"ring_modulus":er,"ring_strength":strength},
              "ring_illustrations":rows,
              "laminate_illustration_J_per_m3":energy_density,
              "laminate_50um_illustration_J_per_m2":energy_density*thickness,
              "notes":["Fractions verify finite algebra; they do not verify general proofs.",
                       "Material inputs are illustrative, not acquired measurements.",
                       "No stability, manufacturing or electrochemical validation."]}
    output = Path(__file__).with_name("mechanism_results.json")
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
