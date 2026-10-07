"""Exact finite diagnostics of the independently derived occupation inequality.

The mathematical proof is in weighted_capacity_proof.md. These diagnostics
check its algebra and degenerate limits; they do not replace the general proof.
Uses only Python standard-library rational arithmetic.
"""
from fractions import Fraction as Q
from itertools import product
import json


def F(x, a):
    return x*x+a*x+a*a/4


def check_one(lam, p, x, a):
    xp = p*x/(lam*lam)
    ap = lam*(a+(1-p)*x)
    energy = (1-lam**4)*xp*xp
    lhs = F(xp, ap)-F(x, a)
    rhs = -Q(3, 4)*(1-p)*x*x-Q(1, 2)*(1-p)*a*x+2*energy
    assert lhs <= rhs, (lam, p, x, a, lhs, rhs)
    b = a+(1-p)*x
    noise = p*p*(lam**-4-1)*x*x+p*(lam**-1-1)*x*b-Q(1, 4)*(1-lam*lam)*b*b
    assert F(xp, ap)-F(p*x, b) == noise
    exact_identity = -(1-p)*((1-Q(1, 4)*(1-p))*x*x+Q(1, 2)*a*x)
    assert F(p*x, b)-F(x, a) == exact_identity
    if lam != 1:
        assert (lam**-1-1)**2/(1-lam*lam) <= lam**-4-1
    return rhs-lhs


def main():
    ls = [Q(1, 10**6), Q(1, 1000), Q(1, 10), Q(1, 2), Q(9, 10),
          Q(999, 1000), Q(10**6-1, 10**6), Q(1)]
    ps = [Q(0), Q(1, 10**6), Q(1, 1000), Q(1, 10), Q(1, 3),
          Q(1, 2), Q(9, 10), Q(999, 1000), Q(10**6-1, 10**6), Q(1)]
    xs = [Q(0), Q(1, 1000), Q(1, 10), Q(1), Q(10), Q(1000)]
    aas = [Q(0), Q(1, 1000), Q(1, 10), Q(1), Q(10), Q(1000)]
    gaps = [check_one(*t) for t in product(ls, ps, xs, aas)]

    # Near-deterministic ray: positive transmission product, weighted telescoping.
    R = Q(1)
    E = Q(0)
    product_lam = Q(1)
    for n in range(1, 41):
        lam = 1-Q(1, 2**(n+1))
        old_R = R
        product_lam *= lam
        R *= lam*lam
        increment = (1-lam**4)/(R*R)
        assert increment == R**-2-old_R**-2
        E += increment
        assert E == R**-2-1
    # Product >= 1-sum mutation >=1/2, with strict first-order slack.
    assert product_lam > Q(1, 2)
    assert E < 15  # R=(product lambda)^2>1/4 => R^-2-1<15.

    # Deterministic channel contributes exactly zero energy; all p are legal.
    for p in ps:
        check_one(Q(1), p, Q(1), Q(2))

    # Degree-free y-subadditivity algebra on worst permitted cubic-saving input.
    c, K = Q(1, 1000), Q(1, 3000)
    for a, b in product([Q(i, 10) for i in range(31)], repeat=2):
        s = a+b-c*a*b*(a+b)
        y_s = s+K*s**3
        y_ab = a+K*a**3+b+K*b**3
        assert y_s <= y_ab

    report = {
        "status": "EXACT_FINITE_DIAGNOSTICS_PASSED",
        "occupation_rational_instances": len(gaps),
        "smallest_nonnegative_gap": str(min(gaps)),
        "degree_free_subadditivity_instances": 31**2,
        "near_deterministic_ray_depth": 40,
        "ray_transmission_product_decimal": float(product_lam),
        "ray_weighted_energy_decimal": float(E),
        "scope": "Exact algebra and boundary fixtures; not an independent general theorem certificate",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
