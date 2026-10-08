#!/usr/bin/env python3
"""Exact finite check for a moment-matched, state-dependent mass-action pair.

Two networks differ only by alpha_j -> alpha_j + eps*w_j in the
first-order channels X -> jY. Both also contain 2X -> X + jY channels.
All finite-volume first and second generator moments match exactly; the
source-only X projection is exactly identical. The full X,Y jump path differs.
"""

from collections import defaultdict
from fractions import Fraction as Q
from math import log, sqrt


W = (Q(-1), Q(3), Q(-3), Q(1))
J = (1, 2, 3, 4)
ALPHA = (Q(1, 10),) * 4                 # s^-1 per X molecule
EPS = Q(1, 100)                        # s^-1
ALPHA_ALT = tuple(a + EPS * w for a, w in zip(ALPHA, W))
BETA = (Q(1, 10), Q(1, 5), Q(3, 10), Q(2, 5))  # concentration^-1 s^-1
OMEGA = Q(5)                           # copy-number/concentration scale
X0 = 5


def moment_rows(alpha, x, omega):
    """Return exact count drift and raw second jump-moment matrix."""
    rates = [alpha[k] * x + BETA[k] * x * (x - 1) / (2 * omega)
             for k in range(4)]
    nus = [(-1, j) for j in J]
    drift = tuple(sum(rates[k] * nus[k][i] for k in range(4))
                  for i in range(2))
    second = tuple(tuple(sum(rates[k] * nus[k][i] * nus[k][m]
                             for k in range(4))
                         for m in range(2))
                   for i in range(2))
    return drift, second


def event_probabilities(alpha, x, omega):
    """Mark probabilities conditional on an X-consuming event at state x."""
    c = Q(x - 1, 2) / omega
    weights = tuple(alpha[k] + BETA[k] * c for k in range(4))
    total = sum(weights)
    return tuple(v / total for v in weights), total


def exact_mark_path_distributions():
    """Enumerate all 4**X0 ordered mark sequences for a complete batch."""
    p0 = {(): Q(1)}
    p1 = {(): Q(1)}
    per_state = {}
    for x in range(X0, 0, -1):
        p0x, total0 = event_probabilities(ALPHA, x, OMEGA)
        p1x, total1 = event_probabilities(ALPHA_ALT, x, OMEGA)
        assert total0 == total1
        per_state[x] = (p0x, p1x, total0)
        next0, next1 = defaultdict(Q), defaultdict(Q)
        for seq, prob in p0.items():
            for k, p in enumerate(p0x):
                next0[seq + (J[k],)] += prob * p
        for seq, prob in p1.items():
            for k, p in enumerate(p1x):
                next1[seq + (J[k],)] += prob * p
        p0, p1 = dict(next0), dict(next1)
    return p0, p1, per_state


def endpoint_y_distribution(path_distribution):
    result = defaultdict(Q)
    for seq, probability in path_distribution.items():
        result[sum(seq)] += probability
    return dict(result)


def tv(p, q):
    return sum(abs(p.get(k, Q(0)) - q.get(k, Q(0)))
               for k in set(p) | set(q)) / 2


def nuisance_profile_fisher():
    """Fisher information for theta with shared unknown kappa, eta scales."""
    kappa = 0.1
    eta = 0.1
    b_shape = (1.0, 2.0, 3.0, 4.0)
    info = [[0.0] * 3 for _ in range(3)]  # theta, kappa, eta
    for x in range(1, X0 + 1):
        c = (x - 1) / (2 * float(OMEGA))
        r = [kappa + eta * b_shape[j] * c for j in range(4)]
        total = sum(r)
        q_x = x * total
        dr = [[kappa * float(W[j]) for j in range(4)],
              [1.0] * 4,
              [b_shape[j] * c for j in range(4)]]
        dtotal = [sum(v) for v in dr]
        scores = [[dr[a][j] / r[j] - dtotal[a] / total
                   for j in range(4)] for a in range(3)]
        for a in range(3):
            for b in range(3):
                info[a][b] += sum((r[j] / total) * scores[a][j] * scores[b][j]
                                  for j in range(4))
        dq = [0.0, 4.0 * x, x * sum(b_shape) * c]
        for a in range(3):
            for b in range(3):
                info[a][b] += dq[a] * dq[b] / (q_x * q_x)
    # Schur complement for the two nuisance scales, using the exact 2x2 inverse formula.
    a, b = info[1][1], info[1][2]
    c, d = info[2][1], info[2][2]
    det = a * d - b * c
    inv00, inv01, inv11 = d / det, -b / det, a / det
    u, v = info[0][1], info[0][2]
    correction = u * (inv00 * u + inv01 * v) + v * (inv01 * u + inv11 * v)
    efficient = info[0][0] - correction
    return info, efficient


def main():
    # Moment-circuit identities: all degree 0, 1, 2 sums vanish, but degree 3 does not.
    assert sum(W) == 0
    assert sum(W[k] * J[k] for k in range(4)) == 0
    assert sum(W[k] * J[k] ** 2 for k in range(4)) == 0
    assert sum(W[k] * J[k] ** 3 for k in range(4)) == 6
    assert all(a > 0 for a in ALPHA_ALT)

    # Exact finite-volume equality of the first two infinitesimal moments.
    for omega in (Q(1), Q(5), Q(100)):
        for x in range(0, 21):
            assert moment_rows(ALPHA, x, omega) == moment_rows(ALPHA_ALT, x, omega)

    # For X-only observations, each reaction decrements X by one and the total
    # rate is unchanged because sum(w)=0. Thus the projected path laws coincide.
    assert sum(ALPHA) == sum(ALPHA_ALT)
    assert sum(BETA) == Q(1)

    p0, p1, per_state = exact_mark_path_distributions()
    assert sum(p0.values()) == sum(p1.values()) == 1
    path_tv = tv(p0, p1)
    y0, y1 = endpoint_y_distribution(p0), endpoint_y_distribution(p1)
    endpoint_tv = tv(y0, y1)

    # Full observed path KL and Fisher information for epsilon with alpha/beta fixed.
    path_kl = 0.0
    endpoint_kl = sum(float(prob1) * log(float(prob1 / y0[y]))
                      for y, prob1 in y1.items())
    full_fisher = 0.0
    expected_time = Q(0)
    expected_integrated_x = Q(0)
    for x, (p0x, p1x, total0) in per_state.items():
        path_kl += sum(float(q1) * log(float(q1 / q0))
                       for q0, q1 in zip(p0x, p1x))
        # d/d epsilon log p_j = w_j / (alpha_j + beta_j*(x-1)/(2 Omega)).
        c = Q(x - 1, 2) / OMEGA
        r0 = tuple(ALPHA[k] + BETA[k] * c for k in range(4))
        full_fisher += sum(float(W[k] ** 2 / (r0[k] * total0))
                           for k in range(4))
        q_x = x * total0
        expected_time += 1 / q_x
        expected_integrated_x += Q(x) / q_x

    print("moment_circuit", [str(sum(W[k] * J[k] ** r for k in range(4)))
                              for r in range(4)])
    print("alpha0", [str(a) for a in ALPHA])
    print("alpha1", [str(a) for a in ALPHA_ALT])
    print("beta", [str(b) for b in BETA])
    print("sum_alpha_equal", sum(ALPHA) == sum(ALPHA_ALT))
    print("source_only_X_path_TV", 0)
    print("state_1_mark_p0", [str(p) for p in per_state[1][0]])
    print("state_1_mark_p1", [str(p) for p in per_state[1][1]])
    print("state_5_mark_p0", [str(p) for p in per_state[5][0]])
    print("state_5_mark_p1", [str(p) for p in per_state[5][1]])
    print("full_mark_path_TV_complete_batch", float(path_tv))
    print("full_mark_path_TV_exact_fraction", str(path_tv))
    print("endpoint_total_Y_TV", float(endpoint_tv))
    print("endpoint_total_Y_TV_exact_fraction", str(endpoint_tv))
    print("full_path_KL_eps1_given0", path_kl)
    print("endpoint_total_Y_KL_eps1_given0", endpoint_kl)
    print("N_necessary_for_TV_0.8_full_path", int(1.28 / path_kl) + 1)
    print("N_necessary_for_TV_0.8_endpoint_Y", int(1.28 / endpoint_kl) + 1)
    print("full_path_Fisher_epsilon_at0", full_fisher)
    nuisance_info, nuisance_efficient = nuisance_profile_fisher()
    assert 13.37 < nuisance_efficient < 13.39
    print("constrained_nuisance_Fisher_theta_kappa_eta", nuisance_info)
    print("constrained_nuisance_efficient_Fisher_theta", nuisance_efficient)
    print("pinsker_TV_upper", sqrt(path_kl / 2))
    print("expected_completion_time_s", float(expected_time), str(expected_time))
    print("expected_integral_X_dt", float(expected_integrated_x),
          str(expected_integrated_x))
    print("ssa_max_events_per_batch", X0)
    print("ssa_channel_propensity_evals_upper_per_batch", 8 * X0)


if __name__ == "__main__":
    main()
