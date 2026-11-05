"""Exact arithmetic certificate for the soup bound; no simulation claim."""
from fractions import Fraction
from pathlib import Path
import json


def main():
    # ta < 1/10000.  There are TWO rectangle and TWO contour soups.
    r = Fraction(32, 10000)
    rectangle_bound = 200 * r / (1-r)**2
    # e > 2, so 32 exp(-20) < 2^-15.
    q = Fraction(1, 2**15)
    # (n+1)^2(2n+3)^2 has consecutive ratio below 4 for n >= 4.
    # Its value at n=4 is 3025.
    contour_bound = 200 * 3025 * q**4 / (1-4*q)
    total = rectangle_bound + contour_bound
    # Bare plus-phase minus-site probability from the same contour cover.
    q_ising = Fraction(1, 2**16)
    ising_minority_bound = 121 * q_ising**4 / (1-2*q_ising)
    result = {
        "mismatch_energy": 20,
        "activity_product_upper_bound": "1/10000",
        "diameter_weight": "2^diameter",
        "inflation": "closed nearest-neighbor radius one",
        "connectivity": "intersection chains of occupied inflated supports; original bad-site nearest-neighbor paths imply these chains",
        "rectangle_bound_exact": str(rectangle_bound),
        "contour_bound_exact": str(contour_bound),
        "total_bound_exact": str(total),
        "bare_ising_minority_bound_exact": str(ising_minority_bound),
        "rectangle_bound_decimal": float(rectangle_bound),
        "contour_bound_decimal": float(contour_bound),
        "total_bound_decimal": float(total),
        "checks": {
            "rectangle_below_0_645": rectangle_bound < Fraction(645,1000),
            "contour_below_1e_minus12": contour_bound < Fraction(1,10**12),
            "total_below_two_thirds": total < Fraction(2,3),
            "geometric_chain_constant_below_2": total/(1-total) < 2,
            "bare_ising_minority_below_1e_minus16": ising_minority_bound < Fraction(1,10**16),
        },
        "scope": "Certifies numerical upper bounds given the proof's counting and coupling lemmas; does not numerically establish the undecidability theorem."
    }
    assert all(result["checks"].values())
    (Path(__file__).resolve().parent / "branching_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
