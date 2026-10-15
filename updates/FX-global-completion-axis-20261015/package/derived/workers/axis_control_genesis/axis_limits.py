#!/usr/bin/env python3
"""Reproduce conditional mathematical limits, not material-response predictions.

No elastic constants, nucleus sizes, susceptibilities, or switching barriers are
assumed. The only process temperature is the published 300 C reference.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KB = 1.380649e-23
EV = 1.602176634e-19
MU0 = 4 * math.pi * 1e-7


def simpson(f, a, b, n=20000):
    assert n > 0 and n % 2 == 0
    h = (b - a) / n
    return h / 3 * (f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i*h) for i in range(1, n)))


def fcc_hamming(cells):
    sites = [(i,j,k) for i in range(2*cells) for j in range(2*cells)
             for k in range(2*cells) if (i+j+k) % 2 == 0]
    mismatch = sum((i % 2) != (j % 2) for i,j,k in sites)
    assert len(sites) == 4*cells**3
    assert mismatch * 2 == len(sites)
    assert mismatch % 2 == 0
    return {"cells_per_side": cells, "metal_sites": len(sites),
            "x_to_y_occupancy_changes": mismatch, "minimum_pair_swaps": mismatch//2}


def run():
    cubic_r = 3*math.sqrt(2)/math.pi * math.atan(1/math.sqrt(2))
    cubic_q = 1/3 + 2/(math.pi*math.sqrt(3))
    # Azimuth-reduced spherical integrals, with exact theta integration.
    cubic_r_quad = 6/math.pi * simpson(lambda phi: 1/(1+math.cos(phi)**2), 0, math.pi/4)
    cubic_q_quad = 4/math.pi * simpson(
        lambda phi: 1-(math.cos(phi)/math.sqrt(1+math.cos(phi)**2))**3,
        0, math.pi/4)
    assert abs(cubic_r-cubic_r_quad) < 2e-12
    assert abs(cubic_q-cubic_q_quad) < 2e-12
    planar_r = 2/math.pi
    planar_quad = 2/math.pi * simpson(math.cos, 0, math.pi/2)
    assert abs(planar_r-planar_quad) < 2e-12
    t = 300 + 273.15
    q = .9
    delta = KB*t*math.log(2*q/(1-q))
    field_products = {str(b): 2*MU0*delta/(b*b) for b in (1.,4.,10.)}
    out = {
        "status": "CONDITIONAL_MATHEMATICS_ONLY_NO_PHYSICAL_OPERATION_ACQUIRED",
        "fcc_perfect_axis_rewrite": {
            "assumptions": "Fixed fcc site registry and 90-degree switch of perfectly ordered x/y FeNi occupations; no lattice rotation; pair exchanges counted abstractly.",
            "changed_occupancy_fraction": .5, "minimum_pair_swap_fraction": .25,
            "enumerations": [fcc_hamming(n) for n in (1,2,3,5,10)]},
        "fixed_random_cubic_parent_variant_ceiling": {
            "assumptions": "Isotropic volume-weighted parent orientations; only three orthogonal parent axes accessible; no parent rotation/recrystallization; ideal full selection.",
            "maximum_mean_absolute_projection": cubic_r,
            "maximum_mean_squared_projection": cubic_q,
            "quadrature_absolute_projection": cubic_r_quad,
            "quadrature_squared_projection": cubic_q_quad,
            "warning": "Not applicable as a universal bound to irregular/reconstructive FeNiN orientation relationships."},
        "uniform_planar_axes_null_model": {
            "assumptions": "All axes in xy plane and uniform azimuth; independent uniaxial remanence if interpreting projection magnetically.",
            "Q": [[.5,0,0],[0,.5,0],[0,0,0]], "D_x_minus_y": 0,
            "mean_absolute_x_projection": planar_r,
            "warning": "A null model showing that planar confinement alone does not establish in-plane axis writing; not a fit to any patent specimen."},
        "equal_prefactor_three_competing_nucleation_benchmark": {
            "temperature_k": t, "target_favored_first_nucleus_probability": q,
            "delta_activation_free_energy_j": delta,
            "delta_activation_free_energy_ev": delta/EV,
            "required_stress_activation_volume_contraction_j": delta,
            "weak_linear_susceptibility_product_delta_chi_times_volume_m3_by_B_t": field_products,
            "assumptions": "One favored and two equivalent unfavored independent nucleation channels with equal attempt prefactors; field expression additionally assumes weak linear susceptibility and appropriate free-energy volume.",
            "warning": "No nucleus size, activation volume, stress limit, susceptibility anisotropy, or kinetic regime has been acquired; these are not FeNiN feasibility predictions."},
        "phase_temperature_overlap": {"reported_fenin_neel_temperature_k":178.,
                                     "nitridation_reference_temperature_k":t,
                                     "reference_temperature_divided_by_neel_temperature":t/178,
                                     "inference":"FeNiN formation reference is above its reported magnetic ordering temperature; ferromagnetic torque cannot be imported from final FeNi."},
    }
    return out


if __name__ == "__main__":
    results = run()
    (ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
