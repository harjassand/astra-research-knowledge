"""Independent audit of the actual-pole reference and an orthogonalized repair.

Uses the root's implemented pulse generator, but independently reconstructs
the input/output displacement and Weyl-phase comparison.  Numerical values
are quadrature checks, not parameter-interval certificates.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_simpson, simpson

HERE = Path(__file__).resolve().parent
ROOT_SCRIPT = HERE.parent / "root" / "actual_pole_reference.py"
spec = importlib.util.spec_from_file_location("root_pole_pulse", ROOT_SCRIPT)
root = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root)


def audit(kappa=1.1e-4, detuning=1e-6, points=16001, number_cap=320, nb=.1):
    t, actual_force = root.pulse(points)
    a = kappa / 2
    centered = t - t[-1] / 2
    rows = np.array([
        np.exp(1j * detuning * centered) * np.cosh(a * centered),
        np.exp(1j * detuning * centered) * np.sinh(a * centered) / a,
    ])
    weight = np.sin(np.pi * t / t[-1])**2
    gram = np.array([[simpson(weight * r * q.conj(), x=t)
                      for q in rows] for r in rows])
    projection = []
    for force in actual_force:
        target = np.array([simpson(r * force, x=t) for r in rows])
        coefficients = np.linalg.solve(gram, target)
        projection.append(weight * np.sum(coefficients[:, None] * rows.conj(), axis=0))
    projected_force = actual_force - np.array(projection)

    def cumulative(values):
        return (cumulative_simpson(values.real, x=t, initial=0)
                + 1j * cumulative_simpson(values.imag, x=t, initial=0))

    pole = a + 1j * detuning

    def response(forces):
        return np.array([-1j * np.exp(-pole * t)
                         * cumulative(np.exp(pole * t) * f) for f in forces])

    def inner(left, right):
        return left[-1].conj() * right[-1] + kappa * simpson(left.conj() * right, x=t)

    def phases(forces, paths):
        self_phases = np.array([-np.real(simpson(f * b.conj(), x=t))
                                for f, b in zip(forces, paths)])
        theta = -np.real(simpson(forces[0] * paths[1].conj()
                                + forces[1] * paths[0].conj(), x=t))
        return self_phases, theta

    actual_path = response(actual_force)
    projected_path = response(projected_force)
    gxx = inner(projected_path[0], projected_path[0])
    gxy = inner(projected_path[0], projected_path[1])
    coefficient = gxy / gxx

    # A linear combination of double-null forces remains double-null.
    repaired_force = projected_force.copy()
    repaired_force[1] -= coefficient * repaired_force[0]
    repaired_path = projected_path.copy()
    repaired_path[1] -= coefficient * repaired_path[0]

    actual_self, actual_theta = phases(actual_force, actual_path)

    def evaluate(forces, paths):
        delta_force = actual_force - forces
        delta_path = actual_path - paths
        old = np.array([-1j * simpson(np.exp((-a + 1j * detuning) * t) * f, x=t)
                        for f in delta_force])
        cross = np.array([[inner(b, c) for c in actual_path] for b in paths])
        delta_gram = np.array([[inner(b, c) for c in delta_path] for b in delta_path])
        reference_gram = np.array([[inner(b, c) for c in paths] for b in paths])
        omega = actual_theta - np.pi / 4 + np.imag(cross[0, 1] + cross[1, 0])
        values = []
        for jd in (-2, 0, 2):
            for za in (-1, 1):
                vector = np.array([jd, za])
                old_component = abs(vector @ old)
                full_norm_squared = np.real(vector @ delta_gram @ vector)
                fresh_norm_squared = full_norm_squared - old_component**2
                bound = (abs(jd * za * omega)
                         + old_component * (np.sqrt(number_cap) + np.sqrt(number_cap + 1))
                         + np.sqrt((2 * nb + 1) * max(0, fresh_norm_squared)))
                values.append(float(bound))
        return {
            "G_real": reference_gram.real.tolist(),
            "G_imag": reference_gram.imag.tolist(),
            "aligned_cross_phase": float(omega),
            "channel_bound": 2 * max(values),
            "closure_residual": float(max(abs(simpson(r * f, x=t))
                                          for r in rows for f in forces)),
            "endpoint_residual": list(abs(paths[:, -1])),
            "matched_self_phase": list(actual_self + np.imag(np.diag(cross))),
        }

    # Full-instrument cross-sector coefficient caused by a real Gxy, despite
    # an ideal parity angle.  D=(++), D'=(+-), raw X+ report; after X+ frame
    # there is no extra data correction.
    G = np.array([[inner(b, c) for c in projected_path] for b in projected_path])
    j, jp = 2, 0
    schur = 0j
    for anc in (-1, 1):
        for ancp in (-1, 1):
            z, zp = np.array([j, anc]), np.array([jp, ancp])
            difference = z - zp
            dephasing = np.exp(-(nb + .5) * np.real(difference @ G @ difference)
                               + 1j * np.imag(zp @ G @ z))
            schur += .25 * np.exp(1j * np.pi / 4 * (anc * j - ancp * jp)) * dephasing

    return {
        "kappa": kappa, "detuning": detuning, "points": points,
        "gram_schmidt_coefficient": [float(coefficient.real), float(coefficient.imag)],
        "projected_only": evaluate(projected_force, projected_path),
        "orthogonalized": evaluate(repaired_force, repaired_path),
        "projected_reference_cross_parity_Schur_entry": [float(schur.real), float(schur.imag)],
        "scope": "Quadrature audit only; no parameter-interval or hardware certificate.",
    }


if __name__ == "__main__":
    results = [audit(points=n) for n in (8001, 16001, 32001)]
    (HERE / "actual_pole_reference_audit_results.json").write_text(
        json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
