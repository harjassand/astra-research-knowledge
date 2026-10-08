#!/usr/bin/env python3
"""Exact symbolic path calculation for the translated order-5 fixture.

Requires SymPy. The fourth coordinate D stays equal to 3; hence every
falling-factorial propensity has the common catalyst factor (3)_3=6.
"""

import sympy as sp

n = sp.symbols("n", positive=True, integer=True)

# State is (A-n, B, C); D=3. Rate constants are (1,1,2,1,1).
reactions = (
    ((0, 1, 0), lambda a, b, c: 6 * a),
    ((0, -1, 1), lambda a, b, c: 6 * a * b if b >= 1 else 0),
    ((-1, 0, 0), lambda a, b, c: 12 * a * c if c >= 1 else 0),
    ((0, 2, -1), lambda a, b, c: 6 * c if c >= 1 else 0),
    ((1, -2, 0), lambda a, b, c: 6 * b * (b - 1) if b >= 2 else 0),
)


def expected_A_increment(k):
    states = {(0, 1, 0): sp.Integer(1)}
    for _ in range(k):
        next_states = {}
        for (a_off, b, c), probability in states.items():
            a = n + a_off
            rates = [rate(a, b, c) for _, rate in reactions]
            total = sum(rates)
            for (jump, _), rate in zip(reactions, rates):
                if rate == 0:
                    continue
                nxt = (a_off + jump[0], b + jump[1], c + jump[2])
                if min(nxt[1:]) < 0:
                    continue
                next_states[nxt] = next_states.get(nxt, 0) + probability * rate / total
        states = next_states
    assert sp.simplify(sum(states.values()) - 1) == 0
    return sp.factor(sum(probability * state[0]
                         for state, probability in states.items())), states


if __name__ == "__main__":
    drift1 = sp.simplify(6 * n * (2 * sp.log(2) - 1))
    count_drift1 = 6 * n
    drift3, endpoint_law = expected_A_increment(3)
    print("one-step entropy generator:", drift1)
    print("one-step total-count generator:", count_drift1)
    print("three-step E[Delta A]:", drift3)
    print("limit E[Delta A]:", sp.limit(drift3, n, sp.oo))
    print("three-step endpoint states:", len(endpoint_law))
    # On (n,1,0,3): p(r1)=1/2; after r1, p(r2)->2/3;
    # after r2, p(r3)->1/2 because kappa_3=2.
    print("r1,r2,r3 path probability limit:", sp.Rational(1, 6))
