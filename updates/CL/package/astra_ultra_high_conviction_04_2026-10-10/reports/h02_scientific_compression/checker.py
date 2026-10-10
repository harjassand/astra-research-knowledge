"""Exact-formula checks for h02's two-state hidden-mixing adversary.

This script checks finite-horizon separation and the exact no-transition
testing bound. It is arithmetic evidence only, not a simulation theorem.
"""
from math import exp, log


def expected_average(gamma: float, horizon: float) -> float:
    if gamma == 0:
        return 1.0
    return -__import__("math").expm1(-2 * gamma * horizon) / (2 * gamma * horizon)


def no_switch_probability(gamma: float, observed_horizon: float) -> float:
    return exp(-gamma * observed_horizon)


def tv_distance(gamma: float, observed_horizon: float) -> float:
    # P_0 is a point mass on the all-+ path. P_gamma has that atom with this
    # probability, and all its other paths are disjoint from the atom.
    return 1.0 - no_switch_probability(gamma, observed_horizon)


def main() -> None:
    smooth_kappa_lower = exp(-32.0 / 45.0) / 4.0
    smooth_output_gap_lower = smooth_kappa_lower / 2.0
    assert smooth_kappa_lower > 0.122
    assert smooth_output_gap_lower > 0.061
    print(
        f"smooth_ode: kappa>={smooth_kappa_lower:.8g} "
        f"output_gap>={smooth_output_gap_lower:.8g} "
        f"predictor_worst_error>={smooth_output_gap_lower/2:.8g}"
    )

    # Horizon-matched rare mode: gamma*H=1, so the requested expected outputs
    # remain separated by a fixed constant while short records are identical
    # with high probability.
    m1 = expected_average(1.0, 1.0)
    gap = 1.0 - m1
    assert abs(m1 - (1.0 - exp(-2.0)) / 2.0) < 1e-15
    assert gap > 0.56
    c = 0.1
    tv = tv_distance(1.0, c)  # rescale time so H=1, gamma=1
    risk = no_switch_probability(1.0, c) / 2.0
    assert abs(tv - (1.0 - exp(-c))) < 1e-15
    assert risk > 0.45
    print(
        f"horizon_matched: target_frozen=1 target_mixing={m1:.8g} "
        f"separation={gap:.8g} B/H={c:g} TV={tv:.8g} "
        f"min_test_error>={risk:.8g}"
    )

    # With a known fixed rate and a horizon far beyond its mixing time, a
    # short burst is sublinear; the failure is uniform acquisition, not a
    # claim that averaging never helps.
    for gamma in (1e-1, 1e-2, 1e-3, 1e-4):
        H = gamma ** -3
        target = expected_average(gamma, H)
        B = 0.5 / gamma
        lower_testing_error = no_switch_probability(gamma, B) / 2
        assert gamma * B <= log(2)
        assert tv_distance(gamma, B) < 0.4
        assert target < 0.01
        assert abs(B / H - 0.5 * gamma**2) < 1e-15
        print(
            f"gamma={gamma:g} H={H:g} E[A_H]={target:.8g} "
            f"B={B:g} B/H={B/H:.8g} "
            f"TV={tv_distance(gamma, B):.8g} "
            f"min_test_error>={lower_testing_error:.8g}"
        )


if __name__ == "__main__":
    main()
