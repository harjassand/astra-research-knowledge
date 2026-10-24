#!/usr/bin/env python3
"""Numerical challenges of the physical C_L processor, not a proof substitute.

Uses NumPy only. The central text supplies the general intertwiner/SU(2) proof.
Run with OPENBLAS_NUM_THREADS=1 python3 verify_involution_clock.py.
"""
from __future__ import annotations

import json
from math import pi, sqrt
from pathlib import Path

import numpy as np


def weights(length: int, alpha: float = 1.0) -> np.ndarray:
    assert length >= 3
    out = alpha * np.sqrt(np.arange(1, length + 1) * np.arange(length, 0, -1))
    out[[0, -1]] /= sqrt(2)
    return out


def cycle_hamiltonian(labels: list[np.ndarray], ww: np.ndarray) -> np.ndarray:
    length, dim = len(labels), labels[0].shape[0]
    out = np.zeros((length * dim, length * dim), dtype=complex)
    for j, (gate, weight) in enumerate(zip(labels, ww)):
        k = (j + 1) % length
        sj, sk = slice(j * dim, (j + 1) * dim), slice(k * dim, (k + 1) * dim)
        out[sk, sj] += weight * gate
        out[sj, sk] += weight * gate.conj().T
    assert np.linalg.norm(out - out.conj().T) < 1e-12
    return out


def evolve_columns(hh: np.ndarray, time: float, cols: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(hh)
    return vectors @ (np.exp(-1j * time * values)[:, None] * (vectors.conj().T @ cols))


def random_unitary(rng: np.random.Generator, dim: int) -> np.ndarray:
    zz = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    qq, rr = np.linalg.qr(zz)
    return qq @ np.diag(np.diag(rr) / np.abs(np.diag(rr)))


def challenge_general_cycles() -> list[dict]:
    rng = np.random.default_rng(20261024)
    rows = []
    for length in range(3, 17):
        dim = 3
        rotation = random_unitary(rng, dim)
        target = rotation @ np.diag([1, -1, 1]) @ rotation.conj().T
        labels = [random_unitary(rng, dim) for _ in range(length - 1)]
        prefix = np.eye(dim, dtype=complex)
        for gate in labels:
            prefix = gate @ prefix
        labels.append(target @ prefix.conj().T)
        word = np.eye(dim, dtype=complex)
        for gate in labels:
            word = gate @ word
        assert np.linalg.norm(word - target) < 1e-12
        assert np.linalg.norm(labels[0] @ labels[1] - labels[1] @ labels[0]) > 1e-2

        hh = cycle_hamiltonian(labels, weights(length))
        initial = np.zeros((length * dim, dim), dtype=complex)
        initial[:dim] = np.eye(dim)
        expected = initial @ (((-1j) ** length) * target)
        actual = evolve_columns(hh, pi / 2, initial)
        endpoint = np.linalg.norm(actual[:dim] - expected[:dim], 2)
        leakage = np.linalg.norm(actual[dim:], 2)
        assert endpoint < 2e-12 and leakage < 2e-12

        # A genuine physical C_L endpoint check in BOTH W eigenspaces.
        sector_errors = []
        for sign in (1, -1):
            projector = (np.eye(dim) + sign * target) / 2
            sector_errors.append(float(np.linalg.norm((actual - expected) @ projector, 2)))
        rows.append({"L": length, "physical_endpoint_error": float(endpoint),
                     "other_physical_head_leakage": float(leakage),
                     "both_sector_errors": sector_errors})
    return rows


def challenge_cover_and_quotient() -> list[dict]:
    rows = []
    for length in range(3, 17):
        ww = weights(length)
        bb = cycle_hamiltonian([np.ones((1, 1))] * (2 * length), np.tile(ww, 2))
        even = np.zeros((2 * length, length + 1))
        even[0, 0] = even[length, length] = 1
        for j in range(1, length):
            even[j, j] = even[2 * length - j, j] = 1 / sqrt(2)
        expected_path = np.zeros((length + 1, length + 1))
        for j in range(length):
            expected_path[j, j + 1] = expected_path[j + 1, j] = sqrt((j + 1) * (length - j))
        quotient_error = np.linalg.norm(bb @ even - even @ expected_path)
        assert quotient_error < 1e-12
        eigenvalues = np.linalg.eigvalsh(expected_path)
        assert np.max(np.abs(eigenvalues - np.arange(-length, length + 1, 2))) < 1e-12
        intertwiners = []
        for sign in (1, -1):
            jj = np.zeros((2 * length, length))
            jj[:length] = np.eye(length) / sqrt(2)
            jj[length:] = sign * np.eye(length) / sqrt(2)
            labels = [np.ones((1, 1))] * (length - 1) + [np.array([[sign]])]
            aa = cycle_hamiltonian(labels, ww)
            intertwiners.append(float(np.linalg.norm(bb @ jj - jj @ aa)))
            assert intertwiners[-1] < 1e-12
        assert abs(np.linalg.norm(bb, 2) - length) < 1e-11
        rows.append({"L": length, "quotient_error": float(quotient_error),
                     "sector_intertwiner_errors": intertwiners})
    return rows


def controlled_x(dim_qubits: int, controls: tuple[int, ...], target: int) -> np.ndarray:
    dim = 1 << dim_qubits
    out = np.zeros((dim, dim), dtype=complex)
    for source in range(dim):
        output = source ^ (1 << target) if all((source >> cc) & 1 for cc in controls) else source
        out[output, source] = 1
    return out


def challenge_local_oracles() -> list[dict]:
    rows = []
    for n in range(1, 4):
        dim, length = 1 << (2 * n), 2 * n + 2
        gates = [controlled_x(2 * n, (0,), n)]
        for i in range(1, n):
            gates.append(controlled_x(2 * n, (n + i - 1, i), n + i))
        cc = np.eye(dim, dtype=complex)
        for gg in gates:
            cc = gg @ cc
        zz = np.diag([(-1) ** ((i >> (2 * n - 1)) & 1) for i in range(dim)])
        word = cc.conj().T @ zz @ cc
        labels = gates + [zz] + [gg.conj().T for gg in reversed(gates)] + [np.eye(dim)]
        assert len(labels) == length
        actual_word = np.eye(dim, dtype=complex)
        for gg in labels:
            actual_word = gg @ actual_word
        assert np.linalg.norm(actual_word - word) < 1e-12
        assert np.linalg.norm(word @ word - np.eye(dim)) < 1e-12

        # Physical vertices f0,...,fn,bn,...,b0 and actual cell supports.
        cells = list(range(n + 1)) + list(range(n, -1, -1))
        touched = [set((cells[j], cells[(j + 1) % length])) for j in range(length)]
        assert all(max(ss) - min(ss) <= 1 for ss in touched)
        incident = [sum(i in ss for ss in touched) for i in range(n + 1)]
        assert max(incident) <= 4
        # hbar=J=1 and the conservative aggregate-strength choice in the text.
        alpha = 1 / (2 * (length + 1))
        ww = weights(length, alpha)
        local_strengths = [sum(ww[j] for j, ss in enumerate(touched) if i in ss)
                           for i in range(n + 1)]
        assert max(local_strengths) <= 1
        hh = cycle_hamiltonian(labels, ww)

        # Entire physical input+work isometry, including dirty work and both eigensectors.
        initial_all = np.zeros((length * dim, dim), dtype=complex)
        initial_all[:dim] = np.eye(dim)
        expected_all = initial_all @ (((-1j) ** length) * word)
        actual_all = evolve_columns(hh, pi / (2 * alpha), initial_all)
        all_error = np.linalg.norm(actual_all - expected_all, 2)
        assert all_error < 3e-12

        # Clean-work code on EVERY input basis vector; therefore arbitrary reference too.
        code = np.eye(dim, dtype=complex)[:, :1 << n]
        mcphase = np.eye(1 << n, dtype=complex)
        mcphase[-1, -1] = -1
        assert np.linalg.norm(word @ code - code @ mcphase) < 1e-12
        clean_expected = np.zeros((length * dim, 1 << n), dtype=complex)
        clean_expected[:dim] = ((-1j) ** length) * code @ mcphase
        clean_error = np.linalg.norm(actual_all @ code - clean_expected, 2)
        assert clean_error < 3e-12
        assert abs(np.linalg.norm(hh @ initial_all, 2) - alpha * sqrt(length)) < 1e-12
        rows.append({"n": n, "L": length, "matrix_dimension": length * dim,
                     "full_input_work_isometry_error": float(all_error),
                     "clean_work_oracle_error": float(clean_error),
                     "physical_other_head_leakage": float(np.linalg.norm(actual_all[dim:], 2)),
                     "maximum_aggregate_cell_strength": float(max(local_strengths))})
    return rows


def negative_control_noninvolution() -> float:
    length, dim = 6, 2
    target = np.diag(np.exp(1j * np.array([0.37, -0.61])))
    labels = [np.eye(dim)] * (length - 1) + [target]
    hh = cycle_hamiltonian(labels, weights(length))
    initial = np.zeros((length * dim, dim), dtype=complex)
    initial[:dim] = np.eye(dim)
    error = np.linalg.norm(evolve_columns(hh, pi / 2, initial)
                           - initial @ (((-1j) ** length) * target), 2)
    assert error > 0.1
    return float(error)


def main() -> None:
    results = {"physical_cycles": challenge_general_cycles(),
               "cover_quotients": challenge_cover_and_quotient(),
               "local_oracles": challenge_local_oracles(),
               "noninvolution_negative_control_error": negative_control_noninvolution(),
               "status": "numerical challenges passed; analytic theorem remains in the text"}
    destination = Path(__file__).with_name("replay.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": results["status"],
                      "max_cycle_endpoint_error": max(r["physical_endpoint_error"] for r in results["physical_cycles"]),
                      "max_other_physical_head_leakage": max(r["other_physical_head_leakage"] for r in results["physical_cycles"]),
                      "max_oracle_isometry_error": max(r["full_input_work_isometry_error"] for r in results["local_oracles"]),
                      "negative_control_error": results["noninvolution_negative_control_error"],
                      "output": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
