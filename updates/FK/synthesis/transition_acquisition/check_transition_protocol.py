"""Independent finite-dimensional checks of the derived transition formulas.

This is a small deterministic algebra check, not a proof, source replay, or
scalability benchmark. It constructs its own 5-level Hamiltonian and observable.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(20261014)
    energies = np.array([0.0, 0.7, 0.7, 1.9, 3.1])
    dim = energies.size
    h = np.diag(energies.astype(complex))
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    a_op = (raw + raw.conj().T) / 2
    a_norm = float(np.linalg.norm(a_op, ord=2))
    a_op /= a_norm
    a_norm = 1.0
    beta = 1.3
    eta = 0.43
    span = float(energies[-1] - energies[0])
    weights = np.exp(-beta * energies)
    probs = weights / weights.sum()
    distinct = np.unique(energies)

    def block_strength(e: float, ep: float) -> float:
        i = np.flatnonzero(energies == e)
        j = np.flatnonzero(energies == ep)
        return float(np.sum(np.abs(a_op[np.ix_(i, j)]) ** 2))

    chi = 0.0
    m1_spectral = 0.0
    y_fold_mean = 0.0
    y_up_mean = 0.0
    y_exp_mean = 0.0
    y_odd_mean = 0.0
    y_fold_second = 0.0
    y_odd_second = 0.0
    success_mass = 0.0
    accepted_mass = 0.0
    accepted_pair_weights: list[tuple[float, float, float]] = []
    pair_count = 0
    for i, e in enumerate(distinct):
        p_e = float(np.mean(probs[energies == e]))
        for ep in distinct[i + 1 :]:
            d = float(ep - e)
            p_ep = p_e * np.exp(-beta * d)
            strength = block_strength(float(e), float(ep))
            chi_pair = 2 * d * (p_e - p_ep) * strength / (d * d + eta * eta)
            chi += chi_pair
            m1_spectral += 2 * d * (p_e - p_ep) * strength
            pair_prob = (p_e + p_ep) * strength / a_norm**2
            success_mass += pair_prob
            folded = a_norm**2 * 2 * d * np.tanh(beta * d / 2) / (d * d + eta * eta)
            upward = a_norm**2 * 2 * d * (1 - np.exp(-beta * d)) / (d * d + eta * eta)
            signed_up = upward / 2
            signed_down = a_norm**2 * d * (np.exp(beta * d) - 1) / (d * d + eta * eta)
            odd_up = a_norm**2 * 2 * d / (d * d + eta * eta)
            odd_down = -odd_up
            y_fold_mean += pair_prob * folded
            y_up_mean += p_e * strength / a_norm**2 * upward
            y_odd_mean += (
                p_e * strength / a_norm**2 * odd_up
                + p_ep * strength / a_norm**2 * odd_down
            )
            y_fold_second += pair_prob * folded**2
            y_odd_second += pair_prob * odd_up**2
            y_exp_mean += (
                p_e * strength / a_norm**2 * signed_up
                + p_ep * strength / a_norm**2 * signed_down
            )
            accept_prob = d * np.tanh(beta * d / 2) / (
                span * np.tanh(beta * span / 2)
            )
            target_pair_weight = d * (p_e - p_ep) * strength
            accepted_pair_weights.append(
                (d, pair_prob * accept_prob, target_pair_weight)
            )
            accepted_mass += pair_prob * accept_prob
            pair_count += 1

    commutator = a_op @ (h @ a_op - a_op @ h) - (h @ a_op - a_op @ h) @ a_op
    m1_commutator = float(np.real(np.trace(np.diag(probs) @ commutator)))
    m1_formula = float(m1_spectral)
    acc_theory = m1_formula / (a_norm**2 * 2 * span * np.tanh(beta * span / 2))
    # The accepted gap law is proportional to d(p_E-p_E')S, i.e. to nu.
    accepted_ratios = []
    for _d, mass, target_mass in accepted_pair_weights:
        if mass > 0:
            accepted_ratios.append(mass / target_mass)

    b_env = max(
        2 * d * np.tanh(beta * d / 2) / (d * d + eta * eta)
        for d in np.linspace(0, span, 100_001)[1:]
    )
    f_signed_negative = a_norm**2 * span * (np.exp(beta * span) - 1) / (
        span * span + eta * eta
    )

    print(f"levels={dim}; distinct_energies={len(distinct)}; pairs={pair_count}")
    print(f"chi={chi:.16g}")
    print(f"E[Y_fold]={y_fold_mean:.16g}; abs_error={abs(y_fold_mean-chi):.3e}")
    print(f"E[Y_odd]={y_odd_mean:.16g}; abs_error={abs(y_odd_mean-chi):.3e}")
    print(f"E[Y_up]={y_up_mean:.16g}; abs_error={abs(y_up_mean-chi):.3e}")
    print(f"E[Y_exp]={y_exp_mean:.16g}; abs_error={abs(y_exp_mean-chi):.3e}")
    print(f"Var(Y_fold)={y_fold_second-chi**2:.16g}; Var(Y_odd)={y_odd_second-chi**2:.16g}")
    print(f"M1_spectral={m1_formula:.16g}; M1_commutator={m1_commutator:.16g}")
    print(f"success_mass={success_mass:.16g}")
    print(f"p_accept_direct={accepted_mass:.16g}; p_accept_formula={acc_theory:.16g}")
    print(f"accepted_to_nu_ratio_spread={np.ptp(accepted_ratios):.3e}")
    print(f"fold_grid_max={a_norm**2*b_env:.16g}")
    print(f"fold_global_cap={a_norm**2*min(beta, 1/eta):.16g}")
    print(f"exp_weight_at_negative_span={f_signed_negative:.8g} (can grow exponentially in beta*span)")

    tol = 2e-12
    assert abs(y_fold_mean - chi) < tol
    assert abs(y_odd_mean - chi) < tol
    assert abs(y_up_mean - chi) < tol
    assert abs(y_exp_mean - chi) < tol
    assert y_fold_second <= y_odd_second + tol
    assert abs(m1_formula - m1_commutator) < tol
    assert abs(accepted_mass - acc_theory) < tol
    assert np.ptp(accepted_ratios) < tol
    assert success_mass <= 1 + tol
    assert a_norm**2 * b_env <= a_norm**2 * min(beta, 1 / eta) + tol


if __name__ == "__main__":
    main()
