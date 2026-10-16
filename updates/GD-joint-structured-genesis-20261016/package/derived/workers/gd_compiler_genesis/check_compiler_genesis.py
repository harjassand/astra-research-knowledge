#!/usr/bin/env python3
"""Independent finite checks; NumPy and Python stdlib only.

This does not import or execute a supplied scientific script.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(2026101607)


def opnorm(a):
    return float(np.linalg.norm(a, 2))


def adj(a):
    return a.conj().T


def dissipator(a, x):
    aa = adj(a) @ a
    return a @ x @ adj(a) - (aa @ x + x @ aa) / 2


def edge(u, v, z, x):
    r = adj(v) @ u
    s = z * r + z.conjugate() * adj(r)
    return z * u @ x @ adj(v) + z.conjugate() * v @ x @ adj(u) - (s @ x + x @ s) / 2


def matrix_units(d):
    for i in range(d):
        for j in range(d):
            x = np.zeros((d, d), complex)
            x[i, j] = 1
            yield x


def map_error(left, right, d):
    return max(float(np.max(np.abs(left(x) - right(x)))) for x in matrix_units(d))


def choi(action, d):
    out = np.zeros((d * d, d * d), complex)
    for i in range(d):
        for j in range(d):
            x = np.zeros((d, d), complex)
            x[i, j] = 1
            out += np.kron(action(x), x) / d
    return out


def random_unitary(d):
    a = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    q, r = np.linalg.qr(a)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q @ np.diag(phases.conjugate())


def unitary_dictionary(a):
    """A = norm(A) (U1+U2)/2 using a full SVD polar extension."""
    norm = opnorm(a)
    if norm == 0:
        return 0.0, (np.eye(len(a)), np.eye(len(a)))
    left, sing, right_h = np.linalg.svd(a / norm, full_matrices=True)
    sing = np.clip(sing, 0, 1)
    polar = left @ right_h
    right = adj(right_h)
    v = right @ np.diag(sing + 1j * np.sqrt(np.maximum(0, 1 - sing * sing))) @ right_h
    return norm, (polar @ v, polar @ adj(v))


def generic_edge_kraus(u, v, z, m):
    t = abs(z)
    phase = z / t if t else 1
    r = adj(v) @ u
    ident = np.eye(len(u), dtype=complex)
    return [
        np.sqrt(max(0, (m + t) / 2)) * (u + phase.conjugate() * v),
        np.sqrt(max(0, (m - t) / 2)) * (u - phase.conjugate() * v),
        np.sqrt(m / 2) * r - z.conjugate() / np.sqrt(2 * m) * ident,
        np.sqrt(m / 2) * adj(r) - z / np.sqrt(2 * m) * ident,
        np.sqrt(max(0, m - t * t / m)) * ident,
    ]


def pair_floor(u, v, m, x):
    r = adj(v) @ u
    return m * (dissipator(u, x) + dissipator(v, x)) + m / 2 * (dissipator(r, x) + dissipator(adj(r), x))


def kraus_generator(ks, rate, x):
    return sum((k @ x @ adj(k) for k in ks), np.zeros_like(x)) - rate * x


def pauli_edge_kraus(p, q, r, omega, z, h, m, u):
    t = abs(z)
    phase = z / t if t else 1
    a = float(np.real(z * omega))
    gamma = float(np.hypot(m, u))
    rate = 2 * m + 2 * gamma
    ident = np.eye(len(p), dtype=complex)
    ks = [
        np.sqrt(max(0, (m + t) / 2)) * (p + phase.conjugate() * q),
        np.sqrt(max(0, (m - t) / 2)) * (p - phase.conjugate() * q),
        np.sqrt(gamma) * r + (-a + 1j * h) / np.sqrt(gamma) * ident,
        np.sqrt(max(0, gamma - (a * a + h * h) / gamma)) * ident,
    ]
    return ks, rate, gamma


def kron_all(items):
    out = np.array([[1]], complex)
    for item in items:
        out = np.kron(out, item)
    return out


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)


def run():
    started = time.perf_counter()
    results = {}
    errs = []
    unit_errs = []
    for d in (2, 4, 8):
        for rank in (0, 1, d):
            a = random_unitary(d) @ np.diag(np.r_[RNG.uniform(.1, 1, rank), np.zeros(d - rank)]) @ random_unitary(d)
            norm, us = unitary_dictionary(a)
            errs.append(float(np.max(np.abs(a - norm * (us[0] + us[1]) / 2))))
            unit_errs.extend(opnorm(adj(u) @ u - np.eye(d)) for u in us)
    results["two_unitary_polar"] = {"cases": 9, "reconstruction_max": max(errs), "unitarity_max": max(unit_errs)}

    errs = []
    scalar_errs = []
    eigmins = []
    for d in (2, 4, 8):
        for j in range(8):
            u, v = random_unitary(d), random_unitary(d)
            m = .07
            z = 0 if j == 2 else m * (1 if j in (0, 1) else RNG.uniform()) * np.exp(1j * RNG.uniform(-np.pi, np.pi))
            ks = generic_edge_kraus(u, v, z, m)
            rate = 4 * m
            scalar_errs.append(opnorm(sum((adj(k) @ k for k in ks), np.zeros_like(u)) - rate * np.eye(d)))
            errs.append(map_error(lambda x: kraus_generator(ks, rate, x), lambda x: edge(u, v, z, x) + pair_floor(u, v, m, x), d))
            cp = choi(lambda x: sum((k @ x @ adj(k) for k in ks), np.zeros_like(x)) / rate, d)
            eigmins.append(float(np.linalg.eigvalsh(cp)[0]))
    results["generic_unitary_edge"] = {"cases": 24, "map_max": max(errs), "scalar_rate_max": max(scalar_errs), "choi_min": min(eigmins)}

    # One nominal partial-isometry correction and three fixed error elements.
    pi = (np.eye(4) + np.kron(Z, Z)) / 2
    j_nom = .6 * np.kron(X, I) @ pi
    atoms = [np.kron(I, Y) @ pi, np.kron(Z, X) @ (np.eye(4) - pi), (np.kron(X, Z) + .3j * np.kron(Y, I)) / 1.3]
    bounds = np.array([.012, .009, .007])
    dict_ops = []
    nominal = []
    envelopes = []
    nominal_norm, nominal_us = unitary_dictionary(j_nom)
    dict_ops.extend(nominal_us)
    nominal.extend([nominal_norm / 2] * 2)
    envelopes.extend([0.0] * 2)
    atom_norms = []
    for a, bnd in zip(atoms, bounds):
        norm, us = unitary_dictionary(a)
        atom_norms.append(norm)
        dict_ops.extend(us)
        nominal.extend([0.0] * 2)
        envelopes.extend([bnd * norm / 2] * 2)
    nominal = np.array(nominal, complex)
    envelopes = np.array(envelopes)
    mtx = np.outer(np.abs(nominal), envelopes) + np.outer(envelopes, np.abs(nominal))
    eps = float(np.dot(bounds, atom_norms))
    rate = float(2 * mtx.sum() + eps * eps)
    ceiling = 4 * nominal_norm * eps + eps * eps
    floor_functions = []
    for a in range(len(dict_ops)):
        if mtx[a, a]:
            floor_functions.append(("diag", a, a, float(mtx[a, a])))
        for b in range(a + 1, len(dict_ops)):
            if mtx[a, b]:
                floor_functions.append(("pair", a, b, float(mtx[a, b])))
    def fixed_floor(x):
        out = np.zeros_like(x)
        for kind, a, b, m in floor_functions:
            out += m * dissipator(dict_ops[a], x) if kind == "diag" else pair_floor(dict_ops[a], dict_ops[b], m, x)
        for a in range(len(dict_ops)):
            for b in range(a + 1, len(dict_ops)):
                m = envelopes[a] * envelopes[b]
                if m:
                    r = adj(dict_ops[b]) @ dict_ops[a]
                    out += m / 2 * (dissipator(r, x) + dissipator(adj(r), x))
        return out
    replacement_errs = []
    replacement_scalar_errs = []
    replacement_choi_mins = []
    cmin = []
    floor_hashes = []
    for case in range(16):
        deltas = np.zeros(3, complex) if case == 0 else bounds * (np.ones(3) if case == 1 else RNG.uniform(size=3)) * np.exp(1j * RNG.uniform(-np.pi, np.pi, 3))
        delta_op = sum((delta * a for delta, a in zip(deltas, atoms)), np.zeros((4, 4), complex))
        dcoef = np.zeros_like(nominal)
        for pos, (delta, norm) in enumerate(zip(deltas, atom_norms)):
            dcoef[2 + 2 * pos:4 + 2 * pos] = delta * norm / 2
        cross_c = np.outer(nominal, dcoef.conjugate()) + np.outer(dcoef, nominal.conjugate())
        c = cross_c + np.outer(dcoef, dcoef.conjugate())
        cmin.append(float(np.linalg.eigvalsh(c)[0]))
        assert np.max(np.abs(cross_c) - mtx) < 1e-14
        ks = []
        for kind, a, b, m in floor_functions:
            if kind == "diag":
                value = float(cross_c[a, a].real)
                ks.extend([np.sqrt(max(0, m + value)) * dict_ops[a], np.sqrt(max(0, m - value)) * np.eye(4)])
            else:
                ks.extend(generic_edge_kraus(dict_ops[a], dict_ops[b], cross_c[a, b], m))
        psd_actual_rate = float(np.sum(np.abs(dcoef) ** 2))
        ks.append(delta_op)
        for a in range(len(dict_ops)):
            for b in range(a + 1, len(dict_ops)):
                m = envelopes[a] * envelopes[b]
                if m:
                    z = dcoef[a] * dcoef[b].conjugate()
                    ks.extend(generic_edge_kraus(dict_ops[a], dict_ops[b], z, m)[2:4])
                    psd_actual_rate += m + abs(z) ** 2 / m
        assert psd_actual_rate <= eps * eps + 1e-14
        ks.append(np.sqrt(max(0, eps * eps - psd_actual_rate)) * np.eye(4))
        target = lambda x: fixed_floor(x) + dissipator(j_nom + delta_op, x) - dissipator(j_nom, x)
        replacement_errs.append(map_error(lambda x: kraus_generator(ks, rate, x), target, 4))
        replacement_scalar_errs.append(opnorm(sum((adj(k) @ k for k in ks), np.zeros((4, 4), complex)) - rate * np.eye(4)))
        cp = choi(lambda x: x + target(x) / rate, 4)
        replacement_choi_mins.append(float(np.linalg.eigvalsh(cp)[0]))
        floor_hashes.append(hashlib.sha256(choi(fixed_floor, 4).tobytes()).hexdigest())
    # Explicit correction dictionary without an SVD.
    v = pi + 1j * (np.eye(4) - pi)
    explicit_error = opnorm(np.kron(X, I) @ pi - (np.kron(X, I) @ v + np.kron(X, I) @ adj(v)) / 2)
    completed_kraus = [np.kron(X, I) @ pi, np.eye(4) - pi]
    completion_error = opnorm(sum((adj(k) @ k for k in completed_kraus), np.zeros((4, 4), complex)) - np.eye(4))
    results["signed_jump_replacement"] = {"cases": 16, "dictionary_size": len(dict_ops), "epsilon": eps, "nominal_norm": nominal_norm, "fixed_rate": rate, "bound": ceiling, "earlier_pairwise_rate_bound": 4 * nominal_norm * eps + 2 * eps * eps, "map_max": max(replacement_errs), "scalar_rate_max": max(replacement_scalar_errs), "choi_min": min(replacement_choi_mins), "signed_C_min": min(cmin), "same_floor_all_cases": len(set(floor_hashes)) == 1, "explicit_projector_dictionary_error": explicit_error, "ideal_completed_channel_error": completion_error, "PSD_piece_support": "Union of the whole fixed error dictionary"}

    pair_cases = [(X, Y, Z, -1j), (np.kron(X, I), np.kron(I, Z), np.kron(X, Z), 1)]
    errs, scalar_errs, minima, trace_norms, desired_trace_norms = [], [], [], [], []
    for p, q, r, omega in pair_cases:
        d = len(p)
        m, hbound = .03, .02
        for n in range(10):
            z = (m / omega) if n == 0 else m * RNG.uniform() * np.exp(1j * RNG.uniform(-np.pi, np.pi))
            h = hbound if n == 0 else RNG.uniform(-hbound, hbound)
            ks, rate, gamma = pauli_edge_kraus(p, q, r, omega, z, h, m, hbound)
            target = lambda x: edge(p, q, z, x) + m * (dissipator(p, x) + dissipator(q, x)) + gamma * dissipator(r, x) - 1j * h * (r @ x - x @ r)
            errs.append(map_error(lambda x: kraus_generator(ks, rate, x), target, d))
            scalar_errs.append(opnorm(sum((adj(k) @ k for k in ks), np.zeros((d, d), complex)) - rate * np.eye(d)))
            minima.append(float(np.linalg.eigvalsh(choi(lambda x: x + target(x) / rate, d))[0]))
            if n == 0:
                je = choi(lambda x: edge(p, q, z, x) - 1j * h * (r @ x - x @ r), d)
                trace_norms.append(float(np.sum(np.abs(np.linalg.eigvalsh(je)))))
                desired_trace_norms.append(rate)
    results["sharp_pauli_edge_product_H"] = {"cases": 20, "map_max": max(errs), "scalar_rate_max": max(scalar_errs), "choi_min": min(minima), "boundary_choi_trace_norms": trace_norms, "optimal_uniform_rates": desired_trace_norms}

    affine_errs, affine_scalar_errs, affine_mins, affine_rates = [], [], [], []
    for p, q, r, omega in pair_cases:
        d = len(p)
        for a, epsilon in ((.6, .02), (.3, .3), (.2, .4), (0, .3)):
            uniform_rate = 4 * a * epsilon if epsilon <= a else (a + epsilon) ** 2
            affine_rates.append(uniform_rate)
            for sample in range(6):
                delta = epsilon * omega if sample == 0 else 0 if sample == 1 else epsilon * RNG.uniform() * np.exp(1j * RNG.uniform(-np.pi, np.pi))
                ident = np.eye(d)
                if a == 0:
                    ks = [delta * q, np.sqrt(max(0, epsilon * epsilon - abs(delta) ** 2)) * ident]
                    floor = lambda x: np.zeros_like(x)
                else:
                    m = a * epsilon
                    alpha, beta = (m, m - epsilon * epsilon) if epsilon <= a else (a * a, 0)
                    z, t = a * delta.conjugate(), abs(delta) ** 2
                    c = float(np.real(z * omega))
                    ks = [np.sqrt(alpha) * p + z.conjugate() / np.sqrt(alpha) * q, np.sqrt(max(0, beta + t - abs(z) ** 2 / alpha)) * q, np.sqrt(m) * r - c / np.sqrt(m) * ident, np.sqrt(max(0, uniform_rate - alpha - beta - t - m - c * c / m)) * ident]
                    floor = lambda x: alpha * dissipator(p, x) + beta * dissipator(q, x) + m * dissipator(r, x)
                target = lambda x: floor(x) + dissipator(a * p + delta * q, x) - dissipator(a * p, x)
                affine_errs.append(map_error(lambda x: kraus_generator(ks, uniform_rate, x), target, d))
                affine_scalar_errs.append(opnorm(sum((adj(k) @ k for k in ks), np.zeros((d, d), complex)) - uniform_rate * ident))
                affine_mins.append(float(np.linalg.eigvalsh(choi(lambda x: x + target(x) / uniform_rate, d))[0]))
    results["sharp_affine_Pauli_replacement"] = {"cases": len(affine_errs), "regimes": "epsilon<a, epsilon=a, epsilon>a, a=0; realized delta=0 included", "map_max": max(affine_errs), "scalar_rate_max": max(affine_scalar_errs), "choi_min": min(affine_mins), "uniform_rates_by_family": affine_rates, "epsilon_zero_case": "delta is identically zero; no floor or clock is needed"}

    # Graph theorem: four independent commuting Z generators, arbitrary graph.
    nvertices = 4
    ps = [kron_all([Z if j == i else I for j in range(nvertices)]) for i in range(nvertices)]
    graph = [(0, 1, .011, .004), (0, 2, .008, .006), (1, 2, .014, .002), (1, 3, .009, .005), (2, 3, .007, .003)]
    graph_rate = sum(2 * m + 2 * np.hypot(m, u) for _, _, m, u in graph)
    graph_old_rate = sum(4 * m + 2 * u for _, _, m, u in graph)
    d = 2 ** nvertices
    products = [ps[i] @ ps[j] for i, j, _, _ in graph]
    def graph_floor(x):
        out = np.zeros_like(x)
        for (i, j, m, u), r in zip(graph, products):
            out += m * (dissipator(ps[i], x) + dissipator(ps[j], x)) + np.hypot(m, u) * dissipator(r, x)
        return out
    graph_mins = []
    for sample in range(8):
        zs = [m if sample == 0 else m * RNG.uniform() * np.exp(1j * RNG.uniform(-np.pi, np.pi)) for _, _, m, _ in graph]
        hs = [u if sample == 0 else RNG.uniform(-u, u) for _, _, _, u in graph]
        def action(x):
            out = graph_floor(x)
            for (i, j, _, _), r, z, h in zip(graph, products, zs, hs):
                out += edge(ps[i], ps[j], z, x) - 1j * h * (r @ x - x @ r)
            return out
        # Only 10-dimensional exact catalog block is needed for positivity.
        vertices = len(ps)
        edges = len(graph)
        block = np.zeros((1 + vertices + edges, 1 + vertices + edges), complex)
        product_gammas = np.array([np.hypot(m, u) for _, _, m, u in graph])
        row_gammas = np.zeros(vertices)
        for (i, j, m, _), z in zip(graph, zs):
            row_gammas[i] += m
            row_gammas[j] += m
            block[1 + i, 1 + j] = z
            block[1 + j, 1 + i] = z.conjugate()
        for i in range(vertices):
            block[1 + i, 1 + i] = row_gammas[i]
        for k, (gamma, z, h) in enumerate(zip(product_gammas, zs, hs)):
            pos = 1 + vertices + k
            block[pos, pos] = gamma
            block[pos, 0] = -z.real - 1j * h
            block[0, pos] = -z.real + 1j * h
        block[0, 0] = graph_rate - row_gammas.sum() - product_gammas.sum()
        graph_mins.append(float(np.linalg.eigvalsh(block)[0]))
        if sample == 0:
            catalog = [np.eye(d)] + ps + products
            vectors = np.column_stack([a.reshape(-1) / np.sqrt(d) for a in catalog])
            expected = vectors @ block @ adj(vectors)
            actual = choi(lambda x: graph_rate * x + action(x), d)
            graph_choi_error = float(np.max(np.abs(expected - actual)))
    results["sharp_graph"] = {"vertices": nvertices, "edges": len(graph), "samples": 8, "optimal_rate": float(graph_rate), "separate_source_rate": float(graph_old_rate), "catalog_choi_error": graph_choi_error, "catalog_min": min(graph_mins)}

    # Collision-free graph with genuinely noncommuting original labels.
    mixed_ps = [np.kron(X, I), np.kron(Z, I), np.kron(I, X), np.kron(I, Z)]
    mixed_products, omegas = [], []
    for i, j, _, _ in graph:
        qp = mixed_ps[j] @ mixed_ps[i]
        omega = 1 if opnorm(qp - adj(qp)) < 1e-12 else 1j
        mixed_products.append(qp / omega)
        omegas.append(omega)
    mixed_map_errs, mixed_scalar_errs, mixed_choi_mins, mixed_catalog_errs = [], [], [], []
    for sample in range(8):
        zs = [m / omega if sample == 0 else m * RNG.uniform() * np.exp(1j * RNG.uniform(-np.pi, np.pi)) for (_, _, m, _), omega in zip(graph, omegas)]
        hs = [u if sample == 0 else RNG.uniform(-u, u) for _, _, _, u in graph]
        ks = []
        for (i, j, m, u), r, omega, z, h in zip(graph, mixed_products, omegas, zs, hs):
            pair_ks, _, _ = pauli_edge_kraus(mixed_ps[i], mixed_ps[j], r, omega, z, h, m, u)
            ks.extend(pair_ks)
        def mixed_action(x):
            out = np.zeros_like(x)
            for (i, j, m, u), r, z, h in zip(graph, mixed_products, zs, hs):
                out += m * (dissipator(mixed_ps[i], x) + dissipator(mixed_ps[j], x)) + np.hypot(m, u) * dissipator(r, x)
                out += edge(mixed_ps[i], mixed_ps[j], z, x) - 1j * h * (r @ x - x @ r)
            return out
        mixed_map_errs.append(map_error(lambda x: kraus_generator(ks, graph_rate, x), mixed_action, 4))
        mixed_scalar_errs.append(opnorm(sum((adj(k) @ k for k in ks), np.zeros((4, 4), complex)) - graph_rate * np.eye(4)))
        actual = choi(lambda x: graph_rate * x + mixed_action(x), 4)
        mixed_choi_mins.append(float(np.linalg.eigvalsh(actual)[0]))
        catalog = [np.eye(4)] + mixed_ps + mixed_products
        vectors = np.column_stack([a.reshape(-1) / 2 for a in catalog])
        block = np.zeros((1 + len(mixed_ps) + len(graph),) * 2, complex)
        row_gammas = np.zeros(4)
        gammas = [np.hypot(m, u) for _, _, m, u in graph]
        for (i, j, m, _), z in zip(graph, zs):
            row_gammas[i] += m
            row_gammas[j] += m
            block[1 + i, 1 + j] = z
            block[1 + j, 1 + i] = z.conjugate()
        for i, value in enumerate(row_gammas):
            block[1 + i, 1 + i] = value
        for e, (gamma, omega, z, h) in enumerate(zip(gammas, omegas, zs, hs)):
            pos = 5 + e
            block[pos, pos] = gamma
            block[pos, 0] = -np.real(omega * z) - 1j * h
            block[0, pos] = -np.real(omega * z) + 1j * h
        block[0, 0] = graph_rate - sum(row_gammas) - sum(gammas)
        mixed_catalog_errs.append(float(np.max(np.abs(actual - vectors @ block @ adj(vectors)))))
    results["sharp_noncommuting_graph"] = {"samples": 8, "anticommuting_edges": sum(omega == 1j for omega in omegas), "map_max": max(mixed_map_errs), "scalar_rate_max": max(mixed_scalar_errs), "choi_min": min(mixed_choi_mins), "catalog_choi_error": max(mixed_catalog_errs)}

    # Missing direction remains an obstruction; arbitrary unknown norm directions
    # were not smuggled into the unitary dictionary.
    h = .01
    two_z = np.kron(Z, Z)
    one_body_floor = lambda x: .05 * sum((dissipator(p, x) for p in [np.kron(X, I), np.kron(Y, I), np.kron(Z, I), np.kron(I, X), np.kron(I, Y), np.kron(I, Z)]), np.zeros_like(x))
    obstruction = []
    for rate in (1, 10, 100):
        obstruction.append(float(np.linalg.eigvalsh(choi(lambda x: x + (one_body_floor(x) - 1j * h * (two_z @ x - x @ two_z)) / rate, 4))[0]))
    results["missing_direction_control"] = {"choi_min_at_rates_1_10_100": obstruction}

    results["resource_receipt"] = {"python": sys.version, "numpy": np.__version__, "platform": platform.platform(), "seed": 2026101607, "wall_seconds": time.perf_counter() - started, "installed_packages": False, "producer_scripts_executed": False, "precision": "IEEE double; analytic proofs carry the general claims"}
    results["all_checks_pass"] = bool(
        results["two_unitary_polar"]["reconstruction_max"] < 1e-12
        and results["two_unitary_polar"]["unitarity_max"] < 1e-12
        and results["generic_unitary_edge"]["map_max"] < 1e-12
        and results["generic_unitary_edge"]["scalar_rate_max"] < 1e-12
        and results["generic_unitary_edge"]["choi_min"] > -1e-12
        and results["signed_jump_replacement"]["map_max"] < 1e-12
        and results["signed_jump_replacement"]["scalar_rate_max"] < 1e-12
        and results["signed_jump_replacement"]["choi_min"] > -1e-12
        and results["signed_jump_replacement"]["same_floor_all_cases"]
        and explicit_error < 1e-12
        and completion_error < 1e-12
        and abs(results["signed_jump_replacement"]["fixed_rate"] - ceiling) < 1e-12
        and results["sharp_pauli_edge_product_H"]["map_max"] < 1e-12
        and results["sharp_pauli_edge_product_H"]["scalar_rate_max"] < 1e-12
        and results["sharp_pauli_edge_product_H"]["choi_min"] > -1e-12
        and max(abs(a - b) for a, b in zip(trace_norms, desired_trace_norms)) < 1e-12
        and max(affine_errs) < 1e-12
        and max(affine_scalar_errs) < 1e-12
        and min(affine_mins) > -1e-12
        and graph_choi_error < 1e-12
        and min(graph_mins) > -1e-12
        and max(mixed_map_errs) < 1e-12
        and max(mixed_scalar_errs) < 1e-12
        and min(mixed_choi_mins) > -1e-12
        and max(mixed_catalog_errs) < 1e-12
        and all(value < 0 for value in obstruction)
    )
    destination = HERE / "CHECKS.json"
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0 if results["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(run())
