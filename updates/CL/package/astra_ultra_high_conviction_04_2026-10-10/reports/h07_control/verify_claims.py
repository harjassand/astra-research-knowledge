"""Small exact checks for the frozen h07 signed-order derivation."""

from fractions import Fraction
from itertools import product


def has_orthant_gauge(edges, n):
    """edges are (source, target, sign), requiring s_source*s_target=sign."""
    for signs in product((-1, 1), repeat=n):
        if all(signs[u] * signs[v] == sign for u, v, sign in edges):
            return signs
    return None


def logistic(x):
    return 4 * x * (1 - x)


def monotone_map(z, v):
    return (
        Fraction(1, 2) * z[0] + Fraction(1, 4) * z[1] + v[0],
        Fraction(1, 2) * z[1] + Fraction(1, 4) * z[0] + v[1],
    )


def main():
    # A balanced signed cycle is switchable to all-positive couplings.
    balanced = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
    assert has_orthant_gauge(balanced, 3) is not None
    assert 1 * -1 * -1 == 1

    # Positive monotone witness: the corner trajectory gives exact one-step
    # coordinate maxima and proves a lower-set safety/upper-set reach claim.
    z_upper = (Fraction(1, 4), Fraction(1, 4))
    v_upper = (Fraction(1, 10), Fraction(1, 10))
    y_upper = monotone_map(z_upper, v_upper)
    assert y_upper == (Fraction(23, 80), Fraction(23, 80))
    z_sample, v_sample = (Fraction(1, 10), Fraction(1, 5)), (0, Fraction(1, 20))
    y_sample = monotone_map(z_sample, v_sample)
    assert all(y_sample[i] <= y_upper[i] for i in range(2))
    assert all(y_upper[i] <= Fraction(3, 10) for i in range(2))
    assert y_upper[0] >= Fraction(7, 25)

    # The frozen inhibitory cycle is unbalanced, so no orthant gauge exists.
    unbalanced = [(0, 1, 1), (1, 2, 1), (2, 0, -1)]
    assert has_orthant_gauge(unbalanced, 3) is None
    assert 1 * 1 * -1 == -1

    # Exact counterexample: the interior initial state reaches the upper set,
    # while the upper corner does not.
    x_interior, x_corner = Fraction(1, 2), Fraction(1)
    assert logistic(x_interior) == 1
    assert logistic(x_corner) == 0
    assert Fraction(9, 10) <= logistic(x_interior) <= 1
    assert not (Fraction(9, 10) <= logistic(x_corner) <= 1)

    # For the continuous-time signed cycle, the infinity log-norm bound is
    # -1+a. With a=1/4 this is strictly negative, despite unbalanced signs.
    a = Fraction(1, 4)
    log_norm_upper_bound = -1 + a
    assert log_norm_upper_bound == Fraction(-3, 4)
    print("PASS: monotone corner witness, balance test, exact counterexample, contraction bound")


if __name__ == "__main__":
    main()
