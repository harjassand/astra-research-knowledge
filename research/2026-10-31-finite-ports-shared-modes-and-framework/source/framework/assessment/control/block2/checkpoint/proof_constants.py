"""Exact rational checks of the conservative analytic constants."""

from fractions import Fraction as Q


def main():
    remainder = Q(7, 6) + Q(2, 25)
    assert remainder == Q(187, 150) < Q(5, 4)
    assert Q(1, 6) + Q(1, 250) < Q(1, 5)
    print("One-cycle constant:", remainder, "< 5/4")
    # A short Machin alternating-series bracket certifies the pi upper bound.
    def atan_bracket(denominator):
        terms = 20
        lower = sum(Q((-1)**k, (2*k + 1)*denominator**(2*k + 1))
                    for k in range(terms))
        return lower, lower + Q(1, (2*terms + 1)*denominator**(2*terms + 1))
    low5, high5 = atan_bracket(5)
    low239, high239 = atan_bracket(239)
    pi_upper = 16*high5 - 4*low239
    assert pi_upper < Q(355, 113)
    rounded_cycle = 5*pi_upper/Q(32) * Q(101, 100)**4
    rounded_angle = pi_upper/Q(2) * Q(30301, 1000000)
    total = rounded_cycle + rounded_angle + Q(1, 4)
    assert rounded_cycle < Q(511, 1000)
    assert rounded_angle < Q(48, 1000)
    assert total < Q(809, 1000) < 1
    print("Finite-precision coefficient including clock tolerance (rounded display):",
          f"{float(total):.12f}", "< 809/1000 < 1")
    print("All scalar comparisons use exact rational arithmetic.")


if __name__ == "__main__":
    main()
