#!/usr/bin/env python3
"""Discriminating mechanical checks; not a hardware or scaling demonstration.

Uses NumPy/SciPy. No reference coordinates enter decode_one_error().
Distances and axial forces are measured; spring stiffness is calibrated.
The simulator, separately, knows the hidden pristine geometry for scoring.

Run:
    python mechanical_comparator_test.py

Writes mechanical_results.json beside this file.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import least_squares


def edges_complete(n):
    return np.asarray(list(itertools.combinations(range(n), 2)), dtype=int)


def lengths(p, edges):
    return np.linalg.norm(p[edges[:, 0]] - p[edges[:, 1]], axis=1)


def rigidity(p, edges):
    n, d = p.shape
    out = np.zeros((len(edges), n*d))
    for j, (a, b) in enumerate(edges):
        v = p[a] - p[b]
        v = v / np.linalg.norm(v)
        out[j, a*d:(a+1)*d] = v
        out[j, b*d:(b+1)*d] = -v
    return out


def canonicalize_3d(p):
    q = p - p[0]
    e1 = q[1] / np.linalg.norm(q[1])
    e2 = q[2] - np.dot(q[2], e1)*e1
    e2 = e2 / np.linalg.norm(e2)
    e3 = np.cross(e1, e2)
    q = q @ np.column_stack([e1, e2, e3])
    q[0] = 0
    q[1, 1:] = 0
    q[2, 2] = 0
    return q


def free_dofs(n):
    return np.array([3, 6, 7] + list(range(9, 3*n)), dtype=int)


def unpack(x, n):
    p = np.zeros(3*n)
    p[free_dofs(n)] = x
    return p.reshape(n, 3)


def settle(rest, stiffness, load, edges, start):
    """Quasistatic spring truss, six coordinate supports eliminate rigid modes."""
    n = len(start)
    free = free_dofs(n)

    def residual(x):
        p = unpack(x, n)
        force = stiffness*(lengths(p, edges)-rest)
        return (rigidity(p, edges).T @ force)[free] - load

    sol = least_squares(residual, start.ravel()[free], xtol=2e-14,
                        ftol=2e-14, gtol=2e-10, max_nfev=1500)
    if not sol.success or np.linalg.norm(sol.fun) > 1e-5:
        raise RuntimeError("Equilibrium solver did not meet force tolerance")
    return unpack(sol.x, n), float(np.linalg.norm(sol.fun))


def tangent_stiffness(p, rest, stiffness, edges):
    n, dim = p.shape
    out = np.zeros((dim*n, dim*n))
    for kedge, (a, b) in enumerate(edges):
        delta = p[a]-p[b]
        length = np.linalg.norm(delta)
        unit = delta/length
        force = stiffness[kedge]*(length-rest[kedge])
        element = (stiffness[kedge]*np.outer(unit, unit)
                   +force/length*(np.eye(dim)-np.outer(unit, unit)))
        for u, su in [(a, 1), (b, -1)]:
            for v, sv in [(a, 1), (b, -1)]:
                out[dim*u:dim*(u+1), dim*v:dim*(v+1)] += su*sv*element
    free = free_dofs(n)
    return out[np.ix_(free, free)]


def mds_initial(rest, n, edges):
    d2 = np.zeros((n, n))
    d2[edges[:, 0], edges[:, 1]] = rest**2
    d2[edges[:, 1], edges[:, 0]] = rest**2
    j = np.eye(n)-np.ones((n, n))/n
    gram = -0.5*j@d2@j
    vals, vecs = np.linalg.eigh(gram)
    pts = vecs[:, -3:] @ np.diag(np.sqrt(np.maximum(vals[-3:], 1e-14)))
    return canonicalize_3d(pts)


def decode_one_error(measured_rest, n, edges):
    """Existing distance-geometry idea: enumerate one omitted edge and fit.

    Deliberately no pristine positions, pristine lengths, load, or true error
    location in arguments. This local numerical fitting implementation does
    not establish convergence for arbitrary large errors or poor geometries.
    """
    pinit = mds_initial(measured_rest, n, edges)
    xinit = pinit.ravel()[free_dofs(n)]
    scores = []
    for omitted in range(len(edges)):
        keep = np.arange(len(edges)) != omitted

        def residual(x):
            return (lengths(unpack(x, n), edges)-measured_rest)[keep]

        def jacobian(x):
            return rigidity(unpack(x, n), edges)[keep][:, free_dofs(n)]

        sol = least_squares(residual, xinit, jac=jacobian, xtol=1e-13,
                            ftol=1e-13, gtol=1e-13, max_nfev=1000)
        pfit = unpack(sol.x, n)
        scores.append((float(np.linalg.norm(sol.fun)), omitted,
                       lengths(pfit, edges)))
    scores.sort(key=lambda s: s[0])
    score, omitted, decoded = scores[0]
    return {"omitted": omitted, "decoded": decoded,
            "residual": score, "runner_up_residual": scores[1][0]}


def sparse_tangent_distance(p, edges):
    """Minimum support of a nonzero tangent-compatible extension, by rank."""
    b = rigidity(p, edges)
    target_rank = np.linalg.matrix_rank(b, tol=1e-10)
    m = len(edges)
    for k in range(1, m+1):
        for remove in itertools.combinations(range(m), k):
            keep = np.ones(m, dtype=bool)
            keep[list(remove)] = False
            if np.linalg.matrix_rank(b[keep], tol=1e-10) < target_rank:
                return k
    raise RuntimeError("Unreachable")


def reflection_ambiguity():
    """K5 in 2D: exact global one-error ambiguity despite tangent distance 3."""
    p = np.array([[0.2, 0.7], [0., 0.], [1., 0.],
                  [0.4, 1.9], [1.7, -0.4]])
    q = p.copy()
    q[0, 1] *= -1   # reflection across the line through nodes 1 and 2
    edges = edges_complete(5)
    a, b = lengths(p, edges), lengths(q, edges)
    changed = np.flatnonzero(np.abs(a-b) > 1e-11)
    received = a.copy()
    received[changed[0]] = b[changed[0]]
    da = int(np.count_nonzero(np.abs(received-a) > 1e-11))
    db = int(np.count_nonzero(np.abs(received-b) > 1e-11))
    assert len(changed) == 2 and da == db == 1
    return {"changed_edges": edges[changed].tolist(),
            "valid_geometries_distance": len(changed),
            "received_distance_to_first": da,
            "received_distance_to_second": db,
            "tangent_minimum_support": sparse_tangent_distance(p, edges),
            "first_lengths": a.tolist(), "second_lengths": b.tolist(),
            "ambiguous_received_lengths": received.tolist()}


def sensor_and_edm_comparator():
    rng = np.random.default_rng(73014)
    n = 7
    p0 = canonicalize_3d(rng.uniform(-0.7, 0.7, (n, 3)))
    edges = edges_complete(n)
    m = len(edges)
    r0 = lengths(p0, edges)
    k = np.full(m, 20000.)  # N/m; compliant axial spring elements
    b0 = rigidity(p0, edges)
    h0 = null_space(b0.T).T

    # Make an arbitrary imposed dead load; the decoder never receives it.
    loaded = p0.copy().ravel()
    loaded[free_dofs(n)] += rng.normal(0, 0.003, 3*n-6)
    loaded = loaded.reshape(n, 3)
    f0 = k*(lengths(loaded, edges)-r0)
    load = (rigidity(loaded, edges).T@f0)[free_dofs(n)]
    original_loaded, original_residual = settle(r0, k, load, edges, loaded)

    bad_edge = 11
    drift = 0.03
    damaged_rest = r0.copy()
    damaged_rest[bad_edge] += drift
    damaged, equilibrium_residual = settle(damaged_rest, k, load, edges,
                                          original_loaded)
    lm = lengths(damaged, edges)
    fm = k*(lm-damaged_rest)
    estimated_rest = lm-fm/k
    exact = decode_one_error(estimated_rest, n, edges)
    assert exact["omitted"] == bad_edge
    corrected_rest = damaged_rest.copy()
    corrected_rest[bad_edge] += (exact["decoded"][bad_edge]
                                 - estimated_rest[bad_edge])
    repaired, repaired_residual = settle(corrected_rest, k, load, edges,
                                         damaged)

    # Check local stability and mechanical actuation effort along a sampled
    # quasistatic correction path. No electronic or motor losses are included.
    path_lengths = np.linspace(damaged_rest[bad_edge],
                               corrected_rest[bad_edge], 21)
    path_position = damaged.copy()
    path_forces, path_eigenvalues = [], []
    for rest_value in path_lengths:
        path_rest = damaged_rest.copy()
        path_rest[bad_edge] = rest_value
        path_position, _ = settle(path_rest, k, load, edges, path_position)
        path_forces.append(float(k[bad_edge]*(lengths(path_position, edges)[bad_edge]-rest_value)))
        path_eigenvalues.append(float(np.linalg.eigvalsh(
            tangent_stiffness(path_position, path_rest, k, edges))[0]))
    assert min(path_eigenvalues) > 0
    sampled_abs_work = float(np.sum(np.abs(np.diff(path_lengths))
                        *(np.abs(path_forces[:-1])+np.abs(path_forces[1:]))/2))

    # A stated finite noise/calibration experiment, not ideal sensors only.
    length_sigma = 2e-6       # 2 micrometers
    force_sigma = 0.05        # N
    stiffness_rel_sigma = 1e-4
    noisy_l = lm + rng.normal(0, length_sigma, m)
    noisy_f = fm + rng.normal(0, force_sigma, m)
    measured_k = k*(1+rng.normal(0, stiffness_rel_sigma, m))
    noisy_rest = noisy_l-noisy_f/measured_k
    noisy = decode_one_error(noisy_rest, n, edges)
    noisy_corrected_rest = damaged_rest.copy()
    noisy_corrected_rest[noisy["omitted"]] += (
        noisy["decoded"][noisy["omitted"]]-noisy_rest[noisy["omitted"]])
    noisy_repaired, _ = settle(noisy_corrected_rest, k, load, edges, damaged)

    # A single force-channel bias produces exactly the same inferred drift.
    healthy_l = lengths(original_loaded, edges)
    healthy_f = k*(healthy_l-r0)
    biased_f = healthy_f.copy()
    biased_f[bad_edge] -= k[bad_edge]*drift
    false_rest = healthy_l-biased_f/k
    indistinguishable_input = float(np.max(np.abs(false_rest-estimated_rest)))
    assert indistinguishable_input < 1e-12

    # Fixed tangent self-stress projection under healthy finite displacement.
    direction = rng.normal(0, 1, 3*n)
    direction[[0, 1, 2, 4, 5, 8]] = 0
    direction /= np.linalg.norm(direction)
    nonlinear_signal = []
    for amplitude in [0.0001, 0.001, 0.01, 0.1]:
        p = p0+amplitude*direction.reshape(n, 3)
        strain = lengths(p, edges)-r0
        nonlinear_signal.append({"displacement_norm_m": amplitude,
                                 "healthy_syndrome_norm_m": float(np.linalg.norm(h0@strain))})

    return {
        "model": "3D K7,21 calibrated axial springs,6 scalar supports,one drift",
        "decoder_has_original_coordinates": False,
        "nodes": n, "edges": m, "self_stress_dimension": len(h0),
        "true_damaged_edge_index": bad_edge,
        "true_damaged_edge_nodes": edges[bad_edge].tolist(),
        "natural_length_drift_m": drift,
        "unknown_imposed_free_load_norm_N": float(np.linalg.norm(load)),
        "max_abs_member_force_N": float(np.max(np.abs(fm))),
        "max_measured_rest_inversion_error_m": float(np.max(np.abs(estimated_rest-damaged_rest))),
        "exact_decoder_selected_edge": exact["omitted"],
        "exact_decoder_residual_m": exact["residual"],
        "exact_decoder_runner_up_residual_m": exact["runner_up_residual"],
        "exact_repair_rest_error_m": float(np.max(np.abs(corrected_rest-r0))),
        "damaged_geometry_error_m": float(np.linalg.norm(damaged-original_loaded)),
        "exact_repaired_geometry_error_m": float(np.linalg.norm(repaired-original_loaded)),
        "sampled_correction_path_absolute_mechanical_work_J": sampled_abs_work,
        "sampled_correction_path_peak_actuator_force_N": float(np.max(np.abs(path_forces))),
        "sampled_correction_path_min_tangent_eigenvalue_N_per_m": min(path_eigenvalues),
        "actuation_path_samples": len(path_lengths),
        "noise_parameters": {"length_sigma_m": length_sigma,
                             "force_sigma_N": force_sigma,
                             "stiffness_relative_sigma": stiffness_rel_sigma},
        "noisy_decoder_selected_edge": noisy["omitted"],
        "noisy_decoder_residual_m": noisy["residual"],
        "noisy_decoder_runner_up_residual_m": noisy["runner_up_residual"],
        "noisy_repair_rest_error_m": float(np.max(np.abs(noisy_corrected_rest-r0))),
        "noisy_repaired_geometry_error_m": float(np.linalg.norm(noisy_repaired-original_loaded)),
        "one_force_bias_equivalent_drift_inference_difference_m": indistinguishable_input,
        "equilibrium_force_residuals_N": [original_residual,equilibrium_residual,repaired_residual],
        "healthy_nonlinear_false_syndrome": nonlinear_signal,
        "physical_costs_not_simulated": ["sensor electronics and calibration drift",
            "actuator mechanical stiffness,stroke,force,efficiency and backlash",
            "bus/controller power and faults", "thermal gradients", "fatigue",
            "fabrication residual stress", "buckling", "spatial tiling and assembly"],
        "scope": "One reproducible modeled case; no global numerical convergence or scalable hardware claim."
    }


def main():
    result = {"reflection_counterexample": reflection_ambiguity(),
              "existing_components_comparator": sensor_and_edm_comparator()}
    out = Path(__file__).with_name("mechanical_results.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
