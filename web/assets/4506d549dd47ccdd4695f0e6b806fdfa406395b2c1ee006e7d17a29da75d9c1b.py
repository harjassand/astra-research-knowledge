"""Exact finite-state witness for rate non-identifiability from untimed paths.

States are A (reactant basin), I (interface), and B (absorbing product).
A -> I has rate a; I -> A and I -> B have rates r and s.  The successful
reactive state sequence is always A,I,B.  Multiplying every rate by c leaves
the embedded jump chain and committor unchanged, while multiplying the
steady A-to-B event rate per unit A-occupation by c.
"""

from fractions import Fraction


def witness(a: Fraction, r: Fraction, s: Fraction, c: Fraction):
    assert a > 0 and r > 0 and s > 0 and c > 0
    p_hit_B = s / (r + s)
    k_per_A_time = a * p_hit_B
    scaled_p_hit_B = (c * s) / (c * r + c * s)
    scaled_k_per_A_time = (c * a) * scaled_p_hit_B
    holding_mean_I = 1 / (r + s)
    scaled_holding_mean_I = 1 / (c * r + c * s)
    return p_hit_B, k_per_A_time, scaled_p_hit_B, scaled_k_per_A_time, holding_mean_I, scaled_holding_mean_I


if __name__ == "__main__":
    a, r, s, c = Fraction(1), Fraction(999), Fraction(1), Fraction(10)
    p, k, p_scaled, k_scaled, tau, tau_scaled = witness(a, r, s, c)
    assert p == p_scaled == Fraction(1, 1000)
    assert k_scaled == c * k
    assert tau_scaled == tau / c
    print(f"P(I -> B before A) = {p} = {p_scaled}")
    print(f"k_AB per unit A-occupation: {k} -> {k_scaled} (factor {c})")
    print(f"mean I holding time: {tau} -> {tau_scaled} (factor 1/{c})")
    print("successful embedded reactive path: A -> I -> B in both models")
