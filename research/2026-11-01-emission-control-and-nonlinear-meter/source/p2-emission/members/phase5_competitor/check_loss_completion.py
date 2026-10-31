"""Finite-model checks for exact loss completion and its limitations.

No laboratory parameters are inferred. All rates below are illustrative / us.
Hilbert space retains vacuum and the complete one-excitation manifold of
three control modes (two rails plus a coupler), and of two target modes.
The mathematical SWS control model can switch chi off during swaps.
The always-on-chi variant is explicitly a failed implementation of that model.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, norm, svdvals


HERE = Path(__file__).resolve().parent
dA, dB = 4, 3
IA, IB = np.eye(dA), np.eye(dB)


def ketbra(i, j, d):
    m = np.zeros((d, d), dtype=complex)
    m[i, j] = 1
    return m


nA = [ketbra(j, j, dA) for j in (1, 2, 3)]
nB = [ketbra(j, j, dB) for j in (1, 2)]
NA, NB = sum(nA), sum(nB)
swap = ketbra(2, 3, dA) + ketbra(3, 2, dA)
V = np.zeros((dA * dB, 4), complex)
for k, (a, b) in enumerate(((1, 1), (1, 2), (2, 1), (2, 2))):
    V[a * dB + b, k] = 1
Uideal = np.diag([1., 1., -1., 1.]).astype(complex)
Pout = V @ V.conj().T


def hazard(a_rates, b_rates):
    return np.kron(sum(k * n for k, n in zip(a_rates, nA)), IB) + np.kron(
        IA, sum(k * n for k, n in zip(b_rates, nB))
    )


def nojump(H, ratesA, ratesB, t):
    return expm((-1j * H - hazard(ratesA, ratesB) / 2) * t)


def sws(ratesA, ratesB, g, chi, tf, tw, tb, always_on=False):
    Hwait = chi * np.kron(nA[2], nB[1])
    Hswap = g * np.kron(swap, IB)
    if always_on:
        Hswap += Hwait
    F = nojump(Hswap, ratesA, ratesB, tf)
    W = nojump(Hwait, ratesA, ratesB, tw)
    B = nojump(Hswap, ratesA, ratesB, tb)
    full = B @ W @ F
    return V.conj().T @ full @ V, full


def metrics(K, full, target=Uideal):
    scalar = np.trace(target.conj().T @ K) / 4
    singular = svdvals(K)
    n2 = np.trace(K.conj().T @ K).real
    psi = np.array([1, 0, 1, 0], complex) / np.sqrt(2)
    ideal = target @ psi
    got = K @ psi
    got /= norm(got)
    # Stable pure-state trace distance using the orthogonal component.
    td = norm(got - ideal * np.vdot(ideal, got))
    return {
        "scalar_residual_operator_norm": float(norm(K - scalar * target, 2)),
        "relative_scalar_residual": float(norm(K - scalar * target, 2) / abs(scalar)),
        "mean_nojump_code_survival": float(n2 / 4),
        "max_uniform_success_after_arbitrary_ideal_filter": float(singular[-1] ** 2),
        "conditional_choi_infidelity": float(max(0, 1 - abs(np.trace(target.conj().T @ K)) ** 2 / (4 * n2))),
        "witness_conditional_trace_distance": float(td),
        "no_jump_coupler_leakage_operator_norm": float(norm((np.eye(12) - Pout) @ full @ V, 2)),
    }


def main():
    a = np.array([0.002, 0.003, 0.030])
    b = np.array([0.002, 0.004])
    t_swap = .120
    t_wait = .260
    g = np.pi / (2 * t_swap)
    chi = np.pi / t_wait
    total = 2 * t_swap + t_wait
    rawK, rawfull = sws(a, b, g, chi, t_swap, t_wait, t_swap)
    lamA, lamB = max(a), max(b)
    balancedK, balancedfull = sws(np.full(3, lamA), np.full(2, lamB), g, chi,
                                t_swap, t_wait, t_swap)
    expected_balanced_scalar = np.exp(-(lamA + lamB) * total / 2)
    # Exact damped transfer, permitted only because chi is off during swaps.
    kbar = (a[1] + a[2]) / 2
    delta = (a[2] - a[1]) / 4
    Omega = np.sqrt(g * g - delta * delta)
    tf = (np.pi / 2 + np.arctan(delta / Omega)) / Omega
    tb = (np.pi / 2 - np.arctan(delta / Omega)) / Omega
    corrected_total = tf + t_wait + tb
    attenuation_exponent_A = kbar * (tf + tb) + a[2] * t_wait
    spectator_rate = attenuation_exponent_A / corrected_total
    endpoint_a = a.copy()
    endpoint_a[0] = spectator_rate
    endpointK, endpointfull = sws(endpoint_a, np.full(2, lamB), g, chi,
                                tf, t_wait, tb)
    expected_endpoint_scalar = np.exp(-.5 * (attenuation_exponent_A + lamB * corrected_total))
    failedK, failedfull = sws(endpoint_a, np.full(2, lamB), g, chi,
                            tf, t_wait, tb, always_on=True)

    scaling = []
    for scale in [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]:
        K, full = sws(scale*a, scale*b, g, chi, t_swap, t_wait, t_swap)
        scaling.append({"rate_scale": scale, **metrics(K, full)})

    # Universal controls also work in the simpler one-block matched-loss model.
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.diag([1., -1.]).astype(complex)
    universal_H = .7 * X + .23 * Z
    universal_t = .37
    universal_lam = .013
    U = expm(-1j * universal_H * universal_t)
    K = expm((-1j * universal_H - universal_lam*np.eye(2)/2)*universal_t)
    universal_error = norm(K - np.exp(-universal_lam*universal_t/2)*U, 2)

    # Jump propagation counterexample: under chi n_A1 n_B1, A1 loss at t
    # leaves an unknown target phase exp(-i chi t n_B1), not a pure A erasure.
    psiB = np.ones(2, complex) / np.sqrt(2)
    loss_time_target_distances = []
    for fraction in [0, .25, .5, .75, 1]:
        phase = chi * t_wait * fraction
        out = np.array([1, np.exp(-1j * phase)], complex) / np.sqrt(2)
        loss_time_target_distances.append({
            "fraction_of_wait": fraction,
            "target_trace_distance_from_unrotated": float(norm(out - psiB*np.vdot(psiB, out))),
        })

    # Complete illustrative cell, not merely Hamiltonian pulse time.
    map_t, read_t, reset_t, feed_t, route_t = .30, .45, .10, .05, .10
    check_t = map_t + read_t + reset_t + feed_t + route_t
    idle_hazard = max(a[:2]) + max(b)
    active_hazard = lamA + lamB
    exposure = active_hazard * total + idle_hazard * check_t
    p_loss_cycle = 1 - np.exp(-exposure)
    q_fn, f_fp = .01, .001
    # This diagnostic gives an instantaneous sample the benefit of occurring
    # after mapping; an actual finite map can have an even longer blind tail.
    sample_t = total + map_t
    sample_exposure = active_hazard*total + idle_hazard*map_t
    tail_t = read_t + reset_t + feed_t + route_t
    p_late = np.exp(-sample_exposure) * (1 - np.exp(-idle_hazard*tail_t))
    out = {
        "model": "12-state vacuum-plus-single-excitation, switchable chi, cold Markovian amplitude damping only",
        "units": "microseconds; rates and angular Hamiltonian coefficients per microsecond",
        "rates_control_a0_a1_c": a.tolist(),
        "rates_target_b0_b1": b.tolist(),
        "parameters": {"g": float(g), "chi": float(chi), "swap_t": t_swap,
                       "wait_t": t_wait, "ideal_gate_t": total},
        "unbalanced": metrics(rawK, rawfull),
        "continuous_loss_completed": {
            **metrics(balancedK, balancedfull),
            "exact_identity_residual": float(norm(balancedK - expected_balanced_scalar*Uideal, 2)),
            "erasure_probability_in_gate": float(1 - expected_balanced_scalar**2),
            "added_rates_A": (lamA-a).tolist(),
            "added_rates_B": (lamB-b).tolist(),
        },
        "endpoint_damped_swap_plus_spectator_loss": {
            **metrics(endpointK, endpointfull),
            "forward_swap_t": float(tf), "backward_swap_t": float(tb),
            "total_gate_t": float(corrected_total),
            "spectator_added_loss_rate": float(spectator_rate-a[0]),
            "exact_identity_residual": float(norm(endpointK - expected_endpoint_scalar*Uideal, 2)),
            "erasure_probability_in_gate": float(1-expected_endpoint_scalar**2),
            "requires": "chi disabled during both swaps; no dephasing or control error",
        },
        "failed_always_on_chi_endpoint_construction": metrics(failedK, failedfull),
        "loss_rate_scaling": scaling,
        "arbitrary_single_qubit_H_matched_loss_scalar_error": float(universal_error),
        "loss_time_partner_error": loss_time_target_distances,
        "complete_cycle_example": {
            "gate": total, "mapping": map_t, "readout": read_t,
            "reset": reset_t, "feedforward": feed_t, "routing": route_t,
            "total_elapsed": total + check_t,
            "integrated_hazard": float(exposure),
            "loss_probability": float(p_loss_cycle),
            "false_negative_probability_given_preexisting_loss": q_fn,
            "false_positive_probability_given_valid": f_fp,
            "single_check_preexisting_loss_miss_term": float(p_loss_cycle*q_fn),
            "ideal_sample_late_loss_passed_unflagged_at_output": float(p_late),
            "latest_sample_time": sample_t,
            "post_sample_quantum_output_exposure": tail_t,
            "warning": "late-loss term is first order even when q_FN is zero; next-cell/terminal coverage is mandatory",
        },
    }
    (HERE / "loss_completion_results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ["loss_rate_scaling", "loss_time_partner_error"]}, indent=2))
    assert out["continuous_loss_completed"]["exact_identity_residual"] < 1e-12
    assert out["endpoint_damped_swap_plus_spectator_loss"]["exact_identity_residual"] < 1e-12
    assert universal_error < 1e-12


if __name__ == "__main__":
    main()
