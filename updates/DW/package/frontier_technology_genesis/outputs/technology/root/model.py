#!/usr/bin/env python3
"""Exact identities and screening estimates; no physical validation.

Standard library only. Run: python3 model.py > model_results.json
"""
import json
import math
from fractions import Fraction as F


def matvec(a, x):
    return [sum((v * w for v, w in zip(row, x)), F(0)) for row in a]


def field_force(alpha, e0, g, x, y, z):
    fields = [[e0 + g*x, -g*y, F(0)],
              [g*y, e0 + g*x, F(0)],
              [g*z, F(0), e0 + g*x]]
    gradients = [[[g, 0, 0], [0, -g, 0], [0, 0, 0]],
                 [[0, g, 0], [g, 0, 0], [0, 0, 0]],
                 [[0, 0, g], [0, 0, 0], [g, 0, 0]]]
    force = [F(0)] * 3
    for electric, grad in zip(fields, gradients):
        f = matvec(grad, matvec(alpha, electric))
        force = [v + w / 3 for v, w in zip(force, f)]
    return force


def field_checks():
    fixtures = 0
    for j in range(1, 21):
        b = [[F(j), F(2), F(-1)], [F(1), F(j+1), F(3)],
             [F(-2), F(1), F(j+2)]]
        alpha = [[sum(b[i][k]*b[l][k] for k in range(3))
                  for l in range(3)] for i in range(3)]
        tr = sum(alpha[i][i] for i in range(3))
        e0, g, x, y, z = F(10), F(2), F(1, 20), F(-1, 30), F(1, 40)
        force = field_force(alpha, e0, g, x, y, z)
        expected_x = g*((e0 + g*x)*tr + g*z*alpha[0][2])/3
        assert force[0] == expected_x
        upper_r = 3*force[0]/(g*(e0+g*x-abs(g*z)/2))
        assert tr <= upper_r
        # Four-sign coefficient projection cancels terms odd in one amplitude,
        # including arbitrary fixed charge and quadratic-gradient nuisances.
        recovered = F(0)
        for s in [-1, 1]:
            for t in [-1, 1]:
                raw = field_force(alpha, s*e0, t*g, x, y, z)[0]
                raw += F(7)*s*e0 + F(5)*t*g + F(11)
                recovered += s*t*raw/4
        assert recovered == e0*g*tr/3
        fixtures += 1
    return {"exact_fraction_fixtures": fixtures,
            "identities": "scalar trace, PSD off-axis upper bound, four-sign projection",
            "scope": "linear induced-dipole model; finite-body argument separate"}


def isotope_checks():
    laws = {"A": [(0, 2, F(1, 2)), (1, 3, F(1, 2))],
            "B": [(0, 3, F(1, 2)), (1, 2, F(1, 2))]}
    steps = {}
    for name, law in laws.items():
        steps[name] = []
        for t in [F(-1), F(1, 2), F(3, 2), F(5, 2), F(7, 2)]:
            probs = [F(0)]*3
            for a, b, p in law:
                n = int(t >= a) + int(t >= b)
                probs[n] += p
            steps[name].append(probs)
    assert steps["A"] == steps["B"]
    period = 8
    results = {}
    for name, law in laws.items():
        h = [F(0)]
        mixed = []
        for width in range(1, 4):
            code = [int(t < width) for t in range(period)]
            p1 = sum(p*F(sum(code[(t-a)%period] != code[(t-b)%period]
                             for t in range(period)), period)
                     for a, b, p in law)
            exact = sum(p*F(2*min(abs(a-b), width), period)
                        for a, b, p in law)
            assert p1 == exact
            mixed.append(p1)
            h.append(F(period, 2)*p1)
        recovered = [1-h[1]]
        for k in range(1, 3):
            recovered.append(2*h[k]-h[k-1]-h[k+1])
        recovered.append(h[3]-h[2])
        truth = [sum(p for a, b, p in law if abs(a-b)==k)
                 for k in range(4)]
        assert recovered == truth
        results[name] = {"pulse_mixed_fractions": list(map(str, mixed)),
                         "recovered_gap_distribution": list(map(str, recovered))}
    # The arbitrary-waveform comparator perfectly separates these witnesses.
    alt = [1, -1]
    alt_parities = {name: sum(p*alt[a%2]*alt[b%2] for a,b,p in law)
                   for name,law in laws.items()}
    assert alt_parities == {"A": F(1), "B": F(-1)}
    return {"step_traces_equal": True, "period": period, "models": results,
            "alternating_code_parity": {k:str(v) for k,v in alt_parities.items()},
            "interpretation": "pulse identity holds; no superiority over arbitrary-code Volterra identification"}


def spheroid_trace_ratio(aspect):
    if aspect == 1:
        return 1.0
    e = math.sqrt(1-1/aspect**2)
    nz = (1-e*e)/(2*e**3)*(math.log((1+e)/(1-e))-2*e)
    nx = (1-nz)/2
    return (1/nz + 2/nx)/9


def powder_screen():
    eps0, rho, radius = 8.8541878128e-12, 2700., 15e-6
    e0, g, kick, drift = 1e6, 1e9, .001, .010
    mass = 4*math.pi*radius**3*rho/3
    r0 = 9*eps0/rho
    accel = e0*g*r0/3
    shift = accel*(kick**2/2+kick*drift)
    eta, epsa, density_margin = .002, .002, .002
    k_relative = (1-eta)*(1-epsa)/(1+density_margin)
    certificate_threshold = k_relative/.99
    return {"assumed_material": "Al, homogeneous PEC; physical uncertainties additional",
            "sphere_acceleration_m_s2": accel,
            "sphere_shift_m": shift,
            "one_percent_void_shift_increment_m": shift*(1/.99-1),
            "particle_mass_kg": mass,
            "particles_per_s_at_1kg_h": (1/3600)/mass,
            "robust_constants_each_0.2percent": {
                "nonmetal_mass_upper": eta, "polarizability_reduction_upper": epsa,
                "density_upper_margin": density_margin,
                "allowed_Rupper_over_ideal_sphere_for_phi_1percent": certificate_threshold},
            "prolate_shape_R_over_sphere": {
                str(q): spheroid_trace_ratio(q) for q in [1,1.05,1.1,1.2,1.5,2]},
            "status": "screening calculation, not device feasibility or measured performance"}


if __name__ == "__main__":
    print(json.dumps({"field_projection":field_checks(),
                      "isotope":isotope_checks(),
                      "powder":powder_screen()}, indent=2))
