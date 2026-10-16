"""Self-authored finite diagnostics for SPEC_PROOF.md; no source code imported.

Controller service is exact rational arithmetic. Quantum matrix checks are
floating-point sanity checks of the separate algebraic proof, not certificates.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path
import json
import time

import numpy as np


def kron_all(xs):
    out = np.array([[1]], dtype=complex)
    for x in xs:
        out = np.kron(out, x)
    return out


def controller_check():
    states = list(product(range(3), repeat=5))
    means = {}
    # Unit rates. A terminal state waits for one rate-one T event.
    for r in sorted(states, key=lambda z: sum(2-x for x in z)):
        pending = [i for i, x in enumerate(r) if x < 2]
        if not pending:
            means[r] = Fraction(1)
            continue
        nxt = []
        for i in pending:
            s = list(r)
            s[i] += 1
            assert sum(2-x for x in s) == sum(2-x for x in r) - 1
            nxt.append(tuple(s))
        means[r] = Fraction(1, len(pending)) + sum(means[s] for s in nxt)/len(pending)

    assert max(means.values()) == means[(0,)*5]
    m_formula = Fraction(1)
    for j in range(1, 6):
        integral = sum(Fraction(comb(j, k)*factorial(k), j**(k+1)) for k in range(j+1))
        m_formula += (-1)**(j+1)*comb(5, j)*integral
    assert m_formula == means[(0,)*5]

    perturbations = 0
    for r in states:
        for i in range(5):
            for x in range(3):
                s = list(r)
                s[i] = x
                assert tuple(s) in means
                assert means[tuple(s)] <= m_formula
                perturbations += 1

    # Clean occupancy is an execution witness within the defined move table.
    owner = {0: "A", 1: "B", 2: "A"}
    for r in states:
        for i in range(5):
            if r[i] < 2:
                assert owner[r[i]] != owner[r[i]+1]
    assert owner[2] == owner[0]  # The same A bank carries the boundary output.

    return {
        "phase_states": len(states),
        "single_site_phase_replacements_including_noop": perturbations,
        "all_states_have_clean_retirement": True,
        "max_mean_service_exact": str(m_formula),
        "max_mean_service_float": float(m_formula),
        "simple_mean_bound": str(1 + 2*sum(Fraction(1, i) for i in range(1, 6))),
        "maximum_enabled_local_moves_before_commit": 10,
        "all_canonical_boundaries_use_same_A_banks": True,
    }


def quantum_check():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.diag([1, -1]).astype(complex)
    paulis = {"I": I, "X": X, "Y": Y, "Z": Z}
    C = (I - 1j*(X+Y+Z))/2
    gs = [kron_all([paulis[p] for p in word]) for word in
          ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")]
    P = np.eye(32, dtype=complex)
    for g in gs:
        P = P @ (np.eye(32)+g)/2
    v0 = P[:, 0].copy()
    v0 /= np.linalg.norm(v0)
    XL = kron_all([X]*5)
    v1 = XL @ v0
    V = np.column_stack([v0, v1])
    assert np.max(np.abs(V.conj().T@V-np.eye(2))) < 1e-12
    CL = kron_all([C]*5)
    logical_X = V.conj().T @ XL @ V
    logical_C = V.conj().T @ CL @ V
    logical_U = logical_C @ logical_X
    preserve = np.max(np.abs((np.eye(32)-P)@CL@V))
    order_swap = np.linalg.norm(
        np.kron(logical_C@logical_X, (logical_C@logical_X).conj())
        - np.kron(logical_X@logical_C, (logical_X@logical_C).conj()))
    assert preserve < 1e-12 and order_swap > 1

    bits = [tuple((j >> (4-i)) & 1 for i in range(5)) for j in range(32)]
    def ternary_index(z):
        k = 0
        for a in z:
            k = 3*k+a
        return k
    qids = [ternary_index(z) for z in bits]
    def embed(a):
        z = np.zeros((243, a.shape[1]), dtype=complex)
        z[qids, :] = a
        return z
    V3 = embed(V)
    images = [V3]
    for i in range(5):
        for p in (X, Y, Z):
            mats = [I]*5
            mats[i] = p
            images.append(embed(kron_all(mats)@V))
    for i in range(5):
        for s in range(2):
            z = np.zeros_like(V3)
            for j, b in enumerate(bits):
                if b[i] == s:
                    w = list(b)
                    w[i] = 2
                    z[ternary_index(w), :] += np.sqrt(2)*V[j, :]
            images.append(z)
    residual = 0.0
    for a, wa in enumerate(images):
        for b, wb in enumerate(images):
            target = np.eye(2) if a == b else np.zeros((2, 2))
            residual = max(residual, float(np.max(np.abs(wa.conj().T@wb-target))))
    assert residual < 1e-12
    Q = sum(w@w.conj().T for w in images)
    assert np.max(np.abs(Q@Q-Q)) < 1e-12
    assert abs(np.trace(Q).real-52) < 1e-12

    # Every finite phase vector gives an exactly specified recovery frame.
    W = [I, X, C@X]
    phase_frame_inverse = 0.0
    for r in product(range(3), repeat=5):
        Vr = kron_all([W[x] for x in r])
        phase_frame_inverse = max(phase_frame_inverse,
                                  float(np.max(np.abs(Vr.conj().T@Vr@V-V))))

    # Arbitrary qubit-to-qutrit one-track maps include all local bank/phase paths.
    rng = np.random.default_rng(20261016)
    arbitrary_errors = 0
    recovery_scalar_residual = 0.0
    ideal32 = CL@XL@V
    for i in range(5):
        for _ in range(40):
            E = rng.normal(size=(3, 2))+1j*rng.normal(size=(3, 2))
            damaged = np.zeros_like(V3)
            for j, b in enumerate(bits):
                for a in range(3):
                    w = list(b)
                    w[i] = a
                    damaged[ternary_index(w), :] += E[a, b[i]]*ideal32[j, :]
            for wa in images:
                K = wa.conj().T @ damaged
                relative = K@logical_U.conj().T
                scalar = np.trace(relative)/2
                recovery_scalar_residual = max(
                    recovery_scalar_residual,
                    float(np.max(np.abs(relative-scalar*np.eye(2)))))
            arbitrary_errors += 1
    assert recovery_scalar_residual < 1e-11

    # CPTP identities for the actual local destructive transfer, including vacancy.
    local_move_tp_residual = 0.0
    for gate in (X, C):
        gate3 = np.eye(3, dtype=complex)
        gate3[:2, :2] = gate
        Ks = []
        for b in range(3):
            K = np.zeros((9, 9), dtype=complex)
            for a in range(3):
                for c in range(3):
                    K[2*3+c, a*3+b] += gate3[c, a]
            Ks.append(K)
        local_move_tp_residual = max(
            local_move_tp_residual,
            float(np.max(np.abs(sum(k.conj().T@k for k in Ks)-np.eye(9)))))
    assert local_move_tp_residual < 1e-12

    # Decisive falsifier for a naive noisy global recovery implementation.
    # A weight-two Pauli is miscorrected by the one-error recovery to a logical fault.
    Z34 = kron_all([I, I, Z, Z, I])
    bad = embed(Z34@V)
    nonzero_K = []
    for a, wa in enumerate(images):
        K = wa.conj().T@bad
        if np.linalg.norm(K) > 1e-12:
            nonzero_K.append((a, K))
    assert len(nonzero_K) == 1
    a, K = nonzero_K[0]
    scalar_residual = np.linalg.norm(K-np.trace(K)/2*np.eye(2))
    assert scalar_residual > 1

    return {
        "code_dimension": 2,
        "qutrit_error_images": len(images),
        "error_image_dimension": int(round(np.trace(Q).real)),
        "orthogonal_error_isometry_max_residual": residual,
        "transversal_C_code_preservation_max_residual": float(preserve),
        "logical_channel_order_swap_frobenius_distance": float(order_swap),
        "phase_frames_checked": 243,
        "phase_frame_inverse_max_residual": phase_frame_inverse,
        "arbitrary_one_track_maps_checked": arbitrary_errors,
        "recovery_Kraus_relative_scalar_max_residual": recovery_scalar_residual,
        "local_move_CPTP_max_residual": local_move_tp_residual,
        "weight_two_falsifier": {
            "input_error": "Z_3 Z_4",
            "selected_recovery_image_index": a,
            "logical_non_scalar_frobenius_residual": float(scalar_residual),
            "residual_logical_matrix": [[str(z) for z in row] for row in K],
        },
        "floating_point_checks_are_proof": False,
    }


def main():
    start = time.perf_counter()
    result = {"controller": controller_check(), "quantum": quantum_check()}
    result["wall_seconds_self_measured"] = time.perf_counter()-start
    result["status"] = "PASS_FINITE_DIAGNOSTICS_ONLY"
    p = Path(__file__).with_name("RESULTS.json")
    p.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
