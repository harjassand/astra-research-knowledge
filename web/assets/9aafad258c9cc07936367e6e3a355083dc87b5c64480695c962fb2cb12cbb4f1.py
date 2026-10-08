#!/usr/bin/env python3
"""Exact, dependency-free checks of the SOS-clock arithmetic-gate reductions.

Tests examples, not historical novelty or the external Hilbert-10 premise.
Run: python3 verify.py
"""
from fractions import Fraction as F
from random import Random
from math import sqrt

RNG = Random(20261008)


def integer_pair(q):
    assert isinstance(q, int)
    return max(q, 0) + 1, max(-q, 0) + 1


def rational_triple(q):
    q = F(q)
    w = F(1, 4 * (abs(q.numerator) + q.denominator))
    u, v = (1 + q * w) / 2, (1 - q * w) / 2
    assert 0 < u < 1 and 0 < v < 1 and 0 < w < 1
    assert (u - v) / w == q
    return u, v, w


def z_grad(z):
    return z * z + z - 1


def integer_residuals(vals, c):
    """Six gates: free a,b, product ab, sum ab+a, constant c, final sum."""
    q = [a-b for (a,b) in vals]
    return (
        q[2] - q[0]*q[1],
        q[3] - q[2] - q[0],
        q[4] - c,
        q[5] - q[3] - q[4],
        q[5],
    )


def rational_residuals(vals, c):
    u = [item[0] for item in vals]
    v = [item[1] for item in vals]
    w = [item[2] for item in vals]
    d = [u[i]-v[i] for i in range(6)]
    product = d[2]*w[0]*w[1] - w[2]*d[0]*d[1]
    addition = d[3]*w[2]*w[0] - w[3]*(d[2]*w[0]+d[0]*w[2])
    constant = d[4] - c*w[4]
    finaladd = d[5]*w[3]*w[4] - w[5]*(d[3]*w[4]+d[4]*w[3])
    outputzero = d[5]
    return product, addition, constant, finaladd, outputzero


def mobility(residuals):
    return sum((r*r for r in residuals), F(0))


def check_one_integer(a,b):
    c = -(a*b+a)
    q = [a,b,a*b,a*b+a,c,0]
    vals = [integer_pair(qi) for qi in q]
    rs = integer_residuals(vals,c)
    assert all(r == 0 for r in rs)
    assert mobility(rs) == 0
    # The other stationary alternative (z=z*) cannot have integral z:
    assert z_grad(1) == 1
    invalid = vals[:]
    invalid[5] = invalid[5][0]+1, invalid[5][1]
    rs2 = integer_residuals(invalid,c)
    assert mobility(rs2) > 0
    # For z=1, the flow's z component -M*(z²+z-1) is nonzero.
    assert -mobility(rs2)*z_grad(1) != 0


def check_one_rational(a,b):
    c = -(a*b+a)
    q = [a,b,a*b,a*b+a,c,F(0)]
    vals = [rational_triple(qi) for qi in q]
    rs = rational_residuals(vals,c)
    assert all(r == 0 for r in rs)
    assert mobility(rs) == 0
    assert z_grad(F(1,2)) == F(-1,4)
    invalid = vals[:]
    u,v,w = invalid[5]
    invalid[5] = (u+w/100,v,w)
    assert invalid[5][0] < 1
    rs2 = rational_residuals(invalid,c)
    assert mobility(rs2) > 0
    assert -mobility(rs2)*z_grad(F(1,2)) != 0


def check_monotonic_clock():
    """Explicit shared-clock base orbit for y and Riccati z, tested by steps."""
    target_z=(sqrt(5)-1)/2
    for start in (0.001,0.1,0.4,0.8,0.999):
        z=start
        y=start
        dt=0.0005
        for _ in range(20000):
            zz=z+dt*(1-z-z*z)
            yy=y+dt*(1-2*y)
            assert min(z,target_z)-1e-12 <= zz <= max(z,target_z)+1e-12
            assert min(y,0.5)-1e-12 <= yy <= max(y,0.5)+1e-12
            z,y=zz,yy
        assert abs(z-target_z)<1e-8 and abs(y-0.5)<1e-8


def main():
    for _ in range(600):
        a=RNG.randint(-20,20)
        b=RNG.randint(-20,20)
        check_one_integer(a,b)
        ar=F(RNG.randint(-100,100),RNG.randint(1,45))
        br=F(RNG.randint(-100,100),RNG.randint(1,45))
        check_one_rational(ar,br)
    check_monotonic_clock()
    assert z_grad(F(1)) == 1
    assert z_grad(F(0)) == -1
    print("PASS: 600 integer witnesses, 600 rational witnesses,")
    print("      1,200 deliberately perturbed nonstationary candidates,")
    print("      100,000 independent monotonic clock Euler steps,")
    print("      exact fractional gate equations and irrational-minimizer checks.")
    print("Degree bounds are analytic (residuals integer <=2, rational <=3);")
    print("the associated SOS and gradient degrees are 4/6 and 6/8.")
    print("NO external H10(Q), mass-action realization, or historical novelty check.")


if __name__ == "__main__":
    main()
