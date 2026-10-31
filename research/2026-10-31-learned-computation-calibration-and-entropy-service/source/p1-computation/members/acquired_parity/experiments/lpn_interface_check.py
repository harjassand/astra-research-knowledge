"""Small exact-density verification of the passive-sample LPN identity."""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import json


def parity(x):
    return x.bit_count() & 1


def check():
    n, secret, rho = 5, 0b1101, Fraction(1, 3)
    a = secret | (1 << (n - 1))
    probabilities = {
        x: (1 + rho * (-1 if parity(a & x) else 1)) / (1 << n)
        for x in range(1 << n)
    }
    assert sum(probabilities.values()) == 1
    eta = (1 - rho) / 2
    integer_energy = {x: parity(a & x) for x in probabilities}
    unnormalized = {x: Fraction(1, 1 << f) for x, f in integer_energy.items()}
    normalizer = sum(unnormalized.values())
    assert {x: w / normalizer for x, w in unnormalized.items()} == probabilities
    integer_query_recovery = sum(integer_energy[1 << i] << i for i in range(n))
    assert integer_query_recovery == a
    for u in range(1 << (n - 1)):
        marginal = sum(probabilities[u | (b << (n - 1))] for b in (0, 1))
        assert marginal == Fraction(1, 1 << (n - 1))
        noisy_b = parity(secret & u) ^ 1
        assert probabilities[u | (noisy_b << (n - 1))] / marginal == eta

    with localcontext() as ctx:
        ctx.prec = 80
        rho_d = Decimal(rho.numerator) / Decimal(rho.denominator)
        c = n * Decimal(2).ln() - ((1 - rho_d * rho_d).ln() / 2)
        theta = -(((1 + rho_d) / (1 - rho_d)).ln() / 2)
        energy = {x: -(Decimal(p.numerator) / Decimal(p.denominator)).ln()
                  for x, p in probabilities.items()}
        max_formula_error = max(abs(energy[x] - c - theta *
                                    (-1 if parity(a & x) else 1))
                                for x in probabilities)
        spectrum = {
            mask: sum(value * (-1 if parity(mask & x) else 1)
                      for x, value in energy.items()) / (1 << n)
            for mask in range(1 << n)
        }
        max_off_support = max(abs(value) for mask, value in spectrum.items()
                              if mask not in (0, a))
        recovered = sum(int(energy[1 << i] != energy[0]) << i for i in range(n))
        assert recovered == a
        assert max_formula_error < Decimal("1e-75")
        assert max_off_support < Decimal("1e-75")
        return {
            "n": n,
            "secret_low_bits_first": [(secret >> i) & 1 for i in range(n - 1)],
            "mask_low_bits_first": [(a >> i) & 1 for i in range(n)],
            "rho": str(rho), "LPN_noise_rate": str(eta),
            "enumerated_points": len(probabilities),
            "exact_total_probability": str(sum(probabilities.values())),
            "distinct_probability_counts": dict(Counter(str(p) for p in probabilities.values())),
            "each_u_marginal": str(Fraction(1, 1 << (n - 1))),
            "each_conditional_error_probability": str(eta),
            "energy_constant": str(c), "nonconstant_energy_coefficient": str(theta),
            "max_80_decimal_formula_error": str(max_formula_error),
            "max_80_decimal_off_support_coefficient": str(max_off_support),
            "exact_energy_query_count": n + 1,
            "recovered_mask_correct": recovered == a,
            "integer_energy_at_beta_ln2_gives_same_LPN_law": True,
            "integer_energy_values": [0, 1],
            "integer_energy_Walsh_coefficients": {"constant": "1/2", "secret_mask": "-1/2"},
            "integer_scalar_query_mask_recovery": integer_query_recovery == a,
            "query_gap": str(-2 * theta),
            "scope": "Density checks exact rational; energy checks use 80 decimal digits. No hardness experiment.",
        }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
