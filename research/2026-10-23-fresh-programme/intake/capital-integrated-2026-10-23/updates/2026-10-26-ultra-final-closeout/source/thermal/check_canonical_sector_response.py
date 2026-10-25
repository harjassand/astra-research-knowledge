"""Finite matrices test the all-normal sector response and pulse bounds.

No continuum-bath/cold-limit/physical-readout certification is inferred.
"""

import json
import numpy as np
from check_canonical_memory_symmetry import charge_operators


def check():
    host, cutoff = 10, 3
    recoil, coupling, beta = 8.0, 0.4, 2.0
    duration, peak = 0.05, 0.02
    charges, jr, qr, tr = charge_operators(cutoff)
    # Exact unrephased half-line representation; use integer raw columns.
    count = cutoff + 1
    raw = np.zeros((len(charges), 2 * count), dtype=np.int64)
    for r in range(count):
        low, high = int(-r - charges[0]), int(1 + r - charges[0])
        raw[low, r] = raw[high, r] = raw[low, count + r] = 1
        raw[high, count + r] = -1
    adjacency = np.diag(np.ones(count - 1, dtype=np.int64), 1)
    adjacency += adjacency.T
    boundary = np.zeros((count, count), dtype=np.int64)
    boundary[0, 0] = 1
    sx = np.array([[0, 1], [1, 0]], dtype=np.int64)
    sz = np.diag([1, -1])
    q_ladder = np.kron(np.eye(2, dtype=np.int64), adjacency) + np.kron(sz, boundary)
    d2_ladder = -np.kron(sx, np.diag(2 * np.arange(count) + 1))
    assert np.array_equal(raw.T @ qr @ raw, 2 * q_ladder)
    assert np.array_equal(raw.T @ np.diag(2 * charges - 1) @ raw, 2 * d2_ladder)
    a = np.diag(np.sqrt(np.arange(1, host)), 1)
    y = (a + a.T) / np.sqrt(2)
    hg = np.diag(np.arange(host) + 0.5)
    ih, ir = np.eye(host), np.eye(len(charges))
    full_y = np.kron(y, ir)
    d = np.kron(ih, np.diag(charges - 0.5))
    j = np.kron(ih, jr)
    parity = np.diag([1 if n % 2 == 0 else -1 for n in range(host)])
    c = np.kron(parity, tr)
    h = np.kron(hg, ir) + recoil * d @ d - coupling * np.kron(y, qr)
    emb = np.zeros((len(charges), cutoff + 1))
    for r in range(cutoff + 1):
        emb[int(-r - charges[0]), r] = 1 / np.sqrt(2)
        emb[int(1 + r - charges[0]), r] = 1 / np.sqrt(2)
    emb = np.kron(ih, emb)
    ep, vp = np.linalg.eigh(emb.T @ h @ emb)
    plus = emb @ vp
    minus = c @ plus
    weights = np.exp(-beta * (ep - ep[0]))
    weights /= weights.sum()
    initial = plus * np.sqrt(weights)

    def mean(op):
        return float(np.real(np.trace(initial.conj().T @ op @ initial)))

    y2 = mean(full_y @ full_y)
    k = mean(d @ d)
    dm = minus.conj().T @ d @ plus
    gaps = ep[:, None] - ep[None, :]
    m0 = float(np.sum(abs(dm)**2 * weights[None, :]))
    m2 = float(np.sum(gaps**2 * abs(dm)**2 * weights[None, :]))
    comm = h @ d - d @ h
    m2_comm = mean(comm.conj().T @ comm)
    assert abs(m0 - k) < 1e-12
    assert abs(m2 - m2_comm) < 1e-12
    assert m2 <= 4 * coupling**2 * y2 + 1e-12

    area = recoil * peak * duration
    reference = np.exp(1j * area * np.diag(d))[:, None] * (plus * (np.sqrt(weights) * np.exp(-1j * ep * duration)))
    reference *= np.exp(-1j * recoil * peak**2 * duration / 3)
    pminus = (np.eye(len(h)) - j) / 2
    reference_probability = float(np.linalg.norm(pminus @ reference, "fro")**2)
    error_bound = coupling * np.sqrt(y2) * area * duration
    assert area * np.sqrt(2 * k) < 1
    assert duration < 1 / (16 * coupling * np.sqrt(y2))

    def evolve(steps):
        state = initial.astype(complex)
        dt = duration / steps
        for step in range(steps):
            time = (step + 0.5) * dt
            eta = peak * (1 - abs(2 * time / duration - 1))
            hp = h - 2 * recoil * eta * d + recoil * eta**2 * np.eye(len(h))
            e, u = np.linalg.eigh(hp)
            state = u @ (np.exp(-1j * dt * e)[:, None] * (u.conj().T @ state))
        return state

    fine = evolve(400)
    coarse = evolve(200)
    actual_probability = float(np.linalg.norm(pminus @ fine, "fro")**2)
    actual_error = float(np.linalg.norm(fine - reference, "fro"))
    # Exact Fourier integral of the triangular detuning waveform.
    pulse_transform = (peak * duration / 2) * np.exp(1j * gaps * duration / 2)
    pulse_transform *= np.sinc(gaps * duration / (4 * np.pi))**2
    quadratic = float(4 * recoil**2 * np.sum(abs(dm)**2 * abs(pulse_transform)**2 * weights[None, :]))
    lower, upper = area**2 / 64, k * area**2
    assert lower <= actual_probability <= upper + 1e-12
    assert actual_error <= error_bound + 1e-10
    return {
        "integer_unrephased_ladder": "PASS",
        "host_cutoff": host, "rotor_charge_cutoff": cutoff,
        "full_transition_spectral_mass": m0,
        "spectral_second_moment": m2,
        "commutator_second_moment": m2_comm,
        "second_moment_upper_bound": 4 * coupling**2 * y2,
        "actual_triangular_pulse_probability": actual_probability,
        "full_quadratic_response_prediction": quadratic,
        "reference_rotation_probability": reference_probability,
        "proved_probability_interval": [lower, upper],
        "actual_purified_state_error": actual_error,
        "proved_state_error_upper": error_bound,
        "time_mesh_state_difference": float(np.linalg.norm(fine - coarse, "fro")),
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
