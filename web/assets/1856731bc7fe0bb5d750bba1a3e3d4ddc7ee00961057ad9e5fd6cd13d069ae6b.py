"""Exact rational checks for the explicit robust A <-> B certificate.

No stochastic simulation is used to justify rare-event probability bounds.
The general stopping argument is in chemical_jump_certificate.md.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def check():
    rates = [F(9, 10), F(11, 10)]
    # exp(theta)=3. Left gap=x-1/10; right gap=9/10-x.
    # No finite-volume approximation is present for unimolecular reactions.
    checks = []
    for side, interval in [("left", [F(1, 10), F(1, 5)]),
                           ("right", [F(4, 5), F(9, 10)])]:
        for x, incoming, outgoing in itertools.product(interval, rates, rates):
            birth, death = incoming*(1-x), outgoing*x
            if side == "left":
                generator_over_V_phi = birth*(F(1, 3)-1) + death*(3-1)
            else:
                generator_over_V_phi = birth*(3-1) + death*(F(1, 3)-1)
            assert generator_over_V_phi <= -F(1, 25)
            checks.append({"side": side, "x": str(x), "incoming": str(incoming),
                           "outgoing": str(outgoing),
                           "generator_over_V_phi": str(generator_over_V_phi)})
    V = 1000
    T = 3**(V//20)
    initial = F(2, 3**(2*V//5))
    leakage = F(22*V, 5*3**(V//20))
    error = initial + leakage
    assert error < F(7, 10**21)
    return {
        "exact_corner_checks": checks, "corner_count": len(checks),
        "max_generator_over_V_phi": str(max(F(x["generator_over_V_phi"]) for x in checks)),
        "V": V, "time_horizon_exact": str(T),
        "time_horizon_approx": float(T), "exit_probability_upper_approx": float(error),
        "exit_probability_upper_certified_less_than": "7e-21",
        "reaction_count_envelope_over_horizon_approx": float(F(11, 10)*V*T),
        "status": "exact polynomial/corner checks; probability theorem proved separately",
    }


if __name__ == "__main__":
    r = check()
    Path(__file__).with_name("chemical_jump_checks.json").write_text(json.dumps(r, indent=2)+"\n")
    print(json.dumps({k:v for k,v in r.items() if k!="exact_corner_checks"},indent=2))
