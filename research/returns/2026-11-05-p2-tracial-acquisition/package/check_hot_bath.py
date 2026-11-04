"""Finite matrix checks of a tracial collision output-information construction.

These are diagnostics, not a proof or a hardware experiment. Full output
correlations are retained in the dense calculations. Large-N resource rows
are analytic formula evaluations, not large bath simulations.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

OUT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
PAULI = [
    I,
    np.array([[0, 1], [1, 0]], complex),
    np.array([[0, -1j], [1j, 0]], complex),
    np.diag([1, -1]).astype(complex),
]


def swap_sites(n: int, first: int, second: int) -> np.ndarray:
    dim = 1 << n
    result = np.zeros((dim, dim), complex)
    a, b = n - 1 - first, n - 1 - second
    for x in range(dim):
        y = x
        if ((x >> a) ^ (x >> b)) & 1:
            y ^= (1 << a) | (1 << b)
        result[y, x] = 1
    return result


def trace_source(a: np.ndarray, e: int) -> np.ndarray:
    return np.trace(a.reshape(2, e, 2, e), axis1=0, axis2=2)


def trace_bath(a: np.ndarray, e: int) -> np.ndarray:
    return np.trace(a.reshape(2, e, 2, e), axis1=1, axis2=3)


def full_unitary(angles: list[float], rotations: bool = False) -> np.ndarray:
    n = len(angles)
    dim = 1 << (n + 1)
    u = np.eye(dim, dtype=complex)
    for j, angle in enumerate(angles):
        if rotations:
            v = expm(-1j * (0.19 * PAULI[1] + 0.13 * (j + 1) * PAULI[3]))
            u = np.kron(v, np.eye(1 << n)) @ u
        gate = np.cos(angle) * np.eye(dim) + 1j * np.sin(angle) * swap_sites(n + 1, 0, j + 1)
        u = gate @ u
    return u


def channel_outputs(u: np.ndarray, e: int) -> list[np.ndarray]:
    return [trace_source(u @ np.kron(p, np.eye(e) / e) @ u.conj().T, e)
            for p in PAULI]


def normalized_choi(images: list[np.ndarray]) -> np.ndarray:
    # |Phi><Phi| = (I I + X X - Y Y + Z Z)/4.
    return sum(np.kron(p.T, image) for p, image in zip(PAULI, images)) / 4


def trace_norm(a: np.ndarray) -> float:
    return float(np.linalg.svd(a, compute_uv=False).sum())


def partial_swap_checks() -> list[dict]:
    rows = []
    for n in range(1, 7):
        for theta in [0.11, 0.37, np.pi / 4, 1.1]:
            for rotations in [False, True]:
                angles = [theta * (1 + 0.02 * j) for j in range(n)]
                u = full_unitary(angles, rotations)
                e = 1 << n
                images = channel_outputs(u, e)
                alpha = 1 - float(np.prod([1 - np.sin(a)**4 for a in angles]))
                b = [image * e / 2 for image in images]
                gram = np.array([[np.trace(x.conj().T @ y) / e
                                  for y in b] for x in b])
                target = np.diag([1, alpha, alpha, alpha])
                error = float(np.max(np.abs(gram - target)))
                # Direct receiver: append an independent maximally mixed dummy,
                # apply the inverse full interaction, trace all bath outputs.
                recovered = [trace_bath(u.conj().T @ np.kron(I / 2, image) @ u, e)
                             for image in images]
                direct_error = max(float(np.max(np.abs(a - factor * p)))
                                   for a, factor, p in zip(recovered, [1, alpha, alpha, alpha], PAULI))
                rho_re = normalized_choi(images)
                baseline = np.eye(2 * e) / (2 * e)
                output_distance = trace_norm(rho_re - baseline)
                bound = np.sqrt(3 * alpha)
                rows.append({
                    "N": n, "theta": float(theta), "source_rotations": rotations,
                    "angles": angles, "alpha": alpha,
                    "gram_error": error, "direct_decoder_error": direct_error,
                    "bell_output_trace_distance": output_distance,
                    "reference_uniform_bound": bound,
                    "bound_holds": output_distance <= bound + 1e-11,
                    "decoder_half_diamond_error": 0.75 * (1 - alpha),
                    "all_decoder_lower_half_diamond": 0.75 * (1 - np.sqrt(alpha)),
                })
    return rows


def hermitian_generator(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    h = (z + z.conj().T) / 2
    h -= np.trace(h).real / 4 * np.eye(4)
    return h / np.linalg.norm(h, 2)


def local_action_checks(rng: np.random.Generator) -> list[dict]:
    rows = []
    for index in range(80):
        h = hermitian_generator(rng)
        action = [0.01, 0.03, 0.1, 0.3][index % 4]
        u = expm(-1j * action * h)
        transfer = []
        for p in PAULI[1:]:
            b = trace_source(u @ np.kron(p, I) @ u.conj().T, 2) / 2
            transfer.append(b)
        gram = np.array([[np.trace(x.conj().T @ y) / 2
                          for y in transfer] for x in transfer])
        b_norm = float(np.sqrt(max(0, np.linalg.eigvalsh(gram).max())))
        rows.append({"index": index, "action": action, "export_amplitude": b_norm,
                     "bound": 2 * action**2,
                     "ratio": b_norm / (2 * action**2)})
    return rows


def feedback_checks(rng: np.random.Generator) -> list[dict]:
    rows = []
    for n in [2, 4, 6, 8]:
        for action in [0.1, 0.25, 0.4]:
            generators = [[hermitian_generator(rng), hermitian_generator(rng)]
                          for _ in range(n)]
            images = []
            for p in PAULI:
                branches = {"": p}
                for j in range(n):
                    next_branches = {}
                    for history, state in branches.items():
                        # Prior output labels select a genuinely different gate.
                        choice = 0 if not history else int(history[-1])
                        u = expm(-1j * action * generators[j][choice])
                        joint = u @ np.kron(state, I / 2) @ u.conj().T
                        joint = joint.reshape(2, 2, 2, 2)
                        for label in [0, 1]:
                            next_branches[history + str(label)] = joint[:, label, :, label]
                    branches = next_branches
                images.append(np.diag([np.trace(state) for state in branches.values()]))
            rho_re = normalized_choi(images)
            baseline = np.kron(I / 2, images[0] / 2)
            distance = trace_norm(rho_re - baseline)
            delta = 1 - (1 - min(1, 4 * action**4))**n
            bound = np.sqrt(3 * delta)
            rows.append({"N": n, "action": action,
                         "bell_record_trace_distance": distance,
                         "reference_uniform_bound": bound,
                         "bound_holds": distance <= bound + 1e-11})
    return rows


def resource_rows() -> dict:
    epsilon = 0.01
    a = 0.75
    rows = []
    for theta in [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]:
        n_forget = int(np.ceil(np.log(a / epsilon) / -np.log(np.cos(theta)**2)))
        n_collect = int(np.ceil(np.log(a / epsilon) / -np.log1p(-np.sin(theta)**4)))
        n_necessary = max(0, int(np.ceil(np.log(a / (2 * epsilon)) / -np.log1p(-np.sin(theta)**4))))
        rows.append({"theta": theta, "forget_N": n_forget,
                     "collect_N_sufficient": n_collect, "collect_N_necessary": n_necessary,
                     "sufficient_to_forgetting_ratio": n_collect / n_forget})
    limit_rows = []
    # Fixed reduced relaxation rate lambda=1, and time T=10.
    for dt in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
        n = int(round(10 / dt))
        s2 = -np.expm1(-dt)
        theta = float(np.arcsin(np.sqrt(s2)))
        alpha = float(-np.expm1(n * np.log1p(-s2**2)))
        limit_rows.append({"dt": dt, "N": n, "theta": theta,
                           "source_half_diamond_from_replacer": 0.75 * np.exp(-10),
                           "output_full_diamond_from_replacer_bound": np.sqrt(3 * alpha),
                           "decoder_half_diamond_error": 0.75 * (1 - alpha),
                           "all_decoder_lower_half_diamond": 0.75 * (1 - np.sqrt(alpha)),
                           "peak_swap_coupling": theta / dt})
    return {"epsilon": epsilon, "partial_swap_resource_rows": rows,
            "fixed_rate_limit_rows": limit_rows}


def qudit_reference_checks() -> list[dict]:
    """Actual correlated channels and inverse receiver in d=3,4.

    A random mixed reference/source input is evolved with all bath factors;
    the real source is traced out, then an independent dummy is appended.
    This supplements, rather than substitutes for, the linear-map proof.
    """
    rng = np.random.default_rng(172943)
    rows = []
    for d, n in [(3, 1), (3, 2), (3, 3), (4, 1), (4, 2)]:
        e, rdim = d**n, d + 1
        size = d * e
        u = np.eye(size, dtype=complex)
        angles = [0.23 + 0.07 * j for j in range(n)]
        for j, angle in enumerate(angles):
            z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            v = expm(-0.1j * (z + z.conj().T))
            u = np.kron(v, np.eye(e)) @ u
            w = np.zeros((size, size), complex)
            for index in range(size):
                digits = list(np.unravel_index(index, [d] * (n + 1)))
                digits[0], digits[j + 1] = digits[j + 1], digits[0]
                w[np.ravel_multi_index(tuple(digits), [d] * (n + 1)), index] = 1
            u = (np.cos(angle) * np.eye(size) + 1j * np.sin(angle) * w) @ u
        alpha = 1 - np.prod([1 - np.sin(x)**4 for x in angles])
        z = rng.normal(size=(rdim * d, 7)) + 1j * rng.normal(size=(rdim * d, 7))
        rho = z @ z.conj().T
        rho /= np.trace(rho)
        ur = np.kron(np.eye(rdim), u)
        encoded = ur @ np.kron(rho, np.eye(e) / e) @ ur.conj().T
        bath = np.trace(encoded.reshape(rdim, d, e, rdim, d, e), axis1=1, axis2=4)
        bath = bath.reshape(rdim * e, rdim * e)
        # Insert the independent dummy between reference and received bath.
        dummy_state = np.einsum('iajb,kl->ikajlb',
                                bath.reshape(rdim, e, rdim, e), np.eye(d) / d)
        dummy_state = dummy_state.reshape(rdim * d * e, rdim * d * e)
        decoded = ur.conj().T @ dummy_state @ ur
        decoded = np.trace(decoded.reshape(rdim, d, e, rdim, d, e), axis1=2, axis2=5)
        decoded = decoded.reshape(rdim * d, rdim * d)
        rho_r = np.trace(rho.reshape(rdim, d, rdim, d), axis1=1, axis2=3)
        target = alpha * rho + (1 - alpha) * np.kron(rho_r, np.eye(d) / d)
        rows.append({"d": d, "N": n, "reference_dimension": rdim,
                     "source_rotations": True, "alpha": float(alpha),
                     "reference_uniform_channel_identity_error":
                         float(np.max(np.abs(decoded - target)))})
    return rows


def main() -> None:
    rng = np.random.default_rng(20261105)
    partial = partial_swap_checks()
    local = local_action_checks(rng)
    feedback = feedback_checks(rng)
    qudit = qudit_reference_checks()
    result = {
        "status": "Finite floating-point diagnostics; no hardware or SDP-optimality execution.",
        "partial_swap": partial, "generic_action": local, "classical_feedback": feedback,
        "qudit_entangled_reference": qudit,
        "resources": resource_rows(),
        "summary": {
            "partial_swap_cases": len(partial),
            "max_gram_error": max(x["gram_error"] for x in partial),
            "max_direct_decoder_error": max(x["direct_decoder_error"] for x in partial),
            "max_action_bound_ratio": max(x["ratio"] for x in local),
            "all_reference_checks_pass": all(x["bound_holds"] for x in partial + feedback),
            "qudit_reference_cases": len(qudit),
            "max_qudit_reference_identity_error": max(
                x["reference_uniform_channel_identity_error"] for x in qudit),
        },
    }
    (OUT / "hot_bath_checks.json").write_text(
        json.dumps(result, indent=2, default=lambda x: x.item()) + "\n")
    print(json.dumps(result["summary"], indent=2))
    print(json.dumps(result["resources"], indent=2))


if __name__ == "__main__":
    main()
