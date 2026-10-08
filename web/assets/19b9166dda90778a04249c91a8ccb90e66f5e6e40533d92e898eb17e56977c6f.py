#!/usr/bin/env python3
"""Exact finite-CTMC calculation for Poisson sample-and-hold feedback.

Time is normalized by gamma (the per-occupied-output death rate), so
delta = nu/gamma and each death rate is 1.  m=0.1 and the held action table
is the least-shared-cap full-information table from the accompanying report.
"""
from __future__ import annotations

import argparse
from mpmath import mp


STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
STATE_INDEX = {state: i for i, state in enumerate(STATES)}
JOINT_INDEX = {(n, y): 4 * STATE_INDEX[n] + STATE_INDEX[y]
               for n in STATES for y in STATES}


def parameters():
    z = mp.sqrt(34)
    p_full = (6 - z) / 10
    # At the crossing q_0(0.1), b=2r and the pointwise shared cap is b.
    r = (z - 4) / 18
    b = 2 * r
    table = {
        (0, 0): (r, r),
        (0, 1): (b, mp.mpf(0)),
        (1, 0): (mp.mpf(0), b),
        (1, 1): (mp.mpf(0), mp.mpf(0)),
    }
    return p_full, r, b, table


def generator(delta):
    """Row generator on states (N,Y), with an independent read clock delta."""
    _, _, _, table = parameters()
    q = mp.matrix(16, 16)
    for n in STATES:
        for y in STATES:
            i = JOINT_INDEX[(n, y)]
            for k in (0, 1):
                nn = list(n)
                if n[k] == 0:
                    nn[k] = 1
                    q[i, JOINT_INDEX[(tuple(nn), y)]] += table[y][k]
                else:
                    nn[k] = 0
                    q[i, JOINT_INDEX[(tuple(nn), y)]] += 1
            # Reads with Y=N still incur cost but do not change the CTMC state.
            if n != y:
                q[i, JOINT_INDEX[(n, n)]] += delta
            q[i, i] = -sum(q[i, j] for j in range(16))
    return q


def stationary(delta):
    if delta <= 0:
        raise ValueError("Use the analytic slow-read limit at delta=0.")
    q = generator(delta)
    a = q.transpose()
    rhs = mp.matrix(16, 1)
    # Replace one redundant balance equation by normalization.
    for j in range(16):
        a[15, j] = 1
    rhs[15] = 1
    return mp.lu_solve(a, rhs)


def metrics(v):
    masses_n = {
        n: sum(v[JOINT_INDEX[(n, y)]] for y in STATES)
        for n in STATES
    }
    return (
        masses_n[(1, 1)],
        sum(n[0] * mass for n, mass in masses_n.items()),
        sum(n[1] * mass for n, mass in masses_n.items()),
    )


def slow_read_limit():
    """Singular-perturbation limit from positive delta, not delta=0 itself."""
    _, r, b, _ = parameters()
    q = r / (1 + r)
    s = b / (1 + b)
    a = q * (1 - q) / (1 - s)
    z = 1 + 2 * a + q * q
    alpha00 = 1 / z
    alpha_single = a / z
    alpha11 = q * q / z
    p11 = alpha00 * q * q
    mean = alpha00 * q + alpha_single * s
    return p11, mean, alpha00, alpha_single, alpha11


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deltas",
        default="0.01,0.1,0.3,0.4677510399078655,1,1.322089772319347,3,10,100",
        help="comma-separated nu/gamma values; all must be positive",
    )
    parser.add_argument(
        "--kappa",
        default="0",
        help="dimensionless read cost kappa=c*gamma in loss 1-P11+kappa*(nu/gamma)",
    )
    parser.add_argument(
        "--cost-threshold",
        action="store_true",
        help="locate the derivative root of the read-cost break-even ratio against P11=0.01",
    )
    args = parser.parse_args()
    mp.dps = 50

    p_full, r, b, _ = parameters()
    p0, m0, alpha00, alpha_single, alpha11 = slow_read_limit()
    m = mp.mpf(1) / 10
    baseline_p = m * m
    baseline_loss = 1 - baseline_p
    kappa = mp.mpf(args.kappa)

    print("gamma-normalized exact CTMC; state order N-major then Y-major")
    print("p_full =", mp.nstr(p_full, 16), "r =", mp.nstr(r, 16),
          "b=B* =", mp.nstr(b, 16))
    print("nu->0+: P11 =", mp.nstr(p0, 16),
          "means =", mp.nstr(m0, 16), mp.nstr(m0, 16))
    print("nu->0+: alpha(Y=00,01,10,11) =",
          *(mp.nstr(x, 14) for x in (alpha00, alpha_single,
                                      alpha_single, alpha11)))
    print("nu->infinity: P11 =", mp.nstr(p_full, 16), "means = 0.1, 0.1")
    print("constant split at target means: lambda/gamma=1/9, cap/gamma=2/9,",
          "P11 =", mp.nstr(baseline_p, 8), "loss =", mp.nstr(baseline_loss, 8))
    if args.cost_threshold:
        def ratio(delta):
            p11, _, _ = metrics(stationary(delta))
            return (p11 - baseline_p) / delta

        delta_star = mp.findroot(lambda delta: mp.diff(ratio, delta),
                                 (mp.mpf("1.2"), mp.mpf("1.5")))
        p_star = metrics(stationary(delta_star))[0]
        print("cost break-even diagnostic:")
        print("  delta* =", mp.nstr(delta_star, 24))
        print("  P11(delta*) =", mp.nstr(p_star, 24))
        print("  kappa_break =", mp.nstr(ratio(delta_star), 24))
    print("delta       P11             mean1           mean2           loss")
    for item in args.deltas.split(","):
        delta = mp.mpf(item.strip())
        p11, mean1, mean2 = metrics(stationary(delta))
        loss = 1 - p11 + kappa * delta
        print(f"{mp.nstr(delta, 9):<11} {mp.nstr(p11, 14):<16} "
              f"{mp.nstr(mean1, 14):<16} {mp.nstr(mean2, 14):<16} "
              f"{mp.nstr(loss, 14)}")


if __name__ == "__main__":
    main()
