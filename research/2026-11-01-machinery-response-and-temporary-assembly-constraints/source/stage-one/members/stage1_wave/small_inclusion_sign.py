"""Independent conductance-force sign check using a sphere and Maxwell stress.

Exterior incident potential is -E*z - gradient*(z*z-x*x)/2. The sphere's
Laplace transmission solution includes its exact l=1 and l=2 induced harmonics.
We integrate the physical exterior Maxwell stress, without using the port-force
identity. The comparison port derivative uses the leading small-sphere
Dirichlet-to-Neumann perturbation. No experimental data or central invention.
"""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss


def stress_force(sigma_particle, sigma_medium=1.0, eps_medium=2.0,
                 radius=0.1, E=1.0, gradient=0.3, surface_ratio=1.7):
    z_cos, z_weights = leggauss(80)
    phi = 2 * np.pi * np.arange(160) / 160
    ct, ph = np.meshgrid(z_cos, phi, indexing="ij")
    st = np.sqrt(1 - ct * ct)
    normal = np.stack((st * np.cos(ph), st * np.sin(ph), ct), axis=-1)
    r = surface_ratio * radius
    pos = r * normal
    x, z = pos[..., 0], pos[..., 2]
    k1 = (sigma_particle - sigma_medium) / (sigma_particle + 2 * sigma_medium)
    k2 = 2 * (sigma_particle - sigma_medium) / (2 * sigma_particle + 3 * sigma_medium)
    inc = np.stack((-gradient * x, np.zeros_like(x), E + gradient * z), axis=-1)
    ez = np.array([0.0, 0.0, 1.0])
    dipole = k1 * radius**3 * E * (3 * z[..., None] * pos / r**5 - ez / r**3)
    grad_harmonic = np.stack((-2 * x, np.zeros_like(x), 2 * z), axis=-1)
    quad = -(0.5 * k2 * radius**5 * gradient
             * (grad_harmonic / r**5 - 5 * (z*z-x*x)[..., None] * pos / r**7))
    field = inc + dipole + quad
    field_normal = np.sum(field * normal, axis=-1)
    field_squared = np.sum(field * field, axis=-1)
    traction = eps_medium / 4 * (2 * field * field_normal[..., None]
                                 - field_squared[..., None] * normal)
    weights = z_weights[:, None, None] * (2 * np.pi / 160) * r*r
    force = np.sum(traction * weights, axis=(0, 1))
    d_port_power_dq = 8 * np.pi * sigma_medium * radius**3 * k1 * E * gradient
    positive_identity = eps_medium / (4 * sigma_medium) * d_port_power_dq
    return {
        "sigma_particle": sigma_particle, "conductivity_CM_factor": k1,
        "surface_ratio": surface_ratio,
        "force_from_exterior_stress": force.tolist(),
        "port_quadratic_derivative_leading_order": d_port_power_dq,
        "positive_input_identity_force": positive_identity,
        "negative_printed_identity_force": -positive_identity,
        "relative_positive_identity_error": abs(force[2] - positive_identity) / abs(positive_identity),
    }


def run():
    results = [stress_force(sigma, surface_ratio=r)
               for sigma in (0.1, 10.0) for r in (1.1, 1.7, 3.0)]
    for r in results:
        assert r["relative_positive_identity_error"] < 1e-10
        assert np.sign(r["force_from_exterior_stress"][2]) == np.sign(r["positive_input_identity_force"])
    output = {"scope": "Analytic continuum sphere with exact l=1,l=2 field; numerical stress quadrature and small-inclusion port variation", "results": results}
    Path(__file__).with_name("small_inclusion_sign_results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run()
