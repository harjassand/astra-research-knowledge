#!/usr/bin/env python3
"""Finite tests for boundary-jet cancellation and conservative return registers.

Only NumPy is required. These are mechanism/counterexample tests, not a proof of
efficient simulation of interacting many-body systems. No tensor-network rank
or acquired quantum samples are supplied to any test.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


OUT = Path(__file__).resolve().parent


def evolve_hermitian(h: np.ndarray, t: float) -> np.ndarray:
    e, v = np.linalg.eigh(h)
    return (v * np.exp(-1j * t * e)) @ v.conj().T


def pauli_product(p: tuple[int, int], q: tuple[int, int]):
    x, z = p
    u, v = q
    r = (x ^ u, z ^ v)
    phase = (
        (x & z).bit_count()
        + (u & v).bit_count()
        - (r[0] & r[1]).bit_count()
        + 2 * (z & u).bit_count()
    ) % 4
    return r, (1, 1j, -1, -1j)[phase]


def commutator_action(h, a):
    """Exact integer coefficients for i[H,A] with integer Pauli H,A."""
    out = {}
    for p, hp in h.items():
        for q, aq in a.items():
            if (((p[0] & q[1]).bit_count() + (p[1] & q[0]).bit_count()) % 2) == 0:
                continue
            r, phase = pauli_product(p, q)
            factor = 2j * phase
            assert factor.imag == 0
            out[r] = out.get(r, 0) + int(factor.real) * hp * aq
    return {p: c for p, c in out.items() if c}


def product_zero_readout(a):
    return sum(c for (x, _z), c in a.items() if x == 0)


def jet_collision_test():
    # H=X_0/2, rho=|00><00|, R=Z_0-Z_1.  The first two boundary
    # derivatives vanish, but F_R(pi)=-2. Integer H'=2H is used below.
    h_twice = {(1, 0): 1}
    r = {(0, 1): 1, (0, 2): -1}
    jets = []
    a = r
    for k in range(7):
        jets.append(product_zero_readout(a) / (2**k))
        a = commutator_action(h_twice, a)
    assert jets[:2] == [0.0, 0.0]
    assert jets[2] == -1.0
    short = []
    for tau in (0.05, 0.1, 0.2):
        # For two-site support s=2, Delta=1, J=1/2, g=1, ||R||<=2.
        certified_bound = 2 * ((1 - tau) ** -2 - 1 - 2 * tau)
        error = abs(math.cos(tau) - 1)
        assert error <= certified_bound + 1e-13
        short.append({"tau": tau, "actual_error": error, "jet_tail_bound": certified_bound})
    return {
        "description": "Different Pauli strings share two boundary jets but differ later",
        "boundary_derivatives_k_0_to_6": jets,
        "short_horizon_certificates": short,
        "error_at_pi_if_the_jet_collision_is_treated_as_exact": 2.0,
    }


def jet_tail_sampler_test(samples=200000, tau=0.2, seed=20261014):
    """Unbiased tail-path construction specialized to the jet collision above.

    The mathematical distribution has infinite support. The implementation
    draws k=2,...,80; its discarded probability and resulting bias are bounded
    and recorded, rather than calling this floating implementation exact.
    """
    rng = np.random.default_rng(seed)
    orders = np.arange(2, 81)
    weights = (orders + 1) * tau**orders
    tail = (1 - tau) ** -2 - 1 - 2 * tau
    represented_mass = float(weights.sum())
    omitted_envelope = max(0.0, tail - represented_mass)
    # Closed geometric-tail formula avoids subtractive cancellation when
    # calculating the genuinely omitted (k>=81) mass.
    first_omitted = 81
    omitted_exact_formula = tau**first_omitted * ((first_omitted + 1) / (1 - tau) + tau / (1 - tau)**2)
    order_indices = rng.choice(len(orders), size=samples, p=weights / represented_mass)
    k = orders[order_indices]
    chooses_z0 = rng.integers(0, 2, samples).astype(bool)
    values = np.zeros(samples)
    for order in np.unique(k):
        if order % 2:
            continue
        select = chooses_z0 & (k == order)
        # The actual commutator path on Z_0 has |derivative|=1; Z_1
        # commutes with H and yields a zero path. Importance sampling uses
        # the conservative s=2 envelope rather than presupposing this.
        pk = (order + 1) * tau**order / represented_mass
        values[select] = 2 * (-1)**(order // 2) * tau**order / math.factorial(int(order)) / pk
    estimate = float(values.mean())
    standard_error = float(values.std(ddof=1) / math.sqrt(samples))
    exact = math.cos(tau) - 1
    bias_bound = 2 * omitted_exact_formula
    assert abs(estimate - exact) <= 6 * standard_error + bias_bound
    assert max(abs(values)) <= 2 * tail + 1e-12
    return {
        "samples": samples,
        "seed": seed,
        "tau": tau,
        "estimate": estimate,
        "exact": exact,
        "standard_error": standard_error,
        "certified_absolute_sample_envelope": 2 * tail,
        "finite_order_truncation_bias_bound": bias_bound,
        "interpretation": "Boundary-jet removal can be corrected by a local signed tail sampler with an explicit variation bound; no full-state evolution is used.",
    }


def commutator_growth_test(n=12, steps=12):
    # Tilted-field Ising, exact integer coefficients. Overall energy scale
    # has no effect on the reported support cardinalities.
    h = {(0, (1 << j) | (1 << (j + 1))): 10 for j in range(n - 1)}
    h.update({(1 << j, 0): 7 for j in range(n)})
    h.update({(0, 1 << j): 3 for j in range(n)})
    a = {(0, 1): 1}
    rows = []
    for k in range(steps + 1):
        rows.append(
            {
                "derivative_order": k,
                "nonzero_exact_Pauli_coefficients": len(a),
                "largest_Pauli_weight": max(((p[0] | p[1]).bit_count() for p in a), default=0),
                "nonzero_zero_product_readout_terms": sum(p[0] == 0 for p in a),
            }
        )
        a = commutator_action(h, a)
    return {"n": n, "rows": rows, "interpretation": "A scalar moment list hides increasing exact acquisition work; finite counts are not an asymptotic lower bound."}


def engineered_xy_test(n=64):
    # This explicit h is the one-particle restriction of a local XY spin
    # Hamiltonian with every bond norm <=1. No 2**n state is constructed.
    j = np.arange(1, n, dtype=float)
    b = 2 * np.sqrt(j * (n - j)) / n
    h = np.diag(b, 1) + np.diag(b, -1)
    revival = math.pi * n / 2
    occupations = (np.arange(n) % 2 == 0).astype(float)
    rows = []
    for fraction in (0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1):
        t = fraction * revival
        u = evolve_hermitian(h, t)
        probability = abs(u[0, 0]) ** 2
        expected_probability = abs(math.cos(2 * t / n)) ** (2 * (n - 1))
        assert abs(probability - expected_probability) < 1e-12
        correlation = (u * occupations) @ u.conj().T
        block = correlation[: n // 2, : n // 2]
        lam = np.clip(np.linalg.eigvalsh(block).real, 1e-15, 1 - 1e-15)
        entropy_bits = -np.sum(lam * np.log2(lam) + (1 - lam) * np.log2(1 - lam))
        local_number = correlation[0, 0].real
        expected_number = (1 + math.cos(4 * t / n) ** (n - 1)) / 2
        assert abs(local_number - expected_number) < 1e-12
        rows.append(
            {
                "time_over_revival": fraction,
                "one_excitation_return_probability": float(probability),
                "neel_initial_local_number": float(local_number),
                "neel_initial_half_chain_entropy_bits": float(entropy_bits),
            }
        )
    quarter = rows[2]
    assert abs(quarter["neel_initial_half_chain_entropy_bits"] - n / 2) < 1e-9
    assert rows[-1]["one_excitation_return_probability"] > 1 - 1e-12
    return {
        "n": n,
        "max_bond_operator_norm": float(b.max()),
        "revival_time": revival,
        "quiet_window_one_excitation_upper_bound": 2.0 ** (-(n - 1)),
        "rows": rows,
        "interpretation": "Bounded nearest-neighbor autonomous dynamics has an exponentially quiet local window then a unit revival. A second product input simultaneously shows maximal volume-law entanglement and polynomial local-observable acquisition through known quadratic closure.",
    }


def moment_adversary_test(m=7):
    # The m-site truncation and (m+1)-site chain have equal endpoint moments
    # through degree 2m-1. A path must cross the missing edge and return.
    full = np.diag(np.ones(m), 1) + np.diag(np.ones(m), -1)
    cut = full[:m, :m]
    p_full = np.eye(m + 1)
    p_cut = np.eye(m)
    rows = []
    for k in range(2 * m + 2):
        delta = float(p_full[0, 0] - p_cut[0, 0])
        rows.append({"order": k, "full_moment": float(p_full[0, 0]), "cut_moment": float(p_cut[0, 0]), "difference": delta})
        if k < 2 * m:
            assert delta == 0
        if k == 2 * m:
            assert delta == 1
        p_full = p_full @ full
        p_cut = p_cut @ cut
    sample = np.linspace(0, 4 * m, 2001)
    ef, vf = np.linalg.eigh(full)
    ec, vc = np.linalg.eigh(cut)
    af = np.exp(-1j * np.outer(sample, ef)) @ abs(vf[0, :]) ** 2
    ac = np.exp(-1j * np.outer(sample, ec)) @ abs(vc[0, :]) ** 2
    error = np.abs(af - ac)
    worst = int(np.argmax(error))
    return {
        "cut_size": m,
        "moments": rows,
        "max_sampled_return_amplitude_difference": float(error[worst]),
        "time_of_max_sampled_difference": float(sample[worst]),
        "time_grid_max": float(sample[-1]),
        "interpretation": "Matching finitely many return moments does not certify long-time invisibility.",
    }


def orthonormal_span(columns, tolerance=1e-12):
    q = []
    for column in columns.T:
        x = column.astype(complex).copy()
        for _ in range(2):
            for v in q:
                x -= v * np.vdot(v, x)
        norm = np.linalg.norm(x)
        if norm > tolerance:
            q.append(x / norm)
    return np.column_stack(q) if q else np.zeros((columns.shape[0], 0), complex)


def phase_register_test(dimension=21, boundary_size=2, blocks=4, seed=20261013):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    full = (z + z.conj().T) / (4 * math.sqrt(dimension))
    b = full[:boundary_size, :boundary_size]
    c = full[boundary_size:, :boundary_size]
    d = full[boundary_size:, boundary_size:]
    columns = []
    power = c.copy()
    for _ in range(blocks):
        columns.append(power)
        power = d @ power
    v = orthonormal_span(np.column_stack(columns))
    dm = v.conj().T @ d @ v
    cm = v.conj().T @ c
    phase_full = np.block([[b, cm.conj().T], [cm, dm]])
    assert np.linalg.norm(phase_full - phase_full.conj().T) < 1e-12
    errors = []
    pf = np.eye(d.shape[0], dtype=complex)
    pm = np.eye(dm.shape[0], dtype=complex)
    for k in range(2 * blocks):
        error = np.linalg.norm(c.conj().T @ pf @ c - cm.conj().T @ pm @ cm)
        errors.append(float(error))
        assert error < 1e-10
        pf = pf @ d
        pm = pm @ dm
    em, vm = np.linalg.eigh(dm)
    residues = [(vm[:, j].conj() @ cm).conj()[:, None] @ (vm[:, j].conj() @ cm)[None, :] for j in range(len(em))]
    min_eigenvalue = min(float(np.linalg.eigvalsh(w).min()) for w in residues)
    assert min_eigenvalue > -1e-12
    rows = []
    lam = max(abs(np.linalg.eigvalsh(d)))
    for t in (0.1, 0.5, 1, 3, 7):
        k = c.conj().T @ evolve_hermitian(d, t) @ c
        km = cm.conj().T @ evolve_hermitian(dm, t) @ cm
        kernel_error = float(np.linalg.norm(k - km, ord=2))
        bound = 2 * np.linalg.norm(c, ord=2) ** 2 * (lam * t) ** (2 * blocks) / math.factorial(2 * blocks)
        assert kernel_error <= bound + 1e-12
        xfull = evolve_hermitian(full, t)[:boundary_size, 0]
        xphase = evolve_hermitian(phase_full, t)[:boundary_size, 0]
        rows.append({"time": t, "actual_kernel_error": kernel_error, "moment_tail_bound": float(bound), "actual_boundary_signal_vector_error": float(np.linalg.norm(xfull - xphase)), "phase_register_total_norm": float(np.linalg.norm(evolve_hermitian(phase_full, t)[:, 0]))})
    return {
        "seed": seed,
        "full_dimension": dimension,
        "boundary_size": boundary_size,
        "phase_register_auxiliary_dimension": dm.shape[0],
        "matched_moment_norm_errors_k_0_to_2m_minus_1": errors,
        "minimum_spectral_residue_eigenvalue": min_eigenvalue,
        "rows": rows,
        "interpretation": "Moment-matched positive residues preserve conservative phase memory; finite accuracy is controlled by a horizon-dependent bound, not alleged memory loss.",
    }


def main():
    results = {
        "scope": "Finite mechanism checks; not a general efficient classical simulator",
        "jet_collision": jet_collision_test(),
        "jet_tail_sampler": jet_tail_sampler_test(),
        "commutator_acquisition_growth": commutator_growth_test(),
        "autonomous_local_recurrence_and_volume_law": engineered_xy_test(),
        "finite_moment_adversary": moment_adversary_test(),
        "conservative_phase_register": phase_register_test(),
    }
    (OUT / "RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "jet_false_merge_error_at_pi": results["jet_collision"]["error_at_pi_if_the_jet_collision_is_treated_as_exact"],
        "last_commutator_count": results["commutator_acquisition_growth"]["rows"][-1],
        "volume_law_entropy_bits": results["autonomous_local_recurrence_and_volume_law"]["rows"][2]["neel_initial_half_chain_entropy_bits"],
        "quiet_window_upper_bound": results["autonomous_local_recurrence_and_volume_law"]["quiet_window_one_excitation_upper_bound"],
        "finite_moment_adversary_max_error": results["finite_moment_adversary"]["max_sampled_return_amplitude_difference"],
        "matched_moment_max_error": max(results["conservative_phase_register"]["matched_moment_norm_errors_k_0_to_2m_minus_1"]),
        "written": str(OUT / "RESULTS.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
