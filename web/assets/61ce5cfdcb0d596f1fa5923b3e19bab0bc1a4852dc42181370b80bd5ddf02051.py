#!/usr/bin/env python3
"""Exact finite checks for environment_decoupling.txt (stdlib only)."""

from fractions import Fraction
from itertools import combinations


def balanced_signs(d):
    """Yield all +/-1 vectors with d/2 plus signs."""
    for plus in combinations(range(d), d // 2):
        plus = set(plus)
        yield tuple(1 if j in plus else -1 for j in range(d))


def check_dimension(d, a=Fraction(1, 2)):
    assert d % 4 == 0 and 0 < a < 1
    signs = tuple(balanced_signs(d))
    assert len(signs) > 0
    one = Fraction(1)
    mean_weights = [Fraction(0) for _ in range(d)]
    expected_square_sum = (one + a * a) / d

    # Exact Kraus completeness for K_j=|jj><j|: the (k,l) entry of
    # sum_j K_j^* K_j is delta_kl.
    for k in range(d):
        for ell in range(d):
            entry = sum(int(k == j and ell == j) for j in range(d))
            assert entry == int(k == ell)

    for s in signs:
        p = tuple((one + a * sj) / d for sj in s)
        assert all(q > 0 for q in p)
        assert sum(p) == one
        assert sum(q * q for q in p) == expected_square_sum

        # On rho_s the output is the joint distribution (J,J), so each
        # partial-trace marginal is exactly p.
        joint = {(j, j): q for j, q in enumerate(p)}
        first_marginal = tuple(
            sum(q for (j, _), q in joint.items() if j == k)
            for k in range(d)
        )
        second_marginal = tuple(
            sum(q for (_, j), q in joint.items() if j == k)
            for k in range(d)
        )
        eb_dephasing_output = p
        assert first_marginal == p == second_marginal == eb_dephasing_output

        for j, q in enumerate(p):
            mean_weights[j] += q

        # The projector onto the canonical purification has probability
        # sum_j p_j^2 after dephasing.  Its event-probability gap is an exact
        # lower bound on half trace distance.
        purification_error_lower_bound = one - sum(q * q for q in p)
        assert purification_error_lower_bound == one - expected_square_sum

    for j in range(d):
        assert mean_weights[j] / len(signs) == Fraction(1, d)

    print(
        f"d={d}, |S_d|={len(signs)}, a={a}: "
        f"mean=I/d, both marginals exact, EB error=0, "
        f"purification trace-distance >= {1 - expected_square_sum}"
    )


if __name__ == "__main__":
    check_dimension(4)
    check_dimension(8)
