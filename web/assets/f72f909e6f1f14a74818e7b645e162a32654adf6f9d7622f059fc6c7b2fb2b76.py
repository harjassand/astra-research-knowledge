#!/usr/bin/env python3
"""Exact rational illustration of common finite-path minorization."""

from fractions import Fraction as F
from itertools import product


T = F(1, 100)
Q_MAX = F(18)
EXP_LOWER = 1 - Q_MAX * T  # e^{-x} >= 1-x for x >= 0
assert EXP_LOWER == F(41, 50) and EXP_LOWER > 0

# Box: alpha, delta, p, u in [1/2,2], q,v in [1,3].
ALPHA_MIN = DELTA_MIN = F(1, 2)
Q_MIN = F(1)


def path(state):
    a, b1, b2 = state
    states = [state]
    rates = []
    channels = []
    if a == 0 and (b1 or b2):
        # 0 -> A has rate at least alpha_min.
        a += 1
        rates.append(ALPHA_MIN)
        channels.append("immigration")
        states.append((a, b1, b2))
    for i in range(2):
        b = b1 if i == 0 else b2
        while b:
            # q(A+B_i -> A) * a * b; here a=1 throughout clearing.
            assert a >= 1
            rates.append(Q_MIN * a * b)
            channels.append(f"remove_B{i + 1}")
            b -= 1
            if i == 0:
                b1 = b
            else:
                b2 = b
            states.append((a, b1, b2))
    while a:
        # delta*A -> 0 at rate at least delta_min*A.
        rates.append(DELTA_MIN * a)
        channels.append("catalyst_death")
        a -= 1
        states.append((a, b1, b2))
    assert states[-1] == (0, 0, 0)
    return states, rates, channels


def path_lower_bound(states, rates):
    n = len(rates)
    if n == 0:
        return EXP_LOWER
    delta = T / (n + 1)
    interval_length = delta / 2
    return EXP_LOWER * interval_length**n * _product(rates)


def _product(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def main():
    receipts = []
    for state in product(range(2), repeat=3):
        states, rates, channels = path(state)
        # On every path state, a<=1 and each b_i<=1, so the total exit-rate
        # upper bound over the box is alpha+2 + death 2 + birth 4
        # + removal 6 + autocatalysis 4 = 18.
        assert max(x[0] for x in states) <= 1
        assert max(x[1] for x in states) <= 1
        assert max(x[2] for x in states) <= 1
        eta_x = path_lower_bound(states, rates)
        receipts.append({
            "state": state,
            "path_length": len(rates),
            "channels": channels,
            "minimum_channel_rates": [str(x) for x in rates],
            "rational_probability_lower_bound": str(eta_x),
        })
    eta = min(F(x["rational_probability_lower_bound"]) for x in receipts)
    assert eta > 0
    print({
        "status": "PASS",
        "scope": "exact rational lower bounds for prescribed-path events on F0",
        "F0_states": len(receipts),
        "T": str(T),
        "uniform_total_exit_bound": str(Q_MAX),
        "e_minus_QT_lower_bound": str(EXP_LOWER),
        "common_minorization_eta": str(eta),
        "minorizing_measure": "delta_(0,0,0)",
        "states": receipts,
        "scope_limit": "This checks the finite path-rate and time-window arithmetic only; the all-state drift and the general skeleton ergodicity theorem are separate proof obligations.",
    })


if __name__ == "__main__":
    main()
