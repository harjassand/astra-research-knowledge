#!/usr/bin/env python3
"""Exact rational finite certificate, not a continuum proof or simulator."""
from fractions import Fraction as Q
from math import factorial, ceil
from pathlib import Path
import json


def enc(x):
    return {"numerator": x.numerator, "denominator": x.denominator,
            "approximate": float(x)}


def main():
    gamma, tau, gplus = Q(2, 5), Q(1, 50), Q(1, 5)
    pi_upper = Q(22, 7)
    assert pi_upper**2 < 10
    # C0^2<=16*(1+10/6)/24=16/9, so C0<=4/3.
    c0_upper = Q(4, 3)
    assert Q(16)*(1+Q(10, 6))/24 == c0_upper**2
    first_lower, second_upper = Q(167, 100), Q(74, 100)
    assert first_lower**2 < 3*(1-gamma/6) == Q(14, 5)
    assert second_upper**2 > c0_upper*gamma == Q(8, 15)
    ell_lower = first_lower-second_upper
    b0 = ell_lower**2/2
    assert b0 == Q(8649, 20000)
    emax = Q(64, 9)*10+4*gamma
    assert emax == Q(3272, 45)
    l0 = max(4, ceil(emax/gamma))
    assert l0 == 182 and gamma*l0 >= emax
    assert tau*emax < Q(3, 2)
    x = Q(3, 2)
    taylor = sum((x**k/Q(factorial(k)) for k in range(9)), Q(0))
    term9 = x**9/Q(factorial(9))
    # From term9 onward, the next-term ratio is at most x/10.
    exp_upper = taylor + term9/(1-x/10)
    assert exp_upper < Q(9, 2)
    assert pi_upper < Q(9, 5)**2
    z1_upper = Q(9, 4)
    d_lower = tau*gplus*b0*Q(2, 9)
    kappa_lower = d_lower/(gplus*z1_upper**2)
    payload = {
        "status": "FINITE-EVIDENCE: exact rational scalar certificate",
        "model": {"J": 1, "tau": enc(tau), "gplus": enc(gplus)},
        "L0": l0, "ell_lower": enc(ell_lower), "b0_lower": enc(b0),
        "Emax_upper": enc(emax), "exp_three_halves_upper": enc(exp_upper),
        "z1_upper": enc(z1_upper), "heat_secant_lower": enc(d_lower),
        "inverse_slope_lower": enc(kappa_lower),
        "checks_passed": True,
        "excluded_claims": ["General physical proof validated by this script",
                            "Useful full localizer n threshold",
                            "Many-body spectral acquisition executed",
                            "External mathematical validation"]}
    out = Path(__file__).with_name("inverse_certificate.json")
    out.write_text(json.dumps(payload, indent=2)+"\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
