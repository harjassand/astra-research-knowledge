#!/usr/bin/env python3
"""Finite, deterministic checks of thermal noise precompensation.

Run:
    python noisy_interface_work/verify_precompensation.py

Produces scoped JSON and a two-panel figure beside this script. These are
finite algebra and sampler checks, not a BDL lifetime or hardware validation.
Dependencies: numpy, scipy, matplotlib, mpmath.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import scipy
from scipy import sparse
from scipy.linalg import eigvalsh
from scipy.stats import binom


OUT = Path(__file__).resolve().parent


def bits(s: int, m: int) -> np.ndarray:
    return np.array([(s >> a) & 1 for a in range(m)], dtype=float)


def gibbs(lambdas: np.ndarray, valid: list[int]) -> np.ndarray:
    weights = np.exp([-np.dot(lambdas, bits(s, len(lambdas))) for s in valid])
    return weights / weights.sum()


def shifts_for(valid: list[int], masks: list[int]) -> list[np.ndarray]:
    lookup = {s: i for i, s in enumerate(valid)}
    return [np.array([lookup[s ^ mask] for s in valid]) for mask in masks]


def invert_bits(pi: np.ndarray, shifts: list[np.ndarray], p: float) -> np.ndarray:
    result = pi.copy()
    for shift in shifts:
        result = ((1 - p) * result - p * result[shift]) / (1 - 2 * p)
    return result


def forward_bits(mu: np.ndarray, shifts: list[np.ndarray], p: float) -> np.ndarray:
    result = mu.copy()
    for shift in shifts:
        result = (1 - p) * result + p * result[shift]
    return result


def inverse_ring() -> dict:
    m, p = 7, 1e-6
    lambdas = np.array([0.7 + 0.1 * a for a in range(m)])
    valid = [s for s in range(1 << m) if s.bit_count() % 2 == 0]
    masks = [(1 << ((i - 1) % m)) ^ (1 << i) for i in range(m)]
    shifts = shifts_for(valid, masks)
    pi = gibbs(lambdas, valid)
    mu = invert_bits(pi, shifts, p)
    prefix = mu.copy()
    errors = []
    for j in range(m + 1):
        rhs = invert_bits(pi, shifts[j:], p)
        errors.append(float(np.linalg.norm(prefix - rhs, 1)))
        if j < m:
            prefix = (1 - p) * prefix + p * prefix[shifts[j]]
    assert mu.min() > 0
    assert abs(mu.sum() - 1) < 1e-13
    assert max(errors) < 1e-13
    return {
        "physical_spins": m, "checks": m, "valid_syndromes": len(valid),
        "constraint": "even syndrome parity", "lambda": lambdas.tolist(),
        "bit_flip_probability": p,
        "minimum_preimage_probability": float(mu.min()),
        "normalization_error": float(abs(mu.sum() - 1)),
        "prefix_identity_l1_errors": errors,
        "final_target_tv": float(np.linalg.norm(prefix - pi, 1) / 2),
    }


def log_series(coeff: list[mp.mpf], order: int) -> list[mp.mpf]:
    """Formal log of 1 + sum_k coeff[k] z^k, through `order`."""
    result = [mp.mpf("0")] * (order + 1)
    for k in range(1, order + 1):
        result[k] = coeff[k] - sum(
            mp.mpf(j) * result[j] * coeff[k - j] for j in range(1, k)
        ) / k
    return result


def mobius_log_check(m: int, masks: list[int], p: float, lam: float) -> dict:
    """High-precision connected-subset order-four calculation on a path."""
    mp.mp.dps = 90
    pp, ll = mp.mpf(str(p)), mp.mpf(str(lam))
    n, order = len(masks), 4
    rr = -pp / (1 - pp)
    b0 = (1 - pp) / (1 - 2 * pp)
    raw = [mp.exp(-ll * s.bit_count()) for s in range(1 << m)]
    norm = sum(raw)
    pi = [value / norm for value in raw]
    mu = pi.copy()
    for mask in masks:
        mu = [((1 - pp) * mu[s] - pp * mu[s ^ mask]) / (1 - 2 * pp)
              for s in range(1 << m)]

    def polynomial(vertices: tuple[int, ...], state: int) -> list[mp.mpf]:
        coeff = [mp.mpf("0")] * (order + 1)
        for flags in range(1 << len(vertices)):
            shifted, size = state, 0
            for j, v in enumerate(vertices):
                if (flags >> j) & 1:
                    shifted ^= masks[v]
                    size += 1
            coeff[size] += rr ** size * mp.exp(
                ll * (state.bit_count() - shifted.bit_count()))
        return coeff

    selected = [0, 1, 42, 85, 170, (1 << m) - 1]
    rows = []
    for state in selected:
        total = [mp.mpf("0")] * (order + 1)
        for size in range(1, order + 1):
            for start in range(n - size + 1):
                connected = tuple(range(start, start + size))
                for flags in range(1 << size):
                    subset = tuple(connected[j] for j in range(size)
                                   if (flags >> j) & 1)
                    sign = (-1) ** (size - len(subset))
                    local_log = log_series(polynomial(subset, state), order)
                    for degree in range(1, order + 1):
                        total[degree] += sign * local_log[degree]
        approximation = sum(total)
        exact = mp.log(mu[state] / pi[state]) - n * mp.log(b0)
        rows.append({
            "syndrome": state,
            "exact_log_partition": mp.nstr(exact, 35),
            "connected_subset_order4": mp.nstr(approximation, 35),
            "absolute_error": mp.nstr(abs(exact - approximation), 12),
        })
        assert abs(exact - approximation) < mp.mpf("1e-18")

    # Two compatible histories: gamma={check 3}, xi={check 1}.
    # This finite difference is nonzero despite hard-core compatibility.
    gamma, xi = 1 << 3, 1 << 1
    odds_empty = mu[gamma] / mu[0]
    odds_with_xi = mu[gamma ^ xi] / mu[xi]
    mixed_log_odds = mp.log(odds_with_xi / odds_empty)
    assert mixed_log_odds != 0
    return {
        "order": order, "decimal_precision": mp.mp.dps,
        "enumerated_connected_sets": sum(n - k + 1 for k in range(1, order + 1)),
        "selected_syndrome_comparisons": rows,
        "compatible_context_example": {
            "birth_polymer_check": 3, "other_polymer_check": 1,
            "log_birth_odds_change": mp.nstr(mixed_log_odds, 35),
            "note": "High precision resolves the small nonzero soft interaction.",
        },
    }


def open_chain_sampler() -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
    m, p, lam = 8, 1e-9, 5.0
    valid = list(range(1 << m))
    masks = [1] + [(1 << (i - 1)) ^ (1 << i) for i in range(1, m)] + [1 << (m - 1)]
    shifts = shifts_for(valid, masks)
    pi = gibbs(np.full(m, lam), valid)
    mu = invert_bits(pi, shifts, p)
    assert mu.min() > 0
    assert np.linalg.norm(forward_bits(mu, shifts, p) - pi, 1) < 1e-13
    raw_normalization_error = float(abs(mu.sum() - 1))
    mu /= mu.sum()  # Remove only floating-point normalization error.

    w, d, D, delta_history = 2, 2, 2, 2
    theta = 2 * p / (1 - 2 * p) * math.exp(w * lam)
    kp_ceiling = 1 / (32 * math.e ** 3 * (D + 1))
    U = math.e ** 2 * theta / (1 - math.e ** 3 * (D + 1) * theta)
    kappa = 2 * d * U
    x = 4 * math.exp(-(lam - kappa))
    U_history = x / (1 - x) ** 2
    influence = (delta_history + 1 + 4 * w * d * U) * U_history
    assert theta < kp_ceiling and influence < 0.5

    polymers = []
    for start in range(m):
        for stop in range(start + 1, m + 1):
            mask = ((1 << (stop - start)) - 1) << start
            boundary = (1 << (start - 1) if start > 0 else 0)
            boundary |= (1 << stop if stop < m else 0)
            polymers.append((mask, boundary))
    K = len(polymers)
    assert K == 36
    P = np.zeros((1 << m, 1 << m))
    for state in valid:
        for mask, boundary in polymers:
            occupied = state & mask
            if (state & boundary) or occupied not in (0, mask):
                P[state, state] += 1 / K
                continue
            absent, present = state & ~mask, state | mask
            birth = mu[present] / (mu[absent] + mu[present])
            P[state, present] += birth / K
            P[state, absent] += (1 - birth) / K
        # Correct accumulated floating-point row summation on the diagonal.
        P[state, state] += 1 - P[state].sum()
    flux = mu[:, None] * P
    stationarity = float(np.linalg.norm(mu @ P - mu, 1))
    balance = float(np.max(np.abs(flux - flux.T)))
    row_error = float(np.max(np.abs(P.sum(axis=1) - 1)))
    assert stationarity < 1e-13 and balance < 1e-13 and row_error < 1e-13
    sym = np.sqrt(mu[:, None]) * P / np.sqrt(mu[None, :])
    assert np.max(np.abs(sym - sym.T)) < 1e-12
    spectrum = eigvalsh((sym + sym.T) / 2)

    # Exactly propagate finite distributions; there are no Monte Carlo draws.
    steps = np.arange(0, 2001)
    starts = [255, 85]
    curves = []
    transition = sparse.csr_matrix(P.T)
    for initial in starts:
        distribution = np.zeros(1 << m)
        distribution[initial] = 1
        curve = []
        for t in steps:
            curve.append(np.linalg.norm(distribution - mu, 1) / 2)
            if t < steps[-1]:
                distribution = transition @ distribution
                distribution /= distribution.sum()
        curves.append(np.array(curve))
    worst_curve = np.maximum(*curves)
    assert worst_curve[-1] < 1e-11
    contraction_bound = np.minimum(1, 2 * m * np.exp(-steps / (2 * K)))
    assert np.max(worst_curve - contraction_bound) < 1e-11
    crossing = np.flatnonzero(worst_curve <= 1e-6)

    result = {
        "physical_spins": m + 1, "checks": m, "syndromes": 1 << m,
        "lambda": lam, "bit_flip_probability": p,
        "polymers": K, "history_graph": "path; maximal occupied intervals",
        "minimum_preimage_probability": float(mu.min()),
        "preimage_normalization_error_before_roundoff_correction": raw_normalization_error,
        "kp_and_mixing": {"theta": theta, "theta_ceiling": kp_ceiling,
                          "U": U, "kappa": kappa, "x": x,
                          "U_history": U_history,
                          "weighted_influence_bound": influence,
                          "required_influence_ceiling": 0.5},
        "row_sum_max_error": row_error,
        "stationarity_l1_error": stationarity,
        "detailed_balance_max_error": balance,
        "reversible_spectral_gap": float(1 - spectrum[-2]),
        "initial_syndromes": starts,
        "tv_curve_interpretation": "Transition-matrix propagation from two specified initial states, evaluated in double precision with roundoff normalization; no Monte Carlo sampling and not worst-case over all initial states.",
        "updates_to_tv_1e_minus_6_for_both_starts": int(crossing[0]),
        "tv_at_update_2000": [float(c[-1]) for c in curves],
        "curve": [{"updates": int(t), "tv_from_255": float(curves[0][t]),
                   "tv_from_85": float(curves[1][t]),
                   "path_coupling_upper_bound": float(contraction_bound[t])}
                  for t in steps[::10]],
        "connected_subset_evaluation": mobius_log_check(m, masks, p, lam),
    }
    return result, steps, worst_curve, contraction_bound


PAULIS = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.diag([1, -1]).astype(complex),
}


def tensor_word(word: str) -> np.ndarray:
    result = np.array([[1]], dtype=complex)
    for char in word:
        result = np.kron(result, PAULIS[char])
    return result


def syndrome_of(word: str, checks: list[str]) -> int:
    answer = 0
    for j, check in enumerate(checks):
        parity = sum(a != "I" and b != "I" and a != b for a, b in zip(word, check)) % 2
        answer |= parity << j
    return answer


def half_trace_norm(matrix: np.ndarray) -> float:
    return float(np.sum(np.abs(eigvalsh((matrix + matrix.conj().T) / 2))) / 2)


def five_qubit_check() -> dict:
    n, p = 5, 1e-6
    checks = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    matrices = [tensor_word(word) for word in checks]
    identity = np.eye(1 << n, dtype=complex)
    projector = identity.copy()
    for generator in matrices:
        projector = projector @ ((identity + generator) / 2)
    logical_z, logical_x = tensor_word("ZZZZZ"), tensor_word("XXXXX")
    zero = np.zeros(1 << n, dtype=complex)
    zero[0] = 1
    zero = projector @ ((identity + logical_z) / 2) @ zero
    zero /= np.linalg.norm(zero)
    code = np.column_stack([zero, logical_x @ zero])
    assert np.max(np.abs(code.conj().T @ code - np.eye(2))) < 1e-13

    words = ["I" * n]
    site_words = []
    for i in range(n):
        group = []
        for pauli in "XYZ":
            word = "I" * i + pauli + "I" * (n - i - 1)
            words.append(word)
            group.append(word)
        site_words.append(group)
    representatives = {syndrome_of(word, checks): word for word in words}
    assert len(representatives) == 16
    isometries = [tensor_word(representatives[s]) @ code for s in range(16)]
    projectors = [V @ V.conj().T for V in isometries]
    assert np.max(np.abs(sum(projectors) - identity)) < 1e-13

    pi = gibbs(np.array([0.7, 0.8, 0.9, 1.0]), list(range(16)))
    mu = pi.copy()
    eigenvalue = 1 - 4 * p / 3
    b0 = (1 + 3 / eigenvalue) / 4
    boff = (1 - 1 / eigenvalue) / 4
    shifts = [[np.arange(16) ^ syndrome_of(word, checks) for word in group]
              for group in site_words]
    for group in shifts:
        mu = b0 * mu + boff * sum(mu[shift] for shift in group)
    assert mu.min() > 0 and abs(mu.sum() - 1) < 1e-13

    target = sum(weight * P / 2 for weight, P in zip(pi, projectors))
    loaded = sum(weight * P / 2 for weight, P in zip(mu, projectors))
    for group in site_words:
        loaded = (1 - p) * loaded + p / 3 * sum(
            tensor_word(word) @ loaded @ tensor_word(word).conj().T for word in group)
    exact_gibbs_error = half_trace_norm(loaded - target)
    assert exact_gibbs_error < 1e-12

    bell_states = []
    for V in isometries:
        psi = np.concatenate([V[:, 0], V[:, 1]]) / math.sqrt(2)
        bell_states.append(np.outer(psi, psi.conj()))
    reference_target = sum(weight * state for weight, state in zip(pi, bell_states))
    reference_loaded = sum(weight * state for weight, state in zip(mu, bell_states))
    for group in site_words:
        ops = [np.kron(np.eye(2), tensor_word(word)) for word in group]
        reference_loaded = (1 - p) * reference_loaded + p / 3 * sum(
            op @ reference_loaded @ op.conj().T for op in ops)
    reference_error = half_trace_norm(reference_loaded - reference_target)
    any_fault_probability = -math.expm1(n * math.log1p(-p))
    assert reference_error <= any_fault_probability + 1e-12
    return {
        "code": "[[5,1,3]] perfect stabilizer code",
        "stabilizers": checks, "syndrome_representatives": representatives,
        "nonidentity_probability_per_physical_site": p,
        "conditional_nonidentity_paulis": "uniform X,Y,Z",
        "minimum_preimage_probability": float(mu.min()),
        "thermal_state_half_trace_error": exact_gibbs_error,
        "bell_reference_half_trace_error": reference_error,
        "any_physical_fault_probability": any_fault_probability,
        "union_bound_5q": 5 * p,
        "scope": "Exact finite density-matrix algebra up to floating-point error; no holding or lifetime assertion.",
    }


def product_bits() -> tuple[dict, np.ndarray, np.ndarray]:
    r, p = 0.1, 0.01
    preimage = (r - p) / (1 - 2 * p)
    naive = p + (1 - 2 * p) * r
    compensated = p + (1 - 2 * p) * preimage
    ns = np.unique(np.rint(np.geomspace(1, 100000, 150)).astype(int))
    values = []
    for n in ns:
        threshold = n * math.log((1 - r) / (1 - naive)) / math.log(
            naive * (1 - r) / (r * (1 - naive)))
        cutoff = int(math.floor(threshold))
        values.append(float(binom.cdf(cutoff, n, r) - binom.cdf(cutoff, n, naive)))
    values = np.array(values)
    assert abs(compensated - r) < 1e-15
    assert abs(values[0] - abs(naive - r)) < 1e-14
    assert values[-1] > 0.999
    invalid_p = 0.12
    negative_preimage = (r - invalid_p) / (1 - 2 * invalid_p)
    assert negative_preimage < 0
    return {
        "thermal_excitation": r, "bit_flip_probability": p,
        "naive_output_excitation": naive,
        "compensating_input_excitation": preimage,
        "compensated_output_excitation": compensated,
        "compensated_product_tv": "0 exactly by the one-bit algebra, at every N",
        "tv_method": "Exact binomial-CDF likelihood-ratio cutoff, using permutation symmetry of product Bernoulli laws.",
        "negative_preimage_boundary_example": {
            "p": invalid_p, "preimage_excitation": negative_preimage},
        "curve": [{"N": int(n), "naive_tv": float(v), "compensated_tv": 0.0}
                  for n, v in zip(ns, values)],
    }, ns, values


def main() -> None:
    ring = inverse_ring()
    chain, steps, tv, bound = open_chain_sampler()
    quantum = five_qubit_check()
    independent, ns, naive_tv = product_bits()
    result = {
        "title": "Finite verification of thermal noise precompensation",
        "scope": "Deterministic finite algebra and finite Markov-chain verification only. No BDL asymptotic lifetime, hardware feasibility, experimental performance, or total-resource advantage is inferred.",
        "command": "python noisy_interface_work/verify_precompensation.py",
        "versions": {"numpy": np.__version__, "scipy": scipy.__version__,
                     "matplotlib": matplotlib.__version__, "mpmath": mp.__version__},
        "checks_passed": True,
        "ring_constraint_check": ring,
        "open_chain_heatbath": chain,
        "five_qubit_quantum_check": quantum,
        "independent_thermal_bits": independent,
    }
    json_path = OUT / "precompensation_verification.json"
    json_path.write_text(json.dumps(result, indent=2) + "\n")

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    axes[0].semilogx(ns, naive_tv, color="#9c3c25", lw=2.2,
                    label="Apply noise to the target law")
    axes[0].semilogx(ns, np.zeros_like(ns), color="#156b55", lw=2.2,
                    label="Prepare the compensating law")
    axes[0].set(xlabel="Number of independent bits N", ylabel="Total variation distance",
                title="A fixed local error creates a global mismatch", ylim=(-0.025, 1.025))
    axes[0].text(0.04, 0.80, "Thermal excitation 0.10\nBit-flip probability 0.01",
                 transform=axes[0].transAxes, fontsize=9)
    axes[0].legend(frameon=False, loc="lower right", fontsize=8.5)
    axes[0].grid(alpha=0.18)
    axes[1].semilogy(steps, np.maximum(tv, 1e-16), color="#156b55", lw=2.2,
                    label="Finite transition-matrix propagation")
    axes[1].semilogy(steps, np.maximum(bound, 1e-16), color="#6f7681", lw=1.8,
                    ls="--", label="Path-coupling upper bound")
    axes[1].set(xlabel="Single-polymer updates", ylabel="Total variation distance",
                title="Context-dependent heat bath converges", ylim=(1e-14, 2), xlim=(0, 2000))
    axes[1].text(0.04, 0.10, "8 checks; 36 interval polymers\nMaximum of two stated initial conditions",
                 transform=axes[1].transAxes, fontsize=9)
    axes[1].legend(frameon=False, loc="upper right", fontsize=8.5)
    axes[1].grid(alpha=0.18)
    fig.suptitle("Finite precompensation checks — no lifetime claim", fontsize=13, fontweight="bold")
    fig.savefig(OUT / "precompensation_verification.png", dpi=200)
    fig.savefig(OUT / "precompensation_verification.pdf")
    plt.close(fig)
    summary = {
        "checks_passed": True,
        "ring_final_tv": ring["final_target_tv"],
        "chain_stationarity_l1": chain["stationarity_l1_error"],
        "chain_mixing_influence_bound": chain["kp_and_mixing"]["weighted_influence_bound"],
        "chain_updates_to_1e_minus_6": chain["updates_to_tv_1e_minus_6_for_both_starts"],
        "five_qubit_gibbs_error": quantum["thermal_state_half_trace_error"],
        "five_qubit_bell_error": quantum["bell_reference_half_trace_error"],
        "bell_union_bound": quantum["union_bound_5q"],
        "naive_product_tv_at_100000": float(naive_tv[-1]),
        "json": str(json_path),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
